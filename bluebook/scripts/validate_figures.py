#!/usr/bin/env python3
"""Validate the eight Excalidraw source files and exported SVGs."""
from pathlib import Path
import json,re,sys
ROOT=Path.cwd(); D=ROOT/"bluebook/images/architecture"; failures=[]
sources=sorted(D.glob("fig*.excalidraw")); svgs=sorted(D.glob("fig*.svg")); pngs=sorted(D.glob("fig*.png"))
if len(sources)!=8: failures.append(f"expected 8 Excalidraw sources, got {len(sources)}")
if len(svgs)!=8: failures.append(f"expected 8 SVG exports, got {len(svgs)}")
if len(pngs)!=8: failures.append(f"expected 8 PNG previews, got {len(pngs)}")
for p in sources:
 try:data=json.loads(p.read_text(encoding="utf-8"))
 except Exception as e:failures.append(f"{p.name}: invalid JSON {e}");continue
 if data.get("type")!="excalidraw" or data.get("version")!=2: failures.append(f"{p.name}: invalid header")
 els=data.get("elements",[]); ids=[e.get("id") for e in els]
 if len(ids)!=len(set(ids)): failures.append(f"{p.name}: duplicate ids")
 if not any(e.get("type")=="arrow" for e in els): failures.append(f"{p.name}: no arrows")
 for e in els:
  if e.get("type") in ("text","rectangle") and e.get("text") and e.get("fontFamily")!=5: failures.append(f"{p.name}:{e.get('id')}: fontFamily must be 5")
  if e.get("width",0)<0 or e.get("height",0)<0: failures.append(f"{p.name}:{e.get('id')}: negative size")
for p in svgs:
 text=p.read_text(encoding="utf-8")
 if not text.startswith("<svg") or "<title" not in text or "<desc" not in text: failures.append(f"{p.name}: accessibility metadata missing")
 if re.search(r"Microsoft|Azure|OpenAI|Anthropic|LangGraph",text,re.I): failures.append(f"{p.name}: vendor binding")
if failures:
 print("Figure validation FAILED");[print(f"- {x}") for x in failures];sys.exit(1)
print("Figure validation PASSED")
print("- 8 editable Excalidraw sources")
print("- 8 final SVG exports")
print("- 8 PNG previews")
