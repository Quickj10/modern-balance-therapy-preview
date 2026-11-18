import numpy as np
from PIL import Image, ImageFilter
D='/private/tmp/claude-502/-Users-ducky/572e0311-2aa7-4266-94e2-2f621f081be4/scratchpad/press/'
OUT='/Users/ducky/.openclaw/workspace/outputs/modern-balance-therapy/deploy/assets/media/'
names=['press-seedling','press-swirl','press-doorway']
sheet=Image.open(D+'masks.png').convert('L')
def blur(a,r):
    return np.asarray(Image.fromarray((a*255).astype('uint8')).filter(ImageFilter.GaussianBlur(r)),dtype=np.float32)/255
for n,name in enumerate(names):
    m=np.asarray(sheet.crop((0,n*512,512,n*512+512)),dtype=np.float32)/255
    m=1-m  # stroke=1
    # rounded pillow profile: wide soft shoulder plus a tighter crown
    h=0.7*blur(m,9)+0.3*blur(m,4.5)
    h=h/ h.max()
    gy,gx=np.gradient(h*20)
    nx,ny,nz=-gx,-gy,np.ones_like(h)
    L=np.array([-0.55,-0.65,0.52]); L=L/np.linalg.norm(L)
    nrm=np.sqrt(nx**2+ny**2+nz**2)
    shade=(nx*L[0]+ny*L[1]+nz*L[2])/nrm
    flat=L[2]
    d=shade-flat
    hi=np.clip(d*3.0,0,1)**0.8
    lo=np.clip(-d*1.6,0,1)**1.1
    # soft cast shadow below/right of the raised form
    cast=np.roll(np.roll(blur(m,9),10,axis=0),8,axis=1)
    cast=np.clip(cast*1.4-blur(m,3)*1.2,0,1)*0.08
    # paper fibre noise only where there is relief
    rng=np.random.default_rng(3); noise=(rng.random(m.shape).astype(np.float32)-.5)*0.08
    a_hi=np.clip(hi*0.95+noise*hi,0,1)
    a_lo=np.clip(np.maximum(lo*0.34,cast)+noise*lo,0,1)
    # composite: white highlight over warm-brown shadow, premultiplied into one RGBA
    sh=np.array([122,110,88],dtype=np.float32); wh=np.array([255,253,248],dtype=np.float32)
    A=a_hi+a_lo*(1-a_hi)
    C=(wh[None,None,:]*a_hi[...,None]+sh[None,None,:]*(a_lo*(1-a_hi))[...,None])/np.maximum(A[...,None],1e-6)
    rgba=np.dstack([C,A[...,None]*255]).clip(0,255).astype('uint8')
    im=Image.fromarray(rgba).resize((168,168),Image.LANCZOS)
    im.save(OUT+name+'.png',optimize=True)
    # preview on page cream
    for bg,tag in (((244,239,228),'new'),((237,232,218),'old')):
        b=Image.new('RGBA',(168,168),bg+(255,)); b.alpha_composite(im); b.convert('RGB').resize((336,336)).save(D+f'prev-{name}-{tag}.png')
print('ok')
