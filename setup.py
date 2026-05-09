"""
py2app setup script for 久坐提醒助手
优化版本 - 完整支持 OpenCV 和所有依赖
"""

from setuptools import setup
import os

APP = ['src/maincharacter.py']

# 资源文件
DATA_FILES = []
if os.path.exists('assets/images/image_0.png'):
    DATA_FILES.append(('', ['assets/images/image_0.png']))

# 检查是否有 .icns 图标文件
ICON_FILE = None
for icon_name in ['assets/icons/app_icon.icns', 'assets/icons/icon.icns', 'assets/icons/AppIcon.icns']:
    if os.path.exists(icon_name):
        ICON_FILE = icon_name
        break

OPTIONS = {
    'argv_emulation': False,
    'iconfile': ICON_FILE,
    
    # 明确指定需要打包的包
    'packages': [
        'cv2',           # OpenCV
        'numpy',         # NumPy（OpenCV 依赖）
        'PIL',           # Pillow
        'rumps',         # 菜单栏框架
        'objc',          # PyObjC
        'Foundation',
        'AppKit',
    ],
    
    # 需要包含的模块
    'includes': [
        'objc',
        'Foundation', 
        'AppKit',
        'threading',
        'subprocess',
        'logging',
        'json',
        'datetime',
    ],
    
    # 排除不需要的模块（减小体积）
    'excludes': [
        'PyInstaller',
        'matplotlib',
        'scipy',
        'pandas',
        'tkinter',
        'test',
        'unittest',
    ],
    
    # 资源文件
    'resources': ['assets/images/image_0.png'] if os.path.exists('assets/images/image_0.png') else [],
    
    # plist 配置
    'plist': {
        'CFBundleName': '久坐提醒助手',
        'CFBundleDisplayName': '久坐提醒助手',
        'CFBundleIdentifier': 'com.sedentary.reminder',
        'CFBundleVersion': '1.1.0',
        'CFBundleShortVersionString': '1.1.0',
        'LSMinimumSystemVersion': '10.13.0',
        'LSUIElement': True,  # 菜单栏应用，不显示在 Dock
        'NSHighResolutionCapable': True,  # 支持 Retina 显示
        
        # 摄像头权限说明
        'NSCameraUsageDescription': '本应用需要访问摄像头来检测您是否在电脑前，以便准确提醒您休息。摄像头仅用于本地检测，不会上传或保存任何图像。',
        
        # 其他权限（如果需要）
        'NSAppleEventsUsageDescription': '用于显示通知和对话框',
    },
    
    # 使用 site-packages（确保所有依赖都被包含）
    'site_packages': True,
    
    # 半独立模式（alias 模式用于开发，去掉此行则为完全独立模式）
    # 'alias': True,  # 开发时取消注释此行，打包发布时注释掉
}

setup(
    name='久坐提醒助手',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
