# Agent Instructions

This repository is an AI-assisted open-source project. Any agent entering this workspace should read this file first, then read `GOALS.md`, `HANDOFF.md`, and `DEVELOPMENT_LOG.md`.

## Project Mission

Build an open-source tool that converts messy academic DOCX manuscripts into journal or thesis formatted DOCX files using explicit templates, deterministic formatting code, and optional AI-assisted structure detection.

## Operating Rules

- Keep the formatter deterministic. AI may classify or review, but code must write the final DOCX.
- Prefer small, runnable increments over large speculative rewrites.
- Preserve the CLI-first workflow unless a task explicitly targets UI or plugin packaging.
- Keep templates explicit and inspectable.
- Update `DEVELOPMENT_LOG.md` after every meaningful change.
- Update `HANDOFF.md` before ending a work session.
- If a design decision changes the project direction, update `GOALS.md`.
- Run a basic smoke test before handoff when code changes affect behavior.

## Current Smoke Test

From the repository root:

```powershell
$env:PYTHONPATH='src'
& 'C:\Users\asus\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' examples\create_example_docx.py
& 'C:\Users\asus\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m paper_format_agent.cli format --input examples\messy_paper.docx --template templates\thesis_basic.json --output examples\output\formatted.docx --report examples\output\report.md
```

Expected result:

- `examples/output/formatted.docx` is generated.
- `examples/output/report.md` is generated.
- The report shows detected roles for title, abstract, keywords, headings, body, figure caption, references heading, and reference.

## Development Style

- Use clear module boundaries: parsing, detection, template rules, formatting, reporting.
- Avoid letting template parsing and DOCX writing become tangled.
- Add tests for detection and rule parsing before expanding heuristics.
- Do not introduce heavyweight dependencies unless they unlock a concrete roadmap item.

## README Maintenance Prompt

When a change affects user-visible behavior, CLI commands, templates, generated outputs, or the smoke-test result, reuse this maintenance prompt before handoff:

```text
Update README.md in both Chinese and English. Keep the Chinese section first when practical. Include:
1. What the tool currently does.
2. How to install and run it.
3. The current observable effect, including inspect output or report summary when behavior changes.
4. Links or paths to generated example outputs if they exist.
5. Any current limitations that a GitHub reader should know.
Keep the formatter description deterministic: AI may classify or review, but code writes the final DOCX.
```

If the current effect changes, update the README's "当前效果 / Current Effect" section during the same work session.
