# Spec & Repo Init Implementation Plan

> **For agentic workers:** 步骤使用复选框（`- [ ]`）语法进行跟踪。

**Goal:** 固化 `AGENTS.md` 的项目定位与技术栈，并搭建 Python 包 + 测试 + lint + 任务的最小仓库骨架，使后续 PR（`#3` MaaFramework 接入骨架、`#4` 最小任务模板）能在已就绪的工程上增量推进。

**Architecture:**
1. 根 `AGENTS.md` 把项目定位、命令、架构边界、测试约束等稳定事实填实，移除所有 `...` 占位。
2. 仓库采用 `src/` 布局：`src/kaesi/` 为业务包，`src/kaesi/maa/` 封装 `maafw`（业务层不直接 import），`src/kaesi/tasks/` 提供 `TaskRegistry`。
3. 工程命令由 `justfile` 统一入口；CI 路径不安装 `maafw`，通过 `tests/fixtures/fake_maafw.py` 完成单元测试。

**Tech Stack:** Python 3.11+、`maafw`（本机）、`pytest` + `pytest-cov`、`ruff`、`mypy`、`pre-commit`、`justfile`。

---

## 文件结构

将创建或修改的文件：

- 修改：`AGENTS.md`：填实项目定位、命令、架构边界、测试约束等占位。
- 修改：`.gitignore`：屏蔽构建产物、venv、`resource/` 运行时缓存。
- 新建：`pyproject.toml`：包元数据、依赖、可选 `dev` extras、`[project.scripts]`。
- 新建：`justfile`：开发命令统一入口。
- 新建：`.pre-commit-config.yaml`：本地钩子（ruff + 通用检查）。
- 新建：`README.md`：项目说明与快速开始。
- 新建：`src/kaesi/__init__.py`：版本常量。
- 新建：`src/kaesi/cli.py`：CLI 入口，`--version` 与占位默认行为。
- 新建：`src/kaesi/maa/__init__.py`：导出 `MaaFacade` 与 `get_facade`。
- 新建：`src/kaesi/maa/facade.py`：定义 `_MaaBackend` 协议、`MaaFacade`、`get_facade`、`MaaUnavailableError`、`_NullBackend`。
- 新建：`src/kaesi/tasks/__init__.py`：导出 `TaskRegistry` 与 `get_registry`。
- 新建：`src/kaesi/tasks/registry.py`：`TaskSpec`、`TaskRegistry`、`get_registry`。
- 新建：`tests/__init__.py`、`tests/conftest.py`、`tests/fixtures/__init__.py`、`tests/fixtures/fake_maafw.py`：测试基础。
- 新建：`tests/unit/test_cli.py`、`tests/unit/test_facade.py`、`tests/unit/test_registry.py`：单元测试。
- 新建：`docs/harness/plans/2026-07-08-spec-and-init-plan.md`：本计划文件。

---

## 任务结构

### 任务 1：根 `AGENTS.md` 稳定事实填实

**文件：**
- 修改：`AGENTS.md`

- [ ] **步骤 1：填实「项目定位」段**

将 `项目定位：...`、`核心技术栈：...`、`关键入口：...` 替换为：

```markdown
- 项目定位：`kaesi` 是「卡厄思梦境」手游的本地自用辅助脚本，使用 `MaaFramework` 的 Python 绑定 (`maafw`) 作为图像识别与原生交互底座，业务逻辑由 Python 编排。
- 核心技术栈：Python 3.11+ / `maafw` / `pydantic` / `pytest` / `pre-commit` / `ruff` / `justfile`。
- 关键入口：`src/kaesi/`（业务包）、`src/kaesi/cli.py`（CLI 入口）、`resource/`（MAA 模板与 pipeline）。
```

- [ ] **步骤 2：填实「命令」「架构边界」「测试约束」「环境与初始化」段**

按上述完整内容填写，每段使用 `@<文件>` 指向真实来源而非复制命令清单。

- [ ] **步骤 3：填实「Repo etiquette」「Review guidelines」段**

明确 Conventional Commits、云端审查支持 = 是、默认审查者 = `chatgpt-codex-connector[bot] / 本地 reviewer`。

- [ ] **步骤 4：替换「地图 MAP」中的目录树占位**

```markdown
目录树 tree : `@.oh-my-harness/tree.md`

```text
.
├── src/
│   └── kaesi/
│       ├── maa/
│       ├── tasks/
│       └── cli.py
├── resource/
├── tests/
├── docs/
│   └── harness/
│       └── plans/
└── tools/
```
```

- [ ] **步骤 5：提交**

```bash
git add AGENTS.md
git commit -m "spec(agents): fill in project facts and boundaries"
```

### 任务 2：仓库配置基线（gitignore + pyproject + justfile + pre-commit）

**文件：**
- 新建：`.gitignore`
- 新建：`pyproject.toml`
- 新建：`justfile`
- 新建：`.pre-commit-config.yaml`

- [ ] **步骤 1：编写 `.gitignore`**

```gitignore
# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.venv/

# Coverage / test
.coverage
.coverage.*
htmlcov/
.pytest_cache/
.mypy_cache/
.ruff_cache/

# Editor
.idea/
.vscode/

# OS
.DS_Store
Thumbs.db

# MAA 资源（用户本机维护，不进仓库）
resource/cache/
resource/runtime/
```

- [ ] **步骤 2：编写 `pyproject.toml`**

```toml
[build-system]
requires = ["hatchling>=1.21"]
build-backend = "hatchling.build"

[project]
name = "kaesi"
version = "0.0.1"
description = "本地自用的卡厄思梦境辅助脚本（MaaFramework + Python）"
readme = "README.md"
requires-python = ">=3.11"
license = { text = "MIT" }
authors = [{ name = "kaesi maintainers" }]
dependencies = [
    "maafw>=1.0",
    "pydantic>=2.6",
    "tomli>=2.0; python_version < '3.11'",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=4.1",
    "ruff>=0.4",
    "mypy>=1.10",
    "pre-commit>=3.7",
    "types-PyYAML",
]

[project.scripts]
kaesi = "kaesi.cli:main"

[tool.hatch.build.targets.wheel]
packages = ["src/kaesi"]

[tool.pytest.ini_options]
addopts = "-ra --strict-markers"
testpaths = ["tests"]
pythonpath = ["src"]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "SIM"]
ignore = ["E501"]

[tool.mypy]
python_version = "3.11"
strict = true
files = ["src/kaesi"]
```

- [ ] **步骤 3：编写 `justfile`**

```just
set shell := ["bash", "-cu"]

_default:
    @just --list

# 创建虚拟环境并安装开发依赖（不含 maafw）
init:
    python3 -m venv .venv
    .venv/bin/pip install -U pip
    .venv/bin/pip install -e ".[dev]"
    .venv/bin/pre-commit install

# 安装 maafw（仅本机）
install:
    .venv/bin/pip install maafw

# 运行测试
test:
    .venv/bin/pytest --cov=kaesi --cov-report=term-missing

# 跳过慢用例
test-fast:
    .venv/bin/pytest -m "not slow"

# ruff 检查
lint:
    .venv/bin/ruff check src tests
    .venv/bin/ruff format --check src tests

# ruff 自动修复
fmt:
    .venv/bin/ruff check --fix src tests
    .venv/bin/ruff format src tests

# mypy
typecheck:
    .venv/bin/mypy src/kaesi

# 清理
clean:
    rm -rf dist build .coverage .pytest_cache .ruff_cache .mypy_cache
    find . -type d -name '__pycache__' -prune -exec rm -rf {} +
```

- [ ] **步骤 4：编写 `.pre-commit-config.yaml`**

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.7
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
```

- [ ] **步骤 5：提交**

```bash
git add .gitignore pyproject.toml justfile .pre-commit-config.yaml
git commit -m "chore(init): add repo config baseline"
```

### 任务 3：`src/kaesi` 包与 CLI 入口

**文件：**
- 新建：`src/kaesi/__init__.py`
- 新建：`src/kaesi/cli.py`

- [ ] **步骤 1：编写 `src/kaesi/__init__.py`**

```python
"""kaesi: 本地自用的卡厄思梦境辅助脚本。"""

__version__ = "0.0.1"
```

- [ ] **步骤 2：编写 `src/kaesi/cli.py`**

```python
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
```

- [ ] **步骤 3：提交**

```bash
git add src/kaesi/__init__.py src/kaesi/cli.py
git commit -m "feat(cli): add entrypoint with --version"
```

### 任务 4：MAA 封装层（facade + 协议）

**文件：**
- 新建：`src/kaesi/maa/__init__.py`
- 新建：`src/kaesi/maa/facade.py`

- [ ] **步骤 1：编写 `src/kaesi/maa/__init__.py`**

```python
"""maafw 封装层。

业务代码必须经此模块访问 maafw，禁止直接 import maafw。
"""

from kaesi.maa.facade import MaaFacade, get_facade

__all__ = ["MaaFacade", "get_facade"]
```

- [ ] **步骤 2：编写 `src/kaesi/maa/facade.py`**

```python
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
```

- [ ] **步骤 3：提交**

```bash
git add src/kaesi/maa/__init__.py src/kaesi/maa/facade.py
git commit -m "feat(maa): add facade and protocol-only backend"
```

### 任务 5：任务注册表

**文件：**
- 新建：`src/kaesi/tasks/__init__.py`
- 新建：`src/kaesi/tasks/registry.py`

- [ ] **步骤 1：编写 `src/kaesi/tasks/__init__.py`**

```python
"""任务注册中心。"""

from kaesi.tasks.registry import TaskRegistry, get_registry

__all__ = ["TaskRegistry", "get_registry"]
```

- [ ] **步骤 2：编写 `src/kaesi/tasks/registry.py`**

```python
"""任务注册表：集中管理所有可执行任务。"""

from __future__ import annotations

from dataclasses import dataclass, field


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
```

- [ ] **步骤 3：提交**

```bash
git add src/kaesi/tasks/__init__.py src/kaesi/tasks/registry.py
git commit -m "feat(tasks): add task registry"
```

### 任务 6：测试基础（conftest + fake_maafw）

**文件：**
- 新建：`tests/__init__.py`
- 新建：`tests/conftest.py`
- 新建：`tests/fixtures/__init__.py`
- 新建：`tests/fixtures/fake_maafw.py`

- [ ] **步骤 1：编写 `tests/__init__.py` 与 `tests/fixtures/__init__.py`**

两个文件均为空（仅保留模块命名空间）。

- [ ] **步骤 2：编写 `tests/conftest.py`**

```python
"""全局 pytest 配置。"""

from __future__ import annotations

import pytest


@pytest.fixture
def fake_maafw():
    """提供假 maafw 后端，避免单元测试依赖真实 MAA 运行时。"""
    from tests.fixtures.fake_maafw import FakeMaaBackend

    return FakeMaaBackend()
```

- [ ] **步骤 3：编写 `tests/fixtures/fake_maafw.py`**

```python
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
```

- [ ] **步骤 4：提交**

```bash
git add tests/__init__.py tests/conftest.py tests/fixtures/__init__.py tests/fixtures/fake_maafw.py
git commit -m "test: add pytest fixtures and fake maafw backend"
```

### 任务 7：单元测试（CLI / facade / registry）

**文件：**
- 新建：`tests/unit/test_cli.py`
- 新建：`tests/unit/test_facade.py`
- 新建：`tests/unit/test_registry.py`

- [ ] **步骤 1：编写 `tests/unit/test_registry.py`**

```python
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
```

- [ ] **步骤 2：编写 `tests/unit/test_facade.py`**

```python
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
```

- [ ] **步骤 3：编写 `tests/unit/test_cli.py`**

```python
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
```

- [ ] **步骤 4：本地运行测试，确认通过**

```bash
just test
```

预期：3 个测试全部通过；CLI 测试依赖 `kaesi` 包已 `pip install -e` 或 `pytest` 配置了 `pythonpath = ["src"]`。

- [ ] **步骤 5：提交**

```bash
git add tests/unit/
git commit -m "test: add unit tests for cli, facade, registry"
```

### 任务 8：README + 本计划提交

**文件：**
- 新建：`README.md`
- 新建：`docs/harness/plans/2026-07-08-spec-and-init-plan.md`（本计划）

- [ ] **步骤 1：编写 `README.md`**

```markdown
# kaesi

本地自用的「卡厄思梦境」手游辅助脚本，基于 [MaaFramework](https://github.com/MaaXYZ/MaaFramework) Python 绑定。

> ⚠️ 本项目仅供学习与自用，请遵守游戏方用户协议与当地法规。

## 当前状态

V1 初始化阶段。已完成仓库骨架与 `MaaFacade` / `TaskRegistry` 占位。后续 PR 将逐步接入：

- MaaFramework 真实接入
- 进入游戏 / 领奖（最小模板）
- 日常任务集（喝咖啡 / 疗愈中心 / 政策审阅 / 共度时光 / 红点清除）
- 战斗与推图（模拟 / 出击 / 自动推图 / 自动剧情）

研究路线图见 `docs/prs/20260708-2330-kaesi_scope_and_roadmap.md`。

## 开发

\`\`\`bash
just init      # 创建 venv 并安装开发依赖（不含 maafw）
just install   # 本机安装 maafw
just test      # 运行测试
just lint      # ruff 检查
just fmt       # 自动修复
just typecheck # mypy
\`\`\`

## 目录

\`\`\`
src/kaesi/        业务代码
src/kaesi/maa/    maafw 封装层
src/kaesi/tasks/  任务注册
resource/         MAA 模板与 pipeline（本仓库暂不提交运行时缓存）
tests/            pytest 测试
\`\`\`

## 规范入口

- 工作流：`docs/specs/agent-workflow.md`
- 审查：`docs/specs/review-guidelines.md`
- 计划编写：`.github/writing-plan.md`
- 项目根约束：`AGENTS.md`
```

- [ ] **步骤 2：提交 README 与本计划**

```bash
git add README.md docs/harness/plans/2026-07-08-spec-and-init-plan.md
git commit -m "docs: add README and implementation plan"
```

---

## 执行交接

计划已完成并保存到 `docs/harness/plans/2026-07-08-spec-and-init-plan.md`。执行选项：

1. **内联执行** — 在本地会话中继续执行任务，使用检查点进行批量执行。