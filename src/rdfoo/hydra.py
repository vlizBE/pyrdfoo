"""
Hydra Core Vocabulary - A Vocabulary for Hypermedia-Driven Web APIs

Documentation: http://www.hydra-cg.com/spec/latest/core/

Namespace : ``http://www.w3.org/ns/hydra/core#``
"""

import rdflib

from typing import Annotated

from .rdf import RDF, RDFType, RDFURIRef

HYDRA = rdflib.Namespace("http://www.w3.org/ns/hydra/core#")


#
# Main Entities
#


class Collection(RDF, frozen=True):
    """
    A collection holding references to a number of related resources.

    IRI: http://www.w3.org/ns/hydra/core#Collection
    """

    rdf_type: RDFType = f"{HYDRA}Collection"

    total_items: Annotated[int | None, {"rdf_property": f"{HYDRA}totalItems"}] = None
    """The total number of items referenced by a collection."""

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        node, rdf_id = cls._node_id(id)

        # total_items
        total_items = graph.value(node, cls._get_rdf_property("total_items"))
        total_items = int(str(total_items)) if total_items else None

        return Collection(rdf_id=rdf_id, total_items=total_items)


class PagedCollection(Collection, frozen=True):
    """
    A collection holding references to a number of related resources.

    IRI: http://www.w3.org/ns/hydra/core#Collection
    """

    rdf_type: RDFType = f"{HYDRA}PagedCollection"

    first: Annotated[RDFURIRef | str | None, {"rdf_property": f"{HYDRA}first"}] = None
    """The first resource of an interlinked set of resources."""

    next: Annotated[RDFURIRef | str | None, {"rdf_property": f"{HYDRA}next"}] = None
    """The resource following the current instance in an interlinked set of resources."""

    previous: Annotated[
        RDFURIRef | str | None, {"rdf_property": f"{HYDRA}previous"}
    ] = None
    """The resource preceding the current instance in an interlinked set of resources."""

    last: Annotated[RDFURIRef | str | None, {"rdf_property": f"{HYDRA}last"}] = None
    """The last resource of an interlinked set of resources."""

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        node, _ = cls._node_id(id)

        # Collection
        collection_dict: dict = Collection.from_graph(node, graph).model_dump()
        collection_dict.pop("rdf_type")
        # first
        first = graph.value(node, cls._get_rdf_property("first"))
        if type(first) is rdflib.URIRef:
            first = RDFURIRef(uri=str(first))
        else:
            first = str(first) if first else None
        # next
        next = graph.value(node, cls._get_rdf_property("next"))
        if type(next) is rdflib.URIRef:
            next = RDFURIRef(uri=str(next))
        else:
            next = str(next) if next else None
        # previous
        previous = graph.value(node, cls._get_rdf_property("previous"))
        if type(previous) is rdflib.URIRef:
            previous = RDFURIRef(uri=str(previous))
        else:
            previous = str(previous) if previous else None
        # last
        last = graph.value(node, cls._get_rdf_property("last"))
        if type(last) is rdflib.URIRef:
            last = RDFURIRef(uri=str(last))
        else:
            last = str(last) if last else None

        return PagedCollection(
            **collection_dict, first=first, next=next, previous=previous, last=last
        )
