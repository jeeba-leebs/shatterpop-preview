import cairosvg, io, os, math, random, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter
OUT="/home/box/agent-data/projects/studio/shatterpop-art/v1"
def d(*p):
    path=os.path.join(OUT,*p); os.makedirs(os.path.dirname(path),exist_ok=True); return path
def render(svg,w,h):
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(),output_width=w,output_height=h))).convert("RGBA")
def save_svg(svg,rel):
    open(d(rel),"w").write(svg)
def save_scales(svg,base,rel_noext,scales=(1,2,3),svg_too=True):
    if svg_too: save_svg(svg,rel_noext+".svg")
    for s in scales:
        render(svg,base*s,base*s).save(d(f"{rel_noext}@{s}x.png"))
def hexrgb(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
def mix(h,o,t):
    a=hexrgb(h); b=hexrgb(o); return '#%02x%02x%02x'%tuple(round(a[i]+(b[i]-a[i])*t) for i in range(3))
COLORS={"peach":"#FF9E7A","mint":"#6FE3C1","lilac":"#B79CFF","honey":"#FFC94D","berry":"#FF6F9C"}
# deeper "candy" tints to match mockup saturation (mockup: orange/teal/purple/pink)
DEEP={"peach":"#FF7A3D","mint":"#1FBFA0","lilac":"#8A5CF0","honey":"#FFAE1A","berry":"#F0457E"}

def block_svg(name):
    c=COLORS[name]; k=DEEP[name]; dk=mix(k,"#2B1B3D",0.35); lt=mix(c,"#FFFFFF",0.45)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
<defs>
<linearGradient id="body" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{lt}"/><stop offset="0.45" stop-color="{c}"/><stop offset="1" stop-color="{k}"/></linearGradient>
<linearGradient id="edge" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{k}"/><stop offset="1" stop-color="{dk}"/></linearGradient>
<radialGradient id="glow" cx="0.5" cy="0.62" r="0.55"><stop offset="0" stop-color="#ffffff" stop-opacity="0.35"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>
<linearGradient id="gloss" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity="0.85"/><stop offset="1" stop-color="#ffffff" stop-opacity="0.05"/></linearGradient>
</defs>
<rect x="6" y="10" width="116" height="114" rx="26" fill="#000" opacity="0.22"/>
<rect x="6" y="6" width="116" height="114" rx="26" fill="url(#edge)"/>
<rect x="9" y="8" width="110" height="104" rx="23" fill="url(#body)"/>
<rect x="9" y="8" width="110" height="104" rx="23" fill="url(#glow)"/>
<path d="M22 14 H106 Q114 14 114 24 V34 Q64 46 14 34 V24 Q14 14 22 14 Z" fill="url(#gloss)"/>
<ellipse cx="28" cy="24" rx="7" ry="4" fill="#fff" opacity="0.9"/>
<rect x="9.5" y="8.5" width="109" height="103" rx="23" fill="none" stroke="#fff" stroke-opacity="0.35" stroke-width="1.5"/>
<path d="M24 104 Q64 110 104 104" stroke="#fff" stroke-opacity="0.25" stroke-width="3" fill="none" stroke-linecap="round"/>
</svg>'''

def crystal_svg(state="intact", extra=""):
    cracks=""
    if state=="cracked":
        cracks='''<g stroke="#ffffff" stroke-width="3.2" fill="none" stroke-linecap="round" stroke-linejoin="round">
<path d="M64 62 L40 30 L30 22"/><path d="M64 62 L96 40 L110 38"/><path d="M64 62 L48 96 L40 112"/><path d="M64 62 L92 92 L104 108"/><path d="M64 62 L20 66"/>
<path d="M40 30 L52 22"/><path d="M48 96 L30 92"/><path d="M92 92 L106 80"/></g>
<g stroke="#2a6f9a" stroke-width="1.2" stroke-opacity="0.6" fill="none"><path d="M65 64 L42 33"/><path d="M66 64 L94 43"/><path d="M65 64 L50 97"/></g>
<circle cx="64" cy="62" r="5" fill="#fff"/>'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
<defs>
<linearGradient id="ice" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.35" stop-color="#D9F3FF"/><stop offset="0.75" stop-color="#3FB4FF"/><stop offset="1" stop-color="#1668D0"/></linearGradient>
<linearGradient id="prism" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#FF9EE8" stop-opacity="0.45"/><stop offset="0.5" stop-color="#9EFFF2" stop-opacity="0.2"/><stop offset="1" stop-color="#FFF59E" stop-opacity="0.45"/></linearGradient>
<radialGradient id="core" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#ffffff" stop-opacity="0.7"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>
</defs>
<rect x="6" y="10" width="116" height="114" rx="20" fill="#000" opacity="0.22"/>
<rect x="6" y="6" width="116" height="114" rx="20" fill="#1466B8"/>
<rect x="8" y="7" width="112" height="108" rx="18" fill="url(#ice)"/>
<g stroke="#ffffff" stroke-opacity="0.75" stroke-width="1.6" fill="none">
<path d="M8 7 L40 34 L88 34 L120 7"/><path d="M8 115 L40 86 L88 86 L120 115"/><path d="M40 34 L40 86"/><path d="M88 34 L88 86"/><path d="M40 34 L64 60 L88 34"/><path d="M40 86 L64 60 L88 86"/></g>
<polygon points="40,34 64,60 88,34" fill="#ffffff" opacity="0.45"/>
<polygon points="8,7 40,34 40,86 8,115" fill="#ffffff" opacity="0.18"/>
<polygon points="120,7 88,34 88,86 120,115" fill="#0A4E9C" opacity="0.22"/>
<rect x="8" y="7" width="112" height="108" rx="18" fill="url(#prism)"/>
<circle cx="64" cy="60" r="30" fill="url(#core)"/>
{cracks}
<path d="M20 16 L36 16 L24 28 Z" fill="#fff" opacity="0.9"/>
<g fill="#fff"><path d="M100 22 l2 6 l6 2 l-6 2 l-2 6 l-2 -6 l-6 -2 l6 -2z"/></g>
<rect x="8.5" y="7.5" width="111" height="107" rx="18" fill="none" stroke="#E6FAFF" stroke-width="2"/>
{extra}
</svg>'''

def shatter_svg(f, n=6):
    t=f/(n-1)  # 0..1
    random.seed(7)
    shards=[]
    cx,cy=64,62
    polys=[[(8,7),(64,60),(40,34)],[(40,34),(64,60),(88,34)],[(88,34),(64,60),(120,7)],[(120,7),(64,60),(120,115)],[(120,115),(64,60),(88,86)],[(88,86),(64,60),(40,86)],[(40,86),(64,60),(8,115)],[(8,115),(64,60),(8,7)],[(64,7),(88,34),(40,34)],[(8,60),(40,34),(40,86)]]
    out=[]
    ease=1-(1-t)**3
    for i,p in enumerate(polys):
        mx=sum(x for x,_ in p)/3; my=sum(y for _,y in p)/3
        dx,dy=mx-cx,my-cy; L=math.hypot(dx,dy) or 1
        dist=ease*(60+random.random()*30)
        ox=dx/L*dist; oy=dy/L*dist + 40*t*t  # gravity
        rot=(random.random()-.5)*240*ease
        sc=1-0.55*t
        op=1-0.95*t**1.5
        pts=" ".join(f"{(x-mx)*sc:.1f},{(y-my)*sc:.1f}" for x,y in p)
        fill = "#ffffff" if i%3==0 else ("#9FE0FF" if i%3==1 else "#4FB4F2")
        out.append(f'<g transform="translate({mx+ox:.1f},{my+oy:.1f}) rotate({rot:.1f})" opacity="{op:.2f}"><polygon points="{pts}" fill="{fill}" stroke="#E6FAFF" stroke-width="1.5"/></g>')
    flash=""
    if f<=2:
        r=[18,40,56][f]; o=[0.95,0.6,0.2][f]
        flash=f'<circle cx="64" cy="62" r="{r}" fill="url(#fl)" opacity="{o}"/>'
    ring=f'<circle cx="64" cy="62" r="{20+80*ease:.1f}" fill="none" stroke="#D9F3FF" stroke-width="{max(0.5,5*(1-t)):.1f}" opacity="{(1-t)*0.8:.2f}"/>' if f>0 else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="-32 -32 192 192" width="192" height="192">
<defs><radialGradient id="fl"><stop offset="0" stop-color="#fff"/><stop offset="0.5" stop-color="#BDEBFF" stop-opacity="0.7"/><stop offset="1" stop-color="#5CC8FF" stop-opacity="0"/></radialGradient></defs>
{ring}{''.join(out)}{flash}</svg>'''

def frosted_overlay():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
<defs><radialGradient id="f" cx="0.5" cy="0.5" r="0.7"><stop offset="0.45" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#EAF6FF" stop-opacity="0.85"/></radialGradient></defs>
<rect x="9" y="8" width="110" height="104" rx="23" fill="url(#f)"/>
<g fill="#fff" opacity="0.8"><circle cx="20" cy="30" r="2"/><circle cx="108" cy="22" r="1.6"/><circle cx="16" cy="96" r="2.2"/><circle cx="110" cy="100" r="1.8"/><circle cx="62" cy="12" r="1.5"/></g></svg>'''

def sparkle_svg(color="#FFFFFF"):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
<defs><radialGradient id="g"><stop offset="0" stop-color="#fff"/><stop offset="0.3" stop-color="{color}" stop-opacity="0.8"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient></defs>
<circle cx="32" cy="32" r="30" fill="url(#g)"/>
<path d="M32 2 Q34 30 62 32 Q34 34 32 62 Q30 34 2 32 Q30 30 32 2Z" fill="#fff"/></svg>'''

def shard_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
<polygon points="4,6 28,2 18,30" fill="#9FE0FF" stroke="#fff" stroke-width="1.5"/><polygon points="4,6 28,2 16,12" fill="#fff" opacity="0.7"/></svg>'''

def glow_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 64" width="256" height="64">
<defs><radialGradient id="g" cx="0.5" cy="0.5" r="0.5" gradientTransform="scale(1,4) translate(0,-0.375)"><stop offset="0" stop-color="#fff"/><stop offset="0.25" stop-color="#E9B8FF" stop-opacity="0.9"/><stop offset="1" stop-color="#B05CFF" stop-opacity="0"/></radialGradient></defs>
<rect width="256" height="64" fill="url(#g)"/></svg>'''

def bg_svg():
    random.seed(3)
    bok=[]
    for _ in range(26):
        x=random.randint(0,1080); y=random.randint(0,1920); r=random.randint(20,110)
        col=random.choice(["#B79CFF","#FF6F9C","#6FE3C1","#FFC94D","#D9F3FF"])
        bok.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" opacity="{random.uniform(0.05,0.14):.2f}" filter="url(#b)"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920">
<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#45285E"/><stop offset="0.42" stop-color="#2B1B3D"/><stop offset="1" stop-color="#1C102B"/></linearGradient>
<radialGradient id="v" cx="0.5" cy="0.45" r="0.75"><stop offset="0.6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.45"/></radialGradient>
<radialGradient id="hi" cx="0.5" cy="0.4" r="0.5"><stop offset="0" stop-color="#7A3FC0" stop-opacity="0.35"/><stop offset="1" stop-color="#7A3FC0" stop-opacity="0"/></radialGradient>
<filter id="b" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>
<pattern id="dots" width="60" height="60" patternUnits="userSpaceOnUse"><circle cx="30" cy="30" r="2" fill="#fff" opacity="0.04"/></pattern></defs>
<rect width="1080" height="1920" fill="url(#bg)"/><rect width="1080" height="1920" fill="url(#dots)"/>
<ellipse cx="540" cy="820" rx="700" ry="800" fill="url(#hi)"/>
{''.join(bok)}<rect width="1080" height="1920" fill="url(#v)"/></svg>'''

CELL=112; COLS=8; ROWS=10; PAD=28
BW=COLS*CELL+2*PAD; BH=ROWS*CELL+2*PAD+40  # 952 x 1216 (incl. jar lip)
def board_svg():
    cells=[]
    for r in range(ROWS):
        for c in range(COLS):
            x=PAD+c*CELL; y=PAD+40+r*CELL
            cells.append(f'<rect x="{x+4}" y="{y+4}" width="{CELL-8}" height="{CELL-8}" rx="20" fill="#120A1E" opacity="0.55"/><rect x="{x+4}" y="{y+4}" width="{CELL-8}" height="3" rx="1.5" fill="#000" opacity="0.25"/>')
    W,H=BW,BH
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs><linearGradient id="glass" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#E8F1FF" stop-opacity="0.32"/><stop offset="0.12" stop-color="#E8F1FF" stop-opacity="0.12"/><stop offset="0.85" stop-color="#E8F1FF" stop-opacity="0.10"/><stop offset="1" stop-color="#E8F1FF" stop-opacity="0.28"/></linearGradient>
<linearGradient id="inner" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2A1840"/><stop offset="1" stop-color="#1A0F29"/></linearGradient>
<linearGradient id="lip" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F3E9FF"/><stop offset="0.5" stop-color="#B79CFF"/><stop offset="1" stop-color="#6D4BB0"/></linearGradient>
<linearGradient id="rim" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C9A8FF"/><stop offset="1" stop-color="#5B3A8F"/></linearGradient></defs>
<rect x="4" y="44" width="{W-8}" height="{H-48}" rx="56" fill="#000" opacity="0.35"/>
<rect x="0" y="34" width="{W}" height="{H-40}" rx="56" fill="url(#rim)"/>
<rect x="8" y="42" width="{W-16}" height="{H-56}" rx="50" fill="url(#inner)"/>
{''.join(cells)}
<rect x="8" y="42" width="{W-16}" height="{H-56}" rx="50" fill="url(#glass)"/>
<path d="M30 120 Q24 {H/2} 34 {H-120}" stroke="#fff" stroke-opacity="0.35" stroke-width="10" fill="none" stroke-linecap="round"/>
<path d="M{W-30} 160 Q{W-24} {H/2} {W-34} {H-200}" stroke="#fff" stroke-opacity="0.15" stroke-width="6" fill="none" stroke-linecap="round"/>
<rect x="60" y="0" width="{W-120}" height="56" rx="24" fill="url(#lip)"/>
<rect x="80" y="8" width="{W-160}" height="12" rx="6" fill="#fff" opacity="0.6"/>
<rect x="60" y="44" width="{W-120}" height="10" rx="5" fill="#3B2266" opacity="0.6"/>
</svg>'''

TW,TH=1000,300
def tray_svg():
    slots=[]
    sw=(TW-80)/3
    for i in range(3):
        x=24+i*(sw+16)
        slots.append(f'<rect x="{x:.0f}" y="28" width="{sw:.0f}" height="{TH-56}" rx="30" fill="#140B22" opacity="0.7"/><rect x="{x:.0f}" y="28" width="{sw:.0f}" height="{TH-56}" rx="30" fill="none" stroke="#fff" stroke-opacity="0.08" stroke-width="2"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {TW} {TH}" width="{TW}" height="{TH}">
<defs><linearGradient id="t" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4A2E6E"/><stop offset="1" stop-color="#26163A"/></linearGradient></defs>
<rect x="0" y="8" width="{TW}" height="{TH-8}" rx="40" fill="#000" opacity="0.35"/>
<rect x="0" y="0" width="{TW}" height="{TH-8}" rx="40" fill="url(#t)"/>
<rect x="2" y="2" width="{TW-4}" height="{TH-12}" rx="38" fill="none" stroke="#C9A8FF" stroke-opacity="0.45" stroke-width="3"/>
<rect x="40" y="6" width="{TW-80}" height="6" rx="3" fill="#fff" opacity="0.18"/>
{''.join(slots)}</svg>'''

def badge(inner, ring="#FFC94D"):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
<defs><linearGradient id="bb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5A3A86"/><stop offset="1" stop-color="#2B1B3D"/></linearGradient></defs>
<rect x="6" y="10" width="116" height="114" rx="30" fill="#000" opacity="0.3"/>
<rect x="6" y="6" width="116" height="114" rx="30" fill="url(#bb)" stroke="{ring}" stroke-width="4"/>
<path d="M22 12 H106 Q116 12 116 24 V30 Q64 42 12 30 V24 Q12 12 22 12Z" fill="#fff" opacity="0.12"/>
{inner}</svg>'''

def icebreaker_svg():
    inner='''<defs><linearGradient id="ic" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff"/><stop offset="0.5" stop-color="#9FE0FF"/><stop offset="1" stop-color="#2E8FE0"/></linearGradient>
<linearGradient id="hd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE38A"/><stop offset="1" stop-color="#E09A12"/></linearGradient></defs>
<polygon points="52,30 80,40 90,72 70,100 40,96 30,64" fill="url(#ic)" stroke="#E6FAFF" stroke-width="2.5"/>
<g stroke="#fff" stroke-width="2.5" fill="none" stroke-linecap="round"><path d="M60 64 L52 34"/><path d="M60 64 L86 60"/><path d="M60 64 L44 92"/><path d="M60 64 L72 96"/></g>
<polygon points="52,30 60,64 30,64" fill="#fff" opacity="0.4"/>
<g transform="rotate(-38 88 44)"><rect x="84" y="36" width="9" height="56" rx="4" fill="#8A4B16"/><rect x="70" y="22" width="38" height="20" rx="6" fill="url(#hd)" stroke="#fff" stroke-opacity="0.6" stroke-width="2"/><rect x="73" y="25" width="30" height="5" rx="2.5" fill="#fff" opacity="0.6"/></g>
<g fill="#fff"><path d="M28 30 l2 6 l6 2 l-6 2 l-2 6 l-2 -6 l-6 -2 l6 -2z"/><circle cx="100" cy="100" r="3"/></g>'''
    return badge(inner,"#7FD6FF")

def bomb_svg():
    inner='''<defs><radialGradient id="bm" cx="0.35" cy="0.3" r="0.75"><stop offset="0" stop-color="#C9A8FF"/><stop offset="0.45" stop-color="#6B3FC8"/><stop offset="1" stop-color="#26124F"/></radialGradient></defs>
<circle cx="60" cy="72" r="34" fill="url(#bm)"/>
<ellipse cx="48" cy="58" rx="11" ry="7" fill="#fff" opacity="0.55" transform="rotate(-30 48 58)"/>
<rect x="66" y="32" width="18" height="14" rx="3" fill="#4A2E6E" transform="rotate(35 75 39)"/>
<path d="M80 34 Q88 22 98 26" stroke="#C9A06A" stroke-width="4" fill="none" stroke-linecap="round"/>
<g transform="translate(100,24)"><circle r="9" fill="#FFC94D" opacity="0.5"/><path d="M0 -11 L3 -3 L11 0 L3 3 L0 11 L-3 3 L-11 0 L-3 -3Z" fill="#FFF4E0"/><circle r="3" fill="#FF9E7A"/></g>'''
    return badge(inner,"#FFC94D")

def pop_svg(pose="idle"):
    cheer = pose=="cheer"
    body='''<defs>
<radialGradient id="pb" cx="0.38" cy="0.32" r="0.75"><stop offset="0" stop-color="#E6D9FF"/><stop offset="0.35" stop-color="#B79CFF"/><stop offset="0.8" stop-color="#8A5CF0"/><stop offset="1" stop-color="#5E34B8"/></radialGradient>
<radialGradient id="pin" cx="0.5" cy="0.7" r="0.45"><stop offset="0" stop-color="#fff" stop-opacity="0.35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
<radialGradient id="eye" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#3A2266"/><stop offset="0.7" stop-color="#1A0F29"/><stop offset="1" stop-color="#0D0716"/></radialGradient>
<linearGradient id="leaf" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#B8FFE6"/><stop offset="1" stop-color="#1FBFA0"/></linearGradient>
</defs>'''
    # body shape: squashed blob, cheer = taller stretch
    by= 300 if not cheer else 285
    ry= 165 if not cheer else 178
    rx= 185 if not cheer else 172
    if cheer:
        arms='''<path d="M110 250 Q60 180 70 120" stroke="#8A5CF0" stroke-width="44" stroke-linecap="round" fill="none"/>
<path d="M110 250 Q60 180 70 120" stroke="#B79CFF" stroke-width="30" stroke-linecap="round" fill="none"/>
<path d="M402 250 Q452 180 442 120" stroke="#8A5CF0" stroke-width="44" stroke-linecap="round" fill="none"/>
<path d="M402 250 Q452 180 442 120" stroke="#B79CFF" stroke-width="30" stroke-linecap="round" fill="none"/>
<circle cx="68" cy="114" r="10" fill="#fff" opacity="0.5"/><circle cx="440" cy="114" r="10" fill="#fff" opacity="0.5"/>'''
        sprout='<path d="M256 120 Q250 70 262 40" stroke="#1FBFA0" stroke-width="10" fill="none" stroke-linecap="round"/><path d="M262 44 Q300 10 326 40 Q296 64 262 44Z" fill="url(#leaf)"/><path d="M262 44 Q228 4 202 30 Q230 58 262 44Z" fill="url(#leaf)"/>'
        mouth='<path d="M216 330 Q256 392 296 330 Q256 344 216 330Z" fill="#5A1035"/><path d="M232 352 Q256 376 280 352 Q256 360 232 352Z" fill="#FF6F9C"/>'
        eyes='''<path d="M180 270 Q200 236 220 270" stroke="#1A0F29" stroke-width="12" fill="none" stroke-linecap="round"/><path d="M292 270 Q312 236 332 270" stroke="#1A0F29" stroke-width="12" fill="none" stroke-linecap="round"/>'''
        fx='''<g fill="#FFC94D"><path d="M60 50 l5 15 l15 5 l-15 5 l-5 15 l-5 -15 l-15 -5 l15 -5z"/><path d="M450 40 l4 12 l12 4 l-12 4 l-4 12 l-4 -12 l-12 -4 l12 -4z"/></g><g fill="#fff"><path d="M120 30 l3 9 l9 3 l-9 3 l-3 9 l-3 -9 l-9 -3 l9 -3z"/><path d="M400 90 l3 8 l8 3 l-8 3 l-3 8 l-3 -8 l-8 -3 l8 -3z"/></g>'''
    else:
        arms='''<ellipse cx="88" cy="330" rx="30" ry="40" fill="#8A5CF0" transform="rotate(-25 88 330)"/><ellipse cx="88" cy="326" rx="22" ry="32" fill="#B79CFF" transform="rotate(-25 88 330)"/>
<ellipse cx="424" cy="330" rx="30" ry="40" fill="#8A5CF0" transform="rotate(25 424 330)"/><ellipse cx="424" cy="326" rx="22" ry="32" fill="#B79CFF" transform="rotate(25 424 330)"/>'''
        sprout='<path d="M256 140 Q244 96 262 66" stroke="#1FBFA0" stroke-width="10" fill="none" stroke-linecap="round"/><path d="M262 70 Q296 40 322 66 Q292 90 262 70Z" fill="url(#leaf)"/>'
        mouth='<path d="M226 332 Q256 366 286 332 Q256 342 226 332Z" fill="#5A1035"/><path d="M242 346 Q256 358 270 346Z" fill="#FF6F9C"/>'
        eyes='''<ellipse cx="200" cy="262" rx="30" ry="36" fill="url(#eye)"/><ellipse cx="312" cy="262" rx="30" ry="36" fill="url(#eye)"/>
<circle cx="190" cy="248" r="11" fill="#fff"/><circle cx="302" cy="248" r="11" fill="#fff"/><circle cx="210" cy="278" r="5" fill="#fff" opacity="0.85"/><circle cx="322" cy="278" r="5" fill="#fff" opacity="0.85"/>
<ellipse cx="200" cy="286" rx="18" ry="5" fill="#8A5CF0" opacity="0.5"/>'''
        fx=''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">{body}
<ellipse cx="256" cy="478" rx="150" ry="18" fill="#000" opacity="0.28"/>
{fx}{arms}{sprout}
<ellipse cx="256" cy="{by}" rx="{rx}" ry="{ry}" fill="url(#pb)"/>
<ellipse cx="256" cy="{by+40}" rx="{rx-40}" ry="{ry-60}" fill="url(#pin)"/>
<ellipse cx="190" cy="{by-110}" rx="62" ry="28" fill="#fff" opacity="0.55" transform="rotate(-20 190 {by-110})"/>
<circle cx="148" cy="{by-120}" r="9" fill="#fff" opacity="0.9"/>
<ellipse cx="256" cy="{by+ry-12}" rx="{rx-50}" ry="10" fill="#4A2690" opacity="0.35"/>
{eyes}
<ellipse cx="160" cy="318" rx="24" ry="14" fill="#FF6F9C" opacity="0.55"/><ellipse cx="352" cy="318" rx="24" ry="14" fill="#FF6F9C" opacity="0.55"/>
{mouth}</svg>'''

manifest=[]
def add(rel,use,ai=False):
    manifest.append({"file":rel,"use":use})

# blocks
for n in COLORS:
    save_scales(block_svg(n),64,f"blocks/block_{n}")
idx={"peach":0,"mint":1,"lilac":2,"honey":3,"berry":4}
save_scales(frosted_overlay(),64,"blocks/overlay_frost_aging")
# crystal
save_scales(crystal_svg("intact"),64,"crystal/crystal_intact")
save_scales(crystal_svg("cracked"),64,"crystal/crystal_cracked")
N=6
for s in (1,2,3):
    frames=[render(shatter_svg(f,N),96*s,96*s) for f in range(N)]
    sheet=Image.new("RGBA",(96*s*N,96*s))
    for i,fr in enumerate(frames):
        sheet.paste(fr,(i*96*s,0))
        if s==2: fr.save(d(f"crystal/shatter/crystal_shatter_{i+1:02d}@2x.png"))
    sheet.save(d(f"crystal/crystal_shatter_sheet@{s}x.png"))
for f in range(N): save_svg(shatter_svg(f,N),f"crystal/shatter/crystal_shatter_{f+1:02d}.svg")
# board, bg, tray
save_svg(bg_svg(),"board/background.svg"); render(bg_svg(),1080,1920).convert("RGB").save(d("board/background_1080x1920.png"))
render(bg_svg(),1080,1920).convert("RGB").save(d("board/background_1080x1920.jpg"),quality=85)
save_svg(board_svg(),"board/board_frame.svg"); render(board_svg(),BW,BH).save(d("board/board_frame.png"))
render(board_svg(),BW//2,BH//2).save(d("board/board_frame@half.png"))
save_svg(tray_svg(),"ui/piece_tray.svg"); render(tray_svg(),TW,TH).save(d("ui/piece_tray.png"))
# powerups
save_scales(icebreaker_svg(),64,"powerups/icon_icebreaker")
save_scales(bomb_svg(),64,"powerups/icon_bomb")
# mascot
for p in ("idle","cheer"):
    sv=pop_svg(p); save_svg(sv,f"mascot/pop_{p}.svg")
    render(sv,512,512).save(d(f"mascot/pop_{p}_512.png")); render(sv,256,256).save(d(f"mascot/pop_{p}_256.png"))
# fx
save_scales(sparkle_svg(),32,"fx/fx_sparkle"); save_scales(sparkle_svg("#FFC94D"),32,"fx/fx_sparkle_honey")
save_scales(shard_svg(),16,"fx/fx_shard"); save_svg(glow_svg(),"fx/fx_row_glow.svg"); render(glow_svg(),512,128).save(d("fx/fx_row_glow.png"))

# ---------- mock screen ----------
def font(sz): return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",sz)
SC=0.84; C2=int(CELL*SC); P2=int(PAD*SC); L2=int(40*SC); bw,bh=int(BW*SC),int(BH*SC)
scr=Image.open(d("board/background_1080x1920.jpg")).convert("RGBA")
dr=ImageDraw.Draw(scr)
dr.text((50,60),"Shatterpop",font=font(72),fill="#FFF4E0",stroke_width=6,stroke_fill="#6B3FC8")
dr.rounded_rectangle((650,64,1030,134),radius=35,fill="#1C102B",outline="#FFC94D",width=3)
dr.text((680,76),"★ 3,480",font=font(42),fill="#FFF4E0")
bx,by=(1080-bw)//2,180
scr.alpha_composite(render(board_svg(),bw,bh),(bx,by))
blk={n:render(block_svg(n),C2,C2) for n in COLORS}
ci=render(crystal_svg("intact"),C2,C2); cc=render(crystal_svg("cracked"),C2,C2); fr=render(frosted_overlay(),C2,C2)
layout=["........","..I...C.","pp.ll..b","pm.lhh.b","mm.....b","........","bm.hh.ll","bb.hhlll","p.C.mmpp","ppcmmmpp"]
mp={"p":"peach","m":"mint","l":"lilac","h":"honey","b":"berry"}
for r,row in enumerate(layout):
    for c,ch in enumerate(row):
        x=bx+P2+c*C2; y=by+P2+L2+r*C2
        if ch in mp: scr.alpha_composite(blk[mp[ch]],(x,y))
        elif ch=="C": scr.alpha_composite(ci,(x,y))
        elif ch=="c": scr.alpha_composite(cc,(x,y))
        elif ch=="I": scr.alpha_composite(blk["lilac"],(x,y)); scr.alpha_composite(fr,(x,y))
ry=by+P2+L2+5*C2-C2//2
scr.alpha_composite(render(glow_svg(),bw,C2*2),(bx,ry))
sp=render(sparkle_svg(),96,96); random.seed(5)
for _ in range(22):
    s_=random.randint(20,70); scr.alpha_composite(sp.resize((s_,s_)),(bx+random.randint(40,bw-80),ry+random.randint(20,C2*2-60)))
k=int(C2*1.5); scr.alpha_composite(render(shatter_svg(2,6),k,k),(bx+P2+1*C2-C2//4,by+P2+L2+8*C2-C2//4))
dr=ImageDraw.Draw(scr); dr.text((bx+bw//2,ry+C2),"+50",font=font(76),fill="#FFC94D",stroke_width=5,stroke_fill="#6B3FC8",anchor="mm")
tw,th=int(TW*0.94),int(TH*0.94); ty=by+bh+16; tx=(1080-tw)//2
scr.alpha_composite(render(tray_svg(),tw,th),(tx,ty))
small=72
def piece(cells,col,ox,oy):
    im=render(block_svg(col),small,small)
    for (r,c) in cells: scr.alpha_composite(im,(ox+c*small,oy+r*small))
sw=(tw-75)/3
piece([(0,0),(1,0),(1,1)],"mint",int(tx+22+sw/2-small),ty+62)
piece([(0,0),(0,1),(1,0),(1,1)],"berry",int(tx+22+sw+15+sw/2-small),ty+62)
piece([(0,0),(0,1),(0,2)],"peach",int(tx+22+2*(sw+15)+sw/2-1.5*small),ty+100)
py=ty+th+8
scr.alpha_composite(render(pop_svg("cheer"),260,260),(40,py-20))
dr.rounded_rectangle((80,py+230,260,py+282),radius=20,fill="#1C102B",outline="#B79CFF",width=2)
dr.text((170,py+256),"Pop ♥",font=font(30),fill="#FFF4E0",anchor="mm")
for i,n in enumerate(["icebreaker","bomb"]):
    ic=render(icebreaker_svg() if i==0 else bomb_svg(),150,150); scr.alpha_composite(ic,(560+i*200,py+10))
    dr.text((560+i*200+75,py+180),n.capitalize(),font=font(30),fill="#FFF4E0",anchor="mm")
scr.convert("RGB").save(d("mock_screen.png"))
print("py",py)
