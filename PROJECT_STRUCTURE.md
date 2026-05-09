# 📁 项目结构说明

## 目录结构

```
久坐提醒助手/
├── maincharacter.py          # 主程序 (v1.1)
├── test_quick.py             # 快速测试版本 (10秒倒计时)
├── image_0.png               # 应用图标
├── requirements.txt          # Python 依赖
├── LICENSE                   # MIT 许可证
├── README.md                 # 项目说明
├── .gitignore               # Git 忽略文件
│
├── screenshots/              # 截图目录
│   └── app-icon.png         # 应用图标
│
├── scripts/                  # 脚本目录
│   ├── install.sh           # 安装脚本
│   ├── run_test.sh          # 快速测试脚本
│   └── view_log.sh          # 查看日志脚本
│
├── docs/                     # 文档目录
│   ├── v1.1功能说明.md      # v1.1 功能详细说明
│   ├── v1.1测试指南.md      # v1.1 测试步骤
│   ├── v1.1完成总结.md      # v1.1 开发总结
│   ├── 快速开始.md          # 快速开始指南
│   ├── 测试指南.md          # 通用测试指南
│   ├── 紧急修复说明.md      # 线程安全问题修复说明
│   └── 修复总结.md          # 问题修复总结
│
└── archive/                  # 归档目录
    ├── maincharacter_backup.py  # v1.0 备份
    └── 久坐提醒助手-v1.0.zip    # v1.0 打包版本
```

## 文件说明

### 核心文件

| 文件 | 说明 |
|------|------|
| `maincharacter.py` | 主程序，1小时倒计时，正式使用 |
| `test_quick.py` | 测试版本，10秒倒计时，快速测试 |
| `image_0.png` | 应用图标，显示在菜单栏 |
| `requirements.txt` | Python 依赖列表 |

### 脚本文件

| 文件 | 说明 |
|------|------|
| `scripts/install.sh` | 一键安装脚本，打包并配置开机自启 |
| `scripts/run_test.sh` | 快速启动测试版本 |
| `scripts/view_log.sh` | 实时查看日志 |

### 文档文件

| 文件 | 说明 |
|------|------|
| `docs/v1.1功能说明.md` | v1.1 版本的详细功能说明 |
| `docs/v1.1测试指南.md` | v1.1 版本的完整测试步骤 |
| `docs/v1.1完成总结.md` | v1.1 版本的开发总结 |
| `docs/快速开始.md` | 最简洁的使用指南 |
| `docs/测试指南.md` | 通用测试指南 |
| `docs/紧急修复说明.md` | 线程安全问题的修复说明 |
| `docs/修复总结.md` | 问题修复的详细总结 |

### 配置和数据文件（运行时生成）

| 文件 | 位置 | 说明 |
|------|------|------|
| `config.json` | `~/.sedentary_reminder/` | 用户配置文件 |
| `stats.json` | `~/.sedentary_reminder/` | 统计数据文件 |
| `app.log` | `~/Library/Logs/久坐提醒助手/` | 日志文件 |
| `test.log` | `~/Library/Logs/久坐提醒助手/` | 测试版本日志 |

## 版本说明

### v1.1 (当前版本)
- ✅ 自定义提醒间隔
- ✅ 使用统计功能
- ✅ 优化的提醒方式
- ✅ 配置持久化
- ✅ 线程安全修复

### v1.0 (已归档)
- 基础功能：定时检测和提醒
- 固定1小时间隔
- 简单的提醒对话框

### v2.0 (规划中)
- 跨平台支持（Windows + macOS）
- 使用 pystray + tkinter 重构
- 统一的用户体验

## 使用指南

### 快速开始
```bash
# 安装依赖
pip install -r requirements.txt

# 运行主程序
python maincharacter.py

# 或运行测试版本（10秒倒计时）
python test_quick.py
```

### 使用脚本
```bash
# 快速测试
./scripts/run_test.sh

# 查看日志
./scripts/view_log.sh

# 安装为应用
./scripts/install.sh
```

## Git 管理

### 忽略的文件
- `.venv/` - 虚拟环境
- `__pycache__/` - Python 缓存
- `.idea/` - IDE 配置
- `.workbuddy/` - 工作记录
- `archive/` - 归档文件
- `.sedentary_reminder/` - 用户数据

### 提交到 GitHub
```bash
# 初始化（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "v1.1: 添加自定义间隔、统计功能和优化提醒方式"

# 推送到 GitHub
git remote add origin https://github.com/你的用户名/sedentary-reminder.git
git branch -M main
git push -u origin main
```

## 开发指南

### 添加新功能
1. 在 `maincharacter.py` 中开发
2. 同步更新 `test_quick.py`（如果需要）
3. 更新文档
4. 测试验证
5. 提交代码

### 文档规范
- 功能说明放在 `docs/`
- 使用 Markdown 格式
- 包含代码示例和截图
- 保持版本号一致

### 测试流程
1. 运行 `test_quick.py` 快速验证
2. 运行 `maincharacter.py` 完整测试
3. 检查日志无错误
4. 验证配置和统计数据

## 常见问题

### Q: 为什么有两个 Python 文件？
A: `maincharacter.py` 是正式版本（1小时），`test_quick.py` 是测试版本（10秒），方便快速测试功能。

### Q: archive 目录是什么？
A: 存放旧版本的备份文件，不会提交到 GitHub。

### Q: 为什么要分 docs 和 scripts 目录？
A: 保持项目结构清晰，便于维护和查找。

### Q: 用户数据会提交到 GitHub 吗？
A: 不会，`.gitignore` 已经排除了 `.sedentary_reminder/` 目录。

## 贡献指南

欢迎提交 Issue 和 Pull Request！

### 提交 Issue
- 描述问题或建议
- 提供日志文件（如果是 bug）
- 说明操作系统版本

### 提交 PR
- Fork 项目
- 创建功能分支
- 提交清晰的 commit message
- 更新相关文档
- 通过测试

## 许可证

MIT License - 详见 LICENSE 文件
