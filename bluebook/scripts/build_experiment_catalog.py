#!/usr/bin/env python3
"""Enrich the 109 primary experiments with chapter targets and provisional evidence metadata."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path.cwd()
OUT = ROOT / "bluebook" / "data" / "experiment-catalog.yml"
ROW_RE = re.compile(r"^\|\s*([0-9][0-9,\-\s]*)\s*\|\s*(.*?)\s*\|\s*([✅📖🚧❌][^|]*)\|\s*(.*?)\s*\|\s*$")
ID_RE = re.compile(r"(?<!\d)(\d{1,2})-(\d{1,2})(?!\d)")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

TARGETS = {1: [1, 2, 3, 9], 2: [4, 11], 3: [5], 4: [6, 11], 5: [7], 6: [8, 9, 11], 7: [10], 8: [13], 9: [12], 10: [14]}
STATUS_MAP = {"✅": "implementation_present", "📖": "external_reproduction", "🚧": "design_only", "❌": "unavailable"}
EVIDENCE_MAP = {"✅": "E2", "📖": "E1", "🚧": "E0", "❌": "E0"}


def yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(str(value), ensure_ascii=False)


def yaml(data: Any, indent: int = 0) -> str:
    p = " " * indent
    if isinstance(data, dict):
        lines: list[str] = []
        for key, value in data.items():
            if isinstance(value, (dict, list)): lines += [f"{p}{key}:", yaml(value, indent + 2)]
            else: lines.append(f"{p}{key}: {yaml_scalar(value)}")
        return "\n".join(lines)
    if isinstance(data, list):
        if not data: return p + "[]"
        lines: list[str] = []
        for value in data:
            if isinstance(value, dict):
                items = list(value.items()); key, first = items[0]
                lines.append(f"{p}- {key}: {yaml_scalar(first)}")
                for key, nested in items[1:]:
                    if isinstance(nested, (dict, list)): lines += [f"{p}  {key}:", yaml(nested, indent + 4)]
                    else: lines.append(f"{p}  {key}: {yaml_scalar(nested)}")
            else: lines.append(f"{p}- {yaml_scalar(value)}")
        return "\n".join(lines)
    return p + yaml_scalar(data)


def clean(value: str) -> str:
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    return re.sub(r"[*_`]", "", value).strip()


def main() -> None:
    records: dict[str, dict[str, Any]] = {}
    for catalog_chapter in range(1, 11):
        path = ROOT / f"chapter{catalog_chapter}" / "README.md"
        for line_no, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            match = ROW_RE.match(line)
            if not match: continue
            id_cell, project_cell, status_cell, description = match.groups()
            ids = [f"{a}-{b}" for a, b in ID_RE.findall(id_cell)]
            if not ids: continue
            symbol = status_cell.strip()[0]
            links = LINK_RE.findall(project_cell)
            project_path = links[0][1].rstrip("/") if links else None
            for experiment_id in ids:
                actual_chapter = int(experiment_id.split("-")[0])
                record = records.setdefault(experiment_id, {
                    "id": experiment_id,
                    "source": "primary",
                    "catalog_locations": [],
                    "projects": [],
                    "catalog_statuses": [],
                    "artifact_class": STATUS_MAP.get(symbol, "unknown"),
                    "provisional_evidence": EVIDENCE_MAP.get(symbol, "E0"),
                    "verification_status": "pending",
                    "target_chapters": TARGETS[actual_chapter],
                    "summaries": [],
                    "license_status": "pending",
                })
                record["catalog_locations"].append(f"chapter{catalog_chapter}/README.md:{line_no}")
                record["projects"].append({
                    "name": clean(project_cell),
                    "code_path": f"chapter{catalog_chapter}/{project_path}" if project_path and not project_path.startswith("http") else None,
                })
                record["catalog_statuses"].append(status_cell.strip())
                record["summaries"].append(clean(description))
                # Keep the least-strong provisional evidence when duplicate rows disagree.
                rank = {"E0": 0, "E1": 1, "E2": 2}
                candidate = EVIDENCE_MAP.get(symbol, "E0")
                if rank[candidate] < rank[record["provisional_evidence"]]: record["provisional_evidence"] = candidate

    ordered = sorted(records.values(), key=lambda record: tuple(map(int, record["id"].split("-"))))
    OUT.write_text(yaml({
        "version": 1,
        "status": "provisional",
        "count": len(ordered),
        "evidence_note": "Catalog status only proves documentation/code presence. E3+ requires execution evidence review.",
        "experiments": ordered,
    }) + "\n", encoding="utf-8")
    print(f"experiments: {len(ordered)}")
    if len(ordered) != 109: raise SystemExit(f"expected 109 experiments, got {len(ordered)}")


if __name__ == "__main__": main()
