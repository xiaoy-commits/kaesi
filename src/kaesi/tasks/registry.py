"""任务注册表：集中管理所有可执行任务。"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable


@dataclass(frozen=True)
class TaskSpec:
    """单个任务的不可变描述。"""

    name: str
    description: str


@dataclass
class TaskRegistry:
    """任务注册表。"""

    _specs: dict[str, TaskSpec] = field(default_factory=dict)

    def register(self, spec: TaskSpec) -> None:
        if spec.name in self._specs:
            raise ValueError(f"任务重复注册：{spec.name}")
        self._specs[spec.name] = spec

    def names(self) -> list[str]:
        return sorted(self._specs)

    def get(self, name: str) -> TaskSpec | None:
        return self._specs.get(name)


_registry: TaskRegistry | None = None


def get_registry() -> TaskRegistry:
    """返回进程内单例的 `TaskRegistry`。"""
    global _registry
    if _registry is None:
        _registry = TaskRegistry()
    return _registry


def register_task(name: str, description: str = "") -> Callable[[TaskSpec], TaskSpec]:
    """装饰器：将函数所属任务注册到全局表。"""

    def decorator(spec: TaskSpec) -> TaskSpec:
        get_registry().register(spec)
        return spec

    # 简化形式：直接接收 name/description 构造 spec
    return decorator