"""
VLIZ Ontology and Application Profile
"""

import rdflib
from typing import Annotated
from collections.abc import Sequence

from . import dcatap
from . import prov

# The imports on the next line are needed at runtime
from .dcatap import Attribution, Distribution, Relationship, Location, PeriodOfTime # noqa: F401
from .rdf import RDFRef, RDFType

# The imports on the next line are needed at runtime
from .rdfs import Resource  # noqa: F401
from .prov import Agent, Activity, Generation  # noqa: F401
from .ssn import Property


def _rdf_type() -> RDFType:
    prov_rdf_type = prov.Entity.get_rdf_type()
    prov_rdf_types = (
        prov_rdf_type if isinstance(prov_rdf_type, list) else [prov_rdf_type]
    )
    dcatap_rdf_type = dcatap.Dataset.get_rdf_type(
        extra="http://www.w3.org/ns/sosa/ObservationCollection"
    )
    dcatap_rdf_types = (
        dcatap_rdf_type if isinstance(dcatap_rdf_type, list) else [dcatap_rdf_type]
    )

    return dcatap_rdf_types + prov_rdf_types


class Dataset(dcatap.Dataset, prov.Entity, frozen=True):

    rdf_type: RDFType = _rdf_type()

    observed_property: Annotated[
        Sequence[RDFRef[Property]],
        {"rdf_property": "http://www.w3.org/ns/sosa/observedProperty"},
    ] = []

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        node, _ = cls._node_id(id)

        dataset_dict = dcatap.Dataset.from_graph(id, graph).model_dump()
        dataset_dict.pop("rdf_type")
        # entity
        entity_dict = prov.Entity.from_graph(node, graph).model_dump()
        entity_dict.pop("rdf_type")
        entity_keys = set(entity_dict.keys())
        for k in entity_keys.difference(dataset_dict.keys()):
            dataset_dict[k] = entity_dict[k]
        # observed_property
        observed_property_objects = graph.objects(
            node, cls._get_rdf_property("observed_property")
        )
        observed_property = [
            Property.from_graph(obj, graph) for obj in observed_property_objects
        ]

        # Dataset
        return Dataset(
            **dataset_dict,
            observed_property=observed_property,
        )
