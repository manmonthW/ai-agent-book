#!/usr/bin/env python3
"""Structural quality checks for core architecture chapters 1-8."""

from pathlib import Path
import re

ROOT = Path.cwd()
CHAPTERS = {
    1: "01-definition-and-boundaries.md",
    2: "02-when-to-use-agents.md",
    3: "03-agent-runtime.md",
    4: "04-context-engineering.md",
    5: "05-memory-rag-knowledge.md",
    6: "06-tools-protocols.md",
    7: "07-coding-agent.md",
    8: "08-multimodal-interaction.md",
}
DIR = ROOT / "bluebook" / "chapters"
required = ["本章回答的三个问题", "5分钟速读", "检查清单", "知识检查", "来源"]
forbidden = [
    r"(?<!不采用[“\"])(?<!不能支持[“\"])(?<!不采用)(?<!拒绝绝对化表述：)每个上下文组件都不可或缺",
    r"多\s*Agent.{0,8}(?:一定|必然).{0,8}(?:更好|更智能)",
    r"Prompt.{0,8}(?:保证|提供).{0,8}(?:授权|权限安全)",
]
failures = []
for number, filename in CHAPTERS.items():
    path = DIR / filename
    if not path.exists(): failures.append(f"ch{number}: missing"); continue
    text = path.read_text(encoding="utf-8")
    if len(text.splitlines()) < 100: failures.append(f"ch{number}: too short")
    for section in required:
        if section not in text: failures.append(f"ch{number}: missing {section}")
    for pattern in forbidden:
        if re.search(pattern, text, re.I | re.S): failures.append(f"ch{number}: forbidden {pattern}")

if failures:
    print("Core chapter validation FAILED")
    for failure in failures: print(f"- {failure}")
    raise SystemExit(1)
print("Core chapter validation PASSED")
for number, filename in CHAPTERS.items():
    path = DIR / filename
    print(f"- ch{number}: {len(path.read_text(encoding='utf-8').splitlines())} lines")
