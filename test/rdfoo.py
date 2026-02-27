import unittest

from rdfoo import dcat, dcatap
from rdfoo.rdf import RDF, RDFType, uri


class RDFTestCase(unittest.TestCase):

    def assetRDFType(self, obj: RDF, rdf_type: RDFType):
        obj_types: list[str] = obj.rdf_type if isinstance(obj.rdf_type, list) else [obj.rdf_type]
        check_types: list[str] = rdf_type if isinstance(rdf_type, list) else [rdf_type]
        for t in check_types:
            self.assertIn(t, obj_types, "RDF type mismatch")


#class TestRDF(RDFTestCase):
#
#    class TModelA(RDF, frozen=True):
#        rdf_type: RDFType = "urn:test:a"
#
#    class TModelB(TModelA, frozen=True):
#        rdf_type: RDFType = ["urn:test:a", "urn:test:b"]
#        value: int = 123
#
#    class TModelC(RDF, frozen=True):
#        rdf_type: RDFType = ["urn:test:c"]
#        objA: "TModelA | None" = None # type: ignore  # noqa: F821
#        objB: "TModelA | None" = None # type: ignore  # noqa: F821
#
#    def test_model_dump(self):
#        # TODO
#        objA = TestRDF.TModelA()
#        objB = TestRDF.TModelB()
#        objC = TestRDF.TModelC(objA=objA, objB=objB)
#        print()
#        print(objA.to_dict())
#        print(objB.to_dict())
#        print(objC.to_dict())
#        self.assetRDFType(objA, "urn:test:a")
#        self.assetRDFType(objB, ["urn:test:a", "urn:test:b"])


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


if __name__ == '__main__':
    unittest.main()


