import unittest
from subprocess import check_output
from kalu_parse import KaluParser
import locale

encoding = locale.getdefaultlocale()[1]


class TestBasics(unittest.TestCase):
    def setUp(self):
        self.parser = KaluParser()

    def test_get_version(self):
        output = check_output("./kalu_parse.py -v", shell=True)
        output = output.decode(encoding).rstrip('\n')
        self.assertEquals(self.parser.VERSION, output)


if __name__ == '__main__':
    unittest.main()
