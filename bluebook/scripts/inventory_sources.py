#!/usr/bin/env python3
"""Inventory Markdown, notebooks, figures, and lesson/experiment entries in both source repos."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
LINK_RE = re.compile(r"!?\[([^\]]*)\]\(([^)]+)\)")
EXPERIMENT_RE = re.compile(r"(?:实验\s*)?(?<!\d)(\d{1,2})-(\d{1,2})(?!\d)")


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def markdown_record(path: Path, root: Path, source_id: str) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    headings: list[dict[str, Any]] = []
    links: list[dict[str, Any]] = []
    experiments: set[str] = set()
    code_fences = 0
    in_fence = False

    for line_no, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            if in_fence:
                code_fences += 1
            continue
        if in_fence:
            continue
        match = HEADING_RE.match(line)
        if match:
            headings.append({"level": len(match.group(1)), "title": match.group(2), "line": line_no})
        for label, target in LINK_RE.findall(line):
            links.append({"label": label, "target": target, "line": line_no})
        for chapter, number in EXPERIMENT_RE.findall(line):
            experiments.add(f"{chapter}-{number}")

    return {
        "id": f"{source_id}:md:{rel(path, root)}",
        "source": source_id,
        "type": "markdown",
        "path": rel(path, root),
        "line_count": len(text.splitlines()),
        "headings": headings,
        "links": links,
        "experiment_mentions": sorted(experiments, key=lambda item: tuple(map(int, item.split("-")))),
        "code_fence_count": code_fences,
        "target": None,
        "action": "unreviewed",
        "review_status": "pending",
    }


def notebook_record(path: Path, root: Path, source_id: str) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    cells = data.get("cells", [])
    return {
        "id": f"{source_id}:notebook:{rel(path, root)}",
        "source": source_id,
        "type": "notebook",
        "path": rel(path, root),
        "cell_count": len(cells),
        "markdown_cells": sum(cell.get("cell_type") == "markdown" for cell in cells),
        "code_cells": sum(cell.get("cell_type") == "code" for cell in cells),
        "target": None,
        "action": "unreviewed",
        "review_status": "pending",
    }


def asset_record(path: Path, root: Path, source_id: str) -> dict[str, Any]:
    return {
        "id": f"{source_id}:figure:{rel(path, root)}",
        "source": source_id,
        "path": rel(path, root),
        "format": path.suffix.lower().lstrip("."),
        "size_bytes": path.stat().st_size,
        "action": "unreviewed",
        "target": None,
        "license_status": "pending",
    }


def discover_experiments(primary: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for chapter in range(1, 11):
        chapter_root = primary / f"chapter{chapter}"
        readme = chapter_root / "README.md"
        mentions: list[str] = []
        project_map: dict[str, set[str]] = {}
        if readme.exists():
            text = readme.read_text(encoding="utf-8", errors="replace")
            mentions = sorted(
                {f"{a}-{b}" for a, b in EXPERIMENT_RE.findall(text) if int(a) == chapter},
                key=lambda item: tuple(map(int, item.split("-"))),
            )
            for line in text.splitlines():
                ids = [f"{a}-{b}" for a, b in EXPERIMENT_RE.findall(line) if int(a) == chapter]
                link_match = re.search(r"\]\(([^)#]+?)/?\)", line)
                if ids and link_match:
                    project = link_match.group(1).strip("./")
                    for experiment_id in ids:
                        project_map.setdefault(experiment_id, set()).add(project)
        directories = sorted(
            p.name for p in chapter_root.iterdir()
            if p.is_dir() and not p.name.startswith(".")
        ) if chapter_root.exists() else []
        records.append({
            "source": "primary",
            "chapter": chapter,
            "readme": rel(readme, primary) if readme.exists() else None,
            "experiment_ids": mentions,
            "experiment_projects": {key: sorted(value) for key, value in sorted(project_map.items())},
            "project_directories": directories,
            "verification_status": "unreviewed",
        })
    return records


def discover_supplementary_lessons(supplementary: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for directory in sorted(supplementary.glob("[0-9][0-9]-*")):
        if not directory.is_dir():
            continue
        records.append({
            "source": "supplementary",
            "lesson": directory.name,
            "readme": rel(directory / "README.md", supplementary) if (directory / "README.md").exists() else None,
            "notebooks": sorted(rel(p, supplementary) for p in directory.rglob("*.ipynb")),
            "role": "supplement",
            "review_status": "pending",
        })
    return records


def yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(str(value), ensure_ascii=False)


def to_yaml(data: Any, indent: int = 0) -> str:
    prefix = " " * indent
    if isinstance(data, dict):
        lines: list[str] = []
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                lines.append(f"{prefix}{key}:")
                lines.append(to_yaml(value, indent + 2))
            else:
                lines.append(f"{prefix}{key}: {yaml_scalar(value)}")
        return "\n".join(lines)
    if isinstance(data, list):
        if not data:
            return f"{prefix}[]"
        lines = []
        for value in data:
            if isinstance(value, dict):
                items = list(value.items())
                first_key, first_value = items[0]
                if isinstance(first_value, (dict, list)):
                    lines.append(f"{prefix}- {first_key}:")
                    lines.append(to_yaml(first_value, indent + 4))
                else:
                    lines.append(f"{prefix}- {first_key}: {yaml_scalar(first_value)}")
                for key, nested in items[1:]:
                    if isinstance(nested, (dict, list)):
                        lines.append(f"{prefix}  {key}:")
                        lines.append(to_yaml(nested, indent + 4))
                    else:
                        lines.append(f"{prefix}  {key}: {yaml_scalar(nested)}")
            elif isinstance(value, list):
                lines.append(f"{prefix}-")
                lines.append(to_yaml(value, indent + 2))
            else:
                lines.append(f"{prefix}- {yaml_scalar(value)}")
        return "\n".join(lines)
    return f"{prefix}{yaml_scalar(data)}"


def dump_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(to_yaml(data) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--primary", type=Path, required=True)
    parser.add_argument("--supplementary", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    primary = args.primary.resolve()
    supplementary = args.supplementary.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    ignored_parts = {
        ".git", ".venv", "venv", "node_modules", "site", "dist", "build",
        "translations", "translated_images", "cursor-chats", "bluebook",
    }

    content_units: list[dict[str, Any]] = []
    notebooks: list[dict[str, Any]] = []
    figures: list[dict[str, Any]] = []

    for source_id, root in (("primary", primary), ("supplementary", supplementary)):
        for path in root.rglob("*"):
            if not path.is_file() or any(part in ignored_parts for part in path.parts):
                continue
            if path.suffix.lower() == ".md":
                content_units.append(markdown_record(path, root, source_id))
            elif path.suffix.lower() == ".ipynb":
                try:
                    notebooks.append(notebook_record(path, root, source_id))
                except (json.JSONDecodeError, OSError) as exc:
                    notebooks.append({
                        "id": f"{source_id}:notebook:{rel(path, root)}",
                        "source": source_id,
                        "type": "notebook",
                        "path": rel(path, root),
                        "parse_error": str(exc),
                        "review_status": "blocked",
                    })
            elif path.suffix.lower() in {".svg", ".png", ".jpg", ".jpeg", ".gif", ".webp"}:
                figures.append(asset_record(path, root, source_id))

    content_units.sort(key=lambda item: (item["source"], item["path"]))
    notebooks.sort(key=lambda item: (item["source"], item["path"]))
    figures.sort(key=lambda item: (item["source"], item["path"]))

    source_map = {
        "version": 1,
        "generated": True,
        "sources": [
            {"id": "primary", "repo": primary.name, "root": str(primary), "role": "primary"},
            {"id": "supplementary", "repo": supplementary.name, "root": str(supplementary), "role": "supplement"},
        ],
        "content_units": content_units,
        "notebooks": notebooks,
    }
    experiments = {
        "version": 1,
        "generated": True,
        "primary_chapters": discover_experiments(primary),
        "supplementary_lessons": discover_supplementary_lessons(supplementary),
        "experiment_cards": [],
    }
    figure_data = {"version": 1, "generated": True, "figures": figures}
    summary = {
        "primary_markdown": sum(item["source"] == "primary" for item in content_units),
        "supplementary_markdown": sum(item["source"] == "supplementary" for item in content_units),
        "primary_notebooks": sum(item["source"] == "primary" for item in notebooks),
        "supplementary_notebooks": sum(item["source"] == "supplementary" for item in notebooks),
        "primary_figures": sum(item["source"] == "primary" for item in figures),
        "supplementary_figures": sum(item["source"] == "supplementary" for item in figures),
        "primary_experiment_mentions": sum(len(item["experiment_ids"]) for item in experiments["primary_chapters"]),
        "supplementary_lessons": len(experiments["supplementary_lessons"]),
    }

    dump_yaml(output / "source-map.yml", source_map)
    dump_yaml(output / "experiments.yml", experiments)
    dump_yaml(output / "figures.yml", figure_data)
    dump_yaml(output / "inventory-summary.yml", summary)
    print(to_yaml(summary))


if __name__ == "__main__":
    main()
