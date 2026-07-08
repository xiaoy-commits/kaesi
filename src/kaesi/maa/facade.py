"""MAA facade：对外暴露稳定的 Python 接口，内部按需调用 maafw。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class _MaaBackend(Protocol):
    """maafw 提供的最小子集，业务层只依赖此协议。"""

    def ping(self) -> bool: ...


@dataclass(frozen=True)
class MaaFacade:
    """MAA 访问门面。

    在生产路径中由 `get_facade()` 注入真实 maafw 后端；
    在单元测试中通过 `fake_maafw` fixture 注入假实现。
    """

    backend: _MaaBackend

    def is_alive(self) -> bool:
        """探测 MAA 运行时是否可用。"""
        return self.backend.ping()


_facade: MaaFacade | None = None


def get_facade() -> MaaFacade:
    """返回当前进程内的 MAA facade。

    首次调用时延迟加载 maafw；加载失败抛出 `MaaUnavailableError`。
    """
    global _facade
    if _facade is not None:
        return _facade

    try:
        import maafw  # type: ignore[import-not-found]  # noqa: F401
    except ImportError as exc:  # pragma: no cover - 仅在本机执行
        raise MaaUnavailableError("maafw 未安装，请运行 `just install`") from exc

    # 占位实现：后续 PR 替换为真实 maafw 接入
    _facade = MaaFacade(backend=_NullBackend())
    return _facade


class MaaUnavailableError(RuntimeError):
    """maafw 不可用时抛出。"""


class _NullBackend:
    """占位后端：返回 False，便于 init 阶段不依赖真实 maafw。"""

    def ping(self) -> bool:
        return False