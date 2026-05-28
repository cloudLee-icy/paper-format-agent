from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class ParagraphRole(str, Enum):
    TITLE = "title"
    ABSTRACT_HEADING = "abstract_heading"
    ABSTRACT = "abstract"
    KEYWORDS = "keywords"
    HEADING_1 = "heading_1"
    HEADING_2 = "heading_2"
    HEADING_3 = "heading_3"
    FIGURE_CAPTION = "figure_caption"
    TABLE_CAPTION = "table_caption"
    REFERENCES_HEADING = "references_heading"
    REFERENCE = "reference"
    BODY = "body"
    EMPTY = "empty"


@dataclass
class ParagraphStyleRule:
    font: str | None = None
    east_asia_font: str | None = None
    size_pt: float | None = None
    bold: bool | None = None
    italic: bool | None = None
    alignment: str | None = None
    first_line_indent_cm: float | None = None
    left_indent_cm: float | None = None
    line_spacing: float | None = None
    space_before_pt: float | None = None
    space_after_pt: float | None = None


@dataclass
class PageRule:
    margin_top_cm: float | None = None
    margin_bottom_cm: float | None = None
    margin_left_cm: float | None = None
    margin_right_cm: float | None = None


@dataclass
class TemplateRules:
    name: str = "Untitled template"
    page: PageRule = field(default_factory=PageRule)
    styles: dict[ParagraphRole, ParagraphStyleRule] = field(default_factory=dict)

    @classmethod
    def from_json(cls, path: Path) -> "TemplateRules":
        data = json.loads(path.read_text(encoding="utf-8"))
        page = PageRule(**data.get("page", {}))
        styles = {
            ParagraphRole(key): ParagraphStyleRule(**value)
            for key, value in data.get("styles", {}).items()
        }
        return cls(name=data.get("name", "Untitled template"), page=page, styles=styles)


@dataclass
class ParagraphInfo:
    index: int
    text: str
    role: ParagraphRole
    style_name: str | None = None


@dataclass
class FormatStats:
    total_paragraphs: int = 0
    styled_paragraphs: int = 0
    role_counts: dict[ParagraphRole, int] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
