import json
import logging
from json import JSONDecodeError
from typing import TextIO


class Key_Entry:
    line: list
    code: int
    name: str
    time: str


class Event_Entry:
    code: str
    type: str
    time: str


class Trial_Entry:
    description: str
    created: str
    keys: list
    correction: str
    state: str
    snipplet: str
    linenumber: int
    events: list


class Entry:
    __timestamp: str
    __user_session_id: str
    __id: str
    __forms: list
    __trials: list

    def __init__(self, timestamp: str, user_session_id: str, id: str, forms: list, trials: list):
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
            timestamp = entry.get('_timestamp')
            session_id = entry.get('USER_SESSION_ID')
            id = entry.get('_id')
            forms: list = entry.get('forms')
            trials_encoded = entry.get('trials')

            self.__log.debug("Decoding entry with id \"%s\"", id)
            data_output.append(Entry(timestamp, session_id, id, forms, trials))

        return data


if __name__ == "__main__":
    json_decoder = PeterJsonDecoder()
    s = json_decoder.decode(open("../resources/db-2018-06-19.json"))
    print(s)
