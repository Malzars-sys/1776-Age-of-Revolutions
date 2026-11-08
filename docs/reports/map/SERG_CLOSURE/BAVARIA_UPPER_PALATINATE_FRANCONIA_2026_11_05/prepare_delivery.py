"""Prepare the authorized Bavarian political B lot; no runtime write here."""
from pathlib import Path
import sys,json,hashlib,collections as C,re,difflib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
OUT=Path(__file__).resolve().parent
ROOT=next(p for p in OUT.parents if (p/'AGENTS.md').exists())
sys.path.insert(0,str(ROOT/'tools'))
import validate_diplomacy_ottoman_1776 as cw
from map2a_patch import edits
from map2b_patch import state,region,append
from map_1776_audit import values
from map2l_belgium import packed,components,allocate
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(n,v):
 p=OUT/n
 if p.exists():
  assert json.loads(p.read_text(encoding='utf-8'))==v,n
  return
 p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
def inside(q,poly):
 h=np.zeros(len(q),bool);xx,yy=q.T
 for i in range(len(poly)):
  ax,ay=poly[i-1];bx,by=poly[i]
  h^=((ay>yy)!=(by>yy))&(xx<(bx-ax)*(yy-ay)/(by-ay+1e-100)+ax)
 return h
b=json.loads((OUT/'BASELINE.json').read_text());inv=json.loads((OUT/'INVENTORY_BEFORE.json').read_text());cfg=json.loads((OUT/'TRACING_REVIEWED.json').read_text())
for rel,h in b['runtime_hashes'].items():assert sha(ROOT/rel)==h,rel
bmp=packed(ROOT/'map_data/provinces.png')
(OUT/'provinces_before.png').write_bytes((ROOT/'map_data/provinces.png').read_bytes())
own={r['key'][0]:(r['key'][1],r['key'][2]) for r in inv['owners']}
T=np.array(cfg['matrix_source_to_game'])
x0,y0,x1,y1=4325,855,4395,912;yy,xx=np.mgrid[y0:y1,x0:x1];xy=np.column_stack((xx.ravel()+.5,yy.ravel()+.5));src=(xy-T[2])@np.linalg.inv(T[:2]);flat=bmp[y0:y1,x0:x1].ravel()
valid=np.array([own.get('x'+format(int(v),'06X')) in [('STATE_BAVARIA','BAV'),('STATE_FRANCONIA','BAV')] for v in flat]);used=np.zeros(len(flat),bool);lots=C.defaultdict(list);diagnostics=[]
for p in cfg['polygons']:
 m=inside(src,p['points'])
 for hole in p.get('holes',[]):m&=~inside(src,hole)
 diagnostics.append(dict(label=p['label'],eligible=int((m&valid&~used).sum()),protected_or_outside=int((m&~valid).sum())))
 m&=valid&~used;used|=m
 lots[p['id']].extend((xy[m]-.5).astype(int).tolist())
# Source-to-game checks are diagnostics. Do not make a transfer out of a
# protected core merely to force an office to appear at the fitted point.
lots={k:v for k,v in lots.items() if v}
selected={tuple(q):k for k,v in lots.items() for q in v};parents=sorted({'x'+format(int(bmp[y,x]),'06X') for x,y in selected})
candidate=bmp.copy();allcolors=set(map(int,np.unique(bmp)));idx=0xEEC800;assign=[];new=[]
for parent in parents:
 sid,tag=own[parent];assert tag=='BAV'
 local=bmp==int(parent[1:],16);zones=np.zeros(bmp.shape,dtype=np.uint8)
 for zone,(k,cells) in enumerate(lots.items(),1):
  for x,y in cells:
   if local[y,x]:zones[y,x]=zone
 groups=[]
 for zone in sorted(set(map(int,zones[local]))):
  for part in components(local&(zones==zone)):
   groups.append(dict(owner='BAV' if zone==0 else 'KPF',sub_lot=None if zone==0 else list(lots)[zone-1],cells=[[x,y] for y,x in part],pixels=len(part)))
 retained=[g for g in groups if g['owner']=='BAV'];assert retained,parent
 keep=max(retained,key=lambda g:g['pixels'])
 for g in groups:
  rgb=parent
  if g is not keep:
   while idx in allcolors:idx+=1
   rgb='x'+format(idx,'06X');idx+=1;allcolors.add(int(rgb[1:],16));new.append(dict(rgb=rgb,parent_rgb=parent))
  for x,y in g['cells']:candidate[y,x]=int(rgb[1:],16)
  assign.append(dict(rgb=rgb,parent_rgb=parent,state=sid,previous_owner='BAV',**g))
Image.fromarray(np.stack(((candidate>>16)&255,(candidate>>8)&255,candidate&255),axis=2).astype(np.uint8)).save(OUT/'provinces_candidate.png')
g=dict(classification='B_POLITICAL_GENERALISATION',historical_cadastral_precision=False,parents=parents,assignments=assign,new_provinces=new,hub_rebindings=[],ownership_cells=len(selected),changed_pixels=int((bmp!=candidate).sum()),candidate_sha256=sha(OUT/'provinces_candidate.png'),sub_lots=[dict(id=k,pixels=len(v),cells=v,status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',attestation=None) for k,v in lots.items()],source_diagnostics=diagnostics,source_tracing_sha256=sha(OUT/'TRACING_REVIEWED.json'))
before={};files={}
def read(rel):
 raw=(ROOT/rel).read_bytes().decode('utf-8');assert sha(ROOT/rel)==b['runtime_hashes'].get(rel,sha(ROOT/rel)),rel
 before[rel]=raw;return raw
sids=sorted({r['state'] for r in assign})
rel='common/history/states/00_states.txt';raw=read(rel)
for sid in sids:
 node=state(raw,sid);s=next(z for z in node.children('create_state') if cw.scalar(z.one('country'))=='c:BAV');f=s.children('owned_provinces')[0]
 bav_extra=[r['rgb'] for r in assign if r['state']==sid and r['owner']=='BAV' and r['rgb']!=r['parent_rgb']]
 raw=edits(raw,[(f.end-1,f.end-1,' '+' '.join(bav_extra)+' ')]) if bav_extra else raw
 node=state(raw,sid);assert not [z for z in node.children('create_state') if cw.scalar(z.one('country'))=='c:KPF']
 children=[r['rgb'] for r in assign if r['state']==sid and r['owner']=='KPF']
 raw=edits(raw,[(node.end-1,node.end-1,'\n\t\t# Bavarian V1: Pfalz-Neuburg/Sulzbach political B cores, distinct sovereign in 1776.\n\t\tcreate_state = { country = c:KPF owned_provinces = { '+' '.join(children)+' } }\n\t')])
files[rel]=raw
rel='map_data/state_regions/00_west_europe.txt';raw=read(rel)
import map2m_r9 as loc
locs=loc.locators(bmp)
for sid in sids:
 n=next(n for n in cw.parse(raw) if n.key==sid);f=n.children('provinces')[0]
 extra=[r['rgb'] for r in new if own[r['parent_rgb']][0]==sid];ops=[(f.end-1,f.end-1,' '+' '.join('"'+z+'"' for z in extra)+' ')]
 for kind in ['city','port','farm','wood','mine']:
  if not n.children(kind):continue
  f=n.children(kind)[0];parent=cw.scalar(f.value)
  if parent not in parents:continue
  row=next(z for z in locs if z['Kind']==kind and z['ID']==int(n.one('id')))
  x,y=row['X'],row['Y'];assert int(bmp[int(y),int(x)])==int(parent[1:],16)
  actual='x'+format(int(candidate[int(y),int(x)]),'06X')
  if actual!=parent:
   ops.append((f.start,f.end,kind+' = "'+actual+'"'))
   g['hub_rebindings'].append(dict(state=sid,field=kind,before=parent,after=actual,point=[x,y],pixel=[int(x),int(y)],locator_moved=False))
 for f in n.children('prime_land'):
  old=values(n,'prime_land');added=[r['rgb'] for r in new if r['parent_rgb'] in old]
  if added:
   ops.append((f.end-1,f.end-1,' '+' '.join('"'+z+'"' for z in added)+' '))
   g['hub_rebindings'].append(dict(state=sid,field='prime_land',before=old,after=old+added))
 raw=edits(raw,ops)
files[rel]=raw
weights={};allocations=[]
for sid in sids:
 total=sum(int((bmp==int(z[1:],16)).sum()) for z,(s,t) in own.items() if s==sid and t=='BAV')
 moved=sum(z['pixels'] for z in assign if z['state']==sid and z['owner']=='KPF');assert 0<moved<total
 weights[sid]={'BAV':total-moved,'KPF':moved}
for path in (ROOT/'common/history/pops').glob('*.txt'):
 original=path.read_bytes().decode('utf-8')
 if not any('s:'+sid in original for sid in sids):continue
 rel=path.relative_to(ROOT).as_posix();original=read(rel);ops=[];pieces=C.defaultdict(list)
 for sid in sids:
  try:n=region(original,sid,'BAV')
  except StopIteration:continue
  for pop in n.children('create_pop'):
   f=pop.children('size')[0];count=int(f.value);amounts=allocate(count,weights[sid]);frag=original[pop.start:pop.end]
   ops.append((f.start,f.end,'size = '+str(amounts['BAV'])))
   if amounts['KPF']:pieces[sid].append(edits(frag,[(f.start-pop.start,f.end-pop.start,'size = '+str(amounts['KPF']))]))
   allocations.append(dict(state=sid,culture=pop.one('culture'),religion=pop.one('religion','DEFAULT'),before=count,after=amounts))
 raw=edits(original,ops)
 for sid,pieces0 in pieces.items():raw=append(raw,sid,'KPF','\n'.join(pieces0))
 if raw!=original:files[rel]=raw
rel='map_data/province_terrains.txt';raw=read(rel);terrains={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',raw)}
files[rel]=raw+'\n'+'\n'.join(r['rgb']+' = "'+terrains[r['parent_rgb'].upper()]+'"' for r in new)+'\n'
rel='docs/reports/map/MAP2L/IMPERIAL_DE_JURE_REGISTRY.json';ledger=json.loads(read(rel));dump('REGISTRY_BEFORE.json',ledger)
previous=[r for r in ledger if r['state'] in sids];updated=list(previous)
for row in new:
 a=next(z for z in assign if z['rgb']==row['rgb'])
 updated.append(dict(rgb=a['rgb'],state=a['state'],beneficiary=a['owner'],basis='Bavaria V1 Upper Palatinate/Neuburg political B cores. Offices attested before1776; source Spindler/Diepolder1789 confronted with Homann1730. Not exact cadastre; see BAVARIA_UPPER_PALATINATE_FRANCONIA_2026_11_05/REPORT.md'))
newledger=sorted([r for r in ledger if r['state'] not in sids]+updated,key=lambda r:(r['rgb'],r['state'],r['beneficiary']))
files[rel]=json.dumps(newledger,ensure_ascii=False,indent=2)+'\n'
migration=dict(replaced_regions=sids,previous=previous,updated=updated,new_members=[],free_cities=[],country_additions={},new_provinces=new,region_reference_changes=g['hub_rebindings'],extent_added_cells=[],extent_removed_cells=[],ownership_cells=len(selected))
dump('GEOMETRY.json',g);dump('REGISTRY_MIGRATION.json',migration)
rel='tools/map2l_registry.py';raw=read(rel);anchor='    return result\n\ndef provincial_membership_overrides'
if '\r\n' in raw:anchor=anchor.replace('\n','\r\n')
assert raw.count(anchor)==1
guard="""    bavarian_upper=ROOT/'docs/reports/map/SERG_CLOSURE/BAVARIA_UPPER_PALATINATE_FRANCONIA_2026_11_05'
    if (bavarian_upper/'REGISTRY_MIGRATION.json').exists():
        m=json.loads((bavarian_upper/'REGISTRY_MIGRATION.json').read_text(encoding='utf-8'))
        g=json.loads((bavarian_upper/'GEOMETRY.json').read_text(encoding='utf-8'))
        assert bavaria in result
        assert __import__('hashlib').sha256((bavarian_upper/'GEOMETRY.json').read_bytes()).hexdigest()==GEOMETRY_HASH
        assert m['replaced_regions']==REGIONS_LITERAL
        assert m['new_members']==m['free_cities']==m['extent_added_cells']==m['extent_removed_cells']==[]
        assert m['country_additions']=={} and m['new_provinces']==g['new_provinces']
        assert g['classification']=='B_POLITICAL_GENERALISATION' and not g['historical_cadastral_precision']
        assert g['ownership_cells']==CELL_COUNT and g['parents']==PARENTS_LITERAL
        assert all(r['previous_owner']=='BAV' and r['owner'] in {'BAV','KPF'} for r in g['assignments'])
        old={r['rgb']:r for r in m['previous']};new={r['rgb']:r for r in m['updated']}
        assert all(new[k]==v for k,v in old.items())
        assert set(new)-set(old)=={r['rgb'] for r in g['new_provinces']}
        assert {(r['rgb'],r['state'],r['beneficiary']) for r in m['updated'] if r['rgb'] not in old}=={(r['rgb'],r['state'],r['owner']) for r in g['assignments'] if r['rgb']!=r['parent_rgb']}
        result.append(bavarian_upper)
"""
guard=guard.replace('GEOMETRY_HASH',repr(sha(OUT/'GEOMETRY.json'))).replace('REGIONS_LITERAL',repr(sids)).replace('CELL_COUNT',str(len(selected))).replace('PARENTS_LITERAL',repr(parents))
if '\r\n' in raw:guard=guard.replace('\n','\r\n')
files[rel]=raw.replace(anchor,guard+anchor)
for rel,raw in list(files.items()):
 old=before[rel]
 if '\r\n' in old and old.count('\n')==old.count('\r\n'):raw=raw.replace('\r\n','\n').replace('\n','\r\n')
 # Remove whitespace on newly inserted blank lines only.
 oldlines=old.splitlines(True);newlines=raw.splitlines(True);parts=[]
 for op,i,j,k,l in difflib.SequenceMatcher(None,oldlines,newlines,autojunk=False).get_opcodes():
  lines=newlines[k:l]
  if op!='equal':lines=[v if v.strip() else ('\r\n' if v.endswith('\r\n') else '\n') for v in lines]
  parts.extend(lines)
 files[rel]=''.join(parts)
 if rel.endswith('.txt'):cw.parse(files[rel].lstrip('\ufeff'))
dump('TEXT_BEFORE.json',before);dump('EXPECTED_TEXT.json',files)
dump('PLAN.json',dict(files=sorted(files),sub_lots=g['sub_lots'],population_allocations=allocations,weights_by_state=weights,moved_population=sum(x['after']['KPF'] for x in allocations),population_method='Provisional exact-integer technical redistribution of existing profiles; NOT a historical census; no demographic closure claimed.',registered_titles_before=len(ledger),registered_titles_after=len(newledger),buildings_units_technologies_unchanged=True,no_human_validation=True))
# Review panels are data visualisations, not game screenshots.
colors={'BAV':(195,195,195),'KPF':(70,130,220),'ANS':(235,160,70),'EIC':(85,175,145),'FBM':(85,155,210),'NUR':(205,75,75),'AUS':(235,220,190)}
afterown=own|{z['rgb']:(z['state'],z['owner']) for z in assign};panels=[]
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
for label,im0,oo in [('AVANT',bmp,own),('APRES - CANDIDAT',candidate,afterown)]:
 local=im0[y0:y1,x0:x1];rgb=np.full((*local.shape,3),225,dtype=np.uint8)
 for v in np.unique(local):rgb[local==v]=colors.get(oo.get('x'+format(int(v),'06X'),('','?'))[1],(220,200,220))
 edge=np.zeros(local.shape,bool);edge[:,1:]|=local[:,1:]!=local[:,:-1];edge[1:]|=local[1:]!=local[:-1];rgb[edge]=45
 image=Image.fromarray(rgb).resize((840,684),Image.Resampling.NEAREST);panel=Image.new('RGB',(840,735),'white');panel.paste(image,(0,35));draw=ImageDraw.Draw(panel);draw.text((8,5),label+' | Gris BAV / Bleu KPF / Vert EIC',fill='black',font=font);panels.append(panel)
im=Image.new('RGB',(1680,735),'white');im.paste(panels[0]);im.paste(panels[1],(840,0));im.save(OUT/'BEFORE_AFTER_CANDIDATE.png')
print('PREPARED',len(selected),'ownership cells',len(new),'new RGB',len(files),'text files','pops',sum(x['after']['KPF'] for x in allocations),'titles',len(newledger),'hubs',g['hub_rebindings'])
print('SUBLOTS',[(k,len(v)) for k,v in lots.items()]);print('DIAGNOSTICS',diagnostics)
