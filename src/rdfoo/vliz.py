'''
VLIZ Ontology and Application Profile
'''

import rdflib
from typing import Annotated
from collections.abc import Sequence

from . import dcatap
# The imports on the next line are needed at runtime
from .dcatap import Attribution, Distribution, Relationship, Location, \
    PeriodOfTime  # noqa: F401
from .rdf import RDFRef, RDFType
# The imports on the next line are needed at runtime
from .rdfs import Resource  # noqa: F401
from .ssn import Property


class Dataset(dcatap.Dataset, frozen=True):

    rdf_type: RDFType = dcatap.Dataset.get_rdf_type("http://www.w3.org/ns/sosa/ObservationCollection")

    observed_property: Annotated[
        Sequence[RDFRef[Property]],
        {"rdf_property": "http://www.w3.org/ns/sosa/observedProperty"},
    ] = []

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        node, _ = cls._node_id(id)
        dataset = dcatap.Dataset.from_graph(id, graph)
        # observed_property
        observed_property_objects = graph.objects(node, cls._get_rdf_property("observed_property"))
        observed_property = [Property.from_graph(obj, graph) for obj in observed_property_objects]
        # Dataset
        return Dataset(
            **dataset.model_dump(),
            observed_property=observed_property,
        )
