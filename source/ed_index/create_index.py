from typing import Dict
from source.ed_index.IIndex import IIndex
from elasticsearch import Elasticsearch
import requests 
import json



def connect_elasticsearch(es_config: Dict[str, str]={'host': 'localhost', 'port': 9200}):
    _es = None
    _es = Elasticsearch([])
    if _es.ping():
        print('Yay Connected')
    else:
        print('Awww it could not connect!')
    return _es

def store_record(es_object, index, data):
    is_stored = True

    try:
        outcome = es_object.index(index=index, doc_type='_doc', body=json.dumps(data))
        print(outcome)
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))
        is_stored = False
    finally:
        return is_stored

def build_index(index_builder: IIndex, es_config: Dict[str, str]={'host': 'localhost', 'port': 9200}, idx_name: str='ontology'):
    try:
        template = index_builder.get_template()
        create_index(str(template), idx_name)
        rows = index_builder.build_rows()

        es = connect_elasticsearch(es_config)
        for row in rows:
            store_record(es, idx_name, row)
            
    except Exception as e:
        print(str(e))
    finally:
        es.close()


def create_index(template: str, es_config: Dict[str, str]={'host': 'localhost', 'port': 9200}, idx_name: str='ontology'):

    query = json.loads(template)
    response = requests.put(f'http://{es_config["host"]}:{es_config["port"]}/{idx_name}', json=query)
    response.json()

