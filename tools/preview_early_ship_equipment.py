"""Read native naval glyphs and make ignored reference/comparison sheets only."""
from pathlib import Path
import argparse
import json
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
NATIVE = Path('C:/Games/Victoria 3/game')
CACHE = ROOT / '.asset-cache/early_ship_equipment_2026-10-08'

def native_sheet():
    CACHE.mkdir(parents=True, exist_ok=True)
    prefix = 'gfx/interface/icons/military_icons/navy_icons/ship_designer_icons/'
    rows = [(slot, [NATIVE / (prefix + f'ship_designer_{slot}_{level}.dds')
                    for level in ('low','mid','high')])
            for slot in ('armor','guns','propulsion','range')]
    sheet = Image.new('RGB',(660,520),'#213138')
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',16)
    for row,(slot,paths) in enumerate(rows):
        for col,path in enumerate(paths):
            im=Image.open(path).convert('RGBA')
            im.thumbnail((110,92),Image.Resampling.NEAREST)
            im=im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST)
            # Enlargement is for inspecting the original pixels, not a replacement asset.
            if im.height>95: im.thumbnail((150,95),Image.Resampling.NEAREST)
            sheet.paste(im,(col*220+(220-im.width)//2,row*130+25),im)
            draw.text((col*220+12,row*130+5),f'{slot} / {path.stem.rsplit("_",1)[1]}',font=font,fill='white')
    output=CACHE/'native_equipment_reference.png'
    sheet.save(output)
    print(output)

def native_utility_sheet():
    """Inspect existing function palettes; never changes a runtime image."""
    sheet=Image.new('RGB',(660,180),'#213138')
    draw=ImageDraw.Draw(sheet)
    font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',16)
    for col,name in enumerate(('marine_capacity','supplies_navy','average_damage_navy')):
        path=NATIVE/f'gfx/interface/icons/military_icons/navy_icons/{name}.dds'
        im=Image.open(path).convert('RGBA')
        im=im.crop(im.getchannel('A').getbbox())
        im.thumbnail((140,120),Image.Resampling.NEAREST)
        sheet.paste(im,(col*220+(220-im.width)//2,40),im)
        draw.text((col*220+12,10),name,font=font,fill='white')
    output=CACHE/'native_utility_reference.png'
    sheet.save(output)
    print(output)

def proposal_sheet(hulls=False,propulsion=False,vertical=False,decks=False,decks_v2=False,decks_revision=1,galley_armament=False,galley_revision=1,galley_hulls=False,galley_propulsion=False,galley_supply=False,cog_hulls=False,cog_armament=False,cog_armament_revision=1,cog_propulsion=False,cog_supply=False):
    if decks_revision > 1:
        decks=True
    directory=CACHE/'artwork_proposals'
    names=['falconets_bronze','long_guns_silver','carronades_gold']
    labels=['Fauconneaux · bronze','Canons longs · argent','Carronades · or']
    if hulls:
        names=['caravel_hull_bronze','caravel_hull_silver','caravel_hull_gold']
        labels=['Franc-bord · bronze','Couples doubles · argent','Renforts diagonaux · or']
    if propulsion:
        names=['caravel_rig_bronze','caravel_rig_silver','caravel_rig_gold']
        labels=['Deux mâts · bronze','Trois mâts · argent','Quatre mâts · or']
    if vertical:
        names=['caravel_rig_vertical_bronze_v2','caravel_rig_vertical_silver_v2','caravel_rig_vertical_gold_v2']
        labels=['Grand-voile · bronze','Hunier ajouté · argent','Perroquet ajouté · or']
    if decks or decks_v2:
        names=['caravel_deck_bronze','caravel_deck_silver','caravel_deck_gold']
        labels=['Tonneaux en cale · bronze','Gaillard et cambuse · argent','Faux-pont et eau · or']
        if decks_v2:
            names[1]='caravel_deck_silver_v2'
        if decks_revision > 1:
            names[1]=f'caravel_deck_silver_v{decks_revision}'
    if galley_armament:
        names=['galley_bow_gun_bronze','galley_chase_gun_silver','galley_axial_gun_gold']
        labels=['Proue · 6 livres · bronze','Chasse · 12 livres · argent','Axial · 24 livres · or']
        if galley_revision > 1:
            names=[f'{name}_v{galley_revision}' for name in names]
    if galley_hulls:
        names=['galley_hull_bronze','galley_hull_silver','galley_hull_gold']
        labels=['Bordage léger · bronze','Traverses de nage · argent','Quille doublée · or']
    if galley_propulsion:
        names=['galley_propulsion_bronze','galley_propulsion_silver','galley_propulsion_gold']
        labels=['Avirons séparés · bronze','Aviron collectif · argent','Deux voiles latines · or']
    if galley_supply:
        names=['galley_supply_bronze','galley_supply_silver','galley_supply_gold']
        labels=['Coffres et outres · bronze','Sous coursie · argent','Cambuse et avirons · or']
    if cog_hulls:
        names=['cog_hull_bronze','cog_hull_silver','cog_hull_gold']
        labels=['Clins rivetés · bronze','Varangues et carlingue · argent','Serres et baux · or']
    if cog_armament:
        names=['cog_swivel_gun_bronze','cog_long_gun_silver','cog_carronade_gold']
        labels=['Pierriers · bronze','Canons de 3 livres · argent','Carronades de 6 livres · or']
        if cog_armament_revision == 2:
            names=['cog_swivel_gun_bronze_v2','cog_long_gun_silver','cog_carronade_gold_v3']
    if cog_propulsion:
        names=['cog_rig_bronze','cog_rig_silver','cog_rig_gold']
        labels=['Voile carrée · bronze','Bandes de ris · argent','Hunier ajouté · or']
    if cog_supply:
        names=['cog_supply_bronze','cog_supply_silver','cog_supply_gold']
        labels=['Cale libre · bronze','Couchettes et râteliers · argent','Pont de troupes · or']
    sheet=Image.new('RGB',(900,310),'#213138')
    draw=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',17)
    stats=[]
    for index,(name,label) in enumerate(zip(names,labels)):
        source=directory/(name+'.png');im=Image.open(source).convert('RGBA')
        alpha=im.getchannel('A');hist=alpha.histogram();bbox=alpha.getbbox()
        assert hist[0]>0,'No real transparency: '+name
        stats.append(dict(name=name,size=im.size,alpha_zero=hist[0],alpha_opaque=hist[255],alpha_partial=sum(hist[1:255]),bbox=bbox))
        draw.text((index*300+12,10),label,font=font,fill='white')
        # Analysis-only crop/scale for readable comparisons; raw masters untouched.
        for size,y in [(180,42),(64,226),(32,270)]:
            thumb=im.crop(bbox);thumb.thumbnail((size,140 if size==180 else size),Image.Resampling.LANCZOS)
            sheet.paste(thumb,(index*300+(300-thumb.width)//2,y),thumb)
    preview_name=f'caravel_deck_proposals_v{decks_revision}.png' if decks_revision>1 else 'caravel_deck_proposals_v2.png' if decks_v2 else 'caravel_deck_proposals.png' if decks else 'caravel_propulsion_vertical_v2.png' if vertical else 'caravel_propulsion_proposals.png' if propulsion else 'caravel_hull_proposals.png' if hulls else 'caravel_armament_proposals.png'
    qa_name=f'deck_artwork_v{decks_revision}_alpha_qa.json' if decks_revision>1 else 'deck_artwork_v2_alpha_qa.json' if decks_v2 else 'deck_artwork_alpha_qa.json' if decks else 'propulsion_vertical_v2_alpha_qa.json' if vertical else 'propulsion_artwork_alpha_qa.json' if propulsion else 'hull_artwork_alpha_qa.json' if hulls else 'artwork_alpha_qa.json'
    if galley_armament:
        preview_name='galley_armament_proposals.png'
        qa_name='galley_armament_alpha_qa.json'
        if galley_revision > 1:
            preview_name=f'galley_armament_proposals_v{galley_revision}.png'
            qa_name=f'galley_armament_v{galley_revision}_alpha_qa.json'
    if galley_hulls:
        preview_name='galley_hull_proposals.png'
        qa_name='galley_hull_alpha_qa.json'
    if galley_propulsion:
        preview_name='galley_propulsion_proposals.png'
        qa_name='galley_propulsion_alpha_qa.json'
    if galley_supply:
        preview_name='galley_supply_proposals.png'
        qa_name='galley_supply_alpha_qa.json'
    if cog_hulls:
        preview_name='cog_hull_proposals.png'
        qa_name='cog_hull_alpha_qa.json'
    if cog_armament:
        preview_name='cog_armament_proposals.png'
        qa_name='cog_armament_alpha_qa.json'
        if cog_armament_revision > 1:
            preview_name=f'cog_armament_proposals_v{cog_armament_revision}.png'
            qa_name=f'cog_armament_v{cog_armament_revision}_alpha_qa.json'
    if cog_propulsion:
        preview_name='cog_propulsion_proposals.png'
        qa_name='cog_propulsion_alpha_qa.json'
    if cog_supply:
        preview_name='cog_supply_proposals.png'
        qa_name='cog_supply_alpha_qa.json'
    path=CACHE/preview_name;sheet.save(path)
    (CACHE/qa_name).write_text(json.dumps(stats,indent=2),encoding='utf-8')
    print(json.dumps({'preview':str(path),'images':stats}))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--proposals',action='store_true');parser.add_argument('--hulls',action='store_true');parser.add_argument('--propulsion',action='store_true');parser.add_argument('--propulsion-v2',action='store_true');parser.add_argument('--decks',action='store_true');parser.add_argument('--decks-v2',action='store_true');parser.add_argument('--decks-revision',type=int,default=1)
    parser.add_argument('--galley-armament',action='store_true');parser.add_argument('--galley-revision',type=int,default=1);parser.add_argument('--galley-hulls',action='store_true');parser.add_argument('--galley-propulsion',action='store_true');parser.add_argument('--galley-supply',action='store_true');parser.add_argument('--cog-hulls',action='store_true');parser.add_argument('--cog-armament',action='store_true')
    parser.add_argument('--cog-armament-revision',type=int,default=1)
    parser.add_argument('--cog-propulsion',action='store_true')
    parser.add_argument('--cog-supply',action='store_true')
    parser.add_argument('--native-utilities',action='store_true')
    args=parser.parse_args()
    if args.native_utilities:native_utility_sheet()
    elif args.cog_supply:proposal_sheet(cog_supply=True)
    elif args.cog_propulsion:proposal_sheet(cog_propulsion=True)
    elif args.cog_armament:proposal_sheet(cog_armament=True,cog_armament_revision=args.cog_armament_revision)
    elif args.cog_hulls:proposal_sheet(cog_hulls=True)
    elif args.galley_supply:proposal_sheet(galley_supply=True)
    elif args.galley_propulsion:proposal_sheet(galley_propulsion=True)
    elif args.galley_hulls:proposal_sheet(galley_hulls=True)
    elif args.galley_armament:proposal_sheet(galley_armament=True,galley_revision=args.galley_revision)
    elif args.decks_revision>1:proposal_sheet(decks_revision=args.decks_revision)
    elif args.decks_v2:proposal_sheet(decks_v2=True)
    elif args.decks:proposal_sheet(decks=True)
    elif args.propulsion_v2:proposal_sheet(vertical=True)
    elif args.propulsion:proposal_sheet(propulsion=True)
    elif args.hulls:proposal_sheet(hulls=True)
    elif args.proposals:proposal_sheet()
    else:native_sheet()
