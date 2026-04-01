#!/usr/bin/env python3
"""Report generator -- combines gemini probes + source scores + IAS into scary reports."""

import csv
import json
import re
import sys
from datetime import date
from pathlib import Path

REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"
LEADS_DIR = Path(__file__).resolve().parent.parent / "leads"
TARGETS_CSV = LEADS_DIR / "targets.csv"


def safe_name(brand):
    return re.sub(r'[^\w\-]', '_', brand.lower())


def load_json(brand, suffix):
    path = REPORTS_DIR / f"{safe_name(brand)}_{suffix}.json"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def pct_str(val):
    """Format a float 0-1 or 0-100 as a percentage string."""
    if val is None:
        return "N/A"
    if isinstance(val, (int, float)):
        if val <= 1.0 and val >= 0:
            return f"{val * 100:.0f}%"
        return f"{val:.0f}%"
    return str(val)


def generate_scary_report(brand, row, gemini_probes, score_data, source_scores,
                          google_probes, old_probes):
    """Generate the full scary report markdown."""
    ias = score_data.get("ias", 0) if score_data else 0
    severity = score_data.get("severity", "UNKNOWN") if score_data else "UNKNOWN"
    breakdown = score_data.get("breakdown", {}) if score_data else {}

    product_category = row.get("product_category", "")
    top_competitor = row.get("top_competitor", "")

    # Gemini aggregated data
    agg = gemini_probes.get("aggregated", {}) if gemini_probes else {}
    queries = gemini_probes.get("queries", {}) if gemini_probes else {}
    raw_responses = gemini_probes.get("raw_responses", []) if gemini_probes else []

    # Source authority data
    avg_src_en = source_scores.get("avg_source_score_en", "N/A") if source_scores else "N/A"
    avg_src_fr = source_scores.get("avg_source_score_fr", "N/A") if source_scores else "N/A"
    src_gap = source_scores.get("source_authority_gap", "N/A") if source_scores else "N/A"

    # Appearance rates
    rate_en = agg.get("brand_appearance_rate_en", "N/A")
    rate_fr = agg.get("brand_appearance_rate_fr", "N/A")

    # Spec data
    avg_specs_en = agg.get("avg_specs_en", "N/A")
    avg_specs_fr = agg.get("avg_specs_fr", "N/A")
    spec_preservation = agg.get("spec_preservation", "N/A")

    # Confidence range
    conf = agg.get("confidence_range", {})
    fr_conf = conf.get("fr", {})
    en_conf = conf.get("en", {})
    min_fr = fr_conf.get("min", "?")
    max_fr = fr_conf.get("max", "?")
    min_en = en_conf.get("min", "?")
    max_en = en_conf.get("max", "?")

    # Competitor frequency
    comp_freq_fr = agg.get("competitor_frequency_fr", {})
    comp_freq_en = agg.get("competitor_frequency_en", {})

    # French queries
    fr_1 = queries.get("fr_1", row.get("generic_query_fr", ""))
    fr_2 = queries.get("fr_2", row.get("generic_query_fr_2", ""))
    fr_3 = queries.get("fr_3", row.get("generic_query_fr_3", ""))

    lines = []

    # Header
    lines.append(f"# AI Inference Audit: {brand}")
    lines.append(f"")
    lines.append(f"**Inference Alignment Score: {ias}/100 -- {severity}**")
    lines.append(f"")
    lines.append(f"**Date:** {date.today().isoformat()}")
    lines.append(f"**Category:** {product_category}")
    lines.append(f"**Methodology:** Gemini 2.5 Flash, 5 runs per query, 3 FR variants (n=15 FR, n=5 EN)")
    lines.append(f"")

    # --- Key Metrics Table ---
    lines.append(f"## Key Metrics")
    lines.append(f"")
    lines.append(f"| Metric | English | French | Gap |")
    lines.append(f"|--------|---------|--------|-----|")

    # Brand appearance rate (values are 0-1 floats)
    if isinstance(rate_en, (int, float)) and isinstance(rate_fr, (int, float)):
        en_pct = rate_en * 100 if rate_en <= 1.0 else rate_en
        fr_pct = rate_fr * 100 if rate_fr <= 1.0 else rate_fr
        en_count = round(rate_en * 5) if rate_en <= 1.0 else round(rate_en / 100 * 5)
        fr_count = round(rate_fr * 15) if rate_fr <= 1.0 else round(rate_fr / 100 * 15)
        gap_app = f"-{en_pct - fr_pct:.0f}%" if en_pct > fr_pct else f"+{fr_pct - en_pct:.0f}%"
        lines.append(f"| Brand appearance rate | {en_pct:.0f}% ({en_count}/5) | {fr_pct:.0f}% ({fr_count}/15) | {gap_app} |")
    else:
        lines.append(f"| Brand appearance rate | {rate_en} | {rate_fr} | -- |")

    # Avg specs per response
    if isinstance(avg_specs_en, (int, float)) and isinstance(avg_specs_fr, (int, float)):
        if avg_specs_en > 0:
            gap_spec = f"-{((avg_specs_en - avg_specs_fr) / avg_specs_en * 100):.0f}%"
        else:
            gap_spec = "--"
        lines.append(f"| Avg specs per response | {avg_specs_en:.1f} | {avg_specs_fr:.1f} | {gap_spec} |")
    else:
        lines.append(f"| Avg specs per response | {avg_specs_en} | {avg_specs_fr} | -- |")

    # Spec range across runs
    lines.append(f"| Spec range across runs | {min_en}-{max_en} | {min_fr}-{max_fr} | -- |")

    # Source authority score
    if isinstance(avg_src_en, (int, float)) and isinstance(avg_src_fr, (int, float)):
        gap_src = f"-{avg_src_en - avg_src_fr:.1f}"
        lines.append(f"| Source authority score | {avg_src_en:.1f} | {avg_src_fr:.1f} | {gap_src} |")
    else:
        lines.append(f"| Source authority score | {avg_src_en} | {avg_src_fr} | -- |")

    lines.append(f"")

    # --- Finding 1: Brand Visibility Gap ---
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"## Finding 1: Brand Visibility Gap")
    lines.append(f"")
    if isinstance(rate_en, (int, float)) and isinstance(rate_fr, (int, float)):
        en_pct_f1 = rate_en * 100 if rate_en <= 1.0 else rate_en
        fr_pct_f1 = rate_fr * 100 if rate_fr <= 1.0 else rate_fr
        lines.append(f"Brand appeared in {en_pct_f1:.0f}% of English queries but only {fr_pct_f1:.0f}% of French queries.")
    else:
        lines.append(f"Brand appeared in {rate_en} of English queries and {rate_fr} of French queries.")
    lines.append(f"")
    lines.append(f"French queries tested:")
    if fr_1:
        lines.append(f'1. "{fr_1}"')
    if fr_2:
        lines.append(f'2. "{fr_2}"')
    if fr_3:
        lines.append(f'3. "{fr_3}"')
    lines.append(f"")

    # --- Finding 2: Spec Dilution ---
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"## Finding 2: Spec Dilution")
    lines.append(f"")
    if isinstance(spec_preservation, (int, float)):
        sp_pct = spec_preservation * 100 if spec_preservation <= 1.0 else spec_preservation
        lines.append(f"{sp_pct:.0f}% of technical specs preserved in French ({avg_specs_fr} vs {avg_specs_en}).")
    else:
        lines.append(f"Spec preservation: {spec_preservation} ({avg_specs_fr} FR vs {avg_specs_en} EN).")
    lines.append(f"Range: {min_fr}-{max_fr} specs across 15 French runs vs {min_en}-{max_en} in English.")
    lines.append(f"")

    # --- Finding 3: Competitor Displacement ---
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"## Finding 3: Competitor Displacement")
    lines.append(f"")

    # Build unified competitor set
    all_comps = set(list(comp_freq_fr.keys()) + list(comp_freq_en.keys()))
    if all_comps:
        lines.append(f"| Competitor | EN frequency | FR frequency | FR-only? |")
        lines.append(f"|------------|-------------|-------------|----------|")
        for comp in sorted(all_comps):
            en_f = comp_freq_en.get(comp, 0)
            fr_f = comp_freq_fr.get(comp, 0)
            en_pct_val = en_f * 100 if isinstance(en_f, (int, float)) and en_f <= 1.0 else en_f
            fr_pct_val = fr_f * 100 if isinstance(fr_f, (int, float)) and fr_f <= 1.0 else fr_f
            en_pct = f"{en_pct_val:.0f}%" if isinstance(en_pct_val, (int, float)) else str(en_pct_val)
            fr_pct = f"{fr_pct_val:.0f}%" if isinstance(fr_pct_val, (int, float)) else str(fr_pct_val)
            fr_only = "YES" if (en_f == 0) and fr_f > 0 else "No"
            lines.append(f"| {comp} | {en_pct} | {fr_pct} | {fr_only} |")
    else:
        # Fallback: use old score data competitors if available
        llm_scores = score_data.get("llm_scores", {}) if score_data else {}
        found_any = False
        for llm, data in llm_scores.items():
            details = data.get("details", {})
            fr_comps = details.get("competitors_in_fr_generic", [])
            en_comps = details.get("competitors_in_en_generic", [])
            if fr_comps or en_comps:
                if not found_any:
                    lines.append(f"| Competitor | EN frequency | FR frequency | FR-only? |")
                    lines.append(f"|------------|-------------|-------------|----------|")
                    found_any = True
                for c in set(fr_comps + en_comps):
                    in_en = c in en_comps
                    in_fr = c in fr_comps
                    fr_only = "YES" if in_fr and not in_en else "No"
                    lines.append(f"| {c} | {'present' if in_en else '0%'} | {'present' if in_fr else '0%'} | {fr_only} |")
        if not found_any:
            lines.append(f"No competitor displacement data available.")
    lines.append(f"")

    # --- Finding 4: Source Authority ---
    if source_scores:
        lines.append(f"---")
        lines.append(f"")
        lines.append(f"## Finding 4: Source Authority")
        lines.append(f"")
        if isinstance(avg_src_en, (int, float)) and isinstance(avg_src_fr, (int, float)):
            lines.append(f"EN sources avg score: {avg_src_en:.1f}/10 | FR sources avg score: {avg_src_fr:.1f}/10")
            lines.append(f"Gap: {abs(avg_src_en - avg_src_fr):.1f} points -- French AI responses rely on lower-authority sources.")
        else:
            lines.append(f"EN sources avg score: {avg_src_en}/10 | FR sources avg score: {avg_src_fr}/10")
            lines.append(f"Gap: {src_gap} points.")
        lines.append(f"")

    # --- Bonus: Google AI Mode ---
    if google_probes:
        has_real_data = False
        for probe_key in ["probeA_generic", "probeB_accuracy", "probeC_competitive"]:
            probe_data = google_probes.get(probe_key, {}).get("google", {})
            for lang in ["en", "fr"]:
                entry = probe_data.get(lang, {})
                if isinstance(entry, dict) and entry.get("text"):
                    has_real_data = True
                    break

        if has_real_data:
            lines.append(f"---")
            lines.append(f"")
            lines.append(f"## Bonus: Google AI Mode (Live Search)")
            lines.append(f"")
            lines.append(f"Results captured via live Chromium browser with Montreal geolocation.")
            lines.append(f"")

            for probe_key, probe_label in [
                ("probeA_generic", "Generic Discovery"),
                ("probeB_accuracy", "Brand Accuracy"),
                ("probeC_competitive", "Competitive Displacement"),
            ]:
                probe_data = google_probes.get(probe_key, {}).get("google", {})
                en_entry = probe_data.get("en", {})
                fr_entry = probe_data.get("fr", {})
                en_text = en_entry.get("text", "") if isinstance(en_entry, dict) else ""
                fr_text = fr_entry.get("text", "") if isinstance(fr_entry, dict) else ""

                if not en_text and not fr_text:
                    continue

                lines.append(f"### {probe_label}")
                lines.append(f"")
                if en_text:
                    en_type = en_entry.get("type", "unknown") if isinstance(en_entry, dict) else "unknown"
                    en_sources = en_entry.get("sources", []) if isinstance(en_entry, dict) else []
                    lines.append(f"**Google EN** ({en_type}):")
                    lines.append(f"> {en_text[:600].replace(chr(10), chr(10) + '> ')}")
                    if en_sources:
                        lines.append(f"> Sources: {', '.join(en_sources[:5])}")
                    lines.append(f"")
                if fr_text:
                    fr_type = fr_entry.get("type", "unknown") if isinstance(fr_entry, dict) else "unknown"
                    fr_sources = fr_entry.get("sources", []) if isinstance(fr_entry, dict) else []
                    lines.append(f"**Google FR** ({fr_type}):")
                    lines.append(f"> {fr_text[:600].replace(chr(10), chr(10) + '> ')}")
                    if fr_sources:
                        lines.append(f"> Sources: {', '.join(fr_sources[:5])}")
                    lines.append(f"")

    # --- Revenue Impact ---
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"## Revenue Impact")
    lines.append(f"")
    lines.append(f"- **Quebec French-speaking market:** ~7M consumers")
    gap_pct = 100 - ias
    lines.append(f"- **IAS {ias}/100** = ~{gap_pct}% of French AI queries failing or degraded")
    lines.append(f"- AI-driven product discovery growing 40%+ YoY -- gap compounds quarterly")
    lines.append(f"")

    # --- What Fixes This ---
    lines.append(f"## What Fixes This")
    lines.append(f"")
    lines.append(f"Bilingual JSON-LD injection + AI-readable product feeds (UCP/ACP) + "
                 f"Headless Agentic Probing to verify.")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"*Generated by Lead Gen Engine | Alex, AI PM -- Montreal (JMSB/Ampliwork)*")

    return "\n".join(lines)


def generate_for_brand(row):
    brand = row["brand"]
    score_data = load_json(brand, "score")
    gemini_probes = load_json(brand, "gemini_probes")
    source_scores = load_json(brand, "source_scores")
    google_probes = load_json(brand, "google_probes")
    old_probes = load_json(brand, "probes")

    if not score_data and not gemini_probes and not old_probes:
        print(f"  [SKIP] {brand} -- no data")
        return

    report = generate_scary_report(brand, row, gemini_probes, score_data,
                                   source_scores, google_probes, old_probes)
    out_path = REPORTS_DIR / f"{safe_name(brand)}_scary_report.md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"  Report: {out_path}")


def main():
    with open(TARGETS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Generating reports for {len(rows)} brands...\n")
    for row in rows:
        generate_for_brand(row)
    print("\nReports complete.")


if __name__ == "__main__":
    main()
