# scripts/make_ascii_svg.py
from PIL import Image

RAMP = " .`:-=+*cs#%@"  # bright (sparse) -> dark (dense); leading space = blank
COLS, ROWS = 100, 53
CHAR_W, CHAR_H = 8, 14
FILL_COLOR = "#c9d1d9"

def image_to_ascii(path):
    img = Image.open(path).convert("L").resize((COLS, ROWS))
    pixels = list(img.getdata())
    grid = []
    for y in range(ROWS):
        row = []
        for x in range(COLS):
            brightness = pixels[y * COLS + x]
            idx = int((brightness / 255) * (len(RAMP) - 1))
            row.append(RAMP[idx])
        grid.append("".join(row))
    return grid

def build_svg(grid, out_path="avi-ascii.svg"):
    width = COLS * CHAR_W
    height = ROWS * CHAR_H
    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" font-family="monospace" font-size="{CHAR_H}">',
        f'<rect width="100%" height="100%" fill="transparent"/>'
    ]

    for row_idx, row in enumerate(grid):
        escaped = (row.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
        y = (row_idx + 1) * CHAR_H
        clip_id = f"clip{row_idx}"
        delay = row_idx * 0.03

        svg_lines.append(f'<clipPath id="{clip_id}">')
        svg_lines.append(f'  <rect x="0" y="{y - CHAR_H}" width="0" height="{CHAR_H}">')
        svg_lines.append(
            f'    <animate attributeName="width" from="0" to="{width}" '
            f'begin="{delay}s" dur="0.4s" fill="freeze" />'
        )
        svg_lines.append('  </rect>')
        svg_lines.append('</clipPath>')

        svg_lines.append(
            f'<text x="0" y="{y}" fill="{FILL_COLOR}" clip-path="url(#{clip_id})" '
            f'xml:space="preserve">{escaped}</text>'
        )

    svg_lines.append('</svg>')
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
    print(f"Saved {out_path}")

if __name__ == "__main__":
    grid = image_to_ascii("source-prepped.png")
    build_svg(grid)