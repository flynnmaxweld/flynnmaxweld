"""
Generate Peter Parker-Inspired Science/Engineering Lab Notebook Profile Suite.
Aesthetic & Tone:
  - Peter Parker the Midtown Science / MIT engineering nerd (Zero Spider-Man puns, zero superhero tropes)
  - Graph paper technical grid lines (dark engineering blue/slate #0d121c)
  - Drafting technical margins, index stamps, precision calipers, ink blue & amber telemetry
  - Header: assets/notebook-header.svg
  - Activity Grid: assets/contrib-heatmap.svg on dark graph paper grid
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
NAME = html.escape(config.get("name", "Flynn Maxwel"))
TITLE = html.escape(config.get("title", "Vibecoder"))
SUBTITLE = html.escape(config.get("subtitle", "Full-Stack Engineer & AI Systems Researcher"))
ABOUT = html.escape(config.get("about", "Building intelligent systems, autonomous agent workflows, and resilient web applications."))
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
# 2. Engineering Lab Notebook Header SVG (Technical Graph Paper / Blueprint)
# -----------------------------------------------------------------------------
def generate_notebook_header():
    W, H = 860, 180

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none">
  <defs>
    <!-- Dark Engineering Graph Paper Pattern -->
    <pattern id="graph-grid" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#162032" stroke-width="0.5"/>
    </pattern>

    <style>
      .hdr-name {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
        font-size: 36px;
        font-weight: 800;
        letter-spacing: -0.5px;
        fill: #f0f6fc;
      }}
      .hdr-title-pill {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        fill: #38bdf8;
      }}
      .hdr-sub {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        font-size: 13.5px;
        font-weight: 500;
        fill: #94a3b8;
      }}
      .meta-lbl {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: 9.5px;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        fill: #475569;
      }}
      .meta-val {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: 9.5px;
        font-weight: 600;
        letter-spacing: 1px;
        fill: #38bdf8;
      }}
    </style>
  </defs>

  <!-- Notebook Chassis with Engineering Slate Background -->
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="8" fill="#0b0f17" stroke="#1e293b" stroke-width="1"/>
  
  <!-- Graph Paper Overlay -->
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="7" fill="url(#graph-grid)"/>

  <!-- Left Technical Margin Guide Line (Drafting red/amber margin mark) -->
  <line x1="28" y1="12" x2="28" y2="{H-12}" stroke="#ef4444" stroke-width="1" stroke-opacity="0.5"/>
  <circle cx="28" cy="28" r="2.5" fill="#ef4444"/>
  <circle cx="28" cy="{H-28}" r="2.5" fill="#ef4444"/>

  <!-- Top Notebook Metadata Header -->
  <text x="44" y="28" class="meta-lbl">LOGBOOK REF: <tspan class="meta-val">MIDTOWN-LAB-2026</tspan></text>
  <text x="{W-36}" y="28" class="meta-lbl" text-anchor="end">SYS: <tspan class="meta-val">ONLINE</tspan></text>

  <!-- Technical Divider Line -->
  <line x1="44" y1="38" x2="{W-36}" y2="38" stroke="#1e293b" stroke-width="0.75"/>

  <!-- Hero Name Block -->
  <text x="44" y="86" class="hdr-name">{NAME}</text>
  
  <!-- Vibecoder Lab Badge -->
  <g transform="translate(305, 62)">
    <rect width="118" height="24" rx="4" fill="#0284c7" fill-opacity="0.18" stroke="#0284c7" stroke-width="0.75"/>
    <text x="59" y="16" class="hdr-title-pill" text-anchor="middle">{TITLE}</text>
  </g>

  <!-- Subtitle -->
  <text x="44" y="116" class="hdr-sub">{SUBTITLE}</text>

  <!-- Bottom Technical Drafting Rule -->
  <line x1="44" y1="138" x2="{W-36}" y2="138" stroke="#1e293b" stroke-width="0.75"/>
  <text x="44" y="158" class="meta-lbl">DISCIPLINE: AUTONOMOUS AGENTS &amp; FULL-STACK ARCHITECTURE</text>
  <text x="{W-36}" y="158" class="meta-lbl" text-anchor="end">EXPERIMENT ARCHIVE // @{USERNAME}</text>
</svg>'''

    ET.fromstring(svg)

    out_path = os.path.join("assets", "notebook-header.svg")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated Engineering Notebook Header: {out_path}")


# -----------------------------------------------------------------------------
# 3. Graph Paper Engineering Contribution Heatmap SVG
# -----------------------------------------------------------------------------
def generate_notebook_heatmap():
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

    CELL, GAP, RAD = 11.5, 3.5, 2
    LEFT, TOP = 44, 42
    # Lab Ink Palette: Deep slate substrate -> Blueprint cyan -> Intense cobalt & amber pulse
    COLORS = ["#131a26", "#0369a1", "#0284c7", "#38bdf8", "#f59e0b"]
    GRAY = "#64748b"
    MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    n = len(contribs)
    NW = (n + 6) // 7
    W = 860
    H = 186
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
        labels.append(f'<text class="lbl" x="12" y="{TOP+r*(CELL+GAP)+CELL-3}">{name}</text>')

    REVEAL, DUR = 2.2, 0.4
    maxorder = (NW - 1) + 6 * 0.55

    for i, c in enumerate(contribs):
        wk, row, lvl = i // 7, i % 7, c["level"]
        x = LEFT + wk * (CELL + GAP)
        y = TOP + row * (CELL + GAP)
        delay = round((wk + row * 0.55) / maxorder * REVEAL, 3)
        cls = "c g" if lvl >= 1 else "c e"
        rects.append(
            f'<rect class="{cls}" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="{RAD}" '
            f'fill="{COLORS[lvl]}" stroke="#1e293b" stroke-width="0.5" style="animation-delay:{delay}s"/>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none">
  <defs>
    <!-- Graph Grid Pattern -->
    <pattern id="heat-graph-grid" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#162032" stroke-width="0.5"/>
    </pattern>

    <style>
      text.lbl {{ fill:{GRAY}; font-size:9.5px; font-weight:600; font-family:ui-monospace, SFMono-Regular, monospace; }}
      text.telemetry {{ fill:#64748b; font-size:9.5px; font-weight:600; font-family:ui-monospace, SFMono-Regular, monospace; letter-spacing:1px; text-transform:uppercase; }}
      text.strong {{ fill:#f0f6fc; font-weight:700; }}
      .c {{ transform-box:fill-box; transform-origin:center; opacity:0; animation:pop {DUR}s ease-out both; }}
      .g {{ animation:pop {DUR}s ease-out both, flash {DUR+0.15}s ease-out both; }}
      @keyframes pop {{ 0%{{opacity:0;transform:scale(.2)}} 60%{{opacity:1;transform:scale(1.05)}} 100%{{opacity:1;transform:scale(1)}} }}
      @keyframes flash {{ 0%{{filter:brightness(2)}} 50%{{filter:brightness(2)}} 100%{{filter:brightness(1)}} }}
      @media (prefers-reduced-motion: reduce) {{ .c {{ opacity:1 !important; animation:none !important; }} }}
    </style>
  </defs>

  <!-- Chassis with Graph Grid -->
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="8" fill="#0b0f17" stroke="#1e293b" stroke-width="1"/>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="7" fill="url(#heat-graph-grid)"/>

  <!-- Top Status -->
  <text x="24" y="24" class="telemetry">RESEARCH LOGS // COMMIT FREQUENCY</text>
  <text x="{W-24}" y="24" class="telemetry" text-anchor="end"><tspan fill="#38bdf8">&#x25CF;</tspan> ACTIVE DAYS IN 2026: <tspan class="strong">{active_days}</tspan></text>

  <!-- Labels & Rects -->
  {"".join(labels)}
  {"".join(rects)}

  <!-- Legend -->
  <g transform="translate({W-140}, {H-16})">
    <text class="lbl" x="-26" y="8">Less</text>
    <rect x="0" y="0" width="9" height="9" rx="1.5" fill="{COLORS[0]}" stroke="#1e293b" stroke-width="0.5"/>
    <rect x="13" y="0" width="9" height="9" rx="1.5" fill="{COLORS[1]}"/>
    <rect x="26" y="0" width="9" height="9" rx="1.5" fill="{COLORS[2]}"/>
    <rect x="39" y="0" width="9" height="9" rx="1.5" fill="{COLORS[3]}"/>
    <rect x="52" y="0" width="9" height="9" rx="1.5" fill="{COLORS[4]}"/>
    <text class="lbl" x="68" y="8">More</text>
  </g>
</svg>'''

    ET.fromstring(svg)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated Graph Paper Heatmap: {out_path}")
    return True


# -----------------------------------------------------------------------------
# 4. Generate Science/Engineering Lab Notebook README.md
# -----------------------------------------------------------------------------
def generate_notebook_readme():
    md = []

    # Notebook Header Banner
    md.append('<div align="center">\n')
    md.append('  <a href="https://flynnmaxweld.github.io">\n')
    md.append('    <img src="./assets/notebook-header.svg" width="860" alt="Flynn Maxwel — Vibecoder" />\n')
    md.append('  </a>\n')
    md.append('</div>\n\n')

    # Concise Scientific Statement
    md.append(f'> **"{ABOUT}"**\n\n')

    # Graph Paper Activity Heatmap
    md.append('### 📊 Research Activity &amp; Commit Logs\n\n')
    md.append('<div align="center">\n')
    md.append('  <img src="./assets/contrib-heatmap.svg" width="860" alt="Research Activity Logs" />\n')
    md.append('</div>\n\n')

    md.append('---\n\n')

    # Lab Stack & Systems Architecture Matrix
    md.append('### 🛠️ Systems &amp; Lab Architecture\n\n')
    md.append('| Technical Domain | Frameworks, Languages &amp; Tooling |\n')
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
        "Autonomous Agents": "https://img.shields.io/badge/Autonomous_Agents-0284C7?style=flat-square&logo=probot&logoColor=white",
        "LLM Pipelines": "https://img.shields.io/badge/LLM_Pipelines-8B5CF6?style=flat-square&logo=openai&logoColor=white",
        "Workflow Systems": "https://img.shields.io/badge/Workflow_Systems-10B981?style=flat-square&logo=githubactions&logoColor=white"
    }

    if isinstance(SKILLS, dict):
        for category, items in SKILLS.items():
            badges = []
            for item in items:
                url = badge_map.get(item, f"https://img.shields.io/badge/{item.replace(' ', '_')}-1e293b?style=flat-square")
                badges.append(f'![]({url})')
            md.append(f'| **{category}** | {" ".join(badges)} |\n')
    md.append('\n---\n\n')

    # Selected Works / Experiments
    md.append('### 📂 Research Prototypes &amp; Deployments\n\n')
    for work in FEATURED_WORKS:
        name = work.get("name", "Project")
        url = work.get("url", "#")
        desc = work.get("desc", "")
        md.append(f'- [**`{name}`**]({url}) &mdash; {desc}\n')
    md.append(f'- [**`github.com/{USERNAME}`**](https://github.com/{USERNAME}) &mdash; All open-source repositories &amp; experiments\n\n')

    md.append('---\n\n')

    # Connect Channels
    md.append('### 🔗 Contact &amp; Channels\n\n')
    connects = []
    for s in SOCIALS:
        label = s.get("label", "Link")
        url = s.get("url", "#")
        connects.append(f'- [**{label}**]({url})')

    md.append('\n'.join(connects) + '\n')

    with open("README.md", "w", encoding="utf-8") as f:
        f.writelines(md)
    print("Generated Engineering Notebook README.md")


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
    print("Rendering Science/Engineering Notebook Suite...")
    print("="*60)

    generate_notebook_header()
    generate_notebook_heatmap()
    generate_notebook_readme()
    generate_workflow()

    print("="*60)
    print("Done!")
    print("="*60)
