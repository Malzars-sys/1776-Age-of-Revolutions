"""Static cost checks and projections of the actual construction-maintenance AST.

Does not execute Victoria 3 or prove the timing of native callbacks/queues.
"""
from copy import deepcopy
from decimal import Decimal
from hashlib import sha256
from pathlib import Path
import json
import re
import subprocess
from validate_diplomacy_ottoman_1776 import parse, normalized, walk
from localization_duplicate_audit import entries

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'docs/reports/military/LAND_FORTIFICATIONS/CONSTRUCTION_R1'
TYPE='building_aor1776_land_fortification'
GROUP='bg_aor1776_land_fortification'
MODTYPE='building_group_'+GROUP+'_construction_efficiency_add'
PENDING='aor1776_fort_construction_monitor_pending'
TICK='aor1776_fort_construction_monitor_tick'
FILES={
 'building':'common/buildings/1776_land_fortifications.txt',
 'group':'common/building_groups/1776_land_fortifications.txt',
 'cost':'common/script_values/1776_land_fortification_construction.txt',
 'modifier_type':'common/modifier_type_definitions/1776_land_fortification_construction.txt',
 'modifiers':'common/static_modifiers/1776_land_fortification_construction.txt',
 'triggers':'common/scripted_triggers/1776_land_fortification_construction.txt',
 'effects':'common/scripted_effects/1776_land_fortification_construction.txt',
 'actions':'common/on_actions/1776_land_fortification_construction.txt',
}
read=lambda rel:(ROOT/rel).read_text(encoding='utf-8-sig')
digest=lambda p:sha256(p.read_bytes()).hexdigest()
DB={kind:{n.key:n for n in parse(read(path))} for kind,path in FILES.items()}
CHECKS={};CASES=[]
def check(name,result): CHECKS[name]=bool(result)


class Projection:
    def __init__(self,countries):
        self.countries=countries;self.queue=[];self.day=0

    def test(self,nodes,obj):
        def one(n):
            if n.key=='OR': return any(one(x) for x in n.children())
            if n.key in {'NOT','NOR'}: return not any(one(x) for x in n.children())
            if n.key=='has_modifier': return n.value in obj.get('modifiers',set())
            if n.key=='has_variable': return n.value in obj.get('variables',{})
            if n.key=='is_building_type': return obj['type']==n.value
            if n.key=='any_scope_state': return any(self.test(n.children(),s) for s in obj['states'])
            if n.key=='state_has_building_type_levels':
                assert n.one('target')=='bt:'+TYPE
                op=n.children('value')[0];value=int(op.value);actual=obj['level']
                return {'>=':actual>=value,'>':actual>value,'=':actual==value,'<':actual<value,'<=':actual<=value}[op.op]
            if n.key in DB['triggers']:
                return self.test(DB['triggers'][n.key].children(),obj)==(n.value=='yes')
            raise ValueError('Unsupported trigger: '+n.key)
        return all(one(n) for n in nodes)

    def effect(self,nodes,obj):
        chain=False
        for n in nodes:
            if n.key in {'if','else_if','else'}:
                if n.key=='if': chain=False
                run=not chain and (n.key=='else' or self.test(n.children('limit')[0].children(),obj))
                if run:
                    self.effect([x for x in n.children() if x.key!='limit'],obj);chain=True
            elif n.key in DB['effects']: self.effect(DB['effects'][n.key].children(),obj)
            elif n.key=='remove_modifier': obj['modifiers'].discard(n.value)
            elif n.key=='add_modifier': obj['modifiers'].add(n.one('name'))
            elif n.key=='remove_variable': obj['variables'].pop(n.value,None)
            elif n.key=='set_variable': obj['variables'][n.one('name')]=self.day+int(n.one('days'))
            elif n.key=='trigger_event': self.queue.append((self.day+int(n.one('days')),n.one('on_action'),obj))
            elif n.key in {'state','owner'}:
                target=obj.get(n.key)
                if target is not None: self.effect(n.children(),target)
                elif n.op!='?=': raise ValueError('Missing scope: '+n.key)
            elif n.key in {'every_country','every_scope_state'}:
                targets=self.countries if n.key=='every_country' else obj['states']
                limits=n.children('limit')
                for target in targets:
                    if not limits or self.test(limits[0].children(),target):
                        self.effect([x for x in n.children() if x.key!='limit'],target)
            else: raise ValueError('Unsupported effect: '+n.key)

    def action(self,key,obj=None):
        n=DB['actions'][key]
        trigger=n.children('trigger')
        if trigger and not self.test(trigger[0].children(),obj): return
        for effect in n.children('effect'): self.effect(effect.children(),obj)
        for links in n.children('on_actions'):
            for link in links.children(): self.action(link.value,obj)

    def tick(self):
        self.day+=1
        for country in self.countries:
            country['variables']={k:v for k,v in country['variables'].items() if v>self.day}
        due=[item for item in self.queue if item[0]<=self.day]
        self.queue=[item for item in self.queue if item[0]>self.day]
        for _,key,obj in due: self.action(key,obj)


def country(): return dict(states=[],variables={})
def state(level,owner,**fields):
    result=dict(level=level,owner=owner,modifiers=set(),**fields)
    owner['states'].append(result);return result
def penalty(obj):
    return sum((Decimal(DB['modifiers'][name].one(MODTYPE)) for name in obj['modifiers']),Decimal(0))


def main():
    for kind,rel in FILES.items(): check('syntax.'+kind,bool(DB[kind]))
    building=DB['building'][TYPE]
    value=DB['cost'][building.one('required_construction')].value
    check('cost.displayed_900',value=='900')
    check('group.native_efficiency_enabled',DB['group'][GROUP].one('construction_efficiency_modifier')=='yes')
    check('modifier.native_exact_group_key',set(DB['modifier_type'])=={MODTYPE})
    check('modifier.only_this_group_targeted',all(
        {n.key for n in mod.children() if n.key!='icon'}=={MODTYPE} for mod in DB['modifiers'].values()))
    base=json.loads((REPORT/'BASELINE.json').read_text(encoding='utf-8'))
    for kind,field in [('building','required_construction'),('group','construction_efficiency_modifier')]:
        before=parse((REPORT/'baseline'/FILES[kind]).read_text(encoding='utf-8-sig'))
        current=deepcopy(list(DB[kind].values()))
        for n in current: n.value[:]=[x for x in n.children() if x.key!=field]
        for n in before: n.value[:]=[x for x in n.children() if x.key!=field]
        check('preservation.only_'+field+'_changed',normalized(before)==normalized(current))

    # Independently specified effective targets; exercise the real branch AST.
    for pm in [1,2,3]:
        for staffing in [0,Decimal('.25'),1]:
            for level,target in enumerate([900,1100,1300,1500,1700,1700]):
                c=country();s=state(level,c,pm=pm,staffing=staffing,queued=5-level);p=Projection([c])
                p.effect(DB['effects']['aor1776_refresh_fort_construction_state'].children(),s)
                expected=set() if level==0 else {f'aor1776_fort_construction_level_{min(level,4)}'}
                cost=Decimal(900)/(1+penalty(s))
                check(f'calibration.{pm}.{staffing}.{level}',s['modifiers']==expected and abs(cost-target)<Decimal('.01'))
                check(f'calibration.efficiency_positive.{pm}.{staffing}.{level}',1+penalty(s)>Decimal('.5'))
                CASES.append(dict(level=level,pm=pm,staffing=str(staffing),penalty=str(penalty(s)),effective_cost=str(cost),target=target))
    for stale in [set(),set(DB['modifiers']),{'aor1776_fort_construction_level_4'}]:
        c=country();s=state(5,c);s['modifiers']=set(stale);p=Projection([c])
        for level in [5,4,3,2,1,0,2,4,0]:
            s['level']=level;p.action('on_monthly_pulse_state',s)
            expected=set() if level==0 else {f'aor1776_fort_construction_level_{min(level,4)}'}
            check(f'cleanup.correct_tier.{len(stale)}.{level}',s['modifiers']==expected)
    c=country();s=state(0,c);p=Projection([c]);b=dict(type=TYPE,state=s,owner=c)
    p.action('on_start_expanding_building',b)
    check('lifecycle.first_level_no_penalty_or_monitor',not s['modifiers'] and not p.queue)
    for level in range(1,6):
        s['level']=level;p.action('on_building_built' if level==1 else 'on_building_expanded',b)
        p.action('on_start_expanding_building',b)
        check('lifecycle.single_monitor.'+str(level),len(p.queue)==1 and PENDING in c['variables'])
        check('lifecycle.immediate_completed_level.'+str(level),s['modifiers']=={f'aor1776_fort_construction_level_{min(level,4)}'})
    s['level']=2;p.tick()
    check('lifecycle.downsize_next_day',s['modifiers']=={'aor1776_fort_construction_level_2'} and len(p.queue)==1)
    s['level']=0;p.tick()
    check('lifecycle.demolition_cleanup_and_stop',not s['modifiers'] and not p.queue and PENDING not in c['variables'])
    c1,c2=country(),country();s=state(3,c1);p=Projection([c1,c2]);p.action('on_game_started')
    p.action('on_game_started_after_lobby')
    check('lifecycle.startup_idempotent',len(p.queue)==1)
    c1['states'].remove(s);c2['states'].append(s);s['owner']=c2;p.action('on_state_owner_change',s);p.tick()
    check('lifecycle.transfer_new_owner_only',len(p.queue)==1 and p.queue[0][2] is c2 and s['modifiers']=={'aor1776_fort_construction_level_3'})
    # Old-save marker with a lost callback can expire and be repaired monthly.
    p.queue.clear();p.tick();p.tick();p.action('on_monthly_pulse_state',s)
    check('lifecycle.monthly_lost_monitor_repair',len(p.queue)==1)
    other=dict(type='building_naval_fortification',state=s,owner=c2)
    before=(deepcopy(s['modifiers']),len(p.queue));p.action('on_building_expanded',other)
    check('scope.other_buildings_do_not_trigger',(s['modifiers'],len(p.queue))==before)

    # Native callback names and roots are checked against canonical examples.
    native=parse((Path('C:/Games/Victoria 3/game/common/on_actions/00_code_on_actions.txt')).read_text(encoding='utf-8-sig'))
    native_keys={n.key for n in native}
    check('hooks.native_parent_actions_exist',all(k in native_keys for k in DB['actions'] if k.startswith('on_')))
    check('hooks.only_add_child_actions',all([x.key for x in DB['actions'][k].children()]==['on_actions'] for k in DB['actions'] if k.startswith('on_')))
    known=set(DB['effects'])|set(DB['triggers'])|set(DB['actions'])|set(DB['modifiers'])|set(DB['cost'])
    check('references.custom_keys_resolve',all(n.key in known or n.key==MODTYPE for kind in ['effects','triggers','actions']
        for node in DB[kind].values() for n in walk([node]) if n.key.startswith('aor1776_')))
    keysets=[]
    for lang in ['french','english']:
        path=ROOT/f'localization/{lang}/1776_land_fortification_construction_l_{lang}.yml'
        text=path.read_text(encoding='utf-8-sig');catalog=entries(lang)
        keys=set(re.findall(r'(?m)^ ([A-Za-z0-9_]+):0 "[^"\n]*"$',text))
        wanted={MODTYPE,MODTYPE+'_desc'}|set(DB['modifiers'])|{k+'_desc' for k in DB['modifiers']}
        check('localization.BOM_and_all_keys.'+lang,path.read_bytes().startswith(b'\xef\xbb\xbf') and keys==wanted and text.startswith('l_'+lang+':\n'))
        check('localization.unique.'+lang,all(len(catalog[k])==1 for k in keys))
        keysets.append(keys)
    check('localization.same_FR_EN',keysets[0]==keysets[1])
    tooltip_baseline=json.loads((REPORT.parent/'TOOLTIPS_R1/BASELINE.json').read_text(encoding='utf-8'))
    protected={rel:h for rel,h in base['protected'].items() if rel not in tooltip_baseline['owned']}
    protected.update(tooltip_baseline['protected'])
    changed=[rel for rel,h in protected.items() if digest(ROOT/rel)!=h]
    check('preservation.other_gameplay_maps_and_art',not changed)
    check('preservation.HEAD',subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==base['head'])
    check('preservation.index',digest(ROOT/'.git/index')==base['index_sha256'])
    result=dict(status='PASS_STATIC' if all(CHECKS.values()) else 'FAIL_STATIC',passed=sum(CHECKS.values()),total=len(CHECKS),
                failed=[k for k,v in CHECKS.items() if not v],checks=CHECKS,scenarios=CASES,
                protected_file_count=len(protected),changed_protected_files=changed,runtime='NOT_RUN',
                limitation='Synthetic AST projections; native efficiency precision, callback timing and construction queues require runtime testing.',
                source_sha256={p:digest(ROOT/p) for p in FILES.values()})
    (REPORT/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ['status','passed','total','failed','protected_file_count','changed_protected_files','runtime']},indent=2))
    return 0 if all(CHECKS.values()) else 1


if __name__=='__main__': raise SystemExit(main())
