# py2app 打包说明

## 快速开始

### 1. 安装 py2app

```bash
pip install py2app
```

### 2. 一键打包

```bash
./build.sh
```

脚本会引导你选择：
- **开发模式** - 快速打包，用于测试（需要 Python 环境）
- **发布模式** - 完整打包，用于分发（独立运行）

### 3. 手动打包

```bash
# 清理旧构建
rm -rf build dist

# 开发模式（快速，用于测试）
python setup.py py2app -A

# 发布模式（完整打包，用于分发）
python setup.py py2app
```

## 运行应用

```bash
# 方式 1: 双击运行
open dist/久坐提醒助手.app

# 方式 2: 命令行运行（可以看到日志）
dist/久坐提醒助手.app/Contents/MacOS/久坐提醒助手
```

## 分发应用

发布模式打包后，可以直接分发：

```bash
# 压缩应用
cd dist
zip -r 久坐提醒助手_v1.1.zip 久坐提醒助手.app

# 或创建 DMG（需要安装 create-dmg）
# brew install create-dmg
# create-dmg --volname "久坐提醒助手" --window-size 600 400 久坐提醒助手.dmg dist/久坐提醒助手.app
```

## 配置说明

### setup.py 主要配置

- **packages**: 明确指定需要打包的 Python 包
  - `cv2` - OpenCV
  - `numpy` - NumPy
  - `PIL` - Pillow
  - `rumps` - 菜单栏框架

- **includes**: 需要包含的模块

- **excludes**: 排除不需要的模块（减小体积）

- **plist**: macOS 应用配置
  - `LSUIElement: True` - 菜单栏应用，不显示在 Dock
  - `NSCameraUsageDescription` - 摄像头权限说明

### 开发模式 vs 发布模式

| 特性 | 开发模式 (-A) | 发布模式 |
|------|--------------|---------|
| 打包速度 | 快（秒级） | 慢（分钟级） |
| 应用大小 | 小（几 MB） | 大（150-200 MB） |
| 依赖 | 需要 Python 环境 | 完全独立 |
| 用途 | 开发测试 | 分发给用户 |

## 常见问题

### 1. 打包后运行报错

```bash
# 查看详细错误信息
dist/久坐提醒助手.app/Contents/MacOS/久坐提醒助手
```

### 2. OpenCV 找不到

确保 setup.py 中包含了 `cv2` 和 `numpy`：

```python
'packages': ['cv2', 'numpy', ...],
```

### 3. 图标不显示

将图标转换为 .icns 格式：

```bash
# 使用 iconutil（macOS 自带）
mkdir AppIcon.iconset
sips -z 16 16     icon.png --out AppIcon.iconset/icon_16x16.png
sips -z 32 32     icon.png --out AppIcon.iconset/icon_16x16@2x.png
sips -z 32 32     icon.png --out AppIcon.iconset/icon_32x32.png
sips -z 64 64     icon.png --out AppIcon.iconset/icon_32x32@2x.png
sips -z 128 128   icon.png --out AppIcon.iconset/icon_128x128.png
sips -z 256 256   icon.png --out AppIcon.iconset/icon_128x128@2x.png
sips -z 256 256   icon.png --out AppIcon.iconset/icon_256x256.png
sips -z 512 512   icon.png --out AppIcon.iconset/icon_256x256@2x.png
sips -z 512 512   icon.png --out AppIcon.iconset/icon_512x512.png
sips -z 1024 1024 icon.png --out AppIcon.iconset/icon_512x512@2x.png
iconutil -c icns AppIcon.iconset
```

### 4. 摄像头权限

首次运行时，macOS 会自动弹出权限请求。如果没有弹出：

1. 打开"系统设置" → "隐私与安全性" → "摄像头"
2. 找到"久坐提醒助手"并勾选

### 5. 应用无法打开（开发者验证）

```bash
# 移除隔离属性
xattr -cr dist/久坐提醒助手.app
```

或在"系统设置" → "隐私与安全性"中点击"仍要打开"。

## 优化建议

### 减小应用体积

1. 排除不需要的模块：

```python
'excludes': [
    'matplotlib',
    'scipy', 
    'pandas',
    'tkinter',
    'test',
    'unittest',
],
```

2. 使用 strip 减小二进制大小：

```bash
find dist/久坐提醒助手.app -name "*.so" -exec strip -x {} \;
```

### 加快启动速度

1. 使用 `site_packages: True`
2. 避免在启动时导入大型库
3. 延迟加载不常用的模块

## 参考资源

- [py2app 官方文档](https://py2app.readthedocs.io/)
- [PyObjC 文档](https://pyobjc.readthedocs.io/)
- [macOS App Bundle 结构](https://developer.apple.com/library/archive/documentation/CoreFoundation/Conceptual/CFBundles/BundleTypes/BundleTypes.html)
