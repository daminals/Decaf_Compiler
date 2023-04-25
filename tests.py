# tests.py
# Daniel Kogan
# 03.02.2023

import unittest
import sys
import os
import subprocess
from helpers import Runner
from helpers import GREEN, RED, UNDERLINE, CLEAR_FORMAT

def generate_tests(num_tests):
    test_cases = []
    for i in range(1, num_tests+1):
        class TestFunc(unittest.TestCase):
            def test_func(self):
                filename = f"test{i:03d}"
                file = f"{self.folder}/{filename}.decaf"
                stdout, stderr = Runner.run_file(self, file, 0)
                self.assertIn("YES", stdout.decode("utf-8"))

        test_cases.append(TestFunc)

    suite = unittest.TestSuite()
    for test_case in test_cases:
        suite.addTests(unittest.makeSuite(test_case))
    return suite

generate_tests(num_tests=41)


class TestDecafFiles(unittest.TestCase):
    folder = f"rsrc/hw2_testing"

    def test_hello_world(self):
        file = f"{self.folder}/hello_world.decaf"
        stdout, stderr = Runner.run_file(self, file)
        self.assertIn("YES", stdout.decode("utf-8"))

    def test_threeclass_decaf(self):
        filename = "threeclass"
        file = f"{self.folder}/{filename}.decaf"
        stdout, stderr = Runner.run_file(self, file, 0)
        self.assertIn("YES", stdout.decode("utf-8"))

    def test_IntList(self):
        file = f"{self.folder}/IntList.decaf"
        stdout, stderr = Runner.run_file(self, file)
        self.assertIn("YES", stdout.decode("utf-8"))

    def test_nrfib(self):
        file = f"{self.folder}/nrfib.decaf"
        stdout, stderr = Runner.run_file(self, file)
        self.assertIn("YES", stdout.decode("utf-8"))

    def test_rfib(self):
        file = f"{self.folder}/rfib.decaf"
        stdout, stderr = Runner.run_file(self, file)
        self.assertIn("YES", stdout.decode("utf-8"))

    def test_Cat(self):
        file = f"{self.folder}/Cat.decaf"
        stdout, stderr = Runner.run_file(self, file)
        self.assertIn("YES", stdout.decode("utf-8"))

    def test_multiply(self):
        file = f"{self.folder}/multiply.decaf"
        stdout, stderr = Runner.run_file(self, file)
        self.assertIn("YES", stdout.decode("utf-8"))

    def test_CelsiusToFahrenheit(self):
        file = f"{self.folder}/CelsiusToFahrenheit.decaf"
        stdout, stderr = Runner.run_file(self, file)
        self.assertIn("YES", stdout.decode("utf-8"))

    def test_Bicycle(self):
        file = f"{self.folder}/Bicycle.decaf"
        stdout, stderr = Runner.run_file(self, file)
        self.assertIn("YES", stdout.decode("utf-8"))

    def test_Lamp(self):
        file = f"{self.folder}/Lamp.decaf"
        stdout, stderr = Runner.run_file(self, file)
        self.assertIn("YES", stdout.decode("utf-8"))

    def test_empty_file(self):
        file = f"{self.folder}/empty_file.decaf"
        stdout, stderr = Runner.run_file(self, file, 0)
        self.assertIn("YES", stdout.decode("utf-8"))

    def test_runningAvgCalc(self):
        file = f"{self.folder}/runningAvgCalc.decaf"
        stdout, stderr = Runner.run_file(self, file)
        self.assertIn("YES", stdout.decode("utf-8"))

    def test_MultiLineComments(self):
        file = f"{self.folder}/MultiLineComments.decaf"
        stdout, stderr = Runner.run_file(self, file)
        self.assertIn("YES", stdout.decode("utf-8"))


class TestDecafFilesExpectErr(unittest.TestCase):
    folder = "rsrc/fail"

    def test_unexpectedEOF(self):
        file = f"{self.folder}/unexpectedEOF.decaf"
        stdout, stderr = Runner.run_file(self, file, 1)
        self.assertIn("Syntax error: unexpected end of input",
                      stderr.decode(), f"\n{file} succeeded to compile")

    def test_failure(self):
        file = f"{self.folder}/failure.decaf"
        stdout, stderr = Runner.run_file(self, file, 1)
        line_col = [8, 3]  # line, column
        self.assertIn(Runner.syntax_err_msg(line_col), stderr.decode(
        ), f"{file} did not throw syntax err @ line {line_col[0]}, column {line_col[1]}")

    def test_IllegalString(self):
        file = f"{self.folder}/IllegalString.decaf"
        stdout, stderr = Runner.run_file(self, file, 1)
        line_col = [10, 30]  # line 10, column 30
        self.assertIn(Runner.syntax_err_msg(line_col), stderr.decode(
        ), f"{file} did not throw syntax err @ line {line_col[0]}, column {line_col[1]}")


class TestHW2(unittest.TestCase):
    folder = "rsrc/hw2_testing/class_tests"

    def test_1_decaf(self):
        file = f"{self.folder}/1.decaf"
        stdout, stderr = Runner.run_file(self, file, 0)
        self.assertIn("YES", stdout.decode("utf-8"))

    def test_2_decaf(self):
        file = f"{self.folder}/2.decaf"
        stdout, stderr = Runner.run_file(self, file, 0)
        self.assertIn("YES", stdout.decode("utf-8"))

    def test_3_decaf(self):
        file = f"{self.folder}/3.decaf"
        stdout, stderr = Runner.run_file(self, file, 0)
        self.assertIn("YES", stdout.decode("utf-8"))

    def test_4_decaf(self):
        filename = "4"
        file = f"{self.folder}/{filename}.decaf"
        stdout, stderr = Runner.run_file(self, file, 0)
        self.assertIn("YES", stdout.decode("utf-8"))

    def test_5_decaf(self):
        filename = "5"
        file = f"{self.folder}/{filename}.decaf"
        stdout, stderr = Runner.run_file(self, file, 0)
        self.assertIn("YES", stdout.decode("utf-8"))

    def test_6_decaf(self):
        filename = "6"
        file = f"{self.folder}/{filename}.decaf"
        stdout, stderr = Runner.run_file(self, file, 0)
        self.assertIn("YES", stdout.decode("utf-8"))

    # def test_7_decaf(self):
    #     filename = "7"
    #     file = f"{self.folder}/{filename}.decaf"
    #     stdout, stderr = Runner.run_file(self, file, 0)
    #     self.assertIn("YES", stdout.decode("utf-8"))

    def test_8_decaf(self):
        filename = "8"
        file = f"{self.folder}/{filename}.decaf"
        stdout, stderr = Runner.run_file(self, file, 0)
        self.assertIn("YES", stdout.decode("utf-8"))

    def test_9_decaf(self):
        filename = "9"
        file = f"{self.folder}/{filename}.decaf"
        stdout, stderr = Runner.run_file(self, file, 0)
        self.assertIn("YES", stdout.decode("utf-8"))

    def test_10_decaf(self):
        filename = "10"
        file = f"{self.folder}/{filename}.decaf"
        stdout, stderr = Runner.run_file(self, file, 0)
        self.assertIn("YES", stdout.decode("utf-8"))

    def test_11_decaf(self):
        filename = "11"
        file = f"{self.folder}/{filename}.decaf"
        stdout, stderr = Runner.run_file(self, file, 0)
        self.assertIn("YES", stdout.decode("utf-8"))

    def test_12_decaf(self):
        filename = "12"
        file = f"{self.folder}/{filename}.decaf"
        stdout, stderr = Runner.run_file(self, file, 0)
        self.assertIn("YES", stdout.decode("utf-8"))

    def test_13_decaf(self):
        filename = "13"
        file = f"{self.folder}/{filename}.decaf"
        stdout, stderr = Runner.run_file(self, file, 0)
        self.assertIn("YES", stdout.decode("utf-8"))

    def test_14_decaf(self):
        filename = "14"
        file = f"{self.folder}/{filename}.decaf"
        stdout, stderr = Runner.run_file(self, file, 0)
        self.assertIn("YES", stdout.decode("utf-8"))

    def test_15_decaf(self):
        filename = "15"
        file = f"{self.folder}/{filename}.decaf"
        stdout, stderr = Runner.run_file(self, file, 0)
        self.assertIn("YES", stdout.decode("utf-8"))

    def test_16_decaf(self):
        filename = "16"
        file = f"{self.folder}/{filename}.decaf"
        stdout, stderr = Runner.run_file(self, file, 0)
        self.assertIn("YES", stdout.decode("utf-8"))

    def test_17_decaf(self):
        filename = "17"
        file = f"{self.folder}/{filename}.decaf"
        stdout, stderr = Runner.run_file(self, file, 0)
        self.assertIn("YES", stdout.decode("utf-8"))

    def test_18_decaf(self):
        filename = "18"
        file = f"{self.folder}/{filename}.decaf"
        stdout, stderr = Runner.run_file(self, file, 0)
        self.assertIn("YES", stdout.decode("utf-8"))

    def test_19_decaf(self):
        filename = "19"
        file = f"{self.folder}/{filename}.decaf"
        stdout, stderr = Runner.run_file(self, file, 0)
        self.assertIn("YES", stdout.decode("utf-8"))

    def test_20_decaf(self):
        filename = "20"
        file = f"{self.folder}/{filename}.decaf"
        stdout, stderr = Runner.run_file(self, file, 0)
        self.assertIn("YES", stdout.decode("utf-8"))

    def test_21_decaf(self):
        filename = "21"
        file = f"{self.folder}/{filename}.decaf"
        stdout, stderr = Runner.run_file(self, file, 0)
        self.assertIn("YES", stdout.decode("utf-8"))

    def test_22_decaf(self):
        filename = "22"
        file = f"{self.folder}/{filename}.decaf"
        stdout, stderr = Runner.run_file(self, file, 0)
        self.assertIn("YES", stdout.decode("utf-8"))

    def test_23_decaf(self):
        filename = "23"
        file = f"{self.folder}/{filename}.decaf"
        stdout, stderr = Runner.run_file(self, file, 0)
        self.assertIn("YES", stdout.decode("utf-8"))

    # def test_24_decaf(self):
    #     filename = "24"
    #     file = f"{self.folder}/{filename}.decaf"
    #     stdout, stderr = Runner.run_file(self, file, 0)
    #     self.assertIn("YES", stdout.decode("utf-8"))

    # def test_25_decaf(self):
    #     filename = "25"
    #     file = f"{self.folder}/{filename}.decaf"
    #     stdout, stderr = Runner.run_file(self, file, 0)
    #     self.assertIn("YES", stdout.decode("utf-8"))

    def test_26_decaf(self):
        filename = "26"
        file = f"{self.folder}/{filename}.decaf"
        stdout, stderr = Runner.run_file(self, file, 0)
        self.assertIn("YES", stdout.decode("utf-8"))

    # def test_27_decaf(self):
    #     filename = "27"
    #     file = f"{self.folder}/{filename}.decaf"
    #     stdout, stderr = Runner.run_file(self, file, 0)
    #     self.assertIn("YES", stdout.decode("utf-8"))

    def test_28_decaf(self):
        filename = "28"
        file = f"{self.folder}/{filename}.decaf"
        stdout, stderr = Runner.run_file(self, file, 0)
        self.assertIn("YES", stdout.decode("utf-8"))

    # failing test cases: expected failure

    def test_err1(self):
        filename = "err1"
        file = f"{self.folder}/{filename}.decaf"
        stdout, stderr = Runner.run_file(self, file, 1)
        self.assertIn("Syntax error: unexpected end of input",
                      stderr.decode(), f"\n{file} succeeded to compile")

    def test_err2(self):
        filename = "err2"
        # 1 is invalid ID for classname
        file = f"{self.folder}/{filename}.decaf"
        stdout, stderr = Runner.run_file(self, file, 1)
        line_col = [1, 7]  # line 1, column 7
        self.assertIn(Runner.syntax_err_msg(line_col), stderr.decode(
        ), f"{file} did not throw syntax err @ line {line_col[0]}, column {line_col[1]}")

    def test_err3(self):
        filename = "err3"        
        # does not contain a ID for the function parameter
        file = f"{self.folder}/{filename}.decaf"
        stdout, stderr = Runner.run_file(self, file, 1)
        line_col = [2, 9]  # line 2, column 10
        self.assertIn(Runner.syntax_err_msg(line_col), stderr.decode(
        ), f"{file} did not throw syntax err @ line {line_col[0]}, column {line_col[1]}")

    def test_err4(self):
        filename = "err4"
        # does not contain class
        file = f"{self.folder}/{filename}.decaf"
        stdout, stderr = Runner.run_file(self, file, 1)
        line_col = [1, 1]  # line 1, column 1
        self.assertIn(Runner.syntax_err_msg(line_col), stderr.decode(
        ), f"{file} did not throw syntax err @ line {line_col[0]}, column {line_col[1]}")

    def test_err5(self):
        filename = "err5"
        # does not have closing )
        file = f"{self.folder}/{filename}.decaf"
        stdout, stderr = Runner.run_file(self, file, 1)
        line_col = [3, 1]  # line 2, column 9
        self.assertIn(Runner.syntax_err_msg(line_col), stderr.decode(
        ), f"{file} did not throw syntax err @ line {line_col[0]}, column {line_col[1]}")

    def test_err6(self):
        filename = "err6"
        # can not assign and declar var in same line
        file = f"{self.folder}/{filename}.decaf"
        stdout, stderr = Runner.run_file(self, file, 1)
        line_col = [2, 8]  # line 2, column 8
        self.assertIn(Runner.syntax_err_msg(line_col), stderr.decode(
        ), f"{file} did not throw syntax err @ line {line_col[0]}, column {line_col[1]}")
                          
    # multi error

    def test_multierr1(self):
        filename = "multierr1"
        # will detect ) missing first before missing }
        file = f"{self.folder}/{filename}.decaf"
        stdout, stderr = Runner.run_file(self, file, 1)
        line_col = [3, 7]  # line 3, column 10
        self.assertIn(Runner.syntax_err_msg(line_col), stderr.decode(
        ), f"{file} did not throw syntax err @ line {line_col[0]}, column {line_col[1]}")

    def test_multierr2(self):
        filename = "multierr2"
        # will detect ( missing first before extraenous )
        file = f"{self.folder}/{filename}.decaf"
        stdout, stderr = Runner.run_file(self, file, 1)
        line_col = [3, 8]  # line 3, column 10
        self.assertIn(Runner.syntax_err_msg(line_col), stderr.decode(
        ), f"{file} did not throw syntax err @ line {line_col[0]}, column {line_col[1]}")

class TestHW3(unittest.TestCase):
  folder = "rsrc/hw3_testing/class_tests"
  # def setUp(self):
  #     self.generate_tests(41)

  # errors

  def test_error1(self):
    filename = "error01"
    file = f"{self.folder}/{filename}.decaf"
    stdout, stderr = Runner.run_file(self, file, 1)
    self.assertIn("\x1b[91mERROR:\x1b[0m Line:", stderr.decode(
    ), f"{file} did not throw syntax err")
  
  def test_error2(self):
    filename = "error02"
    file = f"{self.folder}/{filename}.decaf"
    stdout, stderr = Runner.run_file(self, file, 1)
    self.assertIn("\x1b[91mERROR:\x1b[0m Line:", stderr.decode(
    ), f"{file} did not throw syntax err")
  
  def test_error3(self):
    filename = "error03"
    file = f"{self.folder}/{filename}.decaf"
    stdout, stderr = Runner.run_file(self, file, 1)
    self.assertIn("\x1b[91mERROR:\x1b[0m Line:", stderr.decode(
    ), f"{file} did not throw syntax err")
  
  # passing

  # def test_001_decaf(self):
  #   filename = "test001"
  #   file = f"{self.folder}/{filename}.decaf"
  #   stdout, stderr = Runner.run_file(self, file, 0)
  #   self.assertIn("YES", stdout.decode("utf-8"))

  # def test_002_decaf(self):
  #   filename = "test002"
  #   file = f"{self.folder}/{filename}.decaf"
  #   stdout, stderr = Runner.run_file(self, file, 0)
  #   self.assertIn("YES", stdout.decode("utf-8"))

  # def test_003_decaf(self):
  #   filename = "test003"
  #   file = f"{self.folder}/{filename}.decaf"
  #   stdout, stderr = Runner.run_file(self, file, 0)
  #   self.assertIn("YES", stdout.decode("utf-8"))

  # def test_004_decaf(self):
  #   filename = "test004"
  #   file = f"{self.folder}/{filename}.decaf"
  #   stdout, stderr = Runner.run_file(self, file, 0)
  #   self.assertIn("YES", stdout.decode("utf-8"))
  
  # def test_005_decaf(self):
  #   filename = "test005"
  #   file = f"{self.folder}/{filename}.decaf"
  #   stdout, stderr = Runner.run_file(self, file, 0)
  #   self.assertIn("YES", stdout.decode("utf-8"))
  
  # def test_006_decaf(self):
  #   filename = "test006"
  #   file = f"{self.folder}/{filename}.decaf"
  #   stdout, stderr = Runner.run_file(self, file, 0)
  #   self.assertIn("YES", stdout.decode("utf-8"))
  
  # # repeat until test 42
  # def generate_tests(self, num_tests):
  #   for i in range(1, num_tests + 1):
  #       func_name = f"test_{i:03d}_decaf"
  #       func_content = f"""
  #           filename = "test{i:03d}"
  #           file = f"{{self.folder}}/{{filename}}.decaf"
  #           stdout, stderr = Runner.run_file(self, file, 0)
  #           self.assertIn("YES", stdout.decode("utf-8"))
  #       """
  #       func_def = f"def {func_name}(self):{func_content}"
  #       exec(func_def)
  def test_001_decaf(self):
    filename = "test001"
    file = f"{self.folder}/{filename}.decaf"
    stdout, stderr = Runner.run_file(self, file, 0)
    self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_002_decaf(self):
      filename = "test002"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_003_decaf(self):
      filename = "test003"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_004_decaf(self):
      filename = "test004"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_005_decaf(self):
      filename = "test005"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_006_decaf(self):
      filename = "test006"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_007_decaf(self):
      filename = "test007"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_008_decaf(self):
      filename = "test008"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_009_decaf(self):
      filename = "test009"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_010_decaf(self):
      filename = "test010"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_011_decaf(self):
      filename = "test011"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_012_decaf(self):
      filename = "test012"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_013_decaf(self):
      filename = "test013"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_014_decaf(self):
      filename = "test014"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_015_decaf(self):
      filename = "test015"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_016_decaf(self):
      filename = "test016"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_017_decaf(self):
      filename = "test017"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_018_decaf(self):
      filename = "test018"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_019_decaf(self):
      filename = "test019"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_020_decaf(self):
      filename = "test020"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_021_decaf(self):
      filename = "test021"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_022_decaf(self):
      filename = "test022"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_023_decaf(self):
      filename = "test023"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_024_decaf(self):
      filename = "test024"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_025_decaf(self):
      filename = "test025"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_026_decaf(self):
      filename = "test026"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_027_decaf(self):
      filename = "test027"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_028_decaf(self):
      filename = "test028"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_029_decaf(self):
      filename = "test029"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_030_decaf(self):
      filename = "test030"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_031_decaf(self):
      filename = "test031"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_032_decaf(self):
      filename = "test032"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_033_decaf(self):
      filename = "test033"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_034_decaf(self):
      filename = "test034"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_035_decaf(self):
      filename = "test035"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_036_decaf(self):
      filename = "test036"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_037_decaf(self):
      filename = "test037"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  def test_038_decaf(self):
      filename = "test038"
      file = f"{self.folder}/{filename}.decaf"
      stdout, stderr = Runner.run_file(self, file, 0)
      self.assertIn("YES", stdout.decode("utf-8"))
          
  # def test_generate_tests(self):
  #   self.generate_tests(41)



# if __name__ == '__main__':
#     unittest.main(argv=[''], verbosity=0)