from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.document import Document as DocumentObject

from .models import ParagraphInfo, ParagraphRole
from .structure_detector import detect_role


def load_document(path: Path) -> DocumentObject:
    return Document(str(path))


def detect_structure(document: DocumentObject) -> list[ParagraphInfo]:
    paragraphs: list[ParagraphInfo] = []
    in_references = False
    first_content_seen = False

    for index, paragraph in enumerate(document.paragraphs):
        text = paragraph.text
        style_name = paragraph.style.name if paragraph.style is not None else None
        role = detect_role(text, style_name, in_references=in_references)
        if not first_content_seen and role == ParagraphRole.BODY and 0 < len(text.strip()) <= 100:
            role = ParagraphRole.TITLE
        if role != ParagraphRole.EMPTY:
            first_content_seen = True
        if role == ParagraphRole.REFERENCES_HEADING:
            in_references = True
        paragraphs.append(ParagraphInfo(index=index, text=text, style_name=style_name, role=role))

    return paragraphs


def save_document(document: DocumentObject, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    document.save(str(path))
