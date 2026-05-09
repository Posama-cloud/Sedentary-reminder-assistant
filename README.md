# 久坐提醒助手 v1.1

<div align="center">

![应用图标](./screenshots/app-icon.png)

一个智能的 macOS 久坐提醒工具，通过摄像头检测帮你养成健康的工作习惯。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![macOS](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)

[功能特点](#功能特点) • [快速开始](#快速开始) • [使用说明](#使用说明) • [文档](#文档) • [贡献](#贡献)

</div>

---

## 功能特点

### v1.1 新功能
- **自定义提醒间隔** - 支持 30 分钟、45 分钟、1 小时、2 小时，或自定义任意时间
- **使用统计** - 记录提醒次数、活动次数，计算活动率，激励你保持健康习惯
- **友好的提醒方式** - 三个清晰按钮（我知道了、10分钟后提醒、跳过本次），不再强制
- **配置持久化** - 所有设置自动保存，重启后保持

### 核心功能
- **智能检测** - 使用摄像头人脸检测，准确判断是否久坐
- **定时提醒** - 到时间自动检测，有人则提醒，无人则自动重置
- **隐私安全** - 纯本地运行，不联网，不上传任何数据
- **简洁界面** - 常驻菜单栏，不占桌面空间
- **详细日志** - 完整的日志记录，方便排查问题

---

## 快速开始

### 方式一：一键安装（推荐）

```bash
# 1. 下载项目
git clone https://github.com/Posama-cloud/Sedentary-reminder-assistant.git
cd Sedentary-reminder-assistant

# 2. 运行安装脚本
chmod +x 一键安装.sh
./一键安装.sh
```

安装完成后，双击桌面的「久坐提醒助手.command」即可启动。

### 方式二：手动安装

```bash
# 1. 克隆项目
git clone https://github.com/Posama-cloud/Sedentary-reminder-assistant.git
cd Sedentary-reminder-assistant

# 2. 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行程序
python maincharacter.py
```

### 方式三：下载打包版本

1. 下载最新版本的 `久坐提醒助手_v1.1.zip`
2. 解压后双击 `久坐提醒助手.app` 即可运行
3. **首次运行时会请求摄像头权限**，这是为了检测您是否在电脑前，请点击"允许"
   - 应用仅在本地使用摄像头进行人脸检测
   - 不会上传或保存任何图像数据
4. 如果 macOS 提示"无法验证开发者"，请按以下步骤操作：
   - 打开"系统偏好设置" → "安全性与隐私"
   - 点击"仍要打开"按钮
   - 或者在终端执行：`xattr -cr /path/to/久坐提醒助手.app`

### 方式四：自己打包（开发者）

如果你想自己打包应用：

```bash
# 1. 安装打包工具
pip install py2app

# 2. 一键打包
./build.sh

# 3. 运行打包后的应用
open dist/久坐提醒助手.app
```

详细说明请查看 [py2app 打包说明](docs/py2app打包说明.md)

---

## 使用说明

### 首次使用

1. **启动程序**
   - 运行后会在菜单栏显示图标
   - 首次启动会显示欢迎提示

2. **授予摄像头权限（重要）**
   - 系统会弹出摄像头权限请求，**必须点击"允许"**
   - 权限说明：应用需要访问摄像头来检测您是否在电脑前，以便准确提醒您休息
   - **隐私保证**：摄像头仅用于本地检测，不会上传或保存任何图像
   - 如果没有弹出权限请求，请前往"系统设置 > 隐私与安全性 > 摄像头"手动授权

3. **设置提醒间隔**
   - 点击菜单栏图标
   - 选择"设置提醒间隔"
   - 选择合适的时间或自定义

### 日常使用

**菜单选项：**
- **设置提醒间隔** - 自定义提醒时间
- **重置计时器** - 手动重置倒计时
- **立即测试检测** - 测试摄像头检测功能
- **查看统计** - 查看使用统计数据
- **查看日志** - 打开日志文件
- **关于** - 查看版本信息

**提醒对话框：**
- **我知道了** - 30秒后再次确认是否还在座位上
- **10分钟后提醒** - 延迟10分钟后再提醒
- **跳过本次** - 跳过本次提醒，直接开始下一轮倒计时

### 统计功能

查看统计可以了解：
- 今日提醒次数和活动次数
- 累计提醒次数和活动次数
- 活动率（活动次数 / 提醒次数）

**建议目标：活动率 > 80%**

---

## 系统要求

- **操作系统**: macOS 12.0 或更高版本
- **Python**: 3.8 或更高版本（从源码运行时）
- **硬件**: 内置或外接摄像头
- **权限**: 摄像头访问权限

---

## 配置说明

### 配置文件位置

- **用户配置**: `~/.sedentary_reminder/config.json`
- **统计数据**: `~/.sedentary_reminder/stats.json`
- **日志文件**: `~/Library/Logs/久坐提醒助手/app.log`

### 配置选项

```json
{
  "interval_seconds": 3600,    // 提醒间隔（秒）
  "show_welcome": true,        // 是否显示欢迎提示
  "confirm_delay": 30          // 确认延迟时间（秒）
}
```

### 高级配置

如果需要修改默认行为，可以编辑 `maincharacter.py` 中的常量：

```python
DEFAULT_INTERVAL_SECONDS = 3600  # 默认间隔（秒）
CONFIRM_DELAY_SECONDS = 30       # 确认延迟（秒）
CONFIRM_FRAMES = 5               # 检测帧数
```

---

## 文档

- [v1.1 功能说明](docs/v1.1功能说明.md) - 详细的功能介绍
- [v1.1 测试指南](docs/v1.1测试指南.md) - 完整的测试步骤
- [快速开始](docs/快速开始.md) - 最简洁的使用指南
- [项目结构](PROJECT_STRUCTURE.md) - 项目文件结构说明

---

## 测试

### 快速测试（10秒倒计时）

```bash
python test_quick.py
```

或使用脚本：

```bash
./scripts/run_test.sh
```

### 查看日志

```bash
./scripts/view_log.sh
```

或手动打开：

```bash
tail -f ~/Library/Logs/久坐提醒助手/app.log
```

---

## 卸载

### 卸载应用

```bash
# 停止并移除开机自启动
launchctl unload ~/Library/LaunchAgents/com.yourname.sedentary-reminder.plist
rm ~/Library/LaunchAgents/com.yourname.sedentary-reminder.plist

# 删除应用
rm -rf /Applications/久坐提醒助手.app

# 删除用户数据（可选）
rm -rf ~/.sedentary_reminder
rm -rf ~/Library/Logs/久坐提醒助手
```

---

## 已知问题

### 检测准确性
- 光线太暗时准确率下降
- 侧脸、低头可能检测不到
- 戴口罩可能影响检测

### 解决方法
- 保持良好的光线环境
- 正面面对摄像头
- 调整摄像头角度

### 报告问题
如果遇到问题，请：
1. 查看日志文件：`~/Library/Logs/久坐提醒助手/app.log`
2. 提交 [Issue](https://github.com/Posama-cloud/sedentary-reminder/issues)
3. 附上日志和系统信息

---

## 贡献

欢迎贡献代码、报告问题或提出建议！

### 如何贡献

1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 贡献指南

- 遵循现有的代码风格
- 添加必要的注释和文档
- 确保代码通过测试
- 更新相关文档

---

## 技术栈

- **Python 3** - 主要编程语言
- **OpenCV** - 摄像头和图像处理
- **rumps** - macOS 菜单栏 UI 框架
- **py2app** - macOS 专用打包工具

---

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 致谢

感谢所有为这个项目做出贡献的人！

---

## 联系方式

- **GitHub**: [@Posama-cloud](https://github.com/Posama-cloud)
- **Issues**: [提交问题](https://github.com/Posama-cloud/sedentary-reminder/issues)

---

<div align="center">

**如果这个项目对你有帮助，请给个 Star 支持一下！**

Made with love for healthier work habits

</div>
