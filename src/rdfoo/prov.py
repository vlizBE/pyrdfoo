"""
PROV-O W3C Recommendation 30 April 2013

Documentation: https://www.w3.org/TR/prov-o/

Namespace: ``http://www.w3.org/ns/prov#``
"""

import rdflib

from datetime import datetime
from pydantic import BaseModel, BeforeValidator, PlainSerializer
from typing import Annotated, Any, Callable, ClassVar, Sequence

from .rdf import (
    RDF,
    RDFType,
    RDFRef,
    RDFURIRef,
    graph_node_rdf_types,
)


def entity_serializer(value: list[BaseModel] | BaseModel | None) -> Any:
    """Generic serialiser for entity types, allows serialization of RDFRef[Entity] where the specific Entity could be of type Entity or any of its bases."""
    if isinstance(value, list):
        return [v.model_dump() for v in value]
    elif value:
        return value.model_dump()

    return None


def build_entity_validator(base_entity_type: Any = None) -> Callable[[Any], Any]:
    """Builder for generic entity validator, allows validation of RDFRef[Entity] where the specific Entity could be of type Entity or any of its bases."""

    def validate_entity(value: Any, entity_type: Any) -> Any:
        if isinstance(value, entity_type):
            return value
        elif isinstance(value, dict):
            if "rdf_type" not in value:
                raise ValueError(f'entity should have a "rdf_type" field, got: {value}')

            rdf_types = value.pop("rdf_type")
            entity = Entity._entity_from_rdf_type(rdf_types, Entity)

            if not issubclass(entity, entity_type):
                raise ValueError(
                    f"entity should have base type {entity_type.__name__}, but has type {entity.__name__}"
                )

            return entity(**value)

        raise ValueError(
            f"field expects a (subclass of) {entity_type.__name__}, received {type(value)}"
        )

    def entity_validator(value: Any) -> Any:
        entity_type = base_entity_type if base_entity_type else Entity

        if value is None:
            rval = None
        elif isinstance(value, list):
            rval = [validate_entity(v, entity_type) for v in value]
        else:
            rval = validate_entity(value, entity_type)

        return rval

    return entity_validator


#
# Main Entities
#


class Entity(RDF, frozen=True):
    """
    An entity is a physical, digital, conceptual, or other kind of thing with some fixed aspects; entities may be real or imaginary.

    IRI: http://www.w3.org/ns/prov#Entity
    """

    _RDF_TYPE_MAP: ClassVar[dict] = {}

    rdf_type: RDFType = str(rdflib.PROV.Entity)

    description: Annotated[
        Sequence[str] | str | None,
        {"rdf_property": "http://purl.org/dc/terms/description"},
    ] = None
    """An account of the resource."""

    title: Annotated[
        Sequence[str] | str | None, {"rdf_property": "http://purl.org/dc/terms/title"}
    ] = None
    """ A name given to the resource. """

    influenced: Annotated[
        Sequence[RDFRef["Entity"]] | RDFRef["Entity"] | None,
        {"rdf_property": str(rdflib.PROV.influenced)},
        BeforeValidator(build_entity_validator()),
        PlainSerializer(entity_serializer),
    ] = None
    """Influence is the capacity of an entity, activity, or agent to have an effect on the character, development, or behavior of another by means of usage, start, end, generation, invalidation, communication, derivation, attribution, association, or delegation."""

    was_attributed_to: Annotated[
        Sequence[RDFRef["Agent"]] | RDFRef["Agent"] | None,
        {"rdf_property": str(rdflib.PROV.wasAttributedTo)},
        BeforeValidator(build_entity_validator()),
        PlainSerializer(entity_serializer),
    ] = None
    """Attribution is the ascribing of an entity to an agent."""

    was_derived_from: Annotated[
        RDFRef["Entity"] | None,
        {"rdf_property": str(rdflib.PROV.wasDerivedFrom)},
        BeforeValidator(build_entity_validator()),
        PlainSerializer(entity_serializer),
    ] = None
    """A derivation is a transformation of an entity into another, an update of an entity resulting in a new one, or the construction of a new entity based on a pre-existing entity."""

    was_influenced_by: Annotated[
        Sequence[RDFRef["Entity"]] | RDFRef["Entity"] | None,
        {"rdf_property": str(rdflib.PROV.wasInfluencedBy)},
        BeforeValidator(build_entity_validator()),
        PlainSerializer(entity_serializer),
    ] = None
    """Influence is the capacity of an entity, activity, or agent to have an effect on the character, development, or behavior of another by means of usage, start, end, generation, invalidation, communication, derivation, attribution, association, or delegation."""

    was_generated_by: Annotated[
        Sequence[RDFRef["Activity"]] | RDFRef["Activity"] | None,
        {"rdf_property": str(rdflib.PROV.wasGeneratedBy)},
        BeforeValidator(build_entity_validator()),
        PlainSerializer(entity_serializer),
    ] = None
    """Generation is the completion of production of a new entity by an activity. This entity did not exist before generation and becomes available for usage after this generation."""

    was_used_by: Annotated[
        Sequence[RDFRef["Activity"]] | RDFRef["Activity"] | None,
        {"rdf_property": str(rdflib.PROV.wasUsedBy)},
        BeforeValidator(build_entity_validator()),
        PlainSerializer(entity_serializer),
    ] = None
    """Usage is the beginning of utilizing an entity by an activity. Before usage, the activity had not begun to utilize this entity and could not have been affected by the entity."""

    qualified_generation: Annotated[
        Sequence[RDFRef["Generation"]] | RDFRef["Generation"] | None,
        {"rdf_property": str(rdflib.PROV.qualifiedGeneration)},
    ] = None
    """Generation is the completion of production of a new entity by an activity. This entity did not exist before generation and becomes available for usage after this generation."""

    def __init_subclass__(cls):
        rdf_type = (
            getattr(cls, "rdf_type", None)
            or getattr(cls, "get_rdf_type", lambda: None)()
        )
        if rdf_type:
            rdf_type = [rdf_type] if isinstance(rdf_type, str) else rdf_type
            rdf_type_set = tuple(set(rdf_type))
            Entity._RDF_TYPE_MAP[rdf_type_set] = cls

    @classmethod
    def _entity_from_rdf_type(cls, rdf_types: RDFType | None, alt_entity: Any = None):
        if alt_entity is None:
            alt_entity = Entity

        if rdf_types is None:
            return alt_entity

        rdf_type_set = tuple(
            set([rdf_types] if isinstance(rdf_types, str) else rdf_types)
        )
        entity = cls._RDF_TYPE_MAP.get(rdf_type_set, alt_entity)

        return entity

    @classmethod
    def _entity_from_graph_property(
        cls,
        graph: rdflib.Graph,
        node: Any,
        property: rdflib.URIRef,
        alt_entity: Any = None,
    ) -> Any:
        entity = None
        value = graph.value(node, property)
        if value:
            rdf_types = graph_node_rdf_types(graph, value)
            entity = cls._entity_from_rdf_type(rdf_types, alt_entity)
            entity = entity.from_graph(value, graph)

        return entity

    @classmethod
    def _entities_from_graph_property(
        cls,
        graph: rdflib.Graph,
        node: Any,
        property: rdflib.URIRef,
        alt_entity: Any = None,
    ) -> Any:
        entities = []
        objects = graph.objects(node, property)
        if objects:
            for obj in objects:
                rdf_types = graph_node_rdf_types(graph, obj)
                entity = cls._entity_from_rdf_type(rdf_types, alt_entity)
                entities.append(entity.from_graph(obj, graph))

        if not entities:
            entities = None
        elif len(entities) == 1:
            entities = entities[0]

        return entities

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        node, rdf_id = cls._node_id(id)

        # description
        description = graph.objects(node, cls._get_rdf_property("description"))
        description = (
            [str(obj) for obj in description] if description else None
        ) or None
        if description and len(description) == 1:
            description = description[0]
        # title
        title = graph.objects(node, cls._get_rdf_property("title"))
        title = ([str(obj) for obj in title] if title else None) or None
        if title and len(title) == 1:
            title = title[0]
        # influenced
        influenced = cls._entities_from_graph_property(
            graph, node, cls._get_rdf_property("influenced"), Entity
        )
        # was_derived_from
        was_derived_from = cls._entity_from_graph_property(
            graph, node, cls._get_rdf_property("was_derived_from"), Entity
        )
        # was_attributed_to
        was_attributed_to = cls._entities_from_graph_property(
            graph, node, cls._get_rdf_property("was_attributed_to"), Activity
        )
        # was_generated_by
        was_generated_by = cls._entities_from_graph_property(
            graph, node, cls._get_rdf_property("was_generated_by"), Activity
        )
        # was_influenced_by
        was_influenced_by = cls._entities_from_graph_property(
            graph, node, cls._get_rdf_property("was_influenced_by"), Activity
        )
        # was_used_by
        was_used_by = cls._entities_from_graph_property(
            graph, node, cls._get_rdf_property("was_used_by"), Activity
        )
        # qualified_generation
        qualified_generation = graph.objects(
            node, cls._get_rdf_property("qualified_generation")
        )
        qualified_generation = (
            [Generation.from_graph(qg, graph) for qg in qualified_generation]
            if qualified_generation
            else None
        ) or None
        if qualified_generation and len(qualified_generation) == 1:
            qualified_generation = qualified_generation[0]

        return Entity(
            rdf_id=rdf_id,
            description=description,
            title=title,
            influenced=influenced,
            was_attributed_to=was_attributed_to,
            was_derived_from=was_derived_from,
            was_generated_by=was_generated_by,
            was_influenced_by=was_influenced_by,
            was_used_by=was_used_by,
            qualified_generation=qualified_generation,
        )


class Agent(Entity, frozen=True):
    """
    An agent is something that bears some form of responsibility for an activity taking place, for the existence of an entity, or for another agent's activity.

    IRI: http://www.w3.org/ns/prov#Agent
    """

    rdf_type: RDFType = Entity.get_rdf_type(extra=str(rdflib.PROV.Agent))

    name: Annotated[
        str | None,
        {"rdf_property": "http://xmlns.com/foaf/0.1/name"},
    ] = None
    """ A name for some thing. """

    mbox: Annotated[
        RDFURIRef | str | None, {"rdf_property": "http://xmlns.com/foaf/0.1/mbox"}
    ] = None
    """ A personal mailbox, ie. an Internet mailbox associated with exactly one owner, the first owner of this mailbox. """

    acted_on_behalf_of: Annotated[
        RDFRef["Agent"] | None, {"rdf_property": str(rdflib.PROV.actedOnBehalfOf)}
    ] = None
    """ Delegation is the assignment of authority and responsibility to an agent (by itself or by another agent) to carry out a specific activity as a delegate or representative, while the agent it acts on behalf of retains some responsibility for the outcome of the delegated work. For example, a student acted on behalf of his supervisor, who acted on behalf of the department chair, who acted on behalf of the university; all those agents are responsible in some way for the activity that took place but we do not say explicitly who bears responsibility and to what degree. """

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        node, _ = cls._node_id(id)

        # entity
        entity_dict: dict = Entity.from_graph(node, graph).model_dump()
        entity_dict.pop("rdf_type")
        # name
        name = graph.value(node, cls._get_rdf_property("name"))
        name = str(name) if name else None
        # mbox
        mbox = graph.value(node, cls._get_rdf_property("mbox"))
        if type(mbox) is rdflib.URIRef:
            mbox = RDFURIRef(uri=str(mbox))
        else:
            mbox = str(mbox) if mbox else None
        # acted_on_behalf_of
        acted_on_behalf_of = graph.value(
            node, cls._get_rdf_property("acted_on_behalf_of")
        )
        acted_on_behalf_of = (
            Agent.from_graph(acted_on_behalf_of, graph) if acted_on_behalf_of else None
        )

        return Agent(
            **entity_dict, name=name, mbox=mbox, acted_on_behalf_of=acted_on_behalf_of
        )


class Activity(Entity, frozen=True):
    """
    An activity is something that occurs over a period of time and acts upon or with entities; it may include consuming, processing, transforming, modifying, relocating, using, or generating entities.

    IRI: http://www.w3.org/ns/prov#Activity
    """

    rdf_type: RDFType = Entity.get_rdf_type(extra=str(rdflib.PROV.Activity))

    ended_at_time: Annotated[
        datetime | None, {"rdf_property": str(rdflib.PROV.endedAtTime)}
    ] = None
    """ End is when an activity is deemed to have been ended by an entity, known as trigger. The activity no longer exists after its end. Any usage, generation, or invalidation involving an activity precedes the activity's end. An end may refer to a trigger entity that terminated the activity, or to an activity, known as ender that generated the trigger."""

    generated: Annotated[
        Sequence[RDFRef[Entity]] | RDFRef[Entity] | None,
        {"rdf_property": str(rdflib.PROV.generated)},
        BeforeValidator(build_entity_validator()),
        PlainSerializer(entity_serializer),
    ] = None
    """Generation is the completion of production of a new entity by an activity. This entity did not exist before generation and becomes available for usage after this generation."""

    was_associated_with: Annotated[
        Sequence[RDFRef[Agent]] | RDFRef[Agent] | None,
        {"rdf_property": str(rdflib.PROV.wasAssociatedWith)},
    ] = None
    """An activity association is an assignment of responsibility to an agent for an activity, indicating that the agent had a role in the activity. It further allows for a plan to be specified, which is the plan intended by the agent to achieve some goals in the context of this activity."""

    was_informed_by: Annotated[
        Sequence[RDFRef["Activity"]] | RDFRef["Activity"] | None,
        {"rdf_property": str(rdflib.PROV.wasInformedBy)},
        BeforeValidator(build_entity_validator()),
        PlainSerializer(entity_serializer),
    ] = None
    """Communication is the exchange of an entity by two activities, one activity using the entity generated by the other."""

    qualified_association: Annotated[
        Sequence[RDFRef["Association"]] | RDFRef["Association"] | None,
        {"rdf_property": str(rdflib.PROV.qualifiedAssociation)},
    ] = None
    """An activity association is an assignment of responsibility to an agent for an activity, indicating that the agent had a role in the activity. It further allows for a plan to be specified, which is the plan intended by the agent to achieve some goals in the context of this activity."""

    qualified_usage: Annotated[
        Sequence[RDFRef["Usage"]] | RDFRef["Usage"] | None,
        {"rdf_property": str(rdflib.PROV.qualifiedUsage)},
    ] = None
    """Usage is the beginning of utilizing an entity by an activity. Before usage, the activity had not begun to utilize this entity and could not have been affected by the entity."""

    started_at_time: Annotated[
        datetime | None, {"rdf_property": str(rdflib.PROV.startedAtTime)}
    ] = None
    """ Start is when an activity is deemed to have been started by an entity, known as trigger. The activity did not exist before its start. Any usage, generation, or invalidation involving an activity follows the activity's start. A start may refer to a trigger entity that set off the activity, or to an activity, known as starter, that generated the trigger."""

    used: Annotated[
        Sequence[RDFRef[Entity]] | RDFRef[Entity] | None,
        {"rdf_property": str(rdflib.PROV.used)},
        BeforeValidator(build_entity_validator()),
        PlainSerializer(entity_serializer),
    ] = None
    """Usage is the beginning of utilizing an entity by an activity. Before usage, the activity had not begun to utilize this entity and could not have been affected by the entity."""

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph) -> "Activity":
        node, _ = cls._node_id(id)

        # entity
        entity_dict: dict = Entity.from_graph(node, graph).to_dict()
        entity_dict.pop("rdf_type")
        # ended_at_time
        ended_at_time = graph.value(node, cls._get_rdf_property("ended_at_time"))
        ended_at_time = (
            datetime.fromisoformat(str(ended_at_time)) if ended_at_time else None
        )
        # generated
        generated = cls._entities_from_graph_property(
            graph, node, cls._get_rdf_property("generated"), Entity
        )
        # was_associated_with
        waw_objects = graph.objects(node, cls._get_rdf_property("was_associated_with"))
        was_associated_with = [Agent.from_graph(waw, graph) for waw in waw_objects]
        if not was_associated_with:
            was_associated_with = None
        elif len(was_associated_with) == 1:
            was_associated_with = was_associated_with[0]
        # was_informed_by
        was_informed_by = cls._entities_from_graph_property(
            graph, node, cls._get_rdf_property("was_informed_by"), Activity
        )
        # qualified_association
        qa_objects = graph.objects(node, cls._get_rdf_property("qualified_association"))
        qualified_association = [Association.from_graph(qa, graph) for qa in qa_objects]
        if not qualified_association:
            qualified_association = None
        elif len(qualified_association) == 1:
            qualified_association = qualified_association[0]
        # started_at_time
        started_at_time = graph.value(node, cls._get_rdf_property("started_at_time"))
        started_at_time = (
            datetime.fromisoformat(str(started_at_time)) if started_at_time else None
        )
        # qualified_usage
        qu_objects = graph.objects(node, cls._get_rdf_property("qualified_usage"))
        qualified_usage = [Usage.from_graph(qu, graph) for qu in qu_objects]
        if not qualified_usage:
            qualified_usage = None
        elif len(qualified_usage) == 1:
            qualified_usage = qualified_usage[0]
        # started_at_time
        started_at_time = graph.value(node, cls._get_rdf_property("started_at_time"))
        started_at_time = (
            datetime.fromisoformat(str(started_at_time)) if started_at_time else None
        )
        # used
        used = cls._entities_from_graph_property(
            graph, node, cls._get_rdf_property("used"), Entity
        )

        return Activity(
            **entity_dict,
            ended_at_time=ended_at_time,
            generated=generated,
            was_associated_with=was_associated_with,
            was_informed_by=was_informed_by,
            qualified_association=qualified_association,
            qualified_usage=qualified_usage,
            started_at_time=started_at_time,
            used=used,
        )


class Plan(Entity, frozen=True):
    """
    A plan is an entity that represents a set of actions or steps intended by one or more agents to achieve some goals.

    IRI: http://www.w3.org/ns/prov#Plan
    """

    rdf_type: RDFType = Entity.get_rdf_type(extra=str(rdflib.PROV.Plan))

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        node, _ = cls._node_id(id)

        # entity
        entity_dict: dict = Entity.from_graph(node, graph).model_dump()
        entity_dict.pop("rdf_type")

        return Plan(**entity_dict)


class Role(Entity, frozen=True):
    """
    A role is the function of an entity or agent with respect to an activity, in the context of a usage, generation, invalidation, association, start, and end.

    IRI: http://www.w3.org/ns/prov#Role
    """

    rdf_type: RDFType = Entity.get_rdf_type(extra=str(rdflib.PROV.Role))

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        node, _ = cls._node_id(id)

        # entity
        entity_dict: dict = Entity.from_graph(node, graph).model_dump()
        entity_dict.pop("rdf_type")

        return Role(**entity_dict)


class Location(Entity, frozen=True):
    """
    A location can be an identifiable geographic place (ISO 19112), but it can also be a non-geographic place such as a directory, row, or column. As such, there are numerous ways in which location can be expressed, such as by a coordinate, address, landmark, and so forth.

    IRI: http://www.w3.org/ns/prov#Location
    """

    rdf_type: RDFType = Entity.get_rdf_type(extra=str(rdflib.PROV.Location))

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        node, _ = cls._node_id(id)

        # entity
        entity_dict: dict = Entity.from_graph(node, graph).model_dump()
        entity_dict.pop("rdf_type")

        return Location(**entity_dict)


class InstantaneousEvent(Entity, frozen=True):
    """
    The PROV data model is implicitly based on a notion of instantaneous events (or just events), that mark transitions in the world. Events include generation, usage, or invalidation of entities, as well as starting or ending of activities. This notion of event is not first-class in the data model, but it is useful for explaining its other concepts and its semantics.

    IRI: http://www.w3.org/ns/prov#InstantaneousEvent
    """

    rdf_type: RDFType = Entity.get_rdf_type(extra=str(rdflib.PROV.InstantaneousEvent))

    at_time: Annotated[
        datetime | None,
        {"rdf_property": str(rdflib.PROV.atTime)},
    ] = None
    """The PROV data model is implicitly based on a notion of instantaneous events (or just events), that mark transitions in the world. Events include generation, usage, or invalidation of entities, as well as starting or ending of activities. This notion of event is not first-class in the data model, but it is useful for explaining its other concepts and its semantics."""

    at_location: Annotated[
        RDFRef[Location] | None,
        {"rdf_property": str(rdflib.PROV.atLocation)},
    ] = None
    """A location can be an identifiable geographic place (ISO 19112), but it can also be a non-geographic place such as a directory, row, or column. As such, there are numerous ways in which location can be expressed, such as by a coordinate, address, landmark, and so forth."""

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        node, _ = cls._node_id(id)

        # entity
        entity_dict: dict = Entity.from_graph(node, graph).model_dump()
        entity_dict.pop("rdf_type")
        # at_time
        at_time = graph.value(node, cls._get_rdf_property("at_time"))
        at_time = datetime.fromisoformat(str(at_time)) if at_time else None
        # at_location
        at_location = graph.value(node, cls._get_rdf_property("at_location"))
        at_location = Location.from_graph(at_location, graph) if at_location else None

        return InstantaneousEvent(
            **entity_dict,
            at_time=at_time,
            at_location=at_location,
        )


class Influence(Entity, frozen=True):
    """
    Influence is the capacity of an entity, activity, or agent to have an effect on the character, development, or behavior of another by means of usage, start, end, generation, invalidation, communication, derivation, attribution, association, or delegation.

    IRI: http://www.w3.org/ns/prov#Influence
    """

    rdf_type: RDFType = Entity.get_rdf_type(extra=str(rdflib.PROV.Influence))

    influencer: Annotated[
        RDFRef[Entity] | None,
        {"rdf_property": str(rdflib.PROV.influencer)},
        BeforeValidator(build_entity_validator()),
        PlainSerializer(entity_serializer),
    ] = None
    """ This property is used as part of the qualified influence pattern. Subclasses of prov:Influence use these subproperties to reference the resource (Entity, Agent, or Activity) whose influence is being qualified. """

    had_activity: Annotated[
        RDFRef[Activity] | None,
        {"rdf_property": str(rdflib.PROV.hadActivity)},
        BeforeValidator(build_entity_validator(Activity)),
        PlainSerializer(entity_serializer),
    ] = None
    """ An activity is something that occurs over a period of time and acts upon or with entities; it may include consuming, processing, transforming, modifying, relocating, using, or generating entities. """

    had_role: Annotated[
        RDFRef[Role] | None,
        {"rdf_property": str(rdflib.PROV.hadRole)},
    ] = None
    """ A role is the function of an entity or agent with respect to an activity, in the context of a usage, generation, invalidation, association, start, and end. """

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        node, _ = cls._node_id(id)

        # entity
        entity_dict: dict = Entity.from_graph(node, graph).model_dump()
        entity_dict.pop("rdf_type")
        # influencer
        influencer = cls._entity_from_graph_property(
            graph, node, cls._get_rdf_property("influencer"), Entity
        )
        # had_activity
        had_activity = cls._entity_from_graph_property(
            graph, node, cls._get_rdf_property("had_activity"), Activity
        )
        # had_role
        had_role = graph.value(node, cls._get_rdf_property("had_role"))
        had_role = Role.from_graph(had_role, graph) if had_role else None

        return Influence(
            **entity_dict,
            influencer=influencer,
            had_activity=had_activity,
            had_role=had_role,
        )


class ActivityInfluence(Influence, frozen=True):
    """
    ActivitiyInfluence is the capacity of an activity to have an effect on the character, development, or behavior of another by means of generation, invalidation, communication, or other.

    IRI: http://www.w3.org/ns/prov#ActivityInfluence
    """

    rdf_type: RDFType = Influence.get_rdf_type(extra=str(rdflib.PROV.ActivityInfluence))

    activity: Annotated[
        RDFRef[Activity],
        {"rdf_property": str(rdflib.PROV.activity)},
        BeforeValidator(build_entity_validator(Activity)),
        PlainSerializer(entity_serializer),
    ]
    """The prov:activity property references an prov:Activity which influenced a resource. This property applies to an prov:ActivityInfluence, which is given by a subproperty of prov:qualifiedInfluence from the influenced prov:Entity, prov:Activity or prov:Agent."""

    def __init__(self, **fields: Any) -> None:
        activity = fields.get("activity", None)
        if activity:
            activity = build_entity_validator(Activity)(activity)
            fields["activity"] = activity
            fields["influencer"] = activity
        super().__init__(**fields)

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        node, _ = cls._node_id(id)

        # influence
        influence_dict: dict = Influence.from_graph(node, graph).model_dump()
        influence_dict.pop("rdf_type")
        # activity
        activity = cls._entity_from_graph_property(
            graph, node, cls._get_rdf_property("activity"), Activity
        )
        if activity is None:
            raise Exception(f"{cls.__name__} must have an activity!")

        return ActivityInfluence(**influence_dict, activity=activity)


class AgentInfluence(Influence, frozen=True):
    """
    AgentInfluence is the capacity of an agent to have an effect on the character, development, or behavior of another by means of attribution, association, delegation, or other.

    IRI: http://www.w3.org/ns/prov#AgentInfluence
    """

    rdf_type: RDFType = Influence.get_rdf_type(extra=str(rdflib.PROV.AgentInfluence))

    agent: Annotated[
        RDFRef[Agent],
        {"rdf_property": str(rdflib.PROV.agent)},
        BeforeValidator(build_entity_validator(Agent)),
        PlainSerializer(entity_serializer),
    ]
    """The prov:agent property references an prov:Agent which influenced a resource. This property applies to an prov:AgentInfluence, which is given by a subproperty of prov:qualifiedInfluence from the influenced prov:Entity, prov:Activity or prov:Agent."""

    def __init__(self, **fields: Any) -> None:
        agent = fields.get("agent", None)
        if agent:
            agent = build_entity_validator(Agent)(agent)
            fields["agent"] = agent
            fields["influencer"] = agent
        super().__init__(**fields)

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        node, _ = cls._node_id(id)

        # influence
        influence_dict: dict = Influence.from_graph(node, graph).model_dump()
        influence_dict.pop("rdf_type")
        # agent
        agent = cls._entity_from_graph_property(
            graph, node, cls._get_rdf_property("agent"), Agent
        )
        if agent is None:
            raise Exception(f"{cls.__name__} must have an agent!")

        return AgentInfluence(**influence_dict, agent=agent)


class EntityInfluence(Influence, frozen=True):
    """
    EntityInfluence is the capacity of an entity to have an effect on the character, development, or behavior of another by means of usage, start, end, derivation, or other.

    IRI: http://www.w3.org/ns/prov#EntityInfluence
    """

    rdf_type: RDFType = Influence.get_rdf_type(extra=str(rdflib.PROV.EntityInfluence))

    entity: Annotated[
        RDFRef[Entity],
        {"rdf_property": str(rdflib.PROV.entity)},
        BeforeValidator(build_entity_validator(Entity)),
        PlainSerializer(entity_serializer),
    ]
    """The prov:entity property references an prov:Entity which influenced a resource. This property applies to an prov:EntityInfluence, which is given by a subproperty of prov:qualifiedInfluence from the influenced prov:Entity, prov:Activity or prov:Agent."""

    def __init__(self, **fields: Any) -> None:
        entity = fields.get("entity", None)
        if entity:
            entity = build_entity_validator(Entity)(entity)
            fields["entity"] = entity
            fields["influencer"] = entity
        super().__init__(**fields)

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        node, _ = cls._node_id(id)

        # influence
        influence_dict: dict = Influence.from_graph(node, graph).model_dump()
        influence_dict.pop("rdf_type")
        # entity
        entity = cls._entity_from_graph_property(
            graph, node, cls._get_rdf_property("entity"), Entity
        )
        if entity is None:
            raise Exception(f"{cls.__name__} must have an entity!")

        return EntityInfluence(**influence_dict, entity=entity)


class Association(AgentInfluence, frozen=True):
    """
    An activity association is an assignment of responsibility to an agent for an activity, indicating that the agent had a role in the activity. It further allows for a plan to be specified, which is the plan intended by the agent to achieve some goals in the context of this activity.

    IRI: http://www.w3.org/ns/prov#Association
    """

    rdf_type: RDFType = AgentInfluence.get_rdf_type(extra=str(rdflib.PROV.Association))

    had_plan: Annotated[
        RDFRef["Plan"] | None,
        {"rdf_property": str(rdflib.PROV.hadPlan)},
        BeforeValidator(build_entity_validator(Plan)),
        PlainSerializer(entity_serializer),
    ] = None
    """ A plan is an entity that represents a set of actions or steps intended by one or more agents to achieve some goals. """

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        node, _ = cls._node_id(id)

        # entity
        influence_dict: dict = AgentInfluence.from_graph(node, graph).model_dump()
        influence_dict.pop("rdf_type")
        # had_plan
        had_plan = cls._entity_from_graph_property(
            graph, node, cls._get_rdf_property("had_plan"), Plan
        )

        return Association(**influence_dict, had_plan=had_plan)


class Generation(ActivityInfluence, InstantaneousEvent, frozen=True):
    """
    Generation is the completion of production of a new entity by an activity. This entity did not exist before generation and becomes available for usage after this generation

    IRI: http://www.w3.org/ns/prov#Generation
    """

    rdf_type: RDFType = ActivityInfluence.get_rdf_type(
        extra=str(rdflib.PROV.Generation)
    )

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        node, _ = cls._node_id(id)

        # influence
        influence_dict: dict = ActivityInfluence.from_graph(node, graph).model_dump()
        influence_dict.pop("rdf_type")
        # event
        event_dict: dict = InstantaneousEvent.from_graph(node, graph).model_dump()
        event_dict.pop("rdf_type")
        # merge
        influence_dict["rdf_bindings"].extend(event_dict["rdf_bindings"])
        distinct_keys = set(event_dict.keys()).difference(influence_dict.keys())
        for k in distinct_keys:
            influence_dict[k] = event_dict[k]

        return Generation(**influence_dict)


class Usage(EntityInfluence, InstantaneousEvent, frozen=True):
    """
    Usage is the beginning of utilizing an entity by an activity. Before usage, the activity had not begun to utilize this entity and could not have been affected by the entity

    IRI: http://www.w3.org/ns/prov#Usage
    """

    rdf_type: RDFType = EntityInfluence.get_rdf_type(extra=str(rdflib.PROV.Usage))

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        node, _ = cls._node_id(id)

        # influence
        influence_dict: dict = EntityInfluence.from_graph(node, graph).model_dump()
        influence_dict.pop("rdf_type")
        # event
        event_dict: dict = InstantaneousEvent.from_graph(node, graph).model_dump()
        event_dict.pop("rdf_type")
        # merge
        influence_dict["rdf_bindings"].extend(event_dict["rdf_bindings"])
        distinct_keys = set(event_dict.keys()).difference(influence_dict.keys())
        for k in distinct_keys:
            influence_dict[k] = event_dict[k]

        return Usage(**influence_dict)
