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

```bash
just init      # 创建 venv 并安装开发依赖（不含 maafw）
just install   # 本机安装 maafw
just test      # 运行测试
just lint      # ruff 检查
just fmt       # 自动修复
just typecheck # mypy
```

## 目录

```
src/kaesi/        业务代码
src/kaesi/maa/    maafw 封装层
src/kaesi/tasks/  任务注册
resource/         MAA 模板与 pipeline（本仓库暂不提交运行时缓存）
tests/            pytest 测试
```

## 规范入口

- 工作流：`docs/specs/agent-workflow.md`
- 审查：`docs/specs/review-guidelines.md`
- 计划编写：`.github/writing-plan.md`
- 项目根约束：`AGENTS.md`