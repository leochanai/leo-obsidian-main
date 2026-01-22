---
name: pake-web-to-app
description: 使用 Pake 将任意网页打包成轻量级桌面应用程序（macOS/Windows/Linux）。当用户需要将网站变成桌面 App、创建 Web App 桌面版、打包网页应用、或提及 Pake 时使用。
---

# Pake - 网页打包桌面应用

Pake 是基于 Rust Tauri 的开源工具，一条命令将任意网页打包成桌面应用。

**核心优势**：
- 体积小：比 Electron 小近 20 倍（约 5MB）
- 速度快：Rust 构建，内存占用低
- 易使用：一条命令完成打包

## 环境要求

- Node.js ≥ 22（推荐）或 ≥ 18
- Rust ≥ 1.85（首次运行自动安装）

## 安装

```bash
pnpm install -g pake-cli
# 或
npm install -g pake-cli
```

## 快速开始

```bash
# 基础打包（自动获取网站图标）
pake https://github.com --name GitHub

# 自定义窗口尺寸
pake https://chat.openai.com --name ChatGPT --width 1400 --height 900

# 沉浸式标题栏（仅 macOS）
pake https://twitter.com --name Twitter --hide-title-bar

# 系统托盘 + 全局快捷键
pake https://web.telegram.org --name Telegram --show-system-tray --activation-shortcut "CmdOrControl+Shift+T"

# 自定义图标
pake https://notion.so --name Notion --icon ./notion-icon.png
```

## 常用参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--name` | 应用名称 | `--name "My App"` |
| `--icon` | 自定义图标（可选，默认自动获取） | `--icon ./icon.png` |
| `--width` | 窗口宽度（默认 1200） | `--width 1400` |
| `--height` | 窗口高度（默认 780） | `--height 900` |
| `--hide-title-bar` | 沉浸式标题栏（仅 macOS） | `--hide-title-bar` |
| `--fullscreen` | 全屏启动 | `--fullscreen` |
| `--always-on-top` | 窗口置顶 | `--always-on-top` |
| `--show-system-tray` | 显示系统托盘 | `--show-system-tray` |
| `--activation-shortcut` | 全局激活快捷键 | `--activation-shortcut "CmdOrControl+Shift+P"` |
| `--debug` | 启用开发者工具 | `--debug` |

完整参数列表见 [references/cli-options.md](references/cli-options.md)。

## 使用场景

### 常用网站打包

```bash
# AI 工具
pake https://chat.openai.com --name ChatGPT --width 1400 --height 900
pake https://claude.ai --name Claude --width 1400 --height 900

# 社交媒体
pake https://twitter.com --name Twitter --hide-title-bar
pake https://web.whatsapp.com --name WhatsApp --show-system-tray

# 生产力工具
pake https://notion.so --name Notion --width 1400 --height 900
pake https://figma.com --name Figma --width 1600 --height 1000
```

### 本地 HTML 文件

```bash
# 打包本地 HTML（需要 --use-local-file 复制资源）
pake ./my-app/index.html --name "My App" --use-local-file
```

### 开发调试

```bash
# 快速迭代构建（跳过安装包生成）
pake https://example.com --name TestApp --iterative-build --debug
```

## 平台注意事项

| 平台 | 输出格式 | 特殊选项 |
|------|----------|----------|
| macOS | `.dmg`（默认）或 `.app` | `--hide-title-bar`, `--dark-mode`, `--multi-arch` |
| Windows | `.msi` | `--installer-language` |
| Linux | `.deb`, `.AppImage` | `--targets deb`, `--targets appimage` |

### 指定构建目标

```bash
# macOS 通用二进制（Intel + Apple Silicon）
pake https://example.com --name App --targets universal

# Linux ARM64
pake https://example.com --name App --targets deb-arm64

# Windows ARM64
pake https://example.com --name App --targets arm64
```

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| 首次打包很慢 | 正常现象，需要配置 Rust 环境，后续会很快 |
| Rust 安装失败 | 手动安装：`curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs \| sh` |
| 权限问题 | 使用 `npx pake-cli` 代替全局安装 |
| 图标格式错误 | 提供 PNG 图片，Pake 会自动转换为平台格式 |
| macOS 输出 .app | 设置环境变量 `PAKE_CREATE_APP=1` |

## 验证

打包完成后，应用安装包位于当前工作目录。验证：

```bash
# 列出生成的安装包
ls -la *.dmg *.msi *.deb *.AppImage 2>/dev/null
```
