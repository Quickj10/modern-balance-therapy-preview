#!/usr/bin/env python3
"""Wrap ../site/index.html (artifact page contract) into deploy/index.html (full document).
Usage: python3 -I wrap_home.py            # preview build (noindex)
       python3 -I wrap_home.py --launch   # drops the preview noindex line
"""
import sys, pathlib, re
here=pathlib.Path(__file__).resolve().parent
src=(here.parent/'site'/'index.html').read_text(encoding='utf-8')
head,sep,body=src.partition('</style>')
assert sep, 'no </style> in site/index.html'
head='\n'.join(l for l in head.splitlines() if 'claude:viewport-fit-sides' not in l)
noindex='' if '--launch' in sys.argv else '<meta name="robots" content="noindex,nofollow"><!-- PREVIEW ONLY: remove at launch -->\n'
out=('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
     '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
     + noindex + head + '</style>\n</head>\n<body>\n' + body.lstrip('\n') + '\n</body>\n</html>\n')
(here/'index.html').write_text(out,encoding='utf-8')
print('wrote deploy/index.html', len(out), 'bytes', '(launch)' if '--launch' in sys.argv else '(preview, noindex)')
