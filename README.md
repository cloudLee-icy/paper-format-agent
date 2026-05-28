# Paper Format Agent

Turn messy academic DOCX files into journal or thesis formatted documents.

Paper Format Agent is a template-driven formatter for academic manuscripts. It takes an input Word document, applies a thesis or journal style template, and writes both a formatted DOCX and a human-readable report.

```text
messy.docx + template.json
        |
        v
formatted.docx + report.md
```

## Status

This is an early MVP. It is useful for validating the workflow:

- DOCX in, DOCX out
- JSON formatting templates
- Rule-based paragraph role detection
- Heading, body, abstract, keyword, caption, and reference formatting
- Markdown format report

It does not yet fully validate citation styles, formulas, table layout, or school-specific thesis rules.

## Install

```bash
pip install -e .
```

## Usage

Inspect a document:

```bash
paperfmt inspect --input examples/messy_paper.docx
```

Format a document:

```bash
paperfmt format \
  --input examples/messy_paper.docx \
  --template templates/thesis_basic.json \
  --output examples/output/formatted.docx \
  --report examples/output/report.md
```

## Template Example

```json
{
  "name": "Basic Chinese Thesis Template",
  "page": {
    "margin_top_cm": 2.5,
    "margin_bottom_cm": 2.5,
    "margin_left_cm": 3.0,
    "margin_right_cm": 2.5
  },
  "styles": {
    "body": {
      "font": "Times New Roman",
      "east_asia_font": "SimSun",
      "size_pt": 12,
      "line_spacing": 1.5,
      "first_line_indent_cm": 0.74
    },
    "heading_1": {
      "font": "Times New Roman",
      "east_asia_font": "SimHei",
      "size_pt": 16,
      "bold": true,
      "alignment": "center"
    }
  }
}
```

## Why This Project

Most academic formatting tools either require manual Word work or depend on rigid templates. This project aims to make formatting reproducible:

- AI can help identify structure.
- Deterministic code applies formatting.
- Reports make changes auditable.

## Roadmap

See [docs/roadmap.md](docs/roadmap.md).

## License

MIT
