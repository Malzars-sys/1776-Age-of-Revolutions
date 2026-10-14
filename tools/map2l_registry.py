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

def member_region_overrides():
    # Membership is country-wide, whereas territorial rights are explicit.
    # Do not register Sardinia, Savoy or every other possession of this member.
    return {'SAR': {'STATE_PIEDMONT'}}

def approved_territorial_extensions():
    manifest=ROOT/'docs/reports/map/MAP2L/PIEDMONT/EXTENSION.json'
    return json.loads(manifest.read_text(encoding='utf-8'))['provinces'] if manifest.exists() else []

def approved_territorial_migrations():
    return [json.loads((p/'REGISTRY_MIGRATION.json').read_text(encoding='utf-8')) for p in approved_lot_dirs()]


def approved_lot_dirs():
    # Ordered explicit manifests only; no directory discovery or broad allowlist.
    return [ROOT/'docs/reports/map/MAP2L'/name for name in ['FRANCONIA','RHINE_CENTRAL','MAINZ_PALATINATE','MAINZ_ESTATES','MAINZ_COMPLETION','MILAN_CREMONESE','FRANCONIA_CONTINUATION','RHINE_WESTPHALIA','MINDEN_RAVENSBERG']
            if (ROOT/'docs/reports/map/MAP2L'/name/'REGISTRY_MIGRATION.json').exists()]

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
