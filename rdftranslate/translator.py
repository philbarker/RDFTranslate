from rdflib import Graph, Dataset

knownFormats = {
    "ttl": "turtle",
    "jsonld": "json-ld",
    "json": "json-ld",
    "json-ld": "json-ld",
    "n3": "n3",
    "nt": "nt",
    "xml": "xml",
    "rdf/xml": "xml",
    "trig": "trig",
}

namedGraphFormats = ["json-ld", "trig", "nt"]


class RDFTranslator:
    """Methods to read a file containing a serialization of an RDF graphin one format and display or save it in another format."""

    def __init__(
        self, inFileName, outFileName=None, inFileFormat=None, outFileFormat=None
    ):
        self.ds = Dataset()
        self.inFileName = inFileName
        self.outFileName = outFileName
        self.knownFormats = knownFormats
        self._set_inFileFormat(inFileFormat)
        self._set_outFileFormat(outFileFormat)

    def _set_inFileFormat(self, inFileFormat):
        """Set the input file format to the parameter passed, or guess from the file name extension. Raise error if not a supported format."""
        if inFileFormat is not None:
            iff = inFileFormat.lower()
            if iff in self.knownFormats.keys():
                self.inFileFormat = self.knownFormats[iff]
            else:
                msg = f"File format {inFileFormat} does not correspond to a known serialization format."
                raise ValueError(msg)
        elif "." in self.inFileName:
            ext = self.inFileName.split(".")[1].lower()
            if ext in self.knownFormats.keys():
                self.inFileFormat = self.knownFormats[ext]
            else:
                msg = f"File extension {ext} does not correspond to a known serialization format."
                raise ValueError(msg)
        else:
            msg = "No input file format or file extension provided. Cannot set input file format."
            raise ValueError(msg)

    def _set_outFileFormat(self, outFileFormat):
        """Set the input file format to the parameter passed, or guess from the file name extension. Raise error if not a supported format."""
        if outFileFormat is not None:
            off = outFileFormat.lower()
            if off in self.knownFormats.keys():
                self.outFileFormat = self.knownFormats[off]
            else:
                msg = f"File format {outFileFormat} does not correspond to a known serialization format."
                raise ValueError(msg)
        elif self.outFileName is not None and "." in self.outFileName:
            ext = self.outFileName.split(".")[1].lower()
            if ext in self.knownFormats.keys():
                self.outFileFormat = self.knownFormats[ext]
            else:
                msg = f"File extension {ext} does not correspond to a known serialization format."
                raise ValueError(msg)
        else:
            self.outFileFormat = "turtle"
        return

    def read_graph(self):
        """Read input file, store as graph."""
        # yeah, maybe there could be more checks here.
        self.ds.parse(self.inFileName, format=self.inFileFormat)
        return

    def write_graph(self):
        """Write graph to output file or console."""
        if len(self.ds) == 0:
            msg = "Trying to write graph when no graph is stored."
            raise ValueError(msg)
        # yeah, maybe there could be more checks here.
        f = self.outFileFormat
        if f in namedGraphFormats:
            if self.outFileName is None:
                output = self.ds.serialize(format=f)
                print(output)
                return output
            else:
                self.ds.serialize(destination=self.outFileName, format=f)
                return self.outFileName
        else:
            output = ""
            for graph in self.ds.graphs():
                graphName = str(graph.identifier)
                if graphName == "urn:x-rdflib:default":
                    output = output + graph.serialize(format=self.outFileFormat)
                else:
                    output = output + "\n# Graph: " + str(graph.identifier) + "\n"
                    output = output + graph.serialize(format=self.outFileFormat)
            if self.outFileName is None:
                print(output)
                return output
            else:
                with open(self.outFileName, "w") as outFile:
                    outFile.write(output)
                return self.outFileName
