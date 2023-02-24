import subprocess
import requests
import time

subprocess.Popen(['python', './Ventas/app.py'])
subprocess.Popen(['python', './Consulta_inventario1/app.py'])
subprocess.Popen(['python', './Consulta_inventario2/app.py'])
time.sleep(5)
processes = [subprocess.Popen(['python', './Monitor/app.py'])]
for process in processes:
    process.wait()
