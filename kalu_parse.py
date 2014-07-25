#!/usr/bin/env python
from cli.app import CommandLineApp, CommandLineMixin
import os
import re
import inspect
import sys
import argparse


class KaluParser(CommandLineApp):
    _VERSION = "1.5"

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
                       action="store_true",)
        self.add_param('-f', '--file',
                       type=str,
                       help="read the contents of the file\
                       and redirect them to stdout. If file\
                       is not provided, read from stdin.")
        self.add_param('news',
                       nargs='?', type=str,
                       choices=['news'])

    def main(self):
        if self.params.version:
            self.print_version()
        elif self.params.file:
            self.parse_file(self.params.file)

    def print_version(self):
        print(self.get_version())

    def parse_file(self, input):
        if self.params.news == 'news':
            parsed = self.parse_news(input)
            self.print_content(parsed)
        else:
            content = self.get_unparsed_content(input)
            self.print_content(content)

    def parse_news(self, input):
        news = []
        content = self.get_unparsed_content(input)
        if content:
            first_line = content[0]
            if re.match(r'^([1-9](\d)*) unread news$', first_line):
                for line in content[1:]:
                    if not line.startswith('-'):
                        break
                    news.append(line[2:])
        return news

    def get_unparsed_content(self, input):
        if input == '-':
                lines = sys.stdin.readlines()

        elif os.path.exists(input) and os.path.isfile(input):
            with open(input, 'r') as file:
                lines = file.readlines()
        return lines

    def print_content(self, content, newline=False):
        end_line = ""
        if newline:
            end_line = "\n"
        for line in content:
            print(line, end=end_line)


if __name__ == "__main__":
    KaluParser(name=__file__).run()
