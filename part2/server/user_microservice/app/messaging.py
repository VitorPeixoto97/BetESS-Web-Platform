import pika
import uuid
import threading
from . import views
from django.http import HttpResponseBadRequest
from decimal import Decimal

class RabbitMessaging:
    def __init__(self, queue):
        print('Rabbit thread starting')

        self.internal_lock = threading.Lock()
        self.queue = queue
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue=self.queue, durable=True)
        self.callback_queue = result.method.queue

        thread = threading.Thread(target=self.run)
        thread.setDaemon(True)
        thread.start()


    def callback(self, ch, method, properties, body):
        # recebe mensagem
        print('Mensagem recebida em user_queue')
        command = body.split(';')

        # update de vencedores de apostas
        if(command[0] == 'bet_end'):
            users = command[1].split(',')
            for user in users:
                userdata = user.split('-')
                views.updateCoins(int(userdata[0]), Decimal(userdata[1]), max_digits=10, decimal_places=2) #id, coins
            
        self.channel.basic_publish(exchange='',
                        routing_key= properties.reply_to,
                        body='confirmação de user_queue',
                        properties=pika.BasicProperties(
                            correlation_id=properties.correlation_id,
                            delivery_mode = 2, # make message persistent
                        ))

        ch.basic_ack(delivery_tag = method.delivery_tag)
        

    def run(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.queue, on_message_callback=self.callback)

        self.channel.start_consuming()