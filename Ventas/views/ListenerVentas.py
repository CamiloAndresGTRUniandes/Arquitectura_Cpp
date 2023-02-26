import json
import pika
from views.RabbitConnections import RabbitConnection
from models import LogConsultaVenta
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
import os

class ListenerVentas():
    def __init__(self):
      print("Constructor")

    def listenerVentas(self):
        rabbitCon = RabbitConnection()
        rabbitCon.crearConexion()
        channel = rabbitCon.creacionCola(os.getenv("COLA_RESPUESTA_VENTAS")) 
        def callback(ch, method, properties, body):
            # procesa el mensaje recibido aquí
            message = body
            jsonData= json.loads(message)
            engine = create_engine('sqlite:///c:/sqllite/dbapp.sqlite')
            Session = sessionmaker(bind=engine)
            print(os.getenv("MENSAJE_RECIBIDO"), message)
            p = LogConsultaVenta(idProducto=jsonData['id'], nombreTransacion=os.getenv(
              "COLA_RESPUESTA_VENTAS"), fechaTransaccion=datetime.now(),cantidad = jsonData['cantidad'], precio = jsonData['precio'])
            session = scoped_session(Session)
            session.add(p)
            session.commit()
            print(f'Consulta realizada con éxito para el producto con id: {jsonData["id"]}')
        channel.basic_consume(queue=os.getenv(
          "COLA_RESPUESTA_VENTAS"), on_message_callback=callback, auto_ack=True)
        print(f'Escuchando en la cola: {os.getenv("COLA_RESPUESTA_VENTAS")}')
        channel.start_consuming()
        return 'Suscrito a la cola'
    
    def publicaMensajes(self):
        i=1
        while i<=10000:
            parameters=  pika.ConnectionParameters('127.0.0.1', 5672,'/',pika.PlainCredentials(username='guest', password='guest'))
            connection = pika.BlockingConnection(
              parameters
            )
            channel = connection.channel()
            channel.queue_declare(queue='peticion_ventas')
            channel.basic_publish(exchange='', routing_key='peticion_ventas', body=f'{i}')
            print(f' [x] Consulta producto id: {i}'  )
            connection.close()
            i=i+1

    
