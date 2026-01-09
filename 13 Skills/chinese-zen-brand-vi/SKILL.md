---
name: chinese-zen-brand-vi
description: 生成新中式禅意品牌VI系统提示词。当用户需要创建东方美学品牌识别、新中式品牌全案、禅意风格VI设计时使用。
---

# 新中式禅意品牌VI生成系统

**核心美学**：东方留白 + 宋代极简 + 日式侘寂 = 不对称平衡 + 克制优雅 + 呼吸感构图

---

## 工作流程

### 第一步：收集品牌信息

向用户收集以下信息（未提供则引导补充）：

| 必填项 | 说明 | 示例 |
|--------|------|------|
| 品牌中文名 | 2-4字 | 瑞幸 |
| 品牌口号 | 中文意境口号 | 慢品时光·归心山林 |
| 行业类型 | 咖啡/茶饮/烘焙/酒吧/零食/面馆 | 咖啡 |
| 核心角色 | 动物形象 | 鹿 |

| 可选项 | 说明 | 默认值 |
|--------|------|--------|
| 角色情绪 | serene/peaceful/mysterious/playful | 根据行业推断 |
| 主色调 | 含色值 | 查阅 `reference/COLORS.md` |
| 辅助色 | 含色值 | 查阅 `reference/COLORS.md` |
| 金属色 | gold/rose gold/bronze | gold |
| 核心产品 | 角色手持物 | 根据行业推断 |
| 装饰元素 | 背景点缀 | 查阅 `reference/ELEMENTS.md` |

---

### 第二步：组装提示词

按以下结构生成完整提示词：

#### 2.1 开场定调

```
A modern Chinese Zen aesthetic brand visual identity system displayed in a sophisticated bento grid layout on soft moon-white (#F0F0E8) background with [主色] accents. Professional brand showcase with [行业特质].
```

**行业特质映射**：
- 咖啡/茶饮 → natural woodland elegance
- 烘焙 → warm craftsmanship spirit
- 酒吧 → mysterious nocturnal elegance
- 零食 → refined elegance
- 面馆 → storytelling elements

#### 2.2 核心Logo（占 40-45%）

```
[Center dominant logo, largest element]

Graceful watercolor ink-wash portrait of an anthropomorphic [角色].

The [角色] has soft, contemplative eyes looking [视线方向] with a [情绪] expression, [角色特征描述].

Wearing [服饰] in [主色+色值] with [纹理] as subtle texture.

The [角色] is holding [核心产品] with [肢体描述] in natural, [姿态] gesture.

Surrounded by generous negative space with asymmetric ink-brushed [装饰元素], [次要元素] in misty [色调] gradients.

Elegant Chinese calligraphy "[品牌中文名]" at [位置] in refined [金属色] foil with subtle embossing, soft metallic sheen, gentle dimensional quality.

Below in [文字样式] "[品牌口号]" in matching gentle [金属色] treatment.

Watercolor texture, soft edges, breathing space composition, wabi-sabi aesthetic, refined balance.
```

#### 2.3 必备三件套（各占 8-10%）

```
[Top right position]
Minimalist business card with watercolor [角色] icon and vast negative space on cream paper, subtle [主色] edge painting, [特殊材质]

[Middle right position]
Ceramic [杯具] with [纹理] pattern and subtle [角色] silhouette in [金属色] line art, natural [光线] with [产品特征]

[Bottom right position]
Mobile app icon with soft rounded [角色] [部位] in [主色] circle, modern minimal digital design
```

#### 2.4 功能周边（3个，各占 6-8%）

根据行业选择模板，详见 `reference/ELEMENTS.md` 中的行业周边模板。

#### 2.5 创意周边（2-3个，各占 5-8%）

```
[Bottom left position]
Collection of [主题]-themed merchandise:
- [徽章/胸针]
- [工具/配件]
- [场景插画]
arranged on natural [材质] with [自然装饰] accents

[Lower right position]
Premium [产品套装]: Ceramic/Crystal [核心产品] set with [特殊工艺] glaze and [金属色] rim accent, museum-quality craftsmanship

[Small corner position]
Seasonal [会员卡] with watercolor illustrations of four seasons, each featuring [角色] in different landscape, [金属色] foil headers
```

#### 2.6 设计系统统一声明

```
All elements feature consistent refined [金属色] foil treatment with subtle dimensional quality.

Harmonious palette: moon-white (#F0F0E8), [主色+色值], [辅助色+色值], soft-sheen [金属色], charcoal ink (#3A3A3A).

Consistent [纹理] throughout, asymmetric Zen composition with 33% negative space breathing room, natural material textures with watercolor ink-wash effects.

Modern Chinese [行业] aesthetic with Japanese wabi-sabi minimalism influence, celebrating [品牌价值观].
```

#### 2.7 技术参数

```
Bento grid layout with generous 24px gaps between elements,
natural diffused [时间/氛围] light photography with soft shadows,
contemporary [场景] quality, professional brand showcase,
soft shadows 20% opacity,
visible material textures (paper grain, [材质2], [材质3]),
storytelling through artisan craftsmanship,
cohesive [美学特质] harmony,
8k resolution --ar 16:9 --stylize 245 --v 6.0
```

---

### 第三步：质量验证

生成前检查：

- [ ] 留白比例 ≥ 32%（禅意核心）
- [ ] 主色与行业匹配（参考色彩系统）
- [ ] 角色情绪符合品牌调性
- [ ] 烫金描述词：refined / subtle / gentle（非 bold / dramatic）
- [ ] 装饰元素与产品相关
- [ ] 避免过度对称（保持自然不做作）

---

## 参考资源

按需查阅：

| 文件 | 内容 |
|------|------|
| `reference/PROFILES.md` | 角色/动物库、情绪描述词 |
| `reference/COLORS.md` | 主色/辅助色/金属色系统、行业配色推荐 |
| `reference/ELEMENTS.md` | 装饰元素、文化纹理、品牌口号库、行业周边模板 |

---

## 完整示例

咖啡品牌「瑞幸」的完整输出：

```
A modern Chinese Zen aesthetic brand visual identity system displayed in a sophisticated bento grid layout on soft moon-white (#F0F0E8) background with smoke blue (#8FA3AD) accents. Professional brand showcase with natural woodland elegance.

Graceful watercolor ink-wash portrait of an anthropomorphic deer.

The deer has soft, contemplative eyes looking slightly downward with a serene expression, elegant antlers in smoke blue (#8FA3AD) with subtle natural linen weave texture.

Wearing a refined robe in tea brown (#8B7355) with misty gradient as subtle texture.

The deer is holding a delicate coffee cup with its front hooves in natural, relaxed gesture.

Surrounded by generous negative space with asymmetric ink-brushed coffee cherries, pine needles in misty forest moss green (#6B8E5A) gradients.

Elegant Chinese calligraphy "瑞幸" at top center in refined soft gold (#C9A961) foil with subtle embossing, soft metallic sheen, gentle dimensional quality.

Below in serif typography "慢品时光·归心山林" in matching gentle soft gold treatment.

Watercolor texture, soft edges, breathing space composition, wabi-sabi aesthetic, refined balance.

[Top right position]
Minimalist business card with watercolor deer icon and vast negative space on cream paper, subtle smoke blue edge painting, natural linen texture

[Middle right position]
Ceramic coffee cup with matte smoke blue glaze and subtle deer silhouette in soft gold line art, natural morning light with soft shadow

[Bottom right position]
Mobile app icon with soft rounded deer head in soft gold circle, modern minimal digital design

[Top left position]
Takeaway cup sleeve with single brushstroke deer and coffee cherries pattern, natural kraft paper with smoke blue ink, elegant typography

[Middle left position, larger]
Coffee ritual gift set in wooden box: ceramic cup with Song Dynasty crackle glaze, bamboo stirrer, soft gold coffee scoop, arranged with smoke blue fabric lining, artisan presentation

[Center bottom position]
Premium coffee bean storage tin collection: cylindrical metal tins with matte smoke blue finish, wax seal stamps featuring deer elements, different roast levels labeled with calligraphy, arranged in bamboo tray

[Bottom left position]
Collection of forest-themed merchandise:
- Deer brooch pin
- Pine needle bookmark
- Coffee cherry pattern coaster
- Deer figurine
arranged on natural wood with forest accents

[Lower right position]
Premium coffee set: Crystal cups with special craft glaze and soft gold rim accent, museum-quality craftsmanship

[Small corner position]
Seasonal membership cards with watercolor illustrations of four seasons, each featuring deer in different landscape, soft gold foil headers

All elements feature consistent refined soft gold foil treatment with subtle dimensional quality.

Harmonious palette: moon-white (#F0F0E8), smoke blue (#8FA3AD), forest moss green (#6B8E5A), soft-sheen soft gold (#C9A961), charcoal ink (#3A3A3A).

Consistent natural linen weave texture throughout, asymmetric Zen composition with 33% negative space breathing room, natural material textures with watercolor ink-wash effects.

Modern Chinese coffee aesthetic with Japanese wabi-sabi minimalism influence, celebrating slow living and natural serenity.

Bento grid layout with generous 24px gaps between elements,
natural diffused morning light photography with soft shadows,
contemporary natural setting quality, professional brand showcase,
soft shadows 20% opacity,
visible material textures (paper grain, natural linen, wood grain, ceramic),
storytelling through artisan craftsmanship,
cohesive serene harmony,
8k resolution --ar 16:9 --stylize 245 --v 6.0
```
