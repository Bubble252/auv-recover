# auv-fault Equivalence Evidence

**状态**：`REF_FAULT_COMPLETE`<br>
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
baseline_commit: 80ca3ed
candidate_commit: cdb2bd8
files:
  - src/auv_fault/interfaces.py
  - src/auv_fault/supervisor.py
  - src/auv_fault/__init__.py
public_api_change: initial package
```

FAULT-A1 建立最小故障契约：

- `FaultSignal`：kind、severity、stamp；
- `FaultDetector.detect(context) -> FaultSignal | None`；`None` 明确表示无故障，
  不使用 `severity=0` 作为缺失值；
- `FaultInjector.inject(capability, signal) -> CapabilitySet`；
- `DegradationPolicy.degrade(proposal, signal) -> ControlProposal`；
- `SafetySupervisor.supervise(proposal, context)` 按“检测 -> 降级 -> 共享
  SafetyFilter”顺序执行，返回 `SafeCommand`。

## 2. 行为契约

| 项目 | 契约 | 证据 |
|---|---|---|
| 无故障 | detector 返回 `None`，跳过降级 | supervisor 顺序测试 |
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
.venv/bin/python -m pytest -q tests
.venv/bin/python -m ruff check src tests
.venv/bin/python -m ruff format --check src tests
.venv/bin/python -m mypy
.venv/bin/python /home/bubble/水下机器人/总协调/scripts/check_code_shape.py --root . --check
/home/bubble/水下机器人/.venv/bin/python \
  /home/bubble/水下机器人/scripts/check_repo_dependencies.py --root . --check
```

Preflight 证据：

```yaml
skill_usage:
  - skill: auv-refactor-guard
    phase: preflight
    outcome: passed
    repo: /home/bubble/水下机器人/settled_容错/.worktrees/ref-fault-20261113
    module: src/auv_fault
```

## 3. 结果

- 测试：`17 passed`；
- ruff：PASS；
- format：7 files already formatted；
- mypy：`Success: no issues found in 7 source files`；
- shape：`0 new violations, 0 suppressed`；
- dependency checker：`repository dependency boundaries: ok`；
- 安装 smoke：从 `/tmp` 导入 `auv_fault`，解析到本 worktree 的 `src/`；`auv_core`
  解析到共享基础仓库，未使用跨仓库 `PYTHONPATH`；
- 已知失败：无；
- 是否新增失败：`no`；
- 回滚 commit：`571449a`；
- 结论：`PASS`。

## 4. 人工检查

- [x] 没有修改 reward、termination、success、goal radius、seed split 或 held-out；
- [x] 没有移动或删除 artifact、checkpoint 或历史结果；
- [x] 没有复制局部规划器代码；
- [x] 只依赖 `auv-core` 公共契约，没有跨仓库源码导入；
- [x] supervisor 不读取时钟、不消耗 RNG、不持有模块级可变状态；
- [x] 只改一个仓库、一个候选。
