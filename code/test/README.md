# 测试目录

本目录集中存放**所有后端 API 测试**（pytest）。实现代码在 `../backend/`，规格在 `../spec/`。

## 文件规划（按 Phase 生成）

| 文件 | 驱动 Spec | 阶段 |
|---|---|---|
| `test_auth.py` | [auth_spec.md](../spec/auth_spec.md) | Phase 1 |
| `test_team.py` | [team_spec.md](../spec/team_spec.md) | Phase 2 |
| `test_todo_api.py` | [todo_api_spec.md](../spec/todo_api_spec.md) | Phase 3 |
| `test_frontend_smoke.py` | [todo_ui_spec.md](../spec/todo_ui_spec.md) | 前端冒烟 |

## 运行方式

在 `code/` 目录下执行。**先 pyright，后 pytest**：

```bash
pip install -r backend/requirements.txt
pyright backend test
python -m pytest test/ -q
```

只跑某一域（仍建议先跑 pyright）：

```bash
pyright backend test
python -m pytest test/test_auth.py -q
```

## 约定

- 测试文件名：`test_*.py`
- 每个 spec「边界」条目对应至少一条测试
- 先写测试（红），再写 `backend/` 实现（绿）
- 不在 `backend/` 下放置测试文件
- **静态检查是 pytest 的前置步骤**，pyright 未通过不算完成

## 公共 fixture

共享 fixture（如 TestClient、测试数据库）放在 [conftest.py](conftest.py)。
