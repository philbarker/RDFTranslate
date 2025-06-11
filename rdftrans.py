#!/usr/bin/env python
from parseArguments import parse_arguments
from rdftranslate import RDFTranslator

if __name__ == "__main__":
    args = parse_arguments()
    ifn = args.inputFileName
    ofn = args.outputFileName
    iff = args.inFormat
    off = args.outFormat
    t = RDFTranslator(
        ifn,
        outFileName=ofn,
        inFileFormat=iff,
        outFileFormat=off,
    )
    print(f"Converting {t.inFileName} from {t.inFileFormat} to {t.outFileFormat}\n")
    t.read_graph()
    if ofn is not None:
        print(f"... saving data in {ofn}")
    t.write_graph()
