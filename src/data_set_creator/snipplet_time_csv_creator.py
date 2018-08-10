import platform
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

    __delimiter : str = ';'



    def __init__(self, data: list, log: Logger):
        super().__init__(data, log)

        currentSystem = platform.system()
        if(currentSystem == 'Windows'):
            self.__delimiter = ','

        self.tasks = ['semantic', 'syntactic']
        self.identifier_quality = ['def', 'req']
        self.group = ['datagramMessenger', 'cpanalyzer', 'zipper', 'passwordutils']

    def _addAttribute(self, snippet, attribute):
        return "%s.%s" % (snippet, attribute)

    def create(self, ouputPath: Path):

        snippets = list()

        for entry in self.data:
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
                currentSnipplet = trial._Trial__snipplet[:-5].split('.')
                assert currentSnipplet.__len__() == 3
                snippets.append({"snippet": currentSnipplet[0],"constructor": currentSnipplet[2], "type" : currentSnipplet[1] , "time": deltatime.total_seconds(), "state": trial._Trial__state})

        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')
        output_file_path = ouputPath.joinpath(Path("snippet_time_" + ts.__str__() + ".csv")).resolve().absolute()
        if output_file_path.is_absolute():
            output_file_path.touch(mode=0o777, exist_ok=True)
            if output_file_path.is_file():
                output_file = output_file_path.open(mode='w')
                writer = csv.DictWriter(output_file, fieldnames=['snippet','constructor','type','state', 'time'], dialect='excel',
                                            quoting=csv.QUOTE_NONNUMERIC,
                                            delimiter=self.__delimiter)
                writer.writeheader()
                writer.writerows(snippets)
                self.log.debug("Successfully wrote snippet_time .csv")
            else:
                self.log.error("Output file cannot be created!")
                exit(-1)
        else:
            self.log.error("Output file path cannot be resolved!")
            exit(-1)

