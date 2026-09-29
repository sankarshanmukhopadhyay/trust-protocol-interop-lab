#!/usr/bin/env python3
"""Clean-room HTTP walkthrough for the IC-PDC-MED-001 runnable demonstrator.

This deliberately exercises the documented public HTTP surface rather than calling
CareCore or PDCApplication methods directly. It is a reproducible adoption check,
not a substitute for the human external-adopter evidence required by issue #166.
"""

import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.request import Request, urlopen

from app import PDCApplication, make_handler


class TestPDCAdopterWalkthrough(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.application = PDCApplication()
        cls.server = ThreadingHTTPServer(
            ("127.0.0.1", 0), make_handler(cls.application)
        )
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def request(self, path: str, method: str = "GET") -> dict:
        data = None
        headers = {}
        if method == "POST":
            data = b"{}"
            headers["Content-Type"] = "application/json"
        req = Request(self.base_url + path, data=data, headers=headers, method=method)
        with urlopen(req, timeout=2) as response:
            self.assertEqual(200, response.status)
            return json.loads(response.read().decode("utf-8"))

    def test_documented_permit_revoke_deny_walkthrough(self) -> None:
        initial = self.request("/api/state")
        self.assertEqual("active", initial["authoritative_state"]["delegation"]["status"])

        permitted = self.request("/api/caregiver/re-reminder", "POST")
        self.assertEqual("permit", permitted["result"]["authorization"])

        revoked = self.request("/api/delegation/revoke", "POST")
        self.assertEqual(
            "revoked", revoked["view"]["authoritative_state"]["delegation"]["status"]
        )

        denied = self.request("/api/caregiver/re-reminder", "POST")
        self.assertEqual("deny", denied["result"]["authorization"])
        self.assertEqual("AUTHORITY_REVOKED", denied["result"]["reason"])
        self.assertFalse(denied["result"]["state_mutation"])

    def test_documented_missing_evidence_is_indeterminate(self) -> None:
        self.request("/api/reset", "POST")
        self.request("/api/authority-evidence/remove", "POST")

        result = self.request("/api/caregiver/re-reminder", "POST")
        self.assertEqual("indeterminate", result["result"]["authorization"])
        self.assertEqual("MISSING_AUTHORITY_EVIDENCE", result["result"]["reason"])
        self.assertFalse(result["result"]["state_mutation"])

    def test_http_view_preserves_minimum_disclosure(self) -> None:
        self.request("/api/reset", "POST")
        view = self.request("/api/state")
        payload = view["caregiver_exception"]

        self.assertEqual(
            {"exception_ref", "reminder_time", "permitted_actions"}, set(payload)
        )
        self.assertNotIn("medication_name", payload)
        self.assertNotIn("diagnosis", payload)


if __name__ == "__main__":
    unittest.main()
