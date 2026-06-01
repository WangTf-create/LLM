# 待办事项 API · 后端（课1 命题演示）

> **代码不在这里——它在课堂上从 [spec](../spec/todo_api_spec.md) 现场生成。**
> 这个目录只放：环境依赖 + 运行说明。规格与行为规范见 [spec/](../spec/)。`app.py` / `openapi.json` 在 `backend/` 生成；测试统一在 [../test/](../test/)。

## 这个演示在演什么

从一份人能审完的 spec，用 SDD + TDD 现场长出可信代码：
`spec 探讨（人确认）→ AI 按 spec 写测试（红）→ AI 补实现（绿）→ 产出 OpenAPI 契约 → 契约约束前端`。
完整编排见 [../演示脚本.md](../演示脚本.md)。

## 环境

```bash
source /opt/homebrew/anaconda3/etc/profile.d/conda.sh
conda activate 3.10
pip install -r requirements.txt
```

## 现场会用到的命令（代码现场生成后）

```bash
cd ..                         # 回到 code/ 目录
pyright backend test          # 静态类型检查（先于 pytest）
python -m pytest test/ -q     # TDD 的红/绿
cd backend
python export_openapi.py      # 更新 openapi.json
uvicorn app:app --reload      # 起服务 + 静态前端
# http://127.0.0.1:8000/              —— 前端 SPA
# http://127.0.0.1:8000/openapi.json  —— 机器可读契约
# http://127.0.0.1:8000/docs          —— 交互式文档
```

## 文件

| 文件 | 作用 | 谁产生 |
|---|---|---|
| [../spec/project_overview.md](../spec/project_overview.md) | 项目总览 | 预置 |
| [../spec/auth_spec.md](../spec/auth_spec.md) | 认证 Spec | 预置 |
| [../spec/team_spec.md](../spec/team_spec.md) | 团队 Spec | 预置 |
| [../spec/todo_api_spec.md](../spec/todo_api_spec.md) | 待办 API Spec | **驱动 TDD** |
| [../spec/todo_ui_spec.md](../spec/todo_ui_spec.md) | 前端 UI Spec | 预置 |
| [../spec/workflow.md](../spec/workflow.md) | 工作行为规范 | 预置 |
| `requirements.txt` | 运行环境 | 预置 |
| `app.py` / `openapi.json` | 实现 / 契约 | **现场生成** |
| [../test/test_*.py](../test/) | API 测试 | **现场生成** |

> 课前请用同一套 spec 自己现场跑一遍，把产物存进 `_backup_现场产物/`（git 忽略）当断网后备——后备也是过程生成的，不是手写的。
