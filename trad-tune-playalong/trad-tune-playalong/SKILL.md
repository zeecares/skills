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
- Per piece: title, sheet with full-size view, optional chord panel, then a compact player. Skeleton: [examples/player.html](examples/player.html).
- Player: play/pause, a draggable seek bar, current and total time, pitch-preserving speed controls.
- Play-along cursor: follows bars through the count-in, pickups, repeats and endings. Seeking and speed changes update both the cursor and current chord.
- Chord diagrams for the requested instrument (guitar, ukulele, mandolin and so on). Check every displayed voicing produces the named chord, with string order and fret numbers clear.
- Allow only one piece to play at a time.
- Aim to fit a card on a phone screen without making notation unreadable. Preserve a full-size sheet view; allow scrolling for long or dense sheets.
- Match the requested visual style.

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
- [ ] Final report lists what was heard by ear and what was not.
- [ ] Rights check below done; link returns the working page.

Choose hosting by access, asset size, licensing and maintenance needs. A static page needs no server code. Publish only to the intended audience. Keep source files for later edits. Distinguish simulated pointer checks from real phone touch tests.

## Rights and limitations
- Check permission before publishing scans, arrangements, recordings or copied chord material. Traditional melodies do not automatically make a modern edition or recording free to redistribute.
- Link to comparison sources and retain provenance. Do not bundle third-party source material without permission.
- Label approximate bar coordinates or estimated timing. Do not hide unresolved musical uncertainty behind a polished page.
