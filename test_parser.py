"""Tests for the Nova parser."""

from lexer import Lexer, TokenType
from parser import parse, Assignment, PrintStatement, BinaryOp, IntegerLiteral, StringLiteral, Identifier


def test_simple_assignment():
    """Test parsing a simple assignment."""
    src = "let x = 10"
    lexer = Lexer(src)
    tokens = []
    while True:
        t = lexer.next_token()
        tokens.append(t)
        if t.type == TokenType.EOF:
            break
    
    ast = parse(tokens)
    assert len(ast.statements) == 1
    stmt = ast.statements[0]
    assert isinstance(stmt, Assignment)
    assert stmt.name == "x"
    assert isinstance(stmt.value, IntegerLiteral)
    assert stmt.value.value == 10


def test_print_statement():
    """Test parsing a print statement."""
    src = "print x"
    lexer = Lexer(src)
    tokens = []
    while True:
        t = lexer.next_token()
        tokens.append(t)
        if t.type == TokenType.EOF:
            break
    
    ast = parse(tokens)
    assert len(ast.statements) == 1
    stmt = ast.statements[0]
    assert isinstance(stmt, PrintStatement)
    assert isinstance(stmt.expr, Identifier)
    assert stmt.expr.name == "x"


def test_arithmetic_expression():
    """Test parsing arithmetic expressions with correct precedence."""
    src = "let result = 2 + 3 * 4"
    lexer = Lexer(src)
    tokens = []
    while True:
        t = lexer.next_token()
        tokens.append(t)
        if t.type == TokenType.EOF:
            break
    
    ast = parse(tokens)
    stmt = ast.statements[0]
    assert isinstance(stmt, Assignment)
    
    # Should parse as 2 + (3 * 4)
    expr = stmt.value
    assert isinstance(expr, BinaryOp)
    assert expr.op == "+"
    assert isinstance(expr.left, IntegerLiteral)
    assert expr.left.value == 2
    assert isinstance(expr.right, BinaryOp)
    assert expr.right.op == "*"


def test_parenthesized_expression():
    """Test parsing grouped expressions."""
    src = "let result = (2 + 3) * 4"
    lexer = Lexer(src)
    tokens = []
    while True:
        t = lexer.next_token()
        tokens.append(t)
        if t.type == TokenType.EOF:
            break
    
    ast = parse(tokens)
    stmt = ast.statements[0]
    expr = stmt.value
    assert isinstance(expr, BinaryOp)
    assert expr.op == "*"


def test_string_literal():
    """Test parsing string literals."""
    src = 'let name = "Alice"'
    lexer = Lexer(src)
    tokens = []
    while True:
        t = lexer.next_token()
        tokens.append(t)
        if t.type == TokenType.EOF:
            break
    
    ast = parse(tokens)
    stmt = ast.statements[0]
    assert isinstance(stmt, Assignment)
    assert isinstance(stmt.value, StringLiteral)
    assert stmt.value.value == "Alice"


def test_multiple_statements():
    """Test parsing multiple statements."""
    src = """let x = 10
let y = 20
print x + y"""
    lexer = Lexer(src)
    tokens = []
    while True:
        t = lexer.next_token()
        tokens.append(t)
        if t.type == TokenType.EOF:
            break
    
    ast = parse(tokens)
    assert len(ast.statements) == 3
    assert isinstance(ast.statements[0], Assignment)
    assert isinstance(ast.statements[1], Assignment)
    assert isinstance(ast.statements[2], PrintStatement)


if __name__ == '__main__':
    test_simple_assignment()
    test_print_statement()
    test_arithmetic_expression()
    test_parenthesized_expression()
    test_string_literal()
    test_multiple_statements()
    print('All parser tests passed')

