import unittest, sys, os
from src import decaf_checker

class TestDecafFiles(unittest.TestCase):
    def test_0(self):
      self.assertEqual(FileNotFoundError, decaf_checker.compile("rsrc/hello_world.decaf"))
  

if __name__ == '__main__':
    unittest.main(argv=[''],verbosity=0)
