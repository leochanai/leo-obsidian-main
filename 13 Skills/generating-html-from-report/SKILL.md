---
name: generating-html-from-report
description: 将 A 股复盘报告转换为高度可视化的金融终端风格 HTML 页面。专门针对股市复盘报告的结构特点，提供实时数据展示风格的网页输出。
---

# A 股复盘报告转 HTML

将 A 股复盘报告转换为专业的金融终端风格 HTML 页面。遵循**"数据优先，视觉增强"**原则，将结构化的市场分析转化为沉浸式的数据仪表板体验。

## 工作流

复制此清单并跟踪进度：

```
任务进度：
- [ ] 步骤 1：解析报告结构
- [ ] 步骤 2：确定金融美学风格
- [ ] 步骤 3：建立金融设计系统
- [ ] 步骤 4：数据可视化映射
- [ ] 步骤 5：构建交互组件
- [ ] 步骤 6：生成完整 HTML
```

---

## 步骤 1：解析报告结构

A 股复盘报告具有特定的结构模式，必须识别并正确映射：

### 标准结构识别

| 报告部分 | 数据类型 | 可视化目标 |
|---------|---------|-----------|
| **大盘概览** | 指数表现、涨跌幅、成交额 | 实时数据看板（Dashboard Header） |
| **涨跌统计** | 上涨/下跌家数、涨停数、封板率 | 统计卡片（Stat Cards） |
| **热点板块** | 领涨/领跌板块、核心逻辑 | 排行榜（Ranking Table） |
| **连板龙头** | 个股表现、连板数、市场逻辑 | 高亮卡片（Highlight Cards） |
| **资金流向** | 主力资金、北向资金、两融数据 | 流向图示（Flow Diagram） |
| **重要消息** | 政策面、资金面、消息面 | 新闻卡片（News Cards） |
| **后市展望** | 技术面、机构观点、操作建议 | 分析面板（Analysis Panel） |

### 关键信息提取

1. **日期与市场状态**：从标题和大盘概览提取交易日期、市场趋势（上涨/下跌）
2. **核心数据点**：成交额、涨停数、连板数、资金流向等关键指标
3. **热点主线**：识别市场主流题材和逻辑链条
4. **风险提示**：提取所有 ⚠️ 标记的风险警告

---

## 步骤 2：确定金融美学风格

**强制风格定位**：金融终端 + 数据仪表板

### 核心设计语言

| 设计元素 | 要求 |
|---------|------|
| **Tone** | 专业、精确、高频交易终端感 |
| **Visual Identity** | 类 Bloomberg Terminal / 东方财富终端 |
| **Color Psychology** | 涨=红色、跌=绿色（符合中国股市习惯） |
| **Data Density** | 高信息密度但保持清晰可读 |

### 风格参考

- **金融终端风**：深色背景 + 荧光数据 + 网格线 + 实时闪烁效果
- **编辑杂志质感**：高质量排版 + 数据图表融合
- **极简主义**：去除干扰、聚焦关键数据

---

## 步骤 3：建立金融设计系统

### 字体配置

```css
/* 数字/数据专用 */
--font-mono: 'JetBrains Mono', 'Fira Code', 'IBM Plex Mono', monospace;

/* 标题/强调 */
--font-display: 'Space Grotesk', 'Outfit', 'Inter Tight', sans-serif;

/* 正文/说明 */
--font-body: 'Noto Sans SC', 'PingFang SC', sans-serif;
```

**字体使用原则**：
- 数字、百分比、金额 → 等宽字体（mono）
- 板块名称、股票代码 → Display 字体
- 分析文字 → 中文优化字体

### 色彩系统（中国股市配色）

```css
/* 核心数据色 */
--color-rise: #ff3b30;      /* 上涨红 */
--color-fall: #34c759;      /* 下跌绿 */
--color-neutral: #8e8e93;   /* 平盘灰 */

/* 背景层次 */
--bg-primary: #0a0a0a;      /* 深色主背景 */
--bg-secondary: #1c1c1e;    /* 卡片背景 */
--bg-tertiary: #2c2c2e;     /* 悬停/激活 */

/* 强调色 */
--accent-hot: #ff6b35;      /* 热点板块 */
--accent-capital: #00d4ff;  /* 资金流向 */
--accent-warning: #ff9500;  /* 风险提示 */

/* 文本层次 */
--text-primary: #ffffff;
--text-secondary: #ebebf5;
--text-tertiary: #8e8e93;
```

### 组件设计规范

#### 1. 数据卡片（Stat Card）

```html
<!-- 示例结构 -->
<div class="stat-card">
  <span class="stat-label">成交额</span>
  <span class="stat-value" data-trend="up">3.6 万亿</span>
  <span class="stat-change">+4787 亿</span>
</div>
```

**设计要求**：
- 大号数字（字号 ≥ 32px）
- 涨跌用颜色区分（红涨绿跌）
- 微妙的边框发光效果

#### 2. 排行榜表格（Ranking Table）

**特性**：
- 斑马纹（Zebra Striping）
- 悬停高亮整行
- 涨跌幅列使用柱状图背景
- 排名前三使用特殊标记（🥇🥈🥉 禁用！用 SVG 图标代替）

#### 3. 连板龙头展示

**设计方向**：
- 使用渐变卡片区分连板高度（连板数越高，渐变越强烈）
- 添加脉冲动画模拟"涨停板"闪烁效果
- 卡片顶部显示连板数字徽章

#### 4. 资金流向可视化

**实现方式**：
- 使用 CSS Grid + Flow Arrows（SVG）
- 流入用暖色调，流出用冷色调
- 动态箭头动画

---

## 步骤 4：数据可视化映射

### 报告结构 → HTML 组件映射表

| 报告模块 | HTML 组件 | 视觉形式 |
|---------|----------|---------|
| **大盘概览表格** | Dashboard Header | 三列卡片 + 大号数字 |
| **涨跌统计** | Stat Grid | 4×2 网格统计卡片 |
| **热点板块排行** | Ranking Table | 带有涨跌幅柱状图的表格 |
| **连板龙头** | Hero Cards | 渐变卡片 + 连板数徽章 |
| **资金流向** | Flow Cards | 箭头 + 流向标签 |
| **重要消息（政策/资金/消息面）** | News Timeline | 垂直时间线 + 卡片 |
| **后市展望** | Analysis Panel | 可折叠面板 + 图标 |
| **风险提示** | Alert Banner | 顶部固定警告栏 |
| **操作建议** | Strategy Cards | 三色策略卡片（激进/稳健/防守） |

### 特殊数据增强

| 数据类型 | 增强方式 |
|---------|---------|
| **"17 连阳"、"12 连板"** | 添加 Badge + 动画高亮 |
| **"历史新高"、"创十年新高"** | 使用 ⚡ SVG 闪电图标 + 特殊颜色 |
| **百分比、涨跌幅** | 自动添加 ↑↓ 箭头（SVG） |
| **金额（万亿、亿）** | 等宽字体 + 数字分组 |

---

## 步骤 5：构建交互组件

### 必需的交互功能

1. **顶部导航**：快速跳转到各个章节（锚点导航）
2. **数据筛选**：允许按涨跌幅、连板数排序
3. **悬停提示**：展示更多细节（如个股代码、具体涨幅）
4. **折叠面板**：后市展望、机构观点默认折叠
5. **暗黑/亮色模式切换**（可选）

### 动画效果

```css
/* 数字跳动动画（模拟实时更新） */
@keyframes pulse-number {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; transform: scale(1.05); }
}

/* 涨停板闪烁效果 */
@keyframes limit-up-flash {
  0%, 100% { box-shadow: 0 0 0 rgba(255, 59, 48, 0); }
  50% { box-shadow: 0 0 20px rgba(255, 59, 48, 0.6); }
}

/* 滚动触发的淡入效果 */
.fade-in-on-scroll {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s, transform 0.6s;
}

.fade-in-on-scroll.visible {
  opacity: 1;
  transform: translateY(0);
}
```

---

## 步骤 6：输出要求

### 🎯 快速方式：使用预制模板

**推荐方式**：本 Skill 已提供完整的 HTML 模板（`template.html`），只需替换其中的占位符即可：

1. **阅读使用说明**：查看 `README.md` 了解所有占位符及其使用方法
2. **复制模板**：将 `template.html` 复制为新文件
3. **替换占位符**：根据报告内容替换 `{{占位符}}` 
4. **验证输出**：在浏览器中打开查看效果

**核心占位符：**
- `{{DATE}}` - 报告日期
- `{{INDEX_CARDS}}` - 指数卡片
- `{{STAT_CARDS}}` - 统计数据
- `{{LEADER_CARDS}}` - 连板龙头
- 其他详见 `README.md`

**优势**：
✅ 设计系统已完善，无需重新设计  
✅ 样式统一，保证视觉一致性  
✅ 快速生成，节省时间  
✅ 易于自动化脚本处理

---

### 从零构建：文件结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>2026-01-12 A股复盘 | 市场分析报告</title>
  <style>
    /* 所有 CSS 内联 */
  </style>
</head>
<body>
  <!-- 风险提示横幅（如有） -->
  <div class="risk-banner">...</div>
  
  <!-- Hero Section: 日期 + 核心数据 -->
  <header class="report-header">...</header>
  
  <!-- 导航栏 -->
  <nav class="quick-nav">...</nav>
  
  <!-- 主内容区 -->
  <main>
    <section id="overview">大盘概览</section>
    <section id="stats">涨跌统计</section>
    <section id="hotspots">热点板块</section>
    <section id="leaders">连板龙头</section>
    <section id="capital">资金流向</section>
    <section id="news">重要消息</section>
    <section id="outlook">后市展望</section>
    <section id="strategy">操作建议</section>
  </main>
  
  <!-- 页脚 -->
  <footer>
    <p>⚠️ 免责声明</p>
  </footer>
  
  <script>
    // 所有交互 JS 内联
  </script>
</body>
</html>
```

### 质量检查清单

- [ ] 所有数字使用等宽字体
- [ ] 涨跌颜色符合中国股市习惯（红涨绿跌）
- [ ] 无使用 Emoji 字符，仅使用 SVG 图标
- [ ] 响应式适配（移动端可正常阅读）
- [ ] 页面加载动画（Staggered Entrance）
- [ ] 滚动触发动画流畅
- [ ] 连板龙头有视觉高亮
- [ ] 风险提示明显可见
- [ ] 数据密度高但不拥挤

---

## 核心原则：数据优先，视觉增强

### 1. 保持金融数据的严谨性

**数据完整性 > 视觉设计**

| ❌ 错误做法 | ✅ 正确做法 |
|------------|------------|
| 为了美观省略小数点 | 保留原始数据精度 |
| 简化表格丢失关键列 | 完整展示所有数据维度 |
| 用模糊描述代替具体数字 | 精确呈现每个数据点 |
| 忽略风险提示 | 突出显示所有 ⚠️ 警告 |

### 2. 视觉增强的边界

- **增强目标**：帮助用户快速识别关键信息（如：连板龙头、热点板块、风险点）
- **禁止过度**：不为了炫技而添加无意义的动画或装饰
- **性能优先**：确保页面在低端设备上也能流畅运行

### 3. 金融终端感的营造

通过以下元素营造专业金融终端氛围：
- 深色背景 + 高对比度文字
- 等宽字体的数字排版
- 网格线和分隔符
- 微妙的数据闪烁动画
- 精确的数据对齐

---

## 示例：大盘概览转换

**Markdown 输入**：

```markdown
| 指数 | 收盘表现 | 涨跌幅 | 备注 |
|------|----------|--------|------|
| 上证指数 | 17 连阳 | +1.09% | 历史性连涨纪录 |
| 深证成指 | 探底回升 | +1.75% | 放量上攻 |
| 创业板指 | 探底回升 | +1.82% | 科技股领涨 |
```

**HTML 输出**：

```html
<div class="index-dashboard">
  <div class="index-card">
    <div class="index-name">上证指数</div>
    <div class="index-trend">
      <span class="trend-label">17 连阳</span>
      <span class="trend-badge">历史性纪录</span>
    </div>
    <div class="index-change rise">
      <span class="change-value">+1.09%</span>
      <svg class="arrow-up">...</svg>
    </div>
    <div class="index-note">历史性连涨纪录</div>
  </div>
  
  <!-- 深证成指、创业板指同理 -->
</div>
```

---

## 附录：常用 SVG 图标

### 涨跌箭头

```html
<!-- 上涨箭头 -->
<svg class="icon-rise" viewBox="0 0 24 24" fill="none">
  <path d="M12 4L12 20M12 4L6 10M12 4L18 10" stroke="currentColor" stroke-width="2"/>
</svg>

<!-- 下跌箭头 -->
<svg class="icon-fall" viewBox="0 0 24 24" fill="none">
  <path d="M12 20L12 4M12 20L6 14M12 20L18 14" stroke="currentColor" stroke-width="2"/>
</svg>
```

### 闪电图标（新高标记）

```html
<svg class="icon-lightning" viewBox="0 0 24 24" fill="currentColor">
  <path d="M13 2L3 14h8l-1 8 10-12h-8l1-8z"/>
</svg>
```

### 警告图标

```html
<svg class="icon-warning" viewBox="0 0 24 24" fill="none">
  <path d="M12 9v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" stroke-width="2"/>
</svg>
```
