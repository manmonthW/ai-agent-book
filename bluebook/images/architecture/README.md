# 核心架构图

8张图均提供三种格式：

- `.excalidraw`：可在Excalidraw中继续编辑的权威源文件；
- `.svg`：蓝皮书最终矢量图；
- `.png`：本地快速预览。

## 图表清单

| 图 | 章节 | Excalidraw源 | 最终SVG |
|---|---:|---|---|
| Agent边界与反馈闭环 | 1 | `fig01-agent-boundary-loop.excalidraw` | `fig01-agent-boundary-loop.svg` |
| 最低充分自主性阶梯 | 2 | `fig02-autonomy-ladder.excalidraw` | `fig02-autonomy-ladder.svg` |
| 统一执行图 | 3 | `fig03-unified-execution-graph.excalidraw` | `fig03-unified-execution-graph.svg` |
| 上下文生命周期 | 4 | `fig04-context-lifecycle.excalidraw` | `fig04-context-lifecycle.svg` |
| 知识与记忆边界 | 5 | `fig05-knowledge-memory-boundaries.excalidraw` | `fig05-knowledge-memory-boundaries.svg` |
| 工具执行与协议边界 | 6 | `fig06-tool-protocol-boundary.excalidraw` | `fig06-tool-protocol-boundary.svg` |
| Coding Agent闭环 | 7 | `fig07-coding-agent-loop.excalidraw` | `fig07-coding-agent-loop.svg` |
| 模态×时序与公共控制 | 8 | `fig08-modality-time-control.excalidraw` | `fig08-modality-time-control.svg` |

## 编辑

打开<https://excalidraw.com>，拖入对应`.excalidraw`文件。所有文本元素使用Excalifont（`fontFamily: 5`），颜色表达概念职责而非厂商。

## 再生成与验证

```bash
python3 bluebook/scripts/generate_excalidraw_figures.py
python3 bluebook/scripts/validate_figures.py
```

SVG包含`title`和`desc`无障碍元数据；PNG由本机`rsvg-convert`从最终SVG生成。
