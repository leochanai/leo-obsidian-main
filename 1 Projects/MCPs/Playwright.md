---
source: https://github.com/microsoft/playwright-mcp?utm_source=chatgpt.com
author:
  - "[[Microsoft]]"
published:
created:
description:
tags:
  - mcp
cover:
---

# Playwright

一个通过 [Playwright](https://playwright.dev/) 提供浏览器自动化能力的模型上下文协议 (MCP) 服务端。该服务端允许大语言模型 (LLMs) 通过结构化的无障碍快照与网页进行交互，无需依赖屏幕截图或视觉微调模型。

## 核心特性

*   **快速且轻量**。使用 Playwright 的无障碍树，而非基于像素的输入。
*   **对 LLM 友好**。无需视觉模型，纯粹基于结构化数据运行。
*   **确定性的工具应用**。避免了基于截图的方法中常见的歧义。

## 安装
### Claude Code

``` bash
claude mcp add playwright npx @playwright/mcp@latest
```

### Codex

``` bash
codex mcp add playwright npx "@playwright/mcp@latest"
```

### Warp

``` json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest"
      ]
    }
  }
}
```
