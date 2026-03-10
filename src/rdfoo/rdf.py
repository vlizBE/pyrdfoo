'''
RDF Core Object
'''

from abc import abstractmethod
from collections.abc import Sequence
from pydantic import BaseModel, ConfigDict, Field
import rdflib as rdf
from typing import TypeVar


def RDFId(default=None):
    '''Helper function to create an `rdf_id` field with a default value.'''
    return Field(default=default, serialization_alias="@id")


type RDFType = str | list[str]
'''Type definition for the `rdf_type` field.'''


class RDF(BaseModel, frozen=True):
    '''
    Base class for RDF objects.

    This class provides the `to_graph` method that allows to generate an RDF
    graph for any of its subclasses. It also provides the `from_graph` method to
    construct an object described in a graph.
    '''
    model_config = ConfigDict(
        validate_assignment=True,
        validate_by_name=True,
    )

    rdf_id: str | None = RDFId()
    rdf_type: RDFType
    rdf_bindings: list[tuple[str, str]] = []
    '''[[binding1, namespace1], [binding2, namespace2]]'''

    def has_type(self, type: RDFType) -> bool:
        own_types: list[str] = self.rdf_type if isinstance(self.rdf_type, list) else [self.rdf_type]
        check_types: list[str] = type if isinstance(type, list) else [type]
        for t in check_types:
            if t not in own_types:
                return False
        return True

    def to_dict(self, rdf_id: str | None = None) -> dict:

        def handle_value(v):
            if v is None:
                pass
            elif isinstance(v, RDFURIRef):
                return v.uri
            elif isinstance(v, RDF):
                return v.to_dict()
            elif isinstance(v, str):
                return v
            elif isinstance(v, Sequence):
                values = []
                for vi in v:
                    values.append(handle_value(vi))
                return values
            else:
                return v

        result: dict = {
            "rdf_id": rdf_id or self.rdf_id,
            "rdf_type": [],
        }

        # type
        if isinstance(self.rdf_type, str):
            result["rdf_type"] = [self.rdf_type]
        elif isinstance(self.rdf_type, list):
            result["rdf_type"] = self.rdf_type
        else:
            raise Exception("invalid RDF type")

        # fields
        for f, v in self:
            if f in ["rdf_id", "rdf_type", "rdf_bindings"]:
                continue
            elif v is None:
                pass
            else:
                result[f] = handle_value(v)

        return result

    def to_graph(self, node: rdf.Node | None = None, graph: rdf.Graph | None = None) -> rdf.Graph:
        if graph is None:
            graph = rdf.Graph()

        def handle_value(graph, parent, v):
            if v is None:
                pass
            elif isinstance(v, RDFURIRef):
                graph.add((parent, rdf.URIRef(self._get_rdf_annotation(f)), rdf.URIRef(v.uri)))
            elif isinstance(v, RDF):
                if v.rdf_id is not None:
                    n = rdf.URIRef(v.rdf_id)
                else:
                    n = rdf.BNode()
                graph.add((parent, rdf.URIRef(self._get_rdf_annotation(f)), n))
                v.to_graph(n, graph)
            elif isinstance(v, str):
                graph.add((parent, rdf.URIRef(self._get_rdf_annotation(f)), rdf.Literal(v)))
            elif isinstance(v, Sequence):
                for vi in v:
                    handle_value(graph, parent, vi)
            else:
                graph.add((parent, rdf.URIRef(self._get_rdf_annotation(f)), rdf.Literal(v)))

        # @id
        if node is not None:
            s = node
        elif self.rdf_id is not None:
            s = rdf.URIRef(self.rdf_id)
        else:
            raise Exception("node without identifier")

        # type
        if isinstance(self.rdf_type, str):
            graph.add((s, rdf.RDF.type, rdf.URIRef(self.rdf_type)))
        elif isinstance(self.rdf_type, list):
            for rdf_type in self.rdf_type:
                graph.add((s, rdf.RDF.type, rdf.URIRef(rdf_type)))
        else:
            raise Exception("invalid RDF type")

        # fields
        for f, v in self:
            if f in ["rdf_id", "rdf_type", "rdf_bindings"]:
                continue
            handle_value(graph, s, v)

        for b, ns in self.rdf_bindings:
            graph.bind(b, rdf.Namespace(ns))

        return graph

    @classmethod
    @abstractmethod
    def from_graph[T](cls: T, id: str | rdf.Node, graph: rdf.Graph) -> T:
        ...

    @staticmethod
    def _node_id(id: str | rdf.Node) -> tuple[rdf.Node, str | None]:
        if isinstance(id, rdf.URIRef):
            node = id
            rdf_id = str(id)
        elif isinstance(id, rdf.Node):
            node = id
            rdf_id = None
        else:
            node = rdf.URIRef(id)
            rdf_id = id
        return node, rdf_id

    @classmethod
    def _get_rdf_annotation(cls, field) -> str:
        anns = cls.model_fields[field].metadata
        for ann in anns:
            if "rdf_property" in ann:
                return ann["rdf_property"]
        raise Exception(f"no RDF property for model field {field}")

    @classmethod
    def _get_rdf_property(cls, field: str) -> rdf.URIRef:
        anns = cls.model_fields[field].metadata
        for ann in anns:
            if "rdf_property" in ann:
                return rdf.URIRef(ann["rdf_property"])
        raise Exception(f"no RDF property for model field {field}")

    @classmethod
    def get_rdf_type(cls, *, extra: RDFType = []) -> RDFType:
        if isinstance(extra, str):
            extra = [extra]
        rdf_type = cls.model_fields["rdf_type"].default
        if len(extra) > 0:
            if isinstance(rdf_type, str):
                return [rdf_type] + extra
            else:
                return rdf_type + extra
        return rdf_type

    @classmethod
    def get_rdf_bindings(cls, extra: RDFType = []) -> RDFType:
        if isinstance(extra, str):
            extra = [extra]
        rdf_bindings = cls.model_fields["rdf_bindings"].default
        if len(extra) > 0:
            if isinstance(rdf_bindings, str):
                return [rdf_bindings] + extra
            else:
                return rdf_bindings + extra
        return rdf_bindings


T = TypeVar("T", bound=RDF)
'''An RDF object.'''


class RDFURIRef[T](BaseModel):
    '''
    Reference to a resource.

    This class is used to distinguish between a URI and a string literal.
    '''

    uri: str = Field(serialization_alias="@id")


def uri[T](uri: str):
    '''Helper function to create an URI that references a resource.'''
    return RDFURIRef(uri=uri)


type RDFRef[T] = T | RDFURIRef[T]
'''A resource object or a reference to one.'''
