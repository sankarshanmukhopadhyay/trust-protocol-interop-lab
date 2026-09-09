from pathlib import Path
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
CHARACTERIZATION = ROOT / "evidence" / "workflow-characterization" / "current-openvtc-ab-family.yaml"
REUSABLE = ROOT / ".github" / "workflows" / "reusable-current-openvtc-ab-evidence.yml"
COMMON_RUNNER = ROOT / "scripts" / "run_current_openvtc_ab_member.py"


class OpenVTCABWorkflowCharacterizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = yaml.safe_load(CHARACTERIZATION.read_text(encoding="utf-8"))
        cls.shared = cls.model["shared"]
        cls.members = cls.model["members"]

    def test_family_accounts_for_exact_four_current_members(self):
        self.assertEqual(
            {"track-a", "track-b-policy", "track-b-status", "track-b-task"},
            set(self.members),
        )

    def test_every_manifest_preserves_same_immutable_target_pin(self):
        for name, member in self.members.items():
            manifest = yaml.safe_load((ROOT / member["manifest"]).read_text(encoding="utf-8"))
            with self.subTest(member=name):
                self.assertEqual(self.shared["evidence_class"], manifest["evidence_class"])
                self.assertEqual(self.shared["implementation_repository"], manifest["implementation"]["repository"])
                self.assertEqual(self.shared["implementation_revision"], manifest["implementation"]["revision"])
                self.assertEqual(member["experiment_kind"], manifest["experiment"]["kind"])
                self.assertEqual(member["expected_join"], manifest["experiment"]["expected_join"])

    def test_direct_or_reusable_execution_still_reaches_characterized_mechanics(self):
        reusable_text = REUSABLE.read_text(encoding="utf-8")
        runner_text = COMMON_RUNNER.read_text(encoding="utf-8")
        for name, member in self.members.items():
            text = (ROOT / member["workflow"]).read_text(encoding="utf-8")
            with self.subTest(member=name):
                if "reusable-current-openvtc-ab-evidence.yml" in text:
                    self.assertEqual("track-b-task", name)
                    self.assertIn("member: track-b-task", text)
                    self.assertIn(self.shared["implementation_revision"], reusable_text)
                    self.assertIn("run_current_openvtc_ab_member.py", reusable_text)
                    self.assertIn(self.shared["capture_runner"], runner_text)
                    self.assertIn(self.shared["compatibility_exporter"], runner_text)
                    self.assertIn("status --porcelain", reusable_text)
                else:
                    self.assertIn(self.shared["implementation_revision"], text)
                    self.assertIn(self.shared["capture_runner"], text)
                    self.assertIn(self.shared["compatibility_exporter"], text)
                    self.assertIn("status --porcelain", text)

    def test_status_is_deliberate_positive_control_not_unlinkability_case(self):
        status = self.members["track-b-status"]
        self.assertEqual("positive-control", status["experiment_kind"])
        self.assertEqual("must-detect", status["expected_join"])
        self.assertEqual("detected", status["observed_join"])
        for other in ("track-a", "track-b-policy", "track-b-task"):
            with self.subTest(member=other):
                self.assertEqual("unlinkability-pressure-case", self.members[other]["experiment_kind"])
                self.assertEqual("must-not-emerge", self.members[other]["expected_join"])
                self.assertEqual("not-detected", self.members[other]["observed_join"])

    def test_track_a_explicitly_preserves_not_evidenced_status_and_task(self):
        track_a = self.members["track-a"]["expectations"]
        self.assertEqual("not-evidenced", track_a["ER-STATUS-AB"]["*"]["classification"])
        self.assertEqual("not-evidenced", track_a["ER-TASK-AB"]["*"]["classification"])
        self.assertNotEqual("absent", track_a["ER-STATUS-AB"]["*"]["classification"])

    def test_status_correlators_remain_target_derived(self):
        status = self.members["track-b-status"]["expectations"]["ER-STATUS-AB"]
        for surface in ("status_handle", "status_endpoint"):
            with self.subTest(surface=surface):
                self.assertEqual("identical", status[surface]["classification"])
                self.assertEqual("target-derived", status[surface]["correlator_origin"])

    def test_policy_is_deliberately_deeper_specialist_integration(self):
        policy = self.members["track-b-policy"]
        others = {name: member["integration_depth"] for name, member in self.members.items() if name != "track-b-policy"}
        self.assertEqual("dpip-specialist-return-rahp-consumer", policy["integration_depth"])
        self.assertTrue(policy["specialist_expectations"]["terminal_inference_forbidden"])
        self.assertTrue(all(value == "evidence-export" for value in others.values()))
        workflow_text = (ROOT / policy["workflow"]).read_text(encoding="utf-8")
        self.assertIn("evaluate_privacy_observability.py", workflow_text)
        self.assertIn("tools/assessor_contract.py", workflow_text)
        self.assertNotIn("reusable-current-openvtc-ab-evidence.yml", workflow_text)

    def test_expected_artifact_shapes_remain_intentionally_different(self):
        self.assertEqual(4, len(self.members["track-b-policy"]["expected_artifacts"]))
        for other in ("track-a", "track-b-status", "track-b-task"):
            self.assertEqual(2, len(self.members[other]["expected_artifacts"]))

    def test_claim_boundaries_forbid_global_assurance_inference(self):
        joined = " ".join(
            boundary
            for member in self.members.values()
            for boundary in member.get("claim_boundary_contains", [])
        ).lower()
        self.assertIn("privacy pass", joined)
        self.assertTrue("rahp green" in joined or "terminal assurance pass" in joined)


if __name__ == "__main__":
    unittest.main()
