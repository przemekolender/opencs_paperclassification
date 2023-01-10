from rdflib import Graph, URIRef, Literal, BNode, TIME
from rdflib.namespace import RDF, XSD
import uuid
import datetime
from rdflib.namespace import Namespace
from config import RESULT_DIR
from os import path



def save_result_vocabulary(query, query_res, save_as_file=True):
    schema = Namespace("http://schema.org/")

    res_uuid = str(uuid.uuid4())
    g = Graph()

    g.bind("ocs", "https://w3id.org/ocs/ont/")
    g.bind("schema", schema)
    g.bind("rdf", RDF)
    g.bind("xsd", XSD)

    res = URIRef(f"http://example.org/result/{res_uuid}")

    query_literal = Literal(query)
    query_res_literal = Literal(query_res)
    end_time_literal = Literal(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'), datatype=XSD.date)

    g.add((res, RDF.type, schema.SearchAction))
    g.add((res, schema.query, query_literal))
    g.add((res, schema.result, query_res_literal))
    g.add((res, schema.endTime, end_time_literal))

    if save_as_file:
        dest_path = path.join(RESULT_DIR, f"{res_uuid}.ttl")
        g.serialize(dest_path, format="turtle")

    return str(g.serialize())
    