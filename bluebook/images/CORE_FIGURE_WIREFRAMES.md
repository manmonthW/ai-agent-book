# 核心架构篇图表线框

> 状态：已完成。8张图的可编辑Excalidraw源、最终SVG和PNG预览位于[`architecture/`](architecture/README.md)。本文保留为内容设计记录。

## 图1：Agent边界与反馈闭环

```text
┌──────────────── Agent ────────────────┐
│  ┌──────── Model ────────┐            │
│  │ 语义理解 / 候选决策    │            │
│  └─────────↕─────────────┘            │
│  ┌──────── Harness ──────┐            │
│  │ Context / State / Tools            │
│  │ Policy / Budget / Verify           │
│  └─────────↕─────────────┘            │
└────────────↕──────────────────────────┘
       Observation / Action
┌──────────── Environment ──────────────┐
│ User / Files / DB / Web / Devices     │
└───────────────────────────────────────┘
```

目标：第1章。替代并融合原fig0-1和fig1-1。

## 图2：最低充分自主性阶梯

```text
确定性代码
  → 单次结构化调用
  → RAG调用
  → 固定/条件工作流
  → 有界工具Agent
  → Orchestrator/Handoff
```

每一级标注“升级证据”和“必要控制”。目标：第2章。

## 图3：统一执行图

```text
Input → Route → Plan → Execute → Verify → Terminal
                   ↘ Wait/Approval ↗
                   ↘ Recover/Retry ↗
```

节点图例：Program / Model / Tool / Human / Event。目标：第3章。

## 图4：上下文生命周期

```text
Stable Prefix + Goal + Typed State + Evidence + Relevant Trajectory
                            ↓
                      Model Decision
                            ↓
         Drop / Summarize / Extract / Externalize
```

旁侧标注Poisoning、Distraction、Confusion、Clash。目标：第4章。

## 图5：知识与记忆边界

```text
Current Context ← Retrieval ← Knowledge Base
       ↑                       Authority/ACL
Runtime State ← Events
       ↑
Governed Memory ← Extract/Validate/Confirm
       ↕
Artifact Store (references, not repeated payloads)
```

目标：第5章。

## 图6：工具执行与协议边界

```text
Model proposal
 → Schema
 → Authorization/Policy
 → Approval
 → Idempotent Tool Gateway
 → MCP/API/Actor
 → Environment
 → Result Validation
```

MCP/A2A用虚线标示“互操作，不等于授权”。目标：第6章。

## 图7：Coding Agent闭环

```text
Requirement → Search → Read → Patch → Test/Render → Diagnose
                                 ↑                    ↓
                                 └────── Fix ─────────┘
                                      Verify → Done
```

目标：第7章。

## 图8：模态×时序与公共原语

二维矩阵：Text/API、Voice、GUI、Physical × Sync、Realtime、Async。
底部公共控制：Wake、Checkpoint、Safe Point、Cancel、Preempt、Backpressure、Verify。

目标：第8章。

## 制图门禁

- 不使用产品Logo作为通用概念；
- 颜色表达信任和控制，不表达厂商；
- 图中文字可脱离正文理解；
- 所有数字和版本进入figures登记；
- SVG源文件可编辑且支持黑白打印；
- 图注说明概念图还是实验数据图。
