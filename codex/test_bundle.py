"""Offline packaging contract checks. No network or model calls."""
import hashlib
import json
from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent
BUNDLE = ROOT / "skills"


def catalog():
    return json.loads((BUNDLE / "references/catalog.json").read_text(encoding="utf-8"))["workflows"]


class BundleTests(unittest.TestCase):
    def test_single_discovery_entry(self):
        self.assertEqual(list(BUNDLE.rglob("SKILL.md")), [BUNDLE / "SKILL.md"])
        self.assertEqual(list(BUNDLE.rglob("openai.yaml")), [BUNDLE / "agents/openai.yaml"])

    def test_inventory_and_assets(self):
        lock = json.loads((ROOT / "source-lock.json").read_text(encoding="utf-8"))
        manifest = json.loads((BUNDLE / "references/sources.json").read_text(encoding="utf-8"))
        items = catalog()
        expected = sum(len(names) for names in lock["groups"].values())
        self.assertGreaterEqual(expected, 30)
        self.assertEqual(len(items), expected)
        self.assertEqual(len({item["id"] for item in items}), expected)
        self.assertEqual(sum(item["promoted"] for item in items),
                         len(lock["groups"]["engineering"]) + len(lock["groups"]["productivity"]))
        for item in items:
            self.assertTrue((BUNDLE / item["guide"]).is_file(), item["id"])
        support = [name for name in manifest["source_sha256"]
                   if not name.endswith("/SKILL.md") and "/agents/" not in name]
        source_files = [
            path for bucket in lock["groups"] for path in (BUNDLE / "references" / bucket).rglob("*") if path.is_file()
        ]
        self.assertEqual(len(source_files), expected + len(support))
        self.assertEqual(manifest["source"], lock["source"])
        self.assertEqual(manifest["upstream"], lock["upstream"])

    def test_workflow_map_routes_every_promoted_workflow(self):
        text = (BUNDLE / "SKILL.md").read_text(encoding="utf-8")
        table = text.split("<!-- workflow-map:start -->", 1)[1].split("<!-- workflow-map:end -->", 1)[0]
        routed = re.findall(r"^\| [^|]+ \| \[([a-z0-9-]+)\]\((references/[^)]+)\) \|$", table, flags=re.M)
        ids = [name for name, _ in routed]
        self.assertEqual(len(ids), len(set(ids)))
        promoted = {item["id"]: item["guide"] for item in catalog() if item["promoted"]}
        self.assertEqual(set(ids), set(promoted))
        for name, guide in routed:
            self.assertEqual(guide, promoted[name], name)

    def test_workflow_map_adds_new_and_skips_removed_workflows(self):
        import build_bundle
        entries = [
            {"id": "tdd", "promoted": True, "guide": "references/engineering/tdd/guide.md", "description": "x"},
            {"id": "brand-new", "promoted": True, "guide": "references/engineering/brand-new/guide.md",
             "description": "Plan a launch | ship it. Use when releasing."},
            {"id": "beta-only", "promoted": False, "guide": "references/misc/beta-only/guide.md", "description": "y"},
        ]
        table = build_bundle.render_map(entries)
        self.assertIn("| Concrete behavior and regression tests | [tdd](references/engineering/tdd/guide.md) |", table)
        self.assertIn("| Plan a launch / ship it | [brand-new](references/engineering/brand-new/guide.md) |", table)
        self.assertNotIn("beta-only", table)
        self.assertNotIn("diagnosing-bugs", table)

    def test_catalog_keeps_invocation_policies(self):
        items = {item["id"]: item for item in catalog()}
        self.assertTrue(items["code-review"]["promoted"] and items["code-review"]["implicit"])
        self.assertTrue(items["implement"]["promoted"])
        self.assertFalse(items["implement"]["implicit"])
        self.assertFalse(items["chief-of-staff"]["promoted"])
        self.assertEqual(items["claude-handoff"]["host"], "claude")

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


if __name__ == "__main__":
    unittest.main()
