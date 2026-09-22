#!/usr/bin/env python3
"""Generate eight polished, editable Excalidraw architecture figures and SVG previews."""
from __future__ import annotations
import html,json,subprocess
from pathlib import Path
ROOT=Path.cwd(); OUT=ROOT/"bluebook/images/architecture"; OUT.mkdir(parents=True,exist_ok=True)
P={"navy":"#172B4D","slate":"#42526E","muted":"#6B778C","line":"#B3BAC5","paper":"#FFFFFF","canvas":"#F7F8FA","blue":"#DEEBFF","blueS":"#4C9AFF","purple":"#EAE6FF","purpleS":"#6554C0","green":"#E3FCEF","greenS":"#00875A","amber":"#FFF0B3","amberS":"#FF991F","red":"#FFEBE6","redS":"#DE350B","teal":"#E6FCFF","tealS":"#00A3BF","gray":"#EBECF0"}; NOW=1789948800000

def b(i,t,x,y,w,h,sc=P["navy"],bg="transparent",style="solid",sw=2,rough=1,roundness=None): return {"id":i,"type":t,"x":x,"y":y,"width":w,"height":h,"angle":0,"strokeColor":sc,"backgroundColor":bg,"fillStyle":"solid","strokeWidth":sw,"strokeStyle":style,"roughness":rough,"opacity":100,"groupIds":[],"frameId":None,"index":i,"roundness":roundness,"seed":abs(hash(i))%99991+1,"version":1,"versionNonce":abs(hash(i+'v'))%99991+1,"isDeleted":False,"boundElements":None,"updated":NOW,"link":None,"locked":False}
def rect(i,x,y,w,h,label,bg=P["paper"],sc=P["navy"],fs=18,style="solid",sw=2):
 e=b(i,"rectangle",x,y,w,h,sc,bg,style,sw,1,{"type":3});e.update(text=label,fontSize=fs,fontFamily=5,textAlign="center",verticalAlign="middle");return e
def txt(i,x,y,s,fs=18,c=P["navy"],bold=False):
 ls=s.split('\n');e=b(i,"text",x,y,max(map(len,ls))*fs*.72,len(ls)*fs*1.3,c,sw=1,rough=0);e.update(text=s,fontSize=fs,fontFamily=5,textAlign="left",verticalAlign="top",originalText=s,lineHeight=1.25,bold=bold);return e
def arr(i,x,y,pts,style="solid",c=P["slate"],sw=2,end="arrow"):
 xs=[p[0] for p in pts];ys=[p[1] for p in pts];e=b(i,"arrow",x,y,max(xs)-min(xs),max(ys)-min(ys),c,style=style,sw=sw,rough=1,roundness={"type":2});e.update(points=pts,startBinding=None,endBinding=None,startArrowhead=None,endArrowhead=end,elbowed=False);return e
def line(i,x,y,pts,style="solid",c=P["line"],sw=2):
 xs=[p[0] for p in pts];ys=[p[1] for p in pts];e=b(i,"line",x,y,max(xs)-min(xs),max(ys)-min(ys),c,style=style,sw=sw,rough=0);e.update(points=pts,startBinding=None,endBinding=None);return e
def header(n,title,sub): return [txt("eyebrow",64,34,f"BLUEBOOK  /  CHAPTER {n:02d}",15,P["blueS"]),txt("title",64,66,title,31,P["navy"],True),txt("sub",66,112,sub,17,P["muted"]),line("hr",64,154,[[0,0],[1272,0]],c=P["gray"],sw=2)]
def export(name,els,w=1400,h=900):
 data={"type":"excalidraw","version":2,"source":"https://excalidraw.com","elements":els,"appState":{"viewBackgroundColor":P["canvas"],"gridSize":20,"name":name},"files":{}};(OUT/f"{name}.excalidraw").write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8");(OUT/f"{name}.svg").write_text(svg(name,els,w,h),encoding="utf-8");subprocess.run(["rsvg-convert",str(OUT/f"{name}.svg"),"-o",str(OUT/f"{name}.png")],check=True)
def svg(name,els,w,h):
 z=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d"><title id="t">{html.escape(name)}</title><desc id="d">AI Agent蓝皮书架构概念图，可编辑源为Excalidraw。</desc><defs><filter id="shadow"><feDropShadow dx="0" dy="5" stdDeviation="7" flood-color="#172B4D" flood-opacity=".10"/></filter><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0 0L0 6L9 3z" fill="#42526E"/></marker></defs><rect width="100%" height="100%" fill="{P["canvas"]}"/>']
 for e in els:
  x,y=e['x'],e['y'];dash=' stroke-dasharray="9 7"' if e.get('strokeStyle')=='dashed' else ''
  if e['type']=='rectangle':z.append(f'<rect x="{x}" y="{y}" width="{e["width"]}" height="{e["height"]}" rx="14" fill="{e["backgroundColor"]}" stroke="{e["strokeColor"]}" stroke-width="{e["strokeWidth"]}"{dash} filter="url(#shadow)"/>');center(z,e)
  elif e['type']=='text':labels(z,e)
  elif e['type'] in ('arrow','line'):
   pts=' '.join(f'{x+p[0]},{y+p[1]}' for p in e['points']);mk=' marker-end="url(#arrow)"' if e['type']=='arrow' and e.get('endArrowhead') else '';z.append(f'<polyline points="{pts}" fill="none" stroke="{e["strokeColor"]}" stroke-width="{e["strokeWidth"]}"{dash}{mk}/>')
 z.append('</svg>');return '\n'.join(z)
def center(z,e):
 ls=e.get('text','').split('\n');fs=e.get('fontSize',18);cy=e['y']+e['height']/2-(len(ls)-1)*fs*.64
 for j,s in enumerate(ls):z.append(f'<text x="{e["x"]+e["width"]/2}" y="{cy+j*fs*1.28}" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="{fs}" fill="{e["strokeColor"]}">{html.escape(s)}</text>')
def labels(z,e):
 fs=e['fontSize'];weight='700' if e.get('bold') or fs>=28 else '500'
 for j,s in enumerate(e['text'].split('\n')):z.append(f'<text x="{e["x"]}" y="{e["y"]+fs+j*fs*1.25}" font-family="Inter,Arial,sans-serif" font-size="{fs}" font-weight="{weight}" fill="{e["strokeColor"]}">{html.escape(s)}</text>')

def f1():
 e=header(1,"Agent边界与反馈闭环","模型提出候选，Harness守住权力边界，环境反馈决定下一步")
 e += [rect("agent",70,190,860,540,"",P["paper"],P["line"]),txt("agentlab",100,215,"AGENT  /  DECISION SPACE",15,P["muted"]),rect("model",185,285,350,155,"MODEL\n理解语义 · 生成候选",P["purple"],P["purpleS"],21),rect("harness",185,515,620,155,"HARNESS\nContext · State · Tools\nPolicy · Budget · Verify",P["blue"],P["blueS"],20),arr("mh",360,440,[[0,0],[0,75]]),txt("proposal",380,462,"typed proposal",15,P["muted"]),rect("env",1020,285,310,350,"ENVIRONMENT\n\nUser · Files · DB\nWeb · Devices",P["green"],P["greenS"],21),arr("action",805,545,[[0,0],[170,0],[170,-95],[215,-95]]),arr("obs",1020,600,[[0,0],[-65,0],[-65,40],[-215,40]]),txt("act",840,505,"ACTION",14,P["amberS"]),txt("ob",840,652,"OBSERVATION",14,P["greenS"]),rect("guard",570,285,235,155,"控制面\n身份 · 权限\n副作用 · 审计",P["amber"],P["amberS"],18),rect("rule",245,770,900,72,"模型影响决策，但不能自行授予权限或宣告环境成功",P["red"],P["redS"],20)];export("fig01-agent-boundary-loop",e)
def f2():
 e=header(2,"最低充分自主性阶梯","每升一级，都必须带来可测的新能力，并付出更强控制成本")
 items=[("01","确定性代码","规则覆盖",P["green"],P["greenS"]),("02","结构化调用","语义转换",P["teal"],P["tealS"]),("03","RAG调用","外部事实",P["blue"],P["blueS"]),("04","条件Workflow","路径已知",P["blue"],P["blueS"]),("05","有界工具Agent","路径开放",P["amber"],P["amberS"]),("06","Orchestrator\nHandoff","并行 · 隔离",P["purple"],P["purpleS"])]
 for i,(num,name,why,bg,sc) in enumerate(items):
  x=60+i*220;y=570-i*62;e += [rect(f"card{i}",x,y,185,155,"",bg,sc),txt(f"num{i}",x+18,y+14,num,15,sc),txt(f"name{i}",x+18,y+48,name,18,P["navy"],True),txt(f"why{i}",x+18,y+92+12*name.count('\n'),f"升级证据\n{why}",15,P["slate"])]
  if i:e.append(arr(f"a{i}",x-34,y+112,[[0,0],[34,-20]],c=P["muted"]))
 e += [arr("axis",75,800,[[0,0],[1220,-345]],style="dashed",c=P["line"]),txt("low",65,825,"更确定 · 更易验证",16,P["greenS"]),txt("high",1150,505,"更自主 · 更高控制成本",16,P["purpleS"]),rect("gate",865,750,445,70,"无增量证据  →  停在当前层级",P["red"],P["redS"],20)];export("fig02-autonomy-ladder",e)
def f3():
 e=header(3,"统一执行图","主路径清晰，等待与恢复是显式分支，状态贯穿每一个节点")
 cards=[("INPUT","输入",P["gray"],P["slate"]),("ROUTE","程序",P["green"],P["greenS"]),("PLAN","模型",P["purple"],P["purpleS"]),("EXECUTE","工具",P["blue"],P["blueS"]),("VERIFY","程序",P["green"],P["greenS"]),("TERMINAL","终态",P["gray"],P["slate"])]
 for i,(a,c,bg,sc) in enumerate(cards):
  x=45+i*225;e += [rect(f"n{i}",x,265,180,100,f"{a}\n{c}",bg,sc,18)]
  if i:e.append(arr(f"a{i}",x-45,315,[[0,0],[45,0]]))
 e += [rect("wait",485,485,260,110,"WAIT / APPROVAL\n人工 · 事件",P["amber"],P["amberS"],19),rect("recover",825,485,260,110,"RECOVER / RETRY\n分类错误 · 有界重试",P["red"],P["redS"],18),arr("w1",740,365,[[0,0],[0,75],[-125,75],[-125,120]]),arr("w2",745,540,[[0,0],[40,0],[40,-175]]),arr("r1",1035,365,[[0,0],[0,75],[-80,75],[-80,120]]),arr("r2",955,595,[[0,0],[0,55],[-483,55],[-483,-175],[-370,-175],[-370,-230]],style="dashed"),rect("rail",185,710,1030,82,"TYPED STATE  ·  CHECKPOINT  ·  BUDGET  ·  CANCELLATION  ·  TRACE",P["blue"],P["blueS"],20)];export("fig03-unified-execution-graph",e)
def f4():
 e=header(4,"上下文生命周期","信息进入决策前被筛选，决策之后被丢弃、提炼、摘要或外置")
 inputs=[("稳定前缀","Policy · Tools",P["blue"],P["blueS"]),("目标","Goal",P["green"],P["greenS"]),("类型化状态","State",P["teal"],P["tealS"]),("证据","Sources",P["amber"],P["amberS"]),("相关轨迹","Trajectory",P["purple"],P["purpleS"])]
 for i,(a,c,bg,sc) in enumerate(inputs):e.append(rect(f"i{i}",45+i*266,210,230,92,f"{a}\n{c}",bg,sc,17))
 e += [line(f"fd{i}",160+i*266,302,[[0,0],[0,52]]) for i in range(5)]
 e += [line("fbar",160,354,[[0,0],[1064,0]]),arr("fdown",700,354,[[0,0],[0,66]]),rect("decision",495,420,410,105,"MODEL DECISION\n最小充分上下文",P["purple"],P["purpleS"],21),line("odown",700,525,[[0,0],[0,35]]),line("obar",197.5,560,[[0,0],[1005,0]])]
 e += [arr(f"oa{i}",197.5+i*335,560,[[0,0],[0,40]]) for i in range(4)]
 outs=[("DROP","删除噪声"),("EXTRACT","结构化事实"),("SUMMARIZE","可恢复摘要"),("EXTERNALIZE","Artifact + URI")]
 for i,(a,c) in enumerate(outs):e.append(rect(f"o{i}",55+i*335,600,285,105,f"{a}\n{c}",P["paper"],P["slate"],18))
 risks=[("污染","Poisoning"),("分散","Distraction"),("混淆","Confusion"),("冲突","Clash")]
 for i,(a,c) in enumerate(risks):e.append(rect(f"r{i}",55+i*335,755,285,70,f"⚠  {a} / {c}",P["red"],P["redS"],16,style="dashed"))
 export("fig04-context-lifecycle",e)
def f5():
 e=header(5,"知识、记忆与状态边界","把“当前看见什么”“系统知道什么”“长期记住什么”彻底分开")
 e += [rect("context",490,205,420,105,"CURRENT CONTEXT\n当前决策的工作台",P["purple"],P["purpleS"],21),rect("kb",990,205,340,135,"KNOWLEDGE BASE\n权威来源 · ACL · Provenance",P["blue"],P["blueS"],18),rect("state",70,400,340,125,"RUNTIME STATE\n当前运行 · Durable · Typed",P["green"],P["greenS"],18),rect("mem",515,400,370,135,"GOVERNED MEMORY\nExtract · Validate · Confirm",P["amber"],P["amberS"],18),rect("art",990,400,340,135,"ARTIFACT STORE\nURI · Hash · ACL · Lifecycle",P["teal"],P["tealS"],18),rect("events",70,650,340,105,"EVENTS\nUser · Queue · Webhook",P["gray"],P["slate"],18)]
 e += [arr("retr",990,270,[ [0,0],[-80,0] ]),txt("retrt",915,238,"RETRIEVE",12,P["blueS"]),arr("statectx",410,460,[[0,0],[105,-155]]),arr("memctx",700,400,[[0,0],[0,-90]]),arr("eventstate",240,650,[[0,0],[0,-125]]),arr("artctx",990,470,[[0,0],[-80,-165]]),txt("refs",952,368,"REFERENCE",12,P["tealS"]),rect("note",335,790,730,65,"Memory ≠ 权威数据库    ·    Artifact ≠ 上下文副本",P["red"],P["redS"],19)];export("fig05-knowledge-memory-boundaries",e)
def f6():
 e=header(6,"工具执行与协议边界","从模型候选到环境副作用，每一步都经过可验证的控制关卡")
 stages=[("1","MODEL","候选",P["purple"],P["purpleS"]),("2","SCHEMA","结构",P["gray"],P["slate"]),("3","AUTH / POLICY","授权",P["red"],P["redS"]),("4","APPROVAL","准确载荷",P["amber"],P["amberS"]),("5","TOOL GATEWAY","幂等执行",P["blue"],P["blueS"]),("6","ENVIRONMENT","状态验证",P["green"],P["greenS"])]
 for i,(n,a,c,bg,sc) in enumerate(stages):
  x=40+i*226;e += [rect(f"s{i}",x,250,185,125,"",bg,sc),txt(f"no{i}",x+14,263,n,14,sc),txt(f"a{i}",x+16,300,a,17,P["navy"],True),txt(f"c{i}",x+16,335,c,15,P["slate"])]
  if i:e.append(arr(f"ar{i}",x-41,312,[[0,0],[41,0]]))
 e += [rect("interop",690,515,610,145,"INTEROPERABILITY  /  互操作层\nMCP · API · Actor\nA2A：Agent间任务与消息",P["teal"],P["tealS"],20,style="dashed"),arr("down",1010,375,[[0,0],[0,140]],style="dashed",c=P["tealS"]),rect("truth",240,735,920,75,"协议回答“如何连接”    ｜    策略网关回答“是否允许”",P["amber"],P["amberS"],21)];export("fig06-tool-protocol-boundary",e)
def f7():
 e=header(7,"Coding Agent验证闭环","每次失败都带来新证据；测试通过和Artifact可打开才算完成")
 stages=[("需求","Contract",P["gray"],P["slate"]),("搜索","Search",P["blue"],P["blueS"]),("读取","Read",P["blue"],P["blueS"]),("补丁","Patch",P["amber"],P["amberS"]),("测试 / 渲染","Evidence",P["green"],P["greenS"]),("诊断","Diagnose",P["red"],P["redS"])]
 for i,(a,c,bg,sc) in enumerate(stages):
  x=40+i*225;e.append(rect(f"s{i}",x,250,185,105,f"{a}\n{c}",bg,sc,18));
  if i:e.append(arr(f"a{i}",x-40,302,[[0,0],[40,0]]))
 e += [arr("loop",1257,250,[[0,0],[0,-45],[-450,-45],[-450,0]],style="dashed",c=P["redS"]),txt("fix",915,168,"FIX WITH NEW EVIDENCE",14,P["redS"]),rect("verify",425,665,300,100,"VERIFY\n验收条件 · Diff",P["green"],P["greenS"],20),rect("done",930,665,300,100,"DONE\nArtifact可重新打开",P["purple"],P["purpleS"],20),arr("vd",725,715,[[0,0],[205,0]]),arr("tv",1032,355,[[0,0],[0,155],[-457,155],[-457,310]]),rect("rail",180,810,1040,55,"ISOLATED WORKSPACE  ·  SANDBOX  ·  ARTIFACT  ·  TRACE",P["gray"],P["slate"],17)];export("fig07-coding-agent-loop",e)
def f8():
 e=header(8,"模态 × 时序与公共控制原语","模态不同，控制原语相同：可唤醒、可暂停、可取消、可验证")
 cols=[("SYNC","同步"),("REALTIME","实时"),("ASYNC / LONG","异步 / 长期")];rows=[("TEXT / API",P["blue"],P["blueS"]),("VOICE",P["purple"],P["purpleS"]),("GUI",P["amber"],P["amberS"]),("PHYSICAL",P["green"],P["greenS"])];cells=[["对话\nTool Call","流式文本","邮件\n队列任务"],["语音问答","双向通话\n打断","留言\n回拨"],["单步操作","屏幕协作","长流程\n网页任务"],["设备命令","机器人\n闭环","巡检\n持续任务"]]
 x0,y0,cw,rh=350,205,315,112
 for j,(a,c) in enumerate(cols):e.append(rect(f"c{j}",x0+j*cw,y0,cw-15,72,f"{a}\n{c}",P["gray"],P["slate"],17))
 for i,(r,bg,sc) in enumerate(rows):
  e.append(rect(f"r{i}",55,y0+88+i*rh,250,rh-14,r,bg,sc,18))
  for j in range(3):e.append(rect(f"m{i}{j}",x0+j*cw,y0+88+i*rh,cw-15,rh-14,cells[i][j],P["paper"],P["slate"],17))
 controls=[("WAKE",P["blue"]),("CHECKPOINT",P["teal"]),("SAFE POINT",P["green"]),("CANCEL",P["red"]),("PREEMPT",P["amber"]),("BACKPRESSURE",P["purple"]),("VERIFY",P["green"])]
 for i,(c,bg) in enumerate(controls):e.append(rect(f"p{i}",55+i*176.7,785,165,62,c,bg,P["slate"],13))
 e += [arr("time1",657,241,[[0,0],[8,0]],c=P["muted"]),arr("time2",972,241,[[0,0],[8,0]],c=P["muted"])]
 export("fig08-modality-time-control",e)
if __name__=='__main__':
 for fn in (f1,f2,f3,f4,f5,f6,f7,f8):fn()
 print('generated 8 polished Excalidraw sources + SVG + PNG previews')
