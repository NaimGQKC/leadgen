#!/usr/bin/env python3
"""Scraper -- fetches real EN and FR product pages, extracts specs."""

import csv
import json
import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

LEADS_DIR = Path(__file__).resolve().parent.parent / "leads"
REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"
TARGETS_CSV = LEADS_DIR / "targets.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,fr;q=0.8",
}

SPEC_KEYWORDS = [
    "gore-tex", "goretex", "down", "duvet", "fill power", "pouvoir gonflant",
    "waterproof", "imperméable", "étanche", "seam-sealed", "coutures scellées",
    "nylon", "polyester", "cashmere", "cachemire", "wool", "laine",
    "leather", "cuir", "lambskin", "agneau", "coyote", "fur", "fourrure",
    "insulation", "isolation", "breathable", "respirant", "windproof", "coupe-vent",
    "ripstop", "DWR", "YKK", "bluesign", "recycled", "recyclé",
]


def fetch_page(url, timeout=15):
    """Fetch a page and return parsed soup + raw text."""
    if not url or url.strip() == "":
        return None, ""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        # Remove script/style
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        text = soup.get_text(separator=" ", strip=True)
        return soup, text
    except Exception as e:
        print(f"  [WARN] Failed to fetch {url}: {e}")
        return None, ""


def extract_specs(text):
    """Extract technical specs from page text."""
    text_lower = text.lower()
    found = []
    for kw in SPEC_KEYWORDS:
        if kw.lower() in text_lower:
            found.append(kw)
    return found


def extract_price(text):
    """Try to extract price from page text."""
    patterns = [
        r'\$\s*[\d,]+(?:\.\d{2})?',
        r'CAD\s*\$?\s*[\d,]+(?:\.\d{2})?',
        r'[\d,]+(?:\.\d{2})?\s*\$',
    ]
    for pat in patterns:
        matches = re.findall(pat, text)
        if matches:
            return matches[0]
    return None


def extract_title(soup):
    """Extract product title from page."""
    if not soup:
        return ""
    # Try og:title first
    og = soup.find("meta", property="og:title")
    if og and og.get("content"):
        return og["content"]
    # Try h1
    h1 = soup.find("h1")
    if h1:
        return h1.get_text(strip=True)
    # Fallback to title tag
    title = soup.find("title")
    if title:
        return title.get_text(strip=True)
    return ""


def extract_description(soup):
    """Extract product description."""
    if not soup:
        return ""
    og = soup.find("meta", property="og:description")
    if og and og.get("content"):
        return og["content"]
    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content"):
        return meta["content"]
    return ""


def scrape_brand(brand, url_en, url_fr):
    """Scrape EN and FR pages for a brand."""
    safe_name = re.sub(r'[^\w\-]', '_', brand.lower())
    result = {
        "brand": brand,
        "en": {"url": url_en, "title": "", "description": "", "specs": [], "price": None, "scraped": False, "error": None},
        "fr": {"url": url_fr, "title": "", "description": "", "specs": [], "price": None, "scraped": False, "error": None},
    }

    for lang, url in [("en", url_en), ("fr", url_fr)]:
        if not url:
            result[lang]["error"] = "No URL provided"
            continue

        print(f"  Scraping {lang}: {url[:80]}...")
        soup, text = fetch_page(url)
        if soup:
            result[lang]["title"] = extract_title(soup)
            result[lang]["description"] = extract_description(soup)
            result[lang]["specs"] = extract_specs(text)
            result[lang]["price"] = extract_price(text)
            result[lang]["scraped"] = True
            result[lang]["text_length"] = len(text)
        else:
            result[lang]["error"] = "Failed to fetch or parse"

    out_path = REPORTS_DIR / f"{safe_name}_scraped.json"
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"  Saved to {out_path}")
    return result


def main():
    with open(TARGETS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Scraping {len(rows)} brands...\n")
    for row in rows:
        brand = row["brand"]
        url_en = row.get("product_url_en", "")
        url_fr = row.get("product_url_fr", "")
        print(f"\n[{brand}]")
        scrape_brand(brand, url_en, url_fr)

    print("\nScraping complete.")


if __name__ == "__main__":
    main()
