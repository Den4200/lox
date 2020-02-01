from typing import List
from functools import partial

from .token import Token
from .token_type import TokenType
from .exceptions import Error


class Scanner:

    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens = list()

        self.start = 0
        self.current = 0
        self.line = 1

        self.TOKENS = {
            '(': TokenType.LEFT_PAREN,
            ')': TokenType.RIGHT_PAREN,
            '{': TokenType.LEFT_BRACE,
            '}': TokenType.RIGHT_BRACE,
            ',': TokenType.COMMA,
            '.': TokenType.DOT,
            '-': TokenType.MINUS,
            '+': TokenType.PLUS,
            ';': TokenType.SEMICOLON,
            '*': TokenType.STAR,

            '!': partial(self.check, TokenType.BANG_EQUAL, TokenType.BANG),
            '=': partial(self.check, TokenType.EQUAL_EQUAL, TokenType.EQUAL),
            '<': partial(self.check, TokenType.LESS_EQUAL, TokenType.LESS),
            '>': partial(self.check, TokenType.GREATER_EQUAL, TokenType.GREATER),

            '/': self.check_div,

            ' ': 'ignore',
            '\r': 'ignore',
            '\t': 'ignore',

            '\n': self.new_line,

            '"': self.string
        }

        self.KEYWORDS = {
            'and': TokenType.AND,
            'class': TokenType.CLASS,
            'else': TokenType.ELSE,
            'false': TokenType.FALSE,
            'for': TokenType.FOR,
            'fun': TokenType.FUN,
            'if': TokenType.IF,
            'nil': TokenType.NIL,
            'or': TokenType.OR,
            'print': TokenType.PRINT,
            'return': TokenType.RETURN,
            'super': TokenType.SUPER,
            'this': TokenType.THIS,
            'true': TokenType.TRUE,
            'var': TokenType.VAR,
            'while': TokenType.WHILE
        }

    def check(self, true: int, false: int) -> int:
        return true if self.match('=') else false

    def scan_tokens(self) -> List['Token']:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, '', None, self.line))
        return self.tokens

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def scan_token(self) -> None:
        char = self.advance()
        token = self.TOKENS.get(char, None)

        if token is None:

            if char.isdigit():
                self.number()

            elif char.isalpha() or char == '_':
                self.identifier()

            else:
                raise Error(f'Unexpected character at line {self.line}')

        elif char in ('!', '=', '<', '>'):
            self.add_token(token(), None)

        elif char in ('/', '\n', '"'):
            token()

        elif token != 'ignore':
            self.add_token(token, None)

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, type_, literal) -> None:
        text = self.source[self.start: self.current]

        self.tokens.append(Token(type_, text, literal, self.line))

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False

        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True
    
    def check_div(self) -> int:
        if self.match('/'):
            
            while self.peek() != '\n' and not self.is_at_end():
                self.advance()

        else:
            self.add_token(TokenType.SLASH, '/')

    def peek(self) -> str:
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[current + 1]

    def new_line(self) -> str:
        self.line += 1

    def string(self) -> str:
        while self.peek() != '"' and not self.is_at_end():

            if self.peek() == '\n':
                self.line += 1
            
            self.advance()

        if self.is_at_end():
            raise Error(f'Unterminated string at line {self.line}.')

        self.advance()

        value = self.source[self.start + 1: self.current - 1]

        self.add_token(TokenType.STRING, value)

    def number(self) -> None:
        while self.peek().isdigit():
            self.advance()

        if self.peek() == '.' and self.peek_next().isdigit():
            self.advance()

            while self.peek().isdigit():
                self.advance()

        self.add_token(
            TokenType.NUMBER, float(
                self.source[self.start: self.current]
            )
        )

    def identifier(self) -> None:
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()

        text = self.source[self.start: self.current]
        type_ = self.KEYWORDS.get(text)

        if type_ is None:
            type_ = TokenType.IDENTIFIER

        self.add_token(type_, None)
