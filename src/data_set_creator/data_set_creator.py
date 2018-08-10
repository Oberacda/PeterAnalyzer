from logging import Logger
from pathlib import Path

class DataSetCreator:
    data:list
    log:Logger
    name : str = "DataSetCreator"

    def __init__(self, data: list,log : Logger):
        self.data = data
        self.log = log
        self.log.info(self.name)



    def  create(self,ouputPath : Path):
        pass

    def getName(self):
        return self.name

