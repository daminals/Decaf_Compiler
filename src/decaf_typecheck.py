# decaf_typecheck.py
# Daniel Kogan
# 04.26.2023

from debug import *

valid_types = ["int", "boolean", "string", "float", "double", "char", "void", "error", "null"]

# is type1 subtype of type2
def is_subtype(scope, type1, type2):
  type1 = make_little_type(type1)
  type2 = make_little_type(type2)
  # debug(f"checking if {type1} is subtype of {type2}")
  if type1 == type2:
    return True
  elif type1.lower() == 'null' and  'user(' in type2:
    return True
  elif type1 == 'int' and type2 == 'float':
    return True
  elif 'user(' in type1 or 'user(' in type2:
    return is_subclass(scope, type1, type2)
  elif 'class-literal(' in type1 or 'class-literal(' in type2:
    return is_subclass(scope, type1, type2)
  else:
    return False

# is class1 subclass of class2
def is_subclass(scope, class1,class2):
  if class1 == class2:
    return True
  elif class1 == 'null' and  'user(' in class2:
    return True
  elif 'user(' in class1 and 'user(' in class2:
    # remove user from class1 and class2
    class1_name = class1[5:-1]
    class2_name = class2[5:-1]
    # while class1 has superclass and class1 is not class2
    if class1_name in scope["global"]:
      while scope["global"][class1_name]["superclass_name"] != "" and class1_name != class2_name:
        class1 = scope["global"][class1]["superclass_name"]
        if class1 == class2:
          return True
  elif 'class-literal(' in class1 and 'class-literal(' in class2:
    # remove class from class1 and class2
    class1_name = class1[6:-1]
    class2_name = class2[6:-1]
    # while class1 has superclass and class1 is not class2
    if class1_name in scope["global"]:
      while scope["global"][class1_name]["superclass_name"] != "" and class1_name != class2_name:
        class1 = scope["global"][class1]["superclass_name"]
        if class1 == class2:
          return True
  else:
    return False

def resolve_boolean_operator(operator):
  bool_opp = [
    "true",
    "false",
    "==",
    "!=",
    "&&",
    "||",
    "!",
    "<",
    "<=",
    ">",
    ">="
  ]
  if operator in bool_opp:
    return True
  return False
  
def resolve_boolean_expression(expression): 
  if "expression" not in expression:
    return False
  expression = expression["expression"]
  if "binary_expression" not in expression:
    return False
  if "operator" not in expression["binary_expression"]:
    return False
  operator = expression["binary_expression"]["operator"]
  return resolve_boolean_operator(operator)

def resolve_arithmetic_operator(operator):
  arithmetic_opp = [
    "+",
    "-",
    "*",
    "/",
    "%",
    "&",
    "|"
  ]
  if operator in arithmetic_opp:
    return True
  return False

def resolve_arithmetic_expression(expression):
  if "expression" not in expression:
    return False
  expression = expression["expression"]
  if "binary_expression" not in expression:
    return False
  if "operator" not in expression["binary_expression"]:
    return False
  operator = expression["binary_expression"]["operator"]
  return resolve_arithmetic_operator(operator)

def is_number_type(var_type, scope):
  # what if vartype is subtype of number type
  if var_type == "int": var_type = "Integer"
  if var_type == "float": var_type = "Float"
  return (is_subtype(scope, var_type, "Float") or is_subtype(scope, var_type, "Integer"))

def is_boolean_type(var_type, scope):
  # what if vartype is subtype of number type
  return is_subtype(scope, var_type, "boolean")

def make_little_type(type_name):
  if type_name == "Integer": return "int"
  if type_name == "Float": return "float"
  if type_name == "String": return "string"
  if type_name == "Boolean": return "boolean"
  return type_name

def resolve_expression_type(expression):
  if "expression" not in expression:
    return "error"
  if resolve_arithmetic_expression(expression):
    return "int"
  elif resolve_boolean_expression(expression):
    return "boolean"
  elif "literal" in expression["expression"]:
    return expression["expression"]["literal"]["type"]
  elif "field_access" in expression["expression"]:
    return "*handle_field_access*"
  else:
    return "error"

def create_type_signature(name, args, return_type="void", id=None):
  signature = {}
  signature["name"] = name
  signature["id"] = id
  signature["return_type"] = return_type
  signature["args"] = args
  return signature

def match_signature(sig1, sig2):
  if len(sig1["args"]) != len(sig2["args"]):
    return False
  if sig1["name"] != sig2["name"]:
    return False
  for i in range(len(sig1["args"])):
    if sig1["args"][i] != sig2["args"][i]:
      return False
  return True