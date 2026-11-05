"""
Generate an Apple-inspired Liquid Glass (Cupertino Midnight Frost) GitHub Profile Suite.
Aesthetic:
  - Cupertino Keynote typography: "Flynn Maxwel. Vibecoder." with polished subtitle
  - Frosted liquid glass pill badges (location, status)
  - Zero avatar photo inside the README
  - Liquid Glass Contribution Pod SVG (smooth 20px squircle chassis, glass rim specular gradients, emerald gem tiles)
  - Bento pods for Tech Stack (macOS icon dock), Selected Works & Connect
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
BRAND_NAME = config.get("brand_name", "FLYNN MAXWEL")
TITLE = config.get("title", "Vibecoder")
TAGLINE = config.get("tagline", "Designing, building, and automating intelligent applications.")
LOCATION = config.get("location", "Tirunelveli, Tamil Nadu")
COORDINATES = config.get("coordinates", "8.7139° N, 77.7567° E")
STATUS = config.get("status", "BUILDING IN 2026")
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
# 2. Apple Liquid Glass Contribution Pod SVG
# -----------------------------------------------------------------------------
def generate_liquid_glass_heatmap():
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

    CELL, GAP, RAD, LEFT, TOP = 12, 3.5, 3.5, 42, 42
    # Apple Midnight Gem Palette
    COLORS = ["#1b212b", "#0f4028", "#176e3c", "#28a745", "#3de062"]
    GRAY = "#86868b"
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
        labels.append(f'<text class="lbl" x="12" y="{TOP+r*(CELL+GAP)+CELL-3}">{name}</text>')

    REVEAL, DUR = 2.4, 0.45
    maxorder = (NW - 1) + 6 * 0.55

    for i, c in enumerate(contribs):
        wk, row, lvl = i // 7, i % 7, c["level"]
        x = LEFT + wk * (CELL + GAP)
        y = TOP + row * (CELL + GAP)
        delay = round((wk + row * 0.55) / maxorder * REVEAL, 3)
        cls = "c g" if lvl >= 1 else "c e"
        rects.append(
            f'<rect class="{cls}" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="{RAD}" '
            f'fill="{COLORS[lvl]}" stroke="#2d3440" stroke-width="0.5" style="animation-delay:{delay}s"/>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none">
  <defs>
    <!-- Liquid Glass Surface Gradient -->
    <linearGradient id="glass-body" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#161b22" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#0d1117" stop-opacity="0.95"/>
    </linearGradient>

    <!-- Specular Frosted Glass Rim -->
    <linearGradient id="glass-rim" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#8b949e" stop-opacity="0.45"/>
      <stop offset="40%" stop-color="#30363d" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#161b22" stop-opacity="0.1"/>
    </linearGradient>

    <!-- Top Gloss Sheen -->
    <linearGradient id="top-sheen" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="50%" stop-color="#ffffff" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>

    <style>
      text.lbl {{ fill:{GRAY}; font-size:10px; font-weight:500; font-family:-apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Segoe UI', sans-serif; }}
      text.pod-title {{ fill:#f5f5f7; font-size:11px; font-weight:600; font-family:-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', sans-serif; letter-spacing:0.5px; }}
      text.pod-sub {{ fill:#86868b; font-size:10px; font-weight:500; font-family:-apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif; }}
      .c {{ transform-box:fill-box; transform-origin:center; opacity:0; animation:pop {DUR}s ease-out both; }}
      .g {{ animation:pop {DUR}s ease-out both, flash {DUR+0.15}s ease-out both; }}
      @keyframes pop {{ 0%{{opacity:0;transform:scale(.2)}} 60%{{opacity:1;transform:scale(1.05)}} 100%{{opacity:1;transform:scale(1)}} }}
      @keyframes flash {{ 0%{{filter:brightness(2.2)}} 50%{{filter:brightness(2.2)}} 100%{{filter:brightness(1)}} }}
      @media (prefers-reduced-motion: reduce) {{ .c {{ opacity:1 !important; animation:none !important; }} }}
    </style>
  </defs>

  <!-- Cupertino Liquid Glass Chassis (20px squircle) -->
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="20" fill="url(#glass-body)" stroke="url(#glass-rim)" stroke-width="1"/>
  
  <!-- Subtle Top Specular Glass Sheen Highlight -->
  <rect x="20" y="1" width="{W-40}" height="1" fill="url(#top-sheen)"/>

  <!-- Top Glass Header -->
  <text x="24" y="24" class="pod-title">Telemetry &amp; Contributions</text>
  <text x="{W-24}" y="24" class="pod-sub" text-anchor="end"><tspan fill="#34c759">&#x25CF;</tspan> {active_days} Active Days in 2026</text>

  <!-- Activity Grid -->
  {"".join(labels)}
  {"".join(rects)}

  <!-- Legend -->
  <g transform="translate({W-140}, {H-18})">
    <text class="lbl" x="-28" y="9">Less</text>
    <rect x="0" y="0" width="10" height="10" rx="2.5" fill="{COLORS[0]}" stroke="#2d3440" stroke-width="0.5"/>
    <rect x="14" y="0" width="10" height="10" rx="2.5" fill="{COLORS[1]}"/>
    <rect x="28" y="0" width="10" height="10" rx="2.5" fill="{COLORS[2]}"/>
    <rect x="42" y="0" width="10" height="10" rx="2.5" fill="{COLORS[3]}"/>
    <rect x="56" y="0" width="10" height="10" rx="2.5" fill="{COLORS[4]}"/>
    <text class="lbl" x="72" y="9">More</text>
  </g>
</svg>'''

    ET.fromstring(svg)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated Liquid Glass Contribution Pod: {out_path}")
    return True


# -----------------------------------------------------------------------------
# 3. Generate Apple Liquid Glass README.md
# -----------------------------------------------------------------------------
def generate_apple_readme():
    md = []

    # ==================== APPLE KEYNOTE HEADLINE (NO AVATAR) ====================
    md.append('<div align="center">\n\n')
    md.append('# Flynn Maxwel. Vibecoder.\n\n')
    md.append(f'### *"{TAGLINE}"*\n\n')
    md.append(f'`📍 {LOCATION}` &nbsp;&bull;&nbsp; `⚡ {STATUS}` &nbsp;&bull;&nbsp; `🛰️ {COORDINATES}`\n\n')
    md.append('</div>\n\n')

    md.append('<br/>\n\n')

    # ==================== LIQUID GLASS HEATMAP POD ====================
    md.append('<div align="center">\n')
    md.append('  <img src="./assets/contrib-heatmap.svg" width="860" alt="Contribution Pod" />\n')
    md.append('</div>\n\n')

    md.append('<br/>\n\n')

    # ==================== APPLE BENTO PODS ====================
    md.append('<table>\n')
    md.append('  <tr>\n')

    # Left Pod: macOS Developer Dock & Architecture
    md.append('    <td width="50%" valign="top">\n')
    md.append('      <h3>🛠️ Architecture &amp; Stack</h3>\n')
    md.append('      <p>\n')
    md.append('        <a href="https://skillicons.dev">\n')
    md.append('          <img src="https://skillicons.dev/icons?i=python,js,ts,react,nextjs,nodejs,fastapi,postgres,docker,git,linux&perline=6" alt="Developer Stack" />\n')
    md.append('        </a>\n')
    md.append('      </p>\n')
    md.append('      <ul>\n')
    md.append('        <li><b>Languages:</b> Python, TypeScript, JavaScript, SQL</li>\n')
    md.append('        <li><b>Web &amp; Core:</b> React, Next.js, Node.js, FastAPI</li>\n')
    md.append('        <li><b>Platforms:</b> Docker, PostgreSQL, Linux, Git</li>\n')
    md.append('        <li><b>Intelligence:</b> Autonomous Agents, LLM Pipelines</li>\n')
    md.append('      </ul>\n')
    md.append('    </td>\n')

    # Right Pod: Selected Works & Connect
    md.append('    <td width="50%" valign="top">\n')
    md.append('      <h3>📂 Featured Works</h3>\n')
    md.append('      <ul>\n')
    for work in FEATURED_WORKS:
        name = work.get("name", "Project")
        url = work.get("url", "#")
        desc = work.get("desc", "")
        md.append(f'        <li><a href="{url}"><b><code>{name}</code></b></a><br/>{desc}</li>\n')
    md.append(f'        <li><a href="https://github.com/{USERNAME}"><b><code>github.com/{USERNAME}</code></b></a><br/>Open-source projects &amp; experiments</li>\n')
    md.append('      </ul>\n')
    md.append('      <hr/>\n')
    md.append('      <h3>🔗 Connect</h3>\n')
    md.append('      <p>\n')
    connects = []
    for s in SOCIALS:
        label = s.get("label", "Link")
        url = s.get("url", "#")
        connects.append(f'<a href="{url}"><b><code>{label}</code></b></a>')
    md.append(' &nbsp;&bull;&nbsp; '.join(connects) + '\n')
    md.append('      </p>\n')
    md.append('    </td>\n')

    md.append('  </tr>\n')
    md.append('</table>\n')

    with open("README.md", "w", encoding="utf-8") as f:
        f.writelines(md)
    print("Generated Apple Liquid Glass README.md")


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
    print("Rendering Apple Liquid Glass Profile Suite...")
    print("="*60)

    generate_liquid_glass_heatmap()
    generate_apple_readme()
    generate_workflow()

    print("="*60)
    print("Done!")
    print("="*60)
