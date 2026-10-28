"""Offline packaging and routing contract checks. No network or model calls."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import unittest
from unittest.mock import patch
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent
BUNDLE = ROOT / "skills"
spec = importlib.util.spec_from_file_location("matt_route", BUNDLE / "scripts/route.py")
router = importlib.util.module_from_spec(spec)
spec.loader.exec_module(router)


class BundleTests(unittest.TestCase):
    def test_single_discovery_entry(self):
        self.assertEqual(list(BUNDLE.rglob("SKILL.md")), [BUNDLE / "SKILL.md"])
        self.assertEqual(list(BUNDLE.rglob("openai.yaml")), [BUNDLE / "agents/openai.yaml"])

    def test_inventory_and_assets(self):
        items = router.catalog()
        self.assertEqual(len(items), 38)
        self.assertEqual(len({item["id"] for item in items}), 38)
        self.assertEqual(sum(item["promoted"] for item in items), 27)
        for item in items:
            self.assertTrue((BUNDLE / item["guide"]).is_file(), item["id"])
        source_files = [
            path for bucket in ("engineering", "productivity", "in-progress", "misc")
            for path in (BUNDLE / "references" / bucket).rglob("*") if path.is_file()
        ]
        self.assertEqual(len(source_files), 38 + 27)

    def test_packaged_source_integrity(self):
        manifest = json.loads((BUNDLE / "references/sources.json").read_text(encoding="utf-8"))
        for name, expected in manifest["packaged_sha256"].items():
            self.assertEqual(hashlib.sha256((BUNDLE / name).read_bytes()).hexdigest(), expected, name)

    def test_local_markdown_links_exist(self):
        for path in BUNDLE.rglob("*.md"):
            for target in re.findall(r"\]\(([^)\s]+)\)", path.read_text(encoding="utf-8")):
                parsed = urlsplit(target)
                if parsed.scheme or parsed.netloc or target.startswith(("#", "/")):
                    continue
                linked = (path.parent / unquote(parsed.path)).resolve()
                self.assertTrue(linked.is_relative_to(BUNDLE.resolve()), (path, target))
                self.assertTrue(linked.exists(), (path, target))


class RoutingTests(unittest.TestCase):
    @staticmethod
    def no_call(_):
        raise AssertionError("Inference was not permitted")

    def test_named_workflow_needs_no_inference(self):
        result = router.route({"workflow": "tdd"}, self.no_call)
        self.assertEqual((result["workflow"], result["source"], result["requests"]), ("tdd", "explicit", 0))

    def test_unknown_name_does_not_infer(self):
        self.assertEqual(router.route({"workflow": "../../other"}, self.no_call)["status"], "llm_required")

    def test_implicit_restrictions_and_named_only(self):
        captured = {}
        def decision(payload):
            captured.update(payload["options"])
            return {"status": "ok", "choice": "none", "confidence": 0.9}
        router.route({"request": "Review a patch"}, decision)
        self.assertIn("code-review", captured)
        self.assertNotIn("implement", captured)
        self.assertNotIn("chief-of-staff", captured)
        captured.clear()
        router.route({"request": "Implement a ticket", "invoked": True}, decision)
        self.assertIn("implement", captured)
        self.assertNotIn("chief-of-staff", captured)

    def test_dependency_and_beta_can_be_read_by_name(self):
        result = router.route({"workflow": "chief-of-staff"}, self.no_call)
        self.assertEqual(result["workflow"], "chief-of-staff")
        result = router.route({"workflow": "claude-handoff"}, self.no_call)
        self.assertEqual(result["host"], "claude")

    def test_ineligible_candidate_is_not_sent(self):
        result = router.route({"request": "Do work", "invoked": True, "candidates": ["chief-of-staff"]}, self.no_call)
        self.assertEqual(result["reason"], "ineligible_candidates")

    def test_jev_selection_returns_real_guide(self):
        result = router.route({"request": "Diagnose a failure", "invoked": True},
                              lambda _: {"status": "ok", "choice": "diagnosing-bugs", "confidence": 0.9})
        self.assertEqual(result["workflow"], "diagnosing-bugs")
        self.assertTrue(Path(result["guide"]).is_file())

    def test_failure_and_unknown_output_return_to_llm(self):
        answers = [
            {"status": "fail_open", "reason_code": "timeout"},
            {"status": "ok", "choice": "bogus", "confidence": 1},
            {"status": "ok", "choice": "implement", "confidence": 0.2},
            {"status": "ok", "choice": "implement", "confidence": float("nan")},
            None,
        ]
        for answer in answers:
            with self.subTest(answer=answer):
                self.assertEqual(router.route({"request": "Implement", "invoked": True},
                                              lambda _: answer)["status"], "llm_required")

    def test_confidence_must_be_a_real_number_in_range(self):
        payload = {"request": "Implement", "invoked": True, "candidates": ["implement", "tdd"]}
        for confidence in (True, False, "0.9", None, float("nan"), float("inf"), float("-inf"), -1, 1.01):
            with self.subTest(confidence=confidence):
                result = router.route(payload, lambda _: {"status": "ok", "choice": "implement", "confidence": confidence})
                self.assertEqual((result["status"], result["reason"]), ("llm_required", "invalid_or_uncertain_reply"))
        for confidence in (0.5, 1.0):
            with self.subTest(confidence=confidence):
                result = router.route(payload, lambda _: {"status": "ok", "choice": "implement", "confidence": confidence})
                self.assertEqual((result["status"], result["workflow"]), ("ok", "implement"))

    def test_no_match_and_disabled_integration(self):
        result = router.route({"request": "Check weather", "invoked": True},
                              lambda _: {"status": "ok", "choice": "none", "confidence": 0.9})
        self.assertEqual(result["status"], "no_match")
        with patch.dict(os.environ, {"JEV_CODEX_OFF": "1"}):
            result = router.route({"request": "Review a patch", "invoked": True})
        self.assertEqual(result["reason"], "disabled_by_user")


if __name__ == "__main__":
    unittest.main()
