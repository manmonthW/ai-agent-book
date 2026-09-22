#!/usr/bin/env python3
"""Validate generated bluebook governance artifacts without third-party dependencies."""

from pathlib import Path
import re

ROOT = Path.cwd()
DATA = ROOT / "bluebook" / "data"

checks = {
    "primary_experiments_109": (DATA / "experiment-catalog.yml", r"^count: 109$", re.M),
    "curated_units_33": (DATA / "curated-source-map.yml", r"^  - id: ", re.M),
    "glossary_terms_20": (DATA / "glossary.yml", r"^  - id: ", re.M),
    "claims_seeded": (DATA / "claims.yml", r"^  - id: ", re.M),
}

failures = []
for name, (path, pattern, flags) in checks.items():
    if not path.exists():
        failures.append(f"{name}: missing {path}")
        continue
    text = path.read_text(encoding="utf-8")
    matches = re.findall(pattern, text, flags)
    if name == "curated_units_33" and len(matches) != 33:
        failures.append(f"{name}: expected 33, got {len(matches)}")
    elif name == "glossary_terms_20" and len(matches) != 20:
        failures.append(f"{name}: expected 20, got {len(matches)}")
    elif name == "claims_seeded" and len(matches) < 8:
        failures.append(f"{name}: expected >=8, got {len(matches)}")
    elif name == "primary_experiments_109" and not matches:
        failures.append(f"{name}: count not found")

required = [
    ROOT / "LICENSE",
    ROOT.parent / "ai-agents-for-beginners" / "LICENSE",
    ROOT / "bluebook" / "editorial" / "EVIDENCE_POLICY.md",
    ROOT / "bluebook" / "editorial" / "LICENSE_POLICY.md",
]
for path in required:
    if not path.exists(): failures.append(f"required file missing: {path}")

if failures:
    print("Governance validation FAILED")
    for failure in failures: print(f"- {failure}")
    raise SystemExit(1)

print("Governance validation PASSED")
for name in checks: print(f"- {name}")
