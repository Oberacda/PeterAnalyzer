import time

from peter_analyzer.data_set_creator.data_set_creator import DataSetCreator
from logging import Logger
from pathlib import Path
import csv
import datetime

class SnippletTimeCvsCreator(DataSetCreator):
    name = "CSV-Spss_TimeConstructor"

    __snipplet_name = []
    task : list
    identifier : list
    group : list

    __delimiter : str = ','



    def __init__(self, data: list, log: Logger):
        super().__init__(data, log)

        self.tasks = ['semantic', 'syntactic']
        self.identifier_quality = ['def', 'req']
        self.group = ['datagramMessenger', 'cpanalyzer', 'zipper', 'passwordutils']

    def _addAttribute(self, snippet, attribute):
        return "%s.%s" % (snippet, attribute)

    def create(self, ouputPath: Path):

        snippets = list()

        for entry in self.data:

            entry_current : dict = {
                "id" : entry._Entry__id,
                "default.sem.time" : "",
                "default.sem.state": "",
                "default.syn.time" : "",
                "default.syn.state": "",
                "required.sem.time" : "",
                "required.sem.state": "",
                "required.syn.time" : "",
                "required.syn.state": ""
            }

            for trial in entry._Entry__trials:
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

                current_snipplet = trial._Trial__snipplet[:-5].split('.')
                assert current_snipplet.__len__() == 3

                if current_snipplet[2] == "def":
                    if current_snipplet[1] == "semantic":
                        entry_current.update(
                            {
                                "default.sem.time" : deltatime.total_seconds(),
                                "default.sem.state": trial._Trial__state
                            }
                        )
                    if current_snipplet[1] == "syntactic":
                        entry_current.update(
                            {
                                "default.syn.time" : deltatime.total_seconds(),
                                "default.syn.state": trial._Trial__state
                            }
                        )
                if current_snipplet[2] == "req":
                    if current_snipplet[1] == "semantic":
                        entry_current.update(
                            {
                                "required.sem.time" : deltatime.total_seconds(),
                                "required.sem.state": trial._Trial__state
                            }
                        )
                    if current_snipplet[1] == "syntactic":
                        entry_current.update(
                            {
                                "required.syn.time" : deltatime.total_seconds(),
                                "required.syn.state": trial._Trial__state
                            }
                        )
            snippets.append(entry_current)

        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')
        output_file_path = ouputPath.joinpath(Path("spss_time-constructor_" + ts.__str__() + ".csv")).resolve().absolute()
        if output_file_path.is_absolute():
            output_file_path.touch(mode=0o777, exist_ok=True)
            if output_file_path.is_file():
                output_file = output_file_path.open(mode='w')
                writer = csv.DictWriter(output_file, fieldnames=['id',
                                                                 'default.sem.time','default.sem.state',
                                                                 'required.sem.time', 'required.sem.state',
                                                                 'default.syn.time','default.syn.state',
                                                                 'required.syn.time', 'required.syn.state'
                                                                 ], dialect='excel',
                                            quoting=csv.QUOTE_NONNUMERIC,
                                            delimiter=self.__delimiter)
                writer.writeheader()
                writer.writerows(snippets)
                self.log.debug("Successfully wrote spss_time-constructor .csv")
            else:
                self.log.error("Output file cannot be created!")
                exit(-1)
        else:
            self.log.error("Output file path cannot be resolved!")
            exit(-1)

