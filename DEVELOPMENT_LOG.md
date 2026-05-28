# Development Log

## 2026-05-28

### Built-In UESTC Graduate Template

- Added `templates/uestc_graduate_thesis.json` as a curated built-in template based on the provided UESTC graduate thesis writing specification for Chinese students.
- Extended paragraph style rules with `line_spacing_pt` so templates can express fixed line spacing such as 20 pt.
- Updated `README.md` to list the built-in UESTC template, usage command, and current limitations.
- Verified template loading and formatting with the CLI smoke test.
- Kept this as a built-in curated template; generic DOCX/PDF template extraction remains future work.

### README Bilingual Update

- Rewrote `README.md` as a Chinese/English bilingual project overview.
- Added the current CLI effect, detected structure example, generated output paths, and report summary.
- Added a reusable README maintenance prompt to `AGENTS.md` so future agents update the bilingual README when user-visible behavior changes.
- Verified with `compileall`, example DOCX generation, CLI `inspect`, and CLI `format`.
- `pytest` was not run because the current environment does not have `pytest` installed.

### Initial MVP

- Created the `paper-format-agent` Python project.
- Added CLI support for inspecting and formatting DOCX files.
- Implemented DOCX loading and saving through `python-docx`.
- Implemented rule-based structure detection for common academic sections.
- Added JSON template support for thesis and journal formatting.
- Implemented deterministic formatting for page margins and paragraph styles.
- Added Markdown report generation.
- Added example DOCX generator and generated a sample document.
- Added README, architecture notes, roadmap, license, and gitignore.
- Initialized a local Git repository and created the first commit.

### Workspace Handoff Support

- Added `AGENTS.md` so future AI agents know how to work in this repository.
- Added `GOALS.md` to capture the product goal, MVP scope, non-goals, and milestones.
- Added `HANDOFF.md` for current state, important files, verified commands, and next task.
- Added this chronological development log.

## Logging Convention

Future agents should append entries in this format:

```markdown
## YYYY-MM-DD

### Short Task Name

- What changed.
- Why it changed.
- How it was verified.
- Any known limitations or follow-up tasks.
```
