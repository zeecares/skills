---
name: verification-skill-builder
description: Build a project-local verification skill for any repo - a skill that lets an agent start the real app, drive it the way a user would, and capture proof that features work. Use when a project has no scripted way to prove its own behavior, when the user asks for a verify/control skill for a repo, or before trusting agent-made changes to an app.
---

# Verification skill builder

A verification skill is a small skill that lives inside a project and teaches the next agent how to prove the app works: start it, use a feature like a real user, capture evidence, clean up. It exists because "the tests pass" and "the code looks right" are not proof that the app behaves. The reader is always an agent that has never seen the repo, arriving mid-task, so write for cold reading: exact commands, no assumed context.

This builder produces that skill for a given repo. Studied from Cursor's `create-verification-skill` (https://github.com/cursor/plugins/blob/main/pstack/skills/create-verification-skill/SKILL.md) - same goal, own structure.

## 1. Interrogate the repo, not the user

Answer five questions from the codebase itself. Ask the user only what you genuinely cannot observe.

- **Surface** - what does a user touch? Web UI, CLI/TUI, API, desktop app, mobile app, library. Pick the primary surface, note the rest.
- **Run** - how does it start locally? Trust the repo's own docs first (package scripts, Makefile, README quickstart). Record ports, env vars, seed data, auth needs.
- **Drive** - how can an agent operate it without a human? Prefer harnesses the repo already has (Playwright/Cypress specs, expect scripts, CLI subcommands, debug ports). Generic fallbacks: browser/CDP for web and Electron, tmux or a PTY for CLI/TUI, plain HTTP for services.
- **Observe** - what counts as evidence? Screenshots, terminal transcripts, response bodies, logs, exit codes, database state, files written.
- **Isolate** - can two instances run side by side (ports, data dirs, profiles)? If not, the generated skill must say so. Refusing to drive a shared instance beats corrupting the user's session.

If the checkout does not build or start, fix that first or report it exactly. A skill written against a broken base teaches wrong steps.

## 2. Write the skill

Write `verify/SKILL.md` inside the project's skills directory (`.cursor/skills/verify/`, `.claude/skills/verify/`, or the agent's equivalent). Frontmatter is mandatory - `name` and a `description` naming the app, the surface, and when to reach for it; without it the skill never registers. Then these sections, each grounded in what step 1 found. No placeholders.

- **Launch** - the exact start command, how to tell it is ready (a log line, a port answering, a prompt), and how to stop it. For a short-lived CLI, "launch" means build once, then run each drive in its own PTY or tmux session.
- **Doctor** - one read-only health check: process up, right build, port owned by this run, auth valid. First thing an agent runs when anything looks off.
- **Drive** - the harness recipe using this repo's real selectors and commands, never generic examples. Stable handles only: ARIA labels, data attributes, prompt strings, route paths. No coordinates, no tab order.
- **Evidence** - what to capture and where it goes. State the proof bar: drive the real user path, not internal setters or test-only endpoints; capture the action and the resulting state, not just the final screen; check side effects (files, rows, messages) alongside what is visible. If the safe path is a dry-run mode, verify what it actually skips by observing, not by trusting its name.
- **Cleanup** - kill only what the run started, never by process name. Evidence survives cleanup; name where it lives.
- **Helpers** - any shipped script is executable and its invocation appears in the skill body. A helper the reader must reverse-engineer is not a helper.

## 3. Seed the feature map

Create `verify/features/` with an index README plus one file per user-facing feature, top 3-5 to start (from routes, commands, menus, docs). Each feature file answers from the user's point of view:

1. **What it does** - one paragraph of user-visible behavior.
2. **Entry points** - every way a user reaches it (button, shortcut, CLI command).
3. **Driving recipe** - preconditions, then paired steps: user action, exact command, observable result.
4. **Proof of done** - the end state and artifacts that prove it.
5. **Traps** - what wastes or invalidates a run (debounces, focus rules, shared state).

Keep implementation details out of the map: user paths, stable handles, commands, observable proof only. A proof that drives one convenient entry point is incomplete when the map lists others.

## 4. Prove the skill before handing it over

Run its own instructions end to end once: launch, doctor, drive one mapped feature, capture evidence, clean up. Then confirm the evidence still exists where the skill said it would. Fix what fails, and run cleanup after every failed iteration so broken attempts do not strand processes. A verification skill that was never executed is a draft, not a deliverable.

## 5. Handoff

Tell the user where the skill lives, which feature was proven, and where the evidence is. Suggest re-running the builder (or editing the feature map) when the app gains user-facing features. Do not set a maintenance cadence unless asked.
