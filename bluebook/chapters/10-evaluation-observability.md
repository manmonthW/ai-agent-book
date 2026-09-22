# 第10章　评估、可观测性与成本

> 状态：Release Candidate 1  
> 核心问题：如何判断Agent做对了、为何做错，以及一次改动是否值得发布。

## 本章回答的三个问题

1. Outcome、Trajectory、System和Safety应如何分别评估？
2. Trace/Span与Offline/Online Evaluation如何形成闭环？
3. 如何比较模型、Prompt和架构的质量、延迟与成本？

## 5分钟速读

- Observability回答“发生了什么”，Evaluation回答“是否做对、是否值得”。
- Agent评估不能只看最终文本，还要看工具、参数、循环、恢复和副作用。
- 质量门依次为Schema/Unit、Smoke、Offline和Online；Smoke只验证最小路径。
- 优先使用最终环境状态和确定性验证器，LLM Judge需要校准且不能裁决权限与事实。
- 离线集来自真实任务和失败；线上新失败持续回流离线集。
- 比较方案时保持任务、工具、预算和环境一致，并报告方差与失败类型。
- 成本优化看每成功任务总成本，而不是单次模型Token价格。
- 发布经过离线回放、影子流量、金丝雀和有限放量。

## 一、Trace与Span

```text
Trace: customer refund
├── model: classify
├── tool: get order
├── retrieval: policy
├── model: propose
├── policy: validate
├── approval
├── tool: execute
└── verifier: status
```

Span记录运行、版本、Token、成本、延迟、工具结果码、重试、缓存、Artifact、政策和验证状态。Telemetry应脱敏，不记录不必要的PII、秘密或完整敏感载荷。

## 二、五层评估

| 层 | 问题 | 例子 |
|---|---|---|
| Outcome | 最终目标完成吗？ | 权威状态为refunded |
| Trajectory | 路径正确吗？ | 工具和参数、重复调用 |
| System | 系统可靠？ | 超时、恢复、幂等、取消 |
| Economics | 值得吗？ | p95、每成功任务成本 |
| Safety | 合规且受权？ | 越权、泄漏、审批绕过 |

最终答案正确但重复付款，不是成功；轨迹漂亮但订单未改变，也不是成功。

## 三、四级质量门

### L1 Schema与Unit

验证工具参数、授权、幂等、状态转移、预算和确定性计算。使用Fake Model与Fake Tool减少随机性。

### L2 Smoke

验证部署可达、最小调用可工作、Schema正确和Trace产生。不能替代任务质量评估。

### L3 Offline Evaluation

固定数据、环境和预算，比较模型、Prompt、上下文、RAG、工具或架构。数据集包括：

- 常规真实任务；
- 边界和对抗任务；
- 历史生产失败；
- 高影响政策任务；
- 恢复和取消任务。

### L4 Online Evaluation

追踪真实业务完成、用户反馈、漂移、人工接管、费用和安全拦截。线上标签有偏差，需要抽样人工复核。

## 四、评估数据集

每条任务至少记录：

```yaml
id: refund-017
input: ...
initial_environment: ...
success_assertions:
  - refund_status == completed
forbidden_effects:
  - duplicate_refund
trajectory_constraints:
  - approval_before_execute
impact_level: I4
```

数据集按来源和时间分层，保留私有测试集，避免围绕公开用例过拟合。

## 五、验证器优先级

```text
环境最终状态
→ 确定性规则和测试
→ 专家标签
→ 经校准LLM Judge
→ 未校准主观判断
```

LLM Judge适合风格、完整性和开放任务Rubric，但必须：

- 与人工标签校准；
- 保存Judge版本和Prompt；
- 检查位置、长度和模型偏差；
- 不作为事实、权限或高风险动作唯一裁判。

## 六、统计与比较

Agent非确定性要求重复运行。报告：

- 样本量和随机性设置；
- 成功率与置信区间；
- 延迟分位数；
- 每类失败；
- Token与成本分布；
- 配对任务结果；
- 实际环境、模型和日期。

不要把一次运行或历史点估计写成稳定规律。主仓库多项实验保留“活动完成但原假设未复现”的记录，这种诚实分离是评估制度的一部分。

## 七、模型与路由评估

模型选型不只看通用排行榜。用本系统的：

- Tool Schema；
- Prompt；
- RAG和数据；
- 真实任务；
- 预算和延迟SLO；
- 安全策略。

路由器需要单独评估错误路由和Fallback。小模型处理分类不代表适合长程规划；强模型也不应承担确定性计算。

## 八、成本

```text
每成功任务成本 =
(模型 + 工具 + 基础设施 + 人工处理 + 失败损失) / 成功任务数
```

优化手段：

- 小模型处理简单节点；
- 缓存稳定前缀和常见结果；
- 过滤无关上下文；
- 并行真正独立任务；
- 减少无增益Evaluator轮次；
- 优先确定性验证器；
- 对预算异常设置告警和熔断。

每项优化需重新看成功率，不能只看Token下降。

## 九、从Benchmark到改进

失败归因流程：

```text
识别首个关键错误
→ 分类：Context/Tool/Model/Policy/Runtime
→ 建立最小回归任务
→ 选择最可控更新载体
→ 离线比较
→ 分阶段发布
```

首个错误比最终错误更有用，因为后续失败可能只是级联结果。

## 十、发布监控

发布路径：

```text
Offline Replay → Shadow → Canary → Bounded Rollout → Full
```

阈值覆盖成功率、政策违规、p95、每成功任务成本、重复副作用、Fallback和人工升级。任何安全违规可设置为硬停止。

## 十一、常见失败模式

| 失败 | 控制 |
|---|---|
| 只评文本 | 加环境与轨迹断言 |
| 用Smoke证明质量 | 建立离线和在线集 |
| Judge即真值 | 人工校准、确定性优先 |
| 数据集只有正常例 | 加边界、攻击和恢复任务 |
| 只报平均值 | 分位数、方差和失败分类 |
| 只算Token成本 | 每成功任务总成本 |
| 线上失败不回流 | 持续更新离线集 |

## 十二、检查清单

- [ ] 成功定义为可执行环境断言。
- [ ] Outcome、Trajectory、System、Economics、Safety分开评估。
- [ ] 有Unit、Smoke、Offline和Online四级门。
- [ ] Judge经过人工校准。
- [ ] 比较保持任务、环境和预算一致。
- [ ] 报告样本量、方差、分位数和失败分类。
- [ ] 计算每成功任务成本。
- [ ] 新失败回流评估集。
- [ ] 发布和回滚阈值明确。

## 知识检查

1. Observability与Evaluation有什么区别？
2. 为什么最终答案正确仍可能任务失败？
3. Smoke Test能证明什么？
4. LLM Judge为什么需要校准？
5. 每成功任务成本为何优于Token单价？

## 来源与证据

主要来源为主仓库第7章和各章实验台账；补充来源为Lesson 10、16及Smoke Test目录。具体Benchmark数字留在实验册并附环境与版本。
