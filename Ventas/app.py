from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import pika
import sys
import os
from models import LogConsultaVenta
from models import db
import threading
from  views.ListenerVentas import ListenerVentas

load_dotenv()
app = Flask(__name__)

engine = create_engine('sqlite:///c:/sqllite/dbapp.sqlite')
Session = sessionmaker(bind=engine)
listenerVenta=  ListenerVentas()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///c:/sqllite/dbapp.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()
db.init_app(app)
db.create_all()
#############################
#Borra el log
with app.app_context():
    db.session.query(LogConsultaVenta).delete()
    db.session.commit()


threadServicioPublicar =  threading.Thread(name=os.getenv("COLA_RESPUESTA_VENTAS"), target=listenerVenta.publicaMensajes)
threadServicioConsulta = threading.Thread(name=os.getenv("COLA_VENTA"), target=listenerVenta.listenerVentas)
threadServicioConsulta.setDaemon(True)
threadServicioPublicar.setDaemon(True)
threadServicioConsulta.start()
threadServicioPublicar.start()

app = Flask(__name__)

print('Hola Monitor')
app.run(port=4444)