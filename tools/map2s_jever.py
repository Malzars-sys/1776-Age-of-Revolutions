"""MAP-2S: additive current-workspace baseline and narrowly scoped Jever correction.

All edits are prepared as apply_patch payloads. Old receipts and baselines are
read-only; the historical map raster, not a building name, defines candidates.
"""
from pathlib import Path
import json,sys,subprocess,urllib.request,re,collections as C
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import map2r_anhalt as r
q=r.q;core=q.core;ROOT=r.ROOT;OUT=ROOT/'docs/reports/map/MAP2S'
BOX=(4260,735,4302,776)
SOURCE_URL='https://www.schlossmuseum.de/sammlungen/virtuelle-sammlungen/regionalgeschichte/landkarten-und-plaene/'

def dump(name,data):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

def load(name):return json.loads((OUT/name).read_text(encoding='utf8'))

def capture():
    assert not (OUT/'BASELINE.json').exists(),'Never replace an existing reference'
    inv=core.qa.inventory();bmp=ROOT/'docs/reports/map/MAP2R/provinces_candidate.png'
    assert core.sha(bmp)==core.sha(ROOT/'map_data/provinces.png')
    hashes=q.economy.runtime_hashes()
    originals={p:(ROOT/p).read_text(encoding='utf-8-sig') for p in hashes if p.endswith('.txt') and p.startswith(('common/history/states/','common/history/pops/','map_data/state_regions/'))}
    protected={p.relative_to(ROOT).as_posix():core.sha(p) for directory in ['docs/reports/map','docs/reports/hre','docs/prototypes','tools'] for p in (ROOT/directory).rglob('*') if p.is_file() and OUT not in p.parents and p.name!='map2s_jever.py' and '__pycache__' not in p.parts}
    dump('BASELINE.json',dict(inventory=inv,hashes=hashes,originals=originals,registry=json.loads(core.active_registry_path().read_text(encoding='utf8')),bitmap_backup=bmp.relative_to(ROOT).as_posix(),bitmap_sha256=core.sha(bmp),protected_files=protected,git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),git_index_sha256=core.sha(ROOT/'.git/index')))
    dump('MAP2R_RUNTIME_USER_VALIDATION.json',dict(lot='MAP2R',status='PASS_RUNTIME_USER_VALIDATED',source='C:/Users/simeo/.codex/attachments/8110471d-657d-4079-bcb0-c25ce944a613/Texte collé.txt',recorded='2026-10-17',method='Manual player acceptance explicitly supplied in MAP-2S prompt',coverage='Installed MAP2R inspected and accepted by player; not all historical border fringes',simulation_duration=None,automated_engine_test=False,historical_boundary_certification=False,old_baselines_rewritten=False))
    print('Captured immutable baseline; world',sum(p['count'] for p in inv['pops']),'; registered RGB',len(load('BASELINE.json')['registry']),flush=True)

def fetch():
    OUT.mkdir(parents=True,exist_ok=True)
    target=OUT/'MUSEUM_CATALOGUE.html'
    if not target.exists():
        req=urllib.request.Request(SOURCE_URL,headers={'User-Agent':'HistoricalMapResearch/1.0'})
        target.write_bytes(urllib.request.urlopen(req,timeout=30).read())
    raw=target.read_text(encoding='utf8')
    from html import unescape
    urls=list(dict.fromkeys(unescape(u) for u in re.findall(r'(?:href|src)=[\"\']([^\"\']+\.(?:jpe?g|png)(?:\?[^\"\']*)?)[\"\']',raw,re.I)))
    dump('MUSEUM_IMAGES.json',urls)
    print('\n'.join(urls))

def sources():
    # Bounded acquisition of the museum's three specifically identified maps.
    # These are archival inputs, never instructions, and never overwrite originals.
    items=[('KONIGSHAVEN_1725.jpg','https://www.schlossmuseum.de/wp-content/uploads/2018/01/12085_f-1.jpg'),('KUNSTENBACH_1798.jpg','https://www.schlossmuseum.de/wp-content/uploads/2018/01/12089_f-1.jpg'),('WITTMUND_BORDER_1746.jpg','https://www.schlossmuseum.de/wp-content/uploads/2018/01/12225_f-1.jpg'),('KONIGSHAVEN_DETAIL.jpg','https://www.schlossmuseum.de/wp-content/uploads/2018/01/12085_4-1.jpg'),('KUNSTENBACH_DETAIL_1.jpg','https://www.schlossmuseum.de/wp-content/uploads/2018/01/12089_1-1.jpg'),('KUNSTENBACH_DETAIL_2.jpg','https://www.schlossmuseum.de/wp-content/uploads/2018/01/12089_2-1.jpg')]
    metadata=[]
    for name,url in items:
        p=OUT/name
        if not p.exists():
            req=urllib.request.Request(url,headers={'User-Agent':'HistoricalMapResearch/1.0'})
            with urllib.request.urlopen(req,timeout=30) as res:data=res.read(30_000_001)
            assert len(data)<=30_000_000
            p.write_bytes(data)
        im=Image.open(p)
        metadata.append(dict(name=name,url=url,sha256=core.sha(p),size=im.size))
        print(name,im.size,flush=True)
    dump('MAP_SOURCES.json',metadata)

def library():
    url='https://digital.lb-oldenburg.de/lbolmapo/content/titleinfo/1866630'
    req=urllib.request.Request(url,headers={'User-Agent':'HistoricalMapResearch/1.0'})
    p=OUT/'KUNSTENBACH_LIBRARY.html'
    if not p.exists():p.write_bytes(urllib.request.urlopen(req,timeout=35).read())
    raw=p.read_text(encoding='utf8')
    from html import unescape
    print('\n'.join(dict.fromkeys(unescape(u) for u in re.findall(r'(?:href|src)=[\"\']([^\"\']+)[\"\']',raw) if any(k in u.lower() for k in ['manifest','iiif','mets','download','pageview','zoom','image']))))

def inspect():
    b=load('BASELINE.json');bmp=core.packed(ROOT/b['bitmap_backup']);owners={p['key'][0]:p['key'][1:] for p in b['inventory']['owners']}
    rows=[]
    for rgb,(sid,tag) in owners.items():
        if tag!='OLD' or sid!='STATE_HANNOVER':continue
        yy,xx=np.where(bmp==int(rgb[1:],16))
        rows.append(dict(RGB=rgb,State_ID=sid,Owner=tag,cells=len(xx),bounds=[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())]))
    loc=[x for x in q.r9.locators(bmp) if BOX[0]<=x['X']<BOX[2] and BOX[1]<=x['Y']<BOX[3]]
    dump('INITIAL_LOCAL_INVENTORY.json',dict(provinces=rows,locators=loc,population=[p for p in b['inventory']['regional_pop'] if p['key'][:2]==['STATE_HANNOVER','OLD']],buildings=[p for p in b['inventory']['buildings'] if 'STATE_HANNOVER' in str(p) and 'OLD' in str(p)]))
    print(json.dumps(load('INITIAL_LOCAL_INVENTORY.json'),ensure_ascii=False,indent=2))
    q.core.panel if hasattr(q.core,'panel') else None
    import map2o_east_frisia as o
    o.panel(bmp,owners,BOX,'MAP2S - reference OLD / PRU / Bremen',scale=22).save(OUT/'JEVER_INITIAL_READING.png')

def decisions():
    """Do not turn a known dynasty into an invented pixel boundary."""
    dump('DECISIONS.json',dict(status='MAP2S_PARTIAL_JEVER_GEOMETRY_UNRESOLVED',territorial_corrections_installed=[],new_RGBs=[],changed_cells=[],historical_sovereignty='AZR',current_owner='OLD',State_ID='STATE_HANNOVER',numeric_state_id=69,classification='C_GEOMETRY_A_SOVEREIGNTY',native_town_pixel=None,independently_verified_position_error_px=None,reason='Small archival reproductions establish the neighboring jurisdictions, but not their homologous boundary in the stylized native coastline. Neither an entire OLD carrier nor a guessed northwestern core is justified.',world_population_policy='Historical estimate allowed only for a supported perimeter; otherwise deterministic redistribution. No transfer installed, so no redistribution or historical estimate applied.',next_region='STATE_SAXONY',next_region_started=False))
    dump('COLGREP_USAGE.json',dict(failed_attempts=1,successful_calls=1,executable='C:/Users/simeo/.cargo/bin/colgrep.exe',command='colgrep.exe --agent "Locate retained historical map evidence for Jever/Jeverland boundaries versus Varel and Kniphausen, and existing reusable map transfer helpers for OLD to AZR in STATE_HANNOVER. Return relevant repository files and line ranges only; do not modify project files." .',initial_error='Index lock creation denied in restricted environment; one approved retry succeeded',verified_results=[dict(file='docs/reports/map/MAP2R/JEVER_AUDIT.md',lines='5-11',relevance='Correct current carrier provinces and explicit missing geometry'),dict(file='docs/reports/map/MAP2O/JEVER_VAREL_KNIPHAUSEN_AUDIT.md',lines='11-12',relevance='Exclusion guards, not a boundary'),dict(file='tools/map2r_anhalt.py',lines='11',relevance='Existing four Anhalt TAGs')],limitations='No new geometry supplied. Time and Codex token savings not instrumented; no exact saving claimed.',model_configuration_changed=False))

def tables():
    b=load('BASELINE.json');local=load('INITIAL_LOCAL_INVENTORY.json');datasets={}
    def table(name,fields,rows):datasets[name]=dict(fields=fields,rows=rows)
    audit=[]
    for p in local['provinces']:
        audit.append(dict(RGB=p['RGB'],State_ID=p['State_ID'],Owner_before='OLD',Owner_after='OLD',Carrier_cells=p['cells'],Bounds_XY=';'.join(map(str,p['bounds'])),Status='NOT_APPLIED_C_CARRIER_ONLY',Historical_Jever_owner='AZR',Note='Carrier may contain foreign jurisdictions; not a certified Jever polygon',Source='MAP2R/JEVER_AUDIT.md; MAP2S/MAP_SOURCES.json'))
    table('JEVER_TERRITORIAL_AUDIT.csv',list(audit[0]),audit)
    anomalies=[]
    for sector,issue,reason in [
        ('Hoym','Bernburg-Schaumburg-Hoym cannot automatically be merged into ABG','Distinct jurisdiction and unapproved fifth-country representation; no new native matching evidence'),
        ('Ballenstedt-Harzgerode','Installed ABG interiors only; larger Harz rights unresolved','No new source/native homologues; keep PRU and Brunswick outside approved cores'),
        ('Koethen / Warmsdorf / Groebzig','Installed Warmsdorf core preserved; scattered fringe attribution incomplete','1753 tracing remains clipped to old ANH; no new boundary proof'),
        ('Zerbst / Coswig / Rosslau','AZR pre-partition core remains clipped to old ANH','Do not import 1797 partition or seize neighboring PRU by a town point'),
        ('Residual Dessau','167 ANH cells are not all certified Dessau territory','No new decisive evidence for a residual transfer'),
        ('Historical populations','Technical four-country allocations remain provisional','No comparable dated territorial count established; do not invent residents')]:
        anomalies.append(dict(Sector=sector,Status='UNRESOLVED_NOT_APPLIED',Issue=issue,Reason=reason,Installed_cells=0,Next_action='Retain limitation; no new general Anhalt campaign'))
    table('ANHALT_REMAINING_ANOMALIES.csv',list(anomalies[0]),anomalies)
    table('TERRITORIAL_CHANGES.csv',['X','Y','RGB_before','RGB_after','State_ID','Owner_before','Owner_after','Classification','Installed','Source'],[])
    pop=[]
    for p in b['inventory']['regional_pop']:
        sid,tag,culture,religion=p['key']
        if (sid=='STATE_HANNOVER' and tag=='OLD') or (sid=='STATE_ANHALT' and tag in r.TAGS) or tag=='HLB':
            pop.append(dict(State_ID=sid,TAG=tag,Culture=culture,Religion=religion,Before=p['count'],After=p['count'],Delta=0,Method='UNCHANGED_NO_TERRITORIAL_TRANSFER',Historical_estimate=False))
    table('POPULATION_BEFORE_AFTER.csv',list(pop[0]),pop)
    unresolved=[dict(ID='S01',Sector='Jever',Class='A sovereignty / C geometry',Installed=False,Issue='OLD still owns current carrier; AZR historical title established',Required_evidence='Readable 1776-compatible boundaries and at least local native coastline/river homologues; exclude Kniphausen/Varel',Arbitration='Keep OLD carriers now; direct AZR detached possession only after boundary or explicitly accepted bounded generalization, no corridor'),dict(ID='S02',Sector='Wangerooge',Class='C native placement',Installed=False,Issue='Jever island title does not prove an island footprint in the native bitmap',Required_evidence='Per-island native mask and geographic correspondence',Arbitration='No island creation or PRU transfer in MAP2S'),dict(ID='S03',Sector='Historical demographic estimate',Class='C comparable perimeter',Installed=False,Issue='No supported population for an installed Jever perimeter',Required_evidence='Dated territorial count, not town population or 1830s administrative count',Arbitration='No neighbor compensation; defer estimate until geometry'),dict(ID='S04',Sector='Market and coast',Class='RUNTIME_PENDING_FUTURE_CORRECTION',Installed=False,Issue='An eventual coastal AZR state part must be tested with distant core',Required_evidence='Installed approved territory then new-game market and sea access check',Arbitration='No artificial port, road, corridor or navy'),dict(ID='S05',Sector='Anhalt fringes',Class='C / B truncated',Installed=False,Issue='See ANHALT_REMAINING_ANOMALIES.csv',Required_evidence='New decisive local evidence only',Arbitration='Practical research stop; recommend next region without starting it')]
    table('UNRESOLVED.csv',list(unresolved[0]),unresolved)
    dump('CSV_TABLES.json',datasets)
    print('Prepared five typed audit datasets; installed changes table deliberately empty.')

def preview():
    import map2o_east_frisia as o
    b=load('BASELINE.json');bmp=core.packed(ROOT/b['bitmap_backup']);owners={p['key'][0]:p['key'][1:] for p in b['inventory']['owners']}
    box=(4270,739,4295,762)
    before=o.panel(bmp,owners,box,'AVANT - proprietes actuelles',scale=22)
    after=o.panel(core.packed(ROOT/'map_data/provinces.png'),owners,box,'APRES - aucun transfert autorise (C)',scale=22)
    im=Image.new('RGB',(before.width+after.width+18,max(before.height,after.height)+115),'white');im.paste(before,(0,0));im.paste(after,(before.width+18,0));d=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
    for i,line in enumerate(['OLD orange; PRU bleu. Les deux vues sont volontairement identiques.','xECC3B4 contient une enveloppe a subdiviser, pas une seigneurie certifiee.','Jever : titre historique AZR; position urbaine et limite native non validees.','Aucune frontiere candidate dessinee comme si elle etait etablie.']):d.text((8,before.height+9+i*25),line,font=font,fill='black')
    im.save(OUT/'JEVER_BEFORE_AFTER.png')

def validate():
    b=load('BASELINE.json');inv=core.qa.inventory();checks=[]
    def check(name,ok,detail=None):
        checks.append(dict(name=name,passed=bool(ok),detail=detail))
        if not ok:print('FAIL',name,detail,flush=True)
    now=q.economy.runtime_hashes();changes=sorted(p for p in set(now)|set(b['hashes']) if now.get(p)!=b['hashes'].get(p))
    check('All runtime files unchanged',not changes,changes)
    for k in b['inventory']:check('Full effective inventory unchanged: '+k,inv[k]==b['inventory'][k])
    check('World raster exact original SHA256',core.sha(ROOT/'map_data/provinces.png')==b['bitmap_sha256'])
    for tag,want in [('ANH',167),('ABG',23),('AKT',33),('AZR',56)]:check('Accepted Anhalt core cells '+tag,sum(x['pixels'] for x in r.load('GEOMETRY.json')['assignments'] if x['owner']==tag)==want)
    check('Accepted Anhalt 11 RGB and112 sovereign changes',len(r.load('GEOMETRY.json')['new_provinces'])==11 and sum(x['pixels'] for x in r.load('GEOMETRY.json')['assignments'] if x['owner']!='ANH')==112)
    ledger=json.loads(core.active_registry_path().read_text(encoding='utf8'));check('All521 imperial RGB rights unchanged',ledger==b['registry'] and len(ledger)==521)
    for rel,h in b['protected_files'].items():check('Prior file protected: '+rel,core.sha(ROOT/rel)==h)
    check('HEAD unchanged',subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['git_head'])
    check('Git index unchanged',core.sha(ROOT/'.git/index')==b['git_index_sha256'])
    check('No fabricated placement or transfer',load('DECISIONS.json')['native_town_pixel'] is None and not load('DECISIONS.json')['changed_cells'])
    world=sum(p['count'] for p in inv['pops']);hlb=sum(p['count'] for p in inv['regional_pop'] if p['key'][1]=='HLB')
    check('Baseline world verified and HLB9206 preserved',world==835801255 and hlb==9206)
    dump('WORLD_POPULATION_DELTA.json',dict(before=sum(p['count'] for p in b['inventory']['pops']),after=world,delta=world-sum(p['count'] for p in b['inventory']['pops']),HLB=hlb,historical_estimate_applied=False,technical_redistribution_applied=False,world_not_required_invariant=True,reason='No supported Jever perimeter, so no territorial transfer or population change.'))
    dump('IMPERIAL_REGISTRY_VALIDATION.json',dict(before=len(b['registry']),after=len(ledger),all_rights_unchanged=ledger==b['registry'],new_RGBs=0,physical_extent_unchanged=True,registry_sha256=core.sha(core.active_registry_path()),new_members=[],subject_development_untouched=True))
    result=dict(status='MAP2S_PARTIAL_JEVER_GEOMETRY_UNRESOLVED',static_status='PASS' if all(x['passed'] for x in checks) else 'FAIL',passed=sum(x['passed'] for x in checks),total=len(checks),checks=checks,runtime_files_modified=changes,installed_territorial_cells=0,installed_new_RGBs=0,MAP2R_runtime_status='PASS_RUNTIME_USER_VALIDATED',MAP2S_runtime_status='NO_NEW_RUNTIME_CHANGE_TO_TEST',engine_test_executed=False,preexisting_anomalies=dict(duplicate_RGBs=len(inv['duplicates']),invalid_references=len(inv['errors'])))
    dump('VALIDATION.json',result);print(result['static_status'],result['passed'],'/',result['total'],flush=True)
    assert result['static_status']=='PASS'

def unit_tests():
    import unittest,io,time
    groups={'MAP2S_guards':['test_map2s_jever'],'MAP2R_preservation':['test_map2r_anhalt'],'centralization_preservation':['test_hre_centralization_01'],'legacy_Q':['test_map2q_r3','test_map2q_eutin','test_map2q_r2'],'legacy_cumulative':['test_map2l_registry','test_map2m_r8','test_map2m_r9','test_map2n_island','test_map2n_completion','test_map2o_east_frisia']};results={}
    for name,modules in groups.items():
        start=__import__('time').monotonic();stream=io.StringIO();result=unittest.TextTestRunner(stream=stream).run(unittest.TestLoader().loadTestsFromNames(modules))
        results[name]=dict(modules=modules,tests=result.testsRun,failures=[t.id() for t,_ in result.failures],errors=[t.id() for t,_ in result.errors],output=stream.getvalue(),seconds=round(time.monotonic()-start,2),engine_test=False)
        print(name,result.testsRun,'tests',len(result.failures),'failures',flush=True)
    previous=json.loads((ROOT/'docs/reports/hre/HRE_CENTRALIZATION_01/UNIT_TESTS.json').read_text(encoding='utf8'))['groups']
    known={x for g in previous.values() for x in g['failures']}
    failures={x for g in results.values() for x in g['failures']};new=sorted(failures-known)
    dump('UNIT_TESTS.json',dict(groups=results,known_preexisting_failure_ids=sorted(known),new_failure_ids=new,engine_test_executed=False))
    assert not new and not any(g['errors'] for g in results.values())

def reports():
    v=load('VALIDATION.json');files={}
    files['REPORT.md']=f'''# MAP-2S — Jever et arrêt pratique d’Anhalt

Date historique : 1er janvier 1776. Relevé : 17 octobre 2026.

**Statut : MAP2S_PARTIAL_JEVER_GEOMETRY_UNRESOLVED. Jever n’est pas corrigée.**

## Résultat

La validation manuelle de MAP-2R est enregistrée de façon additive dans `MAP2R_RUNTIME_USER_VALIDATION.json`, à partir de l’acceptation explicite du prompt MAP-2S. Aucune durée de simulation n’est déduite. Aucun ancien rapport ni baseline n’est réécrit et aucun test moteur automatisé n’est revendiqué.

Zéro cellule transférée, zéro nouveau RGB, aucun fichier fonctionnel modifié. Les cinq enveloppes OLD de STATE_HANNOVER restent OLD. Le titre historique de Jever est AZR, pas OLD, PRU ou RUS en1776. Cette anomalie demeure ouverte : la conservation n’est pas une attribution historique validée.

Les nouvelles reproductions du musée (vers1725, frontière1745/46,1798) permettent de distinguer Jever, Kniphausen et les territoires voisins. Elles ne permettent pas encore de placer leurs limites de façon défendable dans le littoral simplifié du jeu. La pièce1798 est postérieure au changement de souverain1793 et n’est pas utilisée seule comme preuve1776. Le catalogue haute définition d’Oldenburg renvoie une vérification de navigateur ; aucune image haute définition n’a été obtenue. Il ne faut ni agrandir les petites images en prétendant gagner du détail, ni attribuer toute xECC3B4 à Zerbst, ni choisir arbitrairement son quart nord-ouest.

L’aperçu avant/après est volontairement identique. `TERRITORIAL_CHANGES.csv` contient son en-tête sans transfert. Les autres CSV séparent les enveloppes d’investigation des modifications installées. Aucun faux contour « prêt à appliquer » n’est livré.

## Anhalt

Les noyaux acceptés ANH167 / ABG23 / AKT33 / AZR56, les112 changements de souveraineté et les11 RGB de MAP2R sont conservés. Hoym, les franges du Harz, Köthen et Zerbst–Coswig–Roßlau n’ont pas de preuve locale nouvelle déterminante. Hoym ne doit pas être fusionnée automatiquement avec Bernbourg ; la partition1797 n’est pas rétroprojetée. Ces limites sont maintenues sans prolonger la recherche générale. Anhalt est arrêté pratiquement, pas déclaré historiquement exhaustif.

## Conservation et contrôles

{v['passed']}/{v['total']} contrôles de conservation réussis. Tous les fichiers fonctionnels, propriétaires, State_ID, populations/profils, bâtiments, PM, propriétés économiques, ressources, infrastructures, unités et pactes sont identiques au début de MAP-2S. Les fichiers antérieurs protégés sont vérifiés par empreintes. Les futurs sujets impériaux, leurs icônes et leur prototype ne sont pas modifiés.

Population mondiale835801255 ; HLB9206. Aucun chiffre historique de Jever n’est installé sans périmètre comparable, aucune compensation voisine. Les44 doublons RGB et12 références invalides préexistants sont inchangés. Les dix échecs anciens de snapshots sont conservés et distingués des nouvelles régressions dans UNIT_TESTS.json.

Aucun commit, merge, reset, push, changement de branche ou modification d’index. Aucun fichier de l’installation du jeu écrit. Les tests en cours du joueur sur HRE-CENTRALIZATION restent une validation distincte, non présumée acquise ici.

## Suite

Une seule région recommandée : Saxe et principautés thuringiennes hors Erfurt–Eichsfeld, STATE_SAXONY73. Elle n’est pas commencée. Voir NEXT_HRE_REGION_RECOMMENDATION.md et l’arbitrage détaillé de JEVER_HISTORICAL_EVIDENCE.md.

ColGrep : une tentative refusée sur le verrou d’index, puis un appel local abouti ; les trois pistes retournées sont vérifiées. Il confirme les fichiers utiles, sans fournir de géométrie nouvelle. Aucune économie exacte de quota mesurée.
'''
    files['JEVER_HISTORICAL_EVIDENCE.md']='''# Jever — preuves acquises et géométrie manquante

## Corpus ciblé, pas de reprise générale

- [NLA OL Best90](https://www.arcinsys.niedersachsen.de/arcinsys/showFondsDetails?fondsId=2640) : autorité d’Anhalt-Zerbst1667–1793 et fonds de l’administration de Jever. Forte preuve de souveraineté, pas un contour raster.
- [Archives urbaines Dep25JEV](https://www.arcinsys.niedersachsen.de/arcinsys/showFondsDetails.action?fondsId=2873&request_locale=en) : portée urbaine à distinguer de toute la seigneurie.
- [Schlossmuseum Jever, cartes et plans](https://www.schlossmuseum.de/sammlungen/virtuelle-sammlungen/regionalgeschichte/landkarten-und-plaene/) : Königshaven vers1725 Ka92 ; limite Wittmund–Jever1745/46 Ka226 ; Kunstenbach1798 Ka94. Six reproductions avec empreintes dans MAP_SOURCES.json. La carte1798 montre une souveraineté russe postérieure, pas celle1776.
- Coldewey/Homann1730 déjà conservée dans MAP2P/COLDEWEY_1730.png et sa provenance : grandes distinctions Jever/Kniphausen/Oldenburg, pas de transformation locale indépendante validée.
- MAP2R/JEVER_AUDIT.md, MAP2O/JEVER_VAREL_KNIPHAUSEN_AUDIT.md et MAP2P : exclusions déjà établies, réutilisées sans écraser leurs baselines.
- [NLA, catalogue Jever](https://www.arcinsys.niedersachsen.de/arcinsys/list.action?nodeid=g182576&page=1) : Siebeck1777 Best298Z31 identifié au catalogue. Notice seule, image non obtenue, aucune frontière extraite.

## Localisation et juridictions

Jever est dans l’ensemble côtier Jeverland, à l’ouest de la Jade et au nord d’Oldenburg. Les cartes distinguent Wangerland, Östringen et les secteurs de Rüstringen ; Kniphausen reste distincte. Les droits Bentinck et Varel ne deviennent pas automatiquement des possessions de Zerbst. Wangerooge est un problème séparé de correspondance insulaire. Ni Wilhelmshaven1853, ni la Russie1793, ni l’intégration à Oldenburg1818 ne sont rétroprojetées.

Le bitmap8192×3616 contient les grandes enveloppes OLD xECC3B4 (184 cellules) et xC00161 (229), STATE_HANNOVER69. Leurs bornes et les trois fragments OLD plus méridionaux sont relevés dans le CSV. Ce sont des transporteurs techniques d’investigation et non des provinces historiques de Jever. Aucun pixel unique de centre urbain de Jever n’est certifié. La position d’un bâtiment ou un profil baltique/thuringien hors domaine n’a pas été employé.

Le seul locator inventorié dans la fenêtre locale est le port de STATE_ELBE58, en RGB BRE x68BE66, X4286.373535/Y742.575195. Ce locator n’est ni un port de Jever ni une preuve de sa frontière. Aucun hub/locator n’est déplacé. OLD conserve146803 habitants de sa subdivision économique69 ; AZR conserve30687 dans son noyau62. Ces chiffres sont techniques, pas la population historique de Jever.

## Pourquoi C et non B

Une généralisation B est autorisée par le prompt, mais doit rester fondée sur une juridiction identifiable dans le raster. Les images obtenues sont petites (420×500,375×528 et813×500 pour les trois vues complètes) ; la limite sud et l’exclusion Kniphausen ne peuvent pas être transposées de manière vérifiable. Le littoral natif schématise la Jade et les terres endiguées. Aucun jeu de repères homologues indépendant n’est présent. Déplacer sept pixels, couper une moitié ou prendre un petit noyau nord-ouest donnerait une règle numérique sans preuve supplémentaire. Cela resterait C, même avec un tracé visuellement propre.

## Arbitrage opérationnel

Conserver les transporteurs OLD pour cette passe. Reprendre seulement avec une image lisible de Ka92 / Siebeck1777 / Ka94, une comparaison de la frontière avec la pièce1745/46, et des repères physiques locaux explicitement identifiés côté source et bitmap. Délimiter alors un noyau généralisé en excluant Varel/Kniphausen, mesurer l’incertitude sans prétention cadastrale, puis créer une possession éloignée directe AZR sans corridor ni pays indépendant.

Il faut ensuite répartir la démographie par un périmètre comparable : donnée historique datée si disponible, sinon redistribution déterministe. Tester marché, capacité portuaire réelle et accès maritime sans créer artificiellement des bâtiments. Aucun correctif géométrique n’est implicitement autorisé par ce rapport.
'''
    files['NEXT_HRE_REGION_RECOMMENDATION.md']='''# Prochain secteur unique : Saxe et principautés thuringiennes, hors Erfurt–Eichsfeld

**STATE_SAXONY, ID73 ; aucun travail commencé.**

Les inventaires MAP2M/R9/HRE_REGIONS_INVENTORY.csv et sa progression indiquent ce secteur RESEARCHED_ONLY. La mise à jour MAP2Q/R3/HRE_REGIONS_INVENTORY_UPDATED.csv conserve cette distinction. Les rapports territoriaux ultérieurs MAP2N–MAP2R concernent d’autres régions : Wismar/Poel/Neukloster, Frise, Eutin/Schwartau, puis Anhalt. Ils ne constituent pas une reconstruction de la Saxe. Les recommandations de R9 sur Wismar et celles ultérieures sur Eutin/Anhalt sont désormais dépassées par les lots acceptés et ne sont pas répétées.

Pays présents à contrôler : SAX, COB, MEI, WEI et SCW. Identifier d’abord la portée exacte de SCW, sans confondre son TAG avec un inventaire complet des Schwarzbourg. Vérifier les principautés ernestines et leurs possessions de1776, l’électorat de Saxe, les petits domaines et enclaves non distincts. Le regroupement de1836 et des partages postérieurs ne constitue pas une frontière1776. L’ajout franconien à Cobourg ne valide pas tout son territoire thuringien.

Sources déjà retenues : R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv, entrées0049–0053 pour les cinq TAGs et source0016 (Freeman/Bury1780). Leur faible précision pour les propriétaires détaillés reste explicite. Les atlas conservés donnent une première base de localisation ; aucune correction n’est promise à partir du seul TAG. Choisir ensuite un sous-secteur bien documenté plutôt qu’une reconstruction de tous les micro-États à la fois.

Problèmes connus : fragmentation, souverainetés et propriétés non équivalentes, correspondance des centres urbains incertaine, profils démographiques régionaux grossiers. Exclure le dossier gelé Erfurt–Eichsfeld et préserver les noyaux Anhalt, les lots franconiens et les mécanismes impériaux. Rien de cela n’est modifié dans MAP-2S.

Ce choix suit la recommandation MAP2R après l’acceptation manuelle de ses noyaux. Il ne dépend pas de la résolution de chaque frange de Jever ou du Harz et évite de recommander à nouveau un secteur déjà validé.
'''
    files['RUNTIME_TEST_PLAN.md']='''# Contrôle en jeu

Aucun nouveau fichier fonctionnel n’est modifié par MAP-2S. Il n’y a donc pas de nouvelle frontière installée à certifier. Jever reste OLD et doit être signalée comme anomalie, pas comme correction réussie.

La validation MAP-2R fournie par le joueur est conservée dans une attestation additive. Aucune durée n’est inventée. Les essais HRE-CENTRALIZATION en cours constituent un autre lot ; ce rapport ne les déclare pas réussis.

Après une future correction approuvée de Jever seulement : nouvelle partie1776 ; vérifier AZR au noyau et sur la côte sans corridor, limites OLD/PRU/Kniphausen/Varel, capitales, populations/profils, marchés de la possession éloignée, accès à la mer et ports réellement existants. Vérifier OLD–HLB et9206 habitants, armées, PM, bâtiments et registre ; laisser ensuite simuler et noter la durée réellement testée. Ne pas promouvoir le dossier C actuel en READY_FOR_RUNTIME_VALIDATION.
'''
    q.core.OUT=OUT;q.core.emit({(OUT/n).relative_to(ROOT).as_posix():s for n,s in files.items()},'REPORTS.patch')
    print('Four reports prepared as patch; no runtime patch emitted.')

if __name__=='__main__':globals()[sys.argv[1]]()
