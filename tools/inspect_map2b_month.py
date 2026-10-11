"""Read-only comparison of user saves; never interpret old history as a patch test."""
import json,re,hashlib
from pathlib import Path
import inspect_oct09_saved_crews as saved
import validate_wallonia_start_1776 as w
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/reports/map/MAP2B'
SOURCE=Path('C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/save games/observateur_3.v3')
def run():
    saved.SAVE=ROOT/'.asset-cache/observateur_3_readonly.txt'
    with saved.SAVE.open(encoding='utf-8') as f: prefix=f.read(1500)
    date=re.search(r'game_date=([^\s]+)',prefix).group(1)
    countries={}; states={}; buildings={}
    for section,ident,raw in saved.objects():
        if section=='country_manager': countries[ident]=saved.field(raw,'definition')
        elif section=='states':
            labour={k:float(v) for k,v in re.findall(r'^\t{4}(population_(?:salaried_workforce|government_workforce|military_workforce|unemployed_workforce|laborer_workforce|peasant_workforce|slave_workforce))=([^\s]+)',raw,re.M)}
            states[ident]={'id':ident,'country_id':int(saved.field(raw,'country') or -1),'region':saved.field(raw,'region'),
                'infrastructure':float(saved.field(raw,'infrastructure') or 0),'usage':float(saved.field(raw,'infrastructure_usage') or 0),
                'market_access':None,'employment_statistics':labour}
        elif section=='building_manager' and saved.field(raw,'building')=='building_railway':
            sid=int(saved.field(raw,'state') or -1)
            buildings.setdefault(sid,[]).append({'id':ident,'levels':float(saved.field(raw,'levels') or 0),'staffing':float(saved.field(raw,'staffing') or 0),
                'pms':w.pms(raw),'subsidized':saved.field(raw,'subsidized'),'inputs':w.goods(raw,'input'),'outputs':w.goods(raw,'output')})
    index={}
    for ident,s in states.items():
        s['country']=countries.get(s.pop('country_id')); s['networks']=buildings.get(ident,[])
        s['balance']=round(s['infrastructure']-s['usage'],5)
        index[(s['country'],s['region'])]=s
    before=json.loads((w.OUT/'SAVE_DIAGNOSIS.json').read_text(encoding='utf-8'))
    plans=json.loads((OUT/'INFRASTRUCTURE_PLAN.json').read_text(encoding='utf-8'))
    previous_path=OUT/'OBSERVATEUR_3_COMPARISON.json'
    previous=json.loads(previous_path.read_text(encoding='utf-8')) if previous_path.exists() else {}
    prelim={(r['country'],r['region']):r.get('preliminary_planned_levels',r['planned_levels']) for r in previous.get('comparison_69',[])}
    rows=[]
    for old in before['deficit_states']:
        s=index.get((old['country'],old['region'])); p=next(x for x in plans if x['country']==old['country'] and x['region']==old['region'])
        preliminary=prelim.get((old['country'],old['region']),p['new_levels'])
        row={'country':old['country'],'region':old['region'],'initial_cache_balance':old['cache_delta'],'planned_levels':p['new_levels'],'preliminary_planned_levels':preliminary,
             'month':s,'history_level_matches':bool(s and sum(b['levels'] for b in s['networks'])==p['new_levels'])}
        rows.append(row)
    wallonia=index.get(('BEO','STATE_WALLONIA'))
    markers={'PAP_Provence':('PAP','STATE_PROVENCE') in index,'VEN_South_Tyrol_still_exists':('VEN','STATE_SOUTH_TYROL') in index,
             'Wallonia_loaded_13_levels':sum(b['levels'] for b in wallonia['networks'])==13}
    current=markers['PAP_Provence'] and not markers['VEN_South_Tyrol_still_exists'] and markers['Wallonia_loaded_13_levels']
    data={'source_save':str(SOURCE),'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'game_date':date,
          'patch_markers':markers,'contains_MAP2B_history':current,'states_inspected':len(states),
          'negative_month_cache_balances':sum(s['balance']<0 for s in states.values()),
          'original_69_still_negative':sum(r['month'] is not None and r['month']['balance']<0 for r in rows),
          'original_69_history_level_matches':sum(r['history_level_matches'] for r in rows),'wallonia':wallonia,'comparison_69':rows,
          'preliminary_69_history_level_matches':sum(bool(r['month'] and sum(b['levels'] for b in r['month']['networks'])==r['preliminary_planned_levels']) for r in rows),
          'all_negative_states':[s for s in states.values() if s['balance']<0],
          'interpretation':'Native month observations. Territorial/Wallonia markers match. East Prussia loads 1 versus target 3. Rio is lowered after this test from 33 to historical 8 using native output; final target matches and preliminary matches are counted separately. Market access is not read from state.counters.market_access: that field is a dirty-cache counter, not a percentage.'}
    (OUT/'OBSERVATEUR_3_COMPARISON.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in data.items() if k not in ['comparison_69','all_negative_states']},ensure_ascii=False,indent=2))
    print('Previously understaffed:')
    for old in before['deficit_states']:
        if any(b['staffing']<b['levels'] for b in old['regional_infrastructure']):
            s=index.get((old['country'],old['region']))
            print(json.dumps(s,ensure_ascii=False))
if __name__=='__main__': run()
