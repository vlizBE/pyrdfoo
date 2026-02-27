'''
DCMI Metadata Terms

Ontology documentation: https://www.dublincore.org/specifications/dublin-core/dcmi-terms/

Namespace: ``http://purl.org/dc/terms/``
'''

from .rdf import RDF, RDFType


class Location(RDF, frozen=True):
    '''
    A spatial region or named place.

    See also: https://www.dublincore.org/specifications/dublin-core/dcmi-terms/terms/Location/
    '''

    rdf_type: RDFType = "http://purl.org/dc/terms/Location"
