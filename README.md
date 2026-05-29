# Paper Format Agent

把杂乱的学术 DOCX 稿件转换成期刊或论文模板格式。

Paper Format Agent is a template-driven formatter that turns messy academic DOCX manuscripts into journal or thesis formatted documents.

```text
messy.docx + template.json
        |
        v
formatted.docx + report.md
```

## 当前状态 / Status

这是一个早期 MVP，已经可以验证核心工作流：

- DOCX 输入、DOCX 输出
- JSON 格式模板
- 内置基础论文模板、期刊模板和电子科技大学研究生学位论文模板
- 基于规则的段落结构识别
- 标题、摘要、关键词、正文、图表题注、参考文献格式化
- Markdown 格式化报告

This is an early MVP. It currently supports:

- DOCX input and output
- JSON formatting templates
- Built-in basic thesis, journal, and UESTC graduate thesis templates
- Rule-based paragraph role detection
- Formatting for title, abstract, keywords, body text, captions, and references
- A Markdown report that explains detected structure and warnings

暂不支持完整引用格式校验、公式排版、表格布局重写或学校级论文规范全量检查。也暂不支持从规范 DOCX/PDF 自动通用提取模板；电子科大模板目前是手工整理的内置 JSON。

It does not yet fully validate citation styles, formulas, table layouts, or complete school-specific thesis requirements. It also does not yet support generic template extraction from specification DOCX/PDF files; the UESTC template is a curated built-in JSON file.

## 安装 / Install

```bash
pip install -e .
```

## 使用 / Usage

生成示例文档：

Create the example manuscript:

```bash
python examples/create_example_docx.py
```

检查文档结构：

Inspect detected paragraph roles:

```bash
paperfmt inspect --input examples/messy_paper.docx
```

格式化文档：

Format a document:

```bash
paperfmt format \
  --input examples/messy_paper.docx \
  --template templates/thesis_basic.json \
  --output examples/output/formatted.docx \
  --report examples/output/report.md
```

使用内置电子科技大学研究生学位论文模板：

Use the built-in UESTC graduate thesis template:

```bash
paperfmt format \
  --input examples/messy_paper.docx \
  --template templates/uestc_graduate_thesis.json \
  --output examples/output/uestc_formatted.docx \
  --report examples/output/uestc_report.md
```

## 当前效果 / Current Effect

示例文档的 `inspect` 输出可以识别标题、摘要、关键词、章节标题、正文、图题和参考文献：

The current `inspect` output for the example document detects title, abstract, keywords, headings, body text, figure caption, and references:

```text
#   Role                Text
0   title               面向学术写作的文档格式化方法研究
1   abstract            摘要：本文讨论一种将不规范论文文档转换为目标模板格式的方法。
2   keywords            关键词：论文格式化；Word；模板；学术写作
3   heading_1           1 引言
4   body                作者在投稿或提交毕业论文前，通常需要花费大量时间处理格式问题。
5   heading_2           1.1 研究背景
6   body                不同期刊和学校对字体、行距、页边距、标题层级和参考文献有不同要求。
7   figure_caption      图 1 文档格式化流程
8   heading_1           2 方法
9   body                本文采用结构识别和确定性格式套用相结合的方式。
10  references_heading  参考文献
11  reference           [1] Zhang S. Academic document formatting workflow. 2026.
```

格式化命令会生成：

The formatting command generates:

- `examples/output/formatted.docx`
- `examples/output/report.md`

当前报告摘要：

Current report summary:

```text
Paragraphs scanned: 12
Paragraphs styled: 12

Detected Structure:
- abstract: 1
- body: 3
- figure_caption: 1
- heading_1: 2
- heading_2: 1
- keywords: 1
- reference: 1
- references_heading: 1
- title: 1

Warnings:
- No basic structural warnings.
```

## 模板示例 / Template Example

当前内置模板：

Built-in templates:

- `templates/thesis_basic.json`
- `templates/journal_basic.json`
- `templates/uestc_graduate_thesis.json`

`uestc_graduate_thesis.json` 是基于用户提供的《电子科技大学研究生学位论文撰写规范- 适用于中国学生》整理的内置模板。它不是通用自动提取结果，当前主要覆盖页面边距、标题、正文、图题、表题和参考文献段落格式。

`uestc_graduate_thesis.json` is curated from the provided UESTC graduate thesis writing specification for Chinese students. It is not a generic automatic extraction result. It currently covers page margins and paragraph styles for headings, body text, captions, and references.

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

## 为什么做这个项目 / Why This Project

大多数学术格式处理仍然依赖手动 Word 操作，或者依赖很难审计的固定模板。本项目希望让格式化过程可复现、可解释：

Most academic formatting workflows still depend on manual Word editing or opaque rigid templates. This project aims to make formatting reproducible and auditable:

- AI 可以辅助识别结构，但不直接写最终 DOCX。
- AI may help identify structure, but it should not directly write the final DOCX.
- 确定性代码先在 Word 中创建或更新命名样式，再把段落应用到对应样式。
- Deterministic code creates or updates named Word styles, then applies those styles to matching paragraphs.
- 输出文档保留人工修改余地：用户可以在 Word 的样式面板里修改 `正文`、`一级标题`、`参考文献条目` 等样式。
- The output remains editable: users can adjust content-matched styles such as `正文`, `一级标题`, and `参考文献条目` in Word after generation.
- 报告记录识别结果和基础告警。
- Reports make detected structure and warnings visible.

## 路线图 / Roadmap

See [docs/roadmap.md](docs/roadmap.md).

## 许可证 / License

MIT
