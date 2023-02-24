import pika
from views.RabbitConnections import RabbitConnection 
from models import db, Producto, LogProducto
import time
from datetime import datetime
import os
class ListenerServicioConsulta():
    def __init__(self):
      print("Contructor")  

    def listenerConsultaVentas(self):
      rabbitCon = RabbitConnection()
      rabbitCon.crearConexion()
      channel = rabbitCon.creacionCola(os.getenv("COLA_SERVICIO_CONSULTA"))
      # channel.queue_declare(queue='service1-consulta')
      def callback(ch, method, properties, body):
          # procesa el mensaje recibido aquí
          message = body
          #self.insertarLog(int(body))
          #p=LogProducto( idProducto = int(body), nombreTransacion=os.getenv("COLA_SERVICIO_CONSULTA"), fechaTransaccion=datetime.now()  )
          #db.session.add(p)
          #db.session.commit()
          print(os.getenv("MENSAJE_RECIBIDO"), message)
        #Ejecutar consulta

      channel.basic_consume(queue=os.getenv("COLA_SERVICIO_CONSULTA"), on_message_callback=callback, auto_ack=True)
      print(f'Escuchando en la cola: {os.getenv("COLA_SERVICIO_CONSULTA")}')
      channel.start_consuming()

    def insertarLog(self, idProducto):
        t = time.localtime(time.time())
        p=LogProducto( idProducto = idProducto, nombreTransacion=os.getenv("COLA_SERVICIO_CONSULTA")  )
        db.session.add(p)
        db.session.commit()