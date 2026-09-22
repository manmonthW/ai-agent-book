# P01 最低充分自主性

> 状态：Release Candidate 1  
> 主要章节：第2章

## Context

团队面对一个包含自然语言、检索、工具或多步骤决策的任务，正在选择实现架构。

## Problem

自主性可以处理开放变化，但增加非确定性、成本、安全和调试负担。如何避免因“Agent能力更强”而过度设计？

## Forces

- 质量：开放任务需要适应性；
- 延迟：循环和委派增加尾延迟；
- 成本：更多模型调用和上下文；
- 安全：动作空间越大，攻击面越大；
- 运维：状态、恢复和评估复杂度上升。

## Solution

按以下阶梯选择最先满足任务合同的一级：

```text
确定性代码
→ 单次结构化调用
→ RAG调用
→ 固定/条件Workflow
→ 有界工具Agent
→ Orchestrator/Handoff/多Agent
```

只有当前一级无法处理已观察到的变化，并且下一级带来可测增益时升级。每次升级同时增加预算、终止、权限和评估控制。

## Consequences

### 收益

- 减少不必要的Agent循环；
- 更易测试、解释和回滚；
- 将复杂性预算留给真正开放环节。

### 代价

- 前期需要清晰任务合同和基线；
- 可能需要组合多种架构，而非单一框架；
- 需要持续证明升级价值。

## Failure Modes

- 因框架支持就默认多Agent；
- 把自然语言输入等同开放决策；
- 只比较成功案例，不比较等预算基线；
- 升级自主性却不升级Harness控制。

## Implementation Sketch

```python
if deterministic_rules_cover(task):
    return run_program(task)
if one_model_call_is_enough(task):
    return structured_call(task)
if path_is_known(task):
    return workflow(task)
return bounded_agent(task, budgets=..., allowed_tools=...)
```

## Evidence

- 蓝皮书章节：第2章、第3章、第14章；
- 实验卡：根据具体场景绑定；
- 外部来源：ReAct等Agent机制论文只说明能力形式，不自动证明业务增益。

## Exit Criteria

当前架构无法在约定预算内处理真实任务变化，并且更高一级在离线和灰度评估中显示稳定净增益。

## Checklist

- [ ] 问题合同和成功断言明确。
- [ ] 有更简单架构基线。
- [ ] 升级解决的是已观察问题。
- [ ] 新增权限、预算和失败路径已治理。
- [ ] 能够回退到较低自主性版本。
