"""Evidence boundary tests; fake process events here are NOT runtime observations."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "experiments/eucalyptus-vti-consumption/run.py"
spec = importlib.util.spec_from_file_location("eucalyptus_consumption", SOURCE)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

ONE_PASS = "running 1 test\ntest test_case ... ok\ntest result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out;\n"
ONE_FAIL = "running 1 test\ntest test_case ... FAILED\ntest result: FAILED. 0 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out;\n"


class EucalyptusNativeConsumerTests(unittest.TestCase):
    def test_source_contract_is_exact_and_bounded(self):
        self.assertEqual("49f5f1beb61adc34bdf7cf0bd3eb10f594415b80", m.TARGET_SHA)
        self.assertEqual(4, len(m.SCENARIOS))
        self.assertEqual(4, len({s[0] for s in m.SCENARIOS}))
        self.assertEqual({"EUC-01", "EUC-05", "EUC-06"}, {s[1] for s in m.SCENARIOS})
        self.assertTrue(all("--locked" in s[2] and s[2][0] == "cargo" for s in m.SCENARIOS))
        self.assertIn("post-restart", " ".join(m.MISSING))

    def test_missing_target_or_changed_revision_is_not_admitted(self):
        with tempfile.TemporaryDirectory() as d:
            target = Path(d) / "source"
            target.mkdir()
            with patch.object(m, "git", return_value="0" * 40):
                with self.assertRaisesRegex(ValueError, "revision"):
                    m.verify_target(target)
            out = Path(d) / "output"
            with patch.object(m, "git", return_value="0" * 40):
                with self.assertRaises(ValueError):
                    m.collect(target, out)
            self.assertFalse(out.exists())

    def test_exit_zero_without_one_named_test_is_not_pass(self):
        for output in ("", "test result: ok. 0 passed; 0 failed; 0 ignored;",
                       "test result: ok. 2 passed; 0 failed; 0 ignored;"):
            with self.subTest(output=output):
                state, counts = m.classify(m.SCENARIOS[0][2], 0, output, False)
                self.assertEqual("ATTEMPTED_UNAVAILABLE", state)
        self.assertEqual("EXECUTED_NONZERO",
                         m.classify(m.SCENARIOS[0][2], 101, ONE_FAIL, False)[0])
        self.assertEqual("EXECUTED_PASS",
                         m.classify(m.SCENARIOS[0][2], 0, ONE_PASS, False)[0])
        self.assertEqual("ATTEMPTED_UNAVAILABLE",
                         m.classify(m.SCENARIOS[0][2], -9, ONE_FAIL, True)[0])

    def test_collection_seals_and_cannot_promote_fixture_to_composition(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            out = root / "run"
            with patch.object(m, "verify_target"), patch.object(m, "git", return_value="c" * 40):
                with patch.object(m, "execute", return_value=(0, ONE_PASS, "", False)):
                    result = m.collect(root, out, 60)
            self.assertEqual("partial", result["status"])
            self.assertEqual("INDETERMINATE", result["assurance_state"])
            self.assertEqual(0, result["composition_pass"])
            self.assertEqual([], result["discharged_euc_propositions"])
            self.assertEqual(4, len(result["attempts"]))
            self.assertEqual("partial", m.verify_packet(out)["status"])
            (out / "positive-sealed-tsp.stdout.txt").write_text("corrupted")
            with self.assertRaisesRegex(ValueError, "integrity"):
                m.verify_packet(out)

    def test_partial_failure_retains_negative_runtime_state(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            observed = [(0, ONE_PASS, "", False)] * 3 + [(101, ONE_FAIL, "", False)]
            with patch.object(m, "verify_target"), patch.object(m, "git", return_value="c" * 40):
                with patch.object(m, "execute", side_effect=observed):
                    result = m.collect(root, root / "run", 60)
            self.assertEqual("fail", result["status"])
            self.assertEqual("EXECUTED_NONZERO", result["attempts"][-1]["state"])
            self.assertEqual("INDETERMINATE", result["assurance_state"])
            self.assertNotIn("PASS", result["status"].upper())
            self.assertIsNotNone(m.verify_packet(root / "run"))

    def test_malformed_or_extra_evidence_file_fails_integrity(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            with patch.object(m, "verify_target"), patch.object(m, "git", return_value="c" * 40):
                with patch.object(m, "execute", return_value=(0, ONE_PASS, "", False)):
                    m.collect(root, root / "run", 60)
            (root / "run" / "injected.txt").write_text("unsealed")
            with self.assertRaisesRegex(ValueError, "integrity"):
                m.verify_packet(root / "run")


if __name__ == "__main__":
    unittest.main()
