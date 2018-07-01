#!/usr/local/bin/python3

import coloredlogs, logging
from argparse import ArgumentParser
from pathlib import Path


if __name__ == "__main__":
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

    args = parser.parse_args()

    log = logging.getLogger("PeterAnalyzer")
    log.setLevel(logging.DEBUG)
    formatter = coloredlogs.ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)

    if args.verbose :

        ch.setLevel(logging.INFO)
    else:
        ch.setLevel(logging.ERROR)

    log.addHandler(ch)

    p = Path(args.logdir)

    logfile = Path('peter_analyzer.log')

    if p.exists():
        if p.is_dir() :
            fh = logging.FileHandler(p.joinpath(logfile))
            fh.setLevel(logging.DEBUG)

            # create formatter and add it to the handlers

            fh.setFormatter(formatter)

            log.addHandler(fh)

        else:
            log.error('Specified log dir is no directory')
    else:
        logfile = Path.cwd().joinpath(p).joinpath(logfile)
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
    if input_path.exists():
        if input_path.is_file():
            log.info("Input path :" + str(input_path.resolve()))
            if not input_path.suffix == ".json":
                log.error("Input file not a json file.")
                exit(-1)



        else:
            log.error("Input param not a file.")
            exit(-1)

    else:
        log.error("Input param file or folder does not exist!")
        exit(-1)





