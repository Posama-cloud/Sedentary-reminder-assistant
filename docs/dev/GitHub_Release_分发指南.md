# GitHub Release 分发指南 - py2app 版本

## 🎯 目标
打包一个可以在 GitHub Release 上分发、其他用户下载后能直接运行的 macOS 应用。

---

## ⚠️ 核心问题

**为什么之前的版本打不开？**

macOS 的 Gatekeeper 安全机制会阻止：
1. **未签名的应用** - 没有开发者证书签名
2. **带隔离属性的应用** - 从网上下载的文件会被标记

---

## 🔧 完整解决方案

### 方案一：正式签名（推荐，但需要开发者账号）

#### 1. 准备工作
```bash
# 检查是否有开发者证书
security find-identity -v -p codesigning

# 如果没有，需要：
# 1. 注册 Apple Developer Program ($99/年)
# 2. 在 Xcode 中下载开发者证书
```

#### 2. 打包并签名
```bash
# 清理旧构建
rm -rf build dist

# 打包
python setup.py py2app

# 签名应用
codesign --deep --force --sign "Developer ID Application: Your Name (TEAM_ID)" \
  --options runtime \
  --entitlements config/entitlements.plist \
  dist/久坐提醒助手.app

# 验证签名
codesign -dv --verbose=4 dist/久坐提醒助手.app
spctl -a -vv dist/久坐提醒助手.app
```

#### 3. 公证（Notarization）
```bash
# 压缩应用
ditto -c -k --keepParent dist/久坐提醒助手.app 久坐提醒助手.zip

# 上传公证
xcrun notarytool submit 久坐提醒助手.zip \
  --apple-id "your@email.com" \
  --password "app-specific-password" \
  --team-id "TEAM_ID" \
  --wait

# 装订公证票据
xcrun stapler staple dist/久坐提醒助手.app

# 验证
spctl -a -vv dist/久坐提醒助手.app
```

#### 4. 分发
```bash
# 重新压缩已公证的应用
cd dist
zip -r ../久坐提醒助手_v1.1_signed.zip 久坐提醒助手.app

# 上传到 GitHub Release
```

---

### 方案二：临时签名 + 用户手动授权（免费，但用户体验差）

这是你当前的方案，用户需要手动操作才能运行。

#### 1. 打包
```bash
# 清理
rm -rf build dist

# 打包（会自动使用 adhoc 签名）
python setup.py py2app
```

#### 2. 移除隔离属性（重要！）
```bash
# 在打包机器上移除隔离属性
xattr -cr dist/久坐提醒助手.app

# 压缩
cd dist
zip -r ../久坐提醒助手_v1.1.zip 久坐提醒助手.app
```

#### 3. 在 README 中添加用户说明
用户下载后需要执行：
```bash
# 方法 1: 移除隔离属性
xattr -cr /path/to/久坐提醒助手.app

# 方法 2: 右键打开
# 1. 右键点击应用
# 2. 选择"打开"
# 3. 在弹出的对话框中点击"打开"

# 方法 3: 系统设置
# 1. 尝试打开应用（会被阻止）
# 2. 打开"系统设置" → "隐私与安全性"
# 3. 找到被阻止的应用，点击"仍要打开"
```

---

### 方案三：使用 DMG 分发（推荐，免费且用户体验好）

DMG 格式更专业，用户体验更好。

#### 1. 安装工具
```bash
brew install create-dmg
```

#### 2. 创建 DMG
```bash
# 打包应用
rm -rf build dist
python setup.py py2app

# 移除隔离属性
xattr -cr dist/久坐提醒助手.app

# 创建 DMG
create-dmg \
  --volname "久坐提醒助手" \
  --volicon "assets/icons/app_icon.icns" \
  --window-pos 200 120 \
  --window-size 600 400 \
  --icon-size 100 \
  --icon "久坐提醒助手.app" 175 190 \
  --hide-extension "久坐提醒助手.app" \
  --app-drop-link 425 190 \
  --no-internet-enable \
  "久坐提醒助手_v1.1.dmg" \
  "dist/久坐提醒助手.app"
```

#### 3. 用户使用
```bash
# 用户下载 DMG 后：
# 1. 双击挂载 DMG
# 2. 拖拽应用到 Applications 文件夹
# 3. 首次打开时右键选择"打开"
```

---

## 📝 当前 setup.py 配置检查

### ✅ 已经正确配置的：

```python
# 1. 源代码路径
APP = ['src/maincharacter.py']  # ✅ 正确

# 2. 资源文件
DATA_FILES = [('', ['assets/images/image_0.png'])]  # ✅ 正确

# 3. plist 配置
'plist': {
    'CFBundleIdentifier': 'com.sedentary.reminder',  # ✅ 正确
    'LSUIElement': True,  # ✅ 菜单栏应用
    'NSCameraUsageDescription': '...',  # ✅ 摄像头权限
}

# 4. 完整打包模式
# 'alias': True,  # ✅ 已注释，使用完整打包
```

### ⚠️ 需要注意的：

1. **entitlements.plist** - 如果要正式签名，需要配置
2. **图标文件** - 建议创建 .icns 格式的图标

---

## 🚀 推荐流程（针对你的情况）

### 如果你没有开发者账号（$99/年）

**使用方案二 + 方案三的组合：**

```bash
# 1. 清理并重新打包
rm -rf build dist
python setup.py py2app

# 2. 移除隔离属性
xattr -cr dist/久坐提醒助手.app

# 3. 创建 ZIP（简单分发）
cd dist
zip -r ../releases/v1.1/久坐提醒助手_v1.1.zip 久坐提醒助手.app
cd ..

# 4. 创建 DMG（专业分发）
create-dmg \
  --volname "久坐提醒助手" \
  --window-size 600 400 \
  --icon-size 100 \
  --app-drop-link 425 190 \
  "releases/v1.1/久坐提醒助手_v1.1.dmg" \
  "dist/久坐提醒助手.app"

# 5. 上传到 GitHub Release
# - 久坐提醒助手_v1.1.zip
# - 久坐提醒助手_v1.1.dmg
```

### 在 README 中添加说明

```markdown
## 下载和安装

### 下载
从 [Releases](https://github.com/your-repo/releases) 下载最新版本：
- `久坐提醒助手_v1.1.dmg` - 推荐，拖拽安装
- `久坐提醒助手_v1.1.zip` - 解压即用

### 首次运行

**重要：由于应用未经过 Apple 公证，首次运行需要手动授权**

#### 方法一：右键打开（推荐）
1. 右键点击应用
2. 选择"打开"
3. 在弹出的对话框中点击"打开"

#### 方法二：命令行授权
```bash
xattr -cr /Applications/久坐提醒助手.app
```

#### 方法三：系统设置
1. 尝试打开应用（会被阻止）
2. 打开"系统设置" → "隐私与安全性"
3. 找到被阻止的应用，点击"仍要打开"

### 为什么需要这些步骤？
- 应用使用临时签名（adhoc），未经过 Apple 公证
- macOS Gatekeeper 会阻止未知来源的应用
- 这是正常的安全机制，授权后即可正常使用
```

---

## 🔒 如果将来要正式签名

### 1. 注册 Apple Developer Program
- 费用：$99/年
- 网址：https://developer.apple.com/programs/

### 2. 获取证书
```bash
# 在 Xcode 中：
# Preferences → Accounts → Manage Certificates → + → Developer ID Application
```

### 3. 更新 entitlements.plist
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
    <true/>
    <key>com.apple.security.cs.disable-library-validation</key>
    <true/>
    <key>com.apple.security.device.camera</key>
    <true/>
</dict>
</plist>
```

### 4. 签名和公证
使用方案一的完整流程。

---

## 📊 三种方案对比

| 方案 | 成本 | 用户体验 | 安全性 | 推荐度 |
|------|------|---------|--------|--------|
| 正式签名+公证 | $99/年 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 临时签名+用户授权 | 免费 | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| DMG分发 | 免费 | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## ✅ 当前配置总结

你的 setup.py 配置是**正确的**，可以打包出符合 macOS 应用框架的 .app。

**问题不在配置，而在签名和分发方式。**

建议：
1. ✅ 使用当前的 setup.py（已经正确）
2. ✅ 打包后移除隔离属性
3. ✅ 使用 DMG 分发（提升用户体验）
4. ✅ 在 README 中说明首次运行需要右键打开

这样用户下载后虽然需要手动授权一次，但之后就能正常使用了。
