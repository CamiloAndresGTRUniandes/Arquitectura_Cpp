import requests

# Microservice endpoints
service1_endpoint = 'http://127.0.0.1:9000/respuesta-estado'
service2_endpoint = 'http://127.0.0.1:8888/respuesta-estado'

def check_microservices():
    # Check status of microservices
    service1_status = requests.get(service1_endpoint).status_code
    service2_status = requests.get(service2_endpoint).status_code
    
    # Determine which microservice to use
    if service1_status == 200:
        return 'service1'
    elif service2_status == 200:
        return 'service2'
    else:
        return None
