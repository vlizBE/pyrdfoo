import unittest

from rdflib import Literal
from rdfoo import dcat

from utils import RDFTestCase


class TestDCAT(RDFTestCase):

    def test_create_catalogue(self):
        obj = dcat.Catalogue()
        self.assertRDFType(obj, "https://www.w3.org/ns/dcat#Catalog")

    def test_create_catalogued_resource(self):
        obj = dcat.CataloguedResource()
        self.assertRDFType(obj, "https://www.w3.org/ns/dcat#Resource")

    def test_create_dataset(self):
        obj = dcat.Dataset()
        self.assertRDFType(obj, "https://www.w3.org/ns/dcat#Dataset")

    def test_create_distribution(self):
        obj = dcat.Distribution()
        self.assertRDFType(obj, "http://www.w3.org/ns/dcat#Distribution")

    def test_create_period_of_time(self):
        obj = dcat.PeriodOfTime()
        self.assertRDFType(obj, "http://purl.org/dc/terms/PeriodOfTime")

    def test_create_location(self):
        obj = dcat.Location()
        self.assertRDFType(obj, "http://purl.org/dc/terms/Location")

    def test_from_graph_000(self):
        # no identifier should lead to a blank node.
        title = "unidentified catalogue"
        catalogue0 = dcat.Catalogue(title=title)
        graph = catalogue0.to_graph()
        # the blank node cannot be pointed to by id, so we have to find it by its properties.
        subj = list(graph.subjects(None, Literal(title)))[0]
        catalogue1 = dcat.Catalogue.from_graph(subj, graph)
        self.assertEqual(catalogue0, catalogue1)

    def test_from_graph_001(self):
        id = "urn:test:TestDCAT:test_from_graph_001:catalogue"
        catalogue0 = dcat.Catalogue(rdf_id=id, title="catalogue")
        graph = catalogue0.to_graph()
        catalogue1 = dcat.Catalogue.from_graph(id, graph)
        self.assertEqual(catalogue0, catalogue1)

    def test_from_graph_002(self):
        id = "urn:test:TestDCAT:test_from_graph_002:catalogued_resource"
        catalogued_resource0 = dcat.CataloguedResource(
            rdf_id=id,
            title="catalogued resource",
        )
        graph = catalogued_resource0.to_graph()
        catalogued_resource1 = dcat.CataloguedResource.from_graph(id, graph)
        self.assertEqual(catalogued_resource0, catalogued_resource1)

    def test_from_graph_003(self):
        id = "urn:test:TestDCAT:test_from_graph_003:dataset"
        dataset0 = dcat.Dataset(
            rdf_id=id,
            title="dataset",
        )
        graph = dataset0.to_graph()
        dataset1 = dcat.Dataset.from_graph(id, graph)
        self.assertEqual(dataset0, dataset1)

    def test_from_graph_004(self):
        id = "urn:test:TestDCAT:test_from_graph_004:dataset"
        dataset0 = dcat.Dataset(
            rdf_id=id,
            title="dataset",
            distribution=[
                dcat.Distribution(
                    access_url="https://example.com/",
                )
            ],
        )
        graph = dataset0.to_graph()
        dataset1 = dcat.Dataset.from_graph(id, graph)
        self.assertEqual(dataset0, dataset1)


if __name__ == "__main__":
    unittest.main()
