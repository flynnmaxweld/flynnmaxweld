"""
Generate a Pure Minimalist GitHub Profile README & Frameless Contribution Heatmap.
Design:
  - Zero heavy banners, zero boxes, zero chassis borders
  - Pure native markdown typography: "# Flynn Maxwel — Vibecoder"
  - Frameless, 100% transparent contribution heatmap (just grid dots + labels)
  - Inline clean monochrome devicons for tech stack
  - Minimalist links for /works and /connect
"""
import os
import json
import urllib.request
import re
import datetime
from html.parser import HTMLParser
import xml.etree.ElementTree as ET

# Ensure directories exist
os.makedirs("assets", exist_ok=True)
os.makedirs(os.path.join(".github", "workflows"), exist_ok=True)

# Load configuration
CONFIG_PATH = "profile_config.json"
if not os.path.exists(CONFIG_PATH):
    raise FileNotFoundError(f"Configuration file {CONFIG_PATH} not found.")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

USERNAME = config.get("github_username", "flynnmaxweld")
DISPLAY_NAME = config.get("display_name", "Flynn Maxwel D")
TAGLINE = config.get("tagline", "Designing, building, and automating intelligent applications from New Delhi, India.")
FEATURED_WORKS = config.get("featured_works", [])
SOCIALS = config.get("social_links", [])


# -----------------------------------------------------------------------------
# 1. Scrape Live Contributions
# -----------------------------------------------------------------------------
class ContributionHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.days = []
        
    def handle_starttag(self, tag, attrs):
        if tag == "td":
            attr_dict = dict(attrs)
            if "data-date" in attr_dict and "data-level" in attr_dict:
                self.days.append({
                    "date": attr_dict["data-date"],
                    "level": int(attr_dict["data-level"])
                })


def fetch_contributions_data():
    url = f"https://github.com/users/{USERNAME}/contributions"
    print(f"Fetching contribution data from: {url}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            html_text = r.read().decode("utf-8")
    except Exception as e:
        print(f"Warning: Could not fetch live contributions: {e}")
        return None

    raw_days = []
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_text, "html.parser")
        for td in soup.select("td.ContributionCalendar-day"):
            dt = td.get("data-date")
            lvl = td.get("data-level")
            if dt and lvl is not None:
                raw_days.append({"date": dt, "level": int(lvl)})
    except ImportError:
        parser = ContributionHTMLParser()
        parser.feed(html_text)
        raw_days = parser.days

    if not raw_days:
        matches = re.findall(r'data-date="([\d\-]+)"[^>]*data-level="(\d+)"', html_text)
        if not matches:
            matches = re.findall(r'data-level="(\d+)"[^>]*data-date="([\d\-]+)"', html_text)
            matches = [(d, l) for (l, d) in matches]
        for dt, lvl in matches:
            raw_days.append({"date": dt, "level": int(lvl)})

    return raw_days


# -----------------------------------------------------------------------------
# 2. Transparent & Frameless Contribution Heatmap SVG
# -----------------------------------------------------------------------------
def generate_contributions():
    raw_days = fetch_contributions_data()
    out_path = os.path.join("assets", "contrib-heatmap.svg")
    
    if not raw_days:
        if os.path.exists(out_path):
            print("Preserving existing contrib-heatmap.svg.")
            return True
        today = datetime.date.today()
        raw_days = []
        for i in range(120):
            d = today - datetime.timedelta(days=119 - i)
            raw_days.append({"date": d.isoformat(), "level": 0})

    raw_days.sort(key=lambda x: x["date"])

    first_2026_idx = -1
    for idx, day in enumerate(raw_days):
        if day["date"] >= "2026-01-01":
            first_2026_idx = idx
            break

    if first_2026_idx != -1:
        start_idx = (first_2026_idx // 7) * 7
        contribs = raw_days[start_idx:]
    else:
        contribs = raw_days[-(26 * 7):] if len(raw_days) >= 26 * 7 else raw_days

    if not contribs:
        contribs = raw_days

    CELL, GAP, RAD, LEFT, TOP = 12, 3.5, 2.5, 30, 22
    # Clean GitHub Emerald Palette with transparent background
    COLORS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
    GRAY = "#7d8590"
    MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    n = len(contribs)
    NW = (n + 6) // 7
    W = LEFT + NW * (CELL + GAP) + 10
    H = TOP + 7 * (CELL + GAP) + 8

    labels = []
    rects = []
    sd = datetime.date.fromisoformat(contribs[0]["date"])
    last_m = None

    for wk in range(NW):
        d = sd + datetime.timedelta(days=wk * 7)
        if d.month != last_m:
            last_m = d.month
            labels.append(f'<text class="lbl" x="{LEFT+wk*(CELL+GAP)}" y="{TOP-8}">{MONTHS[d.month-1]}</text>')

    for name, r in [("Mon", 1), ("Wed", 3), ("Fri", 5)]:
        labels.append(f'<text class="lbl" x="2" y="{TOP+r*(CELL+GAP)+CELL-3}">{name}</text>')

    REVEAL, DUR = 2.4, 0.4
    maxorder = (NW - 1) + 6 * 0.55

    for i, c in enumerate(contribs):
        wk, row, lvl = i // 7, i % 7, c["level"]
        x = LEFT + wk * (CELL + GAP)
        y = TOP + row * (CELL + GAP)
        delay = round((wk + row * 0.55) / maxorder * REVEAL, 3)
        cls = "c g" if lvl >= 1 else "c e"
        rects.append(
            f'<rect class="{cls}" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="{RAD}" '
            f'fill="{COLORS[lvl]}" style="animation-delay:{delay}s"/>'
        )

    # 100% Transparent, frameless SVG
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none">
  <defs>
    <style>
      text.lbl {{ fill:{GRAY}; font-size:10px; font-weight:500; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; }}
      .c {{ transform-box:fill-box; transform-origin:center; opacity:0; animation:pop {DUR}s ease-out both; }}
      .g {{ animation:pop {DUR}s ease-out both, flash {DUR+0.15}s ease-out both; }}
      @keyframes pop {{ 0%{{opacity:0;transform:scale(.2)}} 60%{{opacity:1;transform:scale(1.05)}} 100%{{opacity:1;transform:scale(1)}} }}
      @keyframes flash {{ 0%{{filter:brightness(2)}} 50%{{filter:brightness(2)}} 100%{{filter:brightness(1)}} }}
      @media (prefers-reduced-motion: reduce) {{ .c {{ opacity:1 !important; animation:none !important; }} }}
    </style>
  </defs>

  <!-- Frameless Transparent Grid -->
  {"".join(labels)}
  {"".join(rects)}
</svg>'''

    ET.fromstring(svg)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated Frameless Heatmap: {out_path}")
    return True


# -----------------------------------------------------------------------------
# 3. Pure Minimalist Native Markdown README.md
# -----------------------------------------------------------------------------
def generate_readme(has_contrib):
    md = []

    # Pure Native Markdown Hero
    md.append('# Flynn Maxwel &mdash; Vibecoder\n\n')
    md.append(f'{TAGLINE}\n\n')
    md.append('---\n\n')

    # Frameless Centered Heatmap
    if has_contrib:
        md.append('<div align="center">\n')
        md.append('  <img src="./assets/contrib-heatmap.svg" alt="Flynn Maxwel Contributions" />\n')
        md.append('</div>\n\n')
        md.append('---\n\n')

    # Stack: Inline Devicons
    md.append('### Stack\n\n')
    devicons = [
        '<img src="https://skillicons.dev/icons?i=python,js,ts,react,nextjs,nodejs,fastapi,postgres,docker,git,linux" alt="Tech Stack" />'
    ]
    md.append(f'{" ".join(devicons)}\n\n')
    md.append('---\n\n')

    # Selected Works: Minimal Link List
    md.append('### Works\n\n')
    for work in FEATURED_WORKS:
        name = work.get("name", "Project")
        url = work.get("url", "#")
        desc = work.get("desc", "")
        md.append(f'- [**{name}**]({url}) &mdash; {desc}\n')
    md.append(f'- [**github.com/{USERNAME}**](https://github.com/{USERNAME}) &mdash; Open source repositories & experiments\n\n')

    # Connect: Minimal Link List
    md.append('### Connect\n\n')
    links = []
    for s in SOCIALS:
        label = s.get("label", "Link")
        url = s.get("url", "#")
        links.append(f'- [{label}]({url})')
    md.append('\n'.join(links))
    md.append('\n')

    with open("README.md", "w", encoding="utf-8") as f:
        f.writelines(md)
    print("Generated Pure Minimalist README.md")


# -----------------------------------------------------------------------------
# 4. Generate GitHub Action Workflow
# -----------------------------------------------------------------------------
def generate_workflow():
    workflow_yaml = f'''name: Update Profile Art

on:
  schedule:
    - cron: "17 6 * * *"   # ~06:17 UTC every day
  workflow_dispatch: {{}}
  push:
    branches: [main]

permissions:
  contents: write

jobs:
  refresh-profile:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies (optional bs4/requests)
        run: |
          pip install beautifulsoup4 requests || true

      - name: Render dynamic assets
        run: python make_profile.py

      - name: Commit updated art
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "chore: refresh profile art [skip ci]"
          file_pattern: "assets/*.svg README.md profile_config.json"
'''
    workflow_path = os.path.join(".github", "workflows", "update-profile-art.yml")
    with open(workflow_path, "w", encoding="utf-8") as f:
        f.write(workflow_yaml)
    print(f"Generated GitHub Action Workflow: {workflow_path}")


# -----------------------------------------------------------------------------
# Main Execution
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("="*60)
    print("Rendering Pure Minimalist Profile...")
    print("="*60)

    has_contrib = generate_contributions()
    generate_readme(has_contrib)
    generate_workflow()

    print("="*60)
    print("Done!")
    print("="*60)
