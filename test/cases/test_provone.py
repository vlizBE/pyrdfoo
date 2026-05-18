from datetime import datetime, timedelta, UTC

from utils import RDFTestCase

from rdfoo import prov, provone
from rdfoo.rdf import RDFURIRef
from rdfoo.vliz import Dataset


class TestController(RDFTestCase):

    def test_create(self):
        program = provone.Program(rdf_id="pipeline", version="0.1.0")
        controller = provone.Controller(
            rdf_id="airflow", controls=program, version="0.1.0"
        )
        self.assertRDFType(
            controller, "http://purl.dataone.org/provone/2015/01/15/ontology#Controller"
        )

    def test_from_graph(self):
        program = provone.Program(rdf_id="pipeline", version="0.1.0")
        controller_id = "airflow"
        ref_controller = provone.Controller(
            rdf_id="airflow", controls=program, version="0.1.0"
        )
        graph = ref_controller.to_graph()
        controller = provone.Controller.from_graph(controller_id, graph)
        self.assertEqual(ref_controller, controller)

    def test_from_graph_with_sub_program(self):
        job = provone.Program(rdf_id="job")
        program = provone.Program(
            rdf_id="pipeline", has_sub_program=job, version="0.1.0"
        )
        controller_id = "airflow"
        ref_controller = provone.Controller(
            rdf_id="airflow", controls=program, version="0.1.0"
        )
        graph = ref_controller.to_graph()
        controller = provone.Controller.from_graph(controller_id, graph)
        self.assertEqual(ref_controller, controller)


class TestExecution(RDFTestCase):

    def test_create(self):
        now = datetime.now(UTC)
        execution = provone.Execution(
            rdf_id=f"run_{now.isoformat()}",
            started_at_time=now,
            ended_at_time=now + timedelta(seconds=5),
        )
        self.assertRDFType(
            execution, "http://purl.dataone.org/provone/2015/01/15/ontology#Execution"
        )

    def test_from_graph(self):
        now = datetime.now(UTC)
        instigator = provone.Execution(
            rdf_id=f"pipeline_run_{now.isoformat()}",
            started_at_time=now,
            ended_at_time=now + timedelta(seconds=10),
        )
        execution_id = f"job_run_{now.isoformat()}"
        ref_execution = provone.Execution(
            rdf_id=execution_id,
            started_at_time=now,
            ended_at_time=now + timedelta(seconds=5),
            was_part_of=instigator,
        )
        graph = ref_execution.to_graph()
        execution = provone.Execution.from_graph(execution_id, graph)
        self.assertEqual(ref_execution, execution)

    def test_from_graph_with_association(self):
        now = datetime.now(UTC)
        agent = prov.Agent(rdf_id="https://marineinfo.org/id/person/45562/")
        plan = provone.Program(rdf_id="pipeline")
        role = prov.Role(rdf_id="data_engineer")
        association = prov.Association(
            rdf_id="bram_de", agent=agent, had_plan=plan, had_role=role
        )
        execution_id = f"run_{now.isoformat()}"
        ref_execution = provone.Execution(
            rdf_id=execution_id,
            started_at_time=now,
            ended_at_time=now + timedelta(seconds=5),
            was_associated_with=agent,
            qualified_association=association,
        )
        graph = ref_execution.to_graph()
        execution = provone.Execution.from_graph(execution_id, graph)
        self.assertEqual(ref_execution, execution)

    def test_from_graph_with_generated(self):
        now = datetime.now(UTC)
        execution_id = f"run_{now.isoformat()}"
        dataset = Dataset(rdf_id="dataset", description="A dataset", title="My Dataset")
        ref_execution = provone.Execution(
            rdf_id=execution_id,
            started_at_time=now,
            ended_at_time=now + timedelta(seconds=5),
            generated=dataset,
        )
        graph = ref_execution.to_graph()
        execution = provone.Execution.from_graph(execution_id, graph)
        self.assertEqual(ref_execution, execution)

    def test_from_graph_with_used(self):
        now = datetime.now(UTC)
        execution_id = f"run_{now.isoformat()}"
        dataset = Dataset(rdf_id="dataset", description="A dataset", title="My Dataset")
        usage = prov.Usage(rdf_id="usage", entity=dataset)
        ref_execution = provone.Execution(
            rdf_id=execution_id,
            started_at_time=now,
            ended_at_time=now + timedelta(seconds=5),
            used=dataset,
            qualified_usage=usage,
        )
        graph = ref_execution.to_graph()
        execution = provone.Execution.from_graph(execution_id, graph)
        self.assertEqual(ref_execution, execution)

    def test_from_graph_with_was_informed_by(self):
        now = datetime.now(UTC)
        execution_id = f"run_{now.isoformat()}"
        informed_by = provone.Execution(
            rdf_id=f"run_{(now - timedelta(seconds=5)).isoformat()}"
        )
        ref_execution = provone.Execution(
            rdf_id=execution_id,
            started_at_time=now,
            ended_at_time=now + timedelta(seconds=5),
            was_informed_by=informed_by,
        )
        graph = ref_execution.to_graph()
        execution = provone.Execution.from_graph(execution_id, graph)
        self.assertEqual(ref_execution, execution)

    def test_from_graph_with_was_part_of(self):
        now = datetime.now(UTC)
        execution_id = f"run_{now.isoformat()}"
        part_of = provone.Execution(
            rdf_id=f"run_{(now - timedelta(seconds=5)).isoformat()}",
            started_at_time=now - timedelta(seconds=5),
            ended_at_time=now + timedelta(seconds=10),
        )
        ref_execution = provone.Execution(
            rdf_id=execution_id,
            started_at_time=now,
            ended_at_time=now + timedelta(seconds=5),
            was_part_of=part_of,
        )
        graph = ref_execution.to_graph()
        execution = provone.Execution.from_graph(execution_id, graph)
        self.assertEqual(ref_execution, execution)


class TestProgram(RDFTestCase):

    def test_create(self):
        program = provone.Program(rdf_id="pipeline", version="0.1.0")
        self.assertRDFType(
            program, "http://purl.dataone.org/provone/2015/01/15/ontology#Program"
        )

    def test_from_graph(self):
        program_id = "pipeline"
        ref_program = provone.Program(
            rdf_id=program_id,
            version="0.1.0",
            url=RDFURIRef(uri="https://my.domain.org/pipeline/pipeline"),
        )
        graph = ref_program.to_graph()
        program = provone.Program.from_graph(program_id, graph)
        self.assertEqual(ref_program, program)

    def test_from_graph_with_sub_program(self):
        program_id = "pipeline"
        job = provone.Program(
            rdf_id="job",
            version="0.1.0",
            url=RDFURIRef(uri="https://my.domain.org/pipeline/pipeline/jobs/job"),
        )
        ref_program = provone.Program(
            rdf_id=program_id,
            has_sub_program=job,
            version="0.1.0",
            url=RDFURIRef(uri="https://my.domain.org/pipeline/pipeline"),
        )
        graph = ref_program.to_graph()
        program = provone.Program.from_graph(program_id, graph)
        self.assertEqual(ref_program, program)

    def test_from_graph_with_is_sub_program(self):
        program_id = "job"
        job = provone.Workflow(
            rdf_id="pipeline",
            version="0.1.0",
            url=RDFURIRef(uri="https://my.domain.org/pipeline/pipeline/jobs/job"),
        )
        ref_program = provone.Program(
            rdf_id=program_id,
            is_sub_program_of=job,
            version="0.1.0",
            url=RDFURIRef(uri="https://my.domain.org/pipeline/pipeline"),
        )
        graph = ref_program.to_graph()
        program = provone.Program.from_graph(program_id, graph)
        self.assertEqual(ref_program, program)

    def test_from_graph_with_derived_from(self):
        program_id = "pipeline_v0.1.1"
        old_program = provone.Program(
            rdf_id="pipeline_v0.1.0",
            version="0.1.0",
            url=RDFURIRef(uri="https://my.domain.org/pipeline/pipeline"),
        )
        ref_program = provone.Program(
            rdf_id=program_id,
            version="0.1.1",
            url=RDFURIRef(uri="https://my.domain.org/pipeline/pipeline"),
            was_derived_from=old_program,
        )
        graph = ref_program.to_graph()
        program = provone.Program.from_graph(program_id, graph)
        self.assertEqual(ref_program, program)

    def test_from_graph_with_influence(self):
        program_id = "pipeline"
        upstream = provone.Program(rdf_id="upstream")
        downstream = provone.Program(rdf_id="downstream")
        ref_program = provone.Program(
            rdf_id=program_id, was_influenced_by=upstream, influenced=downstream
        )
        graph = ref_program.to_graph()
        program = provone.Program.from_graph(program_id, graph)
        self.assertEqual(ref_program, program)


class TestWorkflow(RDFTestCase):

    def test_create(self):
        program = provone.Workflow(rdf_id="pipeline", version="0.1.0")
        self.assertRDFType(
            program, "http://purl.dataone.org/provone/2015/01/15/ontology#Workflow"
        )

    def test_from_graph(self):
        workflow_id = "pipeline"
        ref_workflow = provone.Workflow(
            rdf_id=workflow_id,
            version="0.1.0",
            url=RDFURIRef(uri="https://my.domain.org/pipeline/pipeline"),
        )
        graph = ref_workflow.to_graph()
        workflow = provone.Workflow.from_graph(workflow_id, graph)
        self.assertEqual(ref_workflow, workflow)

    def test_from_graph_with_sub_program(self):
        workflow_id = "pipeline"
        job = provone.Program(
            rdf_id="job",
            version="0.1.0",
            url=RDFURIRef(uri="https://my.domain.org/pipeline/pipeline/jobs/job"),
        )
        ref_workflow = provone.Workflow(
            rdf_id=workflow_id,
            has_sub_program=job,
            version="0.1.0",
            url=RDFURIRef(uri="https://my.domain.org/pipeline/pipeline"),
        )
        graph = ref_workflow.to_graph()
        workflow = provone.Workflow.from_graph(workflow_id, graph)
        self.assertEqual(ref_workflow, workflow)

    def test_from_graph_with_derived_from(self):
        workflow_id = "pipeline_v0.1.1"
        old_workflow = provone.Workflow(
            rdf_id="pipeline_v0.1.0",
            version="0.1.0",
            url=RDFURIRef(uri="https://my.domain.org/pipeline/pipeline"),
        )
        ref_workflow = provone.Workflow(
            rdf_id=workflow_id,
            version="0.1.0",
            url=RDFURIRef(uri="https://my.domain.org/pipeline/pipeline"),
            was_derived_from=old_workflow,
        )
        graph = ref_workflow.to_graph()
        workflow = provone.Workflow.from_graph(workflow_id, graph)
        self.assertEqual(ref_workflow, workflow)
