#!/usr/bin/env python3
"""
SiteStripe 自动化脚本
- 打开真实浏览器，你登录 Amazon Associates
- 自动遍历每篇文章中的每个产品
- 点击 SiteStripe "Text" 按钮获取联盟链接
- 将链接保存到 collected-links.json
- 更新所有 Markdown 文章

运行方法：
  python3 sitestripe-links.py
"""

import re
import json
import time
from pathlib import Path
from urllib.parse import quote_plus
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

# ── 配置 ──────────────────────────────────────────────
AFFILIATE_TAG = "zuokun300-21"
AMAZON_BASE   = "https://www.amazon.co.uk"
BLOG_DIR      = Path(__file__).parent / "src/content/blog"
OUTPUT_JSON   = Path(__file__).parent / "collected-links.json"

# 每篇文章补充的搜索上下文词（让搜索结果更精准）
ARTICLE_CONTEXT = {
    "best-dog-food-2026.md":               "dry dog food",
    "best-puppy-food-2026.md":             "puppy food",
    "best-senior-dog-food-2026.md":        "senior dog food",
    "best-dry-dog-food-2026.md":           "dry dog food",
    "best-wet-dog-food-2026.md":           "wet dog food",
    "best-dog-food-sensitive-stomach-2026.md": "sensitive stomach dog food",
    "best-weight-loss-dog-food-2026.md":   "weight management dog food",
    "best-cat-food-2026.md":              "cat food",
    "best-kitten-food-2026.md":           "kitten food",
    "best-senior-cat-food-2026.md":       "senior cat food",
    "best-indoor-cat-food-2026.md":       "indoor cat food",
    "best-wet-cat-food-2026.md":          "wet cat food",
    "best-cat-food-weight-loss-2026.md":  "weight loss cat food",
    "best-fish-oil-for-dogs-2026.md":     "fish oil dogs",
    "best-probiotics-dogs.md":            "probiotics dogs",
    "best-probiotics-for-cats-2026.md":   "probiotics cats",
    "best-calming-treats-for-dogs-2026.md": "calming treats dogs",
}

# 匹配 ### 1. Product Name - Description
H3_RE   = re.compile(r'^###\s+\d+\.\s+([^-\n⭐]+?)(?:\s*[-–]\s*|\s*⭐)', re.MULTILINE)
LINK_RE = re.compile(r'\[Check Price on Amazon →\]\([^)]+\)')
# ──────────────────────────────────────────────────────


def extract_products() -> list[dict]:
    """从所有文章中提取 {article, product, keyword, search_url} 列表"""
    items = []
    for md in sorted(BLOG_DIR.glob("*.md")):
        context = ARTICLE_CONTEXT.get(md.name, "pet food")
        content = md.read_text()
        last_product = None
        for line in content.split("\n"):
            m = H3_RE.match(line)
            if m:
                last_product = m.group(1).strip()
            if last_product and LINK_RE.search(line):
                keyword    = f"{last_product} {context}"
                search_url = f"{AMAZON_BASE}/s?k={quote_plus(keyword)}"
                items.append({
                    "article":    md.name,
                    "product":    last_product,
                    "keyword":    keyword,
                    "search_url": search_url,
                    "link":       None,   # 待填充
                })
                last_product = None
    return items


def get_sitestripe_link(page, search_url: str, product: str) -> str | None:
    """
    访问搜索页 → 点击第一个产品 → 在产品页用 SiteStripe 获取联盟链接。
    返回链接字符串，失败返回 None。
    """
    print(f"  → 搜索: {search_url}")
    page.goto(search_url, wait_until="domcontentloaded", timeout=30_000)
    time.sleep(1.5)

    # ── 点击搜索结果中的第一个产品 ────────────────────
    try:
        link = page.locator("a.s-line-clamp-4").first
        link.wait_for(state="visible", timeout=5_000)
        product_title = link.inner_text().strip()[:60]
        print(f"  → 点击第一个结果: {product_title}")
        link.click()
        page.wait_for_load_state("domcontentloaded", timeout=20_000)
        time.sleep(1.5)
    except Exception as e:
        print(f"  ⚠️  找不到搜索结果: {e}，截图留存")
        shot = Path(__file__).parent / f"debug-{product[:20].replace(' ', '_')}.png"
        page.screenshot(path=str(shot))
        return None

    print(f"  → 产品页: {page.url[:80]}")

    # ── 点击 SiteStripe "Get Link" 按钮 ──────────────
    try:
        btn = page.locator("#amzn-ss-get-link-button").first
        btn.wait_for(state="visible", timeout=5_000)
        btn.click()
        print(f"    ✅ 点击了 Get Link 按钮")
    except Exception as e:
        shot = Path(__file__).parent / f"debug-{product[:20].replace(' ', '_')}.png"
        page.screenshot(path=str(shot))
        print(f"    ⚠️  未找到 #amzn-ss-get-link-button，截图已保存: {shot.name} ({e})")
        return None

    time.sleep(1.0)   # 等待弹出框出现

    # ── 从弹出框的 textarea 中读取链接 ────────────────
    try:
        textarea = page.locator("#amzn-ss-text-shortlink-textarea").first
        textarea.wait_for(state="visible", timeout=5_000)
        link = textarea.input_value()
        if link:
            print(f"    🔗 获取到链接: {link}")
            return link
    except Exception as e:
        print(f"    ❌ 无法读取链接 textarea: {e}")

    return None


def update_articles(items: list[dict]) -> int:
    """用收集到的链接更新 Markdown 文件"""
    # 构建 {(article, product): link} 映射
    link_map: dict[tuple, str] = {}
    for item in items:
        if item["link"]:
            link_map[(item["article"], item["product"])] = item["link"]

    total_updated = 0
    for md in sorted(BLOG_DIR.glob("*.md")):
        content  = md.read_text()
        lines    = content.split("\n")
        new_lines = []
        last_product = None
        changed = False

        for line in lines:
            m = H3_RE.match(line)
            if m:
                last_product = m.group(1).strip()

            if last_product and LINK_RE.search(line):
                link = link_map.get((md.name, last_product))
                if link:
                    new_line = LINK_RE.sub(f"[Check Price on Amazon →]({link})", line)
                    if new_line != line:
                        line = new_line
                        changed = True
                        total_updated += 1
                last_product = None

            new_lines.append(line)

        if changed:
            md.write_text("\n".join(new_lines))
            print(f"  ✅ {md.name} 已更新")

    return total_updated


def main():
    print("=" * 60)
    print("SiteStripe 联盟链接自动采集工具")
    print("=" * 60)

    # 1. 提取所有产品
    items = extract_products()
    print(f"共找到 {len(items)} 个产品链接需要采集\n")

    # 如果已有缓存，询问是否跳过已采集的
    if OUTPUT_JSON.exists():
        cached = json.loads(OUTPUT_JSON.read_text())
        cached_map = {(c["article"], c["product"]): c["link"] for c in cached if c.get("link")}
        for item in items:
            key = (item["article"], item["product"])
            if key in cached_map:
                item["link"] = cached_map[key]
        already = sum(1 for i in items if i["link"])
        print(f"发现缓存文件，已有 {already} 个链接，跳过重新采集。")
        remaining = [i for i in items if not i["link"]]
    else:
        remaining = items

    print(f"需要采集 {len(remaining)} 个链接\n")

    if remaining:
        with sync_playwright() as p:
            # 有头模式，你可以看到浏览器操作
            browser = p.chromium.launch(headless=False, slow_mo=300)
            context = browser.new_context(viewport={"width": 1280, "height": 900})
            page    = context.new_page()

            # 2. 打开 Amazon UK，等待登录
            page.goto(AMAZON_BASE, wait_until="domcontentloaded")
            print("=" * 60)
            print("请在浏览器中登录你的 Amazon Associates 账户")
            print("登录后确保页面顶部出现 SiteStripe 工具栏")
            print("准备好后，按回车继续...")
            print("=" * 60)
            input()

            # 3. 逐个采集
            for idx, item in enumerate(remaining, 1):
                print(f"\n[{idx}/{len(remaining)}] {item['article']} — {item['product']}")
                try:
                    link = get_sitestripe_link(page, item["search_url"], item["product"])
                    item["link"] = link
                except PWTimeout:
                    print("    ⏱ 超时，跳过")
                    item["link"] = None
                except Exception as e:
                    print(f"    ❌ 错误: {e}")
                    item["link"] = None

                # 每次采集后保存进度（断点续传）
                OUTPUT_JSON.write_text(json.dumps(items, ensure_ascii=False, indent=2))
                time.sleep(1.5)   # 礼貌延迟，避免频率过高

            browser.close()

    # 4. 输出采集结果摘要
    success = sum(1 for i in items if i["link"])
    fail    = len(items) - success
    print(f"\n采集完成：成功 {success}，失败 {fail}")
    print(f"链接已保存到 {OUTPUT_JSON.name}\n")

    # 5. 更新 Markdown 文件
    if success > 0:
        print("开始更新 Markdown 文章...")
        total = update_articles(items)
        print(f"\n✅ 完成！共更新 {total} 个链接")
    else:
        print("没有可用链接，Markdown 未更改。")

    # 6. 列出失败项
    failed_items = [i for i in items if not i["link"]]
    if failed_items:
        print(f"\n⚠️  以下 {len(failed_items)} 个产品未获取到链接（可手动处理）：")
        for i in failed_items:
            print(f"  - [{i['article']}] {i['product']}")
            print(f"    搜索: {i['search_url']}&tag={AFFILIATE_TAG}")


if __name__ == "__main__":
    main()
