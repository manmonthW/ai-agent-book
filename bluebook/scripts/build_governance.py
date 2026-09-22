#!/usr/bin/env python3
"""Build curated source mapping and governance seeds for the bluebook."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


PRIMARY = Path.cwd()
SUPPLEMENTARY = (PRIMARY.parent / "ai-agents-for-beginners").resolve()
DATA = PRIMARY / "bluebook" / "data"

CHAPTER_MAP: dict[str, dict[str, Any]] = {
    "book/introduction.md": {"targets": [0, 1], "action": "rewrite", "role": "primary"},
    "book/chapter1.md": {"targets": [1, 2, 3, 9], "action": "split_rewrite", "role": "primary"},
    "book/chapter2.md": {"targets": [4, 11], "action": "split_rewrite", "role": "primary"},
    "book/chapter3.md": {"targets": [5], "action": "rewrite", "role": "primary"},
    "book/chapter4.md": {"targets": [6, 11], "action": "split_rewrite", "role": "primary"},
    "book/chapter5.md": {"targets": [7], "action": "rewrite", "role": "primary"},
    "book/chapter6.md": {"targets": [8, 9, 11], "action": "split_rewrite", "role": "primary"},
    "book/chapter7.md": {"targets": [10], "action": "rewrite", "role": "primary"},
    "book/chapter8.md": {"targets": [13], "action": "rewrite", "role": "primary"},
    "book/chapter9.md": {"targets": [12], "action": "rewrite", "role": "primary"},
    "book/chapter10.md": {"targets": [14], "action": "rewrite", "role": "primary"},
    "book/afterword.md": {"targets": ["conclusion"], "action": "rewrite", "role": "primary"},
    "book/reference-answers.md": {"targets": ["appendix"], "action": "adapt", "role": "support"},
    "docs/zh-CN/LEARNING.md": {"targets": [0, "reader-guide"], "action": "adapt", "role": "support"},
}

LESSON_TARGETS: dict[str, list[Any]] = {
    "00-course-setup": ["digital-appendix"],
    "01-intro-to-ai-agents": [0, 1, 2],
    "02-explore-agentic-frameworks": [2, 9, "platform-appendix"],
    "03-agentic-design-patterns": [2, 3, "pattern-handbook"],
    "04-tool-use": [6],
    "05-agentic-rag": [5],
    "06-building-trustworthy-agents": [11],
    "07-planning-design": [3, "pattern-handbook"],
    "08-multi-agent": [14],
    "09-metacognition": [3, 5, 7, 12],
    "10-ai-agents-production": [9, 10],
    "11-agentic-protocols": [6, 14],
    "12-context-engineering": [4],
    "13-agent-memory": [5, 12],
    "14-microsoft-agent-framework": [9, "platform-appendix"],
    "15-browser-use": [8, 11],
    "16-deploying-scalable-agents": [9, 10, "platform-appendix"],
    "17-creating-local-ai-agents": [5, 6, 9, "platform-appendix"],
    "18-securing-ai-agents": [11],
}

GLOSSARY = [
    ("agent", "AI Agent", "AI Agent", 1, "能够根据上下文选择行动、通过工具接收环境反馈并持续推进目标的系统。"),
    ("model", "模型", "Model", 1, "负责语义理解、推理和候选决策；不承担最终授权。"),
    ("harness", "Agent Harness", "Agent Harness", 9, "环绕模型的运行与治理层，管理上下文、工具、状态、权限、预算、验证和纠正。"),
    ("environment", "环境", "Environment", 1, "Agent 外部的真实或仿真状态及其转移规律。"),
    ("context", "上下文", "Context", 4, "一次模型决策时可见的策略、目标、状态、证据、历史和工具定义。"),
    ("memory", "记忆", "Memory", 5, "跨交互保留且受来源、权限、更新和删除政策治理的信息。"),
    ("rag", "检索增强生成", "Retrieval-Augmented Generation", 5, "从外部知识源检索证据并注入当前决策上下文。"),
    ("tool", "工具", "Tool", 6, "Agent 感知或改变环境的受控接口。"),
    ("skill", "Agent Skill", "Agent Skill", 4, "可按需披露的复用知识和流程说明，不构成硬权限边界。"),
    ("workflow", "工作流", "Workflow", 2, "执行步骤和主要转移由程序预先定义的编排。"),
    ("react", "ReAct 循环", "Reasoning and Acting Loop", 3, "模型决策、工具行动和环境观察反复交替的执行循环。"),
    ("trajectory", "运行轨迹", "Trajectory", 3, "一次运行中的输入、模型决策、工具调用、观察和状态变化序列。"),
    ("artifact", "产物", "Artifact", 3, "可持久引用的中间或最终成果，而非必须反复装入上下文的消息。"),
    ("evaluation", "评估", "Evaluation", 10, "通过数据集、环境和评分方法判断结果、轨迹及系统行为。"),
    ("observability", "可观测性", "Observability", 10, "通过 Trace、Span、指标和日志使系统运行可见和可诊断。"),
    ("mcp", "模型上下文协议", "Model Context Protocol", 6, "连接应用或 Agent 与工具、资源的互操作协议。"),
    ("a2a", "Agent 间协议", "Agent-to-Agent Protocol", 14, "支持跨 Agent 任务委派、状态和消息协作的协议。"),
    ("multi_agent", "多 Agent 系统", "Multi-Agent System", 14, "由多个具有独立上下文、身份、权限或任务所有权的 Agent 组成的系统。"),
    ("approval", "人工审批", "Human Approval", 11, "人在高影响动作执行前对明确、可核验的动作载荷作出允许或拒绝。"),
    ("idempotency", "幂等", "Idempotency", 9, "同一逻辑操作重复提交不会产生重复副作用。"),
]

CLAIMS = [
    ("core-formula", "Agent = LLM + Context + Tools", "conceptual", "E4", "book/introduction.md", "主库上下文消融与全书实验提供机制证据；公式属于工程抽象。"),
    ("production-formula", "Production Agent = Model + Harness + Environment Feedback", "synthesis", "E0", "bluebook/plan/MASTER_PLAN.md", "蓝皮书综合框架，需在样章评审中验证解释力。"),
    ("context-capability", "上下文决定模型在当前决策点能看到什么，并显著约束 Agent 表现。", "mechanism", "E4", "book/chapter1.md", "实验1-1为主要证据，仍需登记具体运行环境。"),
    ("eval-randomness", "没有评估，无法可靠区分设计提升与随机波动。", "engineering-principle", "E5", "book/introduction.md", "由评估方法论和统计常识支持。"),
    ("multi-agent-new-info", "多 Agent 的主要价值需要来自新信息、并行覆盖、上下文隔离或独立权限，而非角色命名。", "architecture", "E4", "book/chapter10.md", "需保留适用条件与成本基线。"),
    ("receipts-boundary", "密码学回执可证明归属、完整性和顺序，但不能证明动作正确或合规。", "security", "E5", "18-securing-ai-agents/README.md", "密码学机制边界，发布前核验标准引用。"),
    ("offline-online-loop", "离线评估与在线评估互补，线上失败应回流离线数据集。", "production", "E5", "10-ai-agents-production/README.md", "成熟软件和ML评估实践。"),
    ("prompt-not-auth", "Prompt 或 Skill 不能替代代码层授权。", "security", "E5", "book/chapter4.md", "最小权限和可信边界原则。"),
]


def q(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(str(value), ensure_ascii=False)


def yaml(data: Any, indent: int = 0) -> str:
    prefix = " " * indent
    if isinstance(data, dict):
        lines: list[str] = []
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                lines.extend([f"{prefix}{key}:", yaml(value, indent + 2)])
            else:
                lines.append(f"{prefix}{key}: {q(value)}")
        return "\n".join(lines)
    if isinstance(data, list):
        if not data:
            return prefix + "[]"
        lines: list[str] = []
        for value in data:
            if isinstance(value, dict):
                items = list(value.items())
                first_key, first_value = items[0]
                if isinstance(first_value, (dict, list)):
                    lines.extend([f"{prefix}- {first_key}:", yaml(first_value, indent + 4)])
                else:
                    lines.append(f"{prefix}- {first_key}: {q(first_value)}")
                for key, nested in items[1:]:
                    if isinstance(nested, (dict, list)):
                        lines.extend([f"{prefix}  {key}:", yaml(nested, indent + 4)])
                    else:
                        lines.append(f"{prefix}  {key}: {q(nested)}")
            else:
                lines.append(f"{prefix}- {q(value)}")
        return "\n".join(lines)
    return prefix + q(data)


def write(name: str, data: Any) -> None:
    (DATA / name).write_text(yaml(data) + "\n", encoding="utf-8")


def extract_sections(path: Path) -> list[dict[str, Any]]:
    sections: list[dict[str, Any]] = []
    in_fence = False
    for line_no, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = re.match(r"^(#{1,2})\s+(.+?)\s*$", line)
        if match:
            sections.append({"level": len(match.group(1)), "title": match.group(2), "line": line_no})
    return sections


def main() -> None:
    curated: list[dict[str, Any]] = []
    for source_path, config in CHAPTER_MAP.items():
        path = PRIMARY / source_path
        curated.append({
            "id": "primary:" + source_path,
            "source": "primary",
            "path": source_path,
            "targets": config["targets"],
            "action": config["action"],
            "role": config["role"],
            "review_status": "reviewed_structure",
            "sections": extract_sections(path) if path.exists() else [],
        })

    for lesson, targets in LESSON_TARGETS.items():
        path = SUPPLEMENTARY / lesson / "README.md"
        curated.append({
            "id": "supplementary:" + lesson,
            "source": "supplementary",
            "path": f"{lesson}/README.md",
            "targets": targets,
            "action": "adapt_case" if lesson in {"02-explore-agentic-frameworks", "14-microsoft-agent-framework", "16-deploying-scalable-agents", "17-creating-local-ai-agents"} else "adapt",
            "role": "supplement",
            "review_status": "reviewed_structure",
            "sections": extract_sections(path) if path.exists() else [],
        })

    write("curated-source-map.yml", {"version": 1, "status": "curated_seed", "units": curated})
    write("glossary.yml", {
        "version": 1,
        "status": "draft_governed",
        "terms": [
            {"id": i, "zh": zh, "en": en, "authority_chapter": ch, "definition": definition, "review_status": "draft"}
            for i, zh, en, ch, definition in GLOSSARY
        ],
    })
    write("claims.yml", {
        "version": 1,
        "status": "seed",
        "claims": [
            {"id": i, "text": text, "type": typ, "evidence_level": level, "source_path": source, "notes": notes, "verification_status": "pending"}
            for i, text, typ, level, source, notes in CLAIMS
        ],
    })
    write("references.yml", {
        "version": 1,
        "status": "seed",
        "references": [
            {"id": "primary-repo", "type": "repository", "title": "深入理解 AI Agent", "path": str(PRIMARY), "license_status": "root_license_present"},
            {"id": "supplementary-repo", "type": "repository", "title": "AI Agents for Beginners", "path": str(SUPPLEMENTARY), "license_status": "root_license_present"},
            {"id": "rfc8785", "type": "standard", "title": "JSON Canonicalization Scheme (JCS)", "url": "https://www.rfc-editor.org/rfc/rfc8785", "verification_status": "pending"},
            {"id": "opentelemetry", "type": "standard_project", "title": "OpenTelemetry", "url": "https://opentelemetry.io/", "verification_status": "pending"},
        ],
    })
    print(f"curated_units: {len(curated)}")
    print(f"glossary_terms: {len(GLOSSARY)}")
    print(f"claim_seeds: {len(CLAIMS)}")


if __name__ == "__main__":
    main()
