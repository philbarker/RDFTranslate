from argparse import ArgumentParser

# defaults
outputFileName = None
outputFileFormat = None
inputFileFormat = None


def parse_arguments():
    parser = ArgumentParser(
        prog="rdftranslate.py",
        description="Translate between RDF serialization formats.",
    )
    parser.add_argument(
        "inputFileName",
        type=str,
        metavar="<input file name>",
        help="The file to convert.",
    )
    parser.add_argument(
        "outputFileName",
        nargs="?",
        type=str,
        metavar="<output file name>",
        default=outputFileName,
        help="The file for the output. If none is provided the conversion will be displayed in the console.",
    )
    parser.add_argument(
        "-iff",
        "--inFormat",
        type=str,
        metavar="<input file format>",
        default=inputFileFormat,
        help="The file format of the input file. If none is provided the extension of the input file will be used to guess. Supported values are jsonld, json, json-ld (all json-ld); n3, nt, rdf/xml and trig",
    )
    parser.add_argument(
        "-off",
        "--outFormat",
        type=str,
        metavar="<output file format>",
        default=outputFileFormat,
        help="The file format for the output. If none is provided the extension of the output file will be used to guess, if an output file name is not provided either, the output will be as Turtle (ttl).",
    )
    return parser.parse_args()
