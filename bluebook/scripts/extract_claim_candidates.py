#!/usr/bin/env python3
"""Extract candidate quantitative and time-sensitive claims for manual governance review."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path.cwd()
SUPP = ROOT.parent / "ai-agents-for-beginners"
OUT = ROOT / "bluebook" / "data" / "claim-candidates.yml"
PATTERNS = [
    re.compile(r"\b(?:19|20)\d{2}\b"),
    re.compile(r"\d+(?:\.\d+)?\s*%"),
    re.compile(r"\d+(?:\.\d+)?\s*(?:倍|万|亿|token|Token|tokens|ms|秒|分钟|小时|天)"),
    re.compile(r"(?:提升|降低|减少|增加|优于|超过|翻倍|显著|最新|首次|第一)"),
]

SOURCES = [ROOT / "book" / "introduction.md"] + [ROOT / "book" / f"chapter{i}.md" for i in range(1, 11)] + [SUPP / f"{i:02d}-{name}" / "README.md" for i, name in []]
SOURCES += sorted(SUPP.glob("[0-9][0-9]-*/README.md"))


def q(value: Any) -> str:
    if value is None: return "null"
    if isinstance(value, (int, float)): return str(value)
    return json.dumps(str(value), ensure_ascii=False)


def yaml(data: Any, indent: int = 0) -> str:
    p = " " * indent
    if isinstance(data, dict):
        lines = []
        for k, v in data.items():
            if isinstance(v, (dict, list)): lines += [f"{p}{k}:", yaml(v, indent + 2)]
            else: lines.append(f"{p}{k}: {q(v)}")
        return "\n".join(lines)
    if isinstance(data, list):
        if not data: return p + "[]"
        lines = []
        for v in data:
            if isinstance(v, dict):
                items = list(v.items()); k, first = items[0]
                lines.append(f"{p}- {k}: {q(first)}")
                for k, nested in items[1:]: lines.append(f"{p}  {k}: {q(nested)}")
            else: lines.append(f"{p}- {q(v)}")
        return "\n".join(lines)
    return p + q(data)


def main() -> None:
    candidates = []
    for path in SOURCES:
        if not path.exists(): continue
        source = "primary" if ROOT in path.parents else "supplementary"
        base = ROOT if source == "primary" else SUPP
        in_fence = False
        for line_no, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if line.lstrip().startswith("```"): in_fence = not in_fence; continue
            stripped = line.strip()
            if in_fence or not stripped or stripped.startswith("|") or stripped.startswith("!["): continue
            hits = [pattern.pattern for pattern in PATTERNS if pattern.search(stripped)]
            if hits:
                candidates.append({
                    "id": f"candidate-{len(candidates)+1:04d}",
                    "source": source,
                    "path": path.relative_to(base).as_posix(),
                    "line": line_no,
                    "text": stripped[:600],
                    "signals": hits,
                    "review_status": "pending",
                    "disposition": None,
                })
    OUT.write_text(yaml({"version": 1, "status": "machine_candidates", "count": len(candidates), "candidates": candidates}) + "\n", encoding="utf-8")
    print(f"claim_candidates: {len(candidates)}")


if __name__ == "__main__": main()
