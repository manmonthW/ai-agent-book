# P03 有界执行循环

> 状态：Release Candidate 1  
> 主要章节：第3、9章

## Context

Agent需要多轮观察和行动，但不能无限运行。

## Problem

开放循环可能重复工具、耗尽费用或永不终止。

## Forces

- 质量与正确性；
- 延迟与成本；
- 安全与合规；
- 运维与可恢复性。

## Solution

```text
Observe → Decide → Act → Verify；由Runtime强制步骤、时间、费用和无进展上限
```

## Consequences

### 收益

支持适应环境反馈并限制最坏成本。

### 代价

预算过紧可能提前终止；需定义部分成功和恢复。

## Failure Modes

只在Prompt中要求停止；用模型自评作为唯一终止。

## Implementation Sketch

实现时使用类型化输入输出，记录版本、来源和Trace；权限、预算和终止由确定性代码执行。

## Evidence

- 蓝皮书章节：第3、9章；
- 实验卡：按具体实现绑定，不以代码存在替代运行证据；
- 外部标准：涉及协议或安全标准时在发布前核验版本与日期。

## Exit Criteria

固定Workflow足够时退出循环。

## Checklist

- [ ] 问题与作用力真实存在。
- [ ] 有更简单方案基线。
- [ ] 失败模式可测试。
- [ ] 权限、预算和恢复已定义。
- [ ] 收益覆盖新增复杂度。
