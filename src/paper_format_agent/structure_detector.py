from __future__ import annotations

import re

from .models import ParagraphRole


ABSTRACT_PATTERNS = ("摘要", "abstract")
KEYWORD_PATTERNS = ("关键词", "关键字", "key words", "keywords")
REFERENCE_PATTERNS = ("参考文献", "references", "bibliography")
UNNUMBERED_HEADING_PATTERNS = (
    "目录",
    "contents",
    "图目录",
    "表目录",
    "主要符号表",
    "缩略词表",
    "独创性声明",
    "论文使用授权",
    "绪论",
    "结论",
    "致谢",
    "acknowledgements",
    "acknowledgments",
)


def detect_role(text: str, style_name: str | None = None, in_references: bool = False) -> ParagraphRole:
    stripped = text.strip()
    lower = stripped.lower()
    style_lower = (style_name or "").lower()

    if not stripped:
        return ParagraphRole.EMPTY
    if lower in ABSTRACT_PATTERNS:
        return ParagraphRole.ABSTRACT_HEADING
    if lower.startswith(ABSTRACT_PATTERNS):
        return ParagraphRole.ABSTRACT
    if lower.startswith(KEYWORD_PATTERNS):
        return ParagraphRole.KEYWORDS
    if lower in REFERENCE_PATTERNS:
        return ParagraphRole.REFERENCES_HEADING
    if re.match(r"^图\s*\d+|^figure\s+\d+", lower):
        return ParagraphRole.FIGURE_CAPTION
    if re.match(r"^表\s*\d+|^table\s+\d+", lower):
        return ParagraphRole.TABLE_CAPTION
    if "heading 3" in style_lower or re.match(r"^\d+\.\d+\.\d+\s+", stripped):
        return ParagraphRole.HEADING_3
    if "heading 2" in style_lower or re.match(r"^\d+\.\d+\s+", stripped):
        return ParagraphRole.HEADING_2
    if (
        "heading 1" in style_lower
        or lower in UNNUMBERED_HEADING_PATTERNS
        or re.match(r"^(第[一二三四五六七八九十\d]+章|\d+)\s+", stripped)
        or re.match(r"^附录\s*[a-zA-Z一二三四五六七八九十\d]*", stripped)
        or stripped.startswith("攻读学位期间")
    ):
        return ParagraphRole.HEADING_1
    if in_references or re.match(r"^\s*(\[\d+\]|\d+[\.\)]|[A-Z][a-z]+,\s)", stripped):
        return ParagraphRole.REFERENCE
    if len(stripped) <= 80 and ("title" in style_lower or "标题" in (style_name or "")):
        return ParagraphRole.TITLE
    return ParagraphRole.BODY
