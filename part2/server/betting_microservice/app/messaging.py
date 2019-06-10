import pika
import uuid
import threading
from . import views
from django.http import HttpResponseBadRequest

class RabbitMessaging:
    def __init__(self, bet_queue='bet_queue', user_queue='user_queue'):
        print('Rabbit thread starting')

        self.internal_lock = threading.Lock()
        self.bet_queue = bet_queue
        self.user_queue = user_queue
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue=self.bet_queue, durable=True)
        self.bet_callback_queue = result.method.queue

        result = self.channel.queue_declare(queue=self.user_queue, durable=True)
        self.user_callback_queue = result.method.queue

        thread = threading.Thread(target=self.run)
        thread.setDaemon(True)
        thread.start()


    def updateUsers(self, body):
        response = None

        self.channel.basic_consume(
            queue=self.user_callback_queue,
            on_message_callback=print('confirmação de user_queue'),
            auto_ack=True)

        self.channel.basic_publish(
            exchange='',
            routing_key=self.user_queue,
            properties=pika.BasicProperties(
                reply_to=self.user_callback_queue,
                correlation_id=str(uuid.uuid4()),
                delivery_mode= 2,
            ),
            body=body)
        while response is None:
            self.connection.process_data_events()
        
        return response

    def callback(self, ch, method, properties, body):
        # recebe mensagem
        print('mensagem recebida: ' + body)
        command = body.split(';')

        # efetua comando da mensagem
        if(command[0] == 'bet_end'):
            users = views.endBets(int(command[1]), int(command[2]), command[3], command[4]) # event, result, equipaC vs equipaV

            body = 'bet_end' + ';'.join(map(str, users)) # bet_end;users

            # envia comando de update a users
            response = self.updateUsers(body)

        
        # responde ao matches
        self.channel.basic_publish(exchange='',
            routing_key= properties.reply_to,
            body=response,
            properties=pika.BasicProperties(
                correlation_id=properties.correlation_id,
                delivery_mode = 2, # make message persistent
            ))

        ch.basic_ack(delivery_tag = method.delivery_tag)

    def run(self):
            self.channel.basic_qos(prefetch_count=1)
            self.channel.basic_consume(queue=self.bet_queue, on_message_callback=self.callback)

            self.channel.start_consuming()