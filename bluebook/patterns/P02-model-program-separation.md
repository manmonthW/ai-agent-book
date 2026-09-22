# P02 模型与程序职责分离

> 状态：Release Candidate 1  
> 主要章节：第1、3章

## Context

Model处理语义不确定性；程序处理状态、权限、预算、业务规则和验证。

## Problem

候选决策与权威执行混在模型中，导致越权、不可复现和无法审计。

## Forces

- 质量与正确性；
- 延迟与成本；
- 安全与合规；
- 运维与可恢复性。

## Solution

```text
Model → typed proposal → policy/validator → program execution → environment verification
```

## Consequences

### 收益

开放式解释能力与确定性控制同时保留。

### 代价

需要设计Schema、策略和验证器；边界过细可能增加延迟。

## Failure Modes

把业务不变量写进Prompt；模型直接写权威数据库。

## Implementation Sketch

实现时使用类型化输入输出，记录版本、来源和Trace；权限、预算和终止由确定性代码执行。

## Evidence

- 蓝皮书章节：第1、3章；
- 实验卡：按具体实现绑定，不以代码存在替代运行证据；
- 外部标准：涉及协议或安全标准时在发布前核验版本与日期。

## Exit Criteria

当任务完全确定性时移除Model；当规则无法显式表达时仍保留受控模型节点。

## Checklist

- [ ] 问题与作用力真实存在。
- [ ] 有更简单方案基线。
- [ ] 失败模式可测试。
- [ ] 权限、预算和恢复已定义。
- [ ] 收益覆盖新增复杂度。
