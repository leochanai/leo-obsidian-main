---
name: generate-fashion-magazine-cover
description: 基于人物参考图，设计并生成国际顶流时尚杂志（如 Harper's BAZAAR）的红毯封面方案。专注于直闪风格摄影、面部一致性与高端排版。
---

# 国际顶流时尚杂志封面

{
  "meta": {
    "system_instruction": "创建一张高端时尚杂志封面。使用上传的人脸进行严格的身份保留。",
    "aspect_ratio": "3:4",
    "quality": "超精细",
    "resolution": "8k",
    "style": "Met Gala 红毯活动，直闪摄影，魅力十足的名人抓拍"
  },

  "reference_usage": {
    "instruction": "严格保留上传参考中的面部身份特征（眼睛、鼻子、嘴巴）。身体比例应修长高挑，具有模特感。",
    "focus": "100% 面部身份匹配"
  },

  "scene": {
    "location": "Met Gala 红毯（纽约）",
    "environment": [
      "背景混乱，布满狗仔队相机",
      "红色天鹅绒围绳",
      "相机闪光爆发（散景光斑）",
      "深色夜空形成强烈对比"
    ],
    "atmosphere": "电力十足、私密尊贵、超级巨星气场"
  },

  "lighting": {
    "type": "直闪光（狗仔风格）",
    "effect": "高对比度硬光，皮肤闪耀光泽，人物身后形成清晰阴影，礼服上有明亮反光"
  },

  "subject": {
    "face": {
      "expression": "魅惑而自信的微笑，回眸注视镜头",
      "makeup": "浓烈红唇，锐利修容，发光高光"
    },
    "pose": {
      "action": "身体向前行走，但头部转动 45 度看向镜头",
      "body": "姿态优雅，背部微微拱起",
      "hair": "头发在风中戏剧性飞扬"
    },
    "outfit": {
      "dress": "未来感液态金属银色礼服",
      "details": "露背设计，反射相机闪光，亮片质感",
      "jewelry": "钻石颈圈，大号耳钉"
    }
  },

  "composition": {
    "layout": "杂志封面版式",
    "branding": {
      "main_logo": "顶部放置大号醒目的白色或银色“Harper's BAZAAR”标志",
      "text_elements": [
        "侧边加入中文副标题",
        "小字：'红毯之夜'",
        "主标题：'独家直击'",
        "底部文字：'年度风尚大典'"
      ]
    }
  },

  "vibe": "奢华、高价感、一线名人、光泽感杂志成品效果",
  "negative_prompt": "低分辨率、难看的手、面部扭曲、缺失标志、文字错误、水印、休闲服装、白天、柔光"
}
