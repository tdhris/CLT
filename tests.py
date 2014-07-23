import unittest
from cli.test import AppTest
from subprocess import check_output
from kalu_parse import KaluParser, Command
import locale
import os

encoding = locale.getdefaultlocale()[1]


class TestCommand(unittest.TestCase):
    def setUp(self):
        def foo():
            pass

        self.command = Command("l", "list", "lists dir", False, "store_true", foo)

    def test_command_short_form_is_correct(self):
        self.assertEquals('-l', self.command.short)

    def test_command_full_form_is_correct(self):
        self.assertEquals('--list', self.command.full)

    def test_help_message_and_default_are_correct(self):
        self.assertEquals('lists dir', self.command.help_message)
        self.assertFalse(self.command.default)
        new_help = "Blah"
        self.command.help_message = new_help
        self.assertEquals(new_help, self.command.help_message)


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

    def test_a_command_can_be_added(self):
        def blah():
            print("blah")

        command = Command("b", "blah", "prints blah", False, "store_true", blah)
        self.app_cls.add_command(command)
        self.assertIn(command, self.app_cls._COMMANDS)


if __name__ == '__main__':
    unittest.main()
