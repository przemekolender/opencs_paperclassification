Topical paper classifier
============
Authors: Paweł Golik | Przemysław Olender
---

 The project was created during the Semantic Data Processing course at Warsaw University of Technology, Faculty of Mathematics and Information Science (2022/23 academic year).

---

## About

 The project aims to implement a tool to assign the best matching concepts from the [OpenCS ontology](https://github.com/OpenCS-ontology/OpenCS) to given scientific articles based on their title and abstract. Although the name contains the word 'classifier,' the task is unsupervised, and our solution employs the `Elastic Search` search engine. The output for each article is a ranking of related concepts (with scorings).

---

## Libraries

- [**Elastic Search**](https://www.elastic.co/enterprise-search): a distributed, free and open search and analytics engine for all types of data, including textual, numerical, geospatial, structured, etc.
- [**elasticsearch-py**](https://elasticsearch-py.readthedocs.io/en/v8.6.0/): official low-level client for Elasticsearch. Its goal is to provide common ground for all Elasticsearch-related code in Python.
- [**rdflib**](https://rdflib.readthedocs.io/en/stable/): RDFLib is a pure Python package for working with RDF. It contains parsers/serializers, graph interfaces and more.
- [**docker**](https://docs.docker.com/engine/api/sdk/#python-sdk): Python SDK for [Docker](https://docs.docker.com/) - an open platform for developing, shipping, and running applications.

---

## Setup
1. Clone this repo to your desktop.

2. Visit `config.py` to change the `BASE_PATH` constant - provide the absolute path to the `opencs_paperclassification` directory (e.g., `r"C:/Users/user/Desktop/opencs_paperclassification"`).
Change other config parameters if needed.

3. Create [**anaconda**](https://conda.io/projects/conda/en/latest/index.html) environment and install all dependencies (listed in the `environment.yml` file): Open Anaconda Prompt, then navigate to the `opencs_paperclassification` directory, and run `conda env create -f environment.yml --name <env_name>`.

4. If you have Elastic Search installed, you can move on to point number 5. If not, install Elastic Search on your computer or utilize our Docker containers providing a ready-to-use Elastic Search application. To learn more about setting up the environment for Elastic Search, please visit our `env_setup.ipynb` notebook for more details.

5. Make sure that Elastic Search is running and responding to requests. The default setting for the Elastic Search host build from our Docker solution is `http://localhost:9200`.

6. Clone (or download) the [OpenCS ontology](https://github.com/OpenCS-ontology/OpenCS). Provide a proper path for the ontology dir (`ONTOLOGY_DIR` in `config.py` file), e.g., `r"D:\OpenCS"`.

7. Build a new index. You can see our notebook `loading_data_and_building_index.py` to see a demo.

8. Make queries containing requested articles to get rankings of the OpenCS ontology concepts. Visit `querying_es.ipynb` for a demo.

---

### Configuration - `config.py` file

This file defines some configuration values used in the project. Please adjust the values if needed.

`paths` section defines absolute and relative paths.
- `ENV_PATH` - an absolute path to the conda environment. Used when installing docker SDK in  `env_setup.ipynb`.
- `BASE_DIR` - an absolute path to the `opencs_paperclassification` directory.
- `ONTOLOGY_DIR` - an absolute path to the `OpenCS` directory.
- `DATA_DIR` - a path to the directory containing input files (with articles) in .ttl format.
- `RESULT_DIR` - a path to the directory in which the results with rankings will be saved.
- `ONTOLOGY_CORE_DIR` - a path to the directory containing the .ttl files with ontology concepts.

`docker` section defines Docker configuration. These constants can be ignored if Elastic Search is not build from our Docker solution.
- `ES_IMAGE`, `KB_IMAGE` - Elastic Search and Kibana images. By default, we provided a baseline images. 
- `ES_CONTAINER_NAME`, `KB_CONTAINER_NAME` - names of the containers created from the images.
- `ES_PORTS`, `KB_PORTS` - ports used by Elastic Search and Kibana applications.
- `PORT` - the main port for ES (e.g. http://localhost:{`PORT`})
- `NETWORK` - docker network name

`Elastic Search index` section defines parameters regarding the ES index.
- `IDX_NAME` - name of the index. The name of the index does not need to be provided via configuration.
Feel free to set a different name directly in code.

---

## Documentation

The `source` directory contains all definitions of functions/classes used in the project.

- `data` defines utilities for reading input articles
- `ontology_parsing` stores functions used for ontology parsing, i.e, `.ttl` files reading/parsing and merging the graphs.
```python
from source.ontology_parsing.data_loading import get_all_concept_file_paths, get_graphs_from_files
from config import ONTOLOGY_CORE_DIR



 # reading files
files = get_all_concept_file_paths(ONTOLOGY_CORE_DIR)

# loading the files data into graphs with rdflib
graphs = get_graphs_from_files(files)  
```
- `env_setup` provides tools for creating Docker containers and connecting with the Elastic Search host.
```python
from config import IDX_NAME, PORT
from source.env_setup.setup import connect_elasticsearch

with connect_elasticsearch(es_config={'host': 'localhost', 'port': PORT}) as es:
    mappings = es.indices.get_mapping(index=IDX_NAME)
```
- `es_index` contains functions/classes used for index building. Classes implementing `IIndexBuilder` allows for creating different types of indices when passed to the `build_index` function.
```python
from source.es_index.IndexBaseline import IndexBaseline
from source.es_index.create_index import build_index
from config import IDX_NAME, PORT



pred_uri_to_idx_colname = {
    'http://www.w3.org/2004/02/skos/core#prefLabel': 'prefLabel',
    'http://www.w3.org/2004/02/skos/core#closeMatch': 'closeMatch',
    'http://www.w3.org/2004/02/skos/core#related': 'related',
    'http://www.w3.org/2004/02/skos/core#broader': 'broader'
}

index_builder = IndexBaseline(pred_uri_to_idx_colname, graphs, include_concept_type=True)

# assumes that elastic search is responding at localhost:{PORT}
build_index(index_builder, es_config={'host': 'localhost', 'port': PORT}, idx_name=IDX_NAME)

```
**IndexBaseline** implements **IIndexBuilder** and aims to build a baseline index, i. e., index where each column is defined as a predicate from the ontology. The `pred_uri_to_idx_colname` argument is a dictionary defining all columns - which predicates to use (their URIs and column names), the `graphs` are parsed ontology files by `rdflib`, and the `include_concept_type` determines whether to use a column corresponding to the type ('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'). The default is `False` because usually concept type literals (e.g., 'C111') are irrelevant for topical paper classification.

Note that `pred_uri_to_idx_colname` can be derived from the ontology automatically (using all present predicates as columns):
```python
from source.ontology_parsing.graph_utils import get_uri_to_colname_dict_from_ontology



pred_uri_to_idx_colname = get_uri_to_colname_dict_from_ontology(graphs)
```

**TO DO** TODO

### Querying the index

The `./source/es_index/query_index.py` file defines a `find_n_best` function, that provides `n` best results (concept names with scores) for a given `query`. 

```python
from source.es_index.query_index import find_n_best
from config import PORT

query = {'query': {
    "match": {"prefLabel" : a0['article_title']}
    }
}

with connect_elasticsearch(es_config={'host': 'localhost', 'port': PORT}) as es:
    res = find_n_best(es, IDX_NAME, query, n=10, label_colname='prefLabel')
```
`find_n_best` requires following arguments: elasticsearch client ('es'), name of the index to be queried ('IDX_NAME`), query, number of 'n' best concepts to be retrieved, name of the index column corresponding to the names of concepts ('label_colname').


A comprehensive guide for the ES queries can be found at: [ES docs](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-multi-match-query.html).
Different examples of queries can be found in our `querying_es.ipynb` notebook.


- `result_saving` defines utilities for saving the output rankings in a `.ttl` format.
```python
from source.result_saving.result_vocabulary import save_result_vocabulary



save_result_vocabulary(query, res)
```

---

## Sample input/output
TO DO


---
## Scripts
TO DO


