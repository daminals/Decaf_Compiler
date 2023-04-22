# decaf_ast.py
# Daniel Kogan dkogan 114439349
# 04.17.2023

import json
from predefined_classes import in_class, out_class, err_class
field_count = 1
method_count = 6
class_count = 1
var_count = 1
valid_types = ["int", "boolean", "string", "float", "double", "char"]
user_defined_types = []

scope = {"global": {"in": in_class, "out": out_class}}

def debug(string):
  PURPLE = '\033[95mDEBUG: '
  CLEAR_COLOR = '\033[0m\n'
  if isinstance(string, dict):
    print(PURPLE + json.dumps(string, indent=4, default=str) + CLEAR_COLOR)
  else: 
    print(PURPLE + str(string) + CLEAR_COLOR)

def warn(string):
  YELLOW = '\033[93mWARN: '
  CLEAR_COLOR = '\033[0m'
  print(YELLOW + str(string) + CLEAR_COLOR)


class AST:

    def __init__(self, ast, fields, methods, constructors):
        self.ast = ast
        self.fields = fields
        self.methods = methods
        self.constructors = constructors
        # Check class name
        if "class_name" not in ast:
            raise Exception("Could not find class name")
        if ast["class_name"] == "":
            raise Exception("Class name is empty")
        self.class_name = ast["class_name"]

        # Check super class
        if "superclass" not in ast:
            raise Exception("Could not find class name")
        self.superclass_name = ast["superclass"]

        global scope

        self.scope = self.add_to_scope(scope["global"], [], self.class_name, {"type": "class", "children": []})

        self.printed = self.create_record(self.ast, self.scope[self.class_name])
        scope["global"] = self.scope

    def print_ast(self):
        return self.printed

    def create_record(self, ast, scope):
        output = ""
        global user_defined_types
        output += f"Class Name: {self.class_name}\n"
        # class name is now a valid type as it has been declared
        user_defined_types.append(ast["class_name"])

        output += f"Superclass: {self.superclass_name}\n"

        # scope 
        scope_array = ["global", self.class_name]

        # Check fields
        if "fields" not in ast["body"]:
            raise Exception("Could not find fields")
        self.fields = ast["body"]["fields"]
        output += self.create_field_record(scope["children"], scope_array + ["children"])

        # check constructors
        if "constructors" not in ast["body"]:
            raise Exception("Could not find constructors")
        self.constructors = ast["body"]["constructors"]
        output += self.create_constructor_record(scope["children"], scope_array + ["children"])

        # check methods
        if "methods" not in ast["body"]:
            raise Exception("Could not find methods")
        self.methods = ast["body"]["methods"]
        output += self.create_method_record(scope["children"], scope_array + ["children"])
        return output

    def create_field_record(self, scope, scope_array):
        """
        Field Record:
        • Field name: name of this field.
        • Field id: A unique integer id for this field. This id should be unique across the entire program: no two
        fields, irrespective of their containing class, should have the same id.
        • Containing class: the name of the class where this field is defined.
        • Field visibility: which encodes the visibility (public/private) of the field.
        • Field applicability: which describes whether this is a class field (i.e. static) or an instance field (non-
        static).
        • Type: an instance of a type record (described later) that describes the declared type of this field.
        """
        output = "Fields:\n"
        for field_id in self.fields.keys():
            field = self.fields[field_id]
            # debug(field)
            # name
            if "id" not in field:
                raise Exception("Could not find field names (id)")
            field_name = field["id"]
            # type
            if "type" not in field:
                raise Exception("Could not find field type")
            field_type = self.create_type_record(field["type"])
            # modifiers
            if "modifiers" not in field:
                raise Exception("Could not find field modifiers")
            field_modifiers = self.create_modifiers_list(field["modifiers"])

            # add field to scope
            self.add_to_scope(scope, scope_array, field_name, {"type": f"field_{field_type}", "id_num": field_id, "modifiers": field["modifiers"]})
            scope_array.append(field_name)
            # scope = scope[field_name]

            # debug(scope)
            output += f"FIELD {field_id}, {field_name}, {self.class_name}, {field_modifiers}, {field_type}\n"
        return output

    def create_constructor_record(self, scope, scope_array):
        """
        Constructor Record:
        • Constructor id: Note that the name of a constructor in Decaf is identical to its containing class. So, we will identify each constructor by a unique integer id.
          - This id should be unique across the entire program: no two constructors, irrespective of their containing class, should have the same id.
        • Constructor visibility: which encodes the visibility (public/private) of the constructor.
        • Constructor parameters: sequence of formal parameters of the constructor. Each parameter is a variable (use variable record).
        • Variable table: A table of variables containing information on all the formal parameters and local variables of the constructor.
        • Constructor body: is a statement (an instance of a statement record, described later).
        """
        output = "Constructors:\n"
        for constructor_id in self.constructors.keys():
            local_scope = scope.copy()
            local_scope_array = scope_array.copy()
            constructor = self.constructors[constructor_id]

            # modifiers
            if "modifiers" not in constructor:
                raise Exception("Could not find field modifiers")
            constructor_modifiers = self.create_modifiers_list_PRIVATE_PUBLIC(
                constructor["modifiers"])

            output += f"CONSTRUCTOR: {constructor_id}, {constructor_modifiers}\n"
            output += "Constructor Parameters:\n"
            
            local_scope = self.add_to_scope(scope, scope_array, constructor_id, {"type": "constructor", "id_num": constructor_id, "modifiers": constructor["modifiers"] ,"children": []})
            local_scope = self.traverse_scope_layer(local_scope, [constructor_id, "children"])
            local_scope_array.append(constructor_id)
            local_scope_array.append("children")

            block = self.create_block_record(constructor["body"], local_scope, local_scope_array)

            output += "Variable Table:\n"
            for variable_id in constructor["formals"].keys():
                variable = constructor["formals"][variable_id]
                self.add_to_scope(local_scope, local_scope_array, variable["id"], {"type": f"{self.create_type_record(variable['type'])}", "id_num": variable_id, "id": variable["id"], "var_type": "formal" })
                output += self.create_variable_record(variable_id, variable)
            
            output += "Constructor Body:\n"
            output += block
        return output

    def create_method_record(self, scope, scope_array):
        output = "Methods:\n"
        for method_id in self.methods.keys():
            local_scope = scope
            local_scope_array = scope_array.copy()
            method = self.methods[method_id]
            # name
            method_name = method["function_id"]
            # modifiers
            method_modifiers = self.create_modifiers_list(method["modifiers"])
            # type
            method_type = self.create_type_record(method["type"], 1)

            output += f"METHOD: {method_id}, {method_name}, {self.class_name}, {method_modifiers}, {method_type}\n"
            output += "Method Parameters:\n"

            local_scope = self.add_to_scope(local_scope, local_scope_array, method_name, {"type": "method", "id_num": method_id, "modifiers": method["modifiers"], "return_type": method["type"], "children": []})
            local_scope = self.traverse_scope_layer(local_scope, [method_name, "children"])
            local_scope_array.append(method_name)
            local_scope_array.append("children")

            for variable_id in method["formals"].keys():
                variable = method["formals"][variable_id]
                self.add_to_scope(local_scope, local_scope_array, variable["id"], {"type": f"{self.create_type_record(variable['type'])}", "id_num": variable_id, "id": variable["id"], "var_type": "formal" })
                output += self.create_variable_record(variable_id, variable)

            block = self.create_block_record(method["body"], local_scope, local_scope_array)
            
            output += "Variable Table:\n"
            # check scope for variables
            for variable in local_scope:
              for var_id in variable.keys():
                if variable[var_id]["var_type"] == "formal":
                  continue
                output += self.create_variable_record(variable[var_id]["id_num"], variable[var_id])

            output += "Method Body:\n"
            output += block
        return output
      
    def create_block_record(self, ast_block, scope, scope_array):
        output = "Block([\n"
        for statement in ast_block:
            expr =  "Expr("
            stmt = self.create_statement_record(statement, scope, scope_array)
            expr += stmt
            expr += ")\n, "
            if stmt == "":
                expr = ""
            output += expr
        output += "\b\b])\n" # use backspace to remove the last comma
        return output

    def create_type_record(self, ast_type, return_type=0):
        """ 
        Type Record: Contents
          • Type: the name of the type
        """
        output = ""
        global valid_types, user_defined_types

        local_valid_types = valid_types.copy()
        if return_type == 1:
            local_valid_types.append("void")

        if ast_type in user_defined_types:
            output += f"user({ast_type})"
            return output

        if ast_type not in local_valid_types:
            raise Exception("Invalid type")
        output += f"{ast_type}"
        return output

    def create_variable_record(self, variable_id, ast_variable):
        output = ""
        output += f"VARIABLE {variable_id}, {ast_variable['id']}, {ast_variable['var_type']}, {ast_variable['type']}\n"
        return output

    # String of modifiers list, including instance or static
    def create_modifiers_list(self, ast_modifiers):
        output = "private"
        if ast_modifiers == []:
            output = "private, instance"
        elif ast_modifiers == ["public"]:
            output = "public, instance"
        elif ast_modifiers == ["static"]:
            output = "private, static"
        elif ast_modifiers == ["public", "static"]:
            output = "public, static"
        elif ast_modifiers == ["private", "static"]:
            output = "private, static"
        return output

    # String of modifiers list, only including public or private
    def create_modifiers_list_PRIVATE_PUBLIC(self, ast_modifiers):
        output = ""
        if ast_modifiers == []:
            output = "private"
        elif "private" in ast_modifiers:
            output = "private"
        else:
            output = "public"
        return output

    def create_statement_record(self, ast_statement, scope, scope_array):
        output = ""
        if "set_equal" in ast_statement:
          output += self.create_assignment_record(ast_statement, scope_array)
        elif "auto" in ast_statement:
          output += self.evaluate_auto(ast_statement, scope, scope_array)
        elif "var_decl" in ast_statement:
          output += self.create_variable_declaration_record(ast_statement, scope, scope_array)
        elif "return" in ast_statement:
          output += self.evaluate_return(ast_statement, scope, scope_array)
        elif "if" in ast_statement:
          output += self.evaluate_if_block(ast_statement, scope, scope_array)
        elif "while" in ast_statement:
          output += self.evaluate_while_block(ast_statement, scope, scope_array)
        elif "for" in ast_statement:
          output += self.evaluate_for_block(ast_statement, scope, scope_array)
        elif "break" in ast_statement:
          output += "Break"
        elif "continue" in ast_statement:
          output += "Continue"
        else:
          raise Exception("Invalid statement")
        return output

    def create_variable_declaration_record(self, ast_variable_declaration, scope, scope_array):
        output = ""
        if "var_decl" not in ast_variable_declaration:
            raise Exception("Could not find variable declaration")
        variable_declaration = ast_variable_declaration["var_decl"]
        for var in variable_declaration.keys():
            if "id" not in variable_declaration[var]:
                raise Exception("Could not find variable id")
            if "type" not in variable_declaration[var]:
                raise Exception("Could not find variable type")
            
            var_id = variable_declaration[var]["id"]
            var_type = variable_declaration[var]["type"]
            # debug(f"adding {var_id} to scope")
            self.add_to_scope(scope, scope_array, var_id, {"type": f"{self.create_type_record(var_type)}", "id_num": var, "id": var_id, "var_type": "local"})
            output += self.create_variable_record(var, variable_declaration[var])

            # output += f"VariableDeclaration({var_id}, {var_type})\n"
        return ""

    def create_assignment_record(self, ast_assignment, scope_array):
        if "set_equal" not in ast_assignment:
            raise Exception("Could not find assignment")
        output = ""
        assignment = ast_assignment["set_equal"]
        if "assign" not in assignment:
            raise Exception("Could not find assignee")
        
        operand = assignment["assign"]
        var_id_num, var_type = self.get_var_from_scope(operand["assignee"]["field_access"]["id"], scope_array)

        expr_type = "Assign"
        var_scope_type = "Variable"
        if "field_" in var_type:
          var_scope_type = "Field-access"

        assignee = f"({var_id_num})"
        assignee = self.evaluate_primary(operand["assignee"]["field_access"])
        
        assigned_value = ""
        if "assigned_value" not in operand:
          raise Exception("Could not find assigned value")
        
        if "expression" in operand["assigned_value"]:
          assigned_value = self.create_expression_record(operand["assigned_value"], scope, scope_array)
        else:
          raise Exception("Could not find assigned value type")
        
        expression = f"{var_scope_type}({assignee}), {assigned_value} "
        if expr_type != "":
          output += f"{expr_type}({expression})"
        else:
          output += expression

        return output

    def create_expression_record(self, ast_expression, scope, scope_array):
      if "expression" not in ast_expression:
        raise Exception("Could not find expression")
      expression = ast_expression["expression"]
      output = ""
      if "field_access" in expression:
        primary = self.evaluate_primary(expression["field_access"])
        output += f" Field-access({primary}) " if expression["field_access"]["primary"] != "" else f" Variable({self.get_var_from_scope(primary, scope_array)[0]}) "
      elif "literal" in expression:
        output += self.evaluate_literal(expression["literal"])
      elif "method_invocation" in expression:
        output += self.evaluate_method_invo(expression["method_invocation"])
      elif "binary_expression" in expression:
        output += self.evaluate_binary_expression(expression, scope, scope_array)
      elif "unary_expression" in expression:
        output += self.evaluate_unary_expression(expression, scope, scope_array)
      elif 'literal' in expression:
        output += self.evaluate_literal(expression["literal"])
      elif 'new' in expression:
        output += self.evaluate_new_object(expression["new"])
      elif "auto" in expression:
        output += self.evaluate_auto(expression, scope, scope_array)
      else:
        Exception("Invalid expression statement")
      return output
    
    def evaluate_auto(self, ast_auto, scope, scope_array):
      if "auto" not in ast_auto:
        raise Exception("Could not find auto")
      output = ""
      assigned_value = ""
      auto = ast_auto["auto"]
      # debug(auto)
      if "operand" not in auto:
        raise Exception("Could not find operand")
      variable_name = auto["operand"]["field_access"]["id"]
      var_id = self.get_var_from_scope(variable_name, scope_array)[0]
      if "postfix" in auto:
        assigned_value = f"Variable({var_id}), {auto['postfix']}, post"
      elif "prefix" in auto:
        assigned_value = f"Variable({var_id}), {auto['prefix']}, pre"
      output += f"Auto({assigned_value})"
      return output

    def evaluate_if_block(self, ast_if, scope, scope_array):
      output = ""
      if "if" not in ast_if:
        raise Exception("Could not find if")
      if_block = ast_if["if"]
      if "condition" not in if_block:
        raise Exception("Could not find condition")
      if "if_block" not in if_block:
        raise Exception("Could not find block")
      condition = self.create_expression_record(if_block["condition"], scope, scope_array)
      block = self.create_block_record(if_block["if_block"], scope, scope_array)
      output += f"If({condition}, {block}"
      if "else_block" in if_block:
        output+= ", "
        output += self.create_block_record(if_block["else_block"], scope, scope_array)
      output += ")"
      return output
    
    def evaluate_while_block(self, ast_while, scope, scope_array):
      output = ""
      if "while" not in ast_while:
        raise Exception("Could not find while")
      while_block = ast_while["while"]
      if "condition" not in while_block:
        raise Exception("Could not find condition")
      if "while_block" not in while_block:
        raise Exception("Could not find block")
      condition = self.create_expression_record(while_block["condition"], scope, scope_array)
      block = self.create_block_record(while_block["while_block"], scope, scope_array)
      output += f"While({condition}, {block})"
      return output
    
    def evaluate_for_block(self, ast_for, scope, scope_array):
      output = ""
      if "for" not in ast_for:
        raise Exception("Could not find for")
      for_block = ast_for["for"]
      if "condition" not in for_block:
        raise Exception("Could not find condition")
      if "for_block" not in for_block:
        raise Exception("Could not find block")
      if "init" not in for_block:
        raise Exception("Could not find init")
      if "update" not in for_block:
        raise Exception("Could not find update")
      init = self.create_expression_record(for_block["init"], scope, scope_array)
      update = self.create_expression_record(for_block["update"], scope, scope_array)
      condition = self.create_expression_record(for_block["condition"], scope, scope_array)
      block = self.create_block_record(for_block["for_block"], scope, scope_array)
      output += f"For({init}, {condition}, {update}, {block})"
      return output

    def evaluate_unary_expression(self, ast_unary, scope, scope_array):
        output=""
        if "unary_expression" not in ast_unary:
            raise Exception("Could not find unary expression")
        unary_expression = ast_unary["unary_expression"]
        if "operator" not in unary_expression:
            raise Exception("Could not find operator")
        expression = self.create_expression_record(unary_expression["operand"], scope, scope_array)
        operator_to_string = { 
          "-": "uminus",
        }
        if unary_expression["operator"] == "+":
          return expression

        if unary_expression["operator"] in operator_to_string:
          operator = operator_to_string[unary_expression["operator"]]
        output += f"Unary({expression}, {operator} )"
        return output

    def evaluate_binary_expression(self, ast_binary, scope, scope_array):
        output = ""
        if "binary_expression" not in ast_binary:
            raise Exception("Could not find binary expression")
        
        binary_expression = ast_binary["binary_expression"]
        if "left" not in binary_expression:
            raise Exception("Could not find left operand")
        if "right" not in binary_expression:
            raise Exception("Could not find right operand")
        if "operator" not in binary_expression:
            raise Exception("Could not find operator")
        # debug(binary_expression["left"])
        left_expression = self.create_expression_record(binary_expression["left"], scope, scope_array)
        right_expression = self.create_expression_record(binary_expression["right"], scope, scope_array)
        operator = binary_expression["operator"]

        operator_to_string = {
          "+": "add",
          "-": "sub",
          "*": "mul",
          "/": "div",
          "%": "mod",
          "&&": "and",
          "||": "or",
          "==": "eq",
          "!=": "neq",
          "<": "lt",
          ">": "gt",
          "<=": "leq",
          ">=": "geq"
        }

        if operator not in operator_to_string:
          raise Exception("Invalid operator")

        operator = operator_to_string[operator]
        output += f"Binary({operator}, {left_expression}, {right_expression})"
        return output

    def evaluate_return(self,ast_return, scope, scope_array):
      output = ""
      if "return" not in ast_return:
        raise Exception("Could not find return")
      statement_eval = self.create_expression_record(ast_return["return"], scope, scope_array)
      output += f"Return({statement_eval})"
      return output
    
    def evaluate_method_invo(self,ast_method_invo):
      output = ""
      if "field_access" not in ast_method_invo:
        raise Exception("Could not find method field_access")
      if "arguments" not in ast_method_invo:
        raise Exception("Could not find method arguments")
      method = ast_method_invo["field_access"]
      if "id" not in method:
        raise Exception("Could not find method id")
      if "primary" not in method:
        raise Exception("Could not find method primary")
      output += f"Method-call({self.evaluate_primary(method)}, {ast_method_invo['arguments']}"
      return output
    
    def evaluate_literal(self,ast_literal):
      output = ""
      if "type" not in ast_literal:
        raise Exception("Could not find literal type")
      if "value" not in ast_literal:
        raise Exception("Could not find literal value")
      if ast_literal["type"] == "boolean" or ast_literal["type"] == "Null":
        output += f"Constant({ast_literal['value']})"
      else:
        output += f" {ast_literal['type']}-Constant({ast_literal['value']})"
      return output
    
    def evaluate_new_object(self,ast_new_object):
      output = ""
      output += f"New-object({ast_new_object['type']}, {ast_new_object['arguments']})"
      return output
    
    def evaluate_primary(self,ast_primary):
      output = ast_primary["id"]
      if ast_primary["primary"] != "":
          primary = ast_primary["primary"]
          if "this" == primary or "super" == primary:
              primary = primary.title()
          output = primary
          output += ", "
          output += ast_primary["id"]
      return output

    def traverse_scope_layer(self, scope, scope_layers):
      new_scope = scope.copy()
      for scope_layer in scope_layers:
        if isinstance(new_scope, list):
          found = False
          for scope_item in new_scope:
            if scope_layer in scope_item:
              new_scope = scope_item[scope_layer]
              found = True
          if not found:
            raise Exception("Invalid scope layer traversal: Could not find scope layer")
        elif isinstance(new_scope, dict):
            if scope_layer in new_scope:
                new_scope = new_scope[scope_layer]
            else:
              raise Exception("Invalid scope layer traversal: Could not find scope layer")
        else:
          raise Exception("Invalid scope layer traversal")
      return new_scope

    def add_to_scope(self, local_scope, scope_array, variable_id, variable):
        # traverse global scope to find if the variable is already defined
        global scope
        # debug(scope)
        legal_types = ["class", "method", "constructor"]
        
        if scope_array == []:
            scope_array = ["global"]
        test_scope = scope
        for scope_layer in scope_array:
          if isinstance(test_scope, list):
            for scope_item in test_scope:
              if variable_id in scope_item:
                if variable["type"] == scope_item[variable_id]["type"]:
                  raise Exception("Variable already defined")
                # if scope[type] is not a class, method, or constructor, and variable is not a class, method, or constructor
                # then they are both variables with the same name, which is not allowed
                if scope_item[variable_id]["type"] not in legal_types and variable["type"] not in legal_types:
                    raise Exception("Variable already defined")
          else:
            if variable_id in test_scope:
                if variable["type"] == test_scope["type"]:
                    raise Exception("Variable already defined")
                # if scope[type] is not a class, method, or constructor, and variable is not a class, method, or constructor
                # then they are both variables with the same name, which is not allowed
                if test_scope["type"] not in legal_types and variable["type"] not in legal_types:
                    raise Exception("Variable already defined")
          test_scope = self.traverse_scope_layer(test_scope, [scope_layer])
        
        if isinstance(local_scope, list):
          local_scope.append({variable_id: variable})
        else:
          local_scope[variable_id] = variable
        # debug(f"added {variable_id} to {scope_array} with type {variable['type']}")
        # debug(f"{local_scope}")
        return local_scope
        
    def get_var_from_scope(self, variable_name, scope_array):
        global scope
        if scope_array == []:
            scope_array = ["global"]
        test_scope = scope
        # debug(scope)
        for scope_layer in scope_array:
            test_scope = self.traverse_scope_layer(test_scope, [scope_layer])
            # debug(f"searching for {variable_name} in {scope_array}, in layer {test_scope}")
            if isinstance(test_scope, list):
              for scope_item in test_scope:
                if variable_name in scope_item:
                    return [scope_item[variable_name]["id_num"], scope_item[variable_name]["type"]]
            else:
              if variable_name in test_scope:
                return [test_scope[variable_name]["id_num"], test_scope[variable_name]["type"]]
        # debug(f"{scope_array}, {test_scope}")
        raise Exception("Variable not found")

# printing functions

def writeJSON(filename, data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent=2)
    return True

def readJSON(filename):
    with open(filename, 'r') as infile:
        data = json.load(infile)
    return data

def writeAST(ast_blocks):
    writeJSON("ast.json", [x.ast for x in ast_blocks if isinstance(x, AST)])
    global scope
    debug(scope)
    # print(ast_blocks)
    output = print_ast_blocks(ast_blocks)
    print(output)

def print_ast_blocks(ast_blocks):
    output = "-----------------------------------------------\n"
    for ast in ast_blocks:
        if ast == None:
            continue
        output += ast.print_ast()
        output += "-----------------------------------------------\n"
    return output

# extraction functions

def extract_body(ast):
    if "body" not in ast:
        raise Exception("Could not find body")
    global field_count, method_count, class_count
    fields = {}
    methods = {}
    constructors = {}
    for item in ast["body"]:
        if 'field' in item:
          for id_name in item['field']['ids']:
              fields[field_count] = item['field']
              fields[field_count]['id'] = id_name
              del fields[field_count]['ids']
              field_count += 1
        elif 'method' in item:
            methods[method_count] = item['method']
            method_count += 1
        elif 'constructor' in item:
            constructors[class_count] = item['constructor']
            class_count += 1
        else:
            raise Exception("Could not find field, method, or constructor")
    ast["body"] = {"fields": fields, "methods": methods,
                   "constructors": constructors}
    return AST(ast, fields, methods, constructors)


def extract_variables_from_formals(key, ast):
    if key not in ast:
        raise Exception(f"Could not find {key}")
    if 'formals' not in ast[key]:
        raise Exception("Could not find formals")
    global var_count
    params = {}
    for item in ast[key]["formals"]:
        if 'parameter' in item:
            item['parameter']['var_type'] = 'formal'
            params[var_count] = item['parameter']
            var_count += 1
        else:
            raise Exception("Could not find variable")
    ast[key]["formals"] = params
    return ast


def extract_variables_from_field(ast):
    if 'field' not in ast:
        raise Exception("Could not find field")
    if 'variables' not in ast['field']:
        raise Exception("Could not find variables")
    if 'type' not in ast['field']['variables']:
        raise Exception("Could not find type")
    if 'ids' not in ast['field']['variables']:
        raise Exception("Could not find ids")
    ast['field']['type'] = ast['field']['variables']['type']
    ast['field']['ids'] = ast['field']['variables']['ids']
    del ast['field']['variables']
    return ast


