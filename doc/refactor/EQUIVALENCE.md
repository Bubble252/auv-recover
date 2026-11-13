# auv-fault Equivalence Evidence

**状态**：`REF_FAULT_BOOTSTRAP`<br>
**仓库**：`settled_容错`<br>
**基线 commit**：`571449a`<br>
**日期**：2026-11-13

## 1. 候选 FAULT-A1

```yaml
goal: META-G03
candidate: FAULT-A1
repository: settled_容错
base_commit: 571449a
branch: refactor/fault-20261113
files:
  - src/auv_fault/interfaces.py
  - src/auv_fault/supervisor.py
  - src/auv_fault/__init__.py
public_api_change: initial package
```

FAULT-A1 建立最小故障契约：

- `FaultSignal`：kind、severity、stamp；
- `FaultDetector.detect(context) -> FaultSignal`；
- `FaultInjector.inject(capability, signal) -> CapabilitySet`；
- `DegradationPolicy.degrade(proposal, signal) -> ControlProposal`；
- `SafetySupervisor.supervise(proposal, context)` 按“检测 -> 降级 -> 共享
  SafetyFilter”顺序执行，返回 `SafeCommand`。

## 2. 行为契约

| 项目 | 契约 | 证据 |
|---|---|---|
| 故障严重度 | finite，范围为 `[0, 1]` | 数据类负控 |
| 时间 | finite、非负秒 | 数据类负控 |
| supervisor 顺序 | 检测、降级、过滤 | spy 测试 |
| context | detector 和 filter 接收原始 context | spy 测试 |
| proposal | 降级后的对象传给 filter | 对象身份测试 |
| RNG/全局状态 | 不消耗、不修改 | 纯组合测试 |
| 外部依赖 | 只导入 `auv_core` | import guard / dependency checker |

验证命令：

```bash
cd /home/bubble/水下机器人/settled_容错/.worktrees/ref-fault-20261113
/home/bubble/水下机器人/.venv/bin/python -m pytest -q tests
```

- 结果：`PENDING`
