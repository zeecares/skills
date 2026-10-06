# Example: a generated verify skill (filled in)

What step 2-3 output looks like for a small notes web app. Use it as a shape reference, not a template to copy blindly - every command below came from interrogating that repo.

---
name: verify-notes-app
description: Drive the Notes web app like a user and prove features work. Use before trusting any change to notes-app, or when asked to confirm UI behavior.
---

## Launch
- `npm run dev` from the repo root. Ready when the log prints `Listening on :4173` (about 3s).
- Always launch with a throwaway data dir: `NOTES_DATA_DIR=/tmp/notes-verify-$RUN_ID npm run dev`.
- Stop with `kill $PID` on the process you started.

## Doctor
- `curl -s localhost:4173/health` returns `{"ok":true,"rev":"<sha>"}`. Check `rev` matches the checkout (`git rev-parse --short HEAD`) so you are not driving someone else's instance.

## Drive
- Playwright against `http://localhost:4173`. Select by ARIA role and accessible name (`getByRole('button', { name: 'New note' })`). The app has no test ids; ARIA names are the stable handles.
- CLI alternative: `node bin/notes.js <command>` reads the same data dir.

## Evidence
- Proof lives in `/tmp/notes-verify-$RUN_ID/artifacts/`.
- Per feature: one screenshot showing the action result, plus a side-effect check (file in the data dir or CLI read-back). A screenshot of the final screen alone is not proof.

## Cleanup
- Kill the dev server you started, remove `/tmp/notes-verify-$RUN_ID/data`, keep `artifacts/`.
- Never `pkill node`. The user runs their own instance on :3000.

## Features
- features/README.md indexes create-note.md and search.md (the top user paths from the routes file).
