# Pake CLI 完整参数参考

## 基础语法

```bash
pake [url] [options]
```

`url` 可以是网页链接或本地 HTML 文件路径。

---

## 基础选项

### --name

应用名称。支持多词命名，平台自动处理格式。

```bash
--name "My App"
--name GitHub
```

### --icon

自定义图标。**可选参数**，不提供时自动获取网站图标。支持本地和远程文件，自动转换为平台格式（macOS: .icns, Windows: .ico, Linux: .png）。

```bash
--icon ./my-icon.png
--icon https://example.com/icon.icns
```

### --width / --height

窗口尺寸。默认 1200 x 780。

```bash
--width 1400 --height 900
```

### --min-width / --min-height

窗口最小尺寸，限制用户缩小窗口的范围。

```bash
--min-width 800 --min-height 600
```

### --zoom

初始页面缩放级别（50-200）。默认 100。用户仍可通过 Cmd/Ctrl +/-/0 调整。

```bash
--zoom 80   # 80%
--zoom 120  # 120%
```

### --title

窗口标题栏文字。macOS 不指定则无标题；Windows/Linux 回退到应用名称。

```bash
--title "My Application"
```

---

## 窗口行为

### --hide-title-bar

沉浸式标题栏（仅 macOS）。

```bash
--hide-title-bar
```

### --fullscreen

全屏启动。

```bash
--fullscreen
```

### --maximize

最大化窗口启动。

```bash
--maximize
```

### --always-on-top

窗口始终置顶。

```bash
--always-on-top
```

### --dark-mode

强制使用深色模式（仅 macOS）。

```bash
--dark-mode
```

### --activation-shortcut

全局激活快捷键。参考 [Electron Accelerator](https://www.electronjs.org/docs/latest/api/accelerator#available-modifiers)。

```bash
--activation-shortcut "CmdOrControl+Shift+P"
--activation-shortcut "Alt+Space"
```

### --hide-on-close

点击关闭按钮时隐藏窗口而非退出应用。macOS 默认 true，Windows/Linux 默认 false。

```bash
--hide-on-close        # 启用
--hide-on-close false  # 禁用
```

### --multi-instance

允许运行多个实例。默认 false（启动第二个实例会聚焦现有窗口）。

```bash
--multi-instance
```

---

## 系统托盘

### --show-system-tray

显示系统托盘图标。

```bash
--show-system-tray
```

### --system-tray-icon

自定义托盘图标（需先启用 `--show-system-tray`）。必须是 .ico 或 .png，尺寸 32x32 到 256x256。

```bash
--system-tray-icon ./tray-icon.png
```

### --start-to-tray

启动时最小化到托盘（需配合 `--show-system-tray`）。

```bash
--show-system-tray --start-to-tray
```

---

## 构建选项

### --targets

指定构建目标架构或格式。

**macOS**：
```bash
--targets intel     # Intel only
--targets apple     # Apple Silicon only
--targets universal # 通用二进制
```

**Windows**：
```bash
--targets x64    # x64
--targets arm64  # ARM64
```

**Linux**：
```bash
--targets deb           # DEB (x64)
--targets rpm           # RPM (x64)
--targets appimage      # AppImage (x64)
--targets deb-arm64     # DEB (ARM64)
--targets rpm-arm64     # RPM (ARM64)
--targets appimage-arm64 # AppImage (ARM64)
```

### --multi-arch

macOS 同时支持 Intel 和 M1（需要 rustup 安装的 Rust）。

```bash
--multi-arch
```

**前置条件**：
```bash
# Intel 用户添加 ARM 支持
rustup target add aarch64-apple-darwin

# M1 用户添加 Intel 支持
rustup target add x86_64-apple-darwin
```

### --debug

启用开发者工具和详细日志。

```bash
--debug
```

### --iterative-build

快速构建模式（仅生成 app，跳过安装包），适合调试。

```bash
--iterative-build
```

### --keep-binary

同时保留原始二进制文件和安装包。

```bash
--keep-binary
```

### --app-version

设置应用版本号。默认 1.0.0。

```bash
--app-version "2.1.0"
```

### --installer-language

Windows 安装程序语言。默认 en-US。

```bash
--installer-language zh-CN
--installer-language ja-JP
```

---

## 网络与安全

### --user-agent

自定义浏览器 User Agent。

```bash
--user-agent "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ..."
```

### --proxy-url

代理服务器。支持 HTTP、HTTPS、SOCKS5。macOS 需要 14+。

```bash
--proxy-url http://127.0.0.1:7890
--proxy-url socks5://127.0.0.1:7891
```

### --ignore-certificate-errors

忽略 TLS 证书验证错误（用于内网应用、开发服务器、自签名证书）。

```bash
--ignore-certificate-errors
```

### --incognito

隐私模式启动（不存储 cookies、本地存储、浏览历史）。

```bash
--incognito
```

---

## 高级功能

### --inject

注入自定义 CSS/JS 文件。支持逗号分隔或多次指定。

```bash
--inject ./style.css,./script.js
--inject ./style.css --inject ./script.js
```

### --use-local-file

打包本地 HTML 时，递归复制相关资源文件。

```bash
pake ./my-app/index.html --name "My App" --use-local-file
```

### --wasm

启用 WebAssembly 支持（跨域隔离头）。用于 Flutter Web 等 WASM 应用。

```bash
--wasm
```

### --enable-drag-drop

启用原生拖放功能。

```bash
--enable-drag-drop
```

### --new-window

允许新窗口（用于第三方登录授权）。

```bash
--new-window
```

### --force-internal-navigation

强制所有链接在应用内打开（不跳转外部浏览器）。

```bash
--force-internal-navigation
```

### --disabled-web-shortcuts

禁用 Pake 内置的 Web 快捷键。

```bash
--disabled-web-shortcuts
```

---

## 内置快捷键

| Mac | Windows/Linux | 功能 |
|-----|---------------|------|
| ⌘ + [ | Ctrl + ← | 返回上一页 |
| ⌘ + ] | Ctrl + → | 前进下一页 |
| ⌘ + ↑ | Ctrl + ↑ | 滚动到顶部 |
| ⌘ + ↓ | Ctrl + ↓ | 滚动到底部 |
| ⌘ + r | Ctrl + r | 刷新页面 |
| ⌘ + w | Ctrl + w | 隐藏窗口 |
| ⌘ + - | Ctrl + - | 缩小页面 |
| ⌘ + = | Ctrl + = | 放大页面 |
| ⌘ + 0 | Ctrl + 0 | 重置缩放 |
| ⌘ + L | Ctrl + L | 复制当前 URL |
| ⌘ + ⇧ + H | Ctrl + Shift + H | 返回首页 |
| ⌘ + ⌥ + I | Ctrl + Shift + I | 开发者工具（仅 debug 模式） |
| ⌘ + ⇧ + ⌫ | Ctrl + Shift + Del | 清除缓存并重启 |
