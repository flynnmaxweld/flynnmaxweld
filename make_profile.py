"""
Generate a Cinematic Christopher Nolan-inspired GitHub profile README & dynamic SVGs.
Features:
  - Deep space/monolith aesthetic (Interstellar / Oppenheimer / Tenet / Inception vibe)
  - Wide letter-spaced cinematic typography, warm tungsten/amber and icy titanium accents
  - Title: "VIBECODER"
  - Removed "Swiss Editorial" tag and timeline date ranges
  - Heatmap formatted as a clean Mission Telemetry Matrix
"""
import os
import json
import urllib.request
import re
import datetime
import html
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
BRAND_NAME = html.escape(config.get("brand_name", "FLYNN MAXWEL"))
TITLE = html.escape(config.get("title", "VIBECODER"))
TAGLINE = config.get("tagline", "Designing, building, and automating intelligent applications from New Delhi, India.")
COORDINATES = html.escape(config.get("coordinates", "28.6139° N, 77.2090° E"))
LOCATION = html.escape(config.get("location", "New Delhi, IN"))
STATUS = html.escape(config.get("status", "ACTIVE // 2026"))
SKILLS = config.get("skills", {})
FEATURED_WORKS = config.get("featured_works", [])
SOCIALS = config.get("social_links", [])

# -----------------------------------------------------------------------------
# 1. Generate Cinematic Nolan Header Banner SVG
# -----------------------------------------------------------------------------
def generate_header():
    W, H = 860, 220
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none">
  <defs>
    <!-- Deep Cinematic Vignette / Radial Glow -->
    <radialGradient id="vignette" cx="50%" cy="50%" r="75%">
      <stop offset="0%" stop-color="#12161f" stop-opacity="0.8"/>
      <stop offset="60%" stop-color="#090c10" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#05070a" stop-opacity="1"/>
    </radialGradient>
    
    <!-- Nolan Titanium Metallic Title Gradient -->
    <linearGradient id="metallic-title" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="40%" stop-color="#e6edf3"/>
      <stop offset="75%" stop-color="#9ea7b3"/>
      <stop offset="100%" stop-color="#545d68"/>
    </linearGradient>

    <!-- Warm Amber / Tungsten Accent Gradient -->
    <linearGradient id="amber-beam" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#e3b341" stop-opacity="0"/>
      <stop offset="50%" stop-color="#f0883e" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#e3b341" stop-opacity="0"/>
    </linearGradient>

    <style>
      .cinematic-brand {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
        font-size: 38px;
        font-weight: 800;
        letter-spacing: 14px;
        fill: url(#metallic-title);
      }}
      .cinematic-sub {{
        font-family: ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 9px;
        fill: #f0883e;
      }}
      .telemetry-label {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: 9.5px;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        fill: #6e7681;
      }}
      .telemetry-val {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 1.5px;
        fill: #c9d1d9;
      }}
    </style>
  </defs>

  <!-- Deep Slate Outer Chassis with 1px border -->
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="4" fill="url(#vignette)" stroke="#21262d" stroke-width="1"/>

  <!-- Ultra-thin Anamorphic Horizontal Light Blade -->
  <line x1="40" y1="42" x2="{W-40}" y2="42" stroke="#161b22" stroke-width="1"/>
  <rect x="180" y="41.5" width="500" height="1" fill="url(#amber-beam)"/>
  <line x1="40" y1="{H-40}" x2="{W-40}" y2="{H-40}" stroke="#161b22" stroke-width="1"/>

  <!-- Left/Right Film Aperture Crop Marks -->
  <line x1="28" y1="36" x2="28" y2="48" stroke="#30363d" stroke-width="1"/>
  <line x1="28" y1="36" x2="40" y2="36" stroke="#30363d" stroke-width="1"/>
  <line x1="{W-28}" y1="36" x2="{W-28}" y2="48" stroke="#30363d" stroke-width="1"/>
  <line x1="{W-28}" y1="36" x2="{W-40}" y2="36" stroke="#30363d" stroke-width="1"/>

  <line x1="28" y1="{H-36}" x2="28" y2="{H-48}" stroke="#30363d" stroke-width="1"/>
  <line x1="28" y1="{H-36}" x2="40" y2="{H-36}" stroke="#30363d" stroke-width="1"/>
  <line x1="{W-28}" y1="{H-36}" x2="{W-28}" y2="{H-48}" stroke="#30363d" stroke-width="1"/>
  <line x1="{W-28}" y1="{H-36}" x2="{W-40}" y2="{H-36}" stroke="#30363d" stroke-width="1"/>

  <!-- Top Metadata Bar -->
  <text x="44" y="28" class="telemetry-label">SEQUENCE // 001</text>
  <text x="{W/2}" y="28" class="telemetry-val" text-anchor="middle">&#x25CF; {STATUS}</text>
  <text x="{W-44}" y="28" class="telemetry-label" text-anchor="end">{COORDINATES} &#183; {LOCATION}</text>

  <!-- Center Nolan Title Block -->
  <!-- Wide-tracked Hero Name -->
  <text x="{W/2}" y="106" class="cinematic-brand" text-anchor="middle">{BRAND_NAME}</text>
  
  <!-- Single Focus Title: VIBECODER in Amber -->
  <text x="{W/2}" y="142" class="cinematic-sub" text-anchor="middle">{TITLE}</text>

  <!-- Subtle Thin Reticle Center Tick -->
  <circle cx="{W/2}" cy="162" r="2" fill="#30363d"/>

  <!-- Bottom Navigation / Frequency Footer -->
  <text x="44" y="{H-18}" class="telemetry-label">TRANSMISSION: ACTIVE</text>
  <text x="{W/2}" y="{H-18}" class="telemetry-label" text-anchor="middle">70MM // PERSPECTIVE</text>
  <text x="{W-44}" y="{H-18}" class="telemetry-label" text-anchor="end">AUTONOMOUS SYSTEMS // @{USERNAME}</text>
</svg>'''

    ET.fromstring(svg)

    out_path = os.path.join("assets", "header.svg")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated Cinematic Nolan Header: {out_path}")


# -----------------------------------------------------------------------------
# 2. Robust HTML Parser Fallback for Contribution Calendar
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
# 3. Dynamic Contribution Heatmap SVG (Nolan Monolith & Space Palette)
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

    CELL, GAP, RAD, LEFT, TOP = 13, 3.5, 2, 42, 44
    # Nolan Palette: Void obsidian, deep titanium, muted emerald, amber highlight, bright solar
    COLORS = ["#13171f", "#0e3a24", "#1b5e39", "#2ea043", "#56d364"]
    GRAY = "#6e7681"
    MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    n = len(contribs)
    NW = (n + 6) // 7
    W = 860
    H = 188

    active_days = sum(1 for c in contribs if c["level"] > 0)

    labels = []
    rects = []
    sd = datetime.date.fromisoformat(contribs[0]["date"])
    last_m = None

    for wk in range(NW):
        d = sd + datetime.timedelta(days=wk * 7)
        if d.month != last_m:
            last_m = d.month
            labels.append(f'<text class="lbl" x="{LEFT+wk*(CELL+GAP)}" y="{TOP-12}">{MONTHS[d.month-1]}</text>')

    for name, r in [("Mon", 1), ("Wed", 3), ("Fri", 5)]:
        labels.append(f'<text class="lbl" x="8" y="{TOP+r*(CELL+GAP)+CELL-3}">{name}</text>')

    REVEAL, DUR = 2.5, 0.45
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
    <radialGradient id="matrix-grad" cx="50%" cy="50%" r="75%">
      <stop offset="0%" stop-color="#10141d" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#070a0e" stop-opacity="1"/>
    </radialGradient>
    <style>
      text.lbl {{ fill:{GRAY}; font-size:10px; font-weight:600; font-family:ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; letter-spacing:1px; }}
      text.telemetry {{ fill:#6e7681; font-size:9.5px; font-family:ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; letter-spacing:2px; text-transform:uppercase; }}
      text.strong {{ fill:#e6edf3; font-weight:700; }}
      .c {{ transform-box:fill-box; transform-origin:center; opacity:0; animation:pop {DUR}s ease-out both; }}
      .g {{ animation:pop {DUR}s ease-out both, flash {DUR+0.15}s ease-out both; }}
      @keyframes pop {{ 0%{{opacity:0;transform:scale(.2)}} 60%{{opacity:1;transform:scale(1.05)}} 100%{{opacity:1;transform:scale(1)}} }}
      @keyframes flash {{ 0%{{filter:brightness(2.2)}} 50%{{filter:brightness(2.2)}} 100%{{filter:brightness(1)}} }}
      @media (prefers-reduced-motion: reduce) {{ .c {{ opacity:1 !important; animation:none !important; }} }}
    </style>
  </defs>

  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="4" fill="url(#matrix-grad)" stroke="#21262d" stroke-width="1"/>

  <!-- Telemetry Bar -->
  <text x="28" y="24" class="telemetry">ORBITAL ACTIVITY // SYSTEM TELEMETRY</text>
  <text x="{W-28}" y="24" class="telemetry" text-anchor="end"><tspan fill="#3fb950">&#x25CF;</tspan> ACTIVE CYCLES: <tspan class="strong">{active_days}</tspan></text>

  <!-- Labels & Heatmap Grid -->
  {"".join(labels)}
  {"".join(rects)}

  <!-- Legend & Bottom Details (Timeline removed) -->
  <text x="28" y="{H-14}" class="telemetry">STATUS: RUNNING CONTINUOUSLY</text>

  <g transform="translate({W-160}, {H-21})">
    <text class="lbl" x="-32" y="8">LOW</text>
    <rect x="0" y="0" width="9" height="9" rx="1.5" fill="{COLORS[0]}" stroke="#21262d" stroke-width="0.5"/>
    <rect x="13" y="0" width="9" height="9" rx="1.5" fill="{COLORS[1]}"/>
    <rect x="26" y="0" width="9" height="9" rx="1.5" fill="{COLORS[2]}"/>
    <rect x="39" y="0" width="9" height="9" rx="1.5" fill="{COLORS[3]}"/>
    <rect x="52" y="0" width="9" height="9" rx="1.5" fill="{COLORS[4]}"/>
    <text class="lbl" x="68" y="8">PEAK</text>
  </g>
</svg>'''

    ET.fromstring(svg)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated Cinematic Contributions Matrix: {out_path}")
    return True


# -----------------------------------------------------------------------------
# 4. Generate Cinematic Nolan README.md
# -----------------------------------------------------------------------------
def generate_readme(has_contrib):
    md = []

    # Dynamic Cinematic Hero Banner
    md.append('<div align="center">\n')
    md.append('  <a href="https://flynnmaxweld.github.io">\n')
    md.append('    <img src="./assets/header.svg" width="860" alt="Flynn Maxwel — Vibecoder" />\n')
    md.append('  </a>\n')
    md.append('</div>\n\n')

    # Cinematic Statement
    md.append(f'> **"{TAGLINE}"**\n\n')

    # Dynamic Heatmap Matrix
    if has_contrib:
        md.append('<div align="center">\n')
        md.append('  <img src="./assets/contrib-heatmap.svg" width="860" alt="Flynn Maxwel Contribution Telemetry" />\n')
        md.append('</div>\n\n')

    md.append('---\n\n')

    # Tech Stack & Systems Architecture Matrix
    md.append('### ⚙️ Systems &amp; Stack Architecture\n\n')
    md.append('| Domain | Stack &amp; Technologies |\n')
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
        "LLM Workflows": "https://img.shields.io/badge/LLMs_%26_Pipelines-8A2BE2?style=flat-square&logo=openai&logoColor=white",
        "LangChain": "https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square&logo=langchain&logoColor=white",
        "Autonomous Agents": "https://img.shields.io/badge/Autonomous_Agents-0052CC?style=flat-square&logo=probot&logoColor=white"
    }

    if isinstance(SKILLS, dict):
        for category, items in SKILLS.items():
            badges = []
            for item in items:
                url = badge_map.get(item, f"https://img.shields.io/badge/{item.replace(' ', '_')}-21262d?style=flat-square")
                badges.append(f'![]({url})')
            md.append(f'| **{category}** | {" ".join(badges)} |\n')
    md.append('\n---\n\n')

    # Selected Works / Projects
    md.append('### 📂 /selected-works\n\n')
    for work in FEATURED_WORKS:
        name = work.get("name", "Project")
        url = work.get("url", "#")
        desc = work.get("desc", "")
        md.append(f'- [**`{name}`**]({url}) &mdash; {desc}\n')
    md.append(f'- [**`github.com/{USERNAME}`**](https://github.com/{USERNAME}) &mdash; All open-source repositories & experiments\n\n')

    # Connect Section
    md.append('---\n\n')
    md.append('### 🛰️ /telemetry &amp; connect\n\n')
    connects = []
    for s in SOCIALS:
        label = s.get("label", "Link")
        url = s.get("url", "#")
        logo = s.get("logo", "").lower()
        color = s.get("color", "0d1117")
        logo_param = f"&logo={logo}" if logo else ""
        badge = f'[![{label}](https://img.shields.io/badge/{label}-{color}?style=flat-square{logo_param}&logoColor=white)]({url})'
        connects.append(badge)

    md.append(" &nbsp; ".join(connects))
    md.append('\n')

    with open("README.md", "w", encoding="utf-8") as f:
        f.writelines(md)
    print("Generated README.md")


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
    print("Rendering Cinematic Nolan Style Profile Suite...")
    print("="*60)

    generate_header()
    has_contrib = generate_contributions()
    generate_readme(has_contrib)
    generate_workflow()

    print("="*60)
    print("Successfully built all assets and README.md!")
    print("="*60)
