# 实验 8-18：中文弯引号作用域 Bad Case：人工审计合成数据 + 显式 Skill 正反规则 → Qwen3-8B bf16 L

> 状态：自动生成，待证据审查  
> 初步证据等级：E2  
> 验证状态：pending

## 要回答的问题

中文弯引号作用域 Bad Case：人工审计合成数据 + 显式 Skill 正反规则 → Qwen3-8B bf16 LoRA SFT → 9 种代码语言和 10 种文章体裁回归；manifest；RTX PRO 6000 真实训练已完成，1024/256/256（训练/留出/边界），适配后 exact 96.9%/97.7%，保护区保持 100%

## 蓝皮书目标章节

13

## 来源位置

chapter8/README.md:39

## 代码与Artifact

- `chapter8/curly-quote-sft`

## 假设、基线与变量

待人工从正文和实验README提取。不得把项目存在视为假设成立。

## 输入、环境与版本

待核验模型、数据、工具、运行日期、硬件和外部依赖。

## 指标与完成门禁

待从EXPERIMENT_LEDGER、validation manifest或实验README登记。

## 观察结果

待审查原始证据后填写。失败、阻塞和未复现结果必须保留。

## 局限

- 当前证据等级仅基于目录和README状态；
- E3及以上需要真实运行或可复核Artifact；
- 不得跨模型、数据集或环境外推。

## 可支持的蓝皮书主张

待人工裁决。
