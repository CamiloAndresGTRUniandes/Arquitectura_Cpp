from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from datetime import datetime

db = SQLAlchemy()


class LogConsultaVenta(db.Model):
    __tablename__ = 'log_consulta_ventas'
    id = db.Column(db.Integer, primary_key=True)
    fechaTransaccion = db.Column(db.DateTime(), default=datetime.now())
    nombreTransacion = db.Column(db.String(128))
    idProducto = db.Column(db.Integer())
    cantidad = db.Column(db.Integer())
    precio = db.Column(db.Integer())

class LogConsultaVentaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = LogConsultaVenta
        load_instance = True