# 正式发布就绪审计

> Blockers：7  
> 结论：**尚未达到正式发布门禁。**

## P0：发布阻断项

- [ ] references.yml remains seed
- [ ] unverified reference: rfc8785
- [ ] unverified reference: opentelemetry
- [ ] missing publication artifact: bluebook/mkdocs.yml
- [ ] missing publication artifact: bluebook/scripts/build_release.py
- [ ] missing publication artifact: bluebook/CITATION.cff
- [ ] missing publication artifact: bluebook/NOTICE.md

## P1：发布前必须人工确认

> 内容负责人已于2026-09-22确认完成全量人工内容审核；以下是证据、发行、外部专业审查和构建事项，不重复要求正文人工审核。

- [ ] exclude from release package: bluebook/chapters/09-11-production-control-plane-sample.md
- [ ] exclude from release package: bluebook/chapters/_CHAPTER_TEMPLATE.md
- [ ] exclude from release package: bluebook/patterns/_PATTERN_CARD.md
- [ ] reference missing author/organization: rfc8785
- [ ] reference missing author/organization: opentelemetry
- [ ] experiment cards deeply reviewed: 4/109; content owner review is recorded for the book, but evidence-level deep review remains 4/109; publish unreviewed cards only as a status-labelled catalog
- [ ] third-party asset register is inventory-wide and mostly pending; public package must include only eight original architecture figures unless each extra asset is cleared
- [ ] external subject-matter, security/privacy, copyediting, accessibility, and legal reviews are not recorded
- [ ] PDF/EPUB/website builds and print preflight have not been demonstrated

## 已通过

- 章节、模式、实验卡数量和结构门禁；
- 第1–14章严格内容扫描；
- 内部Markdown链接完整性；
- 8张Excalidraw/SVG图表及第3、7、8图重叠检查；
- 治理目录基础完整性。

## 建议发布顺序

1. 冻结内容与状态，移除样章/模板出包；
2. 补齐参考文献、脚注、作者、URL访问日期和许可证；
3. 建立独立MkDocs与PDF/EPUB构建；
4. 完成外部专家、安全隐私、编辑、无障碍和法律审查；
5. 生成RC并执行链接、移动端、打印和安装验证；
6. 签署发布清单，打版本Tag并归档构建产物与SBOM。
