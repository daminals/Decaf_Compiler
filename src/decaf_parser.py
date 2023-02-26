# decaf_parser.py
# Daniel Kogan 114439349
# Jason Zhang 112710259
# 02.21.2023
import ply.yacc as yacc
# Get the token map from the lexer.  This is required.
from decaf_lexer import tokens
# precedence for the expressions

precedence = (
    ('right', 'SETEQUAL'),
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
                  | expression OR expression'''

    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
    elif p[2] == '>':
        p[0] = p[1] > p[3]
    elif p[2] == '<':
        p[0] = p[1] < p[3]
    elif p[2] == '>=':
        p[0] = p[1] >= p[3]
    elif p[2] == '<=':
        p[0] = p[1] <= p[3]
    elif p[2] == '==':
        p[0] = p[1] == p[3]
    elif p[2] == '!=':
        p[0] = p[1] != p[3]
    elif p[2] == '&&':
        p[0] = p[1] and p[3] 
    elif p[2] == '||':
        p[0] = p[1] or p[3]
#dosent work?
def p_assignment(p):
    '''assignment : ID SETEQUAL factor
                  | ID SETEQUAL expression
                  | ID SETEQUAL ID
                  | ID SETEQUAL assignment'''
    print(p)
    if p[2] == '=':
        p[0] = ('=', p[1], p[3])
    else:
        p[0] = ('=', p[1], p[3])
 #working       
def p_expression_not(p):
    'expression : NOT expression'
    p[0] = not p[2]
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
    'factor : BOOL'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]


#general rule (for loop apperently the expression seperated by ; is optional need add rule for each)
def p_stmt(p):
    '''
        block : LCURLY statement RCURLY
        statement : LPAREN expression RPAREN statement
                 | IF LPAREN expression RPAREN statement ELSE statement
                 | WHILE LPAREN expression RPAREN statement
                 | FOR LPAREN expression SEMICOLON expression SEMICOLON expression RPAREN statement
                 | RETURN expression SEMICOLON
                 | RETURN SEMICOLON
                 | expression SEMICOLON
                 | BREAK SEMICOLON
                 | CONTINUE SEMICOLON
                 | block'''
    
    

# Build the parser
parser = yacc.yacc()

while True:
   try:
       s = input('> ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)
