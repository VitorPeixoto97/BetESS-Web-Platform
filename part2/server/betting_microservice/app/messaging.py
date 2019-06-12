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

        self.channel.basic_publish(
            exchange='',
            routing_key=self.user_queue,
            properties=pika.BasicProperties(
                delivery_mode= 2,
            ),
            body=body)

    def user_callback(self, ch, method, properties, body):
        print('confirmação de user_queue')

    def callback(self, ch, method, properties, body):
        # recebe mensagem
        print('mensagem recebida: ' + body.decode("utf-8"))
        command = body.decode("utf-8").split(';')

        # efetua comando da mensagem
        if(command[0] == 'bet_end'):
            users = views.endBets(int(command[1]), int(command[2]), command[3], command[4]) # event, result, equipaC vs equipaF
            
            print('users = ' + str(len(users)))
            if(len(users) > 0):
                body = body = 'bet_end' + ';' + ','.join(map(str, users)) # bet_end;users

                # envia comando de update a users
                self.updateUsers(body)

        else: print('comando não reconhecido')

        ch.basic_ack(delivery_tag = method.delivery_tag)

    def run(self):
            self.channel.basic_qos(prefetch_count=1)
            self.channel.basic_consume(queue=self.bet_queue, on_message_callback=self.callback)

            try: 
                self.channel.start_consuming()
            except KeyboardInterrupt:
                self.channel.stop_consuming()

def send_message(message, user_queue='user_queue'):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))

    channel = connection.channel()

    channel.queue_declare(queue=user_queue, durable=True)

    channel.basic_publish(
        exchange='',
        routing_key=user_queue,
        properties=pika.BasicProperties(
            delivery_mode = 2, # make message persistent
        ),
        body=message)
