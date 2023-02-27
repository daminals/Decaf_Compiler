# decaf_parser.py
# Daniel Kogan 114439349
# Jason Zhang 112710259
# 02.21.2023
import sys
import ply.lex as lex
import ply.yacc as yacc

import decaf_lexer
import decaf_parser


def just_scan(fn=""):
    if fn == "":
        print("Missing file name for source program.")
        print("USAGE: python3 decaf_checker.py <decaf_source_file_name>")
        sys.exit()
    lexer = lex.lex(module = decaf_lexer, debug = 1)

    fh = open(fn, 'r')
    source = fh.read()
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
    lexer = lex.lex(module = decaf_lexer, debug = 1)
    parser = yacc.yacc(module = decaf_parser, debug = 1)

    fh = open(fn, 'r')
    source = fh.read()
    fh.close()
    try:
        result = parser.parse(source, lexer = lexer, debug = 1)
        print(result)
    except SyntaxError:
        print("error occured while parsing")
    # Parsing Successful
    #print()
    print("YES")
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