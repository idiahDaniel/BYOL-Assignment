# Nova Language Specification

Language name: Nova

File extension: .myext

Overview
--------
Nova is a tiny, beginner-friendly scripting language for demonstrating lexical analysis, parsing, and evaluation. It supports variable declarations, arithmetic, strings, and printing.

Lexical elements
----------------
- Keywords: `let`, `print`
- Identifiers: letter followed by letters or digits, e.g. `x`, `name1`
- Integers: sequences of digits, e.g. `123`
- Strings: double-quoted sequences, supporting escaped quotes `\"`
- Operators: `+`, `-`, `*`, `/`, `=`
- Parentheses: `(`, `)`
- Comments: `//` until end of line

Examples
--------

1) Basic assignment and print

```
let name = "Daniel"
let age = 20

print name
print age + 5
```

2) Arithmetic

```
let x = 10
let y = 5

print x + y
print x * y
```

3) Expressions and precedence

```
let a = 2
let b = 3
print a + b * 4  // prints 14
print (a + b) * 4  // prints 20
```

EBNF Grammar
------------

program         = { statement } ;

statement       = assignment | print_statement ;

assignment      = "let" , identifier , "=" , expression ;

print_statement = "print" , expression ;

expression      = term , { ("+" | "-") , term } ;

term            = factor , { ("*" | "/") , factor } ;

factor          = integer | string | identifier | "(" , expression , ")" ;

identifier      = letter , { letter | digit } ;

integer         = digit , { digit } ;

string          = '"' , { character } , '"' ;

Notes
-----
- Operator precedence: `*` and `/` bind tighter than `+` and `-`.
- Comments begin with `//` and continue to end of line.


Student submission: IDIAH DANIEL DAVID (UG/22/5806)
