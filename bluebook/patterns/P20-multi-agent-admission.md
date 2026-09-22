# P20 多Agent准入与等预算基线

> 状态：Release Candidate 1  
> 主要章节：第2、14章

## Context

单Agent任务出现长上下文、并行研究、权限隔离或跨组织协作需求，团队考虑拆分多个Agent。

## Problem

多个角色很容易增加Token、延迟、冲突和运维复杂度，但同模型、同信息的多个Agent未必提供新能力。

## Forces

- 质量：并行探索可能扩大覆盖；
- 延迟：并行可加速，也可能受合并阻塞；
- 成本：上下文复制和通信增加费用；
- 安全：身份隔离有益，但权限面增大；
- 运维：生命周期、消息、Artifact和取消更复杂。

## Solution

升级前要求至少一个强理由：

1. 获取独立新信息；
2. 真正可并行的工作；
3. 上下文或安全隔离；
4. 独立身份/权限；
5. 持续交互的Handoff或跨组织边界。

先比较Skill、专业工具或有界子任务。评估时使用相同任务、总Token/费用、工具和截止时间的单Agent基线。

## Consequences

### 收益

- 复杂性与实际增益绑定；
- 能识别Skill足以解决的伪多Agent需求；
- 使成本和故障代价可见。

### 代价

- 等预算实验设计更严格；
- 需要消息和Artifact基础设施；
- 部分并行优势受模型限流影响。

## Failure Modes

- 角色名不同就创建Agent；
- 多Agent拥有相同上下文且无新证据；
- 只与低预算单Agent比较；
- 不计Manager和合并成本；
- Worker继承全部权限；
- 任务结束后留下孤儿运行。

## Implementation Sketch

```text
Candidate topology
→ Admission reason
→ Single-agent baseline
→ Equal budget evaluation
→ Quality/latency/cost/safety comparison
→ Keep only if net benefit persists
```

## Evidence

- 蓝皮书章节：第2、7、14章；
- 实验卡：并行研究、多角色和协作实验；
- 外部协议：A2A只承担互操作，不作为增益证据。

## Exit Criteria

当增量质量或延迟优势不能覆盖通信、合并、成本和安全复杂度时，合并回单Agent、Skill或工具。

## Checklist

- [ ] 有至少一个强准入理由。
- [ ] 已评估Skill和工具替代。
- [ ] 单Agent基线预算相同。
- [ ] Agent身份和权限独立。
- [ ] 消息和Artifact可追踪。
- [ ] 生命周期支持级联取消。
- [ ] 合并错误进入评估。
