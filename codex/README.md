# One Codex Skills Entrypoint

This local Codex package combines the Matt Pocock workflows into one
`skills` skill. It preserves every supporting file and the MIT license.
The promoted (engineering and productivity) workflows can be selected when the
user invokes `$skills`; the beta/misc workflows require their original name.
Ordinary implicit routing retains upstream invocation policies. Counts are not
written here: `catalog.json` and `source-lock.json` are the inventory.

Use `$skills <task>`, or choose **Skills** from the skill picker. Codex's built-in
`/skills` command opens the picker; this package does not replace it.

The main LLM selects the workflow from the catalog and workflow map. The package
ships no routing script and installs no model, credentials, hook, provider or
scheduled updater.

## Sources And Rebuild

`source-lock.json` pins the synchronized fork commit and the identical upstream
commit. The bundled reference tree is committed-ready source, not dependent on any
cache. Nothing here downloads or executes upstream code.

### Automatic refresh

The `Refresh skills umbrella` workflow on the fork's `main` branch
(`.github/workflows/refresh-skills-umbrella.yml`) follows the upstream sync: on a
schedule, on a `skills/**` push to `main`, or manually. It checks out `main` and this
branch, runs `python codex/refresh_bundle.py`, then `python codex/test_bundle.py`,
and pushes one commit to `codex/skills-umbrella` only when the tests pass and files
changed. A failure leaves the branch untouched and fails the run; scheduled failures
send at most one failure email per UTC day. The commit pins the newest fork commit
that changed `skills/`, so unrelated `main` commits never churn the bundle. The run
fails if the fork's `skills/` tree matches no upstream commit (a local workflow edit
in the fork).

`refresh_bundle.py` discovers workflows from the engineering, productivity,
in-progress and misc buckets, rewrites `source-lock.json`, and rebuilds with
`build_bundle.py --replace`, which overwrites changed references and deletes
ones the source dropped. `deprecated/` is never bundled. Hand-written files
(`SKILL.md`, `agents/`, `compatibility.md`) are never touched by a refresh.

Manual refresh, from a full-history checkout of the fork's `main` with upstream
fetched to a ref (for example `git fetch https://github.com/mattpocock/skills.git
main:refs/remotes/upstream/main`):

```text
python -B codex/refresh_bundle.py --fork <fork-checkout> --ref origin/main --upstream-ref refs/remotes/upstream/main
python -B codex/test_bundle.py
python -B <system-skill-creator>/scripts/quick_validate.py codex/skills
```

### Manual rebuild

Without `--replace`, `build_bundle.py` only creates missing files or accepts
identical outputs; changed or stale references need deliberate review.

```text
python -B codex/build_bundle.py
python -B codex/build_bundle.py --check
python -B codex/test_bundle.py
```

Run with the native Python interpreter (PyYAML required) and the Windows hidden
runner. Install the validated `codex/skills` directory as `<CODEX_HOME>/skills/skills`.
For a new install, refuse an existing destination; for an update, review and
preserve local edits first.

Only that runtime directory is discoverable. `references/**/guide.md` replaces
nested source `SKILL.md` files; per-workflow invocation metadata is kept in the
catalog instead of installed as extra entries.
