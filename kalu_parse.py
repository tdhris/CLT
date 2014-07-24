#!/usr/bin/env python
from cli.app import CommandLineApp, CommandLineMixin
import os
import inspect
import sys


class KaluParser(CommandLineApp):
    _VERSION = "1.4"

    @classmethod
    def get_version(cls):
        return cls._get_modulename() + " version " + cls._VERSION

    @classmethod
    def _get_modulename(cls):
        return ''.join(os.path.basename(__file__).split('.')[:-1])

    @classmethod
    def get_path(cls):
        return os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))

    def setup(self):
        CommandLineApp.setup(self)
        CommandLineMixin.setup(self)
        self.add_commands()

    def add_commands(self):
        self.add_param("-v", "--version",
                       help="print the current version number and exit",
                       default=False,
                       action="store_true")
        self.add_param('-f', '--file',
                       nargs='?',
                       type=str,
                       help="read the contents of the file\
                       and redirect them to stdout. If file\
                       is not provided, read from stdin.")

    def main(self):
        if self.params.version:
            self.print_version()
        elif self.params.file:
            self.print_file(self.params.file)

    def print_version(self):
        print(self.get_version())

    def print_file(self, input):
        if input == '-':
            lines = sys.stdin.readlines()

        elif os.path.exists(input) and os.path.isfile(input):
            with open(input, 'r') as file:
                lines = file.readlines()
        for line in lines:
            print(line, end="")


if __name__ == "__main__":
    KaluParser(name=__file__).run()
