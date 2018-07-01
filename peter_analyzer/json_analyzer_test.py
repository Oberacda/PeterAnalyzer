import unittest
from typing import TextIO

from peter_analyzer import json_decoder

class PeterJsonDecoderTest(unittest.TestCase):

    jsonDecoder : json_decoder.PeterJsonDecoder
    fullDatabaseFile : TextIO
    singleDatabaseEntry : TextIO
    invalidDatabaseEntry : TextIO

    def setUp(self):
        self.fullDatabaseFile = open("../resources/db-2018-06-19.json")
        self.singleDatabaseEntry = open("../resources/example_entry.json")
        self.invalidDatabaseEntry = open("../resources/db-2018-06-19.jso")
        self.jsonDecoder = json_decoder.PeterJsonDecoder()

    def tearDown(self):
        self.fullDatabaseFile.close()
        self.singleDatabaseEntry.close()
        self.invalidDatabaseEntry.close()

    def test_decoding(self):
        self.jsonDecoder.decode(self.fullDatabaseFile)

    def test_decoding_invalid(self):
        self.assertListEqual(self.jsonDecoder.decode(self.invalidDatabaseEntry), list())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()