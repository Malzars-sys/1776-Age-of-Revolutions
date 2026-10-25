"""Read-only audit of the two initial technology gates; writes this output folder only."""
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime, timezone
import hashlib
import json
import re
import sys
import unicodedata

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
GAME = Path('C:/Games/Victoria 3/game')
sys.path.insert(0, str(ROOT/'tools'))
from validate_diplomacy_ottoman_1776 import parse, walk, scalar
from localization_duplicate_audit import entries
import tech_start_1776_implementation as prior

TECHS = ['scientific_fortification_siegecraft', 'permanent_engineer_services']
SOURCES = {}
RAW = {}


def read(path):
    data = path.read_bytes()
    SOURCES[str(path)] = hashlib.sha256(data).hexdigest()
    RAW[path] = data.decode('utf-8-sig')
    return RAW[path]


def effective(folder):
    files = {p.name.lower():p for p in (GAME/folder).glob('*.txt')}
    files.update({p.name.lower():p for p in (ROOT/folder).glob('*.txt')})
    return [files[k] for k in sorted(files)]


def ref(path, node):
    return dict(file=str(path), line=RAW[path][:node.start].count('\n')+1)


def display_ref(evidence):
    first = evidence[0]
    text = f"{Path(first['file']).name}, l. {first['line']}"
    if len(evidence)>1:
        target=evidence[-1]
        text += f" ; {Path(target['file']).name}, l. {target['line']}"
    return text


def main():
    start=parse(read(ROOT/'common/defines/00_defines.txt'))[0].one('START_DATE')
    assert scalar(start)=='1776.1.1'
    for rel,kind,expected in [
        ('common/buildings/1776_land_fortifications.txt','building_aor1776_land_fortification',TECHS[0]),
        ('common/combat_unit_types/1776_engineer_corps.txt','combat_unit_type_aor1776_engineer_corps',TECHS[1])]:
        node=next(n for n in parse(read(ROOT/rel)) if n.key==kind)
        assert [n.value for n in node.children('unlocking_technologies')[0].children()]==[expected]
    captech=next(n for n in parse(read(ROOT/'common/technology/technologies/20_tech3a_military.txt')) if n.key==TECHS[0])
    assert captech.children('modifier')[0].one('state_building_aor1776_land_fortification_max_level_add')=='5'

    # Active means owning actual provinces in effective state history. This
    # excludes formable/releasable countries with prewritten country histories.
    states=defaultdict(set)
    for path in effective('common/history/states'):
        for node in walk(parse(read(path))):
            if not node.key.startswith('s:STATE_'): continue
            for creation in node.children('create_state'):
                tag=scalar(creation.one('country')).removeprefix('c:')
                provinces=creation.children('owned_provinces')
                assert provinces and provinces[0].children(), (tag,node.key,'empty state creation')
                states[tag].add(node.key[2:])
    active=set(states)

    # Only these tier effects contain indirect grants of the requested gates.
    tier_path=ROOT/'common/scripted_effects/00_starting_inventions.txt'
    tier_defs={n.key:n for n in parse(read(tier_path))}
    techs=defaultdict(set)
    evidence=defaultdict(lambda:defaultdict(list))
    histories=defaultdict(list)
    conditional=[]
    mutations=[]

    def grants(nodes,tag,path,chain=(),nested=()):
        for node in nodes:
            if node.key=='add_technology_researched':
                assert not nested, (tag,path,nested,'conditional technology grant')
                tech=scalar(node.value)
                techs[tag].add(tech)
                if tech in TECHS: evidence[tag][tech].append(list(chain)+[ref(path,node)])
            elif node.key in tier_defs:
                assert node.value=='yes' and not nested, (path,node.key,nested)
                grants(tier_defs[node.key].children(),tag,tier_path,chain+(ref(path,node),))
            elif node.key in {'add_era_researched','remove_technology_researched','remove_era_researched','copy_technology_from'}:
                mutations.append((tag,str(path),node.key))
            elif isinstance(node.value,list):
                # Other nested effects never grant start technologies here.
                grants(node.children(),tag,path,chain,nested+(node.key,))

    for path in effective('common/history/countries'):
        for wrapper in parse(read(path)):
            assert wrapper.key=='COUNTRIES', (path,wrapper.key)
            for country in wrapper.children():
                if country.key.startswith('c:'):
                    tag=country.key[2:]
                    if tag in active:
                        histories[tag].append(str(path))
                        grants(country.children(),tag,path)
    assert not mutations, mutations
    without_history=sorted(tag for tag in active if not histories[tag])

    # Independent existing resolver: effective filename overlays + explicit
    # country grants + seven starting tiers. Do not infer missing ancestors.
    tiers=prior.parse_tiers()
    # Older resolver assumes country scopes start a physical line. Recent
    # map additions legally put COUNTRIES and c:TAG on the same line.
    prior.TAG_RE=re.compile(r'\bc:([A-Z0-9_]{3,})\s*\?=\s*\{')
    overlay,names=prior.country_overlay()
    for tag in active:
        independently=set()
        for filename in names[tag]:
            independently.update(prior.parse_country_tech(overlay[filename][0],tiers,tag)[0])
        assert {t for t in TECHS if t in independently}=={t for t in TECHS if t in techs[tag]},tag

    # Check for other scripts that could grant/remove either gate indirectly.
    # The only scripted grant sites must be the audited tier file. History
    # sites have already been isolated to their country scope above.
    outside_grants=[]
    for folder in ['common/scripted_effects','common/on_actions','events']:
        for path in effective(folder):
            raw=read(path)
            if not any(t in raw for t in TECHS): continue
            for node in walk(parse(raw)):
                if node.key in {'add_technology_researched','remove_technology_researched'} and scalar(node.value) in TECHS:
                    if path!=tier_path: outside_grants.append(ref(path,node))
    assert not outside_grants,outside_grants

    # Names are identifiers in French, not a simulation of dynamic titles.
    names_catalog={}
    conflicts={}
    for catalog in [entries('french',root=GAME/'localization'),entries('french',replacement=False),entries('french',replacement=True)]:
        for key,values in catalog.items():
            if key not in active and key not in TECHS: continue
            unique={v[2] for v in values}
            if len(unique)>1: conflicts[key]=[dict(file=str(p),line=l,value=v) for p,l,v in values]
            path,line,value=values[-1]
            names_catalog[key]=value
            if str(path) not in SOURCES: read(path)
    def resolve(key,seen=()):
        assert key not in seen
        value=names_catalog.get(key,key)
        return re.sub(r'\$([A-Za-z0-9_.-]+)\$',lambda m:resolve(m[1],seen+(key,)),value)
    missing=[tag for tag in active if tag not in names_catalog]
    assert not missing,missing
    # The American tag's generic French label is "Amérique". The fixed start
    # label is clearer for this audit; the tag is retained alongside it.
    country_names={tag:resolve(tag) for tag in active}
    country_names['USA']='Treize Colonies'
    rows=[]
    for tag in active:
        row=dict(tag=tag,pays=country_names[tag],forts=TECHS[0] in techs[tag],genie=TECHS[1] in techs[tag],
                 states=sorted(states[tag]),histories=histories[tag],proofs={tech:evidence[tag].get(tech,[]) for tech in TECHS})
        row['sources_forts']=display_ref(evidence[tag][TECHS[0]][0]) if row['forts'] else 'Aucune attribution dans les fichiers de départ'
        row['sources_genie']=display_ref(evidence[tag][TECHS[1]][0]) if row['genie'] else 'Aucune attribution dans les fichiers de départ'
        rows.append(row)
    key=lambda r:unicodedata.normalize('NFKD',r['pays']).encode('ascii','ignore').decode().casefold()
    rows.sort(key=key)
    counts=dict(pays=len(rows),forts=sum(r['forts'] for r in rows),genie=sum(r['genie'] for r in rows),
                deux=sum(r['forts'] and r['genie'] for r in rows),
                forts_seuls=sum(r['forts'] and not r['genie'] for r in rows),
                genie_seul=sum(r['genie'] and not r['forts'] for r in rows),
                aucune=sum(not r['forts'] and not r['genie'] for r in rows))
    result=dict(start_date='1776-01-01',audit_date='2026-10-19',utc=datetime.now(timezone.utc).isoformat(),
                technology_ids=TECHS,technology_names=[resolve(t) for t in TECHS],counts=counts,rows=rows,
                name_conflicts=conflicts,independent_resolver='MATCH_ALL_ACTIVE_COUNTRIES',
                active_definition='At least one province in effective initial state history; absent countries excluded.',
                countries_without_history=without_history,source_sha256=SOURCES,runtime='NOT_RUN')
    (OUT/'audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(counts=counts,name_conflicts=conflicts,without_history=without_history,examples={r['tag']:[r['pays'],r['forts'],r['genie']] for r in rows if r['tag'] in {'USA','FRA','GBR','PRU','AUS','SPA','POR','TUR','EGY','CHI','JAP','BIC','MARATH','SAX','BAV'}},genie_only=[r['tag'] for r in rows if r['genie'] and not r['forts']]),ensure_ascii=False,indent=2))


if __name__=='__main__': main()
