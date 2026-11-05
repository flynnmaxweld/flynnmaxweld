"""
Generate a Single Unified Linear / Vercel Craft Bespoke SVG Component & Clean Markdown.
Design:
  - Linear.app & Vercel Design System craft aesthetic
  - Razor-thin 1px micro-borders (#1e242e / #262c36)
  - Muted slate-black background (#090c10 to #0d1117)
  - Crisp typography (-apple-system / Inter / SF Pro)
  - Seamlessly contains:
      1. Brand title + Vibecoder pill + Status indicator
      2. Bio statement
      3. Live Contribution Heatmap Matrix (Emerald Pulse #10b981 / #34d399)
      4. Micro-pill tech stack
  - Output: assets/linear-card.svg
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
NAME = html.escape(config.get("brand_name", "Flynn Maxwel"))
ROLE = html.escape(config.get("role", "Vibecoder"))
SUBROLE = html.escape(config.get("subrole", "Full-Stack Engineer & AI Systems Builder"))
TAGLINE = html.escape(config.get("tagline", "Designing, building, and automating intelligent applications."))
LOCATION = html.escape(config.get("location", "Tirunelveli, Tamil Nadu"))
STATUS = html.escape(config.get("status", "Available for high-impact builds in 2026"))
SKILLS = config.get("skills", [])
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
# 2. Build Unified Linear / Vercel Craft SVG Component
# -----------------------------------------------------------------------------
def generate_linear_unified_card():
    raw_days = fetch_contributions_data()
    out_path = os.path.join("assets", "linear-card.svg")

    if not raw_days:
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

    W = 860
    # Activity Matrix dimensions
    CELL, GAP, RAD = 11.5, 3.5, 2.5
    LEFT, TOP = 44, 156
    COLORS = ["#13171f", "#064e3b", "#047857", "#10b981", "#34d399"]
    GRAY = "#6e7681"
    MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    n = len(contribs)
    NW = (n + 6) // 7
    active_days = sum(1 for c in contribs if c["level"] > 0)

    labels = []
    rects = []
    sd = datetime.date.fromisoformat(contribs[0]["date"])
    last_m = None

    for wk in range(NW):
        d = sd + datetime.timedelta(days=wk * 7)
        if d.month != last_m:
            last_m = d.month
            labels.append(f'<text class="month-lbl" x="{LEFT+wk*(CELL+GAP)}" y="{TOP-8}">{MONTHS[d.month-1]}</text>')

    for name, r in [("M", 1), ("W", 3), ("F", 5)]:
        labels.append(f'<text class="day-lbl" x="22" y="{TOP+r*(CELL+GAP)+CELL-3}">{name}</text>')

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
            f'fill="{COLORS[lvl]}" stroke="#1b2028" stroke-width="0.5" style="animation-delay:{delay}s"/>'
        )

    # Stack Micro-pills inside the card footer
    stack_y = TOP + 7 * (CELL + GAP) + 38
    pill_elements = []
    cur_x = 44
    for skill in SKILLS:
        skill_text = html.escape(skill)
        pill_width = len(skill) * 7.5 + 20
        pill_elements.append(
            f'<g transform="translate({cur_x}, {stack_y})">'
            f'<rect width="{pill_width}" height="22" rx="11" fill="#161b22" stroke="#262c36" stroke-width="0.75"/>'
            f'<text x="{pill_width/2}" y="14" class="pill-text" text-anchor="middle">{skill_text}</text>'
            f'</g>'
        )
        cur_x += pill_width + 8

    H = stack_y + 36

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none">
  <defs>
    <!-- Linear Subtle Glow & Vignette -->
    <radialGradient id="linear-glow" cx="15%" cy="0%" r="65%">
      <stop offset="0%" stop-color="#1f2937" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#090c10" stop-opacity="1"/>
    </radialGradient>

    <!-- Linear Specular Top Border Sheen -->
    <linearGradient id="top-sheen" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#30363d" stop-opacity="0"/>
      <stop offset="30%" stop-color="#3b82f6" stop-opacity="0.5"/>
      <stop offset="50%" stop-color="#10b981" stop-opacity="0.8"/>
      <stop offset="70%" stop-color="#3b82f6" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="#30363d" stop-opacity="0"/>
    </linearGradient>

    <style>
      .hero-name {{
        font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif;
        font-size: 24px;
        font-weight: 700;
        fill: #f0f6fc;
        letter-spacing: -0.6px;
      }}
      .role-pill-text {{
        font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
        font-size: 11px;
        font-weight: 600;
        fill: #34d399;
        letter-spacing: 0.3px;
      }}
      .meta-label {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: 11px;
        font-weight: 500;
        fill: #7d8590;
      }}
      .bio-text {{
        font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif;
        font-size: 13.5px;
        font-weight: 400;
        fill: #9ca3af;
      }}
      .section-hdr {{
        font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        fill: #6e7681;
      }}
      .month-lbl {{
        font-family: ui-monospace, SFMono-Regular, monospace;
        font-size: 9.5px;
        font-weight: 500;
        fill: #6e7681;
      }}
      .day-lbl {{
        font-family: ui-monospace, SFMono-Regular, monospace;
        font-size: 9px;
        font-weight: 500;
        fill: #4b5563;
      }}
      .pill-text {{
        font-family: ui-monospace, SFMono-Regular, monospace;
        font-size: 10px;
        font-weight: 500;
        fill: #c9d1d9;
      }}
      .c {{ transform-box:fill-box; transform-origin:center; opacity:0; animation:pop {DUR}s ease-out both; }}
      .g {{ animation:pop {DUR}s ease-out both, flash {DUR+0.15}s ease-out both; }}
      @keyframes pop {{ 0%{{opacity:0;transform:scale(.2)}} 60%{{opacity:1;transform:scale(1.04)}} 100%{{opacity:1;transform:scale(1)}} }}
      @keyframes flash {{ 0%{{filter:brightness(2)}} 50%{{filter:brightness(2)}} 100%{{filter:brightness(1)}} }}
      @media (prefers-reduced-motion: reduce) {{ .c {{ opacity:1 !important; animation:none !important; }} }}
    </style>
  </defs>

  <!-- Card Chassis with 1px Precision Border -->
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="url(#linear-glow)" stroke="#21262d" stroke-width="1"/>
  
  <!-- Razor 1px Top Sheen Accent Line -->
  <line x1="12" y1="1" x2="{W-12}" y2="1" stroke="url(#top-sheen)" stroke-width="1"/>

  <!-- Top Hero Header Row -->
  <!-- Name -->
  <text x="44" y="44" class="hero-name">{NAME}</text>
  
  <!-- Vibecoder Badge -->
  <g transform="translate(196, 28)">
    <rect width="84" height="22" rx="11" fill="#064e3b" fill-opacity="0.3" stroke="#047857" stroke-width="0.75"/>
    <text x="42" y="15" class="role-pill-text" text-anchor="middle">{ROLE}</text>
  </g>

  <!-- Location & Status (Right Aligned) -->
  <text x="{W-44}" y="36" class="meta-label" text-anchor="end">{LOCATION}</text>
  <text x="{W-44}" y="52" class="meta-label" text-anchor="end"><tspan fill="#10b981">&#x25CF;</tspan> {active_days} active days in 2026</text>

  <!-- Bio Sentence -->
  <text x="44" y="74" class="bio-text">{TAGLINE}</text>
  <text x="44" y="93" class="meta-label" fill="#6e7681">{SUBROLE}</text>

  <!-- Divider Line -->
  <line x1="44" y1="114" x2="{W-44}" y2="114" stroke="#1f2937" stroke-width="0.75"/>

  <!-- Activity Section Header -->
  <text x="44" y="136" class="section-hdr">ENGINEERING ACTIVITY</text>

  <!-- Heatmap Grid -->
  {"".join(labels)}
  {"".join(rects)}

  <!-- Legend -->
  <g transform="translate({W-144}, {TOP + 7 * (CELL + GAP) + 10})">
    <text class="month-lbl" x="-26" y="8">Less</text>
    <rect x="0" y="0" width="9" height="9" rx="2" fill="{COLORS[0]}" stroke="#1b2028" stroke-width="0.5"/>
    <rect x="13" y="0" width="9" height="9" rx="2" fill="{COLORS[1]}"/>
    <rect x="26" y="0" width="9" height="9" rx="2" fill="{COLORS[2]}"/>
    <rect x="39" y="0" width="9" height="9" rx="2" fill="{COLORS[3]}"/>
    <rect x="52" y="0" width="9" height="9" rx="2" fill="{COLORS[4]}"/>
    <text class="month-lbl" x="68" y="8">More</text>
  </g>

  <!-- Stack Section Header -->
  <text x="44" y="{stack_y - 12}" class="section-hdr">SYSTEMS &amp; CRAFT</text>

  <!-- Micro-pills -->
  {"".join(pill_elements)}
</svg>'''

    ET.fromstring(svg)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated Linear Unified Craft Card: {out_path}")


# -----------------------------------------------------------------------------
# 3. Clean Linear-style Markdown Layout (README.md)
# -----------------------------------------------------------------------------
def generate_linear_readme():
    md = []

    # Single Unified Linear Card Component
    md.append('<div align="center">\n')
    md.append('  <a href="https://flynnmaxweld.github.io">\n')
    md.append('    <img src="./assets/linear-card.svg" width="860" alt="Flynn Maxwel — Vibecoder" />\n')
    md.append('  </a>\n')
    md.append('</div>\n\n')

    # Selected Works Section (Linear Clean List)
    md.append('### Deployments\n\n')
    for work in FEATURED_WORKS:
        name = work.get("name", "Project")
        url = work.get("url", "#")
        desc = work.get("desc", "")
        md.append(f'- [**`{name}`**]({url}) &mdash; {desc}\n')
    md.append(f'- [**`github.com/{USERNAME}`**](https://github.com/{USERNAME}) &mdash; Open source codebases &amp; experiments\n\n')

    md.append('---\n\n')

    # Connect Section
    md.append('### Connect\n\n')
    links = []
    for s in SOCIALS:
        label = s.get("label", "Link")
        url = s.get("url", "#")
        links.append(f'- [{label}]({url})')
    md.append('\n'.join(links) + '\n')

    with open("README.md", "w", encoding="utf-8") as f:
        f.writelines(md)
    print("Generated Clean Linear README.md")


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
    print("Rendering Linear / Vercel Craft Profile Suite...")
    print("="*60)

    generate_linear_unified_card()
    generate_linear_readme()
    generate_workflow()

    print("="*60)
    print("Done!")
    print("="*60)
