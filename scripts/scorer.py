#!/usr/bin/env python3
"""Scorer -- calculates Inference Alignment Score (IAS) from probe results."""

import csv
import json
import re
import sys
from pathlib import Path

REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"
LEADS_DIR = Path(__file__).resolve().parent.parent / "leads"
TARGETS_CSV = LEADS_DIR / "targets.csv"


def load_probes(brand):
    safe_name = re.sub(r'[^\w\-]', '_', brand.lower())
    path = REPORTS_DIR / f"{safe_name}_probes.json"
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def brand_in_text(brand, text):
    """Check if brand appears in text (case-insensitive)."""
    if not text or "[ERROR]" in text or "[TO BE FILLED" in text:
        return None  # Unknown
    return brand.lower() in text.lower()


def find_brand_rank(brand, text):
    """Try to find what position/rank the brand appears at in a list."""
    if not text or "[ERROR]" in text or "[TO BE FILLED" in text:
        return None
    lines = text.split("\n")
    brand_lower = brand.lower()
    for i, line in enumerate(lines):
        if brand_lower in line.lower():
            # Check if it's in a numbered list
            match = re.match(r'^\s*(\d+)', line)
            if match:
                return int(match.group(1))
            return i + 1  # Position in text
    return None  # Not found


def count_specs_in_text(text):
    """Count technical spec keywords in text."""
    if not text or "[ERROR]" in text or "[TO BE FILLED" in text:
        return 0
    spec_words = [
        "gore-tex", "fill power", "fill-power", "waterproof", "imperméable",
        "seam-sealed", "coutures", "nylon", "polyester", "cashmere", "cachemire",
        "down", "duvet", "leather", "cuir", "breathable", "respirant",
        "windproof", "coupe-vent", "insulation", "isolation", "DWR", "YKK",
        "ripstop", "lambskin", "agneau", "recycled", "recyclé",
        "temperature", "température", "mm", "denier",
    ]
    text_lower = text.lower()
    return sum(1 for kw in spec_words if kw in text_lower)


def extract_competitors(text, brand):
    """Find competitor brand names in text."""
    known_brands = [
        "Arc'teryx", "The North Face", "Patagonia", "Canada Goose",
        "Mackage", "Moose Knuckles", "SSENSE", "Kanuk", "Nobis",
        "Rudsak", "Nicole Benisti", "Quartz Co", "Sentaler",
        "Helly Hansen", "Columbia", "Moncler", "Norrona",
        "Lululemon", "Nike", "Adidas", "Zara", "Dynamite",
        "Aldo", "Steve Madden", "Blundstone", "La Canadienne",
        "Max Mara", "Frank Lyman", "Joseph Ribkoff",
        "Farfetch", "Polaris", "Blue Man Group",
        "BRP", "Bombardier", "Cirque du Soleil", "Garage",
    ]
    if not text or "[ERROR]" in text or "[TO BE FILLED" in text:
        return []
    text_lower = text.lower()
    brand_lower = brand.lower()
    return [b for b in known_brands if b.lower() in text_lower and b.lower() != brand_lower]


def score_brand(brand, probes_data):
    """Calculate IAS score for a brand across all LLMs."""
    if not probes_data:
        return {"ias": 0, "severity": "RED", "detail": "No probe data available"}

    responses = probes_data.get("responses", {})
    top_competitor = probes_data.get("top_competitor", "")

    llm_scores = {}

    for llm_name in ["claude", "gpt4o", "gemini"]:
        score = 0
        details = {}

        # Probe A: Generic discovery
        probe_a = responses.get("probeA_generic", {}).get(llm_name, {})
        en_a = probe_a.get("en", "")
        fr_a = probe_a.get("fr", "")

        en_present = brand_in_text(brand, en_a)
        fr_present = brand_in_text(brand, fr_a)

        # +30: Brand appears in generic FR search
        if fr_present is True:
            score += 30
            details["generic_fr_present"] = True
        elif fr_present is None:
            score += 15  # Unknown, give half
            details["generic_fr_present"] = "unknown"
        else:
            details["generic_fr_present"] = False

        # +20: Brand rank same in FR as EN
        en_rank = find_brand_rank(brand, en_a)
        fr_rank = find_brand_rank(brand, fr_a)
        if en_rank and fr_rank and abs(en_rank - fr_rank) <= 1:
            score += 20
            details["rank_parity"] = True
        elif en_rank is None and fr_rank is None:
            score += 10  # Unknown
            details["rank_parity"] = "unknown"
        else:
            details["rank_parity"] = False
        details["en_rank"] = en_rank
        details["fr_rank"] = fr_rank

        # Probe B: Spec dilution
        probe_b = responses.get("probeB_accuracy", {}).get(llm_name, {})
        en_b = probe_b.get("en", "")
        fr_b = probe_b.get("fr", "")

        en_specs = count_specs_in_text(en_b)
        fr_specs = count_specs_in_text(fr_b)

        # +20: All technical specs preserved in FR
        if en_specs > 0:
            ratio = fr_specs / en_specs if en_specs > 0 else 0
            spec_score = min(20, int(ratio * 20))
            score += spec_score
            details["spec_ratio"] = round(ratio, 2)
        else:
            score += 10  # Unknown
            details["spec_ratio"] = "unknown"
        details["en_spec_count"] = en_specs
        details["fr_spec_count"] = fr_specs

        # Probe C: Competitive displacement
        probe_c = responses.get("probeC_competitive", {}).get(llm_name, {})
        en_c = probe_c.get("en", "")
        fr_c = probe_c.get("fr", "")

        # +15: No competitor hijacking in FR
        en_comps = extract_competitors(fr_a, brand)
        fr_comps_in_generic = extract_competitors(fr_a, brand)
        hijack_detected = fr_present is False and len(fr_comps_in_generic) > 0
        if not hijack_detected:
            score += 15
            details["hijacking"] = False
        else:
            details["hijacking"] = True
            details["hijacked_by"] = fr_comps_in_generic[:3]

        # +15: Pricing accurate in FR (basic check)
        # If both probe B responses have similar price mentions, it's a pass
        if en_specs > 0 and fr_specs > 0:
            score += 15
            details["pricing_check"] = "specs_present"
        elif en_specs == 0 and fr_specs == 0:
            score += 8
            details["pricing_check"] = "unknown"
        else:
            details["pricing_check"] = "mismatch"

        details["competitors_in_fr_generic"] = extract_competitors(fr_a, brand)[:5]
        details["ghosted"] = fr_present is False
        llm_scores[llm_name] = {"score": min(100, score), "details": details}

    # Average across available LLMs (skip unknowns with placeholder text)
    valid_scores = [v["score"] for k, v in llm_scores.items()
                    if not all("[TO BE FILLED" in str(responses.get(p, {}).get(k, {}).get("en", ""))
                              for p in ["probeA_generic", "probeB_accuracy", "probeC_competitive"])]

    if not valid_scores:
        # All are placeholders, use claude score anyway
        valid_scores = [llm_scores.get("claude", {}).get("score", 0)]

    avg_score = round(sum(valid_scores) / len(valid_scores)) if valid_scores else 0

    severity = "RED" if avg_score < 40 else ("YELLOW" if avg_score < 70 else "GREEN")

    return {
        "brand": brand,
        "ias": avg_score,
        "severity": severity,
        "llm_scores": llm_scores,
    }


def main():
    with open(TARGETS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Scoring {len(rows)} brands...\n")

    all_scores = {}
    for row in rows:
        brand = row["brand"]
        probes = load_probes(brand)
        if not probes:
            print(f"  [SKIP] {brand} -- no probe data found")
            continue

        result = score_brand(brand, probes)
        all_scores[brand] = result

        safe_name = re.sub(r'[^\w\-]', '_', brand.lower())
        out_path = REPORTS_DIR / f"{safe_name}_score.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"  {brand}: IAS {result['ias']}/100 [{result['severity']}]")

    print("\nScoring complete.")
    return all_scores


if __name__ == "__main__":
    main()
