import os
import subprocess
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import main


class TestPrinterQueue(unittest.TestCase):
    def test_lpstat_jobs_parsed(self):
        fake = subprocess.CompletedProcess(["lpstat", "-o"], 0, "printer1-1 user 1024\n", "")
        with mock.patch("main.shutil.which", return_value="/usr/bin/lpstat"), \
             mock.patch("main.subprocess.run", return_value=fake), \
             mock.patch("main.platform.system", return_value="Linux"):
            r = main.check_queue()
        self.assertTrue(r["available"])
        self.assertEqual(len(r["jobs"]), 1)

    def test_no_tool_reports_honest_fallback(self):
        with mock.patch("main.shutil.which", return_value=None), \
             mock.patch("main.platform.system", return_value="Linux"):
            r = main.check_queue()
        self.assertFalse(r["available"])
        self.assertTrue(r["manual_steps"])
        self.assertNotIn("jobs", r)


if __name__ == "__main__":
    unittest.main()
