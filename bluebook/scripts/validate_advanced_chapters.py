#!/usr/bin/env python3
"""Strict structural checks for chapters 9-14 and conclusion."""

from pathlib import Path
import re

ROOT = Path.cwd(); DIR = ROOT / "bluebook/chapters"
FILES = {
    9: "09-production-harness.md",
    10: "10-evaluation-observability.md",
    11: "11-security-governance.md",
    12: "12-continuous-evolution.md",
    13: "13-post-training.md",
    14: "14-multi-agent.md",
    "conclusion": "conclusion-adoption-roadmap.md",
}
required = ["本章回答的三个问题", "5分钟速读", "检查清单", "知识检查", "来源"]
forbidden = [
    r"Prompt.{0,8}(?:保证|提供).{0,8}(?:授权|权限安全)",
    r"多\s*Agent.{0,8}(?:一定|必然).{0,8}(?:更好|更智能)",
    r"密码学回执.{0,12}(?:证明动作正确|证明合规)",
    r"Smoke Test.{0,8}(?:足以|能够|可以)(?:证明|保证).{0,8}(?:完整质量|生产就绪)",
]
failures=[]
for chapter, filename in FILES.items():
    path=DIR/filename
    if not path.exists(): failures.append(f"{chapter}: missing"); continue
    text=path.read_text(encoding="utf-8")
    if len(text.splitlines())<100: failures.append(f"{chapter}: too short")
    for section in required:
        if section not in text: failures.append(f"{chapter}: missing {section}")
    for pattern in forbidden:
        if re.search(pattern,text,re.I|re.S): failures.append(f"{chapter}: forbidden {pattern}")

if failures:
    print("Advanced chapter validation FAILED")
    for failure in failures: print(f"- {failure}")
    raise SystemExit(1)
print("Advanced chapter validation PASSED")
for chapter, filename in FILES.items():
    path=DIR/filename
    print(f"- {chapter}: {len(path.read_text(encoding='utf-8').splitlines())} lines")
