"""
Generate a Sleek Premium Japanese Design GitHub Profile README & SVGs.
Aesthetic & Principles:
  - Inspired by Tokyo luxury minimalism (MUJI Luxury / Kenya Hara / Lexus Monolith / Sony Master Series)
  - Monochrome palette: Sumi ink obsidian (#0b0e14 / #0f141c), matte platinum (#e6edf3), brushed titanium (#8b949e)
  - Zero red accents, zero Japanese characters (100% English)
  - Geometric symmetry, subtle 1px hairline craftsmanship, elegant letter-tracking
  - Frameless pristine contribution matrix in sumi & jade/emerald tones
"""
import os
import json
import urllib.request
import re
import datetime
import html
from html.parser import HTMLParser
import xml.etree.ElementTree as ET

os.makedirs("assets", exist_ok=True)
os.makedirs(os.path.join(".github", "workflows"), exist_ok=True)

CONFIG_PATH = "profile_config.json"
if not os.path.exists(CONFIG_PATH):
    raise FileNotFoundError(f"Configuration file {CONFIG_PATH} not found.")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

USERNAME = config.get("github_username", "flynnmaxweld")
BRAND_NAME = html.escape(config.get("brand_name", "FLYNN MAXWEL"))
TITLE = html.escape(config.get("title", "VIBECODER"))
TAGLINE = config.get("tagline", "Designing, building, and automating intelligent applications from Tirunelveli, Tamil Nadu.")
LOCATION = html.escape(config.get("location", "Tirunelveli, Tamil Nadu"))
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
# 2. Sleek Premium Japanese Header SVG (Kenya Hara / Tokyo Minimalist Monolith)
# -----------------------------------------------------------------------------
def generate_zen_header():
    W, H = 860, 160

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none">
  <defs>
    <!-- Brushed Platinum Monolith Gradient -->
    <linearGradient id="plat-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="60%" stop-color="#e6edf3"/>
      <stop offset="100%" stop-color="#a8b1bd"/>
    </linearGradient>

    <!-- Subtle Sumi Shading -->
    <linearGradient id="sumi-edge" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#30363d" stop-opacity="0"/>
      <stop offset="25%" stop-color="#484f58" stop-opacity="0.8"/>
      <stop offset="50%" stop-color="#8b949e" stop-opacity="1"/>
      <stop offset="75%" stop-color="#484f58" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#30363d" stop-opacity="0"/>
    </linearGradient>

    <style>
      .hero-kanji-balance {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
        font-size: 34px;
        font-weight: 700;
        letter-spacing: 16px;
        fill: url(#plat-grad);
      }}
      .sub-title {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 10px;
        text-transform: uppercase;
        fill: #8b949e;
      }}
      .meta-tag {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: 9px;
        font-weight: 500;
        letter-spacing: 3px;
        text-transform: uppercase;
        fill: #545d68;
      }}
    </style>
  </defs>

  <!-- Top Micro Hairline -->
  <line x1="80" y1="28" x2="{W-80}" y2="28" stroke="url(#sumi-edge)" stroke-width="0.75"/>

  <!-- Top Metadata Markers (Balanced Negative Space) -->
  <text x="80" y="20" class="meta-tag">CRAFT // 001</text>
  <text x="{W/2}" y="20" class="meta-tag" text-anchor="middle">PRECISION SYSTEMS</text>
  <text x="{W-80}" y="20" class="meta-tag" text-anchor="end">TIRUNELVELI &#183; TN</text>

  <!-- Hero Typography: Expansive, Calm, Symmetrical -->
  <text x="{W/2 + 8}" y="82" class="hero-kanji-balance" text-anchor="middle">{BRAND_NAME}</text>
  <text x="{W/2 + 5}" y="112" class="sub-title" text-anchor="middle">{TITLE}</text>

  <!-- Bottom Micro Hairline -->
  <line x1="160" y1="134" x2="{W-160}" y2="134" stroke="url(#sumi-edge)" stroke-width="0.75"/>
</svg>'''

    ET.fromstring(svg)

    out_path = os.path.join("assets", "zen-header.svg")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated Sleek Japanese Header: {out_path}")


# -----------------------------------------------------------------------------
# 3. Frameless Sleek Contribution Matrix (Sumi & Jade Tones)
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

    CELL, GAP, RAD, LEFT, TOP = 11, 4, 2, 28, 22
    # Sumi & Emerald Japanese High-End Palette
    COLORS = ["#161b22", "#0f3822", "#195c36", "#269344", "#39d353"]
    GRAY = "#57606a"
    MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    n = len(contribs)
    NW = (n + 6) // 7
    W = LEFT + NW * (CELL + GAP) + 10
    H = TOP + 7 * (CELL + GAP) + 10

    labels = []
    rects = []
    sd = datetime.date.fromisoformat(contribs[0]["date"])
    last_m = None

    for wk in range(NW):
        d = sd + datetime.timedelta(days=wk * 7)
        if d.month != last_m:
            last_m = d.month
            labels.append(f'<text class="lbl" x="{LEFT+wk*(CELL+GAP)}" y="{TOP-8}">{MONTHS[d.month-1]}</text>')

    for name, r in [("M", 1), ("W", 3), ("F", 5)]:
        labels.append(f'<text class="lbl" x="6" y="{TOP+r*(CELL+GAP)+CELL-3}">{name}</text>')

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
            f'fill="{COLORS[lvl]}" stroke="#21262d" stroke-width="0.5" style="animation-delay:{delay}s"/>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none">
  <defs>
    <style>
      text.lbl {{ fill:{GRAY}; font-size:9.5px; font-weight:500; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', monospace; letter-spacing:0.5px; }}
      .c {{ transform-box:fill-box; transform-origin:center; opacity:0; animation:pop {DUR}s ease-out both; }}
      .g {{ animation:pop {DUR}s ease-out both, flash {DUR+0.15}s ease-out both; }}
      @keyframes pop {{ 0%{{opacity:0;transform:scale(.2)}} 60%{{opacity:1;transform:scale(1.04)}} 100%{{opacity:1;transform:scale(1)}} }}
      @keyframes flash {{ 0%{{filter:brightness(2)}} 50%{{filter:brightness(2)}} 100%{{filter:brightness(1)}} }}
      @media (prefers-reduced-motion: reduce) {{ .c {{ opacity:1 !important; animation:none !important; }} }}
    </style>
  </defs>

  {"".join(labels)}
  {"".join(rects)}
</svg>'''

    ET.fromstring(svg)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated Frameless Zen Heatmap: {out_path}")
    return True


# -----------------------------------------------------------------------------
# 4. Japanese Minimalist README.md (English Only, Pure Precision)
# -----------------------------------------------------------------------------
def generate_readme(has_contrib):
    md = []

    # Sleek Premium Header
    md.append('<div align="center">\n')
    md.append('  <img src="./assets/zen-header.svg" width="860" alt="Flynn Maxwel — Vibecoder" />\n')
    md.append('</div>\n\n')

    # Centered Minimalist Philosophy Statement
    md.append('<div align="center">\n\n')
    md.append(f'*{TAGLINE}*\n\n')
    md.append('</div>\n\n')

    md.append('<br/>\n\n')

    # Frameless Activity Matrix
    if has_contrib:
        md.append('<div align="center">\n')
        md.append('  <img src="./assets/contrib-heatmap.svg" alt="Activity Flow" />\n')
        md.append('</div>\n\n')

    md.append('<br/>\n\n')

    # Craft & Tools (Inline Dark Icons)
    md.append('### Craft &amp; Architecture\n\n')
    md.append('<img src="https://skillicons.dev/icons?i=python,js,ts,react,nextjs,nodejs,fastapi,postgres,docker,git,linux&theme=dark" alt="Craft & Tools" />\n\n')

    md.append('---\n\n')

    # Selected Works
    md.append('### Selected Works\n\n')
    for work in FEATURED_WORKS:
        name = work.get("name", "Project")
        url = work.get("url", "#")
        desc = work.get("desc", "")
        md.append(f'- [**`{name}`**]({url}) &mdash; {desc}\n')
    md.append(f'- [**`github.com/{USERNAME}`**](https://github.com/{USERNAME}) &mdash; All open-source repositories & experiments\n\n')

    md.append('---\n\n')

    # Connect
    md.append('### Connect\n\n')
    for s in SOCIALS:
        label = s.get("label", "Link")
        url = s.get("url", "#")
        md.append(f'- [{label}]({url})\n')

    with open("README.md", "w", encoding="utf-8") as f:
        f.writelines(md)
    print("Generated Sleek Japanese README.md")


# -----------------------------------------------------------------------------
# 5. Generate GitHub Action Workflow
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
    print("Rendering Sleek Japanese Minimalist Profile Suite...")
    print("="*60)

    generate_zen_header()
    has_contrib = generate_contributions()
    generate_readme(has_contrib)
    generate_workflow()

    print("="*60)
    print("Done!")
    print("="*60)
