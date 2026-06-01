# Team Todo API 参考文档

> 版本：0.1.0 · 基础 URL：`http://127.0.0.1:8000`  
> 机器可读契约：[openapi.json](openapi.json) · 交互文档：`/docs`（Swagger UI）

## 概述

跨团队共享待办 REST API。用户注册登录后创建/加入团队，在团队工作区内协作管理待办。

**认证方式**：JWT Bearer Token  
**请求头**：`Authorization: Bearer <access_token>`  
**Content-Type**：`application/json`

### 权限基线

| 场景 | HTTP 状态码 |
|---|---|
| 未登录访问受保护资源 | `401` |
| 已登录但非团队成员 | `403` |
| 资源不存在 | `404` |
| 请求体验证失败 | `422` |
| 唯一约束冲突 | `409` |

---

## 数据模型

### UserPublic

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | int | 用户 ID |
| `username` | str | 用户名（3–32 字，字母数字下划线） |

### TokenResponse

| 字段 | 类型 | 说明 |
|---|---|---|
| `access_token` | str | JWT |
| `token_type` | str | 固定 `bearer` |

### TeamPublic

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | int | 团队 ID |
| `name` | str | 团队名（1–50 字，全局唯一） |
| `created_by` | int | 创建者 user_id |
| `created_by_username` | str | 创建者用户名 |

### TeamMemberPublic

| 字段 | 类型 | 说明 |
|---|---|---|
| `team_id` | int | 团队 ID |
| `user_id` | int | 成员 user_id |
| `role` | str | `owner` 或 `member` |

### TodoPublic

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | int | 待办 ID |
| `team_id` | int | 所属团队 |
| `title` | str | 标题（去空白后 1–100 字） |
| `done` | bool | 是否完成 |
| `created_by` | int | 创建者 user_id |
| `created_by_username` | str | 创建者用户名 |
| `completed_by` | int \| null | 完成者 user_id（未完成时为 null） |
| `completed_by_username` | str \| null | 完成者用户名 |

---

## 认证 Auth

### POST /auth/register — 注册

**无需登录**

请求体：

```json
{
  "username": "alice",
  "password": "secret1"
}
```

| 字段 | 约束 |
|---|---|
| `username` | 3–32 字，字母数字下划线，唯一 |
| `password` | 最少 6 字符 |

| 状态码 | 说明 | 响应体 |
|---|---|---|
| `201` | 成功 | UserPublic |
| `409` | 用户名已存在 | `{ "detail": "..." }` |
| `422` | 校验失败 | ValidationError |

示例响应（201）：

```json
{
  "id": 1,
  "username": "alice"
}
```

---

### POST /auth/login — 登录

**无需登录**

请求体：

```json
{
  "username": "alice",
  "password": "secret1"
}
```

| 状态码 | 说明 | 响应体 |
|---|---|---|
| `200` | 成功 | TokenResponse |
| `401` | 凭据错误 | `{ "detail": "Invalid credentials" }` |
| `422` | 校验失败 | ValidationError |

示例响应（200）：

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

---

### GET /auth/me — 当前用户

**需要 Bearer Token**

| 状态码 | 说明 | 响应体 |
|---|---|---|
| `200` | 成功 | UserPublic |
| `401` | 无/无效 token | `{ "detail": "..." }` |

---

## 团队 Teams

以下端点均需 **Bearer Token**。

### POST /teams — 创建团队

请求体：

```json
{
  "name": "Engineering"
}
```

| 字段 | 约束 |
|---|---|
| `name` | 去空白后 1–50 字，全局唯一 |

| 状态码 | 说明 | 响应体 |
|---|---|---|
| `201` | 成功；创建者自动成为 `owner` | TeamPublic |
| `409` | 团队名重复 | `{ "detail": "..." }` |
| `422` | 名称为空/过长 | ValidationError |

---

### GET /teams — 我的团队列表

| 状态码 | 说明 | 响应体 |
|---|---|---|
| `200` | 成功 | TeamPublic[]（按 id 升序） |

---

### GET /teams/{team_id} — 团队详情

| 状态码 | 说明 | 响应体 |
|---|---|---|
| `200` | 成功 | TeamPublic |
| `403` | 非团队成员 | `{ "detail": "Not a team member" }` |
| `404` | 团队不存在 | `{ "detail": "Team not found" }` |

---

### POST /teams/{team_id}/members — 邀请成员

**仅 team owner 可调用**

请求体：

```json
{
  "username": "bob"
}
```

| 状态码 | 说明 | 响应体 |
|---|---|---|
| `201` | 成功 | TeamMemberPublic（role=member） |
| `403` | 非 owner | `{ "detail": "Owner required" }` |
| `404` | 团队不存在 / 用户不存在 | `{ "detail": "..." }` |
| `409` | 已是成员 | `{ "detail": "User already a team member" }` |

---

## 待办 Todos

路径前缀：`/teams/{team_id}/todos`  
以下端点均需 **Bearer Token** 且为 **团队成员**。

### POST /teams/{team_id}/todos — 新建待办

请求体：

```json
{
  "title": "Write tests"
}
```

| 字段 | 约束 |
|---|---|
| `title` | 去空白后 1–100 字 |

| 状态码 | 说明 | 响应体 |
|---|---|---|
| `201` | 成功 | TodoPublic（done=false） |
| `403` | 非团队成员 | `{ "detail": "..." }` |
| `404` | 团队不存在 | `{ "detail": "..." }` |
| `422` | 标题校验失败 | ValidationError |

---

### GET /teams/{team_id}/todos — 列出待办

| 状态码 | 说明 | 响应体 |
|---|---|---|
| `200` | 成功 | TodoPublic[]（按 id 升序） |
| `403` | 非团队成员 | `{ "detail": "..." }` |
| `404` | 团队不存在 | `{ "detail": "..." }` |

---

### PATCH /teams/{team_id}/todos/{todo_id} — 编辑标题

请求体：

```json
{
  "title": "Updated title"
}
```

| 状态码 | 说明 | 响应体 |
|---|---|---|
| `200` | 成功 | TodoPublic |
| `403` | 非团队成员 | `{ "detail": "..." }` |
| `404` | 待办不存在 | `{ "detail": "Todo not found" }` |
| `422` | 标题校验失败 | ValidationError |

---

### DELETE /teams/{team_id}/todos/{todo_id} — 删除待办

| 状态码 | 说明 | 响应体 |
|---|---|---|
| `204` | 成功 | 无响应体 |
| `403` | 非团队成员 | `{ "detail": "..." }` |
| `404` | 待办不存在 | `{ "detail": "..." }` |

---

### POST /teams/{team_id}/todos/{todo_id}/done — 标记完成

| 状态码 | 说明 | 响应体 |
|---|---|---|
| `200` | 成功 | TodoPublic（done=true，写入 completed_by） |
| `403` | 非团队成员 | `{ "detail": "..." }` |
| `404` | 待办不存在 | `{ "detail": "..." }` |

**幂等**：已完成的待办再次调用仍返回 `200`；`completed_by` 保持首次完成者不变。

---

## 典型调用流程

```text
1. POST /auth/register        -> 201 UserPublic
2. POST /auth/login           -> 200 { access_token }
3. POST /teams                -> 201 TeamPublic（Header: Bearer token）
4. POST /teams/{id}/members   -> 201（owner 邀请成员）
5. POST /teams/{id}/todos     -> 201 TodoPublic
6. POST /teams/{id}/todos/{tid}/done -> 200 TodoPublic
7. GET  /teams/{id}/todos     -> 200 TodoPublic[]
```

---

## 错误响应格式

### 校验错误（422）

```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "...",
      "type": "..."
    }
  ]
}
```

### 业务错误（401 / 403 / 404 / 409）

```json
{
  "detail": "错误描述字符串"
}
```

---

## 相关 Spec

| Spec | 路径 |
|---|---|
| 认证 | `code/spec/auth_spec.md` |
| 团队 | `code/spec/team_spec.md` |
| 待办 | `code/spec/todo_api_spec.md` |
| 前端 UI | `code/spec/todo_ui_spec.md` |
