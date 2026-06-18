#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import pdfplumber
from openai import OpenAI
from dotenv import load_dotenv

# ==================== 请在这里修改你的路径 ====================
# PDF 文件的相对路径（可自行修改）
PDF_PATH = ".pdf"

# 环境变量文件（.env）的绝对路径
ENV_PATH = ".env"

# 输出 LaTeX 文件路径（可自定义）
OUTPUT_TEX_PATH = r"D:\CODE\pyCODE\output.tex"

# API 配置
BASE_URL = "https://api.deepseek.com/v1"
MODEL = "deepseek-chat"   # 或 deepseek-reasoner
# ============================================================

# 1. 加载环境变量（指定文件）
if not os.path.exists(ENV_PATH):
    print(f"❌ 错误：环境变量文件不存在：{ENV_PATH}")
    sys.exit(1)

load_dotenv(dotenv_path=ENV_PATH)
API_KEY = os.getenv("DEEPSEEK_API_KEY")

if not API_KEY:
    print("❌ 错误：未找到 DEEPSEEK_API_KEY，请检查 111.env 文件内容。")
    print("   文件格式应为：DEEPSEEK_API_KEY=sk-你的完整真实密钥")
    sys.exit(1)
else:
    print(f"✅ 成功加载 API Key，长度：{len(API_KEY)}")

# 2. 检查 PDF 文件
if not os.path.exists(PDF_PATH):
    print(f"❌ 错误：PDF 文件不存在：{PDF_PATH}")
    sys.exit(1)

# 3. 读取 PDF 文字
print(f"📄 正在读取 PDF：{PDF_PATH}")
full_text = ""

try:
    with pdfplumber.open(PDF_PATH) as pdf:
        print(f"   总页数：{len(pdf.pages)}")
        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if text:
                full_text += text + "\n"
            else:
                print(f"   ⚠️ 警告：第 {i} 页未提取到文字（可能是扫描图片）")
except Exception as e:
    print(f"❌ 读取 PDF 失败：{e}")
    sys.exit(1)

if not full_text.strip():
    print("❌ 错误：PDF 中没有提取到任何文字，可能为扫描件，请先用 OCR 工具识别。")
    sys.exit(1)

print(f"✅ 成功提取文字，总字符数：{len(full_text)}")

# 4. 构造提示词（略作精简，避免超长）
prompt = f"""
请将下面这篇数学建模论文的内容，转换成一个完整的 LaTeX 文档。要求：

1. 使用 ctexart 文档类，支持中文。
2. 保留所有章节标题。
3. 将文中的公式（如 (3.1)）转为 LaTeX 数学环境。
4. 将文中所有表格转为三线表（booktabs）。
5. 图片保留为 \\begin{{figure}}...\\includegraphics... 占位符。
6. 参考文献转为 thebibliography 环境。

论文内容：
{full_text}
"""

# 5. 调用 API
print("🚀 正在调用 DeepSeek API，请稍候...")
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

try:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "你是一个精通 LaTeX 和数学建模的专家。只输出 LaTeX 代码，不要额外解释。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=16000
    )
except Exception as e:
    print(f"❌ API 调用失败：{e}")
    sys.exit(1)

latex_code = response.choices[0].message.content
print(f"✅ API 返回成功，LaTeX 代码长度：{len(latex_code)} 字符")

# 6. 保存文件
try:
    with open(OUTPUT_TEX_PATH, "w", encoding="utf-8") as f:
        f.write(latex_code)
    print(f"🎉 成功！LaTeX 文件已保存为：{OUTPUT_TEX_PATH}")
except Exception as e:
    print(f"❌ 保存文件失败：{e}")
    sys.exit(1)