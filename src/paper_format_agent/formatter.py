from __future__ import annotations

from docx.document import Document as DocumentObject
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

from .models import FormatStats, ParagraphInfo, ParagraphRole, ParagraphStyleRule, TemplateRules


ALIGNMENTS = {
    "left": WD_ALIGN_PARAGRAPH.LEFT,
    "center": WD_ALIGN_PARAGRAPH.CENTER,
    "right": WD_ALIGN_PARAGRAPH.RIGHT,
    "justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
}

DEFAULT_WORD_STYLE_NAMES = {
    ParagraphRole.TITLE: "PFA Title",
    ParagraphRole.ABSTRACT_HEADING: "PFA Abstract Heading",
    ParagraphRole.ABSTRACT: "PFA Abstract",
    ParagraphRole.KEYWORDS: "PFA Keywords",
    ParagraphRole.HEADING_1: "PFA Heading 1",
    ParagraphRole.HEADING_2: "PFA Heading 2",
    ParagraphRole.HEADING_3: "PFA Heading 3",
    ParagraphRole.FIGURE_CAPTION: "PFA Figure Caption",
    ParagraphRole.TABLE_CAPTION: "PFA Table Caption",
    ParagraphRole.REFERENCES_HEADING: "PFA References Heading",
    ParagraphRole.REFERENCE: "PFA Reference",
    ParagraphRole.BODY: "PFA Body",
}


def apply_template(document: DocumentObject, structure: list[ParagraphInfo], rules: TemplateRules) -> FormatStats:
    stats = FormatStats(total_paragraphs=len(structure))
    apply_page_rules(document, rules)
    word_styles = ensure_template_styles(document, rules)

    for info in structure:
        stats.role_counts[info.role] = stats.role_counts.get(info.role, 0) + 1
        rule = rules.styles.get(info.role) or rules.styles.get(ParagraphRole.BODY)
        if info.role == ParagraphRole.EMPTY or rule is None:
            continue
        style_name = word_styles.get(info.role) or word_styles.get(ParagraphRole.BODY)
        apply_paragraph_style(document.paragraphs[info.index], style_name)
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


def ensure_template_styles(
    document: DocumentObject, rules: TemplateRules
) -> dict[ParagraphRole, str]:
    style_names: dict[ParagraphRole, str] = {}
    for role, rule in rules.styles.items():
        if role == ParagraphRole.EMPTY:
            continue
        style_name = rule.word_style_name or DEFAULT_WORD_STYLE_NAMES.get(role, f"PFA {role.value}")
        style = get_or_create_paragraph_style(document, style_name)
        apply_rule_to_word_style(style, rule)
        style_names[role] = style_name
    return style_names


def get_or_create_paragraph_style(document: DocumentObject, style_name: str):
    try:
        return document.styles[style_name]
    except KeyError:
        return document.styles.add_style(style_name, WD_STYLE_TYPE.PARAGRAPH)


def apply_rule_to_word_style(style, rule: ParagraphStyleRule) -> None:
    fmt = style.paragraph_format
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

    if rule.font:
        style.font.name = rule.font
    if rule.east_asia_font:
        set_style_east_asia_font(style, rule.east_asia_font)
    if rule.size_pt is not None:
        style.font.size = Pt(rule.size_pt)
    if rule.bold is not None:
        style.font.bold = rule.bold
    if rule.italic is not None:
        style.font.italic = rule.italic


def set_style_east_asia_font(style, font_name: str) -> None:
    r_pr = style.element.get_or_add_rPr()
    r_fonts = r_pr.rFonts
    if r_fonts is None:
        r_fonts = OxmlElement("w:rFonts")
        r_pr.append(r_fonts)
    r_fonts.set(qn("w:eastAsia"), font_name)


def apply_paragraph_style(paragraph, style_name: str | None) -> None:
    if style_name is None:
        return
    paragraph.style = style_name


def add_basic_warnings(stats: FormatStats) -> None:
    if stats.role_counts.get(ParagraphRole.ABSTRACT, 0) == 0:
        stats.warnings.append("No abstract paragraph was detected.")
    if stats.role_counts.get(ParagraphRole.KEYWORDS, 0) == 0:
        stats.warnings.append("No keywords paragraph was detected.")
    if stats.role_counts.get(ParagraphRole.REFERENCES_HEADING, 0) == 0:
        stats.warnings.append("No references heading was detected.")
