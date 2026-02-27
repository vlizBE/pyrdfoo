'''
Data Catalog Vocabulary (DCAT) - Version 3

Ontology documentation: https://www.w3.org/TR/vocab-dcat-3/

Namespace: ``http://www.w3.org/ns/dcat#``
'''

from collections.abc import Sequence
from datetime import date, datetime
from typing import Annotated

from . import dcterms
from .foaf import Agent
from .rdf import RDF, RDFRef, RDFType
from .rdfs import Resource
from .vcard import Kind

class Catalogue(RDF, frozen=True):
    '''
    A curated collection of metadata about resources.

    See also: https://www.w3.org/TR/vocab-dcat-3/#Class:Catalog
    '''

    rdf_type: RDFType = "https://www.w3.org/ns/dcat#Catalog"

    dataset: Annotated[
        Sequence[RDFRef["Dataset"]] | None,
        {"rdf_property": "http://www.w3.org/ns/dcat#dataset"},
    ] = None
    '''A Dataset that is part of the Catalogue.'''

    description: Annotated[
        str | Sequence[str] | None,
        {"rdf_property": "http://purl.org/dc/terms/description"},
    ] = None
    '''A free-text account of the Catalogue.'''

    publisher: Annotated[
        RDFRef[Agent] | None,
        {"rdf_property": "http://purl.org/dc/terms/publisher"},
    ] = None
    '''An entity (organisation) responsible for making the Catalogue
    available.'''

    title: Annotated[
        str | Sequence[str] | None,
        {"rdf_property": "http://purl.org/dc/terms/title"},
    ] = None
    '''A name given to the Catalogue.'''


class CataloguedResource(Resource, frozen=True):
    '''
    Resource published or curated by a single agent.

    See also: https://www.w3.org/TR/vocab-dcat-3/#Class:Resource
    '''

    rdf_type: RDFType = Resource.get_rdf_type("https://www.w3.org/ns/dcat#Resource")

    contact_point: Annotated[
        Sequence[RDFRef[Kind]] | None,
        {"rdf_property": "http://www.w3.org/ns/dcat#contactPoint"},
    ] = None

    creator: Annotated[
        Sequence[RDFRef[Agent]] | None,
        {"rdf_property": "http://purl.org/dc/terms/creator"},
    ] = None

    description: Annotated[
        str | Sequence[str] | None,
        {"rdf_property": "http://purl.org/dc/terms/description"},
    ] = None

    is_referenced_by: Annotated[
        "RDFRef[CataloguedResource] | Sequence[RDFRef[CataloguedResource]] | None",
        {"rdf_property": "http://purl.org/dc/terms/isReferencedBy"},
    ] = None

    licence: Annotated[
        str | None,
        {"rdf_property": "http://purl.org/dc/terms/license"},
    ] = None

    qualified_relation: Annotated[
        Sequence[RDFRef["Relationship"]] | None,
        {"rdf_property": "http://www.w3.org/ns/dcat#qualifiedRelation"},
    ] = None

    title: Annotated[
        str | Sequence[str] | None,
        {"rdf_property": "http://purl.org/dc/terms/title"},
    ] = None



class Dataset(CataloguedResource, frozen=True):
    '''
    A collection of data, published or curated by a single agent, and available
    for access or download in one or more representations.

    See also: https://www.w3.org/TR/vocab-dcat-3/#Class:Dataset
    '''

    rdf_type: RDFType = CataloguedResource.get_rdf_type("https://www.w3.org/ns/dcat#Dataset")

    distribution: Annotated[
        Sequence[RDFRef["Distribution"]] | None,
        {"rdf_property": "http://www.w3.org/ns/dcat#distribution"},
    ] = None

    issued: Annotated[
        date | datetime | None,
        {"rdf_property": "http://purl.org/dc/terms/issued"}
    ] = None

    spatial: Annotated[
        Sequence[RDFRef["Location"]] | None,
        {"rdf_property": "http://purl.org/dc/terms/spatial"},
    ] = None

    temporal: Annotated[
        Sequence[RDFRef["PeriodOfTime"]] | None,
        {"rdf_property": "http://purl.org/dc/terms/temporal"},
    ] = None


class Distribution(RDF, frozen=True):
    '''
    A specific representation of a dataset. A dataset might be available in
    multiple serializations that may differ in various ways, including natural
    language, media-type or format, schematic organization, temporal and spatial
    resolution, level of detail or profiles (which might specify any or all of
    the above).

    See also: https://www.w3.org/TR/vocab-dcat-3/#Class:Distribution
    '''

    rdf_type: RDFType = "http://www.w3.org/ns/dcat#Distribution"

    access_url: Annotated[
        RDFRef[Resource] | str | Sequence[RDFRef[Resource] | str] | None,
        {"rdf_property": "http://www.w3.org/ns/dcat#accessURL"},
    ] = None

    description: Annotated[
        str | Sequence[str] | None,
        {"rdf_property": "http://purl.org/dc/terms/description"},
    ] = None


class Relationship(RDF, frozen=True):
    '''
    An association class for attaching additional information to a relationship
    between DCAT Resources.

    See also: https://www.w3.org/TR/vocab-dcat-3/#Class:Relationship
    '''

    rdf_type: RDFType = "http://www.w3.org/ns/dcat#Relationship"


class PeriodOfTime(RDF, frozen=True):
    '''
    An interval of time that is named or defined by its start and end.

    See also: https://www.w3.org/TR/vocab-dcat-3/#Class:Period_of_Time
    '''

    rdf_type: RDFType = "http://purl.org/dc/terms/PeriodOfTime"

    end_date: Annotated[
        date | None,
        {"rdf_property": "http://www.w3.org/ns/dcat#endDate"},
    ] = None

    start_date: Annotated[
        date | None,
        {"rdf_property": "https://www.w3.org/ns/dcat#startDate"},
    ] = None


class Location(dcterms.Location, frozen=True):
    '''
    A spatial region or named place.

    See also: https://www.w3.org/TR/vocab-dcat-3/#Class:Location
    '''

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
