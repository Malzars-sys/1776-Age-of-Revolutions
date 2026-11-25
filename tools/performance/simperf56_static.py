"""Static workload inventory, not a runtime profiler. Writes new issue-56 reports only."""
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
import re
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from validate_diplomacy_ottoman_1776 import parse, walk

STEAM = Path('C:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game')
REPORT = ROOT / 'docs/reports/performance/INITIAL_SIMULATION_ISSUE56_2026_11_17'
SHA = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
REPLACE = json.loads((ROOT / '.metadata/metadata.json').read_text(encoding='utf-8-sig'))['game_custom_data']['replace_paths']
WORLD = {'every_country','any_country','ordered_country','random_country','every_state','any_state','every_market','any_market','every_pop','any_pop'}
SCOPED = {'every_scope_state','any_scope_state','ordered_scope_state','every_scope_building','any_scope_building','every_scope_pop','any_scope_pop','every_interest_group','any_interest_group'}

def overlay(folder, mod):
    result = {}
    if not mod or not any(folder == p or folder.startswith(p + '/') for p in REPLACE):
        result.update({p.relative_to(STEAM).as_posix(): p for p in (STEAM / folder).rglob('*.txt')})
    if mod:
        result.update({p.relative_to(ROOT).as_posix(): p for p in (ROOT / folder).rglob('*.txt')})
    return result

def inventory(mod):
    cache, errors = {}, []
    def read(folder):
        rows = []
        for relative, path in sorted(overlay(folder, mod).items()):
            try:
                text = path.read_text(encoding='utf-8-sig')
                nodes = parse(text)
            except Exception as exc:
                errors.append(dict(file=relative, error=str(exc)))
                continue
            cache[relative] = (path, text, nodes)
            rows.extend((relative, node) for node in nodes if isinstance(node.value, list))
        return rows
    def location(relative, node):
        return dict(file=relative, line=cache[relative][1].count('\n',0,node.start)+1, key=node.key)
    def numeric(value):
        try:return float(str(value).strip('"'))
        except (ValueError,TypeError):return None
    countries = read('common/country_definitions')
    definitions = {n.key.replace('REPLACE_OR_CREATE:',''): n for _,n in countries}
    states = read('common/history/states')
    owners, created_states = set(), 0
    for _,node in states:
        for child in walk([node]):
            if child.key == 'create_state':
                owner = str(child.one('country','')).strip('"')
                if owner.startswith('c:'):owners.add(owner[2:])
                created_states += 1
    pops = read('common/history/pops')
    pop_sizes = [numeric(n.one('size')) for _,node in pops for n in walk([node]) if n.key == 'create_pop']
    buildings = read('common/history/buildings')
    buildings_by_type, levels, uncertain = Counter(), 0, 0
    for _,node in buildings:
        for n in walk([node]):
            if n.key != 'create_building':continue
            buildings_by_type[str(n.one('building','unknown')).strip('"')] += 1
            direct = numeric(n.one('level'))
            ownership = [numeric(k.value) for k in walk(n.children('add_ownership')) if k.key == 'levels']
            if direct is not None:levels += direct
            elif ownership and all(x is not None for x in ownership):levels += sum(ownership)
            else:uncertain += 1
    histories = read('common/history/countries')
    diplomacy = read('common/history/diplomacy')
    pact_types = Counter(str(n.one('type','unknown')).strip('"') for _,root in diplomacy for n in walk([root]) if n.key == 'create_diplomatic_pact')
    effects, triggers = read('common/scripted_effects'), read('common/scripted_triggers')
    helpers = {n.key.replace('REPLACE_OR_CREATE:',''):(r,n) for r,n in effects+triggers}
    helper_refs = {key:Counter(n.key for n in walk([node]) if n.key in helpers and n is not node) for key,(_,node) in helpers.items()}
    helper_local = {key:Counter(n.key for n in walk([node])) for key,(_,node) in helpers.items()}
    def features(node):
        own = Counter(n.key for n in walk([node]))
        reachable, pending = set(), [k for k in own if k in helpers]
        while pending:
            key = pending.pop()
            if key in reachable:continue
            reachable.add(key)
            pending.extend(helper_refs[key])
        transitive = own.copy()
        for key in reachable:transitive.update(helper_local[key])
        return dict(ast_nodes=sum(own.values()), direct_world_loops={k:own[k] for k in WORLD if own[k]},
                    reachable_world_loop_sites={k:transitive[k] for k in WORLD if transitive[k]},
                    direct_scoped_loop_sites={k:own[k] for k in SCOPED if own[k]},
                    reachable_helpers=len(reachable),
                    helper_names=sorted(reachable),
                    world_loop_site_count=sum(transitive[k] for k in WORLD))
    actions = read('common/on_actions')
    action_rows = [dict(**location(r,n), **features(n),
                        children=[str(c.value) for b in n.children('on_actions') for c in b.children() if not c.key],
                        trigger_present=bool(n.children('trigger')), effect_present=bool(n.children('effect')))
                   for r,n in actions]
    by_action=defaultdict(list)
    for row in action_rows:by_action[row['key']].append(row)
    contexts=defaultdict(set)
    for name in by_action:
        if not re.match(r'on_(daily|weekly|monthly|half_yearly|yearly)_pulse',name):continue
        pending=[name];seen=set()
        while pending:
            key=pending.pop()
            if key in seen:continue
            seen.add(key);contexts[key].add(name)
            for row in by_action[key]:pending.extend(row['children'])
    for row in action_rows:row['called_from_periodic_hooks']=sorted(contexts[row['key']])
    journals = read('common/journal_entries')
    journal_rows = []
    for relative,n in journals:
        f=features(n)
        journal_rows.append(dict(**location(relative,n), **f,
            pulses={k:len(n.children(k)) for k in ('on_weekly_pulse','on_monthly_pulse','on_yearly_pulse') if n.children(k)},
            cadence_overrides={c.key:c.value for c in n.children() if 'update' in c.key or 'interval' in c.key},
            top_fields=[c.key for c in n.children()],
            activation_excerpt=cache[relative][1][n.start:min(n.start+1100,n.end)]))
        fields=[]
        for child in n.children():
            if child.key in ('possible','is_shown_when_inactive','is_shown_when_active','should_be_involved','should_show_when_not_involved','on_weekly_pulse','on_monthly_pulse','on_yearly_pulse'):
                fields.append(dict(field=child.key,**location(relative,child),**features(child)))
            if child.key=='outcome':
                for condition in child.children('trigger'):fields.append(dict(field='outcome.trigger',**location(relative,condition),**features(condition)))
        journal_rows[-1]['recurrent_fields']=fields
        journal_rows[-1]['recurrent_world_loop_sites']=sum(v['world_loop_site_count'] for v in fields)
    flags = read('common/flag_definitions')
    flag_rows = [dict(**location(r,n), **features(n), flag_definitions=sum(k.key=='flag_definition' for k in walk([n]))) for r,n in flags]
    ai = read('common/ai_strategies')
    ai_rows = [dict(**location(r,n), **features(n)) for r,n in ai]
    events=read('events')
    defines=read('common/defines')
    selected_defines = {}
    for relative,node in defines:
        for n in node.children():
            if re.search(r'START_DATE|JOURNAL_ENTRY_UPDATE|FLAG.*(UPDATE|INTERVAL)|NUM_TIMES_TO_UPDATE_TRADE_DURING_INITIALIZATION|HIRING_RANGE_WEEKLY|DEFAULT_MAX_HIRING_RATE|QUALIFICATIONS_UPDATE',n.key):
                selected_defines[node.key+'.'+n.key] = dict(value=n.value, **location(relative,n))
    initial_fields = Counter(n.key for _,node in histories for n in walk([node]) if n.key in ('add_journal_entry','create_country','create_market','set_market_owner','set_country_type','create_trade_route'))
    loops_total = Counter(n.key for _,_,nodes in cache.values() for n in walk(nodes) if n.key in WORLD|SCOPED)
    file_deltas = []
    for relative,(path,text,nodes) in cache.items():
        native = STEAM / relative
        origin = 'native' if path == native else ('modified' if native.exists() else 'added')
        if origin == 'modified' and SHA(path)==SHA(native):origin='identical_copy'
        file_deltas.append(dict(file=relative, origin=origin, bytes=path.stat().st_size, sha256=SHA(path)))
    score=lambda r:(r['world_loop_site_count'],r['ast_nodes'])
    return dict(
        static_not_runtime=True, note='Loop sites are syntax sites, not measured invocations or milliseconds. Reachable helpers are counted once; conditions and engine short-circuiting are not evaluated.',
        active_country_proxy=dict(owner_tags=len(owners), tags=sorted(owners), state_fragments=created_states,
             caveat='Owners of statically declared create_state blocks, not a certified runtime country/market count; conditional history and dynamic creations can differ.',
             types=Counter(str(definitions[k].one('country_type','unknown')) if k in definitions else 'undefined' for k in owners)),
        country_definitions=len(definitions), country_history_files=len(overlay('common/history/countries',mod)),
        pops=dict(groups=len(pop_sizes), literal_population=sum(s for s in pop_sizes if s is not None), nonliteral_sizes=sum(s is None for s in pop_sizes)),
        buildings=dict(create_blocks=sum(buildings_by_type.values()), literal_constructed_levels=levels, ambiguous_blocks=uncertain, types=buildings_by_type),
        markets=dict(runtime_count=None, reason='Country count is not market count; subject and market-sharing relationships require engine initialization.'),
        diplomacy=dict(pact_blocks=sum(pact_types.values()), pact_types=pact_types),
        initial_effect_sites=initial_fields, counts=dict(on_action_definitions=len(action_rows),on_action_unique_names=len(by_action), journals=len(journal_rows),journal_unique_names=len({r['key'].replace('REPLACE_OR_CREATE:','') for r in journal_rows}), events=len(events),event_unique_names=len({n.key.replace('REPLACE_OR_CREATE:','') for _,n in events}), scripted_effects=len(effects), scripted_triggers=len(triggers), ai_strategies=len(ai_rows), flag_lists=len(flag_rows), flag_definitions=sum(r['flag_definitions'] for r in flag_rows)),
        declared_pulses=Counter(k for r in journal_rows for k,v in r['pulses'].items() for _ in range(v)),
        loop_sites=loops_total, selected_defines=selected_defines,
        on_actions=action_rows,
        journal_top_world_loops=sorted(journal_rows,key=score,reverse=True)[:35],
        journal_recurrent_risks=sorted(journal_rows,key=lambda r:(r['recurrent_world_loop_sites'],r['ast_nodes']),reverse=True)[:35],
        journal_duplicate_names={k:v for k,v in Counter(r['key'].replace('REPLACE_OR_CREATE:','') for r in journal_rows).items() if v>1},
        flag_top_world_loops=sorted(flag_rows,key=score,reverse=True)[:20],
        ai_top_world_loops=sorted(ai_rows,key=score,reverse=True)[:15],
        largest_modified_script_files=sorted([r for r in file_deltas if r['origin'] in ('added','modified')],key=lambda r:r['bytes'],reverse=True)[:30],
        files=file_deltas, parse_errors=errors)

def main():
    destination=REPORT/(sys.argv[1] if len(sys.argv)>1 else 'STATIC_INVENTORY.json')
    if destination.exists():raise SystemExit('Retain the earlier inventory.')
    REPORT.mkdir(parents=True,exist_ok=True)
    result=dict(utc=datetime.now(timezone.utc).isoformat(),
                local_head=subprocess.check_output(['git','--no-optional-locks','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                vanilla=inventory(False), mod=inventory(True))
    with destination.open('x',encoding='utf-8') as stream:json.dump(result,stream,indent=2,ensure_ascii=False)
    for name in ('vanilla','mod'):
        v=result[name]
        print(json.dumps(dict(environment=name, countries=v['active_country_proxy']['owner_tags'],
            country_types=v['active_country_proxy']['types'],pop_groups=v['pops'],buildings={k:x for k,x in v['buildings'].items() if k!='types'},
            counts=v['counts'],pulses=v['declared_pulses'],parse_errors=v['parse_errors'],
            journal_risks=[{k:r[k] for k in ('key','file','line','world_loop_site_count')} for r in v['journal_top_world_loops'][:7]]),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
