# 前端（课1 命题演示 · 第二幕）

> **页面不预写——现场从后端的 OpenAPI 契约生成。** 这里只说要点。

## 演什么

后端跑起来后产出 `/openapi.json`。把这份契约喂给 AI 生成待办列表 + 新建表单页面，
当众指出：UI 里的每个约束都**不是前端拍脑袋定的，是从契约继承的**——

| UI 里的东西 | 来自契约的哪一项 |
|---|---|
| 只调 `/todos`、`/todos/{id}/done` | 契约的 `paths` |
| 新建只发 `{ title }` | `TodoCreate` 只有 `title` |
| 标题输入 `maxlength=100` | `title` 的 `maxLength` |
| 标题非空才允许提交 | `title` 的 `minLength: 1` |

## 题眼

> **API 定义不是文档，是上一层的产出变成下一层的规格。** AI 没法编一个后端不存在的字段。

进阶：从 OpenAPI 直接生成 typed client / mock，把约束落到代码级别。方法卡见
[../../materials/03_API契约约束前端_方法卡.md](../../materials/03_API契约约束前端_方法卡.md)。

> 课前用同一契约现场生成一版存进 `_backup_现场产物/`（git 忽略）当断网后备。
