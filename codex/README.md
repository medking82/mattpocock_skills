# One Codex Skills Entrypoint

This local Codex package combines the 38 Matt Pocock workflows into one
`skills` skill. It preserves all 27 supporting files and the MIT license.
The 27 promoted workflows can be selected when the user invokes `$skills`;
the 11 beta/misc workflows require their original name. Ordinary implicit routing
retains upstream invocation policies.

Use `$skills <task>`, or choose **Skills** from the skill picker. Codex's built-in
`/skills` command opens the picker; this package does not replace it.

The main LLM handles clear choices. `skills/scripts/route.py` uses the existing
Jev adapter for ambiguity and returns control to the main LLM on failure. It
installs no model, credentials, hook, provider or scheduled updater.

## Sources And Rebuild

`source-lock.json` pins the synchronized fork and upstream. The source checkout
is sparse; this package does not change its sparse rules or restore local deletions.
The bundled reference tree is committed-ready source, not dependent on the cache.

Download the source workflows with the system skill-installer helper, using the
pinned source commit, the paths in `source-lock.json`, and
`--dest codex/.build/source --method download`. Keep temporary extraction under
`codex/.build/temp` on Windows. Save the pinned repository's LICENSE as
`codex/.build/LICENSE`.

Run using the native Python interpreter and the Windows hidden runner:

```text
python -B codex/build_bundle.py
python -B codex/build_bundle.py --check
python -B codex/test_bundle.py
python -B <system-skill-creator>/scripts/quick_validate.py codex/skills
```

The builder only creates missing files or accepts identical outputs; changed
references require deliberate review. It never downloads or executes upstream code.
Install the validated `codex/skills` directory as `<CODEX_HOME>/skills/skills`.
For a new install, refuse an existing destination; for an update, review and
preserve local edits first.

Only that runtime directory is discoverable. `references/**/guide.md` replaces
nested source `SKILL.md` files; per-workflow invocation metadata is kept in the
catalog instead of installed as extra entries.
