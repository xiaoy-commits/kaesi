"""测试用 maafw 假后端。"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class FakeMaaBackend:
    """可在测试中控制 ping 行为的假后端。"""

    alive: bool = True
    ping_calls: int = 0
    script_path: str | None = field(default=None)

    def ping(self) -> bool:
        self.ping_calls += 1
        return self.alive