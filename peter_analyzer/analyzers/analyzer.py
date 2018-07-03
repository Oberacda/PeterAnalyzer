from pathlib import Path

class Analyzer:
    __data:list

    def __init__(self, data: list, verbose : bool = True, libdir : Path = Path.cwd()):
        __data = data

    def  analyze(self):
        pass

class TestAnalyzer(Analyzer):
   pass
