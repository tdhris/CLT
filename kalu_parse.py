#!/usr/bin/env python
from cli.app import CommandLineApp


class KaluParser(CommandLineApp):
    VERSION = "1.0"

    def setup(self):
        CommandLineApp.setup(self)
        self.add_parameters()

    def add_parameters(self):
        self.add_param("-v", "--version",
                       help="See the current version",
                       default=False,
                       action="count")

    def main(self):
        if self.params.version:
            self.get_version()

    def get_version(self):
        print(self.VERSION)


if __name__ == "__main__":
    KaluParser().run()
