#!/usr/bin/env python3
"""
DeepResearch 报告格式化脚本

清理规则：
1. 移除「空格+数字+中文标点」模式，保留标点
2. 移除所有 Markdown 链接 [文本](URL)

用法：
    python3 format_report.py <文件路径>
"""

import re
import sys
import shutil
from pathlib import Path


def format_deepresearch_report(content: str) -> str:
    """
    格式化 DeepResearch 报告内容
    
    Args:
        content: 原始文件内容
        
    Returns:
        格式化后的内容
    """
    # 规则 1: 移除「空格+数字+中文标点」，保留标点
    # 匹配：空格 + 一个或多个数字 + 中文标点符号
    pattern_space_num_punct = r' \d+([。，、；：！？])'
    content = re.sub(pattern_space_num_punct, r'\1', content)
    
    # 规则 2: 移除所有 Markdown 链接 [文本](URL)
    # 匹配：[任意文本](任意URL)
    pattern_markdown_link = r'\[[^\]]*\]\([^)]*\)'
    content = re.sub(pattern_markdown_link, '', content)
    
    return content


def process_file(file_path: str) -> dict:
    """
    处理单个文件
    
    Args:
        file_path: 文件路径
        
    Returns:
        处理结果统计
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    if not path.suffix.lower() in ['.md', '.markdown', '.txt']:
        raise ValueError(f"不支持的文件类型: {path.suffix}")
    
    # 读取原始内容
    original_content = path.read_text(encoding='utf-8')
    original_length = len(original_content)
    
    # 备份原文件
    backup_path = path.with_suffix(path.suffix + '.bak')
    shutil.copy2(path, backup_path)
    
    # 格式化内容
    formatted_content = format_deepresearch_report(original_content)
    formatted_length = len(formatted_content)
    
    # 写入格式化后的内容
    path.write_text(formatted_content, encoding='utf-8')
    
    return {
        'file': str(path),
        'backup': str(backup_path),
        'original_chars': original_length,
        'formatted_chars': formatted_length,
        'removed_chars': original_length - formatted_length
    }


def main():
    if len(sys.argv) < 2:
        print("用法: python3 format_report.py <文件路径>")
        print("示例: python3 format_report.py ./my_report.md")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    try:
        result = process_file(file_path)
        print(f"✅ 格式化完成")
        print(f"   文件: {result['file']}")
        print(f"   备份: {result['backup']}")
        print(f"   原始字符数: {result['original_chars']:,}")
        print(f"   格式化后字符数: {result['formatted_chars']:,}")
        print(f"   移除字符数: {result['removed_chars']:,}")
    except FileNotFoundError as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 意外错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
