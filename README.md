# Arquitectura_Cpp

Flujo desde el consumo por parte del componente de ventas hasta la respuesta.

1. Componente ventas realiza solicitud.
2. Monitor recibe la petición, hace un check de los servicios de consulta(request http para validar el estado del servicio) y escoge a que cola enviar el mensaje.
3. El componente de consulta que procesa la solicitud hace la consulta en base de datos, inserta el log y envía la respuesta a la cola respuesta_ventas.
4. El componente de ventas lee la cola respuesta_ventas con la respuesta de la solicitud e inserta un log con la respuesta recibida.

Para la ejecución del experimento se debe contar con un equipo con sistema operativo windows y la carpeta sqllite en el disco local c donde se encuentre el archivo dbapp.sqlite que se encuentra en la raiz del proyecto adicional  una instancia de rabbitMQ que puede ser instalada en docker de la siguinte forma:
1. Se debe tener Docker instalado en la máquina local. Si aún no lo tiene, puede descargarlo e instalarlo desde la página oficial de Docker: https://docs.docker.com/get-docker/.

2. A continuación, se debe abrir la línea de comandos de la terminal y ejecutar el siguiente comando para descargar la imagen oficial de RabbitMQ desde Docker Hub:

docker pull rabbitmq

3. Una vez que se haya descargado la imagen, se puede crear un contenedor con el siguiente comando:

docker run -d --name rabbitmq-container -p 5672:5672 -p 15672:15672 rabbitmq

Este comando creará un contenedor llamado "rabbitmq-container" a partir de la imagen descargada. La opción "-d" indica que el contenedor se ejecutará en segundo plano. Los puertos "5672" y "15672" son los puertos predeterminados para RabbitMQ, y se están mapeando a los mismos puertos en el host para que se puedan acceder a través de ellos.

4. Una vez que el contenedor esté en ejecución, se puede verificar si RabbitMQ se está ejecutando correctamente y acceder a su panel de control a través del navegador web. Para hacer esto, se debe abrir un navegador y visitar la URL "http://localhost:15672". Se le pedirá que inicie sesión, y las credenciales predeterminadas son "guest" para el nombre de usuario y la contraseña.

Para finalizar la ejecución del proyecto se realiza corriendo el comando python app.py estando ubicado dentro de la carpeta raiz.

Las librerias necesarias para correr el proyecto son:

aniso8601
click
colorama
coverage
Faker=
Flask
Flask-Cors
Flask-JWT
Flask-JWT-Extended
Flask-RESTful
Flask-SQLAlchemy
greenlet
itsdangerous
Jinja2
MarkupSafe
marshmallow
marshmallow-sqlalchemy
PyJWT
pytz
six
SQLAlchemy
Werkzeug
pika
dotenv
request

y pueden ser instaladas por medio del comando pip install -r requirements.txt
