# Fixture: expected sorting

Run the audit on `fixture/` (repo mode). A correct audit sorts like this. Anything else is worth a look.

| File:line | Comment | Bucket | Why |
| --- | --- | --- | --- |
| a.py:1 | Copyright header | Keep | Legal header |
| a.py:5 | loop over items and add up price | Delete | Narrates the code |
| a.py:7 | iterate | Delete | Narrates the code |
| a.py:12 | HACK: vendor API returns 200 with an error body (issue link) | Keep, after a check | Vendor behavior we cannot change plus an issue link. Confirm the code really does check the body; if not, the comment is stale |
| a.py:14 | IMPORTANT do not remove, order matters | Workaround | Scent, no proven reason. Trace `data = r.json()`; if nothing depends on order, delete and flag |
| a.py:16 | x = old_call() | Delete | Commented-out code |
| a.py:20 | increment x | Delete | Narrates the code |
| a.py:21 | fine for now | Workaround | Excuses `new()`; flag, do not just delete |
| b.ts:1 | Public API doc comment | Keep | API contract |
| b.ts:3 | @ts-ignore | Workaround | Suppresses a real error (`u.nmae` is a typo): fix the symbol, then the suppression goes |
| b.ts:4 | TODO fix typo later | Workaround | Same typo; one fix removes both |
| b.ts:5 | trailing real comment | Delete | Narration of nothing useful |
| b.ts:6-7 | multi line | Delete | Empty narration |

Traps the collector must not fall for: `"# not a comment"` (a.py:13) and `"http://x.com//path"` (b.ts:5) are strings, not comments.

Diff mode check: on branch `feat` of this fixture (the last commit adds `new()`), diff mode against `main` must list only a.py:20 and a.py:21.

Pass bar: no Keep deleted, no application code edited in the default audit, every Workaround flagged with its symbol rather than silently deleted.
