Examples
========

Serialize DCAT catalogue
------------------------

To create a DCAT catalogue and serialize it to Turtle:

.. code:: python

    from rdfoo import dcat

    catalogue = dcat.Catalogue(
        rdf_id="urn:ex:catalogue",
        title="My DCAT Catalogue",
    )

    print(catalogue.to_graph().serialize(None, "turtle"))


which renders something similar to:

.. code:: turtle

    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    <urn:ex:catalogue> a dcat:Catalog ;
        dcterms:title "My DCAT Catalogue" .

Deserialize DCAT catalogue
--------------------------

To deserialize the same catalogue from Turtle as DCAT catalogue:

.. code:: python

    from rdflib import Graph, URIRef
    from rdfoo import dcat

    turtle = """
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix dcterms: <http://purl.org/dc/terms/> .

        <urn:ex:catalogue> a dcat:Catalog ;
            dcterms:title \"My DCAT Catalogue\" .
    """
    graph = Graph(identifier=URIRef("urn:ex:catalogue"))
    graph.parse(data=turtle)
    catalogue = dcat.Catalogue.from_graph(graph.identifier, graph)

    print(f"catalogue.title: {catalogue.title}")


**Note**: The identifier and type of the subject to be serialized should be known!

which would result in the following:

.. code::

    catalogue.title: My DCAT Catalogue

Serialize ProvONE Program
-------------------------

To create a ProvONE Program and serialize it to Turtle:

.. code:: python

    from rdfoo import provone

    program = provone.Program(
        rdf_id="urn:ex:program",
        title="My Program",
    )

    graph = program.to_graph()
    graph.bind("provone", provone.PROVONE)
    print(graph.serialize(None, "turtle"))

which renders something similar to:

.. code:: turtle

    @prefix dcterms: <http://purl.org/dc/terms/> .
    @prefix prov: <http://www.w3.org/ns/prov#> .
    @prefix provone: <http://purl.dataone.org/provone/2015/01/15/ontology#> .

    <urn:ex:program> a provone:Program,
            prov:Entity,
            prov:Plan ;
        dcterms:title "My Program" .

Deserialize ProvONE Program
---------------------------

.. code:: python

    from rdflib import Graph, URIRef
    from rdfoo import provone

    turtle = """
        @prefix dcterms: <http://purl.org/dc/terms/> .
        @prefix prov: <http://www.w3.org/ns/prov#> .
        @prefix provone: <http://purl.dataone.org/provone/2015/01/15/ontology#> .

        <urn:ex:program> a provone:Program,
                prov:Entity,
                prov:Plan ;
            dcterms:title "My Program" .
    """
    graph = Graph(identifier=URIRef("urn:ex:program"))
    graph.bind("provone", provone.PROVONE)
    graph.parse(data=turtle)
    program = provone.Program.from_graph(graph.identifier, graph)

    print(f"program.title: {program.title}")

**Note**: The identifier and type of the subject to be serialized should be known!

which would result in the following:

.. code::

    program.title: My Program