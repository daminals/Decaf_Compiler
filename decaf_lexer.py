# decaf_parser.py
# Daniel Kogan 114439349
# Jason Zhang 112710259
# 02.21.2023

import ply.lex as lex

# List of token names.   This is always required
tokens = (
   'NUMBER',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
    'LCURLY',
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

)

# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LCURLY  = r'\{'
t_RCURLY  = r'\}'
t_EQUAL = r'\=\='
t_NOTEQUAL = r'\!\='
t_GREATER = r'\>'
t_LESS = r'\<'
t_GREATEREQ = r'\>\='
t_LESSEQ = r'\<\='
t_OR = r'\|\|'
t_AND = r'\&\&'
t_NOT = r'\!'

# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
data = ''' 3
 + 4 * 10
  + -20 *2
'''

lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)
