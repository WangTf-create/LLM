# 文档目录

跨团队共享 TODO 项目交付文档。

| 文档 | 说明 |
|---|---|
| [api.md](api.md) | 完整 REST API 参考（人类可读） |
| [test-report.md](test-report.md) | 完整测试报告（pyright + pytest + 前端） |
| [openapi.json](openapi.json) | OpenAPI 3.1 机器可读契约 |

> 契约源文件：`code/backend/openapi.json`。更新 API 后请运行 `python code/backend/export_openapi.py` 并同步本目录的 `openapi.json`。

## 快速链接

- 本地 API 文档：http://127.0.0.1:8000/docs
- 本地前端：http://127.0.0.1:8000/
- 运行测试：`cd code && pyright backend test && python -m pytest test/ -q`
