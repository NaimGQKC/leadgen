#!/usr/bin/env python3
"""Scorer -- calculates Inference Alignment Score (IAS) from aggregated Gemini probe data + source authority."""

import csv
import json
import re
import sys
from pathlib import Path

REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"
LEADS_DIR = Path(__file__).resolve().parent.parent / "leads"
TARGETS_CSV = LEADS_DIR / "targets.csv"


# ---------------------------------------------------------------------------
# File loaders
# ---------------------------------------------------------------------------

def safe_name(brand):
    return re.sub(r'[^\w\-]', '_', brand.lower())


def load_gemini_probes(brand):
    path = REPORTS_DIR / f"{safe_name(brand)}_gemini_probes.json"
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_source_scores(brand):
    path = REPORTS_DIR / f"{safe_name(brand)}_source_scores.json"
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_probes(brand):
    """Load old-format probes for backward compatibility / fallback."""
    path = REPORTS_DIR / f"{safe_name(brand)}_probes.json"
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Helper functions (kept for fallback scoring from old probe data)
# ---------------------------------------------------------------------------

def is_valid_response(text):
    """Check if a response is real (not placeholder or error)."""
    if not text:
        return False
    if "[ERROR]" in text or "[TO BE FILLED" in text:
        return False
    if "[key not configured]" in text:
        return False
    return True


def brand_in_text(brand, text):
    """Check if brand appears in text (case-insensitive). Handles sub-brands and variants."""
    if not is_valid_response(text):
        return None  # Unknown
    text_lower = text.lower()
    brand_lower = brand.lower()
    if brand_lower in text_lower:
        return True
    brand_stripped = re.sub(r"['\-\s]", "", brand_lower)
    text_stripped = re.sub(r"['\-\s]", "", text_lower)
    if brand_stripped in text_stripped:
        return True
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
    """Count technical specs using pattern matching."""
    if not is_valid_response(text):
        return 0

    count = 0
    text_lower = text.lower()

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

    if re.search(r'\d+\s*g\b', text_lower):
        count += 1
    if re.search(r'\d+\s*mm\b', text_lower):
        count += 1
    if re.search(r'\d+\s*d\b', text_lower):
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
    if re.search(r'[\$]\s*\d+|\d+\s*\$|\d+\s*cad\b', text_lower):
        count += 1

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
        if b_lower == brand_lower or b_first == brand_first:
            continue
        if b_lower in text_lower:
            results.append(b)
    return results


# ---------------------------------------------------------------------------
# PRIMARY scoring: aggregated Gemini data + source authority
# ---------------------------------------------------------------------------

def score_appearance(agg):
    """Brand in 80%+ FR runs: +25 / 50-79%: +15 / <50%: +0"""
    rate_fr = agg.get("brand_appearance_rate_fr", 0)
    rate_en = agg.get("brand_appearance_rate_en", 0)
    if rate_fr >= 0.80:
        score = 25
    elif rate_fr >= 0.50:
        score = 15
    else:
        score = 0
    return {
        "score": score,
        "rate_fr": round(rate_fr, 2),
        "rate_en": round(rate_en, 2),
    }


def score_spec_preservation(agg):
    """Spec preservation >80%: +25 / 50-80%: +15 / <50%: +5"""
    ratio = agg.get("spec_preservation", 0)
    avg_en = agg.get("avg_specs_en", 0)
    avg_fr = agg.get("avg_specs_fr", 0)
    if ratio > 0.80:
        score = 25
    elif ratio >= 0.50:
        score = 15
    else:
        score = 5
    return {
        "score": score,
        "ratio": round(ratio, 2),
        "avg_en": round(avg_en, 1) if avg_en else 0,
        "avg_fr": round(avg_fr, 1) if avg_fr else 0,
    }


def score_competitor_displacement(agg):
    """No new competitors in FR vs EN: +20 / 1-2 new: +10 / 3+ new: +0
    'new competitors' = competitors in FR but NOT in EN."""
    comp_fr = set(agg.get("competitor_frequency_fr", {}).keys())
    comp_en = set(agg.get("competitor_frequency_en", {}).keys())
    new_in_fr = sorted(comp_fr - comp_en)
    count = len(new_in_fr)
    if count == 0:
        score = 20
    elif count <= 2:
        score = 10
    else:
        score = 0
    return {
        "score": score,
        "new_competitors_fr": new_in_fr,
        "count": count,
    }


def score_source_authority(source_data):
    """Source Authority Gap <2: +15 / 2-4: +10 / >4: +0"""
    if not source_data:
        return {"score": 0, "gap": None, "avg_en": None, "avg_fr": None}
    gap = source_data.get("source_authority_gap", 99)
    avg_en = source_data.get("avg_source_score_en", 0)
    avg_fr = source_data.get("avg_source_score_fr", 0)
    if gap < 2:
        score = 15
    elif gap <= 4:
        score = 10
    else:
        score = 0
    return {
        "score": score,
        "gap": round(gap, 1),
        "avg_en": round(avg_en, 1),
        "avg_fr": round(avg_fr, 1),
    }


def score_rank_parity(agg, brand, old_probes):
    """Brand rank same or better in FR: +15 / drops 1-5: +10 / drops 5+ or absent: +0.
    Uses old probes for rank data if gemini aggregated doesn't have it."""
    en_rank = None
    fr_rank = None

    # Try old probes for rank data (text-based rank extraction)
    if old_probes:
        responses = old_probes.get("responses", {})
        probe_a = responses.get("probeA_generic", {})
        # Try each LLM in order of preference
        for llm in ["gemini", "google", "claude", "gpt4o"]:
            llm_data = probe_a.get(llm, {})
            en_text = llm_data.get("en", "")
            fr_text = llm_data.get("fr", "")
            r_en = find_brand_rank(brand, en_text)
            r_fr = find_brand_rank(brand, fr_text)
            if r_en is not None or r_fr is not None:
                en_rank = r_en
                fr_rank = r_fr
                break

    # If we have no rank data at all, use appearance rates as proxy
    if en_rank is None and fr_rank is None:
        rate_fr = agg.get("brand_appearance_rate_fr", 0)
        rate_en = agg.get("brand_appearance_rate_en", 0)
        if rate_fr >= rate_en and rate_en > 0:
            return {"score": 15, "en_rank": None, "fr_rank": None, "note": "proxy_from_appearance"}
        elif rate_fr > 0:
            return {"score": 10, "en_rank": None, "fr_rank": None, "note": "proxy_from_appearance"}
        else:
            return {"score": 0, "en_rank": None, "fr_rank": None, "note": "no_rank_data"}

    # Brand absent in FR
    if fr_rank is None and en_rank is not None:
        return {"score": 0, "en_rank": en_rank, "fr_rank": None}

    # Brand absent in EN but present in FR -- give full credit
    if en_rank is None and fr_rank is not None:
        return {"score": 15, "en_rank": None, "fr_rank": fr_rank}

    # Both ranks available
    drop = fr_rank - en_rank  # positive = dropped positions
    if drop <= 0:
        score = 15
    elif drop <= 5:
        score = 10
    else:
        score = 0
    return {"score": score, "en_rank": en_rank, "fr_rank": fr_rank}


def score_brand_gemini(brand, gemini_data, source_data, old_probes):
    """Primary scoring path using pre-aggregated Gemini data."""
    agg = gemini_data.get("aggregated", {})

    appearance = score_appearance(agg)
    spec_pres = score_spec_preservation(agg)
    comp_disp = score_competitor_displacement(agg)
    src_auth = score_source_authority(source_data)
    rank_par = score_rank_parity(agg, brand, old_probes)

    ias = (appearance["score"] + spec_pres["score"] + comp_disp["score"]
           + src_auth["score"] + rank_par["score"])
    ias = min(100, ias)

    if ias >= 75:
        severity = "GREEN"
    elif ias >= 50:
        severity = "YELLOW"
    else:
        severity = "RED"

    return {
        "brand": brand,
        "ias": ias,
        "severity": severity,
        "breakdown": {
            "appearance": appearance,
            "spec_preservation": spec_pres,
            "competitor_displacement": comp_disp,
            "source_authority": src_auth,
            "rank_parity": rank_par,
        },
        "methodology": "gemini-2.5-flash, n=5 runs per query, 3 FR variants + 1 EN",
    }


# ---------------------------------------------------------------------------
# FALLBACK scoring: old _probes.json (same logic as v2 but with new thresholds)
# ---------------------------------------------------------------------------

def score_brand_fallback(brand, probes_data):
    """Fallback scoring from old _probes.json when Gemini data is unavailable."""
    if not probes_data:
        return {"brand": brand, "ias": 0, "severity": "RED",
                "breakdown": {}, "methodology": "fallback_no_data"}

    responses = probes_data.get("responses", {})

    # Collect data across LLMs
    all_fr_present = []
    all_en_present = []
    all_en_specs = []
    all_fr_specs = []
    all_en_comps = set()
    all_fr_comps = set()
    best_en_rank = None
    best_fr_rank = None

    for llm_name in ["claude", "gpt4o", "gemini", "google"]:
        # Probe A: Generic discovery
        probe_a = responses.get("probeA_generic", {}).get(llm_name, {})
        en_a = probe_a.get("en", "")
        fr_a = probe_a.get("fr", "")

        en_present = brand_in_text(brand, en_a)
        fr_present = brand_in_text(brand, fr_a)
        if en_present is not None:
            all_en_present.append(1 if en_present else 0)
        if fr_present is not None:
            all_fr_present.append(1 if fr_present else 0)

        r_en = find_brand_rank(brand, en_a)
        r_fr = find_brand_rank(brand, fr_a)
        if r_en is not None and (best_en_rank is None or r_en < best_en_rank):
            best_en_rank = r_en
        if r_fr is not None and (best_fr_rank is None or r_fr < best_fr_rank):
            best_fr_rank = r_fr

        # Probe B: Spec accuracy
        probe_b = responses.get("probeB_accuracy", {}).get(llm_name, {})
        en_b = probe_b.get("en", "")
        fr_b = probe_b.get("fr", "")
        es = count_specs_in_text(en_b)
        fs = count_specs_in_text(fr_b)
        if es > 0 or fs > 0:
            all_en_specs.append(es)
            all_fr_specs.append(fs)

        # Competitors from generic
        for c in extract_competitors(en_a, brand):
            all_en_comps.add(c)
        for c in extract_competitors(fr_a, brand):
            all_fr_comps.add(c)

    # Appearance
    rate_fr = sum(all_fr_present) / len(all_fr_present) if all_fr_present else 0
    rate_en = sum(all_en_present) / len(all_en_present) if all_en_present else 0
    if rate_fr >= 0.80:
        app_score = 25
    elif rate_fr >= 0.50:
        app_score = 15
    else:
        app_score = 0
    appearance = {"score": app_score, "rate_fr": round(rate_fr, 2), "rate_en": round(rate_en, 2)}

    # Spec preservation
    avg_en = sum(all_en_specs) / len(all_en_specs) if all_en_specs else 0
    avg_fr = sum(all_fr_specs) / len(all_fr_specs) if all_fr_specs else 0
    ratio = avg_fr / avg_en if avg_en > 0 else (1.0 if avg_fr > 0 else 0)
    if ratio > 0.80:
        spec_score = 25
    elif ratio >= 0.50:
        spec_score = 15
    else:
        spec_score = 5
    spec_pres = {"score": spec_score, "ratio": round(ratio, 2),
                 "avg_en": round(avg_en, 1), "avg_fr": round(avg_fr, 1)}

    # Competitor displacement
    new_in_fr = sorted(all_fr_comps - all_en_comps)
    count_new = len(new_in_fr)
    if count_new == 0:
        comp_score = 20
    elif count_new <= 2:
        comp_score = 10
    else:
        comp_score = 0
    comp_disp = {"score": comp_score, "new_competitors_fr": new_in_fr, "count": count_new}

    # Source authority -- not available in fallback
    src_auth = {"score": 0, "gap": None, "avg_en": None, "avg_fr": None}

    # Rank parity
    if best_en_rank is not None and best_fr_rank is not None:
        drop = best_fr_rank - best_en_rank
        if drop <= 0:
            rank_score = 15
        elif drop <= 5:
            rank_score = 10
        else:
            rank_score = 0
    elif best_fr_rank is None and best_en_rank is not None:
        rank_score = 0
    elif best_en_rank is None and best_fr_rank is not None:
        rank_score = 15
    else:
        rank_score = 10  # unknown, give partial
    rank_par = {"score": rank_score, "en_rank": best_en_rank, "fr_rank": best_fr_rank}

    ias = min(100, app_score + spec_score + comp_score + src_auth["score"] + rank_score)

    if ias >= 75:
        severity = "GREEN"
    elif ias >= 50:
        severity = "YELLOW"
    else:
        severity = "RED"

    return {
        "brand": brand,
        "ias": ias,
        "severity": severity,
        "breakdown": {
            "appearance": appearance,
            "spec_preservation": spec_pres,
            "competitor_displacement": comp_disp,
            "source_authority": src_auth,
            "rank_parity": rank_par,
        },
        "methodology": "fallback_from_probes.json (no gemini aggregated data)",
    }


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def score_brand(brand):
    """Score a single brand. Uses Gemini aggregated data if available, else fallback."""
    gemini_data = load_gemini_probes(brand)
    source_data = load_source_scores(brand)
    old_probes = load_probes(brand)

    if gemini_data and "aggregated" in gemini_data:
        return score_brand_gemini(brand, gemini_data, source_data, old_probes)
    elif old_probes:
        return score_brand_fallback(brand, old_probes)
    else:
        return {
            "brand": brand,
            "ias": 0,
            "severity": "RED",
            "breakdown": {},
            "methodology": "no_data_available",
        }


def load_targets(priority_filter=None):
    """Load brands from targets.csv, optionally filtering by priority."""
    with open(TARGETS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if priority_filter is not None:
        rows = [r for r in rows if r.get("priority", "") == str(priority_filter)]
    return rows


def main():
    # Parse CLI args
    brand_args = []
    priority_filter = None
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--priority" and i + 1 < len(args):
            priority_filter = args[i + 1]
            i += 2
        else:
            brand_args.append(args[i])
            i += 1

    if brand_args:
        # Score specific brands
        brands = brand_args
    else:
        # Score all brands from targets.csv
        rows = load_targets(priority_filter)
        brands = [r["brand"] for r in rows]

    print(f"Scoring {len(brands)} brand(s)...\n")

    all_scores = {}
    for brand in brands:
        result = score_brand(brand)
        all_scores[brand] = result

        sn = safe_name(brand)
        out_path = REPORTS_DIR / f"{sn}_score.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        method_tag = "gemini" if "gemini" in result.get("methodology", "") else "fallback"
        print(f"  {brand}: IAS {result['ias']}/100 [{result['severity']}] ({method_tag})")

    print("\nScoring complete.")
    return all_scores


if __name__ == "__main__":
    main()
