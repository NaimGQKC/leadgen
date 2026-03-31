#!/usr/bin/env python3
"""Search engine -- uses Tavily API to find real product URLs and contacts."""

import csv
import json
import os
import sys
from pathlib import Path

LEADS_DIR = Path(__file__).resolve().parent.parent / "leads"
TARGETS_CSV = LEADS_DIR / "targets.csv"

def get_tavily_client():
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        print("[WARN] TAVILY_API_KEY not set. Search will be skipped.")
        return None
    from tavily import TavilyClient
    return TavilyClient(api_key=api_key)

def search_product_urls(client, brand, product_category):
    """Search for EN and FR product page URLs."""
    if not client:
        return {"en": "", "fr": ""}

    results = {}
    for lang, query in [
        ("en", f"{brand} {product_category} official product page site:{brand.lower().replace(' ', '')}.com"),
        ("fr", f"{brand} {product_category} page produit francais site:{brand.lower().replace(' ', '')}.com/fr"),
    ]:
        try:
            resp = client.search(query=query, max_results=3)
            urls = [r["url"] for r in resp.get("results", [])]
            results[lang] = urls[0] if urls else ""
        except Exception as e:
            print(f"  [WARN] Tavily search failed for {brand} ({lang}): {e}")
            results[lang] = ""
    return results

def search_contact(client, brand):
    """Search for marketing/digital lead at the brand."""
    if not client:
        return {"name": "", "role": "", "linkedin": ""}

    try:
        query = f"{brand} VP Marketing OR Director Digital OR Head of E-commerce LinkedIn"
        resp = client.search(query=query, max_results=5)
        # Return raw results for manual parsing
        for r in resp.get("results", []):
            title = r.get("title", "")
            url = r.get("url", "")
            if "linkedin.com/in/" in url:
                return {"name": "", "role": "", "linkedin": url}
        return {"name": "", "role": "", "linkedin": ""}
    except Exception as e:
        print(f"  [WARN] Contact search failed for {brand}: {e}")
        return {"name": "", "role": "", "linkedin": ""}

def update_targets_csv(updates):
    """Update targets.csv with search results."""
    if not TARGETS_CSV.exists():
        print(f"Error: {TARGETS_CSV} not found.")
        return

    rows = []
    with open(TARGETS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    for row in rows:
        brand = row["brand"]
        if brand in updates:
            u = updates[brand]
            if u.get("product_url_en"):
                row["product_url_en"] = u["product_url_en"]
            if u.get("product_url_fr"):
                row["product_url_fr"] = u["product_url_fr"]
            if u.get("contact_name"):
                row["contact_name"] = u["contact_name"]
            if u.get("contact_linkedin"):
                row["contact_linkedin"] = u["contact_linkedin"]

    with open(TARGETS_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Updated {TARGETS_CSV}")

def main():
    client = get_tavily_client()

    with open(TARGETS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    updates = {}
    for row in rows:
        brand = row["brand"]
        category = row["product_category"]
        print(f"\nSearching for {brand}...")

        urls = search_product_urls(client, brand, category)
        contact = search_contact(client, brand)

        updates[brand] = {
            "product_url_en": urls.get("en", ""),
            "product_url_fr": urls.get("fr", ""),
            "contact_name": contact.get("name", ""),
            "contact_linkedin": contact.get("linkedin", ""),
        }
        print(f"  EN URL: {urls.get('en', 'not found')}")
        print(f"  FR URL: {urls.get('fr', 'not found')}")
        print(f"  Contact: {contact}")

    update_targets_csv(updates)

if __name__ == "__main__":
    main()
