#!/usr/bin/env python3
"""
Generate an ultra-clean, animated Neofetch-style system info card SVG.
Matches the 840 x 884 canvas of berkay-ascii.svg for a pixel-perfect side-by-side layout.
"""
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "info-card.svg")

W = 840
H = 884
PAD = 28
TITLEBAR_H = 30
FRAME = "#30363d"
BG = "#0d1117"
BG2 = "#111722"
MUTED = "#7d8590"
LABEL_COLOR = "#58a6ff"   # Sleek terminal blue/cyan for keys
VAL_COLOR = "#e6edf3"     # Crisp terminal text for values
ACCENT_GREEN = "#39d353"
ACCENT_GOLD = "#d29922"
ACCENT_CYAN = "#38bdf8"
ACCENT_PURPLE = "#bc8cff"

# Neofetch data items
items = [
    ("OS", "Shaz OS x86_64 / Linux", ACCENT_CYAN),
    ("Host", "GitHub (@berkaysahin-dev)", VAL_COLOR),
    ("Role", "Full-Stack Engineer & Agency Founder", ACCENT_GREEN),
    ("Company", "Shaz Agency", ACCENT_GOLD),
    ("Primary", "TypeScript (198+ MB Codebase)", ACCENT_CYAN),
    ("Languages", "TypeScript · JavaScript · Python · Rust · Dart", VAL_COLOR),
    ("Stack", "React · Next.js · Node.js · Flutter · Tailwind", VAL_COLOR),
    ("E-Commerce", "Shopify Liquid · Storefront Engines", VAL_COLOR),
    ("Focus", "High-End Web & Mobile Apps, AI Systems", VAL_COLOR),
    ("Agency", "hello@shazagency.com", ACCENT_PURPLE),
    ("Direct", "iletisim@berkaysahin.net", ACCENT_GREEN),
]

color_palette = [
    "#484f58", "#ff7b72", "#3fb950", "#d29922", "#58a6ff", "#bc8cff", "#39c5cf", "#f0f6fc"
]
bright_palette = [
    "#6e7681", "#ffa198", "#56d364", "#e3b341", "#79c0ff", "#d2a8ff", "#56e3ec", "#ffffff"
]

css = """
@keyframes fadeIn {
  0%   { opacity: 0; transform: translateY(8px); }
  100% { opacity: 1; transform: translateY(0); }
}
.row { opacity: 0; animation: fadeIn 0.4s ease-out forwards; }
@media (prefers-reduced-motion: reduce) {
  .row { opacity: 1 !important; transform: none !important; animation: none !important; }
}
""".strip()

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    f'<style>{css}</style>',
    '<defs>'
    f'<linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
    '</linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#ibg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}" stroke-width="1"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]

# Titlebar buttons
for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')

parts.append(
    f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" text-anchor="middle">'
    'berkay@github: ~$ neofetch</text>'
)

# Header: berkay@shaz-agency
header_y = TITLEBAR_H + 48
parts.append('<g class="row" style="animation-delay: 0.15s">')
parts.append(f'<text x="{PAD}" y="{header_y}" font-size="22" font-weight="700" fill="{ACCENT_CYAN}">'
             f'berkay<tspan fill="{MUTED}">@</tspan><tspan fill="{ACCENT_GREEN}">shaz-agency</tspan></text>')
parts.append(f'<line x1="{PAD}" y1="{header_y + 12}" x2="{W - PAD}" y2="{header_y + 12}" stroke="{FRAME}" stroke-dasharray="4 4"/>')
parts.append('</g>')

# Neofetch rows
curr_y = header_y + 44
line_height = 44
label_w = 175

for idx, (label, val, val_col) in enumerate(items):
    delay = 0.25 + idx * 0.14
    safe_label = html.escape(label)
    safe_val = html.escape(val)
    parts.append(f'<g class="row" style="animation-delay: {delay:.2f}s">')
    parts.append(f'<text x="{PAD}" y="{curr_y}" font-size="18" font-weight="700" fill="{LABEL_COLOR}">'
                 f'{safe_label}:</text>')
    parts.append(f'<text x="{PAD + label_w}" y="{curr_y}" font-size="18" fill="{val_col}">'
                 f'{safe_val}</text>')
    parts.append('</g>')
    curr_y += line_height

# Divider before color bars
curr_y += 10
parts.append(f'<line x1="{PAD}" y1="{curr_y}" x2="{W - PAD}" y2="{curr_y}" stroke="{FRAME}" stroke-opacity="0.5"/>')
curr_y += 35

# Color pills (Standard & Bright)
box_w = 40
box_h = 24
box_gap = 10
start_x = PAD

parts.append('<g class="row" style="animation-delay: 1.8s">')
for i, col in enumerate(color_palette):
    bx = start_x + i * (box_w + box_gap)
    parts.append(f'<rect x="{bx}" y="{curr_y}" width="{box_w}" height="{box_h}" rx="4" fill="{col}"/>')
curr_y += box_h + 8
for i, col in enumerate(bright_palette):
    bx = start_x + i * (box_w + box_gap)
    parts.append(f'<rect x="{bx}" y="{curr_y}" width="{box_w}" height="{box_h}" rx="4" fill="{col}"/>')
parts.append('</g>')

# Footer terminal prompt
footer_y = H - 24
parts.append('<g class="row" style="animation-delay: 2.1s">')
parts.append(f'<text x="{PAD}" y="{footer_y}" font-size="14" fill="{MUTED}">'
             f'berkay@github:~$ <tspan fill="{ACCENT_GREEN}">uptime</tspan> &#8212; Building the future of digital software</text>')
parts.append('</g>')

parts.append('</svg>')
svg = "".join(parts)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print(f"wrote {OUT}: {W} x {H}, {len(svg)} bytes")
