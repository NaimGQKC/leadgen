#!/usr/bin/env python3
"""
TXT Probe Importer -- reads .txt probe files from probes_txt/<brand>/ folders,
parses them, scores them, and generates scary reports.

Usage:
    python scripts/txt_importer.py                  # process all brands in probes_txt/
    python scripts/txt_importer.py ssense mackage   # process specific brands

Folder structure expected:
    probes_txt/
        ssense/
            probe1.txt
            probe2.txt
            ...
        cirque_du_soleil/
            probe1.txt
            ...

Each .txt file = one probe response. Format:
    Query: <the query that was asked>

    <response body>

    --- SOURCE LINKS ---
    Source Title 1 - URL
    Source Title 2 - URL
    ...

The "--- SOURCE LINKS ---" section is optional.
The "Query: ..." line is optional (filename used as fallback label).
"""

import json
import re
import sys
from datetime import date
from pathlib import Path

# Reuse scoring and reporting from existing pipeline
sys.path.insert(0, str(Path(__file__).resolve().parent))
from scorer import (
    brand_in_text, find_brand_rank, count_specs_in_text, extract_competitors,
    safe_name, score_brand_gemini, score_brand_fallback, REPORTS_DIR
)
from report_generator import generate_scary_report

PROBES_TXT_DIR = Path(__file__).resolve().parent.parent / "probes_txt"
LEADS_DIR = Path(__file__).resolve().parent.parent / "leads"
TARGETS_CSV = LEADS_DIR / "targets.csv"


# ---------------------------------------------------------------------------
# TXT file parser
# ---------------------------------------------------------------------------

def parse_txt_probe(filepath):
    """Parse a single .txt probe file into structured data."""
    text = filepath.read_text(encoding="utf-8", errors="replace").strip()
    if not text:
        return None

    query = None
    sources = []
    body = text

    # Extract query line if present
    m = re.match(r'^Query:\s*(.+)', text, re.IGNORECASE)
    if m:
        query = m.group(1).strip()
        body = text[m.end():].strip()

    # Split off source links section
    source_markers = ["--- SOURCE LINKS ---", "---SOURCE LINKS---", "--- SOURCES ---",
                      "--- Sources ---", "Sources:"]
    for marker in source_markers:
        idx = body.rfind(marker)
        if idx != -1:
            source_block = body[idx + len(marker):].strip()
            body = body[:idx].strip()
            # Each non-empty line is a source
            for line in source_block.splitlines():
                line = line.strip()
                if line and line != "---":
                    sources.append(line)
            break

    return {
        "query": query,
        "text": body,
        "sources": sources,
        "filename": filepath.name,
    }


def detect_language(text, query=None):
    """Heuristic: detect if probe text is French or English."""
    check = (query or "") + " " + text[:500]
    check_lower = check.lower()
    fr_signals = [
        "montréal", "québec", "meilleur", "pour", "avec", "dans", "les",
        "des", "une", "est", "cette", "quel", "où", "acheter",
        "manteau", "hiver", "prix", "résultats", "recherche",
        "spécification", "technique", "comparaison",
    ]
    en_signals = [
        "best", "the", "with", "for", "this", "compare", "what",
        "how", "winter", "coat", "technical", "specs", "pricing",
        "search results", "comparison",
    ]
    fr_count = sum(1 for w in fr_signals if w in check_lower)
    en_count = sum(1 for w in en_signals if w in check_lower)
    return "fr" if fr_count > en_count else "en"


# ---------------------------------------------------------------------------
# Aggregation -- turn parsed probes into the format scorer/reporter expects
# ---------------------------------------------------------------------------

def aggregate_probes(brand, probes):
    """
    Take a list of parsed probe dicts and produce the aggregated data structure
    that matches _gemini_probes.json format (used by scorer.py and report_generator.py).
    """
    en_probes = [p for p in probes if p.get("lang") == "en"]
    fr_probes = [p for p in probes if p.get("lang") == "fr"]

    total_en = len(en_probes) or 1
    total_fr = len(fr_probes) or 1

    # Brand appearance
    en_appearances = sum(1 for p in en_probes if brand_in_text(brand, p["text"]))
    fr_appearances = sum(1 for p in fr_probes if brand_in_text(brand, p["text"]))

    # Specs
    en_specs = [count_specs_in_text(p["text"]) for p in en_probes]
    fr_specs = [count_specs_in_text(p["text"]) for p in fr_probes]
    avg_en = sum(en_specs) / len(en_specs) if en_specs else 0
    avg_fr = sum(fr_specs) / len(fr_specs) if fr_specs else 0
    spec_preservation = avg_fr / avg_en if avg_en > 0 else (1.0 if avg_fr > 0 else 0)

    # Competitors
    comp_freq_en = {}
    comp_freq_fr = {}
    for p in en_probes:
        for c in extract_competitors(p["text"], brand):
            comp_freq_en[c] = comp_freq_en.get(c, 0) + 1
    for p in fr_probes:
        for c in extract_competitors(p["text"], brand):
            comp_freq_fr[c] = comp_freq_fr.get(c, 0) + 1
    # Normalize to rates
    for c in comp_freq_en:
        comp_freq_en[c] = round(comp_freq_en[c] / total_en, 2)
    for c in comp_freq_fr:
        comp_freq_fr[c] = round(comp_freq_fr[c] / total_fr, 2)

    # Confidence range (min/max specs)
    aggregated = {
        "brand_appearance_rate_en": round(en_appearances / total_en, 2),
        "brand_appearance_rate_fr": round(fr_appearances / total_fr, 2),
        "avg_specs_en": round(avg_en, 1),
        "avg_specs_fr": round(avg_fr, 1),
        "spec_preservation": round(spec_preservation, 2),
        "confidence_range": {
            "en": {"min": min(en_specs) if en_specs else 0, "max": max(en_specs) if en_specs else 0},
            "fr": {"min": min(fr_specs) if fr_specs else 0, "max": max(fr_specs) if fr_specs else 0},
        },
        "competitor_frequency_en": comp_freq_en,
        "competitor_frequency_fr": comp_freq_fr,
    }

    # Collect queries used
    queries = {}
    fr_idx = 1
    for p in fr_probes:
        if p.get("query"):
            queries[f"fr_{fr_idx}"] = p["query"]
            fr_idx += 1
    for p in en_probes:
        if p.get("query"):
            queries["en"] = p["query"]
            break

    # Raw responses for reference
    raw_en = []
    for i, p in enumerate(en_probes, 1):
        raw_en.append({
            "run": i,
            "suffix": f"(from {p['filename']})",
            "text": p["text"],
            "brands_mentioned": extract_competitors(p["text"], brand),
            "specs_found": [],  # populated by count but not itemized here
            "sources_cited": p.get("sources", []),
            "brand_rank": find_brand_rank(brand, p["text"]),
        })
    raw_fr = []
    for i, p in enumerate(fr_probes, 1):
        raw_fr.append({
            "run": i,
            "suffix": f"(from {p['filename']})",
            "text": p["text"],
            "brands_mentioned": extract_competitors(p["text"], brand),
            "specs_found": [],
            "sources_cited": p.get("sources", []),
            "brand_rank": find_brand_rank(brand, p["text"]),
        })

    return {
        "brand": brand,
        "product_category": "",  # filled in later from targets.csv if available
        "top_competitor": "",
        "model": "manual-txt-import",
        "runs_per_query": len(probes),
        "queries": queries,
        "aggregated": aggregated,
        "raw_responses": {
            "en": raw_en,
            "fr": raw_fr,
        },
    }


# ---------------------------------------------------------------------------
# Brand folder processing
# ---------------------------------------------------------------------------

def load_targets_map():
    """Load targets.csv into a dict keyed by safe_name."""
    import csv
    result = {}
    if TARGETS_CSV.exists():
        with open(TARGETS_CSV, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                key = safe_name(row["brand"])
                result[key] = row
    return result


def match_target(folder_name, targets_map):
    """Match a folder name to a targets.csv entry. Tries exact, lowercase, and partial."""
    key = safe_name(folder_name)
    # Exact match
    if key in targets_map:
        return targets_map[key]
    # Partial: folder name is a prefix of a target key (e.g. "aldo" matches "aldo_group")
    for tkey, row in targets_map.items():
        if tkey.startswith(key) or key.startswith(tkey):
            return row
    # Partial: folder name appears in brand name
    folder_lower = folder_name.lower().replace("_", " ")
    for tkey, row in targets_map.items():
        if folder_lower in row.get("brand", "").lower():
            return row
    return {}


def process_brand_folder(brand_dir, targets_map):
    """Process all .txt files in a brand folder."""
    brand_key = safe_name(brand_dir.name)  # normalize folder name
    txt_files = sorted(brand_dir.glob("*.txt"))
    if not txt_files:
        print(f"  [SKIP] {brand_key} -- no .txt files found")
        return

    print(f"\n  Processing {brand_key} ({len(txt_files)} txt files)...")

    # Try to find the real brand name from targets.csv (with fuzzy matching)
    row = match_target(brand_dir.name, targets_map)
    brand_display = row.get("brand", brand_dir.name)

    # Parse all probes
    probes = []
    for f in txt_files:
        parsed = parse_txt_probe(f)
        if parsed:
            lang = detect_language(parsed["text"], parsed.get("query"))
            parsed["lang"] = lang
            probes.append(parsed)
            print(f"    {f.name}: {lang} | query={'yes' if parsed['query'] else 'no'} | "
                  f"{len(parsed['sources'])} sources | {len(parsed['text'])} chars")

    if not probes:
        print(f"  [SKIP] {brand_key} -- no valid probes parsed")
        return

    # Aggregate
    gemini_data = aggregate_probes(brand_display, probes)
    gemini_data["product_category"] = row.get("product_category", "")
    gemini_data["top_competitor"] = row.get("top_competitor", "")

    # Save aggregated probes JSON (same format as _gemini_probes.json)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    probes_path = REPORTS_DIR / f"{brand_key}_txt_probes.json"
    with open(probes_path, "w", encoding="utf-8") as f:
        json.dump(gemini_data, f, indent=2, ensure_ascii=False)
    print(f"    Saved: {probes_path.name}")

    # Score using the gemini scorer (same logic, different source data)
    score_result = score_brand_gemini(brand_display, gemini_data, None, None)
    score_result["methodology"] = f"manual-txt-import, {len(probes)} probes ({len([p for p in probes if p['lang']=='en'])} EN, {len([p for p in probes if p['lang']=='fr'])} FR)"

    score_path = REPORTS_DIR / f"{brand_key}_txt_score.json"
    with open(score_path, "w", encoding="utf-8") as f:
        json.dump(score_result, f, indent=2, ensure_ascii=False)
    print(f"    Score: IAS {score_result['ias']}/100 [{score_result['severity']}]")

    # Generate scary report
    report_row = {
        "brand": brand_display,
        "product_category": row.get("product_category", ""),
        "top_competitor": row.get("top_competitor", ""),
        "generic_query_fr": row.get("generic_query_fr", ""),
        "generic_query_fr_2": row.get("generic_query_fr_2", ""),
        "generic_query_fr_3": row.get("generic_query_fr_3", ""),
    }
    report = generate_scary_report(
        brand_display,
        report_row,
        gemini_probes=gemini_data,
        score_data=score_result,
        source_scores=None,
        google_probes=None,
        old_probes=None,
    )

    # Override methodology line to reflect txt import
    report = report.replace(
        "Gemini 2.5 Flash, 5 runs per query, 3 FR variants (n=15 FR, n=5 EN)",
        f"Manual probe import, {len(probes)} probes ({len([p for p in probes if p['lang']=='en'])} EN, {len([p for p in probes if p['lang']=='fr'])} FR)"
    )

    report_path = REPORTS_DIR / f"{brand_key}_txt_scary_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"    Report: {report_path.name}")


def main():
    targets_map = load_targets_map()

    # Build map of lowercase folder name -> actual folder path
    all_folders = {d.name.lower(): d for d in sorted(PROBES_TXT_DIR.iterdir()) if d.is_dir()}

    # Determine which brands to process
    if len(sys.argv) > 1:
        requested = [safe_name(b) for b in sys.argv[1:]]
        brand_dirs = []
        for req in requested:
            # Try exact match, then prefix match
            if req in all_folders:
                brand_dirs.append(all_folders[req])
            else:
                matched = [d for k, d in all_folders.items() if k.startswith(req) or req.startswith(k)]
                if matched:
                    brand_dirs.extend(matched)
                else:
                    print(f"  [SKIP] {req} -- no matching folder in {PROBES_TXT_DIR}")
    else:
        brand_dirs = list(all_folders.values())

    if not brand_dirs:
        print(f"No brand folders found in {PROBES_TXT_DIR}")
        print(f"\nCreate folders like:")
        print(f"  probes_txt/ssense/")
        print(f"  probes_txt/cirque_du_soleil/")
        print(f"  probes_txt/mackage/")
        print(f"\nThen drop .txt probe files into each folder.")
        return

    print(f"TXT Probe Importer -- processing {len(brand_dirs)} brand(s)")
    print(f"Source: {PROBES_TXT_DIR}")
    print(f"Output: {REPORTS_DIR}")

    for brand_dir in brand_dirs:
        process_brand_folder(brand_dir, targets_map)

    print(f"\nDone. Reports saved to {REPORTS_DIR}/")


if __name__ == "__main__":
    main()
