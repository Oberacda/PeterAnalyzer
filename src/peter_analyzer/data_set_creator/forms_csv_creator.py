import time
import platform

from peter_analyzer.data_set_creator.data_set_creator import DataSetCreator
from logging import Logger
from pathlib import Path
import csv
import datetime


class FormCvsCreator(DataSetCreator):
    name = "FormCvsCreator"

    __seperate:bool

    __delimiter : str = ';'

    def __init__(self, data: list, log: Logger, seperate: bool = False):
        super().__init__(data, log)
        self.__seperate = seperate

        currentSystem = platform.system()
        if (currentSystem == 'Windows'):
            self.delimiter = ','

    def create(self, ouputPath: Path):

        result_2: list = list()
        result_4: list = list()

        for entry in self.data:

            self.log.debug("Entry len: " + str(len(entry._Entry__forms)))

            if len(entry._Entry__forms) == 2:
                if(not (entry._Entry__forms[0]['source'] == "/static/templates/forms/questions1.de.html" and
                        entry._Entry__forms[1]['source'] == "/static/templates/forms/questions2.de.html")):
                    self.log.warning("Missing forms, form 1 or 2 are missing!")
                    continue

                result_2.append({"id": entry._Entry__id,
                                 "culture": entry._Entry__forms[0]['culture'],
                                 "academic_degree": entry._Entry__forms[0]['academic_degree'],
                                 "job_description": entry._Entry__forms[0]['job_description'],
                                 "school_leave_qualification": entry._Entry__forms[0]['school_leave_qualification'],
                                 "jobtype": entry._Entry__forms[0]['jobtype'],
                                 "years_experience_java": entry._Entry__forms[1]['years_experience_java'],
                                 "java": entry._Entry__forms[1]['java'],
                                 "python": entry._Entry__forms[1]['python'],
                                 "mother_tounge": entry._Entry__forms[1]['mother_tounge'],
                                 "js": entry._Entry__forms[1]['js'],
                                 "c_or_cpp": entry._Entry__forms[1]['c_or_cpp'],
                                 "csharp": entry._Entry__forms[1]['csharp'],
                                 "net": entry._Entry__forms[1]['net'],
                                 "php": entry._Entry__forms[1]['php'],
                                 "years_experience_any": entry._Entry__forms[1]['years_experience_any']
                                 })
            if len(entry._Entry__forms) == 4:
                if (not (entry._Entry__forms[0]['source'] == "/static/templates/forms/questions1.de.html" and
                         entry._Entry__forms[1]['source'] == "/static/templates/forms/questions2.de.html" and
                         entry._Entry__forms[2]['source'] == "/static/templates/forms/questions4.de.html" and
                         entry._Entry__forms[3]['source'] == "/static/templates/forms/questions3.de.html")):
                    self.log.warning("Missing forms, form 1,2,4 or 3 are missing!")
                    continue
                result_4.append({"id": entry._Entry__id,
                                 "culture": entry._Entry__forms[0]['culture'],
                                 "academic_degree": entry._Entry__forms[0]['academic_degree'],
                                 "job_description": entry._Entry__forms[0]['job_description'],
                                 "school_leave_qualification": entry._Entry__forms[0]['school_leave_qualification'],
                                 "jobtype": entry._Entry__forms[0]['jobtype'],
                                 "years_experience_java": entry._Entry__forms[1]['years_experience_java'],
                                 "java": entry._Entry__forms[1]['java'],
                                 "python": entry._Entry__forms[1]['python'],
                                 "mother_tounge": entry._Entry__forms[1]['mother_tounge'],
                                 "js": entry._Entry__forms[1]['js'],
                                 "c_or_cpp": entry._Entry__forms[1]['c_or_cpp'],
                                 "csharp": entry._Entry__forms[1]['csharp'],
                                 "net": entry._Entry__forms[1]['net'],
                                 "php": entry._Entry__forms[1]['php'],
                                 "years_experience_any": entry._Entry__forms[1]['years_experience_any'],
                                 "simplicity": entry._Entry__forms[2]['simplicity'],
                                 "only_run": entry._Entry__forms[2]['only_run'],
                                 "developmenttime": entry._Entry__forms[2]['developmenttime'],
                                 "results": entry._Entry__forms[2]['results'],
                                 "understanding": entry._Entry__forms[2]['understanding'],
                                 "whatoverwhy": entry._Entry__forms[2]['whatoverwhy'],
                                 "control_run": entry._Entry__forms[2]['control_run'],
                                 "configuration": entry._Entry__forms[2]['configuration'],
                                 "efficency": entry._Entry__forms[2]['efficency'],
                                 "know_api": entry._Entry__forms[3]['know_api'],
                                 "german_level": entry._Entry__forms[3]['german_level'],
                                 "age": entry._Entry__forms[3]['age'],
                                 "sex": entry._Entry__forms[3]['sex'],
                                 "encountered_distraction": entry._Entry__forms[3]['encountered_distraction'],
                                 "english_level": entry._Entry__forms[3]['english_level']
                                 })

        if self.__seperate:
            fieldnames_2 = ["id",
                            "culture",
                            "academic_degree",
                            "job_description",
                            "school_leave_qualification",
                            "jobtype",
                            "mother_tounge",
                            "years_experience_java",
                            "years_experience_any",
                            "java",
                            "python",
                            "js",
                            "c_or_cpp",
                            "csharp",
                            "net",
                            "php"]
            ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')
            output_file_path = ouputPath.joinpath(Path("forms_" + ts.__str__() + ".csv")).resolve().absolute()
            if output_file_path.is_absolute():
                output_file_path.touch(mode=0o777, exist_ok=True)
                if output_file_path.is_file():
                    output_file = output_file_path.open(mode='w')
                    writer = csv.DictWriter(output_file, fieldnames=fieldnames_2, dialect='excel',
                                            quoting=csv.QUOTE_NONNUMERIC,
                                            delimiter=self.__delimiter)
                    writer.writeheader()
                    writer.writerows(result_2)
                    self.log.debug("Successfully wrote forms_2.csv")
                else:
                    self.log.error("Output file cannot be created!")
                    exit(-1)
            else:
                self.log.error("Output file path cannot be resolved!")
                exit(-1)
        else:
            result_4.extend(result_2)

        fieldnames = ["id",
                        "culture",
                        "age",
                        "sex",
                        "academic_degree",
                        "job_description",
                        "school_leave_qualification",
                        "jobtype",
                        "mother_tounge",
                        "english_level",
                        "german_level",
                        "years_experience_java",
                        "years_experience_any",
                        "java",
                        "python",
                        "js",
                        "c_or_cpp",
                        "csharp",
                        "net",
                        "php",
                        "simplicity",
                        "only_run",
                        "developmenttime",
                        "results",
                        "understanding",
                        "whatoverwhy",
                        "control_run",
                        "configuration",
                        "efficency",
                        "culture",
                        "know_api",

                        "encountered_distraction"
                        ]

        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H%M%S')
        output_file_path = ouputPath.joinpath(Path("forms_" + ts.__str__() + ".csv")).resolve().absolute()
        if output_file_path.is_absolute():
            output_file_path.touch(mode=0o777, exist_ok=True)
            if output_file_path.is_file():
                output_file = output_file_path.open(mode='w')
                writer = csv.DictWriter(output_file, fieldnames=fieldnames, dialect='excel',
                                        quoting=csv.QUOTE_NONNUMERIC,
                                        delimiter=self.__delimiter)
                writer.writeheader()
                writer.writerows(result_4)
                self.log.debug("Successfully wrote forms.csv")
            else:
                self.log.error("Output file cannot be created!")
                exit(-1)
        else:
            self.log.error("Output file path cannot be resolved!")
            exit(-1)

