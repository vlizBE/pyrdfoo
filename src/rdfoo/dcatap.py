'''
DCAT-AP 3.0.1

Documentation: https://semiceu.github.io/DCAT-AP/releases/3.0.1/

Namespace: ``http://data.europa.eu/r5r/``
'''

from collections.abc import Sequence
from datetime import date, datetime
import rdflib
from typing import Annotated

from . import dcat
from .dcat import Agent
# The imports on the next line are needed at runtime
from .dcat import Relationship  # noqa: F401
from .rdf import RDF, RDFRef, RDFType
from .rdfs import Resource


#
# Main Entities
#


class Catalogue(dcat.Catalogue, frozen=True):
    '''
    A catalogue or repository that hosts the Datasets or Data Services being
    described.

    See also: https://semiceu.github.io/DCAT-AP/releases/3.0.1/#Catalogue
    '''

    description: Annotated[
        str | Sequence[str],
        {"rdf_property": "http://purl.org/dc/terms/description"},
    ] = ... # type: ignore
    '''A free-text account of the Catalogue.'''

    publisher: Annotated[
        RDFRef[Agent],
        {"rdf_property": "http://purl.org/dc/terms/publisher"},
    ] = ... # type: ignore
    '''An entity (organisation) responsible for making the Catalogue
    available.'''

    title: Annotated[
        str | Sequence[str],
        {"rdf_property": "http://purl.org/dc/terms/title"},
    ] = ... # type: ignore
    '''A name given to the Catalogue.'''

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        catalogue = dcat.Catalogue.from_graph(id, graph)
        return Catalogue(**catalogue.model_dump())


CataloguedResource = dcat.CataloguedResource


class Dataset(dcat.Dataset, frozen=True):
    '''
    A conceptual entity that represents the information published.

    See also: https://semiceu.github.io/DCAT-AP/releases/3.0.1/#Dataset
    '''

    description: Annotated[
        str | Sequence[str],
        {"rdf_property": "http://purl.org/dc/terms/description"},
    ] = ... # type: ignore

    qualified_attribution: Annotated[
        Sequence[RDFRef["Attribution"]],
        {"rdf_property": "http://www.w3.org/ns/prov#qualifiedAttribution"},
    ] = []

    source: Annotated[
        RDFRef[Resource] | Sequence[RDFRef[Resource]],
        {"rdf_property": "http://purl.org/dc/terms/source"},
    ] = []

    title: Annotated[
        str | Sequence[str],
        {"rdf_property": "http://purl.org/dc/terms/title"},
    ] = ... # type: ignore

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        node, _ = cls._node_id(id)
        dataset = dcat.Dataset.from_graph(id, graph)
        # source
        source_objects = graph.objects(node, cls._get_rdf_property("source"))
        source = [Resource.from_graph(obj, graph) for obj in source_objects]
        # Dataset
        return Dataset(
            **dataset.model_dump(),
            source=source,
        )


Distribution = dcat.Distribution
'''
A physical embodiment of the Dataset in a particular format.

See also: https://semiceu.github.io/DCAT-AP/releases/3.0.1/#Distribution
'''


Location = dcat.Location
'''
A spatial region or named place.

See also: https://semiceu.github.io/DCAT-AP/releases/3.0.1/#Location
'''


#
# Supportive Entities
#


class Attribution(RDF, frozen=True):
    '''
    Attribution is the ascribing of an entity to an agent.

    See also: https://semiceu.github.io/DCAT-AP/releases/3.0.1/#Attribution
    '''

    rdf_type: RDFType = "http://www.w3.org/ns/prov#Attribution"

    agent: Annotated[
        RDFRef[Agent],
        {"rdf_property": "http://www.w3.org/ns/prov#agent"},
    ]

    hadRole: Annotated[
        RDFRef["Role"] | None,
        {"rdf_property": "https://www.w3.org/ns/dcat#hadRole"},
    ] = None

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        node, rdf_id = cls._node_id(id)
        # start_date
        agent_obj = graph.value(node, cls._get_rdf_property("agent"))
        agent = Agent.from_graph(agent_obj, graph) if agent_obj is not None else None
        if agent is None:
            raise Exception("Attribution must have an agent")
        # end_date
        hadRole_obj = graph.value(node, cls._get_rdf_property("hadRole"))
        hadRole = Role.from_graph(hadRole_obj, graph) if hadRole_obj is not None else None
        # Attribution
        return Attribution(
            rdf_id=rdf_id,
            agent=agent,
            hadRole=hadRole,
        )


PeriodOfTime = dcat.PeriodOfTime
'''
An interval of time that is named or defined by its start and end dates.

See also: https://semiceu.github.io/DCAT-AP/releases/3.0.1/#PeriodofTime
'''


class Role(RDF, frozen=True):
    '''
    A role is the function of a resource or agent with respect to another
    resource, in the context of resource attribution or resource relationships.

    See also: https://semiceu.github.io/DCAT-AP/releases/3.0.1/#Role
    '''

    rdf_type: RDFType = "https://www.w3.org/ns/dcat#Role"

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        _, rdf_id = cls._node_id(id)
        return Role(rdf_id=rdf_id)

