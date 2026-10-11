"""MAP-2B helpers: immutable dirty-tree baseline and focused read-only queries."""
import sys, json, hashlib, subprocess
from pathlib import Path
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
ROOT=qa.ROOT
OUT=ROOT/'docs/reports/map/MAP2B'
def snapshot():
    OUT.mkdir(parents=True,exist_ok=True)
    dest=OUT/'MAP2B_BASELINE.json'
    assert not dest.exists(), 'Never overwrite the pre-edit snapshot'
    files=list((ROOT/'common').rglob('*.txt'))+list((ROOT/'map_data').rglob('*'))
    protected={p.relative_to(ROOT).as_posix():qa.sha(p) for p in files if p.is_file()}
    for folder in ['docs/reports/map/MAP1C','docs/reports/map/MAP2A','gfx','localization']:
        for p in (ROOT/folder).rglob('*'):
            if p.is_file(): protected[p.relative_to(ROOT).as_posix()]=qa.sha(p)
    histories={p.relative_to(ROOT).as_posix():p.read_text(encoding='utf-8-sig') for p in (ROOT/'common/history').rglob('*.txt')}
    data={'hashes':protected,'originals':histories,'inventory':qa.inventory(),'native_test':'NOT_RUN'}
    dest.write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')
    print('Captured actual dirty-tree baseline:',len(protected),'files; population',sum(r['count'] for r in data['inventory']['pops']))
def query():
    for path in ['common/history/states/00_states.txt','common/history/pops/01_south_europe.txt','common/history/buildings/01_south_europe.txt']:
        ns=cw.parse((ROOT/path).read_text(encoding='utf-8-sig'))
        print('\nFILE',path)
        for n in cw.walk(ns):
            if n.key in ['s:STATE_SOUTH_TYROL','s:STATE_TYROL','s:STATE_ISTRIA','s:STATE_LOMBARDY','s:STATE_PROVENCE','s:STATE_RHONE','s:STATE_CAMPANIA','s:STATE_LAZIO']:
                print(n.key,qa.norm(n))
def save_probe():
    import inspect_oct09_saved_crews as saved
    import validate_wallonia_start_1776 as w
    from collections import Counter, defaultdict
    saved.SAVE=w.SAVE
    want={r['id'] for r in json.loads((w.OUT/'SAVE_DIAGNOSIS.json').read_text())['deficit_states']}
    countries={}; states={}; rows=defaultdict(list); inp=defaultdict(Counter); out=defaultdict(Counter)
    for section,ident,raw in saved.objects():
        if section=='country_manager':
            countries[ident]={'tag':saved.field(raw,'definition'),'market':saved.field(raw,'market')}
        if section=='states':
            states[ident]={'country_id':int(saved.field(raw,'country') or -1),'market':saved.field(raw,'market'),'market_access':saved.field(raw,'market_access'),'population':saved.field(raw,'population'),'raw':raw if ident in want else ''}
        if section=='building_manager':
            sid=int(saved.field(raw,'state') or -1)
            rows[sid].append({'building':saved.field(raw,'building'),'levels':saved.field(raw,'levels'),'staffing':saved.field(raw,'staffing'),'inputs':w.goods(raw,'input'),'outputs':w.goods(raw,'output')})
    for sid,bs in rows.items():
        m=countries.get(states.get(sid,{}).get('country_id'),{}).get('market')
        for b in bs:
            inp[m].update(b['inputs']); out[m].update(b['outputs'])
    data={'countries':countries,'states':{sid:st for sid,st in states.items() if sid in want},'buildings':{sid:rows[sid] for sid in want},'market_building_inputs':dict(inp),'market_building_outputs':dict(out)}
    (OUT/'SAVE_INPUTS.json').write_text(json.dumps(data),encoding='utf-8')
    for sid in sorted(want):
        s=states[sid]; c=countries.get(s['country_id'],{}); m=c.get('market')
        print(sid,c['tag'],s['population'],s['market_access'],'wood',round(out[m][10],1),round(inp[m][10],1),'tools',round(out[m][34],1),round(inp[m][34],1))
    print('STATE SAMPLE',states[818]['raw'][:1000] if 818 in want else next(iter(data['states'].values()))['raw'][:1000])
if __name__=='__main__':
    if '--snapshot' in sys.argv: snapshot()
    elif '--query' in sys.argv: query()
    elif '--save-probe' in sys.argv: save_probe()
