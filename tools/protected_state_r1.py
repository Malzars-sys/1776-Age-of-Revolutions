"""Merge the two DP non-paying subject types into one generic protected state.

No Git/vanilla/map writes. --install captures current files, applies bounded
edits, preserves preimages and exports the imagegen master mechanically.
--validate writes current evidence in this task's private report only.
"""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import argparse,json,re,hashlib,struct,shutil,subprocess
from PIL import Image,ImageDraw
import audit_anzin_regional_infrastructure as a
from validate_diplomacy_ottoman_1776 import parse,walk,scalar,normalized
from localization_duplicate_audit import entries

ROOT=a.ROOT; GAME=a.GAME
OUT=ROOT/'docs/reports/diplomacy/PROTECTED_STATE_R1'
ACTION='aor1776_protected_state';TYPE='subject_type_'+ACTION
OLD=['aor1776_kalat_suzerainty','aor1776_dp02_allegiance']
MASTER='workshop_assets/source/PROTECTED_STATE_R1/protected_state_v2.png'
GENERATED=Path('C:/Users/simeo/.codex/generated_images/01a149d5-1620-7bf2-bf90-7fa9bf443072/exec-2ee5adc9-1054-48be-a488-1df6486e3c3b.png')
TEX='gfx/interface/icons/diplomatic_action_icons/'+ACTION+'.dds'
SMALL='gfx/interface/icons/diplomatic_action_icons/'+ACTION+'_15.dds'
NEW_TYPES='common/subject_types/zz_1776_protected_state.txt'
NEW_ACTION='common/diplomatic_actions/1776_protected_state.txt'
RANKS='great_power major_power minor_power insignificant_power unrecognized_major_power unrecognized_regional_power unrecognized_power'
SCRIPTS=[]

def dump(name,v):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def load(name):return json.loads((OUT/name).read_text(encoding='utf8'))
def read(rel):return a.raw(ROOT/rel) if (ROOT/rel).exists() else a.raw(GAME/rel)
def edits(s,ops):
    for lo,hi,v in sorted(ops,reverse=True):s=s[:lo]+v+s[hi:]
    return s
def field(s,key,child,value):
    n=next(n for n in parse(s) if n.key==key);found=n.children(child)
    if found:
        assert len(found)==1
        t=found[0];return edits(s,[(t.start,t.end,child+' = '+value)])
    return edits(s,[(n.end-1,n.end-1,'\n '+child+' = '+value+'\n')])

def notification_strings(lang):
    fr=lang=='french'
    titles={
     'action_notification_break':'Protection levée' if fr else 'Protection ended',
     'proposal_notification_break':'Fin de la protection demandée' if fr else 'End of protection requested',
     'proposal_break_accepted':'Protection levée' if fr else 'Protection ended',
     'proposal_break_declined':'Fin de protection refusée' if fr else 'End of protection refused',
     'proposal_third_party_accepted':'Un État accepte une protection' if fr else 'A state accepts protection',
     'proposal_third_party_declined':'Une protection est refusée' if fr else 'Protection declined',
     'action_third_party_notification_break':'Protection levée' if fr else 'Protection ended',
     'proposal_third_party_break_accepted':'Protection levée' if fr else 'Protection ended',
     'proposal_third_party_break_declined':'Fin de protection refusée' if fr else 'End of protection refused'}
    descs={
     'action_notification_break':'[INITIATOR_COUNTRY.GetName] a rompu le lien de protection.' if fr else '[INITIATOR_COUNTRY.GetName] has ended the protection agreement.',
     'proposal_notification_break':'[INITIATOR_COUNTRY.GetName] demande la fin du lien de protection.' if fr else '[INITIATOR_COUNTRY.GetName] requests an end to the protection agreement.',
     'proposal_break_accepted':'[TARGET_COUNTRY.GetName] a accepté la fin du lien de protection.' if fr else '[TARGET_COUNTRY.GetName] has agreed to end the protection agreement.',
     'proposal_break_declined':'[TARGET_COUNTRY.GetName] a refusé la fin du lien de protection.' if fr else '[TARGET_COUNTRY.GetName] has refused to end the protection agreement.',
     'proposal_third_party_accepted':'[TARGET_COUNTRY.GetName] a accepté de devenir un État protégé de [INITIATOR_COUNTRY.GetName].' if fr else '[TARGET_COUNTRY.GetName] has agreed to become a protected state of [INITIATOR_COUNTRY.GetName].',
     'proposal_third_party_declined':'[TARGET_COUNTRY.GetName] a refusé l’offre de protection de [INITIATOR_COUNTRY.GetName].' if fr else '[TARGET_COUNTRY.GetName] has declined the offer of protection from [INITIATOR_COUNTRY.GetName].',
     'action_third_party_notification_break':'[INITIATOR_COUNTRY.GetName] a mis fin à la protection de [TARGET_COUNTRY.GetName].' if fr else '[INITIATOR_COUNTRY.GetName] has ended its protection of [TARGET_COUNTRY.GetName].',
     'proposal_third_party_break_accepted':'[TARGET_COUNTRY.GetName] a accepté de mettre fin au lien de protection avec [INITIATOR_COUNTRY.GetName].' if fr else '[TARGET_COUNTRY.GetName] has agreed to end its protection agreement with [INITIATOR_COUNTRY.GetName].',
     'proposal_third_party_break_declined':'[TARGET_COUNTRY.GetName] a refusé de mettre fin au lien de protection avec [INITIATOR_COUNTRY.GetName].' if fr else '[TARGET_COUNTRY.GetName] has refused to end its protection agreement with [INITIATOR_COUNTRY.GetName].'}
    out={ACTION+'_'+k+'_name':v for k,v in titles.items()}
    out.update({ACTION+'_'+k+'_desc':v for k,v in descs.items()})
    out[ACTION+'_proposal_notification_break_effects_desc']='L’État protégé retrouvera son indépendance.' if fr else 'The protected state will regain its independence.'
    return out

def payment_maintenance(s):
    # Also covers autonomy granted through war goals rather than the UI action.
    p=next(n for n in walk(parse(s)) if n.key=='pact')
    extra='\n requirement_to_maintain = { trigger = { scope:target_country = { NOT = { is_subject_type = '+TYPE+' } } } }\n'
    return edits(s,[(p.end-1,p.end-1,extra)])

def complete_ui():
    assert not (OUT/'UI_COMPLETION.json').exists()
    installed=load('INSTALLED.json')['files'];expected={}
    for lang in ['french','english']:
        rel=f'localization/{lang}/1776_protected_state_l_{lang}.yml'
        assert a.sha(ROOT/rel)==installed[rel],('Concurrent edit',rel)
        expected[rel]=read(rel)+''.join(f' {k}:0 "{v}"\n' for k,v in notification_strings(lang).items())
    for name in ['32_subjects_raise_payments.txt','33_subjects_decrease_payments.txt']:
        rel='common/diplomatic_actions/'+name
        assert a.sha(ROOT/rel)==installed[rel],('Concurrent edit',rel)
        expected[rel]=payment_maintenance(read(rel))
    dump('UI_COMPLETION.json',dict(reason='Complete all native notification suffixes and automatically clear supplemental payment pacts when status changes outside the UI.',before={r:a.sha(ROOT/r) for r in expected},expected=expected))
    for rel,s in expected.items():
        assert a.sha(ROOT/rel)==installed[rel]
        (ROOT/rel).write_bytes((b'\xef\xbb\xbf' if rel.endswith('.yml') else b'')+s.encode('utf8'))

def complete_suffixes():
    assert not (OUT/'UI_SUFFIX_COMPLETION.json').exists()
    latest=load('UI_COMPLETION.json')['expected'];expected={}
    for lang in ['french','english']:
        rel=f'localization/{lang}/1776_protected_state_l_{lang}.yml';s=read(rel)
        assert s==latest[rel],('Concurrent edit',rel)
        native=entries(lang,root=GAME/'localization')
        for key,values in native.items():
            if key.startswith(('protectorate_effect_desc_','protectorate_trigger_desc_','protectorate_trigger_false_desc_')):
                new=ACTION+key[len('protectorate'):]
                value=values[-1][2].replace('[concept_protectorate','[concept_'+ACTION)
                s+=f' {new}:0 "{value}"\n'
        expected[rel]=s
    dump('UI_SUFFIX_COMPLETION.json',dict(reason='Match the native effect/trigger tooltip suffix contract, retaining native country expressions and changing only the subject concept.',before={r:a.sha(ROOT/r) for r in expected},expected=expected))
    for rel,s in expected.items():
        assert read(rel)==latest[rel]
        (ROOT/rel).write_bytes(b'\xef\xbb\xbf'+s.encode('utf8'))

def restore_standard_autonomy(s):
    """Prove unrelated/HRE action bytes survive by erasing just our wrappers."""
    ops=[]
    def visit(nodes):
        for i,n in enumerate(nodes):
            limits=n.children('limit')
            typ=limits[0].one('is_subject_type') if n.key=='if' and limits else None
            if i+1<len(nodes) and nodes[i+1].key=='else' and (
               typ==TYPE and n.one('change_subject_type')=='subject_type_tributary' or
               typ=='subject_type_tributary' and n.one('change_subject_type')==TYPE):
                key='decrease_autonomy' if typ==TYPE else 'increase_autonomy'
                if nodes[i+1].one(key)=='yes':ops.append((n.start,nodes[i+1].end,key+' = yes'));continue
            visit(n.children())
    visit(parse(s));return edits(s,ops),len(ops)

def build():
    result={}
    # Keep filename overrides to suppress old definitions, not live aliases:
    # GetSubjectTypes must contain ONE new entry, not two renamed old entries.
    for p in ['common/subject_types/1776_dp01.txt','common/subject_types/1776_dp02.txt',
              'common/diplomatic_actions/1776_dp01.txt','common/diplomatic_actions/1776_dp02.txt']:
        result[p]='# Consolidated into '+TYPE+' / '+ACTION+'. Legacy definition intentionally removed.\n'
    n=a.catalog('common/subject_types')['subject_type_aor1776_kalat_suzerainty'][0]
    s=read('common/subject_types/1776_dp01.txt')[n.start:n.end].replace(n.key,TYPE,1)
    for k,v in dict(diplomatic_action=ACTION,autonomy_level='3',category='same_as_vassal',
        lower_autonomy_subject_type_alternatives='{ subject_type_tributary }',
        higher_autonomy_subject_type_alternatives='{}',
        same_autonomy_subject_type_alternatives='{ subject_type_protectorate }',
        valid_overlord_ranks='{ unrecognized_major_power unrecognized_regional_power unrecognized_power }').items():s=field(s,TYPE,k,v)
    # Exact existing 0-payment/independent-diplomacy flags survive the merge.
    parts=[s]
    for native in ['subject_type_tributary','subject_type_vassal']:
        nn,path=a.catalog('common/subject_types')[native];text=a.raw(path)[nn.start:nn.end]
        if native=='subject_type_tributary':text=field(text,native,'higher_autonomy_subject_type_alternatives','{ '+TYPE+' }')
        ranks=a.ids(nn,'valid_overlord_ranks')
        if 'unrecognized_power' not in ranks:ranks.append('unrecognized_power')
        text=field(text,native,'valid_overlord_ranks','{ '+' '.join(ranks)+' }')
        parts.append(text.replace(native+' = {','REPLACE_OR_CREATE:'+native+' = {',1))
    result[NEW_TYPES]='# Generic unrecognized ladder: protected 3 -> tributary 2 -> vassal 1 -> annexation.\n'+'\n\n'.join(parts)+'\n'
    result[NEW_ACTION]=f'''# Voluntary protected-state agreement; no country-specific whitelist.
{ACTION} = {{
 groups = {{ general }}
 texture = "{TEX}"
 requires_approval = yes
 show_in_lens = yes
 potential = {{
  is_country_type = unrecognized
  scope:target_country = {{
   is_subject = no
   OR = {{ is_country_type = recognized is_country_type = unrecognized is_country_type = colonial }}
   NOT = {{ this = root }}
  }}
 }}
 possible = {{
  is_diplomatic_play_committed_participant = no
  scope:target_country = {{ is_diplomatic_play_committed_participant = no NOT = {{ has_war_with = root }} }}
  "relations(scope:target_country)" >= relations_threshold:cordial
 }}
 pact = {{
  cost = 0 has_junior_participant = yes subject_type = {TYPE}
  income_transfer = 0 second_country_gets_income_transfer = no income_transfer_based_on_second_country = yes
  actor_can_break = {{ is_diplomatic_play_committed_participant = no }}
  target_can_break = {{ is_diplomatic_play_committed_participant = no }}
 }}
 ai = {{
  # Players may offer this to any eligible country; no new global AI spam.
  will_propose = {{ always = no }} will_break = {{ always = no }}
  accept_score = {{ value = -50
   if = {{ limit = {{ "relations(scope:actor)" >= relations_threshold:friendly }} add = 75 }}
   if = {{ limit = {{ has_attitude = {{ who = scope:actor attitude = protective }} }} add = 25 }}
  }}
 }}
}}
'''
    for p in ['common/history/diplomacy/1776_dp01.txt','common/history/diplomacy/1776_dp02.txt','common/history/diplomacy/1776_dp03.txt']:
        s=read(p)
        for old in OLD:s=re.sub(r'(?<=type = )'+old+r'\b',ACTION,s)
        result[p]=s
    # Preserve the live HRE branches. Only the ordinary accept-effect leaf is
    # wrapped; all cooldowns, liberty desire, costs and third-country effects stay.
    for p in ['common/diplomatic_actions/37_subjects_decrease_autonomy.txt','common/diplomatic_actions/38_subjects_increase_autonomy.txt']:
        s=read(p);ops=[]
        for action in parse(s):
            for effect in action.children('accept_effect'):
                for leaf in walk(effect.children()):
                    if leaf.key=='decrease_autonomy':
                        v=f'if = {{ limit = {{ is_subject_type = {TYPE} }} change_subject_type = subject_type_tributary }} else = {{ decrease_autonomy = yes }}'
                        ops.append((leaf.start,leaf.end,v))
                    if leaf.key=='increase_autonomy':
                        v=f'''if = {{ limit = {{ is_subject_type = subject_type_tributary }}
 change_subject_type = {TYPE}
 # Existing payment-adjustment pacts must not survive the non-paying status.
 overlord = {{
  if = {{ limit = {{ has_diplomatic_pact = {{ who = prev type = raise_payments }} }} remove_diplomatic_pact = {{ country = prev type = raise_payments }} }}
  if = {{ limit = {{ has_diplomatic_pact = {{ who = prev type = decrease_payments }} }} remove_diplomatic_pact = {{ country = prev type = decrease_payments }} }}
 }}
}} else = {{ increase_autonomy = yes }}'''
                        ops.append((leaf.start,leaf.end,v))
        assert len(ops)==(1 if '/37_' in p else 2),(p,len(ops))
        result[p]=edits(s,ops)
    # Like a protectorate, this tier must be explicitly ineligible for payment
    # adjustment, even if the parties have an unrelated monetary treaty.
    for name in ['32_subjects_raise_payments.txt','33_subjects_decrease_payments.txt']:
        p='common/diplomatic_actions/'+name;s=read(p)
        marker='is_subject_type = subject_type_protectorate'
        assert s.count(marker)==1,(p,s.count(marker))
        result[p]=s.replace(marker,marker+'\n\t\t\t\t\tis_subject_type = '+TYPE,1)
    result['common/game_concepts/1776_protected_state.txt']=f'concept_{ACTION} = {{ texture = "{TEX}" }}\n'
    result['gui/1776_protected_state_texticons.gui']='\n'.join(
        'texticon = { icon = "'+key+'" '+''.join(f'iconsize = {{ texture = "{TEX}" size = {{ {size} {size} }} offset = {{ 0 7 }} fontsize = {font} }} ' for font,size in [(18,25),(22,30),(24,32),(32,42)])+'}'
        for key in [ACTION,TYPE])+ '\n'
    for lang in ['french','english']:
        fr=lang=='french';name='État protégé' if fr else 'Protected state'
        desc=('Un État protégé reconnaît la suzeraineté d’un pays non reconnu sans lui verser de tribut régulier. Il conserve son gouvernement, ses forces et ses initiatives diplomatiques, et ne rejoint pas automatiquement les guerres du suzerain. Le resserrement du lien le transforme en tributaire, puis en vassal avant une éventuelle intégration.' if fr else
              'A protected state acknowledges an unrecognized country’s suzerainty without paying regular tribute. It retains its government, armed forces and diplomatic initiatives, and does not automatically join its overlord’s wars. Closer subordination makes it a tributary, then a vassal before possible integration.')
        strings={ACTION:name,TYPE:f'@{ACTION}! ${TYPE}_no_icon$',TYPE+'_no_icon':name,
         TYPE+'_desc':desc,'concept_'+ACTION:name,'concept_'+ACTION+'_desc':desc,
         ACTION+'_desc':desc,ACTION+'_pact_desc':desc,
         ACTION+'_action_name':name,ACTION+'_action_propose_name':'Proposer notre protection' if fr else 'Offer our protection',
         ACTION+'_action_break_name':'Rompre le lien de protection' if fr else 'End the protection agreement',
         ACTION+'_action_ask_to_break_name':'Demander la fin de la protection' if fr else 'Request an end to protection',
         ACTION+'_proposal_notification_name':'Une offre de protection' if fr else 'An offer of protection',
         ACTION+'_proposal_notification_desc':'[INITIATOR_COUNTRY.GetName] nous propose de devenir son État protégé, sans tribut financier régulier.' if fr else '[INITIATOR_COUNTRY.GetName] offers to make us its protected state without regular financial tribute.',
         ACTION+'_proposal_notification_effects_desc':desc,
         ACTION+'_proposal_accepted_name':'Protection acceptée' if fr else 'Protection accepted',
         ACTION+'_proposal_accepted_desc':'[TARGET_COUNTRY.GetName] a accepté notre protection.' if fr else '[TARGET_COUNTRY.GetName] has accepted our protection.',
         ACTION+'_proposal_declined_name':'Protection refusée' if fr else 'Protection declined',
         ACTION+'_proposal_declined_desc':'[TARGET_COUNTRY.GetName] a refusé notre offre de protection.' if fr else '[TARGET_COUNTRY.GetName] has declined our offer of protection.',
         ACTION+'_action_notification_name':f'${ACTION}_proposal_notification_name$',
         ACTION+'_action_notification_desc':f'${ACTION}_proposal_notification_desc$',
         ACTION+'_pact_break_name':'Fin de la protection' if fr else 'Protection ended',
         ACTION+'_pact_break_desc':'Le lien de protection entre les deux pays a été rompu.' if fr else 'The protection agreement between the two countries has ended.'}
        # Localization compatibility only; no legacy subject/action definitions.
        for old in OLD:strings['subject_type_'+old+'_no_icon']=f'${TYPE}_no_icon$'
        result[f'localization/{lang}/1776_protected_state_l_{lang}.yml']='l_'+lang+':\n'+''.join(f' {k}:0 "{v}"\n' for k,v in strings.items())
        for p in [f'localization/{lang}/replace/1776_dp01_l_{lang}.yml',f'localization/{lang}/replace/1776_dp02_l_{lang}.yml']:
            s=read(p)
            for old in OLD:
                for suffix,target in [('',ACTION),('_desc',ACTION+'_desc'),('_pact_desc',ACTION+'_pact_desc')]:
                    s=re.sub(r'(?m)^( '+re.escape(old+suffix)+r':(?:0)? )"[^"\r\n]*"',lambda m:m[1]+'"$'+target+'$"',s)
                for suffix,target in [('',TYPE),('_desc',TYPE+'_desc')]:
                    s=re.sub(r'(?m)^( '+re.escape('subject_type_'+old+suffix)+r':(?:0)? )"[^"\r\n]*"',lambda m:m[1]+'"$'+target+'$"',s)
            result[p]=s
    return result

def hashes():
    return {p.relative_to(ROOT).as_posix():a.sha(p) for folder in ['common','events','gui','gfx','localization','map_data','docs/reports/map/SERG_CLOSURE'] for p in (ROOT/folder).rglob('*') if p.is_file()}

def dds(im,size):
    im=im.copy();im.thumbnail((round(size*.94),round(size*.94)),Image.Resampling.LANCZOS)
    canvas=Image.new('RGBA',(size,size));canvas.alpha_composite(im,((size-im.width)//2,(size-im.height)//2))
    levels=[];s=size
    while s>=1:
        levels.append(canvas.resize((s,s),Image.Resampling.LANCZOS).tobytes('raw','BGRA'));s=s//2
    h=bytearray(128);h[:4]=b'DDS '
    for off,v in [(4,124),(8,0x2100f),(12,size),(16,size),(20,size*4),(28,len(levels)),(76,32),(80,0x41),(88,32),(92,0xff0000),(96,0xff00),(100,0xff),(104,0xff000000),(108,0x401008)]:struct.pack_into('<I',h,off,v)
    return bytes(h)+b''.join(levels),canvas

def install():
    assert not (OUT/'BASELINE.json').exists(),'Already installed/captured; inspect existing receipt.'
    files=build();before=hashes();git=a.git_state()
    # Preimages are the CURRENT shared workspace; never an old DP baseline.
    for rel in files:
        p=ROOT/rel
        if p.exists():dest=OUT/'preimages'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
    baseline=dict(utc=datetime.now(timezone.utc).isoformat(),git=git,hashes=before,
       edited_existing={r:before[r] for r in files if r in before},new_text=[r for r in files if r not in before],
       native={str(p.relative_to(GAME)):a.sha(p) for folder in ['common/subject_types','common/diplomatic_actions'] for p in (GAME/folder).glob('*') if p.is_file()},
       expected=files,old_subjects={k:normalized([n]) for k,(n,p) in a.catalog('common/subject_types').items()},
       generated_master=str(GENERATED),generated_sha256=a.sha(GENERATED))
    dump('BASELINE.json',baseline)
    assert all(a.sha(ROOT/r)==h for r,h in baseline['edited_existing'].items()),'Concurrent edit; review before writing.'
    for rel,s in files.items():
        p=ROOT/rel;p.parent.mkdir(parents=True,exist_ok=True)
        if rel in before:assert a.sha(p)==before[rel],('Concurrent edit',rel)
        else:assert not p.exists(),('New path collision',rel)
        p.write_bytes((b'\xef\xbb\xbf' if p.suffix=='.yml' else b'')+s.encode('utf8'))
    master=ROOT/MASTER;assert not master.exists();master.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(GENERATED,master)
    im=Image.open(master).convert('RGBA');alpha=im.getchannel('A')
    bbox=alpha.point(lambda x:255 if x>=24 else 0).getbbox();assert bbox
    # Only crop transparent padding, resize and encode. Artwork/alpha is imagegen.
    im=im.crop(bbox)
    assets={TEX:128,SMALL:30,'gfx/interface/icons/diplomatic_action_icons/'+TYPE+'.dds':30,
            'gfx/interface/icons/lens_toolbar_icons/'+ACTION+'.dds':64,
            'gfx/interface/icons/lens_toolbar_icons/'+ACTION+'_break.dds':64}
    for rel,size in assets.items():
        p=ROOT/rel;assert not p.exists();p.parent.mkdir(parents=True,exist_ok=True);raw,preview=dds(im,size);p.write_bytes(raw)
        cache=ROOT/'.asset-cache/protected_state_r1';cache.mkdir(parents=True,exist_ok=True);preview.save(cache/(p.stem+'_'+str(size)+'.png'))
    dump('ASSETS.json',dict(master=MASTER,master_sha256=a.sha(master),bbox=bbox,
        generation='built-in image_gen, revision 2 with three direct vanilla references',human_approval_claimed=False,
        rejected_revision='exec-58afd1b9-aa75-4231-bd2c-95eefe6b5164.png; not installed',
        textures={r:dict(size=s,sha256=a.sha(ROOT/r)) for r,s in assets.items()}))
    dump('INSTALLED.json',dict(status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',files={r:a.sha(ROOT/r) for r in files},assets=assets))
    print('Installed one generic subject type, consolidated four initial bonds, and exported five icon bindings.',flush=True)

def validate():
    b=load('BASELINE.json');assets=load('ASSETS.json');checks=[]
    if (OUT/'UI_COMPLETION.json').exists():b['expected'].update(load('UI_COMPLETION.json')['expected'])
    if (OUT/'UI_SUFFIX_COMPLETION.json').exists():b['expected'].update(load('UI_SUFFIX_COMPLETION.json')['expected'])
    def c(name,value,detail=None):checks.append(dict(name=name,passed=bool(value),detail=detail))
    types=a.catalog('common/subject_types');actions=a.catalog('common/diplomatic_actions')
    for old in OLD:c('removed duplicate type '+old,'subject_type_'+old not in types);c('removed duplicate action '+old,old not in actions)
    c('single new type',TYPE in types)
    n=types[TYPE][0];action=actions[ACTION][0];pact=action.children('pact')[0]
    for field,value in [('diplomatic_action',ACTION),('autonomy_level','3'),('category','same_as_vassal'),('use_overlord_ruler','no'),('join_overlord_wars','no'),('can_start_own_diplomatic_plays','yes'),('can_have_subjects','yes')]:c(field,n.one(field)==value)
    c('unrecognized overlords only',a.ids(n,'valid_overlord_country_types')==['unrecognized'])
    c('no whitelist',not any(x.key.startswith('c:') for x in walk([action])))
    c('voluntary general-purpose offer',action.one('requires_approval')=='yes' and 'always = no' not in str(action.one('potential')))
    c('zero base payments',pact.one('income_transfer')=='0')
    c('protected -> tributary',a.ids(n,'lower_autonomy_subject_type_alternatives')==['subject_type_tributary'])
    t=types['subject_type_tributary'][0];v=types['subject_type_vassal'][0]
    c('tributary -> protected',a.ids(t,'higher_autonomy_subject_type_alternatives')==[TYPE])
    c('tributary -> vassal',a.ids(t,'lower_autonomy_subject_type_alternatives')==['subject_type_vassal'])
    c('vassal -> tributary',a.ids(v,'higher_autonomy_subject_type_alternatives')==['subject_type_tributary'])
    c('levels strictly ordered',int(n.one('autonomy_level'))>int(t.one('autonomy_level'))>int(v.one('autonomy_level')))
    c('vassal integration eligibility preserved',v.one('annex_on_country_formation')=='yes')
    for key,old in b['old_subjects'].items():
        if key not in ['subject_type_aor1776_kalat_suzerainty','subject_type_aor1776_dp02_allegiance','subject_type_tributary','subject_type_vassal']:
            c('other subject unchanged '+key,key in types and json.loads(json.dumps(normalized([types[key][0]])))==old)
    bonds=[]
    for rel in ['common/history/diplomacy/1776_dp01.txt','common/history/diplomacy/1776_dp02.txt','common/history/diplomacy/1776_dp03.txt']:
        for x in walk(parse(read(rel))):
            if x.key=='create_diplomatic_pact':bonds.append((x.one('country'),x.one('type')))
    c('four initial bonds migrated',Counter(bonds)==Counter((x,ACTION) for x in ['c:KAL','c:BHW','c:LBL','c:D3S']),bonds)
    for rel,s in b['expected'].items():
        c('expected bounded file '+rel,a.raw(ROOT/rel)==s)
        if rel.endswith(('.txt','.gui')):
            try:parse(a.raw(ROOT/rel));ok=True
            except Exception:ok=False
            c('parse '+rel,ok)
    for name,count in [('37_subjects_decrease_autonomy.txt',1),('38_subjects_increase_autonomy.txt',2)]:
        rel='common/diplomatic_actions/'+name
        restored,nwrappers=restore_standard_autonomy(read(rel))
        c('targeted autonomy wrappers '+name,nwrappers==count)
        c('all other autonomy and HRE action bytes preserved '+name,restored==a.raw(OUT/'preimages'/rel))
    # No residual live command can reference either removed subject/action.
    stale=[]
    for folder in ['subject_types','diplomatic_actions','history/diplomacy','scripted_effects','on_actions','events']:
        for path in (ROOT/'common'/folder).glob('*.txt'):
            for leaf in walk(parse(a.raw(path))):
                if isinstance(leaf.value,str) and scalar(leaf.value) in OLD+['subject_type_'+x for x in OLD]:stale.append((str(path),leaf.key,leaf.value))
    c('no dangling legacy runtime references',not stale,stale)
    for lang in ['french','english']:
        loc=entries(lang);new=ROOT/f'localization/{lang}/1776_protected_state_l_{lang}.yml'
        c('BOM '+lang,new.read_bytes().startswith(b'\xef\xbb\xbf'))
        keys=[TYPE,TYPE+'_no_icon',TYPE+'_desc',ACTION,ACTION+'_desc',ACTION+'_pact_desc',ACTION+'_action_propose_name','concept_'+ACTION,'concept_'+ACTION+'_desc']
        for k in keys:c('unique localized '+lang+' '+k,len(loc.get(k,[]))==1)
        for line in a.raw(new).splitlines()[1:]:
            for k in re.findall(r'\$([^$]+)\$',line):c('resolved alias '+lang+' '+k,k in loc)
        c('plain table name '+lang,'@' not in loc[TYPE+'_no_icon'][0][2])
        native_loc=entries(lang,root=GAME/'localization')
        for native_key in native_loc:
            if native_key.startswith('protectorate_'):
                key=ACTION+native_key[len('protectorate'):]
                c('all native action UI suffixes '+lang+' '+key,key in loc)
    icons=read('gui/1776_protected_state_texticons.gui')
    for k in [ACTION,TYPE]:c('text glyph '+k,'icon = "'+k+'"' in icons)
    c('action texture bound',scalar(action.one('texture'))==TEX)
    c('concept texture bound',scalar(a.catalog('common/game_concepts')['concept_'+ACTION][0].one('texture'))==TEX)
    for rel,spec in assets['textures'].items():
        raw=(ROOT/rel).read_bytes();size=spec['size'];im=Image.open(ROOT/rel).convert('RGBA')
        c('DDS size '+rel,im.size==(size,size))
        c('DDS BGRA '+rel,[struct.unpack_from('<I',raw,o)[0] for o in [92,96,100,104]]==[0xff0000,0xff00,0xff,0xff000000])
        expected=128;x=size;count=0
        while x>=1:expected+=x*x*4;count+=1;x//=2
        c('DDS complete mipmaps '+rel,len(raw)==expected and struct.unpack_from('<I',raw,28)[0]==count)
        c('DDS alpha '+rel,im.getchannel('A').getextrema()==(0,255) and im.getpixel((0,0))[3]==0)
    for name in ['32_subjects_raise_payments.txt','33_subjects_decrease_payments.txt']:
        c('no supplementary tax '+name,TYPE in read('common/diplomatic_actions/'+name))
        node=next(n for n in parse(read('common/diplomatic_actions/'+name)))
        maint=[x for x in node.children('pact')[0].children('requirement_to_maintain') if TYPE in str(normalized([x]))]
        c('supplementary pact auto ends on protection '+name,len(maint)==1)
    for rel,h in b['native'].items():c('vanilla unchanged '+rel,a.sha(GAME/rel)==h)
    now=hashes();permitted=set(b['expected'])|set(assets['textures']);external={r:dict(before=h,after=now.get(r)) for r,h in b['hashes'].items() if r not in permitted and now.get(r)!=h}
    c('preexisting unrelated files preserved',not external,external)
    c('Git HEAD branch index preserved',a.git_state()==b['git'])
    dump('STATIC_CHECKS.json',dict(status='PASS_STATIC' if all(x['passed'] for x in checks) else 'FAIL_STATIC',passed=sum(x['passed'] for x in checks),total=len(checks),checks=checks,external_delta=external,runtime='NOT_RUN',human_validation='NONE_ADDED'))
    report()
    dump('DELIVERY_MANIFEST.json',dict(utc=datetime.now(timezone.utc).isoformat(),status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' if all(x['passed'] for x in checks) else 'STATIC_CHECKS_FAILED',
         files={r:a.sha(ROOT/r) for r in list(b['expected'])+list(assets['textures'])+[MASTER]},
         controls={name:a.sha(OUT/name) for name in ['STATIC_CHECKS.json','REPORT.md','ASSETS.json','ASSET_PROMPTS.json']},runtime='NOT_RUN'))
    print(json.dumps(dict(passed=sum(x['passed'] for x in checks),total=len(checks),failed=[x for x in checks if not x['passed']]),ensure_ascii=False,indent=2))
    if not all(x['passed'] for x in checks):raise SystemExit(1)

def report():
    qa=load('STATIC_CHECKS.json');assets=load('ASSETS.json')
    text=f'''# États protégés — fusion des vassalités non reconnues

Statut : {'IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' if qa['status']=='PASS_STATIC' else 'STATIC_CHECKS_FAILED'}. Référence de cette passe : demande utilisateur du 31 octobre 2026.

Un seul type générique remplace « Suzeraineté durranie sur Kalat » et « Allégeance traditionnelle » : **État protégé**. Les anciennes définitions sont supprimées par leurs propres fichiers d’override, pas conservées comme deux alias de types. Les anciens libellés sont des renvois de localisation uniquement.

Les quatre relations initiales DUR–KAL, DUR–BHW, DUR–D3S et KAL–LBL utilisent le même pacte. Aucune frontière, population, institution, armée ou recette n’est changée. Raguse, les protections kazakhes et le système impérial du SERG restent hors fusion.

Progression : **État protégé (autonomie 3, 0 % de tribut) → Tributaire (2, 20 % natifs) → Vassal (1, 30 % natifs) → Intégration**. Le retour Tributaire → État protégé est ajouté. Les actions normales gardent leurs exigences de désir de liberté et leurs délais. Le niveau numérique 3 n’a pas de plafond identifié dans les définitions locales ; sa présentation dans le moteur reste à contrôler. Les branches normales sont explicitement routées pour éviter un saut d’étape.

Le premier niveau conserve gouvernement, forces, diplomatie propre et absence d’entrée automatique en guerre ; aucun versement régulier ni ajustement fiscal n’y est autorisé. Le suzerain doit être non reconnu. Les pays décentralisés sont exclus. Les trois rangs non reconnus peuvent être suzerains ; les règles de rang supérieur des étapes tributaires/vassales restent appliquées. Une proposition volontaire générique permet de réutiliser ce lien hors des Durrani ; l’IA peut y répondre, sans nouvelle campagne automatique de propositions mondiales.

## Icône et affichage

La première génération a été rejetée par l’utilisateur et n’est pas installée. La deuxième utilise directement les PNG convertis des trois DDS vanilla : protectorate_15, tributary_15 et vassal_15. Génération intégrée image_gen, fond transparent. Aucun dessin, changement de couleur ou détourage algorithmique de l’œuvre : seulement suppression de marge transparente, redimensionnement et encodage DDS.

Maître : `{MASTER}`. Source générée : `{GENERATED}`. Les prompts exacts et le statut de chaque version sont conservés dans ASSET_PROMPTS.json. Ne pas confondre installation et approbation visuelle humaine de la deuxième version.

L’action diplomatique et le concept ont une texture explicite ; les variantes avec et sans icône de la localisation, les texticons et les résolutions 128/30/64 px sont installés. Le chemin principal dessert les consommateurs natifs DiplomaticPact.GetDiplomaticActionType.GetTexture et SubjectType.GetTexture ; les noms dérivés et boutons de loupe ont également un DDS. Les fichiers ont alpha, canaux BGRA et chaîne de mipmaps complète.

## Vérifications et limites

Contrôles statiques : {qa['passed']}/{qa['total']}. Aucun test moteur ou reçu joueur ajouté. Les préimages, empreintes et changements ciblés sont conservés dans BASELINE.json et preimages/. Les anciens rapports DP/SERG et leurs tests historiques ne sont pas réécrits pour faire passer la nouvelle attente. Les premières exécutions sont archivées : une comparaison liste/tuple après sérialisation a produit douze faux écarts de non-régression, corrigés sans changer les types concernés ; le contrôle des suffixes natifs a ensuite révélé neuf clés manquantes par langue, complétées. La validation finale conserve ces mêmes exigences.

Il faut redémarrer le jeu et lancer une nouvelle partie pour charger la suppression des anciens types. Aucune compatibilité des anciennes sauvegardes contenant ces types supprimés n’est revendiquée. Dans le tableau des sujets, vérifier une seule ligne État protégé avec un nom lisible, 0 %, la bonne icône et la transition vers Tributaire. Vérifier DUR–KAL/BHW/D3S et KAL–LBL, les fiches pays, infobulles, liste diplomatique et proposition reçue en français/anglais. Vérifier un aller-retour Protégé ↔ Tributaire puis une réduction vers Vassal, et sauvegarder/recharger. Contrôler aussi un sujet impérial et une protection kazakhe comme témoins inchangés.
'''
    (OUT/'REPORT.md').write_text(text,encoding='utf8')

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--install',action='store_true');ap.add_argument('--validate',action='store_true');ap.add_argument('--complete-ui',action='store_true');ap.add_argument('--complete-suffixes',action='store_true');args=ap.parse_args()
    if args.install:install()
    if args.complete_ui:complete_ui()
    if args.complete_suffixes:complete_suffixes()
    if args.validate:validate()
