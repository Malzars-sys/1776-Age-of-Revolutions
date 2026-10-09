"""Emit an apply_patch plan for approved early naval equipment; validate in place.

Never writes runtime files itself. Snapshots/QA previews go to ignored cache.
Historical loadouts are mod designs, not reconstructions of named vessels.
"""
import argparse
import collections
import difflib
import hashlib
import json
import re
import sys
from pathlib import Path

import audit_british_colonial_start as history
import build_start_1776_research_input_pack as catalog
import build_start_1776_world_apply as world
import recolour_pm_icons as colour
from integrate_naval_equipment_art import PROPULSION_ROWS, LOTS, localized_text

ROOT = Path(__file__).resolve().parents[1]
NATIVE = Path('C:/Games/Victoria 3/game')
CACHE = ROOT / '.asset-cache/early_ship_equipment_2026-10-08'
EARLY = 'common/ship_types/10_1776_early_ships.txt'
STANDARD = 'common/ship_types/00_ship_types.txt'
MODS = 'common/ship_modifications/10_1776_early_equipment.txt'
TECH = 'common/technology/technologies/26_1776_early_ship_construction.txt'
GRANTS = 'common/history/countries/99_1776_ship_construction_grants.txt'
DOC = 'docs/reports/naval/early_ship_equipment_integration_2026-10-08.md'
ADVANCED = {'FRA','GBR','SPA','RUS','POR','NET','DEN','NOR','DENNOR','SWE'}
PREFIX = 'gfx/interface/icons/military_icons/navy_icons/ship_designer_icons/'
HULL_TECH = {k:'aor_'+k+'_construction' for k in ('cog','galley','caravel','frigate','line_ship')}
CARR = 'aor_carronade_mountings'
DIAG = 'aor_diagonal_ship_framing'

# Each row: FR name, EN name, FR explanation, EN explanation.
# Numeric battery complements below are affordable game loadouts; they are NOT
# claimed as historical inventories of a particular ship called a caravel/cog.
ROWS = {
 'caravel': {
  'armor': [
   ('Bordage à franc-bord sur membrures','Carvel planking on frames','Planches jointives fixées sur les membrures : coque lisse, sans blindage métallique.','Flush planks fastened to frames: a smooth wooden hull, not metal armor.'),
   ('Couples doubles et serre-bauquières','Double frames and deck clamps','Couples doublés et longues pièces soutenant les baux : meilleure reprise des efforts du pont.','Paired frames and longitudinal deck clamps distribute deck loads.'),
   ('Charpente à renforts diagonaux','Diagonal timber bracing','Pièces diagonales contre la déformation longitudinale, inspirées des travaux de Seppings au XIXe siècle.','Diagonal timbers resist longitudinal distortion, inspired by nineteenth-century Seppings framing.')],
  'guns': [
   ('8 fauconneaux pivotants de 2 livres','8 two-pounder swivel falconets','Petits tubes sur fourches pivotantes pour la défense rapprochée. Les livres désignent le poids du boulet.','Small swivel-mounted barrels for close defense. Pounds refer to shot weight.'),
   ('12 canons longs de 6 livres sur affûts à roulettes','12 six-pounder long guns on truck carriages','Canons à âme lisse chargés par la bouche, avec affûts de pont et recul contrôlé par bragues.','Muzzle-loading smoothbores on deck truck carriages with breeching ropes.'),
   ('8 carronades de 12 livres sur glissières','8 twelve-pounder carronades on slides','Tubes courts à large bouche, montés sur glissières : puissance à courte distance, technologie postérieure au départ de 1776.','Short broad-muzzled barrels on slides: close-range firepower, a technology later than the 1776 start.')],
  'propulsion': [
   *PROPULSION_ROWS],
  'range': [
   ('Tonneaux de vivres en cale','Provisions in hold casks','Vivres et eau stockés dans la cale existante.','Food and water casks stowed in the existing hold.'),
   ('Gaillard arrière et cambuse séparée','Quarterdeck and separate provision store','Pont arrière et réserve de vivres distincte des autres charges.','An aft deck and a provision compartment separate from other cargo.'),
   ('Faux-pont de campagne et soutes à eau','Campaign platform deck and water stores','Plateforme intérieure réservée aux provisions et rangement structuré des tonneaux d’eau.','An internal provision platform and organized water-cask stowage.')]
 },
 'galley': {
  'armor': [
   ('Bordage léger à franc-bord','Light carvel planking','Coque étroite sur membrures, conçue pour la nage et le cabotage.','A narrow framed hull built for rowing and coastal service.'),
   ('Serres longitudinales et traverses de nage','Longitudinal stringers and rowing crossbeams','Longues pièces de charpente et traverses reprenant l’effort des bancs de nage.','Longitudinal timbers and crossbeams carry rowing-bank loads.'),
   ('Quille doublée et carlingue continue','Doubled keel and continuous keelson','Renfort de la quille et poutre intérieure continue : rigidité accrue sans blindage en fer.','Keel reinforcement and a continuous internal beam improve stiffness without iron armor.')],
  'guns': [
   ('1 pièce de proue de 6 livres et 2 pierriers','One six-pounder bow gun and 2 swivels','Une pièce axiale légère, complétée par deux petites armes pivotantes pour l’abordage.','A light axial gun and two small swivel pieces support boarding.'),
   ('1 canon de chasse de 12 livres et 2 canons de 3 livres','One twelve-pounder bow chaser and 2 three-pounders','Canon axial sur affût de proue, accompagné de deux pièces plus petites.','An axial bow-carriage gun accompanied by two smaller pieces.'),
   ('1 canon axial de 24 livres et 2 canons de 6 livres','One twenty-four-pounder axial gun and 2 six-pounders','Batterie concentrée à l’avant, avec affût guidé dans l’axe du navire ; elle ne transforme pas la galère en vaisseau de ligne.','A forward battery with an axial guided gun carriage; it does not turn the galley into a ship of the line.')],
  'propulsion': [
   ('Nage alla sensile : avirons séparés','Alla sensile rowing: separate oars','Plusieurs rameurs par banc, chacun maniant son propre aviron.','Several rowers share a bench, each handling a separate oar.'),
   ('Nage a scaloccio : aviron collectif','A scaloccio rowing: shared sweep','Un grand aviron manœuvré ensemble par plusieurs rameurs.','A large sweep is worked by several rowers together.'),
   ('Nage a scaloccio et deux voiles latines','A scaloccio rowing with two lateen sails','Avirons collectifs complétés par deux mâts à antennes ; aucun moteur.','Shared sweeps supplemented by two lateen-rigged masts; no engine.')],
  'range': [
   ('Coffres de banc et outres d’eau','Bench lockers and water skins','Réserves compactes pour les sorties côtières.','Compact provisions for coastal sorties.'),
   ('Tonneaux sous coursie','Casks beneath the gangway','Rangement de tonneaux sous le passage central reliant proue et poupe.','Casks stowed beneath the central fore-and-aft gangway.'),
   ('Cambuse de poupe et avirons de rechange','Stern provision store and spare oars','Magasin arrière organisé et réserve d’avirons. La portée côtière reste limitée à 1.','An organized stern store and spare sweeps. The coastal distance limit remains 1.')]
 },
 'cog': {
  'armor': [
   ('Bordage à clins riveté','Riveted clinker planking','Planches superposées et fixées par rivets, sur la coque traditionnelle de la cogue.','Overlapping riveted planks form a traditional cog hull.'),
   ('Varangues liées à une carlingue','Floors tied into a keelson','Liaisons structurelles entre le fond et une poutre intérieure dans l’axe de la quille.','Structural ties join the hull bottom to an internal keel-aligned beam.'),
   ('Serres de cale et baux traversants','Hold stringers and through-beams','Longerons intérieurs et baux transversaux reprennent les charges du transport militaire.','Internal longitudinal stringers and transverse beams carry military cargo loads.')],
  'guns': [
   ('4 pierriers pivotants de 1 livre','4 one-pounder swivel guns','Petites armes sur le plat-bord : défense de l’équipage, pas une batterie de combat.','Small rail-mounted pieces protect the crew; this is not a battle battery.'),
   ('4 canons longs de 3 livres','4 three-pounder long guns','Pièces légères sur affûts de pont pour protéger le transport.','Light truck-carriage guns defend the transport.'),
   ('4 carronades de 6 livres','4 six-pounder carronades','Pièces courtes défensives ; adaptation tardive et volontairement limitée d’un transport ancien.','Short defensive pieces: a deliberately limited later refit of an older transport.')],
  'propulsion': [
   ('Mât unique et voile carrée','Single mast and square sail','Le gréement traditionnel de la cogue, à un seul mât.','The traditional single-masted square-sail cog rig.'),
   ('Voile carrée à bandes de ris','Square sail with reef bands','Bandes de ris permettant de réduire la toile plus proprement selon le vent.','Reef bands allow controlled sail-area reduction as winds change.'),
   ('Grand-voile carrée et hunier','Square mainsail with topsail','Ajout d’une voile au-dessus de la grand-voile : adaptation à voile tardive, sans machine.','A sail above the mainsail is a later sailing refit, not machinery.')],
  'range': [
   ('Cale libre et logements sur le pont','Open hold and deck accommodation','Transport rudimentaire dans la cale et sur le pont existants.','Basic transport in the existing hold and on deck.'),
   ('Faux-pont de couchettes et râteliers','Berth platform deck and equipment racks','Couchettes sur plateforme intérieure et équipements arrimés séparément.','Berths on an internal platform, with equipment secured separately.'),
   ('Pont de troupes et panneaux de chargement','Troop deck and cargo hatchways','Pont adapté aux soldats et ouvertures de chargement organisées ; priorité au transport.','A dedicated troop deck and organized loading openings prioritize transport.')]
 }
}

def numbers(kind,slot,index):
    if slot=='armor':
        hp={'caravel':[0,70,160],'galley':[0,100,220],'cog':[0,80,180]}[kind][index]
        return {'ship_hit_points_max_add':hp,'ship_armor_add':[0,1,3][index]}, {'hardwood':[0,4,8][index],'tools':[0,0.5,1][index]}
    if slot=='guns':
        hull={'caravel':[0,6,9],'galley':[0,5,8],'cog':[0,1,2]}[kind][index]
        crew={'caravel':[0,3,5],'galley':[0,2,4],'cog':[0,1,2]}[kind][index]
        # Small transport guns do not demand the same goods as a capital battery.
        scale=0.5 if kind=='cog' else 1
        return {'ship_hull_damage_add':hull,'ship_crew_damage_add':crew}, {'iron':[0,1,2][index]*scale,'artillery':[0,0.5,1][index]*scale}
    if slot=='propulsion':
        speed=([0,0.2,0.4] if kind=='galley' else [0,0.4,0.8])[index]
        modifier={'ship_movement_speed_add':speed}
        if kind=='galley': modifier['ship_crew_max_add']=[0,10,20][index]
        return modifier, {'fabric':[0,2,4][index],'hardwood':[0,1,2][index]}
    if kind=='cog':
        return {'ship_carrying_capacity_add':[0,0.15,0.3][index],'ship_supply_capacity_add':[0,5,10][index]}, {'hardwood':[0,2,4][index],'fabric':[0,1,2][index]}
    return {'ship_supply_capacity_add':([0,4,8] if kind=='galley' else [0,8,18])[index]}, {'hardwood':[0,2,4][index],'fabric':[0,1,2][index]}

def equipment_gate(kind,slot,index):
    if not index: return HULL_TECH[kind]
    if slot=='guns':
        return CARR if index==2 and kind!='galley' else 'armament_standardization_inspection'
    if slot=='armor' and kind=='caravel' and index==2: return DIAG
    return 'scientific_naval_architecture' if index==2 else 'enclosed_dock_systems'

def equipment():
    out=[]
    for kind,slots in ROWS.items():
        for slot,rows in slots.items():
            for i,(fr,en,fr_desc,en_desc) in enumerate(rows):
                modifier,goods=numbers(kind,slot,i)
                level=('low','mid','high')[i]
                out.append(dict(key=f'aor_{kind}_{slot}_{level}',kind=kind,slot='ship_mod_slot_'+slot,icon=PREFIX+f'ship_designer_{slot}_{level}.dds',
                    fr=fr,en=en,fr_desc=fr_desc,en_desc=en_desc,modifier=modifier,goods=goods,gate=equipment_gate(kind,slot,i),level=i+1))
    utilities=[
      ('aor_landing_launches','cog','Chaloupes de débarquement','Landing launches','Chaloupes à avirons pour relier le transport à la côte.','Oared launches connect the transport to the shore.',
       {'ship_naval_invasion_efficiency_mult':0.1,'ship_marine_capacity_add':0.1},{'hardwood':4,'fabric':1},'marine_capacity'),
      ('aor_caravel_blockade','caravel','Organisation de blocus','Blockade organization','Bordées de veille, signaux et contrôle des approches portuaires.','Watch parties, signals and control of port approaches.',
       {'ship_blockade_strength_mult':0.35},{'hardwood':2,'fabric':1},'supplies_navy'),
      ('aor_caravel_landing','caravel','Chaloupes et détachement de débarquement','Launches and landing detachment','Chaloupes et place réservée aux soldats, cumulables avec l’organisation de blocus.','Launches and troop space, compatible with blockade organization.',
       {'ship_marine_capacity_add':0.1,'ship_naval_invasion_efficiency_mult':0.1,'ship_supply_capacity_add':-2},{'hardwood':4,'fabric':1},'marine_capacity'),
      ('aor_galley_coastal_battery','galley','Batterie de combat côtier','Coastal fighting battery','Service de la batterie avant pour le combat près des ports. La pénalité hors de portée est conservée.','Forward-battery drills for fighting near ports. The out-of-range penalty remains.',
       {'ship_hull_damage_mult':0.15,'ship_accuracy_add':1},{'iron':1,'tools':0.5},'average_damage_navy'),
      ('aor_galley_boarding_spur','galley','Éperon d’étrave pour l’abordage','Bow boarding spur','Saillie d’étrave au-dessus de l’eau pour approcher et aborder ; ce n’est pas un bélier blindé moderne.','An above-water bow spur helps close and board, not a modern armored ram.',
       {'ship_crew_damage_mult':0.2,'ship_marine_capacity_add':0.05,'ship_movement_speed_add':-0.1},{'hardwood':3,'iron':0.5},'marine_capacity')]
    for key,kind,fr,en,fd,ed,mods,goods,glyph in utilities:
        out.append(dict(key=key,kind=kind,slot='ship_mod_slot_utility_1',icon=f'gfx/interface/icons/military_icons/navy_icons/{glyph}.dds',
                        fr=fr,en=en,fr_desc=fd,en_desc=ed,modifier=mods,goods=goods,gate=HULL_TECH[kind],level=1))
    return out

TECHS = {
 HULL_TECH['cog']:('Construction maritime à clins','Clinker ship construction',1,[], 'drydock'),
 HULL_TECH['galley']:('Construction de galères','Galley construction',1,[], 'admiralty'),
 HULL_TECH['caravel']:('Gréements océaniques','Ocean-going rigs',1,[HULL_TECH['cog']], 'naval_theory'),
 HULL_TECH['frigate']:('Construction de frégates','Frigate construction',2,[HULL_TECH['caravel'],'scientific_naval_architecture'], 'floating_harbor'),
 HULL_TECH['line_ship']:('Construction de vaisseaux de ligne','Ships-of-the-line construction',3,[HULL_TECH['frigate'],'ship_classification_surveying'], 'admiralty'),
 CARR:('Carronades sur glissières','Slide-mounted carronades',4,[HULL_TECH['frigate'],'armament_standardization_inspection'], 'cannon_artillery'),
 DIAG:('Charpente navale diagonale','Diagonal naval framing',5,[HULL_TECH['line_ship']], 'drydock')
}

def block(values,indent=4):
    pad=' '*indent
    return '\n'.join(f'{pad}{key} = {value:g}' for key,value in values.items())

def mod_text():
    parts=['# Approved early hull equipment; no engines, coal, shells or modern armor.\n# Default low levels add no cost; optional utilities are intentionally inexpensive.\n']
    for row in equipment():
        goods={f'goods_input_{key}_add':n for key,n in row['goods'].items() if n}
        parts.append(f"{row['key']} = {{\n    type = {row['slot']}\n    icon = \"{row['icon']}\"\n    modifier = {{\n{block(row['modifier'],8)}\n    }}\n    construction_goods = {{\n{block(goods,8)}\n    }}\n    unlocking_technologies = {{ {row['gate']} }}\n    ai_weight = {{\n        value = {row['level']}\n        multiply = ship_mod_market_multiplier\n    }}\n}}\n")
    return '\n'.join(parts)

def tech_text():
    parts=['# Dedicated hull gates: do not remove shared naval science from other countries.\n# Carronades/framing are later refits, not default 1776 equipment.\n']
    for key,(_,_,era,requirements,icon) in TECHS.items():
        texture=f'gfx/interface/icons/invention_icons/{icon}.dds'
        if not (NATIVE/texture).exists() and not (ROOT/texture).exists():
            texture='gfx/interface/icons/invention_icons/admiralty.dds'
        prereqs='\n    unlocking_technologies = { '+ ' '.join(requirements)+' }' if requirements else ''
        parts.append(f'{key} = {{\n    era = era_{era}\n    category = military\n    texture = "{texture}"{prereqs}\n    ai_weight = {{\n        value = 1\n        if = {{\n            limit = {{ navy_size >= 1 }}\n            add = 1\n        }}\n    }}\n}}\n')
    return '\n'.join(parts)

def localization(language):
    french=language=='french';parts=['\ufeffl_'+language+':']
    for row in equipment():
        name=row['fr' if french else 'en'];desc=row['fr_desc' if french else 'en_desc']
        parts += [f' {row["key"]}: "{name}"',f' {row["key"]}_desc: "{desc}"']
    for key,(fr,en,_,_,_) in TECHS.items():
        name=fr if french else en
        if key==CARR:
            desc='Pièces courtes sur glissières, pour les adaptations tardives à courte portée.' if french else 'Short slide-mounted pieces for later close-range refits.'
        elif key==DIAG:
            desc='Renforts diagonaux en bois contre la déformation de la coque.' if french else 'Diagonal wooden braces resist hull distortion.'
        else:
            desc='Débloque la construction de la coque correspondante et ses équipements de base.' if french else 'Unlocks the corresponding hull and its basic equipment.'
        parts += [f' {key}: "{name}"',f' {key}_desc: "{desc}"']
    return '\n'.join(parts)+'\n'

def configured_early(raw):
    raw=raw.replace('# Economical pre-industrial hulls; equipment and technology gates are proposed separately.',
                    '# Economical pre-industrial hulls with approved, period-specific equipment.')
    raw=raw.replace('# No modern retrofit slots or hidden modification upkeep in these baseline hulls.',
                    '# Four native equipment slots; compatible utility slots; no modern engines or armor.')
    rows=equipment()
    for kind in ROWS:
        pattern=rf'(?ms)^ship_type_{kind} = \{{.*?^\}}'
        def replace(match):
            text=match.group().replace('    use_modifications = no','    use_modifications = yes\n    modification_construction_cost = 0.5')
            lines=[f'    unlocking_technologies = {{ {HULL_TECH[kind]} }}','    modifications = {']
            for slot in ROWS[kind]:
                lines += [f'        ship_mod_slot_{slot} = {{']
                lines += ['            '+row['key'] for row in rows if row['kind']==kind and row['slot']=='ship_mod_slot_'+slot]
                lines += ['        }']
            utilities=[r for r in rows if r['kind']==kind and r['slot'].startswith('ship_mod_slot_utility')]
            for index,row in enumerate(utilities,1):
                lines += [f'        ship_mod_slot_utility_{index} = {{ {row["key"]} }}']
            lines += ['    }','    default_modifications = {']
            for slot in ROWS[kind]: lines += [f'        ship_mod_slot_{slot} = aor_{kind}_{slot}_low']
            for index,row in enumerate(utilities,1): lines += [f'        ship_mod_slot_utility_{index} = {row["key"]}']
            lines += ['    }']
            return text[:-1]+'\n'+'\n'.join(lines)+'\n}'
        raw,n=re.subn(pattern,replace,raw);assert n==1
    return raw

def configured_standard(raw):
    def replace(match):
        text=match.group();kind='line_ship' if text.startswith('ship_type_ship_of_the_line') else 'frigate'
        gate=f'    unlocking_technologies = {{ {HULL_TECH[kind]} }}'
        if re.search(r'^\s*unlocking_technologies =',text,re.M):
            text=re.sub(r'^    unlocking_technologies = \{[^}]*\}',gate,text,count=1,flags=re.M)
        else: text=text.replace('    profile_texture =',gate+'\n\n    profile_texture =',1)
        return text
    return re.sub(r'(?ms)^ship_type_(?:ship_of_the_line|frigate) = \{.*?^\}',replace,raw)

def runtime_plan():
    before={path.relative_to(ROOT).as_posix():path.read_text(encoding='utf-8-sig')
            for path in (ROOT/'common/history/military_formations').glob('*.txt')}
    fleets=history.fleets(before);by_country=collections.defaultdict(set)
    for fleet in fleets:
        for kind,n in fleet['ships']:
            if n: by_country[fleet['owner']].add(kind)
    tech_before=history.technology_sets()
    existing=catalog.effective_objects('common/technology/technologies',r'[A-Za-z0-9_]+')
    graph={key: set(catalog.tokens_flat(catalog.braced_tokens(obj.text,'unlocking_technologies'))) for key,obj in existing.items()}
    graph.update({key:set(values[3]) for key,values in TECHS.items()})
    def closure(key,seen=None):
        seen=set() if seen is None else seen
        if key in seen:return set()
        return {key}|set().union(*(closure(p,seen|{key}) for p in graph.get(key,set())))
    grants={}
    for tag,kinds in by_country.items():
        # Existing fleets require primitive hulls. Existing navies get all three
        # cheap forms, preserving their ability to build a cheap troop carrier.
        grant=set().union(*(closure(HULL_TECH[k]) for k in ('cog','galley','caravel')))
        if tag in ADVANCED:grant|=closure(HULL_TECH['line_ship'])
        grants[tag]=sorted(grant-tech_before.get(tag,set()))
    for tag in ADVANCED:
        grants[tag]=sorted((set(grants.get(tag,[]))|closure(HULL_TECH['line_ship'])|closure(HULL_TECH['galley']))-tech_before.get(tag,set()))
    # Countries with dockyard institutions but no starting navy receive early
    # hull knowledge, not advanced hull gates. No later refit technology is granted.
    for tag,known in tech_before.items():
        if tag not in grants and 'state_dockyard_systems' in known:
            grants[tag]=sorted(set().union(*(closure(HULL_TECH[k]) for k in ('cog','galley','caravel')))-known)
    grant_text=['# Approved initial naval construction grants; advanced hulls only for the whitelist.','COUNTRIES = {']
    for tag,keys in sorted(grants.items()):
        grant_text += [f'    c:{tag} ?= {{']+['        add_technology_researched = '+key for key in keys]+['    }']
    grant_text+=['}']
    expected={EARLY:configured_early((ROOT/EARLY).read_text(encoding='utf-8-sig')),
              STANDARD:configured_standard((ROOT/STANDARD).read_text(encoding='utf-8-sig')),
              MODS:mod_text(),TECH:tech_text(),GRANTS:'\n'.join(grant_text)+'\n'}
    for lang in ('french','english'):expected[f'localization/{lang}/1776_early_ship_equipment_l_{lang}.yml']=localization(lang)
    converted=[]
    for path,raw in before.items():
        updates=[]
        for owner,a,b in history.country_spans(raw):
            tag=owner.split()[0].removeprefix('c:')
            if tag in ADVANCED: continue
            old=raw[a:b]
            replacement=old.replace('ship_type:ship_type_frigate','ship_type:ship_type_galley').replace('ship_type:ship_type_ship_of_the_line','ship_type:ship_type_caravel')
            if old!=replacement:
                updates.append((a,b,replacement));converted.append(tag)
        for a,b,text in reversed(updates):raw=raw[:a]+text+raw[b:]
        if updates:expected[path]=raw
    return expected,grants,sorted(set(converted)),fleets

def prepare():
    CACHE.mkdir(parents=True,exist_ok=True)
    target=CACHE/'equipment_baseline.json'
    assert not target.exists(),'Never overwrite the before-state'
    expected,grants,converted,fleets=runtime_plan()
    before={p:(ROOT/p).read_text(encoding='utf-8-sig') if (ROOT/p).exists() else None for p in expected}
    # Localization BOM is restored by the emitted full-file add; existing files
    # only get narrow hunks. No source file is written by this planner.
    state=dict(runtime=colour.runtime_hashes(),before=before,expected=expected,grants=grants,
               converted=converted,fleets=fleets,tech_before={k:sorted(v) for k,v in history.technology_sets().items()})
    target.write_text(json.dumps(state,indent=2,ensure_ascii=False),encoding='utf-8')
    emit(state)

def emit(state=None):
    if state is None:
        state=json.loads((CACHE/'equipment_baseline.json').read_text(encoding='utf-8'))
    expected=state['expected'];before=state['before']
    sys.stdout.reconfigure(encoding='utf-8')
    parts=['*** Begin Patch']
    for path,new in expected.items():
        old=before[path]
        if old is None:parts += [f'*** Add File: {path}']+['+'+line for line in new.splitlines()]
        elif old!=new:
            patch=history.patch_file(path,old,new).rstrip('\n');parts.append(patch)
    parts+=['*** End Patch']
    print('\n'.join(parts))

def approved_art_bindings():
    """Whitelist approved lots, without relaxing any gameplay check."""
    from integrate_naval_equipment_art import LOTS
    result={}
    registry=json.loads((ROOT/'docs/reports/assets/source_registry.json').read_text())['entries']
    for lot,config in LOTS.items():
        path=ROOT/f'docs/reports/assets/naval_equipment_{lot}_sources_{config.get("date","2026-10-08")}/manifest.json'
        if not path.exists():continue
        manifest=json.loads(path.read_text(encoding='utf-8'))
        assert manifest['status']=='APPROVED_AND_INTEGRATED'
        assert manifest['approval']==config['approval']
        expected=set(sum(config['bindings'],[])) if config.get('bindings') else {f'aor_{config.get("ship","caravel")}_{config["slot"]}_{level}' for level in ('low','mid','high')}
        seen=set()
        for entry in manifest['entries']:
            bindings=entry['ship_modification_bindings']
            assert bindings and set(bindings)<=expected
            assert entry['dds'].startswith(PREFIX+'1776_')
            assert entry in registry
            for field,hash_field in [('source','source_sha256'),('dds','dds_sha256')]:
                assert hashlib.sha256((ROOT/entry[field]).read_bytes()).hexdigest()==entry[hash_field]
            for key in bindings:
                assert key not in result
                result[key]=entry['dds'];seen.add(key)
        assert seen==expected
    return result

def check():
    state=json.loads((CACHE/'equipment_baseline.json').read_text(encoding='utf-8'))
    art=approved_art_bindings()
    runtime=colour.runtime_hashes();allowed=set(state['expected'])|set(art.values())
    assert not [p for p in set(runtime)|set(state['runtime']) if p not in allowed and runtime.get(p)!=state['runtime'].get(p)],'Unrelated runtime change'
    for path,expected in state['expected'].items():
        if path.startswith('localization/'):
            for lot,config in LOTS.items():
                manifest_path=ROOT/f'docs/reports/assets/naval_equipment_{lot}_sources_2026-10-08/manifest.json'
                if config.get('text_rows') and manifest_path.exists():
                    manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
                    assert manifest.get('localization_rows')==[list(row) for row in config['text_rows']]
                    expected=localized_text(expected,path.split('/')[1],lot)
        if path==MODS:
            for key,icon in art.items():
                pattern=rf'(?m)(^{key} = \{{\n    type = ship_mod_slot_[a-z0-9_]+\n    icon = ")[^"]+("\n)'
                expected,count=re.subn(pattern,lambda m:m[1]+icon+m[2],expected)
                assert count==1
        actual=(ROOT/path).read_text(encoding='utf-8-sig')
        assert actual==expected.lstrip('\ufeff'),f'Unexpected content: {path}'
        if path.endswith('.txt'):
            cleaned=catalog.clean_comments(actual)
            depths,pairs=catalog.brace_maps(cleaned)
            assert len(pairs)>0,path
        else:
            assert (ROOT/path).read_bytes().startswith(b'\xef\xbb\xbf'),f'Localization BOM: {path}'
            for line in actual.splitlines()[1:]:
                assert re.fullmatch(r' [a-z0-9_]+: "[^"\n]*"',line),f'Localization syntax: {path}/{line}'
    definitions=catalog.effective_objects('common/ship_modifications',r'[A-Za-z0-9_]+')
    hulls=catalog.effective_objects('common/ship_types',r'ship_type_[A-Za-z0-9_]+')
    tech=catalog.effective_objects('common/technology/technologies',r'[A-Za-z0-9_]+')
    # Ship modifier parameters are engine-defined, not a modifier_types database.
    # Require every parameter to be demonstrated in the native ship definitions.
    modifiers=set()
    for folder in ('ship_types','ship_modifications'):
        for path in (NATIVE/'common'/folder).glob('*.txt'):
            modifiers.update(re.findall(r'\b(ship_[a-z0-9_]+)\s*=',catalog.clean_comments(path.read_text(encoding='utf-8-sig'))))
    for row in equipment():
        assert row['key'] in definitions
        assert row['gate'] in tech,row['gate']
        assert (ROOT/row['icon']).exists() or (NATIVE/row['icon']).exists(),row['icon']
        for name in row['modifier']:assert name in modifiers,name
    # Validate all seven nodes, their icons, era ordering and graph reachability.
    graph={key:set(catalog.tokens_flat(catalog.braced_tokens(obj.text,'unlocking_technologies'))) for key,obj in tech.items()}
    def visit(key,stack):
        assert key in graph,f'Unknown prerequisite: {key}'
        assert key not in stack,f'Technology cycle: {stack}/{key}'
        for prereq in graph[key]:visit(prereq,stack+[key])
    for key,(_,_,era,prereqs,_) in TECHS.items():
        visit(key,[])
        assert set(prereqs)==graph[key]
        assert catalog.scalar(tech[key].text,'era')==f'era_{era}'
        texture=catalog.scalar(tech[key].text,'texture')
        assert (ROOT/texture).exists() or (NATIVE/texture).exists(),texture
        for prereq in prereqs:
            parent=catalog.scalar(tech[prereq].text,'era')
            assert int(parent.removeprefix('era_'))<=era,(key,prereq)
    known=history.technology_sets()
    advanced_holders={tag for tag,keys in known.items() if HULL_TECH['frigate'] in keys or HULL_TECH['line_ship'] in keys}
    assert advanced_holders==ADVANCED,(advanced_holders,ADVANCED)
    assert not any(CARR in keys or DIAG in keys for keys in known.values()),'Future equipment granted at start'
    # Check every added technology's conjunction at the technology graph, rather
    # than mistakenly encoding conjunction in ship-type unlocking lists (OR).
    for tag,keys in state['grants'].items():
        for key in keys:
            requirements=TECHS[key][3] if key in TECHS else catalog.tokens_flat(catalog.braced_tokens(tech[key].text,'unlocking_technologies'))
            assert set(requirements)<=known[tag],f'Missing prerequisite {tag}/{key}'
    for kind in ROWS:
        text=hulls['ship_type_'+kind].text
        assert catalog.scalar(text,'use_modifications')=='yes'
        for slot in ROWS[kind]:
            match=re.search(rf'(?m)^        ship_mod_slot_{slot} = \{{',text)
            assert match
            opening=text.find('{',match.start(),match.end());_,pairs=catalog.brace_maps(text)
            keys=text[opening+1:pairs[opening]].split()
            assert keys==[f'aor_{kind}_{slot}_{level}' for level in ('low','mid','high')],(kind,slot,keys)
            assert f'ship_mod_slot_{slot} = aor_{kind}_{slot}_low' in text,'Non-economical default'
        utility_rows=[r for r in equipment() if r['kind']==kind and r['slot']=='ship_mod_slot_utility_1']
        for index,row in enumerate(utility_rows,1):
            assert f'ship_mod_slot_utility_{index} = {{ {row["key"]} }}' in text
            assert f'ship_mod_slot_utility_{index} = {row["key"]}' in text
            assert 'incompatible_with' not in definitions[row['key']].text
        # Base stats and running supplies are unchanged; added goods are visible
        # construction/refit costs only, never hidden coal/motor upkeep.
        old=state['before'][EARLY]
        match=re.search(rf'(?ms)^ship_type_{kind} = \{{.*?^\}}',old)
        for name in ('ship_hit_points_max_add','ship_crew_max_add','ship_hull_damage_add','ship_armor_add'):
            assert catalog.scalar(text,name)==catalog.scalar(match.group(),name)
        assert catalog.braced_tokens(text,'materiel_goods')==catalog.braced_tokens(match.group(),'materiel_goods')
    galley=hulls['ship_type_galley'].text
    assert 'ship_max_distance_to_port_add = 1' in galley and galley.count('ship_hull_damage_mult = -0.8')==1
    for row in equipment():
        assert not {'coal','engines','steel','ammunition'}&row['goods'].keys()
        assert 'ship_max_distance_to_port_add' not in row['modifier']
    for lang in ('french','english'):
        loc=catalog.localizations(lang)
        for key in [r['key'] for r in equipment()]+list(TECHS):
            assert key in loc and key+'_desc' in loc,(lang,key)
    raws={p.relative_to(ROOT).as_posix():p.read_text(encoding='utf-8-sig') for p in (ROOT/'common/history/military_formations').glob('*.txt')}
    now=history.fleets(raws)
    identity=lambda row:(row['path'],row['owner'],row['name'])
    assert len(now)==len(state['fleets'])
    for old,new in zip(state['fleets'],now):
        assert identity(old)==identity(new)
        assert sum(n for _,n in old['ships'])==sum(n for _,n in new['ships'])
        if new['owner'] in ADVANCED:assert old['ships']==[list(row) for row in new['ships']]
        else:assert not any(k in ('ship_type_frigate','ship_type_ship_of_the_line') and n for k,n in new['ships'])
        for key,n in new['ships']:
            if n:
                gates=set(catalog.tokens_flat(catalog.braced_tokens(hulls[key].text,'unlocking_technologies')))
                assert not gates or gates&known[new['owner']],f'Illegal initial hull {new["owner"]}/{key}'
    report=dict(status='PASS_STATIC_EARLY_EQUIPMENT',equipment_definitions=len(equipment()),required_choices=36,selected_utilities=5,
                new_technologies=len(TECHS),advanced_initial_tags=sorted(advanced_holders),converted_initial_fleet_tags=state['converted'],
                fleets_checked=len(now),all_fleet_counts_preserved=True,advanced_fleets_preserved=True,
                coastal_constraint_preserved=True,no_motorization=True,
                graphics_status='ALL_EARLY_NAVAL_EQUIPMENT_AND_FUNCTION_ART_APPROVED' if len(art)==len(equipment()) else f'{len(art)}_APPROVED_EQUIPMENT_GLYPHS_ACTIVE_OTHER_ART_PENDING' if art else 'NATIVE_GLYPHS_ACTIVE_NEW_ART_PREVIEW_PENDING',
                approved_art_bindings=len(art),approved_unique_artworks=len(set(art.values())),
                pending_art_bindings=sorted({row['key'] for row in equipment()}-set(art)),engine_tested=False)
    (CACHE/'equipment_validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report))

def report():
    qa=json.loads((CACHE/'equipment_validation.json').read_text(encoding='utf-8'))
    parts=['# Équipements des navires primitifs — intégration du 8 octobre 2026','',
      'Statut : **définitions, descriptions, fonctions et déblocages intégrés ; nouveaux dessins en proposition seulement. Aucun essai en jeu.**',
      '', 'La validation du joueur remplace les anciens intitulés génériques par des techniques, gréements et systèmes d’armes identifiables. Les nombres de pièces sont des configurations de jeu, pas des inventaires attestés de navires nommés.',
      '', '## Quatre catégories et trois choix', '']
    labels={'armor':'Coque / charpente','guns':'Armement','propulsion':'Propulsion','range':'Aménagements / réserves'}
    for kind,label in [('caravel','Caravelle'),('galley','Galère'),('cog','Cogue')]:
        parts += [f'### {label}','','| Catégorie | Bronze | Argent | Or |','| --- | --- | --- | --- |']
        for slot,rows in ROWS[kind].items():parts += ['| '+labels[slot]+' | '+' | '.join(row[0] for row in rows)+' |']
        parts+=['']
    parts += ['## Fonctions choisies et cumul','',
      '- Cogue : chaloupes de débarquement ; efficacité d’invasion +10 % et capacité de débarquement +0,1.',
      '- Caravelle : organisation de blocus (+35 % de force de blocus) **et** chaloupes/détachement de débarquement (+10 % d’efficacité, +0,1 de capacité, −2 de réserve). Deux emplacements compatibles, actifs par défaut.',
      '- Galère : batterie de combat côtier (+15 % de dégâts de coque, +1 de précision) **et** éperon d’étrave pour l’abordage (+20 % de dégâts d’équipage, +0,05 de capacité de débarquement, −0,1 de vitesse). Deux emplacements compatibles, actifs par défaut.',
      '- L’éperon est une saillie d’étrave au-dessus de l’eau destinée à l’approche et à l’abordage, pas un bélier sous-marin moderne.',
      '', 'La portée de la galère reste **1**, avec **−80 % de dégâts de coque et d’équipage hors de portée**, comme le mécanisme de défense côtière natif. Aucun équipement ne supprime cette contrainte.',
      '', '## Coûts et équipement par défaut','',
      'Les quatre catégories commencent explicitement au niveau bronze ; leurs suppléments de caractéristiques et de biens sont nuls à ce niveau. Les coûts de construction, les équipages et le ravitaillement de base des coques sont conservés. Les fonctions sélectionnées ajoutent de faibles coûts de bois, tissu, outils ou fer à la construction/réfection. Le coût de chantier ajoute 0,5 par niveau de modification. Les niveaux supérieurs ajoutent des biens et des caractéristiques modestes ; aucun moteur, charbon, acier moderne ni obus n’est exigé, et aucun nouvel entretien matériel n’est caché dans les modules.',
      '', 'Ces valeurs ne garantissent pas un budget national précis : coûts de chantier, prix, salaires et consommation doivent encore être observés dans le moteur.',
      '', '## Technologies et départ','',
      '| Technologie | Ère | Prérequis |','| --- | ---: | --- |']
    for key,(fr,_,era,prereqs,_) in TECHS.items():
        parts += [f'| {fr} | {era} | '+(', '.join(TECHS[x][0] if x in TECHS else x for x in prereqs) or 'Début de branche')+' |']
    parts += ['',
      'Frégates et vaisseaux de ligne disposent désormais de portes technologiques dédiées. Seules France, Grande-Bretagne, Espagne, Russie, Portugal, Pays-Bas, Danemark-Norvège et Suède en disposent au départ, avec prise en charge des tags Danemark/Norvège séparés lorsqu’ils existent. Les autres nations pourront les rechercher. Les sciences navales partagées ne sont pas retirées.',
      '', 'Les deux technologies de carronades et de charpente diagonale ne sont accordées à **aucun** pays au départ. Elles distinguent les adaptations tardives des systèmes anciens au lieu de changer seulement les mots ou la couleur du bouton.',
      '', 'Les flottes du Brésil, des Indes néerlandaises, de Sardaigne, des Deux-Siciles, de l’Empire ottoman et de Venise avaient encore des classes avancées : elles passent à des coques primitives autorisées. Le nombre de navires de chaque flotte est strictement conservé. Les flottes des puissances autorisées ne sont pas retouchées.',
      '', 'Les pays possédant une flotte initiale ou la technologie des arsenaux navals reçoivent les connaissances de construction primitive. Les prérequis manquants des classes avancées sont ajoutés uniquement aux pays autorisés. Armées, populations, administrations, bâtiments et propriété coloniale sont protégés contre tout changement dans cette passe.',
      '', '## Rééquipement et succession','',
      'Le rééquipement permet d’améliorer les modules d’une même coque. Les successions caravelle → vaisseau de ligne, galère → défenseur côtier et cogue → transport moderne ne constituent **pas** une conversion native confirmée entre types ; elles nécessitent pour l’instant la construction de la coque successeure. Aucun faux champ de conversion n’a été ajouté.',
      '', '## Visuels : premier lot uniquement','',
      'Les définitions actives utilisent toujours les pictogrammes navals natifs des quatre catégories, bronze/argent/or, ainsi que les pictogrammes utilitaires natifs. **Les nouveaux dessins ne sont pas intégrés et les autres catégories ne sont pas déclarées terminées.**',
      '', 'Trois propositions de l’armement de caravelle ont été créées avec la compétence imagegen et le générateur intégré, en utilisant une planche des icônes navales natives comme référence de style : fauconneau bronze, canon long argent, carronade or. Masters proposés copiés dans `.asset-cache/early_ship_equipment_2026-10-08/artwork_proposals/`, planche de comparaison dans `caravel_armament_proposals.png`. Les versions brutes et l’alpha sont conservés ; recadrages/réductions ne servent qu’à la présentation. Aucun DDS ni registre n’est remplacé avant approbation.',
      '', 'Les [prompts exacts, chemins et statut de chaque proposition](early_ship_equipment_art_proposals_2026-10-08.json) sont conservés. Une tentative de suppression du halo argent a été écartée : ce point doit être contrôlé avant export final. Les autres visuels seront proposés après la revue de ce lot.',
      '', '## Références et limites historiques','',
      '- La [caravelle portugaise du National Maritime Museum](https://www.rmg.co.uk/collections/objects/rmgc-object-66267) illustre un gréement tardif à quatre mâts. Les configurations nommées du mod sont des adaptations de jeu, pas trois variantes certifiées d’un bâtiment historique unique.',
      '- Les [canons de la Mary Rose](https://maryrose.org/discover/collections/the-weaponry-of-the-mary-rose/great-guns/) documentent la diversité des systèmes anciens, dont les chargements et affûts distincts. Ils ne justifient pas les nombres de pièces choisis pour nos trois coques.',
      '- Le [plan de 1804 d’affût de carronade de 12 livres](https://www.rmg.co.uk/collections/objects/rmgc-object-86785) et la [carronade de 6 livres conservée à Gibraltar](https://www.ministryforheritage.gi/heritage-and-antiquities/6-pdr-carronade-military-heritage-centre-1315) étayent les calibres et la distinction entre canons longs et pièces courtes, sans représenter des équipements initiaux de 1776.',
      '- Le [National Maritime Museum sur Seppings](https://www.rmg.co.uk/collections/objects/rmgc-object-14491) situe sa carrière et ses travaux de renforcement diagonal après le départ du mod. Cette charpente ne remplace pas une coque en fer.',
      '- La [galère de guerre du Rijksmuseum](https://www.rijksmuseum.nl/en/collection/object/Model-of-a-War-Galley--dd5fdedc5f7f1bd12d46c16da1cdc5d4?tab=catalogue) présente une pièce de proue guidée dans l’axe ; nos trois compléments de batterie restent des choix d’équilibrage, pas son inventaire exact.',
      '', '## Contrôles réalisés','',
      f'- {qa["equipment_definitions"]} modules définis : 36 choix principaux et 5 fonctions, descriptions françaises et anglaises présentes avec BOM.',
      f'- {qa["new_technologies"]} technologies, références/prérequis/ères validés, absence de cycle dans leurs chemins de recherche.',
      f'- {qa["fleets_checked"]} flottes vérifiées, effectifs et flottes des pays autorisés préservés ; aucune coque initiale avec déblocage manquant.',
      '- Définitions cohérentes avec les paramètres navals présents dans les fichiers natifs ; deux fonctions compatibles sur caravelle et galère.',
      '- Fichiers runtime hors de la liste autorisée inchangés. Les 151 exports graphiques existants ne sont pas modifiés.',
      '- QA détaillée : `.asset-cache/early_ship_equipment_2026-10-08/equipment_validation.json` ; réexécution : `tools/build_early_ship_equipment.py --check`.',
      '- **Non vérifié en jeu** : écran du concepteur, cumul effectif des fonctions, coûts observés, rééquipement et emploi des modèles initiaux. Aucun démarrage de nouvelle partie ni redémarrage du jeu effectué.','']
    sys.stdout.reconfigure(encoding='utf-8')
    print('*** Begin Patch\n*** Add File: '+DOC+'\n'+'\n'.join('+'+line for line in parts)+'\n*** End Patch')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--prepare',action='store_true');parser.add_argument('--check',action='store_true');parser.add_argument('--emit',action='store_true');parser.add_argument('--report',action='store_true')
    args=parser.parse_args()
    if args.prepare:prepare()
    elif args.emit:emit()
    elif args.check:check()
    elif args.report:report()
