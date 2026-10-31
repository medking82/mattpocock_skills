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
        items = catalog()
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
