# auv-fault Inventory

**状态**：`REF_FAULT_COMPLETE`<br>
**基线 commit**：`571449a`<br>
**日期**：2026-11-13

## 1. 盘点

| 对象 | 现状 |
|---|---|
| Python 源码 | 3 个模块：契约、supervisor、稳定导出 |
| Python 测试 | 4 个测试模块，17 项测试 |
| 公共 Python API | `FaultSignal`、3 个 Protocol、`SafetySupervisor` |
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
| P0 | FAULT-A1：最小故障契约和 supervisor | 只依赖 `auv-core` 契约；不实现训练/评价 | PASS |
| P1 | 具体故障注入器 | 需要新 Goal 和故障目录 | DEFERRED |
| P2 | 与规划器/控制器的集成 | 需要跨仓库契约评审 | DEFERRED |

## 3. 明确不做

- 不复制局部规划器的 reward、termination、success 或训练代码；
- 不读取历史 Goal artifact；
- 不定义未经验证的故障分类枚举；
- 不新增与 `SafetyFilter` 重复的接口。

## 4. G03 最终验证与 G04 交接

最终验证：

| 检查 | 结果 |
|---|---|
| pytest | `17 passed` |
| ruff | PASS |
| format | 7 files already formatted |
| mypy | 7 source files PASS |
| shape | `0 new / 0 suppressed` |
| dependency | PASS |

| 级别 | 候选 | 证伪条件 | 边界 |
|---|---|---|---|
| L0 | 对候选 diff 运行 ruff import 排序/format | 非格式 diff、lint 失败或测试回退 | 可在 shadow 后自动写入 |
| L1 | 只有在出现第二个真实实现时，才把共同调用顺序抽成无状态组合 helper | 只有一个实现、helper 增加转发层或改变 detector/filter 调用顺序 | 人工批准，禁止提前造抽象 |

禁止自动修改：`FaultSignal` 公共字段、三个 Protocol 签名、`SafetySupervisor`
调用顺序、`auv_core` 契约、故障分类和 severity 语义。新增具体故障目录必须先有
真实场景、测试和独立 Goal。

允许修改目录是 `src/auv_fault/`、`tests/`、`doc/refactor/`；禁止 `artifacts/`、
`outputs/`、`checkpoints/`、历史 Goal 数据和外部仿真源码。G04 shadow 只读，
不得自动扩大公共 API。
