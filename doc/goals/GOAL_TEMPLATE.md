# GoalXX：<一句话目标>

**日期**：YYYY-MM-DD<br>
**状态**：`DRAFT_FOR_APPROVAL`

## Research Contract

```yaml
autoresearch:
  required: true
  triggers:
    - gate_fail_twice
    - no_metric_movement_after_3_fixes
    - heldout_collapse
    - seed_noise_ambiguous
  ledger: research/LEDGER.jsonl
  blockers_dir: research/blockers/
  reading_dir: research/paper_reading/
  max_outer_loops: 3
  check_command: python ../scripts/check_research_ledger.py --goal GoalXX --goal-doc doc/goals/<this_file>.md --strict
```

## 1. 背景与问题

- 上游结果：
- 当前安全/容错问题：
- 为什么现在做：

## 2. 假设

至少写两个可证伪 hypothesis：

1. H1：
2. H2：

## 3. 方法

- 故障模型：
- 检测 / 监督 / 降级策略：
- 与现有模块的关系：

## 4. 执行计划

- [ ] Step 0：只读盘点与契约确认；
- [ ] Step 1：实现；
- [ ] Step 2：smoke 与负控；
- [ ] Step 3：正式实验；
- [ ] Step 4：Gate；
- [ ] Step 5：result、ledger、commit / push。

## 5. Gate

| check | 阈值 | 失败标签 |
|---|---:|---|
| | | |

## 6. Git

禁止 `git add -A`。提交前运行 `git diff --cached --check`；不自动 push。
