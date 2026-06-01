# 待办前端 · UI 规格（SDD 产物）

> OpenAPI 契约（`openapi.json`）是字段与端点的机器可读 Spec；本文件描述 OpenAPI **无法表达**的页面、路由与交互。
> 字段约束（如 `title` 长度）**从契约继承**，不在此重复定义。

## 技术约束

- 调用后端时使用 `Authorization: Bearer <token>`
- API Base URL：开发环境 `http://127.0.0.1:8000`
- token 存 `localStorage`，键名 `access_token`

## 从 OpenAPI 继承（实现时读契约，不自行编造）

| UI 行为 | 契约来源 |
|---|---|
| 可调用的路径 | `paths` 中定义的端点 |
| 注册/登录请求体字段 | `components.schemas` |
| 新建/编辑待办只发 `{ title }` | TodoCreate / TodoUpdate schema |
| 标题输入 `maxlength=100` | `title` 的 `maxLength` |
| 标题非空校验 | `title` 的 `minLength: 1` |

## 页面与路由

### 1. `/login`

| 元素 | 行为 |
|---|---|
| 用户名、密码输入框 | 提交调用 `POST /auth/login` |
| 登录按钮 | 凭据为空时禁用 |
| 注册链接 | 跳转 `/register` |
| 登录成功 | 存 token，跳转 `/teams` |
| 登录失败 | 展示 API 返回的错误信息（如 401） |

### 2. `/register`

| 元素 | 行为 |
|---|---|
| 用户名、密码输入框 | 提交调用 `POST /auth/register` |
| 注册成功 | 自动登录或跳转 `/login`（实现二选一，需在代码中统一） |
| 注册失败 | 展示 422/409 错误信息 |
| 已有账号链接 | 跳转 `/login` |

**本 Spec 约定**：注册成功后调用登录接口，存 token，跳转 `/teams`。

### 3. `/teams`

| 元素 | 行为 |
|---|---|
| 团队列表 | `GET /teams`，展示团队名 |
| 创建团队表单 | 名称输入 + 提交 `POST /teams` |
| 团队项点击 | 跳转 `/teams/:teamId/todos` |
| 团队卡片「协作记录」区域 | 展示创建者 username |
| 空状态 | 无团队时提示创建第一个团队 |

### 4. `/teams/:teamId/todos`

| 元素 | 行为 |
|---|---|
| 待办列表 | `GET /teams/{team_id}/todos` |
| 待办卡片「协作记录」区域 | 展示创建者、完成者（未完成显示「待完成」） |
| 新建表单 | `POST /teams/{team_id}/todos`；成功后刷新列表 |
| 标记完成按钮 | `POST .../todos/{id}/done`；已完成项可隐藏按钮或置灰 |
| 编辑标题 | 内联或弹窗；`PATCH .../todos/{id}` |
| 删除 | 确认后 `DELETE .../todos/{id}` |
| 返回 | 链接回 `/teams` |

### 5. 全局

| 规则 | 行为 |
|---|---|
| 未登录访问 `/teams`、`/teams/:id/todos` | 重定向 `/login` |
| API 返回 401 | 清除 token，重定向 `/login` |
| API 返回 403 | 展示「无权限」提示，不清 token |
| API 返回 404 | 展示「不存在」提示 |

## 边界（交互规则，MVP 可手工验证）

- 标题仅空白时前端禁用提交（与后端 422 双保险）
- 标题超过 100 字前端禁止输入（`maxlength`）
- 删除待办前需用户确认（防误触）

## 不在本次范围

- 国际化、主题切换
- 移动端专属布局
- 前端自动化 E2E 测试（规则写入 Spec，实现阶段可选补测）
- 离线缓存、乐观更新

## Spec 自检

1. 每条规则能否写成测试？ — 交互规则可手工或 E2E 验证
2. 本文件能否 2 分钟内审完？ — 是
3. 「不做」是否划死？ — 是
