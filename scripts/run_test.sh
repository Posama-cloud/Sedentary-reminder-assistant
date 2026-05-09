#!/bin/bash
# 快速测试脚本

cd "$(dirname "$0")"

echo "======================================"
echo "久坐提醒助手 - 快速测试"
echo "======================================"
echo ""
echo "激活虚拟环境..."
source .venv/bin/activate

echo "启动测试版本（10秒倒计时）..."
echo ""
echo "提示："
echo "  - 倒计时: 10 秒"
echo "  - 确认延迟: 5 秒"
echo "  - 日志位置: ~/Library/Logs/久坐提醒助手/test.log"
echo ""
echo "按 Ctrl+C 或菜单栏退出程序"
echo ""

python test_quick.py
