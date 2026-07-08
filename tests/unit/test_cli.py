"""CLI 入口测试。"""

from __future__ import annotations

import subprocess
import sys


def test_cli_version_prints_package_version() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "kaesi.cli", "--version"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "0.0.1" in result.stdout