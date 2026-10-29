"""Guarded repairs found by DP-02's first audit; preserve initial receipts."""
from dp02_refine import *

def repair():
 assert not (OUT/'REPAIR_01.json').exists()
 manifest=load('APPLIED.json');rows={z['file']:z for z in manifest['files']};patches={}
 rel='common/history/characters/gar - garwhal.txt'
 patches[rel]='CHARACTERS = { } # Lalit Shah is already initialized by cleanup2c1 - non europe rulers 1776.txt.\n'
 for rel in BUILD:
  raw=text(ROOT/rel);p=[]
  for s in state_nodes(raw).values():
   if s.key!='s:STATE_PUNJAB':continue
   for country in s.children('region_state:BHW'):
    for b in country.children('create_building'):
     if scalar(b.one('building'))!='building_trade_center':continue
     for q in b.children('activate_production_methods'):
      body=raw[q.start:q.end]
      if 'pm_trade_center_trade_quantity_normal' in body:p.append((q.start,q.end,body.replace('pm_trade_center_trade_quantity_normal','pm_trade_center_trade_quantity_limited')))
  if p:patches[rel]=edit(raw,p)
 assert len(patches)==3
 data=[]
 for rel,s in patches.items():
  p=ROOT/rel;assert sha(p)==rows[rel]['after_sha256'],('Concurrent edit',rel)
  b=encoded(p,s);parse(s);data.append((rel,p.read_bytes(),b))
 receipt=[]
 for rel,old,new in data:
  p=OUT/'repair_preimages'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(old)
  (ROOT/rel).write_bytes(new);receipt.append(dict(file=rel,before_sha256=rows[rel]['after_sha256'],after_sha256=sha(ROOT/rel)))
  rows[rel]['after_sha256']=sha(ROOT/rel)
 dump('REPAIR_01.json',dict(reason='BHW inherited trade quantity requires a later finance technology; use the existing limited trade PM without deleting facilities. GAR already has Lalit Shah in the shared cleanup; suppress duplicate ruler declaration.',files=receipt))
 dump('CURRENT_RUNTIME_MANIFEST.json',dict(files=list(rows.values()),status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',runtime_validated=False))
 print('Three bounded repairs applied; initial manifest and preimages retained.')
if __name__=='__main__':repair()
