# 个人记账管理系统

## 项目简介

一个基于 Python Tkinter 的本地个人记账桌面应用，支持收入/支出记录、月度目标管理、月度收支统计与图表分析，并可将图表导出为 PNG / PDF。

- **当前版本**：v0.10.2
- **数据存储**：本地 JSON 文件（`records.json` / `goals.json`），无需数据库
- **架构**：UI / 弹窗 / ViewModel / Controller / Service / Model / Storage / Config / 异常 / 日志分层，职责清晰、易于测试

## 功能列表

- **收入/支出记录**：记录日期、类型（收入/支出）、金额、用途备注，自动校验输入
- **月度目标**：为指定月份设置支出目标，实时显示剩余额度与达标/超支状态
- **月度统计**：按月查看总收入、总支出、结余与目标执行情况
- **图表展示**：按用途统计的支出分布水平条形图，支持月份切换与滚轮缩放
- **数据导出**：将当前图表导出为 PNG（300dpi）或 PDF 文件

## 项目结构

```
project1_FinancialManager/
├── 记账程序.py          # UI 层：主窗口 FinanceApp（布局、事件、刷新调度）
├── dialogs.py           # 弹窗层：添加账单 / 设置目标 / 月度统计对话框
├── view_models.py       # View Model 层：为表格与图表准备展示数据
├── reports.py           # 报表导出层：Figure 的 PNG / PDF 导出
├── controller.py        # Controller 层：业务操作编排（校验、模型转换、持久化）
├── services.py          # Service 层：月度统计纯函数（收入/支出/结余/目标）
├── models.py            # Model 层：领域模型（Record / Category / Goal / Goals）
├── storage.py           # Storage 层：JSON 文件读写
├── config.py            # Config 层：AppConfig 配置对象与常量
├── exceptions.py        # 异常层：FinanceError / ValidationError / StorageError
├── logger.py            # 日志层：统一日志实例（控制台 + 文件）
├── tests/               # Tests 层：pytest 测试套件
│   ├── conftest.py          # 共享 fixture 与路径注入
│   ├── test_*.py            # models/storage/services/controller/view_models/dialogs/reports/logger
│   └── stubs/               # 无 GUI 环境下使用的 tkinter / matplotlib 桩
├── README.md            # 项目说明
└── requirements.txt     # 第三方依赖
```

分层调用关系：`UI 层 → 弹窗层 → ViewModel 层 → Controller 层 → Service 层 / Model 层 → Storage 层`，`Config 层` 提供全局配置，`异常层 / 日志层` 贯穿各层。

## 安装说明

**Python 版本要求**：Python 3.8 及以上。

**安装依赖**：

```bash
pip install -r requirements.txt
```

> 说明：`tkinter` 为标准库，但部分 Linux 发行版需单独安装，例如 Debian/Ubuntu 执行 `sudo apt install python3-tk`。Windows 官方 Python 安装包已内置 tkinter。

## 运行说明

在项目根目录执行：

```bash
python 记账程序.py
```

程序启动后弹出主窗口，即可添加账单、设置月度目标、查看统计与图表，并导出图表文件。

## 测试说明

在项目根目录执行：

```bash
pytest tests/
```

测试套件包含 57 个用例，覆盖 models / storage / services / controller / view_models / dialogs / reports / logger 各层，测试在隔离的临时目录中运行，不会读写项目内数据文件。

## 重构历史

| 版本 | 说明 |
|------|------|
| v0.1.0 | 原始版本：单文件 Tkinter 程序 |
| v0.2.0 - v0.8.1 | 分层重构：依次拆出 Storage / Controller / Service / Model / dialogs / view_models / reports / config 各层 |
| v0.9.0 | 工程化测试：迁移为 pytest 测试结构（tests/） |
| v0.9.1 | 项目文档化：README 与依赖说明 |
| v0.10.0 | 统一异常处理：FinanceError / ValidationError / StorageError |
| v0.10.1 | 日志系统：统一 logger（控制台 + 文件） |
| v0.10.2 | 配置对象化：AppConfig 类 + 兼容常量别名 |
| v0.10.3 | Release Cleanup：清理死代码与文档同步 |