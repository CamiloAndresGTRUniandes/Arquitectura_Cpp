from flask import Flask
from views import bp
import time
import threading
from views.Monitor import Monitor

# monitor = Monitor()
# hiloListener = threading.Thread(monitor.suscriptor_peticion_ventas())

# hiloListener2 = threading.Thread(monitor.suscriptor_respuesta_consulta())
# hiloListener.start()
# time.sleep(5)
# hiloListener2.start()
# monitor.suscriptor_peticion_ventas()
# monitor.suscriptor_respuesta_consulta()

app = Flask(__name__)
app.register_blueprint(bp)
print('Hola Monitor')

if __name__ == '__main__':
    app.run(debug=True, port=5000)


