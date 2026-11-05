"""
Generate a Dark Glassmorphism Personal Bento Grid GitHub Profile README.
Layout Architecture:
  - Asymmetric Bento Grid using clean GitHub-supported HTML tables & styled cards
  - Card 1: Hero Identity (Avatar + Name + VIBECODER + Tirunelveli, Tamil Nadu coordinates)
  - Card 2: Mission Telemetry & Live Frameless Heatmap
  - Card 3: Stack & Architecture (Categorized high-contrast badges)
  - Card 4: Selected Works & Deployments
  - Card 5: Connect & Frequency Channels
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
TAGLINE = config.get("tagline", "Designing, building, and automating intelligent applications.")
LOCATION = html.escape(config.get("location", "Tirunelveli, Tamil Nadu"))
COORDINATES = html.escape(config.get("coordinates", "8.7139° N, 77.7567° E"))
STATUS = html.escape(config.get("status", "BUILDING IN 2026"))
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
# 2. Sleek Bento Heatmap SVG
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

    CELL, GAP, RAD, LEFT, TOP = 11, 3.5, 2.5, 26, 20
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
            labels.append(f'<text class="lbl" x="{LEFT+wk*(CELL+GAP)}" y="{TOP-6}">{MONTHS[d.month-1]}</text>')

    for name, r in [("Mon", 1), ("Wed", 3), ("Fri", 5)]:
        labels.append(f'<text class="lbl" x="2" y="{TOP+r*(CELL+GAP)+CELL-3}">{name}</text>')

    REVEAL, DUR = 2.0, 0.4
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

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none">
  <defs>
    <style>
      text.lbl {{ fill:{GRAY}; font-size:9.5px; font-weight:500; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', monospace; }}
      .c {{ transform-box:fill-box; transform-origin:center; opacity:0; animation:pop {DUR}s ease-out both; }}
      .g {{ animation:pop {DUR}s ease-out both, flash {DUR+0.15}s ease-out both; }}
      @keyframes pop {{ 0%{{opacity:0;transform:scale(.2)}} 60%{{opacity:1;transform:scale(1.05)}} 100%{{opacity:1;transform:scale(1)}} }}
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
    print(f"Generated Bento Heatmap: {out_path}")
    return True


# -----------------------------------------------------------------------------
# 3. Generate Personal Bento Grid README.md
# -----------------------------------------------------------------------------
def generate_bento_readme():
    md = []

    # ==================== CARD 1: HERO IDENTITY BENTO ====================
    md.append('<table>\n')
    md.append('  <tr>\n')
    md.append('    <td width="130" align="center" valign="middle">\n')
    md.append('      <img src="./avatar.png" width="105" style="border-radius:50%;" alt="Flynn Maxwel" />\n')
    md.append('    </td>\n')
    md.append('    <td valign="middle">\n')
    md.append('      <h2>Flynn Maxwel &mdash; <code>VIBECODER</code></h2>\n')
    md.append(f'      <p><b>{TAGLINE}</b></p>\n')
    md.append(f'      <p><code>📍 {LOCATION}</code> &nbsp;&middot;&nbsp; <code>🛰️ {COORDINATES}</code> &nbsp;&middot;&nbsp; <code>⚡ {STATUS}</code></p>\n')
    md.append('    </td>\n')
    md.append('  </tr>\n')
    md.append('</table>\n\n')

    # ==================== CARD 2: LIVE TELEMETRY & ACTIVITY ====================
    md.append('### 📡 Activity &amp; Live Telemetry\n\n')
    md.append('<div align="center">\n')
    md.append('  <img src="./assets/contrib-heatmap.svg" alt="Live Contributions Flow" />\n')
    md.append('</div>\n\n')

    # ==================== 2-COLUMN ASYMMETRIC BENTO GRID (Cards 3, 4, 5) ====================
    md.append('<table>\n')
    md.append('  <tr>\n')
    
    # Left Column: Tech Stack & Architecture (Card 3)
    md.append('    <td width="50%" valign="top">\n')
    md.append('      <h3>🛠️ Systems &amp; Stack</h3>\n')
    md.append('      <p>\n')
    md.append('        <a href="https://skillicons.dev">\n')
    md.append('          <img src="https://skillicons.dev/icons?i=python,js,ts,react,nextjs,nodejs,fastapi,postgres,docker,git,linux&perline=6" alt="Tech Stack" />\n')
    md.append('        </a>\n')
    md.append('      </p>\n')
    md.append('      <ul>\n')
    md.append('        <li><b>Languages:</b> Python, JavaScript, TypeScript, SQL</li>\n')
    md.append('        <li><b>Web &amp; APIs:</b> React, Next.js, Node.js, FastAPI</li>\n')
    md.append('        <li><b>Systems:</b> Docker, PostgreSQL, Linux, Git</li>\n')
    md.append('        <li><b>AI &amp; Workflows:</b> Autonomous Agents, LLM Pipelines</li>\n')
    md.append('      </ul>\n')
    md.append('    </td>\n')

    # Right Column: Projects & Connect (Cards 4 & 5)
    md.append('    <td width="50%" valign="top">\n')
    md.append('      <h3>📂 Selected Deployments</h3>\n')
    md.append('      <ul>\n')
    for work in FEATURED_WORKS:
        name = work.get("name", "Project")
        url = work.get("url", "#")
        desc = work.get("desc", "")
        md.append(f'        <li><a href="{url}"><b><code>{name}</code></b></a><br/>{desc}</li>\n')
    md.append(f'        <li><a href="https://github.com/{USERNAME}"><b><code>github.com/{USERNAME}</code></b></a><br/>Open-source repositories &amp; experiments</li>\n')
    md.append('      </ul>\n')
    md.append('      <hr/>\n')
    md.append('      <h3>🛰️ Connect</h3>\n')
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
    print("Generated Bento Grid README.md")


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
    print("Rendering Personal Bento Grid Profile Suite...")
    print("="*60)

    generate_contributions()
    generate_bento_readme()
    generate_workflow()

    print("="*60)
    print("Done!")
    print("="*60)
