from __future__ import annotations

from pathlib import Path

from .models import FormatStats, ParagraphInfo, TemplateRules


def write_markdown_report(
    path: Path,
    input_path: Path,
    output_path: Path,
    template: TemplateRules,
    structure: list[ParagraphInfo],
    stats: FormatStats,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Format Report",
        "",
        f"- Input: `{input_path}`",
        f"- Output: `{output_path}`",
        f"- Template: `{template.name}`",
        f"- Paragraphs scanned: `{stats.total_paragraphs}`",
        f"- Paragraphs styled: `{stats.styled_paragraphs}`",
        "",
        "## Detected Structure",
        "",
    ]

    for role, count in sorted(stats.role_counts.items(), key=lambda item: item[0].value):
        lines.append(f"- `{role.value}`: {count}")

    lines.extend(["", "## Warnings", ""])
    if stats.warnings:
        lines.extend(f"- {warning}" for warning in stats.warnings)
    else:
        lines.append("- No basic structural warnings.")

    lines.extend(["", "## Paragraph Map", ""])
    for info in structure:
        preview = info.text.strip().replace("|", "\\|")
        if len(preview) > 90:
            preview = preview[:87] + "..."
        lines.append(f"- `{info.index}` `{info.role.value}` {preview}")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

