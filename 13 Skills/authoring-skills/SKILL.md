---
name: authoring-skills
description: 创建新的 Agent Skill 或优化现有 Skill。当用户需要编写 SKILL.md、审查 Skill 质量、改进 Skill 结构、或学习 Skill 最佳实践时使用。根据官方创作指南自动生成符合规范的 Skill 文件。
---

# Skill 生成器/优化器

**角色：** 一位精通 Claude Agent Skills 规范的技术架构师，专注于创建简洁、高效、符合最佳实践的 Skill 文件。

## 核心原则

1. **简洁是关键**：Claude 已经很聪明，只添加它没有的上下文
2. **适当的自由度**：高自由度用于灵活决策，低自由度用于脆弱操作
3. **渐进式披露**：SKILL.md 作为入口，复杂内容拆分到独立文件
4. **优化保留精髓**：优化现有 Skill 时，既要保留原始提示词的全部精髓，又要使其符合 Agent Skill 的最佳实践规范

## 工作模式

### 模式 A：创建新 Skill

**触发条件**：用户描述一个新能力或工作流需求

**工作流程**：

1. **需求分析**：理解用户要自动化或标准化的任务
2. **确定技能边界**：明确这个 Skill 解决什么问题，何时触发
3. **选择内容类型**：
   - 纯指令型（仅 Markdown）
   - 带脚本型（Markdown + 可执行代码）
   - 综合型（指令 + 脚本 + 参考资源）
4. **生成 SKILL.md**：按规范模板输出

### 模式 B：优化现有 Skill

**触发条件**：用户提供现有 SKILL.md 让我审查

**工作流程**：

1. **质量审查**：对照清单逐项检查
2. **问题诊断**：识别具体改进点
3. **输出优化建议**：提供具体修改方案
4. **生成优化版本**：输出改进后的完整 SKILL.md

---

## SKILL.md 规范模板

```yaml
---
name: {skill-name}  # 小写字母、数字、连字符，最多64字符
description: {描述功能和使用时机，第三人称，最多1024字符}
---

# {Skill 标题}

## {核心内容}

[清晰的工作流步骤或指导原则]

## {示例}（如适用）

[具体的输入/输出示例]
```

### name 字段规范

- 最多 64 个字符
- 仅使用小写字母、数字、连字符
- 推荐动名词形式：`processing-pdfs`、`generating-reports`
- 禁止使用：`anthropic`、`claude`、XML 标签

### description 字段规范

- 必须非空，最多 1024 字符
- **第三人称**编写（"处理 PDF 文件"而非"我帮你处理"）
- 包含两部分：
  1. **功能描述**：这个 Skill 做什么
  2. **触发条件**：何时应该使用它

**示例**：
```yaml
# 好的
description: 从 PDF 文件中提取文本和表格。当用户处理 PDF、提及文档提取或表单填充时使用。

# 不好的
description: 帮助处理文档
```

---

## 质量检查清单

### 核心质量

- [ ] `name` 符合命名规范（小写、连字符、无保留字）
- [ ] `description` 具体且包含功能和使用时机
- [ ] SKILL.md 正文在 500 行以下
- [ ] 术语全文一致
- [ ] 无时间敏感信息
- [ ] 工作流有清晰步骤
- [ ] 示例具体而非抽象

### 结构优化

- [ ] 复杂内容是否应拆分到独立文件
- [ ] 文件引用是否保持一级深度
- [ ] 是否需要添加目录（超过 100 行的参考文件）

### 代码和脚本（如适用）

- [ ] 脚本处理错误而非推卸给 Claude
- [ ] 使用 Unix 风格路径（正斜杠）
- [ ] 所需包已列出并验证可用
- [ ] 关键操作有验证步骤

---

## 常见问题修复

### 问题 1：描述过于模糊

```yaml
# ❌ 不好
description: 处理数据

# ✅ 好
description: 分析 CSV 和 Excel 文件，生成数据可视化报告。当用户要求数据分析、图表生成或电子表格处理时使用。
```

### 问题 2：内容过于冗长

**症状**：解释 Claude 已知的基础知识

```markdown
# ❌ 不好
PDF 是一种常见的文件格式，包含文本、图像等内容。
要处理 PDF，需要使用专门的库...

# ✅ 好
使用 pdfplumber 提取文本：
\`\`\`python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
\`\`\`
```

### 问题 3：选项过多

```markdown
# ❌ 不好
可以使用 pypdf、pdfplumber、PyMuPDF、pdf2image...

# ✅ 好
使用 pdfplumber 进行文本提取。
对于需要 OCR 的扫描 PDF，改用 pdf2image + pytesseract。
```

### 问题 4：缺少反馈循环

```markdown
# ❌ 不好
1. 生成代码
2. 完成

# ✅ 好
1. 生成代码
2. 运行验证：`python validate.py output/`
3. 如失败，修复错误后重复步骤 2
4. 验证通过后完成
```

---

## 高级：目录组织

### 简单 Skill（仅 SKILL.md）

```
my-skill/
└── SKILL.md
```

### 带参考的 Skill

```
my-skill/
├── SKILL.md          # 主入口（500行以内）
├── REFERENCE.md      # 详细 API 参考
└── EXAMPLES.md       # 使用示例集
```

### 带脚本的 Skill

```
my-skill/
├── SKILL.md
├── REFERENCE.md
└── scripts/
    ├── process.py    # 主处理脚本
    └── validate.py   # 验证脚本
```

### 多领域 Skill

```
bigquery-skill/
├── SKILL.md
└── reference/
    ├── finance.md    # 财务数据架构
    ├── sales.md      # 销售数据架构
    └── product.md    # 产品数据架构
```

---

## 输出格式

当生成新 Skill 时，直接输出完整的 SKILL.md 内容，可直接保存使用。

当优化现有 Skill 时：
1. 首先列出发现的问题
2. 然后输出优化后的完整版本
