from lexer import Lexer, TokenType


def scan_tokens(src):
    lex = Lexer(src)
    toks = []
    while True:
        t = lex.next_token()
        toks.append((t.type, t.literal))
        if t.type == TokenType.EOF:
            break
    return toks


def check_assignment_case():
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


def check_string_and_comment_case():
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
    print('All lexer tests passed for IDIAH DANIEL DAVID')
    # also show tokens for demonstration
    from lexer import Lexer
    lex = Lexer('let s = "hi"')
    while True:
        t = lex.next_token()
        print((t.type, t.literal))
        if t.type == TokenType.EOF:
            break
from lexer import Lexer, TokenType


def tokenize(src: str):
    l = Lexer(src)
    tokens = []
    while True:
        t = l.next_token()
        tokens.append((t.type, t.literal))
        if t.type == TokenType.EOF:
            break
    return tokens


def main():
    src = 'let x = 10\nprint x + 5\n// comment\nlet s = "hi"\n'
    toks = tokenize(src)
    for t in toks:
        print(t)


if __name__ == '__main__':
    main()
