"""Fail-closed calibration tests; mocked cargo output is never VTI native evidence."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "experiments/vti-task-size-admission/run.py"
spec = importlib.util.spec_from_file_location("vti_size_admission", SOURCE)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
ONE_PASS = "running 1 test\ntest example ... ok\ntest result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 7 filtered out;\n"
ONE_FAIL = "running 1 test\ntest example ... FAILED\ntest result: FAILED. 0 passed; 1 failed; 0 ignored; 0 measured; 7 filtered out;\n"


class TaskSizeEvidenceTests(unittest.TestCase):
    def test_exact_separate_pin_and_real_native_filters(self):
        self.assertEqual("9d781a7333a198ef24ec229f59ff8fbcae3b1346", runner.TARGET_SHA)
        self.assertNotEqual("49f5f1beb61adc34bdf7cf0bd3eb10f594415b80", runner.TARGET_SHA)
        self.assertEqual(5, len(runner.SCENARIOS))
        self.assertEqual(5, len({s[0] for s in runner.SCENARIOS}))
        self.assertEqual({"RAHP-1174"}, {s[1] for s in runner.SCENARIOS})
        for _, _, pkg, test, kind in runner.SCENARIOS:
            cmd = runner.command(pkg, test, kind)
            self.assertIn("--locked", cmd)
            self.assertEqual(test, cmd[-1])

    def test_wrong_pin_and_dirty_target_are_refused(self):
        with tempfile.TemporaryDirectory() as d:
            with patch.object(runner, "git", return_value="0" * 40):
                with self.assertRaisesRegex(ValueError, "qualified"):
                    runner.admit(Path(d))
            with patch.object(runner, "git", side_effect=[runner.TARGET_SHA, "modified"]):
                with self.assertRaisesRegex(ValueError, "tracked"):
                    runner.admit(Path(d))

    def test_false_success_is_never_counted_as_native_pass(self):
        for output in ("", "test result: ok. 0 passed; 0 failed; 0 ignored;",
                       "test result: ok. 2 passed; 0 failed; 0 ignored;"):
            self.assertEqual("ATTEMPTED_UNAVAILABLE", runner.classify(0, output, False)[0])
        self.assertEqual("EXECUTED_PASS", runner.classify(0, ONE_PASS, False)[0])
        self.assertEqual("EXECUTED_FAIL", runner.classify(101, ONE_FAIL, False)[0])
        self.assertEqual("ATTEMPTED_UNAVAILABLE", runner.classify(-9, ONE_FAIL, True)[0])

    def test_fresh_packet_integrity_and_non_assurance(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            with patch.object(runner, "admit", return_value=[]), \
                 patch.object(runner, "git", return_value="f" * 40), \
                 patch.object(runner, "execute", return_value=(0, ONE_PASS, "", False)):
                result = runner.collect(root, root / "run", 60)
            self.assertEqual("partial", result["status"])
            self.assertEqual("INDETERMINATE", result["assurance_state"])
            self.assertEqual(0, result["composition_pass"])
            self.assertEqual([], result["discharged_propositions"])
            self.assertEqual(5, len(result["attempts"]))
            self.assertEqual("partial", runner.verify(root / "run")["status"])
            with self.assertRaisesRegex(ValueError, "new output"):
                runner.collect(root, root / "run")
            (root / "run" / "result.json").write_text("{}")
            with self.assertRaisesRegex(ValueError, "integrity"):
                runner.verify(root / "run")

    def test_failed_native_vector_never_promotes(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            answers = [(0, ONE_PASS, "", False)] * 4 + [(101, ONE_FAIL, "", False)]
            with patch.object(runner, "admit", return_value=[]), \
                 patch.object(runner, "git", return_value="f" * 40), \
                 patch.object(runner, "execute", side_effect=answers):
                result = runner.collect(root, root / "packet", 60)
            self.assertEqual("fail", result["status"])
            self.assertEqual("EXECUTED_FAIL", result["attempts"][-1]["state"])
            self.assertEqual("INDETERMINATE", runner.verify(root / "packet")["assurance_state"])


if __name__ == "__main__":
    unittest.main()
