from abc import ABC, abstractmethod
from typing import List, Dict
from rdflib import Graph


class IIndexBuilder(ABC):

    def __init__(
        self,
        idx_colnames: Dict[str, str]
    ):
        self.idx_colnames = idx_colnames

    @abstractmethod
    def get_template(self, predicate_names: List[str]) -> Dict:
        pass

    @abstractmethod
    def build_rows(self) -> List[Dict]:
        pass
