from __future__ import annotations

from docx.document import Document as DocumentObject
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

from .models import FormatStats, ParagraphInfo, ParagraphRole, ParagraphStyleRule, TemplateRules


ALIGNMENTS = {
    "left": WD_ALIGN_PARAGRAPH.LEFT,
    "center": WD_ALIGN_PARAGRAPH.CENTER,
    "right": WD_ALIGN_PARAGRAPH.RIGHT,
    "justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
}


def apply_template(document: DocumentObject, structure: list[ParagraphInfo], rules: TemplateRules) -> FormatStats:
    stats = FormatStats(total_paragraphs=len(structure))
    apply_page_rules(document, rules)

    for info in structure:
        stats.role_counts[info.role] = stats.role_counts.get(info.role, 0) + 1
        rule = rules.styles.get(info.role) or rules.styles.get(ParagraphRole.BODY)
        if info.role == ParagraphRole.EMPTY or rule is None:
            continue
        apply_paragraph_rule(document.paragraphs[info.index], rule)
        stats.styled_paragraphs += 1

    add_basic_warnings(stats)
    return stats


def apply_page_rules(document: DocumentObject, rules: TemplateRules) -> None:
    for section in document.sections:
        if rules.page.margin_top_cm is not None:
            section.top_margin = Cm(rules.page.margin_top_cm)
        if rules.page.margin_bottom_cm is not None:
            section.bottom_margin = Cm(rules.page.margin_bottom_cm)
        if rules.page.margin_left_cm is not None:
            section.left_margin = Cm(rules.page.margin_left_cm)
        if rules.page.margin_right_cm is not None:
            section.right_margin = Cm(rules.page.margin_right_cm)


def apply_paragraph_rule(paragraph, rule: ParagraphStyleRule) -> None:
    fmt = paragraph.paragraph_format
    if rule.alignment:
        fmt.alignment = ALIGNMENTS.get(rule.alignment)
    if rule.first_line_indent_cm is not None:
        fmt.first_line_indent = Cm(rule.first_line_indent_cm)
    if rule.left_indent_cm is not None:
        fmt.left_indent = Cm(rule.left_indent_cm)
    if rule.line_spacing_pt is not None:
        fmt.line_spacing = Pt(rule.line_spacing_pt)
    if rule.line_spacing is not None:
        fmt.line_spacing = rule.line_spacing
    if rule.space_before_pt is not None:
        fmt.space_before = Pt(rule.space_before_pt)
    if rule.space_after_pt is not None:
        fmt.space_after = Pt(rule.space_after_pt)

    for run in paragraph.runs:
        if rule.font:
            run.font.name = rule.font
        if rule.east_asia_font:
            run._element.rPr.rFonts.set(qn("w:eastAsia"), rule.east_asia_font)
        if rule.size_pt is not None:
            run.font.size = Pt(rule.size_pt)
        if rule.bold is not None:
            run.bold = rule.bold
        if rule.italic is not None:
            run.italic = rule.italic


def add_basic_warnings(stats: FormatStats) -> None:
    if stats.role_counts.get(ParagraphRole.ABSTRACT, 0) == 0:
        stats.warnings.append("No abstract paragraph was detected.")
    if stats.role_counts.get(ParagraphRole.KEYWORDS, 0) == 0:
        stats.warnings.append("No keywords paragraph was detected.")
    if stats.role_counts.get(ParagraphRole.REFERENCES_HEADING, 0) == 0:
        stats.warnings.append("No references heading was detected.")
