"""Parser for Nova language.

Parses a stream of tokens into an Abstract Syntax Tree (AST).
"""

from dataclasses import dataclass
from typing import List, Optional, Union
from lexer import Token, TokenType, Lexer


# AST Node classes
@dataclass
class Program:
    statements: List['Statement']


@dataclass
class Statement:
    pass


@dataclass
class Assignment(Statement):
    name: str
    value: 'Expression'


@dataclass
class PrintStatement(Statement):
    expr: 'Expression'


@dataclass
class Expression:
    pass


@dataclass
class BinaryOp(Expression):
    left: 'Expression'
    op: str
    right: 'Expression'


@dataclass
class IntegerLiteral(Expression):
    value: int


@dataclass
class StringLiteral(Expression):
    value: str


@dataclass
class Identifier(Expression):
    name: str


@dataclass
class GroupedExpression(Expression):
    expr: 'Expression'


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def current_token(self) -> Optional[Token]:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def peek_token(self) -> Optional[Token]:
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return None

    def advance(self):
        self.pos += 1

    def expect(self, token_type: TokenType) -> Token:
        tok = self.current_token()
        if tok is None or tok.type != token_type:
            raise SyntaxError(f"Expected {token_type}, got {tok}")
        self.advance()
        return tok

    def parse(self) -> Program:
        statements = []
        while self.current_token() is not None and self.current_token().type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return Program(statements)

    def parse_statement(self) -> Optional[Statement]:
        tok = self.current_token()
        if tok is None:
            return None
        
        if tok.type == TokenType.LET:
            return self.parse_assignment()
        elif tok.type == TokenType.PRINT:
            return self.parse_print()
        else:
            raise SyntaxError(f"Unexpected token: {tok}")

    def parse_assignment(self) -> Assignment:
        self.expect(TokenType.LET)
        name_tok = self.expect(TokenType.IDENT)
        self.expect(TokenType.EQUAL)
        expr = self.parse_expression()
        return Assignment(name_tok.literal, expr)

    def parse_print(self) -> PrintStatement:
        self.expect(TokenType.PRINT)
        expr = self.parse_expression()
        return PrintStatement(expr)

    def parse_expression(self) -> Expression:
        return self.parse_additive()

    def parse_additive(self) -> Expression:
        left = self.parse_multiplicative()
        while self.current_token() and self.current_token().type in (TokenType.PLUS, TokenType.MINUS):
            op_tok = self.current_token()
            self.advance()
            right = self.parse_multiplicative()
            left = BinaryOp(left, op_tok.literal, right)
        return left

    def parse_multiplicative(self) -> Expression:
        left = self.parse_primary()
        while self.current_token() and self.current_token().type in (TokenType.STAR, TokenType.SLASH):
            op_tok = self.current_token()
            self.advance()
            right = self.parse_primary()
            left = BinaryOp(left, op_tok.literal, right)
        return left

    def parse_primary(self) -> Expression:
        tok = self.current_token()
        if tok is None:
            raise SyntaxError("Unexpected end of input")

        if tok.type == TokenType.INTEGER:
            self.advance()
            return IntegerLiteral(int(tok.literal))
        elif tok.type == TokenType.STRING:
            self.advance()
            return StringLiteral(tok.literal)
        elif tok.type == TokenType.IDENT:
            self.advance()
            return Identifier(tok.literal)
        elif tok.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return GroupedExpression(expr)
        else:
            raise SyntaxError(f"Unexpected token: {tok}")


def parse(tokens: List[Token]) -> Program:
    """Parse a list of tokens into an AST."""
    parser = Parser(tokens)
    return parser.parse()

