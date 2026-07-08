"""kaesi CLI 入口。"""

from __future__ import annotations

import argparse
import sys
from typing import Sequence


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kaesi",
        description="本地自用的卡厄思梦境辅助脚本",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="打印版本并退出",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.version:
        from kaesi import __version__

        print(__version__)
        return 0
    print("kaesi: 暂无任务注册。请通过后续 PR 添加任务。", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())