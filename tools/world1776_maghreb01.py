"""Bounded political cores of Spanish presidios, 1776; no flavour additions.

Four shared files, four existing land pixels, three new RGBs. No new land,
countries, POPs, buildings, technologies, units, Git or vanilla writes.
"""
import argparse,io,json,shutil
from collections import Counter
from PIL import Image,ImageDraw
import numpy as np
import world1776_balkans03 as b
import world1776_balkans04 as b4

ROOT=b.ROOT;OUT=b.OUT;LOT=OUT/'MAGHREB-01'
ST='common/history/states/00_states.txt';REG='map_data/state_regions/03_north_africa.txt'
TER='map_data/province_terrains.txt';BMP='map_data/provinces.png';EDIT=[ST,REG,TER,BMP]
PLAN=[{'name':'Ceuta','state':'STATE_AL_RIF','parent':'xA0B0C0','rgb':'xE8D231','pixels':[[3973,1252]],'old_owners':['MOR','SPA']},
      {'name':'Melilla','state':'STATE_AL_RIF','parent':'xCA9F75','rgb':'xE8D232','pixels':[[4029,1264]],'old_owners':['MOR','SPA']},
      {'name':'Oran–Mers el-Kebir','state':'STATE_ORAN','parent':'xB735DB','rgb':'xE8D233','pixels':[[4081,1255],[4082,1255]],'old_owners':['MAS']}]
def rgb(k):return tuple(bytes.fromhex(k[1:]))
def load(n):return json.loads((LOT/n).read_text('utf8'))
def dump(n,v):(LOT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def transform(old):
    text=old[ST];ops=[];rif=b.one(text,'s:STATE_AL_RIF')
    spa=next(n for n in rif.children('create_state') if n.one('country')=='c:SPA');owned=spa.children('owned_provinces')[0]
    assert b.a.ids(spa,'owned_provinces')==['xCA9F75','xA0B0C0']
    # Old large polygons remain Moroccan; only the minimum coastal cores are Spanish.
    ops.append((owned.start,owned.end,'owned_provinces = { xE8D231 xE8D232 }'))
    oran=b.one(text,'s:STATE_ORAN');assert not any(n.one('country')=='c:SPA' for n in oran.children('create_state'))
    ops.append((oran.end-1,oran.end-1,'\n\t\t# Spanish fortified coastal core, not the whole Oranais.\n\t\tcreate_state = { country = c:SPA owned_provinces = { xE8D233 } state_type = unincorporated }\n\t'))
    result={ST:b.edits(text,ops)}
    text=old[REG];ops=[]
    for sid in ['STATE_AL_RIF','STATE_ORAN']:
        n=b.one(text,sid);ps=n.children('provinces')[0];added=' '.join('"'+p['rgb']+'"' for p in PLAN if p['state']==sid)
        ops.append((ps.end-1,ps.end-1,' '+added+' '))
    result[REG]=b.edits(text,ops)
    terrain={n.key:n.value for n in b.parse(old[TER])}
    result[TER]=old[TER].rstrip()+'\n\n# MAGHREB-01: terrain inherited from existing coastal parents.\n'+''.join(p['rgb']+' = '+terrain[p['parent']]+'\n' for p in PLAN)
    return result
def apply():
    assert not (LOT/'FILES_MODIFIED.json').exists(),'Already installed; --validate only.'
    originals={r:b.a.raw(ROOT/r) for r in [ST,REG,TER]};updated=transform(originals)
    current={r:b.a.sha(ROOT/r) for r in EDIT}
    for r in EDIT:
        p=LOT/'apply_inputs'/r;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/r,p)
    before=b4.inventory();dump('APPLY_BEFORE.json',before)
    image=Image.open(ROOT/BMP).convert('RGB');arr=np.asarray(image)
    for p in PLAN:
        assert not np.any(np.all(arr==rgb(p['rgb']),axis=2)),p['rgb']+' already exists'
        for xy in p['pixels']:assert image.getpixel(tuple(xy))==rgb(p['parent']);image.putpixel(tuple(xy),rgb(p['rgb']))
    buffer=io.BytesIO();image.save(buffer,format='PNG')
    assert all(b.a.sha(ROOT/r)==h for r,h in current.items()),'Shared files changed; reread.'
    for r,t in updated.items():
        bom=b'\xef\xbb\xbf' if (ROOT/r).read_bytes().startswith(b'\xef\xbb\xbf') else b''
        (ROOT/r).write_bytes(bom+t.encode('utf8'))
    (ROOT/BMP).write_bytes(buffer.getvalue())
    dump('FILES_MODIFIED.json',[{'file':r,'before':current[r],'after':b.a.sha(ROOT/r)} for r in EDIT])
    dump('PIXEL_PATCH.json',PLAN);print('Installed: small Ceuta/Melilla cores, duplicate claims resolved, Oran coastal Spanish core; no flavour.')
def validate():
    base=load('BASELINE.json');before=load('APPLY_BEFORE.json');checks=[]
    def ck(k,v,d=None):checks.append({'check':k,'passed':bool(v),'detail':d})
    originals={r:b.a.raw(LOT/'apply_inputs'/r) for r in [ST,REG,TER]}
    for r,t in transform(originals).items():ck('exact_targeted_text.'+r,b.a.raw(ROOT/r)==t)
    old=np.asarray(Image.open(LOT/'apply_inputs'/BMP).convert('RGB'));now=np.asarray(Image.open(ROOT/BMP).convert('RGB'))
    ys,xs=np.where(np.any(old!=now,axis=2));expected={tuple(xy) for p in PLAN for xy in p['pixels']}
    ck('four_exact_land_pixels',set(zip(xs.tolist(),ys.tolist()))==expected and len(xs)==4)
    ck('dimensions_unchanged',old.shape==now.shape==(3616,8192,3))
    current=b4.inventory();owners=current['owners'];expected_owners=dict(before['owners'])
    for c in ['xA0B0C0','xCA9F75']:expected_owners[c]=[['STATE_AL_RIF','MOR']]
    for p in PLAN:expected_owners[p['rgb']]=[[p['state'],'SPA']]
    ck('only_declared_owner_changes',owners==expected_owners)
    for p in PLAN:
        ck('new_owner.'+p['name'],owners[p['rgb']]==[[p['state'],'SPA']])
        ck('old_color_and_land.'+p['name'],all(tuple(old[y,x])==rgb(p['parent']) for x,y in p['pixels']) and p['parent'] in before['owners'])
        ck('new_color.'+p['name'],all(tuple(now[y,x])==rgb(p['rgb']) for x,y in p['pixels']))
        ck('exact_new_RGB_area.'+p['name'],np.count_nonzero(np.all(now==rgb(p['rgb']),axis=2))==len(p['pixels']))
        # Sea pixels are those without an initial land owner, independent of visual blue.
        coastal=False
        for x,y in p['pixels']:
            for nx,ny in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                if 'x'+''.join(f'{v:02X}' for v in old[ny,nx]) not in before['owners']:coastal=True
        ck('existing_coastal_core.'+p['name'],coastal)
    ck('Oran_hinterland_MAS',owners['xB735DB']==[['STATE_ORAN','MAS']] and np.count_nonzero(np.all(now==rgb('xB735DB'),axis=2))>2)
    ck('Rif_large_polygons_MOR',all(owners[p]==[['STATE_AL_RIF','MOR']] for p in ['xA0B0C0','xCA9F75']))
    for key in ['world_population','git']:ck('unchanged.'+key,current[key]==before[key])
    # Ignore neither new failures nor other inherited duplicate assignments (e.g. Tripoli).
    initial_dups={r for r,v in before['owners'].items() if len(v)>1};after_dups={r for r,v in owners.items() if len(v)>1}
    ck('exact_two_duplicate_assignments_removed',after_dups==initial_dups-{'xA0B0C0','xCA9F75'},sorted(after_dups))
    for rel,keys in [(ST,['s:STATE_AL_RIF','s:STATE_ORAN']),(REG,['STATE_AL_RIF','STATE_ORAN'])]:
        def outside(text):
            nodes=[b.one(text,k) for k in keys]
            return b.edits(text,[(n.start,n.end,'<SCOPED_REGION>') for n in nodes])
        ck('all_other_states_byte_identical.'+rel,outside(originals[rel])==outside(b.a.raw(ROOT/rel)))
    for rel in ['map_data/heightmap.png','map_data/packed_heightmap.png','common/history/pops/05_north_america.txt']:
        ck('protected.'+rel,b.a.sha(ROOT/rel)==base['gameplay'][rel])
    changes={}
    for key in ['gameplay','SERG_proofs','prior_WORLD_proofs']:
        delta=[{'file':r,'before':h,'after':b.a.sha(ROOT/r) if (ROOT/r).exists() else None} for r,h in base[key].items() if r not in EDIT and (not (ROOT/r).exists() or b.a.sha(ROOT/r)!=h)]
        changes[key]=delta;ck('all_prior_'+key+'_preserved',not delta,delta)
    ck('B07_Elaphites_preserved',tuple(now[1065,4503])==rgb('xE8D201'))
    dump('CONCURRENT_CHANGES.json',{'differences_outside_scope':changes,'Git_writes':0,'SERG_writes':0,'vanilla_writes':0})
    dump('POPULATION_LEDGER.json',{'world_before':before['world_population'],'world_after':current['world_population'],'delta':current['world_population']-before['world_population'],'POP_files_written':0,'historical_distribution_reestimated':False,'new_SPA_Oran_portion_population_not_initialized_by_this_map_only_lot':True})
    passed=sum(c['passed'] for c in checks);dump('VALIDATION.json',{'status':'PASS' if passed==len(checks) else 'FAIL','passed':passed,'total':len(checks),'checks':checks,'runtime':'NOT_RUN','human_validation':False})
    print(json.dumps({'passed':passed,'total':len(checks),'failed':[c['check'] for c in checks if not c['passed']]}));return passed==len(checks)
def render():
    old=Image.open(LOT/'apply_inputs'/BMP).convert('RGB');now=Image.open(ROOT/BMP).convert('RGB')
    inv=load('APPLY_BEFORE.json')['owners'];col={'SPA':(190,160,45),'MOR':(155,62,50),'MAS':(76,132,103)}
    rows=[]
    for p in PLAN:
        x,y=p['pixels'][0];box=(x-6,y-5,x+7,y+6)
        panels=[]
        for src,after in [(old,False),(now,True)]:
            crop=src.crop(box);d=ImageDraw.Draw(crop)
            for yy in range(crop.height):
                for xx in range(crop.width):
                    k='x'+''.join(f'{v:02X}' for v in crop.getpixel((xx,yy)))
                    owner='SPA' if after and k in [r['rgb'] for r in PLAN] else inv.get(k,[[None,None]])[-1][1]
                    if after and k in ['xA0B0C0','xCA9F75']:owner='MOR'
                    d.point((xx,yy),fill=col.get(owner,(40,65,83)))
            panels.append(crop.resize((260,220),Image.Resampling.NEAREST))
        rows.append((p['name'],panels))
    image=Image.new('RGB',(580,780),(25,31,38));d=ImageDraw.Draw(image)
    for i,(name,panels) in enumerate(rows):
        y=i*260;d.text((10,y+5),name.replace('–','-')+' | Avant / Apres',fill='white');image.paste(panels[0],(10,y+25));image.paste(panels[1],(300,y+25))
    d.text((10,765),'Jaune : Espagne | Rouge : Maroc | Vert : MAS | Bleu : mer',fill='white')
    image.save(LOT/'COASTAL_BEFORE_AFTER.png')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true');p.add_argument('--validate',action='store_true');p.add_argument('--render',action='store_true');args=p.parse_args()
    if args.apply:apply()
    if args.validate:raise SystemExit(0 if validate() else 1)
    if args.render:render()
