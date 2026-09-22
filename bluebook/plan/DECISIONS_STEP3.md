# ADR-006：Environment Feedback 不是 Agent 的第四个内部组件

- **状态**：Accepted
- **决定**：保留 `Agent = LLM + Context + Tools` 作为 Agent 边界内的实现公式；Environment 位于边界外。生产表达使用“Model + Harness 与 Environment 形成反馈闭环”，而不是把 Environment Feedback 写成 Agent 内部相加项。
- **原因**：主仓库第1章已明确 Agent 与 Environment 的边界；否则会把外部状态转移规律误归入 Harness。
- **影响**：执行摘要总图必须同时画出内部结构和外部闭环。

# ADR-007：Metacognition 改写为可观察的控制节点

- **状态**：Accepted
- **决定**：补充库中的 Metacognition 内容拆解为 Planning、Evidence Evaluation、Corrective RAG、Verifier 和 Replanning，不作为不可测的独立能力层。
- **原因**：蓝皮书要求机制可实现、可观测、可评估。

# ADR-008：Smoke Test 只是可达性与基础行为门禁

- **状态**：Accepted
- **决定**：质量体系采用 Schema/Unit → Smoke → Offline Eval → Online Eval。Smoke Test 不得被描述为完整质量证明。
- **原因**：补充仓库明确其 Smoke Test 只验证部署回答和基本预期。

# ADR-009：实验编号允许跨章节复用实现

- **状态**：Accepted
- **决定**：同一实验编号可以由多个项目实现，同一项目也可支撑其他章节实验。目录保留所有 catalog location，不强行一对一。
- **原因**：例如 `3-1`、`3-2` 和 `6-3` 在用户记忆项目中交叉出现；覆盖会丢失证据关系。
