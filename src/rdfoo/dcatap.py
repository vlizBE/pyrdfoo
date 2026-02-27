'''
DCAT-AP 3.0.1

Documentation: https://semiceu.github.io/DCAT-AP/releases/3.0.1/

Namespace: ``http://data.europa.eu/r5r/``
'''

from collections.abc import Sequence
from datetime import date, datetime
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

    issued: Annotated[
        date | datetime | None,
        {"rdf_property": "http://purl.org/dc/terms/issued"}
    ] = None

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


class Distribution(dcat.Distribution, frozen=True):
    '''
    A physical embodiment of the Dataset in a particular format.

    See also: https://semiceu.github.io/DCAT-AP/releases/3.0.1/#Distribution
    '''


class Location(RDF, frozen=True):
    '''
    A spatial region or named place.

    See also: https://semiceu.github.io/DCAT-AP/releases/3.0.1/#Location
    '''

    rdf_type: RDFType = "http://purl.org/dc/terms/Location"

    bbox: Annotated[
        str | None,
        {"rdf_property": "http://www.w3.org/ns/dcat#bbox"},
    ] = None

    centroid: Annotated[
        str | None,
        {"rdf_property": "http://www.w3.org/ns/dcat#centroid"},
    ] = None

    geometry: Annotated[
        str | None,
        {"rdf_property": "https://www.w3.org/ns/locn#locn:geometry"},
    ] = None


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


class PeriodOfTime(dcat.PeriodOfTime, frozen=True):
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

