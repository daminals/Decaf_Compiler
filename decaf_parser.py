# decaf_parser.py
# Daniel Kogan 114439349
# Jason Zhang 112710259
# 02.21.2023
import ply.yacc as yacc
# Get the token map from the lexer.  This is required.
from decaf_lexer import tokens
# precedence for the expressions
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'EQUAL', 'NOTEQUAL'),
    ('nonassoc', 'GREATER', 'LESS', 'GREATEREQ', 'LESSEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('nonassoc', 'LPAREN', 'RPAREN'),
    ('right', 'NOT'),
)
# arithmetic expression and comparsion
# not sure if we gotta check both left hand right hand side check it type for some of these, but prob do as comparsion return boolean instead of numbers
# need define boolean keyword for this work currently 
def p_binary_operators(p):
    '''expression : expression PLUS term
                  | expression MINUS term
                  | expression TIMES factor
                  | expression DIVIDE factor
                  | expression GREATER expression
                  | expression LESS expression
                  | expression GREATEREQ expression
                  | expression LESSEQ expression
                  | expression EQUAL expression
                  | expression NOTEQUAL expression
                  | expression AND expression
                  | expression OR expression
                  | LPAREN expression RPAREN'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
    elif p[2] == '>':
        p[0] = p.lexer.token(p[1] > p[3] and 'true' or 'false')
    elif p[2] == '<':
        p[0] = p.lexer.token(p[1] < p[3] and 'true' or 'false')
    elif p[2] == '>=':
        p[0] = p.lexer.token(p[1] >= p[3] and 'true' or 'false')
    elif p[2] == '<=':
        p[0] = p.lexer.token(p[1] <= p[3] and 'true' or 'false')
    elif p[2] == '==':
        p[0] = p.lexer.token(p[1] == p[3] and 'true' or 'false')
    elif p[2] == '!=':
        p[0] = p.lexer.token(p[1] != p[3] and 'true' or 'false')
    elif p[2] == '&&':
        p[0] = p.lexer.token(p[1] and p[3] and 'true' or 'false')
    elif p[2] == '||':
        p[0] = p.lexer.token(p[1] or p[3] and 'true' or 'false')


def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]
#Literal
def p_factor_num(p):
    'factor : NUMBER'
    p[0] = p[1]
def p_factor_bool(p):
    'factor : BOOLEAN'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

while True:
   try:
       s = input('calc > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)
