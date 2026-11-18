import math, random
random.seed(11)
W=H=900
BG='#EBE6D8'
out=[]
def P(x,y): return f'{x:.1f},{y:.1f}'
def leaf(x,y,ang,L,w):
    # pointed leaf with a midrib
    ca,sa=math.cos(ang),math.sin(ang)
    def t(u,v): return (x+u*ca-v*sa, y+u*sa+v*ca)
    a=t(0,0); b=t(L,0); c1=t(L*.35,w); c2=t(L*.7,w*.8); d1=t(L*.7,-w*.8); d2=t(L*.35,-w)
    d=f'M{P(*a)} C{P(*c1)} {P(*c2)} {P(*b)} C{P(*d1)} {P(*d2)} {P(*a)}Z'
    rib=f'M{P(*t(L*.08,0))} L{P(*t(L*.85,0))}'
    return f'<path d="{d}"/>', rib
def petal(cx,cy,ang,L,w):
    ca,sa=math.cos(ang),math.sin(ang)
    def t(u,v): return (cx+u*ca-v*sa, cy+u*sa+v*ca)
    a=t(L*.12,0)
    # rounded petal with a shallow notch at the tip
    p1=t(L*.35,w*1.05); p2=t(L*.95,w*1.1); tipL=t(L,w*.3); notch=t(L*.9,0); tipR=t(L,-w*.3); q2=t(L*.95,-w*1.1); q1=t(L*.35,-w*1.05)
    d=f'M{P(*a)} C{P(*p1)} {P(*p2)} {P(*tipL)} Q{P(*notch)} {P(*tipR)} C{P(*q2)} {P(*q1)} {P(*a)}Z'
    veins=' '.join(f'M{P(*t(L*.2,0))} L{P(*t(L*.8,v*w*.55))}' for v in (-1,0,1))
    return f'<path d="{d}"/>', veins
def stem(x0,y0,x1,y1,bend):
    mx=(x0+x1)/2+bend; my=(y0+y1)/2
    return f'M{P(x0,y0)} Q{P(mx,my)} {P(x1,y1)}', (mx,my)
def qpt(x0,y0,mx,my,x1,y1,t):
    return ((1-t)**2*x0+2*(1-t)*t*mx+t*t*x1, (1-t)**2*y0+2*(1-t)*t*my+t*t*y1)
shapes=[]; lines=[]
def flower(cx,cy,R,rot):
    n=5
    for i in range(n):
        s,v=petal(cx,cy,rot+i*2*math.pi/n+random.uniform(-.08,.08),R*random.uniform(.92,1.05),R*.42)
        shapes.append(s); lines.append(v)
    shapes.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{R*.13:.1f}"/>')
    for k in range(9):
        a=k*2*math.pi/9; shapes.append(f'<circle cx="{cx+math.cos(a)*R*.2:.1f}" cy="{cy+math.sin(a)*R*.2:.1f}" r="{R*.035:.1f}"/>')
def bud(x,y,r,ang):
    for i in (-1.2,-.4,.4,1.2):
        s,_=petal(x,y,ang+i*.42,r*random.uniform(.85,1.05),r*.38); shapes.append(s)
    shapes.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r*.22:.1f}"/>')
def big_stem(fx,fy,R,length,bend):
    x1,y1=fx+bend*1.6,fy+length
    d,(mx,my)=stem(fx,fy+R*.1,x1,y1,bend); lines.append(d)
    for t in (.35,.6,.82):
        x,y=qpt(fx,fy,mx,my,x1,y1,t); side=random.choice((-1,1))
        s,r=leaf(x,y,-math.pi/2+side*random.uniform(.6,1.0),random.uniform(58,80),random.uniform(11,15)); shapes.append(s); lines.append(r)
def sprig(x0,y0,length,bend):
    x1,y1=x0+bend*1.3,y0-length
    d,(mx,my)=stem(x0,y0,x1,y1,bend); lines.append(d)
    for t in (.45,.7,.9):
        x,y=qpt(x0,y0,mx,my,x1,y1,t); side=1 if t!=0.7 else -1
        bx=x+side*random.uniform(30,52); by=y-random.uniform(26,44)
        lines.append(f'M{P(x,y)} Q{P((x+bx)/2,y-4)} {P(bx,by)}')
        bud(bx,by,random.uniform(15,20),-math.pi/2+side*.45)
        s,r=leaf(x,y,-math.pi/2-side*random.uniform(.7,1.1),random.uniform(36,52),random.uniform(8,11)); shapes.append(s); lines.append(r)
    bud(x1,y1,19,-math.pi/2+bend*.004)
items=[('f',230,150,88,.35,330,-40),('f',700,90,82,1.15,300,35),('f',170,660,92,.75,300,30),('f',720,560,78,.2,320,-35),('f',470,390,60,.9,220,15),
       ('s',420,560,330,55),('s',850,900,330,-45),('s',70,470,300,40),('s',520,900,280,-35),('s',330,320,230,35),('s',610,330,200,-30),('s',40,890,240,30)]
for it in items:
    if it[0]=='f':
        _,x,y,R,rot,L,b=it; big_stem(x,y,R,L,b); flower(x,y,R,rot)
    else:
        _,x,y,L,b=it; sprig(x,y,L,b)
body=''.join(shapes)
ln=' '.join(lines)
def tiled(content):
    return ''.join(f'<g transform="translate({dx},{dy})">{content}</g>' for dx in (-W,0,W) for dy in (-H,0,H))
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
<filter id="paper" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".75" numOctaves="4" seed="4"/><feColorMatrix values="0 0 0 0 .45  0 0 0 0 .42  0 0 0 0 .36  0 0 0 .11 0"/></filter>
<filter id="emb" x="-5%" y="-5%" width="110%" height="110%">
 <feGaussianBlur in="SourceAlpha" stdDeviation="1.1" result="b"/>
 <feOffset in="b" dx="1.4" dy="1.8" result="sh"/><feComposite in="sh" in2="SourceAlpha" operator="out" result="shOut"/>
 <feFlood flood-color="#9A927F" flood-opacity=".55"/><feComposite in2="shOut" operator="in" result="shadow"/>
 <feOffset in="b" dx="-1.1" dy="-1.3" result="hl"/><feComposite in="hl" in2="SourceAlpha" operator="out" result="hlOut"/>
 <feFlood flood-color="#FFFFFF" flood-opacity=".95"/><feComposite in2="hlOut" operator="in" result="hilite"/>
 <feOffset in="b" dx="1" dy="1.2" result="inS"/><feComposite in="SourceAlpha" in2="inS" operator="out" result="rim"/>
 <feFlood flood-color="#FFFFFF" flood-opacity=".5"/><feComposite in2="rim" operator="in" result="rimHL"/>
 <feMerge><feMergeNode in="shadow"/><feMergeNode in="hilite"/><feMergeNode in="SourceGraphic"/><feMergeNode in="rimHL"/></feMerge>
</filter>
</defs>
<rect width="{W}" height="{H}" fill="{BG}"/>
<g filter="url(#emb)">
 <g fill="{BG}">{tiled(body)}</g>
 <g fill="none" stroke="{BG}" stroke-width="2.3" stroke-linecap="round">{tiled(f'<path d="{ln}"/>')}</g>
</g>
<g fill="none" stroke="#DDD6C5" stroke-width=".7" stroke-linecap="round" opacity=".7">{tiled(f'<path d="{" ".join(l for l in lines if l.count("L")==1 or "Q" not in l)}"/>')}</g>
<rect width="{W}" height="{H}" filter="url(#paper)"/>
</svg>'''
open('/Users/ducky/.openclaw/workspace/outputs/modern-balance-therapy/deploy/assets/emboss-flowers.svg','w').write(svg)
print(len(svg))
