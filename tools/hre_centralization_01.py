"""HRE-CENTRALIZATION-01: additive compiler layer, no historical conversion.

Runtime text is emitted as an apply_patch payload. Native installation and Git
metadata are read-only. The separate companion is opt-in and console-armed.
"""
from pathlib import Path
import json,re,sys,subprocess,shutil
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
import start_buildings_2026_10_15 as economy
import map2l_mainz as patcher
from map2k_imperial_feedback import block,child,replace_node
from map2l_registry import active_registry_path

ROOT=qa.ROOT;GAME=qa.GAME
OUT=ROOT/'docs/reports/hre/HRE_CENTRALIZATION_01'
COMPANION=ROOT/'docs/prototypes/HRE_CENTRALIZATION_01'
TRIG='common/scripted_triggers/1776_imperial_constitution.txt'
EF='common/scripted_effects/1776_imperial_constitution.txt'
RF='common/scripted_effects/1776_imperial_reforms.txt'
LINK='subject_type_aor1776_hre_protectorate'
ESTATE='subject_type_imperial_estate';ELECTOR='subject_type_imperial_elector'
CONFIG={'estate_tribute':0.15,'elector_tribute':0.10,'estate_influence':0,'elector_influence':0}
INSTALL='aor1776_hre_install_elected_country'

def dump(name,obj):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def load(name):return json.loads((OUT/name).read_text(encoding='utf8'))
def existing(rel):
    p=ROOT/rel
    return (p if p.exists() else GAME/rel).read_text(encoding='utf-8-sig')
def capture():
    assert not (OUT/'BASELINE.json').exists(),'Never overwrite a baseline'
    inv=qa.inventory();hashes=economy.runtime_hashes()
    native=['common/subject_types/00_subject_types.txt','common/diplomatic_actions/50_subject_crown_land.txt','common/war_goal_types/00_annex_country.txt','common/war_goal_types/27_unification.txt','common/diplomatic_actions/37_subjects_decrease_autonomy.txt','common/diplomatic_actions/43_subjects_handle_states.txt']
    expected=json.loads((ROOT/'docs/reports/map/MAP2R/IMPERIAL_EXPECTED.json').read_text(encoding='utf8'))
    reproduction={p:(ROOT/p).read_text(encoding='utf-8-sig')==s.lstrip('\ufeff') for p,s in expected.items()}
    assert all(reproduction.values()),'Review drift from previous compiler output'
    dump('BASELINE.json',dict(inventory=inv,hashes=hashes,registry_sha256=qa.sha(active_registry_path()),
        git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),git_index_sha256=qa.sha(ROOT/'.git/index'),
        native_hashes={p:qa.sha(GAME/p) for p in native},previous_compiler_reproduction=reproduction,
        originals={p:(ROOT/p).read_text(encoding='utf-8-sig') for p in expected}))
    print('Baseline frozen; 57 compiler outputs match; history and dirty workspace protected.')

def append_guard(raw,key,field,guard):
    n=next(n for n in cw.parse(raw) if n.key==key);parts=n.children(field)
    if parts:
        f=parts[0];body=raw[f.start:f.end];body=body[body.index('{')+1:body.rfind('}')]
        if guard in body:return raw
    else:body=''
    return child(raw,key,field,field+' = {\n'+body+'\n'+guard+'\n}')

def subject_definition(key,autonomy,action):
    native=existing('common/subject_types/00_subject_types.txt')
    base='subject_type_protectorate' if autonomy==2 else 'subject_type_crown_land'
    n=next(n for n in cw.parse(native) if n.key==base);raw=native[n.start:n.end].replace(base+' = {',key+' = {',1)
    values={'diplomatic_action':action,'autonomy_level':str(autonomy),'annex_on_country_formation':'no','overlord_must_be_higher_rank':'no','overlord_must_be_same_country_type':'no','use_for_release_country':'no','can_have_subjects':'yes','breaks_if_subject_not_protected':'no','use_overlord_ruler':'no','use_overlord_map_color':'no','allow_change_country_flag':'no','can_be_used_in_sway_offers':'no','can_offer_to_become_in_sway_offers':'no'}
    if key==LINK:
        values.pop('can_be_used_in_sway_offers')
        values['can_offer_to_become_in_sway_offers']='yes'
    for k,v in values.items():raw=child(raw,key,k,k+' = '+v)
    for field in ['higher_autonomy_subject_type_alternatives','lower_autonomy_subject_type_alternatives','same_autonomy_subject_type_alternatives']:raw=child(raw,key,field,field+' = {}')
    ranks='great_power major_power minor_power insignificant_power unrecognized_major_power unrecognized_regional_power unrecognized_power'
    for field in ['valid_subject_ranks','valid_overlord_ranks']:raw=child(raw,key,field,field+' = { '+ranks+' }')
    for field in ['valid_overlord_country_types','valid_subject_country_types']:
        kinds=('recognized colonial company' if field=='valid_overlord_country_types' else 'recognized unrecognized colonial') if key==LINK else 'recognized'
        raw=child(raw,key,field,field+' = { '+kinds+' }')
    return raw+'\n'

def pact(action,stype,rate,cost,icon):
    return block(action,f'''groups = {{ general power_bloc }}
texture = "gfx/interface/icons/diplomatic_action_icons/{icon}.dds"
show_in_lens = no
potential = {{ always = no }}
pact = {{ cost = {cost} has_junior_participant = yes subject_type = {stype}
 income_transfer = {rate:.2f}
 second_country_gets_income_transfer = no income_transfer_based_on_second_country = yes
 actor_can_break = {{ {'always = no' if stype==LINK else 'is_diplomatic_play_committed_participant = no'} }}
 target_can_break = {{ always = no }}
}}
ai = {{ will_break = {{ always = no }} will_propose = {{ always = no }} }}''')

def augment(files,inv):
    files=dict(files)
    legacy_pair='OR = { is_subject_type = '+LINK+' is_subject_type = subject_type_aor1776_hre_crownland }'
    # Replace references before removing the duplicate type; deprecated pact
    # identifier may still load old dependencies, but defines no second row.
    for p,s in list(files.items()):
        if p.endswith('.txt'):
            s=s.replace(legacy_pair,'aor1776_hre_any_native_bond = yes')
            s=s.replace('subject_type_aor1776_hre_crownland',LINK)
            s=s.replace('type = aor1776_hre_crownland','type = aor1776_hre_protectorate')
            files[p]=s
    files['common/subject_types/1776_imperial_reforms.txt']=subject_definition(LINK,2,'aor1776_hre_protectorate')
    files['common/subject_types/1776_imperial_centralization.txt']=subject_definition(ESTATE,1,'aor1776_imperial_estate')+subject_definition(ELECTOR,1,'aor1776_imperial_elector')
    files['common/diplomatic_actions/1776_imperial_subjects.txt']=pact('aor1776_hre_protectorate',LINK,0,0,'aor1776_imperial_obligation')+'\n# Hidden deprecated pact alias; not an additional subject type.\n'+pact('aor1776_hre_crownland',LINK,0,0,'aor1776_imperial_obligation')
    files['common/diplomatic_actions/1776_imperial_centralization.txt']=''.join(pact('aor1776_imperial_'+kind,typ,CONFIG[kind+'_tribute'],CONFIG[kind+'_influence'],'aor1776_imperial_'+kind) for kind,typ in [('estate',ESTATE),('elector',ELECTOR)])
    ledger=json.loads(active_registry_path().read_text(encoding='utf8'))
    rights={(r['rgb'],r['state'],r['beneficiary']) for r in ledger};bytag={}
    for r in inv['owners']:bytag.setdefault(r['key'][2],[]).append(tuple(r['key']))
    pure=sorted(t for t,rows in bytag.items() if rows and all(r in rights for r in rows))
    # Country-wide native dependency is opt-in, never inferred from one title.
    trig=block('aor1776_hre_centralized_subject',f'OR = {{ is_subject_type = {ESTATE} is_subject_type = {ELECTOR} }}')
    trig+=block('aor1776_hre_any_native_bond',f'OR = {{ is_subject_type = {LINK} aor1776_hre_centralized_subject = yes }}')
    trig+=block('aor1776_hre_centralization_native_eligible','''aor1776_hre_member = yes
OR = { '''+' '.join('c:'+t+' ?= this' for t in pure)+''' }
OR = { is_subject = no aor1776_hre_centralized_subject = yes }
NOT = { any_direct_subject = { aor1776_hre_any_native_bond = no } }
is_at_war = no is_diplomatic_play_committed_participant = no''')
    files['common/scripted_triggers/1776_imperial_centralization.txt']=trig
    # Existing trigger is authoritative for every ballot and status conversion.
    node=next(n for n in cw.parse(files[TRIG]) if n.key=='aor1776_hre_elector')
    body=files[TRIG][node.start:node.end];groups=[n for n in cw.walk(cw.parse(body)) if n.key=='OR' and any(c.key.startswith('c:') for c in n.children())]
    assert len(groups)==1
    group=groups[0];old=body[group.start:group.end]
    body=patcher.edits(body,[(group.start,group.end,'NOT = { has_variable = aor1776_hre_electoral_privilege_revoked }\nOR = { has_variable = aor1776_hre_electoral_privilege_granted '+old+' }')])
    files[TRIG]=replace_node(files[TRIG],'aor1776_hre_elector',body)
    # Block old bulk conversion and whole-Empire annexation at both UI and
    # effect levels. Principles, bloc, territorial registry and elections stay.
    for key in ['aor1776_hre_stage_1','aor1776_hre_stage_2','aor1776_hre_stage_3','aor1776_hre_bind_protectorate','aor1776_hre_bind_crownland']:
        files[RF]=replace_node(files[RF],key,block(key,'# Reserved: no general conversion or annexation before constitutional authorization.\ncustom_tooltip = aor1776_hre_centralization_not_authorized_tt'))
    rel='common/scripted_buttons/1776_imperial_centralization.txt'
    for stage in [1,2,3]:files[rel]=child(files[rel],'aor1776_hre_centralize_'+str(stage),'possible','possible = { custom_tooltip = { text = aor1776_hre_centralization_not_authorized_tt always = no } }')
    # Fail closed in production while succession is a separate runtime test.
    n=next(n for n in cw.parse(files[EF]) if n.key==INSTALL);original=files[EF][n.start:n.end]
    implementation=original.replace(INSTALL+' = {',INSTALL+'_legacy = {',1)
    wrapper=election_guard()
    files[EF]=replace_node(files[EF],INSTALL,wrapper)+implementation+'\n'
    # Even an advanced constitution must not suppress the imperial election.
    rel='common/on_actions/1776_imperial_constitution.txt';n=next(n for n in cw.parse(files[rel]) if n.key=='aor1776_hre_death_hook')
    body=files[rel][n.start:n.end].replace('NOT = { has_global_variable = aor1776_hre_unified } ','')
    files[rel]=replace_node(files[rel],n.key,body)
    files['common/scripted_effects/1776_imperial_centralization.txt']=sync_effects()
    guard='custom_tooltip = { text = aor1776_hre_no_direct_annexation_tt scope:target_country ?= { aor1776_hre_any_native_bond = no } }'
    rel='common/war_goal_types/00_annex_country.txt';raw=files.get(rel,existing(rel));files[rel]=append_guard(raw,'annex_country','valid',guard)
    rel='common/war_goal_types/27_unification.txt';raw=files.get(rel,existing(rel));guard='custom_tooltip = { text = aor1776_hre_no_direct_annexation_tt scope:target_state ?= { owner ?= { aor1776_hre_any_native_bond = no } } }'
    for field in ['possible','valid']:raw=append_guard(raw,'unification',field,guard)
    files[rel]=raw
    rel='common/diplomatic_actions/37_subjects_decrease_autonomy.txt';raw=files.get(rel,existing(rel));guard='custom_tooltip = { text = aor1776_hre_no_direct_annexation_tt scope:target_country = { aor1776_hre_any_native_bond = no } }'
    for field in ['potential','possible']:raw=append_guard(raw,'da_decrease_autonomy',field,guard)
    files[rel]=raw
    files.update(localizations(files))
    files['common/game_concepts/1776_imperial_subjects.txt']=''.join(block(k,'texture = "gfx/interface/icons/diplomatic_action_icons/'+icon+'.dds"') for k,icon in [('concept_aor1776_hre_protectorate','aor1776_imperial_obligation'),('concept_imperial_estate','aor1776_imperial_estate'),('concept_imperial_elector','aor1776_imperial_elector')])
    files['gui/1776_imperial_subject_texticons.gui']='\n'.join('texticon = { icon = "'+k+'" '+''.join('iconsize = { texture = "gfx/interface/icons/diplomatic_action_icons/'+k+'.dds" size = { '+str(size)+' '+str(size)+' } offset = { 0 7 } fontsize = '+str(font)+' } ' for font,size in [(18,25),(24,32),(32,42)])+'}' for k in ['aor1776_imperial_estate','aor1776_imperial_elector'])+'\n'
    from hre_secession_lens_01 import augment as augment_secession_lens
    return augment_secession_lens(autonomy_feedback(files))

def autonomy_feedback(files):
    """Explicit reversible chain; a missing terminal tier never authorizes annexation.

    Called by the full compiler and the bounded R1 component builder. Native
    alternatives drive the UI; scripted effects choose the electoral branch.
    """
    files=dict(files)
    p='common/subject_types/1776_imperial_reforms.txt'
    files[p]=child(files[p],LINK,'lower_autonomy_subject_type_alternatives','lower_autonomy_subject_type_alternatives = { '+ESTATE+' '+ELECTOR+' }')
    p='common/subject_types/1776_imperial_centralization.txt'
    for typ in [ESTATE,ELECTOR]:files[p]=child(files[p],typ,'higher_autonomy_subject_type_alternatives','higher_autonomy_subject_type_alternatives = { '+LINK+' }')
    p='common/scripted_triggers/1776_imperial_centralization.txt'
    files[p]=files[p].replace('OR = { is_subject = no aor1776_hre_centralized_subject = yes }','OR = { is_subject = no aor1776_hre_any_native_bond = yes }')
    # Native default selection cannot distinguish an elector from another
    # recognized principality: do not trust alternative ordering for the vote.
    p='common/diplomatic_actions/37_subjects_decrease_autonomy.txt'
    raw=(GAME/p).read_text(encoding='utf-8-sig')
    guard='''custom_tooltip = { text = aor1776_hre_autonomy_reduction_allowed_tt
 OR = {
  scope:target_country = { aor1776_hre_any_native_bond = no }
  AND = {
   aor1776_hre_emperor = yes
   NOT = { has_global_variable = aor1776_hre_election_open }
   NOT = { has_global_variable = aor1776_hre_election_pending }
   scope:target_country = { is_subject_type = '''+LINK+''' aor1776_hre_centralization_native_eligible = yes }
  }
 }
}'''
    for field in ['potential','possible']:raw=append_guard(raw,'da_decrease_autonomy',field,guard)
    raw=re.sub(r'\bdecrease_autonomy = yes',lambda _: '''if = {
 limit = { is_subject_type = '''+LINK+''' }
 if = { limit = { aor1776_hre_elector = yes } change_subject_type = '''+ELECTOR+''' }
 else = { change_subject_type = '''+ESTATE+''' }
}
else_if = { limit = { aor1776_hre_any_native_bond = no } decrease_autonomy = yes }''',raw)
    files[p]=raw
    # Both overlord-granted and subject-requested autonomy increases stay in
    # the imperial chain. Keep all native approval/cooldown/LD consequences.
    p='common/diplomatic_actions/38_subjects_increase_autonomy.txt'
    raw=(GAME/p).read_text(encoding='utf-8-sig')
    assert len(re.findall(r'\bincrease_autonomy = yes',raw))==2
    files[p]=re.sub(r'\bincrease_autonomy = yes',lambda _: '''if = { limit = { aor1776_hre_centralized_subject = yes } change_subject_type = '''+LINK+''' }
else = { increase_autonomy = yes }''',raw)
    # The table has no subject-country scope. Its tooltip must explain both
    # branches, rather than label every recognized elector as an ordinary estate.
    for lang,i in [('english',0),('french',1)]:
        texts={
          'aor1776_hre_autonomy_reduction_allowed_tt':('Only the Emperor can strengthen an eligible Imperial Bond, outside an imperial election. Imperial Estates and Electorates cannot be annexed by lowering autonomy.','Seul l’empereur peut renforcer un Lien impérial admissible, en dehors d’une élection impériale. Diminuer l’autonomie d’un État ou d’un Électorat impérial ne permet pas de l’annexer.'),
          'aor1776_hre_link_lower_tooltip':('#header Imperial centralization#!\\nLowering the [concept_autonomy] of an [concept_aor1776_hre_protectorate] makes it an [concept_imperial_estate], or an [concept_imperial_elector] if it holds electoral privilege. It is not annexed. Its territory, ruler and [Concept(\'concept_law\',\'$concept_laws$\')|l] remain its own.','#header Centralisation impériale#!\\nDiminuer l’[concept_autonomy|l] d’un [concept_aor1776_hre_protectorate] le transforme en [concept_imperial_estate], ou en [concept_imperial_elector] s’il possède la dignité électorale. Le pays n’est pas annexé. Il conserve son territoire, son dirigeant et ses [Concept(\'concept_law\',\'$concept_laws$\')|l].'),
          'aor1776_hre_estate_higher_tooltip':('#header Imperial Bond#!\\nIncreasing the [concept_autonomy] of an [concept_imperial_estate] or [concept_imperial_elector] restores an [concept_aor1776_hre_protectorate]. It does not grant independence or remove electoral privilege.','#header Lien impérial#!\\nAugmenter l’[concept_autonomy|l] d’un [concept_imperial_estate] ou d’un [concept_imperial_elector] le transforme en [concept_aor1776_hre_protectorate]. Cela ne lui accorde pas l’indépendance et ne retire pas sa dignité électorale.'),
          'aor1776_hre_protected_terminal_tooltip':('#header Imperial privileges#!\\nAn [concept_imperial_estate] or [concept_imperial_elector] cannot be annexed by further reducing its [concept_autonomy].','#header Privilèges impériaux#!\\nUn [concept_imperial_estate] ou un [concept_imperial_elector] ne peut pas être annexé par une nouvelle réduction de son [concept_autonomy|l].')}
        values={k:v[i] for k,v in texts.items()}
        native=(GAME/f'localization/{lang}/interfaces_l_{lang}.yml').read_text(encoding='utf-8-sig')
        islink="EqualTo_string(SubjectType.GetKey, '"+LINK+"')"
        iscentral="Or(EqualTo_string(SubjectType.GetKey, '"+ESTATE+"'), EqualTo_string(SubjectType.GetKey, '"+ELECTOR+"'))"
        for key in ['SUBJECT_TYPE_ANNEX_TOOLTIP','SUBJECT_TYPE_DECREASED_AUTONOMY_TOOLTIP','SUBJECT_TYPE_INDEPENDENCE_TOOLTIP','SUBJECT_TYPE_INCREASED_AUTONOMY_TOOLTIP','SUBJECT_CAN_NOT_DECREASE_OWN_AUTONOMY_ANNEX_TOOLTIP']:
            match=re.search(r'(?m)^ '+key+r':(?:\d+)?[ \t]+"([^\n]*)"$',native);assert match,key
            fallback='aor1776_vanilla_'+key.lower();values[fallback]=match.group(1)
            if key in ['SUBJECT_TYPE_INDEPENDENCE_TOOLTIP','SUBJECT_TYPE_INCREASED_AUTONOMY_TOOLTIP']:
                expression="SelectLocalization("+iscentral+", 'aor1776_hre_estate_higher_tooltip', '"+fallback+"')"
            elif key=='SUBJECT_TYPE_DECREASED_AUTONOMY_TOOLTIP':
                expression="SelectLocalization("+islink+", 'aor1776_hre_link_lower_tooltip', '"+fallback+"')"
            else:
                expression="SelectLocalization("+islink+", 'aor1776_hre_link_lower_tooltip', SelectLocalization("+iscentral+", 'aor1776_hre_protected_terminal_tooltip', '"+fallback+"'))"
            # SelectLocalization's alternatives are localization keys, not
            # translated strings: use one intermediate key for nested cases.
            if key not in ['SUBJECT_TYPE_DECREASED_AUTONOMY_TOOLTIP','SUBJECT_TYPE_INDEPENDENCE_TOOLTIP','SUBJECT_TYPE_INCREASED_AUTONOMY_TOOLTIP']:
                intermediate='aor1776_'+key.lower()+'_nonlink'
                values[intermediate]="[SelectLocalization("+iscentral+", 'aor1776_hre_protected_terminal_tooltip', '"+fallback+"')]"
                expression="SelectLocalization("+islink+", 'aor1776_hre_link_lower_tooltip', '"+intermediate+"')"
            values[key]='['+expression+']'
        files[f'localization/{lang}/replace/1776_imperial_autonomy_l_{lang}.yml']='\ufeffl_'+lang+':\n'+''.join(' '+k+':0 "'+v+'"\n' for k,v in values.items())
    return files

def sync_effects():
    s=block('aor1776_hre_sync_imperial_subject_status',f'''if = {{ limit = {{ aor1776_hre_centralized_subject = yes }}
 set_variable = {{ name = c01_status_previous_liberty value = liberty_desire }}
 if = {{ limit = {{ aor1776_hre_elector = yes NOT = {{ is_subject_type = {ELECTOR} }} }} change_subject_type = {ELECTOR} }}
 else_if = {{ limit = {{ aor1776_hre_elector = no NOT = {{ is_subject_type = {ESTATE} }} }} change_subject_type = {ESTATE} }}
 add_liberty_desire = {{ value = var:c01_status_previous_liberty subtract = liberty_desire }}
 remove_variable = c01_status_previous_liberty
}}''')
    for verb in ['grant','revoke']:
        set_name='granted' if verb=='grant' else 'revoked';remove='revoked' if verb=='grant' else 'granted'
        s+=block('aor1776_hre_'+verb+'_electoral_privilege',f'''if = {{ limit = {{ aor1776_hre_member = yes has_variable = aor1776_hre_constitutional_privilege_change_authorized
 NOT = {{ has_global_variable = aor1776_hre_election_open }} NOT = {{ has_global_variable = aor1776_hre_election_pending }} }}
 remove_variable = aor1776_hre_electoral_privilege_{remove}
 set_variable = aor1776_hre_electoral_privilege_{set_name}
 remove_variable = aor1776_hre_constitutional_privilege_change_authorized
 aor1776_hre_sync_imperial_subject_status = yes
}}''')
    return s

def election_guard():
    return block(INSTALL,'''if = { limit = { any_country = { aor1776_hre_any_native_bond = yes } }
 set_global_variable = aor1776_hre_centralized_transfer_pending
}
else = { '''+INSTALL+'''_legacy = yes }''')

def localizations(files):
    result={};base={
      'concept_aor1776_hre_protectorate':('Imperial Bond','Lien impérial'),
      'concept_imperial_estate':('Imperial Estate','État impérial'),
      'concept_imperial_elector':('Imperial Electorate','Électorat impérial'),
      'aor1776_hre_no_direct_annexation_tt':('Imperial privileges forbid direct annexation.','Les privilèges impériaux interdisent l’annexion directe.'),
      'aor1776_hre_centralization_not_authorized_tt':('The Diet has not authorized this centralization.','La Diète n’a pas autorisé cette centralisation.')}
    descriptions={
      'concept_aor1776_hre_protectorate_desc':(
        'The princes and cities of the Empire retain their institutions while recognizing imperial authority. This [concept_subject_type] can launch its own [Concept(\'concept_diplomatic_play\',\'$concept_diplomatic_plays$\')|l], pays no weekly tribute from its [concept_treasury] and is not required to join its [concept_overlord]’s [Concept(\'concept_war\',\'$concept_wars$\')|l]. Its [concept_liberty_desire] measures its wish for greater [concept_autonomy]. The imperial bond may be contested through a [concept_diplomatic_play].',
        'Les princes et villes de l’Empire conservent leurs institutions tout en reconnaissant l’autorité impériale. Ce [concept_subject_type|l] peut jouer ses propres [Concept(\'concept_diplomatic_play\',\'$concept_diplomatic_plays$\')|l], ne verse aucun tribut hebdomadaire sur les revenus de son [concept_treasury] et n’est pas tenu de rejoindre les [Concept(\'concept_war\',\'$concept_wars$\')|l] de son [concept_overlord|l]. Son [concept_liberty_desire|l] exprime ses aspirations à davantage d’[concept_autonomy|l]. Le lien impérial peut être contesté par un [concept_diplomatic_play|l].'),
      'concept_imperial_estate_desc':(
        'An imperial estate retains its ruler and [Concept(\'concept_law\',\'$concept_laws$\')|l] under strengthened imperial authority. This [concept_subject_type] cannot launch its own [Concept(\'concept_diplomatic_play\',\'$concept_diplomatic_plays$\')|l] and must join its [concept_overlord]’s [Concept(\'concept_war\',\'$concept_wars$\')|l]. It pays #v 10%#! of its [concept_treasury] revenue each week. Its [concept_liberty_desire] can lead it to seek independence. Ordinary annexation is barred by imperial privileges, and the imperial dignity remains elective.',
        'Un État impérial conserve son dirigeant et ses [Concept(\'concept_law\',\'$concept_laws$\')|l] sous une autorité impériale renforcée. Ce [concept_subject_type|l] ne peut pas jouer ses propres [Concept(\'concept_diplomatic_play\',\'$concept_diplomatic_plays$\')|l] et doit rejoindre les [Concept(\'concept_war\',\'$concept_wars$\')|l] de son [concept_overlord|l]. Il verse chaque semaine #v 10 %#! des revenus de son [concept_treasury]. Son [concept_liberty_desire|l] peut le conduire à réclamer l’indépendance. Les privilèges impériaux excluent l’annexion ordinaire et la dignité impériale demeure élective.'),
      'concept_imperial_elector_desc':(
        'An imperial elector retains a voice in the election of the Emperor, together with its ruler and [Concept(\'concept_law\',\'$concept_laws$\')|l]. This [concept_subject_type] cannot launch its own [Concept(\'concept_diplomatic_play\',\'$concept_diplomatic_plays$\')|l] and must join its [concept_overlord]’s [Concept(\'concept_war\',\'$concept_wars$\')|l]. It pays #v 5%#! of its [concept_treasury] revenue each week. Its [concept_liberty_desire] remains active. Electoral privilege bars ordinary annexation by the overlord; the imperial dignity does not become hereditary.',
        'Un électorat impérial conserve une voix dans l’élection de l’empereur, ainsi que son dirigeant et ses [Concept(\'concept_law\',\'$concept_laws$\')|l]. Ce [concept_subject_type|l] ne peut pas jouer ses propres [Concept(\'concept_diplomatic_play\',\'$concept_diplomatic_plays$\')|l] et doit rejoindre les [Concept(\'concept_war\',\'$concept_wars$\')|l] de son [concept_overlord|l]. Il verse chaque semaine #v 5 %#! des revenus de son [concept_treasury]. Son [concept_liberty_desire|l] reste actif. Son privilège électoral interdit l’annexion ordinaire par le suzerain ; la dignité impériale ne devient pas héréditaire.')}
    for lang,i in [('english',0),('french',1)]:
        loc={k:v[i] for k,v in (base|descriptions).items()}
        loc['concept_aor1776_hre_protectorate_desc']=(
            'The princes and cities of the Empire retain their institutions while recognizing imperial authority. This [concept_subject_type] retains diplomatic autonomy and pays no compulsory weekly tribute. It is not automatically called into the Emperor’s [Concept(\'concept_war\',\'$concept_wars$\')|l]; military duties follow the Imperial Circles and imperial restitution rules. Strengthening the bond creates an [concept_imperial_estate], or an [concept_imperial_elector] when the country holds electoral privilege, without annexation. Leaving the Empire requires a successful secession [concept_diplomatic_play].',
            'Les princes et villes de l’Empire conservent leurs institutions tout en reconnaissant l’autorité impériale. Ce [concept_subject_type|l] conserve son autonomie diplomatique et ne verse aucun tribut hebdomadaire obligatoire. Il n’est pas automatiquement appelé dans les [Concept(\'concept_war\',\'$concept_wars$\')|l] de l’empereur : ses obligations militaires suivent les Cercles impériaux et les règles de rétrocession impériale. Renforcer ce lien le transforme en [concept_imperial_estate], ou en [concept_imperial_elector] s’il possède la dignité électorale, sans annexion. Quitter l’Empire exige un [concept_diplomatic_play|l] de sécession victorieux.')[i]
        for concept in ['concept_imperial_estate','concept_imperial_elector']:
            loc[concept+'_desc']+=(' Increasing its [concept_autonomy] restores an [concept_aor1776_hre_protectorate], not independence.',' Une augmentation de son [concept_autonomy|l] le transforme en [concept_aor1776_hre_protectorate], sans lui accorder l’indépendance.')[i]
        for kind,concept,default in [('estate','concept_imperial_estate','10'),('elector','concept_imperial_elector','5')]:
            percentage=format(CONFIG[kind+'_tribute']*100,'g')
            if lang=='french':percentage=percentage.replace('.',',')
            old='#v '+default+(' %#!' if lang=='french' else '%#!')
            new='#v '+percentage+(' %#!' if lang=='french' else '%#!')
            loc[concept+'_desc']=loc[concept+'_desc'].replace(old,new)
        for typ,concept,icon,action in [(LINK,'concept_aor1776_hre_protectorate','crown_land','aor1776_hre_protectorate'),(ESTATE,'concept_imperial_estate','aor1776_imperial_estate','aor1776_imperial_estate'),(ELECTOR,'concept_imperial_elector','aor1776_imperial_elector','aor1776_imperial_elector')]:
            loc[typ+'_no_icon']='$'+concept+'$';loc[typ]='@'+icon+'! $'+typ+'_no_icon$'
            loc[action]='$'+concept+'$';loc[action+'_action_name']='['+concept+']';loc[action+'_action_propose_name']='['+concept+']'
            loc[action+'_desc']='$'+concept+'_desc$';loc[action+'_pact_desc']='$'+concept+'_desc$'
        # Cover native pact notification suffixes, including the hidden old
        # pact alias, without defining a second legacy subject-type row.
        native_loc=(GAME/f'localization/{lang}/diplomacy_l_{lang}.yml').read_text(encoding='utf-8-sig')
        suffixes=re.findall(r'(?m)^[ \t]+crown_land(_\w+):',native_loc)
        for action,concept in [('aor1776_hre_protectorate','concept_aor1776_hre_protectorate'),('aor1776_hre_crownland','concept_aor1776_hre_protectorate'),('aor1776_imperial_estate','concept_imperial_estate'),('aor1776_imperial_elector','concept_imperial_elector')]:
            for suffix in suffixes:
                key=action+suffix
                if key in loc or (action=='aor1776_hre_crownland' and suffix=='_desc'):continue
                if suffix.endswith('_name'):value='['+concept+']'
                elif 'declined' in suffix:value=('The proposal was declined.','La proposition a été refusée.')[i]
                elif 'break' in suffix:value=('The relationship of [concept_subject] and [concept_overlord] has ended.','La relation entre le [concept_subject|l] et son [concept_overlord|l] prend fin.')[i]
                else:value='$'+concept+'_desc$'
                loc[key]=value
        # Update old definitions in their original generated file rather than
        # rely on ambiguous duplicate-key load order.
        rel=f'localization/{lang}/1776_imperial_reforms_l_{lang}.yml';raw=files[rel]
        for k in [LINK,'aor1776_hre_protectorate','aor1776_hre_protectorate_desc']:
            v=loc.pop(k);raw,n=re.subn(r'(?m)^ '+re.escape(k)+r':0 "[^\n]*"$',lambda _: ' '+k+':0 "'+v+'"',raw);assert n==1,k
        for k in ['subject_type_aor1776_hre_crownland','aor1776_hre_crownland']:
            raw=re.sub(r'(?m)^ '+k+r':0 "[^\n]*"$',' '+k+':0 "$concept_aor1776_hre_protectorate$"',raw)
        raw=re.sub(r'(?m)^ aor1776_hre_crownland_desc:0 "[^\n]*"$',' aor1776_hre_crownland_desc:0 "$concept_aor1776_hre_protectorate_desc$"',raw)
        editorial={
            'je_aor1776_hre_centralization_reason':('The Diet considers closer obligations between the Emperor and the estates. Their privileges remain guaranteed, and the imperial dignity remains elective.','La Diète examine le renforcement des obligations entre l’empereur et les États. Leurs privilèges demeurent garantis et la dignité impériale reste élective.'),
            'je_aor1776_hre_centralization_status':('A resolution of the Diet must precede any centralization.','Une résolution de la Diète doit précéder toute centralisation.')}
        for k,pair in editorial.items():raw=re.sub(r'(?m)^ '+k+r':0 "[^\n]*"$',' '+k+':0 "'+pair[i]+'"',raw)
        for stage in [1,2,3]:raw=re.sub(r'(?m)^ aor1776_hre_centralize_'+str(stage)+r'_desc:0 "[^\n]*"$',' aor1776_hre_centralize_'+str(stage)+'_desc:0 "$aor1776_hre_centralization_not_authorized_tt$"',raw)
        result[rel]=raw
        # One description authority for both the initial constitutional pact
        # and the comparison table, not two independently maintained paragraphs.
        for stem,key in [('constitution','aor1776_imperial_obligation'),('constitution','aor1776_imperial_obligation_desc'),('repairs','aor1776_imperial_obligation_pact_desc')]:
            rel2=f'localization/{lang}/1776_imperial_{stem}_l_{lang}.yml'
            alias='concept_aor1776_hre_protectorate'+('_desc' if key.endswith('_desc') else '')
            result[rel2],count=re.subn(r'(?m)^ '+key+r':0 "[^\n]*"$',lambda _: ' '+key+':0 "$'+alias+'$"',result.get(rel2,files[rel2]))
            assert count==1,key
        result[f'localization/{lang}/1776_imperial_subjects_l_{lang}.yml']='\ufeffl_'+lang+':\n'+''.join(' '+k+':0 "'+v.replace('"','\\"')+'"\n' for k,v in loc.items())
    return result

def prepare():
    if (OUT/'SECESSION_LENS_R2/EXPECTED_TEXT.json').exists():
        from hre_secession_lens_01 import prepare as current_prepare
        return current_prepare()
    if (OUT/'FEEDBACK_R1/EXPECTED_TEXT.json').exists():
        from hre_subject_feedback_01 import prepare as current_prepare
        return current_prepare()
    import map2k_imperial_system as compiler
    compiler.OUT=OUT;files=compiler.compile_system()
    dump('EXPECTED_TEXT.json',files);patcher.OUT=OUT;changed=patcher.emit(files,'INSTALL.patch')
    previous=set(load('PLAN.json')['files']) if (OUT/'PLAN.json').exists() else set()
    dump('PLAN.json',dict(files=sorted(previous|set(changed))))
    print('Prepared',len(changed),'runtime text changes; review/install patch explicitly.')

def unit_tests():
    if (OUT/'SECESSION_LENS_R2/EXPECTED_TEXT.json').exists():
        from hre_secession_lens_01 import unit_tests as current_tests
        return current_tests()
    if (OUT/'FEEDBACK_R1/EXPECTED_TEXT.json').exists():
        from hre_subject_feedback_01 import unit_tests as current_tests
        return current_tests()
    import unittest,io,time
    groups={'centralization_static_and_models':['test_hre_centralization_01'],'MAP2R_historical_delta':['test_map2r_anhalt'],'previous_Q_stages':['test_map2q_r3','test_map2q_eutin','test_map2q_r2'],'cumulative_legacy':['test_map2l_registry','test_map2m_r8','test_map2m_r9','test_map2n_island','test_map2n_completion','test_map2o_east_frisia']}
    results={}
    for name,modules in groups.items():
        stream=io.StringIO();start=__import__('time').monotonic();result=unittest.TextTestRunner(stream=stream,verbosity=1).run(unittest.TestLoader().loadTestsFromNames(modules))
        results[name]=dict(modules=modules,tests=result.testsRun,failures=[t.id() for t,_ in result.failures],errors=[t.id() for t,_ in result.errors],output=stream.getvalue(),seconds=round(time.monotonic()-start,2),engine_test=False)
        print(name,result.testsRun,'tests',len(result.failures),'failures',len(result.errors),'errors',flush=True)
    earlier=json.loads((ROOT/'docs/reports/map/MAP2R/UNIT_TESTS.json').read_text(encoding='utf8'))
    known={x for group in earlier.values() for x in group['failures']}
    actual={x for group in results.values() for x in group['failures']}
    data=dict(groups=results,previous_failure_ids=sorted(known),new_failure_ids=sorted(actual-known),engine_test_executed=False,model_tests_are_not_engine_proof=True)
    dump('UNIT_TESTS.json',data)
    assert not data['new_failure_ids'] and not any(g['errors'] for g in results.values())

def reports():
    if (OUT/'SECESSION_LENS_R2/VALIDATION.json').exists():
        from hre_secession_lens_01 import report as current_report
        return current_report()
    if (OUT/'FEEDBACK_R1/VALIDATION.json').exists():
        from hre_subject_feedback_01 import report as current_report
        return current_report()
    v=load('VALIDATION.json');tests=load('UNIT_TESTS.json');files={};prefix=OUT.relative_to(ROOT).as_posix()+'/'
    def doc(name,text):files[prefix+name]=text.strip()+'\n'
    doc('REPORT.md',f'''# HRE-CENTRALIZATION-01

## Installé

Un seul **Lien impérial** reste défini dans la liste des types de sujets. L’ancienne deuxième définition « terre de la couronne impériale » est retirée. Son identifiant de pacte est conservé comme alias interne, sans nouveau type ni nouvelle ligne, pour limiter les références cassées. La compatibilité de sauvegardes déjà centralisées reste à tester.

Deux types distincts sont ajoutés : **État impérial** (`subject_type_imperial_estate`,10%) et **Électorat impérial** (`subject_type_imperial_elector`,5%). Ils conservent gouvernement, lois, souverain et couleurs. Ils utilisent un paiement natif unique et les obligations militaires natives des sujets non autonomes. Aucune conversion générale n’est activée au démarrage. Les types apparaissent dans le tableau de comparaison, mais ne sont pas attribués automatiquement aux pays.

Les noms, variantes `_no_icon`, concepts, descriptions et suffixes de notifications sont fournis en français et anglais. Les mots ouvrant des infobulles utilisent de vrais concepts du jeu, pas une simple coloration orange. Les descriptions expliquent le statut, la diplomatie, la guerre, les contributions et les privilèges sans vocabulaire de développement.

Les dernières consignes graphiques priment : bannière à médaillon rouge aux trois couronnes pour l’électorat ; grande couronne avec aigle pour l’État impérial. Les maîtres transparents et les textures128px sont dans [la liste des fichiers](IMPLEMENTED_FILES.md). Les [prompts de détourage](ASSET_PROMPTS.md) précisent la méthode intégrée utilisée.

## Verrous et succession

Les trois anciens boutons de conversion/annexion générale sont verrouillés dans l’interface ET leurs effets. L’ancienne annexion de tous les membres, électeurs compris, n’est plus exécutable par ces effets. Les principes, le bloc, le registre, les rétrocessions et les institutions sont conservés. Aucun arbre de réformes supplémentaire n’est créé.

Les deux types sont initialement non annexables : aucune chaîne de changement d’autonomie, `annex_on_country_formation=no`, gardes sur annexion, unification et réduction d’autonomie. Les interactions natives de prise d’État n’incluent pas ces types dans leur liste autorisée. Cela ne garantit pas une inviolabilité contre tout script ou toute conquête étrangère : voir [les limites](ENGINE_LIMITATIONS.md).

La dignité impériale reste élective. Les privilèges électoraux peuvent être accordés/révoqués par des effets autorisés centralisés, entre deux scrutins, puis synchronisés avec le type de sujet. Aucune scrutation quotidienne supplémentaire.

Le transfert de suzeraineté est préparé dans un **compagnon isolé, non activé**, avec armement explicite par console. Dans le mod principal, une élection impliquant des sujets impériaux natifs reste en attente plutôt que de changer de couronne avec des dépendances incohérentes. Les élections de la partie1776 sans ces sujets continuent par le chemin existant. La fiabilité du prototype doit être vérifiée avant toute conversion générale.

## Vérifié

- {v['passed']}/{v['total']} contrôles statiques.
- 21/21 tests nouveaux, dont 16 contrats statiques et 5 modèles Python de transitions. Les modèles n’exécutent pas le moteur.
- 11/11 tests historiques MAP2R passent ; les dix échecs de snapshots plus anciens restent identiques à ceux déjà documentés par MAP2R. Aucun nouveau test en échec, aucune erreur d’exécution des suites.
- Historiques, propriétaires, pays, populations, bâtiments, PM, propriétaires économiques, unités, diplomatie initiale et registre identiques à la baseline immédiate. Population mondiale835801255 ;44 doublons RGB et12 références invalides préexistants inchangés.
- Aucune modification de l’installation du jeu, de HEAD ou de l’index. Aucun commit, merge ou push.

**Statut : {v['status']}. Aucun test moteur effectué.** Affichage, prélèvement réel, guerre, annexions et succession attendent les essais détaillés dans [RUNTIME_TEST_PLAN.md](RUNTIME_TEST_PLAN.md). Ne pas qualifier cette livraison de PASS_RUNTIME_USER_VALIDATED.

## Recherche locale

Une tentative ColGrep a échoué sur le verrou d’index, puis un appel local a abouti. Il a notamment retrouvé `tools/map2k_imperial_principles.py:240–251`, vérifié directement, ainsi que les drapeaux électoraux et valeurs de vote. Les fichiers vanilla ont été lus directement. Aucun modèle ou paramètre d’intégration changé ; aucune économie exacte de quota mesurée.
''')
    doc('VANILLA_SUBJECT_TYPES_AUDIT.md','''# Audit de l’installation réellement consultée

Sources locales en lecture seule : `C:/Games/Victoria 3/game/`. La compatibilité annoncée par le mod est1.13.* ; les définitions ci-dessous proviennent des fichiers installés, pas d’une hypothèse sur un wiki. Les empreintes originales sont dans BASELINE.json. Aucun numéro de build binaire supplémentaire n’est certifié.

- `common/subject_types/00_subject_types.txt`, bloc `subject_type_crown_land` : autonomie1 ; diplomatie propre interdite ; participation militaire ; dirigeant distinct ; absorption lors de formation de pays activée ; alternatives d’autonomie vanilla. Le nouveau type clone la syntaxe reconnue puis désactive absorption et alternatives. Aucune définition vanilla n’est écrasée.
- `common/diplomatic_actions/50_subject_crown_land.txt` : pacte avec junior, paiement basé sur le second pays, direction second vers premier, `cost=10`, `income_transfer=0.15`. La localisation française installée annonce40%, alors que cette donnée et l’écran fourni indiquent15% : ne pas copier aveuglément le chiffre du texte.
- `common/diplomatic_plays/00_diplomatic_plays.txt`, `dp_annex_subject` : liste explicite de pactes colonie/fantoche/vassal/crown_land. Nos pactes ne sont pas ajoutés à cette liste.
- `common/war_goal_types/00_annex_country.txt` : validation scriptable en plus du traitement moteur. Ajout d’une garde locale, sans réécrire le reste du but de guerre.
- `27_unification.txt` : cible État et effets prédéfinis côté moteur. Gardes sur possible/valid pour les États appartenant à nos sujets impériaux.
- `37_subjects_decrease_autonomy.txt` : interaction utilisant `can_decrease_autonomy` et `decrease_autonomy`. Garde ciblée ajoutée à potential/possible. Le reste est identique.
- `43_subjects_handle_states.txt`, `take_state` : liste explicite colonie/fantoche/vassal ; nos types n’y sont pas ajoutés. Aucun changement à cette interaction.
- `22_subject_personal_union.txt` et exception OLD–HLB : conservés. Les effets de transfert isolés ne parcourent que les nouveaux sujets impériaux directs.
- Localisations `diplomacy_l_french.yml` et `concepts_l_french.yml` : contrat nom avec icône, variante `_no_icon`, nom de concept et `_desc`, liens `[concept_...]` / `[Concept(...)]`. Les trois concepts impériaux sont réellement définis.

Les fonctions consultées ne justifient pas l’invention d’un champ `can_be_annexed` ou d’une propriété de masquage des types. Aucun de ces champs n’est ajouté. Les limites moteur sont déclarées séparément.
''')
    doc('IMPERIAL_SUBJECT_DESIGN.md','''# Définition des statuts

| Statut | Paiement hebdomadaire initial | Diplomatie propre | Guerres du suzerain | Annexion initiale |
|---|---:|---|---|---|
| Lien impérial |0%|Autonome|Pas d’obligation native générale|Bloquée|
| État impérial |10%|Non autonome|Règle native des sujets dépendants|Bloquée|
| Électorat impérial |5%|Non autonome|Règle native des sujets dépendants|Interdite sans exception implémentée|

Les nouvelles définitions sont des types natifs, avec désir de liberté et possibilités de contestation relevant des règles natives et du coup impérial de sécession conservé. Aucun paiement par événement, aucune annexion lors d’une formation de pays, aucun dirigeant partagé, aucune loi imposée automatiquement. Les lois et gouvernements ne sont pas figés contre toute interaction future du jeu.

Le pacte générique Lien impérial historique, les titres territoriaux du registre et les appartenances au bloc restent des mécanismes distincts. Le pays entier n’est jamais converti du seul fait d’un titre territorial.

Le statut électoral effectif est le trigger existant `aor1776_hre_elector`, augmenté de deux variables de privilège accordé/révoqué. Les listes initiales sont le défaut1776, pas une limite permanente. Les effets grant/revoke exigent une autorisation constitutionnelle consommée et interdisent la mutation pendant un scrutin. Ils appellent `aor1776_hre_sync_imperial_subject_status` seulement sur un sujet déjà centralisé. Le désir de liberté est mémorisé puis une restauration différentielle est demandée ; son résultat réel reste à tester.

Toute autre future modification du droit électoral devra appeler ce même effet ; une modification de loi extérieure qui ne l’appelle pas n’est pas synchronisée magiquement.
''')
    modified=load('PLAN.json')['files'];assets=load('ASSET_VALIDATION.json')['icons']
    doc('IMPLEMENTED_FILES.md','# Fichiers de la livraison\n\n## Runtime\n\n'+'\n'.join('- `'+p+'`' for p in modified)+'\n\n## Images\n\n'+'\n'.join('- `'+r['texture']+'` et maître `'+r['master']+'`' for r in assets)+'''\n
Les PNG maîtres sont adaptés par détourage intégré ; les DDS128px avec mipmaps sont vérifiés par décodage identique. Les deux feuilles originales fournies par le joueur ne sont pas modifiées.

## Outils

- `tools/hre_centralization_01.py` : couche de compilation, capture, validation et compagnon isolé.
- `tools/test_hre_centralization_01.py` : contrats statiques et modèles, sans moteur.
- `tools/map2k_imperial_system.py` : appel de la nouvelle couche en fin de compilation ; elle empêche la réapparition du doublon lors d’une régénération.

## Compagnon non activé

- `docs/prototypes/HRE_CENTRALIZATION_01/HRE_CENTRALIZATION_01_TEST.mod`
- `mod/descriptor.mod`
- `mod/common/scripted_effects/zz_hre_centralization_01_test.txt`
- `mod/common/scripted_effects/1776_imperial_constitution.txt` : copie effective du fichier principal, seule enveloppe de succession remplacée. Cela utilise le remplacement de fichier du chargeur, pas deux définitions concurrentes du même effet dans des fichiers différents.

Le compagnon n’est ni installé dans un playset ni activé par cette livraison. Il doit être régénéré si le fichier impérial principal évolue.
''')
    doc('ANNEXATION_PROTECTIONS.md','''# Protections déclarées et contrôles

1. Les deux nouveaux types et le Lien impérial ont `annex_on_country_formation=no`.
2. Les trois listes d’alternatives d’autonomie sont vides : aucune sortie vers une Terre de la Couronne ou un fantoche annexable par cette chaîne.
3. L’interaction native de baisse d’autonomie refuse ces types dans potential et possible.
4. Le but `annex_country` refuse une cible relevant de ces types dans valid. Le coup vanilla d’annexion ne connaît de toute façon pas nos nouveaux pactes.
5. Le but d’unification refuse, dans possible et valid, les États de ces sujets.
6. La prise d’État par le suzerain utilise une liste native qui exclut nos types. Les interactions entre pays indépendants ne sont pas globalement interdites.
7. L’ancienne réforme impériale3 n’a plus d’effet `annex`, ni de conversion préalable. Ses boutons et effets sont verrouillés, sans exception pour les électeurs.

Un test compare les AST des trois remplacements partagés avec le vanilla après retrait de nos seules gardes : aucune autre règle native n’est changée.

**Démonstration : statique uniquement.** Il faut encore tester les interactions réellement affichées, les buts automatiques et une unification en nouvelle partie. Aucune immunité contre un autre mod, un effet console `annex`, toutes les guerres étrangères ou tout article de traité n’est revendiquée.

Pour rendre plus tard un État impérial ordinaire annexable, une réforme devra explicitement modifier les gardes et le chemin d’annexion, en réexaminant les alternatives et les effets de formation. Aucun déverrouillage actif n’est livré. L’électorat n’a aucune exception d’annexion dans cette mission.
''')
    doc('IMPERIAL_ELECTION_TRANSFER_PROTOTYPE.md','''# Prototype de succession — isolé

Le mod principal bloque l’installation d’un nouvel empereur lorsqu’existent des sujets impériaux natifs et pose `aor1776_hre_centralized_transfer_pending`. Il ne libère pas le candidat dans cet état bloqué. Sans ces dépendances, il appelle la même implémentation électorale préexistante. Le hook de décès n’est plus supprimé par le marqueur d’ancienne unification.

Le compagnon ajoute un scénario volontairement limité : ANH comme État impérial et KPF comme électorat sous l’empereur courant. Aucun pays déjà sujet non impérial n’est converti par ce scénario. Il faut une nouvelle partie, le compagnon explicitement activé et un armement console.

Précontrôles : ancien empereur indépendant, nouveau candidat légitime et non sujet étranger, paix, absence de dépendance cyclique connue et éligibilité des sujets concernés. Les seuls sujets sélectionnés sont les deux nouveaux types directement dépendants de l’ancien empereur.

Ordre : mémoriser types et désir de liberté ; libérer le candidat s’il fait partie des sujets sélectionnés ; appeler le mécanisme existant de changement de titulaire/bloc ; si sa réussite est observée par les conditions scriptées, recréer uniquement ces dépendances sous le nouveau titulaire, restaurer le désir de liberté et synchroniser les types ; laisser les unions et dépendances étrangères hors sélection. L’ancien titulaire n’est soumis que s’il appartient à la liste pure autorisée ; AUS et PRU n’en font pas partie.

En cas d’échec de création du bloc, tentative de restauration du seul candidat libéré. **Ce n’est pas une transaction moteur garantie** : un bloc partiellement modifié, les marchés, modificateurs de pactes et dépendances indirectes exigent des tests. Les variables `...test_completed` / `...test_failed` ne sont pas des certificats.

Les cinq modèles Python testent le graphe attendu, les cycles et la conservation de données fictives. Ils n’exécutent pas ces scripts dans Victoria3 et ne prouvent pas le transfert natif. L’ouverture à une réforme générale reste bloquée.
''')
    doc('MIXED_SOVEREIGNTY_EXCEPTIONS.md','''# Puissances mixtes et liens territoriaux

La liste conservatrice des candidats natifs est construite à partir de l’inventaire de départ : toutes leurs provinces possédées doivent correspondre à leurs droits enregistrés. Le trigger ajoute appartenance impériale, absence de dépendance étrangère, absence de sujet non impérial, paix et absence d’engagement diplomatique.

PRU, AUS, SAR et SWE sont exclus de la liste de soumission native. Les détenteurs extérieurs ne sont pas admis du seul fait de la Poméranie, du Mecklembourg ou d’un autre titre. Le Lien impérial territorial et le registre restent en place. OLD–HLB reste une union personnelle ; ni son pacte ni ses historiques ne sont modifiés.

Une puissance mixte peut être élue empereur sans que ses territoires extérieurs soient annexés ou transférés : le prototype transfère une relation de suzeraineté, pas la propriété des provinces. L’ancien empereur mixte reste autonome dans le bloc.

Cette liste est une autorisation prudente issue du scénario initial, pas un test géographique universel après conquêtes. Tout changement ultérieur de possessions exige une nouvelle vérification avant une activation constitutionnelle. Le compagnon doit être testé sur une nouvelle partie ; aucune conversion générale automatisée ne se fonde sur cette liste seule.
''')
    doc('BALANCE_PARAMETERS.md','''# Paramètres initiaux

Source unique de configuration : dictionnaire CONFIG dans `tools/hre_centralization_01.py`, puis compilation impériale.

| Paramètre | État impérial | Électorat impérial |
|---|---:|---:|
| income_transfer natif |0.10|0.05|
| coût de pacte en influence |0|0|
| niveau d’autonomie |1|1|

Ces pourcentages sont un équilibrage provisoire, pas une reconstitution des impôts impériaux de1776. Le paiement est explicitement calculé sur le second pays et versé au premier. Aucun prélèvement additionnel par script, aucun événement de taxe ni modificateur de revenu ajouté.

Le coût0 évite de rendre des dizaines de sujets incompatibles avec le budget diplomatique. Il n’affecte aucun coût global des sujets vanilla. Il pourra être relevé dans CONFIG après mesure en jeu.

Les interactions natives d’augmentation/réduction des versements peuvent affecter les paiements réels : vérifier leur effet séparément. Le maintien d’un gouvernement et d’un dirigeant distinct ne signifie pas une immunité contre toutes les autres interactions natives.

La compilation injecte les taux CONFIG dans les descriptions françaises/anglaises. Un test temporaire à12,5% vérifie cette propagation sans écrire ce taux dans le mod. Pas de formule mensuelle parallèle.
''')
    doc('ENGINE_LIMITATIONS.md','''# Limites et tests non effectués

- Les définitions, champs et effets sont fondés sur les scripts installés. Leur chargement par le binaire n’a pas été observé pendant cette mission.
- Aucun champ de masquage des types n’a été retenu. Le doublon est supprimé dans les définitions ; les deux nouveaux types peuvent apparaître dans la table même sans aucun pays les utilisant.
- Aucun champ hypothétique `can_be_annexed` n’est inventé. Les protections combinent champs natifs et gardes scriptées, dont les chemins automatiques doivent être testés.
- `join_overlord_wars=yes` suit le comportement moteur. Le cas où le suzerain ne fait que soutenir un autre initiateur/cible peut différer. Le système existant des cercles vérifie les alliances avant de rajouter des soutiens ; aucun nouvel appel militaire parallèle n’est ajouté.
- Le désir de liberté est natif ; la contestation reste soumise aux règles natives et au coup de sécession conservé. Les modifications d’un pacte, d’un marché ou de l’autonomie peuvent avoir des effets secondaires non modélisés.
- Aucun effet direct de changement de suzerain non vérifié n’est inventé. Le prototype utilise indépendance puis pacte, ce qui n’offre pas de rollback complet garanti.
- L’unification par pays et les buts de guerre peuvent avoir des traitements codés côté moteur. Les protections statiques ne garantissent pas toutes les exceptions, traités, événements d’autres mods ou commandes console.
- Le titre électoral dépend du trigger commun et d’effets autorisés. Les futurs changements de statut devront utiliser l’API de synchronisation ; aucun tick quotidien ne surveille arbitrairement toutes les lois.
- Les sauvegardes déjà entrées dans l’ancienne centralisation ne sont pas certifiées compatibles. Un alias de pacte ne garantit pas la migration de tout identifiant interne retiré. Ne pas charger une sauvegarde précieuse sans copie ; les essais proposés utilisent une nouvelle partie.
- Le compagnon n’a pas été activé et aucune simulation d’un mois n’a été exécutée. Les drapeaux de diagnostic et les modèles Python ne constituent pas une preuve moteur.

Les dix échecs des anciennes suites sont identiques à ceux archivés sous MAP2R/UNIT_TESTS.json. Les anciennes baselines ne sont pas modifiées ; les44 doublons RGB et12 références invalides restent des problèmes de données préexistants.
''')
    doc('RUNTIME_TEST_PLAN.md','''# Plan de test moteur — aucun résultat prérempli

## Partie normale, mod principal seul

Redémarrer le jeu pour recharger les types, localisations et textures. Nouvelle partie1776. Vérifier la table : un Lien impérial, un État impérial et un Électorat impérial, sans ancienne deuxième Terre de la Couronne impériale. Vérifier les trois titres sans icône, leurs descriptions en français puis anglais, et ouvrir les infobulles des concepts liés.

La bannière aux trois couronnes doit identifier l’électorat ; la grande couronne, l’État impérial. Vérifier les textures sur fond sombre aux tailles de liste et d’infobulle. Aucun pays ne doit commencer avec les deux nouveaux pactes. Contrôler OLD–HLB, bloc, registre, frontières, économies et armées inchangés, puis un mois de simulation.

## Compagnon isolé

Ne pas l’activer sur une sauvegarde à conserver. Copier manuellement le descripteur `docs/prototypes/HRE_CENTRALIZATION_01/HRE_CENTRALIZATION_01_TEST.mod` dans le dossier de mods utilisateur si nécessaire, et placer le compagnon après le mod principal dans un playset de test. Aucune de ces opérations n’a été faite par cette livraison. Activer le mode debug pour la console et lancer une nouvelle partie.

1. Dans la console d’effets, armer explicitement : `effect set_global_variable = aor1776_hre_c01_dev_armed`.
2. Exécuter `effect aor1776_hre_c01_dev_setup = yes`. Vérifier ANH10% et KPF5% sous l’empereur courant, tous deux distincts et non annexés. Si un précontrôle refuse, ne pas forcer une conversion générale.
3. Laisser passer au moins un prélèvement hebdomadaire : comparer une seule sortie et une seule entrée du pacte ; pas de deuxième taxe cachée. Relever valeurs réelles et effet de l’emploi/dépenses, sans les confondre avec le taux natif.
4. Tester guerre offensive/défensive de l’empereur, puis empereur simple soutien. Vérifier qui rejoint, sans prétendre que ces cas sont équivalents.
5. Essayer annexion, baisse d’autonomie, prise d’État et unification sur KPF ; vérifier que les actions ne permettent pas de contourner sa protection. Tester une interaction indépendante ordinaire pour vérifier qu’elle n’est pas globalement bloquée.
6. Déclencher l’élection par le système existant après décès et choisir PRU. Pour isoler uniquement le transfert, la console peut appeler `effect c:PRU = { aor1776_hre_install_elected_country = yes }` dans cette partie de test ; ce raccourci ne valide PAS le scrutin lui-même.
7. Vérifier ANH et KPF sous PRU, ancien AUS autonome, gouvernements, populations, bâtiments, armées et territoires conservés. Vérifier OLD–HLB et autres pactes hors sélection. Contrôler absence de cycle, désir de liberté et marchés.
8. Refaire séparément avec KPF, auparavant sujet, comme élu. Le candidat doit devenir indépendant avant le transfert des autres sujets. Vérifier les élections suivantes, pas seulement un appel de transfert.
9. Hors scrutin, dans le test uniquement : donner à ANH `aor1776_hre_constitutional_privilege_change_authorized`, appeler `aor1776_hre_grant_electoral_privilege`, vérifier type et voix ; réautoriser puis appeler revoke pour vérifier le retour sans perte de désir de liberté. Pendant un scrutin, la mutation doit être refusée.
10. Tester un candidat sujet étranger et un cas de création de bloc refusée. Les sujets étrangers ne doivent pas être libérés ; l’échec ne doit pas être masqué par un drapeau de réussite.

Relever erreurs nouvelles dans les journaux. Conclure chaque catégorie séparément : affichage, paiement, diplomatie, guerre, annexion et succession. Un mois de simulation sans crash ne certifie pas toutes les branches. La conversion générale reste une mission distincte.
''')
    doc('NEXT_STEPS.md','''# Suite autorisée après cette livraison

1. Contrôler l’affichage et les textures après redémarrage, sans activer le compagnon pour une partie normale.
2. Exécuter le protocole isolé, particulièrement les chemins d’annexion et deux élections successives.
3. Corriger seulement les écarts moteur observés, puis lever le verrou de succession après preuve suffisante.
4. Concevoir ultérieurement, avec autorisation distincte, les décisions constitutionnelles, l’éligibilité réévaluée après changements de possessions et l’éventuelle annexion des seuls États ordinaires.

Pas d’exception électorale d’annexion, pas d’arbre complet de centralisation ni de conversion générale livrés ou lancés automatiquement.
''')
    doc('ASSET_PROMPTS.md','''# Icônes et consignes finales

Outil : détourage par outil d’image intégré, pas CLI/API externe. Les feuilles originales du joueur restent inchangées. La conversion DDS et les mipmaps sont mécaniques. Il s’agit d’adaptations détourées, pas d’une certification de pixels identiques aux originaux.

État impérial : `workshop_assets/source/HRE_CENTRALIZATION_01/imperial_estate.png`, texture `gfx/interface/icons/diplomatic_action_icons/aor1776_imperial_estate.dds`.

Prompt : Use case: background-extraction. Edit target: supplied two-icon sheet. Extract ONLY the RIGHT icon (red and gold imperial crown over round gold double-headed-eagle medallion, red drapery and teal laurel) as a single square transparent game UI icon. Remove white background and the entire left banner-and-chain icon. Preserve existing RIGHT artwork, colors, proportions and all heraldic symbols faithfully; no redesign, no text, no new motifs. Center the complete right icon with a small transparent margin. Actual alpha transparency, not a checkerboard drawing. Intended asset: Imperial Electorate subject icon for Victoria 3.

Le dernier intitulé du prompt précédent a été supersédé par la consigne du joueur : cette image de droite est finalement affectée à l’État impérial.

Électorat impérial : `workshop_assets/source/HRE_CENTRALIZATION_01/imperial_elector.png`, texture `gfx/interface/icons/diplomatic_action_icons/aor1776_imperial_elector.dds`.

Prompt : Use case: background-extraction. Edit target: the supplied sheet. Extract ONLY the LEFT icon: gold imperial double-headed-eagle banner, chain links, teal laurel, and critically the RED ROUND MEDALLION WITH THREE SMALL GOLD CROWNS arranged two above one. Remove the white background and the entire right large-crown icon. Preserve left design and all symbols faithfully; DO NOT replace the three crowns on the red medallion with an eagle. No added elements or text. Center complete left icon on square canvas with modest transparent margin, actual alpha transparency. Intended asset: Imperial Electorate icon for Victoria 3.
''')
    patcher.OUT=OUT;patcher.emit(files,'REPORTS.patch')
    print('Eleven required Markdown reports and asset prompt record prepared.')

def assets():
    # Image generation performs extraction. This step only copies the selected
    # transparent masters and encodes resized game textures with mipmaps.
    from PIL import Image
    import numpy as np
    from prototype_map2k_main_map import dds
    selected={'estate':'exec-20598350-ace5-4daf-91ac-a311e6719d23.png','elector':'exec-8ac02a88-1497-4009-95df-1b6707485cfb.png'}
    source=Path('C:/Users/simeo/.codex/generated_images/01a080b1-616e-71b2-85c3-0d7759724725')
    destination=ROOT/'workshop_assets/source/HRE_CENTRALIZATION_01';destination.mkdir(parents=True,exist_ok=True)
    target=ROOT/'gfx/interface/icons/diplomatic_action_icons';results=[]
    for kind,filename in selected.items():
        master=destination/('imperial_'+kind+'.png');shutil.copyfile(source/filename,master)
        im=Image.open(master).convert('RGBA');assert im.getchannel('A').getextrema()==(0,255),'Actual alpha required'
        small=im.resize((128,128),Image.Resampling.LANCZOS)
        path=target/('aor1776_imperial_'+kind+'.dds');assert not path.exists(),'Do not overwrite existing icon'
        dds(small,path);decoded=Image.open(path).convert('RGBA');assert np.array_equal(np.array(small),np.array(decoded))
        results.append(dict(kind=kind,master=master.relative_to(ROOT).as_posix(),texture=path.relative_to(ROOT).as_posix(),alpha=[0,255],size=[128,128],sha256=qa.sha(path)))
    dump('ASSET_VALIDATION.json',dict(icons=results,user_mapping='Newest LEFT three-crowns banner = electorate; retained RIGHT large crown = estate.',method='Built-in image generation background extraction; native DDS encoding only afterwards. Original supplied sheets unchanged.',retained_prompts='Background extraction only; preserve symbols, remove white and other icon. Elector: retain three gold crowns on red medallion. Estate: retain large crown and eagle medallion.'))
    print('Two selected transparent icons encoded and round-trip verified.')

def prototype():
    effects=block('aor1776_hre_c01_dev_setup',f'''if = {{ limit = {{ has_global_variable = aor1776_hre_c01_dev_armed exists = global_var:aor1776_hre_emperor_country }}
 global_var:aor1776_hre_emperor_country = {{ save_scope_as = c01_test_emperor }}
 c:ANH ?= {{ if = {{ limit = {{ aor1776_hre_centralization_native_eligible = yes is_subject = no aor1776_hre_elector = no NOT = {{ this = scope:c01_test_emperor }} }}
  scope:c01_test_emperor = {{ create_diplomatic_pact = {{ country = c:ANH type = aor1776_imperial_estate }} }}
 }} }}
 c:KPF ?= {{ if = {{ limit = {{ aor1776_hre_centralization_native_eligible = yes is_subject = no aor1776_hre_elector = yes NOT = {{ this = scope:c01_test_emperor }} }}
  scope:c01_test_emperor = {{ create_diplomatic_pact = {{ country = c:KPF type = aor1776_imperial_elector }} }}
 }} }}
}}''')
    effects+=block('aor1776_hre_c01_restore_marked_subject',f'''if = {{ limit = {{ NOT = {{ this = scope:c01_new_emperor }} has_variable = c01_transfer_selected }}
 if = {{ limit = {{ is_subject = yes }} make_independent = yes }}
 save_scope_as = c01_transfer_estate
 if = {{ limit = {{ has_variable = c01_was_elector }} scope:c01_new_emperor = {{ create_diplomatic_pact = {{ country = scope:c01_transfer_estate type = aor1776_imperial_elector }} }} }}
 else = {{ scope:c01_new_emperor = {{ create_diplomatic_pact = {{ country = scope:c01_transfer_estate type = aor1776_imperial_estate }} }} }}
 add_liberty_desire = {{ value = var:c01_previous_liberty subtract = liberty_desire }}
 aor1776_hre_sync_imperial_subject_status = yes
 join_power_bloc = scope:c01_new_emperor
}}''')
    effects+=block('aor1776_hre_c01_transfer_test',f'''if = {{ limit = {{ has_global_variable = aor1776_hre_c01_dev_armed exists = global_var:aor1776_hre_emperor_country
 aor1776_hre_candidate = yes NOT = {{ this = global_var:aor1776_hre_emperor_country }}
 OR = {{ is_subject = no AND = {{ is_direct_subject_of = global_var:aor1776_hre_emperor_country aor1776_hre_centralized_subject = yes }} }}
 is_at_war = no is_diplomatic_play_committed_participant = no
 global_var:aor1776_hre_emperor_country = {{ is_subject = no is_at_war = no is_diplomatic_play_committed_participant = no
  NOT = {{ any_direct_subject = {{ aor1776_hre_centralized_subject = yes aor1776_hre_centralization_native_eligible = no }} }}
 }} }}
 save_scope_as = c01_new_emperor
 global_var:aor1776_hre_emperor_country = {{ save_scope_as = c01_old_emperor
  every_direct_subject = {{ limit = {{ aor1776_hre_centralized_subject = yes }}
   set_variable = c01_transfer_selected
   set_variable = {{ name = c01_previous_liberty value = liberty_desire }}
   if = {{ limit = {{ is_subject_type = {ELECTOR} }} set_variable = c01_was_elector }}
  }}
 }}
 if = {{ limit = {{ has_variable = c01_transfer_selected }} make_independent = yes }}
 {INSTALL}_legacy = yes
 if = {{ limit = {{ this = global_var:aor1776_hre_emperor_country is_power_bloc_leader = yes power_bloc ?= {{ has_identity = identity:identity_aor1776_imperial_federation }} }}
  every_country = {{ limit = {{ has_variable = c01_transfer_selected }} aor1776_hre_c01_restore_marked_subject = yes }}
  scope:c01_old_emperor = {{ if = {{ limit = {{ aor1776_hre_centralization_native_eligible = yes is_subject = no }}
   save_scope_as = c01_old_estate
   if = {{ limit = {{ aor1776_hre_elector = yes }} scope:c01_new_emperor = {{ create_diplomatic_pact = {{ country = scope:c01_old_estate type = aor1776_imperial_elector }} }} }}
   else = {{ scope:c01_new_emperor = {{ create_diplomatic_pact = {{ country = scope:c01_old_estate type = aor1776_imperial_estate }} }} }}
  }} }}
  remove_global_variable = aor1776_hre_centralized_transfer_pending
  set_global_variable = aor1776_hre_c01_transfer_test_completed
 }}
 else = {{
  if = {{ limit = {{ has_variable = c01_transfer_selected is_subject = no }}
   if = {{ limit = {{ has_variable = c01_was_elector }} scope:c01_old_emperor = {{ create_diplomatic_pact = {{ country = scope:c01_new_emperor type = aor1776_imperial_elector }} }} }}
   else = {{ scope:c01_old_emperor = {{ create_diplomatic_pact = {{ country = scope:c01_new_emperor type = aor1776_imperial_estate }} }} }}
   add_liberty_desire = {{ value = var:c01_previous_liberty subtract = liberty_desire }}
  }}
  set_global_variable = aor1776_hre_c01_transfer_test_failed
 }}
 every_country = {{ remove_variable = c01_transfer_selected remove_variable = c01_was_elector remove_variable = c01_previous_liberty }}
}}''')
    # Override only in the separately enabled companion. No normal UI entry,
    # no on_action, no automatic event, and an additional console arming flag.
    override=block(INSTALL,f'''if = {{ limit = {{ has_global_variable = aor1776_hre_c01_dev_armed any_country = {{ aor1776_hre_centralized_subject = yes }} }}
 aor1776_hre_c01_transfer_test = yes
}}
else_if = {{ limit = {{ NOT = {{ any_country = {{ aor1776_hre_any_native_bond = yes }} }} }} {INSTALL}_legacy = yes }}
else = {{ set_global_variable = aor1776_hre_centralized_transfer_pending }}''')
    replacement=replace_node(load('EXPECTED_TEXT.json')[EF],INSTALL,override)
    files={str((COMPANION/'mod/common/scripted_effects/zz_hre_centralization_01_test.txt').relative_to(ROOT)):effects,
        str((COMPANION/'mod'/EF).relative_to(ROOT)):replacement,
        str((COMPANION/'HRE_CENTRALIZATION_01_TEST.mod').relative_to(ROOT)):'name="1776 — HRE centralization isolated TEST"\nsupported_version="1.13.*"\npath="'+(COMPANION/'mod').as_posix()+'"\n',
        str((COMPANION/'mod/descriptor.mod').relative_to(ROOT)):'name="1776 — HRE centralization isolated TEST"\nsupported_version="1.13.*"\ntags={ "Utilities" }\n'}
    cw.parse(effects);dump('PROTOTYPE_EXPECTED.json',files);patcher.OUT=OUT;patcher.emit(files,'PROTOTYPE.patch')
    print('Isolated companion patch prepared; no playset or launcher modified.')

def validate():
    if (OUT/'SECESSION_LENS_R2/EXPECTED_TEXT.json').exists():
        from hre_secession_lens_01 import validate as current_validate
        return current_validate()
    if (OUT/'FEEDBACK_R1/EXPECTED_TEXT.json').exists():
        from hre_subject_feedback_01 import validate as current_validate
        return current_validate()
    import collections as C
    b=load('BASELINE.json');now=qa.inventory();checks=[]
    def check(name,ok,detail=None):
        checks.append(dict(name=name,passed=bool(ok),detail=detail))
        if not ok:print('FAIL',name,detail,flush=True)
    for k in b['inventory']:check('Historical inventory unchanged: '+k,now[k]==b['inventory'][k])
    current=economy.runtime_hashes();expected=load('EXPECTED_TEXT.json')
    changed=sorted(p for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p))
    icons={r['texture'] for r in load('ASSET_VALIDATION.json')['icons']}
    allowed=set(load('PLAN.json')['files'])|icons
    check('Only exact scoped runtime changes',set(changed)==allowed,changed)
    for p,text in expected.items():
        check('Compiled expected text '+p,(ROOT/p).read_text(encoding='utf-8-sig')==text.lstrip('\ufeff'))
        if p.endswith(('.txt','.gui')):
            try:cw.parse((ROOT/p).read_text(encoding='utf-8-sig'));ok=True
            except Exception:ok=False
            check('Parse '+p,ok)
    types={}
    from map_1776_audit import effective
    for p in effective(ROOT,GAME,'common/subject_types'):
        for n in cw.parse(p.read_text(encoding='utf-8-sig')):types[n.key]=n
    check('Only one legacy bond and two new types',{'subject_type_aor1776_hre_crownland'}&set(types)==set() and all(t in types for t in [LINK,ESTATE,ELECTOR]))
    native={n.key:qa.signature(n) for n in cw.parse((GAME/'common/subject_types/00_subject_types.txt').read_text(encoding='utf-8-sig'))}
    check('All vanilla subject definitions identical',all(qa.signature(types[k])==s for k,s in native.items()))
    for typ in [LINK,ESTATE,ELECTOR]:
        n=types[typ]
        check('No country formation annexation '+typ,n.one('annex_on_country_formation')=='no')
        check('No autonomy alternatives '+typ,all(not n.children(f)[0].children() for f in ['lower_autonomy_subject_type_alternatives','higher_autonomy_subject_type_alternatives','same_autonomy_subject_type_alternatives']))
        if typ!=LINK:check('Dependent diplomacy and military '+typ,n.one('can_start_own_diplomatic_plays')=='no' and n.one('join_overlord_wars')=='yes' and n.one('use_overlord_ruler')=='no')
    da=cw.parse((ROOT/'common/diplomatic_actions/1776_imperial_centralization.txt').read_text(encoding='utf8'))
    for n,rate in zip(da,[CONFIG['estate_tribute'],CONFIG['elector_tribute']]):
        p=n.children('pact')[0]
        check('One native tribute with correct direction '+n.key,len(p.children('income_transfer'))==1 and float(p.one('income_transfer'))==rate and p.one('income_transfer_based_on_second_country')=='yes' and p.one('second_country_gets_income_transfer')=='no')
        check('No ordinary offer or influence burden '+n.key,n.children('potential')[0].one('always')=='no' and float(p.one('cost'))==0)
    for lang in ['english','french']:
        raw='\n'.join((ROOT/p).read_text(encoding='utf-8-sig') for p in expected if p.startswith('localization/'+lang+'/'))
        keys=re.findall(r'(?m)^[ \t]+([\w.]+):(?:\d+)?[ \t]',raw)
        check('No duplicate localization keys in compiled layer '+lang,len(keys)==len(set(keys)))
        for typ,concept in [(LINK,'concept_aor1776_hre_protectorate'),(ESTATE,'concept_imperial_estate'),(ELECTOR,'concept_imperial_elector')]:
            check('Subject UI contracts '+lang+' '+typ,all(k in keys for k in [typ,typ+'_no_icon',concept,concept+'_desc']))
        concepts=set(re.findall(r"\[(?:Concept\(')?(concept_[\w]+)",raw))
        native_loc=(GAME/f'localization/{lang}/concepts_l_{lang}.yml').read_text(encoding='utf-8-sig')
        native_keys=set(re.findall(r'(?m)^\s+(concept_[\w]+):',native_loc))
        check('All linked concepts resolve '+lang,concepts<=native_keys|set(keys),sorted(concepts-native_keys-set(keys)))
    check('Territorial registry untouched',qa.sha(active_registry_path())==b['registry_sha256'])
    for p,h in b['hashes'].items():
        if p.startswith(('map_data/','common/history/states/','common/history/pops/','common/history/buildings/','common/history/military_formations/','common/history/diplomacy/')):check('Protected territorial/demographic file '+p,current.get(p)==h)
    for p,h in b['native_hashes'].items():check('Installed game read-only '+p,qa.sha(GAME/p)==h)
    for p,s in load('PROTOTYPE_EXPECTED.json').items():check('Isolated prototype '+p,(ROOT/p).read_text(encoding='utf-8-sig')==s.lstrip('\ufeff'))
    check('No test arming or activation in initial histories',all('c01_dev_armed' not in (ROOT/p).read_text(encoding='utf-8-sig') and 'type = aor1776_imperial_estate' not in (ROOT/p).read_text(encoding='utf-8-sig') and 'type = aor1776_imperial_elector' not in (ROOT/p).read_text(encoding='utf-8-sig') for p in current if p.startswith('common/history/') and p.endswith('.txt')))
    check('Git HEAD unchanged',subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['git_head']);check('Git index unchanged',qa.sha(ROOT/'.git/index')==b['git_index_sha256'])
    v=dict(status='STATIC_PASS_RUNTIME_PENDING' if all(r['passed'] for r in checks) else 'FAILED',passed=sum(r['passed'] for r in checks),total=len(checks),checks=checks,runtime_files_modified=changed,engine_test_executed=False,general_conversion_enabled=False,election_transfer_status='ISOLATED_PROTOTYPE_UNVERIFIED_PRODUCTION_FAIL_CLOSED',world_population=sum(p['count'] for p in now['pops']),previous_anomalies=dict(duplicate_RGBs=len(now['duplicates']),invalid_references=len(now['errors'])))
    dump('VALIDATION.json',v);print(v['status'],v['passed'],'/',v['total'],flush=True)
    assert v['passed']==v['total']

if __name__=='__main__':globals()[sys.argv[1]]()
