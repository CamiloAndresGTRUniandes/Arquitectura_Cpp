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
  
class VistaRetornaEstado(Resource):
   def get(self):
    if(producirError=='True'):
        t = time.localtime(time.time())
        segundos=  t.tm_sec

        if(segundos%2==0 or segundos%3==0 ):
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