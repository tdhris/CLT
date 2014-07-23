#!/usr/bin/env python
from cli.app import CommandLineApp
import os
import inspect


class Command:
    SHORT_PREFIX = '-'
    FULL_PREFIX = '--'

    def __init__(self, short, full, help_message, default, action, function):
        self._short = short
        self._full = full
        self.help_message = help_message
        self._default = default
        self._action = action
        self._function = function
        self._name = full

    def __eq__(self, other):
        return self.name == other.name

    @property
    def short(self):
        return self.SHORT_PREFIX + self._short

    @property
    def full(self):
        return self.FULL_PREFIX + self._full

    @property
    def name(self):
        return self._name

    @property
    def action(self):
        return self._action

    @property
    def function(self):
        return self._function

    @property
    def default(self):
        return self._default


class KaluParser(CommandLineApp):
    _VERSION = "1.0"
    _COMMANDS = []

    @classmethod
    def get_version(cls):
        return cls._VERSION

    @classmethod
    def get_path(cls):
        return os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))

    def setup(self):
        CommandLineApp.setup(self)
        self.load_commands()
        self.add_commands()

    def add_commands(self):
        for command in self._COMMANDS:
            self.add_command(command)

    def add_command(self, command):
        self.add_param(command.short, command.full,
                       help=command.help_message,
                       default=command.default,
                       action=command.action)
        if command not in self._COMMANDS:
            self._COMMANDS.append(command)

    def load_commands(self):
        self._COMMANDS = []
        version_command = Command("v", "version",
                                  "print the current version number and exit",
                                  False, "store_true", self.print_version)
        self._COMMANDS.append(version_command)

    def main(self):
        for command in self._COMMANDS:
            if hasattr(self.params, command.name):
                command.function()

    def print_version(self):
        print(self.get_version())


if __name__ == "__main__":
    KaluParser().run()
