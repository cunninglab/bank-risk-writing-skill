import re, sys, pathlib, json
X = pathlib.Path(sys.argv[1])
m = dict(l.split(' ', 1)[::-1] for l in (X/'fetch/map.txt').read_text().split('\n') if l)
m = {k.strip(): v for k, v in m.items()}
norm = lambda s: re.sub(r'[\s，,。；;：:、“”"‘’（）()《》〈〉\-—·]', '', s)
txt = {u: norm((X/'fetch'/(f+'.txt')).read_text(encoding='utf-8')) for u, f in m.items()}
res = {}
for rid in sys.argv[2:]:
    out = (X/'out'/(rid+'.md')).read_text(encoding='utf-8')
    rows = []
    for line in out.split('\n'):
        urls = re.findall(r'https?://[^ )>\]]+', line)
        if not urls: continue
        quotes = re.findall(r'“([^”]{2,80})”', line)
        for q in quotes:
            hit = [u for u in urls if norm(q) and norm(q) in txt.get(u, '')]
            rows.append({'excerpt': q, 'urls': urls, 'found_in': hit})
        if not quotes:
            rows.append({'excerpt': None, 'urls': urls, 'found_in': []})
    res[rid] = rows
print(json.dumps(res, ensure_ascii=False, indent=1))
