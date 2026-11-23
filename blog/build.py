#!/usr/bin/env python3
"""Build the Modern Balance Therapy blog.

  python3 -I blog/build.py            # preview build (noindex meta on every page)
  python3 -I blog/build.py --launch   # drops the preview noindex lines

Reads  blog/_src/<slug>.json (see _src/SPEC.md), blog/_src/TOPICS.json, blog/_template.html,
       blog/_article.css and src/home.html (shared header, footer, crisis strip, CSS).
Writes blog/<slug>/index.html, blog/index.html, assets/blog.css, assets/blog.js,
       sitemap.xml, robots.txt, llms.txt (deploy root).
Fails loudly on a missing field or an unverified reference.
"""
import json, re, sys, html, pathlib, datetime

HERE = pathlib.Path(__file__).resolve().parent          # deploy/blog
DEPLOY = HERE.parent                                     # deploy
SITE_SRC = DEPLOY / 'src' / 'home.html'                  # artifact-contract home page (copied in from outputs/modern-balance-therapy/site)
SRC = HERE / '_src'
BASE = 'https://modernbalancetherapy.com/'
LAUNCH = '--launch' in sys.argv
PREVIEW_HOST = 'https://quickj10.github.io/modern-balance-therapy-preview/'
TODAY = '2026-11-18'
NOINDEX = '' if LAUNCH else '<meta name="robots" content="noindex,nofollow"><!-- PREVIEW ONLY: remove at launch -->\n'
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 34 34'%3E"
           "%3Cellipse cx='17' cy='28.5' rx='13' ry='4.5' fill='%238CA48D'/%3E%3Cellipse cx='16' cy='19.5' rx='9.5' ry='4' fill='%23CFC5E9'/%3E"
           "%3Cellipse cx='17.5' cy='11.5' rx='6' ry='3.4' fill='%236B5CAB'/%3E%3C/svg%3E")
STONES_SVG = ('<svg viewBox="0 0 34 34" aria-hidden="true"><ellipse cx="17" cy="28.5" rx="13" ry="4.5" fill="#8CA48D"/>'
              '<ellipse cx="16" cy="19.5" rx="9.5" ry="4" fill="#CFC5E9"/><ellipse cx="17.5" cy="11.5" rx="6" ry="3.4" fill="#6B5CAB"/></svg>')
REQUIRED = ['slug','title','meta_description','direct_answer','key_takeaways','body_html','faqs','references',
            'reading_minutes','date_published','keywords','excerpt']
REF_REQUIRED = ['n','authors','year','title','source','url','verified']
THUMB_DEFAULT = {'how-do-you-know-if-you-need-therapy':'thumb-need-therapy','affordable-therapy-without-insurance':'thumb-affordable',
  'what-to-expect-first-therapy-session':'thumb-first-session','does-online-therapy-work':'thumb-online','signs-of-unresolved-trauma':'thumb-trauma',
  'stress-vs-anxiety-when-to-get-help':'thumb-anxiety','high-functioning-depression':'thumb-depression','when-should-couples-go-to-therapy':'thumb-couples',
  'does-my-teen-need-therapy':'thumb-teen','how-long-does-therapy-take':'thumb-how-long'}
THUMB_ALT = {'thumb-need-therapy':'A quiet path disappearing into morning fog','thumb-affordable':'Smooth grey pebbles packed closely together',
  'thumb-first-session':'A country road on a foggy morning with one tall tree','thumb-online':'Still water reflecting a soft, cloudy sky',
  'thumb-trauma':'A single small stone resting on pale sand','thumb-anxiety':'A still mountain lake under low cloud',
  'thumb-depression':'A lone conifer standing in pale haze','thumb-couples':'Two gulls gliding over mirror-still water',
  'thumb-teen':'A dandelion seed head against soft green','thumb-how-long':'Wind ripples in pale sand'}
def thumb_of(d): return d.get('thumb') or THUMB_DEFAULT.get(d['slug'],'thumb-need-therapy')
def thumb_alt_of(d): return d.get('thumb_alt') or THUMB_ALT.get(thumb_of(d),'Calm nature photograph')

def die(msg):
    print('BUILD FAILED:', msg, file=sys.stderr); sys.exit(1)

def esc(t): return html.escape(str(t), quote=True)

def human_date(iso):
    d = datetime.date.fromisoformat(iso)
    return d.strftime('%B %-d, %Y')

def words(h): return len(re.sub(r'<[^>]+>', ' ', h).split())

# ---------- shared pieces from the home page ----------
home = SITE_SRC.read_text(encoding='utf-8')
css_all = home.split('<style>',1)[1].split('</style>',1)[0]

def css_block(start_marker, end_marker=None):
    i = css_all.index(start_marker)
    j = css_all.index(end_marker, i) if end_marker else len(css_all)
    return css_all[i:j]

shared_css = (css_block(':root{', '/* hero */')
              + css_block('/* crisis */', '/* footer */')
              + css_block('/* contact / form */', '/* crisis */')
              + css_block('/* footer */', '/* stacking stones') )
# the home page's reduced-motion catch-all, trimmed to what blog pages use
shared_css += '\n@media (prefers-reduced-motion: reduce){ .btn,.stones .s{transition:none !important} }\n'

def html_block(open_tag_prefix, close_tag):
    i = home.index(open_tag_prefix)
    j = home.index(close_tag, i) + len(close_tag)
    return home[i:j]

header_html = html_block('<header class="site">', '</header>')
footer_html = html_block('<footer class="site">', '</footer>')
crisis_html = html_block('<aside class="crisis"', '</aside>')
callbar_html = html_block('<nav class="callbar"', '</nav>')

def relink(fragment, root):
    """Point home-page anchors and the blog link at the right place from a sub-page."""
    fragment = fragment.replace('href="#top"', 'href="%s"' % root)
    fragment = re.sub(r'href="#([a-z]+)"', lambda m: 'href="%s#%s"' % (root, m.group(1)), fragment)
    fragment = fragment.replace('href="blog/"', 'href="%sblog/"' % root)
    for sub in ('referral/', 'privacy/', 'hipaa/', 'good-faith-estimate/'):
        fragment = fragment.replace('href="%s"' % sub, 'href="%s%s"' % (root, sub))
    fragment = fragment.replace('id="stones"', '')  # no easter egg wiring on blog pages
    return fragment

BLOG_JS = r"""(function(){
  var yr=document.getElementById('yr'); if(yr) yr.textContent=new Date().getFullYear();
  var hdr=document.querySelector('header.site'), btn=document.querySelector('.menu-btn'), panel=document.getElementById('mnav');
  if(!hdr||!btn||!panel) return;
  function setOpen(on){
    hdr.classList.toggle('open',on); panel.hidden=!on; document.documentElement.classList.toggle('menu-open',on);
    btn.setAttribute('aria-expanded',on?'true':'false'); btn.setAttribute('aria-label',on?'Close menu':'Open menu');
    document.body.style.overflow=on?'hidden':'';
  }
  btn.addEventListener('click',function(){ setOpen(panel.hidden); });
  panel.addEventListener('click',function(e){ if(e.target.closest('a')) setOpen(false); });
  document.addEventListener('keydown',function(e){ if(e.key==='Escape' && !panel.hidden){ setOpen(false); btn.focus(); } });
  document.addEventListener('click',function(e){ if(!panel.hidden && !hdr.contains(e.target)) setOpen(false); });
  window.addEventListener('resize',function(){ if(window.innerWidth>900 && !panel.hidden) setOpen(false); });
})();
"""

# ---------- load sources ----------
topics = json.loads((SRC / 'TOPICS.json').read_text(encoding='utf-8'))
order = {t['slug']: t['n'] for t in topics}
titles = {t['slug']: t['title'] for t in topics}

posts = []
for p in sorted(SRC.glob('*.json')):
    if p.name == 'TOPICS.json': continue
    try:
        d = json.loads(p.read_text(encoding='utf-8'))
    except Exception as e:
        die('%s is not valid JSON: %s' % (p.name, e))
    missing = [k for k in REQUIRED if k not in d or d[k] in ('', [], None)]
    if missing: die('%s missing fields: %s' % (p.name, ', '.join(missing)))
    if d['slug'] != p.stem: die('%s: slug %r does not match filename' % (p.name, d['slug']))
    if d['slug'] not in order: die('%s: slug not in TOPICS.json' % p.name)
    if d['title'] != titles[d['slug']]: die('%s: title differs from TOPICS.json' % p.name)
    if len(d['faqs']) != 3: die('%s: needs exactly 3 faqs' % p.name)
    for r in d['references']:
        miss = [k for k in REF_REQUIRED if k not in r]
        if miss: die('%s: reference missing %s' % (p.name, miss))
        if r.get('verified') is not True: die('%s: reference %s is not verified:true' % (p.name, r['n']))
        if not str(r['url']).startswith('http'): die('%s: reference %s has no http url' % (p.name, r['n']))
    if not (4 <= len(d['references']) <= 8): die('%s: needs 4 to 8 references, has %d' % (p.name, len(d['references'])))
    if not (140 <= len(d['meta_description']) <= 165): die('%s: meta_description is %d chars (140 to 165)' % (p.name, len(d['meta_description'])))
    if '—' in json.dumps(d, ensure_ascii=False): die('%s: contains an em dash' % p.name)
    d.setdefault('date_modified', d['date_published'])
    posts.append(d)
posts.sort(key=lambda d: order[d['slug']])
print('posts found:', len(posts))

# ---------- render helpers ----------
template = (HERE / '_template.html').read_text(encoding='utf-8')

def render(tpl, ctx):
    out = tpl
    for k, v in ctx.items():
        out = out.replace('{{%s}}' % k, str(v))
    left = re.findall(r'\{\{([a-z_]+)\}\}', out)
    if left: die('unfilled placeholders: %s' % sorted(set(left)))
    return out

def ref_li(r):
    link = '<a href="%s" rel="noopener" target="_blank">%s</a>' % (esc(r['url']), esc(r.get('doi_or_id') or r['url']))
    return ('<li id="ref-%d">%s (%s). %s <cite>%s</cite>. %s</li>'
            % (int(r['n']), esc(r['authors']), esc(r['year']), esc(r['title']).rstrip('.') + '.', esc(r['source']), link))

def faq_html(faqs):
    return '\n'.join('<details><summary>%s</summary><p>%s</p></details>' % (esc(f['q']), esc(f['a'])) for f in faqs)

def more_html(current, root):
    others = [p for p in posts if p['slug'] != current][:3]
    return '\n'.join('<li><a href="%sblog/%s/">%s<span>%d min</span></a></li>' % (root, esc(p['slug']), esc(p['title']), int(p['reading_minutes'])) for p in others)

def jsonld_post(d, url):
    wc = words(d['body_html'])
    g = {"@context": "https://schema.org", "@graph": [
        {"@type": "BlogPosting", "@id": url + "#post", "headline": d['title'], "description": d['meta_description'],
         "url": url, "mainEntityOfPage": {"@type": "WebPage", "@id": url},
         "datePublished": d['date_published'], "dateModified": d['date_modified'],
         "author": {"@type": "Person", "@id": BASE + "#jackie", "name": "Jackie McGreggor", "honorificSuffix": "MA, LPC",
                    "jobTitle": "Licensed Professional Counselor", "url": BASE + "#about"},
         "publisher": {"@type": "Organization", "@id": BASE + "#practice", "name": "Modern Balance Therapy", "url": BASE,
                       "logo": {"@type": "ImageObject", "url": BASE + "assets/media/hero-poster.jpg"}},
         "image": {"@type": "ImageObject", "url": BASE + "assets/media/" + thumb_of(d) + ".webp", "width": 1200, "height": 800}, "keywords": ", ".join(d['keywords']), "wordCount": wc,
         "articleSection": "Mental health", "inLanguage": "en-US", "isAccessibleForFree": True,
         "about": [{"@type": "Thing", "name": k} for k in d['keywords'][:5]],
         "citation": [{"@type": "CreativeWork", "name": r['title'], "author": r['authors'], "datePublished": str(r['year']), "url": r['url']} for r in d['references']],
         "isPartOf": {"@id": BASE + "#website"}},
        {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [{"@type": "Question", "name": f['q'], "acceptedAnswer": {"@type": "Answer", "text": f['a']}} for f in d['faqs']]},
        {"@type": "BreadcrumbList", "@id": url + "#crumbs", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": BASE + "blog/"},
            {"@type": "ListItem", "position": 3, "name": d['title'], "item": url}]}
    ]}
    return json.dumps(g, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')

# ---------- article pages ----------
(DEPLOY / 'assets').mkdir(exist_ok=True)
(DEPLOY / 'assets' / 'blog.css').write_text(shared_css + '\n' + (HERE / '_article.css').read_text(encoding='utf-8'), encoding='utf-8')
(DEPLOY / 'assets' / 'blog.js').write_text(BLOG_JS, encoding='utf-8')

for d in posts:
    root = '../../'
    url = BASE + 'blog/' + d['slug'] + '/'
    title_tag = d['title'] if len(d['title']) <= 65 else d['title'].split(':')[0].split('(')[0].strip().rstrip(',')
    if len(title_tag) > 65: title_tag = title_tag[:62].rsplit(' ', 1)[0]
    crumb = d['title'].split(':')[0].split('?')[0].split('(')[0].strip()
    ctx = dict(
        noindex=NOINDEX, title_tag=esc(title_tag), title=esc(d['title']), meta_description=esc(d['meta_description']),
        canonical=url, favicon=FAVICON, root=root, slug=d['slug'], crumb=esc(crumb),
        date_published=d['date_published'], date_modified=d['date_modified'], date_human=human_date(d['date_published']),
        reading_minutes=int(d['reading_minutes']), direct_answer=esc(d['direct_answer']),
        key_takeaways_html=''.join('<li>%s</li>' % esc(t) for t in d['key_takeaways']),
        body_html=d['body_html'], faqs_html=faq_html(d['faqs']),
        references_html='\n'.join(ref_li(r) for r in sorted(d['references'], key=lambda r: int(r['n']))),
        more_articles_html=more_html(d['slug'], root), jsonld=jsonld_post(d, url), stones_svg=STONES_SVG,
        header=relink(header_html, root), footer=relink(footer_html, root), crisis=crisis_html, callbar=relink(callbar_html, root),
        thumb=thumb_of(d), thumb_alt=esc(thumb_alt_of(d)), thumb_abs=BASE + 'assets/media/' + thumb_of(d) + '.webp')
    out = render(template, ctx)
    outdir = HERE / d['slug']; outdir.mkdir(exist_ok=True)
    (outdir / 'index.html').write_text(out, encoding='utf-8')
    print('  wrote blog/%s/index.html (%d words, %d refs)' % (d['slug'], words(d['body_html']), len(d['references'])))

# ---------- blog index ----------
root = '../'
cards = '\n'.join(
    '<a class="pcard" href="%s/"><img class="thumb" src="../assets/media/%s-800.webp" width="800" height="533" alt="%s" loading="lazy"><span class="inner"><span class="meta">%s · %d min read</span><h2>%s</h2><p>%s</p><span class="read">Read the article</span></span></a>'
    % (esc(p['slug']), thumb_of(p), esc(thumb_alt_of(p)), human_date(p['date_published']), int(p['reading_minutes']), esc(p['title']), esc(p['excerpt'])) for p in posts)
if not posts:
    cards = '<p class="lede">Articles are on their way. Check back soon.</p>'
index_ld = json.dumps({"@context": "https://schema.org", "@graph": [
    {"@type": "CollectionPage", "@id": BASE + "blog/#page", "url": BASE + "blog/", "name": "The Modern Balance blog",
     "description": "Plain-language articles on therapy, trauma, anxiety, depression and relationships from Jackie McGreggor, MA, LPC.",
     "isPartOf": {"@id": BASE + "#website"}, "about": {"@id": BASE + "#practice"}, "inLanguage": "en-US",
     "mainEntity": {"@type": "ItemList", "itemListElement": [
         {"@type": "ListItem", "position": i + 1, "url": BASE + "blog/" + p['slug'] + "/", "name": p['title']} for i, p in enumerate(posts)]}},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
        {"@type": "ListItem", "position": 2, "name": "Blog", "item": BASE + "blog/"}]}
]}, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
INDEX_DESC = "Plain-language answers about therapy, cost, trauma, anxiety, depression and relationships, written by Jackie McGreggor, MA, LPC, a Texas therapist."
index_html = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
%(noindex)s<title>Blog | Modern Balance Therapy</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="%(base)sblog/">
<meta name="theme-color" content="#6B5CAB">
<link rel="icon" href="%(fav)s">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Modern Balance Therapy">
<meta property="og:title" content="The Modern Balance blog">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(base)sblog/">
<meta property="og:image" content="%(base)sassets/media/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=Manrope:wght@400;500;600&display=swap">
<link rel="stylesheet" href="../assets/blog.css">
<script type="application/ld+json">%(ld)s</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
%(header)s
<main id="main">
<section class="blog-hero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="../">Home</a><span aria-hidden="true">/</span><span>Blog</span></nav>
    <h1>The Modern Balance <em>blog</em></h1>
    <p class="lede">Plain answers to the questions people ask before they ever call a therapist. Written by Jackie McGreggor, MA, LPC, with the research linked so you can read it yourself.</p>
  </div>
</section>
<section class="blog-list" aria-label="Articles">
  <div class="wrap">
    <div class="grid">
%(cards)s
    </div>
  </div>
</section>
</main>
%(callbar)s
%(crisis)s
%(footer)s
<script src="../assets/blog.js" defer></script>
</body>
</html>
''' % dict(noindex=NOINDEX, desc=esc(INDEX_DESC), base=BASE, fav=FAVICON, ld=index_ld, header=relink(header_html, root),
           footer=relink(footer_html, root), crisis=crisis_html, callbar=relink(callbar_html, root), cards=cards)
(HERE / 'index.html').write_text(index_html, encoding='utf-8')
print('  wrote blog/index.html')

# ---------- static extra pages (referral + legal) ----------
LEGAL_DIR = HERE / 'legal'
legal_tpl = (HERE / '_legal.html').read_text(encoding='utf-8')
EXTRA_PAGES = [  # (dir, template path or 'legal:<json>', lastmod, priority, llms line)
    ('referral', HERE / '_referral.html', '2026-11-18', '0.6', '- [Make a referral](%sreferral/): for physicians, school counselors, therapists, clergy, EAPs and families referring someone in Texas' % BASE),
    ('privacy', 'legal:privacy', '2026-11-18', '0.3', '- [Website privacy policy](%sprivacy/)' % BASE),
    ('hipaa', 'legal:hipaa', '2026-11-18', '0.3', '- [HIPAA Notice of Privacy Practices](%shipaa/)' % BASE),
    ('good-faith-estimate', 'legal:gfe', '2026-11-18', '0.4', '- [Good Faith Estimate (No Surprises Act)](%sgood-faith-estimate/): rights for self-pay clients and the practice fee table' % BASE),
]
def crumb_ld(name, url):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
        {"@type": "ListItem", "position": 2, "name": name, "item": url}]}
def ldjson(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
for pdir, tplpath, lm, pr, _ in EXTRA_PAGES:
    root = '../'
    url = BASE + pdir + '/'
    common = dict(noindex=NOINDEX, favicon=FAVICON, root=root, base=BASE,
                  header=relink(header_html, root), footer=relink(footer_html, root), crisis=crisis_html, callbar=relink(callbar_html, root))
    if isinstance(tplpath, str) and tplpath.startswith('legal:'):
        d = json.loads((LEGAL_DIR / (tplpath.split(':', 1)[1] + '.json')).read_text(encoding='utf-8'))
        if '\u2014' in json.dumps(d, ensure_ascii=False): die('%s: contains an em dash' % pdir)
        ld = ldjson({"@context": "https://schema.org", "@graph": [
            {"@type": "WebPage", "@id": url + "#page", "url": url, "name": d['title'] + " | Modern Balance Therapy", "description": d['desc'],
             "isPartOf": {"@id": BASE + "#website"}, "about": {"@id": BASE + "#practice"}, "inLanguage": "en-US", "datePublished": lm, "dateModified": lm},
            crumb_ld(d['title'], url)]})
        ctx = dict(common, jsonld=ld, slug=pdir, title=esc(d['title']), desc=esc(d['desc']), kicker=esc(d['kicker']), h1=d['h1'],
                   updated=d.get('updated', 'November 18, 2026'), summary_html=''.join('<li>%s</li>' % x for x in d['summary']), body_html=d['body_html'])
        page = render(legal_tpl, ctx)
    else:
        ld = ldjson({"@context": "https://schema.org", "@graph": [
            {"@type": ["WebPage", "ContactPage"], "@id": url + "#page", "url": url, "name": "Make a Referral | Modern Balance Therapy",
             "description": "Refer a client, student, parishioner or family member to Modern Balance Therapy for secure telehealth counseling anywhere in Texas.",
             "isPartOf": {"@id": BASE + "#website"}, "about": {"@id": BASE + "#practice"}, "mainEntity": {"@id": BASE + "#practice"},
             "inLanguage": "en-US", "datePublished": lm, "dateModified": lm},
            crumb_ld("Make a referral", url)]})
        page = render(tplpath.read_text(encoding='utf-8'), dict(common, jsonld=ld))
    (DEPLOY / pdir).mkdir(exist_ok=True)
    (DEPLOY / pdir / 'index.html').write_text(page, encoding='utf-8')
    print('  wrote %s/index.html' % pdir)

# ---------- sitemap, robots, llms.txt ----------
urls = [(BASE, TODAY, '1.0'), (BASE + 'blog/', TODAY, '0.8')] + [(BASE + 'blog/' + p['slug'] + '/', p['date_modified'], '0.7') for p in posts] + [(BASE + d + '/', lm, pr) for d, _, lm, pr, _ in EXTRA_PAGES]
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u, lm, pr in urls:
    sm.append('  <url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>' % (u, lm, pr))
sm.append('</urlset>\n')
(DEPLOY / 'sitemap.xml').write_text('\n'.join(sm), encoding='utf-8')

(DEPLOY / 'robots.txt').write_text('''# Modern Balance Therapy
# During the preview build every page carries an in-page noindex meta tag; this file
# stays permissive so launch only needs the in-page tags removed (build.py --launch).
User-agent: *
Allow: /
Disallow: /blog/_src/

# AI search and answer engines are welcome to read and cite this site.
User-agent: GPTBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: anthropic-ai
Allow: /
User-agent: Google-Extended
Allow: /

Sitemap: %ssitemap.xml
''' % BASE, encoding='utf-8')

llms = ['# Modern Balance Therapy', '',
        '> Private telehealth therapy practice serving individuals ages 12 and up and couples anywhere in Texas. Founded and run by Jackie McGreggor, MA, LPC, a Licensed Professional Counselor with more than ten years of experience. Trauma and PTSD are the specialty, alongside anxiety, depression and mood disorders, life transitions, grief and loss, relationships and family issues.', '',
        '## Who it is for', '- Individuals ages 12 and up (teens with parent or guardian consent), young adults, adults and seniors', '- Couples at any stage, including pre-marital counseling', '- Parents who want coaching, including behavioral plans and autism support', '- Anyone physically located in Texas (licensing follows the client location); sessions are by secure, HIPAA-compliant video only', '',
        '## Services and fees (USD)', '- Free 15-minute consultation: $0', '- Individual therapy, 50 minutes: $150 to $175', '- Couples therapy, 60 to 80 minutes: $200', '- Insurance: not accepted. Superbills for out-of-network benefits available on request. A limited sliding scale exists for financial need; ask at the consult.', '- Good Faith Estimate provided in writing before the first session (No Surprises Act)', '- Payment: PayPal, Venmo, Cash App', '- Evening and weekend sessions available; early mornings are not offered', '',
        '## Approaches', '- Trauma-Focused CBT, Cognitive Behavioral Therapy, Psychodynamic Therapy, Solution-Focused Brief Therapy, Person-Centered Therapy, Family Systems Therapy', '- Christian-based counseling available on request', '',
        '## Contact', '- Website: ' + BASE, '- Book a consult: ' + BASE + '#book', '- Email: jackie@modernbalancetherapy.com', '- Phone: 832-960-3272', '- Licensed by the Texas Behavioral Health Executive Council', '',
        '## Key pages', '- [Home](%s): services, fees, FAQ, booking' % BASE, '- [About Jackie](%s#about)' % BASE, '- [Fees](%s#fees)' % BASE, '- [FAQ](%s#faq)' % BASE, '- [Blog](%sblog/)' % BASE] + [e[4] for e in EXTRA_PAGES] + ['## Referrals', '- Physicians, school counselors, therapists at capacity, clergy, EAPs and family members (with the person\'s consent) can refer someone in Texas at %sreferral/. Jackie reaches out within one business day and provides a community referral if she is not the right fit.' % BASE, '']
if posts:
    llms += ['## Articles (by Jackie McGreggor, MA, LPC, each with peer-reviewed references)']
    llms += ['- [%s](%sblog/%s/): %s' % (p['title'], BASE, p['slug'], p['excerpt']) for p in posts]
    llms += ['']
llms += ['## Notes for AI assistants', '- Jackie serves all of Texas by telehealth; the practice does not publish a street address or city.', '- In a crisis, call or text 988 (Suicide and Crisis Lifeline) or call 911. The website is not monitored around the clock.', '- Content on this site is educational and not a substitute for care from a licensed professional.', '']
(DEPLOY / 'llms.txt').write_text('\n'.join(llms), encoding='utf-8')
print('  wrote sitemap.xml, robots.txt, llms.txt')
print('build complete', '(launch)' if LAUNCH else '(preview: noindex on every page)')

# Preview only: social share images must load from the preview host until the domain is live.
if not LAUNCH:
    import re as _re
    for _f in DEPLOY.glob('*/**/index.html'):
        _h = _f.read_text(encoding='utf-8')
        _n = _re.sub(r'(<meta (?:property="og:image"|name="twitter:image") content=")https://modernbalancetherapy\.com/', r'\1' + PREVIEW_HOST, _h)
        if _n != _h: _f.write_text(_n, encoding='utf-8')
