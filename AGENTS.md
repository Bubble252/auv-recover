# settled_容错项目规则

本仓库是独立 Git 仓库 `/home/bubble/水下机器人/settled_容错`，默认分支 `main`，
当前不配置 remote，只承载容错、安全监督与降级策略。

## 边界

- 不修改其他仓库的训练、评价、reward、termination 或 artifact。
- 安全相关结论必须保留失败样本、触发条件和可复现命令。
- 新增 Goal 使用 `doc/goals/GOAL_TEMPLATE.md`，并包含 Research Contract。
- 与全局/局部规划器的接口以共享契约和显式版本为准，不直接导入其他仓库源码。
- 运行时代码只放在 `src/auv_fault/`；只依赖标准库、NumPy 和已安装的 `auv-core`。
- 不导入 `auv_planner`、`auv_local`、`auv_lowlevel` 或 `auv_rl`。

## 代码与测试

- 故障信号、检测/注入/降级接口在 `src/auv_fault/interfaces.py`；
- 安全监督组合在 `src/auv_fault/supervisor.py`；
- 模块边界以 `doc/refactor/MODULE_MAP.md` 为准；
- 本地验证使用仓库自己的 `.venv`：

```bash
.venv/bin/python -m pytest -q tests
.venv/bin/python -m ruff check src tests
.venv/bin/python -m ruff format --check src tests
.venv/bin/python -m mypy
```

## 治理入口

- 工作区规则：`/home/bubble/水下机器人/AGENTS.md`；
- canonical 代码规范：`/home/bubble/水下机器人/总协调/doc/governance/CODE_STYLE.md`；
- 接口与单位契约：`/home/bubble/水下机器人/总协调/doc/governance/CODE_INTERFACE_CONTRACT.md`；
- Goal / matrix / ledger schema：`/home/bubble/水下机器人/总协调/configs/governance/`。

本仓库当前没有正式 Goal 或 experiment matrix；新增时使用 canonical 模板和 schema，
不复制其他仓库的历史实验契约。

## 实验纪律

- 不把 smoke 写成正式结论；不把 `INVALID` 写成 `FAIL` 或 `PASS`。
- 触发 hard blocker 时按根目录 `AGENTS.md` 进入 autoresearch loop。
- 训练、评价和 artifact 规则沿用目标实验仓库的契约；本仓库不复制其历史数据。

## Git

- 禁止 `git add -A`；只添加本次相关路径。
- 提交前运行 `git diff --cached --check`。
- 不提交 `.venv/`、artifact、checkpoint、日志、缓存和大 PDF。
- 不自动 commit / push；push 必须由用户明确确认。
