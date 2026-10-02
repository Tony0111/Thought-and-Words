#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""从微信公众号导出的 HTML 中抽取正文纯文本。

用法（在仓库根目录）:
    python tools/extract_wechat.py

读取 corpus/raw/<作者>/*.html，正文输出到 corpus/raw/<作者>/_extracted/*.txt
只依赖 lxml。
"""
from __future__ import annotations

import os
import re
import sys

from lxml import html as lhtml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(ROOT, "corpus", "raw")

BLOCK_TAGS = {
    "p", "section", "div", "br", "h1", "h2", "h3", "h4", "h5", "h6",
    "li", "tr", "blockquote", "figure", "figcaption", "hr",
}


def extract_text(html_bytes: bytes) -> tuple[str, str]:
    tree = lhtml.fromstring(html_bytes)
    # 标题
    title = ""
    for xp in ('//*[@id="activity-name"]', "//h1", "//title"):
        nodes = tree.xpath(xp)
        if nodes:
            title = " ".join(nodes[0].text_content().split())
            if title:
                break

    # 正文
    content = tree.xpath('//*[@id="js_content"]')
    if not content:
        content = tree.xpath('//*[contains(@class,"rich_media_content")]')
    if not content:
        return title, ""

    root = content[0]
    parts: list[str] = []
    for node in root.iter():
        tag = node.tag
        if not isinstance(tag, str):
            continue
        if tag in ("script", "style"):
            continue
        if node.text:
            parts.append(node.text)
        if tag in BLOCK_TAGS:
            parts.append("\n")
        if node.tail:
            parts.append(node.tail)
    raw = "".join(parts)
    lines = []
    for line in raw.split("\n"):
        line = re.sub(r"[ \t\u00a0\u2002\u2003\u3000]+", " ", line).strip()
        lines.append(line)
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return title, text


def main() -> int:
    if not os.path.isdir(RAW_DIR):
        print("找不到 corpus/raw 目录", file=sys.stderr)
        return 1
    count = 0
    last_out = ""
    for author in sorted(os.listdir(RAW_DIR)):
        author_dir = os.path.join(RAW_DIR, author)
        if not os.path.isdir(author_dir):
            continue
        out_dir = os.path.join(author_dir, "_extracted")
        os.makedirs(out_dir, exist_ok=True)
        for name in sorted(os.listdir(author_dir)):
            if not name.lower().endswith(".html"):
                continue
            path = os.path.join(author_dir, name)
            with open(path, "rb") as f:
                data = f.read()
            title, text = extract_text(data)
            stem = os.path.splitext(name)[0]
            out_path = os.path.join(out_dir, stem + ".txt")
            with open(out_path, "w", encoding="utf-8") as f:
                if title:
                    f.write("# " + title + "\n\n")
                f.write(text + "\n")
            print(f"OK  {len(text):>7} 字  {name}")
            count += 1
            last_out = out_dir
    print(f"\n共抽取 {count} 篇 -> {last_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
