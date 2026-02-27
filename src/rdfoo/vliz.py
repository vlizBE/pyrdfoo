'''
VLIZ Ontology and Application Profile
'''

from typing import Annotated
# The imports on the next line are needed at runtime
from collections.abc import Sequence  # noqa: F401

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

    observedProperty: Annotated[
        list[RDFRef[Property]],
        {"rdf_property": "http://www.w3.org/ns/sosa/observedProperty"},
    ] = []
