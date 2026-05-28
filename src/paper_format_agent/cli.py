from __future__ import annotations

import argparse
from pathlib import Path

from .docx_io import detect_structure, load_document, save_document
from .formatter import apply_template
from .models import TemplateRules
from .report import write_markdown_report

def inspect_command(input_path: Path) -> None:
    document = load_document(input_path)
    structure = detect_structure(document)

    print(f"Detected structure: {input_path.name}")
    print("#\tRole\tStyle\tText")
    for item in structure:
        preview = item.text.strip()
        if len(preview) > 80:
            preview = preview[:77] + "..."
        print(f"{item.index}\t{item.role.value}\t{item.style_name or ''}\t{preview}")


def format_command(
    input_path: Path,
    template_path: Path,
    output_path: Path,
    report_path: Path,
) -> None:
    rules = TemplateRules.from_json(template_path)
    document = load_document(input_path)
    structure = detect_structure(document)
    stats = apply_template(document, structure, rules)

    save_document(document, output_path)
    write_markdown_report(report_path, input_path, output_path, rules, structure, stats)

    print(f"Wrote formatted document: {output_path}")
    print(f"Wrote report: {report_path}")
    if stats.warnings:
        print("Warnings:")
        for warning in stats.warnings:
            print(f"- {warning}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Template-driven academic DOCX formatter.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect_parser = subparsers.add_parser("inspect", help="Inspect detected paragraph roles.")
    inspect_parser.add_argument("--input", "-i", required=True, type=Path)

    format_parser = subparsers.add_parser("format", help="Apply a JSON template to a DOCX file.")
    format_parser.add_argument("--input", "-i", required=True, type=Path)
    format_parser.add_argument("--template", "-t", required=True, type=Path)
    format_parser.add_argument("--output", "-o", required=True, type=Path)
    format_parser.add_argument("--report", "-r", default=Path("format_report.md"), type=Path)
    return parser


def app() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "inspect":
        inspect_command(args.input)
    elif args.command == "format":
        format_command(args.input, args.template, args.output, args.report)


if __name__ == "__main__":
    app()
