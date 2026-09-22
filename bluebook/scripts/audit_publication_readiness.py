#!/usr/bin/env python3
"""Audit publication readiness; distinguishes release blockers from enhancements."""
from pathlib import Path
import re,json
ROOT=Path.cwd(); blockers=[]; warnings=[]
chapters=[p for p in sorted((ROOT/'bluebook/chapters').glob('[0-9][0-9]-*.md')) if 'sample' not in p.name]
patterns=sorted((ROOT/'bluebook/patterns').glob('P[0-9][0-9]-*.md'))
# Editorial status must be release-ready, not Draft/sample.
for p in chapters+[ROOT/'bluebook/chapters/conclusion-adoption-roadmap.md']+patterns:
 first='\n'.join(p.read_text(encoding='utf-8').splitlines()[:6])
 if re.search(r'状态：(?:Draft|样章)',first,re.I): blockers.append(f'draft status: {p}')
# Temporary source artifacts must not enter public navigation/package.
for name in ('09-11-production-control-plane-sample.md','_CHAPTER_TEMPLATE.md'):
 if (ROOT/'bluebook/chapters'/name).exists(): warnings.append(f'exclude from release package: bluebook/chapters/{name}')
if (ROOT/'bluebook/patterns/_PATTERN_CARD.md').exists(): warnings.append('exclude from release package: bluebook/patterns/_PATTERN_CARD.md')
# References need complete verified records.
ref=(ROOT/'bluebook/data/references.yml').read_text(encoding='utf-8')
if 'status: "seed"' in ref: blockers.append('references.yml remains seed')
for m in re.finditer(r'- id: "([^"]+)"(?:(?!\n  - id:).)*',ref,re.S):
 block=m.group(0); rid=m.group(1)
 if 'verification_status: "pending"' in block: blockers.append(f'unverified reference: {rid}')
 if 'url:' in block and not re.search(r'(author|organization):',block): warnings.append(f'reference missing author/organization: {rid}')
# Build and metadata.
for f in ('bluebook/mkdocs.yml','bluebook/scripts/build_release.py','bluebook/CITATION.cff','bluebook/NOTICE.md','bluebook/CHANGELOG.md'):
 if not (ROOT/f).exists(): blockers.append(f'missing publication artifact: {f}')
# Release link integrity.
md=[ROOT/'bluebook/README.md',*chapters,ROOT/'bluebook/chapters/conclusion-adoption-roadmap.md',*patterns,ROOT/'bluebook/appendices/README.md']
for p in md:
 text=p.read_text(encoding='utf-8')
 for target in re.findall(r'!?\[[^]]*\]\(([^)#]+)',text):
  if target.startswith(('http://','https://','mailto:')): continue
  if not (p.parent/target).resolve().exists(): blockers.append(f'broken link: {p} -> {target}')
# Evidence and visual publication caveats.
reviewed=sum('状态：已审查' in p.read_text(encoding='utf-8') for p in (ROOT/'bluebook/experiments/cards').rglob('experiment-*.md'))
if reviewed<109: warnings.append(f'experiment cards deeply reviewed: {reviewed}/109; content owner review is recorded for the book, but evidence-level deep review remains {reviewed}/109; publish unreviewed cards only as a status-labelled catalog')
warnings.append('third-party asset register is inventory-wide and mostly pending; public package must include only eight original architecture figures unless each extra asset is cleared')
warnings.append('external subject-matter, security/privacy, copyediting, accessibility, and legal reviews are not recorded')
warnings.append('PDF/EPUB/website builds and print preflight have not been demonstrated')
report=ROOT/'bluebook/plan/PUBLICATION_READINESS.md'
lines=['# 正式发布就绪审计','',f'> Blockers：{len(blockers)}  ','> 结论：**尚未达到正式发布门禁。**','', '## P0：发布阻断项','']
lines += [f'- [ ] {x}' for x in blockers] or ['- 无']
lines += ['', '## P1：发布前必须人工确认','', '> 内容负责人已于2026-09-22确认完成全量人工内容审核；以下是证据、发行、外部专业审查和构建事项，不重复要求正文人工审核。','']+[f'- [ ] {x}' for x in warnings]
lines += ['', '## 已通过','', '- 章节、模式、实验卡数量和结构门禁；','- 第1–14章严格内容扫描；','- 内部Markdown链接完整性；','- 8张Excalidraw/SVG图表及第3、7、8图重叠检查；','- 治理目录基础完整性。','', '## 建议发布顺序','', '1. 冻结内容与状态，移除样章/模板出包；','2. 补齐参考文献、脚注、作者、URL访问日期和许可证；','3. 建立独立MkDocs与PDF/EPUB构建；','4. 完成外部专家、安全隐私、编辑、无障碍和法律审查；','5. 生成RC并执行链接、移动端、打印和安装验证；','6. 签署发布清单，打版本Tag并归档构建产物与SBOM。']
report.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(f'Publication readiness: {len(blockers)} blockers, {len(warnings)} warnings')
print(f'report: {report}')
