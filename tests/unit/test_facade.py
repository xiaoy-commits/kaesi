"""MaaFacade 行为测试。"""

from __future__ import annotations

from kaesi.maa import MaaFacade


def test_facade_reports_alive_when_backend_pings(fake_maafw) -> None:
    facade = MaaFacade(backend=fake_maafw)
    assert facade.is_alive() is True
    assert fake_maafw.ping_calls == 1


def test_facade_reports_dead_when_backend_down(fake_maafw) -> None:
    fake_maafw.alive = False
    facade = MaaFacade(backend=fake_maafw)
    assert facade.is_alive() is False