#!/bin/bash
# py2app 打包脚本 - 久坐提醒助手

set -e  # 遇到错误立即退出

echo "=========================================="
echo "  久坐提醒助手 - py2app 打包脚本"
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查虚拟环境
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo -e "${YELLOW}警告: 未检测到虚拟环境${NC}"
    echo "建议在虚拟环境中运行，是否继续？(y/n)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "已取消"
        exit 1
    fi
fi

# 检查 py2app 是否安装
if ! python -c "import py2app" 2>/dev/null; then
    echo -e "${RED}错误: py2app 未安装${NC}"
    echo "正在安装 py2app..."
    pip install py2app
fi

# 清理旧的构建文件
echo -e "${YELLOW}[1/4] 清理旧的构建文件...${NC}"
rm -rf build dist
echo "✓ 清理完成"
echo ""

# 选择构建模式
echo -e "${YELLOW}[2/4] 选择构建模式:${NC}"
echo "  1) 开发模式 (alias mode) - 快速，用于测试"
echo "  2) 发布模式 (standalone) - 完整打包，用于分发"
echo ""
read -p "请选择 (1/2, 默认为 2): " mode
mode=${mode:-2}

# 执行打包
echo ""
if [ "$mode" = "1" ]; then
    echo -e "${YELLOW}[3/4] 开始打包 (开发模式)...${NC}"
    python setup.py py2app -A
else
    echo -e "${YELLOW}[3/4] 开始打包 (发布模式)...${NC}"
    python setup.py py2app
fi

# 检查打包结果
echo ""
if [ -d "dist/久坐提醒助手.app" ]; then
    echo -e "${GREEN}✓ 打包成功！${NC}"
    echo ""
    echo -e "${YELLOW}[4/4] 打包信息:${NC}"
    echo "  应用位置: dist/久坐提醒助手.app"
    
    # 显示应用大小
    app_size=$(du -sh "dist/久坐提醒助手.app" | cut -f1)
    echo "  应用大小: $app_size"
    
    # 显示构建模式
    if [ "$mode" = "1" ]; then
        echo "  构建模式: 开发模式 (需要 Python 环境)"
    else
        echo "  构建模式: 发布模式 (独立运行)"
    fi
    
    echo ""
    echo -e "${GREEN}=========================================="
    echo "  打包完成！"
    echo "==========================================${NC}"
    echo ""
    echo "运行应用:"
    echo "  open dist/久坐提醒助手.app"
    echo ""
    echo "测试应用:"
    echo "  dist/久坐提醒助手.app/Contents/MacOS/久坐提醒助手"
    echo ""
    
    if [ "$mode" = "2" ]; then
        echo "分发应用:"
        echo "  可以直接将 dist/久坐提醒助手.app 拷贝给其他用户"
        echo "  或者压缩后分发: zip -r 久坐提醒助手.zip dist/久坐提醒助手.app"
        echo ""
    fi
    
    # 询问是否立即运行
    read -p "是否立即运行应用？(y/n): " run_now
    if [[ "$run_now" =~ ^[Yy]$ ]]; then
        echo ""
        echo "正在启动应用..."
        open "dist/久坐提醒助手.app"
    fi
else
    echo -e "${RED}✗ 打包失败${NC}"
    echo "请检查错误信息"
    exit 1
fi
