'''
FOAF Vocabulary Specification 0.99

Ontology documentation: https://xmlns.com/foaf/spec/

Namespace: ``http://xmlns.com/foaf/0.1/``
'''


from .rdf import RDF, RDFType


class Agent(RDF, frozen=True):

    rdf_type: RDFType = "http://xmlns.com/foaf/0.1/Agent"
