Decaf Compiler - A04

By: 
  - Daniel Kogan dkogan 114439349

Python Version: 3.9.6
Ply Version: 3.11

Fixes:
  - Precedence
    - Binary expressions are now evaluated with the correct precedence
    - Assignment of variable ID - all variables now have unique identifiers per method and constructor

Installation
  - Install Python 3.9.6
  - Install PLY 3.11
    - Run the following command in the terminal:
      pip3 install ply

How to Run:
  - Run the following command in the terminal:
    python3 decaf_parser_.py <input_file>

  - The program will output the following:
    - On success, the program will exit with the following:
      - Abstract Syntax Tree (AST) printed to stdout
      - "YES" in green text to stdout
      - Return code: 0
    - On failure, the program will exit with the following:
      - "ERROR: {error_message}" in highlighted red text to stderr
      - Return code: 1

  - The program will also output the following files:
    - parser.out
    - parsetab.py

Contents of Submitted Files:

1. decaf_parser.py
  - Applied fixes to precedence and variable ids

2. decaf_ast.py
  - Reformatted outputs of AST class functions to return array: [string_output, type]
  - Improved name resolution by returning found object in primary
  - Implemented type signatures for constructors and methods
  - Implemented Class-Reference-Expression

3. decaf_typechecker.py
  - Added type checking for binary expressions
  - Added functions for detecting subtypes
  - Added functions to create and compare type signatures
  - Added functions for detecting type compatibility

4. decaf_lexer.py
  - No change

5. predefined_classes.py
  - No change

6. decaf_checker.py
  - No change

7. debug.py 
  - Debug features to highlight control flow in the code

========================================================
================ A03 SUBMISSION README =================
========================================================

Decaf Compiler - A03
By: 
  - Daniel Kogan dkogan 114439349

Python Version: 3.9.6
Ply Version: 3.11

Fixes:
  - Fixed failing test case from AO2
    - The test case was failing because we put int above float, meaning floats would not get accounted for

Installation
  - Install Python 3.9.6
  - Install PLY 3.11
    - Run the following command in the terminal:
      pip3 install ply

How to Run:
  - Run the following command in the terminal:
    python3 decaf_parser_.py <input_file>

  - The program will output the following:
    - On success, the program will exit with the following:
      - Abstract Syntax Tree (AST) printed to stdout
      - "YES" in green text to stdout
      - Return code: 0
    - On failure, the program will exit with the following:
      - "ERROR: {error_message}" in highlighted red text to stderr
      - Return code: 1

  - The program will also output the following files:
    - parser.out
    - parsetab.py

Contents of Submitted Files:

1. decaf_parser.py
  - Added output definitions for each grammar expression to create a dictionary of the AST

2. decaf_ast.py
  - Added AST class to represent a decaf class
    - Includes the following attributes:
      - class_name: the name of the class
      - superclass_name: the parent class of the class
      - fields: a list of fields in the class
      - methods: a list of methods in the class
      - constructors: a list of constructors in the class
      - ast: dictionary of the AST
    - Includes the following methods:
      - create_record(): creates a record of the class
      - create_field_record(): creates a record of a field
      - create_method_record(): creates a record of a method
      - create_constructor_record(): creates a record of a constructor
      - create_block_record(): creates a record of a block (statement list)
      - create_type_record(): creates a record of a type
      - create_variable_record(): creates a record of a variable
      - create_modifiers_list(): creates a string of modifiers
      - create_modifiers_list_PRIVATE_PUBLIC(): creates a string of modifiers for private and public exclusively
      - create_statement_record(): creates a record of a statement 
      - create_variable_declaration_record(): creates a record of a variable declaration
      - create_assignment_record(): creates a record of an assignment
      - create_expression_record(): creates a record of an expression
      - evaluate_auto(): evaluates a postfix expression
      - evaluate_if_block(): evaluates an if block
      - evaluate_while_block(): evaluates a while block
      - evaluate_for_block(): evaluates a for block
      - evaluate_return_block(): evaluates a return block
      - evaluate_unary_expression(): evaluates a unary expression
      - evaluate_binary_expression(): evaluates a binary expression
      - evaluate_method_invo(): evaluates a method call
      - evaluate_literal(): evaluates a literal
      - evaluate_new_object(): evaluates a new object
      - evaluate_primary(): evaluates a primary expression
      - traverse_scope_layer(): traverses a scope layer
      - add_to_scope(): adds a variable to a scope
      - get_var_from_scope(): gets a variable from a scope
      - create_current_scope(): creates a new scope
  - debug(): prints a debug statement
  - warn(): prints a warning statement
  - error(): prints an error statement and exits the program
  - writeJSON(): writes a dictionary to a JSON file
  - readJSON(): reads a JSON file and returns a dictionary
  - writeAST(): prints the AST to stdout
  - print_ast_blocks(): Creates a string of AST blocks
  - HELPER FUNCTIONS
    - extract_body(): extracts the body to rearrage elements of AST for readability
    - extract_variables_from_formals(): extracts variable information from formals to create consistent layout
    - extract_variables_from_field(): extracts variable information from field to create consistent layout
    - compare_var(): compares two variables to see if they are the same
3. predefined_classes.py
  - Created predefined classes for in and out to add them to scope
4. decaf_lexer.py
  - Correction implemented as stated in #fixes section 
5. decaf_checker.py
  - Added predefined classes
  - Turned off debug mode


========================================================
================ A02 SUBMISSION README =================
========================================================


Decaf Compiler - A02
By: 
  - Daniel Kogan dkogan 114439349
  - Jason Zhang jasozhang 112710259

Python Version: 3.9.6
Ply Version: 3.11

Installation
  - Install Python 3.9.6
  - Install PLY 3.11
    - Run the following command in the terminal:
      pip3 install ply

How to Run:
  - Run the following command in the terminal:
    python3 decaf_parser_.py <input_file>

  - The program will output the following:
    - On success, the program will exit with the following:
      - "YES" in green text to stdout
      - Return code: 0
    - On failure, the program will exit with the following:
      - "ERROR: {error_message}" in red text to stdout
      - Return code: 1

  - The program will also output the following files:
    - parser.out
    - parsetab.py

Limitations:

- Similar to what Professor Kane mentioned in class where in Python, errors at the end of a line are often times mislabeled as errors on the next line, within a string such as "hello \" world", since the specifications mention a string is anything between double quotes excluding a double quote, the parser will throw an error on 'world' instead of the illegal " character

Contents of Submitted Files:

1. decaf_lexer_.py
 - Contains the lexer for the Decaf language
 - Includes all reserved keywords and tokens
   - Defined keywords and tokens
      - t_COMMA: a comma (,)
      - t_DOT: a period or dot (.)
      - t_AND: a logical AND operator (&&)
      - t_BOOLEAN: the boolean type keyword (boolean)
      - t_BREAK: the keyword for breaking out of a loop (break)
      - t_CLASS: the keyword for defining a class (class)
      - t_CONTINUE: the keyword for skipping to the next iteration of a loop (continue)
      - t_DIVIDE: the division operator (/)
      - t_DO: the keyword for starting a do-while loop (do)
      - t_ELSE: the keyword for defining an alternative condition (else)
      - t_EQUAL: the equality operator (==)
      - t_EXTENDS: the keyword for specifying inheritance (extends)
      - t_FOR: the keyword for starting a for loop (for)
      - t_GREATER: the greater than operator (>)
      - t_GREATEREQ: the greater than or equal to operator (>=)
      - t_IF: the keyword for defining a conditional statement (if)
      - t_INT: the integer type keyword (int)
      - t_LBRACKET: the left square bracket ([)
      - t_LCURLY: the left curly brace or bracket ({)
      - t_LESS: the less than operator (<)
      - t_LESSEQ: the less than or equal to operator (<=)
      - t_LPAREN: the left parenthesis (()
      - t_MINUSMINUS: the decrement operator (--)
      - t_MINUS: the subtraction operator (-)
      - t_NEW: the keyword for creating a new object (new)
      - t_NOT: the logical NOT operator (!)
      - t_NOTEQUAL: the inequality operator (!=)
      - t_NULL: the keyword for representing a null value (null)
      - t_OR: the logical OR operator (||)
      - t_PLUSPLUS: the increment operator (++)
      - t_PLUS: the addition operator (+)
      - t_PRIVATE: the keyword for declaring a member as private (private)
      - t_PUBLIC: the keyword for declaring a member as public (public)
      - t_RBRACKET: the right square bracket (])
      - t_RCURLY: the right curly brace or bracket (})
      - t_RETURN: the keyword for returning a value from a function (return)
      - t_RPAREN: the right parenthesis ())
      - t_SEMICOLON: the semicolon (;)
      - t_SETEQUAL: the assignment operator (=)
      - t_STATIC: the keyword for declaring a member as static (static)
      - t_STRING: the string type keyword (string)
      - t_SUPER: the keyword for accessing the parent class (super)
      - t_THIS: the keyword for accessing the current object (this)
      - t_TIMES: the multiplication operator (*)
      - t_VOID: the void type keyword (void)
      - t_WHILE: the keyword for starting a while loop (while)

2. decaf_parser_.py
  - Defines grammar expressions for the Decaf language
    - start
    - class
    - class_body
    - field_decl
    - modifier
    - var_decl
    - type
    - variables
    - variable
    - method_decl
    - constructor
    - formals
    - formals_param
    - block
    - stmtlist
    - stmt
    - literal
    - primary
    - arg
    - lhs
    - field
    - method_invo
    - expr
    - assign
    - arith_op
    - bool_op
    - unary_op
    - stmt_expr
    - empty
    - error