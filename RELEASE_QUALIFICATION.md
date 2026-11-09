# Release qualification applicability

The default branch publishes skills and metadata through
`.github/workflows/fork-sync-upstream.yml`; it has no executable test suite
(`package.json` has `sync-version`/`check-version` metadata commands, no test
command, and there is no tests directory). Its existing version consistency and
fork ancestry checks remain intact. Shared test timing/sharding for that lane is
**N/A**; no test adapter is fabricated for documentation synchronization.

An executable gate does exist on `codex/skills-umbrella`:
`codex/test_bundle.py`. The owner is the default branch's
`.github/workflows/refresh-skills-umbrella.yml`. The companion branch
`perf/release-qualification-umbrella` adds a pinned shared-runner adapter there;
land it onto the umbrella branch **before** this default-branch workflow change.
The refresh workflow retains its existing bundle tests, creates the bundle
commit, qualifies that exact commit, then pushes with its original concurrency
and fast-forward protection. No refresh or branch push was executed locally.

The shared dependency is `medking82/hermes-fleet-sync` at
`4f79a5b4452d9a91037e4cbf564a927b44e2bac6`. Source locks, upstream provenance and
frozen workflow snapshots remain unchanged. Placement input (`--timings`) stays
read-only and separate from output receipts. The umbrella adapter defaults to
serial execution until actual group measurements demonstrate benefit.
