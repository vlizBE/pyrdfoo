"""
DCMI Metadata Terms

Ontology documentation: https://www.dublincore.org/specifications/dublin-core/dcmi-terms/

Namespace: ``http://purl.org/dc/terms/``
"""

import rdflib

from datetime import date, datetime
from typing import Annotated

from .rdf import RDF, RDFType


class Location(RDF, frozen=True):
    """
    A spatial region or named place.

    See also: https://www.dublincore.org/specifications/dublin-core/dcmi-terms/terms/Location/
    """

    rdf_type: RDFType = "http://purl.org/dc/terms/Location"

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        _, rdf_id = cls._node_id(id)
        return Location(rdf_id=rdf_id)


class PeriodOfTime(RDF, frozen=True):
    """
    An interval of time that is named or defined by its start and end.

    See also: https://www.w3.org/TR/vocab-dcat-3/#Class:Period_of_Time
    """

    rdf_type: RDFType = str(rdflib.DCTERMS.PeriodOfTime)

    end_date: Annotated[
        date | None,
        {"rdf_property": str(rdflib.DCAT.endDate)},
    ] = None

    start_date: Annotated[
        date | None,
        {"rdf_property": str(rdflib.DCAT.startDate)},
    ] = None

    @classmethod
    def from_graph(cls, id: str | rdflib.Node, graph: rdflib.Graph):
        node, rdf_id = cls._node_id(id)
        # start_date
        start_obj = graph.value(node, cls._get_rdf_property("start_date"))
        start_date = datetime.fromisoformat(str(start_obj)) if start_obj is not None else None
        # end_date
        end_obj = graph.value(node, cls._get_rdf_property("end_date"))
        end_date = datetime.fromisoformat(str(end_obj)) if end_obj is not None else None
        # PeriodOfTime
        return PeriodOfTime(
            rdf_id=rdf_id,
            start_date=start_date,
            end_date=end_date,
        )