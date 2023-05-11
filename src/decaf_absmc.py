# decaf_absmc.py
# Daniel Kogan
# 05.10.2023
from debug import *

def write_asm(filename, asm):
  """ 
  :param filename: the name of the file to write the assembly code to
  :param ast: the AST to generate assembly code for
  :return: None
  """
  used_registers = []
  filename = filename.split("/")[-1]
  # remove .decaf extension
  filename = filename.split(".")[0]
  filename += ".ami"
  if debug_mode:
    filename = f"asm/{filename}"
  with open(filename, "w") as f:
    f.write(asm)
    f.close()
  return
  
