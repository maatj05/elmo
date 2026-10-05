import math, random
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

F = '/tmp/claude-0/-home-user-elmo/a7411fc2-5360-5051-9ebd-b0590e782c0c/scratchpad/f/'
random.seed(7)


def text_path(fontfile, text, size, cx, baseline, tracking=0, max_w=None):
    font = TTFont(fontfile)
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    upm = font['head'].unitsPerEm
    hmtx = font['hmtx']
    names = [cmap[ord(c)] for c in text]
    adv = sum(hmtx[n][0] for n in names) + tracking * (len(names) - 1)
    s = size / upm
    if max_w and adv * s > max_w:
        s = max_w / adv
    width = adv * s
    x = cx - width / 2
    pen = SVGPathPen(gs)
    for n in names:
        tp = TransformPen(pen, (s, 0, 0, -s, x, baseline))
        gs[n].draw(tp)
        x += (hmtx[n][0] + tracking) * s
    return pen.getCommands(), width


def star4(cx, cy, r, w=0.22):
    pts = []
    for i in range(8):
        a = math.pi / 4 * i - math.pi / 2
        rr = r if i % 2 == 0 else r * w
        pts.append(f'{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}')
    return 'M' + ' L'.join(pts) + 'Z'


W, H = 1000, 1000
out = []
o = out.append
o(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
o('<title>GLITTERdisco – De kerstdisco van het Kulturhus</title>')
o('''<defs>
<radialGradient id="bg" cx="50%" cy="38%" r="65%">
  <stop offset="0" stop-color="#5b2a9e"/><stop offset="0.55" stop-color="#2c1260"/><stop offset="1" stop-color="#140834"/>
</radialGradient>
<linearGradient id="gold" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#fff6c2"/><stop offset="0.35" stop-color="#ffd23f"/><stop offset="0.6" stop-color="#ffb000"/><stop offset="1" stop-color="#ff7a00"/>
</linearGradient>
<linearGradient id="pink" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#ff9ee8"/><stop offset="0.5" stop-color="#ff3fb4"/><stop offset="1" stop-color="#c41f9a"/>
</linearGradient>
<radialGradient id="ballshade" cx="35%" cy="30%" r="75%">
  <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.7" stop-color="#1a0a40" stop-opacity="0.15"/><stop offset="1" stop-color="#1a0a40" stop-opacity="0.65"/>
</radialGradient>
<radialGradient id="glow" cx="50%" cy="50%" r="50%">
  <stop offset="0" stop-color="#ff7be0" stop-opacity="0.55"/><stop offset="1" stop-color="#ff7be0" stop-opacity="0"/>
</radialGradient>
<linearGradient id="ribbon" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#e8304a"/><stop offset="1" stop-color="#b3122c"/>
</linearGradient>
<linearGradient id="ribbonDark" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#9c0f26"/><stop offset="1" stop-color="#6e0a1a"/>
</linearGradient>
<linearGradient id="beam" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#fff" stop-opacity="0.22"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
</linearGradient>
<clipPath id="disc"><circle cx="500" cy="500" r="480"/></clipPath>
<clipPath id="ballclip"><circle cx="500" cy="255" r="150"/></clipPath>''')

# glitter pattern (random sparkly dots) used on top of the gold title
o('<pattern id="glitter" width="120" height="120" patternUnits="userSpaceOnUse">')
for _ in range(90):
    x, y = random.uniform(0, 120), random.uniform(0, 120)
    r = random.choice([0.8, 1.1, 1.5, 2.0])
    c = random.choice(['#ffffff', '#fffbe0', '#ffe066', '#ff9ee8', '#b06bff'])
    o(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}" opacity="{random.uniform(0.5, 1):.2f}"/>')
o('</pattern>')
o('<pattern id="glitterPink" width="90" height="90" patternUnits="userSpaceOnUse">')
for _ in range(60):
    x, y = random.uniform(0, 90), random.uniform(0, 90)
    o(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{random.choice([0.8, 1.2, 1.7])}" fill="{random.choice(["#fff", "#ffe3f7", "#ffd23f"])}" opacity="{random.uniform(0.4, 0.95):.2f}"/>')
o('</pattern>')
o('</defs>')

# background disc with white + gold rim
o('<circle cx="500" cy="500" r="492" fill="#ffd23f"/>')
o('<circle cx="500" cy="500" r="484" fill="#fff"/>')
o('<circle cx="500" cy="500" r="480" fill="url(#bg)"/>')
o('<g clip-path="url(#disc)">')
# light beams from the ball
for ang, col in [(-55, '#ff6fd8'), (-25, '#6fe3ff'), (25, '#ffe066'), (55, '#8cff8a')]:
    a = math.radians(ang)
    x1, y1 = 500 + 900 * math.sin(a - 0.07), 255 + 900 * math.cos(a - 0.07)
    x2, y2 = 500 + 900 * math.sin(a + 0.07), 255 + 900 * math.cos(a + 0.07)
    o(f'<path d="M500,255 L{x1:.0f},{y1:.0f} L{x2:.0f},{y2:.0f}Z" fill="{col}" opacity="0.13"/>')
# snow / stars in the sky
for _ in range(70):
    x, y = random.uniform(30, 970), random.uniform(30, 970)
    if math.hypot(x - 500, y - 255) < 175:
        continue
    o(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.choice([1.5, 2, 2.5, 3.5])}" fill="#fff" opacity="{random.uniform(0.35, 0.9):.2f}"/>')
o('<circle cx="500" cy="255" r="230" fill="url(#glow)"/>')
o('</g>')

# string
o('<rect x="496" y="20" width="8" height="90" rx="4" fill="#c9c3e6"/>')
o('<rect x="478" y="100" width="44" height="16" rx="5" fill="#d8d2f2" stroke="#8d84b8" stroke-width="2"/>')

# disco ball: projected sphere tiles
BX, BY, R = 500, 255, 150
o('<g clip-path="url(#ballclip)">')
o(f'<circle cx="{BX}" cy="{BY}" r="{R}" fill="#9aa4d8"/>')
light = (-0.5, -0.6, 0.62)
ln = math.sqrt(sum(v * v for v in light))
light = tuple(v / ln for v in light)
palette = ['#ffffff', '#e9f2ff', '#cfe0ff', '#b9c7f2', '#ffd6f4', '#d6fbff', '#fff3c4', '#e2d4ff']
nlat = 14
for i in range(nlat):
    la0 = -math.pi / 2 + math.pi * i / nlat
    la1 = la0 + math.pi / nlat
    lam = (la0 + la1) / 2
    nlon = max(4, int(round(26 * math.cos(lam))))
    for j in range(nlon):
        lo0 = -math.pi / 2 + math.pi * j / nlon + 0.12
        lo1 = lo0 + math.pi / nlon
        if lo1 > math.pi / 2 + 0.001 + 0.12:
            continue
        def P(la, lo):
            return BX + R * math.cos(la) * math.sin(lo), BY + R * math.sin(la)
        pts = [P(la0, lo0), P(la0, lo1), P(la1, lo1), P(la1, lo0)]
        lom = (lo0 + lo1) / 2
        n = (math.cos(lam) * math.sin(lom), math.sin(lam), math.cos(lam) * math.cos(lom))
        d = max(0, sum(a * b for a, b in zip(n, light)))
        if n[2] < 0:
            continue
        base = random.choice(palette)
        op = 0.35 + 0.65 * d
        if random.random() < 0.06:
            base = random.choice(['#ff6fd8', '#6fe3ff', '#ffe066'])
            op = 0.95
        dstr = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + 'Z'
        o(f'<path d="{dstr}" fill="{base}" fill-opacity="{op:.2f}" stroke="#5a5f94" stroke-width="1.6"/>')
o(f'<circle cx="{BX}" cy="{BY}" r="{R}" fill="url(#ballshade)"/>')
o('</g>')
o(f'<circle cx="{BX}" cy="{BY}" r="{R}" fill="none" stroke="#3d2a7a" stroke-width="5"/>')
# shine sparkles on the ball
o(f'<path d="{star4(438, 195, 34, 0.16)}" fill="#fff"/>')
o(f'<path d="{star4(565, 300, 18, 0.18)}" fill="#fff" opacity="0.9"/>')
o(f'<circle cx="438" cy="195" r="9" fill="#fff"/>')

# sparkles around
for (x, y, r, c) in [(250, 160, 30, '#ffd23f'), (770, 140, 24, '#ff7be0'), (215, 330, 16, '#6fe3ff'),
                     (790, 330, 34, '#ffd23f'), (330, 90, 14, '#fff'), (690, 95, 12, '#fff'),
                     (130, 520, 18, '#ff7be0'), (880, 520, 18, '#6fe3ff')]:
    o(f'<path d="{star4(x, y, r)}" fill="{c}"/>')

# ---- title: GLITTER ----
g_d, g_w = text_path(F + 'fredoka.ttf', 'GLITTER', 190, 500, 585, tracking=10, max_w=760)
o('<g>')
o(f'<path d="{g_d}" transform="translate(0,10)" fill="#3a0a5e" stroke="#3a0a5e" stroke-width="34" stroke-linejoin="round"/>')
o(f'<path d="{g_d}" fill="#fff" stroke="#fff" stroke-width="30" stroke-linejoin="round"/>')
o(f'<path d="{g_d}" fill="none" stroke="#ff3fb4" stroke-width="16" stroke-linejoin="round"/>')
o(f'<path d="{g_d}" fill="url(#gold)"/>')
o(f'<path d="{g_d}" fill="url(#glitter)"/>')
o('</g>')

# ---- title: disco (script) ----
d_d, d_w = text_path(F + 'pacifico.ttf', 'disco', 175, 485, 760, max_w=480)
o(f'<path d="{d_d}" transform="translate(0,9)" fill="#3a0a5e" stroke="#3a0a5e" stroke-width="30" stroke-linejoin="round"/>')
o(f'<path d="{d_d}" fill="#fff" stroke="#fff" stroke-width="24" stroke-linejoin="round"/>')
o(f'<path d="{d_d}" fill="url(#pink)"/>')
o(f'<path d="{d_d}" fill="url(#glitterPink)"/>')
# ✨ next to disco
sx = 485 + d_w / 2 + 50
o(f'<path d="{star4(sx, 640, 44, 0.2)}" fill="#ffd23f" stroke="#fff" stroke-width="5" stroke-linejoin="round"/>')
o(f'<path d="{star4(sx + 42, 700, 22, 0.2)}" fill="#fff4b0" stroke="#fff" stroke-width="3" stroke-linejoin="round"/>')
o(f'<path d="{star4(sx - 30, 715, 14, 0.2)}" fill="#fff" />')

# ---- ribbon banner ----
ry, rh = 815, 92
o(f'<path d="M95,{ry + 22} L175,{ry + 22} L175,{ry + rh + 22} L95,{ry + rh + 22} L125,{ry + 22 + rh / 2}Z" fill="url(#ribbonDark)"/>')
o(f'<path d="M905,{ry + 22} L825,{ry + 22} L825,{ry + rh + 22} L905,{ry + rh + 22} L875,{ry + 22 + rh / 2}Z" fill="url(#ribbonDark)"/>')
o(f'<path d="M175,{ry + rh} L175,{ry + rh + 22} L205,{ry + rh}Z" fill="#5c0814"/>')
o(f'<path d="M825,{ry + rh} L825,{ry + rh + 22} L795,{ry + rh}Z" fill="#5c0814"/>')
o(f'<rect x="150" y="{ry}" width="700" height="{rh}" rx="12" fill="url(#ribbon)" stroke="#ffd23f" stroke-width="4"/>')
o(f'<rect x="162" y="{ry + 9}" width="676" height="{rh - 18}" rx="8" fill="none" stroke="#fff" stroke-width="2" stroke-dasharray="2 9" stroke-linecap="round" opacity="0.8"/>')
s1, _ = text_path(F + 'fredoka.ttf', 'De kerstdisco van het Kulturhus', 44, 500, ry + 61, tracking=6, max_w=560)
o(f'<path d="{s1}" fill="#fff"/>')


# christmas trees on either side of the "disco" line
def tree(x, y, s):
    g = [f'<g transform="translate({x},{y}) scale({s})">',
         '<rect x="-9" y="62" width="18" height="22" rx="3" fill="#8a4b22"/>',
         '<path d="M0,-70 L52,8 L28,8 L62,64 L-62,64 L-28,8 L-52,8Z" fill="#1fa65a" stroke="#fff" stroke-width="6" stroke-linejoin="round"/>',
         '<path d="M-30,30 Q0,48 34,22" fill="none" stroke="#ffd23f" stroke-width="5" stroke-linecap="round"/>',
         '<path d="M-20,-8 Q4,6 22,-12" fill="none" stroke="#ffd23f" stroke-width="5" stroke-linecap="round"/>']
    for bx, by, bc in [(-30, 48, '#ff3fb4'), (20, 52, '#6fe3ff'), (-8, 18, '#e8304a'), (14, -24, '#ff3fb4'), (40, 36, '#ffd23f')]:
        g.append(f'<circle cx="{bx}" cy="{by}" r="7" fill="{bc}" stroke="#fff" stroke-width="2"/>')
    g.append(f'<path d="{star4(0, -76, 22, 0.42)}" fill="#ffd23f" stroke="#fff" stroke-width="3" stroke-linejoin="round"/>')
    g.append('</g>')
    return ''.join(g)


o(tree(165, 690, 0.95))
o(tree(845, 690, 0.8))
o('</svg>')

open('/home/user/elmo/glitterdisco-logo.svg', 'w').write('\n'.join(out))
print('ok')
