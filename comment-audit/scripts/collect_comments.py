#!/usr/bin/env python3
"""List comments with file, line and the code on that line. Read-only.

Usage:
  collect_comments.py repo [PATH ...]      every tracked file (default: whole repo)
  collect_comments.py diff [BASE]          comments on lines added vs BASE (default main), working tree included

Handles #, //, /* */ and <!-- --> comments, skipping string literals on one line.
It is a collector, not a classifier: it can miss exotic syntax (heredocs, regex
literals, template strings spanning lines). Read the file when in doubt.
"""
import json, re, subprocess, sys

SKIP = re.compile(r"(^|/)(node_modules|vendor|dist|build|\.git)/|\.(lock|min\.js|map|svg|png|jpg|pdf)$|(package-lock|pnpm-lock)\.")
HASH = {".py", ".sh", ".rb", ".yml", ".yaml", ".toml", ".r", ".pl"}
SLASH = {".js", ".jsx", ".ts", ".tsx", ".java", ".go", ".rs", ".c", ".h", ".cc", ".cpp", ".cs", ".swift", ".kt", ".php", ".css", ".scss"}
HTML = {".html", ".xml", ".vue"}

def ext(p):
    i = p.rfind(".")
    return p[i:].lower() if i >= 0 else ""

def scan(path, text):
    e = ext(path)
    hashc, slashc, htmlc = e in HASH, e in SLASH, e in HTML
    out, block, line_no = [], None, 0
    for raw in text.split("\n"):
        line_no += 1
        i, q, n = 0, None, len(raw)
        while i < n:
            c = raw[i]
            if block:
                end = raw.find(block, i)
                if end < 0:
                    out.append((line_no, raw[i:].strip())); i = n
                else:
                    out.append((line_no, raw[i:end].strip())); i = end + len(block); block = None
                continue
            if q:
                if c == "\\": i += 2; continue
                if c == q: q = None
                i += 1; continue
            if c in "\"'`" and not (c == "'" and hashc is False and slashc is False):
                q = c; i += 1; continue
            if hashc and c == "#":
                out.append((line_no, raw[i + 1:].strip())); break
            if slashc and raw.startswith("//", i):
                out.append((line_no, raw[i + 2:].strip())); break
            if slashc and raw.startswith("/*", i):
                block = "*/"; i += 2; continue
            if htmlc and raw.startswith("<!--", i):
                block = "-->"; i += 4; continue
            i += 1
    return [(ln, t, text.split("\n")[ln - 1].strip()) for ln, t in out if t]

def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True, check=True).stdout

def added_lines(base):
    res, cur = {}, None
    for l in git("diff", "-U0", base, "--").split("\n"):
        if l.startswith("+++ b/"): cur = l[6:]
        elif l.startswith("@@") and cur:
            m = re.search(r"\+(\d+)(?:,(\d+))?", l)
            s, c = int(m[1]), int(m[2] or 1)
            res.setdefault(cur, set()).update(range(s, s + c))
    return res

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "repo"
    rows = []
    if mode == "diff":
        base = sys.argv[2] if len(sys.argv) > 2 else "main"
        for f, lines in added_lines(base).items():
            if SKIP.search(f): continue
            try: txt = open(f, encoding="utf-8").read()
            except (OSError, UnicodeDecodeError): continue
            rows += [(f, *r) for r in scan(f, txt) if r[0] in lines]
    else:
        files = sys.argv[2:] or git("ls-files").split("\n")
        for f in filter(None, files):
            if SKIP.search(f): continue
            try: txt = open(f, encoding="utf-8").read()
            except (OSError, UnicodeDecodeError): continue
            rows += [(f, *r) for r in scan(f, txt)]
    print(json.dumps([{"file": f, "line": l, "comment": c, "code": k} for f, l, c, k in rows], indent=1))

main()
