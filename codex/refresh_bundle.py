"""Refresh the bundle from the synchronized fork without hand-editing the source lock.

Reads workflow sources from git objects of a fork checkout (full history), pins the newest
commit that changed ``skills/``, records the upstream commit with an identical ``skills/``
tree, rewrites ``source-lock.json`` and rebuilds ``codex/skills`` with ``build_bundle.py
--replace``. Run ``test_bundle.py`` afterwards. Nothing is downloaded or executed.
"""
import argparse
import io
import json
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUCKETS = ("engineering", "productivity", "in-progress", "misc")


def git(repo, *args):
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True)
    if result.returncode:
        raise SystemExit(f"git {' '.join(args)} failed: {result.stderr.decode('utf-8', 'replace').strip()}")
    return result.stdout


def text(repo, *args):
    return git(repo, *args).decode("utf-8").strip()


def extract(repo, commit):
    """Return {workflow: {relative path: bytes}} per bucket, plus the license bytes."""
    archive = tarfile.open(fileobj=io.BytesIO(git(repo, "archive", "--format=tar", commit, "skills", "LICENSE")))
    groups, files, owner, license_bytes = {bucket: [] for bucket in BUCKETS}, {}, {}, None
    for member in archive.getmembers():
        if member.name == "LICENSE":
            license_bytes = archive.extractfile(member).read()
            continue
        parts = member.name.split("/")
        if not member.isfile() or len(parts) < 4 or parts[1] not in BUCKETS:
            continue
        bucket, name, relative = parts[1], parts[2], "/".join(parts[3:])
        if owner.setdefault(name, bucket) != bucket:
            raise SystemExit(f"Duplicate workflow ID across buckets: {name}")
        files.setdefault(name, {})[relative] = archive.extractfile(member).read()
        if relative == "SKILL.md":
            groups[bucket].append(name)
    # A folder without SKILL.md is not a workflow (for example a bucket README sibling).
    files = {name: data for name, data in files.items() if "SKILL.md" in data}
    if license_bytes is None or not files:
        raise SystemExit("The fork commit has no LICENSE or no workflows under skills/")
    return {bucket: sorted(names) for bucket, names in groups.items()}, files, license_bytes


def upstream_commit(repo, upstream_ref, tree):
    """Newest upstream commit whose skills/ tree equals the fork's; fail if the fork diverged."""
    for candidate in text(repo, "log", "--format=%H", upstream_ref, "--", "skills").splitlines():
        if text(repo, "rev-parse", f"{candidate}:skills") == tree:
            return candidate
    raise SystemExit(f"No commit on {upstream_ref} has the fork's skills/ tree; the fork has local workflow changes")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fork", required=True, type=Path, help="Checkout of the fork's default branch, full history")
    parser.add_argument("--ref", default="HEAD", help="Fork ref to package (default HEAD)")
    parser.add_argument("--upstream-ref", help="Ref in the fork checkout holding mattpocock/skills main")
    parser.add_argument("--no-build", action="store_true", help="Only rewrite the lock and .build/source")
    args = parser.parse_args()

    lock_path = ROOT / "source-lock.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    commit = text(args.fork, "log", "-1", "--format=%H", args.ref, "--", "skills")
    if not commit:
        raise SystemExit("No commit touches skills/")
    groups, files, license_bytes = extract(args.fork, commit)

    if args.upstream_ref:
        lock["upstream"]["commit"] = upstream_commit(
            args.fork, args.upstream_ref, text(args.fork, "rev-parse", f"{commit}:skills"))
    lock["source"]["commit"] = commit
    lock["groups"] = groups

    build = ROOT / ".build"
    shutil.rmtree(build / "source", ignore_errors=True)
    for name, workflow in files.items():
        for relative, data in workflow.items():
            target = build / "source" / name / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    (build / "LICENSE").write_bytes(license_bytes)
    lock_path.write_bytes((json.dumps(lock, indent=2) + "\n").encode("utf-8"))

    if not args.no_build:
        subprocess.run([sys.executable, "-B", str(ROOT / "build_bundle.py"), "--replace"], check=True)
    print(json.dumps({"source": commit, "upstream": lock["upstream"]["commit"],
                      "workflows": {bucket: len(names) for bucket, names in groups.items()}}))


if __name__ == "__main__":
    main()
