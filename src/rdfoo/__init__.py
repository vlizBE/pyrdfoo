import rdflib
import rdflib.term

# Patch top-level rdflib namespace if running on rdflib 6.x
if not hasattr(rdflib, "Node"):
    rdflib.Node = rdflib.term.Node
    rdflib.IdentifiedNode = rdflib.term.IdentifiedNode
