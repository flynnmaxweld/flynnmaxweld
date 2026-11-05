"""
Generate Friendly Neighborhood Vibecoder (Peter Parker Indie Hacker) Suite.
Features:
  - Subtle spider-web wireline geometry and Peter Parker lab notebook aesthetic
  - Custom Parker Lab Header SVG (assets/parker-header.svg)
  - Subtle web-green / crimson spider accent activity heatmap (assets/contrib-heatmap.svg)
  - Clean indie hacker sticker matrix for stack & lab experiments
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
ALIAS = html.escape(config.get("alias", "YOUR FRIENDLY NEIGHBORHOOD VIBECODER"))
TAGLINE = html.escape(config.get("tagline", "Designing, building, and automating intelligent applications from Tirunelveli, Tamil Nadu."))
LOCATION = html.escape(config.get("location", "Tirunelveli, Tamil Nadu"))
COORDINATES = html.escape(config.get("coordinates", "8.7139° N, 77.7567° E"))
STATUS = html.escape(config.get("status", "PATROLLING & BUILDING // 2026"))
SKILLS = config.get("skills", {})
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
# 2. Peter Parker Lab Header SVG (Subtle Web-line geometry & Indie Badge)
# -----------------------------------------------------------------------------
def generate_parker_header():
    W, H = 860, 200

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none">
  <defs>
    <!-- Dark Lab Background -->
    <radialGradient id="lab-bg" cx="50%" cy="50%" r="70%">
      <stop offset="0%" stop-color="#151b23"/>
      <stop offset="100%" stop-color="#0a0d12"/>
    </radialGradient>

    <!-- Crimson Spider Accent Gradient -->
    <linearGradient id="spider-crimson" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#e53e3e"/>
      <stop offset="100%" stop-color="#c53030"/>
    </linearGradient>

    <style>
      .hero-title {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Impact', sans-serif;
        font-size: 38px;
        font-weight: 900;
        letter-spacing: -0.5px;
        fill: #f0f6fc;
      }}
      .alias-pill {{
        font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
        font-size: 10.5px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        fill: #fca5a5;
      }}
      .lab-meta {{
        font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 1px;
        fill: #8b949e;
      }}
      .status-tag {{
        font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1px;
        fill: #4ade80;
      }}
    </style>
  </defs>

  <!-- Lab Chassis with Subtle 1px Border -->
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="8" fill="url(#lab-bg)" stroke="#262c36" stroke-width="1"/>

  <!-- Subtle Spider Web Geometry Lines (Top Right Corner) -->
  <path d="M {W-140} 0 L {W} 140" stroke="#21262d" stroke-width="0.75"/>
  <path d="M {W-90} 0 L {W} 90" stroke="#21262d" stroke-width="0.75"/>
  <path d="M {W-45} 0 L {W} 45" stroke="#21262d" stroke-width="0.75"/>
  <path d="M {W-110} 30 Q {W-70} 70 {W-30} 110" stroke="#1f2937" stroke-width="0.75" fill="none"/>
  <path d="M {W-75} 20 Q {W-50} 50 {W-20} 75" stroke="#1f2937" stroke-width="0.75" fill="none"/>

  <!-- Top Metadata Bar -->
  <text x="36" y="32" class="lab-meta">LAB REF // INDIE-01</text>
  <text x="210" y="32" class="status-tag">&#x25CF; {STATUS}</text>
  <text x="{W-36}" y="32" class="lab-meta" text-anchor="end">{LOCATION}</text>

  <!-- Hero Name Block -->
  <text x="36" y="96" class="hero-title">{BRAND_NAME}</text>

  <!-- Peter Parker "Friendly Neighborhood Vibecoder" Crimson Sticker Pill -->
  <g transform="translate(36, 114)">
    <rect width="365" height="26" rx="4" fill="#7f1d1d" fill-opacity="0.35" stroke="#dc2626" stroke-width="0.75"/>
    <text x="12" y="17" class="alias-pill">&#x25C6; {ALIAS}</text>
  </g>

  <!-- Subtle Webline Divider -->
  <line x1="36" y1="162" x2="{W-36}" y2="162" stroke="#21262d" stroke-width="1"/>
  <line x1="420" y1="162" x2="480" y2="162" stroke="#dc2626" stroke-width="1.5"/>

  <!-- Bottom Coordinates & Origin -->
  <text x="36" y="184" class="lab-meta">COORD: {COORDINATES}</text>
  <text x="{W-36}" y="184" class="lab-meta" text-anchor="end">AUTONOMOUS AGENTS &amp; FULL-STACK TECH // @{USERNAME}</text>
</svg>'''

    ET.fromstring(svg)

    out_path = os.path.join("assets", "parker-header.svg")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated Peter Parker Lab Header: {out_path}")


# -----------------------------------------------------------------------------
# 3. Web-Themed Contribution Heatmap SVG (Frameless + Crimson/Emerald Accents)
# -----------------------------------------------------------------------------
def generate_parker_heatmap():
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

    CELL, GAP, RAD, LEFT, TOP = 11.5, 3.5, 2.5, 32, 24
    # Web-Slinger Palette: Void Slate -> Web Green -> Crimson Spark
    COLORS = ["#161b22", "#064e3b", "#059669", "#10b981", "#ef4444"]
    GRAY = "#6e7681"
    MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    n = len(contribs)
    NW = (n + 6) // 7
    W = LEFT + NW * (CELL + GAP) + 12
    H = TOP + 7 * (CELL + GAP) + 12

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
      text.lbl {{ fill:{GRAY}; font-size:9.5px; font-weight:600; font-family:ui-monospace, SFMono-Regular, monospace; }}
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
    print(f"Generated Web Activity Matrix: {out_path}")
    return True


# -----------------------------------------------------------------------------
# 4. Generate Parker Indie Hacker README.md
# -----------------------------------------------------------------------------
def generate_parker_readme():
    md = []

    # Custom Header Banner
    md.append('<div align="center">\n')
    md.append('  <a href="https://flynnmaxweld.github.io">\n')
    md.append('    <img src="./assets/parker-header.svg" width="860" alt="Flynn Maxwel — Friendly Neighborhood Vibecoder" />\n')
    md.append('  </a>\n')
    md.append('</div>\n\n')

    # Casual Lab Notebook Quote
    md.append(f'> *"With great compute comes great velocity."*\n>\n> Designing, building, and automating intelligent applications from **Tirunelveli, Tamil Nadu**.\n\n')

    # Centered Frameless Heatmap Matrix
    md.append('### 🕸️ Patrol &amp; Commit Telemetry\n\n')
    md.append('<div align="center">\n')
    md.append('  <img src="./assets/contrib-heatmap.svg" alt="Activity Flow" />\n')
    md.append('</div>\n\n')

    md.append('---\n\n')

    # Lab Tech Stack Matrix
    md.append('### ⚡ Web-Shooters &amp; Lab Gear\n\n')
    md.append('| Gear Category | Technologies &amp; Tools |\n')
    md.append('| :--- | :--- |\n')

    badge_map = {
        "Python": "https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white",
        "JavaScript": "https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black",
        "TypeScript": "https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white",
        "SQL": "https://img.shields.io/badge/SQL-CC292B?style=flat-square&logo=sqlite&logoColor=white",
        "React": "https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB",
        "Next.js": "https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=next.js&logoColor=white",
        "Node.js": "https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=node.js&logoColor=white",
        "FastAPI": "https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white",
        "Docker": "https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white",
        "PostgreSQL": "https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white",
        "Git": "https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white",
        "Linux": "https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black",
        "Autonomous Agents": "https://img.shields.io/badge/Autonomous_Agents-DC2626?style=flat-square&logo=probot&logoColor=white",
        "LLM Pipelines": "https://img.shields.io/badge/LLM_Pipelines-8B5CF6?style=flat-square&logo=openai&logoColor=white",
        "Workflow Automation": "https://img.shields.io/badge/Automation-10B981?style=flat-square&logo=githubactions&logoColor=white"
    }

    if isinstance(SKILLS, dict):
        for category, items in SKILLS.items():
            badges = []
            for item in items:
                url = badge_map.get(item, f"https://img.shields.io/badge/{item.replace(' ', '_')}-21262d?style=flat-square")
                badges.append(f'![]({url})')
            md.append(f'| **{category}** | {" ".join(badges)} |\n')
    md.append('\n---\n\n')

    # Selected Works / Deployments
    md.append('### 🎒 Experiments &amp; Deployments\n\n')
    for work in FEATURED_WORKS:
        name = work.get("name", "Project")
        url = work.get("url", "#")
        desc = work.get("desc", "")
        md.append(f'- [**`{name}`**]({url}) &mdash; {desc}\n')
    md.append(f'- [**`github.com/{USERNAME}`**](https://github.com/{USERNAME}) &mdash; All open-source repositories &amp; lab prototypes\n\n')

    md.append('---\n\n')

    # Connect Channels (Radio Frequency)
    md.append('### 📻 Radio Frequencies\n\n')
    connects = []
    for s in SOCIALS:
        label = s.get("label", "Link")
        url = s.get("url", "#")
        badge = s.get("badge")
        if badge:
            connects.append(f'[![{label}]({badge})]({url})')
        else:
            connects.append(f'[{label}]({url})')

    md.append(" &nbsp; ".join(connects) + '\n')

    with open("README.md", "w", encoding="utf-8") as f:
        f.writelines(md)
    print("Generated Peter Parker Indie Hacker README.md")


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
    print("Rendering Peter Parker Indie Hacker Suite...")
    print("="*60)

    generate_parker_header()
    generate_parker_heatmap()
    generate_parker_readme()
    generate_workflow()

    print("="*60)
    print("Done!")
    print("="*60)
