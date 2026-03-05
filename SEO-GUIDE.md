# 🚀 PetFoodLab SEO 优化指南

## ✅ 已完成的 SEO 优化

### 1. Meta 标签优化

#### 页面标题（Title Tag）
- ✅ 首页：包含主要关键词
- ✅ 文章页：动态生成，包含文章标题
- ✅ 格式：`{标题} | PetFoodLab`
- ✅ 长度：50-60 字符

#### 描述（Meta Description）
- ✅ 首页：概括网站内容
- ✅ 文章页：自动生成，包含关键词
- ✅ 长度：150-160 字符
- ✅ 包含行动号召

### 2. Open Graph（社交媒体分享）

**支持平台**:
- ✅ Facebook
- ✅ Twitter
- ✅ LinkedIn
- ✅ WhatsApp

**OG 标签**:
```html
<meta property="og:type" content="article" />
<meta property="og:title" content="..." />
<meta property="og:description" content="..." />
<meta property="og:image" content="..." />
<meta property="og:url" content="..." />
```

### 3. Twitter Cards

**卡片类型**: `summary_large_image`

**标签**:
```html
<meta property="twitter:card" content="summary_large_image" />
<meta property="twitter:title" content="..." />
<meta property="twitter:description" content="..." />
<meta property="twitter:image" content="..." />
```

### 4. 结构化数据（Schema.org）

**已实现**:
- ✅ Article Schema（文章页面）
- ✅ WebSite Schema（首页）
- ✅ Organization Schema（品牌信息）
- ✅ BreadcrumbList（面包屑导航）

**JSON-LD 格式**:
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "...",
  "author": {...},
  "publisher": {...}
}
```

### 5. Sitemap

**位置**: `/sitemap.xml`

**包含**:
- ✅ 首页
- ✅ 博客列表页
- ✅ 所有文章页
- ✅ About/Contact 页面
- ✅ 优先级设置
- ✅ 更新频率

### 6. Robots.txt

**位置**: `/robots.txt`

**配置**:
- ✅ 允许所有搜索引擎
- ✅ 指向 Sitemap
- ✅ 设置抓取延迟
- ✅ 支持主要搜索引擎

### 7. 技术 SEO

**已优化**:
- ✅ 响应式设计（移动端友好）
- ✅ HTTPS（Vercel 自动）
- ✅ 快速加载（静态生成）
- ✅ 语义化 HTML
- ✅ 图片懒加载
- ✅ 规范 URL（Canonical）

---

## 📋 SEO 检查清单

### 发布前检查

- [ ] 标题包含主要关键词
- [ ] 描述包含关键词 + 行动号召
- [ ] 图片有 alt 文本
- [ ] URL 简洁有意义
- [ ] 内部链接合理
- [ ] 结构化数据验证通过

### 发布后检查

- [ ] 提交到 Google Search Console
- [ ] 提交到 Bing Webmaster Tools
- [ ] 检查索引状态
- [ ] 监控搜索排名
- [ ] 分析流量来源

---

## 🔍 关键词策略

### 主要关键词

| 关键词 | 搜索量 | 难度 | 目标页面 |
|--------|--------|------|----------|
| best dog food 2026 | 高 | 中 | /blog/best-dog-food-2026 |
| best cat food | 高 | 中 | /blog/best-cat-food-2026 |
| dog food reviews | 中 | 低 | /blog |
| pet food recommendations | 中 | 低 | / |
| puppy food guide | 中 | 低 | /blog/best-puppy-food-2026 |

### 长尾关键词

- "best dog food for sensitive stomachs"
- "grain free vs grain inclusive dog food"
- "best probiotics for dogs 2026"
- "how to choose puppy food"
- "senior cat food recommendations"

---

## 📊 监控工具

### Google Search Console

**提交网站**:
1. 访问 https://search.google.com/search-console
2. 添加网站 `https://petfoodlab.it.com`
3. 验证所有权（DNS 或 HTML 文件）
4. 提交 Sitemap: `/sitemap.xml`

**监控指标**:
- 索引页面数
- 搜索展示次数
- 点击率（CTR）
- 平均排名
- 核心网页指标

### Google Analytics

**设置**:
1. 创建 GA4 属性
2. 获取 Measurement ID
3. 添加到网站（在 BaseLayout.astro 中）

**追踪指标**:
- 页面浏览量
- 用户来源
- 跳出率
- 平均停留时间
- 转化目标

---

## 🎯 内容优化建议

### 标题优化

**好标题**:
```
Best Dog Food 2026: Top 10 Brands Reviewed
```

**避免**:
```
Dog Food Review
```

### 描述优化

**好描述**:
```
After testing 50+ dog food brands, here are our top picks for 2026. 
Independent reviews, science-backed recommendations. Find the best 
food for your dog now.
```

**避免**:
```
We review dog food. Read our reviews.
```

### 内容结构

```
H1: 主标题（包含关键词）
  H2: 快速总结
  H2: 评测流程
  H2: Top 10 榜单
    H3: #1 产品
    H3: #2 产品
  H2: 购买指南
  H2: FAQ
```

---

## 🔗 内部链接策略

### 链接结构

```
首页
├── /blog（博客列表）
│   ├── /blog/best-dog-food-2026
│   ├── /blog/best-cat-food-2026
│   └── ...
├── /about
└── /contact
```

### 锚文本

**好**:
```
Read our full review of best dog food →
```

**避免**:
```
Click here →
```

---

## 📈 性能优化

### Core Web Vitals

**目标**:
- LCP (Largest Contentful Paint): < 2.5s
- FID (First Input Delay): < 100ms
- CLS (Cumulative Layout Shift): < 0.1

**优化措施**:
- ✅ 静态生成（Astro）
- ✅ 图片懒加载
- ✅ CSS 内联关键样式
- ✅ 最小化 JavaScript

---

## 🎯 下一步行动

1. **验证结构化数据**
   - 使用 Google Rich Results Test
   - 网址：https://search.google.com/test/rich-results

2. **提交到搜索引擎**
   - Google Search Console
   - Bing Webmaster Tools

3. **监控排名**
   - 设置关键词追踪
   - 每周检查排名变化

4. **持续优化**
   - 每月更新旧内容
   - 添加新文章
   - 优化内部链接

---

*最后更新：2026-03-05*
