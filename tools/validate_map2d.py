"""Independent static MAP-2D checks; no claim to native engine execution."""
import json,collections as C,hashlib,re,sys
from pathlib import Path
import numpy as np
from PIL import Image
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
from map2d_work import ROOT,GAME,OUT,BASE,sha,source_bitmap,packed,TARGETS
from map2d_patch import TRANSFERS
from map_1776_audit import effective

ALLOWED={'common/history/states/00_states.txt','common/history/pops/15_russia.txt',
 'common/history/buildings/98_build_start_1776_world_redistribution.txt',
 'common/diplomatic_actions/31_power_bloc_force_become_subject.txt',
 'common/diplomatic_actions/28_invite_to_power_bloc.txt',
 'common/history/treaties/1776_russian_guarantee_poland.txt',
 'localization/french/1776_map2d_l_french.yml','localization/english/1776_map2d_l_english.yml',
 'map_data/state_regions/02_east_europe.txt','map_data/state_regions/15_russia.txt'}
def pop_attributes(originals=None):
    result=C.Counter()
    texts=[t for p,t in originals.items() if p.startswith('common/history/pops/')] if originals is not None else [p.read_text(encoding='utf-8-sig') for p in (ROOT/'common/history/pops').rglob('*.txt')]
    for text in texts:
        for n in cw.walk(cw.parse(text)):
            if n.key!='create_pop':continue
            attrs=tuple(json.dumps(qa.norm(c),ensure_ascii=False) for c in n.children() if c.key!='size')
            result[attrs]+=int(n.one('size'))
    return result
def validate():
    saved=json.loads(BASE.read_text(encoding='utf-8'));before=saved['inventory'];after=qa.inventory();checks={}
    changed=[p for p,h in saved['hashes'].items() if not (ROOT/p).exists() or sha(ROOT/p)!=h]
    unexpected=[p for p in changed if p not in ALLOWED]
    new_runtime=[p.relative_to(ROOT).as_posix() for f in ['common','map_data','gfx','localization','events','.metadata'] for p in (ROOT/f).rglob('*') if p.is_file() and p.relative_to(ROOT).as_posix() not in saved['hashes']]
    unexpected_new=[p for p in new_runtime if p not in ALLOWED]
    # Report byte-level drift, including harmless line ending changes, as drift.
    checks['no_unexpected_protected_file_changes']=not unexpected and not unexpected_new
    checks['world_population_conserved']=qa.counter(before['pops'])==qa.counter(after['pops'])
    checks['resolved_cultures_religions_conserved']=qa.counter(before['resolved_demographics'])==qa.counter(after['resolved_demographics'])
    checks['all_pop_attributes_including_slave_status_conserved']=pop_attributes(saved['originals'])==pop_attributes()
    def economic(inv):return sum((C.Counter({(r['key'][0],r['key'][2]):r['count']}) for r in inv['buildings']),C.Counter())
    checks['building_bodies_pm_reserves_economic_owners_conserved']=economic(before)==economic(after)
    checks['all_building_levels_conserved']=before['building_levels_written']==after['building_levels_written']
    checks['all_military_formations_types_counts_recruitment_unchanged']=before['units']==after['units']
    checks['countries_capitals_types_unchanged']=before['countries']==after['countries']
    checks['state_region_definitions_unchanged']=before['geometry']==after['geometry']
    def regional_totals(inv):
        result=C.Counter()
        for r in inv['regional_pop']:result[r['key'][0]]+=r['count']
        return result
    checks['every_state_region_population_total_conserved']=regional_totals(before)==regional_totals(after)
    checks['unaffected_owner_state_demographics_unchanged']=[r for r in before['regional_pop'] if r['key'][0] not in TRANSFERS]==[r for r in after['regional_pop'] if r['key'][0] not in TRANSFERS]
    checks['bitmap_byte_exact_preserves_avignon_friuli']=sha(source_bitmap())==saved['bitmap_hash']
    old={r['key'][0]:(r['key'][1],r['key'][2]) for r in before['owners'] if r['key'][0] not in before['duplicates']}
    now={r['key'][0]:(r['key'][1],r['key'][2]) for r in after['owners'] if r['key'][0] not in after['duplicates']}
    expected={v:(s,t) for s,ts in TRANSFERS.items() for t,vs in ts.items() for v in vs}
    actual={v:pair for v,pair in now.items() if old.get(v)!=pair}
    checks['exactly_authorized_28_province_transfers']=actual==expected and len(actual)==28
    checks['province_id_universe_conserved']={r['key'][0] for r in before['owners']}=={r['key'][0] for r in after['owners']}
    checks['no_new_double_assignments']=all(v<=before['duplicates'].get(k,1) for k,v in after['duplicates'].items())
    new_errors=[r for r in after['errors'] if r not in before['errors']]
    checks['no_new_orphan_or_geometry_reference_errors']=not new_errors
    checks['moldavia_wallachia_subjects_ottoman_journals_ai_previous_maps_protected']=not unexpected
    syntax=[]
    for p in ALLOWED:
        if p.endswith('.txt'):
            try:cw.parse((ROOT/p).read_text(encoding='utf-8-sig'))
            except Exception as e:syntax.append([p,str(e)])
    checks['changed_script_braces_parse']=not syntax
    checks['native_game_date_trigger_not_current_date']=all(not any(n.key=='current_date' for n in cw.walk(cw.parse((ROOT/p).read_text(encoding='utf-8-sig')))) for p in ALLOWED if p.endswith('.txt'))
    hist=(ROOT/'common/history/states/00_states.txt').read_text(encoding='utf-8-sig')
    checks['no_accidental_git_commands_in_state_history']=not re.search(r'^\s*git\s+(?:status|fetch)\b',hist,re.M)
    force=cw.parse((ROOT/'common/diplomatic_actions/31_power_bloc_force_become_subject.txt').read_text(encoding='utf-8-sig'))[0]
    original_force=cw.parse(saved['originals']['common/diplomatic_actions/31_power_bloc_force_become_subject.txt'])[0]
    for key in ['selectable','potential','possible','accept_effect']:
        checks['crimean_action_'+key+'_unchanged']=qa.norm(force.children(key)[0])==qa.norm(original_force.children(key)[0])
    vanilla_invite=cw.parse((GAME/'common/diplomatic_actions/28_invite_to_power_bloc.txt').read_text(encoding='utf-8-sig'))[0]
    mod_invite=cw.parse((ROOT/'common/diplomatic_actions/28_invite_to_power_bloc.txt').read_text(encoding='utf-8-sig'))[0]
    for key in ['selectable','potential','possible','accept_effect','decline_effect']:
        checks['invitation_'+key+'_unchanged']=qa.norm(mod_invite.children(key)[0])==qa.norm(vanilla_invite.children(key)[0])
    treaty=cw.parse((ROOT/'common/history/treaties/1776_russian_guarantee_poland.txt').read_text(encoding='utf-8-sig'))[0].children('create_treaty')[0]
    articles=treaty.children('articles_to_create')[0].children();law=next(n for n in articles if n.one('article')=='law_commitment');guarantee=next(n for n in articles if n.one('article')=='guarantee_independence')
    checks['polish_law_commitment_russian_beneficiary']=law.one('source_country')=='c:PLC' and law.one('target_country')=='c:RUS'
    checks['russian_independence_guarantee_to_poland']=guarantee.one('source_country')=='c:RUS' and guarantee.one('target_country')=='c:PLC'
    laws={n.key for p in effective(ROOT,GAME,'common/laws') for n in cw.parse(p.read_text(encoding='utf-8-sig'))}
    plc=(ROOT/'common/history/countries/plc - polish-lithuania.txt').read_text(encoding='utf-8-sig')
    checks['guaranteed_law_exists_and_already_active']='law_oligarchy' in laws and 'activate_law = law_type:law_oligarchy' in plc
    # Exactly one matching guarantee/commitment in effective history, not a duplicate.
    matches=C.Counter()
    for p in effective(ROOT,GAME,'common/history/treaties'):
        for n in cw.walk(cw.parse(p.read_text(encoding='utf-8-sig'))):
            if n.one('article') in ['law_commitment','guarantee_independence'] and {n.one('source_country'),n.one('target_country')}=={'c:RUS','c:PLC'}:matches[(n.one('article'),n.one('source_country'))]+=1
    checks['no_duplicate_russian_polish_articles']=matches==C.Counter({('law_commitment','c:PLC'):1,('guarantee_independence','c:RUS'):1})
    checks['new_localizations_utf8_bom']=all((ROOT/f'localization/{lang}/1776_map2d_l_{lang}.yml').read_bytes().startswith(b'\xef\xbb\xbf') for lang in ['english','french'])
    regression=json.loads((OUT/'REGRESSION_TESTS.json').read_text(encoding='utf-8'))
    checks['existing_ottoman_fixture_suite']=regression['suites']['ottoman_journal_models']['status']=='PASS'
    checks['existing_infrastructure_fixture_suite']=regression['suites']['regional_infrastructure_shortage_models']['status']=='PASS'
    bmp=packed(source_bitmap())
    for sid,kind,want in [('STATE_BESSARABIA','mine','x79D62E'),('STATE_CHERSON','city','xFDD2CF')]:
        definition=next(n for p in effective(ROOT,GAME,'map_data/state_regions') for n in cw.parse(p.read_text(encoding='utf-8-sig')) if n.key==sid)
        locator=(GAME/f'gfx/map/map_object_data/generated_map_object_locators_{kind}.txt').read_text(encoding='utf-8-sig')
        pos={ident:(float(x),3616-float(z)) for ident,x,z in re.findall(r'id\s*=\s*(\d+)\s+position\s*=\s*\{\s*([\d.\-]+)\s+[\d.\-]+\s+([\d.\-]+)',locator)}
        x,y=pos[definition.one('id')]
        checks[sid+'_'+kind+'_hub_matches_physical_locator']=cw.scalar(definition.one(kind))==want=='x%06X'%int(bmp[int(y),int(x)])
    for p in ['map_data/state_regions/02_east_europe.txt','map_data/state_regions/15_russia.txt']:
        a=cw.parse(saved['originals'][p]);b=cw.parse((ROOT/p).read_text(encoding='utf-8-sig'))
        expected_key='STATE_BESSARABIA' if '02_east' in p else 'STATE_CHERSON';hub='mine' if '02_east' in p else 'city'
        def no_hub(nodes):return [[n.key,[qa.norm(x) for x in n.children() if not(n.key==expected_key and x.key==hub)]] for n in nodes]
        checks[p+'_only_target_hub_changed']=no_hub(a)==no_hub(b)
    pop_before=qa.counter(before['regional_pop']);pop_after=qa.counter(after['regional_pop']);population=[]
    for k in sorted(set(pop_before)|set(pop_after)):
        if k[0] in TRANSFERS:population.append([*k,pop_before[k],pop_after[k],pop_after[k]-pop_before[k]])
    population.append(['WORLD','ALL','ALL','ALL',sum(r['count'] for r in before['pops']),sum(r['count'] for r in after['pops']),0])
    rows=[]
    for rgb,(sid,tag) in sorted(expected.items()):
        yy,xx=np.where(bmp==int(rgb[1:],16))
        rows.append([rgb,sid,old[rgb][1],tag,'DOCUMENTED_GAMEPLAY_APPROXIMATION',int(len(xx)),int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())])
    result={'status':'PASS_STATIC' if all(checks.values()) else 'FAIL_STATIC','checks':checks,'native_engine_test':'NOT_RUN','world_population_before':sum(r['count'] for r in before['pops']),'world_population_after':sum(r['count'] for r in after['pops']),'province_transfers':len(actual),'redrawn_provinces':0,'protected_files_changed':changed,'new_runtime_files':new_runtime,'unexpected_changes':unexpected+unexpected_new,'new_reference_errors':new_errors,'preexisting_reference_errors_before':len(before['errors']),'reference_errors_after':len(after['errors']),'removed_reference_errors':[r for r in before['errors'] if r not in after['errors']],'duplicate_rgb_before':len(before['duplicates']),'duplicate_rgb_after':len(after['duplicates']),'syntax_errors':syntax,'regression_suites':regression['suites'],'commit_merge_push':'NOT_PERFORMED'}
    OUT.mkdir(exist_ok=True)
    (OUT/'MAP2D_VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'TABLE_DATA.json').write_text(json.dumps({'population':population,'territorial':rows,'validation':result},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='checks'},ensure_ascii=False,indent=2))
    print('Failed checks:',[k for k,v in checks.items() if not v])
    return all(checks.values())
if __name__=='__main__':sys.exit(0 if validate() else 1)
