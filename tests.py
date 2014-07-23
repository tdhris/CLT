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


if __name__ == '__main__':
    unittest.main()
