---
name: skills
description: Matt Pocock workflows for debugging, TDD, code review, specs, ticket breakdown, module architecture, domain modeling, prototypes, research, handoffs and learning. One entrypoint where the main LLM selects the workflow. Use when this collection fits or the user invokes $skills; not for installing or listing unrelated skills, generic UI styling or unrelated tasks.
---

# Skills

One entrypoint for Matt Pocock's collection. The current LLM owns the work and
chooses the relevant workflow.
Read [Codex compatibility](references/compatibility.md) before a workflow.

## Select The Workflow

- Honor a workflow explicitly named by the user. Resolve it in
  [the catalog](references/catalog.json); read its guide and only the dependencies
  needed for the task.
- Otherwise choose the smallest fitting workflow from the map below. For ambiguous
  choices, compare the catalog descriptions and invocation policies. Choose by the
  requested outcome and current phase, not just shared words, and do not add
  interviews, planning or implementation the user did not ask for.
- An explicit `$skills` invocation delegates the choice among the promoted
  workflows to the current LLM. Without it, preserve each workflow's original
  implicit-invocation policy (`implicit` in the catalog). Beta/misc workflows
  require the user to name the workflow; their full descriptions are in the catalog.
- Make the choice once; don't loop, change models, or ask for routine permission.
  When no workflow fits, continue normally with any applicable installed capability.
- State the chosen workflow briefly. Read its full guide before executing it.
  Follow dependencies as reference reads, not fresh catalog selections. Re-route
  only when the objective changes or the next phase needs a different workflow.
- An outer hook that selected this umbrella has not yet selected its internal
  workflow; make that choice here.

`native-review` owns admitted code review. The collection's `code-review` guide can
inform that work, but does not add a parallel reviewer or replace its evidence owner.

## Workflow Map

<!-- workflow-map:start -->
| Task | Starting Workflow |
| --- | --- |
| Hard bug, regression, intermittent failure | [diagnosing-bugs](references/engineering/diagnosing-bugs/guide.md) |
| Concrete behavior and regression tests | [tdd](references/engineering/tdd/guide.md) |
| Implement one scoped spec or ticket | [implement](references/engineering/implement/guide.md) |
| Implement a spec's existing ticket graph | [implement-spec](references/engineering/implement-spec/guide.md) |
| Review a branch, diff or PR | [code-review](references/engineering/code-review/guide.md) |
| Unclear idea or trade-off in a repository | [grill-with-docs](references/engineering/grill-with-docs/guide.md) |
| Challenge an idea without saved project docs | [grill-me](references/productivity/grill-me/guide.md) |
| Quick stress-test of a plan, decision or idea on a 'grill' request | [grilling](references/productivity/grilling/guide.md) |
| Turn settled requirements into a spec | [to-spec](references/engineering/to-spec/guide.md) |
| Break an existing spec into tickets | [to-tickets](references/engineering/to-tickets/guide.md) |
| Large effort with unresolved decisions | [wayfinder](references/engineering/wayfinder/guide.md) |
| Incoming bug reports and requests | [triage](references/engineering/triage/guide.md) |
| Set up a repo's issue tracker, triage labels and domain docs for these workflows | [setup-matt-pocock-skills](references/engineering/setup-matt-pocock-skills/guide.md) |
| Improve a module interface or test seam | [codebase-design](references/engineering/codebase-design/guide.md) |
| Survey architectural opportunities | [improve-codebase-architecture](references/engineering/improve-codebase-architecture/guide.md) |
| Domain terms, glossary or ADRs | [domain-modeling](references/engineering/domain-modeling/guide.md) |
| Answer one design question with runnable code | [prototype](references/engineering/prototype/guide.md) |
| Primary-source research | [research](references/engineering/research/guide.md) |
| Guided script for steps only a human can do: credentials, CI secrets, dashboards | [wizard](references/engineering/wizard/guide.md) |
| PR description and evidence | [pr](references/engineering/pr/guide.md) |
| Session retrospective | [retro](references/engineering/retro/guide.md) |
| Handoff document | [handoff](references/productivity/handoff/guide.md) |
| Teach a concept across sessions | [teach](references/productivity/teach/guide.md) |
| Explain a confusing answer | [wait-what](references/productivity/wait-what/guide.md) |
| Questionnaire for someone else's knowledge | [to-questionnaire](references/productivity/to-questionnaire/guide.md) |
| Agent instructions and documentation | [writing-for-agents](references/productivity/writing-for-agents/guide.md) |
| How the workflow phases relate to each other | [ask-matt](references/engineering/ask-matt/guide.md) |
<!-- workflow-map:end -->

For the remaining workflows and exact invocation policies, read
[the full index](references/index.md). Read
[ask-matt](references/engineering/ask-matt/guide.md) only when the relationship
between phases itself needs explanation. A settled ticket does not need the
whole idea-to-spec-to-tickets flow.
