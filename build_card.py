#!/usr/bin/env python3
"""Generate assets/profile-card.svg — the ML metrics dashboard.

Every number in here is real and traceable to one of the repos:
  * model leaderboard  -> digger/notebooks/model_comparison.ipynb
  * accuracy by project-> each project's notebook comparison table
Do not invent figures. If a number changes, change it here and rerun:

    python build_card.py
"""
import pathlib

W, H = 1180, 640

# ── palette — GitHub dark theme tokens, so the card blends into the page ──
SURFACE   = "#0d1117"   # GitHub dark canvas.default
PANEL     = "#161b22"   # canvas.subtle
LINE      = "#30363d"   # border.default
INK       = "#e6edf3"   # fg.default
INK_2     = "#c9d1d9"   # fg.subtle-ish
INK_MUTED = "#8b949e"   # fg.muted
BLUE      = "#3987e5"   # categorical slot 1
ORANGE    = "#d95926"   # slot 2
AQUA      = "#199e70"   # slot 3

# ── data ───────────────────────────────────────────────────────────────────
TILES = [
    ("5",      "PROJECTS SHIPPED"),
    ("0.99",   "BEST R²"),
    ("98.2%",  "BEST ACCURACY"),
    ("10",     "FORECAST TARGETS"),
]

# digger — mean R² (%) across 10 commodity targets, held-out split
LEADERBOARD = [
    ("KNN Regressor",     98.97),
    ("SVM",               98.10),
    ("XGBoost",           98.05),
    ("Decision Tree",     96.00),
    ("Random Forest",     96.00),
    ("Linear Regression", 94.12),
]

# best test accuracy (%) per classification project
BY_PROJECT = [
    ("breast-cancer-prediction",  98.2, BLUE),
    ("machine-failure-prediction", 97.4, AQUA),
    ("liver-disease-prediction",   70.2, ORANGE),
]

STACK = "PyTorch · TensorFlow · scikit-learn · XGBoost · pandas · librosa"
FOCUS = ["Deep learning", "Speech & audio", "Time-series forecasting", "Imbalanced data"]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ── stat tiles ─────────────────────────────────────────────────────────────
def tiles():
    out, x, w, gap = [], 40, 263, 16
    for i, (value, label) in enumerate(TILES):
        tx = x + i * (w + gap)
        out.append(f'''  <g class="fade" style="animation-delay:{.10 + i * .07:.2f}s">
    <rect x="{tx}" y="114" width="{w}" height="92" rx="10" fill="{PANEL}" stroke="{LINE}"/>
    <rect x="{tx}" y="114" width="3" height="92" rx="1.5" fill="{BLUE}"/>
    <text x="{tx + 22}" y="163" class="stat">{esc(value)}</text>
    <text x="{tx + 22}" y="186" class="tile-label">{esc(label)}</text>
  </g>''')
    return "\n".join(out)


# ── left panel: dot plot (narrow value band — bars would need a cut axis) ───
def leaderboard():
    px, py, pw, ph = 40, 228, 620, 300
    x0, x1 = px + 188, px + pw - 74          # plot band
    lo, hi = 92.0, 100.0                      # explicit, labelled axis range
    sx = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)
    out = [f'''  <rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="12" fill="{PANEL}" stroke="{LINE}"/>
  <text x="{px + 22}" y="{py + 32}" class="panel-title">Model leaderboard</text>
  <text x="{px + 22}" y="{py + 52}" class="panel-sub">digger &#183; mean R&#178; across 10 commodity targets</text>''']

    # gridlines + axis ticks
    for v in (92, 94, 96, 98, 100):
        gx = sx(v)
        out.append(f'  <line x1="{gx:.1f}" y1="{py + 74}" x2="{gx:.1f}" y2="{py + 250}" stroke="{LINE}"/>')
        out.append(f'  <text x="{gx:.1f}" y="{py + 272}" class="axis" text-anchor="middle">{v}</text>')
    out.append(f'  <text x="{(x0 + x1) / 2:.0f}" y="{py + 290}" class="axis-title" text-anchor="middle">mean R&#178; (%)</text>')

    for i, (name, val) in enumerate(LEADERBOARD):
        y = py + 96 + i * 27
        cx = sx(val)
        out.append(f'''  <g class="fade" style="animation-delay:{.45 + i * .06:.2f}s">
    <text x="{px + 172}" y="{y + 4}" class="row-label" text-anchor="end">{esc(name)}</text>
    <line x1="{x0}" y1="{y}" x2="{cx:.1f}" y2="{y}" stroke="{BLUE}" stroke-opacity=".30" stroke-width="2"/>
    <circle cx="{cx:.1f}" cy="{y}" r="5.5" fill="{BLUE}" stroke="{PANEL}" stroke-width="2"/>
    <text x="{cx + 16:.1f}" y="{y + 4}" class="value">{val:.2f}</text>
  </g>''')
    return "\n".join(out)


# ── right panel: zero-baseline bars, one per project ───────────────────────
def by_project():
    px, py, pw, ph = 676, 228, 464, 300
    x0 = px + 22
    x1 = px + pw - 30
    sx = lambda v: x0 + v / 100 * (x1 - x0)
    out = [f'''  <rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="12" fill="{PANEL}" stroke="{LINE}"/>
  <text x="{px + 22}" y="{py + 32}" class="panel-title">Best test accuracy by project</text>
  <text x="{px + 22}" y="{py + 52}" class="panel-sub">classification repos &#183; held-out test split</text>''']

    for i, (name, val, color) in enumerate(BY_PROJECT):
        y = py + 84 + i * 62
        bw = sx(val) - x0
        out.append(f'''  <g class="fade" style="animation-delay:{.55 + i * .09:.2f}s">
    <text x="{x0}" y="{y}" class="row-label">{esc(name)}</text>
    <rect x="{x0}" y="{y + 10}" width="{x1 - x0}" height="14" rx="7" fill="{LINE}" fill-opacity=".55"/>
    <rect x="{x0}" y="{y + 10}" width="{bw:.1f}" height="14" rx="7" fill="{color}">
      <animate attributeName="width" from="0" to="{bw:.1f}" dur=".9s" begin="{.55 + i * .09:.2f}s" fill="freeze"/>
    </rect>
    <text x="{x1 + 8}" y="{y + 22}" class="value">{val:.1f}</text>
  </g>''')

    out.append(f'''  <line x1="{x0}" y1="{py + 258}" x2="{x1}" y2="{py + 258}" stroke="{LINE}"/>
  <text x="{x0}" y="{py + 280}" class="axis">0</text>
  <text x="{x1}" y="{py + 280}" class="axis" text-anchor="end">100%</text>
  <text x="{(x0 + x1) / 2:.0f}" y="{py + 280}" class="axis" text-anchor="middle">accuracy</text>''')
    return "\n".join(out)


# ── bottom strip ───────────────────────────────────────────────────────────
def footer():
    out = [f'  <line x1="40" y1="556" x2="{W - 40}" y2="556" stroke="{LINE}"/>']
    x = 40
    for i, f in enumerate(FOCUS):
        w = 15 + len(f) * 7.4
        out.append(f'''  <g class="fade" style="animation-delay:{.75 + i * .05:.2f}s">
    <rect x="{x:.0f}" y="580" width="{w:.0f}" height="28" rx="14" fill="none" stroke="{LINE}"/>
    <text x="{x + w / 2:.0f}" y="598" class="chip" text-anchor="middle">{esc(f)}</text>
  </g>''')
        x += w + 10
    out.append(f'  <text x="{W - 40}" y="598" class="stack" text-anchor="end">{esc(STACK)}</text>')
    return "\n".join(out)


SVG = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
  <title id="t">Nourhan Emad — AI engineer</title>
  <desc id="d">Dashboard card for Nourhan Emad, an AI engineer. Five projects shipped, best R-squared 0.99, best accuracy 98.2 percent, ten forecast targets. Model leaderboard for the digger project: KNN 98.97, SVM 98.10, XGBoost 98.05, Decision Tree 96.00, Random Forest 96.00, Linear Regression 94.12 mean R-squared. Best test accuracy by project: breast cancer 98.2, machine failure 97.4, liver disease 70.2 percent.</desc>

  <defs>
    <style>
      text {{ font-family: "Inter", "Segoe UI", -apple-system, "Helvetica Neue", Arial, sans-serif; }}
      .name       {{ font-size: 34px; font-weight: 700; fill: {INK}; letter-spacing: -.5px; }}
      .role       {{ font-size: 15px; fill: {INK_2}; }}
      .meta       {{ font-size: 13px; fill: {INK_MUTED}; }}
      .stat       {{ font-size: 34px; font-weight: 650; fill: {INK}; letter-spacing: -.5px; }}
      .tile-label {{ font-size: 10.5px; fill: {INK_MUTED}; letter-spacing: 1.4px; font-weight: 600; }}
      .panel-title{{ font-size: 16px; font-weight: 650; fill: {INK}; }}
      .panel-sub  {{ font-size: 12.5px; fill: {INK_MUTED}; }}
      .row-label  {{ font-size: 13px; fill: {INK_2}; }}
      .value      {{ font-size: 13px; font-weight: 650; fill: {INK}; font-variant-numeric: tabular-nums; }}
      .axis       {{ font-size: 11px; fill: {INK_MUTED}; }}
      .axis-title {{ font-size: 11px; fill: {INK_MUTED}; letter-spacing: .4px; }}
      .chip       {{ font-size: 12px; fill: {INK_2}; }}
      .stack      {{ font-size: 12.5px; fill: {INK_MUTED}; }}
      .fade       {{ animation: fade .5s ease both; }}
      @keyframes fade {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: none; }} }}
    </style>
  </defs>

  <rect width="{W}" height="{H}" rx="16" fill="{SURFACE}"/>

  <!-- header -->
  <g class="fade">
    <text x="40" y="60" class="name">Nourhan Emad</text>
    <text x="40" y="84" class="role">AI Engineer &#183; Deep learning, forecasting, predictive modelling</text>
    <text x="{W - 40}" y="60" class="meta" text-anchor="end">Egypt</text>
    <text x="{W - 40}" y="84" class="meta" text-anchor="end">github.com/nourhanemadenan</text>
  </g>

{tiles()}

{leaderboard()}

{by_project()}

{footer()}
</svg>
'''

if __name__ == "__main__":
    out = pathlib.Path(__file__).parent / "assets" / "profile-card.svg"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(SVG)
    print(f"wrote {out} ({len(SVG)} bytes)")
