import pika
import uuid
import threading
from . import views
from django.http import HttpResponseBadRequest

class RabbitMessaging:
    def __init__(self, bet_queue, user_queue):
        print('Rabbit thread starting')

        self.internal_lock = threading.Lock()
        self.bet_queue = bet_queue
        self.user_queue = user_queue
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue=self.bet_queue, exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.queue_declare(queue=self.user_queue, exclusive=True)

        thread = threading.Thread(target=self.run)
        thread.setDaemon(True)
        thread.start()


    def updateUsers(self, body):
        response = None

        def on_response(self, ch, method, props, body):
            if self.corr_id == props.correlation_id:
                self.response = body

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=on_response,
            auto_ack=True)

        self.channel.basic_publish(
            exchange='',
            routing_key=self.user_queue,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=str(uuid.uuid4()),
                delivery_mode= 2,
            ),
            body=body)
        while response is None:
            self.connection.process_data_events()
        
        return response

    def callback(self, ch, method, properties, body):
        command = body.split(';')
        response = HttpResponseBadRequest('comando não reconhecido')

        if(command[0] == 'end_bet'):
            users = views.endBets(command[1], command[2])

            body = 'bet_end;' + command[1] + ';' + command[2] + ';'.join(map(str, users))

            response = self.updateUsers(body)

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