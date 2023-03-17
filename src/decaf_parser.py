# decaf_lexer.py
# Daniel Kogan dkogan 114439349
# Jason Zhang jasozhang 112710259
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
    '''start : start_statement
             | empty'''
    p[0] = p[1]

def p_start_statement(p):
  '''start_statement : class_decl
                     | class_decl start_statement'''
  if len(p) == 2:
      p[0] = p[1]
  else:
      if isinstance(p[1], list):
          p[0] = p[1] + [p[2]]  # flatten the list
      else:
          p[0] = [p[1], p[2]]


def p_class(p):
    '''class_decl : CLASS ID LCURLY class_body RCURLY
                  | CLASS ID EXTENDS ID LCURLY class_body RCURLY'''
    if p[3] == '{':
        p[0] = {'class_name': p[2], 'superclass': None, 'body': p[4]}
    else:
        p[0] = {'class_name': p[2], "superclass": p[4], "body": p[6]}
    
def p_class_body(p):
    '''class_body : field_decl
                  | method_decl
                  | constructor_decl
                  | class_body field_decl
                  | class_body constructor_decl
                  | class_body method_decl'''
    if len(p) == 2:
      p[0] = p[1]
    else:
        if isinstance(p[1], list):
            p[0] = p[1] + [p[2]]  # flatten the list
        else:
            p[0] = [p[1], p[2]]

    
def p_field_decl(p):
    '''field_decl : var_decl
                  | modifier var_decl'''
    if len(p) > 2:
      p[0] = {'field': {'modifiers': p[1], "variables": p[2] }}
    else:
      p[0] = {'field': {'modifiers': [], "variables": p[1] }}

def p_modifier(p):
    '''modifier : PUBLIC
                | PRIVATE
                | STATIC
                | PUBLIC STATIC
                | PRIVATE STATIC
                | empty'''
    if len(p) > 2:
      p[0] = [p[1], p[2]]
    else:
      p[0] = [p[1]]

def p_var_decl(p):
    '''var_decl : type variables SEMICOLON'''
    p[0] = {"type": p[1], "ids": p[2]}

#put new types here
def p_type(p):
    '''type : INT
            | FLOAT
            | BOOLEAN
            | STRING
            | ID'''
    p[0] = p[1]

def p_variables(p):
    '''variables : variable
                 | variables COMMA variable'''
    if len(p) > 2:
      p[0] = (p[1], p[3])
    else:
      p[0] = (p[1])

def p_variable(p):
    '''variable : ID'''
    p[0] = p[1]

def p_method_decl(p):
    '''method_decl : modifier type ID LPAREN RPAREN block
                   | modifier type ID LPAREN formals RPAREN block
                   | modifier VOID ID LPAREN RPAREN block
                   | modifier VOID ID LPAREN formals RPAREN block
                   | type ID LPAREN RPAREN block
                   | type ID LPAREN formals RPAREN block
                   | VOID ID LPAREN RPAREN block
                   | VOID ID LPAREN formals RPAREN block'''
    if len(p) == 6:
      p[0] = {'method': {'modifiers': [], "type": p[1],  "function_id":p[2], "formals": None, "function_body": p[5]}}
    elif len(p) == 7:
      if p[3] == '(':
        p[0] = {'method': {'modifiers': [], "type": p[1], "function_id":p[2], "formals": p[4], "function_body": p[6]}}
      else:
        p[0] = {'method': {'modifiers': p[1], "type": p[2], "function_id":p[3], "formals": None, "function_body": p[6]}}
    elif len(p) == 8:
      p[0] = {'method': {'modifiers': p[1], "type": p[2], "function_id":p[3], "formals": p[5], "function_body": p[7]}}

def p_constructor(p):
    '''constructor_decl : modifier ID LPAREN RPAREN block 
                        | modifier ID LPAREN formals RPAREN block
                        | ID LPAREN RPAREN block 
                        | ID LPAREN formals RPAREN block'''
    if len(p) == 7:
      p[0] = {'constructor', {'modifiers': p[1], "constructor_id": p[2], "formals": p[4], "constructor_body": p[6]}}
    elif len(p) == 5:
      p[0] = {'constructor', {'modifiers': [], "constructor_id": p[1], "formals": None, "constructor_body": p[4]}}
    else:
      if p[2] == '(':
        p[0] = {'constructor', {'modifiers': [], "constructor_id": p[1], "formals": p[3], "constructor_body": p[5]}}
      else:
        p[0] = {'constructor', {'modifiers': p[1], "constructor_id": p[2], "formals": None, "constructor_body": p[5]}}

def p_formals(p):
    '''formals : formal_param
               | formal_param COMMA formals '''
    if len(p) > 2:
      p[0] = (p[1], p[3])
    else:
      p[0] = (p[1])

def p_formals_param(p):
    '''formal_param : type variable'''
    p[0] = {'parameter': {"type": p[1], "id": p[2]}}

def p_block(p):
    '''block : LCURLY stmtlist RCURLY
             | empty'''
    if len(p) > 2:
      p[0] = p[2]
    else:
      p[0] = None

def p_stmtlist(p):
    '''stmtlist : stmt
                | stmtlist stmt'''
    if len(p) == 2:
      p[0] = p[1]
    else:
      if isinstance(p[1], list):
          p[0] = p[1] + [p[2]]  # flatten the list
      else:
          p[0] = [p[1], p[2]]


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
    p[0] = p[1]
    
def p_primary(p):
    '''primary : literal
               | THIS
               | SUPER
               | LPAREN expression RPAREN
               | NEW ID LPAREN RPAREN
               | NEW ID LPAREN arguments RPAREN
               | method_invocation
               | lhs'''
    if len(p) == 2:
      p[0] = p[1]
    elif len(p) == 3:
      p[0] = p[2]
    elif len(p) == 4:
      p[0] = {"new": {"type": p[2], "arguments": None}}
    else:
      p[0] = {"new": {"type": p[2], "arguments": p[4]}}
    

def p_arg(p):
    '''arguments : expression
                 | expression COMMA arguments'''
    if len(p) == 2:
        p[0] = p[1]
    else:
      if isinstance(p[1], list):
          p[0] = p[1] + [p[2]]  # flatten the list
      else:
          p[0] = [p[1], p[2]]


def p_lhs(p):
    '''lhs : field_access'''
    p[0] = {'lhs': {'field_access': p[1]}}

def p_field(p):
    '''field_access : primary DOT ID
                    | ID'''
    if len(p) == 2:
      p[0] =  {'id': p[1], 'primary': None}
    else:
      p[0] =  {'primary': p[1], 'id': p[3]}

def p_method_invo(p):
    '''method_invocation : field_access LPAREN arguments RPAREN
                         | field_access LPAREN RPAREN'''
    if len(p) == 5:
      p[0] = {'method_invocation': {'field_access': p[1], 'arguments': p[3]}}
    else:
      p[0] = {'method_invocation': {'field_access': p[1], 'arguments': None}}

def p_expr(p):
    '''expression : primary
                  | assign
                  | expression arith_op expression
                  | expression bool_op expression
                  | unary_op expression'''
    if len(p) == 2:
      p[0] = p[1]
    else:
      if isinstance(p[1], list):
          p[0] = p[1] + [p[2]]  # flatten the list
      else:
          p[0] = [p[1], p[2]]


def p_assign(p):
    '''assign : lhs SETEQUAL expression
              | lhs PLUSPLUS
              | lhs MINUSMINUS
              | PLUSPLUS lhs
              | MINUSMINUS lhs'''
    if len(p) == 4:
      p[0] = {'assign': {'lhs': p[1], 'expression': p[3]}}
    else:
      if p[1] == '++':
        p[0] = {'assign': {'lhs': p[2], 'expression': 'prefix++'}}
      elif p[1] == '--':
        p[0] = {'assign': {'lhs': p[2], 'expression': 'prefix--'}}
      elif p[2] == '++':
        p[0] = {'assign': {'lhs': p[1], 'expression': 'postfix++'}}
      elif p[2] == '--':
        p[0] = {'assign': {'lhs': p[1], 'expression': 'postfix--'}}

def p_arith_op(p):
    '''arith_op : PLUS
                | MINUS
                | TIMES 
                | DIVIDE'''
    p[0] = p[1]

def p_bool_op(p):
    '''bool_op : GREATER
               | LESS
               | GREATEREQ
               | LESSEQ
               | EQUAL
               | NOTEQUAL
               | AND
               | OR'''
    p[0] = p[1]

def p_unary_op(p):
    '''unary_op : PLUS
                | MINUS
                | NOT'''
    p[0] = p[1]

def p_stmt_expr(p):
    '''stmt_expression : assign
                       | method_invocation'''
    p[0] = p[1]

def p_empty(p):
    'empty :'
    pass

RED = '\033[91m'
CLEAR_FORMAT = '\033[0m'

def p_error(p):
    if p:
        print(f"{RED}ERROR: Syntax error at line {p.lineno}, column {find_column(p)}, token: {p.value}'{CLEAR_FORMAT}", file=sys.stderr)
    else:
        print(f"{RED}ERROR: Syntax error: unexpected end of input{CLEAR_FORMAT}",file=sys.stderr)
    raise SyntaxError();     

def find_column(token):
    input_str = token.lexer.lexdata
    last = input_str.rfind('\n', 0, token.lexpos)
    column = (token.lexpos - last)
    return column
