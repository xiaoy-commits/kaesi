"""全局 pytest 配置。"""

from __future__ import annotations

import pytest


@pytest.fixture
def fake_maafw():
    """提供假 maafw 后端，避免单元测试依赖真实 MAA 运行时。"""
    from tests.fixtures.fake_maafw import FakeMaaBackend

    return FakeMaaBackend()