import unittest

from rdfoo.rdf import RDF, RDFType


class RDFTestCase(unittest.TestCase):

    def assertRDFType(self, obj: RDF, rdf_type: RDFType):
        obj_types: list[str] = obj.rdf_type if isinstance(obj.rdf_type, list) else [obj.rdf_type]
        check_types: list[str] = rdf_type if isinstance(rdf_type, list) else [rdf_type]
        for t in check_types:
            self.assertIn(t, obj_types, "RDF type mismatch")