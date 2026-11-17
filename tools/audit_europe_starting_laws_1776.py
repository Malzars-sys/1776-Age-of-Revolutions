"""Read-only law-request audit; reports script requests, never observed active laws.

Resolve effective law metadata including INJECT_OR_CREATE declarations; expand
country-scoped scripted effects in order. Conditional requests remain separate.
Run with --output PATH. No automatic grants, law changes or game launch.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import audit_starting_tech_1776 as core
import validate_starting_technology_1776 as technology

NAMED = ['GBR','FRA','SPA','POR','BEO','PRU','AUS','PLC','NET','TUR',
         'PAP','SWE','DENNOR','SWI','VEN','TUS','PAR','LUC','GEN','MOD','MCA','MON']
FIELDS = ['group','parent','unlocking_technologies','unlocking_laws',
          'requires_law_or','disallowing_laws']


def law_metadata():
    result = {}
    for path in core.effective('common/laws'):
        for node in core.cw.parse(path.read_text(encoding='utf-8-sig')):
            key = node.key.split(':',1)[-1]
            if not key.startswith('law_'):
                continue
            injection = node.key.startswith('INJECT')
            if key not in result or not injection:
                result[key] = {}
            record = result[key]
            for field in FIELDS:
                children = node.children(field)
                if children:
                    record[field] = (core.values(node,field) if field not in {'group','parent'}
                                     else core.val(node,field))
            record['source'] = core.ref(path)
    return result


def collect():
    snapshot = technology.collect_snapshot()
    laws = law_metadata()
    effects, effect_sources, _ = core.objects('common/scripted_effects')
    german = sorted(tag for tag,node in snapshot['definitions'].items()
                    if tag in snapshot['starts'] and
                    set(core.values(node,'cultures')) & {'north_german','south_german'})
    tags = sorted(set(NAMED) | set(german))
    requests = collections.defaultdict(list)
    ambiguous = collections.defaultdict(list)

    def expand(nodes, tag, source, conditional=False, trail=()):
        for node in nodes:
            if node.key == 'activate_law' and isinstance(node.value,str):
                law = core.cw.scalar(node.value).removeprefix('law_type:')
                row = dict(law=law, source=source, offset=node.start,
                           conditional=conditional, effect_chain=list(trail))
                requests[tag].append(row)
            elif node.key in effects and not isinstance(node.value,list):
                if node.key in trail:
                    ambiguous[tag].append('RECURSIVE_EFFECT:'+node.key)
                else:
                    expand(effects[node.key].children(), tag,
                           effect_sources[node.key], conditional, trail+(node.key,))
            elif node.key in {'if','else_if','else','random','random_list'}:
                expand(node.children(),tag,source,True,trail)

    for path in core.effective('common/history/countries'):
        raw = path.read_text(encoding='utf-8-sig')
        for root in core.cw.parse(raw):
            for country in root.children():
                if country.key.startswith('c:'):
                    tag = country.key[2:]
                    if tag in tags:
                        expand(country.children(),tag,core.ref(path))

    def group(law,seen=()):
        if law in seen or law not in laws:
            return None
        return laws[law].get('group') or group(laws[law].get('parent'),seen+(law,))

    rows = []
    for tag in tags:
        known = set(snapshot['starts'].get(tag,{}).get('technologies',[]))
        last = {}
        for request in requests[tag]:
            if not request['conditional']:
                g = group(request['law'])
                if g:
                    last[g] = request['law']
        rows.append(dict(tag=tag,active=tag in snapshot['starts'],german_tag=tag in german,
                         history=snapshot['starts'].get(tag,{}).get('history',[]),
                         technologies=sorted(known),
                         max_era=max([int(core.val(snapshot['techs'][x],'era','era_0').split('_')[-1])
                                      for x in known if x in snapshot['techs']],default=0),
                         ordered_requests=requests[tag],last_unconditional_request_by_group=last,
                         law_gate_findings=[dict(law=l,group=g,
                             missing=sorted(set(laws[l].get('unlocking_technologies',[]))-known))
                             for g,l in last.items() if set(laws[l].get('unlocking_technologies',[]))-known],
                         ambiguities=ambiguous[tag]))
    hashes = {}
    for folder in ('common','events','gui','map_data','localization'):
        for p in (core.ROOT/folder).rglob('*'):
            if p.is_file():
                hashes[p.relative_to(core.ROOT).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    return dict(model='Ordered unconditional country history/scripted-effect requests. '
                      'Conditional branches and engine defaults are not certified active laws; '
                      'enactment gates do not by themselves prove initial activation failure.',
                countries=rows,laws=laws,german_tags=german,runtime_hashes=hashes,
                engine_test=False,technology_grants_added=0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    result = collect()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(countries=len(result['countries']),german_tags=len(result['german_tags']),
                          output=str(args.output),engine_test=False)))


if __name__ == '__main__':
    main()
