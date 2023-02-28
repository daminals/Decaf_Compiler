# decaf_lexer.py
# Daniel Kogan 114439349
# Jason Zhang 112710259
# 02.21.2023
import ply.yacc as yacc
import sys
from decaf_lexer import tokens
precedence = (
    ('right', 'SETEQUAL'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'NOTEQUAL', 'EQUAL'),
    ('nonassoc', 'LESS', 'GREATEREQ', 'LESSEQ', 'GREATER'),
    ('left', 'PLUS', 'MINUS'),  
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'NOT'),
)
def p_start(p):
    '''start : class_decl
             | class_decl start
             | empty'''

def p_class(p):
    '''class_decl : CLASS ID LCURLY class_body RCURLY
                  | CLASS ID EXTENDS ID LCURLY class_body RCURLY'''
    
def p_class_body(p):
    '''class_body : field_decl
                  | method_decl
                  | constructor_decl
                  | class_body field_decl
                  | class_body constructor_decl
                  | class_body method_decl'''
    
def p_field_decl(p):
    '''field_decl : var_decl
                  | modifier var_decl'''

def p_modifier(p):
    '''modifier : PUBLIC
                | PRIVATE
                | STATIC
                | PUBLIC STATIC
                | PRIVATE STATIC
                | empty'''
    p[0] = p[1] if p[1] is not None else ''


def p_var_decl(p):
    '''var_decl : type variables SEMICOLON'''
#put new types here
def p_type(p):
    '''type : INT
            | FLOAT
            | BOOLEAN
            | STRING
            | ID'''

def p_variables(p):
    '''variables : variable
                 | variable COMMA variables'''

def p_variable(p):
    '''variable : ID'''

def p_method_decl(p):
    '''method_decl : modifier type ID LPAREN RPAREN block
                   | modifier type ID LPAREN formals RPAREN block
                   | modifier VOID ID LPAREN RPAREN block
                   | modifier VOID ID LPAREN formals RPAREN block
                   | type ID LPAREN RPAREN block
                   | type ID LPAREN formals RPAREN block
                   | VOID ID LPAREN RPAREN block
                   | VOID ID LPAREN formals RPAREN block'''

def p_constructor(p):
    '''constructor_decl : modifier ID LPAREN RPAREN block 
                        | modifier ID LPAREN formals RPAREN block
                        | ID LPAREN RPAREN block 
                        | ID LPAREN formals RPAREN block'''

def p_formals(p):
    '''formals : formal_param
               | formal_param COMMA formals '''

def p_formals_param(p):
    '''formal_param : type variable'''

def p_block(p):
    '''block : LCURLY stmtlist RCURLY
             | empty'''

def p_stmtlist(p):
    '''stmtlist : stmt
                | stmtlist stmt'''

def p_stmt(p):
    '''stmt : IF LPAREN expression RPAREN stmt
            | IF LPAREN expression RPAREN stmt ELSE stmt
            | WHILE LPAREN expression RPAREN stmt
            | FOR LPAREN stmt_expression SEMICOLON expression SEMICOLON stmt_expression RPAREN stmt
            | FOR LPAREN stmt_expression SEMICOLON expression SEMICOLON RPAREN stmt
            | FOR LPAREN stmt_expression SEMICOLON SEMICOLON stmt_expression RPAREN stmt
            | FOR LPAREN SEMICOLON expression SEMICOLON stmt_expression RPAREN stmt
            | FOR LPAREN stmt_expression SEMICOLON SEMICOLON RPAREN stmt
            | FOR LPAREN SEMICOLON SEMICOLON stmt_expression RPAREN stmt
            | FOR LPAREN SEMICOLON expression SEMICOLON RPAREN stmt
            | FOR LPAREN SEMICOLON SEMICOLON RPAREN stmt
            | RETURN expression SEMICOLON
            | RETURN SEMICOLON
            | stmt_expression SEMICOLON
            | BREAK SEMICOLON
            | CONTINUE SEMICOLON
            | block
            | var_decl
            | SEMICOLON'''
    
def p_literal(p):
    '''literal : INTEGER
               | FLOAT
               | STRING_LITERAL
               | NULL
               | FALSE
               | TRUE'''
    
def p_primary(p):
    '''primary : literal
               | THIS
               | SUPER
               | LPAREN expression RPAREN
               | NEW ID LPAREN RPAREN
               | NEW ID LPAREN arguments RPAREN
               | method_invocation
               | lhs'''

def p_arg(p):
    '''arguments : expression
                 | expression COMMA arguments'''

def p_lhs(p):
    '''lhs : field_access'''

def p_field(p):
    '''field_access : primary DOT ID
                    | ID'''

def p_method_invo(p):
    '''method_invocation : field_access LPAREN arguments RPAREN
                         | field_access LPAREN RPAREN'''

def p_expr(p):
    '''expression : primary
                  | assign
                  | expression arith_op expression
                  | expression bool_op expression
                  | unary_op expression'''
def p_lhs(p):
    '''lhs : field_access'''

def p_field(p):
    '''field_access : primary DOT ID
                    | ID'''
def p_assign(p):
    '''assign : lhs SETEQUAL expression
              | lhs PLUSPLUS
              | lhs MINUSMINUS
              | PLUSPLUS lhs
              | MINUSMINUS lhs'''

def p_arith_op(p):
    '''arith_op : PLUS
                | MINUS
                | TIMES 
                | DIVIDE'''

def p_bool_op(p):
    '''bool_op : GREATER
               | LESS
               | GREATEREQ
               | LESSEQ
               | EQUAL
               | NOTEQUAL
               | AND
               | OR'''

def p_unary_op(p):
    '''unary_op : PLUS
                | MINUS
                | NOT'''

def p_stmt_expr(p):
    '''stmt_expression : assign
                       | method_invocation'''

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print("Syntax error at line %d, column %d, token: %s'" % (p.lineno, find_column(p), p.value))
    else:
        print("Syntax error: unexpected end of input")
    raise SyntaxError();     

def find_column(token):
    input_str = token.lexer.lexdata
    last = input_str.rfind('\n', 0, token.lexpos)
    print(last)
    column = (token.lexpos - last)
    return column
