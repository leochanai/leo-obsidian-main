---
source: https://blog.meathill.com/next-js/migrate-next-js-from-vercel-to-cloudflare.html
author:
  - "[[meathill]]"
published: 2025-11-23
created: 2025-11-24
description: 一起逃离 Vercel 拥抱 Cloudflare 吧Cloudflare 云服务迁移到 OpenNext安装…
tags:
  - cloudflare
cover: "![[https://i0.wp.com/blog.meathill.com/wp-content/uploads/2025/11/1.webp?w=1600&ssl=1]]"
---

# 将 Next.js 项目从 Vercel 迁移到 Cloudflare

## 一起逃离 Vercel 拥抱 Cloudflare 吧

Vercel 再次调价之后，性价比越来越低，每个月 $20 的额度根本扛不住什么访问量；而且建站所需的各种服务（数据库，KV 等）也欠缺，所以我觉得是时候迁离 Vercel，投奔赛博菩萨 Cloudflare 的怀抱了。

不过由于 Cloudflare 平台的整体架构，其 Edge Runtime 和 Serverless runtime 都跟 Vercel，或者说标准架构存在一些不同之处，所以迁移的过程中往往需要我们做一些工作。本篇博客就来分享这些经验。

## Cloudflare 云服务

首先，Cloudflare 不仅提供 Serverless / Edge 托管，更提供一整套几乎是必须的服务器组件：

1. SQLite 接口的关系型数据库 D1，速度很快，第三方工具很多
2. 形似 Redis 的 KV 数据库
3. 存储服务 R2，兼容 AWS S3
4. Queue、Durable Object 等几乎所有服务器长线运营必须的工具

而且以上大部分都包含慷慨的免费额度，当你的产品度过极早期，需要更多额度时，$5/月也够用很久。总之，对比 Vercel 万国造且每个都要独立付费，当然是 Cloudflare 更好用。

（当然，也会越来跟 Cloudflare 绑定越来越深，这方面见仁见智吧。）

接下来，Cloudflare 更推荐我们使用他们家的 Worker 平台。以我的经验，使用 Worker 而不是 Pages 有以下好处：

1. 实时日志，方便我们查看运行时错误和 debug
2. 支持 cron trigger，可以方便的执行一些自动化操作
3. 以及更好的缓存策略，比如预渲染

自然，Worker 需要更多的工作，我们必须整体迁移到 OpenNext 才行。

## 迁移到 OpenNext

首先，请参考官方文档： [https://opennext.js.org/cloudflare/get-started](https://opennext.js.org/cloudflare/get-started)

接下来，我也会捋一遍迁移过程，并分享我的经验。

### 安装 @opennextjs/cloudflare

这个适配器会帮我们在 Cloudflare 上运行我们的 Next.js 应用。

```bash
pnpm install @opennextjs/cloudflare@latest
```

### 安装 Wrangler

Wrangler 是 Cloudflare 提供的命令行工具，可以帮我们完成很多工作，也是上面适配器的必备工具。

```bash
pnpm install --save-dev wrangler@latest
```

### 创建 wrangler 配置文件

这个配置文件会影响到最后的部署和其它云服务使用。我建议大家使用 JSON 格式，因为语法更熟悉。

```json
wrangler.jsonc{
  "$schema": "node_modules/wrangler/config-schema.json",
  "main": ".open-next/worker.js",
  "name": "<应用名称>",
  "compatibility_date": "<最近的日期>",
  "compatibility_flags": [
    "nodejs_compat",
    "global_fetch_strictly_public",
  ],
  "account_id": "<你的 account id>",
  "assets": {
    "directory": ".open-next/assets",
    "binding": "ASSETS",
  },
  "services": [
    {
      "binding": "WORKER_SELF_REFERENCE",
      "service": "<应用名称>",
    },
  ],
  "r2_buckets": [
    {
      "binding": "NEXT_INC_CACHE_R2_BUCKET",
      "bucket_name": "<BUCKET_NAME>",
    },
  ],
  "vars": {
    "NEXT_PUBLIC_SITE_URL": "<你的网站域名>"
  }
}
```

### 添加 open-next.config.ts 配置文件

在根目录添加 `open-next.config.ts` 配置文件。

```typescript
open-next.config.tsimport { defineCloudflareConfig } from "@opennextjs/cloudflare";
import r2IncrementalCache from "@opennextjs/cloudflare/overrides/incremental-cache/r2-incremental-cache";
 
export default defineCloudflareConfig({
  incrementalCache: r2IncrementalCache,
});
```

### 添加.dev.vars 文件

在根目录添加 `.dev.vars` 文件，告诉 Next.js 它应该使用哪一个 `.env` 文件。

```bash
.dev.varsNEXTJS_ENV=development
```

环境变量是比较难处理的一项工作。首先，线上使用的环境变量通常分两部分，一部分就是普通的变量，应该直接放在 `wrangler.jsonc` 的 `vars` 字段里；另一部分是需要加密的比如各种 apiKey，需要通过 `wrangler` 工具放到 secrets 里。

线上的环境变量必须保存在 `wrangler.jsonc` 里。这里我们只需要把本地开发环境所需的变量放在 `.env.development` ，覆盖线上的即可。本地密钥也可以放在 `.env` 文件里。

### 更新 package.json

需要给 `package.json` 加上以下命令，方便开发和部署。

```json
package.json"build": "next build",
"preview": "opennextjs-cloudflare build && opennextjs-cloudflare preview",
"deploy": "opennextjs-cloudflare build && opennextjs-cloudflare deploy",
"upload": "opennextjs-cloudflare build && opennextjs-cloudflare upload",
"cf-typegen": "wrangler types --env-interface CloudflareEnv cloudflare-env.d.ts",
```

其中， `deploy ` 用来完成主动部署， `upload` 用来部署开发分支， `cf-typegen` 用来生成描述文件，让 IDE 的代码补全更强力。

### 添加静态资源缓存

创建 `/public/_headers` 文件，添加以下内容，让 Cloudflare CDN 默认缓存所有静态资源，加速网站访问。

```bash
/public/_headers/_next/static/*
  Cache-Control: public,max-age=31536000,immutable
```

### 移除 pages 相关内容

从代码中移除 `export const runtime = "edge";`

并卸载掉 `@cloudflare/next-on-pages`

### 忽略掉.open-next 和.wrangler

给 `.gitignore` 添加更多的忽略项。如果使用 ESLint，也可能需要添加。

```bash
.gitignore.open-next
.next
.wrangler
```

### 本地开发

修改 `next.config.ts` ，增加 `@opennextjs/cloudflare` 提供的适配器。之后，你就可以使用 Cloudflare 提供的开发环境了。

```typescript
next.config.tsimport type { NextConfig } from "next";
 
const nextConfig: NextConfig = {
  /* config options here */
};
 
export default nextConfig;
 
import { initOpenNextCloudflareForDev } from "@opennextjs/cloudflare";
initOpenNextCloudflareForDev();
```

### 【可选】移除首页的预渲染缓存

如果你的首页需要加载远程数据，那么可能需要手动避免首页被预渲染，否则你可能会面对一个静态的首页。解决方案并不复杂，只需要给首页的 `page.tsx` 里添加下面的语句即可：

```typescript
app/page.tsx// 完全不缓存，每次都重新渲染并加载
export const dynamic = 'force-dynamic';
// 或者如果不希望完全动态，只是希望数据不缓存
// export const revalidate = 0;
```

### 完成第一次部署

接下来，建议大家执行 `pnpm run deploy` 完成第一次部署，这样会在 Cloudflare 里添加一个新的 worker，然后我们才好添加 secrets。

### 关联 GitHub 仓库

找到刚才创建的 Worker，在设置面板里找到“构建”，即可关联到我们的 GitHub 仓库。在构建配置里：

1. 删除“构建命令”（Build command）
2. 部署命令（Deploy comment）为 `pnpm run deploy`
3. 非生产分支部署命令（Non-production branches deploy comment）为 `pnpm run upload`

### 部署完成

至此，迁移完成，后面正常推代码就可以触发自动部署了。

## 总结

其实还有一些工作要做，比如配置缓存，配置可见性，等等。大家可以根据需要来操作。

希望这篇文章对大家所有帮助。如果大家对 Vercel，Cloudflare，Next.js 有任何问题或想法，欢迎留言讨论。
