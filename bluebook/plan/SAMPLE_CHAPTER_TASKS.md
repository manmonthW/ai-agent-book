# Step 4 样章任务包

> 原则：四个样章用于验证整本书的方法，不追求一次完成全书。

## 样章 A：第0章执行摘要

### 目标

让决策者在30分钟内理解定义、适用场景、主要风险和采用路线图。

### 必须包含

- Agent、Workflow、Copilot、RPA 对比；
- Agent 内部三要素和外部环境闭环；
- 最低充分自主性阶梯；
- 十条蓝皮书结论；
- 价值、风险和成熟度模型；
- 90/180/365天采用路线图。

### 证据

`sample-chapter-evidence.yml` 中 core-formula、lowest-sufficient-autonomy、production-control-plane。

### 图

`bluebook-system-overview`、`autonomy-ladder`。

## 样章 B：第2章什么时候应该使用 Agent

### 目标

给出可操作的架构选择顺序，明确何时拒绝 Agent 或多 Agent。

### 必须包含

- Transform/Pipeline/Route/Parallel/Explore/Refine/Delegate/Converse/Long-running 分类；
- 决策序列；
- 模式矩阵；
- 影响等级和审批边界；
- ADR 模板；
- 反例。

### 质量门禁

每项推荐必须说明避免条件、验证方法和成本影响。

## 样章 C：第4章上下文工程

### 目标

把“上下文越长越好”改写为“为每个决策点构造最相关、可信、受预算约束的信息”。

### 必须包含

- 上下文五组件；
- 稳定前缀和动态轨迹；
- Skills、状态栏、压缩；
- Poisoning/Distraction/Confusion/Clash；
- Prompt Injection；
- 实验1-1、2-3、2-10的限定结论。

### 禁止表述

- 每个组件都不可或缺；
- 单次实验结果对所有模型成立；
- Prompt 可以提供硬安全边界。

## 样章 D：第9–11章生产控制面组合样章

### 目标

验证 Harness、评估、安全三章能否形成一条完整生产链。

### 必须包含

- 状态机、Checkpoint、幂等、预算、取消和恢复；
- Trace/Span 与四级质量门；
- 身份、授权、策略和人工审批；
- Exact payload approval；
- 密码学回执及其边界；
- Offline → Shadow → Canary → Rollout → Rollback。

### 图

`production-control-plane`、`quality-gates`、`security-action-chain`。

## 通用验收

- 三种阅读速度均成立；
- 所有精确数字有来源；
- 所有实验结论有适用条件；
- 厂商案例可替换，不影响通用架构；
- 每章包含失败模式、检查清单和知识检查；
- 不引入未登记术语；
- 不出现只靠Prompt保证权限或完成状态的设计。
