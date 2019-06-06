import pika
import views

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='user_queue', durable=True)
channel.queue_declare(queue='bet_queue', durable=True)
channel.queue_declare(queue='match_queue', durable=True)

def callback(ch, method, properties, body):
    command = properties.split(';')
    
    if(command[1] == 'register'):
        response = views.userView(command[2], command[3], command[4], command[5], command[6], command[7])
        
    elif(command[1] == 'login'):
        response = 

    elif(command[1] == 'change_coins'):
        
    channel.basic_publish(exchange='',
                      routing_key= command[0] + '_queue',
                      body=response,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))

    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='user_queue', on_message_callback=callback)

channel.start_consuming()