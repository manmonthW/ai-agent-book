#!/usr/bin/env python3
"""Strict editorial audit for chapters 9-14 and conclusion."""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path.cwd(); DIR=ROOT/"bluebook/chapters"
FILES=[DIR/name for name in (
"09-production-harness.md","10-evaluation-observability.md","11-security-governance.md",
"12-continuous-evolution.md","13-post-training.md","14-multi-agent.md","conclusion-adoption-roadmap.md")]
PRECISION=re.compile(r"(?:\b(?:19|20)\d{2}\b|\d+(?:\.\d+)?\s*%|\d+(?:\.\d+)?\s*(?:倍|万|亿|token|tokens|Token|ms|秒|分钟|小时|天|美元|元))",re.I)
ABSOLUTE=re.compile(r"(?:一定|必然|完全|永远|从不|所有模型|普遍提升|显著提升|不可或缺)")
VENDOR=re.compile(r"(?:Microsoft|Foundry|Azure|OpenAI|Anthropic|Claude|Gemini|Kimi|Qwen|LangGraph|LangChain)",re.I)
HEAD=re.compile(r"^#{1,6}\s+(.+)$")
findings=[]; paragraphs=defaultdict(list)
for path in FILES:
    lines=path.read_text(encoding="utf-8").splitlines(); in_fence=False; para=[]; start=1
    def flush():
        if para:
            normalized=" ".join(x.strip() for x in para).strip()
            if len(normalized)>=80: paragraphs[normalized].append((path.name,start))
        para.clear()
    for number,line in enumerate(lines,1):
        if line.lstrip().startswith("```"): flush(); in_fence=not in_fence; continue
        if in_fence: continue
        if HEAD.match(line) or not line.strip(): flush(); continue
        if not para: start=number
        para.append(line)
        if PRECISION.search(line): findings.append(("precision",path.name,number,line.strip()))
        if ABSOLUTE.search(line) and not any(x in line for x in ("不", "避免", "不能")): findings.append(("absolute",path.name,number,line.strip()))
        if VENDOR.search(line): findings.append(("vendor",path.name,number,line.strip()))
        if len(line)>240: findings.append(("long_line",path.name,number,line[:240]))
    flush()
for text,locations in paragraphs.items():
    if len(locations)>1: findings.append(("duplicate_paragraph",", ".join(f"{f}:{n}" for f,n in locations),0,text[:240]))

counts=Counter(kind for kind,*_ in findings)
report=ROOT/"bluebook/plan/ADVANCED_AUDIT_RAW.md"
with report.open("w",encoding="utf-8") as f:
    f.write("# Advanced Chapters Raw Audit\n\n> Machine-generated candidates for editorial disposition.\n\n")
    for kind in ("absolute","precision","vendor","duplicate_paragraph","long_line"):
        f.write(f"## {kind}\n\n")
        rows=[r for r in findings if r[0]==kind]
        if not rows:f.write("None.\n")
        for _,file,line,text in rows:f.write(f"- `{file}:{line}` — {text}\n")
        f.write("\n")
print("Strict advanced audit")
for kind in ("precision","absolute","vendor","long_line","duplicate_paragraph"):print(f"- {kind}: {counts[kind]}")
print(f"report: {report}")
