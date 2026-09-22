# 第9–11章组合样章　生产控制面：可靠性、评估与安全

> 状态：组合样章 v0.1  
> 用途：验证第9章Harness、第10章评估与可观测性、第11章安全治理能否形成统一闭环。正式版本将拆为三章。

## 本样章回答的三个问题

1. 一个能调用工具的Demo距离生产系统还缺什么？
2. 如何证明Agent真的完成了任务，并能在失败后安全恢复？
3. 如何确保模型无法扩大权限，高影响动作经过准确审批且可审计？

## 5分钟速读：生产控制面的十个不变量

1. 每次运行有唯一`run_id`和版本化状态Schema。
2. 状态转移由代码控制，模型只能提出候选决策。
3. 长任务可Checkpoint、恢复和取消。
4. 写操作具有幂等键，重试不会重复产生副作用。
5. Token、调用、时间、金额、并发和委派深度有硬预算。
6. 身份、授权和业务政策在工具执行前重新校验。
7. 高影响动作先预览，再由人批准准确载荷。
8. “完成”由环境事实或独立验证器判定。
9. 每次运行形成可关联的Trace、Span、Artifact和来源记录。
10. 新版本经过离线回放、影子流量、金丝雀和有限放量，并有明确回滚阈值。

> **蓝皮书结论**  
> 生产级Agent不是“更长的Prompt加更多工具”，而是一个围绕不确定模型建立的持久、受权、可预算、可验证、可恢复的软件控制系统。

---

# 第一部分　Harness：从Demo到可靠产品

## 一、Harness的职责

Model负责语义判断，Harness负责把候选判断变成受控执行：

```text
输入与身份
→ 构造当前上下文
→ Model提出决策
→ Schema与语义校验
→ 授权与政策检查
→ 必要时生成预览并等待审批
→ 幂等执行工具
→ 验证环境结果
→ 更新持久状态和证据
→ 继续、完成、阻塞、失败或取消
```

Harness至少包含：

- 上下文构造；
- 工具注册、过滤和调用；
- 运行状态与Checkpoint；
- 身份、权限和政策网关；
- 预算、超时和取消；
- 验证、重试、Fallback和熔断；
- Trace、Artifact和审计记录；
- 发布版本和回滚。

## 二、运行状态与状态机

### 2.1 推荐运行状态

```yaml
run_id: run_01J...
tenant_id: tenant_123
actor_id: user_456
status: waiting_approval
state_version: 12
policy_version: refund-policy-v7
prompt_version: support-agent-v4
toolset_version: billing-tools-v3
model_route: reasoning-primary
current_step: approve_refund
completed_effects:
  - key: refund-preview-order-789-v1
    result_ref: artifact://runs/run_01J/refund-preview.json
pending_effects:
  - refund-order-789
budgets:
  model_calls_remaining: 3
  tool_calls_remaining: 4
  cost_remaining_usd: 0.42
  deadline: 2026-09-21T11:00:00Z
checkpoint_version: 12
```

### 2.2 终态必须明确

推荐至少区分：

- `succeeded`：独立成功条件已满足；
- `partial_success`：部分成果有效，剩余部分清楚；
- `blocked`：等待用户、审批、凭据或外部事件；
- `failed`：不可恢复失败；
- `cancelled`：收到取消并完成安全清理；
- `budget_exhausted`：达到预算边界，没有伪装成成功。

不要把“模型没有继续调用工具”直接解释为成功。

## 三、持久性、幂等与过期运行

### 3.1 为什么内存循环不够

长任务会遇到进程重启、部署切换、队列重投、供应商超时和人工审批等待。状态只在进程内存中时，系统无法判断哪些步骤已经执行，也无法安全恢复。

### 3.2 Checkpoint

在以下位置保存Checkpoint：

- 工具副作用前；
- 副作用成功并验证后；
- 等待人工审批或外部事件前；
- 模型或工具版本切换前；
- 预算接近阈值时。

Checkpoint应包含状态版本、已完成副作用、Artifact引用和下一步可执行条件。

### 3.3 幂等

写工具接受由业务语义构造的幂等键：

```text
refund:{tenant_id}:{order_id}:{approved_preview_hash}
```

相同键重复执行时返回已有结果，而不是再次退款。HTTP请求成功但响应丢失时，系统可以查询幂等记录恢复，而不是盲目重试。

### 3.4 Stale-run fencing

旧运行恢复后可能覆盖新运行结果。每次写入应校验：

- 当前状态版本；
- 租户和Actor；
- 运行是否仍为当前所有者；
- 审批是否尚未过期；
- 工具和政策版本是否仍兼容。

版本不匹配时拒绝写入并进入重新规划或人工处理。

## 四、错误分类与恢复

| 错误 | 示例 | 默认处理 |
|---|---|---|
| Validation | Schema错误、非法参数 | 修复一次或终止该候选 |
| Authorization | 无权限、审批缺失 | 不重试；阻塞或拒绝 |
| Rate Limit | 供应商限流 | 指数退避、遵循Retry-After |
| Transient | 网络抖动、临时5xx | 有界重试、幂等保护 |
| Permanent Tool | 资源不存在、业务规则拒绝 | 改道、澄清或失败 |
| Model Refusal | 安全拒绝或能力边界 | 分类处理，不伪造空答案 |
| Context Overflow | 超出窗口 | 压缩、分段或失败 |
| Budget | 调用、时间或金额耗尽 | `budget_exhausted`终态 |
| Policy Change | 审批后政策已变化 | 重新生成预览和审批 |

禁止对所有异常统一“重试三次”。授权失败、业务拒绝和确定性校验失败通常不应重试。

## 五、预算与取消

预算应由代码执行：

```yaml
max_model_calls: 8
max_tool_calls: 20
max_wall_time_seconds: 300
max_cost_usd: 1.00
max_concurrency: 4
max_delegation_depth: 1
max_artifact_bytes: 50000000
```

取消采用协作式安全点：工具在可中断位置检查取消信号，完成必要清理并写入最后Checkpoint。无响应时再强制终止。取消父运行时，默认级联取消子任务；长期后台任务需要显式脱离生命周期树。

---

# 第二部分　评估与可观测性

## 六、Observability与Evaluation不是一回事

- **可观测性**回答：“发生了什么，在哪里发生，耗费多少？”
- **评估**回答：“结果是否正确，路径是否合理，系统是否值得发布？”

一次完整任务形成Trace，各步骤形成Span：

```text
Trace: refund request
├── model: classify intent
├── tool: get order
├── retrieval: refund policy
├── model: propose refund
├── policy: validate amount
├── approval: wait / accepted
├── tool: execute refund
└── verifier: authoritative status
```

### 6.1 Span建议字段

- `run_id`、`trace_id`、`span_id`；
- 租户和Actor的脱敏标识；
- 模型路由、Prompt/Schema/Toolset版本；
- 输入输出Token和成本；
- 工具名、参数摘要、结果码和幂等键；
- 重试、延迟、缓存命中；
- Artifact与来源引用；
- 政策、审批和验证结果；
- 错误类别与终态。

不要把原始密钥、完整PII或不必要的推理内容写入Telemetry。

## 七、五层评估

| 层 | 核心问题 | 优先验证方式 |
|---|---|---|
| Outcome | 业务目标是否完成？ | 最终环境状态、业务断言 |
| Trajectory | 工具、参数和步骤是否合理？ | 轨迹规则、步骤标签 |
| System | 超时、恢复、重复写入如何？ | 故障注入、恢复测试 |
| Economics | 延迟和成本是否值得？ | 每成功任务成本、p95 |
| Safety | 是否越权、泄漏或绕过审批？ | 攻击集、策略断言、审计 |

只评最终文本会漏掉“答案正确但重复付款”；只评轨迹会漏掉“路径看起来合理但业务状态没有改变”。

## 八、四级质量门

### L1：Schema与Unit Test

验证：

- 工具参数边界；
- 授权策略；
- 幂等；
- 状态转移；
- 预算和取消；
- 确定性计算。

使用Fake Model和Fake Tool保持测试稳定。

### L2：Smoke Test

验证部署可达和最小路径，例如：

- Agent能够响应；
- 一个只读工具可调用；
- 返回满足基本Schema；
- Trace能够产生。

补充仓库为若干部署课程提供了Smoke Test catalog。它们适合L2，不证明系统在复杂任务上的质量。

### L3：Offline Evaluation

使用真实任务和失败案例，比较：

- Prompt或上下文版本；
- 模型与路由；
- 工具描述；
- RAG和压缩策略；
- Agent与工作流；
- 单Agent与多Agent。

固定数据集、环境版本和预算，报告方差、失败分类和置信区间，而不只报告平均分。

### L4：Online Evaluation

监控真实流量：

- 业务完成率；
- 用户显式与隐式反馈；
- 漂移和新输入类型；
- 人工接管；
- 费用与延迟；
- 安全拦截和政策违规。

线上反馈带有选择偏差，不能直接当作真值。应抽样人工复核，并把代表性失败回流离线评估集。

## 九、验证器优先级

```text
最终环境状态
→ 确定性规则与测试
→ 业务专家标签
→ 经校准的LLM Judge
→ 未校准主观判断
```

LLM Judge适合评价风格、完整性和开放性质量，但不能独立决定：

- 用户权限；
- 账户事实；
- 支付是否完成；
- 法规是否满足；
- 高风险动作是否允许。

## 十、成本与模型路由

优化目标是：

```text
总运行成本 + 人工处理成本 + 失败损失
──────────────────────────────────
             成功任务数
```

模型路由可以把分类、抽取和简单总结交给较小模型，把复杂规划交给强模型。但路由本身需要评估集、Fallback和监控。缓存、并行和压缩也必须看最终成功率，不能只看Token下降。

---

# 第三部分　安全、审批与审计

## 十一、威胁模型

| 威胁 | 典型路径 | 控制 |
|---|---|---|
| 指令操纵 | 用户、网页、邮件要求忽略规则 | 信任分层、策略网关 |
| 关键系统访问 | 广泛数据库、文件或云权限 | 最小权限、读写分离 |
| 资源过载 | 无限循环、大量工具/API调用 | 预算、限流、并发上限 |
| 知识库污染 | 恶意文档进入RAG或Memory | 来源、审核、版本和删除 |
| 级联错误 | 一个工具错误触发后续写操作 | 校验、隔离、熔断 |
| 数据泄漏 | Prompt、Trace或工具结果含秘密 | 脱敏、最少记录、租户隔离 |
| Confused Deputy | 攻击者借Agent权限操作 | 绑定Actor、目的和准确载荷 |
| Replay | 重放旧审批或写请求 | 幂等键、Nonce、过期时间 |

### 11.1 权限不属于模型

模型的工具调用只是提议。执行前由代码检查：

```text
主体是谁？
→ 对哪个资源？
→ 执行什么动作？
→ 为哪个任务目的？
→ 在什么政策版本下？
→ 是否需要批准？
→ 批准是否绑定准确载荷且未过期？
```

外部内容即使被模型完全相信，也不能改变这些检查结果。

## 十二、工具风险等级

| 等级 | 示例 | 控制 |
|---|---|---|
| T0 | 纯计算 | 输入和资源上限 |
| T1 | 只读搜索、查询 | 范围、脱敏、速率限制 |
| T2 | 可逆草稿和临时写入 | 幂等、版本、撤销 |
| T3 | 发消息、提交表单、共享数据修改 | 预览、审批、结果验证 |
| T4 | 支付、删除、生产部署、法律承诺 | 双重控制、强身份、补偿/回滚、审计 |

通用Shell、SQL、HTTP或文件系统工具相当于扩大动作空间，必须使用沙箱、路径/域名白名单、资源限制和输出上限。高风险业务动作优先封装为窄工具。

## 十三、批准准确动作，而不是批准模糊意图

错误做法：

```text
“是否允许Agent处理退款？”
```

正确做法是批准不可歧义的预览：

```yaml
action: issue_refund
order_id: order_789
amount: 128.00
currency: CNY
payment_destination: original_method
policy_version: refund-v7
expires_at: 2026-09-21T10:15:00Z
action_digest: sha256:...
```

执行时重新计算Digest并与审批记录比较。金额、收款目标、政策或期限变化后，旧审批失效。

## 十四、审计与密码学回执

### 14.1 三个层级

1. **普通日志**：便于调试，但有权限者可能修改；
2. **不可变日志**：使用只追加存储和保留策略降低篡改风险；
3. **密码学回执**：对规范化事件签名，可独立验证归属和完整性，并用哈希链检测删除或重排。

### 14.2 回执记录什么

```yaml
type: agent.tool_call.v1
agent_id: support-agent
tool_name: issue_refund
tool_args_hash: sha256:...
result_hash: sha256:...
policy_id: refund-v7
timestamp: 2026-09-21T10:02:00Z
sequence: 47
previous_receipt_hash: sha256:...
signature:
  alg: EdDSA
  key_id: agent-gateway-key-3
  sig: ...
```

采用JCS等规范化编码，可以让不同实现对相同逻辑内容生成一致字节，再使用Ed25519等签名算法签署。

### 14.3 回执不能证明什么

回执不能证明：

- 动作是正确选择；
- 政策真的被执行；
- 签名密钥一定属于某个自然人；
- 输入没有被操纵；
- 外部系统返回的内容是真实世界事实。

因此回执必须与身份、授权、政策执行、验证器和密钥管理共同使用。

## 十五、发布与回滚

推荐发布路径：

```text
Offline replay
→ Shadow traffic
→ Canary
→ Bounded rollout
→ Full rollout
```

每阶段定义停止或回滚阈值：

- 任务成功率下降；
- 政策违规或越权；
- 重复副作用；
- p95延迟；
- 每成功任务成本；
- Fallback和人工接管率。

保留旧Prompt、Schema、模型路由、工具和政策版本，使运行可以解释和回滚。变更模型时，不应默认旧评估结论继续成立。

## 十六、端到端示例：受控退款Agent

```text
1. API验证用户身份，创建run_id
2. Agent只读查询订单和退款政策
3. Model提出退款候选
4. 程序验证订单、金额和政策
5. 生成准确预览和action_digest
6. 用户对准确载荷批准
7. 写入Checkpoint
8. 使用幂等键调用退款工具
9. 查询支付系统确认最终状态
10. 写入Artifact、Trace和签名回执
11. 只有权威状态为refunded才标记succeeded
```

失败恢复：

- 第8步超时：使用幂等键查询，不直接再次退款；
- 审批后金额变化：审批失效，重新预览；
- 服务不可用：Checkpoint后进入blocked或有界重试；
- 用户取消：在安全点停止，保留已完成状态；
- 预算耗尽：标记budget_exhausted，不生成“已完成”回答。

## 十七、生产检查清单

### 状态与可靠性

- [ ] 运行、状态和Schema有版本。
- [ ] 长任务可恢复、取消和防止过期写入。
- [ ] 所有副作用幂等。
- [ ] 错误分类决定是否重试。
- [ ] 预算和终止由代码执行。

### 评估与观测

- [ ] Trace覆盖模型、工具、检索、审批和验证。
- [ ] Telemetry经过秘密和PII脱敏。
- [ ] Outcome、Trajectory、System、Economics和Safety分别评估。
- [ ] Smoke Test不替代Offline Eval。
- [ ] 线上失败回流离线集。

### 安全与治理

- [ ] 授权不由模型决定。
- [ ] 外部内容不能增加权限。
- [ ] 高影响动作审批绑定准确载荷。
- [ ] 工具最小权限、读写分离并受沙箱限制。
- [ ] 审计记录可关联到政策、模型、工具和审批版本。
- [ ] 密码学回执没有被误当成正确性证明。

### 发布

- [ ] 定义Shadow、Canary、放量和回滚门槛。
- [ ] 旧版本仍可恢复。
- [ ] 新模型和Prompt经过私有评估集。
- [ ] 残余风险有明确业务Owner。

## 知识检查

1. 为什么模型不能直接修改运行状态中的`approval_granted`？
2. HTTP超时后为什么不能简单重试退款操作？
3. Observability和Evaluation分别回答什么问题？
4. Smoke Test为什么不能证明Agent质量？
5. 准确载荷审批如何缓解Confused Deputy和Replay？
6. 密码学回执能够证明和不能证明什么？
7. 为什么上线新模型需要重新执行私有评估？

## 来源与证据

本样章综合主仓库第1、4、6、7、9、10章，以及补充仓库Lesson 06、10、15、16、18。协议和标准来源包括OpenTelemetry、RFC 8785和RFC 8032。相关登记见：

```text
bluebook/data/sample-chapter-evidence.yml
bluebook/data/sample-references.yml
bluebook/data/sample-figures.yml
```
