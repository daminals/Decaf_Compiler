import json,sys
debug_mode = False

CLEAR_FORMAT = '\033[0m'
BOLD_FORMAT = '\033[1m'
UNDERLINE_FORMAT = '\033[4m'
RED_FORMAT = '\033[91m'
GREEN_FORMAT = '\033[92m'
YELLOW_FORMAT = '\033[93m'
BLUE_FORMAT = '\033[94m'
PURPLE_FORMAT = '\033[95m'
CYAN_FORMAT = '\033[96m'
WHITE_FORMAT = '\033[97m'

def debug(string):
  global debug_mode
  if not debug_mode:
    return
  PURPLE = '\033[95mDEBUG: '
  CLEAR_COLOR = '\033[0m\n'
  if isinstance(string, dict):
    print(PURPLE + json.dumps(string, indent=4, default=str) + CLEAR_COLOR)
  elif isinstance(string, list):
    # check if each item is dict
    str_list = []
    for item in string:
      if isinstance(item, dict):
        str_list.append(json.dumps(item, indent=4, default=str))
      else: 
        str_list.append(str(item))
    print(PURPLE + '\n=========================================\n'.join(str_list) + CLEAR_COLOR)
  else: 
    print(PURPLE + str(string) + CLEAR_COLOR)

def warn(string):
  global debug_mode
  if not debug_mode:
    return
  YELLOW = '\033[93mWARN: '
  CLEAR_COLOR = '\033[0m'
  print(YELLOW + str(string) + CLEAR_COLOR)

def error(string):
  RED = '\033[91m'
  CLEAR_COLOR = '\033[0m'
  print(f"{RED}ERROR:{CLEAR_COLOR} {string}", file=sys.stderr)
  # raise SyntaxError()
  exit(1)