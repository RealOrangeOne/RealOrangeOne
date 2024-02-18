#!/usr/bin/env python3

import jinja2
from pathlib import Path
import requests
import feedparser
from datetime import date
import time
from operator import itemgetter

PROJECT_DIR = Path(__file__).resolve().parent

TEMPLATE_FILE = PROJECT_DIR / "README.md.j2"
OUTPUT_FILE = PROJECT_DIR / "README.md"


def get_posts() -> list[dict]:
    response = requests.get("https://theorangeone.net/api/latest-posts/?page_size=5&format=json")
    response.raise_for_status()
    return response.json()["results"]

def get_notes() -> list[dict]:
    notes = []
    for note in feedparser.parse("https://notes.theorangeone.net/feed_rss_created.xml")["entries"]:
        notes.append({
            "title": note.title,
            "link": note.link,
            "published": date.fromtimestamp(time.mktime(note.published_parsed)),
            "tags": sorted([tag.term for tag in getattr(note, "tags", [])])
        })

    return sorted(notes, key=itemgetter("published"), reverse=True)[:5]


def main():
    template = jinja2.Template(TEMPLATE_FILE.read_text())

    new_readme = template.render(
        latest_posts=get_posts(),
        recent_notes=get_notes()
    )

    OUTPUT_FILE.write_text(new_readme)

if __name__ == "__main__":
    main()
