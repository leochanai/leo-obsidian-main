---
name: formatting-deepresearch-reports
description: 清理和格式化 DeepResearch 报告文件。删除引用链接标记和多余的数字标点组合。当用户需要清理 DeepResearch 导出的报告、移除引用标记、或格式化研究文档时使用。
---

# DeepResearch 报告格式化工具

清理从 ChatGPT DeepResearch 导出的报告文件，移除引用标记和格式噪音。

## 清理规则

1. **移除空格+数字+标点组合**：将 ` 27。` 这类模式替换为 `。`
   - 匹配：空格 + 一个或多个数字 + 中文标点（。，、；：！？）
   - 示例：`内容 27。` → `内容。`

2. **移除 Markdown 引用链接**：删除所有 `[文本](URL)` 格式的链接
   - 示例：`参考资料[blog.google](https://...)。` → `参考资料。`

## 使用流程

1. 读取目标 Markdown 文件
2. 运行格式化脚本：
   ```bash
   cd scripts
   python3 format_report.py "<文件路径>"
   ```
3. 脚本会自动：
   - 备份原文件为 `.bak`
   - 应用清理规则
   - 保存格式化后的文件
4. 向用户报告处理结果

## 示例

**输入**：
```markdown
Nano Banana Pro 拥有前所未有的图像生成能力 27。这是构建在 Gemini 3 Pro 大模型基础上的最新生成式 AI 绘画模型[blog.google](https://blog.google/technology/ai/nano-banana-pro/)。
```

**输出**：
```markdown
Nano Banana Pro 拥有前所未有的图像生成能力。这是构建在 Gemini 3 Pro 大模型基础上的最新生成式 AI 绘画模型。
```
