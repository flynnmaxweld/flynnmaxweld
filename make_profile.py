"""
Compile Pure Typographic Luxury Editorial Broadside README.
Zero SVG boxes, zero badge clutter, pure typographic distinction.
"""
import os
import json

CONFIG_PATH = "profile_config.json"
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

NAME = config.get("brand_name", "Flynn Maxwel")
ROLE = config.get("role", "Vibecoder")
TAGLINE = config.get("tagline", "Designing, building, and automating intelligent applications.")
LOCATION = config.get("location", "Tirunelveli, Tamil Nadu, India")
USERNAME = config.get("github_username", "flynnmaxweld")
FEATURED_WORKS = config.get("featured_works", [])
SOCIALS = config.get("social_links", [])

def build_readme():
    lines = []
    lines.append(f'# {NAME}\n')
    lines.append(f'### *{ROLE} &mdash; {TAGLINE}*\n\n')
    lines.append('---\n\n')
    
    lines.append('```\n')
    lines.append(f'ORIGIN       {LOCATION}\n')
    lines.append('DISCIPLINE   Autonomous Agents · Full-Stack Systems · Generative Architecture\n')
    lines.append('STATUS       Active // 2026\n')
    lines.append('```\n\n')
    lines.append('---\n\n')

    lines.append('### /manifesto\n\n')
    lines.append('Software engineering is shifting from manual line-by-line syntax to orchestrating autonomous intelligence, intuitive interfaces, and resilient distributed backends.\n\n')
    lines.append(f'Operating from {LOCATION.replace(", India", "")}, I build production systems at the intersection of modern full-stack web architectures and agentic AI pipelines &mdash; prioritizing clean simplicity, velocity, and elegance over unnecessary complexity.\n\n')
    lines.append('---\n\n')

    lines.append('### /architecture-and-stack\n\n')
    lines.append('- **Core &amp; Languages** &mdash; Python, TypeScript, JavaScript, SQL\n')
    lines.append('- **Web &amp; Frameworks** &mdash; React, Next.js, Node.js, FastAPI\n')
    lines.append('- **Data &amp; Systems** &mdash; PostgreSQL, Docker, Git, Linux\n')
    lines.append('- **AI &amp; Automation** &mdash; Autonomous Agents, LLM Pipelines, Prompt Architecture\n\n')
    lines.append('---\n\n')

    lines.append('### /selected-works\n\n')
    for work in FEATURED_WORKS:
        name = work.get("name", "Project")
        url = work.get("url", "#")
        desc = work.get("desc", "")
        lines.append(f'- [**{name}**]({url})  \n  *{desc}*\n\n')
    lines.append('---\n\n')

    lines.append('### /colophon-and-connect\n\n')
    for s in SOCIALS:
        label = s.get("label", "Link")
        url = s.get("url", "#")
        val = s.get("value", url.replace("https://", "").replace("mailto:", ""))
        lines.append(f'- {label} &mdash; [{val}]({url})\n')

    with open("README.md", "w", encoding="utf-8") as f:
        f.writelines(lines)
    print("Compiled Pure Typographic Luxury Editorial README.md")

if __name__ == "__main__":
    build_readme()
