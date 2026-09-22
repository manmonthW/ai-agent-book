#!/usr/bin/env python3
"""Release-level validation for the bluebook workspace."""
from pathlib import Path
import re,sys
ROOT=Path.cwd(); failures=[]
chapters=sorted(p for p in (ROOT/"bluebook/chapters").glob("[0-9][0-9]-*.md") if "sample" not in p.name)
if len(chapters)!=15: failures.append(f"expected 15 numbered chapters, got {len(chapters)}")
if not (ROOT/"bluebook/chapters/conclusion-adoption-roadmap.md").exists(): failures.append("missing conclusion")
patterns=list((ROOT/"bluebook/patterns").glob("P[0-9][0-9]-*.md"))
if len(patterns)!=20: failures.append(f"expected 20 pattern cards, got {len(patterns)}")
cards=list((ROOT/"bluebook/experiments/cards").rglob("experiment-*.md"))
if len(cards)!=109: failures.append(f"expected 109 experiment cards, got {len(cards)}")
reviewed=[p for p in cards if "状态：已审查" in p.read_text(encoding="utf-8")]
for eid in ("1-1","2-3","2-5","2-10"):
 hits=[p for p in reviewed if p.name==f"experiment-{eid}.md"]
 if len(hits)!=1: failures.append(f"missing reviewed priority experiment {eid}")
required_files=["bluebook/data/cross-reference.md","bluebook/plan/CORE_REVIEW_STRICT.md","bluebook/plan/ADVANCED_REVIEW_STRICT.md","bluebook/images/CORE_FIGURE_WIREFRAMES.md","bluebook/images/architecture/README.md"]
for name in required_files:
 if not (ROOT/name).exists(): failures.append(f"missing {name}")
for p in chapters+[ROOT/"bluebook/chapters/conclusion-adoption-roadmap.md"]:
 text=p.read_text(encoding="utf-8")
 if re.search(r"TODO|TBD|FIXME|待写",text,re.I): failures.append(f"placeholder in {p.name}")
 if "知识检查" not in text: failures.append(f"missing quiz in {p.name}")
for p in patterns:
 text=p.read_text(encoding="utf-8")
 for section in ("Context","Problem","Forces","Solution","Consequences","Failure Modes","Evidence","Exit Criteria","Checklist"):
  if f"## {section}" not in text: failures.append(f"{p.name} missing {section}")
if failures:
 print("Release validation FAILED"); [print(f"- {x}") for x in failures]; sys.exit(1)
print("Release validation PASSED")
print(f"- chapters: {len(chapters)} + conclusion")
print(f"- patterns: {len(patterns)}")
print(f"- experiment cards: {len(cards)} ({len(reviewed)} priority cards reviewed)")
