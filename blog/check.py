#!/usr/bin/env python3
"""Check every built page under deploy/: one H1, title <= 65, description 120-165, JSON-LD parses,
relative links resolve to files, external reference URLs answer, no em dashes. Exit 1 on any failure.
  python3 -I blog/check.py [--no-net]
"""
import re, sys, json, html, pathlib, subprocess, urllib.parse
from html.parser import HTMLParser

DEPLOY = pathlib.Path(__file__).resolve().parent.parent
NET = '--no-net' not in sys.argv
pages = [p for p in DEPLOY.rglob('*.html') if '_src' not in p.parts and not p.name.startswith('_') and 'index.v' not in p.name]
pages.sort()

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.h1=0; s.title=None; s.desc=None; s.ld=[]; s.links=[]; s.extrefs=[]; s._t=False; s._ld=False; s._refs=False; s.robots=None
    def handle_starttag(s, tag, attrs):
        a=dict(attrs)
        if tag=='h1': s.h1+=1
        if tag=='title': s._t=True
        if tag=='meta' and a.get('name')=='description': s.desc=a.get('content','')
        if tag=='meta' and a.get('name')=='robots': s.robots=a.get('content','')
        if tag=='script' and a.get('type')=='application/ld+json': s._ld=True
        if tag=='section' and 'refs' in (a.get('class') or ''): s._refs=True
        if tag=='a' and a.get('href'):
            h=a['href']
            if s._refs and h.startswith('http'): s.extrefs.append(h)
            elif not h.startswith(('http','mailto:','tel:','data:','#','javascript:')): s.links.append(h)
    def handle_endtag(s, tag):
        if tag=='title': s._t=False
        if tag=='script': s._ld=False
        if tag=='section': s._refs=False
    def handle_data(s, d):
        if s._t: s.title=(s.title or '')+d
        if s._ld: s.ld.append(d)

fails=0; rows=[]
ext_seen={}
def head(url):
    if url in ext_seen: return ext_seen[url]
    try:
        code=subprocess.run(['curl','-sIL','-o','/dev/null','-w','%{http_code}','--max-time','20','-A','Mozilla/5.0 (compatible; MBT-linkcheck)',url],capture_output=True,text=True,timeout=30).stdout.strip()
        if code in ('403','405','429','000'):
            code=subprocess.run(['curl','-sL','-o','/dev/null','-w','%{http_code}','--max-time','25','-A','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36',url],capture_output=True,text=True,timeout=35).stdout.strip()
    except Exception:
        code='ERR'
    ext_seen[url]=code; return code

for pg in pages:
    txt=pg.read_text(encoding='utf-8'); p=P(); p.feed(txt)
    rel=pg.relative_to(DEPLOY).as_posix(); probs=[]
    if p.h1!=1: probs.append('h1=%d'%p.h1)
    t=(p.title or '').strip()
    if not t: probs.append('no title')
    elif len(t)>65: probs.append('title %d chars'%len(t))
    if p.desc is None: probs.append('no description')
    elif not (120<=len(p.desc)<=165): probs.append('description %d chars'%len(p.desc))
    if not p.ld: probs.append('no JSON-LD')
    for i,blob in enumerate(p.ld):
        try: json.loads(blob.replace('<\\/','</'))
        except Exception as e: probs.append('JSON-LD #%d invalid: %s'%(i+1,e))
    for h in p.links:
        target=urllib.parse.unquote(h.split('#')[0].split('?')[0])
        if not target: continue
        dest=(pg.parent/target).resolve()
        if dest.is_dir(): dest=dest/'index.html'
        if not dest.exists(): probs.append('broken link %s'%h)
    if '—' in txt: probs.append('em dash')
    bad_ext=[]
    if NET:
        for u in p.extrefs:
            c=head(u)
            if not (c.startswith('2') or c.startswith('3')):
                (bad_ext if c!='403' else []).append('%s -> %s'%(u,c))
                if c=='403': rows.append(('  note', rel, '403 (publisher blocks bots): '+u))
    probs+=['ext '+b for b in bad_ext]
    status='PASS' if not probs else 'FAIL'
    if probs: fails+=1
    rows.append((status, rel, '; '.join(probs) if probs else 'title %d, desc %d, ld %d, links %d, refs %d%s'%(len(t),len(p.desc or ''),len(p.ld),len(p.links),len(p.extrefs),'' if not p.robots else ', robots='+p.robots)))

w=max(len(r[1]) for r in rows) if rows else 10
for st,rel,msg in rows: print('%-5s %-*s %s'%(st,w,rel,msg))
print('\n%d page(s), %d failing'%(len(pages),fails))
sys.exit(1 if fails else 0)
