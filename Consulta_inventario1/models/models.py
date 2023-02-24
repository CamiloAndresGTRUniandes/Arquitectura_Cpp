from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()



class Producto(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    cantidad = db.Column(db.Integer)
    precio = db.Column(db.Integer)

class LogProducto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idProducto = db.Column(db.Integer())
    fechaTransaccion = db.Column(db.DateTime())
    nombreTransacion = db.Column(db.String(128))

class ProductoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Producto
        load_instance = True

class LogProductoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = LogProducto
        load_instance = True
