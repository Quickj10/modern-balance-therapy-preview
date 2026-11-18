# Blog article source spec (one JSON file per post: blog/_src/<slug>.json)

Required fields:
- slug, title (from TOPICS.json, do not change), meta_description (140-160 chars, includes primary keyword, ends with a soft reason to read),
- direct_answer (40-60 words, plain answer to the title question; this sits right under the H1 for featured snippets and AI answers),
- key_takeaways (3-5 one-sentence bullets),
- body_html (the article body only: h2/h3/p/ul/ol/strong/em/a. 1,200-1,800 words. No h1, no header/footer, no inline styles. H2s phrased as the questions people search where natural. In-text citations as superscript links: <sup><a href="#ref-3">3</a></sup>. One internal link to the home page fees section (../../#fees) or consult (../../#book) where it fits naturally, at most two internal links. One natural mention that Modern Balance Therapy offers secure telehealth across Texas; never name a city.),
- faqs (exactly 3 objects {q, a}; a is 40-80 words; distinct from the body H2s),
- references (4-8 objects {n, authors, year, title, source, url, doi_or_id, verified:true, verified_how}: peer-reviewed journals, Cochrane, NIMH, NIH, APA, CDC, WHO, SAMHSA, major university research, or dissertations in a university repository. EVERY url must have been fetched by you and confirmed to be the paper/page named. Unverified = not allowed. No blog posts, no therapy directories, no competitors.),
- reading_minutes (integer), date_published ("2026-11-18"), keywords (array), excerpt (1 sentence for the blog index card).

Voice: Jackie McGreggor, MA, LPC, first person singular where personal ("In my practice..."), warm, plain, second person to the reader, short paragraphs (max 3 sentences), no jargon without a one-line definition, no em dashes anywhere, no "Great question", no fear-mongering, no diagnosing the reader. Never state a sliding-scale dollar floor. Published fees are $150 to $175 individual, $200 couples. Insurance: not accepted; superbills "ask at your consult". Never mention any city. Ages served 12 and up. Trauma and PTSD are the specialty.

Safety: body_html ends with a short "If you are in crisis" paragraph pointing to 988 (call or text) and 911. Add a one-line note that the article is educational and not a substitute for care from a licensed professional.
