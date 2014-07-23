import unittest
from cli.test import AppTest
from subprocess import check_output
from kalu_parse import KaluParser
import locale
import os

encoding = locale.getdefaultlocale()[1]


class TestBasicKaluParserFunctions(AppTest):
    def setUp(self):
        self.app_cls = KaluParser()
        os.chdir(self.app_cls.get_path())

    def test_get_version(self):
        output = check_output("./kalu_parse.py -v", shell=True)
        output = output.decode(encoding).rstrip('\n')
        self.assertEquals(self.app_cls.get_version(), output)

    def test_get_path_returns_correct_path(self):
        self.assertIn('kalu_parse.py', os.listdir())

    def test_help(self):
        output = check_output("./kalu_parse.py -h", shell=True)
        output = output.decode(encoding)
        self.assertIn('print the current version number and exit', output)
        self.assertIn('--version', output)
        self.assertIn('--help', output)

    def test_read_file_when_file_does_not_end_with_newline(self):
        text = "lala\nblahblah"
        with open("blah.txt", "w") as mock_file:
            mock_file.write(text)
        output = check_output("./kalu_parse.py -f blah.txt", shell=True)
        output = output.decode(encoding).rstrip('\n')
        self.assertEquals(text, output)
        os.remove("blah.txt")

    def test_read_file_when_file_ends_with_newline(self):
        text = "lala\nblahblah\n"
        with open("blah.txt", "w") as mock_file:
            mock_file.write(text)
        output = check_output("./kalu_parse.py -f blah.txt", shell=True)
        output = output.decode(encoding)
        self.assertEquals(text, output)
        os.remove("blah.txt")


if __name__ == '__main__':
    unittest.main()
