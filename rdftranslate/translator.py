from rdflib import Graph


class RDFTranslator:
    """Methods to read a file containing a serialization of an RDF graphin one format and display or save it in another format."""

    def __init__(
        self, inFileName, outFileName=None, inFileFormat=None, outFileFormat=None
    ):
        self.g = Graph()
        self.inFileName = inFileName
        self.outFileName = outFileName
        self.knownFormats = ["ttl", "jsonld", "json", "n3"]
        self._set_inFileFormat(inFileFormat)
        self._set_outFileFormat(outFileFormat)

    def _set_inFileFormat(self, inFileFormat):
        """Set the input file format to the parameter passed, or guess from the file name extension. Raise error if not a supported format."""
        if inFileFormat is not None:
            iff = inFileFormat.lower()
            if iff in self.knownFormats:
                self.inFileFormat = iff
            else:
                msg = f"File format {inFileFormat} does not correspond to a known serialization format."
                raise ValueError(msg)
        elif "." in self.inFileName:
            ext = self.inFileName.split(".")[1].lower()
            if ext in self.knownFormats:
                self.inFileFormat = ext
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
            if off in self.knownFormats:
                self.outFileFormat = off
            else:
                msg = f"File format {outFileFormat} does not correspond to a known serialization format."
                raise ValueError(msg)
        elif self.outFileName is not None and "." in self.outFileName:
            ext = self.outFileName.split(".")[1].lower()
            if ext in self.knownFormats:
                self.outFileFormat = ext
            else:
                msg = f"File extension {ext} does not correspond to a known serialization format."
                raise ValueError(msg)
        else:
            self.outFileFormat = "ttl"
