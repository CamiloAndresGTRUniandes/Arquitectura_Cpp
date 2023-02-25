from flask import Blueprint, request, jsonify
import pika
import time
from models.models import check_microservices

bp = Blueprint('api', __name__)

class Monitor():
    def __init__(self):
        # RabbitMQ connection details
        self.rabbitmq_host = '127.0.0.1'
        self.rabbitmq_port = 5672
        self.rabbitmq_username = 'guest'
        self.rabbitmq_password = 'guest'

    def suscriptor_peticion_ventas(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmq_host, port=self.rabbitmq_port, credentials=pika.PlainCredentials(username=self.rabbitmq_username, password=self.rabbitmq_password)))
        channel = connection.channel()

        channel.queue_declare(queue='peticion_ventas')

        def callback(ch, method, properties, body):
            # procesa el mensaje recibido aquí
            message = body
            time.sleep(0.1)
            print("Mensaje recibido: ", message)
            # Check status of microservices
            service = check_microservices()

            if service is not None:
                # Connect to RabbitMQ and send message to appropriate queue
                connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmq_host, port=self.rabbitmq_port, credentials=pika.PlainCredentials(username=self.rabbitmq_username, password=self.rabbitmq_password)))
                channel = connection.channel()
                queue_name = f'{service}-consulta'
                channel.queue_declare(queue=queue_name)
                channel.basic_publish(exchange='', routing_key=queue_name, body=message)
                connection.close()

                print(f'Message enviado a {service}-consulta')
            else:
                print('error: No available microservices to process message')

        channel.basic_consume(queue='peticion_ventas', on_message_callback=callback, auto_ack=True)

        print('Escuchando en la cola: peticion_ventas')
        channel.start_consuming()
        
        return 'Suscrito a la cola peticion_ventas'
    

    def suscriptor_respuesta_consulta(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.rabbitmq_host))
        channel = connection.channel()

        channel.queue_declare(queue='respuesta_consulta')

        def callback(ch, method, properties, body):
            # procesa el mensaje recibido aquí
            message = body
            print("Mensaje recibido: ", message)
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmq_host, port=self.rabbitmq_port, credentials=pika.PlainCredentials(username=self.rabbitmq_username, password=self.rabbitmq_password)))
            channel = connection.channel()
            queue_name = f'respuesta_ventas'
            channel.queue_declare(queue=queue_name)
            channel.basic_publish(exchange='', routing_key=queue_name, body=message)
            connection.close()
            print(f'Message sent to {queue_name}')

        channel.basic_consume(queue='respuesta_consulta', on_message_callback=callback, auto_ack=True)

        print('Escuchando en la cola: respuesta_consulta')
        channel.start_consuming()

        return 'Suscrito a la cola respuesta consulta'
