from .token_type import TokenType


class Token:

    def __init__(
        self, 
        type_: 'TokenType', 
        lexeme: str, 
        literal: str, 
        line: int
    ) -> None:
        
        self.type_ = type_
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def to_string(self) -> str:
        return f'Type: {self.type_} Lexeme: {repr(self.lexeme)} Literal: {self.literal} Line: {self.line}'
