#!/usr/bin/env python
from parseArguments import parse_arguments

if __name__ == "__main__":
    args = parse_arguments()
    print(args.inputFileName)
    print(args.outputFileName)
    print(args.outFormat)
    print(args.inFormat)
