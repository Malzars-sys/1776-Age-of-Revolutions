"""Read-only effective economic-reference inventory for issue 23.

Models same-path masks, descriptor replace_path and explicit object replacement.
Reports references and ambiguities; it does not simulate prices or market access.
"""
import argparse, collections, hashlib, json, re, sys
from pathlib import Path
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
GAME = Path('C:/Games/Victoria 3/game')
sys.path.insert(0, str(ROOT / 'tools'))
from validate_diplomacy_ottoman_1776 import parse, walk

CATEGORIES = {
    'goods': 'common/goods', 'buildings': 'common/buildings',
    'building_groups': 'common/building_groups',
    'groups': 'common/production_method_groups', 'methods': 'common/production_methods',
    'technologies': 'common/technology/technologies', 'laws': 'common/laws',
}

def text(path): return path.read_bytes().decode('utf-8-sig')
def bare(node): return [n.value.strip('"') for n in node.children() if not n.key and isinstance(n.value, str)]
def plain(value): return value.strip('"') if isinstance(value, str) else value

def audit(base_only=False, mod=ROOT, game=GAME):
    replacements = [] if base_only else re.findall(r'replace_path\s*=\s*"([^"]+)"', text(mod/'descriptor.mod'))
    pools, sources, parse_errors, masks = {}, {}, [], []
    def paths(folder):
        local = {} if base_only else {p.relative_to(mod).as_posix().casefold(): p for p in (mod/folder).rglob('*.txt')}
        replaced = any(folder == p or folder.startswith(p+'/') for p in replacements)
        native = [] if replaced else [p for p in (game/folder).rglob('*.txt') if p.relative_to(game).as_posix().casefold() not in local]
        if not base_only:
            masks.extend(p.relative_to(mod).as_posix() for p in local.values() if (game/p.relative_to(mod)).exists())
        return sorted(native+list(local.values()), key=lambda p: str(p).casefold())
    def load(folder):
        normal, explicit = collections.defaultdict(list), collections.defaultdict(list)
        for p in paths(folder):
            raw = text(p); origin = 'native' if p.is_relative_to(game) else 'mod'
            rel = p.relative_to(game if origin=='native' else mod).as_posix()
            sources[origin+'/'+rel] = hashlib.sha256(p.read_bytes()).hexdigest()
            try: nodes = parse(raw)
            except ValueError as exc:
                parse_errors.append({'path': origin+'/'+rel, 'error': str(exc)}); continue
            for n in nodes:
                if not isinstance(n.value, list): continue
                directive, sep, name = n.key.partition(':')
                key = name if sep and directive in ('REPLACE', 'REPLACE_OR_CREATE') else n.key
                (explicit if key != n.key else normal)[key].append((n, origin+'/'+rel, raw))
        normal.update(explicit)
        return normal
    for cat, folder in CATEGORIES.items(): pools[cat] = load(folder)
    edges, unresolved, ambiguous = [], [], []
    unsupported_initial, incompatible_prerequisites = [], []
    def ref(cat, key, owner, path, role):
        if not isinstance(key, str): return
        key = key.strip('"'); row = {'category':cat,'target':key,'owner':owner,'path':path,'role':role}
        edges.append(row)
        count = len(pools[cat].get(key, []))
        if count==0: unresolved.append(row)
        elif count>1: ambiguous.append(row)
    for key, defs in pools['buildings'].items():
        for n, path, raw in defs:
            ref('building_groups', n.one('building_group'), key, path, 'building group')
            for block in n.children('production_method_groups'):
                for target in bare(block): ref('groups',target,key,path,'building PM group')
            for block in n.children('unlocking_technologies'):
                for target in bare(block): ref('technologies',target,key,path,'building technology')
    for key, defs in pools['groups'].items():
        for n, path, raw in defs:
            for block in n.children('production_methods'):
                for target in bare(block): ref('methods',target,key,path,'group PM')
    reachable_groups = {e['target'] for e in edges if e['role']=='building PM group'}
    reachable_methods = {e['target'] for e in edges if e['role']=='group PM' and e['owner'] in reachable_groups}
    building_methods = {}
    for building, definitions in pools['buildings'].items():
        allowed = set()
        for n, _, _ in definitions:
            for block in n.children('production_method_groups'):
                for group in bare(block):
                    for group_node, _, _ in pools['groups'].get(group, []):
                        for pm_block in group_node.children('production_methods'):
                            allowed.update(bare(pm_block))
        building_methods[building] = allowed
    goods_flow = collections.defaultdict(lambda: {'inputs': [], 'outputs': []})
    for key, defs in pools['methods'].items():
        for n, path, raw in defs:
            for field in walk(n.children()):
                match = re.fullmatch(r'goods_(input|output)_([a-z0-9_]+)_(add|mult)', field.key)
                if match:
                    direction, good, mode = match.groups()
                    ref('goods',good,key,path,'PM '+direction)
                    goods_flow[good]['inputs' if direction=='input' else 'outputs'].append({'pm':key,'value':field.value,'mode':mode,'reachable':key in reachable_methods,'path':path})
                if field.key=='required_input_goods' and isinstance(field.value,str):
                    ref('goods',field.value,key,path,'required input good')
            for blockname, cat in [('unlocking_technologies','technologies'),('unlocking_global_technologies','technologies'),('unlocking_laws','laws'),('disallowing_laws','laws'),('unlocking_production_methods','methods'),('disallowing_production_methods','methods')]:
                for block in n.children(blockname):
                    for target in bare(block): ref(cat,target,key,path,'PM '+blockname)
            for block in n.children('unlocking_production_methods'):
                for target in bare(block):
                    for building, allowed in building_methods.items():
                        if key in allowed and target not in allowed:
                            incompatible_prerequisites.append({'pm':key,'required':target,'building':building,'path':path})
    for p in paths('map_data/state_regions'):
        raw = text(p); origin = 'native' if p.is_relative_to(game) else 'mod'; path=origin+'/'+p.relative_to(game if origin=='native' else mod).as_posix()
        sources[path] = hashlib.sha256(p.read_bytes()).hexdigest()
        try: states = parse(raw)
        except ValueError as exc: parse_errors.append({'path':path,'error':str(exc)}); continue
        for state in states:
            for block in state.children('capped_resources'):
                for field in block.children(): ref('buildings',field.key,state.key,path,'resource potential')
            for block in state.children('arable_resources'):
                for target in bare(block): ref('buildings',target,state.key,path,'arable resource')
    for p in paths('common/history/buildings'):
        raw=text(p);origin='native' if p.is_relative_to(game) else 'mod';path=origin+'/'+p.relative_to(game if origin=='native' else mod).as_posix()
        sources[path]=hashlib.sha256(p.read_bytes()).hexdigest()
        try: nodes=parse(raw)
        except ValueError as exc: parse_errors.append({'path':path,'error':str(exc)});continue
        for n in walk(nodes):
            if n.key=='create_building':
                owner=plain(n.one('building','unknown'))
                ref('buildings',owner,'history',path,'initial building')
                for block in n.children('activate_production_methods'):
                    for target in bare(block):
                        ref('methods',target,owner,path,'initial PM')
                        if owner in building_methods and target not in building_methods[owner]:
                            unsupported_initial.append({'building':owner,'pm':target,'path':path})
    for row in unresolved+ambiguous:
        row['reachable_pm'] = row['owner'] in reachable_methods if row['role'].startswith('PM ') else None
    duplicates={cat:{k:[d[1] for d in defs] for k,defs in pool.items() if len(defs)>1} for cat,pool in pools.items()}
    return {'status':'FINDINGS_STATIC_ONLY' if unresolved or ambiguous or parse_errors or unsupported_initial or incompatible_prerequisites else 'PASS_STATIC_ONLY',
            'baseline':'native' if base_only else 'mod','replace_paths':replacements,
            'counts':{cat:len(pool) for cat,pool in pools.items()},'reference_count':len(edges),
            'reachable_groups':len(reachable_groups),'reachable_methods':len(reachable_methods),
            'parse_errors':parse_errors,'unresolved':unresolved,'ambiguous_references':ambiguous,
            'duplicate_definitions':duplicates,'same_path_masks':sorted(set(masks)),
            'unsupported_initial_methods':unsupported_initial,'incompatible_pm_prerequisites':incompatible_prerequisites,
            'goods_flow':dict(goods_flow),'source_hashes':sources,'engine_tested':False}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--native',action='store_true');p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();r=audit(a.native)
    a.output.write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:r[k] for k in ['status','baseline','counts','reference_count','reachable_methods','parse_errors']},indent=2))
    print(json.dumps({'unresolved_count':len(r['unresolved']),'ambiguous_count':len(r['ambiguous_references']),'unresolved_examples':r['unresolved'][:12]},indent=2))
