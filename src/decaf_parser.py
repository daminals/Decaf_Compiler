# decaf_lexer.py
# Daniel Kogan dkogan 114439349
# 02.21.2023

import ply.yacc as yacc
import sys
from decaf_lexer import tokens
from decaf_ast import extract_body, extract_variables_from_formals, extract_variables_from_field, extract_var_type, set_var_count
from debug import debug, warn

# x = [0]

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


def flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def p_start(p):
    '''start : class_decl
             | class_decl start
             | empty'''
    if len(p) == 2:
      p[0] = [p[1]]
    else:
      p[0] = flatten([p[1],p[2]])

def p_class(p):
    '''class_decl : CLASS ID LCURLY class_body RCURLY
                  | CLASS ID EXTENDS ID LCURLY class_body RCURLY'''
    if p[3] == '{':
        p[0] = extract_body({'class_name': p[2], 'superclass': "", 'body': p[4], "line_num": p.lineno(2), "col_num": find_col2(p)})
    else:
        p[0] = extract_body({'class_name': p[2], "superclass": p[4], "body": p[6], "line_num": p.lineno(2), "col_num": find_col2(p)})
    # warn(f"{p.lineno()},  {str(p[0].ast)}\n")

    
def p_class_body(p):
    '''class_body : field_decl
                  | method_decl
                  | constructor_decl
                  | class_body field_decl
                  | class_body constructor_decl
                  | class_body method_decl'''
    if len(p) == 2:
      p[0] = [p[1]]
    else:
      p[0] = flatten([p[1], p[2]])
    # warn(f"{p.lineno()},  {str(p[0])}\n")

    
def p_field_decl(p):
    '''field_decl : var_decl
                  | modifier var_decl'''
    if len(p) > 2:
      p[0] = extract_variables_from_field({'field': {'modifiers': p[1], "variables": p[2], "var_type": "field", "line_num": p.lexer.lineno, "col_num": find_col2(p) }})
    else:
      p[0] = extract_variables_from_field({'field': {'modifiers': [], "variables": p[1], "var_type": "field", "line_num": p.lexer.lineno, "col_num": find_col2(p) }})

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
    p[0] = {"type": p[1], "ids": p[2], "line_num": p.lexer.lineno, "col_num": find_col2(p)}

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
      p[0] = flatten([p[1], p[3]])
    else:
      p[0] = [p[1]]

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
      p[0] = extract_variables_from_formals("method",{'method': {'modifiers': [], "type": p[1],  "function_id":p[2], "formals":[], "body": p[5], "line_num": p.lineno(2), "col_num": find_col2(p)}})
    elif len(p) == 7:
      if p[3] == '(':
        p[0] = extract_variables_from_formals("method",{'method': {'modifiers': [], "type": p[1], "function_id":p[2], "formals": p[4], "body": p[6], "line_num": p.lineno(2), "col_num": find_col2(p)}})
      else:
        p[0] = extract_variables_from_formals("method",{'method': {'modifiers': p[1], "type": p[2], "function_id":p[3], "formals": [], "body": p[6], "line_num": p.lineno(3), "col_num": find_col2(p)}})
    elif len(p) == 8:
      p[0] = extract_variables_from_formals("method",{'method': {'modifiers': p[1], "type": p[2], "function_id":p[3], "formals": p[5], "body": p[7], "line_num": p.lineno(3), "col_num": find_col2(p)}})
    # reset var count after method is complete
    set_var_count(1)
    # debug(f"{p.lineno()},  {str(p[0])}\n")

def p_constructor(p):
    '''constructor_decl : modifier ID LPAREN RPAREN block 
                        | modifier ID LPAREN formals RPAREN block
                        | ID LPAREN RPAREN block 
                        | ID LPAREN formals RPAREN block'''
    if len(p) == 7:
      p[0] = extract_variables_from_formals("constructor",{'constructor': {'modifiers': p[1], "constructor_id": p[2], "formals": p[4], "body": p[6], "line_num": p.lineno(2), "col_num": find_col2(p)}})
    elif len(p) == 5:
      p[0] = extract_variables_from_formals("constructor",{'constructor': {'modifiers': [], "constructor_id": p[1], "formals": [], "body": p[4], "line_num": p.lineno(2), "col_num": find_col2(p)}})
    else:
      if p[2] == '(':
        p[0] = extract_variables_from_formals("constructor",{'constructor': {'modifiers': [], "constructor_id": p[1], "formals": p[3], "body": p[5], "line_num": p.lexer.lineno, "col_num": find_col2(p)}})
      else:
        p[0] = extract_variables_from_formals("constructor",{'constructor': {'modifiers': p[1], "constructor_id": p[2], "formals": [], "body": p[5], "line_num": p.lexer.lineno, "col_num": find_col2(p)}})
    set_var_count(1)

def p_formals(p):
    '''formals : formal_param
               | formal_param COMMA formals '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = flatten([p[1], p[3]])

def p_formals_param(p):
    '''formal_param : type variable'''
    p[0] = {'parameter': {"type": p[1], "id": p[2], "line_num": p.lineno(2), "col_num": find_col2(p)}}

def p_block(p):
    '''block : LCURLY stmtlist RCURLY
             | empty'''
    if len(p) > 2:
      p[0] = p[2]
    else:
      p[0] = None
    # debug("block")
    # debug(f"{p.lineno()},  {str(p[0])}\n")

def p_stmtlist(p):
    '''stmtlist : stmt
                | stmtlist stmt'''
    if len(p) == 2:
      p[0] = [p[1]]
    else:
      p[0] = flatten([p[1], p[2]])
    # debug(f"{p.lineno()},  {str(p[0])}")

def p_stmt(p):
    '''stmt : if_stmt
            | while_stmt
            | for_loop
            | return_stmt
            | stmt_expression SEMICOLON
            | BREAK SEMICOLON
            | CONTINUE SEMICOLON
            | block
            | declare_local_var
            | SEMICOLON'''
    p[0] = p[1]
    # debug(f"{p.lineno()},  {str(p[0])}")

def p_declare_local_var(p):
  '''declare_local_var : var_decl'''
  p[0] = {'var_decl': extract_var_type(p[1]),"line_num": p.lexer.lineno, "col_num": find_col2(p)}


def p_return_stmt(p):
    '''return_stmt : RETURN expression SEMICOLON
                   | RETURN SEMICOLON'''
    if len(p) == 4:
      p[0] = {'return': p[2]}
    else:
      p[0] = {'return': {"expression": None, "line_num": p.lineno(2), "col_num": find_col2(p)}}

def p_if_stmt(p):
    '''if_stmt : IF LPAREN expression RPAREN block
               | IF LPAREN expression RPAREN single_stmt
               | IF LPAREN expression RPAREN block ELSE block
               | IF LPAREN expression RPAREN single_stmt ELSE block
               | IF LPAREN expression RPAREN block ELSE single_stmt
               | IF LPAREN expression RPAREN single_stmt ELSE single_stmt'''
    if len(p) == 6:
      p[0] = {'if': {'condition': p[3], 'if_block': p[5], 'else_block': [], "line_num": p.lexer.lineno, "col_num": find_col2(p)}}
    else:
      p[0] = {'if': {'condition': p[3], 'if_block': p[5], 'else_block': p[7], "line_num": p.lexer.lineno, "col_num": find_col2(p)}}

def p_single_stmt(p):
    '''single_stmt : if_stmt
                   | while_stmt
                   | for_loop
                   | return_stmt
                   | stmt_expression SEMICOLON
                   | BREAK SEMICOLON
                   | CONTINUE SEMICOLON
                   | declare_local_var
                   | SEMICOLON'''
    if p[1] != ";": 
      p[0] = [p[1]]
    else:
      p[0] = []

def p_while_stmt(p):
    '''while_stmt : WHILE LPAREN expression RPAREN block
                  | WHILE LPAREN expression RPAREN single_stmt'''
    p[0] = {'while': {'condition': p[3], 'while_block': p[5], "line_num": p.lexer.lineno, "col_num": find_col2(p)}}

def p_for_missing_start(p):
  '''for_missing_start : FOR LPAREN SEMICOLON expression SEMICOLON stmt_expression RPAREN block
                       | FOR LPAREN SEMICOLON expression SEMICOLON stmt_expression RPAREN single_stmt'''
  p[0] = {'for': {'init': None, 'condition': p[4], 'update': p[6], 'for_block': p[8], "line_num": p.lexer.lineno, "col_num": find_col2(p)}}

def p_for_missing_end(p):
  '''for_missing_end : FOR LPAREN stmt_expression SEMICOLON expression SEMICOLON RPAREN single_stmt
                     | FOR LPAREN stmt_expression SEMICOLON expression SEMICOLON RPAREN block'''
  p[0] =  {'for': {'init': p[3], 'condition': p[5], 'update': None, 'for_block': p[8], "line_num": p.lexer.lineno, "col_num": find_col2(p)}}

def p_for_missing_middle(p):
  '''for_missing_middle : FOR LPAREN stmt_expression SEMICOLON SEMICOLON stmt_expression RPAREN single_stmt
                        | FOR LPAREN stmt_expression SEMICOLON SEMICOLON stmt_expression RPAREN block'''
  p[0] =  {'for': {'init': p[3], 'condition': None, 'update': p[6], 'for_block': p[8], "line_num": p.lexer.lineno, "col_num": find_col2(p)}}


def p_for_loop(p):
  '''for_loop : FOR LPAREN stmt_expression SEMICOLON expression SEMICOLON stmt_expression RPAREN single_stmt
              | FOR LPAREN stmt_expression SEMICOLON expression SEMICOLON stmt_expression RPAREN block
              | for_missing_middle
              | for_missing_end
              | for_missing_start
              | FOR LPAREN stmt_expression SEMICOLON SEMICOLON RPAREN block              
              | FOR LPAREN stmt_expression SEMICOLON SEMICOLON RPAREN single_stmt
              | FOR LPAREN SEMICOLON SEMICOLON stmt_expression RPAREN block              
              | FOR LPAREN SEMICOLON SEMICOLON stmt_expression RPAREN single_stmt
              | FOR LPAREN SEMICOLON expression SEMICOLON RPAREN block              
              | FOR LPAREN SEMICOLON expression SEMICOLON RPAREN single_stmt
              | FOR LPAREN SEMICOLON SEMICOLON RPAREN block
              | FOR LPAREN SEMICOLON SEMICOLON RPAREN single_stmt'''   
  if len(p) == 10:
    p[0] = {'for': {'init': p[3], 'condition': p[5], 'update': p[7], 'for_block': p[9], "line_num": p.lexer.lineno, "col_num": find_col2(p)}}
  elif len(p) == 8:
    p[0] = {'for': {'init': None, 'condition': None, 'update': None, 'for_block': p[7], "line_num": p.lexer.lineno, "col_num": find_col2(p)}}
  elif len(p) == 2:
    p[0] = p[1]
  else:
    init = p[3] if p[3] != ';' else None
    update = p[4] if p[4] != ';' else None
    p[0] = {'for': {'init': init, 'condition': condition, 'update': update, 'for_block': p[6], "line_num": p.lexer.lineno, "col_num": find_col2(p)}}


def p_literal(p):
    '''literal : int_literal
               | float_literal
               | string_literal
               | null_literal
               | boolean_literal'''
    p[0] = {"literal": p[1]}

def p_int_literal(p):
    '''int_literal : INTEGER'''
    p[0] = {"type": "Integer", "value": p[1], "line_num": p.lexer.lineno, "col_num": find_col2(p)}

def p_float_literal(p):
    '''float_literal : FLOAT'''
    p[0] = {"type": "Float", "value": p[1], "line_num": p.lexer.lineno, "col_num": find_col2(p)}

def p_boolean_literal(p):
    '''boolean_literal : TRUE
                       | FALSE'''
    value = True if p[1] == 'true' else False
    p[0] = {"type": "Boolean", "value": value, "line_num": p.lexer.lineno, "col_num": find_col2(p)}

def p_string_literal(p):
    '''string_literal : STRING_LITERAL'''
    p[0] = {"type": "String", "value": p[1], "line_num": p.lexer.lineno, "col_num": find_col2(p)}

def p_null_literal(p):
    '''null_literal : NULL'''
    p[0] = {"type": "Null", "value": None, "line_num": p.lexer.lineno, "col_num": find_col2(p)}
    
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
    elif len(p) == 4:
      p[0] = p[2]
    elif len(p) == 5:
      p[0] = {"new": {"type": p[2], "arguments": [], "line_num": p.lexer.lineno, "col_num": find_col2(p)}}
    else:
      p[0] = {"new": {"type": p[2], "arguments": p[4], "line_num": p.lexer.lineno, "col_num": find_col2(p)}}
    

def p_arg(p):
    '''arguments : expression
                 | expression COMMA arguments'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
      p[0] = flatten([p[1], p[3]])


def p_lhs(p):
    '''lhs : field_access'''
    # debug(f"{p.lineno()},  {str(p[1])}")
    p[0] = {'field_access': p[1], "line_num": p.lexer.lineno, "col_num": find_col2(p)}

def p_field(p):
    '''field_access : primary DOT ID
                    | ID'''
    if len(p) == 2:
      p[0] =  {'primary': "", 'id': p[1],"line_num": p.lexer.lineno, "col_num": find_col2(p)}
    else:
      p[0] =  {'primary': p[1], 'id': p[3],"line_num": p.lexer.lineno, "col_num": find_col2(p)}

def p_method_invo(p):
    '''method_invocation : field_access LPAREN arguments RPAREN
                         | field_access LPAREN RPAREN'''
    if len(p) == 5:
      p[0] = {'method_invocation': {'field_access': p[1], 'arguments': p[3], "line_num": p.lexer.lineno, "col_num": find_col2(p)}}
    else:
      p[0] = {'method_invocation': {'field_access': p[1], 'arguments': [], "line_num": p.lexer.lineno, "col_num": find_col2(p)}}

def p_expr(p):
    '''expression : primary
                  | auto_expression
                  | assign
                  | binary_expression
                  | unary_expression'''
    p[0] = {"expression": p[1], "line_num": p.lexer.lineno, "col_num": find_col2(p)}

# def p_binary_expression(p):
#     '''binary_expression : expression bool_op expression
#                          | expression arith_op expression'''
#     p[0] = {"binary_expression": {"left": p[1], "operator": p[2], "right": p[3], "line_num": p.lineno(2), "col_num": find_col2(p)}}

def p_binary_expression(p):
  '''binary_expression : expression OR expression
                       | expression AND expression
                       | expression NOTEQUAL expression
                       | expression EQUAL expression
                       | expression LESS expression
                       | expression GREATEREQ expression
                       | expression LESSEQ expression
                       | expression GREATER expression
                       | expression PLUS expression
                       | expression MINUS expression
                       | expression TIMES expression
                       | expression DIVIDE expression'''
  p[0] = {"binary_expression": {"left": p[1], "operator": p[2], "right": p[3], "line_num": p.lineno(2), "col_num": find_col2(p)}}

def p_unary_expression(p):
    '''unary_expression : unary_op expression'''
    p[0] = {"unary_expression": {"operator": p[1], "operand": p[2], "line_num": p.lexer.lineno, "col_num": find_col2(p)}}

def p_auto_expression(p):
  '''auto_expression : lhs PLUSPLUS
                     | lhs MINUSMINUS
                     | PLUSPLUS lhs
                     | MINUSMINUS lhs'''
  if p[1] == '++':
    p[0] = {"auto": {'prefix': 'inc', "operand": p[2]},"line_num": p.lexer.lineno, "col_num": find_col2(p)}
  elif p[1] == '--':
    p[0] ={"auto": {'prefix': 'dec', 'operand': p[2]},"line_num": p.lexer.lineno, "col_num": find_col2(p)}
  elif p[2] == '++':
    p[0] = {"auto": {'postfix': 'inc', 'operand': p[1]},"line_num": p.lexer.lineno, "col_num": find_col2(p)}
  # elif p[2] == '--':
  else:
    p[0] = {"auto": {'postfix': 'dec', 'operand': p[1]},"line_num": p.lexer.lineno, "col_num": find_col2(p)}


def p_assign(p):
    '''assign : lhs SETEQUAL expression '''
    p[0] = {'set_equal': {'assign': {'assignee': p[1], 'assigned_value': p[3]}, "line_num": p.lineno(2), "col_num": find_col2(p)}}

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
                       | auto_expression
                       | method_invocation'''
    p[0] = {"expression": p[1], "line_num": p.lexer.lineno, "col_num": find_col2(p)}
    # debug(f"{p.lineno()},  {str(p[0])}")


def p_empty(p):
    'empty :'
    pass

RED = '\033[91m'
CLEAR_FORMAT = '\033[0m'

def p_error(p):
    if p:
        print(f"{RED}ERROR:{CLEAR_FORMAT} Syntax error at line {p.lineno}, column {find_column(p)}, token: {p.value}'", file=sys.stderr)
    else:
        print(f"{RED}ERROR:{CLEAR_FORMAT} Syntax error: unexpected end of input",file=sys.stderr)
    raise SyntaxError();     

def find_column(token):
    input_str = token.lexer.lexdata
    last = input_str.rfind('\n', 0, token.lexpos)
    column = (token.lexpos - last)
    return column

def find_col2(token):
    input_str = token.lexer.lexdata
    last = input_str.rfind('\n', 0, token.lexer.lexpos)
    column = (token.lexer.lexpos - last)
    return column
