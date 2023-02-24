import subprocess
import requests
import time

subprocess.Popen(['python', './Ventas/app.py'])
subprocess.Popen(['python', './Consulta_inventario1/app.py'])

time.sleep(5)
processes = [subprocess.Popen(['python', './Monitor/app.py'])]
for process in processes:
    process.wait()

# monitor1_endpoint = 'http://localhost:5000/suscriptor-respuesta-consulta'
# monitor2_endpoint = 'http://localhost:5000/suscriptor-peticion-ventas'
# consulta1_endpoint = 'http://localhost:9000/suscriptor-consulta'
# requests.get(monitor1_endpoint).status_code
# requests.get(monitor2_endpoint).status_code
# requests.get(consulta1_endpoint).status_code