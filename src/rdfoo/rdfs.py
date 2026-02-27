'''
RDF Schema 1.1
'''

from rdfoo.rdf import RDF, RDFType


class Resource(RDF, frozen=True):
    '''
    The class resource, everything.

    See also: https://www.w3.org/TR/rdf-schema/#ch_resource
    '''

    rdf_type: RDFType = "https://www.w3.org/2000/01/rdf-schema#Resource"
