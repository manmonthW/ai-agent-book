#!/usr/bin/env python3
"""Assemble and build the standalone bluebook publication site."""
from __future__ import annotations
import argparse, html, re, shutil, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; BLUE=ROOT/"bluebook"; SITE=BLUE/"site"; DIST=ROOT/"dist"
EXCLUDE={"09-11-production-control-plane-sample.md","_CHAPTER_TEMPLATE.md","_PATTERN_CARD.md"}

def clean():
 shutil.rmtree(SITE,ignore_errors=True); SITE.mkdir(parents=True)
def cp(src:Path,dst:Path): dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst)
def rewrite(text:str)->str:
 text=text.replace("../images/architecture/","../assets/figures/")
 text=re.sub(r'^> 状态：Release Candidate 1\s*$', '<span class="release-badge">Release Candidate 1</span>',text,flags=re.M)
 return text
def build_experiment_catalog(rows):
 def natural(eid):return tuple(int(x) for x in eid.split("-"))
 groups={}
 for eid,title,level,status in sorted(rows,key=lambda r:natural(r[0])):
  chapter=int(eid.split("-")[0]);groups.setdefault(chapter,[]).append((eid,title,level,status))
 out=['<div class="experiment-catalog">']
 for chapter,items in groups.items():
  out.append(f'<section class="experiment-group" data-chapter="{chapter}"><header><span>CHAPTER {chapter:02d}</span><strong>{len(items)} experiments</strong></header><div class="experiment-cards">')
  for eid,title,level,status in items:
   clean=title.replace(f"实验 {eid}：","").replace(f"实验{eid}：","")
   search=f"{eid} {clean} {level} {status} chapter {chapter}"
   state_class="reviewed" if status=="已审查" else "pending"
   evidence_class=re.sub(r"[^a-z0-9]","",level.lower()) or "unknown"
   out.append(f'<article class="experiment-card" data-search="{html.escape(search,quote=True)}"><a class="experiment-id" href="./{eid}/">{eid}</a><div class="experiment-copy"><h2><a href="./{eid}/">{html.escape(clean)}</a></h2><div class="experiment-meta"><span class="evidence {evidence_class}">{html.escape(level)}</span><span class="state {state_class}">{status}</span></div></div></article>')
  out.append('</div></section>')
 out.append('</div>');return "\n".join(out)
def prepare():
 clean();
 # Home and editorial landing pages.
 cp(BLUE/"publishing/index.md",SITE/"index.md")
 for p in sorted((BLUE/"chapters").glob("*.md")):
  if p.name in EXCLUDE: continue
  if p.name=="README.md":
   cp(BLUE/"publishing/chapters-index.md",SITE/"chapters/index.md")
   continue
  name=p.name
  dst=SITE/"chapters"/name;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(rewrite(p.read_text(encoding="utf-8")),encoding="utf-8")
 for p in sorted((BLUE/"patterns").glob("*.md")):
  if p.name in EXCLUDE:continue
  name="index.md" if p.name=="README.md" else p.name
  dst=SITE/"patterns"/name;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(rewrite(p.read_text(encoding="utf-8")),encoding="utf-8")
 # Experiments: 109 pages, with a generated evidence-first catalog.
 exp_out=SITE/"experiments";exp_out.mkdir(parents=True,exist_ok=True)
 rows=[]
 for p in sorted((BLUE/"experiments/cards").rglob("experiment-*.md")):
  text=p.read_text(encoding="utf-8");eid=p.stem.removeprefix("experiment-"); title=text.splitlines()[0].replace("# ","")
  level=(re.search(r"证据等级：([^（\n]+)",text) or re.search(r"初步证据等级：([^\n]+)",text)); level=level.group(1).strip() if level else "待核验"
  reviewed="已审查" if "状态：已审查" in text else "待证据审查"
  dst=exp_out/f"{eid}.md";dst.write_text(text,encoding="utf-8");rows.append((eid,title,level,reviewed))
 catalog=(BLUE/"publishing/experiments-index.md").read_text(encoding="utf-8")+"\n\n"+build_experiment_catalog(rows)+"\n"
 (exp_out/"index.md").write_text(catalog,encoding="utf-8")
 # Appendices and assets.
 cp(BLUE/"publishing/appendices-index.md",SITE/"appendices/index.md")
 cp(BLUE/"data/cross-reference.md",SITE/"appendices/cross-reference.md")
 cp(BLUE/"CHANGELOG.md",SITE/"appendices/changelog.md")
 cross=SITE/"appendices/cross-reference.md";ct=cross.read_text(encoding="utf-8")
 ct=re.sub(r"\.\./experiments/cards/chapter\d+/experiment-(\d+-\d+)\.md",r"../experiments/\1.md",ct)
 cross.write_text(ct,encoding="utf-8")
 for p in (BLUE/"images/architecture").glob("*.svg"):cp(p,SITE/"assets/figures"/p.name)
 cp(BLUE/"publishing/bluebook.css",SITE/"assets/bluebook.css");cp(BLUE/"publishing/bluebook.js",SITE/"assets/bluebook.js")

def main():
 ap=argparse.ArgumentParser();ap.add_argument("--prepare-only",action="store_true");ap.add_argument("--serve",action="store_true");a=ap.parse_args();prepare()
 if a.prepare_only:print(f"prepared {SITE}");return
 try:import mkdocs # noqa
 except ImportError:print("MkDocs is not installed. Run: python3 -m pip install -r bluebook/requirements-publishing.txt",file=sys.stderr);raise SystemExit(2)
 cmd=[sys.executable,"-m","mkdocs","serve" if a.serve else "build","-f",str(BLUE/"mkdocs.yml")]
 if not a.serve:cmd.append("--strict")
 subprocess.run(cmd,check=True,cwd=BLUE)
if __name__=="__main__":main()
