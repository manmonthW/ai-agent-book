# Step 3 知识治理报告

> 日期：2026-09-21  
> 状态：治理种子建立，逐项核验待继续

## 已建立

### 1. 精选内容映射

`bluebook/data/curated-source-map.yml` 收录 33 个核心来源单元：

- 主仓库引言、10章正文、后记、参考答案和学习建议；
- 补充仓库 00–18 课程 README。

每个单元记录目标章节、处理方式、内容角色和二级标题结构。

### 2. 核心术语

`bluebook/data/glossary.yml` 已建立20个核心术语种子，包括 Agent、Model、Harness、Environment、Context、Memory、RAG、Tool、Skill、Workflow、Trajectory、Artifact、Evaluation、Observability、MCP、A2A、Multi-Agent、Approval 和 Idempotency。

### 3. 核心主张

`bluebook/data/claims.yml` 已登记8条高层主张并附证据等级与验证状态。所有记录当前仍为 `pending`，不能直接视作发布级事实。

### 4. 引用与许可证

- 主仓库根许可证：Apache License 2.0；
- 补充仓库根许可证：MIT；
- 第三方图片、论文图、外部项目和产品截图仍需逐项核验；
- 已登记 RFC 8785 与 OpenTelemetry 作为首批标准来源。

## 高风险内容人工抽查

已优先检查补充仓库：

- Lesson 06：威胁分类与 Human-in-the-Loop；
- Lesson 10：Trace/Span、Offline/Online Eval 和成本；
- Lesson 15：Computer Use；
- Lesson 16：部署与 Smoke Test；
- Lesson 18：密码学回执及其能力边界。

相应 Notebook 已确认存在：

- `06-human-in-the-loop.ipynb`
- `06-system-message-framework.ipynb`
- `10-expense_claim-demo.ipynb`
- `10-python-agent-framework.ipynb`
- `15-browser-user.ipynb`
- `16-python-agent-framework.ipynb`
- `18-signed-receipts.ipynb`
- `human-authorization-receipts.ipynb`

补充仓库还包含4组部署 Smoke Test catalog，适合作为蓝皮书四级质量门中的 L2，而不是完整质量评估。

## 质量结论

- 两个仓库可以互补，但不能简单拼接；主库负责体系和实验，补充库负责课程化表达、生产案例和安全补充。
- Microsoft 相关实现统一标为厂商案例，不进入框架无关定义。
- 密码学回执内容可进入安全章，但必须保留“不能证明正确性与合规性”的边界。
- 自我检查和 Metacognition 内容不能直接表述为可靠自纠；必须要求独立环境证据或验证器。
- 所有 E4/E5 主张在样章前仍需补齐具体来源和适用条件。

## Step 3 剩余工作

1. 对主文候选图片逐项作复用/重绘决定；
2. 从正文和补充课程提取定量、时效性主张；
3. 给109个实验填写目标章节和初步证据等级；
4. 补齐核心论文、协议、标准和官方文档引用；
5. 解决术语冲突并形成 ADR；
6. 执行来源路径和许可证自动检查。
