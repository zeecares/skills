---
name: comment-audit
description: Audit the comments in a repo or a diff, delete the ones the code already says, and flag the ones that hide a workaround so the workaround can be fixed instead. Use when the user asks to clean up, prune or audit comments, or to review a PR for comment smells. Manual only; goal is the fewest useful comments, never a lower comment count for its own sake.
---

# Comment audit

A comment is a smell. Sometimes it repeats the code. More often it apologizes for code that should be different: a workaround, a surprise, a "do not touch". The comment lets the workaround stay. So read each comment as a pointer to what is wrong underneath, and fix that first. The comment then has nothing left to say.

The target is the fewest useful comments. Do not chase a number. A repo that ends with more comments than it started with is fine if each one earns its place. A deletion needs a reason from the buckets below, never "there are too many".

## 1. Pick the scope

- **Diff mode** (default when the user mentions a PR, branch or "my changes"): comments added or changed against the base branch (default `main`), including the working tree.
- **Repo mode** (when the user says whole repo, or there is no diff): every tracked source file. Skip vendored code, generated files, lockfiles and fixtures.

State the scope back in one line before starting. Touch nothing outside it.

## 2. Collect

List every comment in scope with file, line and the code it sits on. Include doc comments, block comments, TODOs, commented-out code and lint or type suppressions (`eslint-disable`, `@ts-ignore`, `# noqa`, `# type: ignore` and the like).

## 3. Sort each comment into one bucket

Read the nearby code first. If the comment makes a claim the code does not show, trace the symbol it names before judging.

| Bucket | What it is | Action |
| --- | --- | --- |
| **Keep** | Legal or license header. Doc comment that defines a public API contract. Non-obvious behavior forced by something we cannot change (a vendor API, a platform quirk, a protocol) and still true today. Link to an issue or RFC that explains a constraint the code cannot express. Style-only or faulty lint suppression. Safety, security or compliance note. | Leave it. Say why in one line. |
| **Delete** | Narrates what the code plainly does. Banner or divider. Commented-out code. Stale or wrong. Restates the name of the function below it. | Delete the comment only. |
| **Workaround** | Explains a surprise in our own code: "careful, this is order dependent", "hack", "do not remove", "fine for now", a long justification, or a suppression of a rule that catches real bugs. | Delete nothing yet. Flag it (step 4). |
| **Decision** | Records why a design was chosen, with real history behind it. | Suggest moving it to an ADR or the commit message. Do not delete until it has a home. |

When a keep is doubtful, do not trust the comment's own claim. Check it against the code. If the claim is false or cannot be shown, it is not a keep.

## 4. Fix causes before comments

For each Workaround, name the exact symbol it excuses and the smallest change that makes the behavior obvious without prose: a rename, an extracted function, a type, a test, a parameter dropped, a dead path removed. Then:

- In **report mode** (default), list the flag and the proposed change. Change no application code.
- If the user asks you to fix, make the smallest in-scope fix, then delete the comment. If the root cause is outside scope, report it open and leave the comment.
- If the comment guards a constraint ("do not change wording", "talk to X first") that we cannot change, offer the cheapest check that enforces it in code (a type, test or lint rule). Encode it only with the user's yes, then delete the comment. Without a yes, keep the comment and report the constraint as unenforced.

## 5. Apply

By default, apply only the **Delete** bucket, and only comment text. Never edit application code in the same pass unless the user asked for fixes. After deleting, run the project's formatter, lint and tests if they exist and confirm nothing else changed (`git diff` should show comment lines removed and nothing more).

## 6. Report

Short, in this order:

1. Scope and mode.
2. Counts per bucket, with the number actually deleted.
3. Deleted comments that were stale or wrong, listed (these are worth the user's attention).
4. Workaround flags, one line each: symbol, what it excuses, proposed change.
5. Decisions that need an ADR.
6. Keeps that looked doubtful, with the check you ran.
7. Anything left open.

Never report "comments reduced by N%" as a result. Report what was wrong and what was fixed.

## Do not

- Delete a comment to hit a target.
- Delete a keep because it is long.
- Polish a workaround comment into a shorter excuse.
- Treat code the user kept on purpose as guilty.
- Run unattended or on a merge pipeline unless the caller has said so in advance.

## Credit

The bucket rules and the "comment as workaround smell" framing are adapted, in our own words, from Lauren Tan's `no-comments` skill and `comment-sicko` agent in pstack (MIT): https://github.com/cursor/plugins/tree/main/pstack. The idea of treating comments as smells came up in Matt Pocock's comment audit: https://www.youtube.com/watch?v=jVBlkOF8sHk
