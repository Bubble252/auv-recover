# auv-fault Inventory

**状态**：`REF_FAULT_BOOTSTRAP`<br>
**基线 commit**：`571449a`<br>
**日期**：2026-11-13

## 1. 盘点

| 对象 | 现状 |
|---|---|
| Python 源码 | 无 |
| Python 测试 | 无 |
| 公共 Python API | 无 |
| artifact / checkpoint | 无 |
| remote 运行配置 | 无 |

仓库当前只有治理和 research 结构，不能从旧代码中“去重”。REF-FAULT 只建立：

1. 故障信号数据结构；
2. 故障检测、注入和降级 Protocol；
3. 由检测器、降级策略和共享 `SafetyFilter` 组成的 supervisor；
4. 对应的小型测试。

## 2. 候选队列

| 优先级 | 候选 | 边界 | 状态 |
|---|---|---|---|
| P0 | FAULT-A1：最小故障契约和 supervisor | 只依赖 `auv-core` 契约；不实现训练/评价 | IN_PROGRESS |
| P1 | 具体故障注入器 | 需要新 Goal 和故障目录 | DEFERRED |
| P2 | 与规划器/控制器的集成 | 需要跨仓库契约评审 | DEFERRED |

## 3. 明确不做

- 不复制局部规划器的 reward、termination、success 或训练代码；
- 不读取历史 Goal artifact；
- 不定义未经验证的故障分类枚举；
- 不新增与 `SafetyFilter` 重复的接口。
