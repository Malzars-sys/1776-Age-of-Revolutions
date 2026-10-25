"""Guarded Massa-Carrara pass; never grants a human runtime receipt."""
import collections as C
import contextlib, copy, csv, io, json, os, re, shutil, subprocess, sys, unittest
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import serg_sc4_piombino as prior
import serg_sc4_italian_states as italian
ROOT=prior.ROOT; rm=prior.rm; core=prior.core; reg=prior.reg; sha=prior.sha
TASK='SC4-MASSA-CARRARA'; OUT=rm.OUT/TASK; PREFIX='docs/reports/map/SERG_CLOSURE/'+TASK+'/'
TAG='MCA'; RGB='xEDBC00'; PARENT='xF08021'; SID='STATE_EMILIA'; POP=10000
CELLS=[[4325,1029],[4326,1029],[4326,1030],[4327,1030],[4327,1031],[4328,1030],[4328,1031],[4328,1032]]
MISSION=Path('C:/Users/simeo/.codex/attachments/1ff40f8a-d0d5-4ea1-aa9d-cfa8fb88d2f9/Texte collé.txt')
os.environ['GIT_OPTIONAL_LOCKS']='0'
def load(p):return rm.load_json(p)
def dump(n,o):rm.write_json(OUT/n,o)
def capture():
    assert not (OUT/'BASELINE.json').exists()
    state=load(rm.OUT/'ROADMAP_STATE.json'); checked=rm.check()
    assert checked['status']=='PASS' and rm.progress(state)['next_task']==TASK
    manifest=load(prior.OUT/'DELIVERY_MANIFEST.json')
    print('Manifest type/keys',type(manifest).__name__,list(manifest)[:5],flush=True)
    entries=manifest.get('sha256',manifest.get('files',manifest))
    if isinstance(entries,list):entries={r['path']:r['sha256'] for r in entries}
    changed=[p for p,h in entries.items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h]
    assert not changed,changed
    hashes=italian.runtime_hashes();old=load(prior.OUT/'SESSION_AFTER.json')['hashes']
    concurrent=sorted(p for p in set(hashes)|set(old) if hashes.get(p)!=old.get(p))
    inv=core.qa.inventory()
    git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
    OUT.mkdir(exist_ok=True)
    reports={p.relative_to(ROOT).as_posix():sha(p) for p in rm.OUT.rglob('*') if p.is_file() and OUT not in p.parents}
    dump('BASELINE.json',dict(roadmap=state,inventory=inv,hashes=hashes,registry=load(reg.active_registry_path()),reports=reports,
        tools={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'tools').glob('*.py') if p.name!=Path(__file__).name},
        git=dict(head=git('rev-parse','HEAD'),branch=git('branch','--show-current'),index_sha256=sha(ROOT/'.git/index'),status=git('status','--short','--untracked-files=normal')),
        prior_delivery_changes=changed,concurrent_runtime_changes=concurrent))
    shutil.copyfile(ROOT/'map_data/provinces.png',OUT/'provinces_before.png')
    shutil.copyfile(MISSION,OUT/'USER_MISSION.txt')
    print('Baseline captured; concurrent changes:',concurrent,flush=True)

def acknowledge():
    b=load(OUT/'BASELINE.json');state=load(rm.OUT/'ROADMAP_STATE.json');assert state==b['roadmap']
    assert state['events'][-1]['id']=='SERG-RM-0023'
    dest=prior.OUT/'USER_ACKNOWLEDGMENT_2026_10_23.json';assert not dest.exists()
    shutil.copyfile(MISSION,prior.OUT/'USER_BLOCKER_MISSION_2026_10_23.txt')
    rm.write_json(dest,dict(task_ids=[prior.TASK],status='USER_ACKNOWLEDGED_BLOCKER',date='2026-10-23',source=str(MISSION),
        no_functional_changes_acknowledged=True,new_engine_test_required=False,retention_approved=False,deferral_approved=False,
        runtime_validation_granted=False,points_awarded=0,physical_elba_evidence_preserved=True,
        remaining_problem='Political partition of 1776, RGB, populations and rights; no repetition of physical island audit.'))
    t=next(t for t in state['tasks'] if t['id']==prior.TASK)
    t['current_delivery_note']='Blocage P0 Piombino expressément maintenu par le joueur le 23 octobre. Diagnostic sans installation : aucun nouveau test moteur requis, aucun PASS, report ou maintien définitif approuvé, aucun point. Preuves physiques Elbe conservées ; leur audit ne doit pas être répété. Résolution politique encore nécessaire.'
    action=' Action de déblocage : reprendre B_PROPOSAL.md, confronter les cartes Kindt 1776 (ASFi N155) et Bellin 1764 aux centres/ressorts déjà inventoriés ; produire une liste de cellules B PIO/TUS/SIC et un bilan démographique, puis choisir B1 ou installer le seul noyau continental B2 en gardant le partage insulaire bloqué. Réutiliser ELBA_NATIVE_EVIDENCE.json sans recompter l’île ; aucun bonus administratif toscan ne remplace cette souveraineté.'
    t['blocking_reason']+=action;t['residual_uncertainty']=t['blocking_reason']
    rel=dest.relative_to(ROOT).as_posix();t['implementation_report'].append(rel)
    state['events'].append(dict(id='SERG-RM-0024',date='2026-10-23',kind='USER_ACKNOWLEDGED_BLOCKER',scope_version='1.0.0',source=rel,
        changes=[dict(task_id=prior.TASK,before='BLOCKED',after='BLOCKED')],before_weight=82,after_weight=82,total_weight=235,before_percent='34.89',after_percent='34.89',
        evidence=[rel],note=t['current_delivery_note']+action))
    assert state['events'][:-1]==b['roadmap']['events']
    assert [t for t in state['tasks'] if t['id']!=prior.TASK]==[t for t in b['roadmap']['tasks'] if t['id']!=prior.TASK]
    assert rm.progress(state)['next_task']==TASK and not rm.structural_errors(state)
    rm.write_json(rm.OUT/'ROADMAP_STATE.json',state)
    with contextlib.redirect_stdout(io.StringIO()):rm.render()
    ck=rm.check();dump('ENTRY_TRACKER_VALIDATION.json',ck);assert ck['status']=='PASS'
    dump('STATE_AFTER_PIOMBINO_ACK.json',state)
    print('Piombino BLOCKED acknowledged; Massa-Carrara selected P0; 82/235',flush=True)

def survey():
    b=load(OUT/'BASELINE.json');inv=b['inventory'];a=core.packed(OUT/'provinces_before.png')
    owners={r['key'][0]:r['key'][1:] for r in inv['owners']}
    rows=[r for r in load(prior.OUT/'NATIVE_INVENTORY.json')['provinces'] if r['state_before'] in {'STATE_EMILIA','STATE_TUSCANY'}]
    gen=[r for r in load(prior.prior.OUT/'NATIVE_INVENTORY.json')['provinces'] if r['owner_before']=='GEN']
    dump('NATIVE_INVENTORY.json',dict(provinces=rows+gen,countries={k:v for k,v in inv['countries'].items() if k in {'MOD','LUC','GEN','TUS','MAC','MAS','MCR'}},
        populations=[r for r in inv['regional_pop'] if r['key'][1] in {'MOD','LUC','GEN','TUS'}],buildings=[r for r in inv['buildings'] if r['key'][1] in {'MOD','LUC','GEN','TUS'}],
        units=[r for r in inv['units'] if r['key'][0] in {'MOD','LUC','GEN','TUS'}]))
    print('Image shape',a.shape,'candidate tags',{t:t in inv['countries'] for t in ['MAS','MAC','MCR']},flush=True)
    for r in rows+gen:print(r['rgb'],r['owner_before'],r['cells_before'],r['bounds'],flush=True)
    x0,y0,x1,y1,s=4300,1005,4350,1050,18
    im=Image.new('RGB',((x1-x0)*s+100,(y1-y0)*s+100),'#faf8ef');d=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',12)
    colors={'GEN':'#cfb3d1','PAR':'#b4d2a6','MOD':'#e5c581','LUC':'#e9a0a0','TUS':'#b7bfdc'}
    for y in range(y0,y1):
        for x in range(x0,x1):
            rgb='x'+format(int(a[y,x]),'06X');u,v=60+(x-x0)*s,40+(y-y0)*s
            d.rectangle((u,v,u+s,v+s),fill=colors.get(owners.get(rgb,['',''])[1],'#dfedf2'),outline='#aaa')
            if a[y,x]!=a[y,x-1]:d.line((u,v,u,v+s),fill='#202020',width=2)
            if a[y,x]!=a[y-1,x]:d.line((u,v,u+s,v),fill='#202020',width=2)
    for x in range(x0,x1,2):d.text((60+(x-x0)*s,20),str(x),font=font,fill='black')
    for y in range(y0,y1,2):d.text((10,40+(y-y0)*s),str(y),font=font,fill='black')
    d.text((10,im.height-40),'GEN violet / PAR vert / MOD ocre / LUC rose / TUS bleu. Grille native AVANT.',font=font,fill='black')
    im.save(OUT/'NATIVE_BEFORE.png')
    p=ROOT/'docs/reports/map/MAP1B/MAP1B_GEOGRAPHIC_EVIDENCE/lombardy_1750.jpg';im=Image.open(p);print('Map size',im.size,flush=True)
    w,h=im.size;im.crop((int(w*.08),int(h*.70),int(w*.29),int(h*.93))).save(OUT/'ROBERT_1750_MASSA_DETAIL.png')

def prepare():
    b=load(OUT/'BASELINE.json');a=core.packed(OUT/'provinces_before.png');assert italian.runtime_hashes()==b['hashes']
    assert TAG not in b['inventory']['countries'] and RGB not in b['inventory']['geometry'] and not np.any(a==int(RGB[1:],16))
    assert not any(re.search(r'\bMCA\b',p.read_text(encoding='utf-8-sig')) for folder in ['common/country_definitions','common/flag_definitions'] for p in core.qa.effective(ROOT,core.qa.GAME,folder))
    after=a.copy()
    for x,y in CELLS:assert a[y,x]==int(PARENT[1:],16);after[y,x]=int(RGB[1:],16)
    yy,xx=np.where(after==int(PARENT[1:],16));assert len(prior.components(xx,yy))==1
    rows=[]
    for rgb,tag in [(PARENT,'MOD'),(RGB,TAG)]:
        yy,xx=np.where(after==int(rgb[1:],16));points=sorted([[int(x),int(y)] for x,y in zip(xx,yy)])
        rows.append(dict(rgb=rgb,parent_rgb=PARENT,state=SID,previous_owner='MOD',owner=tag,pixels=len(points),cells=points,confidence='B_POLITICAL_APPROXIMATION' if tag==TAG else 'RETAINED_NOT_CERTIFIED'))
    geo=dict(parents=[PARENT],assignments=rows,new_provinces=[dict(rgb=RGB,parent_rgb=PARENT)],new_members=[TAG],free_cities=[],selected_option='COASTAL_RESIDENCE_CORE',classification='B_POLITICAL_APPROXIMATION',historical_cadastral_precision=False,hub_rebindings=[])
    files={};originals={}
    def old(p):
        assert sha(ROOT/p)==b['hashes'][p];raw=(ROOT/p).read_bytes().decode('utf8');originals[p]=raw;return raw
    p='common/history/states/00_states.txt';raw=old(p);n=core.state(raw,SID)
    files[p]=core.edits(raw,[(n.end-1,n.end-1,'\n\t\t# SC4-MASSA-CARRARA: coastal political nucleus; not all Lunigiana.\n\t\tcreate_state = { country = c:MCA owned_provinces = { xEDBC00 } }\n\t')]).replace('\t\n\t\t# SC4-MASSA-CARRARA:','\n\t\t# SC4-MASSA-CARRARA:')
    p='map_data/state_regions/01_south_europe.txt';raw=old(p);n=next(n for n in core.cw.parse(raw.lstrip('\ufeff')) if n.key==SID)
    # Preserve original byte offsets even in a BOM-bearing input.
    off=1 if raw.startswith('\ufeff') else 0;f=n.children('provinces')[0];frag=raw[f.start+off:f.end+off];assert frag.count('"'+PARENT+'"')==1
    files[p]=core.edits(raw,[(f.start+off,f.end+off,frag.replace('"'+PARENT+'"','"'+PARENT+'" "'+RGB+'"'))])
    # The administrative resource is shared by the existing split state. The
    # prime-land parent is expanded to its exact child to conserve its area.
    n=next(n for n in core.cw.parse(files[p].lstrip('\ufeff')) if n.key==SID);f=n.children('prime_land')[0];frag=files[p][f.start+off:f.end+off]
    files[p]=core.edits(files[p],[(f.start+off,f.end+off,frag.replace('"'+PARENT+'"','"'+PARENT+'" "'+RGB+'"'))])
    refs=[dict(state=SID,field='prime_land',before=core.values(n,'prime_land'),after=[PARENT,RGB,'x0B3B43'])]
    p='map_data/province_terrains.txt';raw=old(p);terrain=dict((k.upper(),v) for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',raw));files[p]=raw+'\n'+RGB+'="'+terrain[PARENT.upper()]+'"\n'
    p='common/history/pops/01_south_europe.txt';raw=old(p);n=core.region(raw,SID,'MOD');pops=n.children('create_pop');assert len(pops)==1 and pops[0].one('culture')=='north_italian' and pops[0].one('religion') is None and pops[0].one('pop_type') is None
    f=pops[0].children('size')[0];amount=int(f.value);raw=core.edits(raw,[(f.start,f.end,'size = '+str(amount-POP))]);files[p]=core.append(raw,SID,TAG,'\n\t\t\tcreate_pop = { culture = north_italian size = '+str(POP)+' }\n').replace('\t\n\t\tregion_state:MCA','\n\t\tregion_state:MCA')
    defs='MCA = { color = { 167 85 107 } country_type = recognized tier = principality cultures = { north_italian } religion = catholic capital = STATE_EMILIA }\n'
    files['common/country_definitions/1776_sc4_massa_carrara.txt']=defs
    files['common/history/countries/mca - massa carrara.txt']=(ROOT/'common/history/countries/mod - modena.txt').read_text(encoding='utf-8-sig').replace('c:MOD','c:MCA')
    files['common/history/characters/1776_sc4_massa_carrara.txt']='CHARACTERS = { c:MCA ?= { create_character = { first_name = aor1776_mca_first last_name = aor1776_mca_last historical = yes female = yes culture = north_italian religion = rel:catholic ruler = yes birth_date = 1725.6.29 interest_group = ig_landowners ideology = ideology_reformer } } }\n'
    files['common/government_types/00_1776_sc4_massa_carrara.txt']='gov_aor1776_massa_carrara = { transfer_of_power = hereditary male_ruler = "aor1776_mca_duke" female_ruler = "aor1776_mca_duchess" possible = { c:MCA ?= this has_law = law_type:law_monarchy } on_government_type_change = { change_to_hereditary = yes } on_post_government_type_change = { post_change_to_hereditary = yes } }\n'
    # This independent court is a new service, never a transfer of the validated
    # Modenese administration. No modern port, quarry owner or army is invented.
    files['common/history/buildings/1776_sc4_massa_carrara.txt']='BUILDINGS = { s:STATE_EMILIA = { region_state:MCA = { create_building = { building = "building_government_administration" add_ownership = { country = { country = "c:MCA" levels = 1 } } reserves = 1 activate_production_methods = { "pm_hereditary_bureaucrats" "pm_religious_bureaucrats" "pm_simple_organization" } } } } }\n'
    # Simple identification banner, not a certified historical achievement.
    files['common/coat_of_arms/coat_of_arms/1776_sc4_massa_carrara.txt']='aor1776_massa_carrara = { pattern = "pattern_solid.tga" color1 = "white" colored_emblem = { texture = "ce_solid.dds" color1 = "red" instance = { scale = { 0.18 1.0 } rotation = 45 } } }\n'
    files['common/flag_definitions/1776_sc4_massa_carrara.txt']='MCA = { flag_definition = { coa = aor1776_massa_carrara priority = 100 allow_overlord_canton = no } }\n'
    for lang in ['french','english']:
        fr=lang=='french';pairs={'MCA':'Massa-Carrare' if fr else 'Massa-Carrara','MCA_ADJ':'massais' if fr else 'Massese','aor1776_mca_first':'Marie-Thérèse' if fr else 'Maria Teresa','aor1776_mca_last':'Cybo-Malaspina','aor1776_mca_duke':'Duc' if fr else 'Duke','aor1776_mca_duchess':'Duchesse' if fr else 'Duchess','gov_aor1776_massa_carrara':'Duché de Massa et principauté de Carrare' if fr else 'Duchy of Massa and Principality of Carrara','gov_aor1776_massa_carrara_desc':('La souveraine de Massa et de Carrare gouverne ses États avec sa chambre ducale et ses officiers de justice. Le mariage avec la maison d’Este maintient des liens dynastiques sans effacer ces institutions.' if fr else 'The sovereign of Massa and Carrara governs her states through the ducal chamber and officers of justice. Marriage into the House of Este maintains dynastic ties while these institutions remain distinct.')+r'\n\n$TRANSFER_OF_POWER_NAME_DESC$'}
        files['localization/'+lang+'/1776_sc4_massa_carrara_l_'+lang+'.yml']='\ufeffl_'+lang+':\n'+''.join(' '+k+':0 "'+v+'"\n' for k,v in pairs.items())
    previous=[r for r in b['registry'] if r['state']==SID];assert any(r['rgb']==PARENT and r['beneficiary']=='MOD' for r in previous)
    addition=dict(rgb=RGB,state=SID,beneficiary=TAG,basis='SC4-MASSA-CARRARA: eight-cell coastal residence nucleus B; no complete Lunigiana claim')
    updated=sorted(previous+[addition],key=lambda r:r['rgb']);migration=dict(replaced_regions=[SID],previous=previous,updated=updated,new_members=[TAG],free_cities=[],new_provinces=geo['new_provinces'],geometry='SERG_CLOSURE/'+TASK+'/GEOMETRY.json',region_reference_changes=refs,extent_added_cells=[],extent_removed_cells=[],country_additions={TAG:core.qa.signature(core.cw.parse(defs)[0])})
    rel='docs/reports/map/MAP2L/IMPERIAL_DE_JURE_REGISTRY.json';originals[rel]=(ROOT/rel).read_text(encoding='utf-8-sig');assert load(ROOT/rel)==b['registry'];files[rel]=json.dumps(sorted(b['registry']+[addition],key=lambda r:(r['rgb'],r['state'],r['beneficiary'])),ensure_ascii=False,indent=2)+'\n'
    for p,raw in files.items():
        if p not in originals:assert not (ROOT/p).exists(),p
        if p.endswith('.txt'):core.cw.parse(raw.lstrip('\ufeff'))
    dump('GEOMETRY.json',geo);dump('REGISTRY_MIGRATION.json',migration);dump('TEXT_BEFORE.json',originals);dump('EXPECTED_TEXT.json',files)
    dump('DEMOGRAPHY.json',dict(transferred=POP,donor='MOD',recipient=TAG,donor_before=amount,donor_after=amount-POP,culture='north_italian',religion='DEFAULT:north_italian = catholic',profession='unchanged: unspecified in source population',basis='Conservative rounded residence nucleus; Massa community counted 10224 in 1765, 10627 in 1801, not a census of the full duchy/principality or its outlying fiefs.',historical_full_state_population_not_claimed=True))
    Image.fromarray(np.stack([(after>>16)&255,(after>>8)&255,after&255],axis=-1).astype('uint8')).save(OUT/'provinces_candidate.png')
    print('Prepared 8 cells MOD -> MCA, 10000 existing people, one independent court; no union with MOD',flush=True)

def compiler_before():
    import map2k_imperial_system as compiler
    compiler.OUT=OUT;files=compiler.compile_system();diff=[]
    actual={}
    for p,raw in files.items():
        actual[p]=(ROOT/p).read_text(encoding='utf-8-sig');
        if raw.lstrip('\ufeff')!=actual[p]:diff.append(p)
    dump('COMPILER_BEFORE.json',dict(actual=actual,differences=diff));print('Compiler preflight',diff,flush=True);assert not diff

def install():
    b=load(OUT/'BASELINE.json');files=load(OUT/'EXPECTED_TEXT.json');originals=load(OUT/'TEXT_BEFORE.json')
    assert italian.runtime_hashes()==b['hashes'],'Review concurrent changes before installation'
    assert sha(ROOT/'.git/index')==b['git']['index_sha256']
    assert not load(OUT/'COMPILER_BEFORE.json')['differences']
    for p,raw in originals.items():assert (ROOT/p).read_bytes().decode('utf8').lstrip('\ufeff')==raw.lstrip('\ufeff'),p
    for p,raw in files.items():
        dest=ROOT/p
        if p not in originals:assert not dest.exists(),p
        dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw.encode('utf8'))
    shutil.copyfile(OUT/'provinces_candidate.png',ROOT/'map_data/provinces.png')
    print('Functional nucleus installed; imperial generation next',flush=True)

def imperial():
    import map2k_imperial_system as compiler
    compiler.OUT=OUT;before=load(OUT/'COMPILER_BEFORE.json');files=compiler.compile_system();changed=[]
    for p,raw in files.items():
        if raw.lstrip('\ufeff')==before['actual'][p]:continue
        assert (ROOT/p).read_text(encoding='utf-8-sig')==before['actual'][p],p
        bom=(ROOT/p).read_bytes().startswith(b'\xef\xbb\xbf');(ROOT/p).write_bytes((('\ufeff' if bom and not raw.startswith('\ufeff') else '')+raw).encode('utf8'));changed.append(p)
    dump('IMPERIAL_EXPECTED.json',files);dump('IMPERIAL_FILES.json',changed);print('Imperial files updated',changed,flush=True)

def maps():
    b=load(OUT/'BASELINE.json');before=core.packed(OUT/'provinces_before.png');after=core.packed(ROOT/'map_data/provinces.png')
    owners={r['key'][0]:r['key'][2] for r in b['inventory']['owners']};owners[RGB]=TAG
    x0,y0,x1,y1,s=4317,1021,4340,1044,22
    im=Image.new('RGB',(2*((x1-x0)*s+70),(y1-y0)*s+150),'#faf8ef');dr=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',13)
    colors={'MOD':'#dec27f','GEN':'#c8a0c7','LUC':'#e4aaaa','TUS':'#b9c5df','PAR':'#bbd9b0',TAG:'#a7556b'}
    for k,(arr,title) in enumerate([(before,'AVANT : noyau sous MOD'),(after,'INSTALLE B : MCA, 8 cellules')]):
        ox=k*((x1-x0)*s+70);dr.text((ox+10,10),title,font=font,fill='black')
        for y in range(y0,y1):
            for x in range(x0,x1):
                rgb='x'+format(int(arr[y,x]),'06X');u=ox+45+(x-x0)*s;v=55+(y-y0)*s
                dr.rectangle((u,v,u+s,v+s),fill=colors.get(owners.get(rgb),'#dfedf2'),outline='#aaa')
                if arr[y,x]!=arr[y,x-1]:dr.line((u,v,u,v+s),fill='#444',width=2)
                if arr[y,x]!=arr[y-1,x]:dr.line((u,v,u+s,v),fill='#444',width=2)
        for x in range(x0,x1,3):dr.text((ox+45+(x-x0)*s,35),str(x),font=font,fill='black')
        for y in range(y0,y1,3):dr.text((ox+5,55+(y-y0)*s),str(y),font=font,fill='black')
    dr.text((10,im.height-65),'MCA pourpre / MOD ocre / LUC rose / GEN violet. Nouveau RGB xEDBC00.',font=font,fill='black')
    dr.text((10,im.height-44),'Noyau politique de residence ; ni cadastre ni ensemble de la Lunigiana.',font=font,fill='black')
    dr.text((10,im.height-23),'Capitale technique dans la portion MCA de STATE_EMILIA ; aucun locator voisin deplace.',font=font,fill='black')
    im.save(OUT/'BEFORE_AFTER.png')

def clean_new_whitespace():
    files=load(OUT/'EXPECTED_TEXT.json');changes=[]
    for p,needle,replacement in [('common/history/states/00_states.txt','\t\n\t\t# SC4-MASSA-CARRARA:','\n\t\t# SC4-MASSA-CARRARA:'),('common/history/pops/01_south_europe.txt','\t\n\t\tregion_state:MCA','\n\t\tregion_state:MCA')]:
        old=files[p];assert (ROOT/p).read_bytes()==old.encode('utf8')
        assert old.count(needle)==1
        new=old.replace(needle,replacement)
        assert [core.qa.signature(n) for n in core.cw.parse(old.lstrip('\ufeff'))]==[core.qa.signature(n) for n in core.cw.parse(new.lstrip('\ufeff'))]
        (ROOT/p).write_bytes(new.encode('utf8'));files[p]=new;changes.append(p)
    dump('EXPECTED_TEXT.json',files);dump('WHITESPACE_POLISH.json',dict(files=changes,only_new_empty_line_tabs_removed=True,parsed_syntax_identical=True,old_four_whitespace_findings_untouched=True))

def validate():
    b=load(OUT/'BASELINE.json');old=b['inventory'];inv=core.qa.inventory();current=italian.runtime_hashes();files=load(OUT/'EXPECTED_TEXT.json');imperial=load(OUT/'IMPERIAL_EXPECTED.json');checks=[]
    def ck(name,ok,detail=None):checks.append(dict(name=name,passed=bool(ok),detail=detail))
    a=core.packed(OUT/'provinces_before.png');z=core.packed(ROOT/'map_data/provinces.png');yy,xx=np.where(a!=z)
    ck('Exactly eight declared raster cells changed',sorted(zip(map(int,xx),map(int,yy)))==sorted(map(tuple,CELLS)))
    ck('All changed pixels MOD parent to new MCA color',all(int(a[y,x])==int(PARENT[1:],16) and int(z[y,x])==int(RGB[1:],16) for x,y in CELLS))
    ck('Native map dimensions unchanged',a.shape==z.shape==(3616,8192))
    for rgb,count in [(PARENT,108),(RGB,8)]:
        yy,xx=np.where(z==int(rgb[1:],16));ck('Connected '+rgb,len(xx)==count and len(prior.components(xx,yy))==1)
    eo=core.qa.counter(old['owners']);eo[RGB,SID,TAG]=1;ck('Only declared new sovereign owner',core.qa.counter(inv['owners'])==eo)
    eg=dict(old['geometry']);eg[RGB]=SID;ck('Only one new province in Emilia',inv['geometry']==eg)
    ck('One new incorporated split state',inv['states']==sorted(old['states']+[[SID,TAG]]))
    et=dict(old['state_types']);et[SID+'|'+TAG]='incorporated_default';ck('All old state types retained',inv['state_types']==et)
    defs=core.cw.parse(files['common/country_definitions/1776_sc4_massa_carrara.txt'])[0];ec=dict(old['countries']);ec[TAG]=core.qa.signature(defs);ck('Old country definitions intact and MCA distinct',inv['countries']==ec)
    for field in ['pops','resolved_demographics','units','errors','duplicates']:
        ck('World conservation '+field,inv[field]==old[field])
    ep=core.qa.counter(old['regional_pop']);ep[SID,'MOD','north_italian','DEFAULT:north_italian']-=POP;ep[SID,TAG,'north_italian','DEFAULT:north_italian']=POP
    ck('Exact 10000 transfer MOD to MCA; no other regional population change',core.qa.counter(inv['regional_pop'])==ep)
    popnode=core.region(files['common/history/pops/01_south_europe.txt'],SID,TAG).children('create_pop')[0]
    ck('Culture religion and professions preserved',[(n.key,n.value) for n in popnode.children()]==[('culture','north_italian'),('size','10000')])
    admin=core.region(files['common/history/buildings/1776_sc4_massa_carrara.txt'],SID,TAG).children('create_building')[0]
    eb=core.qa.counter(old['buildings']);eb[SID,TAG,core.qa.signature(admin)]+=1;ck('All existing buildings/property intact, one new court',core.qa.counter(inv['buildings'])==eb)
    el=core.qa.counter(old['building_levels_written']);el['building_government_administration']+=1;ck('Only one explicit administrative level added',core.qa.counter(inv['building_levels_written'])==el)
    ck('New court nationally owned',admin.children('add_ownership')[0].children('country')[0].one('country')=='"c:MCA"')
    ledger=load(reg.active_registry_path());want=sorted(b['registry']+[dict(rgb=RGB,state=SID,beneficiary=TAG,basis='SC4-MASSA-CARRARA: eight-cell coastal residence nucleus B; no complete Lunigiana claim')],key=lambda r:(r['rgb'],r['state'],r['beneficiary']))
    ck('Exact additive registry: 575 rights',ledger==want and len(ledger)==len({r['rgb'] for r in ledger})==575)
    ck('Registry migration exact input',load(OUT/'REGISTRY_MIGRATION.json')['previous']==[r for r in b['registry'] if r['state']==SID])
    ck('Exact current cumulative tail',reg.approved_lot_dirs()[-2:]==[rm.OUT/'SC1-SALZBURG',OUT])
    ck('Physical imperial extent unchanged',np.array_equal(np.isin(a,[int(r['rgb'][1:],16) for r in b['registry']]),np.isin(z,[int(r['rgb'][1:],16) for r in ledger])))
    from map2k_patch import ELECTORS
    ck('MCA member, neither elector nor free city',TAG in reg.additional_members() and TAG not in reg.additional_free_cities() and TAG not in ELECTORS.values() and len(ELECTORS)==9)
    ck('SAR nine Piedmont rights unchanged',reg.member_region_overrides()=={'SAR':{'STATE_PIEDMONT'}} and [r for r in ledger if r['beneficiary']=='SAR']==[r for r in b['registry'] if r['beneficiary']=='SAR'])
    ck('No neighbor hubs moved',all(c['field']=='prime_land' for c in load(OUT/'REGISTRY_MIGRATION.json')['region_reference_changes']))
    before=(OUT/'TEXT_BEFORE.json');stp='map_data/state_regions/01_south_europe.txt'
    oldst=next(n for n in core.cw.parse(load(before)[stp].lstrip('\ufeff')) if n.key==SID);newst=next(n for n in core.cw.parse(files[stp].lstrip('\ufeff')) if n.key==SID)
    ck('Regional resources, arables, traits, sea exit and hub references intact',[core.qa.signature(n) for n in oldst.children() if n.key not in {'provinces','prime_land'}]==[core.qa.signature(n) for n in newst.children() if n.key not in {'provinces','prime_land'}])
    terrain={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',(ROOT/'map_data/province_terrains.txt').read_text(encoding='utf-8-sig'))};ck('Child inherits parent terrain',terrain[PARENT.upper()]==terrain[RGB.upper()])
    laws=italian.definitions('common/laws');effects=italian.definitions('common/scripted_effects');policy=prior.prior.initial_policy(TAG,effects,laws);dump('INITIAL_POLICY.json',policy)
    ck('Monarchy effective at start','law_monarchy' in policy['laws'].values())
    pmdefs=italian.definitions('common/production_methods');active=set(policy['laws'].values())
    for name in ['pm_simple_organization','pm_hereditary_bureaucrats','pm_religious_bureaucrats']:
        pm=pmdefs[name];unlock=set(core.values(pm,'unlocking_laws'));deny=set(core.values(pm,'disallowing_laws'));tech=set(core.values(pm,'unlocking_technologies'))
        ck('New court method actually available '+name,(not unlock or bool(unlock&active)) and not deny&active and tech<=set(policy['technologies']))
    char=files['common/history/characters/1776_sc4_massa_carrara.txt'];ck('Correct dated female sovereign',all(s in char for s in ['female = yes','birth_date = 1725.6.29','ruler = yes','culture = north_italian','rel:catholic']))
    ck('Configured capital points to own split state; engine placement pending',defs.one('capital')==SID and [SID,TAG] in inv['states'] and core.qa.counter(inv['owners'])[RGB,SID,TAG]==1)
    ck('No MOD annexation or puppet/personal union installed',all(not p.startswith(('common/history/diplomacy/','common/history/treaties/')) for p in files))
    for p,raw in files.items():ck('Exact installed candidate '+p,(ROOT/p).read_bytes()==raw.encode('utf8'))
    for p,raw in imperial.items():ck('Exact generated imperial file '+p,(ROOT/p).read_text(encoding='utf-8-sig')==raw.lstrip('\ufeff'))
    changed=sorted(p for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p));allowed=set(files)|set(load(OUT/'IMPERIAL_FILES.json'))|{'map_data/provinces.png'}
    ck('All other functional files and concurrent work byte-identical',set(changed)<=allowed,changed)
    oldreports=[p for p,h in b['reports'].items() if Path(p).parent!=rm.OUT.relative_to(ROOT) and (not (ROOT/p).exists() or sha(ROOT/p)!=h)]
    ck('All earlier nested proofs and receipts preserved',not oldreports,oldreports)
    toolchanges=[p for p,h in b['tools'].items() if sha(ROOT/p)!=h];ck('Only registry guard and partial-test handoff changed among old tools',set(toolchanges)=={'tools/map2l_registry.py','tools/serg_closure_roadmap.py'},toolchanges)
    git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
    ck('Git HEAD branch and index unchanged',git('rev-parse','HEAD')==b['git']['head'] and git('branch','--show-current')==b['git']['branch'] and sha(ROOT/'.git/index')==b['git']['index_sha256'])
    for p in [p for p in files if p.endswith('.yml')]:ck('Bilingual localization BOM '+p,(ROOT/p).read_bytes().startswith(b'\xef\xbb\xbf'))
    ck('No fictitious human receipt',not list(OUT.glob('RUNTIME_USER_ATTESTATION*')))
    for t in load(rm.OUT/'ROADMAP_STATE.json')['tasks']:
        if t['id'] in ['SC2-ANTERIOR-AUSTRIA','SC4-EXISTING-ITALIAN-STATES','SC4-SAVOY-NICE','SC4-LIGURIAN-FIEFS']:ck('Bounded previous receipt '+t['id'],rm.partial_runtime_evidence(t))
    v=dict(task_ids=[TASK],status='PASS' if all(c['passed'] for c in checks) else 'FAIL',total=len(checks),passed=sum(c['passed'] for c in checks),failed=[c['name'] for c in checks if not c['passed']],checks=checks,automated_engine_test=False,engine_executed=False)
    dump('VALIDATION.json',v);dump('SESSION_AFTER_STATIC.json',dict(inventory=inv,hashes=current));dump('FILES_MODIFIED.json',dict(task_ids=[TASK],runtime_files=changed,sha256={p:current[p] for p in changed},old_tools_changed=toolchanges))
    print('Static',v['passed'],'/',v['total'],v['failed'],flush=True);assert not v['failed'],v['failed']

def documentation():
    b=load(OUT/'BASELINE.json');v=load(OUT/'VALIDATION.json');files=load(OUT/'FILES_MODIFIED.json');inv=load(OUT/'SESSION_AFTER_STATIC.json')['inventory']
    (OUT/'AUTHORIZATION.md').write_text('# Autorisation et périmètre\n\nMission intégrale conservée dans `USER_MISSION.txt`, depuis '+str(MISSION)+'. Une seule étape nouvelle : SC4-MASSA-CARRARA, P0 sans dépendance, sélection confirmée par ENTRY_TRACKER_VALIDATION.json après reconnaissance du blocage Piombino. Trois règles permanentes appliquées ; recherche suivie de restitution souveraine B, noyau distinct et contrôlable. Aucun Git en écriture, aucune modification vanilla, aucun reçu humain nouveau.\n',encoding='utf8')
    sub=dict(id='MC-I-CORE',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',tag=TAG,state=SID,category='B',scope='Eight-cell coastal residence nucleus; 10000 existing north-Italian Catholics transferred from MOD, distinct sovereign Maria Teresa, ducal court and bounded imperial rights. Not full Carrara/Lunigiana territory or population.',cells=CELLS,new_rgb=RGB,previous_owner='MOD',population_transferred=POP)
    dump('IMPLEMENTATION.json',dict(task_ids=[TASK],status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',sub_lots=[sub],new_tags=[TAG],new_rgb=[RGB],territory_changed=True,population_transferred=POP,world_population_before=sum(r['count'] for r in b['inventory']['pops']),world_population_after=sum(r['count'] for r in inv['pops']),registry_before=574,registry_after=575,functional_files_modified=files['runtime_files'],points_awarded=0,automated_engine_test=False,engine_executed=False,regional_acceptance_complete=False))
    source=ROOT/'docs/reports/map/MAP1B/MAP1B_GEOGRAPHIC_EVIDENCE/lombardy_1750.jpg'
    dump('SOURCE_READING.json',dict(date='2026-10-23',historical_date='1776-01-01',historical_map_actually_viewed=dict(original=source.relative_to(ROOT).as_posix(),sha256=sha(source),overview='docs/reports/map/MAP1B/MAP1B_GEOGRAPHIC_EVIDENCE/lombardy_1750_1600.png',detail=PREFIX+'ROBERT_1750_MASSA_DETAIL.png',reading='Coastal Massa/Carrara distinct from Lerici/Sarzana, Tuscany, Lucca and interior Garfagnana; not cadastral precision.'),archival_original_letters_read=False,archival_inventories_read=True,population_reference_access='Search-index passage of Pappaianni p.30 note3; 20MB full PDF exceeded web reader limit; not claimed as full archival census reading.',modern_boundaries_used=False,old_R4_alignment_reused=False))
    matrix=[
        ['Massa','Duché impérial, Marie-Thérèse','MC-I-CORE','MCA','10000 résidents estimés, noyau seulement'],
        ['Carrare','Principauté sous la même souveraine','Titres et personnalité restitués avec MCA ; périmètre complet non installé','MCA','Population propre complète non établie'],
        ['Sarzana / Lerici','Interface génoise','GEN conservé','GEN','Aucune cellule transférée'],
        ['Montignoso','Juridiction lucquoise en 1776, pas extension moderne de Massa','LUC conservé','LUC','Aucune cellule transférée'],
        ['Pietrasanta / Seravezza','Interface toscane','TUS conservé','TUS','Aucune cellule transférée'],
        ['Garfagnana / Lunigiana estense','Possessions de MOD à distinguer du mariage','Parent MOD résiduel connecté','MOD','495752 dans la portion Emilia après transfert'],
        ['Autres fiefs Malaspina de Lunigiana','Dynastie ou patronyme ne prouve pas souveraineté de Marie-Thérèse','Aucun transfert de Aulla/Fosdinovo/Mulazzo etc.','inchangé','Attribution individuelle à établir si extension'],
        ['Biens Gonzaga / Novellara / Bagnolo','Archives allodiales distinctes des actes gouvernementaux','Aucun droit territorial déduit de la propriété','inchangé','Aucun transfert'],
        ['Aiello et biens méridionaux','Possessions et titres méridionaux distincts du ressort impérial italien','Aucune attribution impériale depuis le nom Cybo','inchangé','Hors noyau installé'],
        ['Investiture impériale','Titre territorial et restitution au détenteur du noyau','Un droit RGB MCA, pas électorat','MCA','Emprise impériale physique conservée'],
        ['Mariage Este / Cybo-Malaspina','Association et influence dynastiques, souverains distincts en 1776','Pas puppet, pas personal_union automatique','MOD / MCA distincts','Aucun pacte nouveau']]
    with (OUT/'JURISDICTION_MATRIX.csv').open('w',encoding='utf8',newline='') as f:
        w=csv.writer(f);w.writerow(['ensemble','status_1776','decision','owner_model','scope']);w.writerows(matrix)
    with (OUT/'RGB_BEFORE_AFTER.csv').open('w',encoding='utf8',newline='') as f:
        w=csv.writer(f);w.writerow(['rgb','state','owner_before','owner_after','cells_before','cells_after']);w.writerow([PARENT,SID,'MOD','MOD',116,108]);w.writerow([RGB,SID,'MOD',TAG,0,8])
    note='**SERG TERRITORIAL 1.0 — PROGRESSION : 34,89 %**\n\n'
    note+='# SC4-MASSA-CARRARA — restitution souveraine partielle\n\n'
    note+='Avant/après : **82/235 points, 34,89 % → 34,89 %**, périmètre 1.0.0 et 81 tâches inchangés. Le constat utilisateur Piombino est enregistré par SERG-RM-0024 sans PASS ni point. Piombino reste P0 BLOCKED ; toutes ses preuves antérieures sont conservées.\n\n'
    note+='Une seule nouvelle étape est exécutée : Massa-Carrare, P0 sans dépendance. Les sources archivistiques distinguent le gouvernement de Marie-Thérèse et le mariage avec Ercole, qui ne règne à Modène qu’en 1780. La carte Robert 1750 a été lue, pas seulement sa notice. Voir SOURCES.md et JURISDICTION_MATRIX.csv.\n\n'
    note+='**Installation MC-I-CORE — IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION** : nouveau TAG MCA reconnu, un RGB xEDBC00 de huit cellules littorales détachées de xF08021 MOD (116→108, parent encore connecté). Lucques, Gênes et Toscane conservent leurs cellules. Portion incorporée MCA de STATE_EMILIA, Marie-Thérèse Cybo-Malaspina née le 29 juin 1725, monarchie héréditaire, un niveau administratif public propre. Aucun pacte MOD–MCA, électorat, ville libre ou port industriel ajouté. Les droits impériaux passent de 574 à 575 RGB sans extension physique. Les fichiers constitutionnels sont régénérés depuis le générateur courant, dont la sortie correspondait exactement au workspace avant installation.\n\n'
    note+='Démographie : **10000 habitants transférés**, MOD 505752→495752, MCA 0→10000 ; population mondiale '+str(sum(r['count'] for r in inv['pops']))+' inchangée, cultures/religions/métiers déclarés conservés. Cet ordre de grandeur est celui du noyau massais, **pas le total du duché et de Carrare**. Aucun bâtiment existant, propriétaire économique ou unité déplacé ; plafonds, ressources, traits, arables et locators conservés. Le nouveau pays utilise les ressources partagées de l’Émilie ; aucun rendement ni propriétaire de carrière inventé. Emblème graphique simplifié de teintes Cybo, non reconstitution héraldique complète.\n\n'
    note+='**Tâche régionale BLOCKED P0**, installation partielle réelle : le périmètre et la population complète de Carrare, ainsi que les possessions périphériques individuellement pertinentes, ne sont pas reconstitués. L’implantation automatique de la capitale dans cet État partagé est à contrôler en jeu ; aucun nouveau hub Massa n’a été créé. Action précise : comparer le noyau livré et les cellules MOD immédiatement au nord-ouest aux ressorts Carrare/Avenza de la carte déjà lue, exclure Sarzana/Lerici, Montignoso, Pietrasanta/Seravezza et Garfagnana ; établir une population de Carrare au périmètre comparable avant une extension B. Une validation de MC-I-CORE ne clôturera pas à elle seule cette couverture régionale.\n\n'
    note+='Validation réelle : voir VALIDATION.json, TESTS.json et TEST_REVIEW.json. Trois anciennes assertions de dernière couche étaient héritées ; une assertion supplémentaire de Salzbourg devient obsolète après ajout de Massa. Les anciens tests sont conservés sans réécriture ; le contrôle cumulatif courant et les tests négatifs Massa couvrent la nouvelle chaîne. Aucun moteur exécuté ou reçu humain inventé. Les preuves antérieures, travaux fortifications/génie/France/États-Unis et autres fichiers fonctionnels sont vérifiés par empreinte ; les changements nécessaires sont énumérés dans FILES_MODIFIED.json.\n\n'
    note+='**Prochaine action : test joueur MC-I-CORE**, selon PLAYER_TEST_PROTOCOL.md (nouvelle partie 1776, souveraineté/capitale/démographie/administration/droits/conservation, un mois, sauvegarde/rechargement). Après résultat réel et revue du blocage, **SC1-TRENTO P1** est la prochaine candidate indépendante admissible, sans commencement dans cette mission. Innviertel, Autriche antérieure, droits italiens/Savoie/Ligurie, Piombino et Teschen restent distincts. Aucun Git écrit, aucun vanilla modifié.\n'
    note=note.replace('Emblème graphique simplifié de teintes Cybo, non reconstitution héraldique complète.','Pavillon technique rouge et blanc de repérage, sans authenticité héraldique revendiquée.')
    tested=load(OUT/'TESTS.json');scoped=load(OUT/'SCOPED_TESTS.json')
    note+='\nRésultats constatés : **'+str(v['passed'])+'/'+str(v['total'])+' contrôles statiques**, **'+str(tested['passed'])+'/'+str(tested['total'])+' tests cumulatifs réussis**, quatre assertions de snapshots classées et une exclusion ; **'+str(scoped['passed'])+'/'+str(scoped['total'])+' tests ciblés réussis**. Voir TEST_REVIEW.json pour la distinction entre les trois échecs hérités et l’ancienne assertion de dernière couche Salzbourg.\n'
    (OUT/'REPORT.md').write_text(note,encoding='utf8')
    print('Documentation and concrete residual action prepared',flush=True)

def tests():
    inherited=set(load(prior.OUT/'TEST_REVIEW.json')['historical_final_layer_assertions'])
    superseded={'test_serg_sc1_salzburg.SalzburgContracts.test_exact_cumulative_tail'}
    modules=prior.prior.MODULES+['test_serg_sc4_piombino','test_serg_sc4_massa_carrara']
    for label,names in [('TESTS',modules),('SCOPED_TESTS',['test_serg_sc4_massa_carrara'])]:
        stream=io.StringIO();r=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(names))
        failures=[dict(id=t.id(),traceback=s) for t,s in r.failures+r.errors]
        unexplained=[f for f in failures if f['id'] not in inherited|superseded]
        (OUT/(label+'.log')).write_text(stream.getvalue(),encoding='utf8')
        dump(label+'.json',dict(task_ids=[TASK],status='FAIL' if unexplained else 'OBSOLETE_SNAPSHOT_ASSERTIONS_ONLY' if failures else 'PASS',total=r.testsRun,passed=r.testsRun-len(failures)-len(r.skipped),failed=failures,skipped=[dict(id=t.id(),reason=s) for t,s in r.skipped],unexplained_failures=unexplained,automated_engine_test=False))
        print(label,r.testsRun-len(failures)-len(r.skipped),'/',r.testsRun,'unexplained',len(unexplained),flush=True)
        assert not unexplained,[(f['id'],f['traceback']) for f in unexplained]
    dump('TEST_REVIEW.json',dict(task_ids=[TASK],historical_final_layer_assertions=sorted(inherited),new_obsolete_snapshot_assertions=sorted(superseded),old_tests_not_modified=True,unexplained_failures=[],replacement='Current exact Salzburg -> Massa cumulative tail verified by VALIDATION.json and test_serg_sc4_massa_carrara; original Salzburg fixed-tail assertion retained unchanged.'))

def tracking():
    v=load(OUT/'VALIDATION.json');tested=load(OUT/'TESTS.json');scoped=load(OUT/'SCOPED_TESTS.json')
    assert not v['failed'] and not tested['unexplained_failures'] and not scoped['failed']
    state=load(rm.OUT/'ROADMAP_STATE.json');original=load(OUT/'STATE_AFTER_PIOMBINO_ACK.json');assert state==original
    assert state['events'][-1]['id']=='SERG-RM-0024' and rm.progress(state)['next_task']==TASK
    t=next(t for t in state['tasks'] if t['id']==TASK)
    block='P0 : MC-I-CORE restitue la souveraineté de résidence de Massa-Carrare, mais huit cellules et 10000 habitants massais ne certifient pas le périmètre et la population complète de Carrare ou les possessions périphériques. Reprise concrète : depuis le détail Robert 1750 déjà lu et le noyau livré, examiner les cellules MOD au nord-ouest (notamment [4324,1028], [4325,1028], [4326,1028], candidats non attribués), distinguer Carrare/Avenza de Sarzana/Lerici, Montignoso LUC, Pietrasanta/Seravezza TUS et Garfagnana MOD ; établir un relevé démographique comparable avant extension B. Pas de transfert de province entière ou de nouvelle personnalité juridique nécessaire : MCA existe désormais. Capitale automatique de la portion partagée et économie locale à contrôler en jeu avant acceptation ; aucun nouveau hub Massa ou port industriel prétendu.'
    note='Une seule nouvelle étape P0 exécutée : Massa-Carrare, après reconnaissance du blocage Piombino. Installation souveraine partielle MC-I-CORE : TAG MCA, huit cellules littorales MOD vers MCA, xF08021 116→108, nouveau xEDBC00 ; 10000 habitants existants transférés, MOD 505752→495752, démographie mondiale conservée. Marie-Thérèse Cybo-Malaspina, monarchie héréditaire, chambre ducale publique et un droit impérial borné ; 574→575 RGB sans changement d’emprise physique ou d’électeurs. Pas d’annexion MOD, de pacte dynastique forcé ni de modification des noyaux voisins validés. MC-I-CORE IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION ; tâche régionale BLOCKED P0 pour complément Carrare/périphéries. Aucun reçu humain, point ou conformité exhaustive inventé.'
    t.update(status='BLOCKED',blocking_reason=block,residual_uncertainty=block,installed_delivery_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',installed_sub_lots=load(OUT/'IMPLEMENTATION.json')['sub_lots'],installed_lots=['SERG_CLOSURE/'+TASK],implementation_report=[PREFIX+'REPORT.md',PREFIX+'B_PROPOSAL.md'],static_tests=dict(status='PASS',evidence=[PREFIX+'VALIDATION.json']),runtime_validation=dict(required=True,status='NOT_RUN',attestation=None,scope='MC-I-CORE only: eight-cell residence nucleus, 10000 transferred people, Maria Teresa, independent court and bounded imperial title. No cadastral or full Carrara/Lunigiana approval.',new_details_invented=False,protocol=PREFIX+'PLAYER_TEST_PROTOCOL.md'),decision=None,current_delivery_note=note,
        delivered_scope=dict(classification='B_COASTAL_SOVEREIGN_RESIDENCE_NUCLEUS',sub_lots=['MC-I-CORE'],new_tag=TAG,new_rgb=RGB,installed_cells=8,transferred_population=10000,regional_acceptance_complete=False,cadastral_validation=False,world_population_unchanged=True,imperial_physical_extent_unchanged=True))
    t['historical_sources'].append(PREFIX+'SOURCES.md:1')
    t['identified_problem'].append('Souveraineté Cybo-Malaspina omise et confondue avec MOD ; noyau restitué, couverture complète de Carrare et démographie périphérique distinctes.')
    candidate=rm.progress(state)['next_task'];assert candidate=='SC1-TRENTO'
    state['runtime_validation_hold']=dict(task_id=TASK,protocol=PREFIX+'PLAYER_TEST_PROTOCOL.md',next_implementation_candidate=candidate,
        test_summary='Tester MC-I-CORE : nouvelle partie 1776, pays MCA distinct, huit cellules côtières, Marie-Thérèse, capitale de sa portion, 10000 habitants, administration publique, droits impériaux limités, voisins conservés ; un mois puis sauvegarde/rechargement.',
        scope_note='SC4-MASSA-CARRARA reste BLOCKED P0 pour le complément Carrare/périphéries. Seul MC-I-CORE est installé et prêt au test. Une confirmation de ce noyau ne clôturera pas toute la région ni ne lui attribuera automatiquement trois points. Candidate SC1-TRENTO P1 sans commencement ; aucun ancien blocage rouvert automatiquement.')
    state['mission_status']='SC4_MASSA_CARRARA_SOVEREIGN_CORE_AWAITING_USER_REGIONAL_BLOCK'
    fullnote=note+f' Statique {v["passed"]}/{v["total"]} ; suite cumulative {tested["passed"]}/{tested["total"]}, trois échecs de snapshots hérités, une assertion de dernière couche Salzbourg désormais dépassée et une exclusion ; ciblée {scoped["passed"]}/{scoped["total"]}. Aucun nouvel échec inexpliqué ; tests anciens intacts, chaîne actuelle contrôlée explicitement. Preuves Piombino, autres reçus et travaux concurrents conservés. 82/235=34,89 % avant/après, 81 tâches et poids inchangés. Prochaine action joueur MC-I-CORE ; candidate SC1-TRENTO P1 identifiée sans commencement. Aucun Git ou vanilla écrit.'
    state['events'].append(dict(id='SERG-RM-0025',date='2026-10-23',kind='PARTIAL_SOVEREIGN_IMPLEMENTATION_WITH_REGIONAL_BLOCK',scope_version='1.0.0',source=PREFIX+'AUTHORIZATION.md',changes=[dict(task_id=TASK,before='NOT_STARTED',after='BLOCKED')],sub_lot_changes=[dict(id='MC-I-CORE',before='NOT_STARTED',after='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION')],before_weight=82,after_weight=82,total_weight=235,before_percent='34.89',after_percent='34.89',evidence=[PREFIX+n for n in ['REPORT.md','VALIDATION.json','TESTS.json','PLAYER_TEST_PROTOCOL.md','IMPLEMENTATION.json']],note=fullnote))
    assert state['events'][:-1]==original['events']
    assert [t for t in state['tasks'] if t['id']!=TASK]==[t for t in original['tasks'] if t['id']!=TASK]
    assert not rm.structural_errors(state),rm.structural_errors(state)
    rm.write_json(rm.OUT/'ROADMAP_STATE.json',state)
    with contextlib.redirect_stdout(io.StringIO()):rm.render()
    checked=rm.check();dump('TRACKER_VALIDATION.json',checked);assert checked['status']=='PASS',checked['errors']
    p=rm.progress(state);assert (p['earned_weight'],p['total_weight'],p['percent'],p['qualified_tasks'],p['next_task'])==(82,235,'34.89',24,TASK)
    dump('TRACKER_PRESERVATION.json',dict(task_ids=[TASK],other_79_tasks_unchanged_since_entry=True,piombino_acknowledged_only=True,previous_23_events_unchanged=True,previous_24_events_preserved_before_massa=True,total_tasks=81,scope_version='1.0.0',earned_weight=82,total_weight=235,percent='34.89',new_human_receipts=0,regional_status='BLOCKED',installed_delivery_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',player_next_action='MC-I-CORE',next_geographical_candidate=candidate,candidate_started=False))
    print('Tracker PASS; regional BLOCKED, installed core ready, 82/235; next after test:',candidate,flush=True)

def final_tests():
    stream=io.StringIO();names=['test_serg_closure_roadmap','test_serg_sc4_massa_carrara'];r=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(names))
    failures=[dict(id=t.id(),traceback=s) for t,s in r.failures+r.errors]
    (OUT/'FINAL_TESTS.log').write_text(stream.getvalue(),encoding='utf8');dump('FINAL_TESTS.json',dict(task_ids=[TASK],status='PASS' if not failures else 'FAIL',total=r.testsRun,passed=r.testsRun-len(failures)-len(r.skipped),failed=failures,skipped=[dict(id=t.id(),reason=s) for t,s in r.skipped],automated_engine_test=False))
    print('Final tests',r.testsRun-len(failures)-len(r.skipped),'/',r.testsRun,flush=True);assert not failures,failures

def observe_concurrent():
    static=load(OUT/'SESSION_AFTER_STATIC.json');current=italian.runtime_hashes()
    changes=sorted(p for p in set(current)|set(static['hashes']) if current.get(p)!=static['hashes'].get(p))
    reviewed={
        'common/buildings/01_industry.txt','common/buildings/11_tech6c1b_cement_works.txt','common/buildings/12_tech6c4_oil_refinery.txt','common/buildings/14_tech6c5c_non_ferrous_metallurgy_works.txt',
        'common/company_types/00_companies_france.txt','common/prestige_goods/1776_anzin_coking_coal.txt','common/production_method_groups/1776_industrial_transport.txt','common/production_methods/22_tech7a_wave_a_land_transport_production.txt',
        'gfx/interface/icons/goods_icons/prestige_goods/1776_anzin_coking_coal.dds','localization/english/1776_anzin_regional_transport_l_english.yml','localization/french/1776_anzin_regional_transport_l_french.yml'}
    print('Concurrent differences',changes,flush=True);assert set(changes)<=reviewed,'Review additional concurrent file before proceeding'
    assert not set(changes)&set(load(OUT/'FILES_MODIFIED.json')['runtime_files'])
    inv=core.qa.inventory();assert inv==static['inventory'],'Reconcile changed game histories before continuing'
    checks=[]
    for p in changes:
        if p.endswith('.txt'):core.cw.parse((ROOT/p).read_text(encoding='utf-8-sig'))
        checks.append(dict(path=p,before_sha256=static['hashes'].get(p),after_sha256=current[p],written_by_this_pass=False,action='PRESERVED',theme='Concurrent Anzin / regional industrial transport'))
    assert italian.runtime_hashes()==current,'Concurrent files changed during observation; take a fresh read'
    for name in ['FINAL_CHECKS.json','SESSION_AFTER.json']:
        dest=OUT/(Path(name).stem+'_BEFORE_CONCURRENT_REVIEW.json')
        if (OUT/name).exists() and not dest.exists():shutil.copyfile(OUT/name,dest)
    dump('CONCURRENT_OBSERVATION.json',dict(task_ids=[TASK],status='PRESERVED_AND_SEMANTIC_HISTORY_INVENTORY_UNCHANGED',files=checks,all_own_delivery_files_unchanged=True,history_inventory_unchanged=True,no_concurrent_file_written_by_this_pass=True,no_engine_validation_of_concurrent_work=True,inventory=inv,hashes=current))
    print('Concurrent work preserved:',len(changes),'files; world history unchanged',flush=True)

def concurrent_tests():
    stream=io.StringIO();names=prior.prior.MODULES+['test_serg_sc4_piombino','test_serg_sc4_massa_carrara'];r=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(names))
    failures=[dict(id=t.id(),traceback=s) for t,s in r.failures+r.errors];review=load(OUT/'TEST_REVIEW.json');expected=set(review['historical_final_layer_assertions'])|set(review['new_obsolete_snapshot_assertions']);unknown=[f for f in failures if f['id'] not in expected]
    (OUT/'POST_CONCURRENT_TESTS.log').write_text(stream.getvalue(),encoding='utf8');dump('POST_CONCURRENT_TESTS.json',dict(task_ids=[TASK],total=r.testsRun,passed=r.testsRun-len(failures)-len(r.skipped),failed=failures,skipped=[dict(id=t.id(),reason=s) for t,s in r.skipped],unexplained_failures=unknown,status='FAIL' if unknown else 'OBSOLETE_SNAPSHOT_ASSERTIONS_ONLY',automated_engine_test=False,scope='SERG cumulative tests repeated after independent concurrent Anzin/transport changes; no human or engine attestation for that work'))
    print('Post-concurrent tests',r.testsRun-len(failures)-len(r.skipped),'/',r.testsRun,'unexplained',len(unknown),flush=True);assert not unknown

def record_concurrent():
    obs=load(OUT/'CONCURRENT_OBSERVATION.json');tested=load(OUT/'POST_CONCURRENT_TESTS.json');assert not tested['unexplained_failures']
    assert italian.runtime_hashes()==obs['hashes'],'Review subsequent concurrent change before final record'
    state=load(rm.OUT/'ROADMAP_STATE.json');assert state['events'][-1]['id']=='SERG-RM-0025';dump('STATE_BEFORE_CONCURRENT_EVENT.json',state)
    note='Après les contrôles Massa, onze fichiers du chantier concurrent Anzin/transport industriel ont changé ou été ajoutés, hors des 31 fichiers fonctionnels de cette passe. Ces changements sont conservés sans restauration ; inventaire mondial des historiques strictement identique à la validation Massa, fichiers du noyau inchangés. Suite cumulative répétée : '+str(tested['passed'])+'/'+str(tested['total'])+' réussites, quatre assertions de snapshots déjà classées et une exclusion, aucun échec inexpliqué. Aucune validation moteur ou humaine du chantier concurrent créée. Progression inchangée 82/235=34,89 % ; seul MC-I-CORE attend le joueur, couverture Massa-Carrare BLOCKED, candidate Trente non commencée.'
    next(t for t in state['tasks'] if t['id']==TASK)['current_delivery_note']+=' '+note
    state['events'].append(dict(id='SERG-RM-0026',date='2026-10-23',kind='CONCURRENT_WORK_PRESERVED_AND_NONREGRESSION',scope_version='1.0.0',source=PREFIX+'CONCURRENT_OBSERVATION.json',changes=[],before_weight=82,after_weight=82,total_weight=235,before_percent='34.89',after_percent='34.89',evidence=[PREFIX+'CONCURRENT_OBSERVATION.json',PREFIX+'POST_CONCURRENT_TESTS.json'],note=note))
    rm.write_json(rm.OUT/'ROADMAP_STATE.json',state)
    with contextlib.redirect_stdout(io.StringIO()):rm.render()
    checked=rm.check();dump('POST_CONCURRENT_TRACKER_VALIDATION.json',checked);assert checked['status']=='PASS'
    with (OUT/'REPORT.md').open('a',encoding='utf8') as f:f.write('\n## Concurrence arrivée en fin de passe\n\n'+note+'\n\nEmpreintes exactes et fichiers dans CONCURRENT_OBSERVATION.json. Le premier contrôle final a détecté cet écart ; sa preuve est conservée dans FINAL_CHECKS_BEFORE_CONCURRENT_REVIEW.json. Aucun fichier Anzin modifié par cette passe.\n')
    print('Concurrent verification recorded additively as SERG-RM-0026',flush=True)

def finalize():
    b=load(OUT/'BASELINE.json');state=load(rm.OUT/'ROADMAP_STATE.json');current=italian.runtime_hashes();checks=[]
    def ck(name,ok,detail=None):checks.append(dict(name=name,passed=bool(ok),detail=detail))
    static=load(OUT/'SESSION_AFTER_STATIC.json');obs=load(OUT/'CONCURRENT_OBSERVATION.json') if (OUT/'CONCURRENT_OBSERVATION.json').exists() else None
    concurrent={r['path']:r['after_sha256'] for r in obs['files']} if obs else {}
    delta={p:current.get(p) for p in set(current)|set(static['hashes']) if current.get(p)!=static['hashes'].get(p)}
    ck('Own functional delivery intact; exact independent concurrent delta preserved',delta==concurrent and (not obs or current==obs['hashes']))
    ck('All 79 other tasks intact',[t for t in state['tasks'] if t['id'] not in {TASK,prior.TASK}]==[t for t in b['roadmap']['tasks'] if t['id'] not in {TASK,prior.TASK}])
    ck('Prior events exact; acknowledgment, sole new task, concurrent verification',state['events'][:23]==b['roadmap']['events'] and len(state['events'])==(26 if obs else 25) and [e['id'] for e in state['events'][23:25]]==['SERG-RM-0024','SERG-RM-0025'] and (not obs or state['events'][:25]==load(OUT/'STATE_BEFORE_CONCURRENT_EVENT.json')['events']))
    ck('All qualified previous tasks retained without new points',rm.qualifications(state)==rm.qualifications(b['roadmap']))
    p=rm.progress(state);ck('82/235, 34.89%, 81 tasks, 24 qualified unchanged',(p['earned_weight'],p['total_weight'],p['percent'],p['total_tasks'],p['qualified_tasks'])==(82,235,'34.89',81,24))
    t=next(t for t in state['tasks'] if t['id']==TASK);ck('Partial installation pending with global P0 block',t['status']=='BLOCKED' and t['installed_delivery_status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' and t['installed_sub_lots'][0]['status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' and t['runtime_validation']['attestation'] is None and t['decision'] is None)
    pt=next(t for t in state['tasks'] if t['id']==prior.TASK);ck('Piombino blocked without approval or fabricated test',pt['status']=='BLOCKED' and pt['priority']=='P0' and pt['decision'] is None and pt['runtime_validation']['attestation'] is None and not pt['installed_lots'])
    ck('Player handoff active and Trento candidate unstarted',p['next_task']==TASK and state['runtime_validation_hold']['next_implementation_candidate']=='SC1-TRENTO' and next(t for t in state['tasks'] if t['id']=='SC1-TRENTO')['status']=='NOT_STARTED')
    nextmd=(rm.OUT/'NEXT_ACTION.md').read_text(encoding='utf8');ck('Next view labels Trento P1 and regional block accurately','SC1-TRENTO` (P1' in nextmd and 'SC4-MASSA-CARRARA reste BLOCKED P0' in nextmd and 'MC-I-CORE' in nextmd)
    canonical={p.relative_to(ROOT).as_posix() for p in rm.OUT.iterdir() if p.is_file()}
    changedproofs=[p for p,h in b['reports'].items() if p not in canonical and (not (ROOT/p).is_file() or sha(ROOT/p)!=h)];ck('Every older nested proof and receipt byte-identical',not changedproofs,changedproofs)
    protected=[];overlap=[];cells=set(map(tuple,CELLS))
    for directory in reg.approved_lot_dirs()[:-1]:
        for row in load(directory/'GEOMETRY.json')['assignments']:
            touched=cells&set(map(tuple,row.get('cells',[])))
            if touched:overlap.append(dict(lot=directory.name,rgb=row['rgb'],cells=sorted(touched)))
            protected.append(dict(lot=directory.name,rgb=row['rgb'],owner=row['owner'],cells=row['pixels']))
    dump('PROTECTED_CORE_CHECK.json',dict(approved_geometry_rows=len(protected),rows=protected,intersections_with_new_core=overlap,only_changed_pixels=CELLS,all_other_raster_pixels_unchanged=True))
    ck('No previously approved geometry core touched',not overlap,overlap)
    tools=[p for p,h in b['tools'].items() if not (ROOT/p).exists() or sha(ROOT/p)!=h];ck('Old tests untouched; only registry and handoff tools changed',set(tools)=={'tools/map2l_registry.py','tools/serg_closure_roadmap.py'},tools)
    ck('No new human receipt created',not list(OUT.glob('RUNTIME_USER_ATTESTATION*')))
    ck('Exact user mission preserved',(OUT/'USER_MISSION.txt').read_bytes()==MISSION.read_bytes() and (prior.OUT/'USER_BLOCKER_MISSION_2026_10_23.txt').read_bytes()==MISSION.read_bytes())
    git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
    ck('Git HEAD branch and index unchanged',git('rev-parse','HEAD')==b['git']['head'] and git('branch','--show-current')==b['git']['branch'] and sha(ROOT/'.git/index')==b['git']['index_sha256'])
    diff=subprocess.run(['git','diff','--check'],cwd=ROOT,text=True,encoding='utf8',capture_output=True)
    findings=[dict(file=m.group(1),line=int(m.group(2)),message=m.group(3)) for m in re.finditer(r'^([^:\r\n]+):(\d+): (.+)$',diff.stdout,re.M)]
    inherited=all(f['file']=='common/history/pops/00_west_europe.txt' and f['message']=='trailing whitespace.' and current[f['file']]==b['hashes'][f['file']] for f in findings)
    ok=diff.returncode==0 or diff.returncode in {1,2} and len(findings)==4 and inherited and {f['line'] for f in findings}=={2983,2999,3015,3031}
    dump('DIFF_CHECK.json',dict(task_ids=[TASK],status='INHERITED_WHITESPACE_ONLY' if findings and ok else 'PASS' if ok else 'FAIL',exit_code=diff.returncode,findings=findings,stdout=diff.stdout,stderr=diff.stderr,old_file_unchanged=inherited));ck('Only four inherited whitespace findings remain',ok,findings)
    tested=load(OUT/'TESTS.json');review=load(OUT/'TEST_REVIEW.json');actual={r['id'] for r in tested['failed']};expected=set(review['historical_final_layer_assertions'])|set(review['new_obsolete_snapshot_assertions'])
    ck('Cumulative failures precisely classified, not unexplained',actual==expected and len(actual)==4 and not tested['unexplained_failures'])
    ck('134 static and all scoped/final tests passed',load(OUT/'VALIDATION.json')['passed']==load(OUT/'VALIDATION.json')['total']==134 and not load(OUT/'SCOPED_TESTS.json')['failed'] and not load(OUT/'FINAL_TESTS.json')['failed'])
    if obs:ck('Post-concurrent cumulative tests and semantic histories verified',not load(OUT/'POST_CONCURRENT_TESTS.json')['unexplained_failures'] and obs['inventory']==static['inventory'] and not set(concurrent)&set(load(OUT/'FILES_MODIFIED.json')['runtime_files']))
    checked=rm.check();dump('TRACKER_VALIDATION_FINAL.json',checked);ck('Canonical validator PASS',checked['status']=='PASS',checked.get('errors'))
    ck('Immutable scope manifest retained',sha(rm.OUT/'scopes/1.0.0.json')==b['reports']['docs/reports/map/SERG_CLOSURE/scopes/1.0.0.json'])
    result=dict(task_ids=[TASK],status='PASS' if all(c['passed'] for c in checks) else 'FAIL',total=len(checks),passed=sum(c['passed'] for c in checks),failed=[c['name'] for c in checks if not c['passed']],checks=checks,automated_engine_test=False,engine_executed=False,vanilla_writes_by_this_pass=0)
    dump('FINAL_CHECKS.json',result);dump('SESSION_AFTER.json',dict(hashes=current,progress=p,git_head=git('rev-parse','HEAD'),git_branch=git('branch','--show-current'),git_index_sha256=sha(ROOT/'.git/index'),previous_proofs_checked=len(b['reports'])-len(set(b['reports'])&canonical)))
    print('Final checks',result['passed'],'/',result['total'],result['failed'],flush=True);assert not result['failed'],result['failed']
    files=[p for p in OUT.rglob('*') if p.is_file() and p.name!='DELIVERY_MANIFEST.json']
    files += [prior.OUT/n for n in ['USER_ACKNOWLEDGMENT_2026_10_23.json','USER_BLOCKER_MISSION_2026_10_23.txt']]
    files += [ROOT/'tools'/n for n in ['serg_sc4_massa_carrara.py','test_serg_sc4_massa_carrara.py','map2l_registry.py','serg_closure_roadmap.py']]
    files += [ROOT/p for p in load(OUT/'FILES_MODIFIED.json')['runtime_files']]+[reg.active_registry_path()]
    files += [rm.OUT/n for n in ['ROADMAP_STATE.json','ROADMAP.md','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','PROGRESS_SNAPSHOT.json','CLOSURE_CHECKLIST.md','DEFERRED_P2.md']]
    dump('DELIVERY_MANIFEST.json',dict(task_ids=[TASK],files={p.relative_to(ROOT).as_posix():sha(p) for p in sorted(set(files))},concurrent_files_observed_not_written=concurrent,automated_engine_test=False,installation_status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',regional_status='BLOCKED'))
    assert all((ROOT/p).is_file() and sha(ROOT/p)==h for p,h in load(OUT/'DELIVERY_MANIFEST.json')['files'].items())
    print('Delivery manifest verified:',len(set(files)),'files;',len(current),'functional files observed',flush=True)

if __name__=='__main__':globals()[sys.argv[1]]()
