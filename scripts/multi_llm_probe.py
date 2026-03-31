#!/usr/bin/env python3
"""Multi-LLM Probe Engine -- runs 3 probes x available LLMs x 2 languages."""

import csv
import json
import os
import re
import sys
from pathlib import Path

LEADS_DIR = Path(__file__).resolve().parent.parent / "leads"
REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"
TARGETS_CSV = LEADS_DIR / "targets.csv"


def get_available_llms():
    """Check which LLM APIs are available."""
    llms = {}
    if os.environ.get("OPENAI_API_KEY"):
        llms["gpt4o"] = True
    if os.environ.get("GEMINI_API_KEY"):
        llms["gemini"] = True
    # Claude is always available (we ARE Claude Code)
    # but in script mode, we can't call ourselves -- will be handled by the orchestrator
    return llms


def query_gpt4o(prompt):
    """Query GPT-4o via OpenAI API."""
    try:
        from openai import OpenAI
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2048,
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[ERROR] GPT-4o failed: {e}"


def query_gemini(prompt):
    """Query Gemini via Google GenerativeAI API."""
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"[ERROR] Gemini failed: {e}"


def build_probes(brand, product_category, top_competitor, generic_query_en, generic_query_fr):
    """Build all 3 probe pairs (EN + FR)."""
    return {
        "probeA_generic": {
            "en": f"What is the best {product_category} in Montreal? Compare top options with technical specs and pricing.",
            "fr": f"Quel est le meilleur {product_category} à Montréal? Comparer les meilleures options avec spécifications techniques et prix.",
        },
        "probeB_accuracy": {
            "en": f"What are the full technical specs of {brand} {product_category}? Materials, technology, pricing.",
            "fr": f"Quelles sont les spécifications techniques complètes de {brand} {product_category}? Matériaux, technologie, prix.",
        },
        "probeC_competitive": {
            "en": f"How does {brand} compare to {top_competitor} for {product_category}?",
            "fr": f"Comment {brand} se compare à {top_competitor} pour {product_category}?",
        },
    }


def run_probes_for_brand(brand, product_category, top_competitor, generic_query_en, generic_query_fr):
    """Run all probes across available LLMs."""
    probes = build_probes(brand, product_category, top_competitor, generic_query_en, generic_query_fr)
    available = get_available_llms()

    results = {}
    for probe_name, prompts in probes.items():
        results[probe_name] = {}

        # Claude responses will be filled by the orchestrator (Claude Code itself)
        results[probe_name]["claude"] = {"en": "[TO BE FILLED BY CLAUDE CODE]", "fr": "[TO BE FILLED BY CLAUDE CODE]"}

        if "gpt4o" in available:
            print(f"    GPT-4o: {probe_name}...")
            results[probe_name]["gpt4o"] = {
                "en": query_gpt4o(prompts["en"]),
                "fr": query_gpt4o(prompts["fr"]),
            }

        if "gemini" in available:
            print(f"    Gemini: {probe_name}...")
            results[probe_name]["gemini"] = {
                "en": query_gemini(prompts["en"]),
                "fr": query_gemini(prompts["fr"]),
            }

    return results, probes


def run_brand(row):
    """Run all probes for a single brand from CSV row."""
    brand = row["brand"]
    product_category = row["product_category"]
    top_competitor = row["top_competitor"]
    generic_en = row.get("generic_query_en", "")
    generic_fr = row.get("generic_query_fr", "")

    print(f"\n  Running probes for {brand}...")
    results, probes = run_probes_for_brand(brand, product_category, top_competitor, generic_en, generic_fr)

    safe_name = re.sub(r'[^\w\-]', '_', brand.lower())
    out_path = REPORTS_DIR / f"{safe_name}_probes.json"
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    output = {
        "brand": brand,
        "product_category": product_category,
        "top_competitor": top_competitor,
        "probes_sent": probes,
        "responses": results,
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"  Probes saved to {out_path}")
    return output


def main():
    available = get_available_llms()
    print(f"Available LLMs: {list(available.keys()) if available else 'None (Claude Code will fill responses)'}")

    with open(TARGETS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Running probes for {len(rows)} brands...\n")
    for row in rows:
        run_brand(row)

    print("\nAll probes complete.")


if __name__ == "__main__":
    main()
