"""Conservative written inventories and reference pointers, never transfer code."""
import collections as C
import json,re,hashlib
from map1_prepare import ROOT,OUT,INPUT,GAME,table,savecsv,protected
from map_1776_audit import trees,label,own_inventory,values,prov
from validate_diplomacy_ottoman_1776 import walk,scalar,normalized

def main():
    before=json.loads((OUT/'MAP1_RUNTIME_BEFORE.json').read_text())
    assert protected()==before
    master=table(INPUT/'map1_outputs/WORLD_BORDERS_1776_MASTER.csv')
    candidates=[r for r in master if r['MAP1_Action_Class']=='OWNER_CHANGE_CANDIDATE']
    assert len(candidates)==80
    priorities=table(INPUT/'map1_outputs/MAP1_PRIORITY_ARBITRATION.csv')
    targetstates={r['State_ID'] for r in candidates}|{r['State_ID'] for r in priorities}
    tags={r[k] for r in candidates for k in ('Current_Owner_TAG','Proposed_Owner_TAG') if r[k] not in ('NEW_TAG_REQUIRED','UNCHANGED','')}
    tags|={'LUX','BEO','AUS','VEN','MOL','CRI','TUR'}
    owners,pairs,odd=own_inventory(ROOT,GAME)
    registry={}; definitions={}
    for p,raw,ns in trees(ROOT,GAME,'common/country_definitions'):
        for n in ns:
            if n.children('country_type'): registry[n.key.removeprefix('REPLACE_OR_CREATE:')]=dict(Source=label(p,ROOT,GAME),Line=raw[:n.start].count('\n')+1,Capital=scalar(n.one('capital','')),Definition=normalized(n.children()))
    for p,raw,ns in trees(ROOT,GAME,'map_data/state_regions'):
        for n in ns:
            if n.key in targetstates: definitions[n.key]=dict(Source=label(p,ROOT,GAME),Line=raw[:n.start].count('\n')+1,Definition=normalized(n.children()))
    inventories=C.defaultdict(lambda:C.defaultdict(list)); pops=[]; buildings=[]
    for folder in ('pops','buildings','population'):
        for p,raw,ns in trees(ROOT,GAME,'common/history/'+folder):
            for state in walk(ns):
                if not state.key.startswith('s:STATE_') or state.key[2:] not in targetstates: continue
                sid=state.key[2:]
                for selector in state.children():
                    if not selector.key.startswith('region_state:'): continue
                    tag=selector.key.split(':',1)[1]
                    entry=dict(State_ID=sid,Owner_TAG=tag,Source=label(p,ROOT,GAME),Line=raw[:selector.start].count('\n')+1,
                               Selector_Has_Territory=bool(pairs.get((sid,tag))),Written_Commands=normalized(selector.children()))
                    inventories[sid][folder].append(entry)
                    for n in selector.children('create_pop'):
                        pops.append(dict(State_ID=sid,Owner_TAG=tag,Culture=scalar(n.one('culture','UNSPECIFIED')),Religion=scalar(n.one('religion','UNSPECIFIED')),
                                         Size=int(scalar(n.one('size','0'))),Source=entry['Source'],Line=raw[:n.start].count('\n')+1,Selector_Has_Territory=entry['Selector_Has_Territory']))
                    for n in selector.children('create_building'):
                        ownlevels=[int(scalar(k.value)) for a in n.children('add_ownership') for k in walk(a.children()) if k.key=='levels' and not isinstance(k.value,list)]
                        buildings.append(dict(State_ID=sid,Owner_TAG=tag,Building=scalar(n.one('building','')),Explicit_Level=scalar(n.one('level','UNSPECIFIED')),
                          Ownership_Levels_Written_Sum=sum(ownlevels),Production_Methods='|'.join(values(n,'activate_production_methods')),
                          Written_Commands_JSON=json.dumps(normalized(n.children()),ensure_ascii=False),Source=entry['Source'],Line=raw[:n.start].count('\n')+1,
                          Selector_Has_Territory=entry['Selector_Has_Territory'],Engine_Effective_Level='NOT_SIMULATED'))
    savecsv('MAP1_POP_INVENTORY.csv',pops); savecsv('MAP1_BUILDING_INVENTORY.csv',buildings)
    # Text references are leads, not executed dependency paths; preserve location.
    tokens=targetstates|tags
    pat=re.compile(r'(?<![A-Za-z0-9_])('+'|'.join(re.escape(x) for x in sorted(tokens,key=len,reverse=True))+r')(?![A-Za-z0-9_])')
    refs=[]; bytoken=C.defaultdict(list)
    for folder in ('common','events','localization','map_data'):
        for p in sorted((ROOT/folder).rglob('*')):
            if p.suffix not in ('.txt','.yml','.map'): continue
            raw=p.read_text(encoding='utf-8-sig')
            for line,text in enumerate(raw.splitlines(),1):
                active=text.split('#',1)[0] if p.suffix!='.yml' else text
                for token in sorted(set(pat.findall(active))):
                    rec=dict(Identifier=token,File=p.relative_to(ROOT).as_posix(),Line=line,Text=text.strip(),Reference_Kind='LEXICAL_NOT_EXECUTION_PROOF')
                    refs.append(rec); bytoken[token].append(rec)
    savecsv('MAP1_DEPENDENCY_REFERENCES.csv',refs)
    depdir=OUT/'MAP1_DEPENDENCY_DOSSIERS'; depdir.mkdir(exist_ok=True)
    for sid in sorted(targetstates):
        payload=dict(State_ID=sid,Interpretation='Written effective-file selectors only. No engine, script execution, recruitment, defaults or addition/replace semantics simulated.',
                     Definition=definitions.get(sid),Current_Province_Attributions={tag:ps for (s,tag),ps in pairs.items() if s==sid},
                     Inventories=inventories[sid],Reference_Pointers=bytoken[sid])
        (depdir/(sid+'.json')).write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    (depdir/'COUNTRY_REGISTRY.json').write_text(json.dumps({t:registry.get(t) for t in sorted(tags)},ensure_ascii=False,indent=2),encoding='utf-8')
    rows=[]
    for r in candidates:
        sid=r['State_ID']; cur=r['Current_Owner_TAG']; prop=r['Proposed_Owner_TAG']
        rows.append(dict(Change_ID=r['Change_ID'],State_ID=sid,Research_Current_Owner_TAG=cur,Research_Proposed_Owner_TAG=prop,
            Proposed_TAG_Registry_Status='DEFINED' if prop in registry else ('NOT_A_TAG' if prop=='NEW_TAG_REQUIRED' else 'UNDEFINED'),
            Current_Owner_Search_Domain_RGBs='|'.join(pairs.get((sid,cur),[])),Verified_Province_IDs='',Mapping_Status='MAPPING_REQUIRED',
            Current_Pop_Records_Written=sum(x['State_ID']==sid and x['Owner_TAG']==cur for x in pops),
            Current_Pop_Size_Written=sum(x['Size'] for x in pops if x['State_ID']==sid and x['Owner_TAG']==cur),
            Current_Create_Building_Commands=sum(x['State_ID']==sid and x['Owner_TAG']==cur for x in buildings),
            Dependency_Artifact='MAP1_DEPENDENCY_DOSSIERS/'+sid+'.json',
            Country_Registry_Artifact='MAP1_DEPENDENCY_DOSSIERS/COUNTRY_REGISTRY.json',
            Reference_Pointer_Table='MAP1_DEPENDENCY_REFERENCES.csv',
            Unresolved_Uncertainty=r['Unresolved_Uncertainty'],Admissible_Transfer='NO',Apply_To_Mod='NO',Approved_By_User='NO'))
    savecsv('MAP1_TRANSFER_CANDIDATES_NOT_ADMISSIBLE.csv',rows)
    assert protected()==before
    validation=dict(Candidates_Not_Admissible=len(rows),States_Inventoried=len(targetstates),Written_Pop_Records=len(pops),
                    Written_Create_Building_Commands=len(buildings),Reference_Pointers=len(refs),Runtime_Unchanged=True,Engine_Simulated=False)
    (OUT/'MAP1_DEPENDENCY_VALIDATION.json').write_text(json.dumps(validation,indent=2),encoding='utf-8')
    print(json.dumps(validation))
if __name__=='__main__': main()
