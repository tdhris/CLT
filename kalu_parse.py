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
        self.add_param('parse',
                       nargs='?', type=str,
                       choices=['news', 'aur', 'update'],
                       metavar='PARSE_OPTION')

    def main(self):
        if self.params.version:
            self.print_version()
        elif self.params.file:
            self.parse_file(self.params.file)

    def print_version(self):
        print(self.get_version())

    def parse_file(self, input):
        if self.params.parse == 'news':
            parsed = self.parse_news(input)
            self.print_content(parsed)
        elif self.params.parse == 'aur':
            parsed = self.parse_aur(input)
            self.print_content(parsed)
        elif self.params.parse == 'update':
            parsed = self.parse_update(input)
            self.print_content(parsed, True)
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

    def parse_aur(self, input):
        aurs = []
        content = self.get_unparsed_content(input)
        aur_index = self.get_aur_index(content)
        if aur_index:
            for line in content[aur_index + 1:]:
                aur = self.get_line_content(line)
                if aur:
                    aurs.append(aur)
        return aurs

    def parse_update(self, input):
        updates = []
        content = self.get_unparsed_content(input)
        update_start = self.get_update_index(content)
        update_end = self.get_aur_index(content)
        if update_start and update_end:
            update_lines = content[(update_start + 1): update_end]
            for line in update_lines:
                update = self.get_line_content(line)
                if update:
                    update = self.remove_size_info(update)
                    updates.append(update)
        return updates

    def get_unparsed_content(self, input):
        if input == '-':
                lines = sys.stdin.readlines()

        elif os.path.exists(input) and os.path.isfile(input):
            with open(input, 'r') as file:
                lines = file.readlines()
        return lines

    def get_line_content(self, line):
        parts = re.split(r'(- <b>| |<b>|</b>)', line)
        parsed_line = ['->' if part == '>' else part for part in parts
                       if part and not re.match(r'^(- <b>|<b>|</b>)$', part)]
        return ''.join(parsed_line)

    def get_aur_index(self, lines):
        for index, line in enumerate(lines):
                if re.match(r'^AUR: (\d)+ packages updated$', line):
                    return index

    def get_update_index(self, lines):
        for index, line in enumerate(lines):
                if re.match(r'^(\d)+ updates available (.*)$', line):
                    return index

    def remove_size_info(self, line):
        line = re.sub(r'(D: (.)+)', "", line)
        return line[:-3]

    def print_content(self, content, newline=False):
        end_line = ""
        if newline:
            end_line = os.linesep
        for line in content:
            print(line, end=end_line)


if __name__ == "__main__":
    KaluParser(name=__file__).run()
