"""Read-only yearly event-provider/dependency audit for #46.

Candidate overlays and deliberate regressions stay in memory. No installer,
source mutation, game launch, Git operation or old evidence overwrite.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import sys
sys.dont_write_bytecode=True
from issue24_map_dlc_audit import Audit, ROOT, GAME, parse, walk, plain
from issue44_event_targets_audit import payload, localization_catalogue, references
from issue45_yearly_dispatch_audit import inventory as list_inventory

EVIDENCE=ROOT/'docs/reports/compatibility/V1_15_ISSUE46_YEARLY_EVENT_TARGETS_2026_11_09'
FOLDERS={'events':'events','ideologies':'common/ideologies','laws':'common/laws',
 'lawgroups':'common/law_groups','modifiers':'common/static_modifiers',
 'templates':'common/character_templates','movements':'common/political_movements',
 'buildings':'common/buildings','methods':'common/production_methods',
 'cultures':'common/cultures','traits':'common/character_traits',
 'hierarchies':'common/social_hierarchies','technologies':'common/technology/technologies',
 'journals':'common/journal_entries','roles':'common/character_roles',
 'countries':'common/country_definitions','states':'map_data/state_regions',
 'effects':'common/scripted_effects','triggers':'common/scripted_triggers',
 'interest_groups':'common/interest_groups'}
SPEC={
 'marx_events.3':('events','events/karl_marx_events.txt'),
 'marx_events.4':('events','events/karl_marx_events.txt'),
 'japan_events.32':('events','events/japan_events/ep2_japan_events_03.txt'),
 'japan_events.33':('events','events/japan_events/ep2_japan_events_03.txt'),
 'japan_events.34':('events','events/japan_events/ep2_japan_events_03.txt'),
 'japan_events.35':('events','events/japan_events/ep2_japan_events_03.txt'),
 'ideology_state_socialist':('ideologies','common/ideologies/01_character_ideologies.txt'),
 'ideology_communist_leader':('ideologies','common/ideologies/01_character_ideologies.txt'),
 'law_labour_suffrage':('laws','common/laws/00_distribution_of_power.txt'),
 'ideology_communist_leader_valid_trigger':('triggers','common/scripted_triggers/00_victoria_scripted_triggers.txt'),
}
ANNUAL={'marx_events.3','japan_events.32','japan_events.33','japan_events.34','japan_events.35'}


def typed_refs(node,native_helpers):
    for n in walk(node.children()):
        category=target=None
        if n.key=='trigger_event': category,target='events',plain(n.one('id'))
        elif n.key=='add_modifier': category,target='modifiers',plain(n.one('name'))
        elif n.key=='has_template': category,target='templates',plain(n.value)
        elif n.key=='is_political_movement_type': category,target='movements',plain(n.value)
        elif n.key in ('has_law','has_law_or_variant','law') and isinstance(n.value,str) and n.value.startswith('law_type:'):
            category,target='laws',n.value.removeprefix('law_type:')
        elif n.key in ('is_building_type','building_type','has_building'):category,target='buildings',plain(n.value)
        elif n.key=='production_method':category,target='methods',plain(n.value)
        elif n.key in ('has_role','is_character_role'):category,target='roles',plain(n.value)
        elif n.key=='has_social_hierarchy':category,target='hierarchies',plain(n.value)
        elif n.key=='is_interest_group_type':category,target='interest_groups',plain(n.value)
        elif n.key=='has_ideology':category,target='ideologies',(plain(n.value) or '').removeprefix('ideology:')
        elif n.key=='add_trait':category,target='traits',plain(n.value)
        elif n.key=='has_technology_researched':category,target='technologies',plain(n.value)
        elif n.key=='has_journal_entry':category,target='journals',plain(n.value)
        elif n.key.startswith('lawgroup_'):category,target='lawgroups',n.key
        elif n.key.startswith('law_') and isinstance(n.value,str) and n.value in {'strongly_approve','approve','neutral','disapprove','strongly_disapprove'}:
            category,target='laws',n.key
        elif n.key in native_helpers:category,target=native_helpers[n.key],n.key
        if category and isinstance(target,str) and target:
            yield category,target
        for value in (n.key,plain(n.value)):
            m=re.fullmatch(r'(c|s|cu):([A-Za-z0-9_]+)',value or '')
            if m:yield {'c':'countries','s':'states','cu':'cultures'}[m.group(1)],m.group(2)
        if n.key=='group' and isinstance(n.value,str) and n.value.startswith('lawgroup_'):
            yield 'lawgroups',n.value
        if n.key in ('unlocking_laws','unlocking_technologies'):
            for x in n.children():
                if not x.key and isinstance(x.value,str):yield ('laws' if n.key=='unlocking_laws' else 'technologies'),plain(x.value)


def loc_keys(key,node):
    if key.endswith('_trigger'):return set()
    if not key.startswith(('marx_events.','japan_events.')):
        return {key,key+'_desc'}
    keys=set()
    for field in ('title','desc','flavor'):
        value=node.one(field)
        if isinstance(value,str):keys.add(plain(value))
    for child in walk(node.children()):
        if child.key=='desc' and isinstance(child.value,str):keys.add(plain(child.value))
        if child.key in ('custom_tooltip','custom_tooltip_no_bullet'):
            value=child.one('text') if isinstance(child.value,list) else child.value
            if isinstance(value,str):keys.add(plain(value))
    keys.update(plain(n.one('name')) for n in node.children('option'))
    return set(filter(None,keys))


def verify(objects,native_nodes,helper_kinds,locs,annual_rows):
    checks=[];dependencies=[];texts=[];helper_ids=set()
    def check(name,value):checks.append({'name':name,'passed':bool(value)})
    for key,(category,_) in SPEC.items():
        entries=objects[category].get(key,[])
        check(key+'.unique_provider',len(entries)==1)
        if len(entries)!=1:continue
        node=entries[0][0]
        expected=copy.deepcopy(native_nodes[key])
        if key=='marx_events.3':
            expected.children('trigger')[0].value.insert(1,parse('has_global_variable = big_communism_builder')[0])
            check(key+'.author_context_required',any(n.value=='big_communism_builder' for n in node.children('trigger')[0].children('has_global_variable')))
        if key=='ideology_communist_leader':
            for field in ('interest_group_leader_weight','non_interest_group_leader_weight'):
                expected.children(field)[0].value=parse('value = 0')
            check(key+'.nonrandom_compatibility_alias',all(payload(node.children(field)[0].children())==[('value','=','0')] for field in ('interest_group_leader_weight','non_interest_group_leader_weight')))
        suffix={ 'ideology_communist_leader':'.native_payload_except_two_alias_weights', 'marx_events.3':'.native_payload_except_required_author_context' }.get(key,'.exact_native_payload')
        check(key+suffix,payload([node])==payload([expected]))
        for cat,target in typed_refs(node,helper_kinds):
            providers=objects[cat].get(target,[])
            check(key+'.'+cat+'.'+target,len(providers)==1)
            dependencies.append({'consumer':key,'category':cat,'target':target,'providers':[p[1] for p in providers]})
            if cat in ('effects','triggers'):helper_ids.add((cat,target))
        if key in ANNUAL:
            rows=[r for r in annual_rows if r['target']==key and r['category']=='events']
            check(key+'.retained_annual_registration',len(rows)==1)
        if key.startswith('japan_events.'):
            trigger=node.children('trigger')
            check(key+'.DLC_gate_retained',node.one('dlc')=='dlc018' and any(n.key=='has_dlc_feature' and n.value=='ep2_content' for t in trigger for n in walk(t.children())))
        if key=='marx_events.3':
            delays=[n.one('years') for n in walk(node.children()) if n.key=='trigger_event' and n.one('id')=='marx_events.4']
            check(key+'.both_original_delays',delays==['16','8'])
        if key=='law_labour_suffrage':
            check(key+'.socialism_gate_retained',any(n.value=='socialism' for g in node.children('unlocking_technologies') for n in g.children()))
            check(key+'.council_republic_gate_retained',any(n.value=='law_council_republic' for g in node.children('unlocking_laws') for n in g.children()))
        keys=loc_keys(key,node)
        for lang,catalogue in locs.items():
            pending=list(keys);seen=set()
            while pending:
                name=pending.pop()
                if name in seen:continue
                seen.add(name);rows=catalogue.get(name,[])
                check(key+'.'+lang+'.'+name,len(rows)==1)
                texts.append({'consumer':key,'language':lang,'key':name,'providers':rows})
                if len(rows)==1:pending.extend(re.findall(r'\$([a-zA-Z0-9_.]+)\$',rows[0]['value']))
        icon=plain(node.one('icon'))
        if icon:check(key+'.icon_resource',(ROOT/icon).exists() or (GAME/icon).exists())
        window=plain(node.one('gui_window'))
        if window:
            gui=ROOT/'gui/eventwindow.gui'
            if not gui.exists():gui=GAME/'gui/eventwindow.gui'
            check(key+'.GUI_window',bool(re.search(r'name\s*=\s*"'+re.escape(window)+'"',gui.read_text(encoding='utf-8-sig'))))
    # One additional level resolves typed dependencies of directly used helpers.
    # It does not claim a complete transitive control-flow audit.
    for category,key in sorted(helper_ids):
        entries=objects[category].get(key,[])
        if len(entries)==1:
            for cat,target in typed_refs(entries[0][0],helper_kinds):
                check('helper.'+key+'.'+cat+'.'+target,len(objects[cat].get(target,[]))==1)
                dependencies.append({'consumer':'helper:'+key,'category':cat,'target':target,'providers':[p[1] for p in objects[cat].get(target,[])]})
    return checks,dependencies,texts


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--candidate',action='store_true');p.add_argument('--controls',action='store_true')
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();output=args.output.resolve()
    if not output.is_relative_to(EVIDENCE) or output.exists():p.error('Use a new evidence path; do not overwrite results.')
    audit=Audit(ROOT,GAME);objects={k:audit.load(k,v) for k,v in FOLDERS.items()}
    native=Audit(ROOT,GAME,True)
    native_helpers={}
    for category in ('effects','triggers'):
        native_helpers.update({key:category for key in native.load(category,FOLDERS[category])})
    native_nodes={}
    for key,(_,path) in SPEC.items():
        nodes,_,_=native.read(GAME/path);native_nodes[key]=next(n for n in nodes if n.key==key)
    manifest_path=EVIDENCE/'CANDIDATE_MANIFEST_R4.json'
    if not manifest_path.exists():manifest_path=EVIDENCE/'CANDIDATE_MANIFEST_R3.json'
    if not manifest_path.exists():manifest_path=EVIDENCE/'CANDIDATE_MANIFEST_R2.json'
    if not manifest_path.exists():manifest_path=EVIDENCE/'CANDIDATE_MANIFEST.json'
    manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    if args.candidate:
        for row in manifest['files']:
            category=next(cat for cat,folder in FOLDERS.items() if row['path'].startswith(folder+'/'))
            # Overlay the same runtime file during a revision; retain providers
            # from all other files so genuine duplicate IDs still fail.
            for key in list(objects[category]):
                objects[category][key]=[entry for entry in objects[category][key] if entry[1]!='mod/'+row['path']]
                if not objects[category][key]:del objects[category][key]
            raw=(EVIDENCE/manifest.get('candidate_directory','candidate')/row['path']).read_text(encoding='utf-8-sig')
            for node in parse(raw):
                if isinstance(node.value,list):objects[category].setdefault(node.key,[]).append((node,'candidate/'+row['path'],raw))
    on_actions,_,_=list_inventory(Audit(ROOT,GAME))
    direct=references(audit,objects['events'])
    locs={lang:localization_catalogue(lang) for lang in ('french','english')}
    checks,deps,texts=verify(objects,native_nodes,native_helpers,locs,on_actions['references'])
    checks.append({'name':'no_explicit_event_call_missing','passed':not direct['missing']})
    checks.append({'name':'only_deferred_on_memento_mori_missing_from_lists','passed':{r['target'] for r in on_actions['missing'] if r['target'] not in objects['events']} <= {'on_memento_mori'}})
    checks.append({'name':'yearly_dispatch_no_effect_trigger_conflicts','passed':not on_actions['collisions']})
    checks.append({'name':'parsed_inputs_valid','passed':not audit.errors})
    # Candidate lookup resolves five existing annual references without changing lists.
    remaining=[r for r in on_actions['missing'] if r['category']!='events' or r['target'] not in objects['events']]
    controls=[]
    if args.controls:
        for key,(category,_) in SPEC.items():
            changed=dict(objects);changed[category]=dict(objects[category]);changed[category].pop(key,None)
            c,_,_=verify(changed,native_nodes,native_helpers,locs,on_actions['references'])
            controls.append({'case':'missing.'+key,'passed':any(not r['passed'] and r['name']==key+'.unique_provider' for r in c)})
        for key,kind in [('japan_events.32','DLC'),('marx_events.3','delay'),('law_labour_suffrage','gate')]:
            category=SPEC[key][0];changed=dict(objects);changed[category]=dict(objects[category])
            entries=copy.deepcopy(objects[category][key]);changed[category][key]=entries;node=entries[0][0]
            if kind=='DLC':node.children('trigger')[0].value=[n for n in node.children('trigger')[0].children() if n.key!='has_dlc_feature']
            elif kind=='delay':next(n for n in walk(node.children()) if n.key=='trigger_event').children('years')[0].value='1'
            else:node.children('unlocking_laws')[0].value=[]
            c,_,_=verify(changed,native_nodes,native_helpers,locs,on_actions['references'])
            expected={'DLC':key+'.DLC_gate_retained','delay':key+'.both_original_delays','gate':key+'.council_republic_gate_retained'}[kind]
            controls.append({'case':'broken.'+kind,'passed':any(not r['passed'] and r['name']==expected for r in c)})
        changed=dict(locs);changed['french']=dict(locs['french']);changed['french'].pop('japan_events.32.t',None)
        c,_,_=verify(objects,native_nodes,native_helpers,changed,on_actions['references'])
        controls.append({'case':'missing_French_title','passed':any(not r['passed'] and r['name']=='japan_events.32.french.japan_events.32.t' for r in c)})
        changed=dict(objects);changed['ideologies']=dict(objects['ideologies'])
        entries=copy.deepcopy(objects['ideologies']['ideology_communist_leader']);changed['ideologies']['ideology_communist_leader']=entries
        entries[0][0].children('interest_group_leader_weight')[0].value=parse('value = 100')
        c,_,_=verify(changed,native_nodes,native_helpers,locs,on_actions['references'])
        controls.append({'case':'alias_accidentally_random','passed':any(not r['passed'] and r['name']=='ideology_communist_leader.nonrandom_compatibility_alias' for r in c)})
        changed=dict(objects);changed['events']=dict(objects['events'])
        entries=copy.deepcopy(objects['events']['marx_events.3']);changed['events']['marx_events.3']=entries
        guard=entries[0][0].children('trigger')[0]
        guard.value=[n for n in guard.children() if not (n.key=='has_global_variable' and n.value=='big_communism_builder')]
        c,_,_=verify(changed,native_nodes,native_helpers,locs,on_actions['references'])
        controls.append({'case':'missing_author_context_guard','passed':any(not r['passed'] and r['name']=='marx_events.3.author_context_required' for r in c)})
    result={'status':'PASS_SCOPED_STATIC_ONLY' if all(r['passed'] for r in checks+controls) else 'FAIL_STATIC',
        'mode':'candidate' if args.candidate else 'live','checks':checks,'controls':controls,
        'dependencies':deps,'localization':texts,'on_action_inventory':on_actions,
        'remaining_list_targets_after_overlay':remaining,'explicit_event_calls':direct,
        'source_hashes':audit.hashes,'native_source_hashes':native.hashes,'engine_tested':False,
        'limits':['Literal providers and one helper level, not complete runtime control-flow proof.',
                  'Existing marx_events.1 does not write big_communism_builder; its authored flow is preserved.',
                  'No restoration of on_memento_mori or rewrite of #45 dispatch.']}
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
    print(json.dumps({'status':result['status'],'checks':[sum(x['passed'] for x in checks),len(checks)],
      'controls':[sum(x['passed'] for x in controls),len(controls)],'remaining_list_targets':remaining,
      'failed':[x['name'] for x in checks if not x['passed']]},ensure_ascii=False))
    return 1 if result['status']=='FAIL_STATIC' else 0


if __name__=='__main__':raise SystemExit(main())
