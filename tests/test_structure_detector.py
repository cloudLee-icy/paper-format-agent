from paper_format_agent.models import ParagraphRole
from paper_format_agent.structure_detector import detect_role


def test_detects_common_roles():
    assert detect_role("摘要") == ParagraphRole.ABSTRACT_HEADING
    assert detect_role("关键词：论文；格式") == ParagraphRole.KEYWORDS
    assert detect_role("参考文献") == ParagraphRole.REFERENCES_HEADING
    assert detect_role("1 引言") == ParagraphRole.HEADING_1
    assert detect_role("1.1 研究背景") == ParagraphRole.HEADING_2
    assert detect_role("图 1 系统流程") == ParagraphRole.FIGURE_CAPTION

