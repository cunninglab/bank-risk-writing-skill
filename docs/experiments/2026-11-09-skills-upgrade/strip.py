import re, sys, pathlib
root, m = pathlib.Path(sys.argv[1]), sys.argv[2]
pat = re.compile(r'<!-- mechanism:%s -->.*?<!-- /mechanism:%s -->\n?' % (m, m), re.S)
for f in root.rglob('*.md'):
    s = f.read_text(encoding='utf-8'); t = pat.sub('', s)
    if t != s: f.write_text(t, encoding='utf-8'); print('stripped', f.relative_to(root))
