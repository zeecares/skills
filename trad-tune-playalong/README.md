# trad-tune-playalong

A reusable skill for turning sheet music into a mobile play-along practice page. The main skill works for any sheet music; the [trad pack](trad/README.md) adds Irish session specifics.

The workflow covers tools and fallbacks, melody transcription, chord checks, scan cleanup, synthesized audio, a bar-following cursor, speed controls, chord diagrams and a pass/fail checklist. Examples are in [examples/](examples/).

## Playback and delivery

The workflow now includes selected-tune loading, one shared multi-part clock, per-instrument mutes, pitch-preserving speed, isolated best-effort iOS audio routing, failure-path tests and full-mix peak audits. The trad pack adds jig/reel guitar patterns and beginner D-whistle guidance.

The HTML example is a single-track sketch, not the production multi-part engine. Keep editable source and binary release assets reproducible, work through reviewed PRs, and distinguish desktop emulation from real phone testing.

## Use

Read [SKILL.md](SKILL.md), or add it to a coding assistant that supports Markdown skills. Supply sheet music you have permission to use and ask for a play-along practice page. The assistant needs suitable image, audio, coding and browser capabilities to carry out the steps.

This repository contains instructions, not a runnable generator or a collection of tunes. It does not include scans, recordings or third-party chord collections. Other instruments and musical styles may need different voicings and accompaniment patterns.

## Musical checks

The supplied setting is the starting point. Online versions can differ in key, melody, repeats or accompaniment. Chords are choices, not a single universal answer; uncertain material should stay labeled until checked.

Comparison sources:
- https://www.vashonceltictunes.net/irish/
- https://thesession.org/

## License

The original instructions in this repository are available under the [MIT license](../LICENSE). That license does not cover music, scans, recordings or other third-party material used with the workflow.

## Install

No package install. Copy this folder into your agent's skills directory, such as `.claude/skills/` or `.cursor/skills/` (or `~/.claude/skills/` for every project). The agent registers it from the `SKILL.md` frontmatter. Start a new session and ask for a play-along page.

```
cp -r trad-tune-playalong .claude/skills/
```

## Whistle references

For fingering-chart work, start with Grey Larsen's D-whistle chart: https://greylarsen.com/FreeDownloads/Fingering_Chart_with_Half-Hole_Fingerings.pdf . Its note says whistle pitches sound one octave above the written notes. Check whether a supplied sheet follows that convention before labeling octaves or comparing with piano.

Readable scale, register and alternate-fingering explanation: https://soundovia.com/tin-whistle-fingering-chart/ . Use a tuner on the actual whistle to check C natural and upper-register variants; do not copy diagrams without checking reuse rights.
