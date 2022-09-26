from rdflib import Graph

class RDFTranslator:
    """Methods to read a file containing a serialization of an RDF graphin one format and display or save it in another format."""

    def __init__(self, inFileName, outFileName=None):
        self.g = Graph()
