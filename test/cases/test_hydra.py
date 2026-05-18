from utils import RDFTestCase

from rdfoo import hydra


class TestCollection(RDFTestCase):

    def test_create(self):
        collection = hydra.Collection(rdf_id="collection", total_items=5)
        self.assertRDFType(collection, "http://www.w3.org/ns/hydra/core#Collection")

    def test_from_graph(self):
        collection_id = "collection"
        ref_collection = hydra.Collection(rdf_id=collection_id, total_items=5)
        graph = ref_collection.to_graph()
        collection = hydra.Collection.from_graph(collection_id, graph)
        self.assertEqual(ref_collection, collection)


class TestPagedCollection(RDFTestCase):

    def test_create(self):
        collection = hydra.PagedCollection(
            rdf_id="page_2",
            total_items=4,
            first="page_1",
            next="page_3",
            previous="page_1",
            last="page_4",
        )
        self.assertRDFType(
            collection, "http://www.w3.org/ns/hydra/core#PagedCollection"
        )

    def test_from_graph(self):
        collection_id = "page_2"
        ref_collection = hydra.PagedCollection(
            rdf_id=collection_id,
            total_items=4,
            first="page_1",
            next="page_3",
            previous="page_1",
            last="page_4",
        )
        graph = ref_collection.to_graph()
        collection = hydra.PagedCollection.from_graph(collection_id, graph)
        self.assertEqual(ref_collection, collection)

    def test_from_graph_2(self):
        collection_id = "page_1"
        ref_collection = hydra.PagedCollection(
            rdf_id=collection_id,
            total_items=3,
            first="page_1",
            next="page_2",
            last="page_3",
        )
        graph = ref_collection.to_graph()
        collection = hydra.PagedCollection.from_graph(collection_id, graph)
        self.assertEqual(ref_collection, collection)
