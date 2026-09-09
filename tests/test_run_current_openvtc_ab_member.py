import importlib.util
from pathlib import Path
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "run_current_openvtc_ab_member", ROOT / "scripts" / "run_current_openvtc_ab_member.py"
)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def capture_for(member_name):
    shared, member = MOD.member_contract(member_name)
    requirements = {}
    for requirement_id, expected_surfaces in (member.get("expectations") or {}).items():
        surfaces = {}
        if "*" in expected_surfaces:
            # Representative surfaces are sufficient to test wildcard semantics here;
            # the live runner validates every surface actually produced.
            surfaces = {
                "one": {"classification": expected_surfaces["*"]["classification"]},
                "two": {"classification": expected_surfaces["*"]["classification"]},
            }
        else:
            for surface_name, expected in expected_surfaces.items():
                surface = {}
                execution = {}
                for key, value in expected.items():
                    if key == "context_a_execution":
                        execution["context_a"] = value
                    elif key == "context_b_execution":
                        execution["context_b"] = value
                    else:
                        surface[key] = value
                if execution:
                    surface["execution"] = execution
                surfaces[surface_name] = surface
        requirements[requirement_id] = {"surfaces": surfaces}
    return {
        "provenance": {
            "implementation_repository": shared["implementation_repository"],
            "implementation_revision": shared["implementation_revision"],
        },
        "experiment": {"observed_join": member["observed_join"]},
        "requirements": requirements,
    }


class ReusableOpenVTCABRunnerTests(unittest.TestCase):
    def test_supported_members_are_exactly_two_artifact_evidence_export_members(self):
        supported = []
        for member in ("track-a", "track-b-policy", "track-b-status", "track-b-task"):
            try:
                _, contract = MOD.member_contract(member)
                supported.append((member, len(contract["expected_artifacts"])))
            except ValueError:
                pass
        self.assertEqual(
            [("track-a", 2), ("track-b-status", 2), ("track-b-task", 2)],
            supported,
        )

    def test_policy_fails_closed_because_specialist_integration_is_deeper(self):
        with self.assertRaisesRegex(ValueError, "must not discard deeper specialist semantics"):
            MOD.member_contract("track-b-policy")

    def test_unknown_member_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "unknown characterized member"):
            MOD.member_contract("unknown")

    def test_characterized_capture_validation_accepts_each_supported_member(self):
        for member in ("track-a", "track-b-status", "track-b-task"):
            shared, contract = MOD.member_contract(member)
            with self.subTest(member=member):
                MOD.validate_capture(shared, contract, capture_for(member))

    def test_wrong_join_is_rejected(self):
        shared, contract = MOD.member_contract("track-b-status")
        doc = capture_for("track-b-status")
        doc["experiment"]["observed_join"] = "not-detected"
        with self.assertRaisesRegex(ValueError, "observed_join"):
            MOD.validate_capture(shared, contract, doc)

    def test_not_evidenced_cannot_be_silently_relabelled_absent(self):
        shared, contract = MOD.member_contract("track-a")
        doc = capture_for("track-a")
        doc["requirements"]["ER-STATUS-AB"]["surfaces"]["one"]["classification"] = "absent"
        with self.assertRaisesRegex(ValueError, "expected 'not-evidenced'"):
            MOD.validate_capture(shared, contract, doc)

    def test_status_correlator_origin_is_enforced(self):
        shared, contract = MOD.member_contract("track-b-status")
        doc = capture_for("track-b-status")
        doc["requirements"]["ER-STATUS-AB"]["surfaces"]["status_handle"]["correlator_origin"] = "none"
        with self.assertRaisesRegex(ValueError, "correlator_origin"):
            MOD.validate_capture(shared, contract, doc)


if __name__ == "__main__":
    unittest.main()
