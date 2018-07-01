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
                        metavar="FOLDER")

    parser.add_argument("-q", "--quiet",
                        action="store_false",
                        dest="verbose",
                        default=True,
                        help="don't print log info messages to stdout")

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

        home = Path('.')
        home = home.joinpath(p)
        logfile = home.joinpath(logfile)
        logfile.parent.mkdir(parents=True, exist_ok=True)

        fh = logging.FileHandler(logfile)
        fh.setLevel(logging.DEBUG)

        # create formatter and add it to the handlers

        fh.setFormatter(formatter)

        log.addHandler(fh)











