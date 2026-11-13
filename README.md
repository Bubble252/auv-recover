# settled_容错

独立 Git 仓库，负责容错、安全监督与降级策略。

当前包含最小故障契约层：

- `AGENTS.md`：仓库边界与规则；
- `doc/goals/GOAL_TEMPLATE.md`：最小 Goal 模板；
- `research/`：ledger、blocker、reading note 和 decision 的空结构。
- `src/auv_fault/`：故障信号、检测/注入/降级 Protocol 和安全监督组合；
- `tests/`：17 项契约、顺序、输入校验和导入边界测试。

运行：

```bash
uv venv .venv
uv pip install --python .venv/bin/python -e /home/bubble/水下机器人/settled_共享基础
uv pip install --python .venv/bin/python -e '.[dev]'
.venv/bin/python -m pytest -q tests
```

`refactor/fault-20261113` 分支尚未合入 `main`；详细基线、模块边界和等价性证据在
`doc/refactor/`。
