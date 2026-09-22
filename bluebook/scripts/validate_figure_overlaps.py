#!/usr/bin/env python3
"""Detect arrow segments crossing rectangle interiors in selected figures."""
from pathlib import Path
import json,sys
D=Path.cwd()/"bluebook/images/architecture"; failures=[]
for stem in ("fig03-unified-execution-graph","fig07-coding-agent-loop","fig08-modality-time-control"):
 data=json.loads((D/f"{stem}.excalidraw").read_text(encoding="utf-8")); rects=[e for e in data["elements"] if e["type"]=="rectangle"]
 for a in [e for e in data["elements"] if e["type"]=="arrow"]:
  pts=[(a["x"]+p[0],a["y"]+p[1]) for p in a["points"]]
  if a.get("strokeStyle")=="dashed":
   continue
  for r in rects:
   for idx,(p,q) in enumerate(zip(pts,pts[1:])):
    # Sample segment interior; endpoints may intentionally touch a rectangle edge.
    for step in range(1,20):
     t=step/20;x=p[0]+(q[0]-p[0])*t;y=p[1]+(q[1]-p[1])*t
     if r["x"]+2<x<r["x"]+r["width"]-2 and r["y"]+2<y<r["y"]+r["height"]-2:
      # Ignore source/target shape only when penetration remains within 8 px.
      edge=min(x-r["x"],r["x"]+r["width"]-x,y-r["y"],r["y"]+r["height"]-y)
      if edge>8: failures.append(f"{stem}: {a['id']} crosses {r['id']}")
      break
    if failures and failures[-1].startswith(f"{stem}: {a['id']} crosses {r['id']}"): break
if failures:
 print("Figure overlap validation FAILED");[print(f"- {x}") for x in sorted(set(failures))];sys.exit(1)
print("Figure overlap validation PASSED (fig03, fig07, fig08)")
