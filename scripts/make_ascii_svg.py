#!/usr/bin/env python3
"""
Generate an animated ASCII terminal SVG from Berkay's profile logo.
Typing effect rasters row-by-row with an animated cursor.
Canvas size is 840 x 876 to match info-card.svg side-by-side.
"""
import html
import os
import sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "source-photo.png")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "berkay-ascii.svg")

# Target canvas sizing
ART_W_TARGET = 800
COLS = 110
CELL_W = ART_W_TARGET / COLS
CELL_H = CELL_W * 15 / 8
ROWS = round(COLS * 8 / 15)  # 59 rows
ART_W = COLS * CELL_W
ART_H = ROWS * CELL_H

PAD = 20
TITLEBAR_H = 30
STATUS_H = 30
CANVAS_W = int(ART_W + PAD * 2)  # 840
CANVAS_H = int(TITLEBAR_H + ART_H + STATUS_H + PAD)  # 876

# 1. Sample the logo
im = Image.open(SRC).convert("L")
bbox = im.getbbox()
cropped = im.crop(bbox) if bbox else im
cw, ch = cropped.size

# We give the logo ~24 rows in the vertical center
logo_rows = 24
logo_cols = 100
logo_resized = cropped.resize((logo_cols, logo_rows), Image.Resampling.LANCZOS)
px_logo = logo_resized.load()
ramp = " .`:-=+*cs#%@"

logo_lines = []
for y in range(logo_rows):
    line = []
    for x in range(logo_cols):
        lum = px_logo[x, y] / 255.0
        if lum <= 0.08:
            line.append(" ")
        else:
            idx = int(lum * (len(ramp) - 1))
            idx = max(0, min(len(ramp) - 1, idx))
            line.append(ramp[idx])
    logo_str = "".join(line)
    # Center within COLS
    pad_left = (COLS - logo_cols) // 2
    logo_lines.append(" " * pad_left + logo_str + " " * (COLS - logo_cols - pad_left))

# 2. Build complete terminal screen lines (59 rows)
def center_txt(text, width=COLS):
    return text.center(width)[:width]

def boxed_line(content, width=COLS):
    inner = content.center(width - 4)
    return f"/*{inner}*/"

all_rows = []

# Header section (Rows 0-9)
all_rows.append("/*" + "=" * (COLS - 4) + "*/")
all_rows.append(boxed_line("SYSTEM BOOT: SHAZ-OS // KERNEL v5.19"))
all_rows.append(boxed_line("BERKAY SAHIN  [FOUNDER & LEAD ENGINEER]"))
all_rows.append(boxed_line("SHAZ AGENCY  •  DIGITAL PRODUCT STUDIO"))
all_rows.append("/*" + "=" * (COLS - 4) + "*/")
all_rows.append(" " * COLS)
all_rows.append(center_txt(">>> MOUNTING IDENTIFIER ARTIFACT..."))
all_rows.append(" " * COLS)

# Logo section (Rows 10-33)
all_rows.extend(logo_lines)

# Footer / Specs section (Rows 34-58)
all_rows.append(" " * COLS)
all_rows.append(center_txt("<<< IDENTIFIER VERIFIED: BERKAY SAHIN >>>"))
all_rows.append(" " * COLS)
all_rows.append("/*" + "-" * (COLS - 4) + "*/")
all_rows.append(boxed_line("SPECIALTY : Full-Stack Web, Mobile Apps & AI Architectures"))
all_rows.append(boxed_line("STACK     : TypeScript · JavaScript · Python · Rust · Dart"))
all_rows.append(boxed_line("COMMERCE  : Shopify Liquid & High-Performance Storefronts"))
all_rows.append(boxed_line("ECOSYSTEM : Shaz Agency OS · Universal AI · Jarvis AI"))
all_rows.append("/*" + "-" * (COLS - 4) + "*/")
all_rows.append(" " * COLS)
all_rows.append(center_txt("[ STATUS: ALL SYSTEMS NOMINAL // READY FOR DEPLOYMENT ]"))
all_rows.append("/*" + "=" * (COLS - 4) + "*/")

# Ensure exact row count
while len(all_rows) < ROWS:
    all_rows.append(" " * COLS)
all_rows = all_rows[:ROWS]

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
TITLE_TEXT = "#7d8590"
INK = "#58a6ff"       # Neon cyan / terminal blue
ACCENT = "#7ee787"    # Terminal green
CURSOR = "#58a6ff"

ROW_DUR = 4.8 / ROWS
STAGGER = ROW_DUR

parts = []
parts.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
    f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">'
)
parts.append(
    '<defs>'
    f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
    '</linearGradient></defs>'
)

parts.append(f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="url(#bg)"/>')
parts.append(f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="12" fill="none" stroke="{FRAME}" stroke-width="1"/>')
parts.append(f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>')

for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')

parts.append(
    f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{TITLE_TEXT}" font-size="12" text-anchor="middle">'
    'berkay@github: ~$ ./portrait.sh</text>'
)

art_top = TITLEBAR_H + PAD * 0.35
font_size = CELL_H * 0.86

for ry, line in enumerate(all_rows):
    y = art_top + ry * CELL_H + CELL_H * 0.74
    row_y = art_top + ry * CELL_H
    delay = ry * STAGGER
    safe = html.escape(line)
    
    # Choose color: accent green for special status lines, cyan ink for everything else
    color = ACCENT if ("NOMINAL" in line or "VERIFIED" in line) else INK
    
    text = (
        f'<text xml:space="preserve" x="{PAD}" y="{y:.1f}" fill="{color}" '
        f'font-size="{font_size:.1f}" textLength="{ART_W}" lengthAdjust="spacing">{safe}</text>'
    )

    parts.append(
        f'<clipPath id="r{ry}"><rect x="{PAD}" y="{row_y:.1f}" height="{CELL_H}" width="0">'
        f'<animate attributeName="width" from="0" to="{ART_W}" begin="{delay:.3f}s" dur="{ROW_DUR:.2f}s" fill="freeze"/></rect></clipPath>'
    )
    parts.append(f'<g clip-path="url(#r{ry})">{text}</g>')
    parts.append(
        f'<rect y="{row_y+1:.1f}" width="{CELL_W}" height="{CELL_H-2}" fill="{CURSOR}" opacity="0">'
        f'<animate attributeName="x" from="{PAD}" to="{PAD+ART_W}" begin="{delay:.3f}s" dur="{ROW_DUR:.2f}s" fill="freeze"/>'
        f'<set attributeName="opacity" to="0.85" begin="{delay:.3f}s"/>'
        f'<set attributeName="opacity" to="0" begin="{delay+ROW_DUR:.3f}s"/></rect>'
    )

status_line_y = TITLEBAR_H + ART_H + PAD * 0.35
status_y = status_line_y + 19
parts.append(f'<line x1="0" y1="{status_line_y:.1f}" x2="{CANVAS_W}" y2="{status_line_y:.1f}" stroke="{FRAME}"/>')
parts.append(
    f'<text x="{PAD}" y="{status_y:.1f}" fill="{TITLE_TEXT}" font-size="13">'
    f'berkay@github:~$ whoami <tspan fill="{ACCENT}" font-weight="700">Berkay Şahin</tspan></text>'
)

status_chars = len("berkay@github:~$ whoami Berkay Şahin ")
parts.append(
    f'<rect x="{PAD + status_chars * 13 * 0.6:.1f}" y="{status_y-12:.1f}" width="8" height="14" fill="{ACCENT}">'
    '<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="1s" repeatCount="indefinite"/></rect>'
)

parts.append("</svg>")
svg = "".join(parts)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)

print(f"Generated {OUT} ({CANVAS_W}x{CANVAS_H}, {len(svg)} bytes)")
