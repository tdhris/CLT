import unittest
from cli.test import AppTest
from subprocess import check_output, check_call
from kalu_parse import KaluParser
import locale
import os

encoding = locale.getdefaultlocale()[1]


class TestBasicKaluParserFunctions(AppTest):
    def setUp(self):
        self.app_cls = KaluParser()
        os.chdir(self.app_cls.get_path())

    def test_get_version(self):
        output = check_output("./kalu_parse.py news -v", shell=True)
        output = output.decode(encoding).rstrip('\n')
        self.assertEquals(self.app_cls.get_version(), output)
        self.assertIn(KaluParser._get_modulename() + " version ", output)

    def test_get_path_returns_correct_path(self):
        self.assertIn('kalu_parse.py', os.listdir())

    def test_help(self):
        output = check_output("./kalu_parse.py -h", shell=True)
        output = output.decode(encoding)
        self.assertIn('print the current version number and exit', output)
        self.assertIn('--version', output)
        self.assertIn('--help', output)

    #skipping tests because the script should not work without positional arguments
    @unittest.skip
    def test_read_file_when_file_does_not_end_with_newline(self):
        text = "lala\nblahblah"
        with open("blah.txt", "w") as mock_file:
            mock_file.write(text)
        output = check_output("./kalu_parse.py -f blah.txt", shell=True)
        output = output.decode(encoding).rstrip('\n')
        self.assertEquals(text, output)
        os.remove("blah.txt")

    @unittest.skip
    def test_read_file_when_file_ends_with_newline(self):
        text = "lala\nblahblah\n"
        with open("blah.txt", "w") as mock_file:
            mock_file.write(text)
        output = check_output("./kalu_parse.py -f blah.txt", shell=True)
        output = output.decode(encoding)
        self.assertEquals(text, output)
        os.remove("blah.txt")

    @unittest.skip
    def test_no_difference(self):
        text = "lala\nblahblah\n"
        with open("blah.txt", "w") as mock_file:
            mock_file.write(text)
        check_call("./kalu_parse.py -f blah.txt > lala.txt", shell=True)
        output_dest = check_output("./kalu_parse.py -f lala.txt", shell=True)
        output_dest = output_dest.decode(encoding)
        self.assertEquals(text, output_dest)
        os.remove("blah.txt")
        os.remove("lala.txt")

    @unittest.skip
    def test_can_capture_from_standard_input(self):
        text = "lala\nblahblah\n"
        with open("lalasa.txt", "w") as mock_file:
            mock_file.write(text)
        output = check_output("cat lalasa.txt | ./kalu_parse.py -f -", shell=True)
        output = output.decode(encoding)
        self.assertEquals(text, output)
        os.remove("lalasa.txt")

    def test_module_name_in_help(self):
        output = check_output("./kalu_parse.py -h", shell=True)
        output = output.decode(encoding)
        self.assertIn(KaluParser._get_modulename(), output)


class TestParser(AppTest):
    def setUp(self):
        self.parser = KaluParser()

    def test_news_print_one_news_items(self):
        output = check_output("./kalu_parse.py news -f kalu_output.txt", shell=True)
        output = output.decode(encoding)
        self.assertIn("MariaDB 10.0 enters [extra]", output)

    def test_aur_parser(self):
        output = check_output("./kalu_parse.py aur -f kalu_output.txt", shell=True)
        output = output.decode(encoding)
        self.assertIn("xpra-winswitch 0.13.6-1 -> 0.13.7-1", output)

    def test_update_parser(self):
        output = check_output("./kalu_parse.py update -f kalu_output.txt", shell=True)
        output = output.decode(encoding)
        self.assertIn("poppler 0.26.2-1 -> 0.26.3-1", output)


if __name__ == '__main__':
    unittest.main()
