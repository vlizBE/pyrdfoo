'''
vCard Ontology - for describing People and Organizations

Ontology documentation: https://www.w3.org/TR/vcard-rdf/

Namespace: ``http://www.w3.org/2006/vcard/ns#``
'''

import rdflib
from typing import Annotated

from .rdf import RDF, RDFRef, RDFType


class Kind(RDF, frozen=True):
    '''
    The parent class for all objects.
    '''

    rdf_type: RDFType = "http://www.w3.org/2006/vcard/ns#Kind"

    fn: Annotated[
        str,
        {"rdf_property": "http://purl.org/dc/terms/description"},
    ]
    '''Full name.'''

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        node, rdf_id = cls._node_id(id)
        fn = graph.value(node, rdflib.URIRef("http://www.w3.org/2006/vcard/ns#Kind"))
        return Kind(
            rdf_id=rdf_id,
            fn=str(fn),
        )


class Group(Kind, frozen=True):
    '''
    Object representing a group of persons or entities. A group object will
    usually contain `has_member` properties to specify the members of the group.
    '''

    rdf_type: RDFType = "http://www.w3.org/2006/vcard/ns#Group"

    has_member: list[RDFRef["Individual | Organization"]]

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        kind = Kind.from_graph(id, graph)
        return Group(**kind.model_dump())


class Individual(Kind, frozen=True):
    '''
    An object representing a single person or entity.
    '''

    rdf_type: RDFType = "http://www.w3.org/2006/vcard/ns#Individual"

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        kind = Kind.from_graph(id, graph)
        return Individual(**kind.model_dump())


class Location(Kind, frozen=True):
    '''
    An object representing a named geographical place
    '''

    rdf_type: RDFType = "http://www.w3.org/2006/vcard/ns#Location"

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        kind = Kind.from_graph(id, graph)
        return Location(**kind.model_dump())


class Organization(Kind, frozen=True):
    '''
    An object representing an organization. An organization is a single entity,
    and might represent a business or government, a department or division
    within a business or government, a club, an association, or the like.
    '''

    rdf_type: RDFType = "http://www.w3.org/2006/vcard/ns#Organization"

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        kind = Kind.from_graph(id, graph)
        return Organization(**kind.model_dump())
