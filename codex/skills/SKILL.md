---
name: skills
description: Matt Pocock workflows for debugging, TDD, code review, specs, ticket breakdown, module architecture, domain modeling, prototypes, research, handoffs and learning. One entrypoint with LLM selection and Jev help for ambiguity. Use when this collection fits or the user invokes $skills; not for installing or listing unrelated skills, generic UI styling or unrelated tasks.
---

# Skills

One entrypoint for Matt Pocock's collection. The current LLM owns the work and
chooses the relevant workflow; Jev supplies a bounded recommendation when needed.
Read [Codex compatibility](references/compatibility.md) before a workflow.

## Select The Workflow

- Honor a workflow explicitly named by the user. Resolve it in
  [the catalog](references/catalog.json); read its guide and only the dependencies
  needed for the task. No Jev call is needed for an explicit or settled choice.
- Otherwise choose the smallest fitting workflow from the map below. For ambiguous
  choices, use `scripts/route.py` with a short, non-sensitive task summary. It calls
  the existing installed Jev adapter, not another general LLM or a new provider.
- An explicit `$skills` invocation delegates the choice among the 27 promoted
  workflows to this router. Set `invoked: true` for that case. Without it, preserve
  each workflow's original implicit-invocation policy. Beta/misc workflows require
  the user to name the workflow; their full descriptions are in the catalog.
- The script returns a guide path, `no_match`, or `llm_required`. Treat a Jev result
  as a second opinion on the main LLM's workflow choice. On disagreement, recheck
  the request, invocation policy and guide evidence once, then make the final
  choice without another Jev call. For `llm_required`, select using the catalog
  and task evidence; don't loop, change models, or ask for routine permission.
  For no match, continue normally with any applicable installed capability.
- State the chosen workflow briefly. Read its full guide before executing it.
  Follow dependencies as reference reads, not fresh catalog selections. Re-route
  only when the objective changes or the next phase needs a different workflow.
- Reuse an existing Jev workflow recommendation for the same task. An outer hook
  that selected this umbrella has not yet selected its internal workflow; these
  different routing layers are not a disagreement. Failure or fallback is an
  abstention, not a competing route.

`native-review` owns admitted code review. The collection's `code-review` guide can
inform that work, but does not add a parallel reviewer or replace its evidence owner.
A routing disagreement alone does not authorize code review.

## Workflow Map

| Task | Starting Workflow |
| --- | --- |
| Hard bug, regression, intermittent failure | [diagnosing-bugs](references/engineering/diagnosing-bugs/guide.md) |
| Concrete behavior and regression tests | [tdd](references/engineering/tdd/guide.md) |
| Implement one scoped spec or ticket | [implement](references/engineering/implement/guide.md) |
| Implement a spec's existing ticket graph | [implement-spec](references/engineering/implement-spec/guide.md) |
| Review a branch, diff or PR | [code-review](references/engineering/code-review/guide.md) |
| Unclear idea or trade-off in a repository | [grill-with-docs](references/engineering/grill-with-docs/guide.md) |
| Challenge an idea without saved project docs | [grill-me](references/productivity/grill-me/guide.md) |
| Turn settled requirements into a spec | [to-spec](references/engineering/to-spec/guide.md) |
| Break an existing spec into tickets | [to-tickets](references/engineering/to-tickets/guide.md) |
| Large effort with unresolved decisions | [wayfinder](references/engineering/wayfinder/guide.md) |
| Incoming bug reports and requests | [triage](references/engineering/triage/guide.md) |
| Improve a module interface or test seam | [codebase-design](references/engineering/codebase-design/guide.md) |
| Survey architectural opportunities | [improve-codebase-architecture](references/engineering/improve-codebase-architecture/guide.md) |
| Domain terms, glossary or ADRs | [domain-modeling](references/engineering/domain-modeling/guide.md) |
| Answer one design question with runnable code | [prototype](references/engineering/prototype/guide.md) |
| Primary-source research | [research](references/engineering/research/guide.md) |
| PR description and evidence | [pr](references/engineering/pr/guide.md) |
| Session retrospective | [retro](references/engineering/retro/guide.md) |
| Handoff document | [handoff](references/productivity/handoff/guide.md) |
| Teach a concept across sessions | [teach](references/productivity/teach/guide.md) |
| Explain a confusing answer | [wait-what](references/productivity/wait-what/guide.md) |
| Questionnaire for someone else's knowledge | [to-questionnaire](references/productivity/to-questionnaire/guide.md) |
| Agent instructions and documentation | [writing-for-agents](references/productivity/writing-for-agents/guide.md) |

For the remaining workflows and exact invocation policies, read
[the full index](references/index.md). Read
[ask-matt](references/engineering/ask-matt/guide.md) only when the relationship
between phases itself needs explanation. A settled ticket does not need the
whole idea-to-spec-to-tickets flow.

## Jev Invocation

Read the installed `jev` skill before first Jev use unless already loaded.
The input may come from stdin or `--input`; never put private task text in argv.
Example JSON for an explicitly invoked umbrella:

```json
{"request":"Find why our test sometimes fails; choose diagnosis or implementation.","invoked":true,"candidates":["diagnosing-bugs","implement","tdd"]}
```

Omit `candidates` to consider all eligible workflows. Supply `workflow` only
when the user explicitly named that workflow. `--catalog` prints metadata
without inference.

On Windows, run with the actual Python interpreter through the hidden runner:

```powershell
& "C:\Users\Marck\.codex\bin\invoke-hidden.ps1" -FilePath (Get-Command python.exe).Source -ArgumentList @("-B", "<skill-dir>\scripts\route.py", "--input", "<workspace>\route-input.json") -WorkingDirectory "<workspace>"
```

On other hosts, use their native Python and workspace rules. The adapter uses
the existing Jev credentials and disables; no credentials, provider settings,
hooks or main-model settings are changed by this skill.
