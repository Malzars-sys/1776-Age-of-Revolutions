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
    return [ROOT/'docs/reports/map/MAP2L'/name for name in ['FRANCONIA','RHINE_CENTRAL','MAINZ_PALATINATE','MAINZ_ESTATES','MAINZ_COMPLETION','MILAN_CREMONESE','FRANCONIA_CONTINUATION']
            if (ROOT/'docs/reports/map/MAP2L'/name/'REGISTRY_MIGRATION.json').exists()]

def effective_assignments(geometries):
    """Explicit ordered geometry layers; later splits replace their parent only."""
    rows=[]
    for g in geometries:
        parents=set(g.get('parents',[]))
        rows=[r for r in rows if r['rgb'] not in parents]+g['assignments']
    return rows

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
