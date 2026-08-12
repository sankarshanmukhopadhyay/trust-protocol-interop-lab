#!/usr/bin/env python3
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
pat=re.compile(r'\[[^\]]+\]\(([^)]+)\)')
errors=[]
for p in ROOT.rglob('*.md'):
    text=p.read_text(errors='replace')
    for link in pat.findall(text):
        if link.startswith(('http://','https://','#','mailto:')): continue
        target=link.split('#',1)[0]
        if not target: continue
        if not (p.parent/target).resolve().exists(): errors.append(f'{p.relative_to(ROOT)} -> {link}')
if errors:
    print('\n'.join(errors)); raise SystemExit(1)
print('links: PASS')
