# auv-fault Module Map

**状态**：`REF_FAULT_COMPLETE`

| 模块路径 | 主要职责 | 非职责 | 公共 API | 对应测试 | Owner | Waiver |
|---|---|---|---|---|---|---|
| `src/auv_fault/interfaces.py` | 故障信号、检测/注入/降级 Protocol | 不实现具体故障目录或规划器 | `FaultSignal`, `FaultDetector`, `FaultInjector`, `DegradationPolicy` | `tests/test_fault_interfaces.py` | fault | 无 |
| `src/auv_fault/supervisor.py` | 组合检测、降级和共享安全过滤 | 不定义 success、reward 或训练 | `SafetySupervisor` | `tests/test_fault_supervisor.py` | fault | 无 |
| `src/auv_fault/__init__.py` | 稳定导出 | 不承载业务逻辑 | `__all__` | `tests/test_import_boundary.py` | fault | 无 |

## 边界

- 只允许依赖标准库、NumPy 和已安装的 `auv-core`；
- 不得导入 `auv_planner`、`auv_local`、`auv_lowlevel`、`auv_rl` 或外部仿真源码；
- `SafetyFilter`、`ControlProposal`、`SafetyContext`、`CapabilitySet`、`SafeCommand`
  以 `auv_core` 公共契约为准，不在本仓库复制；
- `supervisor` 只做组合和顺序调用，不改变 proposal 的 shape、单位或坐标系。
