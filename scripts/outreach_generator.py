#!/usr/bin/env python3
"""Outreach generator -- LinkedIn message + email per brand."""

import csv
import json
import re
import sys
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


def get_first_name(contact_name):
    if not contact_name:
        return "there"
    return contact_name.split()[0]


def get_appearance_stats(gemini_probes):
    """Extract brand appearance rates from gemini probes."""
    if not gemini_probes:
        return None, None
    agg = gemini_probes.get("aggregated", {})
    rate_en = agg.get("brand_appearance_rate_en")
    rate_fr = agg.get("brand_appearance_rate_fr")
    return rate_en, rate_fr


def get_source_authority_stats(source_scores):
    """Extract source authority gap from source scores."""
    if not source_scores:
        return None, None, None
    avg_en = source_scores.get("avg_source_score_en")
    avg_fr = source_scores.get("avg_source_score_fr")
    gap = source_scores.get("source_authority_gap")
    return avg_en, avg_fr, gap


def get_specific_finding(brand, score_data, gemini_probes, source_scores):
    """Extract the most compelling specific finding for outreach."""
    ias = score_data.get("ias", 0) if score_data else 0

    # Appearance rate gap is most compelling (rates are 0-1 floats)
    rate_en, rate_fr = get_appearance_stats(gemini_probes)
    if rate_en is not None and rate_fr is not None:
        if isinstance(rate_en, (int, float)) and isinstance(rate_fr, (int, float)):
            en_pct = rate_en * 100 if rate_en <= 1.0 else rate_en
            fr_pct = rate_fr * 100 if rate_fr <= 1.0 else rate_fr
            if en_pct - fr_pct >= 20:
                return (f"{brand} appeared in {en_pct:.0f}% of English AI queries "
                        f"but only {fr_pct:.0f}% of French ones")

    # Source authority gap
    src_en, src_fr, src_gap = get_source_authority_stats(source_scores)
    if src_en is not None and src_fr is not None:
        if isinstance(src_en, (int, float)) and isinstance(src_fr, (int, float)):
            if src_en - src_fr >= 3:
                return (f"French AI sources score {src_fr:.1f}/10 vs {src_en:.1f}/10 "
                        f"in English -- your FR responses rely on weaker sources")

    # Spec dilution from gemini (spec_preservation is 0-1 float)
    if gemini_probes:
        agg = gemini_probes.get("aggregated", {})
        spec_pres = agg.get("spec_preservation")
        if isinstance(spec_pres, (int, float)):
            sp_pct = spec_pres * 100 if spec_pres <= 1.0 else spec_pres
            if sp_pct < 70:
                return f"only {sp_pct:.0f}% of your technical specs survive when AI responds in French"

    # Fallback: ghosting / hijacking from score data
    if score_data:
        llm_scores = score_data.get("llm_scores", {})
        for llm, data in llm_scores.items():
            details = data.get("details", {})
            if details.get("ghosted"):
                return (f"French AI queries return zero mentions of {brand} "
                        f"while English surfaces you immediately")
            if details.get("hijacking"):
                comps = details.get("hijacked_by", [])
                if comps:
                    return (f"French AI queries for your category surface "
                            f"{comps[0]} instead of {brand}")

    # Generic fallback
    if rate_en is not None and rate_fr is not None:
        en_p = rate_en * 100 if isinstance(rate_en, float) and rate_en <= 1.0 else rate_en
        fr_p = rate_fr * 100 if isinstance(rate_fr, float) and rate_fr <= 1.0 else rate_fr
        return (f"{brand} appeared in {en_p:.0f}% of English AI queries "
                f"but only {fr_p:.0f}% of French ones")

    return f"your French AI discovery score is {ias}/100"


def generate_linkedin(brand, row, score_data, gemini_probes):
    """Generate LinkedIn message -- under 280 chars."""
    first_name = get_first_name(row.get("contact_name", ""))
    category = row.get("product_category", "")
    ias = score_data.get("ias", 0) if score_data else "?"

    rate_en, rate_fr = get_appearance_stats(gemini_probes)

    en_pct_li = rate_en * 100 if isinstance(rate_en, (int, float)) and rate_en <= 1.0 else rate_en
    fr_pct_li = rate_fr * 100 if isinstance(rate_fr, (int, float)) and rate_fr <= 1.0 else rate_fr
    if (isinstance(en_pct_li, (int, float)) and isinstance(fr_pct_li, (int, float))
            and en_pct_li - fr_pct_li >= 20):
        msg = (f"Hi {first_name}, ran an AI audit on {brand} in French vs English. "
               f"Brand appeared in {en_pct_li:.0f}% of EN queries but {fr_pct_li:.0f}% of FR. "
               f"Score: {ias}/100. Full report ready.")
    else:
        competitor = row.get("top_competitor", "")
        msg = (f"Hi {first_name}, ran an AI audit on {brand} -- French searches for "
               f"{category} surface {competitor} over you. "
               f"Score: {ias}/100. Full report ready.")

    # Trim if over 280
    if len(msg) > 280:
        msg = msg[:277] + "..."

    return msg


def generate_email(brand, row, score_data, gemini_probes, source_scores):
    """Generate 4-sentence outreach email."""
    first_name = get_first_name(row.get("contact_name", ""))
    generic_fr = row.get("generic_query_fr", "")
    ias = score_data.get("ias", 0) if score_data else "?"
    finding = get_specific_finding(brand, score_data, gemini_probes, source_scores)

    subject = f"{brand} scores {ias}/100 on French AI discovery"

    body = (
        f"{first_name}, I tested how Gemini handles {brand} in French vs English "
        f"across 15 independent runs per brand. "
        f'On "{generic_fr}", {finding}. '
        f"Your Inference Alignment Score is {ias}/100. "
        f"Full audit with the data ready -- 10 min to walk through?\n\n"
        f"Alex, AI PM -- Montreal (JMSB/Ampliwork)"
    )

    return subject, body


def generate_for_brand(row):
    brand = row["brand"]
    score_data = load_json(brand, "score")
    gemini_probes = load_json(brand, "gemini_probes")
    source_scores = load_json(brand, "source_scores")
    old_probes = load_json(brand, "probes")

    LEADS_DIR.mkdir(parents=True, exist_ok=True)
    sn = safe_name(brand)

    # LinkedIn
    linkedin_msg = generate_linkedin(brand, row, score_data, gemini_probes)
    linkedin_path = LEADS_DIR / f"{sn}_linkedin.md"
    with open(linkedin_path, "w", encoding="utf-8") as f:
        f.write(f"# LinkedIn: {brand}\n\n")
        f.write(f"**To:** {row.get('contact_name', 'TBD')} ({row.get('contact_role', 'TBD')})\n")
        if row.get("contact_linkedin"):
            f.write(f"**LinkedIn:** {row['contact_linkedin']}\n")
        f.write(f"**Chars:** {len(linkedin_msg)}/280\n\n")
        f.write(f"---\n\n")
        f.write(linkedin_msg)
        f.write(f"\n")

    # Email
    subject, body = generate_email(brand, row, score_data, gemini_probes, source_scores)
    email_path = LEADS_DIR / f"{sn}_email.md"
    with open(email_path, "w", encoding="utf-8") as f:
        f.write(f"# Email: {brand}\n\n")
        f.write(f"**To:** {row.get('contact_name', 'TBD')} ({row.get('contact_role', 'TBD')})\n")
        f.write(f"**Subject:** {subject}\n\n")
        f.write(f"---\n\n")
        f.write(body)
        f.write(f"\n")

    print(f"  LinkedIn: {linkedin_path}")
    print(f"  Email:    {email_path}")


def main():
    with open(TARGETS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Generating outreach for {len(rows)} brands...\n")
    for row in rows:
        generate_for_brand(row)
    print("\nOutreach complete.")


if __name__ == "__main__":
    main()
