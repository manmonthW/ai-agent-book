# P06 幂等副作用

> 状态：Release Candidate 1  
> 主要章节：第6、9、11章

## Context

Agent调用支付、退款、发送、删除、部署等写工具；网络可能超时，Worker可能重启，运行可能恢复。

## Problem

调用方无法仅凭超时判断副作用是否发生。盲目重试可能重复执行，不重试又可能漏执行。

## Forces

- 质量：业务动作必须准确执行一次；
- 延迟：状态查询增加一次往返；
- 成本：需要幂等记录和权威查询；
- 安全：Replay不能重复副作用；
- 运维：恢复过程必须可解释。

## Solution

使用稳定业务幂等键绑定主体、资源和已批准动作Digest。工具执行原子地保存键和结果；相同键重复调用返回原结果。超时后先查询幂等记录或权威业务状态，再决定是否重试。

```text
Checkpoint(intent + key)
→ Execute(key)
→ Persist result
→ Verify authoritative state
→ Checkpoint(completed)
```

## Consequences

### 收益

- 支持安全重试和进程恢复；
- 防止网络抖动造成重复动作；
- 提升审计和故障处理能力。

### 代价

- 需要业务级键设计和持久存储；
- 请求语义变化必须产生新键；
- 外部系统不支持幂等时需适配层或人工处置。

## Failure Modes

- 使用随机键，重试时键变化；
- 只按Run ID去重，无法表达业务动作；
- 相同键接受不同载荷；
- 把幂等误解为可撤销；
- 只记录请求，不验证最终状态。

## Implementation Sketch

```python
def execute(action, key):
    existing = store.get(key)
    if existing:
        assert existing.action_digest == digest(action)
        return existing.result
    result = provider.execute(action, idempotency_key=key)
    store.put_once(key, digest(action), result)
    return verifier.check(result)
```

## Evidence

- 蓝皮书章节：第6、9、11章；
- 实验卡：恢复、工具和生产实验按场景绑定；
- 外部标准：具体支付或消息系统的幂等契约需逐项核验。

## Exit Criteria

纯只读或数学计算没有外部副作用时无需业务幂等记录；仍需处理调用去重和资源预算。

## Checklist

- [ ] 键由业务语义稳定导出。
- [ ] 键绑定动作Digest。
- [ ] 工具可查询权威状态。
- [ ] 超时后先查状态再重试。
- [ ] 重复调用返回相同结果。
- [ ] 补偿与幂等分开设计。
