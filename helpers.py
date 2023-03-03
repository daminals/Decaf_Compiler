# helpers.py
# Daniel Kogan
# 03.02.2023

import unittest
import sys
import os
import subprocess

GREEN = '\033[92m'
RED = '\033[91m'
UNDERLINE = '\033[4m'
CLEAR_FORMAT = '\033[0m'

class Runner():
  def run_file(testcase_class, file, expected_return_code=0):
    cmd_str = f"python src/decaf_checker.py {file}"
    process = subprocess.Popen(
        cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    err_message = f"{RED}{file}{CLEAR_FORMAT} {UNDERLINE}exited with return code {process.returncode}, not {expected_return_code}{CLEAR_FORMAT}\n {GREEN}Output:{CLEAR_FORMAT} {stdout}\n\n {RED}Error:{CLEAR_FORMAT} {stderr}"
    # print(f"{GREEN}{file}{CLEAR_FORMAT}: {stdout}")
    testcase_class.assertEqual(
        expected_return_code, process.returncode, err_message)
    return stdout, stderr

  def syntax_err_msg(line_col):
    line, column = line_col
    return f"Syntax error at line {line}, column {column}"