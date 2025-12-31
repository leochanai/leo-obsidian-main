---
name: extracting-app-icons
description: 从 macOS 应用程序中提取 icon 图标并转换为 PNG 格式。当用户需要获取 APP 图标、提取应用 icon、将 icns 转 png 时使用。
---

# 提取 macOS 应用图标

从本地 macOS 应用程序 (.app) 中提取 icon 图标，并转换为 PNG 格式。

## 工作流程

### 1. 定位图标文件

macOS 应用图标位置：`/Applications/AppName.app/Contents/Resources/*.icns`

查找 icns 文件名（通常在 Info.plist 中定义）：

```bash
# 获取应用的图标文件名
defaults read "/Applications/AppName.app/Contents/Info" CFBundleIconFile
```

**注意**：返回的文件名可能不含 `.icns` 后缀，需要手动添加。

### 2. 转换为 PNG

使用 macOS 内置的 `sips` 命令转换：

```bash
# 转换为 PNG（保持原始尺寸，通常为 1024x1024）
sips -s format png "/Applications/AppName.app/Contents/Resources/AppIcon.icns" --out ~/Pictures/AppIcon.png
```

### 3. 调整尺寸（可选）

```bash
# 指定输出尺寸（如 512x512）
sips -s format png -z 512 512 "/Applications/AppName.app/Contents/Resources/AppIcon.icns" --out ~/Pictures/AppIcon_512.png
```

## 快捷命令

一行命令提取指定应用图标：

```bash
# 替换 "AppName" 为实际应用名称
APP="AppName" && ICON=$(defaults read "/Applications/$APP.app/Contents/Info" CFBundleIconFile 2>/dev/null | sed 's/\.icns$//').icns && sips -s format png "/Applications/$APP.app/Contents/Resources/$ICON" --out ~/Pictures/"$APP".png
```

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| 找不到 icns 文件 | 检查 `Contents/Resources/` 下的 `.icns` 文件列表 |
| 图标为空或损坏 | 应用可能使用 Asset Catalog，尝试 `Assets.car` 提取 |
| 需要其他格式 | `sips` 支持 jpeg, tiff, gif, bmp 等格式 |

## 验证

转换完成后，确认输出文件存在且可正常预览：

```bash
# 验证文件并用预览打开
ls -la ~/Pictures/AppIcon.png && open ~/Pictures/AppIcon.png
```
