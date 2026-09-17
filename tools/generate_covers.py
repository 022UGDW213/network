#!/usr/bin/env python3
"""Generate cosmic SVG cover art for the 10 featured portfolio projects.
Each cover: deep-space gradient + seeded starfield + nebula blobs +
a project-specific neon geometric motif + title bar. No external assets.
Run: python3 tools/generate_covers.py  (outputs assets/covers/*.svg)
"""
import math, os, random, re

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "assets", "covers")

PROJECTS = [
    # slug, title, tag, palette (bg1, bg2, neon, neon2), motif
    ("nvidia-muse-dev-swarm", "NVIDIA Muse Dev Swarm", "30 AGENTS · HF-TRAINED",
     ("#04040c", "#0a1030", "#00e5ff", "#1e90ff"), "chip"),
    ("agent-mail-intel", "Agent Mail Intel", "EMAIL → INTELLIGENCE",
     ("#04040c", "#0a1030", "#1e90ff", "#00e5ff"), "envelope"),
    ("dev-swarm", "Dev Swarm", "DEVOPS FLEET",
     ("#060412", "#160a33", "#3b6cff", "#00e5ff"), "gears"),
    ("ibot-synthetic-intelligence", "iBot Synthetic Intelligence", "FLAGSHIP AI PLATFORM",
     ("#040a0c", "#0a2030", "#00e5ff", "#3b6cff"), "robot"),
    ("harmony-os-next", "Harmony-OS-Next", "ARKTS · HARMONYOS",
     ("#08040c", "#1a0f2e", "#3b6cff", "#1e90ff"), "phone"),
    ("cyberlab-security-platform", "CyberLab Security", "DEFENSIVE SECURITY",
     ("#04040c", "#0a1030", "#1e90ff", "#00e5ff"), "shield"),
    ("python-programing", "Python Programing", "74 SCRIPTS · PY3",
     ("#040c08", "#0a2e1c", "#00e5ff", "#00ff9d"), "terminal"),
    ("html-programing", "HTML Programing", "30 VANILLA-JS CHALLENGES",
     ("#0c0604", "#2e1a0a", "#1e90ff", "#ffb300"), "brackets"),
    ("qwen", "Qwen Local LLM", "LOCAL-FIRST AI",
     ("#060410", "#141033", "#3b6cff", "#00e5ff"), "brain"),
    ("aws-cli", "AWS CLI Fork", "CLOUD TOOLING",
     ("#04080c", "#0a2430", "#00e5ff", "#ff9d00"), "cloud"),
]

W, H = 800, 450


def stars(rng, n=70):
    out = []
    for _ in range(n):
        x = rng.uniform(0, W); y = rng.uniform(0, H * 0.85)
        r = rng.uniform(0.6, 2.2); o = rng.uniform(0.25, 0.95)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" '
                   f'fill="#fff" opacity="{o:.2f}"/>')
    return "\n".join(out)


def motif(kind, neon, neon2):
    c = f'stroke="{neon}" stroke-width="3" fill="none" stroke-linecap="round"'
    c2 = f'stroke="{neon2}" stroke-width="2" fill="none" stroke-linecap="round"'
    g = f'stroke="{neon}" fill="{neon}"'
    # width-free variants for shapes that set their own stroke-width
    c_nw = re.sub(r' stroke-width="[^"]*"', '', c)
    c2_nw = re.sub(r' stroke-width="[^"]*"', '', c2)
    cx, cy = 400, 195
    if kind == "chip":  # GPU chip
        s = []
        s.append(f'<rect x="{cx-70}" y="{cy-70}" width="140" height="140" rx="10" {c}/>')
        s.append(f'<rect x="{cx-40}" y="{cy-40}" width="80" height="80" rx="6" {c2}/>')
        for i in range(5):
            x = cx - 56 + i * 28
            s.append(f'<line x1="{x}" y1="{cy-70}" x2="{x}" y2="{cy-100}" {c2}/>')
            s.append(f'<line x1="{x}" y1="{cy+70}" x2="{x}" y2="{cy+100}" {c2}/>')
            s.append(f'<circle cx="{x}" cy="{cy-104}" r="4" {g} opacity="0.9"/>')
            s.append(f'<circle cx="{x}" cy="{cy+104}" r="4" {g} opacity="0.9"/>')
        return "\n".join(s)
    if kind == "envelope":  # mail radar
        s = [f'<rect x="{cx-90}" y="{cy-60}" width="180" height="120" rx="12" {c}/>',
             f'<polyline points="{cx-90},{cy-60} {cx},{cy+5} {cx+90},{cy-60}" {c}/>',
             f'<circle cx="{cx+120}" cy="{cy-70}" r="46" {c2} opacity="0.5"/>',
             f'<line x1="{cx+120}" y1="{cy-70}" x2="{cx+152}" y2="{cy-102}" {c2}/>',
             f'<circle cx="{cx+120}" cy="{cy-70}" r="5" {g}/>']
        return "\n".join(s)
    if kind == "gears":  # three nodes
        s = []
        pts = [(cx - 80, cy + 30), (cx + 80, cy + 30), (cx, cy - 60)]
        for (x, y) in pts:
            s.append(f'<circle cx="{x}" cy="{y}" r="30" {c}/>')
            s.append(f'<circle cx="{x}" cy="{y}" r="10" {c2}/>')
        s.append(f'<line x1="{pts[0][0]}" y1="{pts[0][1]}" x2="{pts[1][0]}" y2="{pts[1][1]}" {c2} opacity="0.6"/>')
        s.append(f'<line x1="{pts[0][0]}" y1="{pts[0][1]}" x2="{pts[2][0]}" y2="{pts[2][1]}" {c2} opacity="0.6"/>')
        s.append(f'<line x1="{pts[1][0]}" y1="{pts[1][1]}" x2="{pts[2][0]}" y2="{pts[2][1]}" {c2} opacity="0.6"/>')
        return "\n".join(s)
    if kind == "robot":  # robot head
        s = [f'<rect x="{cx-70}" y="{cy-55}" width="140" height="110" rx="22" {c}/>',
             f'<circle cx="{cx-32}" cy="{cy-8}" r="12" {c2}/>',
             f'<circle cx="{cx+32}" cy="{cy-8}" r="12" {c2}/>',
             f'<circle cx="{cx-32}" cy="{cy-8}" r="4" {g}/>',
             f'<circle cx="{cx+32}" cy="{cy-8}" r="4" {g}/>',
             f'<line x1="{cx}" y1="{cy-55}" x2="{cx}" y2="{cy-90}" {c2}/>',
             f'<circle cx="{cx}" cy="{cy-96}" r="6" {g}/>',
             f'<line x1="{cx-40}" y1="{cy+28}" x2="{cx+40}" y2="{cy+28}" {c2}/>',
             f'<rect x="{cx-95}" y="{cy-30}" width="14" height="60" rx="7" {c2}/>',
             f'<rect x="{cx+81}" y="{cy-30}" width="14" height="60" rx="7" {c2}/>']
        return "\n".join(s)
    if kind == "phone":  # phone orbit
        s = [f'<rect x="{cx-48}" y="{cy-85}" width="96" height="170" rx="18" {c}/>',
             f'<line x1="{cx-30}" y1="{cy+62}" x2="{cx+30}" y2="{cy+62}" {c2}/>',
             f'<ellipse cx="{cx}" cy="{cy}" rx="130" ry="44" {c2} opacity="0.55" '
             f'transform="rotate(-18 {cx} {cy})"/>',
             f'<circle cx="{cx+118}" cy="{cy-44}" r="6" {g}/>']
        return "\n".join(s)
    if kind == "shield":
        s = [f'<path d="M{cx},{cy-85} L{cx+70},{cy-50} V{cy+10} '
             f'C{cx+70},{cy+55} {cx+35},{cy+80} {cx},{cy+92} '
             f'C{cx-35},{cy+80} {cx-70},{cy+55} {cx-70},{cy+10} '
             f'V{cy-50} Z" {c}/>',
             f'<polyline points="{cx-28},{cy+2} {cx-6},{cy+24} {cx+30},{cy-22}" {c2_nw} stroke-width="4"/>']
        return "\n".join(s)
    if kind == "terminal":
        s = [f'<rect x="{cx-95}" y="{cy-65}" width="190" height="130" rx="10" {c}/>',
             f'<line x1="{cx-95}" y1="{cy-32}" x2="{cx+95}" y2="{cy-32}" {c2} opacity="0.6"/>',
             f'<circle cx="{cx-75}" cy="{cy-48}" r="5" {g} opacity="0.8"/>',
             f'<polyline points="{cx-70},{cy+8} {cx-45},{cy+28} {cx-70},{cy+48}" {c_nw} stroke-width="4"/>',
             f'<line x1="{cx-32}" y1="{cy+48}" x2="{cx+10}" y2="{cy+48}" {c_nw} stroke-width="4"/>']
        return "\n".join(s)
    if kind == "brackets":
        s = [f'<polyline points="{cx-30},{cy-70} {cx-95},{cy} {cx-30},{cy+70}" {c_nw} stroke-width="6"/>',
             f'<polyline points="{cx+30},{cy-70} {cx+95},{cy} {cx+30},{cy+70}" {c_nw} stroke-width="6"/>',
             f'<line x1="{cx+18}" y1="{cy-80}" x2="{cx-18}" y2="{cy+80}" {c2_nw} stroke-width="5"/>']
        return "\n".join(s)
    if kind == "brain":  # neural net
        rng = random.Random(7)
        nodes = [(cx + rng.uniform(-90, 90), cy + rng.uniform(-70, 70)) for _ in range(9)]
        s = []
        for i, (x1, y1) in enumerate(nodes):
            for x2, y2 in nodes[i + 1:]:
                if math.hypot(x2 - x1, y2 - y1) < 95:
                    s.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" {c2} opacity="0.5"/>')
        for x, y in nodes:
            s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="7" {g} opacity="0.9"/>')
        return "\n".join(s)
    if kind == "cloud":
        s = [f'<path d="M{cx-80},{cy+40} a38,38 0 0 1 6,-75 a48,48 0 0 1 92,-14 '
             f'a36,36 0 0 1 62,39 a30,30 0 0 1 -8,50 Z" {c}/>',
             f'<line x1="{cx-50}" y1="{cy+78}" x2="{cx-62}" y2="{cy+104}" {c2_nw} stroke-width="4"/>',
             f'<line x1="{cx}" y1="{cy+78}" x2="{cx}" y2="{cy+108}" {c2_nw} stroke-width="4"/>',
             f'<line x1="{cx+50}" y1="{cy+78}" x2="{cx+62}" y2="{cy+104}" {c2_nw} stroke-width="4"/>']
        return "\n".join(s)
    return ""


def cover(slug, title, tag, pal, motif_kind, seed):
    bg1, bg2, neon, neon2 = pal
    rng = random.Random(seed)
    gid = slug.replace("-", "")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{title} cover art">
<defs>
<linearGradient id="bg{gid}" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="{bg1}"/><stop offset="1" stop-color="{bg2}"/>
</linearGradient>
<radialGradient id="neb1{gid}" cx="0.25" cy="0.2" r="0.55">
<stop offset="0" stop-color="{neon}" stop-opacity="0.28"/><stop offset="1" stop-color="{neon}" stop-opacity="0"/>
</radialGradient>
<radialGradient id="neb2{gid}" cx="0.8" cy="0.85" r="0.6">
<stop offset="0" stop-color="{neon2}" stop-opacity="0.24"/><stop offset="1" stop-color="{neon2}" stop-opacity="0"/>
</radialGradient>
<linearGradient id="bar{gid}" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="{neon}"/><stop offset="1" stop-color="{neon2}"/>
</linearGradient>
</defs>
<rect width="{W}" height="{H}" fill="url(#bg{gid})"/>
<rect width="{W}" height="{H}" fill="url(#neb1{gid})"/>
<rect width="{W}" height="{H}" fill="url(#neb2{gid})"/>
{stars(rng)}
<g opacity="0.95" style="filter:drop-shadow(0 0 14px {neon}66)">
{motif(motif_kind, neon, neon2)}
</g>
<rect y="{H-92}" width="{W}" height="92" fill="#04040a" opacity="0.72"/>
<rect y="{H-92}" width="{W}" height="3" fill="url(#bar{gid})"/>
<text x="36" y="{H-52}" font-family="'JetBrains Mono',monospace" font-size="26" font-weight="700" fill="#f2f6ff" letter-spacing="1">{title.upper()}</text>
<text x="36" y="{H-24}" font-family="'JetBrains Mono',monospace" font-size="13" fill="{neon}" letter-spacing="3">{tag}</text>
<text x="{W-36}" y="{H-24}" text-anchor="end" font-family="'JetBrains Mono',monospace" font-size="12" fill="#8b93b8" letter-spacing="2">O22UGDW213</text>
</svg>'''
    return svg


def main():
    os.makedirs(OUT, exist_ok=True)
    for i, (slug, title, tag, pal, mk) in enumerate(PROJECTS):
        p = os.path.join(OUT, f"{slug}.svg")
        with open(p, "w") as f:
            f.write(cover(slug, title, tag, pal, mk, seed=1000 + i))
        print(p, os.path.getsize(p), "bytes")


if __name__ == "__main__":
    main()
