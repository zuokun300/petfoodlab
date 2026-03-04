# 🚀 PetFoodLab 部署指南

## 第一步：安装依赖

```bash
cd /Users/zuokun/.openclaw/workspace/petfoodlab
npm install
```

## 第二步：本地测试

```bash
npm run dev
```

访问 http://localhost:4321 查看网站

## 第三步：推送到 GitHub

```bash
git init
git add .
git commit -m "Initial commit: PetFoodLab website"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/petfoodlab.git
git push -u origin main
```

## 第四步：部署到 Vercel

1. 访问 https://vercel.com
2. 点击 "New Project"
3. 导入你的 GitHub 仓库
4. 点击 "Deploy"
5. 等待部署完成（约 1-2 分钟）

## 第五步：配置域名

1. 在 Vercel 项目设置 → Domains
2. 添加 `petfoodlab.it.com`
3. 在你的域名注册商处配置 DNS：
   ```
   Type: CNAME
   Name: petfoodlab
   Value: cname.vercel-dns.com
   ```

## 第六步：提交到 Google

1. 访问 https://search.google.com/search-console
2. 添加网站 `https://petfoodlab.it.com`
3. 验证所有权（用 DNS 记录）
4. 提交 sitemap: `https://petfoodlab.it.com/sitemap.xml`

## 第七步：配置 Google Analytics

1. 访问 https://analytics.google.com
2. 创建新属性
3. 获取 Measurement ID (G-XXXXXXXXX)
4. 添加到网站代码中

---

## ✅ 下一步

网站上线后：
1. 生成更多文章（目标：100 篇）
2. 申请 Amazon Associates 联盟
3. 在文章中插入联盟链接
4. 持续更新内容
5. 监控 Search Console 的搜索表现
