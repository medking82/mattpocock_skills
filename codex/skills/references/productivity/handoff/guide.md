> Source: [skills/productivity/handoff/SKILL.md](https://github.com/medking82/mattpocock_skills/blob/3a91e1138de4b6c86988e24a643b00054592207f/skills/productivity/handoff/SKILL.md). Adapted for the single skills entrypoint.
> Apply [Codex compatibility](../../compatibility.md) before these source instructions.

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to the temporary directory of the user's OS (`$TMPDIR`, else `/tmp`; `%TEMP%` on Windows) - not the current workspace.

Include a "suggested skills" section in the document, naming which skills the next agent should call the Skill tool for.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.
