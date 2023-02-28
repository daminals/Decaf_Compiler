![github repo badge: Language](https://img.shields.io/badge/Language-Python-181717?color=blue) ![github repo badge: Compiling](https://img.shields.io/badge/Compiling-Decaf-181717?color=orange) [![Unit Tests](https://github.com/TyuiX/CSE307HW2/actions/workflows/action.yaml/badge.svg)](https://github.com/TyuiX/CSE307HW2/actions/workflows/action.yaml)
# Decaf Compiler

This is a simple implementation of a Decaf Compiler using PLY (Python Lex-Yacc) tool for parsing and lexical analysis in Python.

## Prerequisites

You need to have Python 3.x installed on your machine. PLY is a third-party tool that needs to be installed separately. You can install it using pip.

```bash
pip3 install -r requirements.txt
```

## Usage

You can run the Decaf compiler by executing the decaf_compiler.py script. The script reads input code from a file and outputs the result to the console.

```bash
python decaf_compiler.py input_file.decaf
```

The input file should contain the Decaf code that you want to compile.

## Features

- Supports basic arithmetic operations (+, -, *, /)
- Supports comparison operators (<, <=, >, >=, ==, !=)
- Supports boolean operations (&&, ||, !)
- Supports if-else statements and while loops
- Supports integer and boolean literals
- Supports variable declaration and assignment
- Supports function declaration and calling
- Supports arrays and array indexing
- Supports error handling for invalid input
- Supports the Decaf syntax and semantics

## Implementation

The Decaf compiler is implemented in Python using the PLY tool. PLY provides a lexer and parser generator that can be used to build compilers and interpreters. The lexer and parser are defined in separate files (decaf_lexer.py and decaf_parser.py) and are then imported into the main script (decaf_compiler.py). The lexer reads the input code and converts it into tokens, which are then passed to the parser. The parser uses the tokens to build an abstract syntax tree (AST) that represents the input code. The AST is then used to generate the output code.

## Credits

This project was created by Daniel Kogan and Jason Zheng as a part of CSE 304 - Compiler Design at Stony Brook University.
