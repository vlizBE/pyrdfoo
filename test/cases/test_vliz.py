from datetime import datetime, timedelta, UTC

from utils import RDFTestCase

from rdfoo import prov, provone, vliz


class TestController(RDFTestCase):

    def test_create(self):
        dataset = vliz.Dataset(
            rdf_id="dataset", title="My dataset.", description="Just a dataset."
        )
        self.assertRDFType(dataset, "http://www.w3.org/ns/sosa/ObservationCollection")

    def test_from_graph(self):
        dataset_id = "dataset"
        ref_dataset = vliz.Dataset(
            rdf_id=dataset_id, title="My dataset.", description="Just a dataset."
        )
        graph = ref_dataset.to_graph()
        dataset = vliz.Dataset.from_graph(dataset_id, graph)
        self.assertEqual(ref_dataset, dataset)

    def test_from_graph_with_generated_by(self):
        now = datetime.now(UTC)
        dataset_id = "dataset"
        execution1 = provone.Execution(rdf_id=f"run_{now.isoformat()}")
        execution2 = provone.Execution(
            rdf_id=f"run_{(now - timedelta(seconds=5)).isoformat()}"
        )
        generation1 = prov.Generation(
            rdf_id="generation1", activity=execution1, at_time=now
        )
        generation2 = prov.Generation(
            rdf_id="generation2",
            activity=execution2,
            at_time=now - timedelta(seconds=5),
        )
        ref_dataset = vliz.Dataset(
            rdf_id=dataset_id,
            title="My dataset.",
            description="Just a dataset.",
            was_generated_by=[execution1, execution2],
            qualified_generation=[generation1, generation2],
        )
        graph = ref_dataset.to_graph()
        dataset = vliz.Dataset.from_graph(dataset_id, graph)
        self.assertEqual(ref_dataset, dataset)

    def test_from_graph_with_used_by(self):
        now = datetime.now(UTC)
        dataset_id = "dataset"
        execution1 = provone.Execution(rdf_id=f"run_{now.isoformat()}")
        execution2 = provone.Execution(
            rdf_id=f"run_{(now - timedelta(seconds=5)).isoformat()}"
        )
        ref_dataset = vliz.Dataset(
            rdf_id=dataset_id,
            title="My dataset.",
            description="Just a dataset.",
            was_used_by=[execution1, execution2],
        )
        graph = ref_dataset.to_graph()
        dataset = vliz.Dataset.from_graph(dataset_id, graph)
        self.assertEqual(ref_dataset, dataset)
