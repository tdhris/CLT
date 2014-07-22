from cli.test import FunctionalTest
from kalu_parse import KaluParser


class TestVersion(FunctionalTest):
    def test_the_current_version_is_printed_to_the_console(self):
        version = KaluParser.VERSION
        result = self.run_script("kalu-parse.py", [], ["-v"])
        self.assertScriptDoes(result, stdout=version)
