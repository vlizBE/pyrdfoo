Examples
========

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

    @prefix dcterms: <http://purl.org/dc/terms/> .

    <urn:ex:catalogue> a <https://www.w3.org/ns/dcat#Catalog> ;
        dcterms:title "My DCAT Catalogue" .
