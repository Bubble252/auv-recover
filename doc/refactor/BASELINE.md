# auv-fault Refactor Baseline

**状态**：`REF_FAULT_BOOTSTRAP`<br>
**仓库**：`settled_容错`<br>
**基线 commit**：`571449a`<br>
**日期**：2026-11-13

## 1. 基线事实

该 commit 没有 `src/`、`tests/` 或 Python 项目配置，只有 AGENTS、README、Goal 模板和
research 空结构。因此不存在可回归的算法测试，也没有历史 artifact 或公共 Python API。
REF-FAULT 不是对旧实现的改写，而是按 G03 Step 4 建立一个最小、可测试的契约层。

## 2. 运行环境

```bash
cd /home/bubble/水下机器人/settled_容错/.worktrees/ref-fault-20261113
/home/bubble/水下机器人/.venv/bin/python -m pytest -q tests
```

`auv-core` 使用工作区根环境中的已安装版本；不在本仓库复制 core 源码，也不通过
`PYTHONPATH` 指向其他仓库的 `src`。

## 3. 初始检查

| 检查 | 命令 | 基线 |
|---|---|---|
| pytest | `/home/bubble/水下机器人/.venv/bin/python -m pytest -q tests` | 无测试文件（bootstrap） |
| ruff | `/home/bubble/水下机器人/.venv/bin/python -m ruff check src tests` | 无源码（bootstrap） |
| mypy | `/home/bubble/水下机器人/.venv/bin/python -m mypy` | 无源码（bootstrap） |
| shape | `总协调/scripts/check_code_shape.py --root . --check` | 无源码（bootstrap） |
| dependency | `scripts/check_repo_dependencies.py --root . --check` | PASS |

## 4. 已知风险

- 新增包是第一个正式 Python 实现，必须保持最小路径，不能复制局部规划器的训练、
  评价或历史 artifact 代码；
- 共享 `SafetyFilter`、`ControlProposal`、`SafetyContext`、`CapabilitySet` 和
  `SafeCommand` 只能来自已安装的 `auv-core`；
- 新增公共 API 需要测试和 `__all__` 声明；未验证的故障分类不写成冻结契约；
- 本仓库没有 remote 运行配置，pilot 不涉及服务器。

## 5. 回滚点

- 基线 commit：`571449a`；
- 候选失败时 `git revert <candidate-commit>`，不重置 main；
- 回滚后重新运行测试、ruff、mypy、shape 和依赖边界检查。
