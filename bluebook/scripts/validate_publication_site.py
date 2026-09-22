#!/usr/bin/env python3
"""Validate the assembled HTML publication."""
from pathlib import Path
import re,sys
ROOT=Path.cwd(); D=ROOT/"dist/site"; failures=[]
required=["index.html","chapters/00-executive-summary/index.html","chapters/14-multi-agent/index.html","patterns/P20-multi-agent-admission/index.html","experiments/index.html","experiments/1-1/index.html","experiments/10-6/index.html","appendices/index.html"]
for p in required:
 if not (D/p).is_file():failures.append(f"missing {p}")
html=list(D.rglob("*.html"))
if len(html)<150:failures.append(f"expected >=150 HTML pages, got {len(html)}")
if len(list((D/"experiments").glob("*-*/index.html")))!=109:failures.append("expected 109 experiment detail pages")
for banned in ("09-11-production-control-plane-sample","_CHAPTER_TEMPLATE","_PATTERN_CARD"):
 if any(banned in str(p) for p in D.rglob("*")):failures.append(f"editorial artifact leaked: {banned}")
index=(D/"index.html").read_text(encoding="utf-8") if (D/"index.html").exists() else ""
for marker in ("最低充分自主性","让模型处理不确定性","先看证据状态"):
 if marker not in index:failures.append(f"home missing marker: {marker}")
if not (D/"assets/bluebook.css").exists() or not (D/"assets/bluebook.js").exists():failures.append("theme assets missing")
exp_index=(D/"experiments/index.html").read_text(encoding="utf-8") if (D/"experiments/index.html").exists() else ""
if re.search(r'href=["\'][^"\']+\.md["\']',exp_index):failures.append("experiment catalog leaked source .md links")
if 'href="./1-1/"' not in exp_index:failures.append("experiment catalog route is not anchored to experiments directory")
sitemap=(D/"sitemap.xml").read_text(encoding="utf-8") if (D/"sitemap.xml").exists() else ""
if sitemap.count("<url>") < 150 or "https://www.keaimentor.com/bluebook/experiments/1-1/" not in sitemap:failures.append("sitemap missing publication routes")
fallback=(D/"404.html").read_text(encoding="utf-8") if (D/"404.html").exists() else ""
if 'href="/assets/' in fallback or 'href="/chapters/' in fallback:failures.append("404 page escapes /bluebook base path")
for p in html:
 text=p.read_text(encoding="utf-8")
 if re.search(r'(?:href|src)=["\']/(?:assets|chapters|patterns|experiments|appendices|search)/',text):failures.append(f"page escapes /bluebook base path: {p.relative_to(D)}");break
if failures:
 print("Publication site validation FAILED");[print(f"- {x}") for x in failures];sys.exit(1)
print("Publication site validation PASSED")
print(f"- HTML pages: {len(html)}")
print("- experiment detail pages: 109")
print("- editorial samples/templates excluded")
