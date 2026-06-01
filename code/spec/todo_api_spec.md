# 团队待办 API · 规格（SDD 产物）

> 待办归属团队，仅团队成员可操作。所有端点需登录（Bearer JWT）。

## 数据模型 Todo

| 字段 | 类型 | 约束 |
|---|---|---|
| `id` | int | 自增，只读 |
| `team_id` | int | 所属团队，只读 |
| `title` | str | **必填**；去除首尾空白后非空；长度 1–100 |
| `done` | bool | 默认 `false` |
| `created_by` | int | 创建者 user_id，只读 |
| `created_by_username` | str | 创建者用户名（响应用） |
| `completed_by` | int \| null | 标记完成者 user_id；未完成时为 null |
| `completed_by_username` | str \| null | 完成者用户名；未完成时为 null |

## 端点

### 1. 新建待办 `POST /teams/{team_id}/todos`

- 请求体：`{ "title": str }`
- 成功：`201`，返回完整 Todo（含 `id`、`done=false`、`created_by` 为当前用户）
- 失败：
  - 非团队成员 → `403`
  - 团队不存在 → `404`
  - `title` 空 / 仅空白 / 超过 100 字 → `422`

### 2. 列出待办 `GET /teams/{team_id}/todos`

- 成功：`200`，返回 `Todo[]`（按 `id` 升序）
- 失败：
  - 非团队成员 → `403`
  - 团队不存在 → `404`

### 3. 编辑标题 `PATCH /teams/{team_id}/todos/{id}`

- 请求体：`{ "title": str }`（必填）
- 成功：`200`，返回更新后的 Todo
- 失败：
  - 非团队成员 → `403`
  - 团队或待办不存在 → `404`
  - `title` 校验失败 → `422`

### 4. 删除待办 `DELETE /teams/{team_id}/todos/{id}`

- 成功：`204`，无响应体
- 失败：
  - 非团队成员 → `403`
  - 待办不存在 → `404`

### 5. 标记完成 `POST /teams/{team_id}/todos/{id}/done`

- 成功：`200`，返回更新后的 Todo（`done=true`，`completed_by` 为当前用户；幂等时不改已有 `completed_by`）
- 失败：
  - 非团队成员 → `403`
  - 待办不存在 → `404`
- **幂等**：已完成的待办再次标记 → 仍 `200`，`done=true`

## 边界（会逐条变成测试）

- 空标题 `""` → 422
- 仅空白标题 `"   "` → 422
- 超长标题（101 字）→ 422
- 待办 id 不存在 → 404
- 重复标记完成 → 200，幂等
- 非团队成员访问任意待办端点 → 403
- 删除后再次 `GET` 列表不包含该 id；单独 PATCH/DELETE 同一 id → 404

## 不在本次范围

- 待办跨团队移动
- 按 done 状态筛选（前端本地过滤即可）
- 分页、排序字段自定义
- 批量操作

## Spec 自检

1. 每条规则能否写成测试？ — 是
2. 本文件能否 2 分钟内审完？ — 是
3. 「不做」是否划死？ — 是
