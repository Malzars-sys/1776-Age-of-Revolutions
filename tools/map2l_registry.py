"""Versioned, explicitly reviewed territorial registry; keep MAP2K frozen."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def active_registry_path():
    newer=ROOT/'docs/reports/map/MAP2L/IMPERIAL_DE_JURE_REGISTRY.json'
    return newer if newer.exists() else ROOT/'docs/reports/map/MAP2K/IMPERIAL_DE_JURE_REGISTRY.json'

def additional_members():
    if active_registry_path().parent.name=='MAP2L':return ['LGE','STM','SAR']+[t for m in approved_territorial_migrations() for t in m['new_members']]
    return []

def additional_free_cities():
    """Only explicitly declared city estates, not every republican member."""
    result=[]
    for migration in approved_territorial_migrations():
        cities=migration.get('free_cities',[])
        assert set(cities)<=set(migration['new_members'])
        for tag in cities:
            if tag not in result:result.append(tag)
    return result

def member_region_overrides():
    # Membership is country-wide, whereas territorial rights are explicit.
    # Do not register Sardinia, Savoy or every other possession of this member.
    return {'SAR': {'STATE_PIEDMONT'}}

def territorial_holder_overrides():
    """A registered ducal possession is not country-wide bloc membership."""
    result={}
    # Only this explicitly approved manifest may introduce the Swedish title.
    # Do not repeatedly parse every large earlier geometry migration per RGB.
    path=ROOT/'docs/reports/map/MAP2L/PRUSSIAN_BORDERS/REGISTRY_MIGRATION.json'
    for m in ([json.loads(path.read_text(encoding='utf-8'))] if path.exists() else []):
        for tag,regions in m.get('external_territorial_holders',{}).items():
            assert tag=='SWE' and regions==['STATE_POMERANIA']
            result[tag]=set(regions)
    # Separate, additive MAP2N approval: four frozen Swedish Mecklenburg
    # provinces. This never confers country-wide imperial membership.
    completion=ROOT/'docs/reports/map/MAP2N/COMPLETION/REGISTRY_MIGRATION.json'
    if completion.exists():
        m=json.loads(completion.read_text(encoding='utf-8'))
        assert m.get('external_territorial_holders')=={'SWE':['STATE_MECKLENBURG']}
        assert m.get('external_holder_RGBs')==['xEDB102','xEDB103','xEDB104','xEDB105']
        assert not m['new_members']
        assert {(r['rgb'],r['state'],r['owner']) for r in m['new_provinces']}=={(rgb,'STATE_MECKLENBURG','SWE') for rgb in m['external_holder_RGBs']}
        result.setdefault('SWE',set()).add('STATE_MECKLENBURG')
    return result

def rightful_holder_condition(row):
    """Use the reviewed province-specific Swedish title, never a member flag."""
    tag=row['beneficiary']
    if row['state'] in territorial_holder_overrides().get(tag,set()):
        return 'exists = c:'+tag
    return 'c:'+tag+' ?= { aor1776_hre_member = yes }'

def approved_territorial_extensions():
    manifest=ROOT/'docs/reports/map/MAP2L/PIEDMONT/EXTENSION.json'
    return json.loads(manifest.read_text(encoding='utf-8'))['provinces'] if manifest.exists() else []

def approved_territorial_migrations():
    return [json.loads((p/'REGISTRY_MIGRATION.json').read_text(encoding='utf-8')) for p in approved_lot_dirs()]


def approved_lot_dirs():
    # Ordered explicit manifests only; no directory discovery or broad allowlist.
    earlier=[ROOT/'docs/reports/map/MAP2L'/name for name in ['FRANCONIA','RHINE_CENTRAL','MAINZ_PALATINATE','MAINZ_ESTATES','MAINZ_COMPLETION','MILAN_CREMONESE','FRANCONIA_CONTINUATION','RHINE_WESTPHALIA','MINDEN_RAVENSBERG','DUCHY_WESTPHALIA','RHINE_WESTPHALIA_COMPLETION','SWABIA','SWABIA_CONTINUATION','SWABIA_FINISH','SWABIA_COMPLETION','PRUSSIAN_BORDERS']
             if (ROOT/'docs/reports/map/MAP2L'/name/'REGISTRY_MIGRATION.json').exists()]
    # Poel is grouped into Pomerania by explicit player decision. This adds
    # reviewed province rights, not Swedish membership or a new country.
    poel=ROOT/'docs/reports/map/MAP2N'
    completion=poel/'COMPLETION'
    east_frisia=ROOT/'docs/reports/map/MAP2O'
    # Existing coastal province title only; no new rights or Prussian members.
    if (east_frisia/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((east_frisia/'REGISTRY_MIGRATION.json').read_text(encoding='utf-8'))
        assert m['replaced_regions']==['STATE_HANNOVER'] and not m['new_members'] and not m['new_provinces']
        assert not m['extent_added_cells'] and not m['extent_removed_cells']
        assert not m['region_reference_changes']
        old={r['rgb']:r for r in m['previous']};new={r['rgb']:r for r in m['updated']}
        assert set(old)==set(new) and {k for k in old if old[k]!=new[k]}=={'xF9DCA2'}
        assert old['xF9DCA2']['beneficiary']=='HAN' and new['xF9DCA2']['beneficiary']=='PRU'
        assert old['xF9DCA2']['state']==new['xF9DCA2']['state']=='STATE_HANNOVER'
    eutin=ROOT/'docs/reports/map/MAP2Q'
    if (eutin/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((eutin/'REGISTRY_MIGRATION.json').read_text(encoding='utf-8'))
        assert m['replaced_regions']==['STATE_SCHLESWIG_HOLSTEIN']
        assert m['new_members']==['HLB'] and not m['free_cities']
        assert not m.get('extent_added_cells',[]) and not m.get('extent_removed_cells',[])
        assert not m['region_reference_changes']
    kaltenhof=eutin/'R3'
    if (kaltenhof/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((kaltenhof/'REGISTRY_MIGRATION.json').read_text(encoding='utf-8'))
        assert m['replaced_regions']==['STATE_SCHLESWIG_HOLSTEIN']
        assert not m['new_members'] and not m['free_cities']
        assert not m['extent_added_cells'] and not m['extent_removed_cells'] and not m['region_reference_changes']
        assert m['new_provinces']==[{'rgb':'xEDB204','parent_rgb':'x60809F'},{'rgb':'xEDB205','parent_rgb':'x60809F'}]
        old={r['rgb']:r for r in m['previous']};new={r['rgb']:r for r in m['updated']}
        assert all(new.get(k)==v for k,v in old.items())
        assert set(new)-set(old)=={'xEDB204','xEDB205'}
        assert all(new[c]['beneficiary']=='HLB' and new[c]['state']=='STATE_SCHLESWIG_HOLSTEIN' for c in set(new)-set(old))
    anhalt=ROOT/'docs/reports/map/MAP2R'
    if (anhalt/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((anhalt/'REGISTRY_MIGRATION.json').read_text(encoding='utf-8'))
        assert m['replaced_regions']==['STATE_ANHALT']
        assert m['new_members']==['ABG','AKT','AZR'] and not m['free_cities']
        assert not m['extent_added_cells'] and not m['extent_removed_cells']
        geo=json.loads((anhalt/'GEOMETRY.json').read_text(encoding='utf-8'))
        assert geo['parents']==['x8A448C','xED8F7B']
        assert all(r['state']=='STATE_ANHALT' and r['previous_owner']=='ANH' and r['owner'] in {'ANH','ABG','AKT','AZR'} for r in geo['assignments'])
        assert sum(r['pixels'] for r in geo['assignments'])==279
        assert m['new_provinces']==geo['new_provinces']
        assert all(r['parent_rgb'] in geo['parents'] for r in m['new_provinces'])
    saxony=ROOT/'docs/reports/map/MAP2T'
    if (saxony/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((saxony/'REGISTRY_MIGRATION.json').read_text(encoding='utf8'))
        assert m['replaced_regions']==['STATE_SAXONY']
        assert m['new_members']==['GOT','HIL','SSO','RGZ','RGE','RSL'] and not m['free_cities']
        assert not m['extent_added_cells'] and not m['extent_removed_cells']
        geo=json.loads((saxony/'GEOMETRY.json').read_text(encoding='utf8'))
        assert set(geo['parents'])=={'x169073','x31E0C0','x43CE26','x5141A0','x51C021','x66FE0A','x795368','x917939','xAFDFBF','xC00A37','xD0C021'}
        assert all(r['state']=='STATE_SAXONY' and r['previous_owner'] in {'SAX','COB','WEI','MEI','SCW'} and r['owner'] in {'SAX','COB','WEI','MEI','SCW','GOT','HIL','SSO','RGZ','RGE','RSL'} for r in geo['assignments'])
        assert m['new_provinces']==geo['new_provinces']
        assert all(r['parent_rgb'] in geo['parents'] for r in m['new_provinces'])
    thuringia=ROOT/'docs/reports/map/MAP2U'
    if (thuringia/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((thuringia/'REGISTRY_MIGRATION.json').read_text(encoding='utf8'))
        assert m['replaced_regions']==['STATE_SAXONY','STATE_ANHALT']
        assert m['new_members']==['RLO','REB'] and not m['free_cities']
        assert not m['extent_added_cells'] and not m['extent_removed_cells']
        geo=json.loads((thuringia/'GEOMETRY.json').read_text(encoding='utf8'))
        assert set(geo['parents'])=={'x31E0C0','x3C9B93','xC00A37'}
        assert m['new_provinces']==geo['new_provinces']
        for row in geo['assignments']:
            if row['parent_rgb']=='x3C9B93':
                assert row['state']=='STATE_ANHALT' and row['previous_owner']=='PRU' and row['owner'] in {'PRU','SSO'}
            else:
                assert row['state']=='STATE_SAXONY' and row['previous_owner'] in {'SAX','WEI'} and row['owner'] in {'SAX','WEI','RLO','REB'}
            if row['owner']!=row['previous_owner']:
                assert all(4341<=x<=4370 and 818<=y<=849 and not (4342<=x<=4358 and 822<=y<=836) for x,y in row['cells'])
        assert all(r['parent_rgb'] in geo['parents'] for r in m['new_provinces'])
    fulda=ROOT/'docs/reports/map/MAP2W'
    if (fulda/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((fulda/'REGISTRY_MIGRATION.json').read_text(encoding='utf8'))
        assert m['replaced_regions']==['STATE_HESSE','STATE_SAXONY'] and m['new_members']==['FUL']
        assert not m['free_cities'] and not m['extent_added_cells'] and not m['extent_removed_cells']
        geo=json.loads((fulda/'GEOMETRY.json').read_text(encoding='utf8'))
        assert geo['parents']==['xD04121','xD0C021'] and m['new_provinces']==geo['new_provinces']
        assert sum(r['pixels'] for r in geo['assignments'])==345
        assert sum(r['pixels'] for r in geo['assignments'] if r['owner']=='FUL')==39
        assert all((r['state'],r['previous_owner']) in {('STATE_HESSE','HEK'),('STATE_SAXONY','MEI')} and r['owner'] in {r['previous_owner'],'FUL'} for r in geo['assignments'])
        assert all(4319<=x<=4325 and 840<=y<=847 for r in geo['assignments'] if r['owner']=='FUL' for x,y in r['cells'])
        assert geo['protected_saxon_new_RGB']=='xEDB40F'
        assert set(m['country_additions'])=={'FUL'}
    return earlier+([poel] if (poel/'REGISTRY_MIGRATION.json').exists() else [])+([completion] if (completion/'REGISTRY_MIGRATION.json').exists() else [])+([east_frisia] if (east_frisia/'REGISTRY_MIGRATION.json').exists() else [])+([eutin] if (eutin/'REGISTRY_MIGRATION.json').exists() else [])+([kaltenhof] if (kaltenhof/'REGISTRY_MIGRATION.json').exists() else [])+([anhalt] if (anhalt/'REGISTRY_MIGRATION.json').exists() else [])+([saxony] if (saxony/'REGISTRY_MIGRATION.json').exists() else [])+([thuringia] if (thuringia/'REGISTRY_MIGRATION.json').exists() else [])+([fulda] if (fulda/'REGISTRY_MIGRATION.json').exists() else [])

def reviewed_core_exception_owner(point,previous_owner,later_dirs):
    """Only the human-approved Kempten municipal cell, never a broad waiver."""
    result=previous_owner
    for directory in later_dirs:
        migration=json.loads((directory/'REGISTRY_MIGRATION.json').read_text())
        for exc in migration.get('core_exceptions',[]):
            assert directory.name=='SWABIA_COMPLETION'
            assert (exc['preceding_lot'],exc['rgb'],exc['previous_owner'],exc['new_owner'],exc['cells'])==('SWABIA','xEDAD0D','SKE','SKI',[[4324,928]])
            if list(point) not in exc['cells']:continue
            assert result==exc['previous_owner'],'Broken protected-core exception chain'
            geo=json.loads((directory/'GEOMETRY.json').read_text())
            changed=[r for r in geo['assignments'] if list(point) in r['cells']]
            assert len(changed)==1 and changed[0]['owner']==exc['new_owner'] and changed[0]['parent_rgb']==exc['rgb'] and changed[0]['previous_owner']==result and changed[0]['pixels']==1
            result=exc['new_owner']
    return result

def protected_core_preserved(row,bitmap,owners,later_dirs):
    """Exact core identity/count, minus only independently declared exceptions."""
    color=int(row['rgb'][1:],16);retained=0
    for point in row['cells']:
        x,y=point;expected=reviewed_core_exception_owner(point,row['owner'],later_dirs)
        actual_rgb='x'+format(int(bitmap[y,x]),'06X')
        if owners.get(actual_rgb)!=expected:return False
        if expected==row['owner']:
            retained+=1
            if bitmap[y,x]!=color:return False
    return owners.get(row['rgb'])==row['owner'] and int((bitmap==color).sum())==retained

def expected_locator_rgb(original,point,later_dirs):
    """Replay exact approved hub RGB rebindings, never physical movement."""
    value=original
    for directory in later_dirs:
        migration=json.loads((directory/'REGISTRY_MIGRATION.json').read_text())
        for binding in migration.get('region_reference_changes',[]):
            if binding.get('pixel')==list(point):
                assert int(binding.get('bitmap_before',binding['before'])[1:],16)==value
                value=int(binding['after'][1:],16)
    return value

def effective_assignments(geometries):
    """Explicit ordered geometry layers; later splits replace their parent only."""
    rows=[]
    for g in geometries:
        parents=set(g.get('parents',[]))
        rows=[r for r in rows if r['rgb'] not in parents]+g['assignments']
    return rows


def expected_country_definitions(before,migrations):
    """Only exact declared additions; never waive preservation of an old tag."""
    expected=dict(before)
    for migration in migrations:
        change=migration.get('anhalt_name_correction')
        if change:
            assert migration['new_members']==['ABG','AKT','AZR'] and change['tag']=='ANH'
            assert expected['ANH']==change['before_signature']
            node=json.loads(expected['ANH']);fields=[v for v in node[2] if v[0]=='is_named_from_capital']
            assert len(fields)==1 and fields[0][2]=='yes'
            fields[0][2]='no'
            signature=json.dumps(node,ensure_ascii=False,separators=(',',':'))
            assert signature==change['after_signature'],'Only explicit Anhalt naming may change'
            expected['ANH']=signature
        # A reviewed Swabian correction, not a permission to rewrite an old
        # country. Reconstruct the resulting signature by changing tier only.
        for change in migration.get('country_tier_corrections',[]):
            tag=change['tag']
            if tag=='WUR':
                assert change['before']=='kingdom' and change['after']=='principality'
            else:
                assert migration.get('replaced_regions')==['STATE_SAXONY']
                assert migration.get('new_members')==['GOT','HIL','SSO','RGZ','RGE','RSL']
                assert (tag,change['before'],change['after']) in {('SAX','kingdom','principality'),('WEI','grand_principality','principality')}
            assert expected[tag]==change['before_signature']
            node=json.loads(expected[tag]);tiers=[v for v in node[2] if v[0]=='tier']
            assert len(tiers)==1 and tiers[0][2]==change['before']
            tiers[0][2]=change['after']
            signature=json.dumps(node,ensure_ascii=False,separators=(',',':'))
            assert signature==change['after_signature'],'Only the explicitly approved country tier may change'
            expected[tag]=signature
        for change in migration.get('country_capital_corrections',[]):
            assert migration.get('new_members')==['RLO','REB']
            assert migration.get('replaced_regions')==['STATE_SAXONY','STATE_ANHALT']
            assert (change['tag'],change['before'],change['after'])==('SSO','STATE_SAXONY','STATE_ANHALT')
            assert expected['SSO']==change['before_signature']
            node=json.loads(expected['SSO']);capitals=[v for v in node[2] if v[0]=='capital']
            assert len(capitals)==1 and capitals[0][2]=='STATE_SAXONY'
            capitals[0][2]='STATE_ANHALT'
            signature=json.dumps(node,ensure_ascii=False,separators=(',',':'))
            assert signature==change['after_signature'],'Only the Sondershausen capital region may change'
            expected['SSO']=signature
        additions=migration.get('country_additions',{})
        assert set(additions)<=set(migration['new_members'])
        for tag,signature in additions.items():
            assert tag not in expected,'Existing country cannot be overwritten '+tag
            expected[tag]=signature
    return expected


def rebind_state_definitions(raw,migrations):
    """Replay only documented hub-RGB references and prime-land expansion."""
    import validate_diplomacy_ottoman_1776 as parser
    from map_1776_audit import values
    from map2a_patch import edits
    for migration in migrations:
        for change in migration.get('region_reference_changes',[]):
            assert change['field'] in {'city','port','farm','mine','wood','prime_land'}
            assert change['state'] in migration['replaced_regions']
            nodes={n.key:n for n in parser.parse(raw)}
            # A cumulative validator may be checking a different region file
            # (e.g. Italy); no Westphalian node can be rebound in that file.
            if change['state'] not in nodes:continue
            region=nodes[change['state']]
            field=region.children(change['field'])[0]
            if change['field']=='prime_land':
                assert values(region,'prime_land')==change['before']
                replacement='prime_land = { '+' '.join('"'+rgb+'"' for rgb in change['after'])+' }'
            else:
                assert parser.scalar(field.value)==change['before']
                replacement=change['field']+' = "'+change['after']+'"'
            raw=edits(raw,[(field.start,field.end,replacement)])
    return raw

def ancestor_rgb(rgb,existing_colors):
    """Resolve only declared child chains to an immutable bitmap's RGB set."""
    parents={r['rgb']:r['parent_rgb'] for fp in approved_lot_dirs() for r in json.loads((fp/'GEOMETRY.json').read_text())['new_provinces']}
    seen=set()
    while int(rgb[1:],16) not in existing_colors:
        assert rgb not in seen and rgb in parents,'Undeclared or cyclic parent chain '+rgb
        seen.add(rgb);rgb=parents[rgb]
    return int(rgb[1:],16)

def apply_territorial_migrations(rows):
    current=list(rows)
    for m in approved_territorial_migrations():
        regions=set(m['replaced_regions'])
        previous=[r for r in current if r['state'] in regions]
        assert sorted(previous,key=lambda r:r['rgb'])==sorted(m['previous'],key=lambda r:r['rgb']),'Unreviewed registry migration input'
        current=[r for r in current if r['state'] not in regions]+m['updated']
    return sorted(current,key=lambda r:(r['rgb'],r['state'],r['beneficiary']))


def ownership_rows(migration,phase):
    """A nonmember border split must not turn its ownership into imperial rights."""
    return migration.get('ownership_'+phase,migration[phase])


def migrate_extent(mask,migrations):
    """Only exact, explicitly recorded raster cells may extend/remove rights."""
    result=mask.copy()
    for migration in migrations:
        for field,value in [('extent_removed_cells',False),('extent_added_cells',True)]:
            cells=migration.get(field,[])
            assert len({tuple(c) for c in cells})==len(cells),'Duplicate extent cells'
            for x,y in cells:
                assert 0<=y<result.shape[0] and 0<=x<result.shape[1]
                assert bool(result[y,x])!=value,'Extent migration is not a delta'
                result[y,x]=value
    return result
