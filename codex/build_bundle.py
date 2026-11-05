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
BUCKETS = ("engineering", "productivity", "in-progress", "misc")
MAP_START, MAP_END = "<!-- workflow-map:start -->", "<!-- workflow-map:end -->"


def task_phrase(description):
    """First sentence of an upstream description, for a promoted workflow without a curated row."""
    sentence = re.split(r"(?<=[.!?])\s", " ".join(description.split()), maxsplit=1)[0].rstrip(".")
    return sentence if len(sentence) <= 90 else sentence[:87].rstrip() + "..."


def render_map(entries):
    """Route every promoted workflow: curated wording and order first, then upstream additions."""
    curated = json.loads((ROOT / "workflow-map.json").read_text(encoding="utf-8"))["rows"]
    if len({row["id"] for row in curated}) != len(curated):
        raise ValueError("Duplicate workflow ID in workflow-map.json")
    promoted = {item["id"]: item for item in entries if item["promoted"]}
    rows = [(row["task"], promoted[row["id"]]) for row in curated if row["id"] in promoted]
    routed = {item["id"] for _, item in rows}
    rows += [(task_phrase(item["description"]), item) for item in promoted.values() if item["id"] not in routed]
    lines = ["| Task | Starting Workflow |", "| --- | --- |"]
    lines += [f"| {task.replace('|', '/')} | [{item['id']}]({item['guide']}) |" for task, item in rows]
    return "\n".join(lines)


def render_entrypoint(entries):
    """Regenerate only the marked Workflow Map; the rest of SKILL.md stays hand-written."""
    text = (BUNDLE / "SKILL.md").read_text(encoding="utf-8")
    if text.count(MAP_START) != 1 or text.count(MAP_END) != 1 or text.index(MAP_START) > text.index(MAP_END):
        raise ValueError("SKILL.md needs exactly one workflow-map marker pair")
    start, end = text.index(MAP_START) + len(MAP_START), text.index(MAP_END)
    return (text[:start] + "\n" + render_map(entries) + "\n" + text[end:]).encode("utf-8")


def parse_frontmatter(block, name):
    """YAML first; upstream has shipped unquoted ``key: a: b`` descriptions, so fall back to
    reading top-level ``key: value`` lines as plain strings rather than failing the refresh."""
    try:
        return yaml.safe_load(block)
    except yaml.YAMLError:
        metadata, key = {}, None
        for line in block.splitlines():
            match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
            if match:
                key, value = match[1], match[2].strip().strip("\"'")
                metadata[key] = {"true": True, "false": False}.get(value, value)
            elif key and line.startswith((" ", "	")) and isinstance(metadata[key], str):
                metadata[key] = f"{metadata[key]} {line.strip()}".strip()
        if "name" not in metadata:
            raise ValueError(f"Unreadable frontmatter: {name}")
        return metadata


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
            metadata = parse_frontmatter(parts[1], name)
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
    # Outside the source manifest: SKILL.md stays a hand-written entrypoint with a generated map.
    generated["SKILL.md"] = render_entrypoint(entries)
    return generated


def stale_outputs(generated, groups):
    """Files under the generated bucket trees that the current source no longer produces."""
    stale = []
    for bucket in sorted(set(groups) | set(BUCKETS)):
        tree = BUNDLE / "references" / bucket
        if tree.is_dir():
            stale += [path for path in sorted(tree.rglob("*"))
                      if path.is_file() and path.relative_to(BUNDLE).as_posix() not in generated]
    return stale


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--replace", action="store_true",
        help="Overwrite changed outputs and delete stale ones. For the automated refresh "
             "(codex/refresh_bundle.py); review the diff before accepting it by hand.")
    args = parser.parse_args()
    if args.check and args.replace:
        raise SystemExit("--check and --replace are mutually exclusive")
    generated = render()
    groups = json.loads((ROOT / "source-lock.json").read_text(encoding="utf-8"))["groups"]
    stale = stale_outputs(generated, groups)
    for name, data in generated.items():
        target = BUNDLE / name
        if args.check and not target.is_file():
            raise SystemExit(f"Missing generated output: {target}")
        if not args.replace and target.exists() and target.read_bytes() != data:
            raise SystemExit(f"Existing output differs; review before replacing: {target}")
    if stale and not args.replace:
        raise SystemExit(f"Stale output no longer in the source; review before removing: {stale[0]}")
    if not args.check:
        for name, data in generated.items():
            target = BUNDLE / name
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists() or (args.replace and target.read_bytes() != data):
                target.write_bytes(data)
        for path in stale:
            path.unlink()
        for directory in sorted((BUNDLE / "references").rglob("*"), reverse=True):
            if directory.is_dir() and not any(directory.iterdir()):
                directory.rmdir()
    print(json.dumps({"status": "ok", "check": args.check, "replace": args.replace,
                      "generated_files": len(generated), "removed_files": len(stale) if args.replace else 0}))


if __name__ == "__main__":
    main()
