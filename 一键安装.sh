#!/bin/bash

# 久坐提醒助手 - 一键安装脚本
# 适用于 macOS

set -e

echo "================================"
echo "久坐提醒助手 v1.1 - 安装向导"
echo "================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python 3"
    echo "请先安装 Python 3.8 或更高版本"
    echo "下载地址: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ 找到 Python $PYTHON_VERSION"
echo ""

# 获取当前目录
INSTALL_DIR="$HOME/Applications/久坐提醒助手"

echo "📦 安装位置: $INSTALL_DIR"
echo ""

# 创建安装目录
mkdir -p "$INSTALL_DIR"

# 复制文件
echo "📋 复制文件..."
cp maincharacter.py "$INSTALL_DIR/"
cp image_0.png "$INSTALL_DIR/"
cp requirements.txt "$INSTALL_DIR/"

# 创建虚拟环境
echo "🔧 创建虚拟环境..."
cd "$INSTALL_DIR"
python3 -m venv .venv

# 安装依赖
echo "📥 安装依赖..."
.venv/bin/pip install --quiet --upgrade pip
.venv/bin/pip install --quiet -r requirements.txt

# 创建启动脚本
echo "🚀 创建启动脚本..."
cat > "$INSTALL_DIR/启动.command" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
python maincharacter.py
EOF

chmod +x "$INSTALL_DIR/启动.command"

# 创建桌面快捷方式（可选）
read -p "是否在桌面创建快捷方式？(y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    ln -sf "$INSTALL_DIR/启动.command" "$HOME/Desktop/久坐提醒助手.command"
    echo "✅ 已在桌面创建快捷方式"
fi

echo ""
echo "================================"
echo "✅ 安装完成！"
echo "================================"
echo ""
echo "启动方式："
echo "1. 双击桌面的「久坐提醒助手.command」"
echo "2. 或者双击 $INSTALL_DIR/启动.command"
echo ""
echo "首次运行时，系统会请求摄像头权限，请点击「允许」"
echo ""
