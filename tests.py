# tests.py
# Daniel Kogan
# 03.02.2023

import unittest
import sys
import os
import subprocess
from helpers import Runner
from helpers import GREEN, RED, UNDERLINE, CLEAR_FORMAT


class TestDecafFiles(unittest.TestCase):
    folder = f"rsrc"

    def test_hello_world(self):
        file = f"{self.folder}/hello_world.decaf"
        stdout, stderr = Runner.run_file(self, file)
        self.assertIn("YES", stdout.decode())

    def test_IntList(self):
        file = f"{self.folder}/IntList.decaf"
        stdout, stderr = Runner.run_file(self, file)
        self.assertIn("YES", stdout.decode())

    def test_nrfib(self):
        file = f"{self.folder}/nrfib.decaf"
        stdout, stderr = Runner.run_file(self, file)
        self.assertIn("YES", stdout.decode())

    def test_rfib(self):
        file = f"{self.folder}/rfib.decaf"
        stdout, stderr = Runner.run_file(self, file)
        self.assertIn("YES", stdout.decode())

    def test_Cat(self):
        file = f"{self.folder}/Cat.decaf"
        stdout, stderr = Runner.run_file(self, file)
        self.assertIn("YES", stdout.decode())

    def test_multiply(self):
        file = f"{self.folder}/multiply.decaf"
        stdout, stderr = Runner.run_file(self, file)
        self.assertIn("YES", stdout.decode())

    def test_CelsiusToFahrenheit(self):
        file = f"{self.folder}/CelsiusToFahrenheit.decaf"
        stdout, stderr = Runner.run_file(self, file)
        self.assertIn("YES", stdout.decode())

    def test_Bicycle(self):
        file = f"{self.folder}/Bicycle.decaf"
        stdout, stderr = Runner.run_file(self, file)
        self.assertIn("YES", stdout.decode())

    def test_Lamp(self):
        file = f"{self.folder}/Lamp.decaf"
        stdout, stderr = Runner.run_file(self, file)
        self.assertIn("YES", stdout.decode())

    def test_empty_file(self):
        file = f"{self.folder}/empty_file.decaf"
        stdout, stderr = Runner.run_file(self, file, 0)
        self.assertIn("YES", stdout.decode())

    def test_runningAvgCalc(self):
        file = f"{self.folder}/runningAvgCalc.decaf"
        stdout, stderr = Runner.run_file(self, file)
        self.assertIn("YES", stdout.decode())

    def test_MultiLineComments(self):
        file = f"{self.folder}/MultiLineComments.decaf"
        stdout, stderr = Runner.run_file(self, file)
        self.assertIn("YES", stdout.decode())


class TestDecafFilesExpectErr(unittest.TestCase):
    folder = "rsrc/fail"

    def test_unexpectedEOF(self):
        file = f"{self.folder}/unexpectedEOF.decaf"
        stdout, stderr = Runner.run_file(self, file, 1)
        self.assertIn("Syntax error: unexpected end of input",
                      stdout.decode(), f"\n{file} succeeded to compile")

    def test_failure(self):
        file = f"{self.folder}/failure.decaf"
        stdout, stderr = Runner.run_file(self, file, 1)
        self.assertIn("Syntax error at line 8, column 3, token: this'", stdout.decode(
        ), f"{file} did not throw syntax err @ line 8, column 3")

    def test_IllegalString(self):
        file = f"{self.folder}/IllegalString.decaf"
        stdout, stderr = Runner.run_file(self, file, 1)
        self.assertIn("Syntax error at line 10, column 30", stdout.decode(
        ), f"{file} did not throw syntax err @ line 10, column 30")


if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=0)
