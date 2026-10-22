# Workflow Index

Read only the chosen workflow and its required dependencies.

## Engineering

- [ask-matt](engineering/ask-matt/guide.md) (umbrella invocation): Ask which skill or flow fits your situation. A router over the skills in this repo.
- [code-review](engineering/code-review/guide.md) (implicit): Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes: Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/spec asked for?). Runs both reviews in parallel sub-agents and reports them side by side. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to "review since X".
- [codebase-design](engineering/codebase-design/guide.md) (implicit): Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening opportunities, decide where a seam goes, make code more testable or AI-navigable, or when another skill needs the deep-module vocabulary.
- [diagnosing-bugs](engineering/diagnosing-bugs/guide.md) (implicit): Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something broken/throwing/failing/slow.
- [domain-modeling](engineering/domain-modeling/guide.md) (implicit): Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a GLOSSARY.md, or recording or editing an ADR.
- [grill-with-docs](engineering/grill-with-docs/guide.md) (umbrella invocation): A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go.
- [implement-spec](engineering/implement-spec/guide.md) (umbrella invocation): Implement the result of /to-spec and /to-tickets in code.
- [implement](engineering/implement/guide.md) (umbrella invocation): Implement a piece of work based on a spec or set of tickets.
- [improve-codebase-architecture](engineering/improve-codebase-architecture/guide.md) (umbrella invocation): Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick.
- [pr](engineering/pr/guide.md) (implicit): Use when writing a PR body.
- [prototype](engineering/prototype/guide.md) (implicit): Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels right, or explore what a UI should look like.
- [research](engineering/research/guide.md) (implicit): Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent.
- [retro](engineering/retro/guide.md) (umbrella invocation): Conduct a retrospective on a coding session.
- [setup-matt-pocock-skills](engineering/setup-matt-pocock-skills/guide.md) (umbrella invocation): Configure this repo for the engineering skills: set up its issue tracker, triage label vocabulary, and domain doc layout. Run once before first use of the other engineering skills.
- [tdd](engineering/tdd/guide.md) (implicit): Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration tests.
- [to-spec](engineering/to-spec/guide.md) (umbrella invocation): Turn the current conversation into a spec and publish it to the project issue tracker: no interview, just synthesis of what you've already discussed.
- [to-tickets](engineering/to-tickets/guide.md) (umbrella invocation): Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published to the configured tracker (edges as text in one file per ticket locally, or native blocking links on a real tracker).
- [triage](engineering/triage/guide.md) (umbrella invocation): Move issues and external PRs through a state machine of triage roles, categorise, verify, grill if needed, and write agent-ready briefs.
- [wayfinder](engineering/wayfinder/guide.md) (umbrella invocation): Plan a huge chunk of work (more than one agent session can hold) as a shared map of decision tickets on your issue tracker, and resolve them one at a time until the way to the destination is clear.
- [wizard](engineering/wizard/guide.md) (implicit): Generate an interactive bash wizard that walks a human through steps only they can perform. Use when provisioning infrastructure, setting up credentials or CI secrets, walking an unfamiliar third-party dashboard, or running a one-off migration or cutover. Don't invoke this for steps the agent can perform itself.

## Productivity

- [grill-me](productivity/grill-me/guide.md) (umbrella invocation): A relentless interview to sharpen a plan or design.
- [grilling](productivity/grilling/guide.md) (implicit): Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
- [handoff](productivity/handoff/guide.md) (umbrella invocation): Compact the current conversation into a handoff document for another agent to pick up.
- [teach](productivity/teach/guide.md) (umbrella invocation): Teach the user a new skill or concept, within this workspace.
- [to-questionnaire](productivity/to-questionnaire/guide.md) (umbrella invocation): Turn a decision you can't fully answer into a questionnaire for someone else to fill in.
- [wait-what](productivity/wait-what/guide.md) (umbrella invocation): Stop. That last message did not land: re-pitch it.
- [writing-for-agents](productivity/writing-for-agents/guide.md) (implicit): Writing documents for agents. Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md.

## In Progress

- [chief-of-staff](in-progress/chief-of-staff/guide.md) (named-only): Pursue a long-running goal in a single session by co-ordinating subagents.
- [claude-handoff](in-progress/claude-handoff/guide.md) (named-only): Hand the current conversation off to a fresh background agent that picks up the work immediately.
- [loop-me](in-progress/loop-me/guide.md) (named-only): Grill me about specs for the workflows I want to build, within this workspace.
- [setup-ts-deep-modules](in-progress/setup-ts-deep-modules/guide.md) (named-only): Wire dependency-cruiser into a TypeScript repo so each package is a deep module, with implementation hidden in subfolders and reachable only through its entry-point files. User-invoked.
- [writing-beats](in-progress/writing-beats/guide.md) (named-only): Writing, exploit; assemble raw material into a journey of beats, grounding each term before a beat leans on it.
- [writing-fragments](in-progress/writing-fragments/guide.md) (named-only): Writing, explore: mine raw fragments, no structure yet.
- [writing-shape](in-progress/writing-shape/guide.md) (named-only): Writing, exploit: shape raw material into an article, paragraph by paragraph.

## Misc

- [git-guardrails-claude-code](misc/git-guardrails-claude-code/guide.md) (named-only): Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) before they execute. Use when user wants to prevent destructive git operations, add git safety hooks, or block git push/reset in Claude Code.
- [migrate-to-shoehorn](misc/migrate-to-shoehorn/guide.md) (named-only): Migrate test files from `as` type assertions to @total-typescript/shoehorn. Use when user mentions shoehorn, wants to replace `as` in tests, or needs partial test data.
- [scaffold-exercises](misc/scaffold-exercises/guide.md) (named-only): Create exercise directory structures with sections, problems, solutions, and explainers that pass linting. Use when user wants to scaffold exercises, create exercise stubs, or set up a new course section.
- [setup-pre-commit](misc/setup-pre-commit/guide.md) (named-only): Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the current repo. Use when user wants to add pre-commit hooks, set up Husky, configure lint-staged, or add commit-time formatting/typechecking/testing.
