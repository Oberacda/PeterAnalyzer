import json
import logging
from json import JSONDecodeError
from typing import TextIO
import datetime


class Key:
    line: list
    code: int
    name: str
    time: str


class Event:
    code: str
    type: str
    time: str


class Trial:
    """
    Class representing a single trial consisting of one single snipplet and all related data.
    """
    __description: str
    __created: datetime.datetime
    __keys: list
    __correction: str
    __submitted: datetime.datetime
    __state: str
    __snipplet: str
    __linenumber: int
    __events: list

    def __init__(self, description: str, created: datetime.datetime, keys: list, correction: str, submitted: datetime,
                 state: str, file: str, linenumber: int, events: list):
        """
        Creates a new trial instance.
        :param description: The description of the detected error supplied by the subject.
        :param created: the datetime the trial was created.
        :param keys: a list of all keyevents recorded during the trial.
        :param correction: the correction supplied by the subject.
        :param submitted: the datetime the trial was submitted.
        :param state: the state of the trial, may be solved, failed or elapsed.
        :param file: the snipplet the subject looked at.
        :param linenumber: the line number the subject suspected the error.
        :param events: All events recorded during the trial.
        """
        self.__description = description
        self.__created = created
        self.__keys = keys
        self.__correction = correction
        self.__submitted = submitted
        self.__state = state
        self.__snipplet = file
        self.__linenumber = linenumber
        self.__events = events


class Entry:
    """
    Class to represent a single entry in the result database. Every entry represents one user session.
    """
    __timestamp: datetime.datetime
    __user_session_id: str
    __id: str
    __forms: list
    __trials: list

    def __init__(self, timestamp: datetime.datetime, user_session_id: str, id: str, forms: list, trials: list):
        """
        Creates a new Entry.
        :param timestamp: the timestamp the entry was originally created at.
        :param user_session_id: the session id.
        :param id: the id of the entry in the database.
        :param forms: the submitted forms.
        :param trials: the submitted trials.
        """
        self.__timestamp = timestamp
        self.__user_session_id = user_session_id
        self.__id = id
        self.__forms = forms
        self.__trials = trials


class PeterJsonDecoder:
    __log: logging.Logger

    def __init__(self):
        self.__log = logging.getLogger("PeterJsonDecoder")
        self.__log.setLevel(logging.DEBUG)

        fh = logging.FileHandler('peter_json_decoder.log')
        fh.setLevel(logging.DEBUG)

        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        self.__log.addHandler(fh)
        self.__log.addHandler(ch)

    def decode(self, json_file: TextIO) -> list:
        """
        Decodes a peter json db file and mappes the content to the supplied classes.
        :param json_file: the json file to analyze.
        :return: a list of all found entries in the json file. May be a empty list if the json file was invalid.
        """
        self.__log.info("Loading json data from \"%s\"", json_file.name)
        json_data: dict
        try:
            json_data = json.load(json_file)

        except JSONDecodeError as exc:
            self.__log.exception(exc, exc_info=False)
            return list()

        data: list = json_data.get('data')
        data_output = []

        for entry in data:

            self.__log.debug("Decoding entry with id \"%s\"", entry.get('_id'))
            trials:list = list()

            for trial_entry in entry.get('trials'):
                self.__log.debug("Decoding trial with snipplet \"%s\"", trial_entry.get('file'))
                trials.append(Trial(description=trial_entry.get('description'),
                               created=datetime.datetime.strptime(trial_entry.get('created'), '%Y-%m-%dT%H:%M:%S.%f'),
                               keys=trial_entry.get('keys'),
                               correction=trial_entry.get('correction'),
                               submitted=datetime.datetime.strptime(trial_entry.get('submitted'), '%Y-%m-%dT%H:%M:%S.%fZ'),
                               state=trial_entry.get('state'),
                               file=trial_entry.get('file'),
                               linenumber=trial_entry.get('linenumber'),
                               events=trial_entry.get('events')
                               )
                              )

            data_output.append(Entry(timestamp=entry.get('_timestamp'),
                                     user_session_id=entry.get('USER_SESSION_ID'),
                                     id=entry.get('_id'),
                                     forms=entry.get('forms'),
                                     trials=trials)
                               )

        return data
