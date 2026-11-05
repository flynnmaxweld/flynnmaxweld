"""
Generate a minimalist Swiss-style GitHub profile README & dynamic SVGs.
Includes:
  1. Dynamic Swiss Editorial Header Banner SVG (`assets/header.svg`)
  2. Dynamic Contribution Heatmap SVG (`assets/contrib-heatmap.svg`) with zero external dependency fallback
  3. High-contrast Swiss-style README.md layout
  4. GitHub Actions workflow to auto-refresh daily
"""
import os
import json
import urllib.request
import re
import datetime
from html.parser import HTMLParser

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
BRAND_NAME = config.get("brand_name", "FLYNN MAXWEL")
TITLE = config.get("title", "Vibecoder · Fullstack & AI Systems Architect")
TAGLINE = config.get("tagline", "Designing, building, and automating intelligent applications from New Delhi, India.")
COORDINATES = config.get("coordinates", "28.6139° N, 77.2090° E")
LOCATION = config.get("location", "New Delhi, IN")
STATUS = config.get("status", "BUILDING IN 2026")
SKILLS = config.get("skills", {})
FEATURED_WORKS = config.get("featured_works", [])
SOCIALS = config.get("social_links", [])

# -----------------------------------------------------------------------------
# 1. Generate Editorial Swiss Header Banner SVG
# -----------------------------------------------------------------------------
def generate_header():
    W, H = 860, 220
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none">
  <defs>
    <linearGradient id="grid-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#30363d" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#161b22" stop-opacity="0.1"/>
    </linearGradient>
    <linearGradient id="text-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="70%" stop-color="#f0f6fc"/>
      <stop offset="100%" stop-color="#8b949e"/>
    </linearGradient>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&amp;family=Space+Grotesk:wght@500;700;800&amp;display=swap');
      .title {{
        font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-size: 50px;
        font-weight: 800;
        letter-spacing: -1.5px;
        fill: url(#text-grad);
      }}
      .mono-meta {{
        font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, monospace;
        font-size: 11px;
        letter-spacing: 1.5px;
        text-transform: uppercase;
      }}
      .sub {{
        font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 15px;
        font-weight: 500;
        fill: #8b949e;
        letter-spacing: -0.2px;
      }}
      .status-dot {{
        animation: pulse 2.5s infinite;
      }}
      @keyframes pulse {{
        0%, 100% {{ opacity: 1; transform: scale(1); }}
        50% {{ opacity: 0.45; transform: scale(0.9); }}
      }}
    </style>
  </defs>

  <!-- Card Background with 1px Swiss Editorial Border -->
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="8" fill="#0d1117" stroke="#30363d" stroke-width="1"/>
  
  <!-- Subtle Architectural Grid Accent Lines -->
  <line x1="36" y1="48" x2="{W-36}" y2="48" stroke="#21262d" stroke-width="1"/>
  <line x1="36" y1="{H-44}" x2="{W-36}" y2="{H-44}" stroke="#21262d" stroke-width="1"/>
  <line x1="610" y1="48" x2="610" y2="{H-44}" stroke="#21262d" stroke-width="1" stroke-dasharray="3 3"/>

  <!-- Top Metadata Bar -->
  <text x="36" y="32" class="mono-meta" fill="#8b949e">INDEX // 001</text>
  <text x="140" y="32" class="mono-meta" fill="#3fb950">● {STATUS}</text>
  <text x="{W-36}" y="32" class="mono-meta" fill="#8b949e" text-anchor="end">{COORDINATES} · {LOCATION}</text>

  <!-- Big Hero Wordmark -->
  <text x="36" y="112" class="title">{BRAND_NAME}</text>
  
  <!-- Subtitle -->
  <text x="38" y="146" class="sub">{TITLE}</text>

  <!-- Right Telemetry Panel -->
  <text x="630" y="80" class="mono-meta" fill="#8b949e">ARCHITECTURE</text>
  <text x="630" y="102" class="mono-meta" fill="#f0f6fc">AUTONOMOUS &amp; DISTRIBUTED</text>
  
  <text x="630" y="132" class="mono-meta" fill="#8b949e">FOCUS</text>
  <text x="630" y="152" class="mono-meta" fill="#388bfd">AI AGENTS &amp; FULL-STACK</text>

  <!-- Bottom Navigation / Metadata Footer -->
  <text x="36" y="{H-20}" class="mono-meta" fill="#484f58">SYSTEM: ONLINE</text>
  <text x="{W-36}" y="{H-20}" class="mono-meta" fill="#8b949e" text-anchor="end">SWISS EDITORIAL V2.0 // @{USERNAME}</text>
</svg>'''

    out_path = os.path.join("assets", "header.svg")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated Editorial Header Banner: {out_path}")


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

    # Try bs4 if available, otherwise use native HTMLParser
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
# 3. Dynamic Contribution Heatmap SVG Generator
# -----------------------------------------------------------------------------
def generate_contributions():
    raw_days = fetch_contributions_data()
    out_path = os.path.join("assets", "contrib-heatmap.svg")
    
    if not raw_days:
        if os.path.exists(out_path):
            print("Preserving existing contrib-heatmap.svg.")
            return True
        print("No contribution data found. Generating placeholder calendar.")
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

    CELL, GAP, RAD, LEFT, TOP = 13, 3.5, 3, 38, 48
    COLORS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
    GRAY = "#7d8590"
    MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    n = len(contribs)
    NW = (n + 6) // 7
    W = 860
    H = 195

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
        labels.append(f'<text class="lbl" x="6" y="{TOP+r*(CELL+GAP)+CELL-3}">{name}</text>')

    REVEAL, DUR = 3.0, 0.45
    maxorder = (NW - 1) + 6 * 0.55

    for i, c in enumerate(contribs):
        wk, row, lvl = i // 7, i % 7, c["level"]
        x = LEFT + wk * (CELL + GAP)
        y = TOP + row * (CELL + GAP)
        delay = round((wk + row * 0.55) / maxorder * REVEAL, 3)
        cls = "c g" if lvl >= 1 else "c e"
        rects.append(
            f'<rect class="{cls}" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="{RAD}" '
            f'fill="{COLORS[lvl]}" stroke="#30363d" stroke-width="0.5" style="animation-delay:{delay}s"/>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&amp;display=swap');
      text.lbl {{ fill:{GRAY}; font-size:11px; font-weight:500; font-family:'JetBrains Mono', monospace; }}
      text.meta {{ fill:#8b949e; font-size:11px; font-family:'JetBrains Mono', monospace; letter-spacing:1px; }}
      text.strong {{ fill:#f0f6fc; font-weight:600; }}
      .c {{ transform-box:fill-box; transform-origin:center; opacity:0; animation:pop {DUR}s ease-out both; }}
      .g {{ animation:pop {DUR}s ease-out both, flash {DUR+0.15}s ease-out both; }}
      @keyframes pop {{ 0%{{opacity:0;transform:scale(.2)}} 60%{{opacity:1;transform:scale(1.08)}} 100%{{opacity:1;transform:scale(1)}} }}
      @keyframes flash {{ 0%{{filter:brightness(2.2)}} 50%{{filter:brightness(2.2)}} 100%{{filter:brightness(1)}} }}
      @media (prefers-reduced-motion: reduce) {{ .c {{ opacity:1 !important; animation:none !important; }} }}
    </style>
  </defs>

  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="8" fill="#0d1117" stroke="#30363d" stroke-width="1"/>

  <text x="24" y="24" class="meta">ACTIVITY STREAM // LIVE CONTRIBUTION TELEMETRY</text>
  <text x="{W-24}" y="24" class="meta" text-anchor="end"><tspan fill="#39d353">●</tspan> ACTIVE DAYS: <tspan class="strong">{active_days}</tspan></text>

  {"".join(labels)}
  {"".join(rects)}

  <g transform="translate({W-160}, {H-18})">
    <text class="lbl" x="-32" y="9">Less</text>
    <rect x="0" y="0" width="10" height="10" rx="2" fill="{COLORS[0]}" stroke="#30363d" stroke-width="0.5"/>
    <rect x="14" y="0" width="10" height="10" rx="2" fill="{COLORS[1]}"/>
    <rect x="28" y="0" width="10" height="10" rx="2" fill="{COLORS[2]}"/>
    <rect x="42" y="0" width="10" height="10" rx="2" fill="{COLORS[3]}"/>
    <rect x="56" y="0" width="10" height="10" rx="2" fill="{COLORS[4]}"/>
    <text class="lbl" x="72" y="9">More</text>
  </g>
  <text x="24" y="{H-10}" class="meta">TIMELINE: <tspan class="strong">{contribs[0]["date"]} &rarr; {contribs[-1]["date"]}</tspan></text>
</svg>'''

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated Contributions Heatmap: {out_path}")
    return True


# -----------------------------------------------------------------------------
# 4. Generate Swiss Editorial README.md
# -----------------------------------------------------------------------------
def generate_readme(has_contrib):
    md = []

    # Dynamic Editorial Hero Banner
    md.append('<div align="center">\n')
    md.append('  <a href="https://flynnmaxweld.github.io">\n')
    md.append('    <img src="./assets/header.svg" width="100%" alt="Flynn Maxwel — Vibecoder &amp; AI Systems Architect" />\n')
    md.append('  </a>\n')
    md.append('</div>\n\n')

    # Editorial Statement Box
    md.append(f'> **"{TAGLINE}"**\n\n')

    # Dynamic Heatmap Graph
    if has_contrib:
        md.append('<div align="center">\n')
        md.append('  <img src="./assets/contrib-heatmap.svg" width="100%" alt="Flynn Maxwel Contribution Telemetry" />\n')
        md.append('</div>\n\n')

    md.append('---\n\n')

    # Tech Stack & Systems Matrix
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
    print("Rendering Swiss Editorial GitHub Profile Suite...")
    print("="*60)

    generate_header()
    has_contrib = generate_contributions()
    generate_readme(has_contrib)
    generate_workflow()

    print("="*60)
    print("Successfully built all assets and README.md!")
    print("="*60)
