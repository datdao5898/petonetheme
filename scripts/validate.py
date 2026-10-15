import json, re, os, sys, glob
root = sys.argv[1]
errs = []
def E(*a): errs.append(' '.join(map(str,a)))
def load_json(path):
    # Shopify's admin editors prepend a /* auto-generated */ comment to JSON files they touch
    return json.loads(re.sub(r'^\s*/\*.*?\*/', '', open(path, encoding='utf-8').read(), flags=re.S))

locale = load_json(f'{root}/locales/en.default.json')
def has_key(k):
    d = locale
    for p in k.split('.'):
        if not isinstance(d, dict) or p not in d: return False
        d = d[p]
    return True
schemas = {}
pair = {'if':'endif','unless':'endunless','for':'endfor','case':'endcase','capture':'endcapture','form':'endform','paginate':'endpaginate','style':'endstyle','schema':'endschema','comment':'endcomment','javascript':'endjavascript'}
for f in glob.glob(f'{root}/**/*.liquid', recursive=True):
    s = open(f).read()
    rel = os.path.relpath(f, root)
    # schema
    m = re.search(r'{%\s*schema\s*%}(.*?){%\s*endschema\s*%}', s, re.S)
    body = s
    if m:
        try:
            sch = json.loads(m.group(1)); schemas[os.path.basename(f)[:-7]] = sch
        except Exception as e: E(rel, 'schema JSON', e)
        body = s[:m.start()]
    # strip comments
    body = re.sub(r'{%-?\s*comment\s*-?%}.*?{%-?\s*endcomment\s*-?%}', '', body, flags=re.S)
    # tag balance: collect tags including inside {% liquid %}
    tags = []
    for t in re.finditer(r'{%-?\s*(.*?)\s*-?%}', body, re.S):
        inner = t.group(1)
        if inner.startswith('liquid'):
            for line in inner[6:].split('\n'):
                line=line.strip()
                if line: tags.append(line.split()[0])
        else:
            tags.append(inner.split()[0] if inner.split() else '')
    stack = []
    for t in tags:
        if t in pair: stack.append(t)
        elif t.startswith('end'):
            if not stack or pair[stack[-1]] != t: E(rel, 'unbalanced', t, 'stack', stack); break
            stack.pop()
    else:
        if stack: E(rel, 'unclosed', stack)
    # translations
    for k in re.findall(r"'([a-z_]+\.[a-z_]+)'\s*\|\s*t\b", s):
        if not has_key(k): E(rel, 'missing translation', k)
    # renders
    for sn in re.findall(r"render\s+'([\w-]+)'", s):
        if not os.path.exists(f'{root}/snippets/{sn}.liquid'): E(rel, 'missing snippet', sn)
    # assets
    for a in re.findall(r"'([\w.-]+\.(?:css|js|png|svg))'\s*\|\s*asset_url", s):
        if not os.path.exists(f'{root}/assets/{a}'): E(rel, 'missing asset', a)
    # section.settings ids exist
    if m and rel.startswith('sections'):
        ids = {x.get('id') for x in sch.get('settings', [])}
        for sid in set(re.findall(r'section\.settings\.(\w+)', s)):
            if sid not in ids: E(rel, 'unknown section setting', sid)
        bids = {x.get('id') for b in sch.get('blocks', []) for x in b.get('settings', [])}
        for sid in set(re.findall(r'block\.settings\.(\w+)', s)) | set(re.findall(r'\bb\.(\w+)', s)):
            if sid not in bids: E(rel, 'unknown block setting', sid)
        # s.xxx alias in hero
        if 'assign s = section.settings' in s:
            for sid in set(re.findall(r'\bs\.(\w+)', s)):
                if sid not in ids: E(rel, 'unknown s. setting', sid)
# global settings
gs = load_json(f'{root}/config/settings_schema.json')
gids = {x['id'] for g in gs[1:] for x in g['settings'] if 'id' in x}
def check_settings(where, settings):
    for x in settings:
        if x.get('type') == 'range':
            n = (x['max']-x['min'])/x['step']
            if n > 101 or n != int(n): E(where, x['id'], 'range steps', n)
            d = x.get('default')
            if d is None or not (x['min'] <= d <= x['max']) or (d - x['min']) % x['step']: E(where, x['id'], 'range default bad', d)
        if x.get('type') == 'select':
            vals = [o['value'] for o in x['options']]
            if x.get('default') not in vals: E(where, x['id'], 'select default bad')
check_settings('global', [x for g in gs[1:] for x in g['settings']])
for f in glob.glob(f'{root}/**/*', recursive=True):
    if f.endswith('.liquid') or f.endswith('.js'):
        for sid in set(re.findall(r'\bsettings\.(\w+)', open(f).read())):
            pre = open(f).read()
            if re.search(r'(section|block)\.settings\.'+sid, pre): continue
            if sid not in gids: E(os.path.relpath(f,root), 'unknown global setting', sid)
for name, sch in schemas.items():
    check_settings(name, sch.get('settings', []))
    for b in sch.get('blocks', []): check_settings(name+':'+b['type'], b.get('settings', []))
    ids = [x.get('id') for x in sch.get('settings', []) if x.get('id')]
    if len(ids) != len(set(ids)): E(name, 'duplicate ids')
    for p in sch.get('presets', []):
        bt = {b['type'] for b in sch.get('blocks', [])}
        for b in p.get('blocks', []):
            if b['type'] not in bt: E(name, 'preset block type', b['type'])
            bset = {x['id'] for bb in sch['blocks'] if bb['type']==b['type'] for x in bb['settings'] if 'id' in x}
            for k in b.get('settings', {}):
                if k not in bset: E(name, 'preset block setting', k)
# templates & groups
for f in glob.glob(f'{root}/templates/**/*.json', recursive=True) + glob.glob(f'{root}/sections/*.json'):
    rel = os.path.relpath(f, root)
    d = load_json(f)
    for key, sec in d['sections'].items():
        t = sec['type']
        if t not in schemas: E(rel, 'unknown section', t); continue
        sch = schemas[t]
        sids = {x['id'] for x in sch.get('settings', []) if 'id' in x}
        for k in sec.get('settings', {}):
            if k not in sids: E(rel, key, 'unknown setting', k)
        bt = {b['type']: b for b in sch.get('blocks', [])}
        for bk, b in sec.get('blocks', {}).items():
            if b['type'] not in bt: E(rel, key, 'unknown block', b['type']); continue
            bids = {x['id'] for x in bt[b['type']]['settings'] if 'id' in x}
            for k in b.get('settings', {}):
                if k not in bids: E(rel, key, bk, 'unknown block setting', k)
        if set(sec.get('block_order', [])) != set(sec.get('blocks', {}).keys()): E(rel, key, 'block_order mismatch')
    if set(d['order']) != set(d['sections']): E(rel, 'order mismatch')
print('\n'.join(errs) if errs else 'OK — no issues')
