"""Build pinned Matt Pocock references without adding discovery entrypoints."""
import argparse
import hashlib
import json
import posixpath
import re
from pathlib import Path
from urllib.parse import urlsplit

import yaml

ROOT = Path(__file__).resolve().parent
BUNDLE = ROOT / "skills"


def render():
    lock = json.loads((ROOT / "source-lock.json").read_text(encoding="utf-8"))
    source_root = ROOT / ".build/source"
    source = lock["source"]
    base_url = f"https://github.com/{source['repository']}/blob/{source['commit']}/"
    mapped, source_bytes, entries = {}, {}, []
    for bucket, names in lock["groups"].items():
        for name in names:
            folder = source_root / name
            raw = (folder / "SKILL.md").read_bytes()
            parts = raw.decode("utf-8").split("---", 2)
            if len(parts) != 3 or parts[0].strip():
                raise ValueError(f"Missing frontmatter: {name}")
            metadata = yaml.safe_load(parts[1])
            if metadata["name"] != name:
                raise ValueError(f"Workflow ID mismatch: {name}")
            policy_file = folder / "agents/openai.yaml"
            policy = yaml.safe_load(policy_file.read_text(encoding="utf-8")) if policy_file.exists() else {}
            implicit = not metadata.get("disable-model-invocation", False)
            implicit = implicit and policy.get("policy", {}).get("allow_implicit_invocation", True)
            entries.append({
                "id": name, "bucket": bucket, "description": metadata["description"],
                "promoted": bucket in {"engineering", "productivity"},
                "implicit": bool(implicit),
                "host": "claude" if name in {"claude-handoff", "git-guardrails-claude-code"} else "portable",
                "guide": f"references/{bucket}/{name}/guide.md",
                "source_path": f"skills/{bucket}/{name}/SKILL.md",
                "source_metadata": metadata,
            })
            for path in sorted(folder.rglob("*")):
                if path.is_symlink():
                    raise ValueError(f"Unexpected symlink: {path}")
                if not path.is_file():
                    continue
                relative = path.relative_to(folder).as_posix()
                original = f"skills/{bucket}/{name}/{relative}"
                source_bytes[original] = path.read_bytes()
                if relative.startswith("agents/"):
                    continue
                renamed = "guide.md" if relative == "SKILL.md" else relative
                mapped[original] = f"references/{bucket}/{name}/{renamed}"
    if len({item["id"] for item in entries}) != len(entries):
        raise ValueError("Duplicate workflow IDs")

    generated = {}
    link_pattern = re.compile(r"(\]\()([^)\s]+)(\))")
    for original, destination in mapped.items():
        data = source_bytes[original]
        if destination.endswith(".md"):
            content = data.decode("utf-8")
            banner = ""
            if original.endswith("/SKILL.md"):
                content = content.split("---", 2)[2].lstrip()
                compatibility = posixpath.relpath("references/compatibility.md", posixpath.dirname(destination))
                banner = (
                    f"> Source: [{original}]({base_url}{original}). Adapted for the single skills entrypoint.\n"
                    f"> Apply [Codex compatibility]({compatibility}) before these source instructions.\n\n"
                )

            def rewrite(match):
                target = match[2]
                parts = urlsplit(target)
                if parts.scheme or parts.netloc or target.startswith(("#", "/")):
                    return match[0]
                resolved = posixpath.normpath(posixpath.join(posixpath.dirname(original), parts.path))
                if resolved in mapped:
                    rewritten = posixpath.relpath(mapped[resolved], posixpath.dirname(destination))
                else:
                    rewritten = base_url + resolved
                if parts.fragment:
                    rewritten += "#" + parts.fragment
                return match[1] + rewritten + match[3]

            data = (banner + link_pattern.sub(rewrite, content)).encode("utf-8")
        generated[destination] = data

    generated["references/catalog.json"] = (json.dumps(
        {"version": 1, "workflows": entries}, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    lines = ["# Workflow Index", "", "Read only the chosen workflow and its required dependencies.", ""]
    for bucket in lock["groups"]:
        lines += [f"## {bucket.replace('-', ' ').title()}", ""]
        for item in entries:
            if item["bucket"] != bucket:
                continue
            policy = "implicit" if item["implicit"] and item["promoted"] else "umbrella invocation"
            if not item["promoted"]:
                policy = "named-only"
            guide = item["guide"].removeprefix("references/")
            lines.append(f"- [{item['id']}]({guide}) ({policy}): {item['description']}")
        lines.append("")
    generated["references/index.md"] = "\n".join(lines).encode("utf-8")
    license_bytes = (ROOT / ".build/LICENSE").read_bytes()
    generated["LICENSE"] = license_bytes
    manifest = {
        "upstream": lock["upstream"], "source": source,
        "note": "Workflow trees are identical at these commits; packaged once from the synchronized fork.",
        "source_sha256": {name: hashlib.sha256(data).hexdigest() for name, data in sorted(source_bytes.items())},
        "license_sha256": hashlib.sha256(license_bytes).hexdigest(),
        "packaged_sha256": {name: hashlib.sha256(data).hexdigest() for name, data in sorted(generated.items())},
    }
    generated["references/sources.json"] = (json.dumps(manifest, indent=2) + "\n").encode("utf-8")
    return generated


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    generated = render()
    for name, data in generated.items():
        target = BUNDLE / name
        if target.exists() and target.read_bytes() != data:
            raise SystemExit(f"Existing output differs; review before replacing: {target}")
        if args.check and not target.is_file():
            raise SystemExit(f"Missing generated output: {target}")
    if not args.check:
        for name, data in generated.items():
            target = BUNDLE / name
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists():
                target.write_bytes(data)
    print(json.dumps({"status": "ok", "check": args.check, "generated_files": len(generated)}))


if __name__ == "__main__":
    main()
