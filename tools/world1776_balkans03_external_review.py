"""Read and reconcile the concurrent Ortenburg patch; write WORLD evidence only."""
import hashlib
import json
import shutil
import numpy as np
from PIL import Image
import world1776_balkans03 as b


def main():
    base=json.loads((b.LOT/'BASELINE.json').read_text('utf8'))
    peer=b.ROOT/'docs/reports/map/SERG_CLOSURE/SC1-ORTENBURG'
    before=json.loads((peer/'TEXT_BEFORE.json').read_text('utf8'))
    expected=json.loads((peer/'EXPECTED_TEXT.json').read_text('utf8'))
    changed={r:{'before':h,'after':b.a.sha(b.ROOT/r)} for r,h in base['protected'].items() if b.a.sha(b.ROOT/r)!=h}
    allowed={'common/history/states/00_states.txt','common/history/pops/00_west_europe.txt',
             'map_data/state_regions/00_west_europe.txt','map_data/province_terrains.txt','map_data/provinces.png'}
    assert allowed<=set(changed),changed
    # Other agents also edit unrelated imperial gameplay. Observe those files,
    # without validating their mechanics or treating them as our writes.
    b.dump('EXTERNAL_GAMEPLAY_OBSERVATIONS.json',{'date':'2026-10-25','files':changed,
        'territorial_peer_files':sorted(allowed),'unrelated_changes_not_validated':sorted(set(changed)-allowed),
        'own_functional_write_set':b.OWN+base['new'],'scope_collision':False})
    changed={r:e for r,e in changed.items() if r in allowed}
    checks={}
    for r in allowed-{'map_data/provinces.png'}:
        text=before[r]
        # The source JSON preserves the raw text; confirm exact B03 entry bytes.
        matches=changed[r]['before'] in [hashlib.sha256(prefix+text.encode('utf8')).hexdigest() for prefix in [b'',b'\xef\xbb\xbf']]
        checks['peer_preimage_matches_B03_entry.'+r]=matches
        checks['peer_expected_matches_current.'+r]=expected[r].lstrip('\ufeff')==b.a.raw(b.ROOT/r)
    bmp=peer/'provinces_before.png';checks['peer_bitmap_matches_B03_entry']=b.a.sha(bmp)==changed['map_data/provinces.png']['before']
    old=np.array(Image.open(bmp).convert('RGB'));now=np.array(Image.open(b.ROOT/'map_data/provinces.png').convert('RGB'))
    yy,xx=np.where(np.any(old!=now,axis=2));cells=set(zip(map(int,xx),map(int,yy)))
    checks['only_four_Ortenburg_pixels_changed']=cells=={(4392,901),(4392,902),(4393,901),(4393,902)}
    checks['pixel_parent_and_successor_match']=all(tuple(old[y,x])==(140,38,221) and tuple(now[y,x])==(237,193,0) for x,y in cells)
    r='common/history/states/00_states.txt'
    def exterior(t):
        n=b.one(t,'s:STATE_BAVARIA');return t[:n.start]+'<BAVARIA>'+t[n.end:]
    checks['all_states_outside_Bavaria_unchanged']=exterior(before[r])==exterior(expected[r])
    inv=b.inventory();owners=dict(base['before']['owners']);owners['xEDC100']=[['STATE_BAVARIA','ORT']]
    checks['only_Ortenburg_owner_added']=inv['owners']==owners
    checks['world_population_conserved']=inv['world_population']==base['before']['world_population']
    checks['MON_POPs_unchanged']=json.loads(json.dumps(inv['pops']))==base['before']['pops']
    assert all(checks.values()),{k:v for k,v in checks.items() if not v}
    archived={}
    for name in ['TEXT_BEFORE.json','EXPECTED_TEXT.json','GEOMETRY.json','DEMOGRAPHY.json']:
        dest=b.LOT/'external_snapshots/Ortenburg'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(peer/name,dest)
        archived[dest.relative_to(b.LOT).as_posix()]=b.a.sha(dest)
    b.dump('EXTERNAL_ORTENBURG_UPDATE.json',{'date':'2026-10-25','source':peer.relative_to(b.ROOT).as_posix(),
        'verified':True,'checks':checks,'files':changed,'archived_evidence':archived,
        'owner_additions':{'xEDC100':[['STATE_BAVARIA','ORT']]},'pixels_external':4,'WORLD_pixels_modified':0,
        'population_external_transfer':1000,'population_world_delta':0,'WORLD_criteria_awarded':0,
        'external_mechanics_and_historical_claims_validated_here':False})
    # Append a new observation without destroying the first SERG receipt.
    path=b.LOT/'EXTERNAL_SERG_UPDATE.json';record=json.loads(path.read_text('utf8'))
    changed_serg={r:{'before':h,'after':b.a.sha(b.ROOT/r)} for r,h in base['serg'].items() if b.a.sha(b.ROOT/r)!=h}
    if record['files']!=changed_serg:
        dest=b.LOT/'EXTERNAL_SERG_UPDATE_FIRST_OBSERVATION.json'
        if not dest.exists():shutil.copy2(path,dest)
        record['files']=changed_serg;record['further_observation']='Concurrent Ortenburg work after the scoped Regensburg receipt; no WORLD validation or SERG writes by B03.'
        for r in changed_serg:
            dest=b.LOT/'external_snapshots'/r;shutil.copy2(b.ROOT/r,dest)
        b.dump('EXTERNAL_SERG_UPDATE.json',record)
    print('Verified external patch: four Ortenburg pixels, five shared files, no Balkan or world-population change.')

if __name__=='__main__':main()
