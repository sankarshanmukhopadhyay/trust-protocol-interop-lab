"""Fail-closed regression tests for source-pinned *unexecuted* restart judgment."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "experiments/eucalyptus-vti-consumption/restart_readiness.py"
spec = importlib.util.spec_from_file_location("eucalyptus_restart_readiness", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class RestartReadinessTests(unittest.TestCase):
    def fixture(self, directory: Path):
        for role, relative in module.SOURCES.items():
            p = directory / relative
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("\n".join(module.ANCHORS[role]) + "\n")
        # Preserve actual order in dispatcher, and real app builder tempdir.
        (directory / module.SOURCES["dispatch"]).write_text(
            "idempotency::claim(&state.idempotency_ks\n"
            "dispatch_typed(state, auth, doc)\n"
            "idempotency::record_outcome(&state.idempotency_ks\n"
        )
        return directory

    def test_rejects_wrong_source_revision(self):
        with tempfile.TemporaryDirectory() as d:
            root = self.fixture(Path(d))
            with patch.object(module, "repo_head", return_value="0" * 40):
                with self.assertRaisesRegex(ValueError, "revision"):
                    module.check(root)

    def test_reports_inadequate_fixture_without_inventing_pass(self):
        with tempfile.TemporaryDirectory() as d:
            root = self.fixture(Path(d))
            with patch.object(module, "repo_head", return_value=module.TARGET):
                with patch.object(module.subprocess, "check_output", return_value=""):
                    result = module.check(root)
            self.assertEqual("NOT_EXECUTED", result["consumer_post_restart_observation"])
            self.assertEqual("INDETERMINATE", result["assurance_state"])
            self.assertEqual(0, result["composition_pass"])
            self.assertEqual([], result["closed_propositions"])
            self.assertEqual("BLOCKED_MISSING_CONSUMER_RESTART_FIXTURE", result["disposition"])
            self.assertTrue(any("after effect commit" in text or "effect commit" in text
                                for text in result["required_test_seam"]))

    def test_missing_implementation_anchor_is_not_assumed_satisfied(self):
        with tempfile.TemporaryDirectory() as d:
            root = self.fixture(Path(d))
            p = root / module.SOURCES["policy"]
            p.write_text(p.read_text().replace("idempotency claim failed; dispatching unguarded", ""))
            with patch.object(module, "repo_head", return_value=module.TARGET):
                with patch.object(module.subprocess, "check_output", return_value=""):
                    with self.assertRaisesRegex(ValueError, "source anchor missing"):
                        module.check(root)

    def test_unsafe_dispatch_order_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = self.fixture(Path(d))
            p = root / module.SOURCES["dispatch"]
            p.write_text(
                "idempotency::claim(&state.idempotency_ks\n"
                "idempotency::record_outcome(&state.idempotency_ks\n"
                "dispatch_typed(state, auth, doc)\n"
            )
            with patch.object(module, "repo_head", return_value=module.TARGET):
                with patch.object(module.subprocess, "check_output", return_value=""):
                    with self.assertRaisesRegex(ValueError, "dispatcher ordering"):
                        module.check(root)


if __name__ == "__main__":
    unittest.main()
