"""
ProvONE Vocabulary Version 1 Draft

Documentation: https://jenkins-1.dataone.org/jenkins/job/ProvONE-Documentation-1.0.0/ws/provenance/ProvONE/v1/provone.html

Namespace: ``http://purl.dataone.org/provone/2015/01/15/ontology#``
"""

import rdflib

from pydantic import BeforeValidator, PlainSerializer
from typing import Annotated, Sequence

from .prov import Activity, Agent, Association, Entity, Generation, Plan, Usage # fmt: skip # noqa: F401
from .prov import entity_serializer, build_entity_validator
from .rdf import RDFRef, RDFType, RDFURIRef

PROVONE = rdflib.Namespace("http://purl.dataone.org/provone/2015/01/15/ontology#")


#
# Main Entities
#


class Controller(Entity, frozen=True):
    """
    A Controller specifies a Program that controls other Programs under a particular model of computation.

    IRI: http://purl.dataone.org/provone/2015/01/15/ontology#Controller
    """

    rdf_type: RDFType = Entity.get_rdf_type(
        extra="http://purl.dataone.org/provone/2015/01/15/ontology#Controller"
    )

    controls: Annotated[
        Sequence[RDFRef["Program"]] | RDFRef["Program"] | None,
        {
            "rdf_property": "http://purl.dataone.org/provone/2015/01/15/ontology#controls"
        },
        BeforeValidator(build_entity_validator()),
        PlainSerializer(entity_serializer),
    ] = None
    """controls relates a Controller to its destination Program."""

    url: Annotated[
        RDFURIRef | str | None,
        {"rdf_property": "https://schema.org/url"},
    ] = None
    """URL of the item."""

    version: Annotated[
        str | None, {"rdf_property": "http://www.w3.org/ns/dcat#version"}
    ] = None
    """The version indicator (name or identifier) of a resource."""

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        node, _ = cls._node_id(id)

        # entity
        entity_dict: dict = Entity.from_graph(node, graph).model_dump()
        entity_dict.pop("rdf_type")
        # controls
        controls = cls._entities_from_graph_property(
            graph, node, cls._get_rdf_property("controls"), Program
        )
        # url
        url = graph.value(node, cls._get_rdf_property("url"))
        if type(url) is rdflib.URIRef:
            url = RDFURIRef(uri=str(url))
        else:
            url = str(url) if url else None
        # version
        version = graph.value(node, cls._get_rdf_property("version"))
        version = str(version) if version else None

        return Controller(**entity_dict, controls=controls, url=url, version=version)


class Execution(Activity, frozen=True):
    """
    An Execution represents the execution of a Program. If the Program in question is a Workflow, then the Execution represents a trace of its execution.

    IRI: http://purl.dataone.org/provone/2015/01/15/ontology#Execution
    """

    rdf_type: RDFType = Activity.get_rdf_type(
        extra="http://purl.dataone.org/provone/2015/01/15/ontology#Execution"
    )

    was_part_of: Annotated[
        RDFRef["Execution"] | None,
        {
            "rdf_property": "http://purl.dataone.org/provone/2015/01/15/ontology#wasPartOf"
        },
    ] = None
    """wasPartOf nables the specification of the structure of Execution instances in that a parent Execution (associated with a Workflow) has child Executions (associated with Programs and subworkflows)."""

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        node, _ = cls._node_id(id)

        # activity
        activity_dict = Activity.from_graph(node, graph).model_dump()
        activity_dict.pop("rdf_type")
        # was_part_of
        was_part_of = graph.value(node, cls._get_rdf_property("was_part_of"))
        was_part_of = Execution.from_graph(was_part_of, graph) if was_part_of else None

        return Execution(**activity_dict, was_part_of=was_part_of)


class Program(Plan, frozen=True):
    """
    A Program represents a computational task that consumes and produces data through its input and output ports, respectively. It can be atomic or composite, the latter case represented by a possibly nested Program.

    IRI: http://purl.dataone.org/provone/2015/01/15/ontology#Program
    """

    rdf_type: RDFType = Plan.get_rdf_type(
        extra="http://purl.dataone.org/provone/2015/01/15/ontology#Program"
    )

    has_sub_program: Annotated[
        Sequence[RDFRef["Program"]] | RDFRef["Program"] | None,
        {
            "rdf_property": "http://purl.dataone.org/provone/2015/01/15/ontology#hasSubProgram"
        },
    ] = None
    """hasSubProgram specifies the recursive composition of Programs, a parent Program includes a child Program as part of its specification."""

    is_controlled_by: Annotated[
        RDFRef[Controller] | None,
        {
            "rdf_property": "http://purl.dataone.org/provone/2015/01/15/ontology#isControlledBy"
        },
    ] = None
    """Inverse property of controls"""

    is_sub_program_of: Annotated[
        RDFRef["Program"] | None,
        {
            "rdf_property": "http://purl.dataone.org/provone/2015/01/15/ontology#isSubProgramOf"
        },
        BeforeValidator(build_entity_validator()),
        PlainSerializer(entity_serializer),
    ] = None
    """Inverse property of hasSubProgram."""

    version: Annotated[
        str | None, {"rdf_property": "http://www.w3.org/ns/dcat#version"}
    ] = None
    """The version indicator (name or identifier) of a resource."""

    url: Annotated[
        RDFURIRef | str | None,
        {"rdf_property": "https://schema.org/url"},
    ] = None
    """URL of the item."""

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        node, _ = cls._node_id(id)

        # entity
        entity_dict: dict = Entity.from_graph(node, graph).model_dump()
        entity_dict.pop("rdf_type")
        # has_sub_program
        has_sub_program = cls._entities_from_graph_property(
            graph, node, cls._get_rdf_property("has_sub_program"), Program
        )
        # is_controlled_by
        is_controlled_by = graph.value(node, cls._get_rdf_property("is_controlled_by"))
        is_controlled_by = (
            Controller.from_graph(is_controlled_by, graph) if is_controlled_by else None
        )
        # is_sub_program_of
        is_sub_program_of = cls._entity_from_graph_property(
            graph, node, cls._get_rdf_property("is_sub_program_of"), Program
        )
        # version
        version = graph.value(node, cls._get_rdf_property("version"))
        version = str(version) if version else None
        # url
        url = graph.value(node, cls._get_rdf_property("url"))
        if type(url) is rdflib.URIRef:
            url = RDFURIRef(uri=str(url))
        else:
            url = str(url) if url else None

        return Program(
            **entity_dict,
            has_sub_program=has_sub_program,
            is_controlled_by=is_controlled_by,
            is_sub_program_of=is_sub_program_of,
            version=version,
            url=url,
        )


class Workflow(Program, frozen=True):
    """
    A Workflow is a distinguished Program, which indicates that is meant to represent a computational experiment in its entirety. It is also subject to versioning by prov:wasDerivedFrom through its super-class provone:Program.

    IRI: http://purl.dataone.org/provone/2015/01/15/ontology#Workflow
    """

    rdf_type: RDFType = Program.get_rdf_type(
        extra="http://purl.dataone.org/provone/2015/01/15/ontology#Workflow"
    )

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        node, _ = cls._node_id(id)

        # program
        program_dict: dict = Program.from_graph(node, graph).model_dump()
        program_dict.pop("rdf_type")

        return Workflow(**program_dict)
