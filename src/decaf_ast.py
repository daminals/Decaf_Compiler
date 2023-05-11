# decaf_ast.py
# Daniel Kogan dkogan 114439349
# 04.17.2023

import json,sys
import predefined_classes as predef
import decaf_typecheck as dtype
import decaf_codegen as dcodegen
from debug import *
field_count = 1
method_count = 6
class_count = 1
class_overall_count = 3
var_count = 1
valid_types = ["int", "boolean", "string", "float", "double", "char", "void", "error", "null"]
user_defined_types = []
scope = {"global": {}}
for_count = 0
if_count = 0
while_count = 0
bin_count = 0
L_count = 0
# add objects as they are defined
type_table = {
  # size of diff types in bytes
  "int": "4",
  "float": "4",
  "boolean": "1"
}
static_count = 0

class AST:

    def __init__(self, ast, fields, methods, constructors):
        self.ast = ast
        self.fields = fields
        self.methods = methods
        self.constructors = constructors
        self.size = 0
        self.asm = ""
        self.asm_data = {}
        self.asm_registers = ["t0","t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8", "t9",
                          "t10", "t11", "t12", "t13", "t14", "t15", "t16", "t17", "t18",
                          "t19", "t20", "t21", "t22", "t23", "t24", "t25", "t26", "t27",
                          "t28", "t29"]
        self.asm_stack = []

        # Check class name
        if "class_name" not in ast:
            # raise Exception("Could not find class name")
            error("Could not find class name")
        if ast["class_name"] == "":
            error("Class name is empty")
            # raise Exception("Class name is empty")
        self.class_name = ast["class_name"]
        self.asm_data["class_name"] = self.class_name
        self.asm += dcodegen.generate_label(self.class_name)

        # Check super class
        if "superclass" not in ast:
            error("Could not find superclass name")
            # raise Exception("Could not find class name")
        self.superclass_name = ast["superclass"]

        global scope, type_table
        # Check if class name is already defined
        if self.class_name in scope["global"]:
            error(f"Line:{ast['line_num']}:{ast['col_num']}: Class name already defined")
            # raise Exception("Class name already defined")

        # write all superclass children to this class
        children = []
        def set_super_true(child):
          # get keys
          keys = list(child.keys())
          for key in keys:
            child[key]["super"] = True
          return child

        if self.superclass_name != "":
          children = scope["global"][self.superclass_name]["children"]
          children = [set_super_true(child) for child in children]

        self.scope = self.add_to_scope(scope["global"], [], self.class_name, {"type": "class", "superclass_name": self.superclass_name, "children": children, "id_num": class_count, "id": self.class_name,  "line_num": ast["line_num"], "col_num": ast["col_num"]})

        self.printed = self.create_record(self.ast, self.scope[self.class_name])
        scope["global"] = self.scope
        type_table[self.class_name] = str(self.size)

    def print_ast(self):
        asm = ""
        if debug_mode:
            # ignore in and out
            if self.class_name != "In" and self.class_name != "Out":
              # dcodegen.write_asm(f"{self.class_name}.asm",self.asm)
              asm = self.asm
        else:
            # dcodegen.write_asm(f"{self.class_name}.asm",self.asm)
            asm = self.asm
        return self.printed, asm
      
    def get_size(self, _type):
      if (_type in type_table):
        return type_table[_type]
      error(f"ERROR: TYPE {_type} NOT IN TYPE TABLE")

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
            # raise Exception("Could not find fields")
            error("Could not find fields")
        self.fields = ast["body"]["fields"]
        output += self.create_field_record(scope["children"], scope_array + ["children"])

        # check constructors
        if "constructors" not in ast["body"]:
            # raise Exception("Could not find constructors")
            error("Could not find constructors")
        self.constructors = ast["body"]["constructors"]
        output += self.create_constructor_record(scope["children"], scope_array + ["children"])

        # check methods
        if "methods" not in ast["body"]:
            # raise Exception("Could not find methods")
            error("Could not find methods")
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
        blacklist = []
        for field_id in self.fields.keys():
            field = self.fields[field_id]
            # debug(field)
            # name
            if "id" not in field:
                # raise Exception("Could not find field names (id)")
                error(f"Line:{field['line_num']}:{field['col_num']}: Could not find field names (id)")
            field_name = field["id"]
            # type
            if "type" not in field:
                error(f"Line:{field['line_num']}:{field['col_num']}: Could not find field type")
                # raise Exception("Could not find field type")
            field_type = self.create_type_record(field["type"])
            # modifiers
            if "modifiers" not in field:
                error(f"Line:{field['line_num']}:{field['col_num']}: Could not find field modifiers")
                # raise Exception("Could not find field modifiers")
            field_modifiers = self.create_modifiers_list(field["modifiers"])
            # add field to scope
            # for prev_field in blacklist:
            #   if compare_var(prev_field, {"var_type": "field", "type": f"{field_type}", "id": field_name}):
            #     error(f"Line:{field['line_num']}:{field['col_num']}: Field {field_name} already defined")
            # blacklist.append({"var_type": "field", "type": f"{field_type}", "id": field_name})
            var_object = {"super": False, "type": f"{field_type}","id": field_name, "formal": False, "var_type": "field","id_num": field_id, "modifiers": field["modifiers"], "line_num": field["line_num"], "col_num": field["col_num"]}
            self.add_to_scope(scope, scope_array, field_name,var_object)
            # scope_array.append(field_name)
            # scope = scope[field_name]

            # debug(scope)
            output += f"FIELD {field_id}, {field_name}, {self.class_name}, {field_modifiers}, {field_type}\n"
            field_size = self.get_size(field_type)
            self.size += int(field_size)
            # debug(self.asm_registers)
            asm_output, self.asm_registers, self.asm_data = dcodegen.generate_field({"name": field_name,"field_id": field_id, 'line_num': field['line_num'], 'col_num': field['col_num']}, field_size, self.asm_data, self.asm_registers)
            self.asm += asm_output
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
                error(f"Line:{constructor['line_num']}:{constructor['col_num']}: Could not find constructor modifiers")
                # raise Exception("Could not find field modifiers")
            constructor_modifiers = self.create_modifiers_list_PRIVATE_PUBLIC(
                constructor["modifiers"])

            output += f"CONSTRUCTOR: {constructor_id}, {constructor_modifiers}\n"
            output += "Constructor Parameters:\n"
            
            local_scope = self.add_to_scope(scope, scope_array, constructor_id, {"super": False, "type": "constructor", "id": self.class_name, "id_num": constructor_id, "modifiers": constructor["modifiers"] ,"children": [], "line_num": constructor["line_num"], "col_num": constructor["col_num"], "signature": dtype.create_type_signature(self.class_name, [], id=constructor_id) })
            formal_scope = self.traverse_scope_layer(local_scope, [constructor_id])
            local_scope = self.traverse_scope_layer(local_scope, [constructor_id, "children"])
            local_scope_array.append(constructor_id)
            local_scope_array.append("children")

            self.asm += dcodegen.generate_commented_label(f"C_{constructor_id}", f"CONSTRUCTOR: {constructor_id}")
            self.asm_data[f"C_{constructor_id}"] = {}

            output += "Variable Table:\n"
            formal_types = []
            num_params = 0
            local_stack = []
            for variable_id in constructor["formals"].keys():
                variable = constructor["formals"][variable_id]
                formal_types.append(variable["type"])
                self.add_to_scope(local_scope, local_scope_array, variable["id"], {"super": False, "type": f"{self.create_type_record(variable['type'])}", "id_num": variable_id, "id": variable["id"], "formal": True, "var_type": "local", "line_num": variable["line_num"], "col_num": variable["col_num"]})
                output += self.create_variable_record(variable_id, variable)
                self.asm += dcodegen.generate_comment(f"a{num_params}: {variable['id']}")
                self.asm_data[f"PARAMETER_{variable_id}"] = "a" + str(num_params)
                local_stack.insert(0, f"a{num_params}")
                num_params+=1
            local_stack.reverse()
            for register in local_stack:
              self.asm_registers.insert(0, register)
            # add formals to constructor signature in scope
            formal_scope["signature"] = dtype.create_type_signature(self.class_name, formal_types, id=constructor_id)

            block, is_block_type_correct = self.create_block_record(constructor["body"], local_scope, local_scope_array)

            output += "Constructor Body:\n"
            output += block
            self.asm += dcodegen.generate_return("a0")
            self.asm += dcodegen.generate_comment(f"END CONSTRUCTOR: C_{constructor_id}")
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
            # asm_output = dcodegen.generate_method(method, method_id, self.asm_data)
            # self.asm += dcodegen.generate_comment(f"METHOD: {method_name}")
            self.asm += dcodegen.generate_commented_label(f"M_{method_name}_{method_id}", f"METHOD: {method_name}")
            self.asm_data[f"M_{method_name}_{method_id}"] = {}

            output += f"METHOD: {method_id}, {method_name}, {self.class_name}, {method_modifiers}, {method_type}\n"
            output += "Method Parameters:\n"

            local_scope = self.add_to_scope(local_scope, local_scope_array, method_name, {"super": False, "type": "method", "id": method_id, "id_num": method_id, "modifiers": method["modifiers"], "return_type": method["type"], "children": [], "line_num": method["line_num"], "col_num": method["col_num"]})
            formal_scope = self.traverse_scope_layer(local_scope, [method_name])
            local_scope = self.traverse_scope_layer(local_scope, [method_name, "children"])
            local_scope_array.append(method_name)
            local_scope_array.append("children")

            formal_types = []
            num_params = 0
            for variable_id in method["formals"].keys():
                variable = method["formals"][variable_id]
                formal_types.append(variable["type"])
                self.add_to_scope(local_scope, local_scope_array, variable["id"], {"super": False, "type": f"{self.create_type_record(variable['type'])}", "id_num": variable_id, "id": variable["id"], "var_type": "local", "formal": True,"line_num": variable["line_num"], "col_num": variable["col_num"] })
                output += self.create_variable_record(variable_id, variable)
                self.asm += dcodegen.generate_comment(f"a{num_params}: {variable['id']}")
                self.asm_data[f"PARAMETER_{variable_id}"] = "a" + str(num_params)
                num_params += 1

            # add signature
            formal_scope["signature"] = dtype.create_type_signature(method_name, formal_types)

            # method["type"] = return_type
            block, is_block_type_correct = self.create_block_record(method["body"], local_scope, local_scope_array, return_type=self.create_type_record(method["type"]))
            
            output += "Variable Table:\n"
            # check scope for variables
            for variable in local_scope:
              for var_id in variable.keys():
                if variable[var_id]["formal"]:
                  continue
                output += self.create_variable_record(variable[var_id]["id_num"], variable[var_id])

            output += "Method Body:\n"
            output += block
            self.asm += dcodegen.generate_comment("if method does not return, return void. if it does return, this was never reached ;-)")
            self.asm += dcodegen.generate_return("a0")
            self.asm += dcodegen.generate_comment(f"END METHOD: {method_name}")
            if len(self.asm_stack) > 0:
              self.asm_stack.pop(0)
        return output
      
    def create_block_record(self, ast_block, scope, scope_array, return_type='void', skip_stmt=False, labels=[None, None]):
        output = "Block(["
        statements = "\n"
        type_correct = True
        for statement in ast_block:
            expr =  "Expr( "
            # debug(statement)
            # debug(scope)
            stmt_output, stmt_type_correct = self.create_statement_record(statement, scope, scope_array, return_type, labels)
            stmt = stmt_output
            expr += stmt
            if stmt == "":
                expr = ""
            else:
              type_correct &= stmt_type_correct
              type_correct_stmt = "Not " if not stmt_type_correct else ""
              expr += f", {type_correct_stmt}Type Correct )\n, "
            statements += expr
        output += statements
        # if output ends with newline and comma, remove it
        if output[-3:] == "\n, ": 
            output = output[:-2]
        if ast_block == [None]:
          if skip_stmt:
            output = "Skip()"
            return [output, True]
          type_correct = True
        
        type_correct_stmt = "Not " if not type_correct else ""
        output += f"], {type_correct_stmt}Type Correct )\n"
        return [output, type_correct]

    def create_type_record(self, ast_type, return_type=0):
        """ 
        Type Record: Contents
          • Type: the name of the type
        """
        output = ""
        global valid_types, user_defined_types

        local_valid_types = valid_types.copy()
        # if return_type == 1:
        #     local_valid_types.append("void")

        if ast_type in user_defined_types:
            output += f"user({ast_type})"
            return output

        if ast_type not in local_valid_types:
            # raise Exception("Invalid type")
            error(f"Line:{ast_type['line_num']}:{ast_type['col_num']}: Invalid type {ast_type}")
        output += f"{ast_type}"
        return output

    def create_variable_record(self, variable_id, ast_variable):
        output = ""
        output += f"VARIABLE {variable_id}, {ast_variable['id']}, {ast_variable['var_type']}, {ast_variable['type']}\n"
        return output

    # String of modifiers list, including instance or static
    def create_modifiers_list(self, ast_modifiers):
        output = "private"
        if "static" in ast_modifiers:
              global static_count
              static_count += 1
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
        if "static" in ast_modifiers:
              global static_count
              static_count += 1
        if ast_modifiers == []:
            output = "private"
        elif "private" in ast_modifiers:
            output = "private"
        else:
            output = "public"
        return output

    def create_statement_record(self, ast_statement, scope, scope_array, expected_return_type=None, labels=[None, None]):
        output = ""
        type_correct = True
        if ast_statement == None:
          return [output, True]
        if "set_equal" in ast_statement:
          assignment_output, assignment_type = self.create_assignment_record(ast_statement, scope_array, scope)
          output += assignment_output
          if assignment_type == "error":
            type_correct &= False
          # stmt_type = assignment_type
        elif "auto" in ast_statement:
          auto_out, auto_type = self.evaluate_auto(ast_statement, scope, scope_array)
          output += auto_out
          # stmt_type = auto_type
          if auto_type == "error":
            type_correct &= False
        elif "var_decl" in ast_statement:
          var_decl_out, var_decl_type = self.create_variable_declaration_record(ast_statement, scope, scope_array)
          output += var_decl_out
          if var_decl_type == "error":
            type_correct &= False
        elif "return" in ast_statement:
          return_out, return_type = self.evaluate_return(ast_statement, scope, scope_array, expected_return_type)
          output += return_out
          # stmt_type = return_type
          if return_type == "error":
            type_correct &= False
        elif "if" in ast_statement:
          if_out, if_type = self.evaluate_if_block(ast_statement, scope, scope_array, expected_return_type)
          type_correct &= if_type
          output += if_out
        elif "while" in ast_statement:
          while_out, while_type = self.evaluate_while_block(ast_statement, scope, scope_array, expected_return_type)
          type_correct &= while_type
          output += while_out
        elif "for" in ast_statement:
          for_out, for_type = self.evaluate_for_block(ast_statement, scope, scope_array, expected_return_type)
          output += for_out
          type_correct &= for_type
        elif "break" in ast_statement:
          output += "Break"
          self.asm += dcodegen.generate_jump(label[1]) # end label
        elif "continue" in ast_statement:
          output += "Continue"
          # i dont know the label to jump to
          self.asm += dcodegen.generate_jump(label[0]) # start label
        elif "method_invocation" in ast_statement:
          method_invo_out, method_invo_type = self.evaluate_method_invo(ast_statement["method_invocation"], scope, scope_array)
          output += method_invo_out
          if method_invo_type == "error":
            type_correct &= False
        elif "expression" in ast_statement:
          # debug(scope)
          expr_out, expr_type = self.create_expression_record(ast_statement, scope, scope_array, expected_return_type)
          output += expr_out
          if expr_type == "error":
            type_correct &= False
        else:
          # raise Exception(f"Invalid statement: {ast_statement}")
          error(f"Line:{ast_statement['line_num']}:{ast_statement['col_num']}: Invalid statement: {ast_statement}")
        return [output, type_correct]

    def create_variable_declaration_record(self, ast_variable_declaration, scope, scope_array):
        output = ""
        stmt_type = ""
        if "var_decl" not in ast_variable_declaration:
            # raise Exception("Could not find variable declaration")
            error(f"Line:{ast_variable_declaration['line_num']}:{ast_variable_declaration['col_num']}: Could not find variable declaration")
        variable_declaration = ast_variable_declaration["var_decl"]
        for var in variable_declaration.keys():
            if "id" not in variable_declaration[var]:
                # raise Exception("Could not find variable id")
                error(f"Line:{ast_variable_declaration['line_num']}:{ast_variable_declaration['col_num']}: Could not find variable id")
            if "type" not in variable_declaration[var]:
                # raise Exception("Could not find variable type")
                error(f"Line:{ast_variable_declaration['line_num']}:{ast_variable_declaration['col_num']}: Could not find variable type")
            
            var_id = variable_declaration[var]["id"]
            var_type = variable_declaration[var]["type"]
            stmt_type = var_type
            
            self.add_to_scope(scope, scope_array, var_id, {"super": False, "type": f"{self.create_type_record(var_type)}", "id_num": var, "id": var_id, "var_type": "local", "formal": False, "line_num": variable_declaration[var]["line_num"], "col_num": variable_declaration[var]["col_num"]})
            output += self.create_variable_record(var, variable_declaration[var])
            self.asm_data[f"VARIABLE_{var}"] = self.asm_registers.pop(0)
            warn(f"variable {var} is stored in {self.asm_data[f'VARIABLE_{var}']}")
            self.asm_stack.insert(0, self.asm_data[f"VARIABLE_{var}"])
            warn(f"stack is now {self.asm_stack}")
            # output += f"VariableDeclaration({var_id}, {var_type})\n"
        return ["", stmt_type]

    def create_assignment_record(self, ast_assignment, scope_array, local_scope):
        # debug(local_scope)
        debug(f"before assignment record: {self.asm_stack}")
        if "set_equal" not in ast_assignment:
          # raise Exception("Could not find assignment")
          error(f"Line:{ast_variable_declaration['line_num']}:{ast_assignment['col_num']}: Could not find assignment")
        output = ""
        assignee_type = ""
        assigned_value_type = ""
        assignment = ast_assignment["set_equal"]
        if "assign" not in assignment:
            # raise Exception("Could not find assignee")
            error(f"Line:{ast_variable_declaration['line_num']}:{ast_assignment['col_num']}: Could not find assignee ")
        
        operand = assignment["assign"]
        primary_scope = []
        if "field_access" in operand["assignee"]:
          primary_scope = self.create_primary_array(operand["assignee"]["field_access"], scope, scope_array)
          # warn(f"primary_scope: {primary_scope}")
          if primary_scope != ['global'] and primary_scope != []:
            # create new local scope for this variable
            primary_scope = self.get_primary_scope(primary_scope, operand['assignee']['field_access'], scope, scope_array)
          else: primary_scope = scope_array

        var_id_num, var_type, is_field_var, var_info = self.get_var_from_scope(operand["assignee"]["field_access"]["id"], primary_scope)
        assignee_type = var_type
        expr_type = "Assign"
        var_scope_type = "Variable("
        if "field" == is_field_var:
          var_scope_type = "Field-access("

        assignee = f"{var_id_num}"
        # evaluate primary if field access
        if "field_access" in operand["assignee"] and var_scope_type == "Field-access(":
          assignee_primary = self.evaluate_primary(operand['assignee']['field_access'], scope, scope_array)
          assignee_type = assignee_primary[1]
          var_scope_type += f"{assignee_primary[0]}, "
        
        assigned_value = ""
        if "assigned_value" not in operand:
          # raise Exception("Could not find assigned value")
          error(f"Line:{operand['assignee']['line_num']}:{operand['assignee']['col_num']}: Could not find assigned value")
        if "expression" in operand["assigned_value"]:
          # debug(operand["assigned_value"])
          assigned_value, assigned_value_type = self.create_expression_record(operand["assigned_value"], local_scope, scope_array)
          # debug(f"STACK: {self.asm_stack}")
        else:
          # raise Exception("Could not find assigned value type")
          error(f"Line:{operand['assignee']['line_num']}:{operand['assignee']['col_num']}: Could not find assigned value type")
        
        # Consider e1 = e2. The type of this expression is e2's type, provided:
        # • e1 and e2 are type correct
        # • e2's type is a subtype of e1's type.
        stmt_type = "error"
        if dtype.is_subtype(scope, assigned_value_type, assignee_type):
          stmt_type = assignee_type
        expression = f"{var_scope_type}{assignee}), {assigned_value}, {assignee_type}, {assigned_value_type} "
        if expr_type != "":
          output += f"{expr_type}({expression})"
        else:
          output += expression
          
        # create asm for assignment
        # move value of assigned_value to assignee
        assigned_reg = self.asm_stack.pop(0)
        if "field" != is_field_var:
          assignee_reg = self.asm_stack.pop(0)
          self.asm += dcodegen.generate_move(assignee_reg, assigned_reg)
        else:
          assignee_reg = self.asm_data[f"FIELD_{var_id_num}"]
          self.asm += dcodegen.generate_hstore(assigned_reg, assignee_reg)
        
        # free assigned_reg
        self.asm_registers.insert(0, assigned_reg)
        
        # push assignee_reg to stack
        self.asm_stack.insert(0, assignee_reg)
    
        return [output, stmt_type]

    def create_expression_record(self, ast_expression, scope, scope_array, expected_return_type="void"):
      if "expression" not in ast_expression:
        # raise Exception(f"Could not find expression in {ast_expression}")
        error(f"line:{ast_expression['line_num']}:{ast_expression['col_num']}: Could not find expression in {ast_expression}")
      expression = ast_expression["expression"]
      output = ""
      statement_type = ""
      if "field_access" in expression:
        primary, var_type, var_id, expression_info = self.evaluate_primary(expression["field_access"], scope, scope_array)
        primary_array = primary.split(", ")[:-1]
        var = []
        if primary_array != []:
          var = self.get_var_from_scope(var_id, self.get_primary_scope(primary_array, expression["field_access"], scope, scope_array))
        else:
          var = self.get_var_from_scope(var_id, scope_array)
        # debug(f"var: {var}")
        warn(f"asm stack (expr): {self.asm_stack}")
        if var[2] == "field":
          output += f"Field-access({primary}, {var[0]})"
          # get register from var_id
          register = self.asm_data[f"FIELD_{var[0]}"] 
          # need to load the value from the register since it is field
          reg_out, reg_value = dcodegen.generate_get_field_value(register, self.asm_registers)
          self.asm += reg_out
          self.asm_stack.insert(0,reg_value)
          # debug(f"stack: {self.asm_stack}")
        else:
          # debug(f"var: {var}")
          # debug(self.asm_data)
          output+= f"Variable({var[0]})"
          # check if parameter
          if var[3]['formal']:
            # get register from var_id
            register = self.asm_data[f"PARAMETER_{var[0]}"] 
            # need to load the value from the register since it is parameter
            # debug(f"register: {register}")
            self.asm_stack.insert(0, register)
          else:
            # warn(f"var: {var}, {self.asm_stack}")
            # debug(self.asm_data)
            self.asm_stack.insert(0, self.asm_data[f"VARIABLE_{var[0]}"] )
            # warn(f"stack: {self.asm_stack}")
        statement_type = var[1]
      elif "literal" in expression:
        literal_out, literal_type = self.evaluate_literal(expression["literal"])
        output += literal_out
        statement_type = literal_type
      elif "method_invocation" in expression:
        method_invo_out, method_invo_type = self.evaluate_method_invo(expression["method_invocation"], scope, scope_array)
        output += method_invo_out
        statement_type = method_invo_type
      elif "binary_expression" in expression:
        bin_out, bin_type = self.evaluate_binary_expression(expression, scope, scope_array)
        output += bin_out
        statement_type = bin_type
      elif "unary_expression" in expression:
        unary_out, unary_type = self.evaluate_unary_expression(expression, scope, scope_array)
        output += unary_out
        statement_type = unary_type
      elif 'new' in expression:
        new_out, new_type = self.evaluate_new_object(expression["new"],scope, scope_array)
        output += new_out
        statement_type = new_type
      elif "auto" in expression:
        auto_out, auto_type = self.evaluate_auto(expression, scope, scope_array)
        output += auto_out
        statement_type = auto_type
      elif "set_equal" in expression:
        # debug(scope)
        assignment_out, assignment_type = self.create_assignment_record(expression, scope_array, scope)
        output += assignment_out
        statement_type = assignment_type
      elif "this" == expression:
        output += "this"
        statement_type = f"user({self.class_name})"
      elif "super" == expression:
        output += "super"
        if self.superclass_name == "":
          statement_type = "error"
        else:
          statement_type = f"user({self.superclass_name})"
      elif "expression" in expression:
        expression_out, expression_type = self.create_expression_record(expression, scope, scope_array, expected_return_type)
        output+= expression_out
        statement_type = expression_type
      else:
        # Exception("Invalid expression statement")
        error(f"Line:{expression['line_num']}:{expression['col_num']}: Invalid expression statement")
      return [output, dtype.make_little_type(statement_type)]
    
    def evaluate_auto(self, ast_auto, scope, scope_array):
      if "auto" not in ast_auto:
        # raise Exception("Could not find auto")
        error(f"Line:{ast_auto['line_num']}:{ast_auto['col_num']}: Could not find auto")
      output = ""
      stmt_type = ""
      assigned_value = ""
      auto = ast_auto["auto"]
      if "operand" not in auto:
        # raise Exception("Could not find operand")
        error(f"{auto['line_num']}:{auto['col_num']}: Could not find operand")
      variable_name = auto["operand"]["field_access"]["id"]
      var_id, var_type, type_of_variable, var_info = self.get_var_from_scope(variable_name, scope_array)
      
      # implement type check on var type
      if not dtype.is_number_type(var_type, scope):
        error(f"Line:{ast_auto['line_num']}:{ast_auto['col_num']}: {var_type} is not a number type")

      stmt_type = var_type

      if "postfix" in auto:
        assigned_value = f"Variable({var_id}), {auto['postfix']}, post"
      elif "prefix" in auto:
        assigned_value = f"Variable({var_id}), {auto['prefix']}, pre"
      output += f"Auto({assigned_value}, {stmt_type})"
      
      # if auto on field type, need to call hload and hstore on the field var
      if var_info['var_type'] == 'field':
        # get the register from the field
        field_register = self.asm_data[f"FIELD_{var_id}"]
        # hload value
        reg_out, register = dcodegen.generate_get_field_value(field_register, self.asm_registers)
        self.asm += reg_out
        # self.asm_stack.append(reg_value)
        asm_output, register = dcodegen.generate_auto(ast_auto, register, stmt_type, self.asm_registers)
        self.asm += asm_output
        # call hstore on the field register
        self.asm += dcodegen.generate_hstore(register, field_register)
        # free register
        self.asm_registers.insert(0,register)
        self.asm_stack.append(field_register)
      else:
        register = self.asm_stack.pop(0)
        asm_output, register = dcodegen.generate_auto(ast_auto, register, stmt_type, self.asm_registers)
        self.asm += asm_output
        self.asm_stack.append(register)
  
      
      return [output, stmt_type]

    def evaluate_if_block(self, ast_if, scope, scope_array, return_type='void'):
      output = ""
      type_correct = True
      if "if" not in ast_if:
        # raise Exception("Could not find if")
        error(f"line:{ast_if['line_num']}:{ast_if['col_num']}: Could not find if")
      if_block = ast_if["if"]
      if "condition" not in if_block:
        # raise Exception("Could not find condition")
        error(f"Line:{if_block['line_num']}:{if_block['col_num']}: Could not find condition")
      if "if_block" not in if_block:
        # raise Exception("Could not find block")
        error(f"line:{if_block['line_num']}:{if_block['col_num']}: Could not find block")
      
      # condition_type = dtype.resolve_expression_type(if_block["condition"])
      # # implement type resolution for condition (should be boolean)
      # if condition_type != "boolean":
      #   type_correct = False
      condition, condition_type = self.create_expression_record(if_block["condition"], scope, scope_array)
      if condition_type != "boolean":
        type_correct = False

      # evaluate condition first
      # create expression record will also assign a register to the expression
      register = self.asm_stack.pop(0)
      global if_count
      if_header = dcodegen.generate_if_header(ast_if['if'], register, if_count)
      self.asm += if_header

      # create block record
      block, is_if_block_type_correct = self.create_block_record(if_block["if_block"], scope, scope_array, return_type=return_type, skip_stmt=True, labels=[f"if_{if_count}",f"endif_{if_count}"])
      # type correct if block is type correct
      type_correct &= is_if_block_type_correct

      # add else asm
      else_header = dcodegen.generate_else_header(ast_if['if'], if_count)
      self.asm += else_header

      output += f"If({condition}, {block}"
      if "else_block" in if_block:
        output+= ", "
        block_out, is_else_block_type_correct = self.create_block_record(if_block["else_block"], scope, scope_array, skip_stmt=True, return_type=return_type, labels=[f"else_{if_count}",f"endif_{if_count}"])
        output += block_out
        type_correct = type_correct and is_else_block_type_correct
      else:
        output+= ", Skip()"
        
      # add end label
      # self.asm += dcodegen.generate_label(f"end_{if_count}")
      self.asm += dcodegen.generate_if_footer(if_count)
      if_count += 1
      # include type correct param
      if not type_correct:
        output += ", Not Type Correct"
      else :
        output += ", Type Correct"
      output += ")"
      return [output, type_correct]
    
    def evaluate_while_block(self, ast_while, scope, scope_array, return_type='void'):
      output = ""
      type_correct = True
      if "while" not in ast_while:
        # raise Exception("Could not find while")
        error(f"Line:{ast_while['line_num']}:{ast_while['col_num']}: Could not find while")
      while_block = ast_while["while"]
      if "condition" not in while_block:
        # raise Exception("Could not find condition")
        error(f"Line:{while_block['line_num']}:{while_block['col_num']}: Could not find condition")
      if "while_block" not in while_block:
        # raise Exception("Could not find block")
        error(f"Line:{while_block['line_num']}:{while_block['col_num']}: Could not find block")
      
      # condition_type = dtype.resolve_expression_type(while_block["condition"])
      # implement type resolution for condition (should be boolean)
      # if condition_type != "boolean":
      #   type_correct = False
      
      global while_count
      
      self.asm += dcodegen.generate_while_header(ast_while['while'], while_count)

      condition, condition_type = self.create_expression_record(while_block["condition"], scope, scope_array, return_type)
      if condition_type != "boolean":
        type_correct = False
        
      # get register to evaluae condition
      register = self.asm_stack.pop(0)
      self.asm+= dcodegen.generate_while_condition(register, while_count)

      block, is_block_type_correct = self.create_block_record(while_block["while_block"], scope, scope_array, return_type=return_type, skip_stmt=True, labels=[f"while_{while_count}",f"endwhile_{while_count}"])
      # type correct if block is type correct
      type_correct = type_correct and is_block_type_correct
      
      self.asm += dcodegen.generate_while_footer(while_count)
      while_count += 1
      # remove newline if block has 
      if block[-1] == "\n":
        block = block[:-1]
      output += f"While({condition}, {block})"
      if not type_correct:
        output = f"({output}, Not Type Correct)"
      else :
        output = f"({output}, Type Correct)"
      return [output, type_correct]
    
    def evaluate_for_block(self, ast_for, scope, scope_array, return_type='void'):
      output = ""
      type_correct = True
      if "for" not in ast_for:
        # raise Exception("Could not find for")
        error(f"Line:{ast_for['line_num']}:{ast_for['col_num']}: Could not find for")
      for_block = ast_for["for"]
      if "condition" not in for_block:
        # raise Exception("Could not find condition")
        error(f"Line:{for_block['line_num']}:{for_block['col_num']}: Could not find condition")
      if "for_block" not in for_block:
        # raise Exception("Could not find block")
        error(f"Line:{for_block['line_num']}:{for_block['col_num']}: Could not find block")
      if "init" not in for_block:
        # raise Exception("Could not find init")
        error(f"Line:{for_block['line_num']}:{for_block['col_num']}: Could not find init")
      if "update" not in for_block:
        # raise Exception("Could not find update")
        error(f"Line:{for_block['line_num']}:{for_block['col_num']}: Could not find update")

      init = "Skip()"
      init_type_correct = True
      if for_block["init"] != None:
        init_out, init_type = self.create_expression_record(for_block["init"], scope, scope_array, return_type)
        init = init_out
        if init_type == "error":
          init_type_correct = False
      
      init_register = self.asm_stack.pop(0)
      global for_count
      self.asm += dcodegen.generate_for_header(ast_for['for'], for_count)
      
      condition = "Skip()"
      condition_type_correct = True
      if for_block["condition"] != None:
        condition_out, condition_type = self.create_expression_record(for_block["condition"], scope, scope_array, return_type)
        condition = condition_out
        # condition_type = dtype.resolve_expression_type(for_block["condition"])
        # # implement type resolution for condition (should be boolean)
        if condition_type != "boolean":
          condition_type_correct = False
      
      condition_register = self.asm_stack.pop(0)
      self.asm += dcodegen.generate_for_condition(ast_for['for'], for_count, condition_register)
      
      self.asm_stack.insert(0,init_register)
      
      update = "Skip()"
      update_type_correct = True
      if for_block["update"] != None:
        update_out, update_type = self.create_expression_record(for_block["update"], scope, scope_array, return_type)
        update = update_out
        if update_type == "error":
          update_type_correct = False
          
      update_register = self.asm_stack.pop(0)
      if update_register != init_register:
        # move update to init
        self.asm += dcodegen.generate_move(init_register, update_register)
        self.asm_stack.insert(0, update_register)
      

      # type correct if block,update,init are type correct   
      type_correct &= init_type_correct and update_type_correct and condition_type_correct

      block, is_block_type_correct = self.create_block_record(for_block["for_block"], scope, scope_array, return_type=return_type, skip_stmt=True, labels=[f"for_{for_count}",f"endfor_{for_count}"])

      # end for block
      # create jump to start of for
      self.asm += dcodegen.generate_jump(f"for_{for_count}")
      # for footer
      self.asm += dcodegen.generate_for_footer(for_count)
      for_count += 1


      # type correct if block is type correct
      type_correct = type_correct and is_block_type_correct

      # type correct if block,update,init are type correct
      output += f"For({init}, {condition}, {update}, {block})"
      return [output, type_correct]

    def evaluate_unary_expression(self, ast_unary, scope, scope_array):
        output=""
        expr_type = ""
        if "unary_expression" not in ast_unary:
            # raise Exception("Could not find unary expression")
            error(f"Line:{ast_unary['line_num']}:{ast_unary['col_num']}: Could not find unary expression")
        unary_expression = ast_unary["unary_expression"]
        if "operator" not in unary_expression:
            # raise Exception("Could not find operator")
            error(f"Line:{unary_expression['line_num']}:{unary_expression['col_num']}: Could not find operator")
        expression, expr_type = self.create_expression_record(unary_expression["operand"], scope, scope_array)
        # expr_type = dtype.resolve_expression_type(unary_expression["operand"])
        if expr_type == "*handle_field_access*":
          operand = unary_expression["operand"]["expression"]
          if "field_access" in operand:
            primary_scope = self.create_primary_array(operand["field_access"], scope, scope_array)
            if primary_scope != ['global'] and primary_scope != []:
              # create new local scope for this variable
              primary_scope = self.get_primary_scope(primary_scope, operand['field_access'], scope, scope_array)
            else: primary_scope = scope_array

          var_id_num, var_type, is_field_var, var_info = self.get_var_from_scope(operand["field_access"]["id"], primary_scope)
          expr_type = var_type

        operator_to_string = { 
          "-": "uminus",
          "!": "neg",
          "+": "skip"
        }
        skip_flag = False
        if unary_expression["operator"] == "+":
          skip_flag = True

        operator = ""
        if unary_expression["operator"] in operator_to_string:
          operator = operator_to_string[unary_expression["operator"]]
        else:
          error(f"Line:{unary_expression['line_num']}:{unary_expression['col_num']}: Unrecognized unary operator: {unary_expression['operator']}")
        
        register = self.asm_stack.pop(0)
        if dtype.is_number_type(expr_type, scope):
          if operator != "uminus" and operator != "skip":
            expr_type = "error"
          self.asm += dcodegen.generate_negative(register, registers)
          self.asm_stack.insert(0, register)
        if dtype.is_boolean_type(expr_type, scope):
          if operator != "neg":
            expr_type = "error"
          global L_count
          dcodegen.generate_bit_flip(register, registers, L_count)
          self.asm_stack.insert(0, register)
          L_count += 1
        
        if skip_flag:
          return [expression, expr_type]

        output += f"Unary({expression}, {operator}, {expr_type})"
        return [output, expr_type]


    def evaluate_binary_expression(self, ast_binary, scope, scope_array):
        output = ""
        expr_type = ""
        if "binary_expression" not in ast_binary:
            # raise Exception("Could not find binary expression")
            error(f"Line{ast_binary['line_num']}:{ast_binary['col_num']}: Could not find binary expression")
      
        binary_expression = ast_binary["binary_expression"]
        if "left" not in binary_expression:
            # raise Exception("Could not find left operand")
            error(f"Line{binary_expression['line_num']}:{binary_expression['col_num']}: Could not find left operand")
        if "right" not in binary_expression:
            # raise Exception("Could not find right operand")
            error(f"Line{binary_expression['line_num']}:{binary_expression['col_num']}: Could not find right operand")
        if "operator" not in binary_expression:
            # raise Exception("Could not find operator")
            error(f"Line{binary_expression['line_num']}:{binary_expression['col_num']}: Could not find operator")
        left_expression, left_type = self.create_expression_record(binary_expression["left"], scope, scope_array)        
        right_expression, right_type = self.create_expression_record(binary_expression["right"], scope, scope_array)
        operator = binary_expression["operator"] 
        
        register_right = self.asm_stack.pop(0)
        register_left = self.asm_stack.pop(0)
        
        # rl_out, register_left = dcodegen.generate_expression(left_expression, self.asm_registers)
        # rr_out, register_right = dcodegen.generate_expression(right_expression, self.asm_registers)        
        # self.asm+=rl_out + rr_out

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

        operator_to_supertype = {
          "+": "float",
          "-": "float",
          "*": "float",
          "/": "float",
          "%": "float",
          "&&": "boolean",
          "||": "boolean",
          "==": "*",
          "!=": "*",
          "<": "float",
          ">": "float",
          "<=": "float",
          ">=": "float"
        }

        operator_return_bool = ["&&", "||", "==", "!=", "<", ">", "<=", ">="]

        if operator not in operator_to_string:
          # raise Exception("Invalid operator")
          error(f"Line{operator['line_num']}:{operator['col_num']}: Invalid operator")

        operator_type = operator_to_supertype[operator]
        boolean_expr = operator in operator_return_bool
        operator = operator_to_string[operator]

        if operator_type == "*":
          if dtype.is_subtype(scope, left_type, right_type) or dtype.is_subtype(scope, right_type, left_type):
            expr_type = "boolean"
          else:
            expr_type = "error"
        elif dtype.is_subtype(scope, right_type, operator_type) and dtype.is_subtype(scope, left_type, operator_type):
          if boolean_expr:
              expr_type = "boolean"
          elif right_type!=left_type:
            # find who has the super type
            if dtype.is_subtype(scope, right_type, left_type):
              expr_type = right_type
            else:
              expr_type = left_type
          else: 
            # if both are the same type, just pick one
            expr_type = left_type
        else:
          expr_type = "error"

        output += f"Binary({operator}, {left_expression}, {right_expression}, {expr_type})"
        global L_count
        asm_output, self.asm_registers, register_out = dcodegen.generate_binary_expression(ast_binary, L_count, self.asm_data, register_left, register_right, self.asm_registers, expr_type)
        L_count += 1
        self.asm_stack.insert(0, register_out)
        global bin_count
        self.asm_data[f"BINARY_EXPRESSION_{bin_count}"] = register_out
        self.asm += asm_output
        debug(f"Binary expression: {self.asm_stack}")
        return [output, expr_type]

    def evaluate_return(self, ast_return, scope, scope_array, return_type="void"):
      output = ""
      if "return" not in ast_return:
        # raise Exception("Could not find return")
        error(f"{ast_return['line_num']}:{ast_return['col_num']}: Could not find return")
      statement_eval, statement_type = self.create_expression_record(ast_return["return"], scope, scope_array)
      if not dtype.is_subtype(scope, statement_type, return_type):
        # debug(f"statement_type: {statement_type}, return_type: {return_type}")
        statement_type = "error"

      # return type will be equal to expression type
      output += f"Return({statement_eval}, {statement_type})"
      register_out = self.asm_stack.pop()
      self.asm += dcodegen.generate_return(register_out)
      return [output, statement_type]
    
    def evaluate_method_invo(self, ast_method_invo, local_scope, scope_array):
      output = ""
      if "field_access" not in ast_method_invo:
        # raise Exception("Could not find method field_access")
        error(f"Line:{ast_method_invo['line_num']}:{ast_method_invo['col_num']}: Could not find method field_access")
      if "arguments" not in ast_method_invo:
        # raise Exception("Could not find method arguments")
        error(f"Line:{ast_method_invo['line_num']}:{ast_method_invo['col_num']}: Could not find method arguments")
      method = ast_method_invo["field_access"]
      if "id" not in method:
        # raise Exception("Could not find method id")
        error(f"Line:{method['line_num']}:{method['col_num']}: Could not find method id ")
      if "primary" not in method:
        # raise Exception("Could not find method primary")
        error(f"Line:{method['line_num']}:{method['col_num']}: Could not find method primary")

      arguments = ast_method_invo["arguments"]
      arg_str = []
      for arg in arguments:
        arg_str.append(self.create_expression_record(arg, local_scope, scope_array)[0])
      arg_str = ", ".join(arg_str)
      primary, return_type, primary_id, method_info = self.evaluate_primary(method, local_scope, scope_array)
      prim_arr = primary.split(", ")
      return_type = self.create_type_record(return_type)
      global scope
      if prim_arr[0] in scope["global"]:
        if "static" in method_info["modifiers"]:
          prim_arr[0] = f"Class-Reference({prim_arr[0]})"
        else:
          prim_arr[0] = f"user({prim_arr[0]})"
      primary = ", ".join(prim_arr)
      output += f"Method-call({primary}, [{arg_str}], {method_info['id']}, {return_type})"
      # get the method label
      # debug(method_info)
      method_label = f"M_{method_info['signature']['name']}_{method_info['id_num']}"
      self.asm += dcodegen.generate_method_call(method_label)
      self.asm_stack.insert(0,"a0") # return value is in a0
      return [output, return_type]
    
    def evaluate_literal(self,ast_literal):
      output = ""
      literal_type = ""
      if "type" not in ast_literal:
        # raise Exception("Could not find literal type")
        error(f"Line:{ast_literal['line_num']}:{ast_literal['col_num']}: Could not find literal type")
      if "value" not in ast_literal:
        # raise Exception("Could not find literal value")
        error(f"Line:{ast_literal['line_num']}:{ast_literal['col_num']}: Could not find literal value")
      if ast_literal["type"] == "Boolean" or ast_literal["type"] == "Null":
        output += f"Constant({ast_literal['value']})"
      else:
        output += f"{ast_literal['type']}-Constant({ast_literal['value']})"
      literal_type = ast_literal["type"]
      
      value = -1
      is_float = False
      # debug(ast_literal)
      # determine literal value
      if ast_literal["type"] == "Integer":
        value = ast_literal['value']
      elif ast_literal["type"] == "Float":
        is_float = True
        value = ast_literal['value']
      elif ast_literal["type"] == "Boolean":
        if ast_literal['value'] == "true":
          value = 1
        else:
          value = 0
      
      asm_out, register_out = dcodegen.generate_literal(value, self.asm_registers, is_float)
      self.asm_stack.insert(0,register_out)
      self.asm += asm_out
      return [output, literal_type]
    
    def evaluate_new_object(self,ast_new_object, local_scope, scope_array):
      output = ""
      expr_type = ""
      arguments = ast_new_object["arguments"]
      arg_str = []
      arg_types = []
      for arg in arguments:
        arg_record, arg_type = self.create_expression_record(arg, local_scope, scope_array)
        arg_str.append(arg_record)
        arg_types.append(arg_type)
      arg_str = ", ".join(arg_str)

      matching_constructor_id = "-1"

      # do name resolution
      # find class name and check constructor signature
      type_name = f"user({ast_new_object['type']})"
      global scope

      if ast_new_object['type'] in scope["global"]:
        # need public?
        constructor_signatures = self.get_all_constructors(ast_new_object['type'], public_needed=self.is_public_needed(self.class_name, ast_new_object['type']))
        # now i have a list of all constructor signatures
        # create signature for new object
        new_object_signature = dtype.create_type_signature(ast_new_object['type'], arg_types)
        # compare the constructor signature
        found = 0
        for signature in constructor_signatures:
          if dtype.match_signature(signature, new_object_signature):
            matching_constructor_id = signature["id"]
            found = 1
            break
        if found == 0:
          type_name = "error"
      else:
        type_name = "error"

      output += f"New-object(Class-Reference({ast_new_object['type']}), [{arg_str}], {matching_constructor_id}, user({ast_new_object['type']}))"
      
      # move all arguments to a registers
      important_regs = []
      global type_table
      debug(new_object_signature)
      size = type_table[new_object_signature['name']]
      
      for i in range(len(arg_types)-1,-1,-1):
        reg = f"a{i}"
        self.asm += dcodegen.generate_move(reg, self.asm_stack.pop(0))
        important_regs.append(reg)
      
      self.asm += dcodegen.generate_initializer(important_regs, matching_constructor_id, self.asm_registers, size)
      return [output, type_name]
    
    def create_primary_array(self,ast_primary, local_scope, scope_array):
      primary = self.evaluate_primary(ast_primary, local_scope, scope_array)[0]
      primary_array = primary.split(", ")[:-1]
      return primary_array.copy()

    def get_primary_scope(self,primary_array, ast_primary, local_scope, scope_array):
      new_scope = ["global"]
      primary = primary_array.pop(0)
      global scope

      # check if primary array is empty
      if len(primary_array) == 0:
        if primary.lower() == "this":
          new_scope.append(self.class_name)
          new_scope.append("children")
          return new_scope
        elif primary.lower() == "super":
          new_scope.append(self.superclass_name)
          new_scope.append("children")
          return new_scope
        else:
          new_scope.append(primary)
          if primary in scope["global"]:
            if "children" in scope["global"][primary]:
              new_scope.append("children")
          else:
            if isinstance(primary, str):
              # try getting variable from scope
              variable = self.get_var_from_scope(primary, scope_array)
              new_scope = ["global"]
              # get variable type
              var_type = variable[1]
              if "user(" in var_type:
                var_type = var_type[5:-1]
              if "class(" in var_type:
                var_type = var_type[6:-1]
              if var_type in scope["global"]:
                new_scope.append(var_type)
                new_scope.append("children")
          return new_scope    

      # go through scope until primary_array is empty
      cont = True
      current_scope = scope["global"]
      while cont:
        if len(primary_array) == 0:
          cont = False
          continue
        searching_for = primary_array.pop(0)
        if "children" in current_scope:
          new_scope.append("children")
          current_scope = current_scope["children"]
        desired_super = False
        if primary.lower() == "this":
          primary = self.class_name
          new_scope.append(primary)
          new_scope.append("children")
          current_scope = current_scope[primary]["children"]
        elif primary.lower() == "super":
          desired_super = True
          primary = self.class_name
          new_scope.append(primary)
          new_scope.append("children")
          current_scope = current_scope[primary]["children"]
        else:
          if len(primary_array) > 1:
            if "children" in current_scope:
              new_scope.append("children")
              current_scope = current_scope["children"]
            else:
              if isinstance(current_scope, dict):
                if searching_for in current_scope:
                  new_scope.append(searching_for)
                  current_scope = current_scope[searching_for]
                  if "children" in current_scope:
                    new_scope.append("children")
                    current_scope = current_scope["children"]
                else:
                  error(f"Line:{ast_primary['line_num']}:{ast_primary['col_num']}: Could not find identifier in scope (1)")
              elif isinstance(current_scope, list):
                found = False
                for child in current_scope:
                  if searching_for in child:
                    new_scope.append(searching_for)
                    current_scope = child[searching_for]
                    if "children" in current_scope:
                      new_scope.append("children")
                      current_scope = current_scope["children"]
                    found = True
                if not found:
                  error(f"Line:{ast_primary['line_num']}:{ast_primary['col_num']}: Could not find identifier in scope (2)")
        primary = searching_for   
        
      
      if primary == "this":
        found = 0
        for child in scope["global"][self.class_name]["children"]:
          if ast_primary["id"] in child:
            primary_type = child[ast_primary["id"]]["type"]
            found = 1
        if found == 0:
          error(f"Line:{ast_primary['line_num']}:{ast_primary['col_num']}: Could not find identifier in scope (3)")

      elif primary == "super":
        found = 0
        for child in scope["global"][self.class_name]["children"]:
          if ast_primary["id"] in child:
            if child[ast_primary["id"]]["super"]:
              primary_type = child[ast_primary["id"]]["type"]
              found = 1
              # error(f"Line:{ast_primary['line_num']}:{ast_primary['col_num']}: Could not find identifier in scope")

        if found == 0:
          error(f"Line:{ast_primary['line_num']}:{ast_primary['col_num']}: Could not find identifier in scope (4)")

      elif primary == "":
        # warn(ast_primary["id"])
        # check local scope
        if isinstance(local_scope, list):
          for child in local_scope:
            if ast_primary["id"] in scope:
              if not child[ast_primary["id"]]["super"]:
                found = 1
        elif isinstance(local, dict):
          if ast_primary["id"] in scope:
            if not local_scope[ast_primary["id"]]["super"]:
              primary_type = child[ast_primary["id"]]["type"]
              found = 1
        if found==0:
          error(f"Line:{ast_primary['line_num']}:{ast_primary['col_num']}: Could not find identifier in scope (5)")
      else:
        # debug(primary)
        # check if primary is a class that exists in scope
        if primary not in scope["global"]:
          # debug(scope["global"])              
          # check if primary is a variable in scope
          var = self.get_var_from_scope(primary, scope_array)
          # get var type
          if var == None:
            error(f"Line:{ast_primary['line_num']}:{ast_primary['col_num']}: Could not find primary in scope")
          var_type = var[1]
          # remove user() from var_type
          if "user(" in var_type:
            var_type = var_type.replace("user(", "")[:-1]   
          elif "method" in var_type:
            warn("METHOD METHOD METHOD!!!!")
            # get id from method
            pass
          # find class in scope
          if var_type not in scope["global"]:
            error(f"Line:{ast_primary['line_num']}:{ast_primary['col_num']}: Could not find primary in scope")
          # check if class has children
          found = 0
          for child in scope["global"][var_type]["children"]:
            # check if class has child with id
            if ast_primary["id"] in child:
              found = 1
          if found == 0:
            error(f"Line:{ast_primary['line_num']}:{ast_primary['col_num']}: Could not find identifier in scope (6)")
        else:
          found = 0
          for child in scope["global"][primary]["children"]:
            if ast_primary["id"] in child:
              found = 1
          if found == 0:
            error(f"Line:{ast_primary['line_num']}:{ast_primary['col_num']}: Could not find identifier in scope (7)")
      return new_scope


    def evaluate_primary(self,ast_primary, local_scope, scope_array):
      output = ast_primary["id"]
      primary_type = ""
      is_field_var = False
      var_id = ""
      info_dump = None
      global scope
      if ast_primary["primary"] == "":
        # check class level scope, then local scope
        found = 0
        for child in scope["global"][self.class_name]["children"]:
          if ast_primary["id"] in child:
            primary_type = child[ast_primary["id"]]["type"]
            if primary_type == "method":
              primary_type = child[ast_primary["id"]]["return_type"]
            info_dump = child[ast_primary["id"]]
            found = 1
        # check local scope
        if isinstance(local_scope, list):
          for child in local_scope:
            if ast_primary["id"] in child:
              primary_type = child[ast_primary["id"]]["type"]
              info_dump = child[ast_primary["id"]]
              found = 1
        elif isinstance(local_scope, dict):
          if ast_primary["id"] in local_scope:
            primary_type = local_scope[ast_primary["id"]]["type"]
            info_dump = local_scope[ast_primary["id"]]
            found = 1
        # debug(output)
        # warn(local_scope)
        return [output, primary_type, ast_primary["id"], info_dump]

      if ast_primary["primary"] != "":
          primary = ast_primary["primary"]

          if "field_access" in primary:
              primary = self.evaluate_primary(primary["field_access"], scope, scope_array)
              info_dump = primary[3]
              primary = primary[0]
          # check if primary exists in scope
          primary_array = primary.split(", ")
          save_primary = primary_array.copy()
          
          output = ", ".join(save_primary)
          output += ", "
          output += ast_primary["id"]

          primary = primary_array.pop(0)
          # debug(primary)
          # go through scope until primary_array is empty
          cont = True
          current_scope = scope["global"]
          while cont:
            if len(primary_array) == 0:
              cont = False
              continue
            searching_for = primary_array.pop(0)
            desired_super = False
            if primary.lower() == "this":
              primary = self.class_name
              is_field_var = True
              current_scope = current_scope[primary]["children"]
            elif primary.lower() == "super":
              desired_super = True
              primary = self.class_name
              is_field_var = True
              current_scope = current_scope[primary]["children"]
            else:
              if len(primary_array) > 1:
                if "children" in current_scope:
                  current_scope = current_scope["children"]
                else:
                  if isinstance(current_scope, dict):
                    if searching_for in current_scope:
                      current_scope = current_scope[searching_for]
                    else:
                      primary_type = "error"
                      debug(f"Line:{ast_primary['line_num']}:{ast_primary['col_num']}: Could not find identifier in scope (8)")
                      return [output, primary_type, ast_primary["id"], None]
                  elif isinstance(current_scope, list):
                    found = False
                    for child in current_scope:
                      if searching_for in child:
                        current_scope = child[searching_for]
                        found = True
                    if not found:
                      debug(f"Line:{ast_primary['line_num']}:{ast_primary['col_num']}: Could not find identifier in scope (9)")
                      primary_type = "error"
                      return [output, primary_type, ast_primary["id"], None]

            primary = searching_for   
            
          if primary == "this":
            found = 0
            for child in scope["global"][self.class_name]["children"]:
              if ast_primary["id"] in child and "static" not in child[ast_primary["id"]]["modifiers"]:
                primary_type = child[ast_primary["id"]]["type"]
                info_dump = child[ast_primary["id"]]
                if primary_type == "method": 
                    # get return type of method
                    primary_type = child[ast_primary["id"]]["return_type"]
                is_field_var = True
                found = 1
            if found == 0:
              debug(f"Line:{ast_primary['line_num']}:{ast_primary['col_num']}: Could not find identifier in scope (10)")
              primary_type = "error"
              return [output, primary_type, ast_primary["id"], None]

          elif primary == "super":
            found = 0
            for child in scope["global"][self.class_name]["children"]:
              if ast_primary["id"] in child:
                if child[ast_primary["id"]]["super"] and "static" not in child[ast_primary["id"]]["modifiers"]:
                  primary_type = child[ast_primary["id"]]["type"]
                  info_dump = child[ast_primary["id"]]
                  if primary_type == "method": 
                    # get return type of method
                    primary_type = child[ast_primary["id"]]["return_type"]
                  is_field_var = True
                  found = 1

            if found == 0:
              primary_type = "error"
              debug(f"Line:{ast_primary['line_num']}:{ast_primary['col_num']}: Could not find identifier in scope (11)")
              return [output, primary_type, ast_primary["id"], None]

          elif primary == "":
            # check local scope
            if isinstance(local_scope, list):
              for child in local_scope:
                if ast_primary["id"] in child:
                  if not child[ast_primary["id"]]["super"]:
                    primary_type = child[ast_primary["id"]]["type"]
                    info_dump = child[ast_primary["id"]]
                    if primary_type == "method": 
                      # get return type of method
                      primary_type = child[ast_primary["id"]]["return_type"]
                    found = 1
            elif isinstance(local, dict):
              if ast_primary["id"] in child:
                if not local_scope[ast_primary["id"]]["super"]:
                  primary_type = child[ast_primary["id"]]["type"]
                  info_dump = child[ast_primary["id"]]
                  if primary_type == "method": 
                    # get return type of method
                    primary_type = child[ast_primary["id"]]["return_type"]
                  found = 1
            if found==0:
              debug(f"Line:{ast_primary['line_num']}:{ast_primary['col_num']}: Could not find identifier in scope (12)")
              primary_type = "error"
              return [output, primary_type, ast_primary["id"], None]
          else:
            # debug(primary)
            # check if primary is a class that exists in scope
            if primary not in scope["global"]:
              # check if primary is a variable in scope
              var = self.get_var_from_scope(primary, scope_array)
              var_id = var[0]
              # get var type
              if var == None:
                debug(f"Line:{ast_primary['line_num']}:{ast_primary['col_num']}: Could not find primary in scope")
                primary_type = "error"
                return [output, primary_type, ast_primary["id"], None]
              var_type = var[1]
              if var[2] == "field":
                is_field_var = True
              primary_type = var_type
              info_dump = var[3]
              # remove user() from var_type
              if "user(" in var_type:
                var_type = var_type.replace("user(", "")[:-1]   
              # elif "method" in var_type:
              #   # get id from method
              #   pass
              # find class in scope
              if var_type not in scope["global"]:
                debug(f"Line:{ast_primary['line_num']}:{ast_primary['col_num']}: Could not find primary in scope")
                primary_type = "error"
                return [output, primary_type, ast_primary["id"], None]
              # check if class has children
              found = 0
              for child in scope["global"][var_type]["children"]:
                # check if class has child with id
                # not static because it is a variable i just parsed
                if ast_primary["id"] in child and "static" not in child[ast_primary["id"]]["modifiers"]:
                  primary_type = child[ast_primary["id"]]["type"]
                  info_dump = child[ast_primary["id"]]
                  if primary_type == "method": 
                    # get return type of method
                    primary_type = child[ast_primary["id"]]["return_type"]
                  found = 1
              if found == 0:
                debug(f"Line:{ast_primary['line_num']}:{ast_primary['col_num']}: Could not find identifier in scope (13)")                      
                primary_type = "error"
                return [output, primary_type, ast_primary["id"], None]
            else:
              found = 0
              # primary is a class, not var. can only be static to be valid
              for child in scope["global"][primary]["children"]:
                if ast_primary["id"] in child and "static" in child[ast_primary["id"]]["modifiers"]:
                  primary_type = child[ast_primary["id"]]["type"]
                  info_dump = child[ast_primary["id"]]
                  is_field_var = True
                  if primary_type == "method": 
                    # get return type of method
                    primary_type = child[ast_primary["id"]]["return_type"]
                  found = 1
              if found == 0:
                debug(f"Line:{ast_primary['line_num']}:{ast_primary['col_num']}: Could not find identifier in scope (14)")
                primary_type = "error"
                return [output, primary_type, ast_primary["id"], None]

          if "this" == primary or "super" == primary:
              is_field_var = True
              primary = primary.title()

          output = ", ".join(save_primary)
          output += ", "
          output += ast_primary["id"]
      return [output, primary_type, ast_primary["id"], info_dump]

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
            # raise Exception("Invalid scope layer traversal: Could not find scope layer")
            error(f"Could not find scope layer at {scope_layer}")
        elif isinstance(new_scope, dict):
            if scope_layer in new_scope:
                new_scope = new_scope[scope_layer]
            else:
              # raise Exception(f"Could not find scope layer: {scope_layer} in {new_scope}")
              error(f"Could not find scope layer: {scope_layer} in {new_scope}")
        else:
          # raise Exception("Invalid scope layer traversal")
          error(f"Invalid scope layer traversal at {new_scope}, {scope_layer}")
      return new_scope

    def add_to_scope(self, local_scope, scope_array, variable_id, variable):
        # check local scope first
        self.check_current_scope(local_scope, variable_id, {variable_id: variable})

        # traverse global scope to find if the variable is already defined
        global scope
        legal_types = ["class", "method", "constructor"]
        
        if scope_array == []:
            scope_array = ["global"]
        test_scope = scope
        for scope_layer in scope_array:
          if isinstance(test_scope, list):
            for scope_item in test_scope:
              if variable_id in scope_item:
                if variable["type"] == scope_item[variable_id]["type"] and scope_item[variable_id]["var_type"] == variable["var_type"] and scope_item[variable_id]["super"]:
                  # raise Exception(f"Variable already defined: {variable_id}")
                  error(f"Line:{variable['line_num']}:{variable['col_num']}: Variable already defined: {variable_id}")
                # if scope[type] is not a class, method, or constructor, and variable is not a class, method, or constructor
                # then they are both variables with the same name, which is not allowed
                if scope_item[variable_id]["type"] not in legal_types and variable["type"] not in legal_types:
                    # do not raise exception if one is a field var and the other is a local
                    if scope_item[variable_id]["var_type"] == variable["var_type"]:
                    # raise Exception(f"Variable already defined: {variable_id}")
                      error(f"Line:{variable['line_num']}:{variable['col_num']}: Variable already defined: {variable_id}")
          else:
            if variable_id in test_scope:
                if variable["type"] == test_scope[variable_id]["type"] and scope_item[variable_id]["var_type"] == variable["var_type"]:
                    # raise Exception("Variable already defined")
                    error(f"Line{variable['line_num']}:{variable['col_num']}: Variable already defined: {variable_id}")
                # if scope[type] is not a class, method, or constructor, and variable is not a class, method, or constructor
                # then they are both variables with the same name, which is not allowed
                if test_scope[variable_id]["type"] not in legal_types and variable["type"] not in legal_types:
                    if scope_item[variable_id]["var_type"] == variable["var_type"]:
                    # raise Exception(f"Variable already defined: {variable_id}")
                      error(f"Line:{variable['line_num']}:{variable['col_num']}: Variable already defined: {variable_id}")
                    # error(f"Variable already defined: {variable_id} at line:{variable['line_num']}:{variable['col_num']}")
          test_scope = self.traverse_scope_layer(test_scope, [scope_layer])
        
        if isinstance(local_scope, list):
          local_scope.append({variable_id: variable})
        else:
          local_scope[variable_id] = variable
        return local_scope
        
    # returns [id_num, type, var_type]
    def get_var_from_scope(self, variable_name, scope_array, class_var=0):
        global scope
        if scope_array == []:
            scope_array = ["global"] 

        possible_return = None

        test_scope = scope
        illegal_types = ["class", "method", "constructor"]
        for scope_layer in scope_array:
            test_scope = self.traverse_scope_layer(test_scope, [scope_layer])
            # debug(f"searching for {variable_name} in {scope_array}, in layer {test_scope}")
            if isinstance(test_scope, list):
              for scope_item in test_scope:
                if variable_name in scope_item:
                    if scope_item[variable_name]["type"] in illegal_types:
                      continue
                    possible_return = [scope_item[variable_name]["id_num"], scope_item[variable_name]["type"], scope_item[variable_name]["var_type"], scope_item[variable_name]]
            else:
              if variable_name in test_scope:
                if test_scope[variable_name]["type"] in illegal_types:
                  continue
                possible_return = [test_scope[variable_name]["id_num"], test_scope[variable_name]["type"], test_scope[variable_name]["var_type"], test_scope[variable_name]]
                # return [test_scope[variable_name]["id_num"], test_scope[variable_name]["type"], test_scope[variable_name]["var_type"]]
        if possible_return == None:
          error(f"Variable not found: {variable_name} in {scope_array}")
        return possible_return

    def check_current_scope(self, scope, id_, item):
      for scope_item in scope:
        if id_ in scope_item:
          if compare_var(scope_item[id_],item[id_]):
            error(f"Line:{item[id_]['line_num']}:{item[id_]['col_num']} Variable already defined: {id_}")
      return scope

    def is_public_needed(self, class_name, class_needed):
      if class_name == class_needed:
        return False
      global scope
      superclass = scope["global"][class_name]["superclass_name"]
      while superclass != "":
        if superclass == class_needed:
          return False
        superclass = scope["global"][superclass]["superclass_name"]
      return True

    def get_all_constructors(self, class_name, public_needed=True):
      if class_name in scope["global"]:
      # get all constructor signatures

        def get_obj_name(x: dict):
          return list(x.keys())[0]
      
        # object is nested like {name: {type: "constructor"}} but I don't know name. Get name, check constructor, return signature
        constructor_signatures = [child[get_obj_name(child)]["signature"] for child in scope["global"][class_name]["children"] if child[get_obj_name(child)]["type"] == "constructor" and (not public_needed or "public" in child[get_obj_name(child)]["modifiers"])]
        # debug(f"constructor signatures: {constructor_signatures}")
        return constructor_signatures
      return []




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
    # writeJSON("ast.json", [x.ast for x in ast_blocks if isinstance(x, AST)])
    # global scope
    # debug(scope) 
    return print_ast_blocks(ast_blocks)

def print_ast_blocks(ast_blocks):
    big_asm = ""
    output = "-----------------------------------------------\n"
    for ast in ast_blocks:
        if ast == None:
            continue
        out, asm = ast.print_ast()
        output += out
        big_asm += asm
        output += "-----------------------------------------------\n"
    # dabsmc.write_asm("output.asm", big_asm)
    global static_count
    big_asm = f".static_data {static_count}\n{big_asm}"
    return output, big_asm

# extraction functions

def extract_body(ast):
    if "body" not in ast:
        raise Exception("Could not find body")
    global field_count, method_count, class_count, class_overall_count
    ast["id_num"] = class_overall_count
    class_overall_count += 1
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
            # raise Exception("Could not find field, method, or constructor")
            error(f"Could not find field, method, or constructor at line:{['line_num']}:{['col_num']}")
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
            item['parameter']['var_type'] = 'local'
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
    ast['field']['col_num'] = ast['field']['variables']['col_num']
    ast['field']['line_num'] = ast['field']['variables']['line_num']
    del ast['field']['variables']
    return ast

def compare_var(obj1,obj2):
  if obj1 == obj2:
    return True
  if isinstance(obj1, dict) and isinstance(obj2, dict):
    if "type" not in obj1 or "type" not in obj2:
      return False
    if obj1["type"] != obj2["type"]:
      return False
    if "id" not in obj1 or "id" not in obj2:
      return False
    if obj1["id"] != obj2["id"]:
      return False
    if "var_type" not in obj1 or "var_type" not in obj2:
      return False
    if obj1["var_type"] != obj2["var_type"]:
      return False
    return True
  return False

def extract_var_type(var):
  var['var_type'] = "local"
  global var_count
  variable_declarations = {}
  for id_name in var['ids']:
    variable_declarations[var_count] = var.copy()
    variable_declarations[var_count]['id'] = id_name
    del variable_declarations[var_count]['ids']
    var_count += 1
  var = variable_declarations
  return var

def set_var_count(x):
  global var_count
  var_count = x