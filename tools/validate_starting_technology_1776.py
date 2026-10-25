"""Read-only per-TAG starting-knowledge contract for territorial agents.

No uniform technology tier, implicit grant, game launch, or territorial write.
Use collect_snapshot() once, then audit_country(tag, snapshot, expectations).
An explicit empty-profile policy is evidence, never an automatic historical PASS.
"""
import argparse,collections,json,sys
from pathlib import Path
import audit_starting_tech_1776 as core

def walk(nodes):
    for n in nodes:
        yield n
        if isinstance(n.value,list):yield from walk(n.children())

def collect_snapshot():
    techs,_,_=core.objects('common/technology/technologies')
    effects,_,_=core.objects('common/scripted_effects')
    definitions,_,_=core.objects('common/country_definitions')
    buildings,_,_=core.objects('common/buildings')
    pms,_,_=core.objects('common/production_methods')
    groups,_,_=core.objects('common/production_method_groups')
    regions,_,_=core.objects('map_data/state_regions')
    laws,_,_=core.objects('common/laws');units,_,_=core.objects('common/combat_unit_types')
    inv=core.qa.inventory();histories=collections.defaultdict(list);nodes=collections.defaultdict(list)
    for p in core.effective('common/history/countries'):
        for root in core.cw.parse(p.read_text(encoding='utf-8-sig')):
            for country in root.children():
                if country.key.startswith('c:'):
                    tag=country.key[2:];histories[tag].append(core.ref(p));nodes[tag]+=country.children()
    starts={};requests={}
    for tag in {s[1] for s in inv['states']}:
        g,c,called,unresolved=core.resolve(nodes[tag],effects,techs)
        starts[tag]=dict(technologies=sorted(g),conditional_technologies=sorted(c),effects=called,unresolved=unresolved,history=histories[tag])
        # Includes conditional requested laws: these are requests, not certified active laws.
        expanded=list(nodes[tag])+[n for effect in called if effect in effects for n in effects[effect].children()]
        requests[tag]=sorted({core.cw.scalar(n.value).removeprefix('law_type:') for n in walk(expanded) if n.key=='activate_law' and isinstance(n.value,str)})
    selected={};declarations=collections.Counter();unassigned=[]
    for p in core.effective('common/history/buildings'):
        for root in core.cw.parse(p.read_text(encoding='utf-8-sig')):
            for state in root.children():
                if not state.key.startswith('s:STATE_'):continue
                for country in state.children():
                    if not country.key.startswith('region_state:'):continue
                    for n in country.children('create_building'):
                        kind=core.val(n,'building');key=(state.key[2:],country.key.split(':',1)[1],kind);declarations[key]+=1
                        target=selected.setdefault(key,{})
                        for pm in core.values(n,'activate_production_methods'):
                            matching=[g for g in core.values(buildings[kind],'production_method_groups') if g in groups and pm in core.values(groups[g],'production_methods')] if kind in buildings else []
                            for group in matching:target[group]=pm
                            if not matching:unassigned.append((key,pm))
    _,classified=core.historical.parse_graph_and_classifications()
    return dict(starts=starts,techs=techs,graph={k:core.values(n,'unlocking_technologies') for k,n in techs.items()},definitions=definitions,buildings=buildings,pms=pms,groups=groups,regions=regions,laws=laws,units=units,inventory=inv,selected=selected,declarations=declarations,unassigned=unassigned,law_requests=requests,late={k for k,c in classified.items() if c in {'C','D'}}|set(core.historical.FORBIDDEN_START_TECHS))

def audit_country(tag,snapshot=None,expectations=None):
    """Return findings; historical expectations must be supplied for that particular TAG.

    expectations: required/forbidden/allowed technology IDs, historical_evidence,
    absence_policy ('OPEN_DOCUMENTED_REVIEW' or 'INTENTIONAL_VERIFIED') and
    absence_evidence. Missing evidence never certifies an intentional omission.
    Construction, PM, law-request, unit and regional resource checks stay separate.
    """
    s=snapshot if snapshot is not None else collect_snapshot();e=expectations or {};findings=[]
    def add(priority,code,**detail):findings.append(dict(priority=priority,code=code,**detail))
    if tag not in s['starts']:return dict(TAG=tag,status='FAIL_STATIC',findings=[dict(priority='P0',code='UNKNOWN_OR_INACTIVE_TAG')],automated_engine_test=False)
    start=s['starts'][tag];known=set(start['technologies'])
    if not start['history']:
        policy=e.get('absence_policy');evidence=e.get('absence_evidence')
        if policy=='INTENTIONAL_VERIFIED' and evidence:add('P4','DOCUMENTED_INTENTIONAL_NO_HISTORY',evidence=evidence)
        elif policy=='OPEN_DOCUMENTED_REVIEW' and evidence:add('P3','NO_HISTORY_REVIEW_OPEN',evidence=evidence)
        else:add('P0','MISSING_HISTORY_WITHOUT_EVIDENCE')
    if not known and start['history']:add('P3','EMPTY_KNOWLEDGE_SET_REQUIRES_REGIONAL_EVIDENCE')
    for k in sorted(known-set(s['graph'])):add('P0','UNKNOWN_TECHNOLOGY',technology=k)
    for k in sorted(known):
        for parent in sorted(set(s['graph'].get(k,[]))-known):add('P1','MISSING_TECH_PARENT',technology=k,parent=parent)
    for x in start['unresolved']:add('P0','UNRESOLVED_START_EFFECT',reference=x)
    for x in start['conditional_technologies']:add('P3','CONDITIONAL_GRANT_NOT_CERTIFIED_INITIAL',technology=x)
    for x in sorted(known&s['late']):add('P2','HISTORICAL_ANACHRONISM_FLAG_REQUIRES_SOURCE',technology=x)
    if not e.get('historical_evidence'):add('P3','HISTORICAL_PROFILE_NOT_CERTIFIED')
    for x in sorted(set(e.get('required',[]))-known):add('P1','REQUIRED_LOCAL_CAPABILITY_MISSING',technology=x)
    for x in sorted(set(e.get('forbidden',[]))&known):add('P1','FORBIDDEN_LOCAL_START_TECH',technology=x)
    if 'allowed' in e:
        for x in sorted(known-set(e['allowed'])):add('P2','OUTSIDE_REVIEWED_LOCAL_PROFILE',technology=x)
    country_buildings=[]
    for (state,country,kind),selection in sorted(s['selected'].items()):
        if country!=tag:continue
        record=dict(state=state,building=kind,explicit_declarations=s['declarations'][(state,country,kind)],selected_PM_by_group=selection,construction_missing=[],PM_missing={})
        if kind not in s['buildings']:add('P0','UNKNOWN_BUILDING',state=state,building=kind);country_buildings.append(record);continue
        record['construction_missing']=sorted(set(core.values(s['buildings'][kind],'unlocking_technologies'))-known)
        if record['construction_missing']:add('P1','CONSTRUCTION_GATE_ONLY',state=state,building=kind,missing=record['construction_missing'],production_failure_proved=False)
        for group,pm in selection.items():
            if pm not in s['pms']:add('P0','UNKNOWN_PM',state=state,building=kind,PM=pm);continue
            missing=sorted(set(core.values(s['pms'][pm],'unlocking_technologies'))-known);record['PM_missing'][pm]=missing
            if missing:add('P0','SELECTED_PM_UNLOCK_GATE',state=state,building=kind,PM=pm,missing=missing,engine_inactivity_observed=False)
        if (kind.endswith('_mine') or kind.endswith('_quarry') or kind=='building_gold_fields') and state in s['regions']:
            region=s['regions'][state];quantity=sum(float(n.value) for cap in region.children('capped_resources') for n in cap.children() if n.key==kind)
            quantity+=sum(float(core.val(n,'discovered_amount','0')) for n in region.children('resource') if core.val(n,'type')==kind)
            record['regional_discovered_resource']=quantity;record['owner_portion_not_certified']=True
            if quantity<=0:add('P3','REGIONAL_RESOURCE_TEMPLATE_WARNING',state=state,building=kind,final_owner_allocation_certified=False)
        country_buildings.append(record)
    for key,pm in s['unassigned']:
        if key[1]==tag:add('P1','DECLARED_PM_NOT_IN_BUILDING_GROUP',state=key[0],building=key[2],PM=pm,engine_selection_unknown=True)
    for law in s['law_requests'].get(tag,[]):
        if law not in s['laws']:add('P1','UNKNOWN_REQUESTED_LAW',law=law)
        else:
            missing=sorted(set(core.values(s['laws'][law],'unlocking_technologies'))-known)
            if missing:add('P1','REQUESTED_LAW_TECH_GATE',law=law,missing=missing,actual_active_law_not_certified=True)
    types=set()
    def unit_walk(node):
        if not isinstance(node,list):return
        if len(node)==3 and node[0]=='type' and isinstance(node[2],str) and 'unit_type:' in node[2]:types.add(node[2].strip('"').split(':')[-1])
        for x in node:
            if isinstance(x,list):unit_walk(x)
    for row in s['inventory']['units']:
        if row['key'][0]==tag:unit_walk(json.loads(row['key'][3]))
    for unit in sorted(types):
        if unit not in s['units']:add('P0','UNKNOWN_UNIT_TYPE',unit=unit)
        else:
            missing=sorted(set(core.values(s['units'][unit],'unlocking_technologies'))-known)
            if missing:add('P1','INITIAL_UNIT_RECRUITMENT_GATE',unit=unit,missing=missing,existing_unit_operation_not_certified=True)
    severity={f['priority'] for f in findings}
    return dict(TAG=tag,status='FAIL_STATIC' if 'P0' in severity or 'P1' in severity else 'REVIEW' if 'P2' in severity or 'P3' in severity else 'PASS_STATIC_ONLY',technologies=sorted(known),history=start['history'],buildings=country_buildings,law_requests=s['law_requests'].get(tag,[]),unit_types=sorted(types),findings=findings,selection_model='Last explicit PM per group by effective filename order; omitted groups and engine defaults require runtime observation.',automated_engine_test=False,human_validated=False)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--tag',action='append',required=True);p.add_argument('--expectations',type=Path);p.add_argument('--output',type=Path);args=p.parse_args()
    expected=core.load(args.expectations) if args.expectations else {};s=collect_snapshot();results=[audit_country(t,s,expected.get(t,{})) for t in args.tag]
    raw=json.dumps(results,ensure_ascii=False,indent=2)+'\n'
    if args.output:args.output.write_text(raw,encoding='utf8')
    else:print(raw,end='')
    return int(any(r['status']=='FAIL_STATIC' for r in results))
if __name__=='__main__':sys.exit(main())
