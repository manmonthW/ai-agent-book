#!/usr/bin/env python3
"""Quality checks for bluebook sample chapters."""

from pathlib import Path
import re

ROOT = Path.cwd()
CHAPTERS = {
    "00": ROOT / "bluebook/chapters/00-executive-summary.md",
    "02": ROOT / "bluebook/chapters/02-when-to-use-agents.md",
    "04": ROOT / "bluebook/chapters/04-context-engineering.md",
    "09-11": ROOT / "bluebook/chapters/09-11-production-control-plane-sample.md",
}

required_sections = ["知识检查"]
forbidden = [
    r"(?<!不采用[“\"])(?<!不能支持[“\"])(?<!不采用)(?<!拒绝绝对化表述：)每个上下文组件都不可或缺",
    r"Prompt.{0,8}(?:提供|构成|作为)硬(?:安全|权限)边界",
    r"Smoke Test.{0,8}(?:足以|能够|可以)(?:证明|保证).{0,8}(?:完整质量|生产就绪)",
]

failures: list[str] = []
for chapter_id, path in CHAPTERS.items():
    if not path.exists():
        failures.append(f"{chapter_id}: missing {path}")
        continue
    text = path.read_text(encoding="utf-8")
    if len(text.splitlines()) < 80:
        failures.append(f"{chapter_id}: suspiciously short")
    for section in required_sections:
        if section not in text:
            failures.append(f"{chapter_id}: missing section {section}")
    if "本章回答的三个问题" not in text and "本样章回答的三个问题" not in text:
        failures.append(f"{chapter_id}: missing opening questions")
    for pattern in forbidden:
        if re.search(pattern, text, re.I | re.S):
            failures.append(f"{chapter_id}: forbidden absolute claim matches {pattern}")

# Sample-specific evidence requirements.
context = CHAPTERS["04"].read_text(encoding="utf-8")
for experiment in ("实验1-1", "实验2-3", "实验2-10"):
    if experiment not in context:
        failures.append(f"04: missing evidence reference {experiment}")

production = CHAPTERS["09-11"].read_text(encoding="utf-8")
for term in ("幂等", "Checkpoint", "Offline Evaluation", "密码学回执", "回滚"):
    if term not in production:
        failures.append(f"09-11: missing production concept {term}")

if failures:
    print("Sample chapter validation FAILED")
    for failure in failures:
        print(f"- {failure}")
    raise SystemExit(1)

print("Sample chapter validation PASSED")
for chapter_id, path in CHAPTERS.items():
    print(f"- {chapter_id}: {len(path.read_text(encoding='utf-8').splitlines())} lines")
