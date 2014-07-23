#!/usr/bin/env python
from cli.app import CommandLineApp
import os
import inspect


class Command:
    SHORT_PREFIX = '-'
    FULL_PREFIX = '--'

    def __init__(self, short, full, help_message, default):
        self._short = short
        self._full = full
        self.help_message = help_message
        self._default = default

    @property
    def short(self):
        return self.SHORT_PREFIX + self._short

    @property
    def full(self):
        return self.FULL_PREFIX + self._full

    @property
    def default(self):
        return self._default


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
        commands = self.load_commands()
        self.add_commands(commands)

    def add_commands(self, commands):
        for command in commands:
            self.add_command(command)

    def add_command(self, command):
        self.add_param(command.short, command.full,
                       help=command.help_message,
                       default=command.default,
                       action="count")

    def load_commands(self):
        commands = []
        version_command = Command("v", "version",
                                  "print the current version number and exit",
                                  False)
        commands.append(version_command)
        return commands

    def main(self):
        if self.params.version:
            self.print_version()

    def print_version(self):
        print(self.get_version())


if __name__ == "__main__":
    KaluParser().run()
