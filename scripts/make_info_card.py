# scripts/make_info_card.py
import os

LINES = [
    ("Now", "Engineering intelligent systems with AI"),
    ("Focus", "GenAI · RAG · Computer Vision · Deep Learning"),
    ("Stack", "Python · PyTorch · React · FastAPI · AWS"),
    ("Highlights", "VMedithon Top 5 · AI Research · Shipped Projects"),
]

def build_card(out_path="info-card.svg"):
    static = os.environ.get("STATIC") == "1"
    width, height = 550, 40 + len(LINES) * 34
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="monospace" font-size="15">',
        '<rect width="100%" height="100%" rx="8" fill="#0d1117" stroke="#30363d"/>',
        '<rect width="100%" height="26" rx="8" fill="#161b22"/>',
        '<circle cx="16" cy="13" r="5" fill="#ff5f56"/>',
        '<circle cx="34" cy="13" r="5" fill="#ffbd2e"/>',
        '<circle cx="52" cy="13" r="5" fill="#27c93f"/>',
        '<text x="70" y="18" fill="#8b949e">neofetch</text>',
    ]

    for i, (key, val) in enumerate(LINES):
        y = 60 + i * 34
        delay = i * 0.15
        anim = "" if static else (
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay}s" '
            f'dur="0.4s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" '
            f'from="-10,0" to="0,0" begin="{delay}s" dur="0.4s" fill="freeze"/>'
        )
        opacity = "1" if static else "0"
        svg.append(
            f'<g opacity="{opacity}">'
            f'<text x="20" y="{y}" fill="#39d353">{key}:</text>'
            f'<text x="140" y="{y}" fill="#c9d1d9">{val}</text>'
            f'{anim}</g>'
        )

    svg.append('</svg>')
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Saved {out_path}")

if __name__ == "__main__":
    build_card()