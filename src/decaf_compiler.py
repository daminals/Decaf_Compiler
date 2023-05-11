# decaf_parser.py
# Daniel Kogan dkogan 114439349
# 02.21.2023

import sys
import ply.lex as lex
import ply.yacc as yacc

GREEN = '\033[92m'
CLEAR_FORMAT = '\033[0m'

import decaf_lexer
import decaf_parser
import decaf_ast
import decaf_absmc as dabsmc
import predefined_classes as predef


def just_scan(fn=""):
    if fn == "":
        print("Missing file name for source program.")
        print("USAGE: python3 decaf_checker.py <decaf_source_file_name>")
        sys.exit()
    lexer = lex.lex(module = decaf_lexer, debug = 0)

    fh = open(fn, 'r')
    source = fh.read()
    fh.close()
    lexer.input(source)
    next_token = lexer.token()
    while next_token != None:
        print(next_token)
        next_token = lexer.token()
# end def just_scan()


def just_parse(fn=""):
    if fn == "":
        print("Missing file name for source program.")
        print("USAGE: python3 decaf_checker.py <decaf_source_file_name>")
        sys.exit()
    lexer = lex.lex(module = decaf_lexer, debug = 0)
    parser = yacc.yacc(module = decaf_parser, debug = 0)

    fh = open(fn, 'r')
    source = fh.read()
    fh.close()
    result = []
    result.insert(0, decaf_ast.AST(predef.out_class, predef.out_class["body"]["fields"], predef.out_class["body"]["methods"], predef.out_class["body"]["constructors"]))
    result.insert(0, decaf_ast.AST(predef.in_class, predef.in_class["body"]["fields"], predef.in_class["body"]["methods"], predef.in_class["body"]["constructors"]))
    result += parser.parse(source, lexer = lexer, debug = 0)
    ast, asm = decaf_ast.writeAST(result)
    # Parsing Successful
    print(ast)
    dabsmc.write_asm(fn, asm)
    print(GREEN+ "YES" + CLEAR_FORMAT)
    #print()

def main():
    fn = sys.argv[1] if len(sys.argv) > 1 else ""
    just_scan(fn) # lexer
    fn = sys.argv[1] if len(sys.argv) > 1 else ""
    just_parse(fn) # parser

def compile(fn=""):
    just_scan(fn) # lexer
    just_parse(fn) # parser

if __name__ == "__main__":
  main()