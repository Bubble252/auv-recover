from __future__ import annotations

import ast
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[1] / "src" / "auv_fault"
ALLOWED_ROOTS = {"__future__", "dataclasses", "math", "typing", "auv_core", "auv_fault"}
FORBIDDEN_ROOTS = {"auv_local", "auv_lowlevel", "auv_planner", "auv_rl"}


def test_source_imports_stay_inside_declared_boundary() -> None:
    violations: list[str] = []

    for path in sorted(SRC_ROOT.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                roots = [alias.name.split(".", 1)[0] for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                roots = [node.module.split(".", 1)[0]]
            else:
                continue
            for root in roots:
                if root in FORBIDDEN_ROOTS or root not in ALLOWED_ROOTS:
                    violations.append(f"{path.name}: {root}")

    assert violations == []
