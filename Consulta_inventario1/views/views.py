from flask import Blueprint, request, jsonify, Response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
import json
from models import \
    db, \
    Producto, ProductoSchema, \
    LogProducto,LogProductoSchema
from views.RabbitConnections import RabbitConnection

rabbitCon = RabbitConnection()
productoSchema = ProductoSchema()
logProductoSchema=LogProductoSchema()
# RabbitMQ connection details


class VistaSucriptorConsulta(Resource):
    def get(self):
        rabbitCon.crearConexion()
        
        channel = rabbitCon.creacionCola('service1-consulta')

        # channel.queue_declare(queue='service1-consulta')

        def callback(ch, method, properties, body):
            # procesa el mensaje recibido aquí
            message = body
            print("Mensaje recibido por consulta 1: ", message)
            #Ejecutar consulta


        channel.basic_consume(queue='service1-consulta', on_message_callback=callback, auto_ack=True)

        print('Escuchando en la cola: service1-consulta')
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
    resp = Response(json.dumps('OK'), mimetype='application/json')
    resp.status_code = 200
    return resp

