"""Lexer implementation for Nova (.myext) language.

Provides TokenType, Token and Lexer. The lexer recognizes keywords,
identifiers, integers, strings, operators, parentheses, and comments.
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, List


class TokenType(Enum):
    LET = auto()
    PRINT = auto()
    IDENT = auto()
    INTEGER = auto()
    STRING = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    EQUAL = auto()
    LPAREN = auto()
    RPAREN = auto()
    EOF = auto()
    ILLEGAL = auto()


KEYWORDS = {
    "let": TokenType.LET,
    "print": TokenType.PRINT,
}


@dataclass
class Token:
    type: TokenType
    literal: str

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.literal!r})"


class Lexer:
    def __init__(self, input_text: str):
        self.input = input_text
        self.position = 0       # current pos in input (points to current char)
        self.read_position = 0  # current reading position in input (after current char)
        self.ch: Optional[str] = None
        self._read_char()

    def _read_char(self):
        if self.read_position >= len(self.input):
            self.ch = None
        else:
            self.ch = self.input[self.read_position]
        self.position = self.read_position
        self.read_position += 1

    def _peek_char(self) -> Optional[str]:
        if self.read_position >= len(self.input):
            return None
        return self.input[self.read_position]

    def _skip_whitespace(self):
        while self.ch is not None and self.ch.isspace():
            self._read_char()

    def _read_identifier(self) -> str:
        start = self.position
        while self.ch is not None and (self.ch.isalpha() or self.ch.isdigit() or self.ch == '_'):
            self._read_char()
        return self.input[start:self.position]

    def _read_number(self) -> str:
        start = self.position
        while self.ch is not None and self.ch.isdigit():
            self._read_char()
        return self.input[start:self.position]

    def _read_string(self) -> str:
        # consume opening quote
        self._read_char()
        value_chars: List[str] = []
        while self.ch is not None and self.ch != '"':
            if self.ch == '\\' and self._peek_char() in ('"', '\\'):
                # handle simple escapes: \" and \\
                self._read_char()
                value_chars.append(self.ch)
                self._read_char()
                continue
            value_chars.append(self.ch)
            self._read_char()
        # consume closing quote
        if self.ch == '"':
            self._read_char()
        return ''.join(value_chars)

    def next_token(self) -> Token:
        self._skip_whitespace()

        if self.ch is None:
            return Token(TokenType.EOF, "")

        # comments
        if self.ch == '/' and self._peek_char() == '/':
            # consume both slashes
            self._read_char()
            self._read_char()
            while self.ch is not None and self.ch != '\n':
                self._read_char()
            return self.next_token()

        if self.ch.isalpha() or self.ch == '_':
            lit = self._read_identifier()
            ttype = KEYWORDS.get(lit, TokenType.IDENT)
            return Token(ttype, lit)

        if self.ch.isdigit():
            lit = self._read_number()
            return Token(TokenType.INTEGER, lit)

        if self.ch == '"':
            lit = self._read_string()
            return Token(TokenType.STRING, lit)

        ch = self.ch
        if ch == '+':
            tok = Token(TokenType.PLUS, ch)
        elif ch == '-':
            tok = Token(TokenType.MINUS, ch)
        elif ch == '*':
            tok = Token(TokenType.STAR, ch)
        elif ch == '/':
            tok = Token(TokenType.SLASH, ch)
        elif ch == '=':
            tok = Token(TokenType.EQUAL, ch)
        elif ch == '(':
            tok = Token(TokenType.LPAREN, ch)
        elif ch == ')':
            tok = Token(TokenType.RPAREN, ch)
        else:
            tok = Token(TokenType.ILLEGAL, ch)

        self._read_char()
        return tok


if __name__ == "__main__":
    sample = 'let x = 10\nprint x + 5\n'
    lexer = Lexer(sample)
    toks = []
    while True:
        t = lexer.next_token()
        toks.append(t)
        if t.type == TokenType.EOF:
            break
    for t in toks:
        print(t)

