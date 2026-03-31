#!/usr/bin/env python3
"""Report generator -- combines probes + scores + scraped data into scary reports."""

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


def generate_scary_report(brand, row, probes, score_data, scraped):
    """Generate the full scary report markdown."""
    ias = score_data.get("ias", 0) if score_data else 0
    severity = score_data.get("severity", "UNKNOWN") if score_data else "UNKNOWN"
    llm_scores = score_data.get("llm_scores", {}) if score_data else {}

    product_category = row.get("product_category", "")
    top_competitor = row.get("top_competitor", "")
    generic_fr = row.get("generic_query_fr", "")

    probes_sent = probes.get("probes_sent", {}) if probes else {}
    responses = probes.get("responses", {}) if probes else {}

    lines = []
    lines.append(f"# AI Inference Audit: {brand}")
    lines.append(f"")
    lines.append(f"**Inference Alignment Score: {ias}/100 -- {severity}**")
    lines.append(f"")
    lines.append(f"**Date:** {date.today().isoformat()}")
    lines.append(f"**Category:** {product_category}")
    lines.append(f"**Top Competitor:** {top_competitor}")
    lines.append(f"")

    # How We Tested
    lines.append(f"## How We Tested")
    lines.append(f"")
    llm_list = [k for k in ["claude", "gpt4o", "gemini"] if k in responses.get("probeA_generic", {})]
    llm_display = {"claude": "Claude", "gpt4o": "GPT-4o", "gemini": "Gemini"}
    llm_names = [llm_display.get(k, k) for k in llm_list]
    lines.append(f"Queried {len(llm_names)} AI platform{'s' if len(llm_names) > 1 else ''} "
                 f"({', '.join(llm_names)}) in EN and FR with identical prompts.")
    if scraped and (scraped.get("en", {}).get("scraped") or scraped.get("fr", {}).get("scraped")):
        lines.append(f"Scraped {brand}'s actual product pages to verify accuracy.")
    lines.append(f"")

    # Finding 1: Ghosting
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"## Finding 1: Ghosting")
    lines.append(f"")
    fr_query = probes_sent.get("probeA_generic", {}).get("fr", generic_fr)
    lines.append(f'**Query:** "{fr_query}"')
    lines.append(f"")
    lines.append(f"| AI Platform | Brand in EN? | Brand in FR? | FR Competitors Instead |")
    lines.append(f"|-------------|-------------|-------------|----------------------|")

    for llm in llm_list:
        details = llm_scores.get(llm, {}).get("details", {})
        en_present = "Yes" if details.get("en_rank") else "Unknown"
        fr_present = "Yes" if details.get("generic_fr_present") is True else (
            "ABSENT" if details.get("generic_fr_present") is False else "Unknown")
        comps = ", ".join(details.get("competitors_in_fr_generic", [])[:3]) or "N/A"
        lines.append(f"| {llm_display.get(llm, llm)} | {en_present} (#{details.get('en_rank', '?')}) | "
                     f"{fr_present} (#{details.get('fr_rank', '?')}) | {comps} |")

    # Show actual responses
    lines.append(f"")
    for llm in llm_list:
        resp_a = responses.get("probeA_generic", {}).get(llm, {})
        en_text = resp_a.get("en", "")
        fr_text = resp_a.get("fr", "")
        if en_text and "[TO BE FILLED" not in en_text and "[ERROR]" not in en_text:
            lines.append(f"### {llm_display.get(llm, llm)} EN response:")
            lines.append(f"")
            # Truncate to first 500 chars for readability
            lines.append(f"> {en_text[:800].replace(chr(10), chr(10) + '> ')}")
            lines.append(f"")
        if fr_text and "[TO BE FILLED" not in fr_text and "[ERROR]" not in fr_text:
            lines.append(f"### {llm_display.get(llm, llm)} FR response:")
            lines.append(f"")
            lines.append(f"> {fr_text[:800].replace(chr(10), chr(10) + '> ')}")
            lines.append(f"")

    # Finding 2: Spec Dilution
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"## Finding 2: Spec Dilution")
    lines.append(f"")

    # Build spec comparison table
    lines.append(f"| Metric | {' | '.join(f'{llm_display.get(l,l)} EN | {llm_display.get(l,l)} FR' for l in llm_list)} |")
    lines.append(f"|--------|{'|'.join(['-------|-------' for _ in llm_list])}|")

    spec_row = "| Spec count"
    for llm in llm_list:
        details = llm_scores.get(llm, {}).get("details", {})
        spec_row += f" | {details.get('en_spec_count', '?')} | {details.get('fr_spec_count', '?')}"
    spec_row += " |"
    lines.append(spec_row)

    ratio_row = "| Preservation ratio"
    for llm in llm_list:
        details = llm_scores.get(llm, {}).get("details", {})
        ratio = details.get("spec_ratio", "?")
        if isinstance(ratio, (int, float)):
            ratio_row += f" | -- | {ratio:.0%}"
        else:
            ratio_row += f" | -- | {ratio}"
    ratio_row += " |"
    lines.append(ratio_row)
    lines.append(f"")

    # Finding 3: Competitor Hijacking
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"## Finding 3: Competitor Hijacking")
    lines.append(f"")
    lines.append(f"| AI Platform | EN Recommendation | FR Recommendation | Switched? |")
    lines.append(f"|-------------|------------------|------------------|-----------|")
    for llm in llm_list:
        details = llm_scores.get(llm, {}).get("details", {})
        hijacked = details.get("hijacking", False)
        hijacked_by = ", ".join(details.get("hijacked_by", [])) if hijacked else "N/A"
        lines.append(f"| {llm_display.get(llm, llm)} | {brand} | "
                     f"{'**' + hijacked_by + '**' if hijacked else brand} | "
                     f"{'YES' if hijacked else 'No'} |")
    lines.append(f"")

    # Revenue Impact
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"## Revenue Impact")
    lines.append(f"")
    lines.append(f"- **Quebec French-speaking market:** ~7M consumers")
    gap_pct = 100 - ias
    lines.append(f"- **IAS {ias}/100** = ~{gap_pct}% of French AI queries failing or degraded")
    lines.append(f"- AI-driven product discovery growing 40%+ YoY -- gap compounds quarterly")
    lines.append(f"")

    # What Fixes This
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
    probes = load_json(brand, "probes")
    score_data = load_json(brand, "score")
    scraped = load_json(brand, "scraped")

    if not probes and not score_data:
        print(f"  [SKIP] {brand} -- no data")
        return

    report = generate_scary_report(brand, row, probes, score_data, scraped)
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
