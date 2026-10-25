"""One additional authorized Passau-outliers pass, with Berchtesgaden still pending."""
import collections as C,contextlib,copy,csv,io,json,os,re,shutil,subprocess,sys,unittest,urllib.request
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import serg_sc1_berchtesgaden as prior
import serg_sc1_berchtesgaden_native_salt as salt
ROOT=prior.ROOT;rm=prior.rm;core=prior.core;reg=prior.reg;sha=prior.sha
OUT=rm.OUT/'SC1-PASSAU-OUTLIERS';TASK=OUT.name;PREFIX=OUT.relative_to(ROOT).as_posix()+'/'
SID='STATE_AUSTRIA';TAG='PAS';PARENT='xFDA6CB';RGB='xEDC000';POP=1400
CELLS=[[4393,911],[4393,912],[4394,911],[4394,912]]
os.environ['GIT_OPTIONAL_LOCKS']='0'
def load(p):return rm.load_json(p)
def dump(n,o):rm.write_json(OUT/n,o)

def capture():
    assert not (OUT/'BASELINE.json').exists();OUT.mkdir(exist_ok=True)
    state=load(rm.OUT/'ROADMAP_STATE.json');assert state['events'][-1]['id']=='SERG-RM-0033';assert rm.check()['status']=='PASS'
    probe=copy.deepcopy(state);probe.pop('runtime_validation_hold',None);assert rm.progress(probe)['next_task']==TASK
    assert next(t for t in state['tasks'] if t['id']==prior.TASK)['runtime_validation']['attestation'] is None
    before=load(salt.OUT/'DELIVERY_MANIFEST.json');diff=[p for p,h in before['files'].items() if sha(ROOT/p)!=h];assert not diff,diff
    git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
    dump('BASELINE.json',dict(roadmap=state,hashes=prior.italian.runtime_hashes(),inventory=core.qa.inventory(),registry=load(reg.active_registry_path()),proofs={p.relative_to(ROOT).as_posix():sha(p) for p in rm.OUT.rglob('*') if p.is_file() and OUT not in p.parents},tools={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'tools').glob('*.py') if p.name!=Path(__file__).name},git=dict(head=git('rev-parse','HEAD'),branch=git('branch','--show-current'),index=sha(ROOT/'.git/index')),berchtesgaden_delivery_unchanged=True,selection_without_runtime_hold=rm.progress(probe)))
    shutil.copyfile(ROOT/'map_data/provinces.png',OUT/'provinces_before.png')
    (OUT/'AUTHORIZATION.md').write_text('''# Autorisation et sélection

Demande directe du joueur : « Non, finis aussi la suite du prompt. Je relancerai le jeu et vérifierai les deux choses à la fois. »

Interprétation annoncée au joueur avant intervention : une étape supplémentaire SC1-PASSAU-OUTLIERS, candidate indépendante du suivi. Le test BG-I-CORE révisé n'est ni présumé réussi ni un préalable imposé à cette nouvelle autorisation. Le validateur courant est PASS ; après retrait du seul verrou de test pour calcul de sélection, SC1-PASSAU-OUTLIERS est P1 sans dépendance et première admissible. Ce calcul n'accorde aucun point et ne ferme aucun ancien blocage. Un protocole commun couvrira les installations effectivement réalisées ; aucune troisième étape commencée.
''',encoding='utf8');print('Selection confirmed; native Berchtesgaden mine and old proofs intact',flush=True)

def survey():
    b=load(OUT/'BASELINE.json');a=core.packed(OUT/'provinces_before.png');owners={r['key'][0]:r['key'][2] for r in b['inventory']['owners']};rows=[]
    for r in b['inventory']['owners']:
        rgb,sid,tag=r['key']
        if sid not in ['STATE_AUSTRIA','STATE_BAVARIA','STATE_BOHEMIA','STATE_TYROL']:continue
        yy,xx=np.where(a==int(rgb[1:],16))
        if len(xx) and xx.min()<4420 and xx.max()>4385 and yy.min()<927 and yy.max()>881:rows.append(dict(rgb=rgb,state=sid,owner=tag,cells=len(xx),bounds=[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())]))
    dump('NATIVE_INVENTORY.json',dict(provinces=rows,pops=[r for r in b['inventory']['regional_pop'] if r['key'][0] in ['STATE_AUSTRIA','STATE_BAVARIA'] and r['key'][1] in ['AUS','BAV','PAS']],buildings=[r for r in b['inventory']['buildings'] if r['key'][0] in ['STATE_AUSTRIA','STATE_BAVARIA'] and r['key'][1] in ['AUS','BAV','PAS']]))
    import serg_sc1_salzburg as slz
    dump('LOCATORS_BEFORE.json',slz.prior.pas.prior.q.r9.locators(a));print('Native provinces',rows,flush=True)
    rivers=np.asarray(Image.open(core.qa.GAME/'map_data/rivers.png'));print('Rivers',rivers.shape,np.unique(rivers[890:922,4385:4420],return_counts=True),flush=True)
    x0,y0,x1,y1,scale=4385,885,4421,926,22;im=Image.new('RGB',((x1-x0)*scale+80,(y1-y0)*scale+90),'#faf8ed');d=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',11)
    d.text((10,8),'Lecture native : PAS 40 cellules / AUS / BAV ; traits bleus = rivieres natives',fill='black',font=font)
    colors={'AUS':'#d8b783','BAV':'#b6c8aa','PAS':'#a95265','SLZ':'#668baa'}
    for y in range(y0,y1):
        for x in range(x0,x1):
            u,v=60+(x-x0)*scale,45+(y-y0)*scale;rgb='x'+format(int(a[y,x]),'06X');color=colors.get(owners.get(rgb),'#b6b1c8');d.rectangle((u,v,u+scale,v+scale),fill=color,outline='#b8b8b8')
            if int(rivers[y,x]) not in [254,255]:d.ellipse((u+6,v+6,u+16,v+16),fill='#267ca1')
            if a[y,x]!=a[y,x-1]:d.line((u,v,u,v+scale),fill='#333',width=2)
            if a[y,x]!=a[y-1,x]:d.line((u,v,u+scale,v),fill='#333',width=2)
    for x in range(x0,x1,2):d.text((60+(x-x0)*scale,26),str(x),font=font,fill='black')
    for y in range(y0,y1):d.text((18,45+(y-y0)*scale),str(y),font=font,fill='black')
    im.save(OUT/'NATIVE_READING.png')

def atlas():
    url='https://www.geschichte-bayerns.de/files/repo/kblg/hab-ai/kblg.hab.ai.35/HAB-AI-35_Veit_1978.pdf';p=OUT/'VEIT_1978.pdf'
    if not p.exists():
        request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(request,timeout=60) as r,p.open('wb') as f:shutil.copyfileobj(r,f)
    import fitz
    doc=fitz.open(p);matches=[]
    for i,page in enumerate(doc):
        text=page.get_text()
        if 'Obernberg' in text and any(word in text for word in ['1782','1772','Hochstifts','Karte','Karten']):matches.append(dict(pdf_index=i,text=text[:9000]))
    dump('ATLAS_READING_INDEX.json',dict(url=url,sha256=sha(p),pages=len(doc),matches=matches));print('Atlas',len(doc),'pages; candidate indexes',[r['pdf_index'] for r in matches],flush=True)

def prepare():
    import map2k_imperial_system as compiler
    b=load(OUT/'BASELINE.json');assert prior.italian.runtime_hashes()==b['hashes']
    if not (OUT/'COMPILER_BEFORE.json').exists():
        compiler.OUT=OUT;generated=compiler.compile_system();actual={p:(ROOT/p).read_text('utf-8-sig') for p in generated};diff=[p for p in generated if generated[p].lstrip('\ufeff')!=actual[p]];dump('COMPILER_BEFORE.json',dict(actual=actual,differences=diff));assert not diff,diff
    else:
        saved=load(OUT/'COMPILER_BEFORE.json');assert not saved['differences'] and all((ROOT/p).read_text('utf-8-sig')==raw for p,raw in saved['actual'].items())
    a=core.packed(OUT/'provinces_before.png');assert RGB not in b['inventory']['geometry'] and not np.any(a==int(RGB[1:],16));z=a.copy()
    for x,y in CELLS:assert int(z[y,x])==int(PARENT[1:],16);z[y,x]=int(RGB[1:],16)
    rows=[]
    for rgb,owner in [(PARENT,'AUS'),(RGB,TAG)]:
        ys,xs=np.where(z==int(rgb[1:],16));assert len(prior.physical.components(xs,ys))==1;rows.append(dict(rgb=rgb,parent_rgb=PARENT,state=SID,previous_owner='AUS',owner=owner,pixels=len(xs),cells=sorted([[int(x),int(y)] for x,y in zip(xs,ys)]),confidence='B_POLITICAL_APPROXIMATION' if owner==TAG else 'RETAINED_NOT_CERTIFIED'))
    assert rows[0]['pixels']==175 and rows[1]['pixels']==4
    overlaps=[(d.name,r['rgb']) for d in reg.approved_lot_dirs() for r in load(d/'GEOMETRY.json')['assignments'] if set(map(tuple,r.get('cells',[])))&set(map(tuple,CELLS))];assert not overlaps,overlaps
    geo=dict(parents=[PARENT],assignments=rows,new_provinces=[dict(rgb=RGB,parent_rgb=PARENT)],new_members=[],free_cities=[],selected_option='OBERNBERG_MARKET_CORE',classification='B_POLITICAL_APPROXIMATION',historical_cadastral_precision=False,hub_rebindings=[],scope='Obernberg market and immediate suburbs B only, not all Passau outliers or a modern municipal border')
    files={};originals={}
    def old(p):assert sha(ROOT/p)==b['hashes'][p];raw=(ROOT/p).read_bytes().decode('utf8');originals[p]=raw;return raw
    p='common/history/states/00_states.txt';raw=old(p);node=core.state(raw,SID);files[p]=core.edits(raw,[(node.end-1,node.end-1,'\n\t\t# SC1-PASSAU-OUTLIERS: Obernberg sovereign market B, not all Innviertel.\n\t\tcreate_state = { country = c:PAS owned_provinces = { xEDC000 } }\n\t')]).replace('\t\n\t\t# SC1-PASSAU-OUTLIERS:', '\n\t\t# SC1-PASSAU-OUTLIERS:')
    p='map_data/state_regions/00_west_europe.txt';raw=old(p);off=int(raw.startswith('\ufeff'));node=next(n for n in core.cw.parse(raw.lstrip('\ufeff')) if n.key==SID);field=node.children('provinces')[0];frag=raw[field.start+off:field.end+off];assert frag.count('"'+PARENT+'"')==1;files[p]=core.edits(raw,[(field.start+off,field.end+off,frag.replace('"'+PARENT+'"','"'+PARENT+'" "'+RGB+'"'))])
    p='map_data/province_terrains.txt';raw=old(p);terrain={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',raw)};assert RGB.upper() not in terrain;files[p]=raw+'\n'+RGB+'="'+terrain[PARENT.upper()]+'"\n'
    p='common/history/pops/00_west_europe.txt';raw=old(p);node=core.region(raw,SID,'AUS');donor=next(p for p in node.children('create_pop') if p.one('culture')=='south_german' and p.one('religion') is None and p.one('pop_type') is None and int(p.one('size'))>=POP);field=donor.children('size')[0];amount=int(field.value);raw=core.edits(raw,[(field.start,field.end,'size = '+str(amount-POP))]);files[p]=core.append(raw,SID,TAG,'\n\t\t\tcreate_pop = { culture = south_german size = 1400 }\n').replace('\t\n\t\tregion_state:PAS','\n\t\tregion_state:PAS')
    files['common/scripted_effects/1776_sc1_passau_obernberg.txt']='''assign_aor1776_passau_obernberg_names = {
 if = {
  limit = { state_region = s:STATE_AUSTRIA owner = { c:PAS ?= this } }
  set_state_name = aor1776_state_obernberg
  set_hub_name = { type = city name = aor1776_hub_obernberg }
 }
}
'''
    files['common/on_actions/99_1776_sc1_passau_obernberg.txt']='''on_game_started = { on_actions = { aor1776_passau_obernberg_names_initialize } }
on_game_started_after_lobby = { on_actions = { aor1776_passau_obernberg_names_initialize } }
on_state_created = { on_actions = { aor1776_passau_obernberg_state_changed } }
on_state_owner_change = { on_actions = { aor1776_passau_obernberg_state_changed } }
aor1776_passau_obernberg_names_initialize = { effect = { every_state = { assign_aor1776_passau_obernberg_names = yes } } }
aor1776_passau_obernberg_state_changed = { effect = { assign_aor1776_passau_obernberg_names = yes } }
'''
    for lang in ['french','english']:files['localization/'+lang+'/1776_sc1_passau_obernberg_l_'+lang+'.yml']='\ufeffl_'+lang+':\n aor1776_state_obernberg:0 "Obernberg am Inn"\n aor1776_hub_obernberg:0 "Obernberg am Inn"\n'
    previous=[r for r in b['registry'] if r['state']==SID];assert next(r for r in previous if r['rgb']==PARENT)['beneficiary']=='AUS';add=dict(rgb=RGB,state=SID,beneficiary=TAG,basis='SC1-PASSAU-OUTLIERS: Obernberg sovereign market B before 1782; four-cell residence and suburb nucleus, not whole Innviertel or cadastral limits')
    migration=dict(replaced_regions=[SID],previous=previous,updated=sorted(previous+[add],key=lambda r:r['rgb']),new_members=[],free_cities=[],new_provinces=geo['new_provinces'],geometry='SERG_CLOSURE/'+TASK+'/GEOMETRY.json',region_reference_changes=[],extent_added_cells=[],extent_removed_cells=[],country_additions={})
    rel=reg.active_registry_path().relative_to(ROOT).as_posix();originals[rel]=(ROOT/rel).read_bytes().decode('utf8');assert load(ROOT/rel)==b['registry'];files[rel]=json.dumps(sorted(b['registry']+[add],key=lambda r:(r['rgb'],r['state'],r['beneficiary'])),ensure_ascii=False,indent=2)+'\n'
    p='tools/map2l_registry.py';originals[p]=(ROOT/p).read_text('utf8');needle='        result.append(berchtesgaden)\n    return result';assert needle in originals[p]
    guard='''        result.append(berchtesgaden)
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
    return result'''
    files[p]=originals[p].replace(needle,guard)
    for p,raw in files.items():
        if p.endswith('.txt'):core.cw.parse(raw.lstrip('\ufeff'))
        if p not in originals:assert not (ROOT/p).exists(),p
    dump('GEOMETRY.json',geo);dump('REGISTRY_MIGRATION.json',migration);dump('TEXT_BEFORE.json',originals);dump('EXPECTED_TEXT.json',files)
    dump('DEMOGRAPHY.json',dict(transferred=POP,donor='AUS',recipient=TAG,state=SID,donor_total_before=1638057,donor_total_after=1636657,donor_south_german_before=1597398,donor_south_german_after=1595998,selected_group_before=amount,selected_group_after=amount-POP,old_passau_core_unchanged=14267,total_passau_after=15667,historical_basis='OeAW printed p27: 1783 estimate 1441 = parish 3241 minus St Georgen 1800, includes Markt and suburbs; 1782 243 houses, only 95 Markt. Rounded 1400 estimate for 1776 B market/suburb nucleus, uncertainty 1200-1600, not direct census or whole former parish.',culture='south_german',religion='DEFAULT:south_german',professions='not invented',population_per_pixel=False))
    Image.fromarray(np.stack([(z>>16)&255,(z>>8)&255,z&255],axis=-1).astype('uint8')).save(OUT/'provinces_candidate.png');print('Prepared Obernberg four cells, 1400 transferred people; no new country or building',flush=True)

def install():
    b=load(OUT/'BASELINE.json');files=load(OUT/'EXPECTED_TEXT.json');old=load(OUT/'TEXT_BEFORE.json');assert prior.italian.runtime_hashes()==b['hashes'],'Concurrent change requires review'
    for p,raw in old.items():assert (ROOT/p).read_bytes().decode('utf8')==raw,p
    for p,raw in files.items():
        if p not in old:assert not (ROOT/p).exists(),p
        (ROOT/p).write_bytes(raw.encode('utf8'))
    shutil.copyfile(OUT/'provinces_candidate.png',ROOT/'map_data/provinces.png')
    import map2k_imperial_system as compiler
    compiler.OUT=OUT;expected=compiler.compile_system();changed=[];preflight=load(OUT/'COMPILER_BEFORE.json')['actual']
    for p,raw in expected.items():
        assert (ROOT/p).read_text('utf-8-sig')==preflight[p],p
        if raw.lstrip('\ufeff')==preflight[p]:continue
        bom=(ROOT/p).read_bytes().startswith(b'\xef\xbb\xbf');(ROOT/p).write_bytes((('\ufeff' if bom and not raw.startswith('\ufeff') else '')+raw).encode('utf8'));changed.append(p)
    dump('IMPERIAL_EXPECTED.json',expected);dump('IMPERIAL_FILES.json',changed);print('Obernberg installed; imperial files changed',len(changed),flush=True)

def validate():
    b=load(OUT/'BASELINE.json');old=b['inventory'];inv=core.qa.inventory();cur=prior.italian.runtime_hashes();files=load(OUT/'EXPECTED_TEXT.json');checks=[]
    def ck(n,ok,d=None):checks.append(dict(name=n,passed=bool(ok),detail=d))
    a=core.packed(OUT/'provinces_before.png');z=core.packed(ROOT/'map_data/provinces.png');yy,xx=np.where(a!=z)
    ck('Exact four AUS to PAS cells only',sorted(zip(xx.tolist(),yy.tolist()))==sorted(map(tuple,CELLS)) and all(int(a[y,x])==int(PARENT[1:],16) and int(z[y,x])==int(RGB[1:],16) for x,y in CELLS))
    ck('Map dimensions retained',a.shape==z.shape==(3616,8192))
    for rgb,count in [(RGB,4),(PARENT,175)]:
        yy,xx=np.where(z==int(rgb[1:],16));ck('Connected exact '+rgb,len(xx)==count and len(prior.physical.components(xx,yy))==1)
    eo=core.qa.counter(old['owners']);eo[RGB,SID,TAG]=1;ck('Only new province owner added',core.qa.counter(inv['owners'])==eo)
    eg=dict(old['geometry']);eg[RGB]=SID;ck('Only new province geometry added',inv['geometry']==eg)
    ck('Exactly one new PAS state portion',inv['states']==sorted(old['states']+[[SID,TAG]]));types=dict(old['state_types']);types[SID+'|'+TAG]='incorporated_default';ck('State types retained',inv['state_types']==types)
    for key in ['pops','resolved_demographics','countries','buildings','building_levels_written','units','errors','duplicates']:ck('Invariant '+key,inv[key]==old[key])
    ep=core.qa.counter(old['regional_pop']);ep[SID,'AUS','south_german','DEFAULT:south_german']-=POP;ep[SID,TAG,'south_german','DEFAULT:south_german']=POP;ck('Exact 1400-person transfer no other region changed',core.qa.counter(inv['regional_pop'])==ep)
    node=core.region(files['common/history/pops/00_west_europe.txt'],SID,TAG).children('create_pop')[0];ck('No invented profession or religious split',[(n.key,n.value) for n in node.children()]==[('culture','south_german'),('size','1400')])
    ledger=load(reg.active_registry_path());m=load(OUT/'REGISTRY_MIGRATION.json');add=next(r for r in m['updated'] if r['rgb']==RGB)
    ck('Registry 578 to 579 exact additive title',len(ledger)==579 and ledger==sorted(b['registry']+[add],key=lambda r:(r['rgb'],r['state'],r['beneficiary'])))
    ck('AUS parent title and all old rows retained',all(r in ledger for r in b['registry']) and add['beneficiary']=='PAS')
    ck('Same physical imperial extent',np.array_equal(np.isin(a,[int(r['rgb'][1:],16) for r in b['registry']]),np.isin(z,[int(r['rgb'][1:],16) for r in ledger])))
    ck('Obernberg is existing PAS no new member or country',not m['new_members'] and not m['country_additions'] and 'PAS' in reg.additional_members())
    from map2k_patch import ELECTORS
    ck('Nine electors and no Passau free city',len(ELECTORS)==9 and 'PAS' not in ELECTORS.values() and 'PAS' not in reg.additional_free_cities())
    ck('Current strict cumulative tail',reg.approved_lot_dirs()[-2:]==[prior.OUT,OUT])
    import serg_sc1_salzburg as slz
    ck('All physical locators and their RGBs unchanged',slz.prior.pas.prior.q.r9.locators(z)==load(OUT/'LOCATORS_BEFORE.json'))
    p='map_data/state_regions/00_west_europe.txt';node=lambda raw:next(n for n in core.cw.parse(raw.lstrip('\ufeff')) if n.key==SID)
    ck('Every old hub resource arable and trait retained',[core.qa.signature(n) for n in node(load(OUT/'TEXT_BEFORE.json')[p]).children() if n.key!='provinces']==[core.qa.signature(n) for n in node(files[p]).children() if n.key!='provinces'])
    definition=prior.italian.definitions('common/country_definitions')['PAS'];ck('Passau national capital remains STATE_BAVARIA',definition.one('capital')=='STATE_BAVARIA')
    names=files['common/scripted_effects/1776_sc1_passau_obernberg.txt'];ck('Obernberg names limited to PAS Austrian portion','limit = { state_region = s:STATE_AUSTRIA owner = { c:PAS ?= this } }' in names and 'set_capital' not in names)
    for label,rgb,count in [('Passau original','xEDBA00',40),('Salzbourg','xEDBB00',12),('Massa','xEDBC00',8),('Trento','xEDBD00',12),('Brixen','xEDBE00',9),('Berchtesgaden','xEDBF00',4)]:ck('Prior exact core retained '+label,int((z==int(rgb[1:],16)).sum())==count and np.array_equal(a==int(rgb[1:],16),z==int(rgb[1:],16)))
    ck('All six native Berchtesgaden salt correction files unchanged',all(cur[p]==b['hashes'][p] for p in load(salt.OUT/'FILES_MODIFIED.json')['runtime_files']))
    for p,raw in files.items():
        ck('Exact installed bytes '+p,(ROOT/p).read_bytes()==raw.encode('utf8'))
        if p.endswith('.txt'):
            try:core.cw.parse(raw.lstrip('\ufeff'));ok=True
            except Exception:ok=False
            ck('Syntax '+p,ok)
    for p,raw in load(OUT/'IMPERIAL_EXPECTED.json').items():ck('Imperial compiled bytes '+p,(ROOT/p).read_text('utf-8-sig')==raw.lstrip('\ufeff'))
    changed=sorted(p for p in set(cur)|set(b['hashes']) if cur.get(p)!=b['hashes'].get(p));allowed=set(files)|set(load(OUT/'IMPERIAL_FILES.json'))|{'map_data/provinces.png'};ck('All other functional and concurrent files retained',set(changed)<=allowed,changed)
    ck('No new building army country law or treaty file',not any(p.startswith(('common/buildings/','common/production_methods/','common/history/buildings/','common/history/military_formations/','common/country_definitions/','common/history/countries/','common/history/treaties/')) for p in changed))
    ck('All old nested proof bytes unchanged',all(sha(ROOT/p)==h for p,h in b['proofs'].items() if Path(p).parent!=rm.OUT.relative_to(ROOT)))
    tools=[p for p,h in b['tools'].items() if sha(ROOT/p)!=h];ck('Only appended old registry guard changed',tools==['tools/map2l_registry.py'],tools)
    import localization_duplicate_audit as audit
    sets=[]
    for lang in ['french','english']:
        p='localization/'+lang+'/1776_sc1_passau_obernberg_l_'+lang+'.yml';matches=[audit.KEY.match(line) for line in files[p].lstrip('\ufeff').splitlines()[1:]];keys={m.group(1) for m in matches if m};sets.append(keys);entries=audit.entries(lang);van=audit.entries(lang,root=audit.VANILLA)
        ck('Two unique BOM keys no vanilla collision '+lang,len(keys)==2 and all(matches) and (ROOT/p).read_bytes().startswith(b'\xef\xbb\xbf') and all(len(entries[k])==1 for k in keys) and not (keys&set(van)))
    ck('Both languages same keys',sets[0]==sets[1]);ck('No new human validation',not list(OUT.glob('RUNTIME_USER_ATTESTATION*')) and next(t for t in load(rm.OUT/'ROADMAP_STATE.json')['tasks'] if t['id']==prior.TASK)['runtime_validation']['attestation'] is None)
    git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip();ck('Git HEAD branch and index unchanged',git('rev-parse','HEAD')==b['git']['head'] and git('branch','--show-current')==b['git']['branch'] and sha(ROOT/'.git/index')==b['git']['index'])
    v=dict(task_ids=[TASK],status='PASS' if all(c['passed'] for c in checks) else 'FAIL',passed=sum(c['passed'] for c in checks),total=len(checks),failed=[c['name'] for c in checks if not c['passed']],checks=checks,automated_engine_test=False,engine_executed=False);dump('VALIDATION.json',v);print('Static',v['passed'],'/',v['total'],v['failed'],flush=True);assert not v['failed'],v['failed'];dump('SESSION_AFTER_STATIC.json',dict(hashes=cur,inventory=inv));dump('FILES_MODIFIED.json',dict(runtime_files=changed,sha256={p:cur[p] for p in changed},old_tools_changed=tools))

def documentation_and_tracking():
    b=load(OUT/'BASELINE.json');s=load(rm.OUT/'ROADMAP_STATE.json');assert s==b['roadmap'];v=load(OUT/'VALIDATION.json');assert v['status']=='PASS'
    a=core.packed(OUT/'provinces_before.png');z=core.packed(ROOT/'map_data/provinces.png');owners={r['key'][0]:r['key'][2] for r in b['inventory']['owners']};owners[RGB]='PAS'
    x0,y0,x1,y1,scale=4385,893,4409,927,18;panel=(x1-x0)*scale+65;im=Image.new('RGB',(panel*2,(y1-y0)*scale+125),'#faf8ed');d=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',11);rivers=np.asarray(Image.open(core.qa.GAME/'map_data/rivers.png'))
    for k,(arr,title) in enumerate([(a,'AVANT : Obernberg non distingue'),(z,'INSTALLE B : enclave PAS, 4 cellules')]):
        ox=k*panel;d.text((ox+10,8),title,fill='black',font=font)
        for y in range(y0,y1):
            for x in range(x0,x1):
                u,w=ox+48+(x-x0)*scale,46+(y-y0)*scale;rgb='x'+format(int(arr[y,x]),'06X');color='#7d3d82' if rgb==RGB else {'AUS':'#d8b783','BAV':'#b6c8aa','PAS':'#a95265','SLZ':'#668baa'}.get(owners.get(rgb),'#bbb7c3');d.rectangle((u,w,u+scale,w+scale),fill=color,outline='#bbb')
                if rivers[y,x]!=255:d.ellipse((u+6,w+6,u+11,w+11),fill='#267ca1')
                if arr[y,x]!=arr[y,x-1]:d.line((u,w,u,w+scale),fill='#333',width=2)
                if arr[y,x]!=arr[y-1,x]:d.line((u,w,u+scale,w),fill='#333',width=2)
        for x in range(x0,x1,3):d.text((ox+48+(x-x0)*scale,27),str(x),font=font,fill='black')
        for y in range(y0,y1,3):d.text((ox+10,46+(y-y0)*scale),str(y),font=font,fill='black')
        for text,x,y in [('PAS : noyau conserve',4401,897),('Obernberg B',4393.5,911.5),('SLZ conserve',4386.5,925)]:
            u,w=ox+48+(x-x0)*scale,46+(y-y0)*scale;d.text((u-45,w+5),text,font=font,fill='black',stroke_width=2,stroke_fill='white')
    d.text((10,im.height-55),'B politique : centre et faubourgs seulement, sans limite cadastrale ni corridor.',fill='black',font=font);d.text((10,im.height-34),'Le voisinage AUS est technique : le blocage Innviertel bavarois en 1776 reste ouvert.',fill='black',font=font);im.save(OUT/'BEFORE_AFTER.png')
    source=rm.OUT/'SC2-AUSTRIA/EVIDENCE/UPPER_SEUTTER.jpg';dump('SOURCE_READING.json',dict(record_date='2026-10-24',historical_date='1776-01-01',historical_map=dict(path=source.relative_to(ROOT).as_posix(),sha256=sha(source),date='1740-1760',detail=PREFIX+'SEUTTER_INN_DETAIL.png',actually_viewed=True,observed='Passau, Inn, Scharding, Obernberg, Ried; right-bank position upstream of Passau, western relation to Linz/Hausruck',cadastral_boundary_read=False),native_grid_actually_viewed=True,old_R4_alignment_reused=False,modern_boundary_used=False,oeaw=dict(url='https://www.oeaw.ac.at/fileadmin/subsites/Institute/VID/PDF/Publications/diverse_Publications/Historisches_Ortslexikon/Ortslexikon_Oberoesterreich_Teil_2.pdf',reading='PDF text, printed pages 27 and 68, indexes 26 and 67; remote screenshot cache miss',direct_1776_census=False),veit_atlas=dict(identified=True,full_read=False,access_failures=['Web PDF exceeds 55.95 MB reader limit','Terminal DNS unavailable'],high_resolution_map_read=False),bibliography=PREFIX+'SOURCES.md'))
    with (OUT/'RGB_BEFORE_AFTER.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['rgb','region','before_owner','after_owner','before_cells','after_cells','scope'])
        for row in load(OUT/'GEOMETRY.json')['assignments']:w.writerow([row['rgb'],SID,'AUS',row['owner'],179 if row['rgb']==PARENT else 0,row['pixels'],row['confidence']])
    with (OUT/'JURISDICTION_MATRIX.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['jurisdiction','1776_distinction','installed','remaining'])
        w.writerows([['Obernberg','Passau sovereign enclave before 1782','Four-cell market/suburb B; 1400','No cadastral or whole-parish certificate'],['Passau core','Previously accepted PAS, forty cells','Strict retention','Not credited twice'],['Rannariedl/Jandelsbrunn west','1765 acquisition versus Austrian eastern rights','None','Dated assignment and comparable population'],['Niederkessla','Austrian sovereignty after 1765','None','Do not restore from pre-1765 coloring'],['Vichtenstein/Riedenburg','1782 cession cannot be anticipated','None','Jurisdictions beyond one modern commune and population'],['Abteiland/Wolfstein/Freyung/Wegscheid','Sovereign peripheral districts','None','Not the rejected 83-cell extension'],['Hals/St Nikola/Neuburg','Bavarian sovereignty or Austrian sovereignty distinguished from property','None','No artificial corridor or annexation'],['Innviertel','Bavarian outside enclaves in 1776','AUS donor residual retained technically','SC2-AUSTRIA remains blocked without definitive approval']])
    sub=dict(id='PS-OB-CORE',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',tag='PAS',state=SID,category='B',new_rgb=RGB,cells=CELLS,previous_owner='AUS',population_transferred=POP,scope='Obernberg market and immediate suburb nucleus only, not all outliers or whole parish; no new country, army or building; existing Passau national capital and original forty-cell core retained.')
    dump('IMPLEMENTATION.json',dict(task_ids=[TASK],regional_status='BLOCKED',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',sub_lots=[sub],independently_testable_components=[dict(id='PS-OB-T',test='Four-cell enclave, donor connectivity, old forty-cell core, neighbors and imperial right'),dict(id='PS-OB-D',test='1400 inhabitants transferred, 14267 retained in Bavaria, national total 15667'),dict(id='PS-OB-N',test='Obernberg names only on PAS/Austria portion; national capital unchanged')],no_new_country=True,no_new_building=True,no_new_army=True,no_runtime_attestation=True,points_awarded=0))
    protocol='''# Protocole commun — Berchtesgaden et Obernberg

Deux installations en attente : **BG-I-CORE révisé** (mine standard) et **PS-OB-CORE**. Aucun reçu humain anticipé. Un même mois de la même nouvelle partie peut servir aux deux vérifications ; rapporter séparément leurs résultats.

1. Fermer puis relancer Victoria 3 et lancer une **nouvelle partie au 1er janvier 1776** avec le mod actuel. Une ancienne sauvegarde ne valide pas les nouvelles initialisations.
2. **Berchtesgaden/BGT** : quatre cellules, 1000 habitants, capitale Berchtesgaden intérieure ; Hausen prince-prévôt, théocratie, chancellerie publique de 100 postes. Vérifier **un niveau de Mines de sel standard**, visible dans Ressources, propriété BGT et méthodes ordinaires. La capacité affichée de 5000 postes n'est pas un effectif réellement rempli ; le recrutement partiel est voulu. Aucune saline ou petite mine spéciale ne doit exister. Examiner outils, sel, finances et toute anomalie.
3. **Passau/PAS** : le noyau original de quarante cellules reste présent et sa capitale nationale reste dans sa portion bavaroise. Leopold Ernst von Firmian, prince-évêché, lois et relations sont conservés. L'ajout n'est pas un nouveau pays Obernberg.
4. Repérer l'**enclave Obernberg am Inn**, au sud-ouest du noyau de Passau, sur la rive droite de l'Inn : quatre cellules B, sans corridor. Comparer BEFORE_AFTER.png. Nouvelle portion PAS dans la région technique Autriche : **1400 habitants** initiaux. Portion PAS en Bavière **14267**, total national **15667**, avant croissance. Portion AUS/Autriche **1636657**. Aucun nouveau métier, régiment ou bâtiment propre à cet ajout n'est prévu ; observer les moyens de subsistance et l'équilibre réel.
5. Vérifier le nom Obernberg sur la seule portion PAS/Autriche et son point de ville s'il est affiché. Aucune capitale nationale déplacée vers Obernberg ; Vienne/Linz et les hubs autrichiens restent à leur propriétaire. Le placement automatique local n'est pas déjà certifié.
6. Vérifier les droits impériaux de l'enclave au bénéfice de PAS, sans nouvelle admission, ville libre ou dixième électeur. Ne pas exiger de pacte ou armée nouvelle. Vérifier les **douze cellules de Salzbourg**, Trente, Brixen, Massa, BAV/AUS et les autres anciens noyaux.
7. Les territoires voisins encore affichés AUS ne constituent pas une validation historique de tout l'Innviertel en 1776. Vichtenstein, l'Abteiland et les autres périphéries non installées restent bloqués ; ne pas les inclure dans la réussite de PS-OB-CORE.
8. Contrôler les travaux concurrents utilisés dans la partie (fortifications/génie, France/Anzin/Saint-Gobain/drainage, États-Unis). Simuler **un mois complet**, sauvegarder puis recharger. Revérifier la mine BGT, l'enclave PAS, leurs noms, propriétaires, populations, bâtiments, souverains et voisins.
9. Rapporter les résultats réels pour **BG-I-CORE révisé** et **PS-OB-CORE** séparément. Un succès de l'un ne masque pas un échec de l'autre et ne clôture pas leurs régions entières.

Prochaine candidate identifiée dans NEXT_ACTION.md seulement ; aucune autre tâche n'est commencée par cette passe.
''';(OUT/'PLAYER_TEST_PROTOCOL.md').write_text(protocol,encoding='utf8')
    report=f'''**SERG TERRITORIAL 1.0 — PROGRESSION : 34,89 %**

# SC1-PASSAU-OUTLIERS — Obernberg installé, périphéries encore bloquées

**82/235 → 82/235, 34,89 % → 34,89 %**, 24 tâches qualifiées sur 81. Périmètre 1.0.0 et poids inchangés. Votre demande de poursuivre pendant l'attente du test autorise cette seule nouvelle tâche ; Berchtesgaden n'est pas déclaré validé. Le validateur confirme SC1-PASSAU-OUTLIERS P1 sans dépendance après calcul séparé du verrou de test.

## Recherches et choix

SOURCES.md et JURISDICTION_MATRIX.csv distinguent les frontières de 1765, les cessions de 1782, les biens médiats et la souveraineté. HLB et la commune d'Obernberg étayent l'enclave ; Seutter 1740–1760 est réellement relu, avec détail conservé. L'atlas Veit complet n'a pas été obtenu et le rendu PDF ÖAW a échoué ; seule sa partie textuelle consultée est utilisée. Aucune ancienne calibration R4, frontière moderne, carte postérieure de 1791 recopiée ou carte haute résolution non lue n'est invoquée.

B_PROPOSAL.md compare le territoire complet différé, le noyau de marché B retenu et le diagnostic seul. Le chiffre **1400** est arrondi d'après l'estimation publiée de 1441 en 1783 pour Obernberg et ses faubourgs ; ce n'est pas un recensement direct de 1776 ni toute la paroisse. Les limites de cette comparaison sont explicites.

## Installation réellement effectuée

**PS-OB-CORE IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION** : PAS existant, nouveau xEDC000, quatre cellules **{CELLS}**, AUS→PAS dans STATE_AUSTRIA ; xFDA6CB **179→175**, connecté. Petit cartogramme sur la rive droite de l'Inn en amont du confluent, pas restitution cadastrale. Aucun corridor ni nouveau TAG. Les **40 cellules PAS xEDBA00** et son parent BAV sont strictement identiques. Aucun hub physique, ressource, arable ou trait déplacé.

**1400 habitants transférés** depuis le groupe south_german AUS, confession catholique par défaut, aucune profession inventée : AUS/Autriche **1638057→1636657**, sud-germaniques **1597398→1595998**. PAS/Bavière **14267 inchangés** ; PAS/Autriche **1400** ; total PAS **15667**. Monde **834926252**, cultures/confessions globales conservées.

Firmian, gouvernement, lois, drapeau et capitale nationale de Passau dans STATE_BAVARIA restent inchangés. Un effet enfant nomme seulement la portion PAS/Autriche **Obernberg am Inn** ; le point local automatique reste à observer. Aucun bâtiment spécial ou standard, industrie, fort, armée, traité ou technologie ajouté pour Obernberg. L'activité de marché et l'équilibre de la nouvelle portion ne sont pas prétendus simulés par un bonus : leurs moyens réels sont à observer en jeu.

Registre impérial **578→579**, un seul titre borné nouveau ; tous les anciens droits et l'emprise physique conservés. PAS déjà membre, sans nouvelle admission, ville libre ou dixième électeur. Sept fichiers impériaux sont régénérés après comparaison exacte du générateur avec l'état courant ; aucune restauration depuis une ancienne baseline.

## Conservation et blocages

**{v['passed']}/{v['total']} contrôles statiques PASS**, détails VALIDATION.json. Tests cumulatifs et contrats ciblés consignés dans TESTS.json/SCOPED_TESTS.json ; les anciennes assertions de dernière couche restent conservées et classées, jamais supprimées pour obtenir un faux résultat vert. Contrôle final de suivi et conservation dans FINAL_CHECKS.json.

Tous les anciens noyaux, attestations et travaux concurrents sont conservés. Les six fichiers de la correction mine standard BGT restent identiques ; aucun bâtiment spécial du sel n'est rétabli. BR-I-CORE et TR-I-CORE gardent leurs reçus bornés ; Brixen et Trente restent régionalement bloqués. Aucun reçu humain BGT ou Obernberg, aucune écriture Git ou vanilla.

SC1-PASSAU-OUTLIERS reste **BLOCKED P1** : Vichtenstein/Riedenburg, Abteiland/Wolfstein/Freyung, frontière de 1765 et autres juridictions non attribuées, Rent-/Waldgütleramt et possessions dispersées restent ouverts. Le voisinage d'Obernberg, historiquement bavarois hors enclaves, demeure techniquement dans AUS avec le blocage SC2-AUSTRIA/Innviertel inchangé ; sa conservation définitive n'est pas approuvée. Ce noyau B n'est pas une clôture de l'ensemble passavien. Autres blocages canoniques inchangés.

**Prochaine action : protocole commun Berchtesgaden + Obernberg**, une nouvelle partie 1776, les deux installations, un mois, sauvegarde/rechargement. Aucun moteur exécuté par l'agent. La candidate indépendante suivante est identifiée après calcul du suivi sans être commencée.
''';(OUT/'REPORT.md').write_text(report,encoding='utf8')
    t=next(t for t in s['tasks'] if t['id']==TASK);reason='PS-OB-CORE ne représente que le marché et ses faubourgs approximatifs d’Obernberg. Vichtenstein/Riedenburg, Abteiland nord/Wolfstein/Freyung, Rannariedl/Jandelsbrunn après 1765, Obernzell/Wegscheid, Rent-/Waldgütleramt et droits dispersés demandent attribution politique et population comparables. Hals, Niederkessla après 1765, St. Nikola et Neuburg ne doivent pas être annexés depuis une propriété ou un diocèse. Le noyau B ne certifie pas leurs frontières ni le voisinage Innviertel, toujours bloqué dans SC2-AUSTRIA.'
    t.update(status='BLOCKED',installed_delivery_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',installed_sub_lots=[sub],installed_lots=['SERG_CLOSURE/'+TASK],implementation_report=[PREFIX+'REPORT.md',PREFIX+'B_PROPOSAL.md'],static_tests=dict(status='PASS',evidence=[PREFIX+'VALIDATION.json']),runtime_validation=dict(required=True,status='NOT_RUN',attestation=None,scope=sub['scope'],new_details_invented=False,protocol=PREFIX+'PLAYER_TEST_PROTOCOL.md'),blocking_reason=reason,residual_uncertainty=reason+' Population arrondie et point local automatique à vérifier ; aucune attestation humaine nouvelle.',decision=None,current_delivery_note='Obernberg PS-OB-CORE : PAS existant, quatre cellules xEDC000 depuis AUS xFDA6CB 179→175, 1400 habitants transférés ; ancien PAS/Bavière 14267 et quarante cellules inchangés, total PAS 15667. Aucun bâtiment, pays, armée ou pacte ajouté. Registre 578→579, même emprise et neuf électeurs. Installations en attente, région BLOCKED P1, zéro point.',delivered_scope=dict(classification='B_OBERNBERG_MARKET_NUCLEUS',sub_lots=['PS-OB-CORE'],new_rgb=RGB,existing_tag='PAS',installed_cells=4,transferred_population=POP,cadastral_validation=False,full_principality_coverage=False),identified_problem=['Abteiland et possessions périphériques de Passau','Obernberg et Vichtenstein avant leur cession de 1782','Échanges de 1765 et distinction des biens médiats'],remaining_territorial_obligations=[dict(id=id,status='OPEN_NOT_VALIDATED',scope=scope) for id,scope in [('PO-NORTH','Abteiland north, Wolfstein/Freyung and western fringes'),('PO-EAST','Rannariedl/Jandelsbrunn west after 1765, Obernzell/Wegscheid versus Austrian eastern rights and Niederkessla'),('PO-VICHTENSTEIN','Vichtenstein/Riedenburg and their jurisdictions before 1782; comparable population'),('PO-SOUTH','Rent-/Waldguetleramt, St Nikola and Neuburg sovereignty distinctions, no corridor'),('PO-DISTANT','Distant and mediate possessions versus direct temporal sovereignty'),('PO-OBERNBERG-LIMITS','Limits beyond market/suburb B, separate parish and surrounding Innviertel jurisdictions')]])
    t['historical_sources'].append(PREFIX+'SOURCES.md:1');probe=copy.deepcopy(s);probe.pop('runtime_validation_hold',None);candidate=rm.progress(probe)['next_task'];assert candidate and candidate!=TASK
    s['mission_status']='BERCHTESGADEN_AND_OBERNBERG_PENDING_COMBINED_PLAYER_TEST'
    summary='Nouvelle partie 1776 : vérifier BG-I-CORE révisé et sa mine de sel standard sous-occupée, puis PS-OB-CORE, enclave PAS d’Obernberg de quatre cellules et 1400 habitants. Ancien noyau PAS de quarante cellules et capitale conservés ; total PAS 15667, droits impériaux sans dixième électeur. Vérifier les voisins et travaux concurrents, simuler un mois, sauvegarder/recharger ; résultats séparés pour les deux sous-lots, aucune validation humaine présumée.'
    s['runtime_validation_hold']=dict(task_id=TASK,pending_task_ids=[prior.TASK,TASK],protocol=PREFIX+'PLAYER_TEST_PROTOCOL.md',next_implementation_candidate=candidate,reason='Le joueur a autorisé une étape indépendante supplémentaire avant de tester les deux installations ensemble ; ne commencer aucune autre étape.',test_summary=summary,scope_note='Berchtesgaden et Passau-périphéries restent BLOCKED P1 ; seuls BG-I-CORE révisé et PS-OB-CORE sont installés en attente. Le reçu Brixen n’est pas étendu, l’Innviertel et les autres blocages restent ouverts. '+candidate+' identifiée sans commencement.')
    s['events'].append(dict(id='SERG-RM-0034',date='2026-10-24',kind='AUTHORIZED_INDEPENDENT_PASSAU_OUTLIER_WITH_COMBINED_PENDING_TEST',scope_version='1.0.0',source=PREFIX+'AUTHORIZATION.md',changes=[dict(task_id=TASK,before='NOT_STARTED',after='BLOCKED')],sub_lot_changes=[dict(id='PS-OB-CORE',before='NOT_STARTED',after='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION')],before_weight=82,after_weight=82,total_weight=235,before_percent='34.89',after_percent='34.89',evidence=[PREFIX+n for n in ['REPORT.md','VALIDATION.json','IMPLEMENTATION.json','PLAYER_TEST_PROTOCOL.md']],note=t['current_delivery_note']+' '+reason+' Mine standard de Berchtesgaden conservée sans reçu humain ; test commun autorisé par le joueur. Candidate suivante '+candidate+' identifiée seulement. 82/235=34,89 % avant/après, 81 tâches, périmètre 1.0.0 inchangés.'))
    assert s['events'][:-1]==b['roadmap']['events'];assert [x for x in s['tasks'] if x['id']!=TASK]==[x for x in b['roadmap']['tasks'] if x['id']!=TASK]
    p=rm.progress(s);assert (p['earned_weight'],p['total_weight'],p['percent'],p['qualified_tasks'],p['next_task'])==(82,235,'34.89',24,TASK),p
    assert not rm.structural_errors(s),rm.structural_errors(s);rm.write_json(rm.OUT/'ROADMAP_STATE.json',s)
    with contextlib.redirect_stdout(io.StringIO()):rm.render()
    checked=rm.check();dump('TRACKER_VALIDATION.json',checked);assert checked['status']=='PASS',checked;dump('TRACKER_PRESERVATION.json',dict(other_80_tasks_unchanged=True,previous_33_events_unchanged=True,points_awarded=0,next_candidate=candidate,combined_pending_tasks=[prior.TASK,TASK]));print('Tracker PASS; joint test pending; next candidate',candidate,flush=True)

def tests():
    import serg_sc4_ligurian_fiefs as lig
    known={f['id'] for f in load(salt.OUT/'TESTS.json')['failed']}|{'test_serg_sc1_berchtesgaden.BerchtesgadenContracts.test_current_cumulative_tail'}
    modules=lig.MODULES+['test_serg_sc4_piombino','test_serg_sc4_massa_carrara','test_serg_sc1_trento','test_serg_sc1_brixen','test_serg_sc1_berchtesgaden','test_serg_sc1_passau_outliers']
    for label,names in [('SCOPED_TESTS',['test_serg_sc1_passau_outliers']),('TESTS',modules)]:
        stream=io.StringIO();r=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(names));failed=[dict(id=t.id(),traceback=s) for t,s in r.failures+r.errors];unknown=[f for f in failed if f['id'] not in known]
        (OUT/(label+'.log')).write_text(stream.getvalue(),encoding='utf8');dump(label+'.json',dict(task_ids=[TASK],status='FAIL' if unknown else 'OBSOLETE_SNAPSHOT_ASSERTIONS_ONLY' if failed else 'PASS',total=r.testsRun,passed=r.testsRun-len(failed)-len(r.skipped),failed=failed,skipped=[dict(id=t.id(),reason=s) for t,s in r.skipped],unexplained_failures=unknown,old_tests_unchanged=True,automated_engine_test=False));print(label,r.testsRun-len(failed)-len(r.skipped),'/',r.testsRun,'unexplained',len(unknown),flush=True);assert not unknown,unknown
    dump('TEST_REVIEW.json',dict(classification='Eight fixed-final-layer expectations plus one old absence-of-Brixen-receipt expectation; current tail and real partial receipts covered without changing old tests.',classified_ids=sorted(known),new_failure_relative_to_previous='Berchtesgaden historical final-tail assertion only',unexplained_failures=[],old_tests_not_modified=True))

def finalize():
    b=load(OUT/'BASELINE.json');s=load(rm.OUT/'ROADMAP_STATE.json');p=rm.progress(s);cur=prior.italian.runtime_hashes();checked=rm.check();dump('TRACKER_VALIDATION_FINAL.json',checked);candidate=s['runtime_validation_hold']['next_implementation_candidate'];tests=load(OUT/'TESTS.json');scoped=load(OUT/'SCOPED_TESTS.json');checks={}
    checks['Current runtime equals successfully validated bytes']=cur==load(OUT/'SESSION_AFTER_STATIC.json')['hashes']
    checks['Canonical validator PASS']=checked['status']=='PASS'
    checks['82 of 235 and 24 of 81 unchanged']=(p['earned_weight'],p['total_weight'],p['percent'],p['qualified_tasks'],len(s['tasks']))==(82,235,'34.89',24,81)
    checks['All other 80 tasks unchanged']=[t for t in s['tasks'] if t['id']!=TASK]==[t for t in b['roadmap']['tasks'] if t['id']!=TASK]
    checks['Previous 33 events unchanged']=s['events'][:-1]==b['roadmap']['events'] and s['events'][-1]['id']=='SERG-RM-0034'
    checks['All prior qualifications retained']=rm.qualifications(s)==rm.qualifications(b['roadmap'])
    checks['Joint protocol covers two still-pending installations']=set(s['runtime_validation_hold']['pending_task_ids'])=={prior.TASK,TASK} and s['runtime_validation_hold']['protocol']==PREFIX+'PLAYER_TEST_PROTOCOL.md' and p['next_task']==TASK
    for id in [prior.TASK,TASK]:
        t=next(t for t in s['tasks'] if t['id']==id);checks['No new human receipt '+id]=t['status']=='BLOCKED' and t['installed_delivery_status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' and t['runtime_validation']['attestation'] is None
    checks['No next independent stage started']=next(t for t in s['tasks'] if t['id']==candidate)['status']=='NOT_STARTED'
    checks['All old nested proofs and receipts retained']=all(sha(ROOT/rel)==h for rel,h in b['proofs'].items() if Path(rel).parent!=rm.OUT.relative_to(ROOT))
    tools=[rel for rel,h in b['tools'].items() if sha(ROOT/rel)!=h];checks['Only appended old registry guard changed']=tools==['tools/map2l_registry.py']
    checks['Native Berchtesgaden mine correction untouched']=all(cur[rel]==b['hashes'][rel] for rel in load(salt.OUT/'FILES_MODIFIED.json')['runtime_files'])
    checks['New tests pass all cumulative failures classified']=scoped['status']=='PASS' and not tests['unexplained_failures'] and len(tests['failed'])==9 and len(tests['skipped'])==1
    checks['Both source and native maps and joint protocol present']=all((OUT/n).is_file() for n in ['BEFORE_AFTER.png','SEUTTER_INN_DETAIL.png','SOURCES.md','SOURCE_READING.json','B_PROPOSAL.md','REPORT.md','PLAYER_TEST_PROTOCOL.md','JURISDICTION_MATRIX.csv'])
    diff=subprocess.run(['git','diff','--check'],cwd=ROOT,text=True,capture_output=True);white=[line for line in diff.stdout.splitlines() if 'trailing whitespace.' in line];checks['Only four inherited whitespace findings']=diff.returncode==2 and len(white)==4 and all(line.startswith('common/history/pops/00_west_europe.txt:') for line in white);dump('DIFF_CHECK.json',dict(returncode=diff.returncode,findings=white,inherited_count=4,stderr=diff.stderr))
    git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip();checks['Git HEAD main index preserved']=git('rev-parse','HEAD')==b['git']['head'] and git('branch','--show-current')==b['git']['branch'] and sha(ROOT/'.git/index')==b['git']['index']
    v=dict(task_ids=[TASK,prior.TASK],status='PASS' if all(checks.values()) else 'FAIL',passed=sum(checks.values()),total=len(checks),failed=[n for n,ok in checks.items() if not ok],checks=checks,automated_engine_test=False);dump('FINAL_CHECKS.json',v);print('Final checks',v['passed'],'/',v['total'],v['failed'],flush=True);assert not v['failed']
    with (OUT/'REPORT.md').open('a',encoding='utf8') as f:f.write('\nRésultats finaux exécutés : '+str(scoped['passed'])+'/'+str(scoped['total'])+' contrats ciblés, '+str(tests['passed'])+'/'+str(tests['total'])+' cumulatifs réussis, neuf assertions anciennes classées et une exclusion héritée ; aucun échec inexpliqué. '+str(v['passed'])+'/'+str(v['total'])+' contrôles finaux PASS. Prochaine candidate '+candidate+' identifiée sans commencement.\n')
    dump('SESSION_AFTER.json',dict(progress=p,hashes=cur,git=b['git'],previous_nested_proofs_preserved=True))
    manifest={rel:sha(ROOT/rel) for rel in load(OUT/'FILES_MODIFIED.json')['runtime_files']}
    for fp in OUT.rglob('*'):
        if fp.is_file() and fp.name!='DELIVERY_MANIFEST.json':manifest[fp.relative_to(ROOT).as_posix()]=sha(fp)
    for fp in rm.OUT.iterdir():
        if fp.is_file():manifest[fp.relative_to(ROOT).as_posix()]=sha(fp)
    for rel in ['tools/map2l_registry.py','tools/serg_sc1_passau_outliers.py','tools/test_serg_sc1_passau_outliers.py',reg.active_registry_path().relative_to(ROOT).as_posix()]+load(salt.OUT/'FILES_MODIFIED.json')['runtime_files']:manifest[rel]=sha(ROOT/rel)
    dump('DELIVERY_MANIFEST.json',dict(task_ids=[TASK,prior.TASK],files=manifest,installed_sub_lots=['PS-OB-CORE','BG-I-CORE_REVISED_ORDINARY_SALT_MINE'],installation_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',regional_statuses={TASK:'BLOCKED',prior.TASK:'BLOCKED'},no_human_receipt=True,automated_engine_test=False));assert all(sha(ROOT/rel)==h for rel,h in manifest.items());print('Final delivery manifest verified',len(manifest),'files; next',candidate,'not started',flush=True)

if __name__=='__main__':globals()[sys.argv[1]]()
