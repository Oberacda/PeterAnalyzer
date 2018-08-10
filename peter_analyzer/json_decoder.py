import json
import logging
from json import JSONDecodeError
from typing import TextIO
import datetime
from pathlib import Path

import coloredlogs


class Key:
    """
    Key event triggerd by the user during the trial.
    """

    __line: list
    __code: int
    __name: str
    __time: str

    def __init__(self, line:list, code:int, name:str, time:datetime.datetime):
        """
        Creates a new key event.
        :param line: the lines shown to the user while the key was pressed.
        :param code: the code of the key press.
        :param name: the name of the key event.
        :param time: the time the event occurred.
        """
        self.__line = line.copy()
        self.__code = code
        self.__name = name
        self.__time = time

class Event:
    """
    Class representing a single event that occures during a trial.
    """

    __code: str
    __type: str
    __time: datetime.datetime

    def __init__(self, code:str, type:str, time:datetime.datetime):
        """
        Creates a new event.
        :param code: code of the event.
        :param type: the type of the event, may be Clock or Snipplet.
        :param time: the time the event occurred.
        """
        self.__code = code
        self.__type = type
        self.__time = time


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
    """
    Class to decode peter json output and mapping it to python files.
    """
    __log: logging.Logger

    def __init__(self, verbose:bool, logdir:Path):
        """
        Creates a new json decoder
        :param verbose: should the decoder log verbose
        :param logdir: the directory to save log files.
        """
        self.__log = logging.getLogger("JsonDecoder")
        self.__log.setLevel(logging.DEBUG)

        formatter = coloredlogs.ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)

        if verbose:

            ch.setLevel(logging.INFO)
        else:
            ch.setLevel(logging.ERROR)

        self.__log.addHandler(ch)

        logfile = Path('peter_json_decoder.log')

        if logdir.exists():
            if logdir.is_dir():
                fh = logging.FileHandler(logdir.joinpath(logfile))
                fh.setLevel(logging.DEBUG)

                # create formatter and add it to the handlers

                fh.setFormatter(formatter)

                self.__log.addHandler(fh)

            else:
                self.__log.error('Specified log dir is no directory')
        else:
            logfile = Path.cwd().joinpath(p).joinpath(logfile)
            logfile.parent.mkdir(parents=True, exist_ok=True)

            fh = logging.FileHandler(logfile)
            fh.setLevel(logging.DEBUG)

            # create formatter and add it to the handlers

            fh.setFormatter(formatter)

            self.__log.addHandler(fh)

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

                events:list = list()
                for event in trial_entry.get('events'):
                    events.append(Event(code=event.get('code'),
                                        type=event.get('type'),
                                        time=datetime.datetime.strptime(event.get('time'), '%Y-%m-%dT%H:%M:%S.%fZ')
                                        )
                                  )


                keys:list = list()
                for key in trial_entry.get('keys'):
                    keys.append(Key(line=key.get('line'),
                                    code=key.get('code'),
                                    name=key.get('name'),
                                    time=datetime.datetime.strptime(key.get('time'), '%Y-%m-%dT%H:%M:%S.%fZ')
                                    )
                                )

                trials.append(Trial(description=trial_entry.get('description'),
                               created=datetime.datetime.strptime(trial_entry.get('created'), '%Y-%m-%dT%H:%M:%S.%f'),
                               keys=keys,
                               correction=trial_entry.get('correction'),
                               submitted=datetime.datetime.strptime(trial_entry.get('submitted'), '%Y-%m-%dT%H:%M:%S.%fZ'),
                               state=trial_entry.get('state'),
                               file=trial_entry.get('file'),
                               linenumber=trial_entry.get('linenumber'),
                               events=events
                              )
                            )

            data_output.append(Entry(timestamp=entry.get('_timestamp'),
                                     user_session_id=entry.get('USER_SESSION_ID'),
                                     id=entry.get('_id'),
                                     forms=entry.get('forms'),
                                     trials=trials)
                               )

        return data_output
