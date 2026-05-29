# Development Log

## 2026-05-29

### Full Thesis Demo And Structure Check

- Added `examples/create_full_thesis_docx.py` to generate an original full-structure thesis demo.
- Generated `examples/full_thesis_demo.docx` covering cover metadata, statements, abstracts, contents, figure/table lists, symbols, acronyms, chapters, captions, formula text, conclusion, acknowledgements, references, appendix, and achievements.
- Improved detection for unnumbered thesis headings such as contents, declarations, acknowledgements, appendices, and achievements.
- Fixed reference-section state handling so a table-of-contents `参考文献` line does not cause following body paragraphs to be classified as references.
- Formatted the full demo with `templates/uestc_graduate_thesis.json`; the report detected 87 paragraphs and styled 73 non-empty paragraphs.
- Verified generated Word styles by reading the output DOCX: `正文` 24, `一级标题` 22, `二级标题` 10, `参考文献条目` 4, plus abstract, keyword, caption, and title styles.
- Microsoft Word exported the formatted full demo to a 6-page PDF. LibreOffice render QA could not complete because local LibreOffice reports a damaged `D:\Software\LibreOffice\program\bootstrap.ini`.

## 2026-05-28

### Content-Matched Word Style Names

- Renamed default generated Word styles from internal `PFA ...` labels to content-matched Chinese names such as `正文`, `一级标题`, and `参考文献条目`.
- Kept `word_style_name` as the template-level override for journals, schools, Overleaf-derived templates, or Markdown-derived templates that need custom names.
- Updated README wording so users know they can inspect and edit generated styles by content role.

### Style-Based Formatting Engine

- Changed the formatter from direct run formatting to a style-based workflow.
- JSON rules now create or update named Word paragraph styles such as `PFA Body`, `PFA Heading 1`, and `PFA Reference`.
- Paragraphs are assigned to generated styles, leaving room for manual style edits in Word after formatting.
- Added optional `word_style_name` to template rules for future template-specific style naming.
- Preserved inline run formatting instead of clearing author emphasis.

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
