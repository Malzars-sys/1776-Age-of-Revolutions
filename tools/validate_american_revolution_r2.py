"""Read-only static regression checks for American Revolution R2.

Prints JSON. Does not run the game, write saves, change Git, or apply patches.
Accounting scenarios are arithmetic invariants, not simulated campaign results.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import re
import collections

from validate_diplomacy_ottoman_1776 import parse, walk, scalar, normalized
from localization_duplicate_audit import entries

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/reports/military/AMERICAN_REVOLUTION_R2'
CHECKS={}

def read(path):return (ROOT/path).read_text(encoding='utf-8-sig')
def baseline(path):return (OUT/'baseline'/path).read_text(encoding='utf-8-sig')
def tree(path):return parse(read(path))
def definition(path,key):return next(n for n in tree(path) if n.key==key)
def check(name,value):CHECKS[name]=bool(value)
def country(raw,tag):return next(n for n in walk(parse(raw)) if n.key=='c:'+tag)

def support_checks():
    effectfile='common/scripted_effects/1776_usa_french_support.txt'
    nodes=definition(effectfile,'aor1776_support_conclude_effect')
    native_guard=next(n for n in walk(nodes.children()) if n.key=='can_create_treaty')
    native_effect=next(n for n in walk(nodes.children()) if n.key=='create_treaty')
    check('support.same_native_inputs_for_guard_and_creation',normalized(native_guard.children())==normalized([n for n in native_effect.children() if n.key!='name']))
    articles=next(n for n in native_effect.children() if n.key=='articles_to_create').children()
    check('support.exactly_money_arms_artillery_articles',len(articles)==3)
    check('support.every_article_FRA_to_USA',all(n.one('source_country')=='c:FRA' and n.one('target_country')=='c:USA' for n in articles))
    for name,flag in [('aor1776_support_money','is_money_transfer'),('aor1776_support_supplies','is_goods_transfer')]:
        n=definition('common/treaty_articles/1776_usa_french_support.txt',name)
        flags=[scalar(x.value) for f in n.children('flags') for x in f.children()]
        check(name+'.native_flag_only',flags==[flag])
        check(name+'.bounded_by_active_agreement',any(x.key=='has_variable' and x.value=='aor1776_support_active' for x in walk(n.children('requirement_to_maintain'))))
    effects=read(effectfile)
    check('support.no_scripted_cash_creation','add_treasury' not in effects and 'country_tax_income_add' not in effects)
    accept=definition('common/scripted_triggers/1776_usa_french_support.txt','aor1776_french_support_can_accept')
    check('support.accept_rejects_duplicates','aor1776_french_support_can_accept = yes' in effects and any(n.key=='NOT' and n.one('has_variable')=='aor1776_support_active' for n in walk(accept.children())))
    check('support.literal_levels',all(s in effects for s in ['MONEY = 14000 ARMS = 6','MONEY = 21000 ARMS = 12']))
    check('support.contract_182_days_and_gap_14_days','name = aor1776_support_active days = 182' in effects and 'name = aor1776_support_cooldown days = 196' in effects)
    check('support.max_six_contracts',any(n.key=='var:aor1776_support_rounds' and n.op=='<' and n.value=='6' for n in walk(accept.children())))
    check('support.obligation_not_refreshed','NOT = { owes_obligation_to = c:FRA }' in effects and 'aor1776_support_obligation_issued' in effects)
    a=json.loads(read('docs/reports/military/AMERICAN_REVOLUTION_R2/ECONOMIC_AUDIT.json'))
    scenarios=json.loads(read('docs/reports/military/AMERICAN_REVOLUTION_R2/SUPPORT_SCENARIOS.json'))
    for row in scenarios:
        check('accounting.'+row['scenario']+'.conserved_pair',abs(row['USA_balance_before_market_feedback']+row['FRA_balance_before_goods_freight_feedback']-a['USA']['balance']-a['FRA']['balance'])<0.00001)
        check('accounting.'+row['scenario']+'.USA_deficit_retained',row['USA_balance_before_market_feedback']<0)
        check('accounting.'+row['scenario']+'.France_surplus_before_goods',row['FRA_balance_before_goods_freight_feedback']>0)
    oldfile='events/french_revolution_mod_events.txt'
    for i in range(1,5):
        n=definition(oldfile,'french_revolution_mod_events.'+str(i))
        check('legacy.event_'+str(i)+'.no_unfunded_debt_or_forced_revolution',not any(x.key in ['change_infamy','add_modifier','add_journal_entry','trigger_event'] for x in walk(n.children())))
    old=parse(baseline(oldfile));new=tree(oldfile)
    keep=lambda n:n.key not in ['french_revolution_mod_events.'+str(i) for i in range(1,5)]
    check('legacy.French_events_5_onward_preserved',normalized([n for n in old if keep(n)])==normalized([n for n in new if keep(n)]))
    war=read('common/history/diplomatic_plays/00_american_revolution.txt')
    check('chronology.France_not_forced_into_initial_war','c:FRA' not in war)
    check('chronology.other_initial_backers_preserved',all('c:'+t in war for t in ['SPA','SC1','SC2','SC3','SC4']))
    check('chronology.no_scripted_entry_into_war',not any(n.key in ['create_diplomatic_play','start_war','join_war'] for n in walk(tree(effectfile))))
    for f in ['common/history/countries/usa - usa.txt','common/history/countries/fra - france.txt','common/character_templates/1776_usa_commanders.txt']:
        check('protected.'+f,read(f)==baseline(f))
    na='common/history/military_formations/01_military_formations_north_america.txt'
    old,new=country(baseline(na),'USA'),country(read(na),'USA')
    check('protected.seven_USA_commanders_unchanged',normalized(old.children('create_character'))==normalized(new.children('create_character')))
    army=lambda c:[f for f in c.children('create_military_formation') if f.one('type')=='army']
    check('protected.MIL_USA_army_unchanged',normalized(army(old))==normalized(army(new)))

def localization_checks():
    found={}
    for lang in ['french','english']:
        p=ROOT/f'localization/{lang}/1776_usa_revolution_r2_l_{lang}.yml'
        raw=p.read_text(encoding='utf-8-sig');lines=raw.splitlines()
        matches=[re.fullmatch(r' ([\w.]+):0 "(?:[^"\\]|\\.)*"',s) for s in lines[1:] if s]
        check('loc.'+lang+'.BOM_and_header',p.read_bytes().startswith(b'\xef\xbb\xbf') and lines[0]=='l_'+lang+':')
        check('loc.'+lang+'.syntax',all(matches))
        found[lang]={m.group(1) for m in matches if m}
        all_entries=entries(lang)
        check('loc.'+lang+'.unique_keys',all(len(all_entries[k])==1 for k in found[lang]))
    check('loc.same_keys_FR_EN',found['french']==found['english'])
    for lang in ['french','english']:
        path='localization/'+lang+'/mod_v2content_l_'+lang+'.yml'
        keep=lambda raw:'\n'.join(line for line in raw.splitlines() if not re.match(r'\s*je_usa_independence_fra(?:_reason|_lobby)?:',line))
        check('loc.'+lang+'.legacy_journal_only_three_keys_changed',keep(read(path))==keep(baseline(path)))
        check('loc.'+lang+'.legacy_journal_no_duplicate',all(len(entries(lang)[k])==1 for k in ['je_usa_independence_fra','je_usa_independence_fra_reason','je_usa_independence_fra_lobby']))
    consumer=[]
    for folder in ['events','common/journal_entries','common/decisions','common/scripted_buttons','common/scripted_triggers','common/ship_types','common/ship_modifications','common/static_modifiers','common/laws','common/character_templates','common/character_traits','common/treaty_articles']:
        for p in (ROOT/folder).glob('*1776*usa*'):
            if p.suffix=='.txt':consumer+=list(walk(parse(p.read_text(encoding='utf-8-sig'))))
    refs={scalar(n.value) for n in consumer if n.key in ['title','desc','flavor'] and isinstance(n.value,str) and str(n.value).startswith('aor1776_')}
    refs.update(scalar(n.one('name')) for n in consumer if n.key=='option' and isinstance(n.one('name'),str) and n.one('name').startswith('aor1776_'))
    refs.update(scalar(n.value) for n in consumer if n.key in ['first_name','last_name'] and isinstance(n.value,str) and n.value.startswith('aor1776_founder_'))
    refs.update(scalar(n.value) for n in consumer if n.key=='text' and isinstance(n.value,str) and n.value.startswith('aor1776_'))
    refs.update(scalar(n.one('name')) for p in (ROOT/'common/scripted_buttons').glob('*1776*usa*.txt') for n in tree(p.relative_to(ROOT)) if isinstance(n.one('name'),str))
    check('loc.all_explicit_USA_R2_text_refs',refs<=found['english'])
    for folder in ['common/decisions','common/ship_types','common/ship_modifications','common/static_modifiers','common/laws','common/treaty_articles']:
        keys={n.key for p in (ROOT/folder).glob('*1776*usa*.txt') for n in parse(p.read_text(encoding='utf-8-sig'))}
        check('loc.all_names.'+folder,keys<=found['english'])
    journal_names={n.key for p in (ROOT/'common/journal_entries').glob('*1776*usa*.txt') for n in parse(p.read_text(encoding='utf-8-sig'))}
    check('loc.all_new_journal_titles_and_reasons',journal_names|{k+'_reason' for k in journal_names}<=found['english'])

def naval_checks():
    import start_buildings_2026_10_15 as e
    from map_1776_audit import values
    oldkey='ship_type_caravel';key='ship_type_aor1776_armed_merchantman'
    units=e.catalog('common/ship_types');mods=e.catalog('common/ship_modifications');tech=e.starting_tech('USA')
    n=units[key]
    check('nav.hull_gate_available',set(values(n,'unlocking_technologies'))<=tech)
    slots={x.key:scalar(x.value) for b in n.children('default_modifications') for x in b.children()}
    check('nav.five_default_equipment_slots',len(slots)==5)
    for slot,m in slots.items():
        check('nav.'+slot+'.equipment_exists_and_unlocked',m in mods and set(values(mods[m],'unlocking_technologies'))<=tech)
        choices=next(x for b in n.children('modifications') for x in b.children() if x.key==slot)
        check('nav.'+slot+'.only_contemporary_option',[scalar(x.value) for x in choices.children()]==[m])
    ignore={'modifications','default_modifications','unlocking_technologies','ai_weight'}
    check('nav.caravel_performance_and_costs_preserved',normalized([x for x in units[oldkey].children() if x.key not in ignore])==normalized([x for x in n.children() if x.key not in ignore]))
    f='common/ship_types/10_1776_early_ships.txt'
    check('nav.other_early_hulls_unchanged',read(f)==baseline(f))
    f='common/history/military_formations/01_military_formations_north_america.txt'
    expected=baseline(f).replace('type = ship_type:ship_type_caravel','type = ship_type:'+key,1)
    check('nav.only_USA_hull_identifier_changed',read(f)==expected)
    usa=country(read(f),'USA');ships=[x for x in walk(usa.children()) if x.key=='ship']
    check('nav.five_USA_ships_preserved',len(ships)==1 and ships[0].one('count')=='5')

def content_r1_checks():
    from decimal import Decimal
    law=definition('common/laws/00_army_model.txt','law_aor1776_minutemen')
    check('minutemen.army_variant_not_internal_security',law.one('group')=='lawgroup_army_model' and law.one('parent')=='law_national_militia')
    mods={n.key:n.value for g in law.children('modifier') for n in g.children()}
    check('minutemen.keep_initial_capacity',mods.get('state_conscription_rate_add')=='0.04' and mods.get('state_building_barrack_max_level_add')=='25' and mods.get('state_building_conscription_center_max_level_add')=='25')
    check('minutemen.no_internal_security_or_rebellion_bonus',not any(s in k for k in mods for s in ['coup','radical','secession','leverage','revolution']))
    check('minutemen.USA_only_and_not_imposable','c:USA ?= this' in read('common/laws/00_army_model.txt') and normalized(law.children('can_impose')[0].children())==[('always','=','no')])
    fx=read('common/scripted_effects/1776_usa_content_r1.txt')
    check('fervour.clamp_0_100','var:aor1776_fervour > 100' in fx and 'var:aor1776_fervour < 0' in fx)
    for name in ['low','high','steady']:
        check('fervour.'+name+'.removed_on_refresh_and_end',fx.count('remove_modifier = aor1776_fervour_'+name)==2)
    check('fervour.no_calendar_score_decay','change_variable' not in fx[fx.index('aor1776_content_monthly_effect'):].split('aor1776_support_fervour_awarded')[0])
    hooks=read('common/on_actions/1776_usa_content_r1.txt')
    check('fervour.native_nonempty_battle_hooks_only','on_empty_battle' not in hooks and 'on_battle_won =' in hooks and 'on_battle_lost =' in hooks)
    check('fervour.cooldowns_and_scoped_enemy',hooks.count('days = 90')==2 and hooks.count('exists = scope:enemy_country')==2 and hooks.count('c:GBR ?= this')==2)
    effects=[n for n in walk(tree('common/scripted_effects/1776_usa_content_r1.txt')) if n.key.startswith('every_')]
    check('fervour.no_global_or_army_scans',not effects)
    for level,expected in [('low',{'unit_morale_recovery_mult':'-0.05','unit_morale_loss_mult':'0.05'}),('high',{'unit_morale_recovery_mult':'0.05','unit_morale_loss_mult':'-0.05'})]:
        n=definition('common/static_modifiers/1776_usa_revolution_r2.txt','aor1776_fervour_'+level)
        check('fervour.'+level+'.exact_bounded_effects',{x.key:x.value for x in n.children() if x.key!='icon'}==expected)
    # Exhaustive mathematical bounds for every score, not a campaign simulation.
    check('fervour.every_score_within_R1_envelope',all(Decimal('0.10')<=Decimal('0.15')+Decimal('-0.05' if s<35 else '0.05' if s>65 else '0')<=Decimal('0.20') for s in range(101)))

def content_r2_checks():
    import start_buildings_2026_10_15 as e
    from map_1776_audit import effective, values
    templates=e.catalog('common/character_templates');traits=e.catalog('common/character_traits')
    births={'aor1776_benjamin_franklin':'1706.1.17','aor1776_john_adams':'1735.10.30','aor1776_thomas_jefferson':'1743.4.13'}
    counts=collections.Counter(n.key for p in effective(ROOT,Path('C:/Games/Victoria 3/game'),'common/character_templates') for n in parse(p.read_text(encoding='utf-8-sig')))
    history=tree('common/history/characters/zz_1776_usa_founders.txt')
    creates=[n for n in walk(history) if n.key=='create_character']
    check('founders.exactly_three_creations',collections.Counter(n.one('template') for n in creates)==collections.Counter(births.keys()))
    for key,birth in births.items():
        t=templates[key]
        check('founders.'+key+'.unique_definition',counts[key]==1)
        check('founders.'+key+'.historical_birth',t.one('birth_date')==birth)
        check('founders.'+key+'.politician_without_imposed_office',t.one('role')=='politician' and t.one('ig_leader') is None and t.one('ruler') is None)
        check('founders.'+key+'.deterministic_existing_traits',t.one('trait_generation')==[] and all(v in traits for v in values(t,'traits')))
    guards=[n for n in walk(history) if n.key=='if']
    check('founders.each_creation_guarded_against_duplicates',len(guards)==3 and all(any(n.key=='NOT' and any(x.key=='has_template' and x.value==g.children('create_character')[0].one('template') for x in walk(n.children())) for b in g.children('limit') for n in b.children()) for g in guards))
    availability=tree('common/scripted_triggers/1776_usa_founders.txt')
    check('founders.alive_adult_USA_available_politicians',len(availability)==3 and all(all(s in {x.key for x in walk(n.children())} for s in ['has_template','is_character_alive','owner','has_role_of_type','age','is_busy']) for n in availability))
    decisions=read('common/decisions/1776_usa_founders.txt');events=tree('events/1776_usa_founders.txt')
    check('founders.Franklin_dated_and_annual_cost','game_date >= 1776.9.26' in decisions and 'days = 365' in decisions and 'add_treasury = -5000' in read('events/1776_usa_founders.txt'))
    commission=next(n for n in events if n.key=='aor1776_usa_founders.2')
    policy=[o for o in commission.children('option') if o.children('add_modifier')]
    check('founders.commission_one_choice_only',len(policy)==2 and all('aor1776_founders_commission_done' in [x.value for x in walk(o.children('trigger')) if x.key=='has_variable'] for o in policy))
    check('founders.commission_rechecks_republic_independence_life',all(any(x.key=='has_law_or_variant' and x.value=='law_type:law_presidential_republic' for x in walk(o.children('trigger'))) and any(x.key=='is_subject' and x.value=='no' for x in walk(o.children('trigger'))) and any(x.key.endswith('_available') for x in walk(o.children('trigger'))) for o in policy))
    check('founders.policies_expire_after_24_months',all(m.one('months')=='24' for o in policy for m in o.children('add_modifier')))
    combined=read('common/scripted_effects/1776_usa_echoes.txt')
    maintenance=definition('common/scripted_effects/1776_usa_echoes.txt','aor1776_founders_maintenance_effect')
    check('founders.policies_removed_on_death_departure_government_change',combined.count('remove_modifier = aor1776_')==2 and len([n for n in walk(maintenance.children()) if n.key=='is_character_alive' and n.value=='yes'])==2 and len([n for n in walk(maintenance.children()) if n.key=='has_law_or_variant'])==2)
    check('founders.no_automatic_presidency_or_law',not any(n.key in ['set_ruler','activate_law','create_character'] for n in walk(events)))
    check('founders.Hancock_unchanged',subprocess.check_output(['git','show',json.loads((OUT/'BASELINE.json').read_text())['head']+':common/character_templates/country_usa.txt'],cwd=ROOT).decode('utf-8-sig').replace('\r\n','\n')==read('common/character_templates/country_usa.txt'))
    journal=definition('common/journal_entries/06_usa_independence_mod.txt','je_usa_independence')
    for result in ['on_complete','on_fail']:
        nodes=list(walk(journal.children(result)))
        check('echoes.'+result+'.explicit_dispatch_and_funding_end',all(any(n.key==k for n in nodes) for k in ['aor1776_independence_outcome_effect','aor1776_support_stop_effect','aor1776_content_finish_effect']))
    outcome=definition('common/scripted_effects/1776_usa_echoes.txt','aor1776_independence_outcome_effect')
    check('echoes.once_only_outcome_latch','NOT = { has_variable = aor1776_outcome_dispatched }' in combined and 'set_variable = aor1776_outcome_dispatched' in combined)
    check('echoes.no_global_pulse_or_country_scan',not any(n.key in ['every_country','random_country','every_scope_country','random_scope_country'] for n in walk(tree('common/scripted_effects/1776_usa_echoes.txt'))) and 'aor1776_independence_outcome_effect' not in read('common/on_actions/1776_usa_revolution_r2.txt'))
    roots={n.key for n in outcome.children()[0].children() if n.key.startswith('c:')}
    check('echoes.limited_named_recipients',roots=={'c:FRA','c:GBR','c:SPA','c:POR','c:NET','c:SWE','c:DEN'})
    check('echoes.colonies_filtered_by_subject_and_political_contact','is_subject = yes' in combined and 'has_law_or_variant = law_type:law_right_of_assembly' in combined and 'relations:c:USA >= 20' in combined)
    check('echoes.Europe_requires_exchange_and_intelligentsia','has_technology_researched = institutionalized_scientific_exchange' in combined and 'ig_counts_as_marginal = no' in combined)
    echoevents=[n for n in tree('events/1776_usa_echoes.txt') if n.key!='namespace']
    check('echoes.four_country_event_families',len(echoevents)==4)
    check('echoes.recipient_repeat_guards',all(any(x.key=='has_variable' and x.value=='aor1776_echo_seen' for x in walk(n.children('trigger'))) and any(x.key=='set_variable' and x.value=='aor1776_echo_seen' for x in walk(n.children('immediate'))) for n in echoevents))
    check('echoes.all_effects_expire_in_12_months',all(n.one('months')=='12' for n in walk(echoevents) if n.key=='add_modifier'))
    check('echoes.every_event_can_be_declined_without_modifier',all(any(o.one('default_option')=='yes' and not o.children('add_modifier') for o in n.children('option')) for n in echoevents))
    check('echoes.no_forced_revolution_independence_war',not any(n.key in ['add_journal_entry','create_diplomatic_play','set_subject_type','set_independent','start_war','create_country','create_character','activate_law'] for n in walk(echoevents)))

def reference_checks(files):
    import start_buildings_2026_10_15 as e
    nodes=[n for file in files for n in walk(tree(file))]
    definitions={n.key for folder in ['common/scripted_effects','common/scripted_triggers'] for p in (ROOT/folder).glob('*.txt') for n in parse(p.read_text(encoding='utf-8-sig'))}
    calls={n.key for n in nodes if n.key.startswith('aor1776_') and n.key not in definitions and n.key.endswith(('_effect','_available'))}
    check('references.all_custom_effects_and_triggers_defined',not calls)
    all_definitions=definitions|{n.key for file in files for n in tree(file)}
    check('references.all_custom_call_keys_defined',all(n.key in all_definitions for n in nodes if n.key.startswith('aor1776_')))
    eventdefs=e.catalog('events')
    check('references.all_triggered_events_exist',all(n.one('id') in eventdefs for n in nodes if n.key=='trigger_event'))
    moddefs=e.catalog('common/static_modifiers')
    usedmods=[scalar(n.value) if isinstance(n.value,str) else n.one('name') for n in nodes if n.key in ['add_modifier','remove_modifier']]
    check('references.all_static_modifiers_exist',all(k in moddefs for k in usedmods))
    lawdefs=e.catalog('common/laws')
    # Native law rules can compare a dynamic law scope (e.g. scope:law in
    # can_impose). Only fixed identifiers can be resolved through the catalog.
    check('references.all_law_identifiers_exist',all(scalar(n.value).startswith(('scope:','var:')) or scalar(n.value) in {'root','this','prev'} or scalar(n.value).split(':')[-1] in lawdefs for n in nodes if n.key in ['activate_law','has_law','has_law_or_variant'] and isinstance(n.value,str)))
    buttons=e.catalog('common/scripted_buttons')
    check('references.all_journal_buttons_exist',all(scalar(n.value) in buttons for n in nodes if n.key=='scripted_button'))
    techdefs=e.catalog('common/technology/technologies')
    check('references.all_technology_gates_exist',all(v in techdefs for n in nodes if n.key=='unlocking_technologies' for v in [scalar(x.value) for x in n.children()]))
    paths={scalar(n.value) for n in nodes if isinstance(n.value,str) and scalar(n.value).startswith('gfx/')}
    check('references.all_graphical_assets_exist',all((ROOT/p).exists() or (Path('C:/Games/Victoria 3/game')/p).exists() for p in paths))

def prior_military_checks():
    import start_buildings_2026_10_15 as e
    after=json.loads(read('docs/reports/military/MIL_START_AUDIT/AFTER.json'))
    locations={'POR':'00_military_formations_europe.txt','BRZ':'02_military_formations_south_america.txt','SC2':'02_military_formations_south_america.txt','SC4':'02_military_formations_south_america.txt'}
    for tag,file in locations.items():
        root=country(read('common/history/military_formations/'+file),tag)
        actual=collections.Counter()
        for n in walk(root.children('create_military_formation')):
            if n.key in ['combat_unit','ship']:
                actual[(n.key,n.one('type').split(':')[-1],n.one('service_type','regular'))]+=int(n.one('count'))
        expected=collections.Counter()
        for f in after[tag]['formations']:
            for u in f['units']:expected[(u['kind'],u['type'],u['service'])]+=u['count']
        check('protected.'+tag+'.MIL_START_forces',actual==expected)
        check('protected.'+tag+'.starting_technologies',sorted(e.starting_tech(tag))==after[tag]['technologies'])
    mod=definition('common/static_modifiers/76mod_modifiers.txt','modifier_usa_war_of_independence')
    check('protected.exact_Liberty_Or_Death_R1',{n.key:n.value for n in mod.children()}=={'icon':'gfx/interface/icons/timed_modifier_icons/modifier_rifle_positive.dds','building_training_rate_mult':'0.15','unit_morale_recovery_mult':'0.15','unit_morale_loss_mult':'-0.10','country_liberty_desire_add':'0.35'})

def runtime_fix_checks():
    """Prevent the observed January startup failure and raw-variable UI relapse.

    These are script invariants against locally shipped native examples, not a
    claim that a new treaty has been accepted or paid inside the game.
    """
    t='common/scripted_triggers/1776_usa_french_support.txt'
    war=definition(t,'aor1776_usa_independence_war_active')
    wn=list(walk(war.children()))
    check('startup.war_uses_native_war_relation',any(n.key=='has_war_with' and n.value=='c:GBR' for n in wn) and not any(n.key=='is_diplomatic_play_enemy_of' for n in wn))
    for key in ['je_usa_independence','je_usa_independence_fra']:
        journal=definition('common/journal_entries/06_usa_independence_mod.txt',key)
        check('startup.'+key+'.actual_war_condition',any(n.key=='has_war_with' and n.value=='c:GBR' for n in walk(journal.children('possible'))))
    relationship=definition(t,'aor1776_french_support_relationship_valid')
    check('startup.hostility_covers_play_and_actual_war',any(n.key=='NOR' and n.one('has_war_with')=='c:USA' and n.one('is_diplomatic_play_enemy_of')=='c:USA' for n in walk(relationship.children())))
    onactions=tree('common/on_actions/1776_usa_revolution_r2.txt')
    native=parse((Path('C:/Games/Victoria 3/game/common/on_actions/00_code_on_actions.txt')).read_text(encoding='utf-8-sig'))
    startup=next(n for n in onactions if n.key=='on_game_started_after_lobby')
    check('startup.post_lobby_hook_is_native',any(n.key==startup.key for n in native) and startup.one('on_actions') is not None)
    scheduler=next(n for n in onactions if n.key=='aor1776_usa_support_startup')
    check('startup.J_plus_2_after_lobby',any(n.key=='trigger_event' and n.one('id')=='aor1776_french_support.1' and n.one('days')=='2' for n in walk(scheduler.children())))
    check('startup.no_history_scheduling_race','trigger_event' not in read('common/history/countries/zz_1776_usa_revolution_r2.txt'))
    check('startup.scheduled_only_once','aor1776_support_startup_scheduled' in read('common/on_actions/1776_usa_revolution_r2.txt'))
    journal=definition('common/journal_entries/1776_usa_french_support.txt','je_aor1776_french_support')
    check('startup.weekly_retry_from_American_journal',any(n.key=='aor1776_support_weekly_effect' for n in walk(journal.children('on_weekly_pulse'))))
    fx=read('common/scripted_effects/1776_usa_french_support.txt')
    check('startup.no_retry_before_January_3','game_date >= 1776.1.3' in fx)
    check('startup.retry_has_no_global_scans',not any(n.key.startswith(('every_','random_scope_')) for n in walk(tree('common/scripted_effects/1776_usa_french_support.txt'))))
    request=definition(t,'aor1776_french_support_can_request')
    check('startup.request_prevents_pending_duplicates',all(any(n.key=='has_variable' and n.value==v for n in walk(request.children())) for v in ['aor1776_support_request_pending','aor1776_support_offer_window']))
    funds=definition(t,'aor1776_french_support_finances_available')
    check('startup.zero_budget_allowed_with_cash_floor',any(n.key=='net_total_income' and n.op=='>=' and n.value=='0' for n in walk(funds.children())) and any(n.key=='gold_reserves' and n.op=='>=' and n.value=='84000' for n in walk(funds.children())))
    for name in ['je_aor1776_french_support','je_aor1776_revolutionary_spirit']:
        file='common/journal_entries/'+('1776_usa_french_support.txt' if name.endswith('french_support') else '1776_usa_revolutionary_spirit.txt')
        complete=definition(file,name).children('complete')[0]
        check('UI.'+name+'.no_bare_variable_condition',len(complete.children())==1 and complete.children()[0].key=='custom_tooltip' and complete.children()[0].one('text')=='aor1776_independence_resolved_tt')
    check('UI.journal_has_request_and_stop_buttons',{n.value for n in journal.children('scripted_button')}=={'aor1776_request_french_support_button','aor1776_end_french_support_button'})
    buttons=tree('common/scripted_buttons/1776_usa_french_support.txt')
    check('UI.request_button_uses_common_guard_and_action',buttons[0].children('possible')[0].one('aor1776_french_support_can_request')=='yes' and buttons[0].children('effect')[0].one('aor1776_support_request_effect')=='yes')
    refusal=definition('events/1776_usa_french_support.txt','aor1776_french_support.1').children('option')[-1]
    check('UI.French_refusal_notifies_America',any(n.key=='trigger_event' and n.one('id')=='aor1776_french_support.4' for n in walk(refusal.children())))
    option=definition('events/1776_usa_french_support.txt','aor1776_french_support.2').children('option')[0]
    check('support.acceptance_option_rechecks_finances',option.children('trigger')[0].one('aor1776_french_support_can_accept')=='yes')
    bad=[]
    def guarded_removals(nodes,guards=frozenset()):
        for n in nodes:
            scoped=guards
            if n.key=='if':
                scoped=guards|{x.value for lim in n.children('limit') for x in lim.children('has_modifier')}
            if n.key=='remove_modifier' and n.value not in guards:bad.append(n.value)
            guarded_removals(n.children(),scoped)
    for f in ['common/scripted_effects/1776_usa_french_support.txt','common/scripted_effects/1776_usa_content_r1.txt','common/scripted_effects/1776_usa_echoes.txt']:
        guarded_removals(tree(f))
    check('logs.all_R2_modifier_removals_guarded',not bad)

def main():
    start=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    files=[]
    for folder in ['events','common/scripted_effects','common/scripted_triggers','common/treaty_articles','common/decisions','common/scripted_buttons','common/on_actions','common/history/countries','common/history/characters','common/journal_entries','common/laws','common/ship_types','common/ship_modifications','common/static_modifiers','common/character_templates','common/character_traits']:
        for p in (ROOT/folder).glob('*1776*usa*'):
            if p.suffix=='.txt':parse(p.read_text(encoding='utf-8-sig'));files.append(str(p.relative_to(ROOT)))
    check('syntax.all_USA_namespaced_files_parse',bool(files))
    support_checks();localization_checks()
    if (ROOT/'common/ship_types/1776_usa_armed_merchantman.txt').exists():naval_checks()
    if (ROOT/'common/laws/1776_usa_minutemen.txt').exists():content_r1_checks()
    if (ROOT/'common/character_templates/1776_usa_founders.txt').exists():content_r2_checks()
    reference_checks(files);prior_military_checks();runtime_fix_checks()
    b=json.loads((OUT/'BASELINE.json').read_text())
    index=Path(subprocess.check_output(['git','rev-parse','--git-path','index'],cwd=ROOT,text=True).strip())
    if not index.is_absolute():index=ROOT/index
    check('git.index_preserved',hashlib.sha256(index.read_bytes()).hexdigest()==b['index_sha256'])
    check('git.HEAD_preserved',subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['head']==start)
    print(json.dumps(dict(status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' if all(CHECKS.values()) else 'STATIC_VALIDATION_FAILED',runtime_executed=False,checked_head=start,passed=sum(CHECKS.values()),failed=[k for k,v in CHECKS.items() if not v],checks=CHECKS,parsed_files=files),ensure_ascii=False,indent=2))
    return 0 if all(CHECKS.values()) else 1

if __name__=='__main__':raise SystemExit(main())
