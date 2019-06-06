import pika
import views

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='user_queue', durable=True)
channel.queue_declare(queue='bet_queue', durable=True)
channel.queue_declare(queue='match_queue', durable=True)

# Estava a pensar que a mensagem seria algo tipo servicoqueenviou;comando;argumentos

def callback(ch, method, properties, body):
    command = properties.split(';')



    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='user_queue', on_message_callback=callback)

channel.start_consuming()