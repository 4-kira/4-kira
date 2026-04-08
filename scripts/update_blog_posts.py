#!/usr/bin/env python3
"""Updates README.md with the 3 latest blog posts by parsing the live feed."""

import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

FEED_URL = "https://4-kira.github.io/feed.xml"
README_PATH = Path(__file__).parent.parent / "README.md"
ATOM_NS = "http://www.w3.org/2005/Atom"


def get_latest_posts(n=3):
    with urllib.request.urlopen(FEED_URL) as response:
        root = ET.parse(response).getroot()

    entries = root.findall(f"{{{ATOM_NS}}}entry")
    posts = []
    for entry in entries[:n]:
        title = entry.findtext(f"{{{ATOM_NS}}}title")
        link = entry.find(f"{{{ATOM_NS}}}link").get("href")
        posts.append((title, link))
    return posts


def build_section(posts):
    lines = ["### Latest blog posts", ""]
    for title, link in posts:
        lines.append(f"- [{title}]({link})")
    lines.append("")
    return "\n".join(lines)


def update_readme(posts):
    readme = README_PATH.read_text(encoding="utf-8")
    new_section = build_section(posts)
    updated = re.sub(
        r"### Latest blog posts\n.*?(?=###)",
        new_section + "\n",
        readme,
        flags=re.DOTALL,
    )

    if updated == readme:
        print("No changes.")
        return False

    README_PATH.write_text(updated, encoding="utf-8")
    print("README.md updated:")
    for title, link in posts:
        print(f"  {title} → {link}")
    return True


if __name__ == "__main__":
    posts = get_latest_posts()
    update_readme(posts)
