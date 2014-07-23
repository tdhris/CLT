#!/usr/bin/env python
from cli.app import CommandLineApp, CommandLineMixin
import os
import inspect


class KaluParser(CommandLineApp):
    _VERSION = "1.3"

    @classmethod
    def get_version(cls):
        return cls._VERSION

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
        self.add_param('-f', '--file', default='',
                       type=str)

    def main(self):
        if self.params.version:
            self.print_version()
        elif self.params.file:
            self.print_file(self.params.file)

    def print_version(self):
        print(self.get_version())

    def print_file(self, filename):
        try:
            file = open(filename, "r")
            for line in file.readlines():
                print(line.rstrip('\n'))
            file.close()
        except:
            print('File does not exist!')


if __name__ == "__main__":
    KaluParser().run()
