# 认证 API · 规格（SDD 产物）

> 用户注册与登录。JWT Bearer 作为后续所有受保护端点的凭证。

## 数据模型 User

| 字段 | 类型 | 约束 |
|---|---|---|
| `id` | int | 自增，只读 |
| `username` | str | **唯一**；3–32 字；仅字母、数字、下划线 |
| `password_hash` | str | 仅存 hash，**响应中 never 返回** |

**对外响应 UserPublic**（注册、/me）：`{ "id": int, "username": str }`

## 端点

### 1. 注册 `POST /auth/register`

- 请求体：`{ "username": str, "password": str }`
- 成功：`201`，返回 UserPublic
- 失败：
  - 用户名格式不合法 / 密码过短 → `422`
  - 用户名已存在 → `409`

**密码约束**：最少 6 字符（写入请求校验）。

### 2. 登录 `POST /auth/login`

- 请求体：`{ "username": str, "password": str }`
- 成功：`200`，返回 `{ "access_token": str, "token_type": "bearer" }`
- 失败：用户名不存在或密码错误 → `401`（不区分具体原因，防枚举）

### 3. 当前用户 `GET /auth/me`

- 请求头：`Authorization: Bearer <token>`
- 成功：`200`，返回 UserPublic
- 失败：缺少 / 无效 / 过期 token → `401`

## 边界（会逐条变成测试）

- 用户名为空 `""` → 422
- 用户名过短（2 字）→ 422
- 用户名含非法字符（如 `user-name`）→ 422
- 密码少于 6 字符 → 422
- 重复注册同一 username → 409
- 登录密码错误 → 401
- 登录不存在的 username → 401
- `/auth/me` 无 Authorization header → 401
- `/auth/me` 无效 token → 401

## 不在本次范围

- 邮箱注册、Magic Link、找回密码
- Refresh token、token 吊销列表
- 用户资料编辑、头像

## Spec 自检

1. 每条规则能否写成测试？ — 是（见边界列表）
2. 本文件能否 2 分钟内审完？ — 是
3. 「不做」是否划死？ — 是
