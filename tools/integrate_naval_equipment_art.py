"""Hash-lock approved naval artwork; emit source patches and check narrow bindings.

Never edits game text directly. Binary export uses the existing DDS exporter.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import recolour_pm_icons as colour
import audit_british_colonial_start as history

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / '.asset-cache/early_ship_equipment_2026-10-08'
REGISTRY = 'docs/reports/assets/source_registry.json'
MODS = 'common/ship_modifications/10_1776_early_equipment.txt'
PROPULSION_ROWS = [
    ('Grand-voile carrée','Square course sail','Une grand-voile carrée sur le mât principal, sans machine.','One square course sail on the main mast, without machinery.'),
    ('Grand-voile et hunier','Course sail and topsail','Un hunier est ajouté au-dessus de la grand-voile, sur le même mât.','A topsail is added above the course sail on the same mast.'),
    ('Grand-voile, hunier et perroquet','Course sail, topsail and topgallant','Un perroquet complète le hunier au sommet du même mât : trois étages de voiles, sans moteur.','A topgallant above the topsail completes three sail tiers on the same mast, without engines.')
]
LOTS = {
    'armament': dict(slot='guns',names=['falconets_bronze','long_guns_silver','carronades_gold'],
        proposal='docs/reports/naval/early_ship_equipment_art_proposals_2026-10-08.json',
        approval='le premier lot est aprouve tu peut passé au lot de la coque',
        labels=['Fauconneaux bronze','Canons longs argent','Carronades or']),
    'hull': dict(slot='armor',names=['caravel_hull_bronze','caravel_hull_silver','caravel_hull_gold'],
        proposal='docs/reports/naval/caravel_hull_art_proposals_2026-10-08.json',
        approval='Hop, je valide le lot, tu peux passer au suivant. À savoir la propulsion.',
        labels=['Franc-bord bronze','Couples doubles argent','Renforts diagonaux or']),
    'propulsion': dict(slot='propulsion',names=['caravel_rig_vertical_bronze_v2','caravel_rig_vertical_silver_v2','caravel_rig_vertical_gold_v2'],
        proposal='docs/reports/naval/caravel_propulsion_art_proposals_v2_2026-10-08.json',
        approval='Hop, tu peux intégrer et passer au jeu suivant, le pont.',
        labels=['Grand-voile bronze','Hunier ajouté argent','Perroquet ajouté or'],text_rows=PROPULSION_ROWS),
    'deck': dict(slot='range',names=['caravel_deck_bronze','caravel_deck_silver_v5','caravel_deck_gold'],
        proposal='docs/reports/naval/caravel_deck_art_proposals_v5_2026-10-08.json',
        approval='Tu peux intégrer et passer au lot suivant.',
        labels=['Tonneaux en cale bronze','Gaillard et cambuse argent','Faux-pont et eau or']),
    'galley_armament': dict(ship='galley',slot='guns',
        names=['galley_bow_gun_bronze_v2','galley_chase_gun_silver_v2','galley_axial_gun_gold_v2'],
        proposal='docs/reports/naval/galley_armament_art_proposals_v2_2026-10-08.json',
        approval='que tu peux intégrer et passer au suivant.',
        labels=['Proue sur pivots bronze','Affûts à roues argent','Glissière axiale or']),
    'galley_hull': dict(ship='galley',slot='armor',
        names=['galley_hull_bronze','galley_hull_silver','galley_hull_gold'],
        proposal='docs/reports/naval/galley_hull_art_proposals_2026-10-08.json',
        approval="ok tu peut integré et passé au lot suivant, aussi je n'ai pas verifié mais toute ces modification donne des statisitque n'est ce pas ?",
        labels=['Bordage léger bronze','Traverses de nage argent','Quille doublée or']),
    'galley_propulsion': dict(ship='galley',slot='propulsion',
        names=['galley_propulsion_bronze','galley_propulsion_silver','galley_propulsion_gold'],
        proposal='docs/reports/naval/galley_propulsion_art_proposals_2026-10-08.json',
        approval='Ok, tu peux tout incorporer et passer au lot suivant.',
        labels=['Avirons séparés bronze','Aviron collectif argent','Voiles latines or']),
    'galley_supply': dict(ship='galley',slot='range',
        names=['galley_supply_bronze','galley_supply_silver','galley_supply_gold'],
        proposal='docs/reports/naval/galley_supply_art_proposals_2026-10-08.json',
        approval='Ok, tu peux intégrer et passer au suivant.',
        labels=['Coffres et outres bronze','Tonneaux sous coursie argent','Cambuse et avirons or']),
    'cog_hull': dict(ship='cog',slot='armor',
        names=['cog_hull_bronze','cog_hull_silver','cog_hull_gold'],
        proposal='docs/reports/naval/cog_hull_art_proposals_2026-10-08.json',
        approval='Ok, tu peux intégrer et passer au lot suivant.',
        labels=['Clins rivetés bronze','Varangues et carlingue argent','Serres et baux or']),
    'cog_armament': dict(ship='cog',slot='guns',
        names=['cog_swivel_gun_bronze_v2','cog_long_gun_silver','cog_carronade_gold_v3'],
        proposal='docs/reports/naval/cog_armament_art_proposals_2026-10-08.json',
        approval='Hop, tu peux intégrer et passer au le suivant.',
        labels=['Pierriers sur pivots bronze','Canons de 3 livres argent','Carronades de 6 livres or']),
    'cog_propulsion': dict(ship='cog',slot='propulsion',
        names=['cog_rig_bronze','cog_rig_silver','cog_rig_gold'],
        proposal='docs/reports/naval/cog_propulsion_art_proposals_2026-10-08.json',
        approval='Je vais, tu peux intégrer, passer au lot suivant.',
        labels=['Voile carrée bronze','Bandes de ris argent','Hunier ajouté or']),
    'cog_supply': dict(ship='cog',slot='range',
        names=['cog_supply_bronze','cog_supply_silver','cog_supply_gold'],
        proposal='docs/reports/naval/cog_supply_art_proposals_2026-10-08.json',
        approval='OK, tu peux intégrer et passer au lot suivant.',
        labels=['Cale libre bronze','Couchettes et râtelier argent','Pont de troupes or']),
    'naval_functions': dict(slot='utility_1',date='2026-10-09',
        names=['landing_launches_blue','blockade_supply_bronze_v2','coastal_battery_red'],
        keys=['landing_launches_blue','blockade_supply_bronze','coastal_battery_red'],
        bindings=[['aor_landing_launches','aor_caravel_landing'],['aor_caravel_blockade'],['aor_galley_coastal_battery']],
        proposal='docs/reports/naval/naval_functions_art_proposals_v2_2026-10-09.json',
        approval="Ok, tu peux intégrer et passer au lot suivant s'il y en a un.",
        labels=['Chaloupes de débarquement','Organisation de blocus','Batterie côtière']),
    'galley_boarding_spur': dict(slot='utility_1',date='2026-10-09',
        names=['galley_boarding_spur_blue'],keys=['galley_boarding_spur_blue'],
        bindings=[['aor_galley_boarding_spur']],
        proposal='docs/reports/naval/galley_boarding_spur_art_proposal_2026-10-09.json',
        approval='que tu peux intégrer. Je vais relancer le jeu de mon côté, ensuite.',
        labels=['Éperon d’étrave · abordage'])
}

def localized_text(text,language,lot):
    """Change only the three approved equipment names and descriptions."""
    config=LOTS[lot];index=0 if language=='french' else 1
    for level,row in zip(('low','mid','high'),config.get('text_rows',[])):
        key=f'aor_{config.get("ship","caravel")}_{config["slot"]}_{level}'
        for suffix,value in [('',row[index]),('_desc',row[index+2])]:
            pattern=rf'(?m)(^ {key}{suffix}: ")[^"\n]*("$)'
            text,count=re.subn(pattern,lambda m:m[1]+value+m[2],text)
            assert count==1,(key,suffix,count)
    return text

def select_lot(lot):
    global LOT, CONFIG, PACK, MANIFEST, KEYS, NAMES, PLAN
    LOT=lot;CONFIG=LOTS[lot]
    PACK=f'docs/reports/assets/naval_equipment_{lot}_sources_{CONFIG.get("date","2026-10-08")}'
    MANIFEST=PACK+'/manifest.json'
    KEYS=CONFIG.get('keys') or [f'aor_{CONFIG.get("ship","caravel")}_{CONFIG["slot"]}_{level}' for level in ('low','mid','high')]
    NAMES=CONFIG['names'];PLAN=CACHE/f'approved_{lot}_plan.json'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def prepare():
    assert not PLAN.exists(), 'Do not overwrite approval baseline'
    proposals = json.loads((ROOT/CONFIG['proposal']).read_text())
    assert len(KEYS)==len(NAMES)==len(proposals.get('proposals',proposals.get('entries'))), 'Mismatched approved lot'
    entries = []
    for key,name,proposal in zip(KEYS,NAMES,proposals.get('proposals',proposals.get('entries'))):
        assert proposal['key'] == key
        source = f'{PACK}/{name}.png'
        assert digest(ROOT/source) == digest(ROOT/proposal.get('path',proposal.get('proposed_master'))), 'Approved original changed'
        if proposal.get('source_sha256'):assert digest(ROOT/source)==proposal['source_sha256']
        bindings=CONFIG.get('bindings',[[k] for k in KEYS])[len(entries)]
        if CONFIG.get('bindings'):assert proposal['bindings']==bindings
        im=Image.open(ROOT/source)
        assert im.mode=='RGBA'
        alpha=im.getchannel('A'); assert alpha.histogram()[0]>0
        left,top,right,bottom=alpha.getbbox()
        entries.append(dict(dds=f'gfx/interface/icons/military_icons/navy_icons/ship_designer_icons/1776_{name}.dds',
            size=120,mips=7,source=source,source_sha256=digest(ROOT/source),
            crop=dict(left=left,top=top,width=right-left,height=bottom-top),
            padding=round(max(right-left,bottom-top)*.06),
            provenance=MANIFEST,ship_modification_bindings=bindings,palette=proposal.get('palette',['bronze','silver','gold'][len(entries)])))
        assert not (ROOT/entries[-1]['dds']).exists(), 'Existing destination'
    manifest=dict(schema=1,date=CONFIG.get('date','2026-10-08'),status='APPROVED_AND_INTEGRATED',
        approval=CONFIG['approval'],
        generation='Built-in imagegen. Exact approved originals; no discarded revisions or extraction attempts.',
        prompts=proposals['prompts'],entries=entries,
        export=dict(tool='tools/rebuild_asset_icons.cjs',format='native BGRA8 A8R8G8B8',size=120,mips=7,
            alpha_preserved=True,retouch=False,exterior_haze='Preserved as present in approved originals'),engine_tested=False)
    if CONFIG.get('text_rows'):manifest['localization_rows']=CONFIG['text_rows']
    state=dict(before_runtime=colour.runtime_hashes(),registry_text=(ROOT/REGISTRY).read_text(),
        definition_text=(ROOT/MODS).read_text(),manifest=manifest)
    state['localization_before']={f'localization/{lang}/1776_early_ship_equipment_l_{lang}.yml':(ROOT/f'localization/{lang}/1776_early_ship_equipment_l_{lang}.yml').read_text(encoding='utf-8') for lang in ('french','english')} if CONFIG.get('text_rows') else {}
    PLAN.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(status='APPROVED_MASTERS_LOCKED',entries=len(entries))))

def expected_text(state):
    text=state['definition_text']
    for e in state['manifest']['entries']:
        for key in e['ship_modification_bindings']:
            pattern=rf'(?m)(^{key} = \{{\n    type = ship_mod_slot_{CONFIG["slot"]}\n    icon = ")[^"]+("\n)'
            text,n=re.subn(pattern,lambda m:m[1]+e['dds']+m[2],text)
            assert n==1,(key,n)
    return text

def emit():
    state=json.loads(PLAN.read_text(encoding='utf-8'))
    registry=json.loads(state['registry_text'])
    registry['entries'] += state['manifest']['entries']
    parts=['*** Begin Patch',f'*** Add File: {MANIFEST}']
    parts+=['+'+line for line in json.dumps(state['manifest'],indent=2,ensure_ascii=False).splitlines()]
    parts.append(history.patch_file(REGISTRY,state['registry_text'],json.dumps(registry,indent=2,ensure_ascii=False)+'\n').rstrip())
    parts.append(history.patch_file(MODS,state['definition_text'],expected_text(state)).rstrip())
    for path,old in state.get('localization_before',{}).items():
        lang=path.split('/')[1]
        parts.append(history.patch_file(path,old,localized_text(old,lang,LOT)).rstrip())
    parts+=['*** End Patch'];sys.stdout.reconfigure(encoding='utf-8');print('\n'.join(parts))

def check():
    state=json.loads(PLAN.read_text(encoding='utf-8'))
    manifest=json.loads((ROOT/MANIFEST).read_text(encoding='utf-8'))
    assert manifest==state['manifest']
    assert (ROOT/MODS).read_text()==expected_text(state), 'Non-icon gameplay change'
    assert manifest.get('localization_rows',[])==[list(row) for row in CONFIG.get('text_rows',[])]
    for path,old in state.get('localization_before',{}).items():
        assert (ROOT/path).read_text(encoding='utf-8')==localized_text(old,path.split('/')[1],LOT)
        assert (ROOT/path).read_bytes().startswith(b'\xef\xbb\xbf')
    registry=json.loads((ROOT/REGISTRY).read_text())
    assert registry['entries']==json.loads(state['registry_text'])['entries']+manifest['entries']
    allowed={MODS}|{e['dds'] for e in manifest['entries']}|set(state.get('localization_before',{}))
    runtime=colour.runtime_hashes();before=state['before_runtime']
    assert not [p for p in set(runtime)|set(before) if p not in allowed and runtime.get(p)!=before.get(p)], 'Unrelated runtime change'
    sheet=Image.new('RGB',(300*len(manifest['entries']),230),'#213138');draw=ImageDraw.Draw(sheet)
    font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',17)
    for i,e in enumerate(manifest['entries']):
        assert digest(ROOT/e['source'])==e['source_sha256']
        assert digest(ROOT/e['dds'])==e['dds_sha256']
        im=colour.decode(ROOT/e['dds']);assert im.size==(120,120)
        assert im.getchannel('A').histogram()[0]>0
        for size,y in [(120,40),(64,165)]:
            thumb=im.resize((size,size),Image.Resampling.LANCZOS)
            sheet.paste(thumb,(i*300+(300-size)//2,y),thumb)
        draw.text((i*300+15,12),CONFIG['labels'][i],font=font,fill='white')
    sheet.save(CACHE/f'{LOT}_integrated_dds_preview.png')
    report=dict(status='PASS_APPROVED_'+LOT.upper()+'_INTEGRATION',approved_originals_preserved=True,
        only_icon_bindings_changed=True,icon_bindings_count=sum(len(e['ship_modification_bindings']) for e in manifest['entries']),
        dds_count=len(manifest['entries']),dds_size=120,dds_mips=7,
        protected_runtime_files=len(before)-1,registry_assets=len(registry['entries']),engine_tested=False)
    (CACHE/f'{LOT}_integration_validation.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['prepare','emit','check']);p.add_argument('--lot',choices=LOTS,default='armament');a=p.parse_args()
    select_lot(a.lot)
    globals()[a.mode]()
