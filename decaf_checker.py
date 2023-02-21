

import sys
import ply.lex as lex
import ply.yacc as yacc

def just_scan():
    fn = sys.argv[1] if len(sys.argv) > 1 else ""
    if fn == "":
        print("Missing file name for source program.")
        print("USAGE: python3 decaf_checker.py <decaf_source_file_name>")
        sys.exit()
    import decaf_lexer
    lexer = lex.lex(module = decaf_lexer, debug = 1)

    fh = open(fn, 'r')
    source = fh.read()
    lexer.input(source)
    next_token = lexer.token()
    while next_token != None:
        print(next_token)
        next_token = lexer.token()
# end def just_scan()


def main():
    fn = sys.argv[1] if len(sys.argv) > 1 else ""
    if fn == "":
        print("Missing file name for source program.")
        print("USAGE: python3 decaf_checker.py <decaf_source_file_name>")
        sys.exit()
    import decaf_lexer
    import decaf_parser
    lexer = lex.lex(module = decaf_lexer, debug = 1)
    parser = yacc.yacc(module = decaf_parser, debug = 1)

    fh = open(fn, 'r')
    source = fh.read()
    fh.close()
    result = parser.parse(source, lexer = lexer, debug = 1)
    #print(result)
    # Parsing Successful
    #print()
    print("YES")
    #print()

if __name__ == "__main__":
    just_scan()
    main()
