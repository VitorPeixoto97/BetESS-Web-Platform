import pika
import uuid
import threading
from django.http import HttpResponseBadRequest

def send_message(message, bet_queue='bet_queue'):
    bet_queue = bet_queue
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))

    channel = connection.channel()

    result = channel.queue_declare(queue=bet_queue, durable=True)
    callback_queue = result.method.queue

    channel.basic_consume(
        queue=callback_queue,
        on_message_callback=print('confirmação de bet_queue'),
        auto_ack=True)

    corr_id = str(uuid.uuid4())        
    channel.basic_publish(
        exchange='',
        routing_key=bet_queue,
        properties=pika.BasicProperties(
            reply_to=callback_queue,
            correlation_id=corr_id,
            delivery_mode = 2, # make message persistent
        ),
        body=message)
