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


def is_valid_response(text):
    """Check if a response is real (not placeholder or error)."""
    if not text:
        return False
    if "[ERROR]" in text or "[TO BE FILLED" in text:
        return False
    return True


def brand_in_text(brand, text):
    """Check if brand appears in text (case-insensitive). Handles sub-brands and variants."""
    if not is_valid_response(text):
        return None  # Unknown
    text_lower = text.lower()
    brand_lower = brand.lower()
    # Direct match
    if brand_lower in text_lower:
        return True
    # Handle variants: "Arc'teryx" -> also check "arcteryx", "arc teryx"
    brand_stripped = re.sub(r"['\-\s]", "", brand_lower)
    text_stripped = re.sub(r"['\-\s]", "", text_lower)
    if brand_stripped in text_stripped:
        return True
    # Handle "Aldo Group" -> check for just "Aldo"
    first_word = brand_lower.split()[0] if " " in brand_lower else None
    if first_word and len(first_word) >= 3 and first_word in text_lower:
        return True
    return False


def find_brand_rank(brand, text):
    """Try to find what position/rank the brand appears at in a list."""
    if not is_valid_response(text):
        return None
    lines = text.split("\n")
    brand_lower = brand.lower()
    brand_stripped = re.sub(r"['\-\s]", "", brand_lower)
    first_word = brand_lower.split()[0] if " " in brand_lower else None

    for i, line in enumerate(lines):
        line_lower = line.lower()
        line_stripped = re.sub(r"['\-\s]", "", line_lower)
        found = (brand_lower in line_lower or
                 brand_stripped in line_stripped or
                 (first_word and len(first_word) >= 3 and first_word in line_lower))
        if found:
            match = re.match(r'^\s*(\d+)', line)
            if match:
                return int(match.group(1))
            return i + 1
    return None


def count_specs_in_text(text):
    """Count technical specs using pattern matching for materials, measurements, tech names, pricing."""
    if not is_valid_response(text):
        return 0

    count = 0
    text_lower = text.lower()

    # Materials (EN + FR)
    materials = [
        r"gore[\-\s]?tex", r"nylon", r"polyester", r"cashmere", r"cachemire",
        r"leather", r"cuir", r"lambskin", r"agneau", r"down\b", r"duvet",
        r"ripstop", r"merino", r"alpaca", r"alpaga", r"wool", r"laine",
        r"silk", r"soie", r"cotton", r"coton", r"canvas", r"toile",
        r"suede", r"daim", r"rubber", r"caoutchouc", r"eva\b", r"tpr\b",
        r"pu\b", r"kevlar", r"cordura", r"pertex", r"primaloft",
        r"thinsulate", r"polartec", r"lycra", r"spandex", r"elastane",
        r"satin", r"velour", r"velvet", r"fleece", r"textile",
    ]
    for pat in materials:
        if re.search(pat, text_lower):
            count += 1

    # Measurements: weight (g/kg), length (mm/cm), denier (D), volume (cc/L), power (hp/ch)
    if re.search(r'\d+\s*g\b', text_lower):
        count += 1
    if re.search(r'\d+\s*mm\b', text_lower):
        count += 1
    if re.search(r'\d+\s*d\b', text_lower):  # denier
        count += 1
    if re.search(r'\d+\s*cc\b', text_lower):
        count += 1
    if re.search(r'\d+\s*(hp|ch|chevaux)\b', text_lower):
        count += 1
    if re.search(r'\d+\s*kg\b', text_lower):
        count += 1
    if re.search(r'\d+\s*cm\b', text_lower):
        count += 1
    if re.search(r'fill[\-\s]?power', text_lower):
        count += 1
    if re.search(r'ret\s*[<>]\s*\d', text_lower):
        count += 1
    if re.search(r'hydrostatic|colonne\s+d.eau', text_lower):
        count += 1

    # Pricing ($ or CAD or prix)
    if re.search(r'[\$]\s*\d+|\d+\s*\$|\d+\s*cad\b', text_lower):
        count += 1

    # Technology names (brand-specific)
    tech_names = [
        r"stormhood", r"futurelight", r"e[\-\s]?tec", r"rotax",
        r"dwr\b", r"bluesign", r"recco", r"ykk", r"vislon",
        r"watertight", r"thermoscell[eé]", r"seam[\-\s]?tape", r"seam[\-\s]?seal",
        r"coutures?\s+(thermo)?scell[eé]", r"n[\-\s]?fuse",
        r"waterproof", r"imperm[eé]able", r"breathable", r"respirant",
        r"windproof", r"coupe[\-\s]?vent", r"insulation", r"isolation",
        r"earthkind", r"h2no", r"omni[\-\s]?heat", r"omni[\-\s]?tech",
        r"windstopper", r"solartex", r"hyvent", r"goretex",
    ]
    for pat in tech_names:
        if re.search(pat, text_lower):
            count += 1

    # Construction terms
    construction = [
        r"recycl[eé]", r"recycled", r"pit\s*zip", r"a[eé]ration",
        r"helmet[\-\s]?compatible", r"compatible\s+casque",
        r"harness[\-\s]?compatible", r"compatible\s+baudrier",
        r"velcro", r"snap", r"zipper", r"fermeture",
    ]
    for pat in construction:
        if re.search(pat, text_lower):
            count += 1

    return count


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
    if not is_valid_response(text):
        return []
    text_lower = text.lower()
    brand_lower = brand.lower()
    brand_first = brand_lower.split()[0] if " " in brand_lower else brand_lower
    results = []
    for b in known_brands:
        b_lower = b.lower()
        b_first = b_lower.split()[0] if " " in b_lower else b_lower
        # Skip if it's the brand itself
        if b_lower == brand_lower or b_first == brand_first:
            continue
        if b_lower in text_lower:
            results.append(b)
    return results


def detect_pricing(text):
    """Check if pricing info is present in text."""
    if not is_valid_response(text):
        return False
    return bool(re.search(r'[\$]\s*\d+|\d+\s*\$|\d+\s*cad\b|\d+\s*€', text.lower()))


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
            ratio = fr_specs / en_specs
            spec_score = min(20, int(ratio * 20))
            score += spec_score
            details["spec_ratio"] = round(ratio, 2)
        elif fr_specs > 0:
            # FR has specs but EN somehow didn't match -- still give credit
            score += 15
            details["spec_ratio"] = "fr_only"
        else:
            score += 10  # Unknown
            details["spec_ratio"] = "unknown"
        details["en_spec_count"] = en_specs
        details["fr_spec_count"] = fr_specs

        # +15: No competitor hijacking in FR
        # Hijacking = competitor appears in FR generic AND brand does NOT appear
        fr_comps_in_generic = extract_competitors(fr_a, brand)
        en_comps_in_generic = extract_competitors(en_a, brand)
        # Only flag hijacking if brand is ABSENT in FR but competitors are present
        hijack_detected = (fr_present is False and len(fr_comps_in_generic) > 0)
        if not hijack_detected:
            score += 15
            details["hijacking"] = False
        else:
            details["hijacking"] = True
            details["hijacked_by"] = fr_comps_in_generic[:3]

        # +15: Pricing accurate in FR
        en_has_price = detect_pricing(en_b)
        fr_has_price = detect_pricing(fr_b)
        if en_has_price and fr_has_price:
            score += 15
            details["pricing_check"] = "both_present"
        elif not en_has_price and not fr_has_price:
            score += 8  # Unknown / N/A category
            details["pricing_check"] = "none"
        elif fr_has_price and not en_has_price:
            score += 15  # FR actually has more info
            details["pricing_check"] = "fr_only"
        else:
            score += 5  # EN has price, FR doesn't -- mild penalty
            details["pricing_check"] = "en_only"

        details["competitors_in_fr_generic"] = fr_comps_in_generic[:5]
        details["competitors_in_en_generic"] = en_comps_in_generic[:5]
        # Ghosting: brand absent in FR generic. Case-insensitive full-text check already done above.
        details["ghosted"] = (fr_present is False)
        llm_scores[llm_name] = {"score": min(100, score), "details": details}

    # Average across available LLMs (skip those with all placeholder text)
    valid_scores = []
    for k, v in llm_scores.items():
        # Check if this LLM has any real responses
        has_real = False
        for probe_key in ["probeA_generic", "probeB_accuracy", "probeC_competitive"]:
            llm_resp = responses.get(probe_key, {}).get(k, {})
            if is_valid_response(llm_resp.get("en", "")) or is_valid_response(llm_resp.get("fr", "")):
                has_real = True
                break
        if has_real:
            valid_scores.append(v["score"])

    if not valid_scores:
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
