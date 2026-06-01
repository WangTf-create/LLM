# Team Todo 测试报告

> 生成时间：2026-06-01  
> 项目：跨团队共享 TODO  
> 结论：**全部通过**

---

## 1. 摘要

| 类别 | 工具 | 用例数 | 通过 | 失败 | 结果 |
|---|---|---:|---:|---:|---|
| 静态类型检查 | pyright | — | — | 0 error | PASS |
| 后端 API 测试 | pytest | 42 | 42 | 0 | PASS |
| 前端冒烟测试 | pytest | 5 | 5 | 0 | PASS |
| 前端 UI 规范核对 | 人工核对清单 | 18 | 18 | 0 | PASS |
| **合计** | | **65** | **65** | **0** | **PASS** |

**验证顺序**（项目规范）：`pyright backend test` → `pytest test/`

---

## 2. 测试环境

| 项 | 值 |
|---|---|
| 操作系统 | Windows 10 |
| Python | 3.12.10 |
| 测试框架 | pytest 9.0.3 |
| 静态检查 | pyright（basic 模式） |
| HTTP 客户端 | httpx（via FastAPI TestClient） |
| 后端框架 | FastAPI + SQLAlchemy + SQLite |
| 前端 | 静态 SPA（`code/frontend/`） |
| 工作目录 | `code/` |
| 配置文件 | `code/pyrightconfig.json`、`code/pytest.ini` |

---

## 3. 静态类型检查（pyright）

**命令**：

```bash
cd code
pyright backend test
```

**结果**：

```text
0 errors, 0 warnings, 0 informations
```

**扫描范围**：`code/backend/`、`code/test/`

---

## 4. 后端 API 测试（pytest）

**命令**：

```bash
cd code
python -m pytest test/test_auth.py test/test_team.py test/test_todo_api.py -v
```

**结果**：`42 passed in ~14s`

### 4.1 认证 Auth（12 条）— 驱动 `code/spec/auth_spec.md`

| 用例 | 结果 |
|---|---|
| test_register_success | PASS |
| test_register_empty_username_422 | PASS |
| test_register_short_username_422 | PASS |
| test_register_invalid_username_422 | PASS |
| test_register_short_password_422 | PASS |
| test_register_duplicate_username_409 | PASS |
| test_login_success | PASS |
| test_login_wrong_password_401 | PASS |
| test_login_nonexistent_user_401 | PASS |
| test_me_success | PASS |
| test_me_no_authorization_401 | PASS |
| test_me_invalid_token_401 | PASS |

### 4.2 团队 Team（14 条）— 驱动 `code/spec/team_spec.md`

| 用例 | 结果 |
|---|---|
| test_create_team_success | PASS |
| test_create_team_empty_name_422 | PASS |
| test_create_team_blank_name_422 | PASS |
| test_create_team_name_too_long_422 | PASS |
| test_create_team_duplicate_name_409 | PASS |
| test_list_teams_success | PASS |
| test_get_team_success | PASS |
| test_get_team_non_member_403 | PASS |
| test_get_team_not_found_404 | PASS |
| test_invite_member_success | PASS |
| test_invite_member_not_owner_403 | PASS |
| test_invite_nonexistent_user_404 | PASS |
| test_invite_duplicate_member_409 | PASS |
| test_teams_require_auth_401 | PASS |

### 4.3 待办 Todo（16 条）— 驱动 `code/spec/todo_api_spec.md`

| 用例 | 结果 |
|---|---|
| test_create_todo_success | PASS |
| test_create_todo_empty_title_422 | PASS |
| test_create_todo_blank_title_422 | PASS |
| test_create_todo_title_too_long_422 | PASS |
| test_create_todo_non_member_403 | PASS |
| test_create_todo_team_not_found_404 | PASS |
| test_list_todos_success | PASS |
| test_list_todos_non_member_403 | PASS |
| test_patch_todo_success | PASS |
| test_patch_todo_not_found_404 | PASS |
| test_delete_todo_success | PASS |
| test_delete_todo_not_found_404 | PASS |
| test_mark_done_success | PASS |
| test_mark_done_idempotent | PASS |
| test_mark_done_not_found_404 | PASS |
| test_delete_then_absent_from_list_and_patch_404 | PASS |

---

## 5. 前端测试

### 5.1 自动化冒烟测试（5 条）— 驱动 `code/spec/todo_ui_spec.md`

**命令**：

```bash
cd code
python -m pytest test/test_frontend_smoke.py -v
```

**结果**：`5 passed`

| 用例 | 验证点 | 结果 |
|---|---|---|
| test_static_index_page | 首页 200，引用 app.js / style.css | PASS |
| test_static_assets | `/app.js`、`/style.css` 可访问 | PASS |
| test_app_js_openapi_constraints | token 键名、Bearer 头、maxlength、协作记录文案 | PASS |
| test_app_js_routes_and_flows | 路由与 API 路径、删除确认对话框 | PASS |
| test_openapi_json_available | 契约可访问且含核心 schema | PASS |

### 5.2 运行时 HTTP 冒烟（服务启动时）

在 `http://127.0.0.1:8000` 验证：

| 路径 | 状态码 | 结果 |
|---|---|---|
| `/` | 200 | PASS |
| `/index.html` | 200 | PASS |
| `/app.js` | 200 | PASS |
| `/style.css` | 200 | PASS |
| `/openapi.json` | 200 | PASS |
| `/docs` | 200 | PASS |

### 5.3 UI 规范核对清单（18 条）

依据 `code/spec/todo_ui_spec.md`，对照 `code/frontend/app.js` 实现核对：

| # | 页面/规则 | 预期行为 | 结果 |
|---|---|---|---|
| F01 | `#/login` | 调用 `POST /auth/login` | PASS |
| F02 | `#/login` | 凭据为空时禁用登录按钮 | PASS |
| F03 | `#/login` | 注册链接跳转 | PASS |
| F04 | `#/login` | 成功存 token 并跳转 teams | PASS |
| F05 | `#/register` | 调用 `POST /auth/register` | PASS |
| F06 | `#/register` | 注册后自动登录跳转 teams | PASS |
| F07 | `#/teams` | `GET /teams` 列表 | PASS |
| F08 | `#/teams` | `POST /teams` 创建团队 | PASS |
| F09 | `#/teams` | 协作记录展示创建者 | PASS |
| F10 | `#/teams/:id/todos` | 待办列表与新建 | PASS |
| F11 | `#/teams/:id/todos` | 协作记录展示创建者/完成者 | PASS |
| F12 | `#/teams/:id/todos` | 标记完成 / 编辑 / 删除 | PASS |
| F13 | 全局 | 未登录重定向 login | PASS |
| F14 | 全局 | 401 清 token 回 login | PASS |
| F15 | 全局 | 403/404 toast 提示 | PASS |
| F16 | 边界 | 空白标题禁用提交 | PASS |
| F17 | 边界 | 标题 maxlength=100 | PASS |
| F18 | 边界 | 删除前 confirm 确认 | PASS |

> 说明：F01–F18 通过自动化冒烟 + 源码对照完成；未引入 Playwright/Cypress E2E 框架（见 UI Spec「不在本次范围」）。

---

## 6. 复现命令

在 `code/` 目录一次性跑完全部自动化检查：

```bash
pip install -r backend/requirements.txt
pyright backend test
python -m pytest test/ -v
```

---

## 7. 结论

- 静态检查、后端 42 条 API 测试、前端 5 条冒烟测试 **全部通过**
- UI Spec 18 条交互规则 **全部满足**
- 当前版本可作为交付基线；API 文档见 [api.md](api.md)

---

## 8. 相关文档

| 文档 | 路径 |
|---|---|
| API 参考 | [api.md](api.md) |
| OpenAPI 契约 | [openapi.json](openapi.json) |
| 测试代码 | `code/test/` |
| 工作规范 | `code/spec/workflow.md` |
