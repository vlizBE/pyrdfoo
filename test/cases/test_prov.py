from datetime import UTC, datetime, timedelta

from rdfoo import prov
from rdfoo.rdf import RDFURIRef

from utils import RDFTestCase


class TestEntity(RDFTestCase):

    def test_create(self):
        base_entity = prov.Entity(
            rdf_id="base",
            title="The base entity!",
        )
        entity = prov.Entity(
            rdf_id="entity",
            title="The deriving entity",
            was_derived_from=base_entity,
        )
        self.assertRDFType(entity, "http://www.w3.org/ns/prov#Entity")

    def test_from_graph(self):
        base_entity = prov.Entity(
            rdf_id="base",
            title="The base entity!",
        )
        entity_id = "entity"
        ref_entity = prov.Entity(
            rdf_id=entity_id,
            title="The deriving entity",
            was_derived_from=base_entity,
        )
        graph = ref_entity.to_graph()
        entity = prov.Entity.from_graph(entity_id, graph)
        self.assertEqual(ref_entity, entity)

    def test_from_graph_with_activity(self):
        now = datetime.now(UTC)
        base_activity = prov.Activity(
            rdf_id="base",
            title="The base activity!",
            ended_at_time=now - timedelta(seconds=95),
            started_at_time=now - timedelta(seconds=100),
        )
        activity_id = "activity"
        ref_activity = prov.Activity(
            rdf_id=activity_id,
            title="The deriving activity",
            was_derived_from=base_activity,
            ended_at_time=now - timedelta(seconds=85),
            started_at_time=now - timedelta(seconds=90),
        )
        graph = ref_activity.to_graph()
        activity = prov.Activity.from_graph(activity_id, graph)
        self.assertEqual(ref_activity, activity)

    def test_from_graph_with_attribution(self):
        entity_id = "entity"
        agent = prov.Agent(rdf_id="https://marineinfo.org/id/person/45562/")
        ref_entity = prov.Entity(rdf_id=entity_id, was_attributed_to=agent)
        graph = ref_entity.to_graph()
        entity = prov.Entity.from_graph(entity_id, graph)
        self.assertEqual(ref_entity, entity)


class TestActivity(RDFTestCase):

    def test_create_activity(self):
        now = datetime.now(UTC)
        activity = prov.Activity(
            rdf_id="work",
            ended_at_time=now - timedelta(seconds=95),
            started_at_time=now - timedelta(seconds=100),
        )
        self.assertRDFType(activity, "http://www.w3.org/ns/prov#Activity")

    def test_from_graph(self):
        id = "work"
        now = datetime.now(UTC)
        ref_activity = prov.Activity(
            rdf_id=id,
            ended_at_time=now - timedelta(seconds=95),
            started_at_time=now - timedelta(seconds=100),
        )
        graph = ref_activity.to_graph()
        activity = prov.Activity.from_graph(id, graph)
        self.assertEqual(ref_activity, activity)

    def test_from_graph_with_informed_by(self):
        activity_id = "work"
        now = datetime.now(UTC)
        informed_activity = prov.Activity(rdf_id="eat")
        ref_activity = prov.Activity(
            rdf_id=activity_id,
            was_informed_by=informed_activity,
            ended_at_time=now - timedelta(seconds=95),
            started_at_time=now - timedelta(seconds=100),
        )
        graph = ref_activity.to_graph()
        activity = prov.Activity.from_graph(activity_id, graph)
        self.assertEqual(ref_activity, activity)

    def test_from_graph_with_derived_from(self):
        activity_id = "work"
        now = datetime.now(UTC)
        derived_entity = prov.Entity(rdf_id="thing")
        informed_activity = prov.Activity(rdf_id="eat")
        ref_activity = prov.Activity(
            rdf_id=activity_id,
            was_derived_from=derived_entity,
            was_informed_by=informed_activity,
            ended_at_time=now - timedelta(seconds=95),
            started_at_time=now - timedelta(seconds=100),
        )
        graph = ref_activity.to_graph()
        activity = prov.Activity.from_graph(activity_id, graph)
        self.assertEqual(ref_activity, activity)

    def test_from_graph_with_association(self):
        activity_id = "pipeline"
        now = datetime.now(UTC)
        agent = prov.Agent(rdf_id="https://marineinfo.org/id/person/45562/")
        agent_activity = prov.Activity(rdf_id="triggered")
        plan = prov.Plan(rdf_id="script")
        agent_role = prov.Role(rdf_id="owner")
        association = prov.Association(
            rdf_id="association",
            agent=agent,
            had_activity=agent_activity,
            had_plan=plan,
            had_role=agent_role,
        )
        ref_activity = prov.Activity(
            rdf_id=activity_id,
            was_associated_with=agent,
            qualified_association=association,
            ended_at_time=now - timedelta(seconds=95),
            started_at_time=now - timedelta(seconds=100),
        )
        graph = ref_activity.to_graph()
        activity = prov.Activity.from_graph(activity_id, graph)
        self.assertEqual(ref_activity, activity)

    def test_from_graph_with_multiple_association(self):
        activity_id = "pipeline"
        now = datetime.now(UTC)
        agent1 = prov.Agent(rdf_id="https://marineinfo.org/id/person/45562/")
        agent2 = prov.Agent(rdf_id="https://marineinfo.org/id/person/45563/")
        agent_activity = prov.Activity(rdf_id="triggered")
        plan = prov.Plan(rdf_id="script")
        agent_role = prov.Role(rdf_id="owner")
        association1 = prov.Association(
            rdf_id="association1",
            agent=agent1,
            had_activity=agent_activity,
            had_plan=plan,
            had_role=agent_role,
        )
        association2 = prov.Association(
            rdf_id="association2",
            agent=agent2,
            had_activity=agent_activity,
            had_plan=plan,
            had_role=agent_role,
        )
        ref_activity = prov.Activity(
            rdf_id=activity_id,
            was_associated_with=[agent1, agent2],
            qualified_association=[association1, association2],
            ended_at_time=now - timedelta(seconds=95),
            started_at_time=now - timedelta(seconds=100),
        )
        graph = ref_activity.to_graph()
        activity = prov.Activity.from_graph(activity_id, graph)
        self.assertEqual(ref_activity, activity)

    def test_from_graph_with_influence(self):
        activity_id = "sleep"
        eat = prov.Activity(rdf_id="eat")
        rave = prov.Activity(rdf_id="rave")
        ref_activity = prov.Activity(
            rdf_id=activity_id, was_influenced_by=eat, influenced=rave
        )
        graph = ref_activity.to_graph()
        activity = prov.Activity.from_graph(activity_id, graph)
        self.assertEqual(ref_activity, activity)


class TestAgent(RDFTestCase):

    def test_create_agent(self):
        agent = prov.Agent(
            rdf_id="https://marineinfo.org/id/person/45562/",
            name="Bram Van der Streeck",
            mbox=RDFURIRef(uri="mailto:bram.van.der.streeck@vliz.be"),
        )
        self.assertRDFType(agent, "http://www.w3.org/ns/prov#Agent")

    def test_from_graph(self):
        agent_id = "https://marineinfo.org/id/person/45562/"
        ref_agent = prov.Agent(
            rdf_id=agent_id,
            name="Bram Van der Streeck",
            mbox="bram.van.der.streeck@vliz.be",
        )
        graph = ref_agent.to_graph()
        agent = prov.Agent.from_graph(agent_id, graph)
        self.assertEqual(ref_agent, agent)

    def test_from_graph_with_mail_uri(self):
        agent_id = "https://marineinfo.org/id/person/45562/"
        ref_agent = prov.Agent(
            rdf_id=agent_id,
            name="Bram Van der Streeck",
            mbox=RDFURIRef(uri="mailto:bram.van.der.streeck@vliz.be"),
        )
        graph = ref_agent.to_graph()
        agent = prov.Agent.from_graph(agent_id, graph)
        self.assertEqual(ref_agent, agent)

    def test_from_graph_with_on_behalf(self):
        org_id = "https://marineinfo.org/id/institute/36/"
        ref_org = prov.Agent(
            rdf_id=org_id,
            name="VLIZ (Vlaams Instituut voor de Zee)",
            mbox=RDFURIRef(uri="mailto:info@vliz.be"),
        )
        agent_id = "https://marineinfo.org/id/person/45562/"
        ref_agent = prov.Agent(
            rdf_id=agent_id,
            name="Bram Van der Streeck",
            mbox=RDFURIRef(uri="mailto:bram.van.der.streeck@vliz.be"),
            acted_on_behalf_of=ref_org,
        )
        graph = ref_agent.to_graph()
        agent = prov.Agent.from_graph(agent_id, graph)
        self.assertEqual(ref_agent, agent)


class TestRole(RDFTestCase):

    def test_create(self):
        role = prov.Role(
            rdf_id="software_engineer",
            title="Software Engineer",
            description="A software engineer applies a software development process to define, implement, test, manage, and maintain software systems.",
        )
        self.assertRDFType(role, "http://www.w3.org/ns/prov#Role")

    def test_from_graph(self):
        role_id = "software_engineer"
        ref_role = prov.Role(
            rdf_id=role_id,
            title="Software Engineer",
        )
        graph = ref_role.to_graph()
        role = prov.Role.from_graph(role_id, graph)
        self.assertEqual(ref_role, role)

    def test_from_graph_with_description(self):
        role_id = "software_engineer"
        ref_role = prov.Role(
            rdf_id=role_id,
            title="Software Engineer",
            description="A software engineer applies a software development process to define, implement, test, manage, and maintain software systems.",
        )
        graph = ref_role.to_graph()
        role = prov.Role.from_graph(role_id, graph)
        self.assertEqual(ref_role, role)

    def test_from_graph_with_multiple(self):
        role_id = "software_engineer"
        ref_role = prov.Role(
            rdf_id=role_id,
            title=["Software Engineer", "Software Ingenieur"],
            description=[
                "A software engineer applies a software development process to define, implement, test, manage, and maintain software systems.",
                "Een software-engineer past een softwareontwikkelingsproces toe om softwaresystemen te definiëren, implementeren, testen, beheren en onderhouden.",
            ],
        )
        graph = ref_role.to_graph()
        role = prov.Role.from_graph(role_id, graph)
        self.assertEqual(ref_role, role)


class TestLocation(RDFTestCase):

    def test_create(self):
        location = prov.Location(rdf_id="http://marineregions.org/mrgid/57661")
        self.assertRDFType(location, "http://www.w3.org/ns/prov#Location")


class TestInstantaneousEvent(RDFTestCase):

    def test_create(self):
        location = prov.Location(rdf_id="http://marineregions.org/mrgid/57661")
        event = prov.InstantaneousEvent(
            rdf_id="event", at_time=datetime.now(UTC), at_location=location
        )
        self.assertRDFType(event, "http://www.w3.org/ns/prov#InstantaneousEvent")

    def test_from_graph(self):
        location = prov.Location(rdf_id="http://marineregions.org/mrgid/57661")
        event_id = "event"
        ref_event = prov.InstantaneousEvent(
            rdf_id=event_id, at_time=datetime.now(UTC), at_location=location
        )
        graph = ref_event.to_graph()
        event = prov.InstantaneousEvent.from_graph(event_id, graph)
        self.assertEqual(ref_event, event)


class TestInfluence(RDFTestCase):

    def test_create(self):
        activity = prov.Activity(
            rdf_id="work",
            started_at_time=datetime.now(UTC),
            ended_at_time=datetime.now(UTC),
        )
        role = prov.Role(
            rdf_id="software_engineer",
        )
        influence = prov.Influence(
            rdf_id="influence",
            had_activity=activity,
            had_role=role,
        )
        self.assertRDFType(influence, "http://www.w3.org/ns/prov#Influence")

    def test_from_graph(self):
        activity = prov.Activity(
            rdf_id="work",
            started_at_time=datetime.now(UTC),
            ended_at_time=datetime.now(UTC),
        )
        role = prov.Role(
            rdf_id="software_engineer",
        )
        influence_id = "influence"
        ref_influence = prov.Influence(
            rdf_id=influence_id,
            had_activity=activity,
            had_role=role,
        )
        graph = ref_influence.to_graph()
        influence = prov.Influence.from_graph(influence_id, graph)
        self.assertEqual(ref_influence, influence)

    def test_from_graph_with_influencer(self):
        agent = prov.Agent(
            rdf_id="https://marineinfo.org/id/person/45562/",
        )
        activity = prov.Activity(
            rdf_id="work",
            started_at_time=datetime.now(UTC),
            ended_at_time=datetime.now(UTC),
        )
        role = prov.Role(
            rdf_id="software_engineer",
        )
        influence_id = "influence"
        ref_influence = prov.Influence(
            rdf_id=influence_id,
            influencer=agent,
            had_activity=activity,
            had_role=role,
        )
        graph = ref_influence.to_graph()
        influence = prov.Influence.from_graph(influence_id, graph)
        self.assertEqual(ref_influence, influence)


class TestActivityInfluence(RDFTestCase):

    def test_create(self):
        influence_activity = prov.Activity(rdf_id="eat")
        activity = prov.Activity(
            rdf_id="work",
            started_at_time=datetime.now(UTC),
            ended_at_time=datetime.now(UTC),
        )
        role = prov.Role(
            rdf_id="work_completed",
        )
        influence = prov.ActivityInfluence(
            rdf_id="influence",
            activity=influence_activity,
            had_activity=activity,
            had_role=role,
        )
        self.assertRDFType(influence, "http://www.w3.org/ns/prov#ActivityInfluence")

    def test_from_graph(self):
        influence_activity = prov.Activity(rdf_id="eat")
        activity = prov.Activity(
            rdf_id="work",
            started_at_time=datetime.now(UTC),
            ended_at_time=datetime.now(UTC),
        )
        role = prov.Role(
            rdf_id="work_completed",
        )
        influence_id = "influence"
        ref_influence = prov.ActivityInfluence(
            rdf_id=influence_id,
            activity=influence_activity,
            had_activity=activity,
            had_role=role,
        )
        graph = ref_influence.to_graph()
        influence = prov.ActivityInfluence.from_graph(influence_id, graph)
        self.assertEqual(ref_influence, influence)


class TestAgentInfluence(RDFTestCase):

    def test_create(self):
        activity = prov.Activity(
            rdf_id="work",
            started_at_time=datetime.now(UTC),
            ended_at_time=datetime.now(UTC),
        )
        agent = prov.Agent(
            rdf_id="https://marineinfo.org/id/person/45562/",
            name="Bram Van der Streeck",
        )
        role = prov.Role(
            rdf_id="software_engineer",
        )
        influence = prov.AgentInfluence(
            rdf_id="influence",
            agent=agent,
            had_activity=activity,
            had_role=role,
        )
        self.assertRDFType(influence, "http://www.w3.org/ns/prov#AgentInfluence")

    def test_from_graph(self):
        activity = prov.Activity(
            rdf_id="work",
            started_at_time=datetime.now(UTC),
            ended_at_time=datetime.now(UTC),
        )
        agent = prov.Agent(
            rdf_id="https://marineinfo.org/id/person/45562/",
            name="Bram Van der Streeck",
        )
        role = prov.Role(
            rdf_id="software_engineer",
        )
        influence_id = "influence"
        ref_influence = prov.AgentInfluence(
            rdf_id=influence_id,
            agent=agent,
            had_activity=activity,
            had_role=role,
        )
        graph = ref_influence.to_graph()
        influence = prov.AgentInfluence.from_graph(influence_id, graph)
        self.assertEqual(ref_influence, influence)


class TestEntityInfluence(RDFTestCase):

    def test_create(self):
        activity = prov.Activity(
            rdf_id="work",
            started_at_time=datetime.now(UTC),
            ended_at_time=datetime.now(UTC),
        )
        entity = prov.Entity(
            rdf_id="thing",
        )
        role = prov.Role(
            rdf_id="thingifier",
        )
        influence = prov.EntityInfluence(
            rdf_id="influence",
            entity=entity,
            had_activity=activity,
            had_role=role,
        )
        self.assertRDFType(influence, "http://www.w3.org/ns/prov#EntityInfluence")

    def test_from_graph(self):
        activity = prov.Activity(
            rdf_id="work",
            started_at_time=datetime.now(UTC),
            ended_at_time=datetime.now(UTC),
        )
        entity = prov.Entity(
            rdf_id="thing",
        )
        role = prov.Role(
            rdf_id="thingifier",
        )
        influence_id = "influence"
        ref_influence = prov.EntityInfluence(
            rdf_id=influence_id,
            entity=entity,
            had_activity=activity,
            had_role=role,
        )
        graph = ref_influence.to_graph()
        influence = prov.EntityInfluence.from_graph(influence_id, graph)
        self.assertEqual(ref_influence, influence)


class TestAssociation(RDFTestCase):

    def test_create(self):
        activity = prov.Activity(
            rdf_id="work",
            started_at_time=datetime.now(UTC),
            ended_at_time=datetime.now(UTC),
        )
        agent = prov.Agent(
            rdf_id="https://marineinfo.org/id/person/45562/",
            name="Bram Van der Streeck",
        )
        role = prov.Role(
            rdf_id="software_engineer",
        )
        association = prov.Association(
            rdf_id="bram_software_engineer",
            had_activity=activity,
            agent=agent,
            had_role=role,
        )
        self.assertRDFType(association, "http://www.w3.org/ns/prov#Association")

    def test_from_graph(self):
        activity = prov.Activity(
            rdf_id="work",
            started_at_time=datetime.now(UTC),
            ended_at_time=datetime.now(UTC),
        )
        agent = prov.Agent(
            rdf_id="https://marineinfo.org/id/person/45562/",
            name="Bram Van der Streeck",
        )
        role = prov.Role(
            rdf_id="software_engineer",
        )
        association_id = "bram_software_engineer"
        ref_association = prov.Association(
            rdf_id=association_id,
            had_activity=activity,
            agent=agent,
            had_role=role,
        )
        graph = ref_association.to_graph()
        association = prov.Association.from_graph(association_id, graph)
        self.assertEqual(ref_association, association)

    def test_from_graph_with_plan(self):
        activity = prov.Activity(
            rdf_id="work",
            started_at_time=datetime.now(UTC),
            ended_at_time=datetime.now(UTC),
        )
        agent = prov.Agent(
            rdf_id="https://marineinfo.org/id/person/45562/",
            name="Bram Van der Streeck",
        )
        plan = prov.Plan(
            rdf_id="my_plan",
        )
        role = prov.Role(
            rdf_id="software_engineer",
        )
        association_id = "bram_software_engineer"
        ref_association = prov.Association(
            rdf_id=association_id,
            had_activity=activity,
            agent=agent,
            had_plan=plan,
            had_role=role,
        )
        graph = ref_association.to_graph()
        association = prov.Association.from_graph(association_id, graph)
        self.assertEqual(ref_association, association)


class TestGeneration(RDFTestCase):

    def test_create(self):
        influence_activity = prov.Activity(rdf_id="eat")
        location = prov.Location(rdf_id="http://marineregions.org/mrgid/57661")
        activity = prov.Activity(
            rdf_id="work",
            started_at_time=datetime.now(UTC),
            ended_at_time=datetime.now(UTC),
        )
        role = prov.Role(
            rdf_id="work_completed",
        )
        generation = prov.Generation(
            rdf_id="generation",
            activity=influence_activity,
            had_activity=activity,
            had_role=role,
            at_location=location,
            at_time=datetime.now(UTC),
        )
        self.assertRDFType(generation, "http://www.w3.org/ns/prov#Generation")

    def test_from_graph(self):
        influence_activity = prov.Activity(rdf_id="eat")
        location = prov.Location(rdf_id="http://marineregions.org/mrgid/57661")
        activity = prov.Activity(
            rdf_id="work",
            started_at_time=datetime.now(UTC),
            ended_at_time=datetime.now(UTC),
        )
        role = prov.Role(
            rdf_id="work_completed",
        )
        generation_id = "generation"
        ref_generation = prov.Generation(
            rdf_id=generation_id,
            activity=influence_activity,
            had_activity=activity,
            had_role=role,
            at_location=location,
            at_time=datetime.now(UTC),
        )
        graph = ref_generation.to_graph()
        generation = prov.Generation.from_graph(generation_id, graph)
        self.assertEqual(ref_generation, generation)


class TestUsage(RDFTestCase):

    def test_create(self):
        influence_entity = prov.Entity(rdf_id="entity")
        location = prov.Location(rdf_id="http://marineregions.org/mrgid/57661")
        activity = prov.Activity(
            rdf_id="work",
            started_at_time=datetime.now(UTC),
            ended_at_time=datetime.now(UTC),
        )
        role = prov.Role(
            rdf_id="work_completed",
        )
        usage = prov.Usage(
            rdf_id="usage",
            entity=influence_entity,
            had_activity=activity,
            had_role=role,
            at_location=location,
            at_time=datetime.now(UTC),
        )
        self.assertRDFType(usage, "http://www.w3.org/ns/prov#Usage")

    def test_from_graph(self):
        influence_entity = prov.Entity(rdf_id="entity")
        location = prov.Location(rdf_id="http://marineregions.org/mrgid/57661")
        activity = prov.Activity(
            rdf_id="work",
            started_at_time=datetime.now(UTC),
            ended_at_time=datetime.now(UTC),
        )
        role = prov.Role(
            rdf_id="work_completed",
        )
        usage_id = "usage"
        ref_usage = prov.Usage(
            rdf_id=usage_id,
            entity=influence_entity,
            had_activity=activity,
            had_role=role,
            at_location=location,
            at_time=datetime.now(UTC),
        )
        graph = ref_usage.to_graph()
        usage = prov.Usage.from_graph(usage_id, graph)
        self.assertEqual(ref_usage, usage)
