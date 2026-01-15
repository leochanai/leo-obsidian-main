#!/bin/bash

# 脚本功能：将当前目录下的所有文件夹拷贝到 ~/.claude/skills 目录
# 作者：Antigravity
# 日期：2025-12-26

# 设置颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 获取脚本所在目录（即 13 Skills 目录）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 目标目录列表
TARGET_DIRS=(
    "$HOME/.claude/skills"
    "$HOME/.codex/skills"
    "$HOME/.gemini/antigravity/skills"
)

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}技能文件夹拷贝脚本${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

for TARGET_DIR in "${TARGET_DIRS[@]}"; do
    echo -e "正在处理目标目录: ${YELLOW}${TARGET_DIR}${NC}"
    echo ""

    # 先删除目标目录（如果存在）
    if [ -d "$TARGET_DIR" ]; then
        echo -e "${YELLOW}正在删除旧的目标目录...${NC}"
        rm -rf "$TARGET_DIR"
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ 旧目录删除成功${NC}"
        else
            echo -e "${RED}✗ 旧目录删除失败${NC}"
            continue
        fi
    fi

    # 创建新的目标目录
    echo -e "${YELLOW}正在创建目标目录...${NC}"
    mkdir -p "$TARGET_DIR"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ 目标目录创建成功${NC}"
    else
        echo -e "${RED}✗ 目标目录创建失败${NC}"
        continue
    fi

    echo ""
    echo -e "${GREEN}开始拷贝文件夹到 $TARGET_DIR ...${NC}"
    echo ""

    # 计数器
    copied_count=0
    skipped_count=0

    # 遍历当前目录下的所有项目
    for item in "$SCRIPT_DIR"/*; do
        # 检查是否为目录
        if [ -d "$item" ]; then
            # 获取文件夹名称
            folder_name=$(basename "$item")
            
            # 跳过隐藏文件夹（以 . 开头的文件夹）
            if [[ "$folder_name" == .* ]]; then
                echo -e "${YELLOW}⊘ 跳过隐藏文件夹: ${folder_name}${NC}"
                ((skipped_count++))
                continue
            fi
            
            # 目标路径
            target_path="$TARGET_DIR/$folder_name"
            
            # 拷贝文件夹
            echo -e "正在拷贝: ${YELLOW}${folder_name}${NC}"
            
            # 使用 rsync 进行拷贝（保留权限和时间戳）
            rsync -av --delete "$item/" "$target_path/"
            
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}✓ 拷贝成功: ${folder_name}${NC}"
                ((copied_count++))
            else
                echo -e "${RED}✗ 拷贝失败: ${folder_name}${NC}"
            fi
        fi
    done

    echo ""
    echo -e "目标 ${YELLOW}${TARGET_DIR}${NC} 处理完成: 成功 ${GREEN}${copied_count}${NC}, 跳过 ${YELLOW}${skipped_count}${NC}"
    echo -e "${GREEN}----------------------------------------${NC}"
    echo ""
done

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}所有目标目录已更新！${NC}"
echo -e "${GREEN}========================================${NC}"
