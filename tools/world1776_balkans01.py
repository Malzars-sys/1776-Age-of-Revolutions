"""BALKANS-01: scoped history patch and static receipts; no SERG/vanilla/Git writes.

Use --apply once, then --validate. Default is a current read-only inventory.
Regional documents are leads; the dated historical decision lives in SOURCES.md.
"""
from pathlib import Path
from collections import defaultdict
from copy import deepcopy
import argparse
import csv
import hashlib
import json
import re
import shutil

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import audit_anzin_regional_infrastructure as a
import audit_starting_tech_1776 as tech
import map_1776_audit as geography
from validate_diplomacy_ottoman_1776 import parse, walk, scalar, normalized

ROOT=a.ROOT
OUT=ROOT/'docs/reports/map/WORLD_1776_CLOSURE'
LOT=OUT/'BALKANS-01'
SID='STATE_WEST_AEGEAN_ISLANDS'
CELLS={'x6090A0','x6960A0'}
STATE='common/history/states/00_states.txt'
POPS='common/history/pops/01_south_europe.txt'
BUILD='common/history/buildings/01_south_europe.txt'
COUNTRIES=[f'common/history/countries/{tag} - {name}.txt' for tag,name in [('mol','moldavia'),('wal','wallachia')]]
OWN=[STATE,POPS,BUILD]+COUNTRIES


def dump(name,obj):
    (LOT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def state_node(raw,sid=SID):
    found=[n for n in walk(parse(raw)) if n.key=='s:'+sid]
    assert len(found)==1,(sid,len(found))
    return found[0]


def edit(raw,operations):
    for start,end,text in sorted(operations,reverse=True):raw=raw[:start]+text+raw[end:]
    return raw


def transform(originals):
    result=dict(originals)
    node=state_node(result[STATE])
    creates=node.children('create_state')
    assert len(creates)==1 and creates[0].one('country')=='c:VEN'
    assert {geography.prov(x) for x in geography.values(creates[0],'owned_provinces')}==CELLS
    country=creates[0].children('country')[0]
    result[STATE]=edit(result[STATE],[(country.start,country.end,'country = c:TUR')])
    for rel in [POPS,BUILD]:
        raw=result[rel];node=state_node(raw)
        regions=node.children('region_state:VEN')
        assert len(regions)==1 and not node.children('region_state:TUR')
        region=regions[0]
        # Change the political scope only. Foreign economic ownership stays VEN.
        result[rel]=edit(raw,[(region.start,region.start+len('region_state:VEN'),'region_state:TUR')])
    for rel in COUNTRIES:
        raw=result[rel];operations=[]
        for node in walk(parse(raw)):
            if node.key=='activate_law' and node.value in ['law_type:law_organic_regulation','law_type:law_elected_bureaucrats']:
                lo=raw.rfind('\n',0,node.start)+1
                hi=raw.find('\n',node.end)
                if hi<0:hi=len(raw)
                else:hi+=1
                operations.append((lo,hi,''))
        assert len(operations)==2,rel
        result[rel]=edit(raw,operations)
    return result


def inventory():
    owners,pairs,odd=geography.own_inventory(ROOT,a.GAME)
    pops=[];world=0;assets=[]
    for path in tech.effective('common/history/pops'):
        for root in parse(a.raw(path)):
            for state in root.children():
                if not state.key.startswith('s:'):continue
                for region in state.children():
                    for pop in region.children('create_pop'):
                        size=int(pop.one('size'));world+=size
                        if state.key in ['s:'+SID,'s:STATE_IONIAN_ISLANDS','s:STATE_MONTENEGRO']:
                            pops.append(dict(state=state.key,owner=region.key,size=size,
                                culture=pop.one('culture'),religion=pop.one('religion'),pop_type=pop.one('pop_type'),
                                full=json.loads(json.dumps(normalized([pop])))))
    for path in tech.effective('common/history/buildings'):
        for root in parse(a.raw(path)):
            for state in root.children():
                if state.key!='s:'+SID:continue
                for region in state.children():
                    for building in region.children('create_building'):
                        assets.append(dict(owner=region.key,building=scalar(building.one('building')),
                            level=building.one('level',building.one('levels','1')),
                            methods=geography.values(building,'activate_production_methods'),
                            full=json.loads(json.dumps(normalized([building])))))
    return dict(owners={k:[list(pair) for pair in v] for k,v in owners.items()},pairs={s+'|'+t:v for (s,t),v in pairs.items()},
                odd=odd,pops=pops,world_population=world,assets=assets)


def capture_current_inputs():
    assert not (LOT/'PATCH_INPUTS.json').exists(),'Already captured/applied; do not replay this patch.'
    base=json.loads((LOT/'BASELINE.json').read_text(encoding='utf-8'))
    originals={r:a.raw(ROOT/r) for r in OWN}
    for rel in OWN:
        dest=LOT/'patch_inputs'/rel;dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(ROOT/rel,dest)
    hashes={r:a.sha(ROOT/r) for r in OWN}
    dump('PATCH_INPUTS.json',dict(hashes=hashes,entry_differences=[r for r in OWN if hashes[r]!=base['owned'][r]]))
    dump('BEFORE.json',inventory())
    return originals,hashes


def apply():
    originals,hashes=capture_current_inputs()
    after=transform(originals)
    for rel in OWN:
        path=ROOT/rel
        assert a.sha(path)==hashes[rel], 'Concurrent edit: reread before writing '+rel
        bom=b'\xef\xbb\xbf' if path.read_bytes().startswith(b'\xef\xbb\xbf') else b''
        path.write_bytes(bom+after[rel].encode('utf-8'))
    dump('AFTER.json',inventory())
    print('Five scoped histories patched; no bitmap, state-definition, SERG or vanilla write.')


def render_map():
    old=json.loads((LOT/'BEFORE.json').read_text(encoding='utf-8'))
    new=json.loads((LOT/'AFTER.json').read_text(encoding='utf-8'))
    arr=np.array(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32)
    rgb=(arr[:,:,0]<<16)|(arr[:,:,1]<<8)|arr[:,:,2]
    anchors=[]
    for kind,number,name,expected in [('farm',119,'MON : noyau conservé','x8C6292'),
        ('farm',129,'Îles ioniennes : VEN','x405060'),('farm',123,'Tinos / x6090A0','x6090A0'),
        ('port',123,'Thera / x6960A0','x6960A0')]:
        path=a.GAME/f'gfx/map/map_object_data/generated_map_object_locators_{kind}.txt'
        values={int(i):(float(x),float(z)) for i,x,z in re.findall(
            r'id\s*=\s*(\d+)\s+position\s*=\s*\{\s*([\d.\-]+)\s+[\d.\-]+\s+([\d.\-]+)',a.raw(path))}
        x,z=values[number];y=rgb.shape[0]-z
        assert 'x%06X'%int(rgb[int(y),int(x)])==expected,(kind,number)
        anchors.append((name,x,y))
    x0,y0,x1,y1=4495,1040,4720,1265;sub=rgb[y0:y1,x0:x1]
    canvas=Image.new('RGB',(1860,1060),(20,29,39));d=ImageDraw.Draw(canvas)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
    small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
    title=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',24)
    colors={'TUR':(199,174,119),'VEN':(105,166,207),'MON':(171,102,138),
            'AUS':(202,201,196),'HUN':(150,173,145)}
    d.text((24,15),'BALKANS-01 — Réattribution politique, sans redessin du bitmap',font=title,fill='white')
    for ix,(data,label) in enumerate([(old,'AVANT : Cyclades vénitiennes'),(new,'APRÈS : Cyclades ottomanes')]):
        im=np.zeros((*sub.shape,3),dtype=np.uint8);im[:]=(32,58,77)
        for value in np.unique(sub):
            key='x%06X'%int(value)
            if key in data['owners']:
                tag=sorted({p[1] for p in data['owners'][key]})[0]
                im[sub==value]=colors.get(tag,(147,151,151))
        edge=np.zeros(sub.shape,dtype=bool)
        edge[:,1:]|=sub[:,1:]!=sub[:,:-1];edge[1:,:]|=sub[1:,:]!=sub[:-1,:]
        im[edge]=(43,51,56)
        px=24+ix*924;py=105
        canvas.paste(Image.fromarray(im).resize((900,900),Image.Resampling.NEAREST),(px,py))
        d.text((px,65),label,font=title,fill='white')
        for name,x,y in anchors:
            xx=px+(x-x0)*4;yy=py+(y-y0)*4
            tx,ty=(xx-235,yy+(15 if name.startswith('Thera') else -42)) if name.startswith(('Tinos','Thera')) else (xx-70,yy-40)
            box=d.textbbox((tx,ty),name,font=font)
            d.line((xx,yy,box[2],(box[1]+box[3])/2),fill='white',width=1)
            d.rectangle((box[0]-4,box[1]-3,box[2]+4,box[3]+3),fill=(19,29,40))
            d.text((tx,ty),name,font=font,fill='white');d.ellipse((xx-3,yy-3,xx+3,yy+3),fill='white')
    d.text((24,1016),'2 RGB réattribués : 453 pixels représentés. Aucun pixel du fichier du jeu recolorié.',font=font,fill=(220,224,228))
    d.text((24,1040),'Coordonnées du jeu et hubs natifs ; limites administratives internes de 1776 non reconstituées.',font=small,fill=(185,193,201))
    canvas.save(LOT/'AEGEAN_BEFORE_AFTER.png')
    print('Analytical map saved; all four annotation anchors checked against the current raster.')


def validate():
    base=json.loads((LOT/'BASELINE.json').read_text(encoding='utf-8'))
    before=json.loads((LOT/'BEFORE.json').read_text(encoding='utf-8'))
    inputs=json.loads((LOT/'PATCH_INPUTS.json').read_text(encoding='utf-8'))
    after=inventory();checks={}
    def check(name,ok):checks[name]=bool(ok)
    originals={r:a.raw(LOT/'patch_inputs'/r) for r in OWN}
    expected=transform(originals)
    # A separate technology agent patched five files after the first successful
    # WORLD validation. Verify the exact preimages and token edits; never restore
    # these files or simply ignore a changed hash. The shared building preimage
    # must already contain our complete WORLD patch, with no edit in our state.
    external_receipts={}
    peer=ROOT/'docs/reports/technology/STARTING_TECH_AUDIT_1776_R2'
    if (peer/'PM_PATCHES.json').exists() and (peer/'ALLOYS_PATCH.json').exists():
        patches=json.loads((peer/'PM_PATCHES.json').read_text(encoding='utf-8'))+[
            json.loads((peer/'ALLOYS_PATCH.json').read_text(encoding='utf-8'))]
        for patch in patches:
            rel=patch['file'];preimage=ROOT/patch['preimage'];text=a.raw(preimage)
            assert a.sha(preimage)==patch['before_sha256']
            if rel==BUILD:
                assert text==expected[BUILD]
                assert all(e.get('state')!=SID for e in patch['edits'])
            elif rel in base['protected']:
                assert patch['before_sha256']==base['protected'][rel]
            else:continue
            for e in sorted(patch['edits'],key=lambda e:e['start'],reverse=True):
                assert text[e['start']:e['end']]==e['old']
                text=text[:e['start']]+e['new']+text[e['end']:]
            assert text==a.raw(ROOT/rel) and a.sha(ROOT/rel)==patch['after_sha256']
            external_receipts[rel]=dict(before=patch['before_sha256'],after=patch['after_sha256'],
                 preimage=patch['preimage'],edits=patch['edits'],scope='INDEPENDENT_TECH_R2_TOKEN_PATCH')
            if rel in expected:expected[rel]=text
        receipt_dir=LOT/'concurrent_tech_r2';receipt_dir.mkdir(exist_ok=True)
        for name in ['PM_PATCHES.json','ALLOYS_PATCH.json','FILES_MODIFIED.json','CONCURRENT_CHANGES.json']:
            shutil.copy2(peer/name,receipt_dir/name)
    dump('CONCURRENT_PATCH_RECONCILIATION.json',external_receipts)
    for rel in OWN:
        check('only_authorized_or_verified_composed_bytes.'+rel,a.raw(ROOT/rel)==expected[rel])
        check('paradox_parse.'+rel,bool(parse(a.raw(ROOT/rel))))
    changed={rgb for rgb in set(before['owners'])|set(after['owners']) if before['owners'].get(rgb)!=after['owners'].get(rgb)}
    check('exact_two_owner_changes',changed==CELLS)
    for rgb in CELLS:
        check('VEN_to_TUR.'+rgb,before['owners'][rgb]==[[SID,'VEN']] and after['owners'][rgb]==[[SID,'TUR']])
    check('other_state_owner_pairs_preserved',
          {k:v for k,v in before['pairs'].items() if not k.startswith(SID+'|')}==
          {k:v for k,v in after['pairs'].items() if not k.startswith(SID+'|')})
    check('no_empty_old_VEN_scope',SID+'|VEN' not in after['pairs'] and not state_node(a.raw(ROOT/POPS)).children('region_state:VEN')
          and not state_node(a.raw(ROOT/BUILD)).children('region_state:VEN'))
    check('world_population_conserved',before['world_population']==after['world_population'])
    def nonpolitical(items):return [{k:v for k,v in x.items() if k!='owner'} for x in items]
    check('all_target_POP_bytes_preserved',nonpolitical(before['pops'])==nonpolitical(after['pops']))
    check('80404_greek_people_transferred',sum(x['size'] for x in after['pops'] if x['state']=='s:'+SID)==80404 and
          all(x['owner']=='region_state:TUR' and x['culture']=='greek' for x in after['pops'] if x['state']=='s:'+SID))
    check('buildings_PM_levels_economic_ownership_preserved',nonpolitical(before['assets'])==nonpolitical(after['assets']))
    check('two_buildings_under_TUR',len(after['assets'])==2 and all(x['owner']=='region_state:TUR' for x in after['assets']))
    check('VEN_private_financial_ownership_not_confiscated',a.raw(ROOT/BUILD).count('country="c:VEN"')==originals[BUILD].count('country="c:VEN"'))
    check('islands_no_new_land_connection_or_coast_change',a.sha(ROOT/'map_data/provinces.png')==base['protected']['map_data/provinces.png'])
    definitions=a.catalog('map_data/state_regions')
    state=definitions[SID][0]
    check('cells_still_same_state',set(a.ids(state,'provinces'))=={'"x6090A0"','"x6960A0"'})
    check('naval_exit_3117_preserved',state.one('naval_exit_id')=='3117')
    image=np.array(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32)
    bitmap=(image[:,:,0]<<16)|(image[:,:,1]<<8)|image[:,:,2]
    geometry=[]
    for rgb in sorted(CELLS):
        y,x=np.where(bitmap==int(rgb[1:],16))
        check('RGB_exists.'+rgb,len(x)>0)
        geometry.append(dict(rgb=rgb,from_owner='VEN',to_owner='TUR',state=SID,pixels=int(len(x)),
              bbox=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)],
              evidence='Native Cyclades hub locators and current raster; no cadastral boundary claimed'))
    dump('TERRITORIAL_CHANGES.json',geometry)
    effects=a.catalog('common/scripted_effects')
    starting=effects['effect_starting_politics_traditional'][0]
    direct={x.value for x in starting.children('activate_law')}
    check('native_traditional_sets_autocracy_and_hereditary_bureaucrats',
          {'law_type:law_autocracy','law_type:law_hereditary_bureaucrats'}<=direct)
    for rel in COUNTRIES:
        raw=a.raw(ROOT/rel)
        check('anachronistic_overrides_removed.'+rel,'law_organic_regulation' not in raw and 'law_elected_bureaucrats' not in raw)
        check('traditional_setup_kept.'+rel,'effect_starting_politics_traditional = yes' in raw)
    technologies,_,_=tech.objects('common/technology/technologies')
    scripted,_,_=tech.objects('common/scripted_effects')
    tags={};history=defaultdict(list)
    for p in tech.effective('common/history/countries'):
        for root in parse(a.raw(p)):
            for country in root.children():
                if country.key.startswith('c:'):history[country.key[2:]]+=country.children()
    for tag in ['TUR','VEN','WAL','MOL','MON']:
        g,c,calls,u=tech.resolve(history[tag],scripted,technologies)
        tags[tag]=dict(technologies=sorted(g),conditional=sorted(c),unresolved=u,effects=calls)
        check('target_country_starting_history_exists.'+tag,bool(history[tag]) and bool(g) and not u)
        check('target_granted_technologies_resolve.'+tag,g<=set(technologies))
    methods=a.catalog('common/production_methods');buildings=a.catalog('common/buildings')
    for asset in after['assets']:
        gates=set(a.ids(buildings[asset['building']][0],'unlocking_technologies'))
        check('transferred_building_technology.'+asset['building'],gates<=set(tags['TUR']['technologies']))
        for pm in asset['methods']:
            check('transferred_PM_technology.'+pm,set(a.ids(methods[pm][0],'unlocking_technologies'))<=set(tags['TUR']['technologies']))
    dump('STARTING_TECH_CHECK.json',dict(targets=tags,new_countries=0,new_grants=0,
        scope='Only unchanged target profiles and technologies needed by the transferred assets; not a repeat of the global audit'))
    # Input changes by the other agent are observable, never silently overwritten.
    external=[dict(path=r,before=h,current=a.sha(ROOT/r) if (ROOT/r).is_file() else None)
              for r,h in base['protected'].items() if not (ROOT/r).is_file() or a.sha(ROOT/r)!=h]
    serg_changes=[r for r,h in base['serg_proofs'].items() if not (ROOT/r).is_file() or a.sha(ROOT/r)!=h]
    check('protected_gameplay_unchanged_or_verified_external',all(
          x['path'] in external_receipts and x['current']==external_receipts[x['path']]['after'] for x in external))
    check('external_technology_receipts_reconstructed_exactly',
          not external or set(x['path'] for x in external)<=set(external_receipts))
    check('SERG_reports_and_receipts_unchanged',not serg_changes)
    check('native_vanilla_unchanged',all(a.sha(a.GAME/r)==h for r,h in base['vanilla'].items()))
    check('git_HEAD_branch_index_unchanged',a.git_state()==base['git'])
    check('no_new_tag',a.sha(ROOT/'common/country_definitions/00_countries.txt')==base['protected']['common/country_definitions/00_countries.txt'])
    check('all_armies_pacts_laws_resources_localization_untouched',all(x['path'].startswith(
          ('common/history/buildings/','common/technology/technologies/')) for x in external))
    concurrent=dict(status='EXTERNAL_TECH_R2_PATCHES_VERIFIED_AND_PRESERVED' if external_receipts else
                    ('NO_EXTERNAL_CHANGE_DETECTED' if not external and not serg_changes else 'CHANGES_TO_RECONCILE'),
                    gameplay=external,serg_documents=serg_changes,shared_inputs_changed_before_patch=inputs['entry_differences'],
                    shared_file_composition=external_receipts.get(BUILD),
                    verified_external_receipts='BALKANS-01/CONCURRENT_PATCH_RECONCILIATION.json',
                    rule='No whole-file restoration. Both agents token patches reconstructed exactly; all other bytes preserved.')
    (OUT/'CONCURRENT_CHANGES.json').write_text(json.dumps(concurrent,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    dump('POPULATION_BEFORE_AFTER.json',dict(world_before=before['world_population'],world_after=after['world_population'],
         delta=after['world_population']-before['world_population'],transferred=80404,from_owner='VEN',to_owner='TUR',
         culture='greek',religion='orthodox by native Greek culture default; explicit values unchanged',
         historical_population_correction=False))
    result=dict(status='PASS_STATIC' if all(checks.values()) else 'FAIL',passed=sum(checks.values()),total=len(checks),
                failed=[k for k,v in checks.items() if not v],checks=checks,runtime='NOT_RUN',
                installation_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',protected_gameplay_files=len(base['protected']),
                protected_gameplay_unchanged=len(base['protected'])-len(external),
                external_protected_files_verified=len(external),protected_serg_proofs=len(base['serg_proofs']))
    dump('VALIDATION.json',result)
    dump('FILES_MODIFIED.json',dict(files={r:dict(before=inputs['hashes'][r],after=a.sha(ROOT/r)) for r in OWN},
             unchanged_bitmap=a.sha(ROOT/'map_data/provinces.png'),new_tags=0,new_RGBs=0,changed_political_RGBs=2))
    print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
    assert all(checks.values()),result['failed']


def main():
    p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true');p.add_argument('--validate',action='store_true')
    p.add_argument('--map',action='store_true')
    args=p.parse_args()
    if args.apply:apply()
    elif args.validate:validate()
    elif args.map:render_map()
    else:
        data=inventory();print(json.dumps(dict(world_population=data['world_population'],target_owners={r:data['owners'][r] for r in CELLS},
                    target_assets=data['assets']),ensure_ascii=False,indent=2))


if __name__=='__main__':main()
