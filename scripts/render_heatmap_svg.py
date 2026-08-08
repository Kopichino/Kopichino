# scripts/render_heatmap_svg.py
import json

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
BOX, GAP = 11, 3

def render(data_path="data/contributions.json", out_path="contrib-heatmap.svg"):
    with open(data_path) as f:
        data = json.load(f)

    days = data["days"]
    weeks = [days[i:i + 7] for i in range(0, len(days), 7)]

    width = len(weeks) * (BOX + GAP) + 40
    height = 7 * (BOX + GAP) + 60

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="monospace" font-size="12">',
        '<rect width="100%" height="100%" fill="transparent"/>',
    ]

    for w_idx, week in enumerate(weeks):
        for d_idx, day in enumerate(week):
            x = 20 + w_idx * (BOX + GAP)
            y = 20 + d_idx * (BOX + GAP)
            color = PALETTE[min(day["level"], 5)]
            delay = (w_idx + d_idx) * 0.01
            svg.append(
                f'<rect x="{x}" y="{y}" width="{BOX}" height="{BOX}" rx="2" '
                f'fill="{color}" opacity="0">'
                f'<animate attributeName="opacity" from="0" to="1" '
                f'begin="{delay}s" dur="0.3s" fill="freeze"/>'
                f'</rect>'
            )

    footer_y = height - 15
    svg.append(
        f'<text x="20" y="{footer_y}" fill="#8b949e">'
        f'{data["total_contributions"]} contributions in the last year</text>'
    )
    svg.append('</svg>')

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Saved {out_path}")

if __name__ == "__main__":
    render()