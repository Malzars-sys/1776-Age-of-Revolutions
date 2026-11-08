"""User-approved client-state artwork/name, liberty rules and Ethiopian army follow-up.

No Git writes, no vanilla writes. Current shared-file preimages only.
"""
import argparse, collections as C, hashlib, json, math, re, shutil, struct, sys
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image
import audit_anzin_regional_infrastructure as a
import audit_starting_tech_1776 as t
import protected_state_r1 as prior
from validate_diplomacy_ottoman_1776 import parse, walk, normalized, scalar
from localization_duplicate_audit import entries

ROOT=a.ROOT; GAME=a.GAME
OUT=ROOT/'docs/reports/diplomacy/CLIENT_STATE_R2'
ACTION=prior.ACTION; TYPE=prior.TYPE
ORIGINAL=Path('C:/Users/simeo/AppData/Local/Temp/codex-clipboard-a00253d8-e9fe-4d4a-a546-fb1ddc3ad985.png')
CUTOUT=Path('C:/Users/simeo/.codex/generated_images/01a149d5-1620-7bf2-bf90-7fa9bf443072/exec-b36f4eb2-2744-4762-bb4a-ae3a1055f28c.png')
MASTER='workshop_assets/source/CLIENT_STATE_R2'
ARMY='common/history/military_formations/07_military_formations_subsaharan_africa.txt'
HORN='common/history/diplomacy/1776_world_horn01.txt'
LIBERTY='common/script_values/zz_1776_client_state_liberty.txt'
ASSETS={prior.TEX:128,prior.SMALL:30,
 'gfx/interface/icons/diplomatic_action_icons/'+TYPE+'.dds':30,
 'gfx/interface/icons/lens_toolbar_icons/'+ACTION+'.dds':64,
 'gfx/interface/icons/lens_toolbar_icons/'+ACTION+'_break.dds':64}

def dump(name,value):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def load(name):return json.loads((OUT/name).read_text(encoding='utf8'))
def source(p):return ('MOD:' if p.is_relative_to(ROOT) else 'VANILLA:')+p.relative_to(ROOT if p.is_relative_to(ROOT) else GAME).as_posix()
def changes(s,ops):
    for lo,hi,text in sorted(ops,reverse=True):s=s[:lo]+text+s[hi:]
    return s
def hash_tree():
    return {p.relative_to(ROOT).as_posix():a.sha(p) for folder in
      ['common','events','gui','gfx','localization','map_data','docs/reports/map/SERG_CLOSURE']
      for p in (ROOT/folder).rglob('*') if p.is_file()}
def eth_node(s):return next(n for n in walk(parse(s)) if n.key=='c:ETH')

def rename(lang,s):
    if lang=='french':
        s=s.replace('État protégé','État client').replace('état protégé','état client')
        replacements={
         'Proposer notre protection':'Proposer un lien de clientèle',
         'Rompre le lien de protection':'Rompre le lien de clientèle',
         'Demander la fin de la protection':'Demander la fin du lien de clientèle',
         'Une offre de protection':'Une offre de clientèle',
         'Protection acceptée':'Lien de clientèle accepté',
         'Protection refusée':'Lien de clientèle refusé',
         'Fin de la protection demandée':'Fin du lien de clientèle demandée',
         'Fin de protection refusée':'Fin du lien de clientèle refusée',
         'Fin de la protection':'Fin du lien de clientèle',
         'Protection levée':'Lien de clientèle rompu',
         'Un État accepte une protection':'Un État accepte un lien de clientèle',
         'Une protection est refusée':'Un lien de clientèle est refusé',
         'lien de protection':'lien de clientèle',
         'notre protection':'le lien de clientèle',
         'notre offre de protection':'notre offre de clientèle',
         'l’offre de protection':'l’offre de clientèle',
         'mettre fin à la protection de':'rompre le lien de clientèle avec',
         'a mis fin à la protection de':'a rompu le lien de clientèle avec',
        }
        for old,new in replacements.items():s=s.replace(old,new)
        # All country-number agreement is explicit, using the native grammar contract.
        for scope in ['TARGET_COUNTRY','INITIATOR_COUNTRY']:
            for old,new in [(' a accepté',' accepté'),(' a refusé',' refusé'),(' a rompu',' rompu')]:
                s=s.replace('['+scope+'.GetName]'+old,'['+scope+'.GetName] ['+scope+".GetAltNameNoFormatting('AOnt')]"+new)
        for suffix in ['first','third']:
            key=ACTION+'_trigger_false_desc_'+suffix
            replacement='Le statut d’[concept_aor1776_protected_state|l] ne s’applique pas à [TARGET_COUNTRY.GetName] vis-à-vis de [COUNTRY.GetName].'
            s=re.sub(r'(?m)^ '+re.escape(key)+r':0 "[^\r\n]*"',lambda m:' '+key+':0 "'+replacement+'"',s)
        extra={
         'aor1776_client_prestige_negative':'Le prestige du suzerain dépasse celui de l’État client (seuil : ×1)',
         'aor1776_client_prestige_positive':'Le prestige du suzerain ne dépasse pas celui de l’État client (seuil : ×1)',
         'aor1776_client_army_negative':'La puissance militaire du suzerain dépasse le seuil de l’État client (×2,5)',
         'aor1776_client_army_positive':'La puissance militaire du suzerain ne dépasse pas le seuil de l’État client (×2,5)',
        }
    else:
        s=s.replace('Protected state','Client state').replace('protected state','client state')
        for old,new in [('protection agreement','client-state agreement'),('our protection','a client-state agreement'),
          ('offer of protection','offer of a client-state agreement'),('Offer our protection','Offer a client-state agreement'),
          ('end to protection','end to the client-state agreement'),('An offer of protection','An offer of a client-state agreement'),
          ('Protection accepted','Client-state agreement accepted'),('Protection declined','Client-state agreement declined'),
          ('Protection ended','Client-state agreement ended'),('End of protection','End of client-state agreement'),
          ('A state accepts protection','A state accepts a client-state agreement'),('its protection of','its client-state agreement with')]:s=s.replace(old,new)
        extra={
         'aor1776_client_prestige_negative':'Overlord prestige exceeds the client-state threshold (×1)',
         'aor1776_client_prestige_positive':'Overlord prestige does not exceed the client-state threshold (×1)',
         'aor1776_client_army_negative':'Overlord military power exceeds the client-state threshold (×2.5)',
         'aor1776_client_army_positive':'Overlord military power does not exceed the client-state threshold (×2.5)',
        }
    return s+''.join(f' {k}:0 "{v}"\n' for k,v in extra.items())

def liberty_branch(metric,threshold,negative_divisor,max_negative,label):
    return f'''else_if = {{
 limit = {{ is_diplomatic_action_type = {ACTION} }}
 if = {{
  limit = {{ root.first_country.{metric} > {{ add = root.second_country.{metric} multiply = {threshold} }} }}
  add = {{ add = root.first_country.{metric} divide = root.second_country.{metric}
   divide = {negative_divisor} min = 0.01 max = {max_negative} multiply = -1
   desc = "aor1776_client_{label}_negative" }}
 }}
 else = {{
  add = {{ add = root.second_country.{metric} multiply = {threshold} divide = root.first_country.{metric}
   divide = {'prestige' if label=='prestige' else 'army_projection'}_to_libery_desire_factor max = 0.5
   desc = "aor1776_client_{label}_positive" }}
 }}
}}
'''

def plan():
    out={}
    for lang in ['french','english']:
        rel=f'localization/{lang}/1776_protected_state_l_{lang}.yml'
        out[rel]=b'\xef\xbb\xbf'+rename(lang,a.raw(ROOT/rel)).encode('utf8')
    # Preserve the existing ETH general, formation identity and every other country byte.
    s=a.raw(ROOT/ARMY);n=eth_node(s);form=n.children('create_military_formation')[0]
    units=form.children('combat_unit');assert [u.one('count') for u in units]==['4','12','25','23']
    regular=units[1];conscript=units[2]
    reg=s[regular.start:regular.end].replace('count = 12','count = 10')
    con=s[conscript.start:conscript.end].replace('count = 25','count = 15')
    s=changes(s,[(units[0].start,units[0].end,''),(regular.start,regular.end,reg),
                (conscript.start,conscript.end,con),(units[3].start,units[3].end,'')])
    out[ARMY]=s.encode('utf8')
    # Source-backed nominal imperial affiliation: no new claim against independent neighbours.
    s=a.raw(ROOT/HORN);assert s.count('type = tributary')==3
    out[HORN]=s.replace('type = tributary','type = '+ACTION).replace(
        '# Provincial autonomy under a surviving imperial crown; not direct annexation.',
        '# Nominal provincial allegiance to the surviving imperial crown: no regular financial tribute.').encode('utf8')
    node,path=a.catalog('common/script_values')['liberty_desire_weekly_change']
    s=a.raw(path);text=s[node.start:node.end];ops=[]
    for marker,metric,threshold,divisor,maximum,label in [
      ('prestige','prestige','1','100','0.05','prestige'),
      ('army','army_power_projection','2.5','50','0.10','army')]:
        branch=next(c for c in node.children() if c.key=='else_if' and
          any(x.key=='is_diplomatic_action_type' and x.value=='tributary' for x in walk([c])) and
          any(x.key=='root.first_country.'+metric for x in walk([c])))
        offset=branch.start-node.start
        ops.append((offset,offset,liberty_branch(metric,threshold,divisor,maximum,label)))
    text=changes(text,ops).replace('liberty_desire_weekly_change =','REPLACE_OR_CREATE:liberty_desire_weekly_change =',1)
    out[LIBERTY]=('# Only the client-state prestige/army branches are added; native calculations otherwise preserved.\n'+text+'\n').encode('utf8')
    im=Image.open(CUTOUT).convert('RGBA');bbox=im.getchannel('A').point(lambda x:255 if x>=24 else 0).getbbox()
    im=im.crop(bbox);cache=ROOT/'.asset-cache/client_state_r2';cache.mkdir(parents=True,exist_ok=True)
    for rel,size in ASSETS.items():
        data,preview=prior.dds(im,size);out[rel]=data;preview.save(cache/(Path(rel).stem+'_'+str(size)+'.png'))
    out[MASTER+'/user_original.png']=ORIGINAL.read_bytes();out[MASTER+'/client_state_transparent.png']=CUTOUT.read_bytes()
    return out,source(path),s[node.start:node.end]

def inventory():
    countries=a.catalog('common/country_definitions');types=a.catalog('common/subject_types')
    active=set()
    for p in t.effective('common/history/states'):
        active|={scalar(n.one('country')).removeprefix('c:') for n in walk(parse(a.raw(p))) if n.key=='create_state'}
    actions={n.one('diplomatic_action') for n,p in types.values()};rows=[]
    def visit(nodes,tag,path):
        for n in nodes:
            if n.key.startswith('c:'):visit(n.children(),n.key[2:],path);continue
            if n.key=='create_diplomatic_pact' and n.one('type') in actions:
                target=scalar(n.one('country','')).removeprefix('c:')
                if tag in active and target in active and countries[tag][0].one('country_type')=='unrecognized':
                    rows.append(dict(overlord=tag,subject=target,action=n.one('type'),file=source(path),
                      overlord_type=countries[tag][0].one('country_type'),subject_type=countries[target][0].one('country_type')))
            visit(n.children(),tag,path)
    for p in t.effective('common/history/diplomacy'):visit(parse(a.raw(p)),None,p)
    return rows

def numeric_term(nodes,stats):
    """Evaluate the real arithmetic of the isolated prestige/army terms, not their prose."""
    def number(value):
        if isinstance(value,list):return numeric_term(value,stats)
        return stats[value] if value in stats else float(value)
    def condition(nodes):
        for x in nodes:
            if x.key=='OR':ok=any(condition([y]) for y in x.children())
            elif x.key=='is_diplomatic_action_type':ok=stats['action']==x.value
            elif x.key=='root.second_country':ok=False # India-only special case; tests use a generic subject.
            else:
                left=number(x.key);right=number(x.value)
                ok={'<':left<right,'>':left>right,'=':left==right}[x.op]
            if not ok:return False
        return True
    value=0.;matched=False
    for x in nodes:
        if x.key in ['if','else_if','else']:
            if x.key=='if':matched=False
            if (x.key=='else' or condition(x.children('limit')[0].children())) and not matched:
                value+=numeric_term([y for y in x.children() if y.key!='limit'],stats);matched=True
        elif x.key in ['desc','limit']:continue
        elif x.key in ['value','add','subtract','multiply','divide','min','max']:
            v=number(x.value)
            if x.key=='value':value=v
            elif x.key=='add':value+=v
            elif x.key=='subtract':value-=v
            elif x.key=='multiply':value*=v
            elif x.key=='divide':value/=v
            elif x.key=='min':value=max(value,v)
            elif x.key=='max':value=min(value,v)
        else:raise ValueError(x.key)
    return value

def install():
    assert not (OUT/'BASELINE.json').exists(),'Follow-up already installed; do not overwrite baseline.'
    before=hash_tree();files,liberty_source,liberty_original=plan()
    assert all(a.sha(ROOT/r)==h for r,h in before.items() if r in files),'Concurrent input changed while planning.'
    baseline=dict(utc=datetime.now(timezone.utc).isoformat(),git=a.git_state(),hashes=before,
      touched={r:a.sha(ROOT/r) if (ROOT/r).exists() else None for r in files},
      native_liberty_source=liberty_source,native_liberty_original=liberty_original,
      native_hashes={str(p.relative_to(GAME)):a.sha(p) for p in [GAME/'common/script_values/00_diplomacy_values.txt',GAME/'common/subject_types/00_subject_types.txt']},
      source_original_sha256=a.sha(ORIGINAL),cutout_sha256=a.sha(CUTOUT),starting_relations=inventory())
    for rel,h in baseline['touched'].items():
        if h:
            dest=OUT/'preimages'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,dest)
    dump('BASELINE.json',baseline)
    for rel,data in files.items():
        p=ROOT/rel;old=baseline['touched'][rel]
        assert (a.sha(p) if p.exists() else None)==old,('Concurrent edit',rel)
        p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
    dump('INSTALLED.json',dict(files={r:a.sha(ROOT/r) for r in files},internal_ids_retained=[ACTION,TYPE],
      status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',runtime='NOT_RUN',human_validation='NOT_ACQUIRED'))
    dump('DIPLOMATIC_INVENTORY.json',inventory())
    print('Installed',len(files),'files; follow-up baseline preserved.',flush=True)

def validate():
    b=load('BASELINE.json');installed=load('INSTALLED.json');checks=[]
    def ck(name,ok,details=None):checks.append(dict(name=name,passed=bool(ok),details=details))
    for rel,h in installed['files'].items():ck('installed_hash.'+rel,a.sha(ROOT/rel)==h)
    now=hash_tree();allowed=set(installed['files'])
    unrelated=[r for r,h in b['hashes'].items() if r not in allowed and now.get(r)!=h]
    added=[r for r in now if r not in b['hashes'] and r not in allowed]
    ck('preserve_all_unrelated_runtime_map_and_SERG_files',not unrelated and not added,dict(changed=unrelated,added=added))
    ck('git_head_branch_index_unchanged',a.git_state()==b['git'])
    for rel,h in b['native_hashes'].items():ck('vanilla_unchanged.'+rel,a.sha(GAME/rel)==h)
    types=a.catalog('common/subject_types');n=types[TYPE][0]
    for field,value in dict(autonomy_level='3',can_start_own_diplomatic_plays='yes',join_overlord_wars='no',can_have_subjects='yes').items():ck('client_rule.'+field,n.one(field)==value)
    ck('one_new_subject_type_no_legacy_duplicates',all(x not in types for x in ['subject_type_aor1776_kalat_suzerainty','subject_type_aor1776_dp02_allegiance']))
    ck('ladder_client_to_tributary',a.ids(n,'lower_autonomy_subject_type_alternatives')==['subject_type_tributary'])
    n,p=a.catalog('common/diplomatic_actions')[ACTION]
    pact=n.children('pact')[0];ck('regular_income_transfer_zero',pact.one('income_transfer')=='0')
    ck('action_texture',scalar(n.one('texture'))==prior.TEX)
    # Strip only our two independent branches: all old subject calculations must compare exactly.
    s=a.raw(ROOT/LIBERTY);n=parse(s)[0];ours=[c for c in n.children('else_if') if c.children('limit') and c.children('limit')[0].one('is_diplomatic_action_type')==ACTION]
    ck('two_exclusive_client_liberty_branches',len(ours)==2)
    removed=changes(s,[(c.start,c.end,'') for c in ours]);rest=parse(removed)[0];rest.key='liberty_desire_weekly_change'
    ck('native_liberty_value_preserved_outside_client',normalized([rest])==normalized(parse(b['native_liberty_original'])))
    ck('client_thresholds',all(k in s for k in ['multiply = 1 }','multiply = 2.5 }','aor1776_client_prestige_negative','aor1776_client_army_negative']))
    # Boundary and zero-denominator cases evaluated from the installed Paradox expressions.
    parsed_terms=[]
    for label,metric,start,end,cases in [
      ('prestige','prestige','#prestige','#army projection power',[
       (ACTION,0,100,1),(ACTION,100,0,-.10),(ACTION,100,100,.20),
       (ACTION,125,100,-.0125),('tributary',125,100,.24),('tributary',150,100,.20),
       ('tributary',151,100,-151/100/150)]),
      ('army','army_power_projection','#army projection power',"# overlord's overlord",[
       (ACTION,0,100,1),(ACTION,100,0,-.25),(ACTION,250,100,.10),
       (ACTION,251,100,-.0502),('tributary',251,100,5/(2.51*10)),
       ('tributary',500,100,.10),('tributary',501,100,-.0501)])]:
        section=parse(s.split(start,1)[1].split(end,1)[0])
        for action,overlord,subject,expected in cases:
            actual=numeric_term(section,{'action':action,'root.first_country.'+metric:overlord,
              'root.second_country.'+metric:subject,'prestige_to_libery_desire_factor':5,
              'army_projection_to_libery_desire_factor':10})
            ck(f'actual_script_value.{label}.{action}.{overlord}.{subject}',math.isclose(actual,expected,rel_tol=1e-9,abs_tol=1e-9),dict(actual=actual,expected=expected))
            parsed_terms.append(dict(metric=label,action=action,overlord=overlord,subject=subject,actual=actual,expected=expected))
    dump('SCRIPT_VALUE_BOUNDARY_TESTS.json',parsed_terms)
    # Numeric boundary examples exercise both branches and guarantee lighter requirements.
    examples=[]
    for label,threshold,old,divisor,factor,maximum in [('prestige',1,1.5,100,5,.05),('army',2.5,5,50,10,.10)]:
        for ratio in [.5,1,1.25,1.5,2.5,3,5,10]:
            value=-min(max(ratio/divisor,.01),maximum) if ratio>threshold else min(threshold/ratio/factor,.5)
            examples.append(dict(metric=label,overlord_to_subject_ratio=ratio,weekly_component=value))
        ck('lighter_threshold.'+label,threshold<old)
    dump('LIBERTY_BOUNDARY_EXAMPLES.json',dict(note='Two contributions only, not net weekly liberty desire; native zero-power checks and other factors retained.',examples=examples))
    old=a.raw(OUT/'preimages'/ARMY);current=a.raw(ROOT/ARMY);on=eth_node(old);nn=eth_node(current)
    ck('army_other_countries_bytes_unchanged',old[:on.start]==current[:nn.start] and old[on.end:]==current[nn.end:])
    ck('ETH_general_unchanged',normalized(on.children('create_character'))==normalized(nn.children('create_character')))
    units=[u for form in nn.children('create_military_formation') for u in form.children('combat_unit')]
    ck('ETH_10_regular',sum(int(u.one('count')) for u in units if u.one('service_type')!='conscript')==10)
    ck('ETH_15_reserve',sum(int(u.one('count')) for u in units if u.one('service_type')=='conscript')==15)
    ck('ETH_no_unresearched_dragoons',all(u.one('type')=='unit_type:combat_unit_type_irregular_infantry' for u in units))
    ck('ETH_all_recruitment_in_owned_Gonder',all(u.one('state_region')=='s:STATE_GONDER' for u in units))
    cohorts=[]
    for p in t.effective('common/history/pops'):
        for st in walk(parse(a.raw(p))):
            for part in st.children('region_state:ETH'):
                for pop in part.children('create_pop'):cohorts.append(dict(state=st.key,culture=pop.one('culture'),religion=pop.one('religion'),type=pop.one('pop_type','default'),size=int(pop.one('size'))))
    civilian=sum(x['size'] for x in cohorts if x['type']!='slaves')
    law,law_path=a.catalog('common/laws')['law_peasant_levies']
    mods={x.key:x.value for g in law.children('modifier') for x in g.children()}
    rate=float(mods['state_conscription_rate_add']);cap=int(mods['state_building_conscription_center_max_level_add'])
    barracks_cap=int(mods['state_building_barrack_max_level_add'])
    defines=ROOT/'common/defines/00_defines.txt'
    if not defines.exists():defines=GAME/'common/defines/00_defines.txt'
    divisor=int(re.search(r'CONSCRIPTION_CENTER_LEVEL_POPULATION_DIVISOR\s*=\s*(\d+)',a.raw(defines))[1])
    ck('ETH_current_law_values',rate==.04 and cap==25 and barracks_cap==25)
    histories=[n for p in t.effective('common/history/countries') for n in walk(parse(a.raw(p))) if n.key=='c:ETH']
    ck('ETH_peasant_levies_explicit',any(n.one('activate_law')=='law_type:law_peasant_levies' or any(x.value=='law_type:law_peasant_levies' for x in n.children('activate_law')) for n in histories))
    capacity=min(cap,math.floor(civilian*rate/divisor));ck('ETH_conscription_static_capacity_15',capacity>=15)
    ck('ETH_barracks_capacity_10',barracks_cap>=10)
    unit,_=a.catalog('common/combat_unit_types')['combat_unit_type_irregular_infantry']
    ck('ETH_unit_no_technology_gate',not a.ids(unit,'unlocking_technologies'))
    ck('ETH_unit_valid_for_peasant_levies',unit.one('conscript_peasant_levies')=='yes')
    owned=[]
    for p in t.effective('common/history/states'):
        for st in walk(parse(a.raw(p))):
            if st.key=='s:STATE_GONDER':owned += [x for x in st.children('create_state') if x.one('country')=='c:ETH']
    ck('ETH_Gonder_recruitment_state_exists',len(owned)==1)
    dump('ETH_ARMY_CAPACITY.json',dict(total_population=sum(x['size'] for x in cohorts),civilian_cohorts=civilian,law='law_peasant_levies',law_source=source(law_path),rate=rate,cap_per_state=cap,barracks_cap=barracks_cap,divisor=divisor,divisor_source=source(defines),static_ceiling=capacity,regular_requested=10,reserve_requested=15,cohorts=cohorts,limits='Ceiling is not manpower or employment observed in engine. Only peasants can be conscripted; actual recruitment and costs require runtime validation.'))
    rows=inventory();eth=[r for r in rows if r['overlord']=='ETH']
    ck('ETH_three_nominal_clients',sorted((r['subject'],r['action']) for r in eth)==[(x,ACTION) for x in ['GJM','TGR','WLO']])
    others=lambda rows:sorted((r['overlord'],r['subject'],r['action']) for r in rows if r['overlord']!='ETH')
    ck('other_starting_relations_unchanged',others(rows)==others(b['starting_relations']))
    for lang in ['french','english']:
        rel=f'localization/{lang}/1776_protected_state_l_{lang}.yml';s=a.raw(ROOT/rel);loc=entries(lang)
        ck(lang+'.BOM',(ROOT/rel).read_bytes().startswith(b'\xef\xbb\xbf'))
        ck(lang+'.new_name',('État client' if lang=='french' else 'Client state') in s)
        ck(lang+'.no_old_visible_name',('protégé' if lang=='french' else 'protected state') not in s.lower())
        keys=re.findall(r'^\s*([^\s:]+):\d+ ',s,re.M)
        ck(lang+'.no_duplicate_keys',all(len(loc[k])==1 for k in keys))
        for key in re.findall(r'desc = "(aor1776_client_[^"]+)"',a.raw(ROOT/LIBERTY)):ck(lang+'.liberty_label.'+key,key in loc)
        native=entries(lang,root=GAME/'localization')
        ck(lang+'.all_native_notification_suffixes',all(ACTION+key[len('protectorate'):] in loc for key in native if key.startswith('protectorate_')))
        ck(lang+'.aliases_resolve',all(key in loc for key in re.findall(r'\$([^$]+)\$',s)))
        ck(lang+'.parseable_localization_lines',all(not line.strip() or line==f'l_{lang}:' or re.fullmatch(r' [^\s:]+:\d+ "[^"\r\n]*"',line) for line in s.splitlines()))
    for rel,size in ASSETS.items():
        p=ROOT/rel;data=p.read_bytes();im=Image.open(p).convert('RGBA');alpha=im.getchannel('A')
        ck('asset.'+rel,im.size==(size,size) and struct.unpack_from('<I',data,28)[0]==math.floor(math.log2(size))+1 and alpha.getextrema()==(0,255) and all(alpha.getpixel(pt)==0 for pt in [(0,0),(size-1,0),(0,size-1),(size-1,size-1)]))
    ck('original_art_archived_exactly',a.sha(ROOT/MASTER/'user_original.png')==b['source_original_sha256'])
    ck('concept_icon_binding',scalar(a.catalog('common/game_concepts')['concept_'+ACTION][0].one('texture'))==prior.TEX)
    gui=a.raw(ROOT/'gui/1776_protected_state_texticons.gui')
    ck('action_and_subject_text_glyph_bindings',all('icon = "'+k+'"' in gui for k in [ACTION,TYPE]))
    for filename in ['32_subjects_raise_payments.txt','33_subjects_decrease_payments.txt']:
        n=parse(a.raw(ROOT/'common/diplomatic_actions'/filename))[0]
        ck('client_no_supplemental_payments.'+filename,TYPE in str(normalized(n.children('potential'))) and TYPE in str(normalized(n.children('pact')[0].children('requirement_to_maintain'))))
    result=dict(status='PASS_STATIC' if all(c['passed'] for c in checks) else 'FAIL_STATIC',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,runtime='NOT_RUN',human_validation='NOT_ACQUIRED')
    dump('STATIC_CHECKS.json',result);print(result['status'],result['passed'],'/',result['total']);print([c for c in checks if not c['passed']])
    return 0 if result['status']=='PASS_STATIC' else 1

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['install','validate','inventory']);arg=ap.parse_args()
    if arg.mode=='install':install()
    elif arg.mode=='validate':sys.exit(validate())
    else:print(json.dumps(inventory(),ensure_ascii=False,indent=2))
