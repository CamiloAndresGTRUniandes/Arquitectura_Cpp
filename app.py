import subprocess
import time

subprocess.Popen(['python', './Consulta_inventario1/app.py'])
subprocess.Popen(['python', './Consulta_inventario2/app.py'])
subprocess.Popen(['python', './Ventas/app.py'])
time.sleep(5)
processes = [subprocess.Popen(['python', './Monitor/app.py'])]
for process in processes:
    process.wait()
