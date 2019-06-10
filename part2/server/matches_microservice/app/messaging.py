import pika
import uuid
import threading
from . import views
from django.http import HttpResponseBadRequest

class RabbitMessaging:

    def callback(self, ch, method, properties, body):
        command = body.split(';')
        response = HttpResponseBadRequest('comando não reconhecido')
        print('AQUI')
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