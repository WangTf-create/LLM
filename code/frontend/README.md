# 前端（OpenAPI + todo_ui_spec 驱动）

> 页面由 [openapi.json](../backend/openapi.json) 与 [todo_ui_spec.md](../spec/todo_ui_spec.md) 生成。

## 启动

```bash
cd code/backend
pip install -r requirements.txt
uvicorn app:app --reload
```

浏览器打开：

- 前端：`http://127.0.0.1:8000/`（hash 路由：`#/login`、`#/teams`、`#/teams/1/todos`）
- OpenAPI：`http://127.0.0.1:8000/openapi.json`
- 交互文档：`http://127.0.0.1:8000/docs`

## 文件

| 文件 | 作用 |
|---|---|
| `index.html` | 单页应用入口 |
| `app.js` | 路由、API 调用、页面逻辑 |
| `style.css` | 样式 |

## 契约继承

| UI | 来源 |
|---|---|
| 端点路径 | openapi `paths` |
| 请求体字段 | `components.schemas` |
| 标题 `maxlength=100` | TodoCreate / TodoUpdate |
| 团队名 `maxlength=50` | TeamCreate |
