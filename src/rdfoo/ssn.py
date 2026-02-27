'''
Semantic Sensor Network Ontology

Ontology documentation: https://www.w3.org/TR/vocab-ssn/

Namespace for SSN terms: ``http://www.w3.org/ns/ssn/``

Namespace for SOSA terms: ``http://www.w3.org/ns/sosa/``
'''

from typing import Annotated

from .rdf import RDF, RDFType


class Property(RDF, frozen=True):
    '''
    A quality of an entity. An aspect of an entity that is intrinsic to and
    cannot exist without the entity.
    '''

    rdf_type: RDFType = "http://www.w3.org/ns/sosa/Property"

    label: Annotated[
        str,
        {"rdf_property": "http://www.w3.org/2000/01/rdf-schema#label"},
    ]

    description: Annotated[
        str | None,
        {"rdf_property": "http://purl.org/dc/terms/description"},
    ] = None
