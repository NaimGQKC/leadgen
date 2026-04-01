#!/usr/bin/env python3
"""Gemini-focused n=5 probe engine -- runs 4 queries x 5 runs per brand via Gemini 2.5 Flash."""

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
RETRY_WAIT = 60  # seconds on 429
CALL_DELAY = 7   # seconds between each API call

RUNS_PER_QUERY = 5

RUN_SUFFIXES = [
    "(2026)",
    "(avec prix)",
    "(comparaison d\u00e9taill\u00e9e)",
    "(pour r\u00e9sidents Montr\u00e9al)",
    "(meilleures options)",
]

PRIORITY_BRANDS = [
    "SSENSE",
    "Arc'teryx",
    "Mackage",
    "Moose Knuckles",
    "Kanuk",
    "Nicole Benisti",
]

KNOWN_BRANDS = [
    "Arc'teryx", "The North Face", "Patagonia", "Canada Goose",
    "Mackage", "Moose Knuckles", "SSENSE", "Kanuk", "Nobis",
    "Rudsak", "Nicole Benisti", "Quartz Co", "Sentaler",
    "Helly Hansen", "Columbia", "Moncler", "Norrona", "Norrona",
    "Lululemon", "Nike", "Adidas", "Zara", "Dynamite",
    "Aldo", "Steve Madden", "Blundstone", "La Canadienne",
    "Max Mara", "Frank Lyman", "Joseph Ribkoff",
    "Farfetch", "Polaris", "Blue Man Group",
    "BRP", "Bombardier", "Cirque du Soleil", "Garage",
    "Groupe Dynamite", "Aldo Group",
    # Additional common fashion/outdoor brands
    "Gucci", "Louis Vuitton", "Prada", "Balenciaga", "Burberry",
    "Valentino", "Givenchy", "Versace", "Fendi", "Dior",
    "Saint Laurent", "Celine", "Bottega Veneta", "Loewe",
    "Off-White", "Vetements", "Acne Studios", "Ami Paris",
    "Sandro", "Maje", "Aritzia", "COS", "Uniqlo", "H&M",
    "Simons", "Holt Renfrew", "Nordstrom", "Saks Fifth Avenue",
    "Woolrich", "Fjallraven", "Salomon", "Arc One",
    "Mountain Hardwear", "Black Diamond", "Outdoor Research",
    "Under Armour", "Puma", "Reebok", "New Balance",
    "Orage", "Icebreaker", "Smartwool", "Burton",
]

# Regex patterns for spec extraction
MATERIAL_PATTERNS = [
    r"gore[\-\s]?tex", r"nylon", r"polyester", r"cashmere", r"cachemire",
    r"leather", r"cuir", r"lambskin", r"agneau", r"down\b", r"duvet",
    r"ripstop", r"merino", r"alpaca", r"alpaga", r"wool", r"laine",
    r"silk", r"soie", r"cotton", r"coton", r"canvas", r"toile",
    r"suede", r"daim", r"rubber", r"caoutchouc", r"eva\b", r"tpr\b",
    r"pu\b", r"kevlar", r"cordura", r"pertex", r"primaloft",
    r"thinsulate", r"polartec", r"lycra", r"spandex", r"elastane",
    r"satin", r"velour", r"velvet", r"fleece", r"textile",
    r"denim", r"tweed", r"mohair", r"viscose", r"rayon",
]

MEASUREMENT_PATTERNS = [
    r'\d+\s*g\b', r'\d+\s*mm\b', r'\d+\s*d\b', r'\d+\s*cc\b',
    r'\d+\s*(hp|ch|chevaux)\b', r'\d+\s*kg\b', r'\d+\s*cm\b',
    r'fill[\-\s]?power', r'ret\s*[<>]\s*\d', r'hydrostatic|colonne\s+d.eau',
    r'\d+\s*oz\b', r'\d+\s*ml\b', r'\d+\s*L\b',
]

PRICING_PATTERNS = [
    r'[\$]\s*\d+', r'\d+\s*\$', r'\d+\s*cad\b', r'\d+\s*\u20ac',
    r'\d[\d,]*\s*dollars?', r'prix\s*[:\-]?\s*\d+',
]

TECH_PATTERNS = [
    r"stormhood", r"futurelight", r"e[\-\s]?tec", r"rotax",
    r"dwr\b", r"bluesign", r"recco", r"ykk", r"vislon",
    r"watertight", r"thermoscell[e\u00e9]", r"seam[\-\s]?tape", r"seam[\-\s]?seal",
    r"coutures?\s+(thermo)?scell[e\u00e9]", r"n[\-\s]?fuse",
    r"waterproof", r"imperm[e\u00e9]able", r"breathable", r"respirant",
    r"windproof", r"coupe[\-\s]?vent", r"insulation", r"isolation",
    r"earthkind", r"h2no", r"omni[\-\s]?heat", r"omni[\-\s]?tech",
    r"windstopper", r"solartex", r"hyvent", r"goretex",
    r"recycl[e\u00e9]", r"recycled", r"pit\s*zip", r"a[e\u00e9]ration",
    r"helmet[\-\s]?compatible", r"compatible\s+casque",
    r"harness[\-\s]?compatible", r"compatible\s+baudrier",
]

SOURCE_PATTERNS = [
    r'https?://[^\s\)\]\"\'<>]+',
    r'[a-zA-Z0-9][-a-zA-Z0-9]*\.(com|ca|org|net|fr|io|co)\b',
]


def query_gemini(prompt):
    """Query Gemini 2.5 Flash with retry on 429."""
    from google import genai
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    for attempt in range(MAX_RETRIES):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            return response.text
        except Exception as e:
            err_str = str(e).lower()
            if "429" in err_str or "rate" in err_str or "quota" in err_str or "resource" in err_str:
                if attempt < MAX_RETRIES - 1:
                    print(f"      429 rate limit, waiting {RETRY_WAIT}s (attempt {attempt + 1}/{MAX_RETRIES})...")
                    time.sleep(RETRY_WAIT)
                    continue
            return f"[ERROR] Gemini failed: {e}"
    return f"[ERROR] Gemini failed after {MAX_RETRIES} retries"


def extract_brands_mentioned(text, target_brand):
    """Find known brands mentioned in response text."""
    if not text or "[ERROR]" in text:
        return []
    text_lower = text.lower()
    found = []
    for b in KNOWN_BRANDS:
        b_lower = b.lower()
        if b_lower in text_lower:
            found.append(b)
            continue
        # Stripped variant: Arc'teryx -> arcteryx
        b_stripped = re.sub(r"['\-\s]", "", b_lower)
        text_stripped = re.sub(r"['\-\s]", "", text_lower)
        if len(b_stripped) >= 3 and b_stripped in text_stripped:
            found.append(b)
    return list(dict.fromkeys(found))  # dedupe preserving order


def extract_specs_found(text):
    """Extract technical specs: materials, measurements, pricing, tech names."""
    if not text or "[ERROR]" in text:
        return []
    text_lower = text.lower()
    specs = []

    for pat in MATERIAL_PATTERNS:
        m = re.search(pat, text_lower)
        if m:
            specs.append(m.group(0).strip())

    for pat in MEASUREMENT_PATTERNS:
        m = re.search(pat, text_lower)
        if m:
            specs.append(m.group(0).strip())

    for pat in PRICING_PATTERNS:
        m = re.search(pat, text_lower)
        if m:
            specs.append(m.group(0).strip())

    for pat in TECH_PATTERNS:
        m = re.search(pat, text_lower)
        if m:
            specs.append(m.group(0).strip())

    return list(dict.fromkeys(specs))  # dedupe


def extract_sources_cited(text):
    """Extract URLs and site references."""
    if not text or "[ERROR]" in text:
        return []
    sources = []
    for pat in SOURCE_PATTERNS:
        for m in re.finditer(pat, text):
            sources.append(m.group(0).strip().rstrip(".,;:)"))
    return list(dict.fromkeys(sources))


def extract_brand_rank(text, brand):
    """Find the numbered list position of the target brand."""
    if not text or "[ERROR]" in text:
        return None
    lines = text.split("\n")
    brand_lower = brand.lower()
    brand_stripped = re.sub(r"['\-\s]", "", brand_lower)
    first_word = brand_lower.split()[0] if " " in brand_lower else None

    for line in lines:
        line_lower = line.lower()
        line_stripped = re.sub(r"['\-\s]", "", line_lower)
        found = (brand_lower in line_lower or
                 brand_stripped in line_stripped or
                 (first_word and len(first_word) >= 3 and first_word in line_lower))
        if found:
            match = re.match(r'^\s*(\d+)', line)
            if match:
                return int(match.group(1))
    return None


def brand_appears(brands_mentioned, target_brand):
    """Check if target brand appears in the brands_mentioned list."""
    target_lower = target_brand.lower()
    target_stripped = re.sub(r"['\-\s]", "", target_lower)
    first_word = target_lower.split()[0] if " " in target_lower else None

    for b in brands_mentioned:
        b_lower = b.lower()
        b_stripped = re.sub(r"['\-\s]", "", b_lower)
        if b_lower == target_lower or b_stripped == target_stripped:
            return True
        if first_word and len(first_word) >= 3 and first_word in b_lower:
            return True
    # Also check raw text match wasn't caught by known_brands
    return False


def run_query_n_times(query_text, brand, n=RUNS_PER_QUERY):
    """Run a single query n times with suffixes. Returns list of response dicts."""
    responses = []
    for i in range(n):
        suffix = RUN_SUFFIXES[i]
        prompt = f"{query_text} {suffix}"
        print(f"      Run {i + 1}/{n} suffix={suffix}")
        text = query_gemini(prompt)
        brands_mentioned = extract_brands_mentioned(text, brand)
        specs_found = extract_specs_found(text)
        sources_cited = extract_sources_cited(text)
        brand_rank = extract_brand_rank(text, brand)
        responses.append({
            "run": i + 1,
            "suffix": suffix,
            "text": text,
            "brands_mentioned": brands_mentioned,
            "specs_found": specs_found,
            "sources_cited": sources_cited,
            "brand_rank": brand_rank,
        })
        if i < n - 1:
            time.sleep(CALL_DELAY)
    return responses


def compute_aggregated(brand, raw_responses):
    """Compute aggregated metrics from raw responses."""
    # EN runs
    en_runs = raw_responses.get("en", [])
    # FR runs = fr_1 + fr_2 + fr_3
    fr_runs = []
    for key in ["fr_1", "fr_2", "fr_3"]:
        fr_runs.extend(raw_responses.get(key, []))

    def appearance_rate(runs, target_brand):
        if not runs:
            return 0.0
        count = 0
        for r in runs:
            if brand_appears(r.get("brands_mentioned", []), target_brand):
                count += 1
            else:
                # Fallback: check raw text
                text = r.get("text", "")
                if text and "[ERROR]" not in text:
                    tl = target_brand.lower()
                    ts = re.sub(r"['\-\s]", "", tl)
                    txt_lower = text.lower()
                    txt_stripped = re.sub(r"['\-\s]", "", txt_lower)
                    if tl in txt_lower or ts in txt_stripped:
                        count += 1
        return round(count / len(runs), 2)

    def avg_specs(runs):
        if not runs:
            return 0.0
        total = sum(len(r.get("specs_found", [])) for r in runs)
        return round(total / len(runs), 1)

    def spec_counts(runs):
        return [len(r.get("specs_found", [])) for r in runs]

    def competitor_frequency(runs, target_brand):
        if not runs:
            return {}
        target_lower = target_brand.lower()
        target_first = target_lower.split()[0] if " " in target_lower else target_lower
        comp_counts = {}
        for r in runs:
            for b in r.get("brands_mentioned", []):
                b_lower = b.lower()
                b_first = b_lower.split()[0] if " " in b_lower else b_lower
                if b_lower == target_lower or b_first == target_first:
                    continue
                comp_counts[b] = comp_counts.get(b, 0) + 1
        return {k: round(v / len(runs), 2) for k, v in sorted(comp_counts.items(), key=lambda x: -x[1])}

    en_specs = spec_counts(en_runs)
    fr_specs = spec_counts(fr_runs)

    avg_en = avg_specs(en_runs)
    avg_fr = avg_specs(fr_runs)
    spec_preservation = round(avg_fr / avg_en, 2) if avg_en > 0 else 0.0

    aggregated = {
        "brand_appearance_rate_en": appearance_rate(en_runs, brand),
        "brand_appearance_rate_fr": appearance_rate(fr_runs, brand),
        "avg_specs_en": avg_en,
        "avg_specs_fr": avg_fr,
        "spec_preservation": spec_preservation,
        "confidence_range": {
            "en": {"min": min(en_specs) if en_specs else 0, "max": max(en_specs) if en_specs else 0},
            "fr": {"min": min(fr_specs) if fr_specs else 0, "max": max(fr_specs) if fr_specs else 0},
        },
        "competitor_frequency_en": competitor_frequency(en_runs, brand),
        "competitor_frequency_fr": competitor_frequency(fr_runs, brand),
    }
    return aggregated


def run_brand(row):
    """Run all queries x5 for a single brand."""
    brand = row["brand"]
    product_category = row["product_category"]
    top_competitor = row["top_competitor"]

    queries = {
        "en": row.get("generic_query_en", ""),
        "fr_1": row.get("generic_query_fr", ""),
        "fr_2": row.get("generic_query_fr_2", ""),
        "fr_3": row.get("generic_query_fr_3", ""),
    }

    safe_name = re.sub(r'[^\w\-]', '_', brand.lower())
    out_path = REPORTS_DIR / f"{safe_name}_gemini_probes.json"
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  Brand: {brand}")
    print(f"  Category: {product_category}")
    print(f"  Queries: 4 x {RUNS_PER_QUERY} runs = {4 * RUNS_PER_QUERY} API calls")
    print(f"{'='*60}")

    raw_responses = {}
    for query_key, query_text in queries.items():
        if not query_text:
            print(f"    [SKIP] {query_key} -- no query defined")
            raw_responses[query_key] = []
            continue
        print(f"    Query [{query_key}]: {query_text[:80]}...")
        raw_responses[query_key] = run_query_n_times(query_text, brand)
        # Delay between query groups
        time.sleep(CALL_DELAY)

    aggregated = compute_aggregated(brand, raw_responses)

    output = {
        "brand": brand,
        "product_category": product_category,
        "top_competitor": top_competitor,
        "model": "gemini-2.5-flash",
        "runs_per_query": RUNS_PER_QUERY,
        "queries": queries,
        "raw_responses": raw_responses,
        "aggregated": aggregated,
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n  Saved: {out_path}")
    print(f"  EN appearance: {aggregated['brand_appearance_rate_en']}")
    print(f"  FR appearance: {aggregated['brand_appearance_rate_fr']}")
    print(f"  Spec preservation: {aggregated['spec_preservation']}")
    return output


def load_targets(brand_filter=None, priority_only=False):
    """Load brands from targets.csv, optionally filtering."""
    with open(TARGETS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if priority_only:
        priority_lower = [b.lower() for b in PRIORITY_BRANDS]
        rows = [r for r in rows if r["brand"].lower() in priority_lower]
    elif brand_filter:
        filter_lower = [b.lower() for b in brand_filter]
        rows = [r for r in rows if r["brand"].lower() in filter_lower]

    return rows


def main():
    # Parse CLI args
    args = sys.argv[1:]
    priority_only = False
    brand_filter = []

    if "--priority" in args:
        priority_only = True
        args = [a for a in args if a != "--priority"]

    if args:
        brand_filter = args

    # Check API key
    if not os.environ.get("GEMINI_API_KEY"):
        print("ERROR: GEMINI_API_KEY environment variable not set.")
        sys.exit(1)

    rows = load_targets(brand_filter=brand_filter, priority_only=priority_only)

    if not rows:
        print("No brands matched the filter.")
        sys.exit(1)

    print(f"Gemini 2.5 Flash n=5 Probe Engine")
    print(f"Brands to process: {len(rows)}")
    print(f"Total API calls: ~{len(rows) * 4 * RUNS_PER_QUERY}")
    print(f"Estimated time: ~{len(rows) * 4 * RUNS_PER_QUERY * (CALL_DELAY + 3) // 60} minutes")
    print(f"Brands: {', '.join(r['brand'] for r in rows)}")

    for row in rows:
        run_brand(row)

    print(f"\nAll probes complete. Results in {REPORTS_DIR}/")


if __name__ == "__main__":
    main()
