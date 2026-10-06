# skills

Agent skills by Ziyi Wang. One folder per skill. Each has a `SKILL.md` in the Agent Skills format, so Claude Code, Codex, Cursor and similar agents can load it.

| Skill | What it does |
| --- | --- |
| [trad-tune-playalong](trad-tune-playalong/) | Turn sheet music into a play-along page: chords, audio, and printable PDFs. Irish trad specifics live in its `trad/` folder. |
| [verification-skill-builder](verification-skill-builder/) | Study a repo and write a project-local skill that teaches agents to prove the app works by driving it. |

## Install

No package install. A skill is a folder with a `SKILL.md`; your agent registers it from the name and description in the frontmatter.

```
git clone https://github.com/zeecares/skills.git
cd skills
```

Copy the skill folder you want into your agent's skills directory. Project-level is `.claude/skills/` (Claude Code) or `.cursor/skills/` (Cursor). For every project, use the global one, for example `~/.claude/skills/` or `~/.cursor/skills/`. Other agents that read `SKILL.md` work the same way.

```
# trad-tune-playalong
mkdir -p .claude/skills && cp -r trad-tune-playalong .claude/skills/

# verification-skill-builder
mkdir -p .claude/skills && cp -r verification-skill-builder .claude/skills/
```

Swap `.claude` for `.cursor` or your agent's folder. Restart the agent or start a new session, then ask for the task (for example "build a verification skill for this repo") and the skill loads when its description matches.

## Layout

```
skill-name/
  SKILL.md        required: name, description, instructions
  references/     optional: longer docs loaded on demand
  examples/       optional: small working samples
```

## Credits

verification-skill-builder was written after studying Cursor's create-verification-skill: https://github.com/cursor/plugins/blob/main/pstack/skills/create-verification-skill/SKILL.md

## License

MIT, see [LICENSE](LICENSE).
