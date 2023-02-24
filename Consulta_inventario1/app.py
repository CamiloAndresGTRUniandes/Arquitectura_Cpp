from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from faker.generator import random
from models import db, Producto
from views import VistaProducto, VistaSucriptorConsulta,VistaRetornaEstado

app = Flask(__name__)
# app.register_blueprint(bp)
engine = create_engine('sqlite:///products.db')
Session = sessionmaker(bind=engine)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbapp.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()
db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
api.add_resource(VistaSucriptorConsulta, '/suscriptor-consulta')
api.add_resource(VistaProducto, '/producto/<int:id>')
api.add_resource(VistaRetornaEstado, '/respuesta-estado')

#Poblar bd

# with app.app_context():
#    i=0
#    data_factory = Faker()
#    totalProductos= Producto.query.count()
#    if totalProductos==0:
#      while i<500:
#         p=Producto( nombre = data_factory.name(), cantidad =  round(random.uniform(1, 9999), 0),  precio = round(random.uniform(1000, 9999999999), 2))
#         db.session.add(p)
#         db.session.commit()

if __name__ == '__main__':
    print('Orale')
    app.run(debug=True, port=9000)

