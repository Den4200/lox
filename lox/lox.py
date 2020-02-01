import sys
from pathlib import Path

from .scanner import Scanner
from .exceptions import Error


class Lox:

    def __init__(self, *args, **kwargs) -> None:
        if len(sys.argv) > 2:
            print('Usage: lox: [script]')
            sys.exit(1)

        elif len(sys.argv) == 2:
            self.run_file(sys.argv[1])

        else:
            self.run_prompt()

    def run_file(self, file: str) -> None:
        with open(file, 'r') as f:
            self.run(f.read())

    def run_prompt(self) -> None:
        while True:
            try:
                self.run(input('> '))
            except KeyboardInterrupt:
                sys.exit(0)

    def run(self, source: str) -> None:
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        for token in tokens:
            print(token.to_string())
