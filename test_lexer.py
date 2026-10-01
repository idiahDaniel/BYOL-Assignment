from lexer import Lexer, TokenType


def tokens_for(src):
    lex = Lexer(src)
    toks = []
    while True:
        t = lex.next_token()
        toks.append((t.type, t.literal))
        if t.type == TokenType.EOF:
            break
    return toks


def test_basic():
    src = 'let x = 10\nprint x + 5\n'
    toks = tokens_for(src)
    expected = [
        (TokenType.LET, 'let'),
        (TokenType.IDENT, 'x'),
        (TokenType.EQUAL, '='),
        (TokenType.INTEGER, '10'),
        (TokenType.PRINT, 'print'),
        (TokenType.IDENT, 'x'),
        (TokenType.PLUS, '+'),
        (TokenType.INTEGER, '5'),
        (TokenType.EOF, ''),
    ]
    assert toks == expected


def test_string_and_comment():
    src = 'let name = "Daniel"\n// this is a comment\nprint name\n'
    toks = tokens_for(src)
    expected = [
        (TokenType.LET, 'let'),
        (TokenType.IDENT, 'name'),
        (TokenType.EQUAL, '='),
        (TokenType.STRING, 'Daniel'),
        (TokenType.PRINT, 'print'),
        (TokenType.IDENT, 'name'),
        (TokenType.EOF, ''),
    ]
    assert toks == expected


if __name__ == '__main__':
    test_basic()
    test_string_and_comment()
    print('All lexer tests passed')
