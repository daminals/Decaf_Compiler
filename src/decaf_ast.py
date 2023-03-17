import json


def writeJSON(filename, data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent=2)
    return True

def readJSON(filename):
    with open(filename, 'r') as infile:
        data = json.load(infile)
    return data

def writeAST(ast_block):
  print(ast_block)
  writeJSON("ast.json", ast_block)