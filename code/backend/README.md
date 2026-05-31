# 待办事项 API · 后端（课1 命题演示）

> **代码不在这里——它在课堂上从 [spec](spec/todo_api_spec.md) 现场生成。**
> 这个目录只放：规格（驱动）+ 环境依赖 + 运行说明。`app.py / test_todo_api.py / openapi.json` 都是现场长出来的产物。

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
python -m pytest -q          # TDD 的红/绿；照 spec 生成的实现预期 8 passed
uvicorn app:app --reload     # 起服务
# http://127.0.0.1:8000/openapi.json  —— 机器可读契约 = 前端的 spec
# http://127.0.0.1:8000/docs          —— 交互式文档
```

## 文件

| 文件 | 作用 | 谁产生 |
|---|---|---|
| `spec/todo_api_spec.md` | SDD 产物：人确认的规格 | **你带去（驱动）** |
| `requirements.txt` | 运行环境 | 预置 |
| `app.py` / `test_todo_api.py` / `openapi.json` | 实现 / 测试 / 契约 | **课堂现场生成** |

> 课前请用同一套 spec 自己现场跑一遍，把产物存进 `_backup_现场产物/`（git 忽略）当断网后备——后备也是过程生成的，不是手写的。
