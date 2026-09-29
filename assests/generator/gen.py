"""Generate assests/dark.svg and assests/light.svg from one shared layout.

Usage:  python3 gen.py                       (writes ../dark.svg and ../light.svg)
        python3 gen.py out_dir               (writes elsewhere for previewing)
        python3 gen.py out_dir --themes portfolio            (one theme)
        python3 gen.py out_dir --themes portfolio --card left (left card only, own canvas)
Edit the DATA block below to change any profile text.

Both themes share geometry, copy and animation timing; only the palette,
glow strength and portrait ramp direction differ.  SMIL only, no scripts,
no external assets.  Every element is visible in its base state so the
banner reads correctly even when animation is unsupported.
"""
import json, os, sys, random
from xml.sax.saxutils import escape as _esc

S = os.path.dirname(os.path.abspath(__file__))
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
OUT = ARGS[0] if ARGS else os.path.dirname(S)   # default: write assests/dark.svg + light.svg
def _opt(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default
THEMES_TO_BUILD = _opt("--themes", "dark,light").split(",")
CARD = _opt("--card", None)          # None = full banner, "left" = portrait card only
os.makedirs(OUT, exist_ok=True)

def esc(s): return _esc(s, {'"': "&quot;"})

# ---------------------------------------------------------------- DATA (resume + portfolio) — edit here
NAME      = "Sushant Kumar"
HEADLINE  = "Full-Stack & React Native Engineer · Industrial IoT"
ROLES     = ["Full-Stack Engineer", "React Native Engineer", "IoT Engineer", "Product Lead"]
USER_HOST = "sushantkr961@dev"
ROWS = [
    ("ROLE",      "Full-Stack Developer & Product Lead"),
    ("COMPANY",   "Uptime Linked"),
    ("LOCATION",  "New Delhi, India"),
    ("FOCUS",     "Web · Mobile · Industrial IoT · System Design"),
    ("EDUCATION", "B.Tech Mechanical · Masai School Full-Stack"),
    ("BUILDING",  "UptimeLinked · TaktBoard · School ERP"),
]
PILLS = [["TypeScript", "React", "Next.js", "React Native", "Node.js", "Express", "Prisma"],
         ["MySQL", "MongoDB", "Redis", "Socket.IO", "AWS", "Docker", "MQTT / Modbus"]]
PROJECTS = [
    ("UptimeLinked", "Manufacturing IoT platform · machine data to OEE & downtime"),
    ("LoadingWalla", "Logistics marketplace · React Native app on Google Play + web"),
    ("School ERP",   "One-click on-prem school ERP · Electron + Next.js · open source"),
]
LINKS = ["github.com/sushantkr961", "linkedin.com/in/sushantkr961", "sushantkr961.github.io"]
TAGLINE = "Full-Stack · React Native · IoT"
ARIA = ("Sushant Kumar, Full-Stack and React Native Engineer working on Industrial IoT, "
        "Full-Stack Developer and Product Lead at Uptime Linked, New Delhi, India. "
        "Stack: TypeScript, React, Next.js, React Native, Node.js, Express, Prisma, MySQL, MongoDB, Redis, AWS, Docker.")

# ---------------------------------------------------------------- themes
THEMES = {
  "dark": dict(
    bg0="#030712", bg1="#07111F", bg2="#0B1220",
    panel="#0F172A", panel_op=".55", panel_stroke="#334155", panel_stroke_op=".55",
    header="#0B1220", header_op=".7",
    text="#F8FAFC", text2="#CBD5E1", muted="#94A3B8", faint="#64748B",
    a1="#7C3AED", a2="#22D3EE", a3="#10B981", a1l="#A78BFA", a2l="#67E8F9", a3l="#34D399",
    grid="#94A3B8", grid_op=".045", noise_op=".035",
    blob1="#4C1D95", blob2="#155E75", blob3="#065F46", blob_op=".55",
    pill="#1E293B", pill_op=".6", pill_stroke="#475569",
    glow_std=3.2, glow_op=".8", scan_op=".18", shadow=False,
    ascii=("#22D3EE", "#7C3AED", "#34D399"), invert=False,
    cursor="#22D3EE", divider="#334155", divider_op=".7",
    dot_r="#FF5F57", dot_y="#FEBC2E", dot_g="#28C840",
    particle="#A5F3FC", particle_op=".5",
  ),
  "portfolio": dict(   # sushantkr961.github.io landing tokens: asphalt, warm paper, signal orange, telemetry green
    bg0="#0E1116", bg1="#12161C", bg2="#161B22",
    panel="#161B22", panel_op=".75", panel_stroke="#EDE9E1", panel_stroke_op=".12",
    header="#1C222B", header_op=".8",
    text="#EDE9E1", text2="#D6D2CA", muted="#A3A199", faint="#7A7974",
    a1="#FF7A1A", a2="#FFA45C", a3="#5CE0A8", a1l="#FFB067", a2l="#FF7A1A", a3l="#5CE0A8",
    grid="#EDE9E1", grid_op=".035", noise_op=".03",
    blob1="#FF7A1A", blob2="#2A3340", blob3="#5CE0A8", blob_op=".16",
    pill="#1C222B", pill_op=".9", pill_stroke="#3A4250",
    glow_std=2.4, glow_op=".5", scan_op=".14", shadow=False,
    ascii=("#FF7A1A", "#FFB067", "#FF9A3C"), invert=False,
    cursor="#FF7A1A", divider="#EDE9E1", divider_op=".12",
    dot_r="#FF5F57", dot_y="#FEBC2E", dot_g="#28C840",
    particle="#FFB067", particle_op=".35",
  ),
  "light": dict(
    bg0="#FFFFFF", bg1="#F8FAFC", bg2="#EEF6FF",
    panel="#FFFFFF", panel_op=".72", panel_stroke="#CBD5E1", panel_stroke_op=".9",
    header="#F1F5F9", header_op=".9",
    text="#0F172A", text2="#1E293B", muted="#475569", faint="#94A3B8",
    a1="#2563EB", a2="#0891B2", a3="#059669", a1l="#4F46E5", a2l="#0E7490", a3l="#047857",
    grid="#1E3A8A", grid_op=".05", noise_op=".025",
    blob1="#BFDBFE", blob2="#A5F3FC", blob3="#BBF7D0", blob_op=".7",
    pill="#EFF6FF", pill_op=".9", pill_stroke="#93C5FD",
    glow_std=1.6, glow_op=".35", scan_op=".10", shadow=True,
    ascii=("#1D4ED8", "#0E7490", "#6D28D9"), invert=True,
    cursor="#2563EB", divider="#CBD5E1", divider_op=".9",
    dot_r="#FF5F57", dot_y="#FEBC2E", dot_g="#28C840",
    particle="#2563EB", particle_op=".25",
  ),
}

# ---------------------------------------------------------------- geometry
W, H = 1180, 610
L = dict(x=28, y=28, w=430, h=554)            # left card
R = dict(x=478, y=28, w=674, h=554)           # right card
HEAD_H = 42
MONO = "ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace"
CW = 0.60                                     # em -> glyph width (monospace)

PORT = json.load(open(os.path.join(S, "portrait.json")))
LUM = PORT["lum"]; PCOLS, PROWS = len(LUM[0]), len(LUM)
P_FS, P_LH = 9.0, 8.6
P_W = round(PCOLS * P_FS * CW, 1)             # forced row width via textLength
P_X = L["x"] + (L["w"] - P_W) / 2
P_Y = 104
RAMP = " .·:-=+*#%@"

def reveal(start, dur=.55, total=None):
    """opacity 0 until `start`, then fade in. begins at 0s so no flash; base opacity=1 for no-SMIL."""
    total = total or (start + dur)
    k = round(start / total, 4)
    return (f'<animate attributeName="opacity" values="0;0;1" keyTimes="0;{k};1" '
            f'dur="{total}s" begin="0s" fill="freeze"/>')

def rise(start, dy=8, dur=.6):
    total = start + dur; k = round(start / total, 4)
    return (f'<animateTransform attributeName="transform" type="translate" values="0 {dy};0 {dy};0 0" '
            f'keyTimes="0;{k};1" calcMode="spline" keySplines="0 0 1 1;.2 .8 .2 1" dur="{total}s" begin="0s" fill="freeze"/>')

# ---------------------------------------------------------------- pieces
def defs(t, CW_=W, CH_=H):
    g = t["glow_std"]
    return f'''
<defs>
  <linearGradient id="accent" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{t['a1']}"/><stop offset=".5" stop-color="{t['a2']}"/><stop offset="1" stop-color="{t['a3']}"/>
  </linearGradient>
  <linearGradient id="nameGrad" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{t['a1l']}"><animate attributeName="stop-color" values="{t['a1l']};{t['a2l']};{t['a3l']};{t['a1l']}" dur="10s" repeatCount="indefinite"/></stop>
    <stop offset="1" stop-color="{t['a2l']}"><animate attributeName="stop-color" values="{t['a2l']};{t['a3l']};{t['a1l']};{t['a2l']}" dur="10s" repeatCount="indefinite"/></stop>
  </linearGradient>
  <linearGradient id="asciiGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{t['ascii'][0]}"><animate attributeName="stop-color" values="{t['ascii'][0]};{t['ascii'][1]};{t['ascii'][2]};{t['ascii'][0]}" dur="12s" repeatCount="indefinite"/></stop>
    <stop offset=".5" stop-color="{t['ascii'][1]}"><animate attributeName="stop-color" values="{t['ascii'][1]};{t['ascii'][2]};{t['ascii'][0]};{t['ascii'][1]}" dur="12s" repeatCount="indefinite"/></stop>
    <stop offset="1" stop-color="{t['ascii'][2]}"><animate attributeName="stop-color" values="{t['ascii'][2]};{t['ascii'][0]};{t['ascii'][1]};{t['ascii'][2]}" dur="12s" repeatCount="indefinite"/></stop>
  </linearGradient>
  <linearGradient id="borderGrad" x1="0" y1="0" x2="1" y2=".25">
    <stop offset="0" stop-color="{t['a1']}" stop-opacity=".15"/>
    <stop offset=".45" stop-color="{t['a2']}" stop-opacity=".95"/>
    <stop offset=".55" stop-color="{t['a3']}" stop-opacity=".95"/>
    <stop offset="1" stop-color="{t['a1']}" stop-opacity=".15"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0;-1 0" dur="9s" repeatCount="indefinite"/>
  </linearGradient>
  <linearGradient id="sheen" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ffffff" stop-opacity="{'.07' if not t['shadow'] else '.6'}"/>
    <stop offset=".6" stop-color="#ffffff" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="sweep" x1="0" y1="0" x2="1" y2=".5">
    <stop offset="0" stop-color="#ffffff" stop-opacity="0"/>
    <stop offset=".5" stop-color="#ffffff" stop-opacity="{'.08' if not t['shadow'] else '.45'}"/>
    <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-1.2 0;1.2 0" dur="11s" repeatCount="indefinite"/>
  </linearGradient>
  <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{t['a2']}" stop-opacity="0"/>
    <stop offset=".5" stop-color="{t['a2']}" stop-opacity="{t['scan_op']}"/>
    <stop offset="1" stop-color="{t['a2']}" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{t['bg0']}"/><stop offset=".55" stop-color="{t['bg1']}"/><stop offset="1" stop-color="{t['bg2']}"/>
  </linearGradient>
  <radialGradient id="blob1"><stop offset="0" stop-color="{t['blob1']}" stop-opacity="{t['blob_op']}"/><stop offset="1" stop-color="{t['blob1']}" stop-opacity="0"/></radialGradient>
  <radialGradient id="blob2"><stop offset="0" stop-color="{t['blob2']}" stop-opacity="{t['blob_op']}"/><stop offset="1" stop-color="{t['blob2']}" stop-opacity="0"/></radialGradient>
  <radialGradient id="blob3"><stop offset="0" stop-color="{t['blob3']}" stop-opacity="{t['blob_op']}"/><stop offset="1" stop-color="{t['blob3']}" stop-opacity="0"/></radialGradient>
  <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
    <path d="M24 0H0V24" fill="none" stroke="{t['grid']}" stroke-opacity="{t['grid_op']}" stroke-width="1"/>
  </pattern>
  <filter id="noise" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/>
    <feColorMatrix type="saturate" values="0"/>
  </filter>
  <filter id="glow" x="-20%" y="-40%" width="140%" height="180%">
    <feGaussianBlur stdDeviation="{g}" result="b"/>
    <feComponentTransfer in="b" result="b2"><feFuncA type="linear" slope="{t['glow_op']}"/></feComponentTransfer>
    <feMerge><feMergeNode in="b2"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="softGlow" x="-10%" y="-10%" width="120%" height="120%">
    <feGaussianBlur stdDeviation="{g*0.6}" result="b"/>
    <feComponentTransfer in="b" result="b2"><feFuncA type="linear" slope="{float(t['glow_op'])*0.6:.2f}"/></feComponentTransfer>
    <feMerge><feMergeNode in="b2"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="shadow" x="-10%" y="-10%" width="120%" height="130%">
    <feDropShadow dx="0" dy="10" stdDeviation="14" flood-color="#0F172A" flood-opacity=".10"/>
  </filter>
  <clipPath id="frame"><rect x="6" y="6" width="{CW_-12}" height="{CH_-12}" rx="24"/></clipPath>
  <clipPath id="portraitClip"><rect x="{L['x']+12}" y="{P_Y-8}" width="{L['w']-24}" height="{PROWS*P_LH+16}"/></clipPath>
</defs>'''

def background(t, w=W, h=H):
    rnd = random.Random(7)
    sx, sy = w / W, h / H
    parts = [f'<rect x="6" y="6" width="{w-12}" height="{h-12}" rx="24" fill="url(#bgGrad)"/>',
             '<g clip-path="url(#frame)">',
             f'<rect x="0" y="0" width="{w}" height="{h}" fill="url(#grid)"/>']
    blobs = [("blob1", 200, 120, 420, "0 0;60 40;0 0", 26), ("blob2", 960, 470, 380, "0 0;-70 -30;0 0", 31), ("blob3", 620, 80, 300, "0 0;-40 50;0 0", 37)]
    for gid, cx, cy, r, vals, dur in blobs:
        parts.append(f'<circle cx="{cx*sx:.0f}" cy="{cy*sy:.0f}" r="{r if w == W else r*0.55:.0f}" fill="url(#{gid})"><animateTransform attributeName="transform" type="translate" values="{vals}" dur="{dur}s" repeatCount="indefinite"/></circle>')
    parts.append(f'<rect x="0" y="0" width="{w}" height="{h}" filter="url(#noise)" opacity="{t["noise_op"]}"/>')
    for i in range(16 if w == W else 8):
        x = rnd.randint(30, w-30); y = rnd.randint(30, h-30); r = rnd.choice([1, 1, 1.5, 2]); d = rnd.randint(9, 20); dl = rnd.uniform(0, 8)
        parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{t["particle"]}" opacity="{t["particle_op"]}">'
                     f'<animate attributeName="cy" values="{y};{y-28};{y}" dur="{d}s" begin="-{dl:.1f}s" repeatCount="indefinite"/>'
                     f'<animate attributeName="opacity" values="0;{t["particle_op"]};0" dur="{d}s" begin="-{dl:.1f}s" repeatCount="indefinite"/></circle>')
    parts.append('</g>')
    return "\n".join(parts)

def card(t, c, start):
    sh = ' filter="url(#shadow)"' if t["shadow"] else ""
    return f'''<g opacity="1">{reveal(start)}
  <rect x="{c['x']}" y="{c['y']}" width="{c['w']}" height="{c['h']}" rx="18" fill="{t['panel']}" fill-opacity="{t['panel_op']}" stroke="{t['panel_stroke']}" stroke-opacity="{t['panel_stroke_op']}"{sh}/>
  <rect x="{c['x']}" y="{c['y']}" width="{c['w']}" height="{c['h']}" rx="18" fill="url(#sheen)"/>
  <path d="M{c['x']} {c['y']+HEAD_H}H{c['x']+c['w']}" stroke="{t['divider']}" stroke-opacity="{t['divider_op']}"/>
  <circle cx="{c['x']+24}" cy="{c['y']+HEAD_H/2}" r="5.5" fill="{t['dot_r']}"/>
  <circle cx="{c['x']+42}" cy="{c['y']+HEAD_H/2}" r="5.5" fill="{t['dot_y']}"/>
  <circle cx="{c['x']+60}" cy="{c['y']+HEAD_H/2}" r="5.5" fill="{t['dot_g']}"/>
</g>'''

def left(t):
    c = L; cx = c["x"] + c["w"] / 2
    hy = c["y"] + HEAD_H / 2 + 4
    out = [card(t, c, .1)]
    out.append(f'<text x="{c["x"]+80}" y="{hy}" font-size="11.5" fill="{t["muted"]}">{esc(USER_HOST + ":~")}</text>')
    out.append(f'<g>{reveal(.5)}<circle cx="{c["x"]+c["w"]-70}" cy="{hy-4}" r="3" fill="{t["a3"]}"><animate attributeName="opacity" values="1;.35;1" dur="2.4s" repeatCount="indefinite"/></circle>'
               f'<text x="{c["x"]+c["w"]-60}" y="{hy}" font-size="10.5" fill="{t["a3"]}" letter-spacing="1">ONLINE</text></g>')
    # section label
    out.append(f'<g>{reveal(.4)}<text x="{c["x"]+24}" y="{c["y"]+HEAD_H+26}" font-size="10.5" fill="{t["a2"]}" letter-spacing="2.5" font-weight="600">VISUAL.MAP</text>'
               f'<text x="{c["x"]+c["w"]-24}" y="{c["y"]+HEAD_H+26}" font-size="10.5" fill="{t["faint"]}" text-anchor="end">$ render --ascii</text></g>')
    # portrait
    ramp = RAMP
    rows = []
    for i, lum in enumerate(LUM):
        chars = []
        for v in LUM[i]:
            idx = min(len(ramp) - 1, int(v / 256 * len(ramp)))
            if t["invert"]:
                # light theme: dark areas dense, background (0) empty
                idx = 0 if v == 0 else min(len(ramp) - 1, int((255 - v) / 256 * len(ramp)) + 1)
            chars.append(ramp[idx])
        line = "".join(chars)
        y = P_Y + P_LH * (i + 1) - 2
        st = .45 + i * .028
        rows.append(f'<text x="{P_X:.1f}" y="{y:.1f}" textLength="{P_W}" lengthAdjust="spacing" xml:space="preserve">{esc(line)}{reveal(st, .3)}</text>')
    out.append(f'<g clip-path="url(#portraitClip)">'
               f'<g font-family="{MONO}" font-size="{P_FS}" fill="url(#asciiGrad)" filter="url(#softGlow)">'
               f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -2.5;0 0;0 2.5;0 0" dur="9s" repeatCount="indefinite"/>'
               + "\n".join(rows) + '</g>'
               f'<rect x="{c["x"]+12}" y="{P_Y-30}" width="{c["w"]-24}" height="26" fill="url(#scan)">'
               f'<animate attributeName="y" values="{P_Y-30};{P_Y+PROWS*P_LH+6}" dur="6s" begin="1s" repeatCount="indefinite"/></rect>'
               f'<g opacity="0"><animate attributeName="opacity" values="0;0;.35;0;0;.25;0" keyTimes="0;.62;.64;.66;.83;.845;1" dur="13s" repeatCount="indefinite"/>'
               f'<rect x="{c["x"]+12}" y="{P_Y}" width="{c["w"]-24}" height="{PROWS*P_LH}" fill="{t["a2"]}" opacity=".08"/></g>'
               '</g>')
    # divider + tagline + prompt + status
    by = P_Y + PROWS * P_LH + 12
    out.append(f'<path d="M{c["x"]+24} {by}H{c["x"]+c["w"]-24}" stroke="{t["divider"]}" stroke-opacity="{t["divider_op"]}"/>')
    out.append(f'<g>{reveal(1.2)}{rise(1.2)}<text x="{cx}" y="{by+26}" font-size="12.5" fill="{t["text2"]}" text-anchor="middle" letter-spacing=".8">{esc(TAGLINE)}</text></g>')
    py = by + 54
    out.append(f'<g>{reveal(1.5)}<text x="{c["x"]+24}" y="{py}" font-size="12" fill="{t["muted"]}">'
               f'<tspan fill="{t["a3"]}">~/profile</tspan> <tspan fill="{t["faint"]}">$</tspan> <tspan fill="{t["text"]}">build --ship</tspan></text>'
               f'<rect x="{c["x"]+24+12*CW*24+2:.0f}" y="{py-10}" width="7" height="13" fill="{t["cursor"]}"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/></rect></g>')
    sy = c["y"] + c["h"] - 16
    out.append(f'<g>{reveal(1.7)}<text x="{c["x"]+24}" y="{sy}" font-size="10.5" fill="{t["faint"]}">'
               f'<tspan fill="{t["a2"]}">◈</tspan> profile v2026 · <tspan fill="{t["muted"]}">New Delhi, India</tspan></text>'
               f'<text x="{c["x"]+c["w"]-24}" y="{sy}" font-size="10.5" fill="{t["faint"]}" text-anchor="end">svg · smil · no-js</text></g>')
    return "\n".join(out)

def typed_roles(t, x, y, fs):
    """Rotating roles, true per-character reveal + block cursor stepping with the text. 18s loop."""
    per = 4.5; total = per * len(ROLES)
    cw = fs * CW
    texts, events = [], []
    for i, role in enumerate(ROLES):
        s = i * per; n = len(role)
        spans = []
        for j, ch in enumerate(role):
            on = s + .3 + j * .06
            off = s + 3.4 + (n - 1 - j) * .03
            base = "1" if i == 0 else "0"
            spans.append(f'<tspan opacity="{base}">{esc(ch)}<animate attributeName="opacity" values="0;1;0;0" keyTimes="0;{on/total:.4f};{off/total:.4f};1" calcMode="discrete" dur="{total}s" begin="0s" repeatCount="indefinite"/></tspan>')
            events.append((on, j + 1)); events.append((off, j))
        texts.append(f'<text x="{x}" y="{y}" font-size="{fs}" fill="{t["text"]}" textLength="{n*cw:.1f}" lengthAdjust="spacing" xml:space="preserve">{"".join(spans)}</text>')
    events.sort()
    vals, keys = [f"{x:.1f}"], ["0"]
    for tm, k in events:
        vals.append(f"{x + k*cw:.1f}"); keys.append(f"{tm/total:.4f}")
    cur = (f'<rect x="{x + len(ROLES[0])*cw:.1f}" y="{y-fs+2}" width="{cw:.1f}" height="{fs+2}" fill="{t["cursor"]}">'
           f'<animate attributeName="x" values="{";".join(vals)}" keyTimes="{";".join(keys)}" calcMode="discrete" dur="{total}s" begin="0s" repeatCount="indefinite"/>'
           f'<animate attributeName="opacity" values="1;1;.15;.15" keyTimes="0;.5;.5;1" dur="1s" repeatCount="indefinite"/></rect>')
    return "\n".join(texts) + cur

def right(t):
    c = R; x0 = c["x"] + 32; hy = c["y"] + HEAD_H / 2 + 4
    out = [card(t, c, .2)]
    out.append(f'<text x="{c["x"]+80}" y="{hy}" font-size="11.5" fill="{t["a2"]}" letter-spacing="2.5" font-weight="600">SYSTEM.INFO</text>')
    out.append(f'<text x="{c["x"]+c["w"]-24}" y="{hy}" font-size="11" fill="{t["muted"]}" text-anchor="end">{esc(USER_HOST + ":~$ ./profile.sh")}</text>')
    # name / headline / role
    out.append(f'<g>{reveal(.8)}{rise(.8)}<text x="{x0}" y="{c["y"]+92}" font-size="34" font-weight="700" fill="url(#nameGrad)" filter="url(#glow)" letter-spacing="-.5">{esc(NAME)}</text></g>')
    out.append(f'<g>{reveal(1.05)}{rise(1.05)}<text x="{x0}" y="{c["y"]+120}" font-size="14.5" fill="{t["a2"]}">{esc(HEADLINE)}</text></g>')
    ry = c["y"] + 150
    out.append(f'<g>{reveal(1.3)}<text x="{x0}" y="{ry}" font-size="14" fill="{t["a1l"]}" font-weight="700">&gt;</text>' + typed_roles(t, x0 + 20, ry, 14) + '</g>')
    out.append(f'<path d="M{x0} {ry+18}H{c["x"]+c["w"]-32}" stroke="{t["divider"]}" stroke-opacity="{t["divider_op"]}"/>')
    # info rows: label right-aligned, value left-aligned
    lx = x0 + 88; vx = lx + 18; y = ry + 46
    for i, (k, v) in enumerate(ROWS):
        st = 1.55 + i * .13
        out.append(f'<g>{reveal(st, .4)}{rise(st, 6, .45)}'
                   f'<text x="{lx}" y="{y}" font-size="11" fill="{t["a2"]}" text-anchor="end" letter-spacing="1.2">{esc(k)}</text>'
                   f'<text x="{vx-8}" y="{y}" font-size="11" fill="{t["faint"]}">:</text>'
                   f'<text x="{vx}" y="{y}" font-size="13" fill="{t["text"]}">{esc(v)}</text></g>')
        y += 24
    # stack
    y += 6
    out.append(f'<g>{reveal(2.4)}<text x="{x0}" y="{y}" font-size="10.5" fill="{t["a2"]}" letter-spacing="2.5" font-weight="600">STACK</text>'
               f'<path d="M{x0+56} {y-4}H{c["x"]+c["w"]-32}" stroke="{t["divider"]}" stroke-opacity="{t["divider_op"]}"/></g>')
    y += 14
    n = 0
    for row in PILLS:
        px = x0
        for name in row:
            w = round(len(name) * 12 * CW + 24)
            st = 2.5 + n * .045; n += 1
            out.append(f'<g>{reveal(st, .35)}'
                       f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -1.5;0 0" dur="{4 + (n % 5) * .7:.1f}s" begin="-{n * .4:.1f}s" repeatCount="indefinite" additive="sum"/>'
                       f'<rect x="{px}" y="{y}" width="{w}" height="24" rx="12" fill="{t["pill"]}" fill-opacity="{t["pill_op"]}" stroke="{t["pill_stroke"]}" stroke-opacity=".7"/>'
                       f'<circle cx="{px+12}" cy="{y+12}" r="2.5" fill="url(#accent)"/>'
                       f'<text x="{px+20}" y="{y+16}" font-size="12" fill="{t["text2"]}">{esc(name)}</text></g>')
            px += w + 8
        y += 32
    # projects
    y += 12
    out.append(f'<g>{reveal(3.0)}<text x="{x0}" y="{y}" font-size="10.5" fill="{t["a2"]}" letter-spacing="2.5" font-weight="600">PROJECTS</text>'
               f'<path d="M{x0+76} {y-4}H{c["x"]+c["w"]-32}" stroke="{t["divider"]}" stroke-opacity="{t["divider_op"]}"/></g>')
    y += 22
    for i, (name, desc) in enumerate(PROJECTS):
        st = 3.1 + i * .15
        out.append(f'<g>{reveal(st, .4)}{rise(st, 5, .45)}<text x="{x0}" y="{y}" font-size="12" fill="{t["text"]}" font-weight="700">{esc(name)}</text>'
                   f'<text x="{x0+118}" y="{y}" font-size="11.5" fill="{t["muted"]}">{esc(desc)}</text></g>')
        y += 20
    # links
    ly = c["y"] + c["h"] - 18
    out.append(f'<path d="M{x0} {ly-22}H{c["x"]+c["w"]-32}" stroke="{t["divider"]}" stroke-opacity="{t["divider_op"]}"/>')
    spans = []
    for i, l in enumerate(LINKS):
        if i: spans.append(f'<tspan fill="{t["faint"]}">  ·  </tspan>')
        spans.append(f'<tspan fill="{t["a2"]}">{esc(l)}</tspan>')
    out.append(f'<g>{reveal(3.6)}<text x="{x0}" y="{ly}" font-size="11" xml:space="preserve">{"".join(spans)}</text></g>')
    return "\n".join(out)

def overlay(t, w=W, h=H):
    return (f'<rect x="6" y="6" width="{w-12}" height="{h-12}" rx="24" fill="url(#sweep)" pointer-events="none"/>'
            f'<rect x="6.5" y="6.5" width="{w-13}" height="{h-13}" rx="24" fill="none" stroke="url(#borderGrad)" stroke-width="1.2"/>')

def svg(theme, card=None):
    t = THEMES[theme]
    if card == "left":
        # portrait card only: canvas hugs the left card with a 12px gutter
        m = 12
        w, h = L["w"] + 2 * m, L["h"] + 2 * m
        dx, dy = m - L["x"], m - L["y"]
        body = f'<g transform="translate({dx} {dy})">{left(t)}</g>'
        aria = f"{NAME}, {TAGLINE}. Character-rendered portrait card."
    else:
        w, h = W, H
        body = f"{left(t)}\n{right(t)}"
        aria = ARIA
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(aria)}" font-family="{MONO}">
<title>{esc(NAME)} · {esc(HEADLINE)}</title>
<desc>{esc(aria)} Animated terminal-style profile banner ({theme} theme).</desc>
{defs(t, w, h)}
{background(t, w, h)}
{body}
{overlay(t, w, h)}
</svg>
'''

for theme in THEMES_TO_BUILD:
    name = f"{theme}.svg" if CARD is None else f"{theme}-{CARD}.svg"
    path = os.path.join(OUT, name)
    open(path, "w", encoding="utf-8").write(svg(theme, CARD))
    print(path, os.path.getsize(path), "bytes")
