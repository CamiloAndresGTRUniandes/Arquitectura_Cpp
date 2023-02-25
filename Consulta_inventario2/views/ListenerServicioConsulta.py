import json
import pika
from views.RabbitConnections import RabbitConnection
from models import Producto, LogProducto
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
import os


class ListenerServicioConsulta():
    def __init__(self):
      print("Constructor")

    def listenerConsultaVentas(self):
      rabbitCon = RabbitConnection()
      rabbitCon.crearConexion()
      channel = rabbitCon.creacionCola(os.getenv("COLA_SERVICIO_CONSULTA"))

      def callback(ch, method, properties, body):
          # procesa el mensaje recibido aquí
          message = body
          engine = create_engine('sqlite:///c:/sqllite/dbapp.sqlite')
          Session = sessionmaker(bind=engine)

          p = LogProducto(idProducto=int(body), nombreTransacion=os.getenv(
              "COLA_SERVICIO_CONSULTA"), fechaTransaccion=datetime.now())
          session = scoped_session(Session)
          productoBd = session.query(Producto).get(int(body))
          session.add(p)
          session.commit()

          print(os.getenv("MENSAJE_RECIBIDO"), message)
        # Ejecutar consulta
          producto = {'id': productoBd.id, 'nombre': productoBd.nombre,
                      'cantidad': productoBd.cantidad, 'precio': productoBd.precio}
          jsonData = json.dumps(producto)
          # Connect to RabbitMQ and send message to appropriate queue
          self.sender(jsonData)
          # Close connection to RabbitMQ
      channel.basic_consume(queue=os.getenv(
          "COLA_SERVICIO_CONSULTA"), on_message_callback=callback, auto_ack=True)
      print(f'Escuchando en la cola: {os.getenv("COLA_SERVICIO_CONSULTA")}')
      channel.start_consuming()

    def sender(self, data):
        connectionSend = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv("RABBITMQ_HOST"), port=os.getenv(
            "RABBITMQ_PORT"), credentials=pika.PlainCredentials(username=os.getenv("RABBITMQ_USERNAME"), password=os.getenv("RABBITMQ_PASSWORD"))))
        channelSend = connectionSend.channel()
        queue_name = os.getenv("COLA_RESPUESTA_VENTAS")
        channelSend.queue_declare(queue=queue_name)
        channelSend.basic_publish(
            exchange='', routing_key=queue_name, body=data)
        connectionSend.close()
