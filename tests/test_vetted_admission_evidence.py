import importlib.util
from pathlib import Path
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_capture_module():
    path = ROOT / "experiments" / "dtg-protected-access" / "capture_ab_runtime.py"
    spec = importlib.util.spec_from_file_location("capture_ab_runtime", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class VettedAdmissionEvidenceTests(unittest.TestCase):
    def test_dpip_vetting_requirements_are_registered(self):
        contract = yaml.safe_load((ROOT / "cases/dtg-protected-access/dpip-runtime-evidence-contract.yaml").read_text())
        expected = {
            "ER-VETTING-DISCOVERY-AB",
            "ER-VETTER-DIRECTORY-AB",
            "ER-STATUS-AB",
            "ER-VETTING-TICKET-AB",
            "ER-VETTING-RETENTION-AB",
        }
        self.assertTrue(expected.issubset(contract["requirements"]))

    def test_vetted_admission_is_a_characterized_reusable_member(self):
        model = yaml.safe_load((ROOT / "evidence/workflow-characterization/current-openvtc-ab-family.yaml").read_text())
        member = model["members"]["vetted-admission"]
        self.assertEqual("evidence-export", member["integration_depth"])
        self.assertEqual("OpenVTC/openvtc", member["implementation_repository"])
        self.assertEqual(40, len(member["implementation_revision"]))
        self.assertEqual("not-detected", member["observed_join"])

    def test_ticket_probe_never_exports_raw_ticket_material(self):
        source = (ROOT / "experiments/dtg-protected-access/current_openvtc_vetting_ticket_context.py").read_text()
        self.assertIn('"raw_secret_exported": false', source)
        self.assertNotIn('"ticket_secret"', source)
        self.assertNotIn('"ticket_code"', source)
        executed = yaml.safe_load((ROOT / "cases/dtg-protected-access/current-openvtc-vetted-admission-ab.yaml").read_text())
        self.assertIn("Fresh ticket fingerprints", executed["assurance_boundary"])

    def test_detector_still_flags_a_deliberately_seeded_correlator(self):
        capture = load_capture_module()
        same = "sha256:seeded-control"
        self.assertEqual("identical", capture.classify(same, same, True, True))
        self.assertEqual("fresh", capture.classify("sha256:a", "sha256:b", True, True))
        self.assertEqual("not-evidenced", capture.classify(None, None, False, False))


if __name__ == "__main__":
    unittest.main()
