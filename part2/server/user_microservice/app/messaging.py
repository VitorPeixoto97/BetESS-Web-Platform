import pika
import uuid
import threading
from . import views
from django.http import HttpResponseBadRequest
from decimal import Decimal, ROUND_HALF_UP

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
        print('Mensagem recebida em user_queue: ' + body.decode("utf-8"))
        command = body.decode("utf-8").split(';')

        # update de vencedores de apostas
        if(command[0] == 'bet_end'):
            users = command[1].split(',')
            for user in users:
                userdata = user.split('-')
                views.updateCoins(int(userdata[0]), Decimal(userdata[1]).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)) #id, coins
            
        # update de aposta efetuada
        elif(command[0] == 'bet_made'):
            views.updateCoins(int(command[1]), -Decimal(command[2]).quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
        
        # update de aposta cancelada
        elif(command[0] == 'bet_cancel'):
            views.updateCoins(int(command[1]), Decimal(command[2]).quantize(Decimal('.01'), rounding=ROUND_HALF_UP))

        else: print('comando não reconhecido')

        ch.basic_ack(delivery_tag = method.delivery_tag)
        

    def run(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.queue, on_message_callback=self.callback)

        try: 
           self.channel.start_consuming()
        except KeyboardInterrupt:
           self.channel.stop_consuming()