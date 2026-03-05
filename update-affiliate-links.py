#!/usr/bin/env python3
"""
批量更新 PetFoodLab 文章的 Amazon 联盟链接
使用搜索联盟链接格式：https://www.amazon.com/s?k=关键词&tag=zuokun300-21
"""

import re
from pathlib import Path

# 你的 Amazon Associates 联盟 ID
AFFILIATE_TAG = "zuokun300-21"

# 品牌到搜索关键词的映射
BRAND_KEYWORDS = {
    # 狗粮品牌
    "Orijen": "orijen+dog+food",
    "Acana": "acana+dog+food",
    "Hill's Science Diet": "hills+science+diet+dog+food",
    "Blue Buffalo": "blue+buffalo+dog+food",
    "Wellness CORE": "wellness+core+dog+food",
    "Royal Canin": "royal+canin+dog+food",
    "Purina Pro Plan": "purina+pro+plan+dog+food",
    "Taste of the Wild": "taste+of+the+wild+dog+food",
    "Merrick": "merrick+dog+food",
    "Nutro": "nutro+dog+food",
    "Farmer's Dog": "farmers+dog+fresh+food",
    "Ollie": "ollie+fresh+dog+food",
    
    # 猫粮品牌
    "Hill's Science Diet": "hills+science+diet+cat+food",
    "Royal Canin": "royal+canin+cat+food",
    "Purina Pro Plan": "purina+pro+plan+cat+food",
    "Wellness CORE": "wellness+core+cat+food",
    "Blue Buffalo": "blue+buffalo+cat+food",
    "Orijen": "orijen+cat+food",
    "Acana": "acana+cat+food",
    "Fancy Feast": "fancy+feast+cat+food",
    "Friskies": "friskies+cat+food",
    "Iams": "iams+cat+food",
    
    # 保健品品牌
    "Zesty Paws": "zesty+paws",
    "Nutramax": "nutramax+pet+supplements",
    "VetriScience": "vetriscience+pet",
    "PetHonesty": "pethonesty",
    "Amazing Nutrition": "amazing+nutrition+pet",
}

def generate_affiliate_link(brand_name, product_type="dog+food"):
    """生成 Amazon 搜索联盟链接"""
    keyword = BRAND_KEYWORDS.get(brand_name, f"{brand_name.lower().replace(' ', '+')}+{product_type}")
    return f"https://www.amazon.com/s?k={keyword}&tag={AFFILIATE_TAG}"

def update_article_links(file_path):
    """更新文章中的联盟链接"""
    content = file_path.read_text()
    
    # 匹配现有的 amzn.to 短链接或占位符链接
    pattern_amzn = r'\[Check Price on Amazon →\]\(https://amzn\.to/[A-Za-z0-9]+\)'
    pattern_placeholder = r'\[Check Price(?: on Amazon)? →\]\(#\)'
    
    # 查找所有匹配
    matches_amzn = list(re.finditer(pattern_amzn, content))
    matches_placeholder = list(re.finditer(pattern_placeholder, content))
    total_matches = len(matches_amzn) + len(matches_placeholder)
    
    if total_matches == 0:
        print(f"  ⚠️  {file_path.name}: 没有找到需要更新的链接")
        return False
    
    # 从文章内容中推断品牌名
    content_lower = content.lower()
    detected_brands = []
    
    # 确定产品类型（先于品牌检测，以便正确匹配关键词）
    if "cat" in content_lower:
        product_type = "cat+food"
    elif "dog" in content_lower:
        product_type = "dog+food"
    else:
        product_type = "pet+supplements"
    
    # 检测品牌（优先考虑与产品类型匹配的品牌）
    for brand, keyword in BRAND_KEYWORDS.items():
        if brand.lower() in content_lower:
            # 如果关键词与产品类型匹配，优先添加
            if product_type.replace('+', ' ') in keyword:
                detected_brands.insert(0, brand)
            else:
                detected_brands.append(brand)
    
    # 替换链接 - 如果有多个品牌，使用通用搜索链接
    if detected_brands:
        # 使用第一个检测到的品牌
        affiliate_link = generate_affiliate_link(detected_brands[0], product_type)
    else:
        # 使用文章标题中的关键词
        title_match = re.search(r"title:\s*['\"](.+?)['\"]", content)
        if title_match:
            keyword = title_match.group(1).lower().replace(' ', '+').replace(':', '')[:50]
            affiliate_link = f"https://www.amazon.com/s?k={keyword}&tag={AFFILIATE_TAG}"
        else:
            affiliate_link = f"https://www.amazon.com/s?k={product_type}&tag={AFFILIATE_TAG}"
    
    # 替换所有链接
    new_content = re.sub(pattern_amzn, f"[Check Price on Amazon →]({affiliate_link})", content)
    new_content = re.sub(pattern_placeholder, f"[Check Price on Amazon →]({affiliate_link})", new_content)
    
    file_path.write_text(new_content)
    print(f"  ✅ {file_path.name}: 更新了 {total_matches} 个链接 (品牌：{detected_brands[:2] if detected_brands else '通用'})")
    return True

def main():
    blog_dir = Path("/Users/zuokun/.openclaw/workspace/petfoodlab/src/content/blog")
    
    print(f"🔗 开始更新 Amazon 联盟链接 (Tag: {AFFILIATE_TAG})\n")
    
    updated = 0
    for md_file in sorted(blog_dir.glob("*.md")):
        if update_article_links(md_file):
            updated += 1
    
    print(f"\n✨ 完成！更新了 {updated} 篇文章")

if __name__ == "__main__":
    main()
