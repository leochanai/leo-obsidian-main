---
name: bilingual-translation
description: 将英文内容翻译成中英文双语对照格式。当用户要求翻译、提供双语版本、进行中英文对照阅读，或处理英文文档需要生成双语版本时使用。
---

# 双语翻译

## 核心目标

将英文内容（标题和正文）转换为规范的中英文双语对照格式。

## 工作流程

1. 识别原文：确定需要翻译的完整英文内容
2. 逐段翻译：将英文内容逐段翻译成流畅的中文
3. 格式化输出：按以下模板组织输出内容
4. 就地修改：直接在原文件上进行修改（如适用）

## 格式模板

### 标题格式（斜杠分隔，同行）

```markdown
### English Title / 中文标题
```

### 正文格式（段落对齐，分隔线间隔）

```markdown
English paragraph 1

中文译文段落 1

---

English paragraph 2

中文译文段落 2
```

**格式要点**：
- 每个段落对之间使用 `---` 分隔线
- 原文和译文一一对应

### 表格格式（双表对照）

遇到表格时，保留完整的英文表格，紧跟一个完整的中文表格：

```markdown
| Column A | Column B |
|----------|----------|
| Value 1  | Value 2  |

| 列 A   | 列 B   |
|--------|--------|
| 值 1   | 值 2   |

---
```

**注意**：不要在单元格内换行显示中英文，而是分别生成两个独立的表格。

## 完整示例

**输入**：

> ## The Power of Generative AI
>
> Generative AI is a type of artificial intelligence that can create a wide variety of data, such as images, videos, audio, text, and 3D models. It does this by learning patterns from existing data, then using this knowledge to generate new, original content.
>
> This technology has the potential to revolutionize many industries, from entertainment and art to engineering and product design. However, it also raises important questions about ethics, copyright, and the nature of creativity.

**输出**：

> ### The Power of Generative AI / 生成式人工智能的力量
>
> Generative AI is a type of artificial intelligence that can create a wide variety of data, such as images, videos, audio, text, and 3D models. It does this by learning patterns from existing data, then using this knowledge to generate new, original content.
>
> 生成式人工智能是一种可以创建各种数据的人工智能，例如图像、视频、音频、文本和 3D 模型。它通过从现有数据中学习模式，然后利用这些知识来生成全新的原创内容。
>
> ---
>
> This technology has the potential to revolutionize many industries, from entertainment and art to engineering and product design. However, it also raises important questions about ethics, copyright, and the nature of creativity.
>
> 这项技术有潜力彻底改变许多行业，从娱乐和艺术到工程和产品设计。然而，它也引发了关于道德、版权和创造力本质的重要问题。