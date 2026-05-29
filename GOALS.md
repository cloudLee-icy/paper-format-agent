# Goals

## Product Goal

Create a practical open-source academic document formatter:

```text
source.docx + format_template.json -> formatted.docx + report.md
```

The tool should help authors turn draft papers, journal manuscripts, and thesis documents into a target format with less manual Word work.

## MVP Scope

The current MVP focuses on:

- DOCX input and output.
- JSON formatting templates.
- Rule-based structure detection.
- Formatting for title, abstract, keywords, headings, body text, figure captions, table captions, references heading, and references.
- A Markdown report that explains detected structure and warnings.

## Non-Goals For Now

- PDF reverse editing.
- Full LaTeX support.
- Perfect school-specific thesis compliance.
- Full citation style validation.
- AI rewriting of paper content.
- Web UI or SaaS workflow.

## Near-Term Milestones

1. Improve paragraph role detection accuracy.
2. Add template validation and clearer error messages.
3. Add DOCX template extraction as an experimental command.
4. Add optional AI-assisted role detection that returns structured paragraph labels only.
5. Add before/after screenshots or rendered previews for GitHub README.
6. Package as a Codex plugin after the CLI stabilizes.

## Design Principle

AI identifies structure. Deterministic code creates Word styles and applies formatting through those styles where possible.
