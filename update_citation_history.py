#!/usr/bin/env python3
"""
Citation History Updater

Scrapes the current Google Scholar citation count for every publication
that has a `google_scholar_id` in _bibliography/papers.bib (the same
technique as _plugins/google-scholar-citations.rb, reimplemented as a
standalone script so it can run on a schedule without a full Jekyll
build), and appends a dated entry to _data/citation_history.json
whenever the count has changed since the last recorded entry.

Entries can also be added or edited by hand in citation_history.json
(e.g. {"date": "2026-08-17", "count": 5, "source": "manual"}) --
this script only ever appends, it never removes or overwrites existing
entries.
"""

import json
import os
import random
import re
import time
import urllib.request
from datetime import date

SCHOLAR_USER_ID = "IZuASToAAAAJ"  # must match _data/socials.yml -> scholar_userid


def load_papers_from_bib(bib_path):
    """Extract {bib_key: google_scholar_id} for every entry that has one."""
    text = open(bib_path, encoding="utf-8").read()
    papers = {}
    for entry_match in re.finditer(r"@(?!string\b)\w+\{([^,]+),(.*?)\n\}", text, re.DOTALL):
        key = entry_match.group(1).strip()
        body = entry_match.group(2)
        gsid_match = re.search(r"google_scholar_id\s*=\s*\{([^}]*)\}", body)
        if gsid_match and gsid_match.group(1).strip():
            papers[key] = gsid_match.group(1).strip()
    return papers


def fetch_citation_count(article_id):
    url = (
        "https://scholar.google.com/citations?view_op=view_citation&hl=en"
        f"&user={SCHOLAR_USER_ID}&citation_for_view={SCHOLAR_USER_ID}:{article_id}"
    )
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=20) as response:
        html = response.read().decode("utf-8", errors="ignore")
    match = re.search(r"Cited by ([\d,]+)", html)
    return int(match.group(1).replace(",", "")) if match else None


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bib_path = os.path.join(script_dir, "_bibliography", "papers.bib")
    history_path = os.path.join(script_dir, "_data", "citation_history.json")

    papers = load_papers_from_bib(bib_path)

    history = {}
    if os.path.exists(history_path):
        with open(history_path, "r", encoding="utf-8") as f:
            history = json.load(f)

    today = date.today().isoformat()
    changed = False

    for key, article_id in papers.items():
        try:
            count = fetch_citation_count(article_id)
        except Exception as e:
            print(f"Failed to fetch citation count for {key}: {e}")
            continue

        if count is None:
            print(f"Could not parse a citation count for {key}")
            continue

        entries = history.setdefault(key, [])
        last_count = entries[-1]["count"] if entries else None
        if count != last_count:
            entries.append({"date": today, "count": count, "source": "scraped"})
            changed = True
            print(f"{key}: {last_count} -> {count}")
        else:
            print(f"{key}: unchanged at {count}")

        time.sleep(random.uniform(1.5, 3.5))

    if changed:
        with open(history_path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print("citation_history.json updated")
    else:
        print("No changes to citation_history.json")


if __name__ == "__main__":
    main()
