# Modern Balance Therapy: SEO / AEO / blog build notes (Nov 18, 2026)

## What was built
- **Home page SEO/AEO** (edited in `site/index.html`, backup `site/index.v5-pre-seo.html`): title "Modern Balance Therapy | Online Trauma Therapy in Texas" (55 chars), 158-char meta description, canonical, Open Graph + Twitter cards, theme-color, inline SVG favicon (three stones), one JSON-LD `@graph` with MedicalBusiness+Organization (`#practice`, Texas-only address, no city), Person (`#jackie`, LPC credential, no license number), WebSite, WebPage, FAQPage (the nine on-page FAQs). Nav "Journals" became "Blog" (Journals stays in the footer and on the page). New "From the blog" section between About and Fees; Fees moved to the cream band with white cards. Fees lede now states prices plainly for answer engines.
- **`deploy/wrap_home.py`** regenerates `deploy/index.html` from `site/index.html` (preview adds a noindex meta; `--launch` drops it).
- **Blog scaffolding** in `deploy/blog/`: `_template.html` (article page, placeholders in `{{ }}`; JSON-LD is assembled by build.py and injected as `{{jsonld}}`), `_article.css` (blog-only styles), `build.py`, `check.py`, `_src/SPEC.md` and `_src/TOPICS.json` (written by the orchestrator).
- `build.py` extracts the shared CSS, header, footer and crisis strip from `site/index.html` at every run, so blog pages always match the home page. Outputs: `assets/blog.css`, `assets/blog.js` (mobile menu + year), `blog/<slug>/index.html`, `blog/index.html`, `sitemap.xml`, `robots.txt`, `llms.txt`.
- Each article page carries: BlogPosting (author Person `#jackie`, publisher `#practice`, `citation[]` from the references, wordCount, keywords), FAQPage (3 Qs), BreadcrumbList; a 40-60 word "short answer" block under the H1; key takeaways; numbered references with live links; author card; consult CTA; "Keep reading" list of 3.

## Rebuild
```
cd ~/.openclaw/workspace/outputs/modern-balance-therapy/deploy
python3 -I wrap_home.py          # home page (add --launch at go-live)
python3 -I blog/build.py         # blog, sitemap, robots, llms.txt (add --launch at go-live)
python3 -I blog/check.py         # H1 / title / description / JSON-LD / links / reference URLs / em dashes
```
`check.py --no-net` skips the external reference URL check. A 403 from a publisher that blocks bots is printed as a note, not a failure.

## What Jackie must supply
- `assets/og.png`, 1200 x 630 (her headshot or the stones mark on lavender). Referenced from every page's Open Graph tags and the schema logo/image.
- Texas LPC license number for the footer and the Person credential.
- Confirmation of fees, payment methods and superbill policy as published.

## Launch checklist
1. Run both build scripts with `--launch` to remove the in-page noindex tags (robots.txt is already permissive).
2. Point the canonical URLs at the live domain if it is anything other than https://modernbalancetherapy.com/ (search `BASE` in build.py and the canonical in site/index.html).
3. Upload `assets/og.png`.
4. Verify home and one article in Google's Rich Results Test and validator.schema.org.
5. Submit `sitemap.xml` in Search Console; add the site to Bing Webmaster Tools.
6. Create the Google Business Profile (service-area business, no address shown) and a Psychology Today profile, both linking to the site; add their URLs to `sameAs` on `#practice`.
7. Add Privacy Practices and Good Faith Estimate pages (footer currently shows them as plain text).
8. Re-run `check.py` with network on so every reference URL is confirmed live.

## v19 (Nov 18): earth/wine restyle
- Tokens live in site/index.html :root and propagate to every page through build.py (shared CSS block). Legacy names (--violet, --lav, --sage...) are aliases to the new palette so older rules follow.
- Fonts: Jost 300/400/500 + Fraunces italic (accent only). Google Fonts link appears in site/index.html, _template.html, _referral.html, _legal.html and the blog index string inside build.py; change all five together.
- Pattern: assets/petals.svg (hand-drawn seamless 720px tile, slate petals on cream) is used only by the mirror section.
- Pending images, do NOT generate without Ally's approval: three "cozy conversation" alternates for the mirror snapshot slot (two people talking on a sofa in warm light, hands around mugs across a table, a person listening from behind). Current slot uses CC0 hands with salvia.
- Blog thumbnails were not re-shot this round; they still carry the round-2 grade. Re-grade with the round-3 curve if they read cool.
