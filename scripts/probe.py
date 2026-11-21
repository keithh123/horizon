import json,sys,urllib.request,urllib.parse
UA={'User-Agent':'project-horizon-builder/0.1'}
def get(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA)))
slugs=sys.argv[1:]
for s in slugs:
    q=urllib.parse.urlencode({'loaders':'["neoforge"]','game_versions':'["1.21.1"]'})
    try:
        vs=get(f'https://api.modrinth.com/v2/project/{s}/version?{q}')
        if vs:
            rel=[v for v in vs if v['version_type']=='release']
            v=(rel or vs)[0]
            print(f"OK   {s:38} {v['version_number'][:40]:40} {v['version_type']:7} {v['date_published'][:10]}")
        else:
            p=get(f'https://api.modrinth.com/v2/project/{s}')
            print(f"NONE {s:38} loaders={p['loaders']} gv={p['game_versions'][-3:]}")
    except Exception as e:
        r=get('https://api.modrinth.com/v2/search?'+urllib.parse.urlencode({'query':s,'limit':3,'facets':'[["categories:neoforge"],["versions:1.21.1"]]'}))
        print(f"MISS {s:38} search-> {[h['slug'] for h in r['hits']]}")
