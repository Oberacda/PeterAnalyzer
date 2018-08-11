import time
import platform

from peter_analyzer.data_set_creator.data_set_creator import DataSetCreator
from logging import Logger
from pathlib import Path
import csv
import datetime


class SnippletLineTimeCvsCreator(DataSetCreator):
    name = "CSV_Spss_Time-Constructor-Section"

    __snipplet_name = []
    task: list
    identifier: list
    group: list

    __delimiter: str = ','

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

            entry_current: dict = {
                "id": entry._Entry__id,
                "default.sem.time": "",
                "default.sem.doc": "",
                "default.sem.pre": "",
                "default.sem.def": "",
                "default.sem.post": "",
                "default.sem.state": "",
                "default.syn.time": "",
                "default.syn.doc": "",
                "default.syn.pre": "",
                "default.syn.def": "",
                "default.syn.post": "",
                "default.syn.state": "",
                "required.sem.time": "",
                "required.sem.doc": "",
                "required.sem.pre": "",
                "required.sem.def": "",
                "required.sem.post": "",
                "required.sem.state": "",
                "required.syn.time": "",
                "required.syn.doc": "",
                "required.syn.pre": "",
                "required.syn.def": "",
                "required.syn.post": "",
                "required.syn.state": ""
            }

            for trial in entry._Entry__trials:
                starttime: datetime.datetime = None
                endtime: datetime.datetime = None

                for event in trial._Trial__events:
                    if event._Event__code == "Start" and event._Event__type == "Snippet":
                        starttime = event._Event__time
                    if event._Event__code == "Done" and event._Event__type == "Snippet":
                        endtime = event._Event__time
                    if event._Event__code == "Elapsed" and event._Event__type == "Clock":
                        endtime = event._Event__time
                totaltime = endtime - starttime
                totaltime = totaltime.total_seconds()

                current_snipplet = trial._Trial__snipplet[:-5].split('.')
                assert current_snipplet.__len__() == 3

                starttime: datetime.datetime = None

                defectline: int = 0
                docline: int = 0
                maxline: int = 0

                if current_snipplet[0] == "datagramMessenger":
                    defectline = 144
                    docline = 100
                    maxline = 185

                if current_snipplet[0] == "zipper":
                    defectline = 155
                    docline = 111
                    maxline = 177

                if current_snipplet[0] == "passwordutils":
                    defectline = 189
                    docline = 136
                    maxline = 205

                if current_snipplet[0] == "cpanalyzer":
                    defectline = 111
                    maxline = 136
                    docline = 81

                assert defectline > 0 and maxline > 0 and docline > 0
                assert docline < defectline < maxline

                for event in trial._Trial__events:
                    if event._Event__code == "Start" and event._Event__type == "Snippet":
                        starttime = event._Event__time

                assert starttime is not None

                firstline: int = 1
                lastline: int = 17

                doc_time  =  0.0
                pre_time =  0.0
                def_time =  0.0
                post_time =  0.0

                for key in trial._Trial__keys:
                    delta = (key._Key__time - starttime).total_seconds()
                    starttime = key._Key__time
                    assert key._Key__line.__len__() == 2

                    for line in range(firstline, lastline):

                        if line < docline + 10:
                            doc_time += delta
                        if docline + 10 <= line < defectline - 10:
                            pre_time += delta
                        if defectline - 10 <= line <= defectline + 10:
                            def_time += delta
                        if line > defectline + 10:
                            post_time += delta

                    if key._Key__name == 'down':
                        if lastline + 2 < maxline:
                            firstline = firstline + 2
                            lastline = lastline + 2
                    if key._Key__name == 'up':
                        if firstline - 2 > 0:
                            firstline = firstline - 2
                            lastline = lastline - 2
                    assert lastline > firstline > 0

                doc_time /= (15 * totaltime)
                pre_time /= (15 * totaltime)
                def_time /= (15 * totaltime)
                post_time /= (15 * totaltime)

                if current_snipplet[2] == "def":
                    if current_snipplet[1] == "semantic":
                        entry_current.update(
                            {
                                "default.sem.time": totaltime,
                                "default.sem.doc": doc_time,
                                "default.sem.pre": pre_time,
                                "default.sem.def": def_time,
                                "default.sem.post": post_time,
                                "default.sem.state": trial._Trial__state
                            }
                        )
                    if current_snipplet[1] == "syntactic":
                        entry_current.update(
                            {
                                "default.syn.time": totaltime,
                                "default.syn.doc": doc_time,
                                "default.syn.pre": pre_time,
                                "default.syn.def": def_time,
                                "default.syn.post": post_time,
                                "default.syn.state": trial._Trial__state
                            }
                        )
                if current_snipplet[2] == "req":
                    if current_snipplet[1] == "semantic":
                        entry_current.update(
                            {
                                "required.sem.time": totaltime,
                                "required.sem.doc": doc_time,
                                "required.sem.pre": pre_time,
                                "required.sem.def": def_time,
                                "required.sem.post": post_time,
                                "required.sem.state": trial._Trial__state
                            }
                        )
                    if current_snipplet[1] == "syntactic":
                        entry_current.update(
                            {
                                "required.syn.time": totaltime,
                                "required.syn.doc": doc_time,
                                "required.syn.pre": pre_time,
                                "required.syn.def": def_time,
                                "required.syn.post": post_time,
                                "required.syn.state": trial._Trial__state
                            }
                        )

            snippets.append(entry_current)

        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')
        output_file_path = ouputPath.joinpath(
            Path("spss_time-constructor-section_" + ts.__str__() + ".csv")).resolve().absolute()
        if output_file_path.is_absolute():
            output_file_path.touch(mode=0o777, exist_ok=True)
            if output_file_path.is_file():
                output_file = output_file_path.open(mode='w')
                writer = csv.DictWriter(output_file, fieldnames=["id",
                                                                 "default.sem.time",
                                                                 "default.sem.doc",
                                                                 "default.sem.pre",
                                                                 "default.sem.def",
                                                                 "default.sem.post",
                                                                 "default.sem.state",
                                                                 "default.syn.time",
                                                                 "default.syn.doc",
                                                                 "default.syn.pre",
                                                                 "default.syn.def",
                                                                 "default.syn.post",
                                                                 "default.syn.state",
                                                                 "required.sem.time",
                                                                 "required.sem.doc",
                                                                 "required.sem.pre",
                                                                 "required.sem.def",
                                                                 "required.sem.post",
                                                                 "required.sem.state",
                                                                 "required.syn.time",
                                                                 "required.syn.doc",
                                                                 "required.syn.pre",
                                                                 "required.syn.def",
                                                                 "required.syn.post",
                                                                 "required.syn.state"
                                                                 ], dialect='excel',
                                        quoting=csv.QUOTE_NONNUMERIC,
                                        delimiter=self.__delimiter)
                writer.writeheader()
                writer.writerows(snippets)
                self.log.debug("Successfully wrote spss_time-constructor-section .csv")
            else:
                self.log.error("Output file cannot be created!")
                exit(-1)
        else:
            self.log.error("Output file path cannot be resolved!")
            exit(-1)
