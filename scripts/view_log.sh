#!/bin/bash
# 查看实时日志

LOG_FILE="$HOME/Library/Logs/久坐提醒助手/test.log"

echo "======================================"
echo "实时查看测试日志"
echo "======================================"
echo "日志文件: $LOG_FILE"
echo ""
echo "按 Ctrl+C 退出"
echo ""

if [ ! -f "$LOG_FILE" ]; then
    echo "日志文件还不存在，请先运行程序"
    exit 1
fi

tail -f "$LOG_FILE"
