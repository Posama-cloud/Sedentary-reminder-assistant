# 久坐提醒助手 - 项目目录规范

## 📋 目录结构标准（绝对纲领）

```
PythonProject/
├── src/                          # 源代码目录
│   ├── maincharacter.py          # 主程序
│   └── __init__.py               # Python 包标识
│
├── assets/                       # 资源文件目录
│   ├── icons/                    # 图标文件
│   │   ├── app_icon.icns         # macOS 应用图标
│   │   └── menu_icon.png         # 菜单栏图标
│   └── images/                   # 其他图片
│       └── app-icon.png          # 应用图标（PNG）
│
├── config/                       # 配置文件目录
│   ├── entitlements.plist        # macOS 权限配置
│   └── Info.plist                # 应用信息配置
│
├── scripts/                      # 脚本目录
│   ├── build.sh                  # 打包脚本
│   ├── install.sh                # 安装脚本
│   ├── run_test.sh               # 测试运行脚本
│   └── view_log.sh               # 查看日志脚本
│
├── tests/                        # 测试文件目录
│   ├── test_quick.py             # 快速测试
│   └── __init__.py               # Python 包标识
│
├── docs/                         # 文档目录
│   ├── user/                     # 用户文档
│   │   ├── 快速开始.md
│   │   └── 使用说明.md
│   ├── dev/                      # 开发文档
│   │   ├── py2app打包说明.md
│   │   ├── py2app测试清单.md
│   │   └── 开发指南.md
│   ├── release/                  # 发布文档
│   │   ├── v1.1功能说明.md
│   │   ├── v1.1测试指南.md
│   │   └── CHANGELOG.md
│   └── archive/                  # 归档文档
│       ├── 紧急修复说明.md
│       ├── 修复总结.md
│       ├── v1.1完成总结.md
│       ├── 整理完成总结.md
│       ├── 测试指南.md
│       └── 故障排查记录.md
│
├── releases/                     # 发布文件目录
│   ├── v1.0/
│   │   └── 久坐提醒助手-v1.0.zip
│   ├── v1.1/
│   │   ├── 久坐提醒助手_v1.1.zip
│   │   └── 久坐提醒助手_v1.1_fixed.zip
│   └── latest -> v1.1            # 软链接指向最新版本
│
├── archive/                      # 归档目录（旧代码、旧配置）
│   ├── maincharacter_backup.py
│   └── 久坐提醒助手.spec         # PyInstaller 配置（已废弃）
│
├── build/                        # 构建临时文件（不提交到 git）
├── dist/                         # 打包输出目录（不提交到 git）
│
├── .venv/                        # 虚拟环境（不提交到 git）
├── __pycache__/                  # Python 缓存（不提交到 git）
│
├── setup.py                      # py2app 打包配置
├── requirements.txt              # Python 依赖
├── .gitignore                    # Git 忽略配置
├── README.md                     # 项目说明（主文档）
├── LICENSE                       # 开源协议
├── CHANGELOG.md                  # 版本更新日志
├── PROJECT_STRUCTURE.md          # 项目结构说明（本文件）
└── 一键安装.sh                   # 用户安装脚本
```

---

## 📐 目录规范说明

### 1. 源代码目录 `src/`
**用途**: 存放所有 Python 源代码  
**规则**:
- ✅ 所有 `.py` 源文件必须放在这里
- ✅ 必须包含 `__init__.py`
- ❌ 不允许放配置文件、文档、资源文件

### 2. 资源文件目录 `assets/`
**用途**: 存放所有静态资源  
**规则**:
- ✅ 图标放在 `assets/icons/`
- ✅ 图片放在 `assets/images/`
- ✅ 其他资源按类型分类
- ❌ 不允许放代码、文档

### 3. 配置文件目录 `config/`
**用途**: 存放应用配置文件  
**规则**:
- ✅ `.plist` 文件放这里
- ✅ 其他配置文件（如 `.ini`, `.yaml`）也放这里
- ❌ 不允许放代码、文档

### 4. 脚本目录 `scripts/`
**用途**: 存放各种自动化脚本  
**规则**:
- ✅ 所有 `.sh` 脚本放这里
- ✅ 脚本必须有执行权限 (`chmod +x`)
- ✅ 脚本必须有清晰的注释说明用途
- ❌ 不允许放源代码、测试代码

### 5. 测试目录 `tests/`
**用途**: 存放所有测试代码  
**规则**:
- ✅ 测试文件以 `test_` 开头
- ✅ 必须包含 `__init__.py`
- ❌ 不允许放源代码、脚本

### 6. 文档目录 `docs/`
**用途**: 存放所有文档  
**规则**:
- ✅ 用户文档放在 `docs/user/`
- ✅ 开发文档放在 `docs/dev/`
- ✅ 发布文档放在 `docs/release/`
- ✅ 过期文档放在 `docs/archive/`
- ❌ 不允许在根目录放 `.md` 文档（除了 README.md, LICENSE, CHANGELOG.md）

### 7. 发布目录 `releases/`
**用途**: 存放所有发布的打包文件  
**规则**:
- ✅ 按版本号分目录（v1.0, v1.1, ...）
- ✅ 每个版本目录只放该版本的发布文件
- ✅ 使用软链接 `latest` 指向最新版本
- ❌ 不允许在根目录放 `.zip` 文件

### 8. 归档目录 `archive/`
**用途**: 存放废弃的代码、配置  
**规则**:
- ✅ 不再使用但需要保留的文件放这里
- ✅ 文件名应包含归档日期或版本号
- ❌ 不允许放当前使用的文件

### 9. 构建目录 `build/` 和 `dist/`
**用途**: 打包工具生成的临时文件和输出  
**规则**:
- ✅ 必须在 `.gitignore` 中忽略
- ✅ 可以随时删除和重新生成
- ❌ 不允许手动放文件

### 10. 根目录
**用途**: 只放核心配置文件和主文档  
**规则**:
- ✅ 允许的文件：
  - `setup.py` - 打包配置
  - `requirements.txt` - 依赖配置
  - `.gitignore` - Git 配置
  - `README.md` - 项目说明
  - `LICENSE` - 开源协议
  - `CHANGELOG.md` - 版本日志
  - `PROJECT_STRUCTURE.md` - 项目结构说明
  - `一键安装.sh` - 用户安装脚本（特殊）
- ❌ 不允许的文件：
  - 其他 `.md` 文档（应放在 `docs/`）
  - `.zip` 文件（应放在 `releases/`）
  - `.spec` 文件（应放在 `archive/`）
  - `.plist` 文件（应放在 `config/`）
  - 图片文件（应放在 `assets/`）
  - 其他脚本（应放在 `scripts/`）

---

## 🔧 .gitignore 规范

必须忽略的内容：

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# 虚拟环境
.venv/
venv/
ENV/
env/

# 构建产物
build/
dist/
*.egg-info/

# macOS
.DS_Store
.AppleDouble
.LSOverride

# IDE
.vscode/
.idea/
*.swp
*.swo

# 日志
*.log

# 临时文件
*.tmp
*.bak
*~
```

---

## 📝 文件命名规范

### Python 文件
- ✅ 使用小写字母和下划线：`main_character.py`
- ❌ 不使用驼峰命名：`mainCharacter.py`
- ❌ 不使用中文：`主程序.py`

### 脚本文件
- ✅ 使用小写字母和下划线：`build_app.sh`
- ✅ 功能清晰：`install.sh`, `test.sh`

### 文档文件
- ✅ 中文文档可以用中文命名：`快速开始.md`
- ✅ 英文文档用小写和连字符：`quick-start.md`
- ✅ 版本号格式：`v1.1功能说明.md`

### 发布文件
- ✅ 格式：`应用名_版本号.zip`
- ✅ 示例：`久坐提醒助手_v1.1.zip`
- ✅ 修复版本：`久坐提醒助手_v1.1_fixed.zip`

---

## 🚀 setup.py 配置规范

打包配置必须遵循以下规则：

```python
# 源代码
APP = ['src/maincharacter.py']

# 资源文件
DATA_FILES = [
    ('', ['assets/images/menu_icon.png']),
]

# 图标
ICON_FILE = 'assets/icons/app_icon.icns'

# plist 配置
PLIST_FILE = 'config/Info.plist'
```

---

## 📦 打包流程规范

### 1. 开发阶段
```bash
# 在项目根目录
python src/maincharacter.py
```

### 2. 测试阶段
```bash
# 运行测试
python -m pytest tests/

# 快速测试
python tests/test_quick.py
```

### 3. 打包阶段
```bash
# 使用脚本打包
./scripts/build.sh

# 或手动打包
python setup.py py2app
```

### 4. 发布阶段
```bash
# 创建版本目录
mkdir -p releases/v1.2

# 压缩应用
cd dist
zip -r ../releases/v1.2/久坐提醒助手_v1.2.zip 久坐提醒助手.app

# 更新 latest 链接
cd ../releases
rm -f latest
ln -s v1.2 latest
```

---

## ⚠️ 违规处理

如果发现不符合规范的文件：

1. **立即停止工作**
2. **按照规范重新整理**
3. **更新相关文档**
4. **提交整理记录**

---

## 📅 维护规范

### 每次开发前
- [ ] 检查目录结构是否符合规范
- [ ] 清理临时文件（`rm -rf build dist __pycache__`）
- [ ] 更新依赖（`pip install -r requirements.txt`）

### 每次提交前
- [ ] 检查是否有文件放错位置
- [ ] 检查 `.gitignore` 是否正确
- [ ] 运行测试确保功能正常
- [ ] 更新 CHANGELOG.md

### 每次发布前
- [ ] 更新版本号
- [ ] 更新文档
- [ ] 完整测试
- [ ] 按规范打包和归档

---

## 🎯 总结

**核心原则：**
1. **分类明确** - 每种文件都有固定位置
2. **层次清晰** - 目录结构一目了然
3. **易于维护** - 新文件知道放哪里
4. **便于协作** - 团队成员都能理解

**记住：**
- 源代码 → `src/`
- 资源文件 → `assets/`
- 配置文件 → `config/`
- 脚本文件 → `scripts/`
- 测试文件 → `tests/`
- 文档文件 → `docs/`（分类）
- 发布文件 → `releases/`（按版本）
- 废弃文件 → `archive/`
- 根目录 → 只放核心配置和主文档

**这是绝对的纲领，任何修改都必须遵循！**
