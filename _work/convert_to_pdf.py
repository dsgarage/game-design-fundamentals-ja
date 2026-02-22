#!/usr/bin/env python3
"""
Markdownファイルを日本語対応PDFに変換するスクリプト
"""
import os
import glob
import subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
TEXTBOOK_DIR = os.path.join(BASE, "textbook")
IMAGES_DIR = os.path.join(BASE, "images")
OUTPUT_PDF = os.path.join(BASE, "ゲームデザインの基礎_教科書.pdf")

# 全Lectureファイルを番号順にソートして結合
md_files = sorted(glob.glob(os.path.join(TEXTBOOK_DIR, "Lecture*.md")))

if not md_files:
    print("Error: No Lecture*.md files found")
    exit(1)

print(f"Found {len(md_files)} lecture files:")
for f in md_files:
    print(f"  {os.path.basename(f)}")

# 結合したMarkdownを作成
combined_md = os.path.join(BASE, "combined_textbook.md")
with open(combined_md, "w", encoding="utf-8") as out:
    out.write("---\n")
    out.write("title: ゲームデザインの基礎\n")
    out.write("subtitle: Fundamentals of Game Design 講義テキスト\n")
    out.write("author: Ernest Adams 著（講義用日本語要約版）\n")
    out.write("---\n\n")

    for i, f in enumerate(md_files):
        with open(f, "r", encoding="utf-8") as inp:
            content = inp.read()
        if i > 0:
            out.write("\n\\newpage\n\n")
        out.write(content)
        out.write("\n\n")

print(f"Combined markdown: {combined_md}")

# pandocでPDF変換（日本語フォント対応）
cmd = [
    "pandoc",
    combined_md,
    "-o", OUTPUT_PDF,
    "--pdf-engine=weasyprint",
    "--css", os.path.join(BASE, "style.css"),
    "--resource-path", IMAGES_DIR,
    "-f", "markdown",
    "--metadata", "lang=ja",
]

print(f"Running: {' '.join(cmd)}")
result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode == 0:
    print(f"PDF created: {OUTPUT_PDF}")
else:
    print(f"Error: {result.stderr}")
    # Fallback: try without CSS
    cmd2 = [
        "pandoc",
        combined_md,
        "-o", OUTPUT_PDF,
        "--pdf-engine=weasyprint",
        "--resource-path", IMAGES_DIR,
        "-f", "markdown",
    ]
    result2 = subprocess.run(cmd2, capture_output=True, text=True)
    if result2.returncode == 0:
        print(f"PDF created (fallback): {OUTPUT_PDF}")
    else:
        print(f"Fallback error: {result2.stderr}")
