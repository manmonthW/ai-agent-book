# AI Agent蓝皮书

<div class="bluebook-hero" markdown>

<div class="hero-copy" markdown>

<span class="release-badge">Release Candidate 1</span>

# 构建可信、可控、可演进的AI Agent

一本面向决策者、架构师与开发者的厂商中立工程手册。它不从“哪个模型最强”出发，而从权力、状态、证据和环境反馈出发。

<div class="hero-actions">
<a class="primary-action" href="chapters/00-executive-summary/">开始阅读</a>
<a href="experiments/">查看实验图谱</a>
</div>

</div>

<div class="autonomy-spectrum" markdown>

**最低充分自主性**

1. 确定性代码　<small>规则充分</small>
2. 结构化调用　<small>语义转换</small>
3. RAG调用　<small>外部事实</small>
4. 条件Workflow　<small>路径已知</small>
5. 有界工具Agent　<small>路径开放</small>
6. 多Agent　<small>并行 / 隔离</small>

</div>

</div>

<div class="manifesto" markdown>

<span>系统原则 01 / 03</span>

## 让模型处理不确定性，  
让代码守住**权力与事实**。

</div>

## 三条阅读路径

<div class="reader-paths" markdown>

### 决策者

**30分钟形成采用判断**

执行摘要 → 什么时候使用Agent → 安全治理 → 组织采用。

### 架构师

**3小时画清权力边界**

定义 → Runtime → Context → Tool Gateway → Harness。

### 开发者

**按任务查阅与复用**

Coding Agent → 评估 → 模式卡 → 实验与Artifact。

</div>

## 四篇，从边界走向演进

<div class="book-parts" markdown>

### I　认知与架构选择
定义边界、问题合同与最低充分自主性。

### II　核心能力
Runtime、上下文、知识、工具与多模态。

### III　生产控制面
Harness、评估、权限、审批与审计。

### IV　能力提升
持续进化、后训练与多Agent准入。

</div>

## 先看证据状态，再看结果

本书保留失败、阻塞、零事件和未复现结果。实验存在不等于假设成立，代码存在也不等于真实环境已经验证。

<div class="evidence-summary" markdown>

| 实验 | 问题 | 证据状态 |
|---|---|---|
| 1-1 | 上下文组件消融 | `E4 · 已审查` |
| 2-3 | 稳定前缀与KV Cache | `E4 · 已审查` |
| 2-5 | Prompt Injection矩阵 | `E4 · 零事件` |
| 2-10 | 上下文压缩策略 | `E3 · 证据降级` |

</div>

[进入109张实验图谱](experiments/index.md){ .primary-action }
