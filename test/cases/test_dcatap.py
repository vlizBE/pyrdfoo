from rdfoo import dcatap
from rdfoo.rdf import uri

from utils import RDFTestCase


class TestDCATAP(RDFTestCase):

    def test_create_catalogue(self):
        obj = dcatap.Catalogue(
            title="Test Catalogue",
            description="A test catalogue.",
            publisher=uri("https://marineinfo.org/id/institute/36"),
        )
        self.assertRDFType(obj, "http://www.w3.org/ns/dcat#Catalog")

    def test_create_catalogued_resource(self):
        obj = dcatap.CataloguedResource()
        self.assertRDFType(obj, "http://www.w3.org/ns/dcat#Resource")

    def test_create_dataset(self):
        obj = dcatap.Dataset(
            title="Test Dataset",
            description="A test dataset.",
        )
        self.assertRDFType(obj, "http://www.w3.org/ns/dcat#Dataset")

    def test_create_distribution(self):
        obj = dcatap.Distribution()
        self.assertRDFType(obj, "http://www.w3.org/ns/dcat#Distribution")

    def test_create_period_of_time(self):
        obj = dcatap.PeriodOfTime()
        self.assertRDFType(obj, "http://purl.org/dc/terms/PeriodOfTime")

    def test_create_location(self):
        obj = dcatap.Location()
        self.assertRDFType(obj, "http://purl.org/dc/terms/Location")

    def test_from_graph_001(self):
        id = "urn:test:TestDCATAP:test_from_graph_001:catalogue"
        catalogue0 = dcatap.Catalogue(
            rdf_id=id,
            title="catalogue",
            publisher=uri("urn:test:TestDCATAP:test_from_graph_001:publisher"),
            description="A test catalogue.",
        )
        graph = catalogue0.to_graph()
        catalogue1 = dcatap.Catalogue.from_graph(id, graph)
        self.assertEqual(catalogue0, catalogue1)

    def test_from_graph_002(self):
        id = "urn:test:TestDCATAP:test_from_graph_002:catalogued_resource"
        catalogued_resource0 = dcatap.CataloguedResource(
            rdf_id=id,
            title="catalogued resource",
        )
        graph = catalogued_resource0.to_graph()
        catalogued_resource1 = dcatap.CataloguedResource.from_graph(id, graph)
        self.assertEqual(catalogued_resource0, catalogued_resource1)

    def test_from_graph_003(self):
        id = "urn:test:TestDCATAP:test_from_graph_003:dataset"
        dataset0 = dcatap.Dataset(
            rdf_id=id,
            title="dataset",
            description="A test dataset.",
        )
        graph = dataset0.to_graph()
        dataset1 = dcatap.Dataset.from_graph(id, graph)
        self.assertEqual(dataset0, dataset1)

    def test_from_graph_004(self):
        id = "urn:test:TestDCATAP:test_from_graph_004:dataset"
        dataset0 = dcatap.Dataset(
            rdf_id=id,
            title="dataset",
            description="A test dataset.",
            distribution=[
                dcatap.Distribution(
                    access_url="https://example.com/",
                )
            ]
        )
        graph = dataset0.to_graph()
        dataset1 = dcatap.Dataset.from_graph(id, graph)
        self.assertEqual(dataset0, dataset1)