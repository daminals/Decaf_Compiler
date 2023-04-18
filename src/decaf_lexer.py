# decaf_lexer.py
# Daniel Kogan dkogan 114439349
# 02.21.2023

import ply.lex as lex
TERMINAL_RED_PRINT = '\033[91m'
TERMINAL_CLEAR_PRINT = '\033[0m'

# List of reserved keywords for functions
reserved = {
    'boolean': 'BOOLEAN',
    'break': 'BREAK',
    'extends': 'EXTENDS',
    'new': 'NEW',
    'null': 'NULL',
    'super': 'SUPER',
    'this': 'THIS',
    'continue': 'CONTINUE',
    'class': 'CLASS',
    'float': 'FLOAT',
    'for': 'FOR',
    'private': 'PRIVATE',
    'public': 'PUBLIC',
    'void': 'VOID',
    'while': 'WHILE',
    'do': 'DO',
    'else': 'ELSE',
    'if': 'IF',
    'int': 'INT',
    'return': 'RETURN',
    'static': 'STATIC',
    'string': 'STRING'
}

# List of token names.   This is always required
tokens = [
    'DOT',
    'COMMA',
    'INTEGER',
    'PLUS',
    'PLUSPLUS',
    'MINUS',
    'MINUSMINUS',
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
    'TRUE',
    'FALSE',  
    'SETEQUAL',
    'SEMICOLON',
    'STRING_LITERAL',
    'ERROR',  # error type, no rule associated with type except throw err
    'ID'
] + list(reserved.values())

# Regular expression rules for simple tokens\
t_COMMA = r'\,'
t_DOT = r'\.'
t_AND = r'\&\&'
t_BOOLEAN = r'boolean'
t_BREAK = r'break'
t_CLASS = r'class'
t_CONTINUE = r'continue'
t_DIVIDE = r'/'
t_DO = r'do'
t_ELSE = r'else'
t_EQUAL = r'\=\='
t_EXTENDS = r'extends'
t_FOR = r'for'
t_GREATER = r'\>'
t_GREATEREQ = r'\>\='
t_IF = r'if'
t_INT = r'int'
t_LBRACKET = r'\['
t_LCURLY = r'\{'
t_LESS = r'\<'
t_LESSEQ = r'\<\='
t_LPAREN = r'\('
t_MINUSMINUS = r'\-\-'
t_MINUS = r'-'
t_NEW = r'new'
t_NOT = r'\!'
t_NOTEQUAL = r'\!\='
t_NULL = r'null'
t_OR = r'\|\|'
t_PLUSPLUS = r'\+\+'
t_PLUS = r'\+'
t_PRIVATE = r'private'
t_PUBLIC = r'public'
t_RBRACKET = r'\]'
t_RCURLY = r'\}'
t_RETURN = r'return'
t_RPAREN = r'\)'
t_SEMICOLON = r'\;'
t_SETEQUAL = r'\='
t_STATIC = r'static'
t_STRING= r'string'
t_SUPER = r'super'
t_THIS = r'this'
t_TIMES = r'\*'
t_VOID = r'void'
t_WHILE = r'while'

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# A regular expression rule with some action code
def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Regular expression rule for string literals
def t_STRING_LITERAL(t):
    r'"[^"]*"'
    t.value = t.value[1:-1] # remove the quotes from the value
    return t

def t_TRUE(t):
    r'true'
    t.value = True
    return t

def t_FALSE(t):
    r'false'
    t.value = False
    return t


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


# rules for reserved words
# needs to be last in the file since regex is greedy
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in reserved:
        t.type = reserved[t.value]  # set the token type to the reserved word's type
    else:
        t.type = 'ID'  # set the token type to 'ID' if it's a valid ID
    return t

# Error handling rule

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    t.lexer.lexpos += len(t.value)    

# comments
def t_COMMENT(t):
    r'(/\*(.|\n)*?\*/)|(//.*)'
    t.lexer.lineno += t.value.count('\n')
    
