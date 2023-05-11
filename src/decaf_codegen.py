# decaf_codegen.py
# Daniel Kogan
# 05.09.2023

from debug import *
  
def generate_program(ast_program):
  """
  :param ast_program: the program AST node
  :return: the assembly code for the program 
  """
  output = ""
  return output
  
def generate_label(label):
  """
  :param label: the label
  :return: the assembly code for the label
  """
  output = f"\n{label}:\n"
  return output
  
def generate_commented_label(label,comment):
  """
  :param label: the label
  :param comment: the comment
  :return: the assembly code for the label
  """
  output = f"\n# {comment}\n{label}:\n"
  return output  
  
def generate_comment(comment):
  """
  :param comment: the comment
  :return: the assembly code for the comment
  """
  output = f"# {comment}\n"
  return output  
  
def generate_method(method, method_id, data: dict()):
  """
  :param ast_method: the function AST node
  :param data: the data dictionary (all data accessible by the function)
  :return: the assembly code for the function
  """
  output = f"\n# method {method_id}\n"
  method_name = method_id
  output += generate_label(f"M_{method_name}_")
  # output += generate_label(f"{data['class_name']}_{method_name}")
  return output  

def generate_field(ast_field, field_size, data: dict(), registers: list()):
  """
  :param ast_field: the field AST node
  :param field_size: the type of the field
  :param data: the data dictionary (all data accessible by the field)
  :param registers: the available registers for the field
  :return: output, registers, data
  """
  output = f"\n# field {ast_field['field_id']}: {ast_field['name']} - {ast_field['line_num']}:{ast_field['col_num']}\n"
  # get available register
  register = registers.pop(0)
  # send field to heap, save heap location in data
  output += f"move_immed_i {register}, " + str(field_size) + "\n"
  # use sap for base address
  output += f"halloc sap, {register}\n"
  # save heap location in data
  data[f"FIELD_{ast_field['field_id']}"] = register
  return output, registers, data
  
  
def generate_block(ast_block):
  """
  :param ast_block: the block AST node
  :return: the assembly code for the block
  """
  output = ""
  return output
  
def generate_statement(ast_statement):
  """
  :param ast_statement: the statement AST node
  :return: the assembly code for the statement
  """
  output = ""
  return output

def generate_expression(ast_expression, registers: list()):
  """
  :param ast_expression: the expression AST node
  :return: the assembly code for the expression
  """
  output = ""
  return output, registers.pop(0)
  
def generate_get_field_value(register, registers: list()):
  """ 
  :param register: the register to get the field value from
  :return: the assembly code for getting the field value
  """
  new_reg = registers.pop(0)
  output = f"hload {new_reg}, sap, {register}\n"
  return output, new_reg

def generate_method_call(method_label):
  """
  :param ast_method_call: the method call AST node
  :param data: the data dictionary (all data accessible by the method call)
  :return: the assembly code for the method call
  """
  output = f"call {method_label}\n"
  return output



def generate_literal(value, registers: list(), is_float=False):
  """
  :param value: the literal value
  :param registers: the available registers for the literal
  :return: the assembly code for the literal
  """
  reg = registers.pop(0)
  output = ""
  if is_float:
    output = f"move_immed_f {reg}, {value}\n"
  else: output = f"move_immed_i {reg}, {value}\n"
  return output, reg



def generate_binary_expression(ast_binary, Lnum, data, register_left, register_right, registers: list(), _type="int"):
  
  int_operator_to_string = {
    "+": "iadd",
    "-": "isub",
    "*": "imul",
    "/": "idiv",
    "%": "imod",
    "&&": "and",
    "||": "or",
    "==": "eq",
    "!=": "neq",
    "<": "ilt",
    ">": "igt",
    "<=": "ileq",
    ">=": "igeq"
  }
  
  float_operator_to_string = {
    "+": "fadd",
    "-": "fsub",
    "*": "fmul",
    "/": "fdiv",
    "%": "fmod",
    "&&": "and",
    "||": "or",
    "==": "eq",
    "!=": "neq",
    "<": "flt",
    ">": "fgt",
    "<=": "fleq",
    ">=": "fgeq"
  }
  
  if _type == "float":
    return generate_binary_expression_type(ast_binary, Lnum, data, register_left, register_right, registers, float_operator_to_string)
  else:
    return generate_binary_expression_type(ast_binary, Lnum, data, register_left, register_right, registers, int_operator_to_string)



# binary expression
def generate_binary_expression_type(ast_binary, Lnum, data, register_left, register_right, registers: list(), operator_to_string):
  """  
  :param ast_binary: the binary expression AST node
  :param registers: the available registers for the binary expression
  :return: the assembly code for the binary expression
  
  Generates assembly code for a binary expression between two integers
  """
  # convert binary expression to assembly
  if "binary_expression" not in ast_binary:
    # raise Exception("Could not find binary expression")
    error(f"ERROR: Could not find binary expression")

  binary_expression = ast_binary["binary_expression"]
  output = f"\n# binary expression {binary_expression['line_num']}:{binary_expression['col_num']}\n"
  if "left" not in binary_expression:
      # raise Exception("Could not find left operand")
      error(f"Line{binary_expression['line_num']}:{binary_expression['col_num']}: Could not find left operand")
  if "right" not in binary_expression:
      # raise Exception("Could not find right operand")
      error(f"Line{binary_expression['line_num']}:{binary_expression['col_num']}: Could not find right operand")
  if "operator" not in binary_expression:
      # raise Exception("Could not find operator")
      error(f"Line{binary_expression['line_num']}:{binary_expression['col_num']}: Could not find operator")
  # left_expression = self.create_expression_record(binary_expression["left"], scope, scope_array)
  # right_expression = self.create_expression_record(binary_expression["right"], scope, scope_array)
  operator = binary_expression["operator"]

  if operator not in operator_to_string:
    # raise Exception("Invalid operator")
    error(f"Line{operator['line_num']}:{operator['col_num']}: Invalid operator")

  operator = operator_to_string[operator]
  # rl_out, register_left = generate_expression(left_expression, registers)
  # rr_out, register_right = generate_expression(right_expression, registers)
  register_out = registers.pop(0)
  
  if operator == "eq":
    output+= "# eq workaround\n"
    output += f"beq {register_left}, {register_right}, L_{Lnum}_TRUE\n"
    output += f"move_immed_i {register_out}, 0\n"
    output += f"jmp L_{Lnum}_END\n"
    output += f"L_{Lnum}_TRUE:\n"
    output += f"move_immed_i {register_out}, 1\n"
    output += f"L_{Lnum}_END:\n"  
  elif operator == "neq":
    output+= "# neq workaround\n"
    output += f"beq {register_left}, {register_right}, L_{Lnum}_TRUE\n"
    output += f"move_immed_i {register_out}, 1\n"
    output += f"jmp L_{Lnum}_END\n"
    output += f"L_{Lnum}_TRUE:\n"
    output += f"move_immed_i {register_out}, 0\n"
    output += f"L_{Lnum}_END:\n"
  
  # output += rl_out + rr_out
  output += operator + " " + register_out + "," + register_left + "," + register_right + "\n" 
  
  # declare which register was used  
  return output, registers, register_out

def generate_bit_flip(register, registers: list(), Lnum):
  reg = registers.pop(0)
  output+= "# bit flip\n"
  output += f"move_immed_i {reg}, 1\n"
  output += f"beq {reg}, {register}, L_{Lnum}_TRUE\n"
  output += f"move_immed_i {register}, 1\n"
  output += f"jmp L_{Lnum}_END\n"
  output += f"L_{Lnum}_TRUE:\n"
  output += f"move_immed_i {register}, 0\n"
  output += f"L_{Lnum}_END:\n"
  return output


def generate_auto(ast_auto, register, _type, registers: list()):
  """ 
  :param ast_auto: the auto AST node
  :param register: the register to store the auto in
  :param registers: the available registers for the auto
  :return: the assembly code for the auto
  """
  output = f"\n# auto expression {ast_auto['line_num']}:{ast_auto['col_num']}\n"
  if "auto" not in ast_auto:
    # raise Exception("Could not find auto")
    error(f"Line{ast_auto['line_num']}:{ast_auto['col_num']}: Could not find auto")
  auto = ast_auto["auto"]

  # Generate move_immediate expression
  
  # Get available register
  available_reg = registers.pop(0)
  # Generate move_immediate expression
  output += "move_immediate_i " + available_reg + ","
  if "postfix" in auto:
    value = auto['postfix']      
  elif "prefix" in auto:
    value = auto['prefix']
  else:
    # raise Exception("Could not find prefix or postfix")
    error(f"Line{auto['line_num']}:{auto['col_num']}: Could not find prefix or postfix")
  
  if "inc" in value:
    output += "1\n"
  elif "dec" in value:
    output += "-1\n"
  else:
    # raise Exception("Invalid postfix or prefix")
    error(f"Line{auto['line_num']}:{auto['col_num']}: Invalid postfix or prefix")

  if _type == "float":
    output += "ftoi " + available_reg + "," + available_reg + "\n"
    output += "fadd " + register + "," + register + "," + available_reg + "\n"
  else:
    output += "iadd " + register + "," + register + "," + available_reg + "\n"
  return output, register

def generate_if_header(ast_if, register, count):
  """ 
  :param: ast_if: the if AST node
  :param: data: the data dictionary
  :param: register: the register to store the if in
  :return: the assembly code for the if header
  
  Generates assembly code for the if header
  Caller is required to have interpreted the if condition before calling this function, and 
  the result of the if condition should be stored in the register passed in
  """
  output = f"\n# if expression {ast_if['line_num']}:{ast_if['col_num']}\n"
  output += f"bnz {register}, else_{count}\n"
  return output

def generate_else_header(ast_if, count):
  """ 
  :param: ast_if: the if AST node
  :param: register: the register to store the if in
  :return: the assembly code for the else header
  
  Generates assembly code for the else header
  if header must be called before this function
  """
  output = f"\n# else expression {ast_if['line_num']}:{ast_if['col_num']}\n"
  output += f"jmp endif_{count}\n"
  output += f"else_{count}:\n"
  return output

def generate_while_header(ast_while, count):
  """ 
  :param ast_while: the while AST node
  :param count: the
  """
  output = f"\n# while expression {ast_while['line_num']}:{ast_while['col_num']}\n"
  output += f"while_{count}:\n"
  return output

def generate_while_condition(register, count):
  """ 
  :param ast_while: the while AST node
  :param count: the
  """
  output = ""
  output += f"bz {register}, endwhile_{count}\n"
  return output

def generate_while_footer(count):
  """ 
  :param ast_while: the while AST node
  :param count: the
  """
  output = ""
  output += f"jmp while_{count}\n"
  output += f"endwhile_{count}:\n"
  return output

def generate_for_header(ast_for, count):
  """
  :param ast_for_header: the for header AST node
  :param count: the count
  :return: the assembly code for the for header
  
  this should be called after initializing the for loop and before the condition
  """
  output = f"\n# for expression {ast_for['line_num']}:{ast_for['col_num']}\n"
  output += f"for_{count}:\n"
  # output += f"beq {register}, for_{count}\n"
  return output


def generate_for_condition(ast_for, count, register1):
  """
  :param ast_for_header: the for header AST node
  :param count: the count
  :param register1: the register to evaluate the condition in
  :param register2: the register with a changing value
  :return: the assembly code for the for header
  
  this should be called after initializing the for loop and before the condition
  """
  return f"bz {register1}, endfor_{count}\n"

def generate_for_footer(count):
  return generate_label(f"endfor_{count}")

def generate_if_footer(count):
  return generate_label(f"endif_{count}")

def generate_move(reg1,reg2):
  """ 
  :param: reg1: the register to
  :param: reg2: the register to
  :return: the assembly code for the move statement
  """
  output = ""
  output += f"move {reg1}, {reg2}\n"
  return output

def generate_jump(label):
  """ 
  :param: label: the label to jump
  :return: the assembly code for the jump statement
  """
  output = ""
  output += f"jmp {label}\n"
  return output

def generate_return(register):
  """ 
  :param: register: the register to return
  :return: the assembly code for the return statement
  """
  output = f"\n# return expression\n"
  output += f"move a0, {register}\n"
  output += "ret\n"
  return output

def generate_hstore(register, field_register):
  """ 
  :param register: the register with the value
  :param field_register: the register with the field address
  :return: the assembly code for the hstore statement
  """
  output = ""
  output += f"hstore sap, {field_register}, {register}\n"
  return output

def generate_initializer(important_registers: list(), constructor_id, registers: list(), size):
  output = generate_comment(f"create new object of with constructor: C_{constructor_id}\n")
  size_reg = registers.pop(0)
  output += f"move_immediate_i {size_reg}, {size}\n"
  output += f"halloc sap, {size_reg}\n"
  for reg in important_registers:
    output += f"save {reg}\n"
  output += f"save {size_reg}\n"
  output += f"call C_{constructor_id}\n"
  for reg in important_registers:
    output += f"restore {reg}\n"
  output += f"restore {size_reg}\n"
  return output
  
def generate_negative(register, registers: list()):
  """
  :param register: the register to negate
  :return: the assembly code for the negation
  """
  output = ""
  temp = registers.pop(0)
  output += f"move_immediate_i {temp}, -1\n"
  output += f"imul {register}, {register}, {temp}\n"
  output += f"# free {temp}\n"
  return output
  

def get_vreg(var_id, asm_data):
  # warn(asm_data)
  if var_id in asm_data:
    return asm_data[var_id]
  else:
    return "None"
  