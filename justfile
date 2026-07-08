set shell := ["bash", "-cu"]

_default:
    @just --list

# 创建虚拟环境并安装开发依赖（不含 maafw；maafw 在用户本机安装）
init:
    python3 -m venv .venv
    .venv/bin/pip install -U pip
    .venv/bin/pip install -e ".[dev]"
    .venv/bin/pre-commit install

# 安装 maafw（仅本机，不进 CI）
install:
    .venv/bin/pip install maafw

# 运行测试（含覆盖率）
test:
    .venv/bin/pytest --cov=kaesi --cov-report=term-missing

# 跳过慢用例
test-fast:
    .venv/bin/pytest -m "not slow"

# ruff 检查 + format --check
lint:
    .venv/bin/ruff check src tests
    .venv/bin/ruff format --check src tests

# ruff 自动修复
fmt:
    .venv/bin/ruff check --fix src tests
    .venv/bin/ruff format src tests

# 静态类型检查
typecheck:
    .venv/bin/mypy src/kaesi

# 清理构建产物
clean:
    rm -rf dist build .coverage .pytest_cache .ruff_cache .mypy_cache
    find . -type d -name '__pycache__' -prune -exec rm -rf {} +