# Architecture

Paper Format Agent follows a conservative split:

1. Deterministic code reads and writes DOCX files.
2. A structure detector labels paragraphs as title, abstract, headings, body, captions, or references.
3. A template rule engine applies formatting.
4. A report explains what was changed and what could not be verified.

The current MVP intentionally uses rule-based detection only. The AI-assisted detector should be added as a separate provider that returns paragraph roles, while the formatter remains deterministic.

```text
messy.docx + template.json
        |
        v
DOCX reader -> structure detector -> style engine -> formatted.docx
        |                                      |
        +--------------------------------------+
                         v
                    report.md
```

## Design Rules

- Never let an LLM directly generate the final DOCX.
- Keep template rules explicit and inspectable.
- Make every output reproducible from the same input and template.
- Treat AI as a classifier and reviewer first, not as the formatting engine.
