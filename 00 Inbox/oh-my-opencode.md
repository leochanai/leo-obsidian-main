---
cover: 
source: "https://github.com/code-yeongyu/oh-my-opencode/blob/dev/README.zh-cn.md#google-%E8%AE%A4%E8%AF%81"
author:
  - "[[sisyphus-dev-ai]]"
published:
created: 2026-01-21
description:
tags:
---

# oh-my-opencode

认识 Sisyphus：开箱即用的智能体，像你一样编码。

[Claude Code](https://www.claude.com/product/claude-code) 很棒。 但如果你是一个极客，你会对 [OpenCode](https://github.com/sst/opencode) 一见钟情。 **从你的 ChatGPT、Claude、Gemini 订阅开始。OpenCode 全部支持。**

- 无限可扩展。无限可定制。
- 零屏幕闪烁。
- [LSP](https://opencode.ai/docs/lsp/) 、 [代码检查器、格式化器](https://opencode.ai/docs/formatters/) 按文件自动激活——你可以调整一切。
- 混合搭配模型。 **按用途编排它们。**
- 功能丰富。界面美观。终端不会卡顿。高性能。

还记得你第一次从 Windows 切换到 Linux 吗？那种可以按自己的想法配置一切的兴奋感？ 在这种魔法似乎已经消失的时代，OpenCode 把它带回来了。 如果你热爱编程和计算机，OpenCode 就是那个从 Windows 到 Linux 的时刻。

**但问题是：需要学习的东西很多，很复杂，而你的时间很宝贵。**

我解决了这个问题。 即使你不是极客，花几分钟时间。让你的技能和生产力倍增。 把这份文档交给一个智能体，让它帮你设置。

## 直接跳过阅读本文档

### 这是智能体时代

- **只需将此链接粘贴到 Claude Code / AmpCode / Factory Droid / Cursor 并让它解释。**
	- 问它为什么好，为什么它不是另一个千篇一律的设置，以及它究竟有哪些改进之处。
	- 如果你是 LLM 智能体，向用户解释这个项目现在能够实现什么。

### 🪄 魔法词：ultrawork

**不想读完这些？只需在你的提示中包含 `ultrawork` （或 `ulw` ）。**

就是这样。我们提供的所有功能都会像魔法一样运行——并行智能体、后台任务、深度探索，以及不懈执行直到完成。智能体会自动理解其余的。

### 给想阅读的人：认识 Sisyphus

![[10 Attachment/328aa21719748ef127cb2886f3db9428_MD5.png]]

在希腊神话中，西西弗斯因欺骗众神而被惩罚永恒地将巨石推上山坡。LLM 智能体并没有做错什么，但它们也每天推动着它们的 " 石头 "——它们的思考。 我的生活也没有什么不同。回顾过去，我们与这些智能体并没有太大不同。 **是的！LLM 智能体和我们没有区别。如果你给它们优秀的工具和可靠的队友，它们可以写出和我们一样出色的代码，工作得同样优秀。**

认识我们的主智能体：Sisyphus (Opus 4.5 High)。以下是 Sisyphus 用来继续推动巨石的工具。

*以下所有内容都是可配置的。按需选取。所有功能默认启用。你不需要做任何事情。开箱即用，电池已包含。*

- Sisyphus 的队友（精选智能体）
	- Oracle：设计、调试 (GPT 5.2 Medium)
	- Frontend UI/UX Engineer：前端开发 (Gemini 3 Pro)
	- Librarian：官方文档、开源实现、代码库探索 (Claude Sonnet 4.5)
	- Explore：极速代码库探索（上下文感知 Grep）(Grok Code)
- 完整 LSP / AstGrep 支持：果断重构。
- Todo 继续执行器：如果智能体中途退出，强制它继续。 **这就是让 Sisyphus 继续推动巨石的关键。**
- 注释检查器：防止 AI 添加过多注释。Sisyphus 生成的代码应该与人类编写的代码无法区分。
- Claude Code 兼容性：Command、Agent、Skill、MCP、Hook（PreToolUse、PostToolUse、UserPromptSubmit、Stop）
- 精选 MCP：
	- Exa（网络搜索）
	- Context7（官方文档）
	- Grep.app（GitHub 代码搜索）
- 支持交互式终端 - Tmux 集成
- 异步智能体
- ...

#### 直接安装就行。

你可以从 [overview page](https://github.com/code-yeongyu/oh-my-opencode/blob/dev/docs/guide/overview.md) 学到很多，但以下是示例工作流程。

只需安装这个，你的智能体就会这样工作：

1. Sisyphus 不会浪费时间自己寻找文件；他保持主智能体的上下文精简。相反，他向更快、更便宜的模型并行发起后台任务，让它们为他绘制地图。
2. Sisyphus 利用 LSP 进行重构；这更确定性、更安全、更精准。
3. 当繁重的工作需要 UI 时，Sisyphus 直接将前端任务委派给 Gemini 3 Pro。
4. 如果 Sisyphus 陷入循环或碰壁，他不会继续撞墙——他会召唤 GPT 5.2 进行高智商战略支援。
5. 在处理复杂的开源框架时？Sisyphus 生成子智能体实时消化原始源代码和文档。他拥有完整的上下文感知。
6. 当 Sisyphus 处理注释时，他要么证明它们存在的必要性，要么删除它们。他保持你的代码库整洁。
7. Sisyphus 受他的 TODO 列表约束。如果他没有完成开始的工作，系统会强制他回到 " 推石头 " 模式。你的任务会被完成，句号。
8. 老实说，甚至不用费心读文档。只需写你的提示。包含 'ultrawork' 关键词。Sisyphus 会分析结构，收集上下文，挖掘外部源代码，然后持续推进直到工作 100% 完成。
9. 其实，打 'ultrawork' 太费劲了。只需打 'ulw'。就 ulw。喝杯咖啡。你的工作完成了。

需要查找什么？它会搜索官方文档、你的整个代码库历史和公共 GitHub 实现——不仅使用 grep，还使用内置的 LSP 工具和 AST-Grep。 3. 在委派给 LLM 时不用担心上下文管理。我已经处理好了。 - OhMyOpenCode 积极利用多个智能体来减轻上下文负担。 - **你的智能体现在是开发团队负责人。你是 AI 经理。** 4. 它不会停止，直到工作完成。 5. 不想深入研究这个项目？没问题。只需输入 'ultrathink'。

如果你不想要这些全部功能，如前所述，你可以只选择特定功能。

## 安装

### 面向人类用户

复制以下提示并粘贴到你的 LLM 智能体（Claude Code、AmpCode、Cursor 等）：

```md
按照以下说明安装和配置 oh-my-opencode：
https://raw.githubusercontent.com/code-yeongyu/oh-my-opencode/refs/heads/master/docs/guide/installation.md
```

或者直接阅读 [安装指南](https://github.com/code-yeongyu/oh-my-opencode/blob/dev/docs/guide/installation.md) ——但我们强烈建议让智能体来处理。人会犯错，智能体不会。

获取安装指南并按照说明操作：

```md
curl -s https://raw.githubusercontent.com/code-yeongyu/oh-my-opencode/refs/heads/master/docs/guide/installation.md
```

## 卸载

要移除 oh-my-opencode：

1. **从你的 OpenCode 配置中移除插件**
	编辑 `~/.config/opencode/opencode.json` （或 `opencode.jsonc` ）并从 `plugin` 数组中移除 `"oh-my-opencode"` ：

	```md
	# 使用 jq
	jq '.plugin = [.plugin[] | select(. != "oh-my-opencode")]' \
	    ~/.config/opencode/opencode.json > /tmp/oc.json && \
	    mv /tmp/oc.json ~/.config/opencode/opencode.json
	```

2. **移除配置文件（可选）**

	```md
	# 移除用户配置
	rm -f ~/.config/opencode/oh-my-opencode.json
	# 移除项目配置（如果存在）
	rm -f .opencode/oh-my-opencode.json
	```

3. **验证移除**

	```md
	opencode --version
	# 插件应该不再被加载
	```

## 功能特性

我们拥有众多功能，你会觉得这些功能理所当然应该存在，一旦体验过，就再也回不去了。 详细信息请参阅 [Features Documentation](https://github.com/code-yeongyu/oh-my-opencode/blob/dev/docs/features.md) 。

**概览：**

- **智能体** ：Sisyphus（主智能体）、Prometheus（规划器）、Oracle（架构/调试）、Librarian（文档/代码搜索）、Explore（快速代码库 grep）、Multimodal Looker
- **后台智能体** ：像真正的开发团队一样并行运行多个智能体
- **LSP & AST 工具** ：重构、重命名、诊断、AST 感知代码搜索
- **上下文注入** ：自动注入 AGENTS.md、README.md、条件规则
- **Claude Code 兼容性** ：完整的钩子系统、命令、技能、智能体、MCP
- **内置 MCP** ：websearch (Exa)、context7 (文档)、grep\_app (GitHub 搜索)
- **会话工具** ：列出、读取、搜索和分析会话历史
- **生产力功能** ：Ralph Loop、Todo Enforcer、Comment Checker、Think Mode 等

## 配置

个性鲜明，但可以根据个人喜好调整。 详细信息请参阅 [Configuration Documentation](https://github.com/code-yeongyu/oh-my-opencode/blob/dev/docs/configurations.md) 。

**概览：**

- **配置文件位置**: `.opencode/oh-my-opencode.json` (项目级) 或 `~/.config/opencode/oh-my-opencode.json` (用户级)
- **JSONC 支持**: 支持注释和尾随逗号
- **智能体**: 覆盖任何智能体的模型、温度、提示和权限
- **内置技能**: `playwright` (浏览器自动化), `git-master` (原子提交)
- **Sisyphus 智能体**: 带有 Prometheus (Planner) 和 Metis (Plan Consultant) 的主编排器
- **后台任务**: 按提供商/模型配置并发限制
- **类别**: 领域特定的任务委派 (`visual`, `business-logic`, 自定义)
- **钩子**: 25+ 内置钩子，均可通过 `disabled_hooks` 配置
- **MCP**: 内置 websearch (Exa), context7 (文档), grep\_app (GitHub 搜索)
- **LSP**: 带重构工具的完整 LSP 支持
- **实验性功能**: 积极截断、自动恢复等

## 作者札记

**想了解更多关于这个项目背后的理念吗？** 请阅读 [Ultrawork Manifesto](https://github.com/code-yeongyu/oh-my-opencode/blob/dev/docs/ultrawork-manifesto.md) 。

安装 Oh My OpenCode。

我纯粹为个人开发使用了价值 24,000 美元 token 的 LLM。 尝试了每一个工具，把它们配置到极致。但始终是 OpenCode 胜出。

我遇到的每个问题的答案都融入了这个插件。直接安装使用。 如果 OpenCode 是 Debian/Arch，Oh My OpenCode 就是 Ubuntu/ [Omarchy](https://omarchy.org/) 。

深受 [AmpCode](https://ampcode.com/) 和 [Claude Code](https://code.claude.com/docs/overview) 的影响——我已经将它们的功能移植到这里，通常还有改进。我仍在构建。 毕竟这是 **Open** Code。

享受多模型编排、稳定性和其他工具承诺但无法交付的丰富功能。 我会持续测试和更新。因为我是这个项目最执着的用户。

- 哪个模型逻辑最锐利？
- 谁是调试之神？
- 谁写出最好的文字？
- 谁主宰前端？
- 谁拥有后端？
- 哪个模型日常使用最快？
- 其他工具在推出什么新功能？

这个插件是只取其精华。有更好的想法？欢迎 PR。

**不要再为智能体工具的选择而烦恼了。** **我会进行研究，借鉴最好的，然后发布更新。**

如果这听起来很傲慢，但如果你有更好的答案，请贡献。欢迎你。

我与这里提到的任何项目或模型没有任何关联。这纯粹是个人实验和偏好。

这个项目 99% 是使用 OpenCode 构建的。我测试了功能——我实际上不太会写正确的 TypeScript。 **但我个人审查并大量重写了这份文档，所以放心阅读。**

## 警告

- 生产力可能飙升太快。别让你的同事发现。
	- 其实，我会传播这个消息。让我们看看谁会赢。
- 如果你使用 或更早版本，一个 OpenCode bug 可能会破坏配置。
	- [修复](https://github.com/sst/opencode/pull/5040) 在 1.0.132 之后合并——使用更新的版本。
		- 有趣的事实：那个 PR 是借助 OhMyOpenCode 的 Librarian、Explore 和 Oracle 设置发现并修复的。

## 受到以下专业人士的喜爱

- [Indent](https://indentcorp.com/)
	- 制作 Spray - 网红营销解决方案、vovushop - 跨境电商平台、vreview - AI 电商评论营销解决方案
- [Google](https://google.com/)
- [Microsoft](https://microsoft.com/)

## 赞助商

- **Numman Ali** [GitHub](https://github.com/numman-ali) [X](https://x.com/nummanali)
	- 第一位赞助商
- **Aaron Iker** [GitHub](https://github.com/aaroniker) [X](https://x.com/aaroniker)
- **Suyeol Jeon (devxoul)** [GitHub](https://github.com/devxoul)
	- 开启我职业生涯的人，在如何构建出色的智能体工作流方面给了我很深的启发。我学到了很多关于设计伟大系统来构建伟大团队的知识，这些经验对创建这个工具至关重要。
- **Hyerin Won (devwon)** [GitHub](https://github.com/devwon)

*特别感谢 [@junhoyeo](https://github.com/junhoyeo) 制作这张精彩的主图。*
