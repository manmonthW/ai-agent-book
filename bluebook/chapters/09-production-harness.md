# 第9章　Harness：从Demo到可靠产品

> 状态：Release Candidate 1  
> 核心问题：如何把不确定的模型决策放进持久、可预算、可恢复的软件控制面。

## 本章回答的三个问题

1. Harness在模型之外负责哪些生产职责？
2. 长任务如何Checkpoint、恢复、取消并避免重复副作用？
3. 错误、预算、模型路由和发布版本如何治理？

## 5分钟速读

- Model负责语义判断，Harness负责状态、权限、预算、工具、验证和恢复。
- 每次运行有唯一ID、版本化状态Schema和明确终态。
- 长任务不能只存在进程内存；副作用前后和等待事件前保存Checkpoint。
- 所有写操作幂等；超时后先查询状态，不盲目重试。
- 旧运行恢复时必须通过状态版本和所有权fencing，不能覆盖新结果。
- 错误按校验、授权、暂态、永久、模型、上下文和预算分类处理。
- Token、工具、时间、金额、并发和委派深度由代码强制限制。
- 发布遵循离线回放、影子流量、金丝雀、有限放量和回滚。

## 一、Harness控制循环

```text
输入与身份
→ 构造上下文
→ Model提出候选决策
→ Schema/语义校验
→ 授权与政策
→ 审批（如需要）
→ 幂等执行
→ 环境结果验证
→ 持久状态更新
→ 继续/完成/阻塞/失败/取消
```

模型不能直接修改权威状态，也不能自行批准高影响动作。

## 二、运行状态

```yaml
run_id: run_01J
actor_id: user_456
tenant_id: tenant_123
status: waiting_approval
state_version: 12
current_step: approve_refund
completed_effects:
  - idempotency_key: refund-preview-order-789-v1
    result_ref: artifact://runs/run_01J/preview.json
pending_effects: [refund-order-789]
budgets:
  model_calls_remaining: 3
  tool_calls_remaining: 4
  deadline: 2026-09-21T11:00:00Z
versions:
  graph: 3
  prompt: support-v4
  toolset: billing-v3
  policy: refund-v7
```

运行终态至少区分：`succeeded`、`partial_success`、`blocked`、`failed`、`cancelled`和`budget_exhausted`。模型停止生成不等于成功。

## 三、持久Checkpoint

在以下位置保存：

- 副作用执行前；
- 副作用成功且验证后；
- 等待审批、用户或事件前；
- 重规划和版本切换前；
- 接近预算阈值时。

Checkpoint包括状态版本、已完成副作用、Artifact引用、等待条件和下一步。

## 四、幂等与恢复

业务幂等键示例：

```text
refund:{tenant}:{order}:{approved_action_digest}
```

HTTP超时不代表操作失败。恢复流程：

```text
查询幂等记录/权威状态
→ 已完成则复用结果
→ 未执行且仍允许才重试
→ 状态不确定则人工处理
```

### Stale-run fencing

每次写入校验状态版本、运行所有者、审批有效期和政策兼容性。旧运行不得覆盖更新后的状态。

## 五、错误分类

| 错误 | 默认处理 |
|---|---|
| Schema/Validation | 修复一次或拒绝候选 |
| Authorization | 不重试；拒绝或等待授权 |
| Rate Limit | 遵循Retry-After，有界退避 |
| Transient Network | 幂等保护下有界重试 |
| Permanent Business | 改道、澄清或失败 |
| Model Refusal | 分类和Fallback，不伪造回答 |
| Context Overflow | 压缩、分段或终止 |
| Budget Exhausted | 明确终态，不伪装成功 |
| Policy Changed | 重新预览和审批 |

统一“重试三次”会让授权失败和业务拒绝重复消耗资源，甚至放大副作用。

## 六、预算、取消和并发

```yaml
max_model_calls: 8
max_tool_calls: 20
max_wall_time_seconds: 300
max_cost_usd: 1.00
max_concurrency: 4
max_delegation_depth: 1
max_artifact_bytes: 50000000
```

取消采用协作式安全点：先停止新工作、清理资源、写Checkpoint，再退出；无响应时强制终止。取消父运行默认级联子任务。并发达到上限时排队或拒绝，不能无限创建Worker。

## 七、Artifact与来源

大型网页、文档、代码、日志和报告存入Artifact Store。状态只保存：

- URI；
- 内容Hash；
- 来源；
- 创建者；
- 权限；
- Schema和版本；
- 生命周期。

这样可恢复、审计，也避免上下文重复膨胀。

## 八、模型与工具版本

每次运行记录：

- 模型供应商、模型ID和路由；
- Prompt ID、版本和Hash；
- 输出Schema版本；
- Toolset与每个工具版本；
- 政策和执行图版本。

切换模型不能默认旧Prompt和评估继续有效。路由器也需要评估和Fallback。

## 九、部署选择

| 形态 | 适用 | 代价 |
|---|---|---|
| 应用内Runtime | 简单、短任务 | 持久和扩缩容自建 |
| Worker/Queue | 异步、长任务 | 状态和消息复杂 |
| 托管Agent Service | 快速上线和集中观测 | 平台约束与锁定 |
| 本地Agent | 隐私、离线、设备工具 | 模型能力和运维限制 |
| 混合 | 本地敏感处理+云端复杂推理 | 路由、数据边界复杂 |

无论部署在哪，状态、授权和审计契约应保持可迁移。

## 十、发布和回滚

```text
Offline Replay → Shadow → Canary → Bounded Rollout → Full
```

定义回滚阈值：任务成功率、政策违规、重复副作用、p95延迟、每成功任务成本、Fallback和人工接管率。保留旧模型、Prompt、Schema和工具版本。

## 十一、常见失败模式

| 失败 | 控制 |
|---|---|
| 长任务进程重启后丢失 | 持久状态和Checkpoint |
| 写请求重复执行 | 幂等键和状态查询 |
| 旧运行覆盖新状态 | 版本和所有权fencing |
| 所有错误都重试 | 错误分类 |
| Agent成本失控 | 多维硬预算 |
| 模型切换不可追溯 | 全链路版本记录 |
| 发布后无法回滚 | 保留旧版本和迁移策略 |

## 十二、检查清单

- [ ] Run ID、状态Schema和终态明确。
- [ ] 长任务可Checkpoint、恢复和取消。
- [ ] 所有副作用幂等。
- [ ] 旧运行不能覆盖新状态。
- [ ] 错误类型决定重试策略。
- [ ] 多维预算由代码执行。
- [ ] Artifact有来源、Hash和权限。
- [ ] 模型、Prompt、Schema、工具和政策可追踪。
- [ ] 发布和回滚阈值明确。

## 知识检查

1. 为什么超时后不能直接重试退款？
2. Stale-run fencing解决什么问题？
3. 哪些错误不应自动重试？
4. 为什么模型切换后要重新评估？
5. 本地和托管部署的控制契约为何应保持一致？

## 来源与证据

主要来源为主仓库第1、6、9、10章，以及补充仓库Lesson 02、14、16和17。本章是生产控制面的综合架构，不归因于单一框架。
