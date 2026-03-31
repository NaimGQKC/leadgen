#!/usr/bin/env python3
"""Multi-LLM Probe Engine -- runs 3 probes x available LLMs x 2 languages."""

import csv
import json
import os
import re
import sys
import time
from pathlib import Path

LEADS_DIR = Path(__file__).resolve().parent.parent / "leads"
REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"
TARGETS_CSV = LEADS_DIR / "targets.csv"

MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds


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
    """Query GPT-4o via OpenAI API with retry logic."""
    for attempt in range(MAX_RETRIES):
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
            err_str = str(e).lower()
            if "rate" in err_str or "429" in err_str or "quota" in err_str:
                if attempt < MAX_RETRIES - 1:
                    print(f"      Rate limited, waiting {RETRY_DELAY}s (attempt {attempt + 1}/{MAX_RETRIES})...")
                    time.sleep(RETRY_DELAY)
                    continue
            return f"[ERROR] GPT-4o failed: {e}"
    return f"[ERROR] GPT-4o failed after {MAX_RETRIES} retries"


def query_gemini(prompt):
    """Query Gemini via Google GenerativeAI API with retry logic."""
    for attempt in range(MAX_RETRIES):
        try:
            import google.generativeai as genai
            genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            err_str = str(e).lower()
            if "rate" in err_str or "429" in err_str or "quota" in err_str or "resource" in err_str:
                if attempt < MAX_RETRIES - 1:
                    print(f"      Rate limited, waiting {RETRY_DELAY}s (attempt {attempt + 1}/{MAX_RETRIES})...")
                    time.sleep(RETRY_DELAY)
                    continue
            return f"[ERROR] Gemini failed: {e}"
    return f"[ERROR] Gemini failed after {MAX_RETRIES} retries"


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


def run_probes_for_brand(brand, product_category, top_competitor, generic_query_en, generic_query_fr, existing_responses=None):
    """Run all probes across available LLMs. Preserves existing responses."""
    probes = build_probes(brand, product_category, top_competitor, generic_query_en, generic_query_fr)
    available = get_available_llms()

    results = existing_responses if existing_responses else {}
    for probe_name, prompts in probes.items():
        if probe_name not in results:
            results[probe_name] = {}

        # Keep existing claude responses
        if "claude" not in results[probe_name]:
            results[probe_name]["claude"] = {"en": "[TO BE FILLED BY CLAUDE CODE]", "fr": "[TO BE FILLED BY CLAUDE CODE]"}

        # GPT-4o
        if "gpt4o" in available:
            existing_gpt = results[probe_name].get("gpt4o", {})
            if not existing_gpt or "[TO BE FILLED" in str(existing_gpt.get("en", "")) or "[ERROR]" in str(existing_gpt.get("en", "")):
                print(f"    GPT-4o: {probe_name}...")
                results[probe_name]["gpt4o"] = {
                    "en": query_gpt4o(prompts["en"]),
                    "fr": query_gpt4o(prompts["fr"]),
                }
        elif "gpt4o" not in results[probe_name]:
            results[probe_name]["gpt4o"] = {
                "en": "[OpenAI key not configured]",
                "fr": "[OpenAI key not configured]",
            }

        # Gemini
        if "gemini" in available:
            existing_gem = results[probe_name].get("gemini", {})
            if not existing_gem or "[TO BE FILLED" in str(existing_gem.get("en", "")) or "[ERROR]" in str(existing_gem.get("en", "")):
                print(f"    Gemini: {probe_name}...")
                results[probe_name]["gemini"] = {
                    "en": query_gemini(prompts["en"]),
                    "fr": query_gemini(prompts["fr"]),
                }
        elif "gemini" not in results[probe_name]:
            results[probe_name]["gemini"] = {
                "en": "[Gemini key not configured]",
                "fr": "[Gemini key not configured]",
            }

    return results, probes


def run_brand(row):
    """Run all probes for a single brand from CSV row. Merges with existing data."""
    brand = row["brand"]
    product_category = row["product_category"]
    top_competitor = row["top_competitor"]
    generic_en = row.get("generic_query_en", "")
    generic_fr = row.get("generic_query_fr", "")

    safe_name = re.sub(r'[^\w\-]', '_', brand.lower())
    out_path = REPORTS_DIR / f"{safe_name}_probes.json"
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # Load existing probes to preserve Claude responses
    existing_responses = None
    if out_path.exists():
        with open(out_path, "r", encoding="utf-8") as f:
            existing = json.load(f)
            existing_responses = existing.get("responses", {})

    print(f"\n  Running probes for {brand}...")
    results, probes = run_probes_for_brand(
        brand, product_category, top_competitor, generic_en, generic_fr,
        existing_responses=existing_responses,
    )

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
