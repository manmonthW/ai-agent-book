# AI Agent 蓝皮书全局规划

> 状态：规划基线 v0.1  
> 方法：Planning with Files  
> 主内容源：本仓库 `ai-agent-book`  
> 补充内容源：`../ai-agents-for-beginners`  
> 原则：先盘点、再映射、后写作；不直接覆盖现有 `book/`。

## 1. 项目使命

将两个仓库融合为一套厂商中立、决策导向、证据可追溯的 AI Agent 蓝皮书体系：

- 主册帮助决策者、架构师和工程团队建立统一认知并作出技术决策；
- 模式手册提供可复用架构模式和生产检查表；
- 实验图谱保存主仓库 109 个实验以及补充仓库精选 Notebook、Smoke Test 和案例；
- 所有结论能追溯到正文、实验、代码、论文或厂商案例；
- 主文容易阅读，深层技术和复现细节不丢失，但下沉到附录和实践册。

核心叙事：

```text
Agent = LLM + Context + Tools
Production Agent = Model + Harness + Environment Feedback
```

核心立场：选择满足任务的最低自主性；把语义判断交给模型，把权限、事实、状态、预算、验证和不可逆副作用留在确定性控制面。

## 2. 成功标准

### 2.1 内容成功

- 两个仓库的全部主要内容单元均有迁移状态：主文、附录、实验卡、引用或明确排除。
- 主文不依赖任何单一厂商框架；Microsoft Foundry/MAF 只作为案例。
- 每个定量结论注明来源、日期、环境和证据级别。
- 每个核心概念只有一个权威定义位置，其他章节通过链接引用。
- 109 个主仓库实验全部进入实验登记，补充仓库示例单独标记为辅助案例。

### 2.2 阅读成功

- 决策者可在 30 分钟内读完执行摘要并理解采用建议、风险和路线图。
- 每章支持 5 分钟速读、30 分钟理解、动手验证三条路径。
- 每章包含：问题、结论、架构、取舍、案例、失败模式、检查清单。
- 深层算法、长代码、环境安装和外部仓库命令不打断主线。

### 2.3 工程成功

- PDF、EPUB、Web 尽量由同一 Markdown 内容源生成。
- 内部链接、代码路径、引用、术语和实验状态可自动校验。
- 每个实践案例至少有 Schema/Unit Test 或 Smoke Test；核心案例进入 Offline Eval。
- 原始书稿保持不变，蓝皮书在独立目录迭代。

## 3. 读者与阅读路线

| 读者 | 核心问题 | 推荐路线 |
|---|---|---|
| 决策者/产品负责人 | 是否值得做、收益、风险、路线图 | 执行摘要 → 场景选择 → 评估 → 治理 → 采用路线图 |
| 架构师/技术负责人 | 用何种架构、边界和控制面 | 自主性选择 → Runtime → Context/Memory/Tools → Harness → Security |
| 开发者 | 如何实现、验证、部署 | 架构篇 → 生产篇 → 模式手册 → 实验图谱 |
| 研究者/高级工程师 | 后训练、持续进化、多 Agent | 评估 → 进化 → 后训练 → 多 Agent → 技术附录 |

每章设置：

- **5 分钟速读**：一页结论、核心图、决策表；
- **30 分钟理解**：正文、案例、风险；
- **动手验证**：实验卡、代码路径、验收条件。

## 4. 出版物总体架构

### 4.1 主册：《AI Agent 蓝皮书：从原理、架构到生产实践》

目标 250–350 页，强调决策、架构、生产和趋势。

### 4.2 辅册 A：《AI Agent 架构与工程模式手册》

模式卡、ADR 模板、威胁模型、生产检查清单、平台选型矩阵。

### 4.3 辅册 B：《AI Agent 实验与证据图谱》

主仓库 109 个实验 + 补充仓库精选 Notebook/Smoke Test，记录机制、基线、变量、指标、证据和复现状态。

### 4.4 数字附录

完整参考文献、外部仓库固定版本、平台案例、代码索引、构建说明和变更记录。

## 5. 主册目录

### 第 0 章 执行摘要

回答：AI Agent 是什么、为何现在重要、企业如何判断是否采用。

- 十条蓝皮书结论；
- Agent、Chatbot、Copilot、Workflow、RPA 对比；
- 自主性升级阶梯；
- 企业成熟度模型；
- 价值、风险、成本和采用路线图；
- 全书总架构图。

主要来源：主库引言/第1章；补充库 01、03、STUDY_GUIDE；新增综合内容。

### 第一篇：认知与架构选择

#### 第 1 章 定义、边界与产业演进

- `Agent = LLM + Context + Tools`；
- 大脑/眼睛/手脚与 Policy/Observation/Action；
- Model–Harness–Environment 边界；
- 典型产品与场景；
- 什么不是 Agent。

来源：主库引言、第1章；补充库 01。

#### 第 2 章 什么时候应该使用 Agent

- 任务分类：Transform、Pipeline、Route、Parallel、Explore、Refine、Delegate、Converse、Long-running；
- 最低充分自主性：确定性代码 → 结构化调用 → RAG → Workflow → 有界 Agent → 多 Agent；
- 是否需要环境反馈、动态步骤、成功验证和人工批准；
- 延迟、质量、成本和影响等级；
- 架构决策记录 ADR。

来源：主库第1、7、10章；补充库 01、02、03、07、08；新增决策框架。

#### 第 3 章 Agent Runtime 与执行图

- ReAct 与轨迹；
- 静态前缀 + 动态历史；
- Planning、Routing、Fan-out/Fan-in、Evaluator–Optimizer；
- Workflow 与自主循环；
- 结构化中间状态；
- 终止条件和预算；
- Graph Engineering。

来源：主库第1、10章；补充库 03、07、09、14。

### 第二篇：核心能力

#### 第 4 章 上下文工程

- API 消息结构；
- 当前决策所需上下文；
- KV Cache 三条工程结论；
- Prompt、Skills、状态栏、压缩；
- Context Poisoning、Distraction、Confusion、Clash；
- Prompt Injection 和信任标签；
- 上下文预算与渐进披露。

来源：主库第2章；补充库 12、09。

#### 第 5 章 记忆、RAG 与知识系统

- 当前状态、用户记忆、知识库、Artifact 的边界；
- 用户记忆四级策略；
- 稀疏/向量/混合检索、Rerank；
- Agentic/Corrective RAG；
- 多模态记忆；
- 来源、时效、租户隔离、删除和污染防护。

来源：主库第3章；补充库 05、09、13、17。

#### 第 6 章 工具、协议与动作边界

- 感知、执行、协作、事件触发、用户沟通；
- Narrow capability、Typed input、Read/Write separation、Dry-run、Idempotency；
- 工具风险等级 L0–L4；
- Tool Calling、MCP、A2A、NLWeb、REST/Event 的边界；
- 工具发现与 Skill Hub；
- 协议不替代身份、授权和策略。

来源：主库第4章；补充库 04、11、17。

#### 第 7 章 Coding Agent：通用 Agent 的工程母型

- 代码作为元工具；
- 搜索、编辑、测试、修复循环；
- 文件系统与 Artifact；
- 沙箱、权限和验证器；
- OpenClaw 等架构案例；
- 代码用于分析、文档、PPT、视频和新工具创建。

来源：主库第5章；补充库 09 的代码工具内容。

#### 第 8 章 实时、异步与多模态交互

- 模态 × 时序框架；
- 事件驱动和长任务；
- 实时语音；
- Computer Use 的 Agent/Actor 分层；
- 机器人；
- 唤醒、取消、抢占、安全点、快慢路径；
- API 优先，GUI 作为受控兜底。

来源：主库第6章；补充库 15。

### 第三篇：生产控制面

#### 第 9 章 Harness：从 Demo 到可靠产品

- Run identity、状态 schema、状态机和版本；
- Checkpoint、恢复、取消、Stale-run fencing；
- 幂等、重试、超时、Fallback、Circuit Breaker；
- Token/Tool/Time/Cost/Concurrency 预算；
- Artifact 与 Provenance；
- Human approval；
- 本地、云端、托管与混合部署；
- Agent SDK、Graph、Hosted Service 选择。

来源：主库第1、6、9、10章；补充库 02、14、16、17。

#### 第 10 章 评估、可观测性与成本

- 成功条件；
- 结果、轨迹、系统、成本、安全五层评估；
- Trace/Span 与 OpenTelemetry；
- Schema/Unit → Smoke → Offline → Online 四级质量门；
- 数据集、确定性验证器、LLM Judge；
- 统计显著性、模型路由与成本/成功任务；
- Offline → Shadow → Canary → Rollout；
- 线上失败回流离线集。

来源：主库第7章；补充库 10、16、tests。

#### 第 11 章 安全、权限、审批与审计

- 所有模型/检索/工具结果均视为不可信输入；
- 身份、授权、策略在代码层执行；
- 最小权限、沙箱、网络/文件/数据库边界；
- Task manipulation、Critical systems、Overload、Knowledge poisoning、Cascading errors；
- Preview + Approval + Exact payload binding；
- 普通日志、不可变日志、密码学回执；
- Ed25519/JCS/哈希链的概念与边界；
- Prompt Injection 不可扩权；
- 数据隐私、多租户和秘密管理。

来源：主库第2、4、6、10章；补充库 06、15、18。

### 第四篇：能力提升

#### 第 12 章 从轨迹到持续进化

- 环境结果、过程规则和 Rubric 学习信号；
- 知识、Prompt/Skill、程序/Harness、参数四类更新载体；
- 失败聚类和根因分析；
- 版本化、离线回放、灰度和回滚；
- 经验污染与遗忘；
- 优先更新最可控的外部载体。

来源：主库第9章；补充库 09、10、13。

#### 第 13 章 模型后训练

- Pre-training、Mid-training、SFT、RL；
- SFT 记忆、RL 泛化；
- 数据与环境比算法更重要；
- 工具调用轨迹合成；
- 奖励、验证路径惩罚、多轮信用分配；
- 蒸馏和样本效率；
- 何时不该训练模型。

来源：主库第8章；补充库仅作框架/本地模型案例补充。

#### 第 14 章 多 Agent：何时值得复杂化

- 准入测试：新信息、并行、上下文隔离、身份/权限、Artifact ownership；
- 共享/独立上下文；
- Peer、Manager、Handoff、Decentralized；
- 数据平面与控制平面；
- 虚拟文件系统、消息、状态、取消、预算和调度；
- Proposer–Reviewer 必须读取独立证据；
- A2A；
- 失败模式和成本；
- Agent 社会作为趋势判断。

来源：主库第10章；补充库 08、11。

### 结语：组织如何采用 Agent

- 试点选择；
- 评估先行；
- 组织能力与职责；
- 90/180/365 天路线图；
- 残余风险和未来方向。

## 6. 辅册 A：模式手册目录

每个模式固定一页模板：问题、适用、避免、执行图、状态、终止、控制、指标、实验。

1. Single Structured Call
2. Retrieval-Augmented Call
3. Prompt Chain
4. Router
5. Parallel Fan-out/Fan-in
6. Planning + Replanning
7. ReAct Tool Loop
8. Evaluator–Optimizer
9. Proposer–Reviewer
10. Human Approval Gate
11. Durable State Machine
12. Event-driven Agent
13. Agentic/Corrective RAG
14. Orchestrator–Workers
15. Handoff
16. Computer Use Agent/Actor
17. Local/Cloud Hybrid Router
18. Budget-aware Loop
19. Cryptographic Action Receipt
20. Multi-Agent Artifact Merge

## 7. 辅册 B：实验与证据体系

### 7.1 实验分类

- 机制实验：验证单一设计变量；
- 架构案例：展示端到端系统；
- 框架示例：演示具体 SDK，不作为通用结论；
- 部署示例：Hosted/Local/Hybrid；
- 安全实验：审批、沙箱、注入、审计；
- 外部复现：固定上游版本但不等于已完成验证。

### 7.2 实验卡 schema

```yaml
id:
title:
source_repo:
source_path:
chapter_target:
question:
claim_supported:
mechanism:
baseline:
variant:
inputs:
outputs:
metrics:
expected_result:
observed_result:
evidence_paths:
verification_status:
runtime:
hardware:
credentials:
external_dependencies:
difficulty:
cost_level:
license_status:
```

### 7.3 证据级别

- E0：观点/经验判断；
- E1：第三方文档或厂商案例；
- E2：仓库有代码但未验证；
- E3：本地 Smoke Test 通过；
- E4：可重复实验与指标；
- E5：多环境/多模型复现或外部研究一致。

主文中的强因果表述原则上需要 E4+；否则改写为观察、案例或待验证假设。

## 8. 内容融合规则

### 8.1 来源优先级

1. 主仓库：概念主干、工程原则、实验；
2. 补充仓库：初学者表达、Planning、框架、部署、安全、Smoke Test；
3. 一手标准/论文/官方文档：事实核验；
4. 新编内容：跨来源综合、决策矩阵、生产控制面。

### 8.2 厂商中立

- MAF/Foundry、LangGraph、OpenAI、Anthropic 等均作为案例；
- 主文先给框架无关契约，再给具体实现；
- 产品功能必须标注版本和日期；
- 不把 SDK 便利性等同于系统可靠性。

### 8.3 去重与归属

- Harness 权威定义：第9章；
- 安全治理：第11章；
- ReAct/执行图：第3章；
- Context：第4章；Memory/RAG：第5章；
- 轨迹评估：第10章；轨迹学习：第12章；
- Proposer–Reviewer：第14章定义，第7章给 Coding 案例；
- 文件系统：第7章讲单 Agent，第14章讲多 Agent；
- 算法深潜移至附录。

### 8.4 引用与许可证

- 不直接复制补充仓库长段正文；采用原创重写；
- 图片、表格和代码逐项登记来源、许可证和修改说明；
- 每条外部定量结论进入 `claims.yml`；
- Microsoft 商标和产品截图遵循其品牌和商标条款；
- 第三方子项目单独核验许可证。

## 9. 统一写作规范

每章结构：

```markdown
# 标题
## 本章回答的三个问题
## 5 分钟速读：一页结论
## 核心概念与边界
## 架构与运行机制
## 设计选择和取舍
## 代表案例
## 常见失败模式
## 生产建议
## 实验与证据
## 决策/检查清单
## 知识检查
## 延伸阅读
```

段落顺序：问题 → 原理 → 架构 → 案例 → 风险 → 建议。

信息框：蓝皮书结论、架构决策、风险警示、实验结论、厂商案例、技术深潜。

术语规则：首次出现给出中英文和缩写；后续使用统一中文名；避免将“Agent、Workflow、Skill、Memory、RAG”互相替代。

## 10. 核心图表清单

### 全书级

1. Agent–Environment 闭环与 Model–Harness 结构
2. 最低充分自主性阶梯
3. Agent 场景选择决策树
4. 企业 Agent 成熟度模型
5. 从 Prototype 到 Production 控制面
6. Context/Memory/RAG/Artifact 边界
7. 工具风险 L0–L4
8. 评估与发布闭环
9. 持续进化四载体
10. 多 Agent 准入与拓扑选择
11. Local/Cloud/Hybrid 部署
12. 安全、审批、执行和审计链

### 图表要求

- 可单独理解；
- 数据图注明来源、版本、日期和环境；
- 不使用无法核验的营销数字；
- SVG 为源格式，PNG 仅用于兼容输出；
- 统一配色、字体、线型和图例。

## 11. Planning with Files 工作区

计划创建：

```text
bluebook/
├── README.md
├── plan/
│   ├── MASTER_PLAN.md
│   ├── TASKS.md
│   ├── DECISIONS.md
│   ├── RISKS.md
│   └── PROGRESS.md
├── editorial/
│   ├── STYLE_GUIDE.md
│   ├── TERMINOLOGY.md
│   ├── EVIDENCE_POLICY.md
│   └── LICENSE_POLICY.md
├── data/
│   ├── source-map.yml
│   ├── experiments.yml
│   ├── claims.yml
│   ├── references.yml
│   ├── glossary.yml
│   └── figures.yml
├── chapters/
├── handbook/
├── experiments/
├── appendices/
├── images/
└── scripts/
```

文件职责：

- `MASTER_PLAN.md`：稳定总体目标和架构；
- `TASKS.md`：当前可执行任务、依赖和验收；
- `DECISIONS.md`：ADR，记录目录、术语、取舍变更；
- `RISKS.md`：内容、许可证、事实时效、构建风险；
- `PROGRESS.md`：每次工作后的进展、证据和下一步；
- `source-map.yml`：两个仓库所有内容的去向；
- `claims.yml`：定量与高风险断言；
- `experiments.yml`：实验登记；
- `figures.yml`：原图复用/重绘/淘汰决定。

## 12. 分阶段执行计划

### Phase 0：冻结规划与规则

产物：目录、编辑规范、证据政策、许可证政策、ADR 模板。

验收：目标、读者、目录、来源优先级和完成定义获得确认。

### Phase 1：双仓库全量盘点

任务：

- 解析所有 Markdown 标题、图、代码块、参考文献；
- 枚举主库 109 个实验；
- 枚举补充库 18 课、Notebook、Smoke Test；
- 生成内容单元 ID；
- 标记重复、冲突、过时和厂商特定内容。

产物：`source-map.yml`、`experiments.yml`、`figures.yml` 初版。

验收：每个二级标题、实验、图和主要代码案例均有记录。

### Phase 2：术语、主张与引用治理

任务：

- 建立术语表和唯一权威定义；
- 提取所有定量主张和时间敏感产品信息；
- 登记来源与许可证；
- 将主张标记为事实、实验观察、案例或预测。

验收：强主张均可追溯；冲突术语有 ADR。

### Phase 3：四个样章

先写：

1. 第0章执行摘要；
2. 第2章何时使用 Agent；
3. 第4章上下文工程；
4. 第9–11章合并样章“生产控制面”。

目的：验证易读性、技术深度、厂商中立和证据链。

验收：目标读者走查；每章三层阅读路径完整；引用和实验卡可跳转。

### Phase 4：核心能力篇

重构第1、3、5、6、7、8章；先图表和决策表，再写正文。

验收：概念不重复定义；关键架构有图；每章至少一个证据案例。

### Phase 5：生产与提升篇

完成第9–14章和组织采用结语。

验收：状态、预算、权限、评估、回滚形成闭环；多 Agent 有准入门槛。

### Phase 6：实验资产化

- 109 个主实验全部生成实验卡；
- 选 20–30 个进入主文；
- 其余进入实验图谱；
- 补充仓库示例按 framework/case/smoke 分类；
- 自动校验路径和状态。

### Phase 7：模式手册与附录

完成 20 张模式卡、检查清单、技术深潜和平台案例。

### Phase 8：编辑、构建与发布

- 技术审校、中文编辑、事实核验；
- 图表统一；
- PDF/EPUB/Web 构建；
- 链接、引用、术语、实验路径自动检查；
- 发布候选版、反馈、修订和版本日志。

## 13. 工作包与依赖

| WP | 工作包 | 依赖 | 主要产物 |
|---|---|---|---|
| WP0 | 规划与编辑制度 | 无 | 计划、规范、ADR |
| WP1 | 主仓库内容盘点 | WP0 | 主源映射 |
| WP2 | 补充仓库内容盘点 | WP0 | 补充源映射 |
| WP3 | 实验与证据登记 | WP1, WP2 | experiments/claims |
| WP4 | 术语和引用治理 | WP1, WP2 | glossary/references |
| WP5 | 样章 | WP3, WP4 | 4 个样章 |
| WP6 | 核心能力篇 | WP5 | 第1–8章 |
| WP7 | 生产与提升篇 | WP5 | 第9–14章 |
| WP8 | 模式手册 | WP6, WP7 | 20 张模式卡 |
| WP9 | 实验图谱 | WP3, WP6, WP7 | 实践册 |
| WP10 | 图表系统 | WP5 | SVG 资产 |
| WP11 | 构建与 QA | WP6–WP10 | PDF/EPUB/Web |

## 14. 风险与控制

| 风险 | 控制 |
|---|---|
| 内容过大，主册重新变成教材全集 | 严格主文/附录/实验册分层；设置页数预算 |
| 两库概念冲突 | 术语表 + ADR；以框架无关定义为准 |
| Microsoft 内容导致厂商偏向 | 先抽象契约，再放厂商案例；显式标记 |
| 未来日期或快速变化内容失效 | 每条时间敏感主张记录 as-of 日期 |
| 实验存在不等于结果已验证 | verification_status 和证据等级分离 |
| 第三方图片/代码许可证不清 | 许可证登记；不清晰则重绘或原创重写 |
| LLM Judge 被当作事实裁判 | 优先确定性验证；Judge 需校准且非唯一依据 |
| 多 Agent 被过度包装 | 准入测试；与单 Agent 等预算基线对比 |
| 安全只停留在 Prompt | 权限、审批、幂等、审计均在代码控制面 |
| 浅克隆缺少历史信息 | 内容规划不依赖历史；需要归因时再补取提交 |

## 15. 完成定义

蓝皮书进入发布候选版前，必须满足：

- 两个仓库主要内容覆盖率 100%，每项有明确去向或排除理由；
- 主库 109 个实验登记率 100%；
- 主文无未登记定量主张；
- 核心概念术语一致；
- 每章有一页结论、核心图、失败模式、检查清单和来源；
- 高风险动作章节覆盖授权、审批、幂等、审计和恢复；
- 所有内部链接、代码路径和引用检查通过；
- PDF、EPUB、Web 构建通过；
- 至少完成一次决策者、架构师、开发者三类读者走查；
- 发布说明包含版本日期、已知局限和后续更新策略。

## 16. 下一步

本规划确认后进入 Phase 0/1，依次创建 `bluebook/` 规划文件、自动盘点脚本和双仓库内容映射；暂不开始正文大规模改写。
