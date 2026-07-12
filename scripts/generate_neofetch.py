#!/usr/bin/env python3
"""
Generates a neofetch-style terminal SVG card using LIVE GitHub API data.
Run in CI (GITHUB_TOKEN is auto-provided, avoids rate limits) or locally with
GITHUB_TOKEN env var set.

Output: assets/neofetch.svg
"""

import os
import sys
import datetime
import urllib.request
import json

USERNAME = os.environ.get("GH_USERNAME", "Dhanesh10war")
TOKEN = os.environ.get("GITHUB_TOKEN", "")

API = "https://api.github.com"


def gh(path):
    req = urllib.request.Request(f"{API}{path}")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "neofetch-svg-generator")
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode())


def safe_gh(path, default):
    try:
        return gh(path)
    except Exception as e:
        print(f"[warn] {path} failed: {e}", file=sys.stderr)
        return default


def main():
    user = safe_gh(f"/users/{USERNAME}", {})
    repos = safe_gh(f"/users/{USERNAME}/repos?per_page=100&type=owner", [])

    followers = user.get("followers", 0)
    following = user.get("following", 0)
    public_repos = user.get("public_repos", len(repos) if isinstance(repos, list) else 0)
    created_at = user.get("created_at", "")

    account_age = ""
    if created_at:
        created = datetime.datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
        delta = datetime.datetime.utcnow() - created
        years = delta.days // 365
        months = (delta.days % 365) // 30
        account_age = f"{years}y {months}m"

    total_stars = 0
    lang_bytes = {}
    if isinstance(repos, list):
        for r in repos:
            total_stars += r.get("stargazers_count", 0) or 0
            lang = r.get("language")
            if lang:
                lang_bytes[lang] = lang_bytes.get(lang, 0) + 1

    top_langs = sorted(lang_bytes.items(), key=lambda kv: -kv[1])[:5]
    top_langs_str = ", ".join(l for l, _ in top_langs) if top_langs else "N/A"

    name = user.get("name") or USERNAME
    bio = user.get("bio") or ""
    location = user.get("location") or "Unknown"

    rows = [
        ("OS", "AI-Automation-OS x86_64"),
        ("Host", "Final-Year B.E. IT (2026)"),
        ("Uptime", account_age or "n/a"),
        ("Location", location),
        ("Languages", top_langs_str),
        ("Repos", str(public_repos)),
        ("Stars", str(total_stars)),
        ("Followers", str(followers)),
        ("Following", str(following)),
        ("Certs", "AWS Cloud Practitioner"),
        ("Hackathons", "SIH 2025 (Finalist), TANSAM 2025 (Finalist)"),
        ("Focus", "n8n * LLM Tooling * FastAPI * Next.js"),
    ]

    ascii_art = r"""
     ┌──────────────┐
     │ 01001000 01101001
     │ ┌──┐  ┌──┐  ┌──┐
     │ │01│──│10│──│11│
     │ └──┘  └──┘  └──┘
     │   │      │     │
     │ ┌─┴─┐  ┌─┴─┐ ┌─┴─┐
     │ │ D │  │ H │ │ R │
     │ └───┘  └───┘ └───┘
     │      >_ _______
     └──────────────┘
""".strip("\n").split("\n")

    width = 900
    line_h = 26
    top_pad = 70
    height = top_pad + max(len(ascii_art), len(rows) + 2) * line_h + 60

    def esc(s):
        return (
            str(s)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

    svg_parts = []
    svg_parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
    )
    svg_parts.append(
        f"""
        <defs>
          <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#0b0f14"/>
            <stop offset="100%" stop-color="#111827"/>
          </linearGradient>
          <style>
            .mono {{ font-family: 'Fira Code','Consolas',monospace; }}
            .title {{ fill: #00ff9d; font-weight: bold; }}
            .key {{ fill: #00d4ff; }}
            .val {{ fill: #cbd5e1; }}
            .art {{ fill: #00ff9d; opacity: 0.85; }}
            .dim {{ fill: #64748b; }}
          </style>
        </defs>
        <rect x="0" y="0" width="{width}" height="{height}" rx="14" fill="url(#bg)" stroke="#00ff9d" stroke-opacity="0.35"/>
        <circle cx="28" cy="28" r="7" fill="#ff5f56"/>
        <circle cx="50" cy="28" r="7" fill="#ffbd2e"/>
        <circle cx="72" cy="28" r="7" fill="#27c93f"/>
        <text x="{width/2}" y="33" text-anchor="middle" class="mono dim" font-size="13">{esc(USERNAME)}@github ~ neofetch</text>
        <line x1="24" y1="46" x2="{width-24}" y2="46" stroke="#1f2937"/>
        """
    )

    ax, ay = 40, top_pad
    for i, line in enumerate(ascii_art):
        svg_parts.append(
            f'<text x="{ax}" y="{ay + i*line_h}" class="mono art" font-size="15" xml:space="preserve">{esc(line)}</text>'
        )

    kx, ky = 430, top_pad
    svg_parts.append(
        f'<text x="{kx}" y="{ky}" class="mono title" font-size="20">{esc(name)}</text>'
    )
    svg_parts.append(
        f'<text x="{kx}" y="{ky+22}" class="mono dim" font-size="13">{esc(bio)}</text>'
    )
    svg_parts.append(f'<line x1="{kx}" y1="{ky+34}" x2="{width-40}" y2="{ky+34}" stroke="#1f2937"/>')

    for i, (k, v) in enumerate(rows):
        y = ky + 60 + i * line_h
        svg_parts.append(f'<text x="{kx}" y="{y}" class="mono key" font-size="14">{esc(k)}</text>')
        svg_parts.append(f'<text x="{kx+150}" y="{y}" class="mono val" font-size="14">{esc(v)}</text>')

    # color swatch row like real neofetch
    swatch_y = ky + 60 + len(rows) * line_h + 16
    colors = ["#0b0f14", "#ff5f56", "#27c93f", "#ffbd2e", "#00d4ff", "#a78bfa", "#00ff9d", "#cbd5e1"]
    for i, c in enumerate(colors):
        svg_parts.append(f'<rect x="{kx + i*26}" y="{swatch_y}" width="22" height="14" fill="{c}"/>')

    svg_parts.append(
        f'<text x="24" y="{height-16}" class="mono dim" font-size="11">generated {datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")} — auto-refreshed daily via GitHub Actions</text>'
    )
    svg_parts.append("</svg>")

    svg = "\n".join(svg_parts)

    os.makedirs("assets", exist_ok=True)
    with open("assets/neofetch.svg", "w") as f:
        f.write(svg)

    print("Wrote assets/neofetch.svg")


if __name__ == "__main__":
    main()
