# Owner release qualification

This adapter belongs on `codex/skills-umbrella`, not the docs-only main branch. The actual owner is `.github/workflows/refresh-skills-umbrella.yml` on main; its companion change qualifies the prepared bundle commit between the existing bundle tests/commit and push. Land this umbrella companion before that main workflow change. `codex/source-lock.json`, frozen workflow copies, upstream ancestry and drift checks are unchanged.

Existing `codex/test_bundle.py` unittest suite, run from codex. Class timings are available; default remains serial. No branch-refresh/network operation is executed by this gate.

The runner is `medking82/hermes-fleet-sync` at
`4f79a5b4452d9a91037e4cbf564a927b44e2bac6` (branch
`perf/shared-release-qualification`). `scripts/qualify-release.py` reads the exact
committed manifest, source commit, and pinned engine blobs through Git. It never
fetches or edits the shared checkout. Dirty source bytes are not release evidence.
Receipts retain runner, source/tree/lock, environment/package, command, scope,
coverage, log and freshness identities; failed or stale evidence cannot be reused.
No local receipt substitutes for the owner's CI, ancestry, authorization, or locks.

Run with native Linux Python/Node and state on the WSL filesystem, for example:

```sh
python3 -B scripts/qualify-release.py \
  --runner /mnt/c/GitHub/hermes-release-opt \
  --state "$HOME/sop-release-qualification/matt-umbrella"
```

Install the same prerequisites as the existing gate first. Python unittest suites
may use `--class-shards N --timings /absolute/path/prior-receipt.json`; custom and
Node commands remain serial. Keep one shard unless a measured comparison proves
benefit with the same covered tests. Receipts include whole-class measurements
and group weights; optional packages/skips remain visible in the suite logs.

`--timings` is a read-only placement input. Preserve that file across repeated
runs and write results to the runner's separate receipt path. To refresh weights,
explicitly choose a new prior receipt; never overwrite placement input after each
success. `--reuse` is allowed only where the committed lane enables local reuse,
with the exact same weights and identity, intact logs, and a fresh success. Each
CI runner starts with fresh native state; CI does not request reuse.
