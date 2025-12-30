#!/bin/bash

# 脚本功能：将符合条件的 Skill (仅包含 SKILL.md 的目录) 拷贝并重命名到 Antigravity workflows 目录
# 作者：Antigravity
# 日期：2025-12-30

# 设置颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 获取脚本所在目录（即 13 Skills 目录）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 目标目录
TARGET_DIR="/Users/farghost/.gemini/antigravity/global_workflows"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Antigravity Skill 提取同步脚本${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "源目录: ${YELLOW}${SCRIPT_DIR}${NC}"
echo -e "目标目录: ${YELLOW}${TARGET_DIR}${NC}"
echo ""

# 先删除目标目录（如果存在）
if [ -d "$TARGET_DIR" ]; then
    echo -e "${YELLOW}正在删除旧的目标目录...${NC}"
    rm -rf "$TARGET_DIR"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ 旧目录删除成功${NC}"
    else
        echo -e "${RED}✗ 旧目录删除失败${NC}"
        exit 1
    fi
fi

# 创建新的目标目录
echo -e "${YELLOW}正在创建目标目录...${NC}"
mkdir -p "$TARGET_DIR"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ 目标目录创建成功${NC}"
else
    echo -e "${RED}✗ 目标目录创建失败${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}开始检查并拷贝 Skill...${NC}"
echo ""

# 计数器
copied_count=0
skipped_count=0
ignored_count=0

# 遍历当前目录下的所有项目
for item in "$SCRIPT_DIR"/*; do
    # 检查是否为目录
    if [ -d "$item" ]; then
        # 获取文件夹名称
        folder_name=$(basename "$item")
        
        # 跳过隐藏文件夹
        if [[ "$folder_name" == .* ]]; then
            continue
        fi
        
        # 检查是否存在 SKILL.md
        if [ ! -f "$item/SKILL.md" ]; then
             # 如果连 SKILL.md 都没有，默默忽略，或者作为 ignored 计数
             ((ignored_count++))
             continue
        fi

        # 检查目录下是否只有 SKILL.md (忽略隐藏文件如 .DS_Store)
        # ls -1 只列出非隐藏文件
        visible_files_count=$(ls -1 "$item" | wc -l | tr -d ' ')
        
        if [ "$visible_files_count" -eq 1 ]; then
            # 只有 SKILL.md，执行拷贝
            target_path="$TARGET_DIR/${folder_name}.md"
            
            echo -e "正在处理: ${YELLOW}${folder_name}${NC}"
            cp "$item/SKILL.md" "$target_path"
            
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}✓ 转换成功: SKILL.md -> ${folder_name}.md${NC}"
                ((copied_count++))
            else
                echo -e "${RED}✗ 拷贝失败: ${folder_name}${NC}"
            fi
        else
            # 包含其他文件，跳过
            echo -e "${YELLOW}⊘ 跳过: ${folder_name} (包含其他文件)${NC}"
            ((skipped_count++))
        fi
    fi
done

# 输出统计信息
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}同步完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "成功转换: ${GREEN}${copied_count}${NC} 个 Skill"
echo -e "跳过(多文件): ${YELLOW}${skipped_count}${NC} 个 Skill"
echo ""
echo -e "目标位置: ${YELLOW}${TARGET_DIR}${NC}"
echo ""
