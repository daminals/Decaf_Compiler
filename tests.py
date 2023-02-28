import unittest, sys, os
import subprocess

class TestDecafFiles(unittest.TestCase):

    def test_hello_world(self):
      file = "rsrc/hello_world.decaf"
      cmd_str = f"source venv/bin/activate && python3 src/decaf_checker.py {file} > /dev/null 2>&1"
      result = os.system(cmd_str)
      self.assertEqual(0, result, f"{file} failed to compile")

    def test_IntList(self):
      file = "rsrc/IntList.decaf"
      cmd_str = f"source venv/bin/activate && python3 src/decaf_checker.py {file} > /dev/null 2>&1"
      result = os.system(cmd_str)
      self.assertEqual(0, result, f"{file} failed to compile")

    def test_nrfib(self):
      file = "rsrc/nrfib.decaf"
      cmd_str = f"source venv/bin/activate && python3 src/decaf_checker.py {file} > /dev/null 2>&1"
      result = os.system(cmd_str)
      self.assertEqual(0, result, f"{file} failed to compile")

    def test_rfib(self):
      file = "rsrc/rfib.decaf"
      cmd_str = f"source venv/bin/activate && python3 src/decaf_checker.py {file} > /dev/null 2>&1"
      result = os.system(cmd_str)
      self.assertEqual(0, result, f"{file} failed to compile")

    # def test_failure(self):
    #   file = "rsrc/failure.decaf"
    #   cmd_str = f"source venv/bin/activate && python3 src/decaf_checker.py {file} > /dev/null 2>&1"
    #   result = os.system(cmd_str)
    #   self.assertEqual(1, result, f"{file} succeeded to compile")

    def test_failure(self):
        file = "rsrc/failure.decaf"
        cmd_str = f"source venv/bin/activate && python3 src/decaf_checker.py {file}"
        process = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        self.assertEqual(1, process.returncode, f"{file} succeeded to compile")
        self.assertIn("Syntax error at line 8, column 3, token: this'", stderr.decode(), f"{file} succeeded to compile")
    
    def test_unexpectedEOF(self):
        file = "rsrc/unexpectedEOF.decaf"
        cmd_str = f"source venv/bin/activate && python3 src/decaf_checker.py {file}"
        process = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        self.assertEqual(1, process.returncode, f"{file} succeeded to compile")
        self.assertIn("Syntax error: unexpected end of input", stderr.decode(), f"\n{file} succeeded to compile")


  
if __name__ == '__main__':
    unittest.main(argv=[''],verbosity=0)
