"""Read-only gameplay audit for MIL-FORT-ENGINEERS-1776 A1.

Writes only its dedicated report directory. The restricted AST projection is
explicitly a static check, never a Victoria 3 runtime validation.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from copy import deepcopy
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
import csv
import hashlib
import json
import re
import sys

from validate_diplomacy_ottoman_1776 import parse, walk, scalar
from map_1776_audit import own_inventory
import tech_start_1776_implementation as tech_audit
from validate_land_fortifications import Projection, sides
import build_land_fortification_battles as battle_build

ROOT = Path(__file__).resolve().parents[1]
GAME = Path('C:/Games/Victoria 3/game')
OUT = ROOT/'docs/reports/military/MIL_FORT_ENGINEERS_1776'
PLAN = json.loads((OUT/'PLAN.json').read_text(encoding='utf-8'))
GATE = 'scientific_fortification_siegecraft'
ENG = 'permanent_engineer_services'
LAND = 'building_aor1776_land_fortification'
COAST = 'building_naval_fortification'
FLAG = 'aor1776_historical_forts_a1_seeded'
EFFECTS = 'common/scripted_effects/1776_historical_forts_start.txt'
ACTIONS = 'common/on_actions/1776_historical_forts_start.txt'
HELPERS = {
    'FRA':'aor1776_historical_forts_a1_france',
    'GBR':'aor1776_historical_forts_a1_britain',
    'SPA':'aor1776_historical_forts_a1_spain',
    'POR':'aor1776_historical_forts_a1_portugal',
    'NET':'aor1776_historical_forts_a1_netherlands',
}
CHECKS = {}
CASES = []


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read(rel):
    return (ROOT/rel).read_text(encoding='utf-8-sig')


def check(name, condition, detail=None):
    CHECKS[name] = {'pass':bool(condition)}
    if detail is not None:
        CHECKS[name]['detail'] = detail


def json_file(name, value):
    (OUT/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def csv_file(name, rows, fields=None):
    with (OUT/name).open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fields or list(rows[0]), extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)


def effective(folder):
    files = {p.name.lower():p for p in (GAME/folder).glob('*.txt')}
    files.update({p.name.lower():p for p in (ROOT/folder).glob('*.txt')})
    return [files[k] for k in sorted(files)]


def get_defs(folder):
    result = {}
    for path in effective(folder):
        for n in parse(path.read_text(encoding='utf-8-sig')):
            result[n.key.removeprefix('REPLACE_OR_CREATE:')] = n
    return result


def starting_forts():
    result = {}
    for path in effective('common/history/buildings'):
        for s in walk(parse(path.read_text(encoding='utf-8-sig'))):
            if not s.key.startswith('s:STATE_'):
                continue
            for region in s.children():
                if not region.key.startswith('region_state:'):
                    continue
                for b in region.children('create_building'):
                    kind = scalar(b.one('building'))
                    if kind not in {LAND,COAST}:
                        continue
                    direct = b.one('level')
                    level = int(direct) if direct is not None else sum(
                        int(scalar(n.value)) for own in b.children('add_ownership')
                        for n in walk(own.children()) if n.key == 'levels')
                    pm = [scalar(n.value) for group in b.children('activate_production_methods') for n in group.children()]
                    key = (region.key.split(':',1)[1], s.key[2:], kind)
                    if key in result:
                        raise ValueError(f'Duplicate fort history selector: {key}')
                    result[key] = {'level':level,'pm':pm,'reserves':scalar(b.one('reserves')),
                                   'file':str(path),'line':path.read_text(encoding='utf-8-sig')[:b.start].count('\n')+1}
    return result


class StartProjection:
    """Only understands the exact supported start-script vocabulary; fails closed."""
    def __init__(self, definitions, world, technology, date=(1776,1,1), fail_create=False):
        self.definitions, self.world, self.technology = definitions, world, technology
        self.date, self.fail_create = date, fail_create
        self.creations, self.refreshes = [], []

    def cond(self, nodes, state=None, tag=None):
        return all(self.one(n,state,tag) for n in nodes)

    def one(self, n, state, tag):
        if n.key == 'NOT' or n.key == 'NOR':
            return not any(self.one(c,state,tag) for c in n.children())
        if n.key == 'owner':
            return self.cond(n.children(),state,state['tag'])
        if n.key == 'has_technology_researched':
            return scalar(n.value) in self.technology.get(tag,set())
        if n.key == 'has_variable':
            return scalar(n.value) in state['variables']
        if n.key == 'has_building':
            return scalar(n.value) in state['buildings']
        if n.key == 'is_coastal':
            return state['coastal'] == (n.value == 'yes')
        if n.key == 'state_region':
            return state['state'] == scalar(n.value).removeprefix('s:')
        if n.key == 'current_date':
            expected = tuple(map(int,scalar(n.value).split('.')))
            return {'>=':self.date>=expected,'<':self.date<expected}[n.op]
        raise ValueError('Unsupported start predicate: '+n.key)

    def effect(self, nodes, state=None, tag=None):
        for n in nodes:
            if n.key == 'limit':
                continue
            if n.key in self.definitions:
                assert n.value == 'yes'
                self.effect(self.definitions[n.key].children(),state,tag)
            elif n.key.startswith('c:'):
                country = n.key[2:]
                assert n.op == '?='
                if country in self.world:
                    self.effect(n.children(),None,country)
            elif n.key == 'every_scope_state':
                for s in self.world.get(tag,[]):
                    if self.cond(n.children('limit')[0].children(),s,tag):
                        self.effect(n.children(),s,tag)
            elif n.key == 'if':
                if self.cond(n.children('limit')[0].children(),state,tag):
                    self.effect(n.children(),state,tag)
            elif n.key == 'create_building':
                if self.fail_create:
                    continue
                kind = scalar(n.one('building'))
                assert kind not in state['buildings']
                state['buildings'][kind] = {'level':int(n.one('level')),
                    'pm':[scalar(c.value) for c in n.children('activate_production_methods')[0].children()],
                    'reserves':scalar(n.one('reserves'))}
                self.creations.append((tag,state['state'],kind))
            elif n.key == 'set_variable':
                state['variables'].add(scalar(n.value))
            elif n.key == 'owner':
                self.effect(n.children(),state,state['tag'])
            elif n.key in {'aor1776_refresh_fort_construction_state','aor1776_ensure_fort_construction_monitor'}:
                self.refreshes.append((n.key,tag,state['state']))
            else:
                raise ValueError('Unsupported start effect: '+n.key)

    def run(self, action):
        if self.cond(action.children('trigger')[0].children()):
            self.effect(action.children('effect')[0].children())


def main():
    baseline = json.loads((OUT/'BASELINE.json').read_text(encoding='utf-8'))
    old_audit = json.loads((ROOT/'outputs/01a149d5-1620-7bf2-bf90-7fa9bf443072/audit_forts_genie_1776/audit.json').read_text(encoding='utf-8'))
    state_audit = json.loads((OUT/'INITIAL_STATE_AUDIT.json').read_text(encoding='utf-8'))
    workbook = json.loads((OUT/'WORKBOOK_READ.json').read_text(encoding='utf-8'))
    wb_rows = {}
    for row in workbook['rows']:
        for key,value in row.items():
            if key.startswith('B') and key[1:].isdigit() and 6 <= int(key[1:]) <= 471:
                ix=key[1:]
                wb_rows[value] = (row['C'+ix]=='Oui',row['D'+ix]=='Oui')
    check('workbook.sha256',sha(Path(baseline['reference_workbook'])) == baseline['reference_workbook_sha256'])
    check('workbook.actual_rows',len(wb_rows)==466)
    owners,pairs,_ = own_inventory(ROOT,GAME)
    active = {tag for state,tag in pairs}
    check('workbook.active_country_set',set(wb_rows)==active)

    tech_audit.TAG_RE = re.compile(r'\bc:([A-Z0-9_]{3,})\s*\?=\s*\{')
    tiers = tech_audit.parse_tiers()
    overlay, names = tech_audit.country_overlay()
    techs = {}
    tech_rows = []
    evidence_rows = {r['tag']:r for r in old_audit['rows']}
    for tag in sorted(active):
        current = set()
        for filename in names[tag]:
            current |= tech_audit.parse_country_tech(overlay[filename][0],tiers,tag)[0]
        techs[tag] = current
        flags = (GATE in current, ENG in current)
        check('technology.'+tag, flags==wb_rows[tag])
        check('technology.independent_ast.'+tag, current==set(state_audit['technology_grants'].get(tag,[])))
        researched = next((e for e in PLAN['engineers'] if e['tag']==tag),None)
        tech_rows.append({'tag':tag,'pays':evidence_rows[tag]['pays'],
            'fort_tableur':int(wb_rows[tag][0]),'fort_mod_effectif':int(flags[0]),
            'genie_tableur':int(wb_rows[tag][1]),'genie_mod_effectif':int(flags[1]),
            'comparaison':'MATCH' if flags==wb_rows[tag] else 'MISMATCH',
            'preuve_fort':evidence_rows[tag]['sources_forts'],'preuve_genie':evidence_rows[tag]['sources_genie'],
            'recherche_historique':'A1 documenté' if researched else 'NOT_STARTED',
            'interpretation':'Technologie disponible ; aucune implantation automatique',
            'exception_a_etudier':'Lağımcı : recherche historique requise malgré absence du génie' if tag=='TUR' else ''})
    csv_file('TECHNOLOGY_CROSSCHECK.csv',tech_rows)

    buildings = get_defs('common/buildings')
    pms = get_defs('common/production_methods')
    regions = get_defs('map_data/state_regions')
    effects = {n.key:n for n in parse(read(EFFECTS))}
    actions = {n.key:n for n in parse(read(ACTIONS))}
    action = actions['aor1776_historical_forts_a1_initialize']
    check('syntax.new_scripts', bool(effects) and bool(actions))
    definitions = get_defs('common/scripted_effects')
    for n in walk(parse(read(EFFECTS))):
        if n.key.startswith('aor1776_') and n not in effects.values() and n.value=='yes':
            check('reference.'+n.key,n.key in definitions)
    for key in effects:
        occurrences = sum(n.key==key for p in effective('common/scripted_effects')
                          for n in parse(p.read_text(encoding='utf-8-sig')))
        check('unique_effect.'+key,occurrences==1)
    for hook in ['on_game_started','on_game_started_after_lobby']:
        check('hook.additive.'+hook,len(actions[hook].children())==1 and
              actions[hook].children()[0].key=='on_actions' and
              [n.value for n in actions[hook].children()[0].children()]==[action.key])
    check('hook.no_monthly_or_pulse',set(actions)=={'on_game_started','on_game_started_after_lobby',action.key})
    check('hook.country_dispatch',[(n.key,n.op,[c.key for c in n.children()]) for n in action.children('effect')[0].children()]==
          [('c:'+tag,'?=',[helper]) for tag,helper in HELPERS.items()])

    initial = starting_forts()
    state_rows = {(r['tag'],r['state']):r for r in state_audit['rows']}
    placements, before_after, inventory = [],[],[]
    selected = set()
    world = defaultdict(list)
    for (sid,tag),provinces in pairs.items():
        if tag not in HELPERS:
            continue
        row = state_rows.get((tag,sid))
        # Non-target state coastal flags cannot affect a selector, and are
        # deliberately unknown. Target flags come from actual raster adjacency.
        world[tag].append({'tag':tag,'state':sid,'coastal':row['is_coastal'] if row else None,
                          'variables':set(),'buildings':{kind:deepcopy(v) for (t,s,kind),v in initial.items() if (t,s)==(tag,sid)}})
    for p in PLAN['placements']:
        tag,sid = p['tag'],p['state']
        selected.add((tag,sid))
        check('placement.owned.'+p['id'],bool(pairs.get((sid,tag))))
        check('placement.region.'+p['id'],sid in regions)
        check('placement.technology.'+p['id'],GATE in techs[tag])
        check('placement.actual_coast.'+p['id'],p['coastal']==state_rows[tag,sid]['is_coastal'])
        kind = COAST if p['coastal'] else LAND
        pm = 'pm_naval_fortification_basic' if p['coastal'] else 'pm_aor1776_land_fortification_basic'
        check('placement.building.'+p['id'],kind in buildings and buildings[kind].children('potential')[0].one('is_coastal')==('yes' if p['coastal'] else 'no'))
        check('placement.pm.'+p['id'],pm in pms and not pms[pm].children('unlocking_technologies'))
        check('placement.gate.'+p['id'],[n.value for n in buildings[kind].children('unlocking_technologies')[0].children()]==[GATE])
        helper = effects[HELPERS[tag]]
        selectors = [n for n in helper.children('every_scope_state') if n.children('limit')[0].one('state_region')=='s:'+sid]
        target_helper = 'aor1776_historical_fort_a1_add_'+('coastal' if p['coastal'] else 'land')
        check('placement.selector.'+p['id'],len(selectors)==1 and [n.key for n in selectors[0].children() if n.key!='limit']==[target_helper])
        existing = [v for (t,s,k),v in initial.items() if (t,s)==(tag,sid)]
        check('placement.no_initial_duplicate.'+p['id'],not existing)
        placements.append({'id':p['id'],'lot':'A1','pays':evidence_rows[tag]['pays'],'tag':tag,'state_region':sid,
            'etat_affiche':p['label'],'subdivision_proprietaire':tag,'provinces_possedees':' '.join(pairs[sid,tag]),
            'coastal_reel':int(p['coastal']),'places_historiques':' ; '.join(p['sites']),
            'building':kind,'level':1,'pm':pm,'reserves':1,'sources':' ; '.join(p['sources']),
            'statut':'IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION','precision':'Bâtiment régional ; pas de placement à une province de citadelle'})
        before_after.append({'tag':tag,'state_region':sid,'building':kind,'avant_niveaux':sum(v['level'] for v in existing),
                             'apres_projection_niveaux':1,'pm_apres':pm,'autres_batiments':'Conservés ; aucun historique réécrit'})
        for site in p['sites']:
            construction,modernization,form,sovereign=PLAN['site_details'][site]
            inventory.append({'id':p['id']+'-'+str(len(inventory)+1),'lot':'A1','nom':site,'noms_alternatifs':'',
                'souverain_1776':sovereign,'localite':site,'construction':construction,'modernisation':modernization,
                'systeme':form,'etat_1776':'Actif ; continuité d’usage militaire retenue, pas une inspection de garnison datée du 1er janvier',
                'state_region':sid,'proprietaire_mod':tag,'niveau_propose':1,'groupe_placement':p['id'],
                'statut':'IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION','confiance':'Élevée pour le noyau antérieur à 1776 ; conversion régionale conventionnelle',
                'sources':' ; '.join(p['sources']),'decision':'Un seul niveau pour le réseau, même si plusieurs places partagent ce groupe'})
    check('placement.count',len(selected)==12 and len(placements)==12)
    check('placement.total_levels',sum(p['level'] for p in placements)==12)
    check('placement.type_counts',Counter(p['building'] for p in placements)=={LAND:5,COAST:7})
    actual_selectors = {(tag,scalar(n.children('limit')[0].one('state_region')).removeprefix('s:'))
                        for tag,key in HELPERS.items() for n in effects[key].children('every_scope_state')}
    check('placement.only_authorized_selectors',actual_selectors==selected)
    csv_file('FORTRESS_PLACEMENT.csv',placements)
    csv_file('BEFORE_AFTER.csv',before_after)

    # Actual AST projection: dates, duplicate callbacks, saved state markers,
    # failure to create, tech/coast denial and separate British/Spanish states.
    def project(label,date=(1776,1,1),alter=None,twice=False,fail=False):
        w=deepcopy(world); t=deepcopy(techs)
        if alter: alter(w,t)
        model=StartProjection(effects,w,t,date,fail)
        model.run(action)
        if twice: model.run(action)
        CASES.append({'case':label,'created':len(model.creations),'land':sum(k==LAND for _,_,k in model.creations),
                      'coastal':sum(k==COAST for _,_,k in model.creations)})
        return model
    first=project('new_start_both_callbacks',twice=True)
    check('projection.new_start',set(first.creations)=={(p['tag'],p['state'],COAST if p['coastal'] else LAND) for p in PLAN['placements']} and len(first.creations)==12)
    check('projection.construction_refresh',sum(k=='aor1776_refresh_fort_construction_state' for k,_,_ in first.refreshes)==5)
    for date in [(1775,12,31),(1776,1,2),(1780,1,1)]:
        check('projection.no_retroactive.'+str(date),not project('other_date_'+str(date),date).creations)
    def no_tech(w,t): t['FRA'].discard(GATE)
    check('projection.no_free_technology',len(project('France_without_gate',alter=no_tech).creations)==8)
    def wrong_coast(w,t):
        for s in w['FRA']:
            if s['state']=='STATE_ALSACE_LORRAINE': s['coastal']=True
    check('projection.wrong_coast_skip',len(project('inland_became_coastal',alter=wrong_coast).creations)==11)
    def upgraded(w,t):
        for s in w['FRA']:
            if s['state']=='STATE_ALSACE_LORRAINE': s['buildings'][LAND]={'level':4,'pm':['pm_aor1776_land_fortification_advanced'],'reserves':'0.42'}
    kept=project('existing_upgraded_fort',alter=upgraded,twice=True)
    check('projection.existing_preserved',len(kept.creations)==11 and next(s for s in kept.world['FRA'] if s['state']=='STATE_ALSACE_LORRAINE')['buildings'][LAND]=={'level':4,'pm':['pm_aor1776_land_fortification_advanced'],'reserves':'0.42'})
    def wrong_kind(w,t):
        for s in w['FRA']:
            if s['state']=='STATE_FRENCH_LOW_COUNTRIES': s['buildings'][LAND]={'level':2,'pm':['legacy'],'reserves':'0.5'}
    check('projection.no_two_fort_types',len(project('legacy_wrong_type_not_duplicated',alter=wrong_kind).creations)==11)
    check('projection.failed_creation_unmarked',all(not s['variables'] for ss in project('creation_failure',fail=True).world.values() for s in ss))
    reload_world=deepcopy(first.world)
    for s in reload_world['FRA']:
        if s['state']=='STATE_ALSACE_LORRAINE': s['buildings'].clear()
    loaded=StartProjection(effects,reload_world,techs)
    loaded.run(action)
    check('projection.demolition_not_respawned',not loaded.creations)
    check('projection.Gibraltar_not_Spain',('GBR','STATE_UPPER_ANDALUSIA',COAST) in first.creations and not any(t=='SPA' and s=='STATE_UPPER_ANDALUSIA' for t,s,k in first.creations))
    check('projection.Maastricht_omitted',not any(s=='STATE_GELRE' for t,s,k in first.creations))
    check('mapping.Gibraltar_province',pairs.get(('STATE_UPPER_ANDALUSIA','GBR'))==['xBC6ED3'])
    check('mapping.Maastricht_actual_owner',owners.get('x0000DF')==[('STATE_GELRE','BEO')])
    check('native.coastal_cap', 'state_building_naval_fortification_max_level_add = 5' in (GAME/'common/static_modifiers/00_code_static_modifiers.txt').read_text(encoding='utf-8-sig'))
    check('land.cap_technology',get_defs('common/technology/technologies')[GATE].children('modifier')[0].one('state_building_aor1776_land_fortification_max_level_add')=='5')

    # Reuse the existing restricted evaluator, without changing old tests or
    # their old full-workspace preservation baseline.
    battle_helpers = {n.key:n for n in parse(read(battle_build.TRIGFILE))}
    battle = Projection(battle_helpers)
    for level,pm_strength in [(1,1),(1,2),(1,3),(5,1),(5,2),(5,3)]:
        protection=5*level*pm_strength
        for engineers in [0,1,5,25,50,75,100]:
            unit=[('A','unit_type:combat_unit_type_aor1776_engineer_corps',1000)]*engineers
            side=sides(level*pm_strength,units=unit)
            net=battle.value('aor1776_land_fort_net_protection',side,[],side)
            check(f'battle.net.L{level}.PM{pm_strength}.E{engineers}',net==Decimal(max(0,protection-engineers)))
    for label,kwargs in [('no_fort',{'fort':False}),('coastal',{'coast':True}),('attacker',{'advancing':True}),('occupied',{'controller':'A'})]:
        side=sides(5,**kwargs)
        check('battle.ineligible.'+label,not battle.all(battle_helpers['aor1776_land_fortification_battle_eligible'].children(),side))
    for tag in ['D','F']:
        side=sides(5,units=[(tag,'unit_type:combat_unit_type_aor1776_engineer_corps',1000)]*25)
        check('battle.defensive_engineers_do_not_counter.'+tag,battle.value('aor1776_land_fort_net_protection',side,[],side)==25)
    side=sides(5,units=[('A','unit_type:combat_unit_type_cannon_artillery',1000)]*75)
    check('battle.ordinary_artillery_no_engineer_bonus',battle.value('aor1776_land_fort_net_protection',side,[],side)==25)
    side=sides(5,units=[('A','unit_type:combat_unit_type_aor1776_engineer_corps',500)]*10)
    check('battle.actual_strength',battle.value('aor1776_land_fort_net_protection',side,[],side)==20)

    # No specialist battalion is created by this lot. Absence of adequate
    # sizing evidence is not a claim that a historical service did not exist.
    engineer_rows=[]
    researched={e['tag']:e for e in PLAN['engineers']}
    priority={'FRA','GBR','SPA','POR','NET','PRU','AUS','SAX','RUS','SWE','BIC','TUR'}
    for tag in sorted({t for t in active if ENG in techs[t]} | priority):
        e=researched.get(tag,{})
        engineer_rows.append({'tag':tag,'pays':evidence_rows.get(tag,{}).get('pays',tag),
            'nom_historique':e.get('name','À rechercher — aucune organisation présumée'),
            'classe':e.get('class','UNRESEARCHED'),'creation':e.get('created','À rechercher'),
            'statut_1776':e.get('status','NOT_STARTED'),'effectif':e.get('strength','Non établi'),
            'repartition':e.get('territory','Non établie'),'technologie_genie':int(ENG in techs.get(tag,set())),
            'unites_proposees':e.get('units',''),'sources':' ; '.join(e.get('sources',[])),
            'decision':e.get('reason','Ne pas confondre technologie disponible et preuve historique ; recherche nécessaire')})
    csv_file('ENGINEER_CORPS_INVENTORY.csv',engineer_rows)
    csv_file('ENGINEER_DEPLOYMENT.csv',[{'tag':e['tag'],'formation_historique':e['name'],'classe':e['class'],
        'unites_ajoutees':0,'formation_jeu':'Aucune ajoutée','dimensionnement':e['strength'],
        'technologie_preservee':1,'justification':e['reason'],'sources':' ; '.join(e['sources'])} for e in PLAN['engineers']])
    check('engineers.no_start_units_added',not any(n.key in {'combat_unit','create_military_formation','add_technology_researched'} for n in walk(parse(read(EFFECTS)))))

    inventory.append({'id':'A-BLOCKED-MAASTRICHT','lot':'A2','nom':'Maastricht — Fort Sint Pieter','noms_alternatifs':'Maestricht',
        'souverain_1776':'Condominium République des Provinces-Unies / prince-évêque de Liège ; droit et commandement à préciser',
        'localite':'Maastricht','construction':'1701-1702','modernisation':'Avant 1776',
        'systeme':'Fort d’artillerie bastionné','etat_1776':'Fort actif attesté ; implantation suspendue',
        'state_region':'STATE_GELRE','proprietaire_mod':'BEO, province x0000DF','niveau_propose':'',
        'groupe_placement':'','statut':'BLOCKED','confiance':'Élevée sur le fort ; attribution politique et carte à réconcilier',
        'sources':'N02','decision':'Aucun fort chez NET ni BEO dans cette passe ; aucune compensation ailleurs'})
    for lot,countries in PLAN['pending'].items():
        for tag,sites in countries.items():
            for site in sites:
                inventory.append({'id':f'{lot}-PENDING-{len(inventory)+1:03}', 'lot':lot,'nom':site,
                    'noms_alternatifs':'','souverain_1776':'À vérifier ; tag indicatif : '+tag,
                    'localite':site,'construction':'À rechercher','modernisation':'À rechercher',
                    'systeme':'Candidat uniquement ; admissibilité non démontrée','etat_1776':'NOT_STARTED',
                    'state_region':'À cartographier','proprietaire_mod':'À vérifier','niveau_propose':'',
                    'groupe_placement':'','statut':'NOT_STARTED','confiance':'Non évaluée',
                    'sources':'','decision':'Aucune installation ; vérifier chronologie, propriétaire réel et côte'})
    for site,date in [('Goryōkaku','XIXe siècle'),('Hwaseong','À partir de 1794'),('Citadelles Nguyễn de type Vauban','XIXe siècle')]:
        inventory.append({'id':'E-EXCLUSION-'+str(len(inventory)+1),'lot':'E','nom':site,'noms_alternatifs':'',
            'souverain_1776':'Sans objet pour ces constructions postérieures','localite':site,
            'construction':date,'modernisation':'','systeme':'Exclusion chronologique du cahier de mission',
            'etat_1776':'Non construit sous cette forme','state_region':'Non implanté','proprietaire_mod':'',
            'niveau_propose':0,'groupe_placement':'','statut':'NOT_APPLICABLE_VERIFIED',
            'confiance':'Exclusion imposée par la mission ; pas une recherche régionale complète',
            'sources':'Cahier de mission, section Asie orientale','decision':'Ne pas utiliser pour justifier des niveaux en 1776'})
    csv_file('FORTRESS_INVENTORY.csv',inventory)
    json_file('START_PROJECTION_CASES.json',CASES)
    json_file('PREEXISTING_FORTS.json',[{'tag':tag,'state':sid,'building':kind,**v} for (tag,sid,kind),v in initial.items()])

    changed=[rel for rel,digest in baseline['files'].items() if not (ROOT/rel).is_file() or sha(ROOT/rel)!=digest]
    # The root task only creates new files. Keep independently observed
    # concurrent changes visible, rather than restoring them or claiming an
    # unchanged full workspace. Reviewed files outside this task can keep
    # evolving: report their current hashes without failing unrelated A1 work.
    external_path=OUT/'EXTERNAL_CHANGES.json'
    external=json.loads(external_path.read_text(encoding='utf-8')) if external_path.exists() else {}
    unexpected=[rel for rel in changed if rel not in external or not (ROOT/rel).is_file()]
    check('preservation.preexisting_files_except_reviewed_concurrent_changes',not unexpected,{'changed':changed,'unreviewed':unexpected})
    check('preservation.concurrent_files_not_owned',not set(external)&{EFFECTS,ACTIONS})
    check('preservation.git_index',sha(ROOT/'.git/index')==baseline['git_index_sha256'])
    if (OUT/'BASELINE_DOCS.json').exists():
        docs=json.loads((OUT/'BASELINE_DOCS.json').read_text(encoding='utf-8'))
        changed_docs=[rel for rel,digest in docs.items() if not (ROOT/rel).is_file() or sha(ROOT/rel)!=digest]
        unreviewed_docs=[rel for rel in changed_docs if rel not in external or not (ROOT/rel).is_file()]
        check('preservation.other_reports_except_reviewed_concurrent_changes',not unreviewed_docs,
              {'changed':changed_docs,'unreviewed':unreviewed_docs})
    for rel,record in external.items():
        record['current_sha256']=sha(ROOT/rel) if (ROOT/rel).is_file() else None
    runtime_files=[EFFECTS,ACTIONS]
    check('preservation.only_new_gameplay_files',all(rel not in baseline['files'] for rel in runtime_files))
    source_hashes={str(p):sha(p) for folder in ['common/buildings','common/building_groups','common/production_methods',
        'common/production_method_groups','common/technology/technologies','common/history/countries','common/history/states',
        'common/history/buildings','map_data/state_regions'] for p in effective(folder)}
    for rel in ['common/static_modifiers/00_code_static_modifiers.txt','map_data/default.map']:
        source_hashes[str(GAME/rel)]=sha(GAME/rel)
    json_file('SOURCE_HASHES.json',source_hashes)
    counts={'active_countries':len(active),'fort_technology':sum(GATE in ts for ts in techs.values()),
            'engineer_technology':sum(ENG in ts for ts in techs.values()),
            'both':sum(GATE in ts and ENG in ts for ts in techs.values()),
            'placements':len(placements),'land_levels':5,'coastal_levels':7,'engineer_units_added':0,
            'fort_inventory_rows':len(inventory),'engineer_inventory_rows':len(engineer_rows)}
    result={'mission':PLAN['mission'],'lot':'A1','generated_utc':datetime.now(timezone.utc).isoformat(),
        'status':'IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' if all(c['pass'] for c in CHECKS.values()) else 'STATIC_CHECK_FAILED',
        'historical_date':PLAN['historical_date'],'counts':counts,'checks_passed':sum(c['pass'] for c in CHECKS.values()),
        'checks_total':len(CHECKS),'checks':CHECKS,'runtime':'NOT_RUN','user_runtime_approval':False,
        'protected_files_count':len(baseline['files']),'concurrent_changes_preserved':external,
        'baseline_drift_files':changed,'new_gameplay_files':{rel:sha(ROOT/rel) for rel in runtime_files},
        'limitations':['Restricted AST projection, not engine execution','Historical research outside A1 is pending',
            'Coastal buildings retain naval-only mechanics; land engineer counter does not affect them',
            'Employment and prices require runtime observation','Maastricht mapping/sovereignty remains blocked']}
    json_file('VALIDATION.json',result)
    print(json.dumps({k:result[k] for k in ['status','counts','checks_passed','checks_total','runtime']},ensure_ascii=False,indent=2))
    failures={k:v for k,v in CHECKS.items() if not v['pass']}
    if failures:
        print(json.dumps(failures,ensure_ascii=False,indent=2))
        raise SystemExit(1)


if __name__=='__main__':
    main()
