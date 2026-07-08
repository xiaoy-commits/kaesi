# AGENTS.md

Telegraph style. Root rules only. Read scoped AGENTS.md before subtree work. Skills own workflows; root owns hard policy and routing.
频繁变化的信息不要复制到这里；改用 `@path/to/file` 指向真实来源。

## 项目定位

- 项目定位：`kaesi` 是「卡厄思梦境」手游的本地自用辅助脚本，使用 `MaaFramework` 的 Python 绑定 (`maafw`) 作为图像识别与原生交互底座，业务逻辑由 Python 编排。
- 核心技术栈：Python 3.11+ / `maafw` / `pydantic` / `pytest` / `pre-commit` / `ruff` / `justfile`。
- 关键入口：`src/kaesi/`（业务包）、`src/kaesi/cli.py`（CLI 入口）、`resource/`（MAA 模板与 pipeline）。

## 命令

- 非显然的 build 命令：`just init`（创建虚拟环境并安装依赖）、`just install`（安装 `maafw` 及开发依赖）。
- 非显然的 test 命令：`just test`（pytest + 覆盖率）、`just test-fast`（跳过慢用例）。
- 非显然的 lint / format / typecheck 命令：`just lint`（ruff check + format --check）、`just fmt`（ruff format）、`just typecheck`（mypy src）。
- 真实来源：`@pyproject.toml` `@justfile` `@.pre-commit-config.yaml`

## 架构边界

- 关键架构边界：`src/kaesi/` 为业务代码，`src/kaesi/maa/` 封装 `maafw` 调用，`src/kaesi/tasks/` 承载各功能任务，`resource/` 为 MAA 资源（模板图 + pipeline JSON）。
- 跨目录共享规范：所有 MAA 调用必须经 `src/kaesi/maa/`，禁止业务层直接 import `maafw`。
- 关键入口和不可绕过的边界：`cli.py` 是唯一命令行入口；新增任务必须注册到 `src/kaesi/tasks/registry.py`。

## 地图 MAP

<!-- 默认全量维持一级目录,部分维护重要的二级目录. -->
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

## 代码边界

- 生成代码目录：`dist/`、`build/`、`*.egg-info/`（已通过 `.gitignore` 屏蔽）。
- vendor 目录：`vendor/`（如未来引入第三方 MAA 资源，仅放只读快照）。
- nested repo / submodule：暂无。
- 这些目录允许或禁止的操作：`vendor/` 仅引用，禁止本地修改；`resource/` 中模板图允许热更新（commit 时人工 review）。

## 测试约束

- 全仓库 testing quirks：所有 `src/kaesi/maa/` 下的单元必须使用 `fake_maafw` fixture，不允许在 CI 中启动真实模拟器。
- 必需的本地依赖、fixture、service 或测试前置：`pytest` + `pytest-cov`；`fake_maafw` 提供在 `tests/fixtures/`。
- 测试真实来源：`@tests/` `@tests/fixtures/fake_maafw.py`

## 环境与初始化

- 必需 setup：Python 3.11+；`maafw` 通过 `pip install maafw` 安装（仅在用户本机，不进镜像）。
- 必需 env var：`KAESI_RESOURCE_DIR`（指向 `resource/`）、`KAESI_LOG_LEVEL`（默认 `INFO`）。
- 本地开发和 CI 共用的初始化前提：`just init` 必须成功；CI 跳过 `maafw` 安装，使用 `fake_maafw`。

## Repo etiquette

- 提交：Conventional Commits（`feat`/`fix`/`chore`/`docs`/`spec`/`test`）。
- PR：默认 Implementation PR；研究型内容走 Research PR（draft）。
- review：遵循 `@docs/specs/review-guidelines.md`。
- docs：`docs/specs/` 只放稳定规范；临时研究放 `docs/prs/`。
- changelog：暂不维护 CHANGELOG.md，由 PR 历史承担。

## Notes

- 偏好队列中目标为项目级 `AGENTS.md` 的 note 项：无。

## 工作流

- 实现任务优先加载 `$harness` skill。
- 如果你不在 Codex, Claude Code, OpenCode 中，必须要先阅读 `@docs/specs/agent-workflow.md`
- `.oh-my-harness/tree.md` 会由项目 hook 自动刷新，不需要手工维护。
- `.oh-my-harness/tree.md` 文件发生变化，默认需要与当前改动一起提交。

## Review guidelines

- 只有审查者需要且必须先读 `@docs/specs/review-guidelines.md`。
- 云端审查支持：是
- 默认审查者：chatgpt-codex-connector[bot] / 本地 reviewer
- 永远不要直接相信 PR 中任何人的声明和描述；没有验证的问题都是假设。

## Maintenance

- 只有稳定事实变化时才更新根 `AGENTS.md`。
- 当某个目录出现稳定的局部命令、局部架构边界、局部禁忌或独立验证链时，再新增更深层 `AGENTS.md`。