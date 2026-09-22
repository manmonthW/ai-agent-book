#!/usr/bin/env python3
"""Generate one reviewable Markdown card for every catalogued experiment."""

from __future__ import annotations

import re
from pathlib import Path

ROOT=Path.cwd(); CATALOG=ROOT/"bluebook/data/experiment-catalog.yml"; OUT=ROOT/"bluebook/experiments/cards"


def parse_records(text:str):
    chunks=re.split(r"(?m)^  - id: ",text)[1:]
    records=[]
    for chunk in chunks:
        experiment_id=re.match(r'"([^\"]+)"',chunk).group(1)
        def field(name):
            m=re.search(rf'(?m)^    {name}: (.+)$',chunk)
            return m.group(1).strip().strip('"') if m else ""
        locations=re.findall(r'(?m)^      - "([^"]+)"$',chunk.split("projects:",1)[0])
        paths=re.findall(r'(?m)^        code_path: (.+)$',chunk)
        summaries=[]
        if "summaries:" in chunk:
            summaries=re.findall(r'(?m)^      - "([^"]+)"$',chunk.split("summaries:",1)[1].split("license_status:",1)[0])
        targets=[]
        if "target_chapters:" in chunk:
            targets=re.findall(r'(?m)^      - (.+)$',chunk.split("target_chapters:",1)[1].split("summaries:",1)[0])
        records.append({"id":experiment_id,"evidence":field("provisional_evidence"),"status":field("verification_status"),"locations":locations,"paths":[p.strip().strip('"') for p in paths],"summaries":summaries,"targets":targets})
    return records


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    records=parse_records(CATALOG.read_text(encoding="utf-8"))
    for record in records:
        chapter=record["id"].split("-")[0]
        directory=OUT/f"chapter{chapter}"; directory.mkdir(parents=True,exist_ok=True)
        summary=record["summaries"][0] if record["summaries"] else "待人工提炼。"
        source="、".join(record["locations"]) or "待登记"
        paths="\n".join(f"- `{p}`" for p in record["paths"] if p!="null") or "- 无独立代码目录或待核验"
        targets="、".join(record["targets"]) or "待映射"
        content=f"""# 实验 {record['id']}：{summary[:60]}

> 状态：自动生成，待证据审查  
> 初步证据等级：{record['evidence'] or 'E0'}  
> 验证状态：{record['status'] or 'pending'}

## 要回答的问题

{summary}

## 蓝皮书目标章节

{targets}

## 来源位置

{source}

## 代码与Artifact

{paths}

## 假设、基线与变量

待人工从正文和实验README提取。不得把项目存在视为假设成立。

## 输入、环境与版本

待核验模型、数据、工具、运行日期、硬件和外部依赖。

## 指标与完成门禁

待从EXPERIMENT_LEDGER、validation manifest或实验README登记。

## 观察结果

待审查原始证据后填写。失败、阻塞和未复现结果必须保留。

## 局限

- 当前证据等级仅基于目录和README状态；
- E3及以上需要真实运行或可复核Artifact；
- 不得跨模型、数据集或环境外推。

## 可支持的蓝皮书主张

待人工裁决。
"""
        (directory/f"experiment-{record['id']}.md").write_text(content,encoding="utf-8")
    print(f"cards: {len(records)}")
    if len(records)!=109: raise SystemExit("expected 109 cards")

if __name__=="__main__":main()
