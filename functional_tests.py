from cli.test import FunctionalTest
from kalu_parse import KaluParser
import os


class TestVersion(FunctionalTest):
    def test_the_current_version_is_printed_to_the_console(self):
        version = KaluParser.VERSION
        path = KaluParser.get_path()
        command = "./kalu_parse.py -v"
        result = self.run_script(os.path.join(path, command))

        #ProcResult stdout and stderr are b'' not strings
        result.stdout = result.stdout.decode('utf-8')
        result.stderr = result.stderr.decode('utf-8')

        self.assertScriptDoes(result, stdout=version)
