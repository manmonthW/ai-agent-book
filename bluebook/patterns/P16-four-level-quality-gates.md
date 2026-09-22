# P16 四级质量门

> 状态：Release Candidate 1  
> 主要章节：第10章

## Context

Agent变更需要从代码测试走向真实发布。

## Problem

只做Smoke或只看在线指标无法兼顾速度与真实性。

## Forces

- 质量与正确性；
- 延迟与成本；
- 安全与合规；
- 运维与可恢复性。

## Solution

```text
Schema/Unit → Smoke → Offline Eval → Online Eval，逐级增加真实性和成本。
```

## Consequences

### 收益

早期快速失败，发布证据完整。

### 代价

维护数据集和环境成本较高。

## Failure Modes

用Smoke证明质量；线上试错无Canary。

## Implementation Sketch

实现时使用类型化输入输出，记录版本、来源和Trace；权限、预算和终止由确定性代码执行。

## Evidence

- 蓝皮书章节：第10章；
- 实验卡：按具体实现绑定，不以代码存在替代运行证据；
- 外部标准：涉及协议或安全标准时在发布前核验版本与日期。

## Exit Criteria

纯确定性小改动仍可简化，但不得跳过相关回归。

## Checklist

- [ ] 问题与作用力真实存在。
- [ ] 有更简单方案基线。
- [ ] 失败模式可测试。
- [ ] 权限、预算和恢复已定义。
- [ ] 收益覆盖新增复杂度。
