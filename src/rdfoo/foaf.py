'''
FOAF Vocabulary Specification 0.99

Ontology documentation: https://xmlns.com/foaf/spec/

Namespace: ``http://xmlns.com/foaf/0.1/``
'''

import rdflib

from .rdf import RDF, RDFType


class Agent(RDF, frozen=True):

    rdf_type: RDFType = "http://xmlns.com/foaf/0.1/Agent"

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        _, rdf_id = cls._node_id(id)
        return Agent(rdf_id=rdf_id)
