import pika
import sys
import os
#, username="yonathan", password="YonathanBr1983*"
print("Hello")
i=1
while i<30:
  try:
    parameters=  pika.ConnectionParameters('127.0.0.1', 5672,'/',pika.PlainCredentials(username='yonathan', password='YonathanBr1983*'))
    connection = pika.BlockingConnection(
      parameters
    )
    channel = connection.channel()
    channel.queue_declare(queue='peticion_ventas')
    channel.basic_publish(exchange='', routing_key='peticion_ventas', body=f'{i}')
    print(f' [x] Sent Hello World!  {i}'  )
    connection.close()
    i=i+1
  except NameError:
    print(NameError)