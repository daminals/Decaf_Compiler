# decaf_parser.py
# Daniel Kogan 114439349
# Jason Zhang 112710259
# 02.21.2023

import ply.lex as lex
TERMINAL_RED_PRINT = '\033[91m'
TERMINAL_CLEAR_PRINT = '\033[0m'

# List of reserved keywords for functions
reserved = {
   'boolean' : 'BOOLEAN',
   'break' : 'BREAK',
   'extends' : 'EXTENDS',
   'false' : 'FALSE',
   'new' : 'NEW',
   'null' : 'NULL',
   'super' : 'SUPER',
   'this' : 'THIS',
   'continue' : 'CONTINUE',
   'class' : 'CLASS',
   'float' : 'FLOAT',
   'for' : 'FOR',
   'private' : 'PRIVATE',
   'public' : 'PUBLIC',
   'true' : 'TRUE',
   'void' : 'VOID',
   'while' : 'WHILE',
   'do' : 'DO',
   'else' : 'ELSE',
   'if' : 'IF',
   'int' : 'INT',
   'return' : 'RETURN',
   'static' : 'STATIC'
}

# List of token names.   This is always required
tokens = [
   'NUMBER',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
    'LCURLY',
    'RBRACKET',
    'LBRACKET',
   'RCURLY',
    'EQUAL',
    'NOTEQUAL',
    'GREATER',
    'LESS',
    'GREATEREQ',
    'LESSEQ',
    'OR',
    'AND',
    'NOT',
    'BOOL',
    'SETEQUAL',
    'SEMICOLON',
    'ERROR', # error type, no rule associated with type except throw err
    'ID'
] + list(reserved.values())

# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LCURLY  = r'\{'
t_RCURLY  = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_EQUAL = r'\=\='
t_NOTEQUAL = r'\!\='
t_GREATER = r'\>'
t_LESS = r'\<'
t_GREATEREQ = r'\>\='
t_LESSEQ = r'\<\='
t_OR = r'\|\|'
t_AND = r'\&\&'
t_NOT = r'\!'
t_SETEQUAL = r'\='
t_SEMICOLON = r'\;'
t_IF = r'if'
t_ELSE = r'else'
t_WHILE = r'while'
t_DO = r'do'
t_FOR = r'for'
t_RETURN = r'return'
t_BOOLEAN = r'boolean'
t_BREAK = r'break'
t_EXTENDS = r'extends'
t_NEW = r'new'
t_NULL = r'null'
t_SUPER = r'super'
t_THIS = r'this'
t_CONTINUE = r'continue'
t_CLASS = r'class'
t_FLOAT = r'float'
t_PRIVATE = r'private'
t_PUBLIC = r'public'
t_VOID = r'void'
t_INT = r'int'


# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_BOOL(t):
    r'(true|false)'
    t.value = True if t.value == 'true' else False
    return t

# def t_if(t):
#     r'if'
#     return t

# def t_for(t):
#     r'for'
#     return t

# def t_else(t):
#     r'else'
#     return t

# def t_while(t):
#     r'while'
#     return t

# def t_do(t):
#     r'do'
#     return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Compute column.
# input is the input text string
# token is a token instance
def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

# EOF handling rule
'''def t_eof(t):
    # Get more input (Example)
    more = input('... ')
    if more:
        self.lexer.input(more)
        return self.lexer.token()
    return None '''


# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# rules for reserved words
# needs to be last in the file since regex is greedy
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in reserved:             # Check for reserved words
      t.type = reserved.get(t.value,'ID')    # Check for reserved words
    elif t.value not in tokens:
        print(f"{TERMINAL_RED_PRINT}Invalid token: {t.value}{TERMINAL_CLEAR_PRINT}")
        t.type = 'ERROR'
    return t

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
