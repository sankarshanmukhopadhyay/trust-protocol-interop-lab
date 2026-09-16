import copy
import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("admit", ROOT / "experiments" / "dpip-evidence-obligation" / "admit.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(mod)
FIXTURE = ROOT / "experiments" / "dpip-evidence-obligation" / "dpip-191-obligations.json"


class AdmissionTests(unittest.TestCase):
    def setUp(self):
        self.items = json.loads(FIXTURE.read_text())["obligations"]

    def test_dpip_191_targetless_obligations_are_blocked(self):
        results = [mod.evaluate(x) for x in self.items]
        self.assertTrue(all(r["admission"] == "BLOCKED" for r in results))
        self.assertTrue(all(r["reason"] == "NO_TARGET" for r in results))

    def test_bound_black_box_runtime_is_admissible(self):
        ob = copy.deepcopy(self.items[0])
        ob["target"] = {"repository": "example/target", "revision": "0123456789abcdef"}
        ob["supplier"] = {"role": "INTEROP_LAB", "evidence_source_class": "BLACK_BOX_RUNTIME"}
        ob["access"] = {"status": "AVAILABLE", "blocker": "NONE"}
        self.assertEqual(mod.evaluate(ob)["admission"], "ADMISSIBLE")

    def test_unbound_runtime_is_blocked_even_if_marked_available(self):
        ob = copy.deepcopy(self.items[0])
        ob["supplier"] = {"role": "INTEROP_LAB", "evidence_source_class": "BLACK_BOX_RUNTIME"}
        ob["access"] = {"status": "AVAILABLE", "blocker": "NONE"}
        result = mod.evaluate(ob)
        self.assertEqual(result["admission"], "BLOCKED")
        self.assertEqual(result["reason"], "NO_BOUND_TARGET_REVISION")

    def test_operator_only_white_box_requires_supplier(self):
        ob = copy.deepcopy(self.items[0])
        ob["target"] = {"repository": "example/target", "revision": "0123456789abcdef"}
        ob["access"] = {"status": "AVAILABLE", "blocker": "NONE"}
        result = mod.evaluate(ob)
        self.assertEqual(result["admission"], "SUPPLIER_OR_AUTHORITY_REQUIRED")

    def test_governance_evidence_is_not_lab_evidence(self):
        ob = copy.deepcopy(self.items[0])
        ob["target"] = {"repository": "example/target", "revision": "0123456789abcdef"}
        ob["supplier"] = {"role": "GOVERNANCE_AUTHORITY", "evidence_source_class": "GOVERNANCE"}
        ob["access"] = {"status": "AVAILABLE", "blocker": "NONE"}
        self.assertEqual(mod.evaluate(ob)["admission"], "SUPPLIER_OR_AUTHORITY_REQUIRED")

    def test_output_never_claims_privacy_or_harm_judgment(self):
        result = mod.evaluate(self.items[0])
        forbidden = result["claim_boundary"]["lab_may_not_claim"]
        self.assertIn("privacy PASS/FAIL", forbidden)
        self.assertIn("harm", forbidden)
        self.assertIn("portfolio assurance", forbidden)


if __name__ == "__main__":
    unittest.main()
