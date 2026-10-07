---
name: trad-tune-playalong
description: Turn sheet music (scans or PDFs) into a mobile play-along practice page with checked chords, synthesized audio, a bar-following cursor, speed control and chord diagrams. Works for any sheet music; an Irish trad pack adds session sources, bodhran and mandolin. Use when someone shares sheet music and wants to practice along, add chords, clean up handwriting, or build a practice site.
---

# Sheet music play-along

Build from the supplied musical setting, not a different online version. Keep uncertain notes, chords, timing and image edits visible for review.

For Irish or other traditional tunes, also read [trad/README.md](trad/README.md). Everything below works without it.

## 0. Tools
Check what is installed before starting. If a tool is missing, install it or use the fallback. Do not skip a step silently.

| Need | Preferred | Install hint | Fallback |
|---|---|---|---|
| PDF to image | `pdftoppm` (poppler) | `apt install poppler-utils` / `brew install poppler` | PyMuPDF (`pip install pymupdf`) |
| ABC to MIDI | `abc2midi` (abcmidi) | `apt install abcmidi` / `brew install abcmidi` | `music21` or `mido` in Python, writing MIDI from your own note list |
| ABC to sheet SVG/PDF | `abcm2ps` | `apt install abcm2ps` | abcjs in the browser (`npm i abcjs`), or LilyPond (`apt install lilypond`) |
| MIDI to audio | `fluidsynth` + a General MIDI soundfont (e.g. `fluid-soundfont-gm`) | `apt install fluidsynth fluid-soundfont-gm` | `timidity`, or play MIDI live in the page with a Web Audio synth (abcjs synth) |
| Encode audio | `ffmpeg` | `apt install ffmpeg` | `lame` for MP3, `oggenc` for OGG |
| Browser checks | Playwright or any headless Chrome | `pip install playwright && playwright install chromium` | Manual screenshots at 390px |

State in your report which tools you used and which fallbacks you took.

## 1. Read the sheets
- Render each PDF page as an image. Read scans visually and enlarge unclear bars.
- Transcribe the melody from the supplied sheet into ABC. Online settings are comparison aids, not substitutes. See [examples/tune.abc](examples/tune.abc).
- Check key signatures, accidentals, meter, pickups, repeats and alternate endings before rendering audio. Ask about unreadable passages rather than inventing notes.

## 2. Check chords
- If a source setting exists, verify the melody and arrangement match it. A matching title or bar count alone is not enough.
- Transpose source chords when needed, then check them against the supplied melody bar by bar. Include repeats and alternate endings.
- Use one or two chords per bar where musically appropriate. Several accompaniments can be valid.
- Label chords as source-checked, suggested, or unverified. Never present suggested chords as a teacher's chords.

## 3. Clean the sheet
- Keep an untouched copy. Remove handwriting only when requested; preserve printed notation, titles and other requested markings.
- Inspect the edited image beside the original to catch deleted notes, staff lines or printed text.
- Transcribe handwritten chords only when legible. Flag any removed musical information.
- Use one chord data set to drive labels above the bars and chord diagrams. See [examples/chords.json](examples/chords.json). Avoid conflicting labels baked into images.

## 4. Render audio
- Render from the transcribed melody: ABC to MIDI to audio (see Tools).
- Provide a clear melody and optional quiet click. Use the requested tempo; otherwise start at a moderate practice tempo, such as 72 BPM, stating whether beats are quarter notes or dotted quarters.
- Include a two-bar count-in, correctly timed pickups, printed repeats and alternate endings.
- Check durations and opening pitches programmatically, and listen when possible. State exactly what was and was not checked. Never imply an unheard render was checked by ear.

## 5. Build the mobile practice page
- Per piece: title, sheet with full-size view, optional chord panel, then a compact player. Single-track sketch: [examples/player.html](examples/player.html). It is not a multi-part engine; do not duplicate its audio elements for every tune and instrument.
- Player: play/pause, a draggable seek bar, current and total time, pitch-preserving speed controls.
- Play-along cursor: follows bars through the count-in, pickups, repeats and endings. Seeking and speed changes update both the cursor and current chord.
- Chord diagrams for the requested instrument (guitar, ukulele, mandolin and so on). Check every displayed voicing produces the named chord, with string order and fret numbers clear.
- Allow only one piece to play at a time.
- Aim to fit a card on a phone screen without making notation unreadable. Preserve a full-size sheet view; allow scrolling for long or dense sheets.
- Match the requested visual style.

## 5a. Multi-part playback and iOS
- Use one AudioContext and one shared clock for melody, accompaniment, drum, count-in, cursor and chord changes. Start sources at the same scheduled time. Do not run independent HTML audio clocks.
- Load and decode only the selected tune's parts. Stop old sources, cancel stale loads and release decoded and speed-rendered buffers on tune switch. Never preload a book as 110 audio elements.
- Give each part its own gain and mute control. Mute changes gain, not its clock or playback position. Label active states accessibly and keep controls inside the phone width.
- Preserve pitch during speed changes with a tested overlap/add time-stretcher (or another verified method). AudioBufferSource playbackRate alone changes pitch. Map stretched time back to the original score; rebuild all parts together after speed changes or seeking.
- Call AudioContext.resume() synchronously from the real Play gesture, before asynchronous loading or optional media setup. Only start parts and advance the cursor when the context is running; suspended/interrupted audio must not show false progress.
- Treat navigator.audioSession.type='playback' and a media-element unlock as optional routing hints. Isolate session access/assignment, Audio construction, play() synchronous throws and promise rejections, and cleanup in their own error handling. Never await optional play(), include it in Promise.all with resume(), or let it reject/delay the Web Audio path. A pending media promise must not hang Play.
- Judge success by context.state after the gesture resume attempt. A resume rejection with an already-running context need not block it. Error only when the required context cannot run, not when optional routing fails. Keep cleanup safe on pause, end and failure.
- Test normal start, audioSession getter/setter throws, media constructor throw, media play synchronous throw, rejection and permanently pending promise, cleanup throw, resume rejection with running context, and resume rejection or resolution with suspended context. The latter must block sources and cursor. Test interruption during playback too.
- Chrome mobile emulation is layout and logic evidence, not iPhone Safari or silent-switch proof. Check real hardware with silent mode both on and off when possible; report the gap otherwise. Do not claim a specific phone decoder failure without a captured trace.

## 5b. Mix audit
- Balance actual part energy, not only slider numbers. Keep accompaniment behind melody and make rhythm audible. Meter/RMS targets are project choices, not a universal artistic standard.
- Audit every full mix, not a single demo: measure part RMS and sample peaks, then oversampled peaks to catch inter-sample overs. Compute headroom from the actual speed-rendered buffers; protect every mute combination (a per-sample absolute-sum bound is one conservative method).
- Recheck after speed changes, part replacement and gain changes. State sample and oversampled peak results separately; listening remains a separate check.

## 6. Verify and deliver
Run this checklist. Each item is pass or fail; report any fail instead of shipping around it.

- [ ] Every bar of the transcription matches the supplied sheet (key, meter, pickup, repeats, endings).
- [ ] Rendered audio length matches the expected bars at the stated tempo, within one beat.
- [ ] First note of each audio file matches the first written pitch.
- [ ] Every chord label is tagged source-checked, suggested or unverified.
- [ ] Every chord diagram sounds the named chord (checked against `chords.json`).
- [ ] At 390px: no horizontal overflow, no clipped text, sheet readable.
- [ ] Scrubbing both ways puts the cursor and chord right at known bar lines, including repeats.
- [ ] Play/pause, speed change and track switching work; only one piece plays at once.
- [ ] Mixer mutes affect only the named part; seek, speed and switching keep all parts on the shared clock.
- [ ] Optional iOS routing failure tests pass; suspended/interrupted contexts do not advance sources or cursor.
- [ ] All full mixes and supported speed settings have documented sample and oversampled headroom.
- [ ] Final report lists what was heard by ear and what was not.
- [ ] Rights check below done; link returns the working page.

Choose hosting by access, asset size, licensing and maintenance needs. A static page needs no server code. Publish only to the intended audience. Keep source files for later edits. Distinguish simulated pointer checks from real phone touch tests.

## 7. Keep the source reproducible
- Version editable text sources and tune/chord/timing metadata, not only a bundled page. When using a source JSON snapshot, include a restore script and exact install/build commands.
- Put large audio/image binaries in versioned release assets when they do not belong in git. Record asset names, checksums, source revision and restore order; test a clean restore/build against the published version.
- Make one capability per branch/PR. Never commit directly to main. Self-review against the pre-change parent, fix catches with regression tests and report them. Merge only on the owner's approval or an applicable standing grant.
- A small patch applied after a baseline restore is acceptable if its base version is explicit and its output is checked byte-for-byte. Release notes must distinguish source changes, asset changes and already-published changes.

## Rights and limitations
- Check permission before publishing scans, arrangements, recordings or copied chord material. Traditional melodies do not automatically make a modern edition or recording free to redistribute.
- Link to comparison sources and retain provenance. Do not bundle third-party source material without permission.
- Label approximate bar coordinates or estimated timing. Do not hide unresolved musical uncertainty behind a polished page.
