"""Lexer implementation for Nova (.myext) language.

Week 1 lexer solution prepared by IDIAH DANIEL DAVID (UG/22/5806). This version keeps the same logic but uses a slightly different coding style.
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
    def __init__(self, data: str):
        self.input = data
        self.position = 0       # current pos in input (points to current char)
        self.cursor_ahead = 0  # current reading position in input (after current char)
        self.ch: Optional[str] = None
        self.step()

    def step(self):
        if self.cursor_ahead >= len(self.input):
            self.ch = None
        else:
            self.ch = self.input[self.cursor_ahead]
        self.position = self.cursor_ahead
        self.cursor_ahead += 1

    def look(self) -> Optional[str]:
        if self.cursor_ahead >= len(self.input):
            return None
        return self.input[self.cursor_ahead]

    def eat_space(self):
        while self.ch is not None and self.ch.isspace():
            self.step()

    def capture_word(self) -> str:
        start = self.position
        while self.ch is not None and (self.ch.isalpha() or self.ch.isdigit() or self.ch == '_'):
            self.step()
        return self.input[start:self.position]

    def capture_number(self) -> str:
        start = self.position
        while self.ch is not None and self.ch.isdigit():
            self.step()
        return self.input[start:self.position]

    def capture_string(self) -> str:
        # consume opening quote
        self.step()
        value_chars: List[str] = []
        while self.ch is not None and self.ch != '"':
            if self.ch == '\\' and self.look() in ('"', '\\'):
                # handle simple escapes: \" and \\
                self.step()
                value_chars.append(self.ch)
                self.step()
                continue
            value_chars.append(self.ch)
            self.step()
        # consume closing quote
        if self.ch == '"':
            self.step()
        return ''.join(value_chars)

    def next_symbol(self) -> Token:
        self.eat_space()

        if self.ch is None:
            return Token(TokenType.EOF, "")

        # comments
        if self.ch == '/' and self.look() == '/':
            # consume both slashes
            self.step()
            self.step()
            while self.ch is not None and self.ch != '\n':
                self.step()
            return self.next_symbol()

        if self.ch.isalpha() or self.ch == '_':
            lit = self.capture_word()
            ttype = KEYWORDS.get(lit, TokenType.IDENT)
            return Token(ttype, lit)

        if self.ch.isdigit():
            lit = self.capture_number()
            return Token(TokenType.INTEGER, lit)

        if self.ch == '"':
            lit = self.capture_string()
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

        self.step()
        return tok


if __name__ == "__main__":
    sample = 'let x = 10\nprint x + 5\n'
    lexer = Lexer(sample)
    toks = []
    while True:
        t = lexer.next_symbol()
        toks.append(t)
        if t.type == TokenType.EOF:
            break
    for t in toks:
        print(t)
