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
      cmd_str = f"source venv/bin/activate && python3 src/decaf_checker.py {file} > /dev/null 2>&1"
      process = subprocess.Popen(cmd_str, shell=True, stderr=subprocess.PIPE)
      process.wait()
      self.assertNotEqual(process.returncode, 0, f"{file} succeeded to compile")


  
if __name__ == '__main__':
    unittest.main(argv=[''],verbosity=0)
