#!/usr/bin/env python3
"""Regression tests for the runnable IC-PDC-MED-001 demonstrator."""

import json
import unittest

from app import MAX_BODY_BYTES, PDCApplication, parse_json_body


class TestPDCApplication(unittest.TestCase):
    def setUp(self) -> None:
        self.app = PDCApplication()

    def test_permit_then_revocation_denies_new_same_class_request(self) -> None:
        permitted = self.app.request_re_reminder()["result"]
        self.assertEqual("permit", permitted["authorization"])
        self.assertEqual(1, self.app.core.re_reminder_effects)

        self.app.revoke()
        reminder_before = self.app.core.snapshot()["reminder"]
        denied = self.app.request_re_reminder()["result"]

        self.assertEqual("deny", denied["authorization"])
        self.assertEqual("AUTHORITY_REVOKED", denied["reason"])
        self.assertFalse(denied["state_mutation"])
        self.assertEqual(1, self.app.core.re_reminder_effects)
        self.assertEqual(reminder_before, self.app.core.snapshot()["reminder"])

    def test_missing_authority_evidence_is_indeterminate(self) -> None:
        self.app.remove_authority_evidence()
        result = self.app.request_re_reminder()["result"]

        self.assertEqual("indeterminate", result["authorization"])
        self.assertEqual("MISSING_AUTHORITY_EVIDENCE", result["reason"])
        self.assertFalse(result["state_mutation"])

    def test_caregiver_view_stays_inside_minimum_disclosure_contract(self) -> None:
        payload = self.app.view()["caregiver_exception"]
        self.assertEqual(
            {"exception_ref", "reminder_time", "permitted_actions"}, set(payload)
        )
        self.assertFalse(
            {
                "medication_name",
                "diagnosis",
                "prescription_image",
                "medication_history",
                "caregiver_graph",
            }
            & set(payload)
        )

    def test_evidence_contains_authorization_and_effect(self) -> None:
        self.app.request_re_reminder()
        events = [record["event"] for record in self.app.view()["evidence"]]
        self.assertIn("authorization_decision", events)
        self.assertIn("effect_recorded", events)

    def test_reset_restores_canonical_exception_state(self) -> None:
        self.app.revoke()
        self.app.reset()
        view = self.app.view()

        self.assertEqual("active", view["authoritative_state"]["delegation"]["status"])
        self.assertEqual(
            "escalation_pending", view["authoritative_state"]["reminder"]["status"]
        )
        self.assertEqual([], view["evidence"])

    def test_json_parser_rejects_malformed_non_object_and_oversize(self) -> None:
        for raw in (b"{", b"[]"):
            with self.assertRaises(ValueError):
                parse_json_body(raw)

        with self.assertRaises(ValueError):
            parse_json_body(b"x" * (MAX_BODY_BYTES + 1))

        self.assertEqual(
            {"x": 1}, parse_json_body(json.dumps({"x": 1}).encode("utf-8"))
        )


if __name__ == "__main__":
    unittest.main()
