"""Durable regression tests for envcheck.py (stdlib unittest only).

Run from the repo root:  python -m unittest test_envcheck -v
"""
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "envcheck.py"


def run_envcheck(directory):
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(directory)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )


def write_case(tmpdir, example_lines, env_lines):
    d = Path(tmpdir)
    (d / ".env.example").write_text(example_lines, encoding="utf-8")
    (d / ".env").write_text(env_lines, encoding="utf-8")
    return d


class TestEnvcheckCLI(unittest.TestCase):
    def test_missing_var_exits_1_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = write_case(tmp, "FOO=\nBAR=xxx\n", "BAR=xxx\n")
            proc = run_envcheck(d)
            self.assertEqual(proc.returncode, 1)
            self.assertIn("missing", proc.stdout)
            self.assertIn("FOO", proc.stdout)

    def test_clean_env_exits_0_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = write_case(tmp, "FOO=\nBAR=xxx\n", "FOO=1\nBAR=xxx\n")
            proc = run_envcheck(d)
            self.assertEqual(proc.returncode, 0)
            self.assertIn("required vars present", proc.stdout)


if __name__ == "__main__":
    unittest.main()
