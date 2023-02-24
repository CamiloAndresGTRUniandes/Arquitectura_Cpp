from flask import Blueprint, request, jsonify, Response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
import time
import json
import os
from models.models import \
    db, \
    Producto, ProductoSchema, \
    LogProducto,LogProductoSchema
from views.RabbitConnections import RabbitConnection

rabbitCon = RabbitConnection()
productoSchema = ProductoSchema()
logProductoSchema=LogProductoSchema()
# RabbitMQ connection details

#producir error

producirError=os.getenv("PRODUCE_ERROR")

class VistaSucriptorConsulta(Resource):
    def get(self):
        rabbitCon = RabbitConnection()
        rabbitCon.crearConexion()
        channel = rabbitCon.creacionCola(os.getenv("COLA_SERVICIO_CONSULTA"))
        # channel.queue_declare(queue='service1-consulta')
        def callback(ch, method, properties, body):
            # procesa el mensaje recibido aquí
            message = body  
            print(os.getenv("MENSAJE_RECIBIDO"), message)
            #Ejecutar consulta

        channel.basic_consume(queue=os.getenv("COLA_SERVICIO_CONSULTA"), on_message_callback=callback, auto_ack=True)
        print(f'Escuchando en la cola: {os.getenv("COLA_SERVICIO_CONSULTA")}')
        channel.start_consuming()
        return 'Suscrito a la cola'


class VistaProducto(Resource):
    def get(self, id):
       return productoSchema.dump(Producto.query.get_or_404(1))
    
class VistaLogProducto(Resource):
    def get(self, id):
     return logProductoSchema.dump(LogProducto.query.filter(LogProducto.nombreTransacion==id).all())
    
class VistaRetornaEstado(Resource):
   def get(self):
    if(producirError=='True'):
        t = time.localtime(time.time())
        segundos=  t.tm_sec
        #print("********Segundos*********");
        #print(segundos)
        #print("********Segundos*********");
        if(segundos%2==0):
            resp = Response(json.dumps('OK'), mimetype='application/json')
            resp.status_code = 200
            return resp
        else:
            resp = Response(json.dumps('OK'), mimetype='application/json')
            resp.status_code = 400
            return resp
    else:
            resp = Response(json.dumps('OK'), mimetype='application/json')
            resp.status_code = 200
            return resp