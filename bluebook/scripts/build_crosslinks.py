#!/usr/bin/env python3
"""Build chapter-pattern-experiment cross-reference indexes."""
from pathlib import Path
import re
ROOT=Path.cwd(); chapters=ROOT/"bluebook/chapters"; patterns=ROOT/"bluebook/patterns"; cards=ROOT/"bluebook/experiments/cards"
chapter_files={int(m.group(1)):p for p in chapters.glob("[0-9][0-9]-*.md") if (m:=re.match(r"(\d+)-",p.name))}
pattern_rows=[]
for p in sorted(patterns.glob("P[0-9][0-9]-*.md")):
 text=p.read_text(encoding="utf-8"); title=text.splitlines()[0].lstrip("# "); nums=[int(x) for x in re.findall(r"第(\d+)",text.split("## Context",1)[0])]; pattern_rows.append((p,title,nums))
exp_rows=[]
for p in sorted(cards.rglob("experiment-*.md")):
 text=p.read_text(encoding="utf-8"); eid=re.search(r"experiment-(\d+-\d+)\.md",p.name).group(1); nums=[]
 for n in chapter_files:
  if re.search(rf"第{n}章",text): nums.append(n)
 exp_rows.append((p,eid,sorted(set(nums))))
lines=["# 章节—模式—实验交叉索引","","> 自动生成；实验无人工映射时仍保留目录入口。",""]
for n,p in sorted(chapter_files.items()):
 ps=[(x,t) for x,t,ns in pattern_rows if n in ns]; es=[(x,e) for x,e,ns in exp_rows if n in ns]
 lines += [f"## 第{n}章", "", f"章节：[`{p.name}`](../chapters/{p.name})", "", "### 模式"]
 lines += [f"- [{t}](../patterns/{x.name})" for x,t in ps] or ["- 暂无直接模式映射"]
 lines += ["", "### 已审查实验"]
 reviewed=[]
 for x,e in es:
  if "状态：已审查" in x.read_text(encoding="utf-8"): reviewed.append(f"- [实验{e}](../experiments/cards/{x.parent.name}/{x.name})")
 lines += reviewed or ["- 暂无直接已审查实验"]
 lines.append("")
(ROOT/"bluebook/data/cross-reference.md").write_text("\n".join(lines),encoding="utf-8")
print(f"chapters={len(chapter_files)} patterns={len(pattern_rows)} experiments={len(exp_rows)}")
