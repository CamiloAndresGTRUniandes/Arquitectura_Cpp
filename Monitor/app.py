from flask import Flask
from views import bp
import threading
from views.Monitor import Monitor
import pika
import time
import sys
import os
# print("----------------Temporal ventas-----------------------------")
# i=1
# while i<150:
#   try:
#     parameters=  pika.ConnectionParameters('127.0.0.1', 5672,'/',pika.PlainCredentials(username='yonathan', password='YonathanBr1983*'))
#     connection = pika.BlockingConnection(
#       parameters
#     )
#     channel = connection.channel()
#     channel.queue_declare(queue='peticion_ventas')
#     channel.basic_publish(exchange='', routing_key='peticion_ventas', body=f'{i}')
#     print(f' [x] Sent Hello World!  {i}'  )
#     connection.close()
#     i=i+1
#   except NameError:
#     print(NameError)
# print("----------------Fin ventas-----------------------------")
monitor= Monitor()
threadPeticionVentas = threading.Thread(name='suscriptor_peticion_ventas', target=monitor.suscriptor_peticion_ventas)
threadPeticionVentas.setDaemon(True)
threadPeticionVentas.start()
app = Flask(__name__)
app.register_blueprint(bp)
print('Hola Monitor')
app.run(port=5555)


