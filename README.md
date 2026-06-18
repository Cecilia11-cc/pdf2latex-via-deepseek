# 📄 PDF → LaTeX 转换工具（via DeepSeek）

一个 Python 脚本，调用 DeepSeek 大模型，将中文数学建模论文 PDF 自动转换为结构清晰的 LaTeX 文档。

## ✨ 能做什么

- 提取 PDF 中的全部文字（支持多页）
- 自动生成符合中文排版习惯的 LaTeX 文件（`ctexart`）
- 将原文中的公式转为 LaTeX 数学环境
- 表格转为三线表（`booktabs`）
- 保留图片、参考文献的占位符
- 本地运行，你的 PDF 不会上传到任何地方（仅将提取的文字发送给 DeepSeek API）

## 📦 依赖库

```bash
pip install pdfplumber openai python-dotenv