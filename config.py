from os import path



# paths
ENV_PATH = path.join(r"C:\Users\User\anaconda3\envs\sdp_env")
BASE_DIR = path.join(r"C:\Users\User\Desktop\SDP_project\opencs_paperclassification")
DATA_DIR = path.join(BASE_DIR, "data")
ONTOLOGY_DIR = path.join(r"D:\OpenCS\OpenCS")
ONTOLOGY_CORE_DIR = path.join(ONTOLOGY_DIR, r"ontology\core" )

# docker images
ES_IMAGE = "docker.elastic.co/elasticsearch/elasticsearch:7.12.1"
KB_IMAGE = "docker.elastic.co/kibana/kibana:7.12.1"

# containers
ES_CONTAINER_NAME = "opencs-pc-es"
KB_CONTAINER_NAME = "opencs-pc-kb"

ES_PORTS = {9200:9200, 9300:9300}
KB_PORTS = {5601:5601}

# docker network
NETWORK = 'elastic_net'
