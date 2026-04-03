#!/usr/bin/env python3
"""Source Scorer -- classifies sources from AI responses and calculates Source Authority Scores."""

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"
LEADS_DIR = Path(__file__).resolve().parent.parent / "leads"
TARGETS_CSV = LEADS_DIR / "targets.csv"

PRIORITY_BRANDS = [
    "SSENSE", "Arc'teryx", "Mackage", "Moose Knuckles", "Kanuk", "Nicole Benisti"
]

# --- Source classification tiers ---

BRAND_DOMAINS = {
    "arcteryx.com": 10,
    "ssense.com": 10,
    "mackage.com": 10,
    "mooseknucklescanada.com": 10,
    "kanuk.com": 10,
    "rudsak.com": 10,
    "nicolebenisti.com": 10,
    "dynamiteclothing.com": 10,
    "aldoshoes.com": 10,
    "lacanadienneshoes.com": 10,
    "franklyman.com": 10,
    "lululemon.com": 10,
    "sentaler.com": 10,
    "cirquedusoleil.com": 10,
    "brp.com": 10,
    "ski-doo.brp.com": 10,
}

RETAILER_DOMAINS = {
    "holtrenfrew.com": 8,
    "sail.ca": 8,
    "altitude-sports.com": 8,
    "simons.ca": 8,
    "sportsexperts.ca": 8,
    "mec.ca": 8,
    "nordstrom.com": 8,
    "sportchek.ca": 8,
}

REVIEW_DOMAINS = {
    "switchbacktravel.com": 6,
    "outdoorgearlab.com": 6,
    "thekit.ca": 6,
    "wirecutter.com": 6,
    "gearjunkie.com": 6,
}

NEWS_DOMAINS = {
    "cbc.ca": 4,
    "canoe.com": 4,
    "torontolife.com": 4,
    "lapresse.ca": 4,
    "ledevoir.com": 4,
    "journaldemontreal.com": 4,
    "globeandmail.com": 4,
    "montrealgazette.com": 4,
}

# Social/forum patterns checked via substring
SOCIAL_PATTERNS = {
    "reddit.com": 2,
    "quora.com": 2,
    "forum": 2,
    "youtube.com": 1,
    "instagram.com": 1,
    "tiktok.com": 1,
}


def safe_name(brand: str) -> str:
    return re.sub(r'[^\w\-]', '_', brand.lower())


def extract_domain(url: str) -> str:
    """Extract the registrable domain from a URL."""
    try:
        parsed = urlparse(url)
        host = parsed.hostname or ""
        # strip www.
        if host.startswith("www."):
            host = host[4:]
        return host.lower()
    except Exception:
        return ""


def classify_source(url: str, target_brand_safe: str) -> tuple[str, int]:
    """Classify a single URL and return (domain, score).

    SSENSE special case: ssense.com = 10 when target brand is ssense,
    otherwise 8 (retailer).
    """
    domain = extract_domain(url)
    if not domain:
        return (url, 0)

    # Check for subdomain matches (e.g. ski-doo.brp.com -> brp.com)
    # Try full domain first, then progressively strip subdomains
    domain_parts = domain.split(".")
    candidates = []
    for i in range(len(domain_parts)):
        candidates.append(".".join(domain_parts[i:]))

    # SSENSE special case
    for candidate in candidates:
        if candidate == "ssense.com":
            if target_brand_safe == "ssense":
                return (domain, 10)
            else:
                return (domain, 8)

    # Brand official sites
    for candidate in candidates:
        if candidate in BRAND_DOMAINS:
            return (domain, BRAND_DOMAINS[candidate])

    # Authorized retailers
    for candidate in candidates:
        if candidate in RETAILER_DOMAINS:
            return (domain, RETAILER_DOMAINS[candidate])

    # Review sites
    for candidate in candidates:
        if candidate in REVIEW_DOMAINS:
            return (domain, REVIEW_DOMAINS[candidate])

    # News/magazines
    for candidate in candidates:
        if candidate in NEWS_DOMAINS:
            return (domain, NEWS_DOMAINS[candidate])

    # Social/forum patterns (substring match on full domain)
    for pattern, score in SOCIAL_PATTERNS.items():
        if pattern in domain:
            return (domain, score)

    # Unknown
    return (domain, 0)


def load_json(path: Path):
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_sources_from_google_probes(data: dict) -> dict[str, list[str]]:
    """Extract sources from _google_probes.json format.

    Returns {"en": [url, ...], "fr": [url, ...]}.
    """
    en_sources = []
    fr_sources = []

    for probe_key in ["probeA_generic", "probeB_accuracy", "probeC_competitive"]:
        probe = data.get(probe_key, {})
        for llm_key, llm_data in probe.items():
            if isinstance(llm_data, dict):
                for lang in ["en", "fr"]:
                    lang_data = llm_data.get(lang, {})
                    if isinstance(lang_data, dict):
                        sources = lang_data.get("sources", [])
                        if lang == "en":
                            en_sources.extend(sources)
                        else:
                            fr_sources.extend(sources)

    return {"en": en_sources, "fr": fr_sources}


def extract_sources_from_probes(data: dict) -> dict[str, list[str]]:
    """Extract sources from _probes.json format.

    The responses.probeX.{llm}.{lang} entries that have structured data
    (google key) may contain sources. Also check for the google key
    which mirrors google_probes data.
    """
    en_sources = []
    fr_sources = []

    responses = data.get("responses", {})
    for probe_key in ["probeA_generic", "probeB_accuracy", "probeC_competitive"]:
        probe = responses.get(probe_key, {})
        for llm_key, llm_data in probe.items():
            if isinstance(llm_data, dict):
                for lang in ["en", "fr"]:
                    lang_data = llm_data.get(lang, "")
                    # If it's a dict with sources
                    if isinstance(lang_data, dict):
                        sources = lang_data.get("sources", [])
                        if lang == "en":
                            en_sources.extend(sources)
                        else:
                            fr_sources.extend(sources)
                    # If it's a string, try to extract URLs from text
                    elif isinstance(lang_data, str) and lang_data:
                        urls = re.findall(r'https?://[^\s\)\]"\'<>,]+', lang_data)
                        if lang == "en":
                            en_sources.extend(urls)
                        else:
                            fr_sources.extend(urls)

    return {"en": en_sources, "fr": fr_sources}


def score_brand(brand: str) -> dict | None:
    """Run source scoring for a single brand."""
    sn = safe_name(brand)

    # Collect all sources from available probe files
    all_en_sources = []
    all_fr_sources = []

    # Load _probes.json (multi-LLM: claude, gpt4o, gemini, google)
    probes_path = REPORTS_DIR / f"{sn}_probes.json"
    probes_data = load_json(probes_path)
    if probes_data:
        extracted = extract_sources_from_probes(probes_data)
        all_en_sources.extend(extracted["en"])
        all_fr_sources.extend(extracted["fr"])

    # Load _google_probes.json (Google AI Mode)
    google_path = REPORTS_DIR / f"{sn}_google_probes.json"
    google_data = load_json(google_path)
    if google_data:
        extracted = extract_sources_from_google_probes(google_data)
        all_en_sources.extend(extracted["en"])
        all_fr_sources.extend(extracted["fr"])

    # Load _gemini_probes.json if it exists
    gemini_path = REPORTS_DIR / f"{sn}_gemini_probes.json"
    gemini_data = load_json(gemini_path)
    if gemini_data:
        extracted = extract_sources_from_google_probes(gemini_data)
        all_en_sources.extend(extracted["en"])
        all_fr_sources.extend(extracted["fr"])

    if not all_en_sources and not all_fr_sources:
        print(f"  [{brand}] No sources found in any probe files. Skipping.")
        return None

    # Classify and deduplicate
    en_breakdown = {}
    fr_breakdown = {}

    for url in all_en_sources:
        domain, score = classify_source(url, sn)
        if domain and domain not in en_breakdown:
            en_breakdown[domain] = score

    for url in all_fr_sources:
        domain, score = classify_source(url, sn)
        if domain and domain not in fr_breakdown:
            fr_breakdown[domain] = score

    # Calculate averages
    avg_en = round(sum(en_breakdown.values()) / len(en_breakdown), 2) if en_breakdown else 0.0
    avg_fr = round(sum(fr_breakdown.values()) / len(fr_breakdown), 2) if fr_breakdown else 0.0
    gap = round(avg_en - avg_fr, 2)

    result = {
        "brand": brand,
        "avg_source_score_en": avg_en,
        "avg_source_score_fr": avg_fr,
        "source_authority_gap": gap,
        "sources_breakdown_en": dict(sorted(en_breakdown.items(), key=lambda x: -x[1])),
        "sources_breakdown_fr": dict(sorted(fr_breakdown.items(), key=lambda x: -x[1])),
        "total_sources_en": len(en_breakdown),
        "total_sources_fr": len(fr_breakdown),
    }

    # Save to reports/
    out_path = REPORTS_DIR / f"{sn}_source_scores.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"  [{brand}] EN avg={avg_en:.1f} ({len(en_breakdown)} sources) | "
          f"FR avg={avg_fr:.1f} ({len(fr_breakdown)} sources) | gap={gap:+.1f}")
    print(f"  -> {out_path}")

    return result


def load_all_brands() -> list[str]:
    """Load all brand names from targets.csv."""
    brands = []
    with open(TARGETS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            brands.append(row["brand"])
    return brands


def main():
    parser = argparse.ArgumentParser(description="Source Authority Scorer")
    parser.add_argument("brands", nargs="*", help="Brand names to score")
    parser.add_argument("--priority", action="store_true",
                        help="Score the 6 priority brands")
    args = parser.parse_args()

    if args.priority:
        brands = PRIORITY_BRANDS
    elif args.brands:
        brands = args.brands
    else:
        brands = load_all_brands()

    print(f"Source Authority Scorer -- scoring {len(brands)} brand(s)\n")

    results = []
    for brand in brands:
        result = score_brand(brand)
        if result:
            results.append(result)
        print()

    # Summary
    if results:
        print("=" * 60)
        print("SUMMARY")
        print("=" * 60)
        for r in sorted(results, key=lambda x: -abs(x["source_authority_gap"])):
            flag = "RED" if r["source_authority_gap"] > 3 else "YEL" if r["source_authority_gap"] > 1 else "OK"
            print(f"  [{flag}] {r['brand']:20s}  EN={r['avg_source_score_en']:.1f}  "
                  f"FR={r['avg_source_score_fr']:.1f}  gap={r['source_authority_gap']:+.1f}")


if __name__ == "__main__":
    main()
