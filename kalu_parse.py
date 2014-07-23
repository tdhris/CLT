#!/usr/bin/env python
from cli.app import CommandLineApp
import os
import inspect


class KaluParser(CommandLineApp):
    _VERSION = "1.0"

    @classmethod
    def get_version(cls):
        return cls._VERSION

    @classmethod
    def get_path(cls):
        return os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))

    def setup(self):
        CommandLineApp.setup(self)
        self.add_commands()

    def add_commands(self):
        self.add_param("-v", "--version",
                       help="print the current version number and exit",
                       default=False,
                       action="store_true")

    def main(self):
        if self.params.version:
            self.print_version()

    def print_version(self):
        print(self.get_version())


if __name__ == "__main__":
    KaluParser().run()
