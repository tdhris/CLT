import unittest
from subprocess import check_output
from kalu_parse import KaluParser


class TestBasics(unittest.TestCase):
    def setUp(self):
        self.parser = KaluParser()

    def test_get_version(self):
        output = check_output("./kalu_parse.py -v", shell=True).rstrip('\n')
        self.assertEquals(self.parser.VERSION, output)


if __name__ == '__main__':
    unittest.main()
