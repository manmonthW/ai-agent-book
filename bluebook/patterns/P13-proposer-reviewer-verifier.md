# P13 Proposer–Reviewer–Verifier

> 状态：Release Candidate 1  
> 主要章节：第7、10、14章

## Context

开放任务需要迭代提高代码、文档或视觉产物。

## Problem

同一模型自评容易重复偏见，意见循环没有新信息。

## Forces

- 质量与正确性；
- 延迟与成本；
- 安全与合规；
- 运维与可恢复性。

## Solution

```text
Proposer生成；执行/渲染；Reviewer读取独立证据并给结构化缺口；Verifier按门禁终止。
```

## Consequences

### 收益

利用环境反馈改进并可定位失败。

### 代价

增加调用、延迟和终止设计。

## Failure Modes

Reviewer只看候选文本；没有轮数和最小增益。

## Implementation Sketch

实现时使用类型化输入输出，记录版本、来源和Trace；权限、预算和终止由确定性代码执行。

## Evidence

- 蓝皮书章节：第7、10、14章；
- 实验卡：按具体实现绑定，不以代码存在替代运行证据；
- 外部标准：涉及协议或安全标准时在发布前核验版本与日期。

## Exit Criteria

确定性验证一次通过时无需Reviewer循环。

## Checklist

- [ ] 问题与作用力真实存在。
- [ ] 有更简单方案基线。
- [ ] 失败模式可测试。
- [ ] 权限、预算和恢复已定义。
- [ ] 收益覆盖新增复杂度。
