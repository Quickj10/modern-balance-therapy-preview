# Media credits and licenses (Modern Balance Therapy)

Every shipped item is licensed for free commercial use without attribution (CC0 / Public Domain via the WordPress Photo Directory and Wikimedia Commons, Mixkit License for video). Credits are recorded anyway. Ally's reference images (design-references/modern-balance-therapy/round2) were NOT used anywhere. Earlier rawpixel candidates were dropped because their free previews are watermarked.

Grading toward the site palette (noted per the brief): photos get saturation reduced about 16 percent, blacks lifted about 5 percent, a touch of warmth (blue channel slightly lower). The band image is graded harder (saturation about 25 percent lower, blacks lifted 7 percent) to pull a pink dandelion macro toward peach and cream; on Nov 18 the band was re-graded with a hue shift of about minus 65 degrees so the pink reads as lavender, then re-graded again (hue shift, saturation 0.42, 38 percent blend with #E2DBF0) to a soft muted lavender, per Ally. The hero video was graded in ffmpeg (eq saturation 0.8, brightness +0.03, contrast 0.96, curves lift) and loop-crossfaded over 0.6 s.

## Hero video

| File | Source | License | Notes |
|---|---|---|---|
| hero.mp4, hero.webm, hero-poster.jpg | Mixkit, "Dandelions in spring", https://mixkit.co/free-stock-video/dandelions-in-spring-34706/ | Mixkit License (free for commercial and personal use, no attribution) | 1280x720 source, 1 s to 10 s, graded, 9 s loop |
| alternate, not shipped | Mixkit, "A tranquil forest amids the morning mist", https://mixkit.co/free-stock-video/a-tranquil-forest-amids-the-morning-mist-50867/ | Mixkit License | 1080p available |
| alternate, not shipped | Mixkit, "Close up of a full dandelion", https://mixkit.co/free-stock-video/close-up-of-a-full-dandelion-45332/ | Mixkit License | 720p |

## Photos (shipped)

| File | Used for | Source page | Creator | License | Native size |
|---|---|---|---|---|---|
| frame-stones.webp and frame-stones-800.webp | Focus section frame | https://wordpress.org/photos/photo/61865c314c/ | Manjit — The AF Themes Support Team | CC0 (wordpress) | 1536x2048 |
| frame-grass.webp and frame-grass-800.webp | Mirror section frame | https://wordpress.org/photos/photo/370670ac14/ | Mohammed Jamsheed KM | CC0 (wordpress) | 2048x1365 |
| band-mist.webp and band-mist-800.webp | Full-bleed band | https://wordpress.org/photos/photo/23761e9afb/ | AlfieGrand | CC0 (wordpress) | 2048x1361 |
| thumb-need-therapy.webp and thumb-need-therapy-800.webp | Blog: need therapy (rocks on a sandy beach, swapped Nov 18 per Ally) | https://wordpress.org/photos/photo/3166763b9b/ | SadikAli | CC0 (wordpress) | 1536x2048 |
| thumb-affordable.webp and thumb-affordable-800.webp | Blog: affordable therapy | https://wordpress.org/photos/photo/62869d21e6/ | Tawhid Sadman | CC0 (wordpress) | 2048x1536 |
| thumb-first-session.webp and thumb-first-session-800.webp | Blog: first session (river cairn, swapped Nov 18 per Ally) | https://wordpress.org/photos/photo/45765c64a8/ | Vishnu Chandra | CC0 (wordpress) | 2048x1536 |
| thumb-online.webp and thumb-online-800.webp | Blog: online therapy | https://wordpress.org/photos/photo/81668ea316/ | Bigul Malayi | CC0 (wordpress) | 2048x2048 |
| thumb-trauma.webp and thumb-trauma-800.webp | Blog: trauma | https://wordpress.org/photos/photo/3166763b9b/ | SadikAli | CC0 (wordpress) | 2048x1536 |
| thumb-anxiety.webp and thumb-anxiety-800.webp | Blog: stress vs anxiety | https://wordpress.org/photos/photo/5736a10966/ | Sakin Shrestha | CC0 (wordpress) | 2048x1536 |
| thumb-depression.webp and thumb-depression-800.webp | Blog: high-functioning depression | https://wordpress.org/photos/photo/94869d7387/ | Roopa Ashok Mirajkar | CC0 (wordpress) | 2048x1153 |
| thumb-couples.webp and thumb-couples-800.webp | Blog: couples | https://wordpress.org/photos/photo/49069e9184/ | Jos Velasco | CC0 (wordpress) | 1536x2048 |
| thumb-teen.webp and thumb-teen-800.webp | Blog: teens | https://wordpress.org/photos/photo/9416631e76/ | werkform | CC0 (wordpress) | 2048x1365 |
| thumb-how-long.webp and thumb-how-long-800.webp | Blog: how long | https://wordpress.org/photos/photo/8866846a28/ | Suraj Sutar | CC0 (wordpress) | 2048x1266 |

## Alternates (kept in _raw, not shipped)

- frame-stones: Pebble Stack (Unsplash) | https://commons.wikimedia.org/w/index.php?curid=61886889 | Nick Tong thenickt16 | CC0 | 3840x5760
- frame-stones: balanced stacks of smooth rocks | https://wordpress.org/photos/photo/91761eb1bb/ | Jennifer Bourn | CC0 | 2048x1365
- frame-stones: Stacked stones on the shore of a river with tall mountain ranges in th | https://wordpress.org/photos/photo/45765c64a8/ | Vishnu Chandra | CC0 | 1532x2048
- frame-grass: Foggy morning with a winding road, a lone tree, and a small house in m | https://wordpress.org/photos/photo/454692efd4/ | Tawhid Sadman | CC0 | 2048x1536
- frame-grass: A serene landscape at dawn with a lush green hill and tall trees under | https://wordpress.org/photos/photo/2816a2ae07/ | Roman Khadka | CC0 | 1536x2048
- frame-grass: A serene landscape depicting a misty scene by a calm river. On the lef | https://wordpress.org/photos/photo/8086524b1f/ | Nicholas Garofalo | CC0 | 2048x1365
- band-mist: Silhouetted conifer tree stands tall against a hazy, forested landscap | https://wordpress.org/photos/photo/94869d7387/ | Roopa Ashok Mirajkar | CC0 | 2048x1153
- band-mist: Grasses swaying in the breeze backlit by the sun. | https://wordpress.org/photos/photo/370670ac14/ | Mohammed Jamsheed KM | CC0 | 2048x1365
- band-mist: white pebbles | https://wordpress.org/photos/photo/843621a618/ | Umesh Gupta | CC0 | 2048x1365

## Swapping a pick
Put the new source file in assets/media/_raw, change the key in the plan inside assets/media/process.py (copy of the processing script), run it, then `python3 -I deploy/wrap_home.py` and `python3 -I deploy/blog/build.py`. Sizes: frames 1600 px wide, thumbnails 1200 px plus 800 px card versions, all WebP quality 80.

## Round 3 (Nov 18, earth/wine restyle)

| File | Used for | Source page | Creator | License |
|---|---|---|---|---|
| frame-hands.webp (removed Nov 18, v5: purple salvia fought the palette) | formerly mirror section photo | https://wordpress.org/photos/photo/57367ca6d7/ | WordPress Photo Directory contributor (see page) | CC0 |
| frame-ripples.webp | Focus section blob frame | https://wordpress.org/photos/photo/6706a994f1/ | see page | CC0 |
| band-light.webp | Full-bleed band (plant shadow on cream wall) | https://wordpress.org/photos/photo/24168f4752/ | see page | CC0 |
| mosaic-grass.webp | Mosaic tile (backlit grass, 4:5 crop of the earlier frame-grass source) | https://wordpress.org/photos/photo/370670ac14/ | Mohammed Jamsheed KM | CC0 |
| (dropped) 47167a9e19 walking pair | too urban once cropped, kept in _raw only | https://wordpress.org/photos/photo/47167a9e19/ | see page | CC0 |
| mosaic-lake.webp | Mosaic tile (lake ripples) | https://wordpress.org/photos/photo/8636ad268e/ | see page | CC0 |
| frame-hands-alt.webp | alternate, not shipped | https://wordpress.org/photos/photo/5006a0837c/ | see page | CC0 |

Grade: saturation 0.8, warm lift (R +10, G +8, B +4, blue ceiling 246). Hero video re-graded warmer (eq saturation 0.72, gamma_r 1.03, gamma_b 0.97).
Retired this round: frame-grass, frame-stones, band-mist (kept on disk for the contact sheet).


## v5 (Nov 18): painted shapes replace the hero video
- Hero video files (hero.mp4, hero.webm, hero-poster.jpg) stay in the folder but are no longer referenced; the hero is now a painted SVG shape (assets/paint-hero.svg). The mirror band uses assets/paint-strokes.svg and the About section uses assets/petals.svg, all drawn in code, no stock.
- frame-ripples.webp moved from the specialties frame to the "From the blog" offset photo.
