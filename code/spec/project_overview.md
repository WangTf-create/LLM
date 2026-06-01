# 跨团队共享 TODO · 项目总览

## 一句话目标

注册用户可创建或加入团队，在团队工作区内协作管理待办（新建、列表、编辑、删除、标记完成）。

## 架构

```
用户浏览器 → 前端（静态页/轻量 SPA）
                ↓ Bearer JWT
            FastAPI 后端
                ↓
            SQLite 持久化
```

**业务域划分**（各域独立 Spec，见 sibling 文件）：

| 域 | Spec 文件 | 职责 |
|---|---|---|
| 认证 | [auth_spec.md](auth_spec.md) | 注册、登录、当前用户 |
| 团队 | [team_spec.md](team_spec.md) | 团队创建、成员邀请 |
| 待办 | [todo_api_spec.md](todo_api_spec.md) | 团队内待办 CRUD + 完成 |
| 前端 | [todo_ui_spec.md](todo_ui_spec.md) | 页面、路由、交互（继承 OpenAPI） |

**权限基线**（全局，每条可测）：

- 未登录访问受保护资源 → `401`
- 已登录但非团队成员访问该团队资源 → `403`
- 资源不存在 → `404`

## 技术栈

| 层 | 选型 | 说明 |
|---|---|---|
| 后端 | FastAPI | 现有栈 |
| 持久化 | SQLite + SQLAlchemy | MVP 单文件数据库 |
| 认证 | JWT Bearer（python-jose） | 无状态 token |
| 密码 | passlib bcrypt hash | 响应中 never 返回 password |
| 测试 | pyright + pytest + httpx | 先静态检查，再行为测试 |
| 前端 | 静态 HTML/JS 或轻量 SPA | Phase 5 由 OpenAPI + UI Spec 驱动 |

**允许的新依赖**（写代码前写入 `requirements.txt`）：`sqlalchemy`、`python-jose[cryptography]`、`passlib[bcrypt]`、`pyright`。

## 分阶段实施

严格遵循 [workflow.md](workflow.md)：**Spec 确认 → 测试红 → 实现绿 → 重构**；一个端点一个循环。

| 阶段 | 内容 | 产出 |
|---|---|---|
| Phase 1 | Auth TDD | `test/test_auth.py` + `backend/` 认证模块 |
| Phase 2 | Team TDD | `test/test_team.py` + 团队模块 |
| Phase 3 | Todo TDD | `test/test_todo_api.py` + 待办模块 |
| Phase 4 | 契约 | 运行服务导出 `openapi.json` |
| Phase 5 | 前端 | 按 OpenAPI + [todo_ui_spec.md](todo_ui_spec.md) 实现页面 |

## 明确不做（MVP）

- SSO / OAuth / 第三方登录
- 实时推送 / WebSocket 同步
- 待办评论、附件、截止日期、优先级、标签
- 组织多级层级（公司/部门/小组）
- 分页（待办总量 <500 时全量返回）
- 邮件通知、Magic Link 登录

## Spec 自检

1. 每条规则能否写成测试？ — 权限基线与各域 Spec 边界均已列出
2. 本文件能否 2 分钟内审完？ — 是
3. 「不做」是否划死？ — 是
