from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from views import ListenerServicioConsulta
from views import VistaRetornaEstado
from models import db, LogProducto
import threading
from dotenv import load_dotenv
import os
load_dotenv()
app = Flask(__name__)

engine = create_engine('sqlite:///dbapp.db')
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
api.add_resource(VistaRetornaEstado, '/respuesta-estado')

#Borra el log
with app.app_context():
    db.session.query(LogProducto).delete()
    db.session.commit()

#Daemons

listenerServicioConsulta=  ListenerServicioConsulta()
threadServicioConsulta = threading.Thread(name=os.getenv("COLA_suscriptor_peticion_ventas"), target=listenerServicioConsulta.listenerConsultaVentas)
threadServicioConsulta.setDaemon(True)
threadServicioConsulta.start()

if __name__ == '__main__':
    print(os.getenv("COLA_suscriptor_peticion_ventas"))
    app.run(debug=True, port=int(os.getenv("PORT")))