---
name: subtitle-plugin
description: Generate, test, validate, debug, and safely run the local subtitle plugin, including importing a verified final SRT into DaVinci Resolve. Use when the user says "字幕插件", asks to generate or test SRT output, verify subtitle timing/text quality, check repeated Chinese sentence-splitting bugs, import subtitles into DaVinci/Resolve, or summarize/fix recurring subtitle plugin feedback.
---

# Subtitle Plugin

Use this skill for the local project:

`C:\Users\Administrator\Documents\Codex\2026-06-16\files-mentioned-by-the-user-codex\script_forced_aligner`

## Core Contract

- Treat the source script as the only subtitle text source.
- Treat ASR as timing input only.
- Keep preprocessing structural: clean titles/markup and preserve explicit clause boundaries, but do not hard-cut an unknown phrase at an arbitrary character.
- If no verified semantic boundary exists, prefer one overlong subtitle with a warning over a broken word or incomplete grammatical phrase.
- Enforce text conservation: after intentional title/markup/punctuation cleanup, concatenated subtitle text must equal the cleaned source text; never silently drop an untimed subtitle.
- Never claim success from logs alone; inspect the actual target `.srt` file on disk.
- Keep trials in a temporary `work` directory. Copy only one verified final SRT into the user's project directory.
- Use a clear final filename such as `source_最终.srt`; do not expose trial versions to the user or DaVinci.
- If the user points out a bad subtitle, fix the category, add or adjust regression tests, regenerate, and self-check the real output.

## Standard Flow

1. Read the symptom and identify the bug category.
2. Inspect `debug/script_preprocessed.txt`, `debug/subtitle_segments.json`, and the target `.srt`.
3. Fix `src/script_preprocessor.py` if the issue exists in preprocessed text.
4. Fix `src/sentence_splitter.py` or `src/subtitle_builder.py` if the issue appears only after splitting.
5. Add regression tests for a newly found bug category.
6. Run regressions:

```powershell
$env:PYTHONIOENCODING='utf-8'
& 'C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest tests.test_sentence_splitter_regressions tests.test_script_preprocessor_regressions tests.test_resolve_integration
```

7. Run compile checks:

```powershell
$env:PYTHONPYCACHEPREFIX = Join-Path $env:TEMP 'subtitle_pycache_check'
& 'C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m py_compile main.py src\script_preprocessor.py src\sentence_splitter.py src\subtitle_builder.py src\resolve_integration.py
```

8. Run the real pipeline with a unique filename inside `work`.
9. Inspect the real candidate SRT: existence, size, modification time, SHA256, subtitle count, corrected phrases, bad fragments, non-positive durations, overlaps, duplicates, and abnormal reading speed.
10. Require diagnosis `PASS` before automatic Resolve import. Copy only the verified final SRT to the project directory and remove superseded plugin-generated versions there.
11. If Resolve is running, import the final SRT with `scripts/import_to_resolve.py`.
12. Report the final path, size, subtitle count, diagnosis, hash, checked snippets, and Resolve import status.

## Required Real-File Checks

Before delivery or Resolve import, verify:

- The final SRT exists and is larger than 0 KB.
- Subtitle count is greater than 0.
- Modification time matches the current run.
- Displayed samples come from the final SRT.
- `diagnose_report.json` says `PASS` with no drift risk blocks.
- There are no non-positive durations, overlaps, consecutive duplicate texts, or known bad splits.
- No boundary leaves an incomplete modal/adverb phrase such as `需要 / 同时...` or `共同 / 完成...`.
- Every cleaned short spoken line is present in the final SRT, including title-like speech and spaces inside unknown English phrases.
- If any non-empty subtitle lacks timing, stop delivery instead of writing a partial SRT.

## DaVinci Resolve Auto-Import

After all checks pass, run:

```powershell
$env:PYTHONIOENCODING='utf-8'
& 'C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  'C:\Users\Administrator\.codex\skills\subtitle-plugin\scripts\import_to_resolve.py' `
  '<FINAL_SRT_PATH>' --expected-count <SUBTITLE_COUNT>
```

The importer must:

- connect to the running Resolve instance and active project/timeline;
- import the SRT into the current Media Pool folder, select it, and switch to the Edit page;
- refresh the existing Media Pool item when that final filename changed; if Resolve cannot replace an SRT item, delete that same Media Pool item and reimport the verified final file without leaving duplicates;
- treat import failure as a handoff failure, not SRT generation failure.

Resolve 21's documented API cannot append an external SRT Media Pool item to a subtitle track. Never claim automatic timeline placement. Tell the user to drag the selected subtitle onto the subtitle track. If Resolve is unavailable, keep the verified SRT and report that import was skipped or failed.

## Recurring Bug Categories

Read [references/splitting-regressions.md](references/splitting-regressions.md) when testing sentence splitting or when screenshots show broken phrases.

## Encoding Note

PowerShell may corrupt inline Chinese passed into Python heredocs. Use PowerShell-native file reads or Unicode escapes inside Python for Chinese self-check strings.
