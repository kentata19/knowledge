#!/usr/bin/env python3
"""books/*/index.md のfrontmatterを読んで books/README.md の索引を更新する。

依存なし。使い方: python3 scripts/build-index.py
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKS = ROOT / "books"
INDEX = BOOKS / "README.md"
START, END = "<!-- INDEX:START -->", "<!-- INDEX:END -->"

STATUS_LABEL = {
    "unread": "未読",
    "reading": "読書中",
    "done": "読了",
    "paused": "中断",
    "dropped": "離脱",
}
STATUS_ORDER = ["reading", "done", "paused", "unread", "dropped"]


def parse_frontmatter(text):
    """--- で囲まれた最小限のYAMLを辞書にする（key: value と [a, b] のみ対応）。"""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    data = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        key, _, value = line.partition(":")
        value = value.split("  #")[0].strip()
        if value.startswith("[") and value.endswith("]"):
            items = [v.strip() for v in value[1:-1].split(",")]
            data[key.strip()] = [v for v in items if v]
        else:
            data[key.strip()] = value
    return data


def cell(value):
    if isinstance(value, list):
        return "、".join(value) or "—"
    return value or "—"


def main():
    rows = []
    for path in sorted(BOOKS.glob("*/index.md")):
        fm = parse_frontmatter(path.read_text(encoding="utf-8"))
        slug = path.parent.name
        title = fm.get("title") or slug
        status = fm.get("status", "unread")
        rows.append(
            {
                "sort": (
                    STATUS_ORDER.index(status) if status in STATUS_ORDER else 99,
                    fm.get("finished") or "",
                    slug,
                ),
                "cells": [
                    f"[{title}]({slug}/)",
                    cell(fm.get("authors")),
                    STATUS_LABEL.get(status, status),
                    cell(fm.get("finished")),
                    cell(fm.get("rating")),
                    cell(fm.get("tags")),
                ],
            }
        )
    rows.sort(key=lambda r: r["sort"])

    table = ["| 書名 | 著者 | 状態 | 読了日 | 評価 | タグ |", "| --- | --- | --- | --- | --- | --- |"]
    table += ["| " + " | ".join(r["cells"]) + " |" for r in rows]
    if not rows:
        table = ["まだ1冊もありません。"]
    block = f"{START}\n" + "\n".join(table) + f"\n{END}"

    original = INDEX.read_text(encoding="utf-8")
    if START not in original or END not in original:
        raise SystemExit(f"{INDEX} に {START} / {END} のマーカーがありません")
    head, _, rest = original.partition(START)
    _, _, tail = rest.partition(END)
    INDEX.write_text(head + block + tail, encoding="utf-8")
    print(f"{len(rows)} 冊を books/README.md に反映しました")


if __name__ == "__main__":
    main()
