from flask import Flask
from views import bp
import threading
from views.Monitor import Monitor
import pika
import time
import sys
import os

monitor= Monitor()
threadPeticionVentas = threading.Thread(name='suscriptor_peticion_ventas', target=monitor.suscriptor_peticion_ventas)
threadPeticionVentas.setDaemon(True)
threadPeticionVentas.start()
app = Flask(__name__)
app.register_blueprint(bp)
print('Hola Monitor')
app.run(port=5555)


