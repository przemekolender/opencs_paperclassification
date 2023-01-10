from elasticsearch import Elasticsearch



def _find_n_best(result, n: int, label_colname: str):
    results = []
    for i in range(n):
        results.append(
            {
                label_colname: result["hits"]["hits"][i]["_source"][label_colname],
                "score": result["hits"]["hits"][i]["_score"]
            }
        )
    return results

def find_n_best(es: Elasticsearch, index_name: str, query: str, n: int, label_colname: str='prefLabel'):
    res = es.search(index=index_name, body=query)
    return _find_n_best(res, n, label_colname)