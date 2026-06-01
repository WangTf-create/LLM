# 客座第 1 课 · 用 SDD + TDD 驯服 AI

模块 7「AI Coding 带来的范式变革」第 1 课。2 小时 · 讲师现场演示学员观看。

> **核心原则：代码不预写，课堂上从 spec 用 SDD→TDD 过程现场生成。**
> 这个文件夹放的是"带去课堂的东西"——讲义脚本、驱动用的 spec、演示编排、带走物模板。

## 怎么用

1. **讲义**：[讲义.ipynb](讲义.ipynb)——学员直接阅读的课程正文（VS Code Jupyter 打开）。标 🔴 的环节，现场从规格长出代码。
2. **现场演示**：照 [code/演示脚本.md](code/演示脚本.md) 走，用 [spec](code/spec/project_overview.md) 现场长出后端 → 契约 → 前端。
3. **带走物**：[materials/](materials/) 里 6 份模板，课后带走复现。

## 结构

```
讲义.ipynb                      学员阅读版（19 cell）
code/
  演示脚本.md                   现场生成编排
  spec/
    project_overview.md         项目总览
    workflow.md                 工作行为规范
    auth_spec.md / team_spec.md / todo_api_spec.md / todo_ui_spec.md
  test/                         所有后端 pytest 用例
  backend/
    requirements.txt            环境
    README.md
  frontend/README.md            从契约现场生成 UI 的要点
materials/                      6 份带走物模板
```

## 课前准备

见 [code/演示脚本.md](code/演示脚本.md) 顶部清单：环境就绪、选好 agent、**用同一套 spec 自己现场跑一遍存档当断网后备**（后备也是过程生成的，不手写）。已验证：照这份 spec 生成的实现，测试为 8 passed（spec 自洽可实现）。

## 关联

- 提案（节奏/时间轴/必讲清单）：[提纲提案/客座1](../../提纲提案/客座1_大厂工程师的AI-Coding方法与经验_提纲.md)
- 资料出处：[资料调研/](../../资料调研/)
