import unittest, sys, os
import subprocess

class TestDecafFiles(unittest.TestCase):
    def run_file(file, expected_return_code=0):
      cmd_str = f"source venv/bin/activate && python3 src/decaf_checker.py {file}"
      process = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      stdout, stderr = process.communicate()
      err_message = f"{file} exited with return code {process.returncode}, not {expected_return_code}"
      self.assertEqual(expected_return_code, process.returncode, err_message)
      return stdout, stderr

    def test_hello_world(self):
      file = "rsrc/hello_world.decaf"
      stdout, stderr = TestDecafFiles.run_file(file)
      self.assertIn("YES", stdout.decode())

    def test_IntList(self):
      file = "rsrc/IntList.decaf"
      stdout, stderr = TestDecafFiles.run_file(file)
      self.assertIn("YES", stdout.decode())

    def test_nrfib(self):
      file = "rsrc/nrfib.decaf"
      stdout, stderr = TestDecafFiles.run_file(file)
      self.assertIn("YES", stdout.decode())

    def test_rfib(self):
      file = "rsrc/rfib.decaf"
      stdout, stderr = TestDecafFiles.run_file(file)
      self.assertIn("YES", stdout.decode())

    def test_failure(self):
      file = "rsrc/failure.decaf"
      stdout, stderr = TestDecafFiles.run_file(file,1)
      self.assertIn("Syntax error at line 8, column 3, token: this'", stdout.decode(), f"{file} did not throw syntax err @ line 8, column 3")
    
    def test_unexpectedEOF(self):
      file = "rsrc/unexpectedEOF.decaf"
      stdout, stderr = TestDecafFiles.run_file(file,1)
      self.assertIn("Syntax error: unexpected end of input", stdout.decode(), f"{file} reached unexpected EOF")

    def test_unexpectedEOF(self):
      file = "rsrc/unexpectedEOF.decaf"
      stdout, stderr = TestDecafFiles.run_file(file,1)
      self.assertIn("Syntax error: unexpected end of input", stdout.decode(), f"\n{file} succeeded to compile")

    def test_Cat(self):
      file = "rsrc/Cat.decaf"
      stdout, stderr = TestDecafFiles.run_file(file)
      self.assertIn("YES", stdout.decode())

if __name__ == '__main__':
    unittest.main(argv=[''],verbosity=0)
