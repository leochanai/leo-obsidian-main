---
title: "aaaaalexis/obsidian-baseline: Baseline sets a new standard for your Obsidian vault experience."
source: https://github.com/aaaaalexis/obsidian-baseline
author:
  - "[[aaaaalexis]]"
published:
created: 2025-12-30
description: Baseline sets a new standard for your Obsidian vault experience. - aaaaalexis/obsidian-baseline
tags:
  - obsidian-theme
cover: "[[_Attachment/ebdfd5dbea293b607afa83d51c4222db_MD5.png]]"
---

# obsidian-baseline / obsidian-baseline

![[_Attachment/ebdfd5dbea293b607afa83d51c4222db_MD5.png]]

Baseline sets a new standard for your Obsidian vault experience — sleek, familiar, and effortlessly minimal, offering endless ways to make it yours.

Baseline 为您的 Obsidian 库体验设定了新标准 —— 时尚、熟悉且极度简约，提供无限的自定义方式。

---

## Quick Start / 快速开始

Seamlessly migrate your existing Style Settings from supported themes.

从支持的主题无缝迁移您现有的样式设置 (Style Settings)。

---

**Get started with [Style Settings Migration Tool ↗](https://aaaaalexis.github.io/obsidian-baseline/migration)**

**通过 [样式设置迁移工具 ↗](https://aaaaalexis.github.io/obsidian-baseline/migration) 开始使用**

---

Discover and share Style Settings presets in Baseline Marketplace.

在 Baseline 市场中发现并分享样式设置预设。

---

**Check out [Baseline Marketplace ↗](https://aaaaalexis.github.io/obsidian-baseline/marketplace)**

**查看 [Baseline 市场 ↗](https://aaaaalexis.github.io/obsidian-baseline/marketplace)**

---

## Overview / 概览

- **Beautifully yours** — Customize your experience to your heart's content with [Style Settings](https://github.com/mgmeyers/obsidian-style-settings)
	![[_Attachment/e694072238189e8e9421868d26aa52ff_MD5.png]]

- **Beautifully yours** — 通过 [Style Settings](https://github.com/mgmeyers/obsidian-style-settings) 尽情定制您的体验。

---

- **Minimal interface** — Clean, organized look and feel, with playful animations and effects.
	![[_Attachment/84435593a7757e9a7e3504fe8c82e713_MD5.png]]

- **Minimal interface** — 干净、有条理的外观和触感，伴有灵动的动画和效果。

---

- **Optimized for mobile** — Enhanced navigation, menus, editor, and more, with comfortable spacing for better usability.
  ![[_Attachment/e03b4897bc306a5ddc38a537f62b5bf3_MD5.png]]

- **Optimized for mobile** — 增强后的导航、菜单、编辑器等，拥有更舒适的间距以提升易用性。

---

## Features / 功能特性

Baseline supports all helper classes (e.g. block width, cards, etc.) from [Minimal](https://github.com/kepano/obsidian-minimal).

Baseline 支持来自 [Minimal](https://github.com/kepano/obsidian-minimal) 的所有辅助类（例如块宽度、卡片等）。

---

### Banner / 横幅

| Class                   | Description                                                                                 |
| ----------------------- | ------------------------------------------------------------------------------------------- |
| `banner`                | Add at the end of the image link, e.g. `![[image.jpeg\|banner]]`                            |
| `banner-fade`           | Add faded edge to the banner (requires `banner`)                                            |
| `banner-icon`           | Add an emoji or letter as note icon using callout, e.g. `> [!banner-icon] 👋`               |
| `banner-title`          | Moves inline title next to the icon (requires `banner-icon`)                                |
| `y0`, `y5`... to `y100` | Adjust the vertical position of the banner (requires `banner`), from 0 to 100 in steps of 5 |

| 类                       | 描述                                                  |
| ----------------------- | --------------------------------------------------- |
| `banner`                | 添加在图片链接末尾，例如 `![[image.jpeg\|banner]]`              |
| `banner-fade`           | 为横幅添加淡入边缘（需要 `banner`）                              |
| `banner-icon`           | 使用 callout 添加表情符号或字母作为笔记图标，例如 `> [!banner-icon] 👋` |
| `banner-title`          | 将内联标题移动到图标旁边（需要 `banner-icon`）                      |
| `y0`, `y5`... to `y100` | 调整横幅的垂直位置（需要 `banner`），从 0 到 100，步长为 5              |

### Block width / 块宽度

| Class | Description |
| --- | --- |
| `wide` | Entire note uses wide line width |
| `max` | Entire note uses max line width |
| `table-100`, `bases-100`, `img-100` | Fill 100% of the pane width |
| `table-max`, `bases-max`, `img-max` | Fill the max line width (default 90%) |
| `table-wide`, `bases-wide`, `img-wide` | Fill the wide line width |

| 类 | 描述 |
| --- | --- |
| `wide` | 整个笔记使用较宽的行宽 |
| `max` | 整个笔记使用最大行宽 |
| `table-100`, `bases-100`, `img-100` | 填充 100% 的面板宽度 |
| `table-max`, `bases-max`, `img-max` | 填充最大行宽（默认 90%） |
| `table-wide`, `bases-wide`, `img-wide` | 填充较宽的行宽 |

### Cards / 卡片

| Class | Description |
| --- | --- |
| `cards` (required) | Set all Dataview tables to card layout |
| `list-cards` | Set all bullet lists to card layout |
| `cards-align-bottom` | Align the last element of a card to the bottom |
| `cards-cover` | Images are resized to fill the defined space |
| `cards-16-9` | Fit images in cards to 16:9 ratio |
| `cards-1-1` | Fit images in cards to 1:1 ratio (square) |
| `cards-2-1` | Fit images in cards to 2:1 ratio |
| `cards-2-3` | Fit images in cards to 2:3 ratio |
| `cards-cols-1` to `8` | Force a specific number of columns (from 1 to 8) |

| 类 | 描述 |
| --- | --- |
| `cards` (required) | 将所有 Dataview 表格设置为卡片布局 |
| `list-cards` | 将所有无序列表设置为卡片布局 |
| `cards-align-bottom` | 将卡片的最后一个元素底部对齐 |
| `cards-cover` | 图像调整大小以填充定义的空间 |
| `cards-16-9` | 将卡片中的图像适应为 16:9 比例 |
| `cards-1-1` | 将卡片中的图像适应为 1:1 比例（方形） |
| `cards-2-1` | 将卡片中的图像适应为 2:1 比例 |
| `cards-2-3` | 将卡片中的图像适应为 2:3 比例 |
| `cards-cols-1` to `8` | 强制指定列数（从 1 到 8） |

### Embeds / 嵌入

| Class | Description |
| --- | --- |
| `embed-strict` | Remove embed background |
| `embed-hide-title` | Hide embedded file title |

| 类 | 描述 |
| --- | --- |
| `embed-strict` | 移除嵌入背景 |
| `embed-hide-title` | 隐藏嵌入文件标题 |

### Image filters / 图像滤镜

Add at the end of the image link, e.g. `![[image.jpeg#invert]]`

添加在图片链接的末尾，例如 `![[image.jpeg#invert]]`

---

| Filter | Description |
| --- | --- |
| `#blend` | Blend image into background |
| `#invert` | Invert images in dark mode — ideal for charts and handwriting on light backgrounds |
| `#invertW` | Invert images in light mode — ideal for charts and handwriting on dark backgrounds |
| `#circle` | Crop image to a circle |
| `#outline` | Add outline around image |
| `#interface` | Add drop shadow behind image |

| 滤镜 | 描述 |
| --- | --- |
| `#blend` | 将图像混合到背景中 |
| `#invert` | 在深色模式下反转图像 —— 适用于浅色背景上的图表和手写体 |
| `#invertW` | 在浅色模式下反转图像 —— 适用于深色背景上的图表和手写体 |
| `#circle` | 将图像裁剪为圆形 |
| `#outline` | 在图像周围添加轮廓 |
| `#interface` | 在图像后添加投影 |

### Image grids / 图像网格

| Class | Description |
| --- | --- |
| `img-grid` | Activate image grids |

| 类 | 描述 |
| --- | --- |
| `img-grid` | 激活图像网格 |

### Tables / 表格

| Class | Description |
| --- | --- |
| `table-nowrap` | Disable line wrapping in table cells |
| `table-wrap` | Force line wrapping in table cells |
| `table-center` | Center small tables narrower than line width |
| `table-numbers` | Add row numbers to tables |
| `table-tabular` | Use tabular figures in tables |
| `table-small` | Use small font size in tables |
| `table-tiny` | Use tiny font size in tables |
| `table-lines` | Add borders around all table cells |
| `row-lines` | Add borders between table rows |
| `col-lines` | Add borders between table columns |
| `row-alt` | Add striped background to alternating table rows |
| `col-alt` | Add striped background to alternating table columns |
| `row-hover` | Highlight rows on hover |
| `bases-row-alt` | Add striped background to alternating Bases table view rows |
| `bases-col-alt` | Add striped background to alternating Bases table view columns |

| 类 | 描述 |
| --- | --- |
| `table-nowrap` | 禁用单元格内的换行 |
| `table-wrap` | 强制单元格内换行 |
| `table-center` | 居中显示宽度小于行宽的小表格 |
| `table-numbers` | 为表格添加行号 |
| `table-tabular` | 在表格中使用等宽数字 |
| `table-small` | 在表格中使用小号字体 |
| `table-tiny` | 在表格中使用极小号字体 |
| `table-lines` | 在所有单元格周围添加边框 |
| `row-lines` | 在行之间添加边框 |
| `col-lines` | 在列之间添加边框 |
| `row-alt` | 为交替行添加条纹背景 |
| `col-alt` | 为交替列添加条纹背景 |
| `row-hover` | 悬停时高亮显示行 |
| `bases-row-alt` | 为 Bases 表格视图的交替行添加条纹背景 |
| `bases-col-alt` | 为 Bases 表格视图的交替列添加条纹背景 |

### Alternate checkboxes / 替代复选框

![[_Attachment/c5c774db0c76de8ad39bb448720a4280_MD5.png]]

| Syntax | Description |
| --- | --- |
| `- [ ]` | To-do |
| `- [/]` | Incomplete |
| `- [x]` | Done |
| `- [-]` | Canceled |
| `- [>]` | Forwarded |
| `- [<]` | Scheduling |
| `- [?]` | Question |
| `- [!]` | Important |
| `- [*]` | Star |
| `- ["]` | Quote |
| `- [l]` | Location |
| `- [b]` | Bookmark |
| `- [i]` | Information |
| `- [S]` | Savings |
| `- [I]` | Idea |
| `- [p]` | Pros |
| `- [c]` | Cons |
| `- [f]` | Fire |
| `- [k]` | Key |
| `- [w]` | Win |
| `- [u]` | Up |
| `- [d]` | Down |
| `- [+]` | Add |
| `- [B]` | Brainstorm |
| `- [a]` | Alarm |
| `- [n]` | Note |
| `- [R]` | Review |
| `- [t]` | Time |
| `- [P]` | Phone |
| `- [L]` | Love |

| 语法 | 描述 |
| --- | --- |
| `- [ ]` | 待办 |
| `- [/]` | 未完成 |
| `- [x]` | 完成 |
| `- [-]` | 已取消 |
| `- [>]` | 已转发 |
| `- [<]` | 计划中 |
| `- [?]` | 疑问 |
| `- [!]` | 重要 |
| `- [*]` | 星标 |
| `- ["]` | 引用 |
| `- [l]` | 位置 |
| `- [b]` | 书签 |
| `- [i]` | 信息 |
| `- [S]` | 储蓄 |
| `- [I]` | 想法 |
| `- [p]` | 优点 |
| `- [c]` | 缺点 |
| `- [f]` | 热门 |
| `- [k]` | 关键 |
| `- [w]` | 胜利 |
| `- [u]` | 上升 |
| `- [d]` | 下降 |
| `- [+]` | 添加 |
| `- [B]` | 头脑风暴 |
| `- [a]` | 提醒 |
| `- [n]` | 笔记 |
| `- [R]` | 复习 |
| `- [t]` | 时间 |
| `- [P]` | 电话 |
| `- [L]` | 喜爱 |
