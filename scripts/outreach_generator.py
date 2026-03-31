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


def get_specific_finding(brand, probes, score_data):
    """Extract the most compelling specific finding for outreach."""
    if not score_data:
        return f"your brand has gaps in French AI discovery"

    llm_scores = score_data.get("llm_scores", {})
    ias = score_data.get("ias", 0)

    # Check for ghosting first (most dramatic)
    for llm, data in llm_scores.items():
        details = data.get("details", {})
        if details.get("ghosted"):
            return f"French AI queries return zero mentions of {brand} while English surfaces you immediately"

    # Check for hijacking
    for llm, data in llm_scores.items():
        details = data.get("details", {})
        if details.get("hijacking"):
            comps = details.get("hijacked_by", [])
            if comps:
                return f"French AI queries for your category surface {comps[0]} instead of {brand}"

    # Check for spec dilution
    for llm, data in llm_scores.items():
        details = data.get("details", {})
        ratio = details.get("spec_ratio", 1)
        if isinstance(ratio, (int, float)) and ratio < 0.8:
            pct = int((1 - ratio) * 100)
            return f"{pct}% of your technical specs get dropped when AI responds in French"

    return f"your French AI discovery score is {ias}/100 across Claude, GPT-4o, and Gemini"


def generate_linkedin(brand, row, probes, score_data):
    """Generate LinkedIn message -- under 280 chars."""
    first_name = get_first_name(row.get("contact_name", ""))
    category = row.get("product_category", "")
    competitor = row.get("top_competitor", "")
    ias = score_data.get("ias", 0) if score_data else "?"

    msg = (f"Hi {first_name}, ran an AI audit on {brand} -- French searches for "
           f"{category} surface {competitor} over you across GPT, Gemini + Claude. "
           f"Score: {ias}/100. Have the full report.")

    # Trim if over 280
    if len(msg) > 280:
        msg = msg[:277] + "..."

    return msg


def generate_email(brand, row, probes, score_data):
    """Generate 4-sentence outreach email."""
    first_name = get_first_name(row.get("contact_name", ""))
    generic_fr = row.get("generic_query_fr", "")
    ias = score_data.get("ias", 0) if score_data else "?"
    finding = get_specific_finding(brand, probes, score_data)

    subject = f"{brand} scores {ias}/100 on French AI discovery"

    body = (
        f"{first_name}, I tested how Claude, GPT-4o, and Gemini handle {brand} in French vs English. "
        f'On "{generic_fr}", {finding}. '
        f"Your Inference Alignment Score is {ias}/100 across all three platforms. "
        f"Full audit with side-by-side receipts ready -- 10 min to walk through?\n\n"
        f"Alex -- AI PM, Montreal (JMSB/Ampliwork)"
    )

    return subject, body


def generate_for_brand(row):
    brand = row["brand"]
    probes = load_json(brand, "probes")
    score_data = load_json(brand, "score")

    LEADS_DIR.mkdir(parents=True, exist_ok=True)
    sn = safe_name(brand)

    # LinkedIn
    linkedin_msg = generate_linkedin(brand, row, probes, score_data)
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
    subject, body = generate_email(brand, row, probes, score_data)
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
