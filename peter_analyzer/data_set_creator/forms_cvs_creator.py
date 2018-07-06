from data_set_creator.data_set_creator import DataSetCreator
from logging import Logger
from pathlib import Path
import csv

class FormCvsCreator(DataSetCreator):
    name = "FormCvsCreator"

    def __init__(self, data: list, log: Logger):
        super().__init__(data, log)

    def create(self, ouputPath : Path):

        result : list = list()

        for entry in self.data:
            result.append({"id" : entry._Entry__id,
             "culture" : entry._Entry__forms[0]['culture'],
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

        fieldnames = ["id","culture","academic_degree",
             "job_description",
             "school_leave_qualification",
             "jobtype",
             "years_experience_java",
             "java",
             "python",
             "mother_tounge",
             "js",
             "c_or_cpp",
             "csharp",
             "net",
             "php",
             "years_experience_any"]

        output_file_path = ouputPath.joinpath(Path("forms.csv")).resolve()
        if output_file_path.is_absolute():
            output_file_path.touch(mode=0o777, exist_ok=True)
            if output_file_path.is_file():
                output_file = output_file_path.open(mode='w')
                writer = csv.DictWriter(output_file, fieldnames=fieldnames, dialect='excel', quoting=csv.QUOTE_NONNUMERIC,
                                    delimiter=';')
                writer.writeheader()
                writer.writerows(result)
            else:
                self.log.error("Output file cannot be created!")
                exit(-1)
        else:
            self.log.error("Output file path cannot be resolved!")
            exit(-1)

