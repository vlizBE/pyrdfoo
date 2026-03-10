'''
Data Catalog Vocabulary (DCAT) - Version 3

Ontology documentation: https://www.w3.org/TR/vocab-dcat-3/

Namespace: ``http://www.w3.org/ns/dcat#``
'''

from collections.abc import Sequence
from datetime import date, datetime
import rdflib
from typing import Annotated

from . import dcterms
from .foaf import Agent
from .rdf import RDF, RDFRef, RDFType, uri
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
        Sequence[str] | str | None,
        {"rdf_property": "http://purl.org/dc/terms/title"},
    ] = None
    '''A name given to the Catalogue.'''

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        node, rdf_id = cls._node_id(id)
        # dataset
        dataset_objects = graph.objects(node, cls._get_rdf_property("dataset"))
        dataset = [Dataset.from_graph(obj, graph) for obj in dataset_objects]
        if len(dataset) == 0:
            dataset = None
        # description
        description_objects = graph.objects(node, cls._get_rdf_property("description"))
        descriptions = [str(obj) for obj in description_objects]
        if len(descriptions) > 1:
            description = descriptions
        elif len(descriptions) == 1:
            description = descriptions[0]
        else:
            description = None
        # publisher
        publisher_object = graph.value(node, cls._get_rdf_property("publisher"))
        agent_type = Agent.get_rdf_type()
        if agent_type is str:
            agent_type = [agent_type]
        def flatten(xss):
            return [x for xs in xss for x in xs]
        if len(flatten([graph.triples((publisher_object, rdflib.RDF.type, rdflib.URIRef(t))) for t in agent_type])) > 0:
            publisher = Agent.from_graph(publisher_object, graph) if publisher_object is not None else None
        else:
            publisher = uri(str(publisher_object)) if publisher_object is not None else None
        # title
        title_objects = graph.objects(node, cls._get_rdf_property("title"))
        titles = [str(obj) for obj in title_objects]
        if len(titles) > 1:
            title = titles
        elif len(titles) == 1:
            title = titles[0]
        else:
            title = None
        # Catalogue
        return Catalogue(
            rdf_id=rdf_id,
            dataset=dataset,
            description=description,
            publisher=publisher,
            title=title,
        )


class CataloguedResource(Resource, frozen=True):
    '''
    Resource published or curated by a single agent.

    See also: https://www.w3.org/TR/vocab-dcat-3/#Class:Resource
    '''

    rdf_type: RDFType = Resource.get_rdf_type(extra="https://www.w3.org/ns/dcat#Resource")

    contact_point: Annotated[
        Sequence[RDFRef[Kind]] | None,
        {"rdf_property": "http://www.w3.org/ns/dcat#contactPoint"},
    ] = None

    creator: Annotated[
        Sequence[RDFRef[Agent]] | None,
        {"rdf_property": "http://purl.org/dc/terms/creator"},
    ] = None

    description: Annotated[
        Sequence[str] | str | None,
        {"rdf_property": "http://purl.org/dc/terms/description"},
    ] = None

    is_referenced_by: Annotated[
        "Sequence[RDFRef[CataloguedResource]] | RDFRef[CataloguedResource] | None",
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
        Sequence[str] | str | None,
        {"rdf_property": "http://purl.org/dc/terms/title"},
    ] = None

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        node, rdf_id = cls._node_id(id)
        # contact_point
        contact_point_objects = graph.objects(node, cls._get_rdf_property("contact_point"))
        contact_point = [Kind.from_graph(obj, graph) for obj in contact_point_objects]
        if len(contact_point) == 0:
            contact_point = None
        # creator
        creator_objects = graph.objects(node, cls._get_rdf_property("creator"))
        creator = [Agent.from_graph(obj, graph) for obj in creator_objects]
        if len(creator) == 0:
            creator = None
        # description
        description_objects = graph.objects(node, cls._get_rdf_property("description"))
        descriptions = [str(obj) for obj in description_objects]
        if len(descriptions) > 1:
            description = descriptions
        elif len(descriptions) == 1:
            description = descriptions[0]
        else:
            description = None
        # is_referenced_by
        is_referenced_by_objects = graph.objects(node, cls._get_rdf_property("is_referenced_by"))
        is_referenced_by = [CataloguedResource.from_graph(obj, graph) for obj in is_referenced_by_objects]
        if len(is_referenced_by) == 0:
            is_referenced_by = None
        # licence
        licence_object = graph.value(node, cls._get_rdf_property("licence"))
        licence = str(licence_object) if licence_object is not None else None
        # qualified_relation
        qualified_relation_objects = graph.objects(node, cls._get_rdf_property("qualified_relation"))
        qualified_relation = [Relationship.from_graph(obj, graph) for obj in qualified_relation_objects]
        if len(qualified_relation) == 0:
            qualified_relation = None
        # title
        title_objects = graph.objects(node, cls._get_rdf_property("title"))
        titles = [str(obj) for obj in title_objects]
        if len(titles) > 1:
            title = titles
        elif len(titles) == 1:
            title = titles[0]
        else:
            title = None
        # CataloguedResource
        return CataloguedResource(
            rdf_id=rdf_id,
            contact_point=contact_point,
            creator=creator,
            description=description,
            is_referenced_by=is_referenced_by,
            licence=licence,
            qualified_relation=qualified_relation,
            title=title,
        )


class Dataset(CataloguedResource, frozen=True):
    '''
    A collection of data, published or curated by a single agent, and available
    for access or download in one or more representations.

    See also: https://www.w3.org/TR/vocab-dcat-3/#Class:Dataset
    '''

    rdf_type: RDFType = CataloguedResource.get_rdf_type(extra="https://www.w3.org/ns/dcat#Dataset")

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

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        node, _ = cls._node_id(id)
        # CataloguedResource
        catalogued_resource = CataloguedResource.from_graph(node, graph)
        # distribution
        distribution_objects = graph.objects(node, cls._get_rdf_property("distribution"))
        distribution = [Distribution.from_graph(obj, graph) for obj in distribution_objects]
        if len(distribution) == 0:
            distribution = None
        # issued
        issued_object = graph.value(node, cls._get_rdf_property("issued"))
        issued = datetime.fromisoformat(str(issued_object)) if issued_object is not None else None
        # spatial
        spatial_objects = graph.objects(node, cls._get_rdf_property("spatial"))
        spatial = [Location.from_graph(obj, graph) for obj in spatial_objects]
        if len(spatial) == 0:
            spatial = None
        # temporal
        temporal_objects = graph.objects(node, cls._get_rdf_property("temporal"))
        temporal = [PeriodOfTime.from_graph(obj, graph) for obj in temporal_objects]
        if len(temporal) == 0:
            temporal = None
        # Dataset
        catalogued_resource_dict: dict = catalogued_resource.model_dump()
        catalogued_resource_dict.pop("rdf_type")
        return Dataset(
            **catalogued_resource_dict,
            distribution=distribution,
            issued=issued,
            spatial=spatial,
            temporal=temporal,
        )


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
        Sequence[RDFRef[Resource] | str] | RDFRef[Resource] | str | None,
        {"rdf_property": "http://www.w3.org/ns/dcat#accessURL"},
    ] = None

    description: Annotated[
        Sequence[str] | str | None,
        {"rdf_property": "http://purl.org/dc/terms/description"},
    ] = None

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        node, rdf_id = cls._node_id(id)
        # access_url
        access_url_objects = graph.objects(node, cls._get_rdf_property("access_url"))
        access_url = [str(obj) for obj in access_url_objects]
        if len(access_url) > 1:
            access_url = access_url
        elif len(access_url) == 1:
            access_url = access_url[0]
        else:
            access_url = None
        # description
        description_objects = graph.objects(node, cls._get_rdf_property("description"))
        descriptions = [str(obj) for obj in description_objects]
        if len(descriptions) > 1:
            description = descriptions
        elif len(descriptions) == 1:
            description = descriptions[0]
        else:
            description = None
        # Distribution
        return Distribution(
            rdf_id=rdf_id,
            access_url=access_url,
            description=description,
        )


class Relationship(RDF, frozen=True):
    '''
    An association class for attaching additional information to a relationship
    between DCAT Resources.

    See also: https://www.w3.org/TR/vocab-dcat-3/#Class:Relationship
    '''

    rdf_type: RDFType = "http://www.w3.org/ns/dcat#Relationship"

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        _, rdf_id = cls._node_id(id)
        return Relationship(rdf_id=rdf_id)


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

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        node, rdf_id = cls._node_id(id)
        # start_date
        start_obj = graph.value(node, cls._get_rdf_property("start_date"))
        start_date = datetime.fromisoformat(str(start_obj)) if start_obj is not None else None
        # end_date
        end_obj = graph.value(node, cls._get_rdf_property("end_date"))
        end_date = datetime.fromisoformat(str(end_obj)) if end_obj is not None else None
        # PeriodOfTime
        return PeriodOfTime(
            rdf_id=rdf_id,
            start_date=start_date,
            end_date=end_date,
        )


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

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        node, rdf_id = cls._node_id(id)
        # location
        base_loc = dcterms.Location.from_graph(node, graph)
        # bbox
        bbox_obj = graph.value(node, cls._get_rdf_property("bbox"))
        bbox = str(bbox_obj) if bbox_obj is not None else None
        # centroid
        centroid_obj = graph.value(node, cls._get_rdf_property("centroid"))
        centroid = str(centroid_obj) if centroid_obj is not None else None
        # geometry
        geometry_obj = graph.value(node, cls._get_rdf_property("geometry"))
        geometry = str(geometry_obj) if geometry_obj is not None else None
        # Location
        loc_dict: dict = base_loc.model_dump()
        loc_dict.pop("rdf_type")
        return Location(
            **loc_dict,
            bbox=bbox,
            centroid=centroid,
            geometry=geometry,
        )
