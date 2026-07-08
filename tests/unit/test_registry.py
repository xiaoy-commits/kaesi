"""任务注册表测试。"""

from __future__ import annotations

from kaesi.tasks import TaskRegistry, TaskSpec


def test_register_and_lookup() -> None:
    reg = TaskRegistry()
    reg.register(TaskSpec(name="daily.claim", description="领奖"))
    assert reg.get("daily.claim") is not None
    assert reg.names() == ["daily.claim"]


def test_duplicate_register_raises() -> None:
    reg = TaskRegistry()
    reg.register(TaskSpec(name="x", description=""))
    try:
        reg.register(TaskSpec(name="x", description=""))
    except ValueError:
        return
    raise AssertionError("重复注册应抛出 ValueError")