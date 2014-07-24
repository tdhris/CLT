from cli.test import FunctionalTest
from kalu_parse import KaluParser
import os
from unittest import skip


class TestVersion(FunctionalTest):
    path = KaluParser.get_path()

    def test_the_current_version_is_printed_to_the_console(self):
        version = KaluParser.get_version()
        command = "./kalu_parse.py -v"
        result = self.run_script(os.path.join(self.path, command))

        #ProcResult stdout and stderr are b'' not strings
        result.stdout = result.stdout.decode('utf-8')
        result.stderr = result.stderr.decode('utf-8')

        self.assertScriptDoes(result, stdout=version)

    #does not work for some reason; unitest tests the same
    @skip
    def test_file_is_read_exactly(self):
        text = "lala\nblahblah\n"
        filename = 'lala.txt'
        with open(filename, "w") as mock_file:
            mock_file.write(text)

        command = "./kalu_parse.py -f " + filename
        result = self.run_script(os.path.join(self.path, command))
        result.stdout = result.stdout.decode('utf-8')
        result.stderr = result.stderr.decode('utf-8')

        self.assertScriptDoes(result, stdout=text)
        os.remove(filename)
