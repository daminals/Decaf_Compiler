# decaf_ast.py
# Daniel Kogan dkogan 114439349
# 04.17.2023

import json
field_count = 1
method_count = 1
class_count = 1
var_count = 1
valid_types = ["int", "boolean", "string", "float", "double", "char"]
user_defined_types = []

class AST:

    def __init__(self, ast):
        self.ast = ast
        self.printed = self.create_record(self.ast)

    def __init__(self, ast, fields, methods, constructors):
        self.ast = ast
        self.fields = fields
        self.methods = methods
        self.constructors = constructors
        self.printed = self.create_record(self.ast)


    def print_ast(self):
        return self.printed

    def create_record(self, ast):
        output = ""
        global user_defined_types
        # Check class name
        if "class_name" not in ast:
            raise Exception("Could not find class name")
        if ast["class_name"] == "":
            raise Exception("Class name is empty")

        self.class_name = ast["class_name"]
        output += f"Class Name: {self.class_name}\n"
        # class name is now a valid type as it has been declared
        user_defined_types.append(ast["class_name"])

        # Check super class
        if "superclass" not in ast:
            raise Exception("Could not find class name")
        self.superclass_name = ast["superclass"]
        output += f"Superclass: {self.superclass_name}\n"

        # Check fields
        if "fields" not in ast["body"]:
            raise Exception("Could not find fields")
        self.fields = ast["body"]["fields"]
        output += self.create_field_record()

        # check constructors
        if "constructors" not in ast["body"]:
            raise Exception("Could not find constructors")
        self.constructors = ast["body"]["constructors"]
        output += self.create_constructor_record()

        # check methods
        if "methods" not in ast["body"]:
            raise Exception("Could not find methods")
        self.methods = ast["body"]["methods"]
        output += self.create_method_record()
        return output

    def create_field_record(self):
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
            # name
            if "ids" not in field:
                raise Exception("Could not find field name")
            field_names = field["ids"]
            # type
            if "type" not in field:
                raise Exception("Could not find field type")
            field_type = self.create_type_record(field["type"])
            # modifiers
            if "modifiers" not in field:
                raise Exception("Could not find field modifiers")
            field_modifiers = self.create_modifiers_list(field["modifiers"])
            for field_name in field_names:
                output += f"FIELD {field_id}, {field_name}, {self.class_name}, {field_modifiers}, {field_type}\n"
        return output

    def create_constructor_record(self):
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
            constructor = self.constructors[constructor_id]

            # modifiers
            if "modifiers" not in constructor:
                raise Exception("Could not find field modifiers")
            constructor_modifiers = self.create_modifiers_list_PRIVATE_PUBLIC(
                constructor["modifiers"])

            output += f"CONSTRUCTOR: {constructor_id}, {constructor_modifiers}\n"
            output += "Constructor Parameters:\n"

            output += "Variable Table:\n"
            for variable_id in constructor["formals"].keys():
                variable = constructor["formals"][variable_id]
                output += self.create_variable_record(variable_id, variable)
        return output

    def create_method_record(self):
        output = "Methods:\n"
        for method_id in self.methods.keys():
            method = self.methods[method_id]
            # name
            method_name = method["function_id"]
            # type
            method_type = self.create_type_record(method["type"], 1)
            # modifiers
            method_modifiers = self.create_modifiers_list(method["modifiers"])
            output += f"METHOD: {method_id}, {method_name}, {self.class_name}, {method_modifiers}, {method_type}\n"
            output += "Method Parameters:\nVariable Table:\n"
            for variable_id in method["formals"].keys():
                variable = method["formals"][variable_id]
                output += self.create_variable_record(variable_id, variable)
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

    def create_statement_record(self, ast_statement):
        pass

    def create_assignment_record(self, ast_assignment):
        if "setequal" not in ast_assignment:
            raise Exception("Could not find assignment")

        output = ""
        assignment = ast_assignment["setequal"]
        operand = assignment["assign"]

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
    # print(ast_blocks)

    # output = print_ast_blocks(ast_blocks)
    # print(output)


def print_ast_blocks(ast_blocks):
    output = "-----------------------------------------------\n"
    all_asts = []
    for ast in ast_blocks:
        current_ast = AST(ast)
        all_asts.append(current_ast)
        output += current_ast.print_ast()
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
            fields[field_count] = item['field']
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
