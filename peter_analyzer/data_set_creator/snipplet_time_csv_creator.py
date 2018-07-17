import itertools
import random
import time

from data_set_creator.data_set_creator import DataSetCreator
from logging import Logger
from pathlib import Path
import csv
import datetime

class SnippletTimeCvsCreator(DataSetCreator):
    name = "SnippletTimeCvsCreator"

    __snipplet_name = []
    task : list
    identifier : list
    group : list

    def __init__(self, data: list, log: Logger):
        super().__init__(data, log)

        self.tasks = ['semantic', 'syntactic']
        self.identifier_quality = ['def', 'req']
        self.group = ['datagramMessenger', 'cpanalyzer', 'zipper', 'passwordutils']

    def _addAttribute(self, snippet, attribute):
        return "%s.%s" % (snippet, attribute)

    def create(self, ouputPath: Path):
        snippet_perms = itertools.permutations(self.group)

        snippets = dict()

        for p in self.group:
            snippets[self._addAttribute(self._addAttribute(p, self.tasks[0]),self.identifier_quality[0])] = list()
            snippets[self._addAttribute(self._addAttribute(p, self.tasks[0]), self.identifier_quality[1])] = list()
            snippets[self._addAttribute(self._addAttribute(p, self.tasks[1]),self.identifier_quality[0])]= list()
            snippets[self._addAttribute(self._addAttribute(p, self.tasks[1]),self.identifier_quality[1])] = list()

        print(snippets)
        for entry in self.data:
            for trial in entry._Entry__trials:
                print(trial)
                starttime : datetime.datetime = None
                endtime : datetime.datetime = None

                for event in trial._Trial__events:
                    if event._Event__code == "Start" and event._Event__type == "Snippet" :
                        starttime = event._Event__time
                    if event._Event__code == "Done" and event._Event__type == "Snippet":
                        endtime = event._Event__time
                    if event._Event__code == "Elapsed" and event._Event__type == "Clock":
                        endtime = event._Event__time
                deltatime = endtime - starttime
                snippets[trial._Trial__snipplet[:-5]].append({"time": deltatime.total_seconds(), "state": trial._Trial__state})

        for key in snippets:
            ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')
            output_file_path = ouputPath.joinpath(Path("snippet_time_" + key.replace(".", "-") + "_" + ts.__str__() + ".csv")).resolve().absolute()
            if output_file_path.is_absolute():
                output_file_path.touch(mode=0o777, exist_ok=True)
                if output_file_path.is_file():
                    output_file = output_file_path.open(mode='w')
                    writer = csv.DictWriter(output_file, fieldnames=['state', 'time'], dialect='excel',
                                            quoting=csv.QUOTE_NONNUMERIC,
                                            delimiter=';')
                    writer.writeheader()
                    writer.writerows(snippets[key])
                    self.log.debug("Successfully wrote " + key + ".csv")
                else:
                    self.log.error("Output file cannot be created!")
                    exit(-1)
            else:
                self.log.error("Output file path cannot be resolved!")
                exit(-1)

