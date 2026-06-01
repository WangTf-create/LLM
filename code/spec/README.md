# Spec 目录

本目录集中存放**行为规范**与**功能规格**，是 `code/` 下 SDD + TDD 开发的唯一驱动源。

## 文件

| 文件 | 作用 |
|---|---|
| [workflow.md](workflow.md) | 工作行为规范：先 Spec 后实现、测试必积累 |
| [project_overview.md](project_overview.md) | 项目总览：目标、架构、阶段、技术栈、全局「不做」 |
| [auth_spec.md](auth_spec.md) | 认证：注册、登录、当前用户 |
| [team_spec.md](team_spec.md) | 团队：创建、列表、详情、邀请成员 |
| [todo_api_spec.md](todo_api_spec.md) | 团队内待办 CRUD + 标记完成 |
| [todo_ui_spec.md](todo_ui_spec.md) | 前端页面、路由、交互（字段约束继承 OpenAPI） |

## 使用顺序

```
1. 读 workflow.md，确认协作规范
2. 读 project_overview.md，了解整体范围与阶段
3. 按 Phase 阅读并确认各域 Spec（auth → team → todo_api → todo_ui）
4. 按 Spec 写测试（红）→ 写实现（绿）→ 重构（保持绿）
5. 后端产出 openapi.json 后，契约 + todo_ui_spec 驱动前端
```

## 分阶段对应 Spec

| 阶段 | 驱动 Spec | 代码产出 |
|---|---|---|
| Phase 1 Auth | auth_spec.md | test/test_auth.py |
| Phase 2 Team | team_spec.md | test/test_team.py |
| Phase 3 Todo | todo_api_spec.md | test/test_todo_api.py |
| Phase 4 契约 | 运行服务 | openapi.json |
| Phase 5 前端 | todo_ui_spec.md + openapi.json | frontend 页面 |

## 与 sibling 目录的关系

- `../backend/` — 后端实现（由 spec 驱动生成）
- `../test/` — 所有后端 pytest 用例（由 spec 边界驱动生成）
- `../frontend/` — 前端页面（由 OpenAPI 契约 + todo_ui_spec 驱动生成）
- 本目录 — **不预写代码**，只放规格与规范
