'''
RDF Schema 1.1
'''

import rdflib

from .rdf import RDF, RDFType


class Resource(RDF, frozen=True):
    '''
    The class resource, everything.

    See also: https://www.w3.org/TR/rdf-schema/#ch_resource
    '''

    rdf_type: RDFType = "https://www.w3.org/2000/01/rdf-schema#Resource"

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        _, rdf_id = cls._node_id(id)
        return Resource(rdf_id=rdf_id)
