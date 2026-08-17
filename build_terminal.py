#!/usr/bin/env python3
"""Generate assets/profile-terminal.svg — the neural-lab dossier card.

Regenerate after editing the DOSSIER / FOCUS constants:
    python build_terminal.py
"""
import random

W, H = 1180, 720

# ── neural network geometry (left panel) ────────────────────────────────────
LAYERS = [
    (96,  [168, 228, 288, 348, 408]),   # input
    (188, [150, 210, 270, 330, 390, 450]),
    (280, [186, 246, 306, 366]),
    (368, [246, 306]),
]

def edges():
    out = []
    random.seed(7)
    for (x1, ys1), (x2, ys2) in zip(LAYERS, LAYERS[1:]):
        for y1 in ys1:
            for y2 in ys2:
                op = round(random.uniform(0.07, 0.30), 3)
                out.append(f'    <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#94e2d5" stroke-opacity="{op}"/>')
    return "\n".join(out)

def nodes():
    out = []
    for li, (x, ys) in enumerate(LAYERS):
        for ni, y in enumerate(ys):
            delay = round(0.15 * li + 0.06 * ni, 2)
            fill = "#94e2d5" if li == len(LAYERS) - 1 else "#181825"
            out.append(
                f'    <circle cx="{x}" cy="{y}" r="7" fill="{fill}" stroke="#94e2d5" stroke-opacity=".75">'
                f'<animate attributeName="r" values="7;8.6;7" dur="3.4s" begin="{delay}s" repeatCount="indefinite"/>'
                f'<animate attributeName="stroke-opacity" values=".75;1;.75" dur="3.4s" begin="{delay}s" repeatCount="indefinite"/>'
                f'</circle>'
            )
    return "\n".join(out)

def pulses():
    """Signal packets travelling along a few sampled paths."""
    random.seed(11)
    out = []
    for i in range(7):
        path = []
        for x, ys in LAYERS:
            path.append((x, random.choice(ys)))
        d = "M" + " L".join(f"{x} {y}" for x, y in path)
        out.append(
            f'    <circle r="3.2" fill="#89dceb">'
            f'<animateMotion path="{d}" dur="{2.6 + i * 0.35:.2f}s" begin="{i * 0.4:.2f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;1;1;0" dur="{2.6 + i * 0.35:.2f}s" begin="{i * 0.4:.2f}s" repeatCount="indefinite"/>'
            f'</circle>'
        )
    return "\n".join(out)

# ── right panel content ─────────────────────────────────────────────────────
DOSSIER = [
    ("identity", "Nourhan Emad"),
    ("role",     "AI Engineer · Deep Learning"),
    ("origin",   "Egypt"),
    ("runtime",  "PyTorch · TensorFlow · scikit-learn"),
    ("status",   "Training · evaluating · shipping"),
]

FOCUS = [
    ("Deep Learning",        "Time-Series Regression"),
    ("Speech &amp; Audio Models", "Imbalanced Data"),
    ("Classical ML",         "Feature Engineering"),
]

BUILDING = [
    ("project",  "nasam"),
    ("position", "Author &amp; Maintainer"),
    ("purpose",  "Breath-sound disease detection · Wav2Vec2"),
]

GRID = [
    ("mail", "nourhanemadenan11111@gmail.com", "stack", "Python"),
    ("in",   "nourhan-emad",                   "field", "Medical AI"),
]


def dossier_rows():
    out, y = [], 151
    for i, (k, v) in enumerate(DOSSIER):
        out.append(f'''  <g class="row r{i + 2}">
    <text x="476" y="{y}" class="dim">[+]</text>
    <text x="508" y="{y}" class="key">{k}</text>
    <text x="640" y="{y}" class="value">{v}</text>
  </g>''')
        y += 27
    return "\n".join(out)


def focus_rows():
    out, y = [], 334
    for i, (a, b) in enumerate(FOCUS):
        out.append(f'''  <g class="row r{i + 7}">
    <text x="476" y="{y}" class="dim">0{i + 1} /</text>
    <text x="530" y="{y}" class="value">{a}</text>
    <text x="762" y="{y}" class="dim">0{i + 4} /</text>
    <text x="816" y="{y}" class="value">{b}</text>
  </g>''')
        y += 27
    return "\n".join(out)


def building_rows():
    out, y = [], 463
    for i, (k, v) in enumerate(BUILDING):
        out.append(f'''  <g class="row r{i + 8}">
    <text x="476" y="{y}" class="key">{k}</text>
    <text x="610" y="{y}" class="value">{v}</text>
  </g>''')
        y += 27
    return "\n".join(out)


def grid_rows():
    out, y = [], 592
    for i, (k1, v1, k2, v2) in enumerate(GRID):
        out.append(f'''  <g class="row r{i + 10}">
    <text x="476" y="{y}" class="key">{k1}</text>
    <text x="535" y="{y}" class="value">{v1}</text>
    <text x="852" y="{y}" class="key">{k2}</text>
    <text x="912" y="{y}" class="value">{v2}</text>
  </g>''')
        y += 27
    return "\n".join(out)


SVG = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
  <title id="title">Nourhan Emad — AI engineer dossier</title>
  <desc id="desc">Terminal-inspired profile card for Nourhan Emad, an AI engineer working on deep learning, speech and audio models, and medical machine learning.</desc>

  <defs>
    <linearGradient id="frame" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#94e2d5">
        <animate attributeName="stop-color" values="#94e2d5;#89dceb;#a6e3a1;#94e2d5" dur="10s" repeatCount="indefinite"/>
      </stop>
      <stop offset=".52" stop-color="#89b4fa"/>
      <stop offset="1" stop-color="#6c7086">
        <animate attributeName="stop-color" values="#6c7086;#94e2d5;#89b4fa;#6c7086" dur="10s" repeatCount="indefinite"/>
      </stop>
    </linearGradient>

    <radialGradient id="background" cx="22%" cy="12%" r="105%">
      <stop offset="0" stop-color="#1f2335"/>
      <stop offset=".48" stop-color="#181825"/>
      <stop offset="1" stop-color="#11111b"/>
    </radialGradient>

    <radialGradient id="netGlow">
      <stop offset="0" stop-color="#94e2d5" stop-opacity=".20"/>
      <stop offset=".55" stop-color="#89b4fa" stop-opacity=".07"/>
      <stop offset="1" stop-color="#11111b" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#94e2d5" stop-opacity="0"/>
      <stop offset=".48" stop-color="#94e2d5" stop-opacity=".03"/>
      <stop offset=".5" stop-color="#89dceb" stop-opacity=".30"/>
      <stop offset=".52" stop-color="#94e2d5" stop-opacity=".03"/>
      <stop offset="1" stop-color="#94e2d5" stop-opacity="0"/>
    </linearGradient>

    <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="1" fill="#94e2d5" opacity=".022"/>
    </pattern>

    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="5" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>

    <style>
      text, tspan {{ white-space: pre; }}
      .mono {{ font-family: "IBM Plex Mono", "SFMono-Regular", Consolas, "Liberation Mono", monospace; }}
      .label {{ font: 600 11px "IBM Plex Mono", "SFMono-Regular", Consolas, monospace; fill: #a6adc8; letter-spacing: 2.2px; }}
      .titlebar {{ font: 12px "IBM Plex Mono", "SFMono-Regular", Consolas, monospace; fill: #6c7086; letter-spacing: .5px; }}
      .key {{ font: 600 14px "IBM Plex Mono", "SFMono-Regular", Consolas, monospace; fill: #94e2d5; }}
      .value {{ font: 14px "IBM Plex Mono", "SFMono-Regular", Consolas, monospace; fill: #cdd6f4; }}
      .dim {{ font: 13px "IBM Plex Mono", "SFMono-Regular", Consolas, monospace; fill: #6c7086; }}
      .green {{ fill: #a6e3a1; }}
      .teal {{ fill: #94e2d5; }}
      .row {{ animation: reveal .45s ease both; }}
      .r1 {{ animation-delay: .25s; }} .r2 {{ animation-delay: .34s; }}
      .r3 {{ animation-delay: .43s; }} .r4 {{ animation-delay: .52s; }}
      .r5 {{ animation-delay: .61s; }} .r6 {{ animation-delay: .70s; }}
      .r7 {{ animation-delay: .79s; }} .r8 {{ animation-delay: .88s; }}
      .r9 {{ animation-delay: .97s; }} .r10 {{ animation-delay: 1.06s; }}
      .r11 {{ animation-delay: 1.15s; }} .r12 {{ animation-delay: 1.24s; }}
      .cursor {{ animation: blink 1.05s steps(1) infinite; }}
      .pulse {{ animation: pulse 2.2s ease-in-out infinite; }}
      @keyframes reveal {{ from {{ opacity: 0; transform: translateX(10px); }} to {{ opacity: 1; transform: translateX(0); }} }}
      @keyframes blink {{ 0%,49% {{ opacity: 1; }} 50%,100% {{ opacity: 0; }} }}
      @keyframes pulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: .35; }} }}
    </style>
  </defs>

  <rect width="{W}" height="{H}" rx="19" fill="url(#background)"/>
  <rect width="{W}" height="{H}" rx="19" fill="url(#scanlines)"/>
  <rect x="1.5" y="1.5" width="{W - 3}" height="{H - 3}" rx="18" fill="none" stroke="url(#frame)" stroke-width="2"/>

  <!-- terminal chrome -->
  <path d="M2 19A17 17 0 0 1 19 2h1142a17 17 0 0 1 17 17v26H2z" fill="#181825" fill-opacity=".9"/>
  <line x1="2" y1="45" x2="1178" y2="45" stroke="#313244"/>
  <circle cx="24" cy="23" r="5" fill="#f38ba8"/>
  <circle cx="44" cy="23" r="5" fill="#f9e2af"/>
  <circle cx="64" cy="23" r="5" fill="#a6e3a1"/>
  <text x="590" y="27" text-anchor="middle" class="titlebar">nourhan@lab:~$ python -m dossier --verbose</text>
  <circle cx="1086" cy="23" r="4" fill="#a6e3a1" class="pulse"/>
  <text x="1098" y="27" class="titlebar green">KERNEL UP</text>

  <!-- panels -->
  <rect x="18" y="63" width="422" height="595" rx="14" fill="#11111b" fill-opacity=".42" stroke="#45475a"/>
  <rect x="456" y="63" width="706" height="595" rx="14" fill="#11111b" fill-opacity=".42" stroke="#45475a"/>
  <text x="38" y="84" class="label">NETWORK.SIGNATURE</text>
  <text x="476" y="84" class="label">ENGINEER.DOSSIER</text>

  <!-- left: neural network -->
  <ellipse cx="232" cy="300" rx="200" ry="180" fill="url(#netGlow)"/>
  <text x="232" y="336" text-anchor="middle" class="mono" font-size="118" font-weight="700" fill="#94e2d5" opacity=".07" letter-spacing="-6">知能</text>

  <g>
{edges()}
  </g>
  <g>
{nodes()}
  </g>
  <g>
{pulses()}
  </g>

  <g class="mono" font-size="11" fill="#6c7086">
    <text x="42" y="126">LAYERS: 4</text>
    <text x="330" y="126">EPOCH: ∞</text>
    <text x="42" y="462">LOSS: ↓ CONVERGING</text>
    <text x="352" y="462" class="green">FIT</text>
  </g>

  <text x="232" y="497" text-anchor="middle" class="mono" font-size="25" font-weight="700" fill="#cdd6f4" letter-spacing="4">NOURHAN EMAD</text>
  <text x="232" y="519" text-anchor="middle" class="mono" font-size="11" fill="#6c7086" letter-spacing="3">AI · DEEP LEARNING</text>

  <g transform="translate(42 536)">
    <rect width="376" height="106" rx="9" fill="#181825" stroke="#313244"/>
    <text x="16" y="26" class="mono" font-size="12"><tspan class="green">nourhan@lab</tspan><tspan fill="#6c7086">:</tspan><tspan class="teal">~</tspan><tspan fill="#6c7086">$ cat approach.txt</tspan></text>
    <text x="16" y="53" class="mono" font-size="13" fill="#cdd6f4">Models are hypotheses. Metrics</text>
    <text x="16" y="74" class="mono" font-size="13" fill="#cdd6f4">are how you cross-examine them.</text>
    <text x="16" y="95" class="mono" font-size="12" fill="#a6adc8">confusion matrix &gt; accuracy score</text>
    <rect x="345" y="83" width="8" height="14" fill="#94e2d5" class="cursor"/>
  </g>

  <!-- right: dossier -->
  <g class="row r1">
    <text x="476" y="119" class="key">nourhan@lab</text>
    <line x1="596" y1="114" x2="1138" y2="114" stroke="#313244"/>
  </g>
{dossier_rows()}

  <g class="row r6">
    <text x="476" y="303" class="key green">:: focus</text>
    <line x1="558" y1="298" x2="1138" y2="298" stroke="#313244"/>
  </g>
{focus_rows()}

  <g class="row r7">
    <text x="476" y="432" class="key green">:: building</text>
    <line x1="582" y1="427" x2="1138" y2="427" stroke="#313244"/>
  </g>
{building_rows()}

  <g class="row r9">
    <text x="476" y="561" class="key green">:: grid</text>
    <line x1="548" y1="556" x2="1138" y2="556" stroke="#313244"/>
  </g>
{grid_rows()}

  <!-- live scan and footer -->
  <rect x="2" y="-150" width="1176" height="180" fill="url(#scan)" pointer-events="none">
    <animate attributeName="y" values="-180;720" dur="7s" repeatCount="indefinite"/>
  </rect>
  <text x="24" y="694" class="titlebar">SIGNAL OVER NOISE · GRADIENTS DESCENDING</text>
  <text x="1156" y="694" text-anchor="end" class="titlebar teal">NOURHAN EMAD / 知能</text>
</svg>
'''

if __name__ == "__main__":
    import pathlib
    out = pathlib.Path(__file__).parent / "assets" / "profile-terminal.svg"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(SVG)
    print(f"wrote {out} ({len(SVG)} bytes)")
