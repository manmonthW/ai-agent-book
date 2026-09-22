#!/usr/bin/env python3
"""Strict editorial audit for bluebook core chapters 1-8."""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path.cwd()
DIR = ROOT / "bluebook" / "chapters"
FILES = [
    DIR / "01-definition-and-boundaries.md",
    DIR / "02-when-to-use-agents.md",
    DIR / "03-agent-runtime.md",
    DIR / "04-context-engineering.md",
    DIR / "05-memory-rag-knowledge.md",
    DIR / "06-tools-protocols.md",
    DIR / "07-coding-agent.md",
    DIR / "08-multimodal-interaction.md",
]

PRECISION_RE = re.compile(
    r"(?:\b(?:19|20)\d{2}\b|\d+(?:\.\d+)?\s*%|\d+(?:\.\d+)?\s*(?:倍|万|亿|token|tokens|Token|ms|秒|分钟|小时|天|美元|元))",
    re.I,
)
ABSOLUTE_RE = re.compile(r"(?:一定|必然|完全|永远|从不|所有模型|普遍提升|显著提升|不可或缺)")
VENDOR_RE = re.compile(r"(?:Microsoft|Foundry|Azure|OpenAI|Anthropic|Claude|Gemini|Kimi|Qwen|LangGraph|LangChain)", re.I)
HEAD_RE = re.compile(r"^#{1,6}\s+(.+)$")
BULLET_RE = re.compile(r"^\s*[-*]\s+(.+)$")

findings: list[tuple[str, str, int, str]] = []
heading_counts: Counter[str] = Counter()
paragraphs: defaultdict[str, list[tuple[str, int]]] = defaultdict(list)

for path in FILES:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    in_fence = False
    current_para: list[str] = []
    para_start = 1

    def flush() -> None:
        if current_para:
            normalized = " ".join(part.strip() for part in current_para).strip()
            if len(normalized) >= 80:
                paragraphs[normalized].append((path.name, para_start))
        current_para.clear()

    for number, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            flush(); in_fence = not in_fence; continue
        if in_fence:
            continue
        heading = HEAD_RE.match(line)
        if heading:
            flush(); heading_counts[heading.group(1).strip()] += 1
            continue
        if not line.strip():
            flush(); continue
        if not current_para: para_start = number
        current_para.append(line)

        if PRECISION_RE.search(line):
            findings.append(("precision", path.name, number, line.strip()))
        if ABSOLUTE_RE.search(line) and not any(token in line for token in ("不采用", "不能", "避免", "不是", "不应")):
            findings.append(("absolute", path.name, number, line.strip()))
        if VENDOR_RE.search(line):
            findings.append(("vendor", path.name, number, line.strip()))
        if len(line) > 240:
            findings.append(("long_line", path.name, number, line[:240]))
    flush()

for paragraph, locations in paragraphs.items():
    if len(locations) > 1:
        findings.append(("duplicate_paragraph", ", ".join(f"{f}:{n}" for f, n in locations), 0, paragraph[:240]))

print("Strict core audit")
counts = Counter(kind for kind, *_ in findings)
for kind in ("precision", "absolute", "vendor", "long_line", "duplicate_paragraph"):
    print(f"- {kind}: {counts[kind]}")

report = ROOT / "bluebook" / "plan" / "CORE_AUDIT_RAW.md"
with report.open("w", encoding="utf-8") as handle:
    handle.write("# Core Architecture Raw Audit\n\n")
    handle.write("> Machine-generated candidates; each item requires editorial disposition.\n\n")
    for kind in ("absolute", "precision", "vendor", "duplicate_paragraph", "long_line"):
        handle.write(f"## {kind}\n\n")
        rows = [row for row in findings if row[0] == kind]
        if not rows:
            handle.write("None.\n\n")
        for _, file, number, content in rows:
            location = f"{file}:{number}" if number else file
            handle.write(f"- `{location}` — {content}\n")
        handle.write("\n")
print(f"report: {report}")
