from typing import List, Dict
from rdflib import Graph
from source.ed_index.IIndex import IIndex
import rdflib
from source.ontology_parsing.graph_utils import get_concepts_pref_labels



class IndexBaseline(IIndex):

    def __init__(
        self,
        pred_uri_to_idx_colnames: Dict[str, str],
        graphs: List[Graph],
        include_concept_type: bool=False,
        concept_type_uri: str='http://www.w3.org/1999/02/22-rdf-syntax-ns#type'
    ):
        idx_colnames = ['name']
        if include_concept_type: idx_colnames += ['type']
        idx_colnames += list(pred_uri_to_idx_colnames.values())

        super(IndexBaseline, self).__init__(idx_colnames)
        self.pred_uri_to_idx_colnames = pred_uri_to_idx_colnames
        self.graphs = graphs
        self.include_concept_type = include_concept_type
        self.concept_type_uri = concept_type_uri
        self.concept_pref_labels = get_concepts_pref_labels(graphs)

    def get_template(self) -> Dict:
        template = {
            "mappings": {
                "properties": {
                    pn: {"type": "text"} for pn in self.idx_colnames
                }
            }
        }
        return template

    def build_rows(self) -> Dict:
        rows = []
        for graph in self.graphs:
            data = { name: [] for name in list(self.pred_uri_to_idx_colnames.values()) }

            concept_type = None
            for index, (sub, pred, obj) in enumerate(graph):
                name = sub.split('/')[-1]
                
                if pred == rdflib.term.URIRef(self.concept_type_uri):
                    if self.include_concept_type:
                        concept_type = obj.split('#')[-1]
                    continue

                self._parse_pred(pred, obj, data)

            row = {}
            row.update({'name': name})

            if self.include_concept_type:
                row.update({'type': concept_type})

            row.update(**data)
            rows.append(row)
        return rows

    def _try_get_concept_pref_label(self, obj_str: str, concepts_pref_labels: Dict[str, str]):
        pref_label = None
        try:
            obj_name = obj_str.split('/')[-1]
            pref_label = concepts_pref_labels[obj_name]
        except:
            pass
        return pref_label

    def _parse_pred(self, pred, obj, data):
        if not str(pred) in self.pred_uri_to_idx_colnames: return
        pred_name = self.pred_uri_to_idx_colnames[str(pred)]
        pref_label = self._try_get_concept_pref_label(obj, self.concept_pref_labels)
        res = pref_label if pref_label != None else str(obj)
        data[pred_name].append(res)
         

