import json,os,io,urllib.request,glob,shutil
from PIL import Image,ImageEnhance,ImageOps
SRC='/private/tmp/claude-502/-Users-ducky/572e0311-2aa7-4266-94e2-2f621f081be4/scratchpad/src'
M='/Users/ducky/.openclaw/workspace/outputs/modern-balance-therapy/deploy/assets/media'; RAW=M+'/_raw'
# wipe previous photo outputs and raw (rawpixel watermarked)
for f in glob.glob(M+'/*.webp'): os.remove(f)
for f in glob.glob(RAW+'/*'): os.remove(f)
c2=json.load(open(SRC+'/cands2.json')); byk={c['key']:c for L in c2.values() for c in L}
plan={ # name: (key, ratio, grade_strength)
 'frame-stones':('b92364610a',3/4,1.0),'frame-grass':('0ce024b6f7',1.0,1.0),'band-mist':('32fb471031',16/7,1.6),
 'thumb-need-therapy':('60e1c85c55',1.5,1.0),'thumb-affordable':('dc2a290b01',1.5,1.0),'thumb-first-session':('a6859e15b5',1.5,1.0),
 'thumb-online':('d04803a098',1.5,1.0),'thumb-trauma':('5328d7ff6c',1.5,1.0),'thumb-anxiety':('1ab2409e6c',1.5,1.0),
 'thumb-depression':('47ce60ee9c',1.5,1.0),'thumb-couples':('e19ba926b0',1.5,1.0),'thumb-teen':('4599f5ca3f',1.5,1.0),'thumb-how-long':('c62cb33763',1.5,1.0)}
alts={'frame-stones':['d848956ac4','2dacb56044','928f148030'],'frame-grass':['a6859e15b5','4bdc0ca93c','a8a0f586f0'],'band-mist':['47ce60ee9c','0ce024b6f7','4977691606']}
need=set(k for k,_,_ in plan.values())|set(k for v in alts.values() for k in v)
picked={}
for k in need:
    c=byk[k]; url=c['url']; hdr={'User-Agent':'DuckyMBT/1.0 (quickj10@live.com)'} if 'wikimedia' in url else {'User-Agent':'Mozilla/5.0 (Macintosh)'}
    d=urllib.request.urlopen(urllib.request.Request(url,headers=hdr),timeout=180).read(); im=Image.open(io.BytesIO(d)); im.load()
    p=f"{RAW}/{k}.jpg"; open(p,'wb').write(d); picked[k]=dict(c,file=os.path.basename(p),w=im.width,h=im.height); print('got',k,im.width,im.height,c['src'])
def grade(im,s=1.0):
    im=im.convert('RGB'); im=ImageEnhance.Color(im).enhance(max(0.3,1-0.16*s))
    lift=int(12*s); 
    lr=[min(255,int(lift+v*((255-lift)/255))) for v in range(256)]; lb=[min(255,int(lift+v*((252-lift)/255))) for v in range(256)]
    r,g,b=im.split(); return Image.merge('RGB',(r.point(lr),g.point(lr),b.point(lb)))
def fit(im,ratio):
    w,h=im.size
    if w/h>ratio: nw=int(h*ratio); return im.crop(((w-nw)//2,0,(w-nw)//2+nw,h))
    nh=int(w/ratio); return im.crop((0,(h-nh)//2,w,(h-nh)//2+nh))
res={}
for name,(k,ratio,s) in plan.items():
    im=ImageOps.exif_transpose(Image.open(f"{RAW}/{k}.jpg")); im=grade(fit(im,ratio),s)
    W=1600 if not name.startswith('thumb') else 1200
    big=im.resize((W,round(im.height*W/im.width)),Image.LANCZOS); big.save(f"{M}/{name}.webp",quality=80,method=6)
    sm=im.resize((800,round(im.height*800/im.width)),Image.LANCZOS); sm.save(f"{M}/{name}-800.webp",quality=78,method=6)
    res[name]={'file':name+'.webp','w':big.width,'h':big.height,'key':k}; print(name,big.size)
os.makedirs(SRC+'/altprev',exist_ok=True)
for f in glob.glob(SRC+'/altprev/*'): os.remove(f)
for slot,ks in alts.items():
    for k in ks:
        im=grade(ImageOps.exif_transpose(Image.open(f"{RAW}/{k}.jpg"))); im.thumbnail((800,800)); im.save(f"{SRC}/altprev/{slot}_{k}.jpg",quality=80)
json.dump({'picked':picked,'res':res,'plan':{k:v[0] for k,v in plan.items()},'alts':alts},open(SRC+'/processed.json','w'),indent=1)
use={'frame-stones':'Focus section frame','frame-grass':'Mirror section frame','band-mist':'Full-bleed band','thumb-need-therapy':'Blog: need therapy','thumb-affordable':'Blog: affordable therapy','thumb-first-session':'Blog: first session','thumb-online':'Blog: online therapy','thumb-trauma':'Blog: trauma','thumb-anxiety':'Blog: stress vs anxiety','thumb-depression':'Blog: high-functioning depression','thumb-couples':'Blog: couples','thumb-teen':'Blog: teens','thumb-how-long':'Blog: how long'}
L=['# Media credits and licenses (Modern Balance Therapy)','',"Every shipped item is licensed for free commercial use without attribution (CC0 / Public Domain via the WordPress Photo Directory and Wikimedia Commons, Mixkit License for video). Credits are recorded anyway. Ally's reference images (design-references/modern-balance-therapy/round2) were NOT used anywhere. Earlier rawpixel candidates were dropped because their free previews are watermarked.",'','Grading toward the site palette (noted per the brief): photos get saturation reduced about 16 percent, blacks lifted about 5 percent, a touch of warmth (blue channel slightly lower). The band image is graded harder (saturation about 25 percent lower, blacks lifted 7 percent) to pull a pink dandelion macro toward peach and cream. The hero video was graded in ffmpeg (eq saturation 0.8, brightness +0.03, contrast 0.96, curves lift) and loop-crossfaded over 0.6 s.','','## Hero video','','| File | Source | License | Notes |','|---|---|---|---|','| hero.mp4, hero.webm, hero-poster.jpg | Mixkit, "Dandelions in spring", https://mixkit.co/free-stock-video/dandelions-in-spring-34706/ | Mixkit License (free for commercial and personal use, no attribution) | 1280x720 source, 1 s to 10 s, graded, 9 s loop |','| alternate, not shipped | Mixkit, "A tranquil forest amids the morning mist", https://mixkit.co/free-stock-video/a-tranquil-forest-amids-the-morning-mist-50867/ | Mixkit License | 1080p available |','| alternate, not shipped | Mixkit, "Close up of a full dandelion", https://mixkit.co/free-stock-video/close-up-of-a-full-dandelion-45332/ | Mixkit License | 720p |','','## Photos (shipped)','','| File | Used for | Source page | Creator | License | Native size |','|---|---|---|---|---|---|']
for name,r in res.items():
    m=picked[r['key']]; L.append(f"| {r['file']} and {name}-800.webp | {use[name]} | {m['page']} | {m.get('creator') or 'unknown'} | {m['lic'].upper()} ({m['src']}) | {m['w']}x{m['h']} |")
L+=['','## Alternates (kept in _raw, not shipped)','']
for slot,ks in alts.items():
    for k in ks: m=picked[k]; L.append(f"- {slot}: {m['title']} | {m['page']} | {m.get('creator') or 'unknown'} | {m['lic'].upper()} | {m['w']}x{m['h']}")
L+=['','## Swapping a pick','Put the new source file in assets/media/_raw, change the key in the plan inside assets/media/process.py (copy of the processing script), run it, then `python3 -I deploy/wrap_home.py` and `python3 -I deploy/blog/build.py`. Sizes: frames 1600 px wide, thumbnails 1200 px plus 800 px card versions, all WebP quality 80.']
open(M+'/CREDITS.md','w').write('\n'.join(L)+'\n'); shutil.copy(__file__,M+'/process.py'); print('credits ok')
