"""Scoped Freising / Regensburg political layers, never a new projection fit."""
import collections as C,hashlib,json,subprocess,sys,re
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import map2w_r4_political as pas

ROOT=pas.ROOT
OUT=pas.R4/'POLITICAL_REPRESENTATION/FREISING_REGENSBURG'
core=pas.prior.core
def load(p):return pas.load(p)
def dump(name,obj):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def snapshot():
    assert not (OUT/'BASELINE.json').exists()
    inv=core.qa.inventory(); hashes=pas.prior.q.economy.runtime_hashes()
    assert sum(r['count'] for r in inv['pops'])==835801255
    assert pas.sha(ROOT/'map_data/provinces.png')==pas.sha(pas.OUT/'provinces_candidate.png')
    dump('BASELINE.json',dict(inventory=inv,hashes=hashes,registry=load(ROOT/'docs/reports/map/MAP2L/IMPERIAL_DE_JURE_REGISTRY.json'),git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),git_index_sha256=pas.sha(ROOT/'.git/index'),protected_tool_hashes={p:pas.sha(ROOT/p) for p in ['tools/test_map2w_r4_political.py','tools/test_map2w_r2b_completion.py','tools/map2w_r4_bavaria.py','tools/map2w_r3_calibration.py']},bitmap_backup=(pas.OUT/'provinces_candidate.png').relative_to(ROOT).as_posix()))
    print('Fresh baseline: 568 imperial RGB, PAS preserved, world 835801255',flush=True)
def audit():
    b=load(OUT/'BASELINE.json');assert pas.sha(ROOT/b['bitmap_backup'])==b['hashes']['map_data/provinces.png']
    a=core.packed(ROOT/b['bitmap_backup']);rivers=np.array(Image.open(ROOT/'map_data/rivers.png'));owners={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']}
    boxes={'FREISING':(4340,895,4384,930),'WERDENFELS':(4320,922,4365,950),'REGENSBURG':(4350,870,4402,903)}
    diagnostics={r['name']:r['diagnostic_pixel'] for r in load(pas.R4/'GEOGRAPHIC_ASSESSMENT.json')['diagnostic_windows']}
    hubs=pas.prior.q.r9.locators(a);rows=[];f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',12)
    for name,box in boxes.items():
        x0,y0,x1,y1=box;s=20;im=Image.new('RGB',((x1-x0)*s+60,(y1-y0)*s+110),'#faf9f5');d=ImageDraw.Draw(im)
        d.text((15,8),name+' — AVANT le lot ; RGB natifs ; points bleus : rivières ; cercles : diagnostics non certifiés',font=f,fill='black')
        for y in range(y0,y1):
            for x in range(x0,x1):
                v=int(a[y,x]);rgb='x'+format(v,'06X');color=((v>>16)&255,(v>>8)&255,v&255);u=45+(x-x0)*s;w=45+(y-y0)*s
                d.rectangle((u,w,u+s,w+s),fill=color,outline='#555555')
                if rivers[y,x]<=15:d.ellipse((u+6,w+6,u+14,w+14),fill='#167cd2',outline='white')
        for x in range(x0,x1,2):d.text((45+(x-x0)*s,28),str(x),font=f,fill='black')
        for y in range(y0,y1,2):d.text((2,45+(y-y0)*s),str(y),font=f,fill='black')
        for label,(x,y) in diagnostics.items():
            if x0<=x<x1 and y0<=y<y1:
                u=45+(x-x0)*s;v=45+(y-y0)*s;d.ellipse((u-5,v-5,u+5,v+5),outline='white',width=3);d.text((u+8,v),label+' diagnostic R4',font=f,fill='black',stroke_width=1,stroke_fill='white')
        for r in hubs:
            if x0<=r['X']<x1 and y0<=r['Y']<y1:
                u=45+(r['X']-x0)*s;v=45+(r['Y']-y0)*s;d.rectangle((u-4,v-4,u+4,v+4),outline='white',width=2);d.text((u+6,v+10),'hub '+r['Kind']+' '+str(r['ID'])+' (indicatif)',font=f,fill='black',stroke_width=1,stroke_fill='white')
        values,counts=np.unique(a[y0:y1,x0:x1],return_counts=True)
        rr=[]
        for v,n in zip(values,counts):
            rgb='x'+format(int(v),'06X');rr.append(dict(rgb=rgb,owner=owners.get(rgb),window_cells=int(n),total_cells=int((a==v).sum())))
        rows.append(dict(name=name,box=box,RGBs=rr,hubs=[r for r in hubs if x0<=r['X']<x1 and y0<=r['Y']<y1]))
        im.save(OUT/(name+'_NATIVE.png'))
    dump('NATIVE_AUDIT.json',rows);print('Three native audit maps generated',flush=True)

def candidates():
    b=load(OUT/'BASELINE.json');assert pas.sha(ROOT/'map_data/provinces.png')==b['hashes']['map_data/provinces.png']
    a=core.packed(ROOT/'map_data/provinces.png');owners={r['key'][0]:r['key'][1:] for r in b['inventory']['owners']}
    specs=load(OUT/'POLITICAL_CHOICES.json');rgbvalues=[int(r['key'][0][1:],16) for r in b['inventory']['owners'] if r['key'][1:]==['STATE_BAVARIA','BAV']];donor=np.isin(a,rgbvalues)
    results=[]
    for opt in specs['options']:
        poly=np.array(opt['polygon_native']);lo=poly.min(axis=0);hi=poly.max(axis=0);yy,xx=np.mgrid[lo[1]:hi[1],lo[0]:hi[0]];inside=core.inside(np.column_stack([xx.ravel()+.5,yy.ravel()+.5]),poly);cells=[]
        for x,y in zip(xx.ravel()[inside],yy.ravel()[inside]):
            rgb='x'+format(int(a[y,x]),'06X')
            if rgb not in opt['allowed_parents']:continue
            assert owners[rgb]==['STATE_BAVARIA','BAV'] and not rgb.startswith('xED')
            cells.append([int(x),int(y)])
        mask=np.zeros(a.shape,bool)
        for x,y in cells:mask[y,x]=True
        parents=sorted({'x'+format(int(a[y,x]),'06X') for x,y in cells})
        results.append(dict(**opt,cells=cells,cell_count=len(cells),components=[len(c) for c in core.components(mask)],parents=[dict(rgb=p,before=int((a==int(p[1:],16)).sum()),remaining=int(((a==int(p[1:],16))&~mask).sum()),remaining_components=[len(c) for c in core.components((a==int(p[1:],16))&~mask)]) for p in parents],BAV_components_after=[len(c) for c in core.components(donor&~mask)],hubs_affected=[r for r in pas.prior.q.r9.locators(a) if mask[int(r['Y']),int(r['X'])]]))
    dump('CANDIDATES.json',dict(phase='BEFORE_SELECTION',donor_cells=int(donor.sum()),options=results))
    for r in results:print(r['id'],r['cell_count'],r['components'],r['parents'],'BAV',r['BAV_components_after'],'hubs',r['hubs_affected'],flush=True)

def evidence():
    from urllib.request import Request,urlopen
    from concurrent.futures import ThreadPoolExecutor
    items={
      'FREISING_ARCHIVE.html':'https://www2.erzbistum-muenchen.de/archiv-und-bibliothek/schaufenster/ausstellung-200-jahre-erzbistum/das-alte-bistum-freising/das-weltliche-fuerstentum-freising',
      'WELDEN.html':'https://personendatenbank.germania-sacra.de/persons/view/338846',
      'STADTAMHOF.html':'https://tourismus.regensburg.de/erleben-entdecken/sehenswuerdigkeiten-unesco-welterbe/stadtamhof',
      'FREISING_ARMS_SOURCE.html':'https://commons.wikimedia.org/wiki/File:Hochstift_Freising_coat_of_arms.svg',
      'FREISING_ARMS.svg':'https://upload.wikimedia.org/wikipedia/commons/8/8c/Hochstift_Freising_coat_of_arms.svg',
      'REGENSBURG_1700.jpg':'https://www.historisches-lexikon-bayerns.de/images/2/23/Ausschnitt_Stadtplan_Regensburg_1700.jpg',
      'REGENSBURG_HAB_MAP_379.jpg':'https://api.digitale-sammlungen.de/iiif/image/v2/bsb00007675_00379/full/2400,/0/default.jpg',
      'REGENSBURG_HAB_MANIFEST.json':'https://api.digitale-sammlungen.de/iiif/presentation/v2/bsb00007675/manifest'
    }
    dest=OUT/'EVIDENCE';dest.mkdir(exist_ok=True)
    def fetch(pair):
        name,url=pair;p=dest/name
        try:
            if not p.exists():
                with urlopen(Request(url,headers={'User-Agent':'1776-map-research/1.0'}),timeout=35) as r:p.write_bytes(r.read())
            return dict(file=name,url=url,bytes=p.stat().st_size,sha256=pas.sha(p),success=True)
        except Exception as e:return dict(file=name,url=url,success=False,error=str(e))
    results=list(ThreadPoolExecutor(max_workers=4).map(fetch,items.items()));dump('SOURCES_FETCH.json',results)
    for r in results:print(r['file'],r['success'],r.get('bytes',r.get('error')),flush=True)
    mf=dest/'REGENSBURG_HAB_MANIFEST.json'
    if mf.exists():
        m=load(mf);can=m['sequences'][0]['canvases'];print('HAB final leaves:',[(i,c['label'],c['images'][0]['resource']['service']['@id']) for i,c in enumerate(can) if i>len(can)-8],flush=True)
        thumbs=[]
        for i in range(len(can)-6,len(can)):
            resource=can[i]['images'][0]['resource'];url=resource['service']['@id']+'/full/650,/0/default.jpg';row=fetch(('HAB_LEAF_'+str(i+1)+'.jpg',url));thumbs.append(row)
        dump('HAB_LEAVES.json',dict(license=m.get('license'),metadata=m.get('metadata'),downloads=thumbs,scope='Six final leaves only, not the volume'))
        sheet=Image.new('RGB',(1950,1100),'white');d=ImageDraw.Draw(sheet)
        for k,r in enumerate(thumbs):
            if not r['success']:continue
            im=Image.open(dest/r['file']).convert('RGB');im.thumbnail((630,490));u=(k%3)*650;v=(k//3)*550;sheet.paste(im,(u,v+30));d.text((u+8,v+5),r['file'],fill='black')
        sheet.save(OUT/'HAB_FINAL_LEAVES.png')

def prepare():
    """Prepare only four reviewed political nuclei, in two explicit layers."""
    b=load(OUT/'BASELINE.json');assert pas.sha(ROOT/'map_data/provinces.png')==b['hashes']['map_data/provinces.png']
    a=core.packed(ROOT/'map_data/provinces.png');after=a.copy();opts={r['id']:r for r in load(OUT/'CANDIDATES.json')['options']};SID='STATE_BAVARIA'
    plan=[('R4B','FREISING_MINIMAL','x68CE1C','xEDBA10','FSI'),('R4C','DONAUSTAUF_MINIMAL','x3101A0','xEDBA11','RBI'),('R4C','WOERTH_MINIMAL','x3101A0','xEDBA12','RBI'),('R4C','REGENSBURG_CITY_MINIMAL','xA7094D','xEDBA13','RCI'),('R4C','REGENSBURG_CITY_MINIMAL','xFE59E7','xEDBA14','RCI')]
    assert not {'FSI','RBI','RCI'}&set(b['inventory']['countries'])
    for sector,ident,parent,rgb,tag in plan:
        assert not np.any(a==int(rgb[1:],16)) and rgb not in b['inventory']['geometry']
        for x,y in opts[ident]['cells']:
            if a[y,x]==int(parent[1:],16):after[y,x]=int(rgb[1:],16)
    assert np.count_nonzero(a!=after)==30
    country_defs={tag:f'{tag} = {{ color = {{ {color} }} country_type = recognized tier = principality cultures = {{ south_german }} religion = {religion} capital = STATE_BAVARIA }}\n' for tag,color,religion in [('FSI','203 174 65','catholic'),('RBI','178 51 64','catholic'),('RCI','172 83 112','protestant')]}
    ledger=b['registry'];geos={};migrations={}
    for sector,members,free in [('R4B',['FSI'],[]),('R4C',['RBI','RCI'],['RCI'])]:
        entries=[r for r in plan if r[0]==sector];parents=sorted({r[2] for r in entries});rows=[];new=[]
        for parent in parents:
            colors=[(parent,'BAV')]+[(rgb,tag) for sec,ident,par,rgb,tag in entries if par==parent]
            for rgb,tag in colors:
                yy,xx=np.where(after==int(rgb[1:],16));cells=[[int(x),int(y)] for x,y in zip(xx,yy)]
                assert len(core.components(after==int(rgb[1:],16)))==1
                rows.append(dict(rgb=rgb,parent_rgb=parent,state=SID,previous_owner='BAV',owner=tag,pixels=len(cells),cells=cells,confidence='B_POLITICAL_APPROXIMATION' if tag!='BAV' else 'RETAINED_NOT_HISTORICALLY_CERTIFIED'))
                if rgb!=parent:new.append(dict(rgb=rgb,parent_rgb=parent))
        geo=dict(parents=parents,assignments=rows,new_provinces=new,new_members=members,free_cities=free,hub_rebindings=[],classification='B_POLITICAL_APPROXIMATION',historical_cadastral_precision=False)
        previous=[r for r in ledger if r['state']==SID];updated=[r for r in previous if r['rgb'] not in parents]+[dict(rgb=r['rgb'],state=SID,beneficiary=r['owner'],basis='MAP2W-'+sector+': documented political nucleus B, not cadastral; see R4/POLITICAL_REPRESENTATION/FREISING_REGENSBURG/REPORT.md') for r in rows]
        migration=dict(replaced_regions=[SID],previous=previous,updated=updated,new_members=members,free_cities=free,new_provinces=new,geometry='MAP2W/R4/POLITICAL_REPRESENTATION/FREISING_REGENSBURG/'+sector+'/GEOMETRY.json',region_reference_changes=[],extent_added_cells=[],extent_removed_cells=[],country_additions={tag:core.qa.signature(core.cw.parse(country_defs[tag])[0]) for tag in members})
        (OUT/sector).mkdir(exist_ok=True);geos[sector]=geo;migrations[sector]=migration;dump(sector+'/GEOMETRY.json',geo)
        ledger=sorted([r for r in ledger if r['state']!=SID]+updated,key=lambda r:(r['rgb'],r['state'],r['beneficiary']))
    files={};original={}
    def old(rel):
        assert pas.sha(ROOT/rel)==b['hashes'][rel],rel
        raw=(ROOT/rel).read_text(encoding='utf-8-sig');original[rel]=raw;return raw
    rel='common/history/states/00_states.txt';raw=old(rel);n=core.state(raw,SID)
    text=''.join('\n create_state = { country = c:'+tag+' owned_provinces = { '+' '.join(r[3] for r in plan if r[4]==tag)+' } }\n' for tag in ['FSI','RBI','RCI'])
    files[rel]=core.edits(raw,[(n.end-1,n.end-1,text)])
    rel='map_data/state_regions/00_west_europe.txt';raw=old(rel);n=next(n for n in core.cw.parse(raw) if n.key==SID);f=n.children('provinces')[0];values=core.values(n,'provinces');expanded=[]
    for rgb in values:expanded += [rgb]+[r[3] for r in plan if r[2]==rgb]
    assert not any(parent in core.values(n,'prime_land') for parent in {r[2] for r in plan}),'Explicit prime-land review required'
    files[rel]=core.edits(raw,[(f.start,f.end,'provinces = { '+' '.join('"'+v+'"' for v in expanded)+' }')])
    assert all(a[int(r['Y']),int(r['X'])]==after[int(r['Y']),int(r['X'])] for r in pas.prior.q.r9.locators(a))
    rel='common/history/pops/00_west_europe.txt';raw=old(rel);n=core.region(raw,SID,'BAV');donor=load(OUT/'CANDIDATES.json')['donor_cells'];weights={'BAV':donor-30,'FSI':14,'RBI':14,'RCI':2};ops=[];pieces={tag:[] for tag in ['FSI','RBI','RCI']};alloc=[]
    for p in n.children('create_pop'):
        f=p.children('size')[0];amounts=core.allocate(int(f.value),weights);ops.append((f.start,f.end,'size = '+str(amounts['BAV'])))
        for tag in pieces:
            if amounts[tag]:pieces[tag].append(core.edits(raw[p.start:p.end],[(f.start-p.start,f.end-p.start,'size = '+str(amounts[tag]))]))
        alloc.append(dict(state=SID,source='BAV',culture=p.one('culture'),religion=p.one('religion','DEFAULT:'+p.one('culture')),before=int(f.value),after=amounts))
    raw=core.edits(raw,sorted(ops))
    for tag,p in pieces.items():raw=core.append(raw,SID,tag,'\n'.join(p))
    files[rel]=raw;dump('ALLOCATION.json',dict(weights=weights,profiles=alloc,method='CONSERVATION_OF_EXISTING_PROFILES_NOT_HISTORICAL_CENSUS',historical_population=None,populations={tag:sum(r['after'][tag] for r in alloc) for tag in pieces}))
    rel='map_data/province_terrains.txt';raw=old(rel);terrain={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',raw)}
    files[rel]=raw.rstrip()+'\n'+''.join(rgb+'="'+terrain[parent.upper()]+'"\n' for _,_,parent,rgb,_ in plan)
    for tag,defs in country_defs.items():
        files[f'common/country_definitions/1776_map2w_r4bc_{tag.lower()}.txt']=defs
        source=ROOT/'common/history/countries/pas - map2w_r4.txt';assert pas.sha(source)==b['hashes'][source.relative_to(ROOT).as_posix()]
        raw=source.read_text(encoding='utf-8-sig').replace('c:PAS','c:'+tag)
        if tag=='RCI':raw=raw.replace('law_autocracy','law_oligarchy').replace('law_theocracy','law_presidential_republic').replace('law_state_religion','law_freedom_of_conscience')
        files[f'common/history/countries/{tag.lower()} - map2w_r4bc.txt']=raw
    files['common/history/characters/1776_map2w_r4bc.txt']='CHARACTERS = {\n c:FSI ?= { create_character = { first_name = aor1776_fsi_first last_name = aor1776_fsi_last historical = yes culture = south_german religion = rel:catholic ruler = yes birth_date = 1727.5.11 interest_group = ig_devout ideology = ideology_traditionalist } }\n c:RBI ?= { create_character = { first_name = aor1776_sew_first last_name = aor1776_sew_last historical = yes culture = south_german religion = rel:catholic ruler = yes age = 64 interest_group = ig_devout ideology = ideology_traditionalist } }\n}\n'
    gov=''
    for tag in ['FSI','RBI','RCI']:
        city=tag=='RCI';law='law_presidential_republic' if city else 'law_theocracy';transfer='presidential_elective' if city else 'dictatorial';title='aor1776_city_councillor_title' if city else 'RULER_TITLE_PRINCE_BISHOP'
        gov+=f'gov_aor1776_{tag.lower()} = {{ transfer_of_power = {transfer} '+('new_leader_on_reform_government = no ' if city else '')+f'male_ruler = "{title}" female_ruler = "{title}" possible = {{ c:{tag} ?= this has_law = law_type:{law} }} on_government_type_change = {{ change_to_{transfer} = yes }} on_post_government_type_change = {{ post_change_to_{transfer} = yes }} }}\n'
    files['common/government_types/00_1776_map2w_r4bc.txt']=gov
    files['common/coat_of_arms/coat_of_arms/1776_map2w_r4bc.txt']='aor1776_freising = { pattern = "pattern_solid.tga" color1 = "yellow" textured_emblem = { texture = "te_aor1776_freising.dds" instance = { scale = { 0.8 0.8 } position = { 0.5 0.5 } } } }\naor1776_regensburg_bishop = { pattern = "pattern_solid.tga" color1 = "red" colored_emblem = { texture = "ce_bend_dexter.dds" color1 = "white" instance = { scale = { 1.0 1.0 } } } }\naor1776_regensburg_city = { pattern = "pattern_solid.tga" color1 = "red" colored_emblem = { texture = "ce_keys_st_peter.dds" color1 = "white" color2 = "white" instance = { scale = { 0.8 0.8 } } } }\n'
    files['common/flag_definitions/1776_map2w_r4bc.txt']=''.join(tag+' = { flag_definition = { coa = '+coa+' priority = 100 allow_overlord_canton = no } }\n' for tag,coa in [('FSI','aor1776_freising'),('RBI','aor1776_regensburg_bishop'),('RCI','aor1776_regensburg_city')])
    for lang in ['french','english']:
        fr=lang=='french';pairs={'FSI':'Freising','FSI_ADJ':'freisingois' if fr else 'Freising','RBI':'Évêché de Ratisbonne' if fr else 'Bishopric of Regensburg','RBI_ADJ':'ratisbonnais' if fr else 'Regensburg','RCI':'Ville impériale de Ratisbonne' if fr else 'Imperial City of Regensburg','RCI_ADJ':'ratisbonnais' if fr else 'Regensburg','aor1776_fsi_first':'Ludwig Joseph','aor1776_fsi_last':'von Welden','gov_aor1776_fsi':'Principauté épiscopale de Freising' if fr else 'Prince-Bishopric of Freising','gov_aor1776_rbi':'Principauté épiscopale de Ratisbonne' if fr else 'Prince-Bishopric of Regensburg','gov_aor1776_rci':'Conseil de la ville impériale' if fr else 'Imperial City Council'}
        descriptions={'fsi':('Le prince-évêque gouverne les possessions temporelles de Freising, distinctes des terres de son diocèse. Le chapitre cathédral désigne son successeur.','The prince-bishop governs the temporal possessions of Freising, distinct from the lands of his diocese. The cathedral chapter designates his successor.'),'rbi':('Le prince-évêque exerce sa souveraineté sur les possessions temporelles de son Église. La ville impériale de Ratisbonne conserve ses propres institutions ; le chapitre cathédral élit le prélat.','The prince-bishop exercises sovereignty over the temporal possessions of his church. The imperial city of Regensburg retains its own institutions; the cathedral chapter elects the prelate.'),'rci':('Le conseil urbain administre la ville libre de Ratisbonne et veille à ses privilèges impériaux. Ses magistrats exercent une autorité distincte de celle du prince-évêque.','The urban council administers the free city of Regensburg and upholds its imperial privileges. Its magistrates exercise authority distinct from that of the prince-bishop.')}
        for tag,ds in descriptions.items():pairs['gov_aor1776_'+tag+'_desc']=ds[0 if fr else 1]+'\\n\\n$TRANSFER_OF_POWER_NAME_DESC$'
        files[f'localization/{lang}/1776_map2w_r4bc_l_{lang}.yml']='\ufeffl_'+lang+':\n'+''.join(' '+k+':0 "'+v+'"\n' for k,v in pairs.items())
    files['docs/reports/map/MAP2L/IMPERIAL_DE_JURE_REGISTRY.json']=json.dumps(ledger,ensure_ascii=False,indent=2)+'\n'
    for sector,m in migrations.items():files[(OUT/sector/'REGISTRY_MIGRATION.json').relative_to(ROOT).as_posix()]=json.dumps(m,ensure_ascii=False,indent=2)+'\n'
    for rel,raw in files.items():
        if rel.endswith('.txt'):core.cw.parse(raw)
    dump('TEXT_BEFORE.json',original);dump('EXPECTED_TEXT.json',files);dump('PLAN.json',dict(plan=plan,changed_cells=30,registered_RGBs=len(ledger),selected_ids=['FREISING_MINIMAL','DONAUSTAUF_MINIMAL','WOERTH_MINIMAL','REGENSBURG_CITY_MINIMAL'],classification='B',new_members=['FSI','RBI','RCI']))
    Image.fromarray(np.stack([(after>>16)&255,(after>>8)&255,after&255],axis=-1).astype('uint8')).save(OUT/'provinces_candidate.png')
    core.OUT=OUT;core.emit(files,'HISTORY.patch');print('Prepared 30 cells, 5 new RGB, registry',len(ledger),'population',load(OUT/'ALLOCATION.json')['populations'],flush=True)

def maps():
    b=load(OUT/'BASELINE.json');a=core.packed(ROOT/b['bitmap_backup']);after=core.packed(OUT/'provinces_candidate.png');rivers=np.array(Image.open(ROOT/'map_data/rivers.png'));owners={int(r['key'][0][1:],16):r['key'][2] for r in b['inventory']['owners']};opts=load(OUT/'CANDIDATES.json')['options'];installed=pas.sha(ROOT/'map_data/provinces.png')==pas.sha(OUT/'provinces_candidate.png')
    colors={'BAV':'#e6dbb4','FSI':'#c49b1b','RBI':'#b24e61','RCI':'#3983ba','EIC':'#98bc9f','FBM':'#b4a0ca','ANS':'#a6c5d1','NUR':'#e6aaa0','PAS':'#b0bbdc','AUS':'#d3d3dd'}
    f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',11)
    names={0xEDBA10:'FSI',0xEDBA11:'RBI',0xEDBA12:'RBI',0xEDBA13:'RCI',0xEDBA14:'RCI'}
    for sector,box in [('R4B',(4349,901,4364,915)),('R4C',(4363,881,4388,896))]:
        x0,y0,x1,y1=box;s=25;pw=(x1-x0)*s+65;ph=(y1-y0)*s+165;canvas=Image.new('RGB',(3*pw,ph),'#faf9f5');d=ImageDraw.Draw(canvas)
        for k,(arr,label) in enumerate([(a,'AVANT — BAV'),(after,'APRÈS — installé (B)' if installed else 'PROPOSITION RETENUE (B)'),(a,'ÉCARTÉ — non installé (C)')]):
            ox=k*pw;d.text((ox+10,10),sector+' / '+label,font=f,fill='#173143')
            for y in range(y0,y1):
                for x in range(x0,x1):
                    val=int(arr[y,x]);owner=names.get(val,owners.get(val));col=colors.get(owner,'#dddddd');u=ox+45+(x-x0)*s;v=55+(y-y0)*s
                    d.rectangle((u,v,u+s,v+s),fill=col,outline='#a8a18c')
                    if rivers[y,x]<=15:d.ellipse((u+8,v+8,u+16,v+16),fill='#207bd2',outline='white')
            if k==2:
                for opt in opts:
                    if opt['sector']!=sector or opt['class_proposed']!='C':continue
                    for x,y in opt['cells']:
                        if not (x0<=x<x1 and y0<=y<y1):continue
                        u=ox+45+(x-x0)*s;v=55+(y-y0)*s;d.rectangle((u+2,v+2,u+s-2,v+s-2),outline='#b22175',width=3);d.line((u+3,v+3,u+s-3,v+s-3),fill='#b22175',width=2)
            for x in range(x0,x1,2):d.text((ox+45+(x-x0)*s,35),str(x),font=small,fill='black')
            for y in range(y0,y1,2):d.text((ox+5,55+(y-y0)*s),str(y),font=small,fill='black')
            d.text((ox+12,65+(y1-y0)*s),'FSI : ocre / RBI : rouge / RCI : bleu',font=small,fill='black')
            d.text((ox+12,86+(y1-y0)*s),'Points bleus : rivières natives, pas centres urbains.',font=small,fill='black')
        d.text((15,ph-49),'B = généralisation politique, non cadastrale. Hachures roses : hypothèses rejetées, jamais installées.',font=f,fill='black')
        d.text((15,ph-25),'Freising et Ratisbonne : noyaux seulement ; possessions périphériques et immunités intra-urbaines non restituées.',font=small,fill='black');canvas.save(OUT/(sector+'_BEFORE_AFTER.png'))
    print('Two scoped before/after and rejected-option maps generated; installed=',installed,flush=True)

def review():
    b=load(OUT/'BASELINE.json');current=pas.prior.q.economy.runtime_hashes();changed=sorted(p for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p));print('Runtime changes since capture:',changed)
    for sector in ['R4B','R4C']:
        g=load(OUT/sector/'GEOMETRY.json');footprint=sorted([r['rgb'],r['owner'],x,y] for r in g['assignments'] for x,y in r['cells']);print(sector,'footprint SHA',hashlib.sha256(json.dumps(footprint,separators=(',',':')).encode()).hexdigest(),[(r['rgb'],r['owner'],r['pixels']) for r in g['assignments']])
    assert not changed,'Review concurrent edits before installation'

def install_bitmap():
    b=load(OUT/'BASELINE.json');assert pas.sha(ROOT/'map_data/provinces.png')==b['hashes']['map_data/provinces.png']
    for rel,raw in load(OUT/'EXPECTED_TEXT.json').items():assert (ROOT/rel).read_text(encoding='utf-8-sig')==raw.lstrip('\ufeff'),rel
    from build_saint_gobain_icon import dds_bytes
    flag=ROOT/'gfx/coat_of_arms/textured_emblems/te_aor1776_freising.dds';assert not flag.exists()
    flag.write_bytes(dds_bytes(Image.open(OUT/'FREISING_FLAG_EMBLEM.png').convert('RGBA')))
    (ROOT/'map_data/provinces.png').write_bytes((OUT/'provinces_candidate.png').read_bytes())
    print('Installed exactly 30 cells and Freising flag; old Passau core untouched',flush=True)

def imperial():
    import map2k_imperial_system as compiler
    compiler.OUT=OUT;files=compiler.compile_system();dump('IMPERIAL_EXPECTED.json',files);core.OUT=OUT;patches=[]
    for i,(rel,raw) in enumerate(files.items()):
        if (ROOT/rel).read_text(encoding='utf-8-sig')==raw.lstrip('\ufeff'):continue
        name=f'IMPERIAL_{i}.patch';core.emit({rel:raw},name);patches.append(name)
    dump('IMPERIAL_PATCHES.json',patches);print('Prepared',len(patches),'changed imperial files out of',len(files),flush=True)

def journal():
    import render_map2k_imperial_map as render
    render.OUT=OUT;render.render()

def validate():
    import map2l_registry as reg
    from map2k_patch import ELECTORS
    b=load(OUT/'BASELINE.json');plan=load(OUT/'PLAN.json');inv=core.qa.inventory();checks=[]
    def check(name,value,detail=None):
        checks.append(dict(name=name,passed=bool(value),detail=detail))
        if not value:print('FAIL',name,detail,flush=True)
    def counter(rows):return C.Counter({tuple(r['key']):r['count'] for r in rows})
    before=core.packed(ROOT/b['bitmap_backup']);after=core.packed(ROOT/'map_data/provinces.png');expected=before.copy();geos=[load(OUT/s/'GEOMETRY.json') for s in ['R4B','R4C']];migrations=[load(OUT/s/'REGISTRY_MIGRATION.json') for s in ['R4B','R4C']]
    for g in geos:
        for r in g['assignments']:
            for x,y in r['cells']:expected[y,x]=int(r['rgb'][1:],16)
            check('Exact connected RGB '+r['rgb'],int((after==int(r['rgb'][1:],16)).sum())==r['pixels'] and len(core.components(after==int(r['rgb'][1:],16)))==1)
    check('Exact full bitmap, only 30 approved cells changed',np.array_equal(expected,after) and int((before!=after).sum())==30)
    eo=counter(b['inventory']['owners']);eg=dict(b['inventory']['geometry']);ec=dict(b['inventory']['countries']);et=dict(b['inventory']['state_types'])
    for sector,ident,parent,rgb,tag in plan['plan']:eo[rgb,'STATE_BAVARIA',tag]=1;eg[rgb]='STATE_BAVARIA'
    for m in migrations:ec=reg.expected_country_definitions(ec,[m])
    for tag in plan['new_members']:et['STATE_BAVARIA|'+tag]='incorporated_default'
    for key,wanted in [('owners',eo),('geometry',eg),('countries',ec),('state_types',et)]:check('Exact effective '+key,(counter(inv[key]) if key=='owners' else inv[key])==wanted)
    for key in ['pops','resolved_demographics','buildings','building_levels_written','units','duplicates','errors']:check('Global invariant '+key,inv[key]==b['inventory'][key])
    alloc=load(OUT/'ALLOCATION.json');ep=counter(b['inventory']['regional_pop'])
    for r in alloc['profiles']:
        ep[r['state'],r['source'],r['culture'],r['religion']]-=r['before']
        for tag,n in r['after'].items():ep[r['state'],tag,r['culture'],r['religion']]+=n
        check('Conserved integer demographic '+r['culture']+'/'+r['religion'],sum(r['after'].values())==r['before'] and all(isinstance(n,int) and n>=0 for n in r['after'].values()))
    check('Exact regional population transfers',counter(inv['regional_pop'])==ep)
    check('World population 835801255',sum(r['count'] for r in inv['pops'])==835801255)
    for tag,total in alloc['populations'].items():check('Technical population '+tag,sum(r['count'] for r in inv['regional_pop'] if r['key'][1]==tag)==total)
    for rel,old in load(OUT/'TEXT_BEFORE.json').items():
        if '/history/' in rel:
            raw=(ROOT/rel).read_text(encoding='utf-8-sig');nodes=lambda s:{n.key:core.qa.signature(n) for n in core.cw.walk(core.cw.parse(s)) if n.key.startswith('s:STATE_') and n.key!='s:STATE_BAVARIA'}
            check('All other state histories preserved '+rel,nodes(old)==nodes(raw))
        if rel.startswith('map_data/state_regions/'):
            oldnodes={n.key:n for n in core.cw.parse(old)};newnodes={n.key:n for n in core.cw.parse((ROOT/rel).read_text(encoding='utf-8-sig'))}
            for sid,n in oldnodes.items():
                exclude={'provinces'} if sid=='STATE_BAVARIA' else set();check('Resources/IDs/hubs/traits retained '+sid,[core.qa.signature(c) for c in n.children() if c.key not in exclude]==[core.qa.signature(c) for c in newnodes[sid].children() if c.key not in exclude])
    check('All map-object locator positions unchanged',pas.prior.q.r9.locators(before)==pas.prior.q.r9.locators(after))
    check('PAS exact 40-cell footprint unchanged',np.array_equal(before==0xEDBA00,after==0xEDBA00))
    check('PAS historical definition and data untouched',all(inv[k]==b['inventory'][k] for k in ['buildings','units']) and inv['countries']['PAS']==b['inventory']['countries']['PAS'] and [r for r in inv['regional_pop'] if r['key'][1]=='PAS']==[r for r in b['inventory']['regional_pop'] if r['key'][1]=='PAS'])
    check('All formerly installed xED cores unchanged',all(np.array_equal(before==int(rgb[1:],16),after==int(rgb[1:],16)) for rgb in b['inventory']['geometry'] if rgb.startswith('xED')))
    donor_colors=[int(r['key'][0][1:],16) for r in inv['owners'] if r['key'][1:]==['STATE_BAVARIA','BAV']];check('No new Bavarian country fragments',[len(c) for c in core.components(np.isin(after,donor_colors))]==[3374,5,3])
    for tag,wanted_parts in [('FSI',[14]),('RBI',[9,5]),('RCI',[2])]:
        colors=[int(r['key'][0][1:],16) for r in inv['owners'] if r['key'][2]==tag];check('Political country connectivity '+tag,[len(c) for c in core.components(np.isin(after,colors))]==wanted_parts)
    registry=load(ROOT/'docs/reports/map/MAP2L/IMPERIAL_DE_JURE_REGISTRY.json');wanted=b['registry']
    for m in migrations:
        check('Chronological registry migration '+str(m['new_members']),sorted([r for r in wanted if r['state']=='STATE_BAVARIA'],key=lambda r:r['rgb'])==sorted(m['previous'],key=lambda r:r['rgb']))
        wanted=sorted([r for r in wanted if r['state']!='STATE_BAVARIA']+m['updated'],key=lambda r:(r['rgb'],r['state'],r['beneficiary']))
    check('Exact unique registry 573 RGB',registry==wanted and len(registry)==len({r['rgb'] for r in registry})==573)
    check('Physical imperial extent unchanged',np.array_equal(np.isin(before,[int(r['rgb'][1:],16) for r in b['registry']]),np.isin(after,[int(r['rgb'][1:],16) for r in registry])))
    check('Strict cumulative approved layers',reg.approved_lot_dirs()[-3:]==[pas.OUT,OUT/'R4B',OUT/'R4C'])
    check('Nine electors unchanged, only RCI new free city',len(ELECTORS)==9 and not set(plan['new_members'])&set(ELECTORS.values()) and migrations[0]['free_cities']==[] and migrations[1]['free_cities']==['RCI'])
    for rel,raw in load(OUT/'EXPECTED_TEXT.json').items():
        check('Reviewed scoped text '+rel,(ROOT/rel).read_text(encoding='utf-8-sig')==raw.lstrip('\ufeff'))
        if rel.endswith('.txt'):core.cw.parse((ROOT/rel).read_text(encoding='utf-8-sig'))
    compiled=load(OUT/'IMPERIAL_EXPECTED.json')
    for rel,raw in compiled.items():check('Current cumulative compiler '+rel,(ROOT/rel).read_text(encoding='utf-8-sig')==raw.lstrip('\ufeff'))
    techs=set();laws=set();game=Path('C:/Games/Victoria 3/game')
    for folder,keys in [('common/technology/technologies',techs),('common/laws',laws)]:
        for root in [game,ROOT]:
            for p in (root/folder).glob('*.txt'):keys.update(n.key for n in core.cw.parse(p.read_text(encoding='utf-8-sig')))
    for tag in plan['new_members']:
        n=core.cw.parse((ROOT/f'common/history/countries/{tag.lower()} - map2w_r4bc.txt').read_text())[0].children()[0]
        check('Starting laws and technologies exist '+tag,all(c.value in techs for c in n.children('add_technology_researched')) and all(c.value.removeprefix('law_type:') in laws for c in n.children('activate_law')))
    sets=[]
    for lang in ['french','english']:
        p=ROOT/f'localization/{lang}/1776_map2w_r4bc_l_{lang}.yml';raw=p.read_text(encoding='utf-8-sig');ks=set(re.findall(r'^\s*([A-Za-z0-9_.-]+):0',raw,re.M));sets.append(ks)
        counts=C.Counter(k for fp in (ROOT/'localization'/lang).rglob('*.yml') for k in re.findall(r'^\s*([A-Za-z0-9_.-]+):(?:\d+)?\s',fp.read_text(encoding='utf-8-sig'),re.M) if k in ks)
        check('Localization BOM/header and fourteen unique keys '+lang,p.read_bytes().startswith(b'\xef\xbb\xbf') and raw.startswith('l_'+lang+':') and len(ks)==14 and all(counts[k]==1 for k in ks))
        check('Three dynamic succession descriptions '+lang,raw.count('$TRANSFER_OF_POWER_NAME_DESC$')==3)
    check('FR/EN keys identical',sets[0]==sets[1])
    flag=ROOT/'gfx/coat_of_arms/textured_emblems/te_aor1776_freising.dds';check('Freising DDS decoded pixels match source export',np.array_equal(np.array(Image.open(flag).convert('RGBA')),np.array(Image.open(OUT/'FREISING_FLAG_EMBLEM.png').convert('RGBA'))))
    for kind,name in [('colored_emblems','ce_keys_st_peter.dds'),('colored_emblems','ce_bend_dexter.dds')]:check('Native coat asset exists '+name,(game/'gfx/coat_of_arms'/kind/name).exists())
    check('Earlier tests and calibration tools never rewritten',all(pas.sha(ROOT/p)==h for p,h in b['protected_tool_hashes'].items()))
    current=pas.prior.q.economy.runtime_hashes();ours=set(load(OUT/'EXPECTED_TEXT.json'))|{p for p in compiled if current.get(p)!=b['hashes'].get(p)}|{'map_data/provinces.png',flag.relative_to(ROOT).as_posix(),'gfx/interface/journal_entries/aor1776_hre_registered_map.dds'}
    changed=sorted(p for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p));other=sorted(set(changed)-ours)
    dump('CONCURRENT_OBSERVATION.json',dict(files=[dict(path=p,before=b['hashes'].get(p),after=current.get(p)) for p in other],not_written_or_restored_by_MAP=True))
    check('No unexpected runtime writes outside scoped delivery',not other,other)
    check('HEAD unchanged',subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['git_head']);check('Git index unchanged',pas.sha(ROOT/'.git/index')==b['git_index_sha256'])
    check('44 duplicate RGB and 12 bad references preexisting only',len(inv['duplicates'])==44 and len(inv['errors'])==12 and inv['duplicates']==b['inventory']['duplicates'] and inv['errors']==b['inventory']['errors'])
    result=dict(status='READY_FOR_SCOPED_RUNTIME_VALIDATION' if all(r['passed'] for r in checks) else 'STATIC_REVIEW_REQUIRED',passed=sum(r['passed'] for r in checks),total=len(checks),checks=checks,world_before=835801255,world_after=sum(r['count'] for r in inv['pops']),populations=alloc['populations'],classification='B',changed_cells=30,registered_RGBs=len(registry),new_errors=[e for e in inv['errors'] if e not in b['inventory']['errors']],preexisting_duplicate_RGBs=44,preexisting_invalid_references=inv['errors'],engine_executed=False,runtime_status='NOT_TESTED_NEW_FREISING_REGENSBURG_CHANGES',Passau_runtime_status='PASS_RUNTIME_USER_VALIDATED')
    dump('VALIDATION.json',result);dump('POPULATION_VALIDATION.json',dict(world_before=835801255,world_after=result['world_after'],profiles=alloc['profiles'],populations=alloc['populations'],historical_census=False,buildings_and_economic_owners_conserved=inv['buildings']==b['inventory']['buildings'],units_conserved=inv['units']==b['inventory']['units']))
    dump('FILES_MODIFIED.json',dict(runtime_files=sorted(set(changed)&ours),registry='docs/reports/map/MAP2L/IMPERIAL_DE_JURE_REGISTRY.json',tools=['tools/map2w_r4bc.py','tools/map2w_r4bc_flags.mjs','tools/test_map2w_r4bc.py','tools/map2l_registry.py'],concurrent_files=other,workshop_generated=['workshop_assets/source/map2k_hre_registered_map.png']))
    for sector in ['R4B','R4C']:dump(sector+'/VALIDATION.json',dict(status='MAP2W_'+sector+'_READY_FOR_SCOPED_RUNTIME_VALIDATION' if result['passed']==result['total'] else 'STATIC_REVIEW_REQUIRED',classification='B',new_changes_runtime_validated=False,cumulative_validation='../VALIDATION.json',checks_passed=result['passed'],checks_total=result['total'],new_members=migrations[0 if sector=='R4B' else 1]['new_members']))
    print('Current installation validation',result['passed'],'/',result['total'],result['status'],flush=True);assert all(r['passed'] for r in checks)

def tests():
    import io,unittest
    modules=['test_map2w_r4bc','test_map2w_r4_political','test_map2w_r4_bavaria','test_map2l_registry','test_hre_centralization_01','test_hre_subject_feedback_01','test_hre_secession_lens_01','test_saint_gobain_icon','test_map2w_west_south','test_map2w_r2_hesse_nassau','test_map2w_r2b_completion','test_map2w_r3_franconia','test_map2w_r3_calibration']
    stream=io.StringIO();result=unittest.TextTestRunner(stream=stream).run(unittest.defaultTestLoader.loadTestsFromNames(modules))
    # Earlier tests assert their stage is the final registry layer. Preserve
    # their failures verbatim; validate the exact extended chain independently.
    stage_ids={'test_map2w_r4_political.PassauPoliticalPilot.test_registry_current_layer','test_map2w_r2b_completion.HesseNassauCompletion.test_registry_guard_accepts_current_layer'}
    failures=[dict(test=str(t),id=t.id(),traceback=s,classification='SUPERSEDED_FINAL_LAYER_ASSERTION' if t.id() in stage_ids else 'UNEXPECTED') for t,s in result.failures]
    errors=[dict(test=str(t),traceback=s) for t,s in result.errors];unexpected=[r for r in failures if r['classification']=='UNEXPECTED']
    dump('TESTS.json',dict(run=result.testsRun,passed_count=result.testsRun-len(failures)-len(errors),all_passed=result.wasSuccessful(),unexpected_failures=unexpected,failures=failures,errors=errors,old_tests_modified=False,output=stream.getvalue(),engine_executed=False,modules=modules,new_tests=37,accepted_only_with_strict_current_chain_validation=True))
    print(stream.getvalue(),flush=True);assert not unexpected and not errors

def source_maps():
    f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16);title=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',19)
    im=Image.open(pas.R4/'EVIDENCE/BSB_1791_READING.jpg').convert('RGB').crop((330,410,1210,1015));out=Image.new('RGB',(1250,725),'#faf9f5');out.paste(im,(10,45));d=ImageDraw.Draw(out)
    d.text((10,12),'Freising — lecture politique du panneau Reilly 1791, pas un calage sur le jeu',font=title,fill='#173143')
    for k,(text,x,y) in enumerate([('Freising / Burgfrieden : noyau B',675,510),('Ismaning : bande non restituée',575,845),('Burgrain : possession séparée',1030,845),('Munich : souveraineté bavaroise',385,990)]):
        u=920;v=95+k*130;px=10+x-330;py=45+y-410;d.text((u,v),text,font=f,fill='#173143');d.line((u-10,v+10,px,py),fill='#173143',width=2);d.ellipse((px-4,py-4,px+4,py+4),fill='#173143')
    d.text((10,680),'Repères de lecture schématiques, non limites 1776 pixel-exactes. Werdenfels figure sur un autre panneau de cette feuille.',font=f,fill='black');out.save(OUT/'FREISING_SOURCE_ANNOTATED.png')
    # New HAB plate is source evidence only, never a game texture or exact warp.
    source=Image.open(OUT/'EVIDENCE/REGENSBURG_HAB_MAP_379.jpg').convert('RGB');source.thumbnail((1600,1100));out=Image.new('RGB',(1600,source.height+100),'#faf9f5');out.paste(source,(0,50));d=ImageDraw.Draw(out)
    d.text((10,10),'Ratisbonne — juridictions temporelles distinctes (Schmid, HAB 41, planche finale)',font=title,fill='#173143');d.text((10,source.height+60),'Ville / Stadtamhof / Donaustauf / Wiesent / Wörth : source confrontée aux noyaux B ; aucune superposition métrique.',font=f,fill='black');out.save(OUT/'REGENSBURG_SOURCE_CONTEXT.png')
    # Concrete C alternatives: screening windows, not candidate borders.
    a=core.packed(ROOT/load(OUT/'BASELINE.json')['bitmap_backup']);rivers=np.array(Image.open(ROOT/'map_data/rivers.png'));owners={int(r['key'][0][1:],16):r['key'][2] for r in load(OUT/'BASELINE.json')['inventory']['owners']}
    screens=[dict(name='BUR GRAIN'.replace(' ',''),box=[4360,907,4375,920],alternatives=[[4364,910,4368,914],[4367,912,4371,916]],reason='Two eastern screening sectors without demonstrated identification of the Burgrain jurisdiction; no candidate transfer selected.'),dict(name='WERDENFELS',box=[4328,925,4355,941],alternatives=[[4334,930,4341,934],[4340,931,4350,936]],reason='Western/Bavarian and eastern/Tyrolean screens differ in current sovereignty; Loisach/valley and Ettal boundary not identifiable sufficiently. No relocation of prior Swabian cores.')]
    results=[]
    for spec in screens:
        x0,y0,x1,y1=spec['box'];s=25;out=Image.new('RGB',(max(750,(x1-x0)*s+65),(y1-y0)*s+140),'#faf9f5');d=ImageDraw.Draw(out);d.text((12,10),spec['name']+' — alternatives C, AUCUN transfert',font=title,fill='#173143')
        for y in range(y0,y1):
            for x in range(x0,x1):
                owner=owners.get(int(a[y,x]));u=45+(x-x0)*s;v=50+(y-y0)*s;d.rectangle((u,v,u+s,v+s),fill='#e6dbb4' if owner=='BAV' else '#d2d0e3' if owner=='AUS' else '#9ab3a1',outline='#aaa58e')
                if rivers[y,x]<=15:d.ellipse((u+8,v+8,u+16,v+16),fill='#207bd2',outline='white')
        alternatives=[]
        for i,(xx0,yy0,xx1,yy1) in enumerate(spec['alternatives']):
            d.rectangle((45+(xx0-x0)*s,50+(yy0-y0)*s,45+(xx1-x0)*s,50+(yy1-y0)*s),outline=['#b52f6f','#773c97'][i],width=3);d.text((45+(xx0-x0)*s+3,52+(yy0-y0)*s),'C'+str(i+1),font=f,fill='black',stroke_width=1,stroke_fill='white')
            vs,counts=np.unique(a[yy0:yy1,xx0:xx1],return_counts=True);alternatives.append(dict(box=[xx0,yy0,xx1,yy1],not_candidate_boundary=True,installed=False,RGBs=[dict(rgb='x'+format(int(v),'06X'),owner=owners.get(int(v)),cells=int(n)) for v,n in zip(vs,counts)]))
        for x in range(x0,x1,2):d.text((45+(x-x0)*s,32),str(x),font=f,fill='black')
        for y in range(y0,y1,2):d.text((0,50+(y-y0)*s),str(y),font=f,fill='black')
        d.text((10,60+(y1-y0)*s),'Beige : BAV ; gris : AUS ; vert : autres pays, préservés.',font=f,fill='black');d.text((10,85+(y1-y0)*s),'Rectangles : fenêtres de comparaison, PAS contours historiques.',font=f,fill='black');out.save(OUT/(spec['name']+'_C_OPTIONS.png'));results.append(dict(**spec,alternatives_inventory=alternatives,installed=False))
    dump('UNRESOLVED_OPTIONS.json',results)

def delivery():
    v=load(OUT/'VALIDATION.json');t=load(OUT/'TESTS.json');assert v['passed']==v['total'] and not t['unexpected_failures'] and not t['errors']
    rows=[]
    for sector in ['R4B','R4C']:
        g=load(OUT/sector/'GEOMETRY.json');changes=[dict(**r,sector=sector,State_ID=71) for r in g['assignments'] if r['owner']!='BAV'];rows+=changes;dump(sector+'/TERRITORIAL_CHANGES.json',changes)
        table=['# Cellules effectivement transférées — '+sector,'','Catégorie B : représentation politique documentée, pas un cadastre.','', '| X | Y | Parent | Nouveau RGB | Avant | Après | State_ID |','| ---: | ---: | --- | --- | --- | --- | ---: |']
        table += [f"| {x} | {y} | {r['parent_rgb']} | {r['rgb']} | BAV | {r['owner']} | 71 |" for r in changes for x,y in sorted(r['cells'],key=lambda p:(p[1],p[0]))]
        (OUT/sector/'TERRITORIAL_CHANGES.md').write_text('\n'.join(table)+'\n',encoding='utf8')
        dump(sector+'/POPULATION_VALIDATION.json',dict(cumulative_world_before=835801255,cumulative_world_after=v['world_after'],populations={tag:v['populations'][tag] for tag in g['new_members']},allocation='../ALLOCATION.json',historical_census=False))
    dump('TERRITORIAL_CHANGES.json',rows)
    dump('DECISION.json',dict(R4B='MAP2W_R4B_READY_FOR_SCOPED_RUNTIME_VALIDATION',R4C='MAP2W_R4C_READY_FOR_SCOPED_RUNTIME_VALIDATION',classification='B_POLITICAL_APPROXIMATION',installed_cells=30,new_members=['FSI','RBI','RCI'],new_RGBs=['xEDBA10','xEDBA11','xEDBA12','xEDBA13','xEDBA14'],registered_RGBs=573,runtime_test_executed=False,Passau='PASS_RUNTIME_USER_VALIDATED',historical_precision='No cadastral or urban-centre pixel-exact claim',unresolved='UNRESOLVED.md',test_summary=dict(run=t['run'],passed=t['passed_count'],superseded_final_layer_failures=len(t['failures']),new_current_contracts=37)))
    f=load(OUT/'FILES_MODIFIED.json');paths=set(f['runtime_files']+f['tools']+f['workshop_generated']+[f['registry']]);paths|={p.relative_to(ROOT).as_posix() for p in OUT.rglob('*') if p.is_file() and p.name!='DELIVERY_MANIFEST.json'}
    paths|={'docs/reports/map/MAP2W/REPORT.md','docs/reports/map/MAP2W/R4/REPORT.md','docs/reports/map/MAP2W/R4/POLITICAL_REPRESENTATION/PASSAU/RUNTIME_USER_ATTESTATION.json','docs/reports/map/MAP2W/R4/POLITICAL_REPRESENTATION/PASSAU/REPORT.md','docs/reports/map/MAP2W/R4/POLITICAL_REPRESENTATION/PASSAU/PLAYER_GUIDE.md','docs/reports/map/MAP2W/R4/POLITICAL_REPRESENTATION/PASSAU/DECISION.json'}
    dump('DELIVERY_MANIFEST.json',dict(files=[dict(path=p,sha256=pas.sha(ROOT/p),bytes=(ROOT/p).stat().st_size) for p in sorted(paths)],git_head_unchanged=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==load(OUT/'BASELINE.json')['git_head'],git_index_unchanged=pas.sha(ROOT/'.git/index')==load(OUT/'BASELINE.json')['git_index_sha256'],engine_executed=False))
    print('Independent sector deliveries and manifest exported',flush=True)
if __name__=='__main__':globals()[sys.argv[1]]()
