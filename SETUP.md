# Setup Instructions (v2)

## 1. Create the special profile repo
GitHub only renders a README on your profile page if you have a repo with the
**exact same name as your username**.

1. github.com/new → name it `Dhanesh10war` → Public → initialize with a README
2. Clone it, then drop in everything from this package, keeping the folder structure:
   ```
   README.md
   SETUP.md
   scripts/generate_neofetch.py
   .github/workflows/neofetch.yml
   .github/workflows/metrics.yml
   .github/workflows/snake.yml   (optional, from the first version)
   ```

## 2. Enable Actions write access
Settings → Actions → General → Workflow permissions → **"Read and write permissions"** → Save.
(This lets the neofetch workflow commit the SVG back into your repo.)

## 3. Live neofetch card (`assets/neofetch.svg`)
This is a **custom script I wrote**, not a third-party badge — `scripts/generate_neofetch.py`
calls the GitHub REST API for your real repo count, stars, followers, top languages, and
account age, then renders an SVG terminal card from scratch.

- It runs automatically via `.github/workflows/neofetch.yml` (daily + on push)
- To test manually: Actions tab → "Generate Neofetch Card" → Run workflow
- First run may show 0s until the Action's `GITHUB_TOKEN` populates real numbers — that's normal,
  give it one run

## 4. 3D isometric analytics (`github-metrics.svg`)
Uses [lowlighter/metrics](https://github.com/lowlighter/metrics) — the `plugin_isocalendar` is
what renders your contribution calendar as an isometric 3D grid (this is the closest thing to a
"Skyline inside your README" that actually works as a live embed).

You need a **Personal Access Token** (the default `GITHUB_TOKEN` doesn't have enough scope for
the deeper analytics plugins):

1. github.com/settings/tokens → **Generate new token (classic)**
2. Scopes: `public_repo`, `read:user` (add `read:org` if you want org stats too)
3. Copy the token → your repo's **Settings → Secrets and variables → Actions → New repository secret**
   → name it `METRICS_TOKEN`, paste the value
4. Actions tab → "Analytics Metrics" → Run workflow manually once

This single workflow also gives you: language-usage breakdown, lines-of-code history graph,
coding "habits" (peak hours/days), and achievement badges — genuinely analytical, not decorative.

## 5. GitHub Skyline (the real interactive 3D model)
Being fully honest: a static README **cannot** embed live WebGL — GitHub strips scripts/iframes
from README rendering, so true drag-to-orbit 3D only exists on GitHub's own site, not inside the
page itself. What you get in the README is a link + badge to your live Skyline. If you want a
visual preview embedded too:

1. Visit `https://skyline.github.com/Dhanesh10war/2026`
2. Screenshot or export the render
3. Save it as `assets/skyline.png` in the repo
4. Uncomment the `<img src="assets/skyline.png">` line in `README.md`

## 6. Fill in placeholder links
Swap these in `README.md`:
- LinkedIn badge → your profile URL
- Portfolio badge → your deployed site
- Email badge → `mailto:you@example.com`

## What's genuinely new here vs. the first version
| Piece | Before | Now |
|---|---|---|
| Identity card | Generic stats widget | Custom-coded neofetch terminal card, real API data, your own script |
| 3D visual | Snake animation only | + isometric 3D contribution calendar (metrics) + link to true WebGL Skyline |
| Analytics | Stats/streak/langs | + lines-of-code history, coding habits, achievement tier badges |
| Honesty | — | Clearly marked which parts are live-embeddable vs. link-out only (WebGL limitation) |
