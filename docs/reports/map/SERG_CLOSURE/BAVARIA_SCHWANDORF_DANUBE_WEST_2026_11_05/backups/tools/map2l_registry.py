"""Versioned, explicitly reviewed territorial registry; keep MAP2K frozen."""
import json,hashlib
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
    result=earlier+([poel] if (poel/'REGISTRY_MIGRATION.json').exists() else [])+([completion] if (completion/'REGISTRY_MIGRATION.json').exists() else [])+([east_frisia] if (east_frisia/'REGISTRY_MIGRATION.json').exists() else [])+([eutin] if (eutin/'REGISTRY_MIGRATION.json').exists() else [])+([kaltenhof] if (kaltenhof/'REGISTRY_MIGRATION.json').exists() else [])+([anhalt] if (anhalt/'REGISTRY_MIGRATION.json').exists() else [])+([saxony] if (saxony/'REGISTRY_MIGRATION.json').exists() else [])+([thuringia] if (thuringia/'REGISTRY_MIGRATION.json').exists() else [])+([fulda] if (fulda/'REGISTRY_MIGRATION.json').exists() else [])
    nassau=fulda/'R2'
    if (nassau/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((nassau/'REGISTRY_MIGRATION.json').read_text(encoding='utf8'))
        geo=json.loads((nassau/'GEOMETRY.json').read_text(encoding='utf8'))
        assert m['replaced_regions']==['STATE_HESSE'] and m['new_members']==['NOU','NWB']
        assert not m['free_cities'] and not m['extent_added_cells'] and not m['extent_removed_cells']
        assert geo['parents']==['x1357DB','x3E794B','x8B7C67'] and m['new_provinces']==geo['new_provinces']
        assert len(m['new_provinces'])==9 and sum(r['pixels'] for r in geo['assignments'])==561
        assert sum(r['pixels'] for r in geo['assignments'] if r['owner']!=r['previous_owner'])==72
        assert all(r['state']=='STATE_HESSE' and r['previous_owner'] in {'NAS','WLD','HES'} and r['owner'] in {r['previous_owner'],'NOU','NWB','NAS'} for r in geo['assignments'])
        assert all(4270<=x<=4305 and 830<=y<=860 for r in geo['assignments'] if r['owner']!=r['previous_owner'] for x,y in r['cells'])
        assert set(m['country_additions'])=={'NOU','NWB'}
        assert all(r['beneficiary'] in {'NOU','NWB','NAS','HES','WLD'} for r in m['updated'] if r['rgb'] in {a['rgb'] for a in geo['assignments']})
        result.append(nassau)
    continuation=fulda/'R2B'
    if (continuation/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((continuation/'REGISTRY_MIGRATION.json').read_text(encoding='utf8'))
        geo=json.loads((continuation/'GEOMETRY.json').read_text(encoding='utf8'))
        assert m['replaced_regions']==['STATE_HESSE','STATE_RHINELAND','STATE_SAXONY']
        assert m['new_members']==['NSB'] and set(m['country_additions'])=={'NSB'}
        assert not m['free_cities'] and not m['extent_added_cells'] and not m['extent_removed_cells']
        assert geo['parents']==['x11C021','x11C0A0','x1357DB','x8B7C67','x90C0A0','xD04121','xD0C021']
        assert m['new_provinces']==geo['new_provinces']
        assert [r['rgb'] for r in m['new_provinces']]==['xEDB8'+format(i,'02X') for i in range(13)]
        transferred=[r for r in geo['assignments'] if r['owner']!=r['previous_owner']]
        assert sum(r['pixels'] for r in transferred)==45
        allowed={('x11C021','KPF','NSB','STATE_RHINELAND'),('x11C0A0','FRM','NAS','STATE_HESSE'),('x1357DB','NAS','NOU','STATE_HESSE'),('x1357DB','NAS','NWB','STATE_HESSE'),('x90C0A0','NAS','NOU','STATE_HESSE'),('x8B7C67','HES','NAS','STATE_HESSE'),('xD04121','HEK','FUL','STATE_HESSE'),('xD0C021','MEI','FUL','STATE_SAXONY')}
        assert all((r['parent_rgb'],r['previous_owner'],r['owner'],r['state']) in allowed for r in transferred)
        for r in transferred:
            bounds=(4260,4269,875,884) if r['owner']=='NSB' else (4314,4335,836,846) if r['owner']=='FUL' else (4280,4300,843,860)
            x0,x1,y0,y1=bounds
            assert all(x0<=x<=x1 and y0<=y<=y1 for x,y in r['cells'])
        # No waiver for any previously accepted core; all eligible parents
        # are retained residuals or unsplit pre-MAP colours, never xED cores.
        assert all(not r['parent_rgb'].startswith('xED') for r in geo['assignments'])
        assert all(r['field'] in {'prime_land','mine'} for r in m['region_reference_changes'])
        result.append(continuation)
    passau=fulda/'R4/POLITICAL_REPRESENTATION/PASSAU'
    if (passau/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((passau/'REGISTRY_MIGRATION.json').read_text(encoding='utf8'))
        geo=json.loads((passau/'GEOMETRY.json').read_text(encoding='utf8'))
        assert m['replaced_regions']==['STATE_BAVARIA'] and m['new_members']==['PAS']
        assert set(m['country_additions'])=={'PAS'} and not m['free_cities']
        assert not m['extent_added_cells'] and not m['extent_removed_cells'] and not m['region_reference_changes']
        assert geo['parents']==['xB08021'] and geo['selected_option']=='OPTION_1_MINIMAL'
        assert geo['classification']=='B_POLITICAL_APPROXIMATION' and not geo['historical_cadastral_precision']
        assert m['new_provinces']==geo['new_provinces']==[{'rgb':'xEDBA00','parent_rgb':'xB08021'}]
        assert len(geo['assignments'])==2 and sum(r['pixels'] for r in geo['assignments'])==252
        assert {(r['rgb'],r['owner'],r['pixels']) for r in geo['assignments']}=={('xB08021','BAV',212),('xEDBA00','PAS',40)}
        assert all(r['parent_rgb']=='xB08021' and r['state']=='STATE_BAVARIA' and r['previous_owner']=='BAV' for r in geo['assignments'])
        cells=sorted(c for r in geo['assignments'] if r['owner']=='PAS' for c in r['cells'])
        assert len(cells)==len({tuple(c) for c in cells})==40
        assert hashlib.sha256(json.dumps(cells,separators=(',',':')).encode()).hexdigest()=='3d95b83f8956e38d29a34303b537469ff812ea70d33ea0ebdefa2aa6ba4c0ea6'
        old={r['rgb']:r for r in m['previous']};new={r['rgb']:r for r in m['updated']}
        assert set(new)==set(old)|{'xEDBA00'} and all(new[k]==v for k,v in old.items() if k!='xB08021')
        assert new['xB08021']['beneficiary']=='BAV' and new['xEDBA00']['beneficiary']=='PAS'
        result.append(passau)
    # Two separately reviewed political layers; no reopening of Passau or R3.
    bc=fulda/'R4/POLITICAL_REPRESENTATION/FREISING_REGENSBURG'
    contracts=[('R4B',['FSI'],[],['x68CE1C'],[('xEDBA10','x68CE1C')],
                {('x68CE1C','BAV',167),('xEDBA10','FSI',14)},
                'fdcb024cebfd604d09b73b75631806c494ef705cc39313fd32b3b4741deab8a5'),
               ('R4C',['RBI','RCI'],['RCI'],['x3101A0','xA7094D','xFE59E7'],
                [('xEDBA11','x3101A0'),('xEDBA12','x3101A0'),('xEDBA13','xA7094D'),('xEDBA14','xFE59E7')],
                {('x3101A0','BAV',219),('xEDBA11','RBI',5),('xEDBA12','RBI',9),('xA7094D','BAV',126),('xEDBA13','RCI',1),('xFE59E7','BAV',165),('xEDBA14','RCI',1)},
                '9912e18bd05d16c5a46d0ec6d1793bab3a147da6fb377034bb3e5d6dd2213452')]
    for sector,members,free,parents,children,assignments,digest in contracts:
        directory=bc/sector
        if not (directory/'REGISTRY_MIGRATION.json').exists():continue
        assert passau in result
        if sector=='R4C':assert bc/'R4B' in result
        m=json.loads((directory/'REGISTRY_MIGRATION.json').read_text(encoding='utf8'))
        geo=json.loads((directory/'GEOMETRY.json').read_text(encoding='utf8'))
        assert m['replaced_regions']==['STATE_BAVARIA'] and m['new_members']==members and m['free_cities']==free
        assert set(m['country_additions'])==set(members)
        assert not m['extent_added_cells'] and not m['extent_removed_cells'] and not m['region_reference_changes']
        assert geo['parents']==parents and geo['new_members']==members and geo['free_cities']==free
        assert geo['classification']=='B_POLITICAL_APPROXIMATION' and not geo['historical_cadastral_precision']
        assert m['new_provinces']==geo['new_provinces']==[dict(rgb=rgb,parent_rgb=parent) for rgb,parent in children]
        assert {(r['rgb'],r['owner'],r['pixels']) for r in geo['assignments']}==assignments
        assert all(r['state']=='STATE_BAVARIA' and r['previous_owner']=='BAV' and r['parent_rgb'] in parents for r in geo['assignments'])
        footprint=sorted([r['rgb'],r['owner'],x,y] for r in geo['assignments'] for x,y in r['cells'])
        assert len({(x,y) for _,_,x,y in footprint})==len(footprint)
        assert hashlib.sha256(json.dumps(footprint,separators=(',',':')).encode()).hexdigest()==digest
        old={r['rgb']:r for r in m['previous']};new={r['rgb']:r for r in m['updated']}
        assert set(new)==set(old)|{rgb for rgb,_ in children}
        assert all(new[k]==v for k,v in old.items() if k not in parents)
        assert all(new[parent]['beneficiary']=='BAV' for parent in parents)
        assert all(new[r['rgb']]['beneficiary']==r['owner'] for r in geo['assignments'])
        result.append(directory)
    # Authorized SC1-SALZBURG installation: a residence nucleus only. Runtime
    # validation remains pending; this manifest authorizes no peripheral claims.
    salzburg=ROOT/'docs/reports/map/SERG_CLOSURE/SC1-SALZBURG'
    if (salzburg/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((salzburg/'REGISTRY_MIGRATION.json').read_text(encoding='utf8'))
        geo=json.loads((salzburg/'GEOMETRY.json').read_text(encoding='utf8'))
        assert bc/'R4C' in result
        assert m['replaced_regions']==['STATE_BAVARIA'] and m['new_members']==['SLZ'] and not m['free_cities']
        assert set(m['country_additions'])=={'SLZ'}
        assert not m['extent_added_cells'] and not m['extent_removed_cells'] and not m['region_reference_changes']
        assert geo['parents']==['x6EA29B'] and geo['selected_option']=='CITY_ONLY'
        assert geo['classification']=='B_POLITICAL_APPROXIMATION' and not geo['historical_cadastral_precision']
        assert m['new_provinces']==geo['new_provinces']==[{'rgb':'xEDBB00','parent_rgb':'x6EA29B'}]
        assert {(r['rgb'],r['owner'],r['pixels']) for r in geo['assignments']}=={('x6EA29B','BAV',53),('xEDBB00','SLZ',12)}
        assert all(r['state']=='STATE_BAVARIA' and r['previous_owner']=='BAV' and r['parent_rgb']=='x6EA29B' for r in geo['assignments'])
        assert next(r['cells'] for r in geo['assignments'] if r['owner']=='SLZ')==[[x,y] for x in range(4385,4389) for y in range(924,927)]
        old={r['rgb']:r for r in m['previous']};new={r['rgb']:r for r in m['updated']}
        assert set(new)==set(old)|{'xEDBB00'} and all(new[k]==v for k,v in old.items())
        assert new['x6EA29B']['beneficiary']=='BAV' and new['xEDBB00']['beneficiary']=='SLZ'
        result.append(salzburg)
    # Authorized SC4-MASSA-CARRARA political nucleus, explicitly bounded.
    # No annexation of Lucca, Genoa or the whole Modenese coastal province.
    massa=ROOT/'docs/reports/map/SERG_CLOSURE/SC4-MASSA-CARRARA'
    if (massa/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((massa/'REGISTRY_MIGRATION.json').read_text(encoding='utf8'))
        geo=json.loads((massa/'GEOMETRY.json').read_text(encoding='utf8'))
        assert salzburg in result
        assert m['replaced_regions']==['STATE_EMILIA'] and m['new_members']==['MCA'] and not m['free_cities']
        assert set(m['country_additions'])=={'MCA'}
        assert not m['extent_added_cells'] and not m['extent_removed_cells']
        assert m['region_reference_changes']==[{'state':'STATE_EMILIA','field':'prime_land','before':['xF08021','x0B3B43'],'after':['xF08021','xEDBC00','x0B3B43']}]
        assert geo['parents']==['xF08021'] and geo['selected_option']=='COASTAL_RESIDENCE_CORE'
        assert geo['classification']=='B_POLITICAL_APPROXIMATION' and not geo['historical_cadastral_precision']
        assert m['new_provinces']==geo['new_provinces']==[{'rgb':'xEDBC00','parent_rgb':'xF08021'}]
        assert {(r['rgb'],r['owner'],r['pixels']) for r in geo['assignments']}=={('xF08021','MOD',108),('xEDBC00','MCA',8)}
        assert all(r['state']=='STATE_EMILIA' and r['previous_owner']=='MOD' and r['parent_rgb']=='xF08021' for r in geo['assignments'])
        assert next(r['cells'] for r in geo['assignments'] if r['owner']=='MCA')==[[4325,1029],[4326,1029],[4326,1030],[4327,1030],[4327,1031],[4328,1030],[4328,1031],[4328,1032]]
        old={r['rgb']:r for r in m['previous']};new={r['rgb']:r for r in m['updated']}
        assert set(new)==set(old)|{'xEDBC00'} and all(new[k]==v for k,v in old.items())
        assert old['xF08021']['beneficiary']==new['xF08021']['beneficiary']=='MOD'
        assert new['xEDBC00']['beneficiary']=='MCA'
        result.append(massa)
    # SC1-TRENTO: residence only; never all South Tyrol or the diocese.
    trento=ROOT/'docs/reports/map/SERG_CLOSURE/SC1-TRENTO'
    if (trento/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((trento/'REGISTRY_MIGRATION.json').read_text(encoding='utf8'))
        geo=json.loads((trento/'GEOMETRY.json').read_text(encoding='utf8'))
        assert massa in result
        assert m['replaced_regions']==['STATE_SOUTH_TYROL'] and m['new_members']==['TRT'] and not m['free_cities']
        assert set(m['country_additions'])=={'TRT'}
        assert not m['extent_added_cells'] and not m['extent_removed_cells']
        assert m['region_reference_changes']==[{'state':'STATE_SOUTH_TYROL','field':'city','before':'xD0BF60','after':'xEDBD00','pixel':[4352,973]}]
        assert geo['hub_rebindings']==m['region_reference_changes']
        assert geo['parents']==['xD0BF60'] and geo['selected_option']=='TRENT_RESIDENCE_CORE'
        assert geo['classification']=='B_POLITICAL_APPROXIMATION' and not geo['historical_cadastral_precision']
        assert m['new_provinces']==geo['new_provinces']==[{'rgb':'xEDBD00','parent_rgb':'xD0BF60'}]
        assert {(r['rgb'],r['owner'],r['pixels']) for r in geo['assignments']}=={('xD0BF60','AUS',291),('xEDBD00','TRT',12)}
        assert all(r['state']=='STATE_SOUTH_TYROL' and r['previous_owner']=='AUS' and r['parent_rgb']=='xD0BF60' for r in geo['assignments'])
        assert next(r['cells'] for r in geo['assignments'] if r['owner']=='TRT')==[[4350,973],[4350,974],[4351,972],[4351,973],[4351,974],[4352,972],[4352,973],[4352,974],[4353,972],[4353,973],[4353,974],[4354,973]]
        old={r['rgb']:r for r in m['previous']};new={r['rgb']:r for r in m['updated']}
        assert set(new)==set(old)|{'xEDBD00'} and all(new[k]==v for k,v in old.items())
        assert old['xD0BF60']['beneficiary']==new['xD0BF60']['beneficiary']=='AUS'
        assert new['xEDBD00']['beneficiary']=='TRT'
        result.append(trento)
    # SC1-BRIXEN: nine-cell residence, no diocesan/Puster annexation.
    # No hub rebind: the human-validated Trento city reference is retained.
    brixen=ROOT/'docs/reports/map/SERG_CLOSURE/SC1-BRIXEN'
    if (brixen/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((brixen/'REGISTRY_MIGRATION.json').read_text(encoding='utf8'))
        geo=json.loads((brixen/'GEOMETRY.json').read_text(encoding='utf8'))
        assert trento in result
        assert m['replaced_regions']==['STATE_SOUTH_TYROL'] and m['new_members']==['BRX'] and not m['free_cities']
        assert set(m['country_additions'])=={'BRX'}
        assert not m['extent_added_cells'] and not m['extent_removed_cells']
        assert m['region_reference_changes']==geo['hub_rebindings']==[]
        assert geo['parents']==['xD040E0'] and geo['selected_option']=='BRIXEN_RESIDENCE_CORE'
        assert geo['classification']=='B_POLITICAL_APPROXIMATION' and not geo['historical_cadastral_precision']
        assert m['new_provinces']==geo['new_provinces']==[{'rgb':'xEDBE00','parent_rgb':'xD040E0'}]
        assert {(r['rgb'],r['owner'],r['pixels']) for r in geo['assignments']}=={('xD040E0','AUS',453),('xEDBE00','BRX',9)}
        assert all(r['state']=='STATE_SOUTH_TYROL' and r['previous_owner']=='AUS' and r['parent_rgb']=='xD040E0' for r in geo['assignments'])
        assert next(r['cells'] for r in geo['assignments'] if r['owner']=='BRX')==[[x,y] for x in range(4362,4365) for y in range(948,951)]
        old={r['rgb']:r for r in m['previous']};new={r['rgb']:r for r in m['updated']}
        assert set(new)==set(old)|{'xEDBE00'} and all(new[k]==v for k,v in old.items())
        assert old['xD040E0']['beneficiary']==new['xD040E0']['beneficiary']=='AUS'
        assert old['xEDBD00']['beneficiary']==new['xEDBD00']['beneficiary']=='TRT'
        assert new['xEDBE00']['beneficiary']=='BRX'
        result.append(brixen)
    # Berchtesgaden residence B only; no cell from the validated SLZ core.
    berchtesgaden=ROOT/'docs/reports/map/SERG_CLOSURE/SC1-BERCHTESGADEN'
    if (berchtesgaden/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((berchtesgaden/'REGISTRY_MIGRATION.json').read_text(encoding='utf8'))
        geo=json.loads((berchtesgaden/'GEOMETRY.json').read_text(encoding='utf8'))
        assert brixen in result
        assert m['replaced_regions']==['STATE_TYROL'] and m['new_members']==['BGT'] and not m['free_cities']
        assert set(m['country_additions'])=={'BGT'}
        assert not m['extent_added_cells'] and not m['extent_removed_cells']
        assert m['region_reference_changes']==geo['hub_rebindings']==[]
        assert geo['parents']==['xAB7EB0'] and geo['selected_option']=='BERCHTESGADEN_RESIDENCE_CORE'
        assert geo['classification']=='B_POLITICAL_APPROXIMATION' and not geo['historical_cadastral_precision']
        assert m['new_provinces']==geo['new_provinces']==[{'rgb':'xEDBF00','parent_rgb':'xAB7EB0'}]
        assert {(r['rgb'],r['owner'],r['pixels']) for r in geo['assignments']}=={('xAB7EB0','AUS',304),('xEDBF00','BGT',4)}
        assert all(r['state']=='STATE_TYROL' and r['previous_owner']=='AUS' and r['parent_rgb']=='xAB7EB0' for r in geo['assignments'])
        assert next(r['cells'] for r in geo['assignments'] if r['owner']=='BGT')==[[4384,930],[4384,931],[4385,930],[4385,931]]
        old={r['rgb']:r for r in m['previous']};new={r['rgb']:r for r in m['updated']}
        assert set(new)==set(old)|{'xEDBF00'} and all(new[k]==v for k,v in old.items())
        assert old['xAB7EB0']['beneficiary']==new['xAB7EB0']['beneficiary']=='AUS'
        assert new['xEDBF00']['beneficiary']=='BGT'
        result.append(berchtesgaden)
    passau_outliers=ROOT/'docs/reports/map/SERG_CLOSURE/SC1-PASSAU-OUTLIERS'
    if (passau_outliers/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((passau_outliers/'REGISTRY_MIGRATION.json').read_text(encoding='utf8'))
        geo=json.loads((passau_outliers/'GEOMETRY.json').read_text(encoding='utf8'))
        assert berchtesgaden in result
        assert m['replaced_regions']==['STATE_AUSTRIA'] and m['new_members']==[] and not m['free_cities'] and m['country_additions']=={}
        assert not m['extent_added_cells'] and not m['extent_removed_cells']
        assert m['region_reference_changes']==geo['hub_rebindings']==[]
        assert geo['parents']==['xFDA6CB'] and geo['selected_option']=='OBERNBERG_MARKET_CORE'
        assert geo['classification']=='B_POLITICAL_APPROXIMATION' and not geo['historical_cadastral_precision']
        assert m['new_provinces']==geo['new_provinces']==[{'rgb':'xEDC000','parent_rgb':'xFDA6CB'}]
        assert {(r['rgb'],r['owner'],r['pixels']) for r in geo['assignments']}=={('xFDA6CB','AUS',175),('xEDC000','PAS',4)}
        assert all(r['state']=='STATE_AUSTRIA' and r['previous_owner']=='AUS' and r['parent_rgb']=='xFDA6CB' for r in geo['assignments'])
        assert next(r['cells'] for r in geo['assignments'] if r['owner']=='PAS')==[[4393,911],[4393,912],[4394,911],[4394,912]]
        old={r['rgb']:r for r in m['previous']};new={r['rgb']:r for r in m['updated']}
        assert set(new)==set(old)|{'xEDC000'} and all(new[k]==v for k,v in old.items())
        assert old['xFDA6CB']['beneficiary']==new['xFDA6CB']['beneficiary']=='AUS'
        assert new['xEDC000']['beneficiary']=='PAS'
        result.append(passau_outliers)
    ortenburg=ROOT/'docs/reports/map/SERG_CLOSURE/SC1-ORTENBURG'
    if (ortenburg/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((ortenburg/'REGISTRY_MIGRATION.json').read_text(encoding='utf8'))
        geo=json.loads((ortenburg/'GEOMETRY.json').read_text(encoding='utf8'))
        assert passau_outliers in result
        assert m['replaced_regions']==['STATE_BAVARIA'] and m['new_members']==['ORT'] and m['free_cities']==[]
        assert not m['extent_added_cells'] and not m['extent_removed_cells'] and m['region_reference_changes']==geo['hub_rebindings']==[]
        assert geo['parents']==['x8C26DD'] and geo['selected_option']=='ORTENBURG_MARKET_CASTLE_CORE'
        assert geo['classification']=='B_POLITICAL_APPROXIMATION' and not geo['historical_cadastral_precision']
        assert m['new_provinces']==geo['new_provinces']==[{'rgb':'xEDC100','parent_rgb':'x8C26DD'}]
        assert {(r['rgb'],r['owner'],r['pixels']) for r in geo['assignments']}=={('x8C26DD','BAV',272),('xEDC100','ORT',4)}
        assert next(r['cells'] for r in geo['assignments'] if r['owner']=='ORT')==[[4392,901],[4392,902],[4393,901],[4393,902]]
        old={r['rgb']:r for r in m['previous']};new={r['rgb']:r for r in m['updated']}
        assert set(new)==set(old)|{'xEDC100'} and all(new[k]==v for k,v in old.items())
        assert old['x8C26DD']['beneficiary']==new['x8C26DD']['beneficiary']=='BAV' and new['xEDC100']['beneficiary']=='ORT'
        assert set(m['country_additions'])=={'ORT'}
        result.append(ortenburg)
    teschen=ROOT/'docs/reports/map/SERG_CLOSURE/SC2-TESCHEN'
    if (teschen/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((teschen/'REGISTRY_MIGRATION.json').read_text(encoding='utf8'))
        g=json.loads((teschen/'GEOMETRY.json').read_text(encoding='utf8'))
        native=json.loads((teschen/'NATIVE_INVENTORY.json').read_text(encoding='utf8'))
        assert ortenburg in result
        assert m['replaced_regions']==['STATE_WEST_GALICIA'] and m['previous']==[]
        assert len(m['updated'])==1
        row=m['updated'][0]
        assert (row['rgb'],row['state'],row['beneficiary'])==('x9061E0','STATE_WEST_GALICIA','AUS')
        assert m['new_members']==m['free_cities']==m['new_provinces']==m['region_reference_changes']==[]
        assert m['country_additions']=={} and m['ownership_previous']==m['ownership_updated']==[]
        assert m['extent_removed_cells']==[]
        assert len(m['extent_added_cells'])==179 and len({tuple(p) for p in m['extent_added_cells']})==179
        assert m['extent_added_cells']==native['cells']==g['registry_extent_cells']
        assert native['target']=='x9061E0' and native['state']=='STATE_WEST_GALICIA' and native['owner']=='AUS'
        assert g['classification']=='B_EXISTING_POLITICAL_REPRESENTATION_REGISTRY_ONLY' and g['physical_map_changed'] is False
        assert not g['historical_cadastral_precision'] and g['parents']==g['new_provinces']==g['assignments']==g['hub_rebindings']==[]
        assert m['province_membership_overrides']==[dict(rgb='x9061E0',state='STATE_WEST_GALICIA',owner='AUS')]
        result.append(teschen)
    prussia=ROOT/'docs/reports/map/SERG_CLOSURE/PRUSSIA_V1_2026_11_02'
    if (prussia/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((prussia/'REGISTRY_MIGRATION.json').read_text(encoding='utf8'))
        g=json.loads((prussia/'GEOMETRY.json').read_text(encoding='utf8'))
        assert teschen in result
        assert m['replaced_regions']==['STATE_BRANDENBURG','STATE_LOWER_SILESIA']
        assert m['new_members']==m['free_cities']==m['extent_added_cells']==m['extent_removed_cells']==[]
        assert m['country_additions']=={} and m['new_provinces']==g['new_provinces']
        assert g['classification']=='B_POLITICAL_GENERALISATION' and not g['historical_cadastral_precision']
        assert set(g['parents'])=={'xDF4020','x60BF20','xB90BFF','x76EF4E','x1B72C9','x614121','x272E48'}
        assert all(r['state'] in m['replaced_regions'] and r['previous_owner']=='PRU' and r['owner'] in {'PRU','SAX'} for r in g['assignments'])
        old={r['rgb']:r for r in m['previous']};new={r['rgb']:r for r in m['updated']}
        assert all(new[k]==v for k,v in old.items() if k not in g['parents'])
        assert len(new)==len(old)+len(g['new_provinces'])
        assert {(r['rgb'],r['state'],r['beneficiary']) for r in m['updated'] if r['rgb'] not in old or r['rgb'] in g['parents']}=={(r['rgb'],r['state'],r['owner']) for r in g['assignments']}
        result.append(prussia)
    north_saxony=ROOT/'docs/reports/map/SERG_CLOSURE/NORTH_SAXONY_1_2026_11_05'
    if (north_saxony/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((north_saxony/'REGISTRY_MIGRATION.json').read_text(encoding='utf8'))
        g=json.loads((north_saxony/'GEOMETRY.json').read_text(encoding='utf8'))
        assert prussia in result
        assert m['replaced_regions']==['STATE_ANHALT','STATE_BRANDENBURG']
        assert m['new_members']==m['free_cities']==m['extent_added_cells']==m['extent_removed_cells']==[]
        assert m['country_additions']=={} and m['new_provinces']==g['new_provinces']
        assert g['classification']=='B_POLITICAL_GENERALISATION' and not g['historical_cadastral_precision']
        assert set(g['parents'])=={'x34386E','x83B1A8','x9B9076','xA65DA6','xCF5D8E','xDF4020'}
        assert g['ownership_cells']==606 and len(g['new_provinces'])==5
        assert all(r['state'] in m['replaced_regions'] and r['previous_owner']=='PRU' and r['owner'] in {'PRU','SAX'} for r in g['assignments'])
        old={r['rgb']:r for r in m['previous']};new={r['rgb']:r for r in m['updated']}
        assert all(new[k]==v for k,v in old.items() if k not in g['parents'])
        assert len(new)==len(old)+len(g['new_provinces'])
        assert {(r['rgb'],r['state'],r['beneficiary']) for r in m['updated'] if r['rgb'] not in old or r['rgb'] in g['parents']}=={(r['rgb'],r['state'],r['owner']) for r in g['assignments']}
        result.append(north_saxony)
    polish_frontier=ROOT/'docs/reports/map/SERG_CLOSURE/PRUSSIA_POLAND_2026_11_05'
    if (polish_frontier/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((polish_frontier/'REGISTRY_MIGRATION.json').read_text(encoding='utf8'))
        g=json.loads((polish_frontier/'GEOMETRY.json').read_text(encoding='utf8'))
        assert north_saxony in result
        assert m['replaced_regions']==['STATE_POSEN','STATE_WEST_PRUSSIA']
        assert m['previous']==m['updated']==m['new_members']==m['free_cities']==m['extent_added_cells']==m['extent_removed_cells']==[]
        assert m['country_additions']=={} and m['external_to_hre'] is True
        assert m['new_provinces']==g['new_provinces'] and len(g['new_provinces'])==4
        assert g['classification']=='B_POLITICAL_GENERALISATION' and not g['historical_cadastral_precision']
        assert set(g['parents'])=={'x41A021','xC02121','xFCC7B7','x374AC3'}
        assert sum(r['pixels'] for r in g['assignments'] if r['owner']!=r['previous_owner'])==285
        assert all(r['state'] in m['replaced_regions'] and {r['owner'],r['previous_owner']}<={'PRU','PLC'} for r in g['assignments'])
        assert len(m['locator_relocations'])==1 and m['locator_relocations']==g['locator_relocations']
        loc=m['locator_relocations'][0]
        assert (loc['state'],loc['kind'],loc['id'])==('STATE_WEST_PRUSSIA','farm',158)
        assert loc['before_position']==[4519.314941,0.,2843.895264] and loc['after_position']==[4521.5,0.,2848.5]
        result.append(polish_frontier)
    prussian_west=ROOT/'docs/reports/map/SERG_CLOSURE/PRUSSIAN_WEST_PHYSICAL_ANCHORS_2026_11_05'
    if (prussian_west/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((prussian_west/'REGISTRY_MIGRATION.json').read_text(encoding='utf8'))
        g=json.loads((prussian_west/'GEOMETRY.json').read_text(encoding='utf8'))
        assert m['replaced_regions']==['STATE_HANNOVER','STATE_WESTPHALIA']
        assert m['new_members']==m['free_cities']==m['extent_added_cells']==m['extent_removed_cells']==[]
        assert m['country_additions']=={} and m['new_provinces']==g['new_provinces']
        assert g['classification']=='B_POLITICAL_GENERALISATION' and g['ownership_cells']==32
        assert set(g['parents'])=={'x1BA4F6','x910095','xEDAC00'}
        old={r['rgb']:r for r in m['previous']};new={r['rgb']:r for r in m['updated']}
        assert all(new[k]==v for k,v in old.items()) and len(new)==len(old)+3
        assert {r['owner'] for r in g['assignments'] if r['owner']!=r['previous_owner']}=={'PRU'}
        result.append(prussian_west)
    magdeburg=ROOT/'docs/reports/map/SERG_CLOSURE/MAGDEBURG_HALBERSTADT_2026_11_05'
    if (magdeburg/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((magdeburg/'REGISTRY_MIGRATION.json').read_text(encoding='utf8'))
        g=json.loads((magdeburg/'GEOMETRY.json').read_text(encoding='utf8'))
        assert prussian_west in result
        assert m['replaced_regions']==['STATE_ANHALT']
        assert m['new_members']==m['free_cities']==m['extent_added_cells']==m['extent_removed_cells']==[]
        assert m['country_additions']=={} and m['new_provinces']==g['new_provinces']
        assert g['classification']=='B_POLITICAL_GENERALISATION' and g['ownership_cells']==77
        assert set(g['parents'])=={'x618061','xA080E0','xCF5D8E'}
        assert len(g['new_provinces'])==3 and sum(z['pixels'] for z in g['sub_lots'])==77
        assert all(z['previous_owner']=='PRU' and z['owner'] in {'PRU','SAX'} and z['state']=='STATE_ANHALT' for z in g['assignments'])
        old={z['rgb']:z for z in m['previous']};new={z['rgb']:z for z in m['updated']}
        assert all(new[k]==v for k,v in old.items()) and len(new)==len(old)+3
        assert {(z['rgb'],z['beneficiary']) for z in m['updated'] if z['rgb'] not in old}=={(z['rgb'],'SAX') for z in g['new_provinces']}
        result.append(magdeburg)
    gueldre=ROOT/'docs/reports/map/SERG_CLOSURE/CLEVE_GUELDRE_MARK_2026_11_05'
    if (gueldre/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((gueldre/'REGISTRY_MIGRATION.json').read_text(encoding='utf8'))
        g=json.loads((gueldre/'GEOMETRY.json').read_text(encoding='utf8'))
        assert magdeburg in result
        assert m['replaced_regions']==['STATE_GELRE']
        assert m['new_members']==m['free_cities']==m['extent_added_cells']==m['extent_removed_cells']==[]
        assert m['country_additions']=={} and m['new_provinces']==g['new_provinces']
        assert g['classification']=='B_POLITICAL_GENERALISATION' and g['ownership_cells']==72
        assert [(z['id'],z['pixels']) for z in g['sub_lots']]==[('PW-GUELDRE-B53',53),('PW-CLEVE-GUELDRE-NORTH-B19',19)]
        assert g['parents']==['x0000DF'] and g['new_provinces']==[{'rgb':'xEEC600','parent_rgb':'x0000DF'}]
        assert {(z['owner'],z['previous_owner'],z['state']) for z in g['assignments']}=={('BEO','BEO','STATE_GELRE'),('PRU','BEO','STATE_GELRE')}
        old={z['rgb']:z for z in m['previous']};new={z['rgb']:z for z in m['updated']}
        assert all(new[k]==v for k,v in old.items()) and len(new)==len(old)+1
        assert new['xEEC600']['beneficiary']=='PRU'
        result.append(gueldre)
    western_reserves=ROOT/'docs/reports/map/SERG_CLOSURE/WESTERN_RESERVES_ARBITRATION_2026_11_05'
    if (western_reserves/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((western_reserves/'REGISTRY_MIGRATION.json').read_text(encoding='utf8'))
        g=json.loads((western_reserves/'GEOMETRY.json').read_text(encoding='utf8'))
        assert gueldre in result
        assert m['replaced_regions']==['STATE_GELRE'] and m['previous']==m['updated']
        assert m['new_members']==m['free_cities']==m['extent_added_cells']==[] and m['country_additions']=={}
        assert m['dutch_sovereign_cores_excluded_from_BEO_restitution'] is True
        assert m['new_provinces']==g['new_provinces']==[{'rgb':'xEEC700','parent_rgb':'x0000DF'},{'rgb':'xEEC701','parent_rgb':'x0000DF'}]
        assert g['parents']==['x0000DF'] and g['classification']=='B_POLITICAL_GENERALISATION' and g['ownership_cells']==8
        assert [(z['id'],z['pixels']) for z in g['sub_lots']]==[('PW-VENLO-NET-B4',4),('PW-BEESEL-NET-B4',4)]
        removed=[c for z in g['sub_lots'] for c in z['cells']]
        assert sorted(m['extent_removed_cells'])==sorted(removed) and len({tuple(c) for c in removed})==8
        assert {(z['owner'],z['previous_owner'],z['state']) for z in g['assignments']}=={('BEO','BEO','STATE_GELRE'),('NET','BEO','STATE_GELRE')}
        assert not {'xEEC700','xEEC701'} & {z['rgb'] for z in m['updated']}
        result.append(western_reserves)
    bavaria=ROOT/'docs/reports/map/SERG_CLOSURE/BAVARIA_V1_2026_11_05'
    if (bavaria/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((bavaria/'REGISTRY_MIGRATION.json').read_text(encoding='utf-8'))
        g=json.loads((bavaria/'GEOMETRY.json').read_text(encoding='utf-8'))
        assert western_reserves in result
        assert m['replaced_regions']==['STATE_AUSTRIA']
        assert m['new_members']==m['free_cities']==m['new_provinces']==m['region_reference_changes']==m['extent_added_cells']==m['extent_removed_cells']==[]
        assert m['country_additions']=={} and m['bitmap_unchanged'] is True and m['ownership_cells']==175
        assert g['parents']==['xFDA6CB'] and g['new_provinces']==g['hub_rebindings']==[]
        assert g['classification']=='B_POLITICAL_GENERALISATION' and g['changed_pixels']==0 and g['ownership_cells']==175
        assert len(g['assignments'])==1
        r=g['assignments'][0]
        assert (r['rgb'],r['state'],r['previous_owner'],r['owner'],r['pixels'])==('xFDA6CB','STATE_AUSTRIA','AUS','BAV',175)
        assert len(r['cells'])==len({tuple(c) for c in r['cells']})==175
        old={r['rgb']:r for r in m['previous']};new={r['rgb']:r for r in m['updated']}
        assert set(old)==set(new) and old['xFDA6CB']['beneficiary']=='AUS' and new['xFDA6CB']['beneficiary']=='BAV'
        assert all(new[k]==v for k,v in old.items() if k!='xFDA6CB')
        assert old['xEDC000']==new['xEDC000'] and new['xEDC000']['beneficiary']=='PAS'
        result.append(bavaria)
    bavarian_upper=ROOT/'docs/reports/map/SERG_CLOSURE/BAVARIA_UPPER_PALATINATE_FRANCONIA_2026_11_05'
    if (bavarian_upper/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((bavarian_upper/'REGISTRY_MIGRATION.json').read_text(encoding='utf-8'))
        g=json.loads((bavarian_upper/'GEOMETRY.json').read_text(encoding='utf-8'))
        assert bavaria in result
        assert __import__('hashlib').sha256((bavarian_upper/'GEOMETRY.json').read_bytes()).hexdigest()=='5ea4518c7a683fa03369978a2ca570673ec516b45fb4f3bbcb229cb2e3c49f27'
        assert m['replaced_regions']==['STATE_BAVARIA']
        assert m['new_members']==m['free_cities']==m['extent_added_cells']==m['extent_removed_cells']==[]
        assert m['country_additions']=={} and m['new_provinces']==g['new_provinces']
        assert g['classification']=='B_POLITICAL_GENERALISATION' and not g['historical_cadastral_precision']
        assert g['ownership_cells']==156 and g['parents']==['x3101A0', 'x318021', 'x565185', 'x82F4B9', 'xA7094D', 'xFE59E7']
        assert all(r['previous_owner']=='BAV' and r['owner'] in {'BAV','KPF'} for r in g['assignments'])
        old={r['rgb']:r for r in m['previous']};new={r['rgb']:r for r in m['updated']}
        assert all(new[k]==v for k,v in old.items())
        assert set(new)-set(old)=={r['rgb'] for r in g['new_provinces']}
        assert {(r['rgb'],r['state'],r['beneficiary']) for r in m['updated'] if r['rgb'] not in old}=={(r['rgb'],r['state'],r['owner']) for r in g['assignments'] if r['rgb']!=r['parent_rgb']}
        result.append(bavarian_upper)
    return result

def provincial_membership_overrides():
    """Exact reviewed RGB exceptions, never a whole State Region inclusion."""
    return {(r['rgb'],r['state'],r['owner']) for m in approved_territorial_migrations() for r in m.get('province_membership_overrides',[])}

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
            elif tag=='HES':
                assert migration.get('new_members')==['NOU','NWB'] and migration.get('replaced_regions')==['STATE_HESSE']
                assert change['before']=='grand_principality' and change['after']=='principality'
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
