Decaf Compiler - A02

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