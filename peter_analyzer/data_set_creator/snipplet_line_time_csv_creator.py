import time
import platform

from peter_analyzer.data_set_creator.data_set_creator import DataSetCreator
from logging import Logger
from pathlib import Path
import csv
import datetime

class SnippletLineTimeCvsCreator(DataSetCreator):
    name = "SnippletLineTimeCvsCreator"


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

                defectline : int = 0
                docline : int = 0
                maxline : int = 0


                currentSnipplet = trial._Trial__snipplet[:-5].split('.')
                assert currentSnipplet.__len__() == 3

                currentSnippletDict = next((item for item in snippets if item["snippet"] == currentSnipplet[0] and item["constructor"] == currentSnipplet[2] and
                                         item["type"] == currentSnipplet[1]), None)

                if currentSnippletDict is None:
                    currentSnippletDict = {"snippet": currentSnipplet[0], "constructor": currentSnipplet[2],
                                         "type": currentSnipplet[1], "lines" : list()}
                    snippets.append(currentSnippletDict)

                if currentSnippletDict["snippet"] == "datagramMessenger":
                    defectline = 144
                    docline = 100
                    maxline = 185

                if currentSnippletDict["snippet"] == "zipper":
                    defectline = 155
                    docline = 111
                    maxline = 177


                if currentSnippletDict["snippet"] == "passwordutils":
                    defectline = 189
                    docline = 136
                    maxline = 205

                if currentSnippletDict["snippet"] == "cpanalyzer":
                    defectline = 111
                    maxline = 136
                    docline = 81

                assert defectline > 0 and maxline > 0 and docline > 0
                assert docline < defectline < maxline

                for event in trial._Trial__events:
                    if event._Event__code == "Start" and event._Event__type == "Snippet" :
                        starttime = event._Event__time

                assert starttime is not None

                firstline : int = 1
                lastline : int = 17

                for key in trial._Trial__keys:
                    delta = key._Key__time - starttime
                    starttime = key._Key__time
                    assert key._Key__line.__len__() == 2

                    for line in range(firstline, lastline):
                        currentLine = {"time": delta.total_seconds(),
                                         "line": line}

                        lable : str = None

                        if line < docline + 10:
                            lable = 'doc'
                        if line >= docline + 10 and line < defectline - 10:
                            lable = 'pre'
                        if defectline - 10 <= line <= defectline + 10:
                            lable = 'def'
                        if line > defectline + 10:
                            lable = 'post'

                        assert lable is not None

                        cline = next((item for item in currentSnippletDict['lines'] if item["line"] == line),None)

                        if cline is not None:
                            previousLine = currentSnippletDict['lines'].pop(currentSnippletDict['lines'].index(cline))
                            currentSnippletDict['lines'].append({"time": delta.total_seconds() + previousLine['time'],
                                         "line": line, "lable" : lable})
                        else:
                            currentSnippletDict['lines'].append(currentLine)

                    if key._Key__name == 'down':
                        if lastline + 2 < maxline:
                            firstline = firstline + 2
                            lastline = lastline + 2
                    if key._Key__name == 'up':
                        if firstline - 2 > 0:
                            firstline = firstline - 2
                            lastline = lastline - 2
                    assert firstline < lastline and firstline > 0

        snippletsComplete = list()

        for snipplet in snippets:
            root = {"snippet": snipplet['snippet'], "constructor": snipplet['constructor'],
                                         "type": snipplet['type']}
            for line in snipplet['lines']:
                snippletsComplete.append({**root, **line})

        snippletsComplete =  sorted(snippletsComplete , key=lambda elem: "%s %s %s %d" % (elem['snippet'], elem['constructor'], elem['type'], elem['line']))
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')
        output_file_path = ouputPath.joinpath(Path("snippet_time_line_" + ts.__str__() + ".csv")).resolve().absolute()
        if output_file_path.is_absolute():
            output_file_path.touch(mode=0o777, exist_ok=True)
            if output_file_path.is_file():
                output_file = output_file_path.open(mode='w')
                writer = csv.DictWriter(output_file, fieldnames=['snippet','constructor','type','line', 'lable', 'time'], dialect='excel',
                                            quoting=csv.QUOTE_NONNUMERIC,
                                            delimiter=self.__delimiter)
                writer.writeheader()
                writer.writerows(snippletsComplete)
                self.log.debug("Successfully wrote snippet_time .csv")
            else:
                self.log.error("Output file cannot be created!")
                exit(-1)
        else:
            self.log.error("Output file path cannot be resolved!")
            exit(-1)

