# 🚀 GitHub 上传指南

## 📋 上传前检查清单

### ✅ 文件整理
- [x] 项目结构已整理
- [x] 文档已移动到 `docs/` 目录
- [x] 脚本已移动到 `scripts/` 目录
- [x] 备份文件已移动到 `archive/` 目录
- [x] 版本号已更新为 v1.1
- [x] `.gitignore` 已创建

### ✅ 文档完善
- [x] README.md 已更新
- [x] CHANGELOG.md 已创建
- [x] PROJECT_STRUCTURE.md 已创建
- [x] LICENSE 文件存在

### ✅ 代码检查
- [x] 语法检查通过
- [x] 版本号一致（v1.1）
- [x] 注释完整
- [x] 无敏感信息

---

## 🎯 上传步骤

### 1. 初始化 Git（如果还没有）

```bash
cd /Users/a1/PythonProject
git init
```

### 2. 配置 Git 用户信息

```bash
git config user.name "你的用户名"
git config user.email "你的邮箱"
```

### 3. 添加所有文件

```bash
# 查看将要添加的文件
git status

# 添加所有文件
git add .

# 查看暂存的文件
git status
```

### 4. 提交到本地仓库

```bash
git commit -m "v1.1.0: 添加自定义间隔、统计功能和优化提醒方式

新增功能：
- 自定义提醒间隔（30分钟、45分钟、1小时、2小时或自定义）
- 使用统计功能（记录提醒次数、活动次数、活动率）
- 优化的提醒方式（三个清晰按钮，更友好）
- 配置持久化（自动保存和加载）

改进：
- 修复线程安全问题
- 完善错误处理和日志系统
- 优化菜单结构
- 模块化代码设计

文档：
- 更新 README.md
- 添加 CHANGELOG.md
- 添加 PROJECT_STRUCTURE.md
- 整理项目结构"
```

### 5. 在 GitHub 上创建仓库

1. 登录 GitHub
2. 点击右上角的 "+" → "New repository"
3. 填写信息：
   - Repository name: `sedentary-reminder`
   - Description: `一个智能的 macOS 久坐提醒工具，通过摄像头检测帮你养成健康的工作习惯`
   - Public（公开）或 Private（私有）
   - **不要**勾选 "Initialize this repository with a README"
4. 点击 "Create repository"

### 6. 关联远程仓库

```bash
# 替换为你的 GitHub 用户名
git remote add origin https://github.com/你的用户名/sedentary-reminder.git

# 查看远程仓库
git remote -v
```

### 7. 推送到 GitHub

```bash
# 设置主分支名称为 main
git branch -M main

# 推送到 GitHub
git push -u origin main
```

如果需要输入用户名和密码：
- 用户名：你的 GitHub 用户名
- 密码：使用 Personal Access Token（不是账号密码）

### 8. 创建 Personal Access Token（如果需要）

1. GitHub 右上角头像 → Settings
2. 左侧菜单最下方 → Developer settings
3. Personal access tokens → Tokens (classic)
4. Generate new token (classic)
5. 勾选 `repo` 权限
6. 生成后复制 token（只显示一次）
7. 在推送时使用 token 作为密码

---

## 🏷️ 创建 Release

### 1. 在 GitHub 上创建 Release

1. 进入你的仓库页面
2. 点击右侧的 "Releases"
3. 点击 "Create a new release"
4. 填写信息：
   - Tag version: `v1.1.0`
   - Release title: `v1.1.0 - 自定义间隔和统计功能`
   - Description: 复制 CHANGELOG.md 中 v1.1.0 的内容
5. 点击 "Publish release"

### 2. Release 描述模板

```markdown
## ✨ v1.1.0 新功能

### 主要更新
- 🎯 **自定义提醒间隔** - 支持任意时间设置
- 📊 **使用统计** - 记录和展示使用数据
- 💬 **优化提醒** - 更友好的交互方式
- 💾 **配置保存** - 设置自动保存

### 改进
- 🔧 修复线程安全问题
- 📝 完善日志系统
- 🎨 优化菜单结构

### 安装方式

**从源码运行：**
\`\`\`bash
git clone https://github.com/你的用户名/sedentary-reminder.git
cd sedentary-reminder
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python maincharacter.py
\`\`\`

**详细文档：**
- [功能说明](docs/v1.1功能说明.md)
- [测试指南](docs/v1.1测试指南.md)
- [更新日志](CHANGELOG.md)

### 系统要求
- macOS 12.0+
- Python 3.8+
- 摄像头

---

**完整更新日志：** [CHANGELOG.md](CHANGELOG.md)
```

---

## 📝 后续维护

### 日常提交

```bash
# 1. 修改代码后
git add .
git commit -m "描述你的修改"
git push

# 2. 提交信息格式建议
# feat: 新功能
# fix: 修复bug
# docs: 文档更新
# style: 代码格式调整
# refactor: 重构
# test: 测试相关
# chore: 构建/工具相关
```

### 创建新版本

```bash
# 1. 更新版本号
# - maincharacter.py 中的版本号
# - CHANGELOG.md 添加新版本记录
# - README.md 更新功能说明

# 2. 提交更改
git add .
git commit -m "v1.2.0: 新版本描述"
git push

# 3. 创建 tag
git tag -a v1.2.0 -m "v1.2.0 release"
git push origin v1.2.0

# 4. 在 GitHub 上创建 Release
```

### 分支管理

```bash
# 创建功能分支
git checkout -b feature/new-feature

# 开发完成后合并
git checkout main
git merge feature/new-feature
git push

# 删除分支
git branch -d feature/new-feature
```

---

## 🔍 验证上传

### 检查 GitHub 仓库

1. 访问你的仓库页面
2. 确认文件都已上传
3. 检查 README.md 显示正常
4. 查看 commit 历史

### 克隆测试

```bash
# 在另一个目录测试克隆
cd /tmp
git clone https://github.com/你的用户名/sedentary-reminder.git
cd sedentary-reminder
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python maincharacter.py
```

---

## ⚠️ 注意事项

### 不要上传的文件（已在 .gitignore 中）

- ❌ `.venv/` - 虚拟环境
- ❌ `__pycache__/` - Python 缓存
- ❌ `.idea/` - IDE 配置
- ❌ `.workbuddy/` - 工作记录
- ❌ `archive/` - 归档文件
- ❌ `.sedentary_reminder/` - 用户数据
- ❌ `*.log` - 日志文件

### 敏感信息检查

- ❌ 不要上传个人配置文件
- ❌ 不要上传 API 密钥
- ❌ 不要上传用户数据
- ❌ 不要上传日志文件

### 文件大小

- GitHub 单个文件限制：100MB
- 仓库大小建议：< 1GB
- 如果有大文件，使用 Git LFS

---

## 🎨 美化仓库

### 添加 Badges

在 README.md 顶部添加徽章：

```markdown
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![macOS](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)
```

### 添加截图

1. 在 `screenshots/` 目录添加更多截图
2. 在 README.md 中引用
3. 提交并推送

### 设置 GitHub Pages（可选）

1. 仓库 Settings → Pages
2. Source 选择 main 分支
3. 可以创建项目网站

---

## 📞 遇到问题？

### 常见问题

**Q: 推送时提示权限错误？**
A: 使用 Personal Access Token 而不是密码

**Q: 文件太大无法上传？**
A: 检查 .gitignore，确保大文件被忽略

**Q: 如何撤销提交？**
```bash
# 撤销最后一次提交（保留修改）
git reset --soft HEAD^

# 撤销最后一次提交（丢弃修改）
git reset --hard HEAD^
```

**Q: 如何修改提交信息？**
```bash
# 修改最后一次提交信息
git commit --amend -m "新的提交信息"
git push --force
```

---

## ✅ 完成！

上传完成后，你的项目就在 GitHub 上了！

**下一步：**
- 📝 完善 README.md
- 📸 添加更多截图
- 🏷️ 创建 Release
- 📢 分享你的项目

**项目地址：**
`https://github.com/你的用户名/sedentary-reminder`

---

祝你的项目获得更多 ⭐️ Star！
