import pika
import uuid
import threading
from . import views
from django.http import HttpResponseBadRequest

class RabbitMessaging:
    def __init__(self, queue):
        self.internal_lock = threading.Lock()
        self.queue = queue
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue=self.queue, exclusive=True)
        self.callback_queue = result.method.queue

        thread = threading.Thread(target='run')
        thread.setDaemon(True)
        thread.start()


    def callback(self, ch, method, properties, body):
        command = body.split(';')
        response = HttpResponseBadRequest('comando não reconhecido')
        
        if(command[0] == 'bet_end'):
            response = views.cUserView(command[1], command[2], command[3], command[4], command[5], command[6], command[7])
            
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
        self.channel.basic_consume(queue=self.queue, on_message_callback='callback')

        self.channel.start_consuming()


if __name__ == '__main__':
    rabbit = RabbitMessaging('user_queue')