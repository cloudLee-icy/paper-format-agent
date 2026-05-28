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

