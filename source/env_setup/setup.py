import docker
from config import *
from typing import List, Dict
from elasticsearch import Elasticsearch



def start_docker_containers() -> List[docker.models.containers.Container]:
    client = docker.from_env()
    pull_images(client, ES_IMAGE, KB_IMAGE)

    # create a network so kibana can find elastic
    create_docker_network(client, NETWORK)

    containers = []
    es_container = start_es_container(client, ES_IMAGE, ES_CONTAINER_NAME, NETWORK, ES_PORTS)
    containers.append(es_container)

    local_host_port = list(ES_PORTS.keys())[0]
    env = {'ELASTICSEARCH_HOSTS': f'http://{ES_CONTAINER_NAME}:{local_host_port}'}
    kb_container = start_kb_container(client, KB_IMAGE, KB_CONTAINER_NAME, NETWORK, env, KB_PORTS)
    containers.append(kb_container)

    return containers

def stop_docker_containers(containers: List[docker.models.containers.Container]):
    for container in containers:
        container.stop()


def remove_docker_containers(containers: List[docker.models.containers.Container]):
    for container in containers:
        container.stop()
        container.remove()

def pull_images(client: docker.DockerClient, es_image: str, kb_image: str):
    # pull elasticsearch
    image = client.images.pull(es_image)
    print(image)

    # pull kibana
    image = client.images.pull(kb_image)
    print(image)

def create_docker_network(client: docker.DockerClient, network_name: str):
    try:
        client.networks.create(name=network_name, check_duplicate=True)
    except docker.errors.APIError as e:
        client.networks.get(network_name).remove()
        client.networks.create(network_name)


def start_es_container(client: docker.DockerClient, image: str, container_name: str, network: str, ports: dict):
    container = client.containers.run(
        image=image,
        environment={'discovery.type': 'single-node'},
        name=container_name,
        ports=ports,
        network=network,
        detach=True)
    container.logs()

    return container

def start_kb_container(client: docker.DockerClient, image: str, container_name: str, network: str, environment: dict,
                       ports: dict):
    container = client.containers.run(
        image=image,
        name=container_name,
        environment=environment,
        ports=ports,
        network=network,
        detach=True)
    container.logs()

    return container

def connect_elasticsearch(es_config: Dict[str, str]={'host': 'localhost', 'port': 9200}):
    _es = None
    _es = Elasticsearch([es_config])
    if _es.ping():
        print('Yay Connected')
    else:
        print('Awww it could not connect!')
    return _es
