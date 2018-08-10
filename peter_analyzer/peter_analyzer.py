#!/usr/local/bin/python3
import importlib
import os

import coloredlogs, logging
from argparse import ArgumentParser
from pathlib import Path
import pkgutil

from peter_analyzer import json_decoder
from peter_analyzer.data_set_creator import data_set_creator

def main(args:list):
    parser = ArgumentParser()
    parser.add_argument("-l", "--log-dir",
                        dest="logdir",
                        help="destination of the logfiles",
                        default="./logs/",
                        metavar="DIR")

    parser.add_argument("-q", "--quiet",
                        action="store_false",
                        dest="verbose",
                        default=True,
                        help="don't print log info messages to stdout")

    parser.add_argument("-i", "--input",
                        dest="input",
                        help="Json input file containing the data.",
                        required=True,
                        metavar="FILE.json")

    parser.add_argument("-o", "--output-dir",
                        dest="output",
                        default=".",
                        help="Output dir for the data.",
                        metavar="DIR")

    args = parser.parse_args(args)

    log = logging.getLogger("PeterAnalyzer")
    log.setLevel(logging.DEBUG)
    formatter = coloredlogs.ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)

    if args.verbose:

        ch.setLevel(logging.INFO)
    else:
        ch.setLevel(logging.ERROR)

    log.addHandler(ch)

    logdir = Path(args.logdir)

    logfile = Path('peter_analyzer.log')

    if logdir.exists():
        if logdir.is_dir():
            fh = logging.FileHandler(logdir.joinpath(logfile))
            fh.setLevel(logging.DEBUG)

            # create formatter and add it to the handlers

            fh.setFormatter(formatter)

            log.addHandler(fh)

        else:
            log.error('Specified log dir is no directory')
    else:
        logfile = Path.cwd().joinpath(logdir).joinpath(logfile)
        logfile.parent.mkdir(parents=True, exist_ok=True)

        fh = logging.FileHandler(logfile)
        fh.setLevel(logging.DEBUG)

        # create formatter and add it to the handlers

        fh.setFormatter(formatter)

        log.addHandler(fh)

    output_path = Path(args.output)
    if output_path.exists():
        if output_path.is_dir():
            log.info("Output path :" + str(output_path.resolve()))

        else:
            log.error("Output param not a directory using default.")
            output_path = Path.cwd()

    else:
        output_path = Path.cwd().joinpath(output_path)
        output_path.mkdir(parents=True, exist_ok=True)
        log.info("Output path :" + str(output_path.resolve()))

    input_path = Path(args.input)
    if input_path.is_absolute():
        if input_path.is_file():
            log.info("Input path :" + str(input_path.resolve()))
            if not input_path.suffix == ".json":
                log.error("Input file not a json file.")
                exit(-1)
        else:
            log.error("Input param not a file.")
            exit(-1)

    else:
        input_path = Path().cwd().joinpath(input_path).resolve()
        if input_path.is_file():
            log.info("Input path :" + str(input_path.resolve()))
            if not input_path.suffix == ".json":
                log.error("Input file not a json file.")
                exit(-1)
        else:
            log.error("Input param not a file or doesnt exist")
            exit(-1)

    j = json_decoder.PeterJsonDecoder(verbose=args.verbose, logdir=logdir)
    data = j.decode(open(input_path))
    log.info("Loaded " + str(data.__len__()) + " elements!")

    pkg_dir = os.path.dirname("../data_set_creator/data_set_creator.py")

    for (module_loader, name, ispkg) in pkgutil.iter_modules([pkg_dir]):
        importlib.import_module('.' + name, "data_set_creator")

    all_creators = data_set_creator.DataSetCreator.__subclasses__()
    for creator in all_creators:
        r = creator(data, log)
        r.create(output_path)



if __name__ == "__main__":
    import sys
    main(sys.argv[1:])