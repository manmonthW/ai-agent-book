# P19 独立Agent工作区与Artifact交换

> 状态：Release Candidate 1  
> 主要章节：第7、14章

## Context

多个Worker并行处理文件、研究或生成产物。

## Problem

共享可变目录导致覆盖，复制全上下文导致膨胀和泄漏。

## Forces

- 质量与正确性；
- 延迟与成本；
- 安全与合规；
- 运维与可恢复性。

## Solution

```text
每个Agent私有Scratch/Worktree；通过带Schema、Hash、来源和ACL的Artifact发布；单一Owner合并。
```

## Consequences

### 收益

隔离冲突、减少消息体并增强追溯。

### 代价

需要存储、合并和垃圾回收。

## Failure Modes

多个Agent直接编辑同一文件；消息中粘贴全部产物。

## Implementation Sketch

实现时使用类型化输入输出，记录版本、来源和Trace；权限、预算和终止由确定性代码执行。

## Evidence

- 蓝皮书章节：第7、14章；
- 实验卡：按具体实现绑定，不以代码存在替代运行证据；
- 外部标准：涉及协议或安全标准时在发布前核验版本与日期。

## Exit Criteria

单Agent顺序任务无需多工作区。

## Checklist

- [ ] 问题与作用力真实存在。
- [ ] 有更简单方案基线。
- [ ] 失败模式可测试。
- [ ] 权限、预算和恢复已定义。
- [ ] 收益覆盖新增复杂度。
