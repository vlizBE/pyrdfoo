import unittest

from rdfoo import dcat, dcatap
from rdfoo.rdf import RDF, RDFType, uri


class RDFTestCase(unittest.TestCase):

    def assetRDFType(self, obj: RDF, rdf_type: RDFType):
        obj_types: list[str] = obj.rdf_type if isinstance(obj.rdf_type, list) else [obj.rdf_type]
        check_types: list[str] = rdf_type if isinstance(rdf_type, list) else [rdf_type]
        for t in check_types:
            self.assertIn(t, obj_types, "RDF type mismatch")


class TestDCAT(RDFTestCase):

    def test_create_catalogue(self):
        obj = dcat.Catalogue()
        self.assetRDFType(obj, "https://www.w3.org/ns/dcat#Catalog")

    def test_create_catalogued_resource(self):
        obj = dcat.CataloguedResource()
        self.assetRDFType(obj, "https://www.w3.org/ns/dcat#Resource")

    def test_create_dataset(self):
        obj = dcat.Dataset()
        self.assetRDFType(obj, "https://www.w3.org/ns/dcat#Dataset")

    def test_create_distribution(self):
        obj = dcat.Distribution()
        self.assetRDFType(obj, "http://www.w3.org/ns/dcat#Distribution")

    def test_create_period_of_time(self):
        obj = dcat.PeriodOfTime()
        self.assetRDFType(obj, "http://purl.org/dc/terms/PeriodOfTime")

    def test_create_location(self):
        obj = dcat.Location()
        self.assetRDFType(obj, "http://purl.org/dc/terms/Location")

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
            ]
        )
        graph = dataset0.to_graph()
        dataset1 = dcat.Dataset.from_graph(id, graph)
        self.assertEqual(dataset0, dataset1)


class TestDCATAP(RDFTestCase):

    def test_create_catalogue(self):
        obj = dcatap.Catalogue(
            title="Test Catalogue",
            description="A test catalogue.",
            publisher=uri("https://marineinfo.org/id/institute/36"),
        )
        self.assetRDFType(obj, "https://www.w3.org/ns/dcat#Catalog")

    def test_create_catalogued_resource(self):
        obj = dcatap.CataloguedResource()
        self.assetRDFType(obj, "https://www.w3.org/ns/dcat#Resource")

    def test_create_dataset(self):
        obj = dcatap.Dataset(
            title="Test Dataset",
            description="A test dataset.",
        )
        self.assetRDFType(obj, "https://www.w3.org/ns/dcat#Dataset")

    def test_create_distribution(self):
        obj = dcatap.Distribution()
        self.assetRDFType(obj, "http://www.w3.org/ns/dcat#Distribution")

    def test_create_period_of_time(self):
        obj = dcatap.PeriodOfTime()
        self.assetRDFType(obj, "http://purl.org/dc/terms/PeriodOfTime")

    def test_create_location(self):
        obj = dcatap.Location()
        self.assetRDFType(obj, "http://purl.org/dc/terms/Location")

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


if __name__ == '__main__':
    unittest.main()


