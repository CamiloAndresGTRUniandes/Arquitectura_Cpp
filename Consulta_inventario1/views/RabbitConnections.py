import pika

class RabbitConnection():
    def __init__(self):
        self.rabbitmq_host = 'localhost'
        self.rabbitmq_port = 5672
        self.rabbitmq_username = 'guest'
        self.rabbitmq_password = 'guest'
        self.connection = None
        self.callback=None
    def crearConexion(self):
        parameters = pika.ConnectionParameters(
            self.rabbitmq_host, self.rabbitmq_port, '/', pika.PlainCredentials(username=self.rabbitmq_username, password=self.rabbitmq_password))
        self.connection = pika.BlockingConnection(parameters)
        return self.connection

    def creacionCola(self, cola):
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=cola)
        return self.channel
    
    def enviarMensaje(self, cola, mensaje):
        self.channel.basic_publish(
            exchange='', routing_key=cola, body=f'{mensaje}')
        print(f' Consulta1 envia   {mensaje}')
        self.cerrarConexion()
        
    def cerrarConexion(self):
        self.channel.stop_consuming()
        self.connection.close()

    def crearListener(self, cola):
        #self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=cola, on_message_callback=self.callback, auto_ack=False)
        self.channel.start_consuming()