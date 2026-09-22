# 实验2-5：Prompt Injection攻击与防御矩阵

> 状态：已审查  
> 证据等级：E4（完整真实运行矩阵、Manifest与逐Cell Artifact）  
> 证据截至：2026-07-30

## 问题与设计

比较直接、间接和Memory注入三类攻击，在无防御、Prompt加固、来源标记和组合防御四种条件下的行为。每个Cell重复五次，共60次试验。

## 证据

- `chapter2/prompt-injection/validation/latest.json`；
- `validation/runs/exp2-5-kimi-k3-20260730-v1/comparison.json`；
- 同目录`manifest.json`和60个Cell文件；
- 模型：Kimi K3；
- 153次Provider调用；
- 使用隔离文件系统、Outbox和新Session验证Memory攻击；
- Manifest保存Artifact Hash，凭据扫描通过。

## 观察

所有三类攻击、四种防御条件的观测攻击成功均为0，包括无防御基线。

## 可支持的主张

- 攻击矩阵和防御实现已按协议运行；
- 测试环境可检查文件、Outbox和Memory副作用；
- 零事件结果暴露了攻击集或模型覆盖不足，需要更强攻击与更多模型。

## 不支持的主张

- Prompt加固、来源标记或组合防御降低了攻击成功率；
- 模型或系统已经安全；
- 每增加一层防御都带来方向性收益。

## 局限

单模型、每Cell五次、预定义攻击；全部零事件导致无法估计防御间相对效果。运行通过只表示实验协议完成，不表示原假设成立。

## 蓝皮书映射

第4章外部内容信任；第10章零事件结果解释；第11章Prompt不能代替代码授权。
