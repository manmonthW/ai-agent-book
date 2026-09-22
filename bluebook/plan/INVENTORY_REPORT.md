# Step 2 盘点报告

> 生成日期：2026-09-21  
> 状态：自动扫描完成，等待人工深度分类

## 范围

主源：`ai-agent-book`  
补充源：`../ai-agents-for-beginners`

为避免翻译镜像和历史对话造成重复，自动扫描排除了：

- `.git`、虚拟环境、构建目录；
- 主仓库 `cursor-chats`；
- 补充仓库 `translations`、`translated_images`；
- 当前 `bluebook` 工作区。

多语言书稿仍保留在仓库中，但蓝皮书内容映射以中文原稿和补充库英文原稿为准；翻译发布策略后续单独处理。

## 自动盘点结果

| 类型 | 主仓库 | 补充仓库 |
|---|---:|---:|
| Markdown 文件 | 1,145 | 67 |
| Notebook | 0 | 40 |
| 图片资产 | 2,897 | 78 |
| 正文/README 实验编号 | 109 | — |
| 课程目录 | — | 19（含 00 setup） |

机器可读结果：

- `bluebook/data/source-map.yml`
- `bluebook/data/experiments.yml`
- `bluebook/data/figures.yml`
- `bluebook/data/inventory-summary.yml`

扫描脚本：

```bash
python3 bluebook/scripts/inventory_sources.py \
  --primary . \
  --supplementary ../ai-agents-for-beginners \
  --output bluebook/data
```

## 质量观察

1. 主仓库 Markdown 数量远高于书稿章节数，原因是每个实验及其验证材料均包含文档；后续不能把每个文件等权纳入主文。
2. 主仓库实验 README 成功识别 109 个编号，与总览声明一致。
3. 补充仓库的 40 个 Notebook 应标记为框架案例或补充实践，不能与主仓库实验自动合并计数。
4. 图片资产数量较大，包含实验输出、翻译资源、网页资产和正文图；需要按“正文候选/实验证据/界面截图/排除”分类。
5. 自动盘点仅证明资产存在，不证明代码运行、实验完成、结论正确或许可证已核验。

## 人工抽查策略

下一轮按风险分层抽查：

- 100% 检查 `book/chapter1–10.md`、引言、后记和答案；
- 100% 检查 `chapter1–10/README.md` 的 109 个实验映射；
- 100% 检查补充库 01–18 课程 README；
- 100% 检查安全、评估、部署和协议相关 Notebook 的标题与目标；
- 图片按章节分层抽样，并对所有拟进入主文的图片做许可证核验；
- 其他实验文档先自动分类，再对进入主文的候选进行逐项人工审查。

## 当前结论

Step 2 的资产发现和数量门禁已经达到；内容目标章节、证据等级、许可证和保留/排除决定将在 Step 3 治理阶段完成。
