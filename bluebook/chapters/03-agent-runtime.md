# 第3章　Agent Runtime与执行图

> 状态：Release Candidate 1  
> 本章定位：把模型调用、工具、状态和人工节点组织为可检查的执行图。

## 本章回答的三个问题

1. ReAct、工作流、Planning和多Agent如何放进同一执行模型？
2. 执行图中的状态、节点、边和终止条件如何设计？
3. 什么情况下应增加路由、并行、Evaluator或Handoff？

## 5分钟速读

- Agent Runtime执行的是一个状态图：节点处理状态，边决定下一步，终态结束运行。
- LLM节点只承担语义决策；权限、计算、状态转移和副作用由确定性节点控制。
- Planning产生候选任务结构，环境变化后允许Replanning；计划不是事实。
- 并行只用于独立子任务，共享可变状态必须显式合并。
- Evaluator只有在读取独立证据时才比“再想一次”更可信。
- 每个循环必须有环境反馈、进步信号、硬预算和退出条件。
- 长任务需要持久状态机，而不是长时间占用一个进程。

## 一、统一执行图

![图3：统一执行图](../images/architecture/fig03-unified-execution-graph.svg)

可以用同一结构描述工作流和Agent：

```text
Node：模型、工具、普通程序、人工审批或等待事件
Edge：固定、条件、失败、重试或超时转移
State：节点之间传递的类型化事实和引用
Terminal：成功、部分成功、阻塞、失败、取消、预算耗尽
```

工作流和Agent的差别，不在于是否有图，而在于哪些边由程序预先决定，哪些边由模型根据当前观察提出。

## 二、最小状态Schema

```yaml
run_id: run_123
status: running
objective: 生成带引用的竞争分析
current_node: research
facts: []
artifacts: []
errors: []
approvals: []
budget:
  model_calls_remaining: 6
  tool_calls_remaining: 15
  deadline: 2026-09-21T12:00:00Z
versions:
  graph: 3
  prompt: research-v5
  toolset: web-readonly-v2
```

状态只保存权威事实、阶段进展和Artifact引用。冗长网页、代码和日志存入Artifact Store，由节点按需读取。

## 三、基础模式

### 3.1 Prompt Chain

```text
抽取需求 → 检索证据 → 生成草稿 → 格式校验
```

适合步骤稳定的任务。每个节点有输入输出Schema，节点失败不应悄悄把无效结果传给下游。

### 3.2 Router

根据任务类别、风险或复杂度选择不同路径：

```text
请求 → 确定性规则 → 模型辅助分类 → 专用流程 / Fallback
```

路由器需要独立评估，尤其检查边界类别和错误路由成本。

### 3.3 Fan-out/Fan-in

对独立子任务并行：

```text
任务 → [来源A, 来源B, 来源C] → 结构化合并 → 冲突检查
```

设置并发上限、超时、部分成功规则和合并契约。多个Worker不应直接修改同一文件或状态对象。

### 3.4 Evaluator–Optimizer

```text
生成候选 → 获取独立证据 → 评价缺口 → 修复 → 再验证
```

必须限制最大轮数并衡量每轮增益。测试、渲染、事实查询和业务规则属于有效新证据；同一模型只重读原文的自评较弱。

### 3.5 Tool Loop

下一步无法预先确定时：

```text
观察 → 模型提出行动 → 校验执行 → 新观察 → 继续/停止
```

必须有工具白名单、预算、重复检测和完成验证。

## 四、Planning与Replanning

Planning适合把模糊目标转为可追踪子任务，但计划应满足：

- 输出结构化；
- 子任务有完成条件；
- 依赖关系明确；
- 不把未知事实写成已确认事实；
- 工具反馈变化后允许更新；
- 高影响步骤提前标记审批。

示例：

```yaml
steps:
  - id: collect_sources
    depends_on: []
    success: at_least_three_authoritative_sources
  - id: compare_claims
    depends_on: [collect_sources]
    success: conflicts_explicitly_recorded
  - id: write_report
    depends_on: [compare_claims]
    success: citations_resolve
```

## 五、Loop Engineering

可靠循环包含：

```text
发现下一项工作
→ 执行
→ 独立验证
→ 提交进度
→ 判断继续或终止
```

模型可以提出完成，不能批准自己的完成。循环应检测：

- 状态是否有进展；
- 是否重复同一工具和参数；
- 最近错误是否变化；
- 剩余预算是否足够；
- 是否等待外部输入；
- 验证器是否通过。

## 六、Orchestrator、Worker与Handoff

### Orchestrator–Workers

适合未知、独立、可并行的子问题。Orchestrator负责拆分、预算、Artifact合并和冲突解决；Worker返回结构化结果而非全部轨迹。

### Handoff

适合专家需要直接继续用户对话。移交时必须过滤上下文、明确新责任主体、记录身份和政策变化，并支持转回或升级人工。

### Skill不是Subagent

如果差异只来自知识、流程或风格，优先加载Skill；只有需要独立上下文、权限、生命周期或任务所有权时才创建Subagent。

## 七、人工与事件节点

长任务常包含：

- 等待用户补充信息；
- 等待审批；
- 等待Webhook；
- 定时器；
- 外部任务完成通知。

Runtime应将运行持久化为`blocked/waiting`，收到相关事件后再恢复，而不是让线程持续等待。事件必须绑定`run_id`、期待类型和过期时间，防止错误唤醒。

## 八、失败和终止

每个节点定义：

- 输入Schema；
- 输出Schema；
- 超时；
- 可重试错误；
- 最大尝试次数；
- 补偿操作；
- 失败去向。

每个循环定义：

- 最大轮数；
- 最大成本和时间；
- 重复行为阈值；
- 成功验证器；
- 阻塞条件；
- 取消处理。

## 九、常见失败模式

| 失败 | 表现 | 控制 |
|---|---|---|
| 计划幻觉 | 把未查证事实写入计划 | 计划只存任务和假设 |
| 路由漂移 | 相似请求走不同路径 | 固定集评估、规则优先 |
| 并行冲突 | Worker覆盖同一产物 | 私有工作区、合并节点 |
| 无效审核 | Reviewer无新证据 | 接入测试、渲染或事实工具 |
| 过早完成 | 模型自称完成 | 外部验证器 |
| 循环不止 | 重复行动无进展 | 预算、重复检测、终态 |
| 上下文泄漏 | Handoff暴露无关信息 | Context filter与审计 |

## 十、执行图设计检查清单

- [ ] 每个节点职责单一且输入输出类型化。
- [ ] 模型只处理需要语义判断的节点。
- [ ] 状态与大型Artifact分离。
- [ ] 所有循环有新环境反馈和退出条件。
- [ ] 并行任务独立并有合并契约。
- [ ] Reviewer读取独立证据。
- [ ] 等待和审批通过持久状态实现。
- [ ] 失败、取消和预算耗尽都有终态。
- [ ] 图、Prompt、Schema和工具集均有版本。

## 知识检查

1. 工作流与Agent在执行图上的主要差别是什么？
2. 为什么计划不能包含未经验证的业务事实？
3. Evaluator–Optimizer需要什么信息增量？
4. 什么情况下Skill比Subagent更合适？
5. 等待人工审批时为什么不应持续占用进程？

## 来源与证据

主要来源为主仓库第1章和第10章，以及补充仓库Lesson 03、07、08、09和14。模式选择边界与第2章保持一致。
