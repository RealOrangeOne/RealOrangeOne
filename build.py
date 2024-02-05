#!/usr/bin/env python3

import jinja2
from pathlib import Path
import requests

PROJECT_DIR = Path(__file__).resolve().parent

TEMPLATE_FILE = PROJECT_DIR / "README.md.j2"
OUTPUT_FILE = PROJECT_DIR / "README.md"


def get_posts() -> list[dict]:
    response = requests.get("https://theorangeone.net/api/latest-posts/?page_size=5&format=json")
    response.raise_for_status()
    return response.json()["results"]


def main():
    template = jinja2.Template(TEMPLATE_FILE.read_text())

    OUTPUT_FILE.write_text(template.render(
        latest_posts=get_posts()
    ))

if __name__ == "__main__":
    main()
