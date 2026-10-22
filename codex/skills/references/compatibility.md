# Codex Compatibility

These rules adapt the bundled source workflows to this host. They take precedence
over conflicting upstream workflow mechanics. User instructions, repository rules,
available tools and existing authorization still govern execution.

- References are guidance for the requested outcome, not permission for additional
  actions. Preserve the selected main model, effort, Fast, permissions and tool bans.
- Resolve a named collection workflow through `catalog.json` and read its guide.
  Upstream `/name`, `$name` and "Skill tool" calls mean these internal reads.
  Do not install standalone copies, invoke an unrelated same-name skill, or run a
  second router for an already named dependency.
- An explicit `$skills` delegates selection among promoted workflows. Without that
  explicit umbrella invocation, only originally model-invoked promoted workflows
  participate in automatic routing. Beta/misc workflows are named-only.
- Use the user's current phase. Implementation does not require a new interview,
  spec, tracker setup, ADR, retrospective or full flow when the task is already
  settled. Reuse existing project conventions and previous answers. Ask only for
  unresolved material choices; do not re-request permission already given.
- Use repository validation commands and proportionate tests. Do not add tests
  that only mirror reversible low-impact edits, or impose unrelated checks.
- Where references prescribe fixed parallel agent counts, specific models, or
  recursive coordinators, follow current delegation authorization and quota rules.
  Prefer one bounded delegate when useful; use a direct/sequential fallback when
  delegation is unavailable. Do not create user-owned chats as subagents.
- Prepare concrete results before asking for any missing approval. Reading a guide
  grants no blanket authority to send messages, publish tickets, push, merge, deploy
  or delete work. Continue actions already authorized by the user/repository.
  Do not commit merely because a source guide says to commit.
- Use canonical workspace locations, preserve dirty work, and use host worktree
  tools where applicable. Reset/cleanup instructions apply only within authorized
  scope and verified owned paths.
- Follow native Windows tooling and the hidden runner for Windows projects. Bundled
  Bash templates are source examples; adapt them to PowerShell for Windows rather
  than switching a Windows checkout to WSL. Launch an interactive terminal only
  when the user asks for one.
- `claude-handoff` and `git-guardrails-claude-code` are named-only Claude-targeted
  references, not Codex capabilities. Do not run Claude or install its hooks merely
  to provide a Codex handoff or safety policy. Explain the host difference and use
  an available Codex alternative that fits the actual request.
- Use actual context and host capabilities. Ignore fixed upstream context limits
  and do not issue imaginary `/clear` or `/compact` tool calls.
- Setup is conditional on missing required configuration. Do not install tracker
  labels or edit instruction files just because this collection was selected.
- Preserve explicit product/tool choices. For UI implementation, honor the user's
  existing design workflow and Title Case English UI copy. A Matt prototype may
  use the existing design capability without replacing it.
- In Chinese prose, keep technical/workflow terms in English and always write
  `ticket`. Source uses of "issue" mean the repository's actual tracker entity.

The source lock and file hashes are in `sources.json`; preserve the bundled MIT
license and `engineering/pr/CREDITS.md`. The fork and upstream have identical
workflow content at these commits. Only the root `SKILL.md` is discoverable.
