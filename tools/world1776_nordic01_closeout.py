"""Reports, data map, user receipt and isolated WORLD tracking for NORDIC-01."""
import json,shutil
from collections import Counter
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import world1776_nordic01 as n
ROOT=n.ROOT;LOT=n.LOT;WORLD=n.WORLD
USER="Je relançais tous les contrôles passe. L'Afrique est terminée pour le moment. Passe à la Scandinavie, en comptant la Finlande. On n'a pas encore fait la région."
TRACK=['ROADMAP.md','ROADMAP_STATE.json','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','OWNERSHIP_BOUNDARIES.md','CONCURRENT_CHANGES.json']
def write(p,text):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(text.encode('utf8'))
def evidence():
    n.save('USER_REQUEST.json',dict(date='2026-10-29',source='Direct message in this chat',verbatim=USER,
        scope='Scandinavia including Finland; territorial cartography and necessary ownership initialization only',
        excluded=['SERG possessions and tracking','American and overseas Scandinavian colonial revisions','characters/flavour','economic refinement','cosmetic border smoothing']))
    n.save('AFRICA_USER_ACCEPTANCE.json',dict(date_received='2026-10-29',source='Direct message in this chat',verbatim=USER,
        interpretation='User reports all grouped African controls pass and accepts Africa for now; explicitly authorizes transition to Scandinavia including Finland.',
        status='USER_REPORTED_PASS_GROUPED_AFRICA',previous_issue_receipt='../AFRICA-POLITY-FIX-01/USER_FINDINGS.json',
        expected_latest_delivery='../AFRICA-POLITY-FIX-01/DELIVERY_MANIFEST.json',
        exact_game_version=None,mod_fingerprint_tested=None,game_start_date=None,simulation_duration=None,save_reload_confirmed=None,
        acceptance_is_historical_total_closure=False,full_canonical_V_criterion_credit=False,
        remaining_limits='Documented basemap, population proxies and deferred content remain; no fictional observation added.'))
    rows=n.load('TERRITORIAL_INVENTORY.json')
    archive=LOT/'INITIAL_TERRITORIAL_INVENTORY.json'
    if not archive.exists():shutil.copy2(LOT/'TERRITORIAL_INVENTORY.json',archive)
    _,pops=n.demographics();cat=n.b.a.catalog('map_data/state_regions')
    # Repair a reporting-only owner-key extraction mistake and add Uusimaa,
    # whose native name differs from the survey's initial generic label.
    img=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32)
    packed=img[:,:,0]*65536+img[:,:,1]*256+img[:,:,2]
    if not any(r['state']=='STATE_UUSIMAA' for r in rows):
        reg,path=cat['STATE_UUSIMAA'];cells=[];crop=packed[400:580,4480:4780]
        for c in n.b.a.ids(reg,'provinces'):
            c=c.strip('"');yy,xx=np.where(crop==int(c[1:],16));xx+=4480;yy+=400
            assert len(xx)
            cells.append(dict(rgb=c,owners=n.load('BEFORE.json')['inventory']['owners'].get(c,[]),pixels=len(xx),bbox=[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())],center=[float(xx.mean()),float(yy.mean())]))
        rows.append(dict(state='STATE_UUSIMAA',file=path.relative_to(ROOT).as_posix(),hubs={k:reg.one(k) for k in ['city','port','farm','mine','wood']},provinces=cells))
    before=n.owner_map(n.b.a.raw(LOT/'apply_inputs'/n.STATES));after=n.b4.inventory()['owners']
    for r in rows:
        sid=r['state'];counts=Counter(t for c in r['provinces'] for s,t in before.get(c['rgb'],[]))
        countsafter=Counter(t for c in r['provinces'] for s,t in after.get(c['rgb'],[]))
        r['parts_before']=[dict(owner=t,province_count=v) for t,v in counts.items()]
        r['parts_after']=[dict(owner=t,province_count=v,population=pops[sid,t]) for t,v in countsafter.items()]
        r.pop('parts',None)
    n.save('TERRITORIAL_INVENTORY.json',rows)
    n.save('INVENTORY_REPORTING_REPAIR.json',dict(functional_writes=0,archived_initial='INITIAL_TERRITORIAL_INVENTORY.json',
        corrected='region_state:TAG extraction used the wrong substring, showing zero populations; effective key parsing is now explicit.',
        added_native_name='STATE_UUSIMAA',state_count=len(rows)))
    n.save('FILES_DELIVERED.json',n.load('FILES_MODIFIED.json'))
    # All African owners, including the latest polity fix, must be preserved.
    africa=[]
    for path in n.b.tech.effective('map_data/state_regions'):
        if path.name not in ['03_north_africa.txt','04_subsaharan_africa.txt']:continue
        for reg in n.b.parse(n.b.a.raw(path)):
            for c in n.b.a.ids(reg,'provinces'):
                c='x'+c.strip('"')[1:].upper();africa.append(c)
    bad=[c for c in africa if before.get(c)!=after.get(c)]
    n.save('AFRICAN_NON_REGRESSION.json',dict(status='PASS' if not bad else 'FAIL',RGBs_checked=len(set(africa)),ownership_changes=bad,
        population_files_unchanged=True,polity_definitions_unchanged=True,comparison='Immediate preimage and final composed workspace; file protection validation covers definitions/POP.'))
    assert not bad
    print('Evidence refreshed:',len(rows),'Nordic/contact regions;',len(set(africa)),'African RGBs preserved.')

def map_image():
    owners=n.b4.inventory()['owners'];raw=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32)
    packed=raw[:,:,0]*65536+raw[:,:,1]*256+raw[:,:,2]
    lut=np.zeros((1<<24,3),dtype=np.uint8);lut[:]=[221,233,239]
    palette={'SWE':(228,190,84),'DENNOR':(197,106,100),'RUS':(127,172,124)}
    for c,p in owners.items():lut[int(c[1:],16)]=palette.get(p[0][1],(211,209,199))
    font=lambda z:ImageFont.truetype('C:/Windows/Fonts/arial.ttf',z)
    canvas=Image.new('RGB',(1560,1310),'#f6f3eb');d=ImageDraw.Draw(canvas)
    d.text((34,24),'Scandinavie et Finlande - 1er janvier 1776',font=font(32),fill='#252c32')
    d.text((34,68),'NORDIC-01 | Proprietaires installes, limites tracees sur les provinces du jeu',font=font(18),fill='#4f5860')
    def panel(box,size,at,borders=False):
        x0,y0,x1,y1=box;a=packed[y0:y1,x0:x1];pic=lut[a].copy()
        if borders:
            ed=np.zeros(a.shape,dtype=bool);ed[1:]|=a[1:]!=a[:-1];ed[:,1:]|=a[:,1:]!=a[:,:-1];pic[ed]=(115,120,113)
        for r in n.PLAN:
            for c in r['rgb']:pic[a==int(c[1:],16)]=(91,77,141)
        canvas.paste(Image.fromarray(pic).resize(size,Image.Resampling.NEAREST),at)
        return lambda x,y:(at[0]+(x-x0)*size[0]/(x1-x0),at[1]+(y-y0)*size[1]/(y1-y0))
    xy=panel((4150,55,4960,919),(900,960),(28,115))
    for x,y,label in [(4500,445,'SUEDE'),(4370,460,'NORVEGE'),(4720,365,'FINLANDE'),(4370,682,'DANEMARK'),(4900,430,'RUSSIE')]:
        px,py=xy(x,y);d.text((px,py),label,font=font(17),fill='#343b40',stroke_width=2,stroke_fill='#f6f3eb')
    for x,y,label in [(4750,478,'1'),(4770,187,'2')]:
        px,py=xy(x,y);d.ellipse((px-15,py-15,px+15,py+15),fill='#51406d',outline='white',width=2);d.text((px-6,py-11),label,font=font(19),fill='white')
    d.text((966,120),'1 - Savonlinna / Nyslott',font=font(22),fill='#292e35')
    panel((4669,447,4811,533),(545,330),(968,162),True)
    for x,y,line in [(968,506,'Province transferee : Suede -> Russie.'),(968,533,'Cession de 1743 ; contour natif conserve.')]:d.text((x,y),line,font=font(17),fill='#414b52')
    d.text((966,606),'2 - Neiden / Pasvik',font=font(22),fill='#292e35')
    panel((4705,140,4845,225),(545,330),(968,647),True)
    for i,line in enumerate(['Quatre provinces des districts communs.', 'Proprietaire moteur : Russie, pour la juridiction.', 'Fiscalite danoise-norvegienne superposee :', 'limite documentee du modele a un proprietaire.']):d.text((968,992+i*26),line,font=font(16),fill='#414b52')
    for i,(tag,text) in enumerate([('SWE','Suede'),('DENNOR','Danemark-Norvege'),('RUS','Russie')]):
        x=40+i*280;d.rectangle((x,1130,x+24,1154),fill=palette[tag]);d.text((x+34,1127),text,font=font(20),fill='#30363b')
    d.rectangle((940,1130,964,1154),fill=(91,77,141));d.text((974,1127),'Provinces corrigees',font=font(20),fill='#30363b')
    for i,line in enumerate(['Islande et Feroe : conservees au Danemark-Norvege, hors cadre de cette vue.', 'La majeure partie de la Finlande reste suedoise ; la Vieille Finlande est russe.', 'Sources : Wetterstedt (1775), Merovuo (2017), NOU 1994:21. Approximation de provinces ; test moteur non execute.']):
        d.text((38,1192+i*30),line,font=font(17 if i<2 else 15),fill='#505961')
    canvas.save(LOT/'CARTE_REPERES.png')
    print('Map rendered.')

def reports():
    v=n.load('VALIDATION.json');pop=n.load('POPULATION_LEDGER.json')
    write(LOT/'SOURCES.md','''# NORDIC-01 — Sources effectivement consultées

Référence : 1er janvier 1776. Consultation le 29 octobre 2026. Les cartes servent à établir l'autorité et les repères ; la correspondance avec les RGB est notre interprétation documentée, pas un cadastre mesuré.

1. **Eric Wetterstedt, Charta öfwer Finland, 1775**, université de Jyväskylä, item56012, URN:NBN:fi:jyu-200910204001. [Notice et original](https://expo.oscapps.jyu.fi/s/vanhakartta/item/56012). Original téléchargé et examiné : sources/Wetterstedt1775_Finland.jpeg (7235×11358). Feuilles contemporaines [Etelä-Savo](https://expo.oscapps.jyu.fi/s/vanhakartta/item/55947), [Karjala](https://expo.oscapps.jyu.fi/s/vanhakartta/item/55971), 1775, également examinées (copies sources/). Frontière suédo-russe, continuité de la Finlande suédoise ; ne décrit pas le Grand-Duché russe de1809. Une ligne d'atlas de1775 ne certifie pas tous les villages.
2. **Jenni Merovuo**, « ‘Divided and validated’? The institutionalization of the Russo-Swedish border region in the1743 peace treaty », Hungarian Geographical Bulletin66(4), 2017, p283–293, DOI10.15201/hungeobull.66.4.1. [Éditeur](https://ojs.mtak.hu/index.php/hungeobull/article/view/686) ; [numéro PDF consulté](https://hungarian-geography.hu/konyvtar/kiadv/HunGeoBull2017/HunGeoBull_66_4.pdf), copie sources/Merovuo_2017_issue.pdf. Pages286–289 et **figure1 p289** lues ; figure rendue sources/Merovuo_figure1.png. Nyslott cédée avec un périmètre défensif de deux milles suédois ; frontières locales et zones contestées de Kerimäki non entièrement résolues. Ce périmètre ne coïncide pas exactement avec la province du jeu.
3. **Archives nationales de Finlande**, [Vanha Suomi](https://portti.kansallisarkisto.fi/arkistojen-portti/vanha-suomi), section de définition : acquisitions1721/1743, administration de Viipuri, réunion au Grand-Duché en1812. Confirme que la Vieille Finlande russe ne comprend pas toute la Finlande suédoise.
4. **Gouvernement norvégien, NOU1994:21**, [ch3, section3.5](https://www.regjeringen.no/no/dokumenter/nou-1994-21/id374516/?ch=3), «Grensekonvensjonen med Russland.1826». Texte consulté : districts communs Neiden/Pasvik/Petsjenga après1751, situés au sud du Varangerfjord ; juridictions séculière/ecclésiastique russes et perception fiscale norvégienne superposée. **Ne prouve pas une souveraineté russe exclusive.** Quatre polygones méridionaux natifs sont choisis comme approximation du contrôle juridictionnel ; franges de Neiden et siida saisonnières non cadastrées.
5. **Convention de1826, préambule et art1–3**, [texte primaire reproduit dans Lovdata](https://lovdata.no/dokument/TRAKTAT/traktat/1826-05-14-1). Délimitation définitive postérieure, districts communs antérieurs, maintien de la ligne1751 dans son ressort. [NOU2009:20, section sur les frontières](https://www.regjeringen.no/no/dokumenter/nou-2009-20/id576868/?ch=4) confirme l'origine1751 de la frontière Suède–Norvège/Finlande. La ligne1826 ne doit pas être projetée en1776.
6. **Rigsarkivet**, [guide Danske Kancelli, sections1771–1773 et territoires particuliers](https://www.rigsarkivet.dk/vejledning/danske-kancelli-kom-godt-i-gang/) ; **Nationalmuseet**, [De nordatlantiske områder](https://natmus.dk/historisk-viden/temaer/genstande-af-enestaaende-betydning/genstande-fra-danmarks-nyere-tid-1660-2000/toej/). Administration de la monarchie composite et îles nord-atlantiques ; aucun nouveau pays NOR/FIN/ICE indépendant installé. Les institutions fines sont hors de cette refonte.

## Réutilisation et limites

Les recommandations MAP1 R2-0088/0092/0093/0107/0108/0152/0154/0155/0157 ont été relues comme pistes, sans reprendre leurs propriétaires comme preuve. La carte d'Homann signalée par la Ville d'Helsinki constitue un contexte supplémentaire ; son record Finna était inaccessible et n'est pas présenté comme une image effectivement consultée. Le téléchargement direct non privilégié échouait sur la résolution DNS ; les copies publiques ont été obtenues avec l'accès réseau approuvé. Aucune modification des sources originales.

Les hubs du jeu (notamment Savonlinna xB81268) ne constituent que des ancres techniques. Géométrie, voisinages et sources historiques ont été rapprochés. Le rapport expose les approximations politiques et démographiques restantes. Aucune frontière interne moderne, ferme précise, personnage ou tribu supplémentaire n'est inventé.
''')
    write(LOT/'REPORT.md',f'''# NORDIC-01 — Scandinavie et Finlande

**29 octobre2026 ; référence1er janvier1776. IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION.** Autorisation directe dans USER_REQUEST.json. Le joueur déclare le test africain groupé passé et l'Afrique terminée pour le moment ; reçu borné AFRICA_USER_ACCEPTANCE.json. Cette acceptation lève la transition, sans inventer durée/version/rechargement ni certification historique totale.

## Corrections installées

**Cinq RGB existants, trois fichiers ciblés ; aucun pixel redessiné, nouveau TAG ou territoire SERG.**

| Secteur | RGB | Avant | Après | Portée |
|---|---|---|---|---|
| Savonlinna/Nyslott | xB81268 | SWE | RUS | Cession1743 ; polygone natif entier, pas périmètre cadastral du château |
| Sud du Varangerfjord, Neiden/Pasvik | x2495FE, xFEC50D, x7005BB, x6480A4 | DENNOR | RUS | Approximation de la juridiction russe dans les districts communs, pas annexion exclusive ni suppression attestée des droits danois-norvégiens |

Les deux ensembles touchent directement un territoire russe conservé. La côte nord du Varangerfjord reste danoise-norvégienne. La majorité de la Finlande, Åland, la Suède proprement dite et Gotland restent suédoises ; la Vieille Finlande demeure russe. Norvège, Danemark, Islande et Féroé restent dans DENNOR. Les contacts du Schleswig-Holstein, Poméranie/Wismar/Poel sont réservés au SERG. Les colonies et le Groenland ne sont pas repris sous cette autorisation.

## Populations et capacités

Monde **{pop['world_before']:,} → {pop['world_after']:,}**, delta0. Kuopio : SWE160946→155916 et RUS0→5030. Norvège septentrionale : DENNOR233686→226658 et RUS0→7028. Total réaffecté12058 ; aucune assimilation ni variation mondiale, cohortes culture/religion/profession conservées.

La ventilation par1/32 et4/133 des pools donne uniquement une allocation technique, arrondie séparément par cohorte ; ce n'est pas une estimation démographique1776. Les populations héritées, notamment majoritairement norvégiennes dans le secteur septentrional, restent des proxies et ne certifient pas le peuplement des siida. Les effectifs historiques fins sont différés.

Institutions, lois, capitales nationales, technologies, PM, niveaux bâtis, recettes et unités inchangés. Aucun nouveau pays à initialiser. Le seul centre agricole natif nommé Savonlinna change de propriétaire territorial ; les bâtiments existants restent aux portions conservées. Les hubs et ressources partagés de région moteur demeurent un compromis à observer ; aucune rentabilité ni localisation physique exacte n'est attestée.

## Sources et incertitudes

[SOURCES.md](SOURCES.md) distingue documents réellement lus, données, interprétation et lacunes. Carte Wetterstedt1775, Merovuo2017 p286–289 et fig1, Archives nationales finlandaises, NOU1994:21 §3.5 et convention1826. Savonlinna : contour natif plus large que le rayon historique ; poches contestées de Kerimäki non représentées. Nord : le moteur a un propriétaire unique, ne reproduit pas les fiscalités superposées ou tous les usages sámi ; limite occidentale/siida approximative. Pas de nouveau TAG artificiel ni frontière arbitraire au pixel. Courbes volontairement non lissées.

## Contrôles et concurrence

**{v['passed']}/{v['total']} contrôles statiques réussis**, VALIDATION.json. Syntaxe, patch exact, extérieur des scopes inchangé, cinq affectations uniques, connexion directe à la Russie, conservation des cohortes/totaux et Git/index. La première exécution28/30 reste INITIAL_VALIDATION.json : deux échecs venaient de la comparaison avec la capture d'avant l'installation indienne concurrente ; ils n'ont pas été masqués par une restauration. La normalisation des clés RGB minuscules a ensuite été corrigée dans le comparateur des préimages. Les entrées et sorties du pair sont vérifiées exactement, sans exemption générale.

Le contrat technologique courant SWE/DENNOR/RUS a également été exécuté (TECH_CURRENT.json). **FAIL_STATIC hérité**, pas validation de leurs profils historiques : trois demandes de lois sans gate par pays pour SWE/DENNOR et gate de recrutement des cuirassiers russes. Les mêmes entrées nationales, lois, technologies et unités sont inchangées dans notre lot ; aucun grant n'est distribué pour les masquer. Deux avertissements de ressources et les réserves historiques restent séparés des erreurs de frontière. Ce contrat ne prouve ni loi effectivement active ni panne d'unité existante.

Le lot **DURRANI_PUNJAB_1776/DP-02** a installé81 réattributions et42 sorties pendant cette passe. Manifestes, préimages et sorties relus ; états nordiques identiques dans ses versions, puis notre patch appliqué sur son état courant. Dix fichiers fonctionnels existants modifiés extérieurement sont rapprochés de ses reçus, nouvelles sorties également contrôlées. EXTERNAL_COMPOSITION_REVIEW.json conserve les preuves. Aucune écriture de ses fichiers ou suivis. Afrique entière, Amériques, Arabie, SERG, TECH-R1/R2/R3 et ECON-ALLOYS/quincaillerie préservés. Aucun Git/vanilla/SERG écrit.

## Suite

Cette passe livre les deux corrections défendables trouvées dans les19 régions et contacts examinés. Carte de repères CARTE_REPERES.png. Contrôle moteur groupé de la Scandinavie encore NOT_RUN : nouvelle partie1776, propriétaire des deux repères, Åland et Finlande suédoises, côte nord du Varangerfjord DENNOR, population/chargement des portions RUS, puis simulation et sauvegarde/rechargement lors du test groupé. Pas de demande de test par sous-lot.

L'Afrique est acceptée pour le moment par le joueur. Extension documentaire WORLD1.0.2 pour la Scandinavie hors de l'ancien registre à320 critères : aucune progression artificielle ni nouveau dénominateur SERG. Le calcul historique WORLD reste10/320 (3,13%) ; aucun critère V entier nouveau certifié à partir d'un retour global sans détails.
''')
    write(LOT/'REPRODUCE.md','''# Reproduire les contrôles

Python du runtime Codex, PYTHONIOENCODING=utf-8 :

`python tools/world1776_nordic01.py --validate`

Ne pas rejouer --survey, --apply ou --tracking. Les préimages sont celles du workspace courant au moment de la mutation, incluant DP-02. Le validateur exige les sorties exactes du manifeste DP-02 archivé ; si elles changent, lire les nouveaux reçus plutôt que désactiver la protection. --inspect est un outil de travail, pas une attestation de rendu moteur.

`world1776_nordic01_closeout.py --evidence --map --reports --final` actualise les preuves dérivées ; cette commande ne lance pas le jeu.
''')
    print('Reports written.')

def tracking():
    assert not (LOT/'TRACKING_PATCHES.json').exists(),'Tracking already recorded.'
    old={k:n.b.a.raw(WORLD/k) for k in TRACK};sha={k:n.b.a.sha(WORLD/k) for k in TRACK}
    for k in TRACK:
        p=LOT/'tracking_inputs'/k;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(WORLD/k,p)
    state=json.loads(old['ROADMAP_STATE.json']);state['scope_version']='1.0.2'
    acceptance='NORDIC-01/AFRICA_USER_ACCEPTANCE.json'
    for phase in state['phases']:
        if phase['id']=='P3':
            phase['status']='CARTOGRAPHIC_PASS_ACCEPTED_BY_USER_FOR_NOW'
            phase['grouped_user_acceptance']=dict(receipt=acceptance,date='2026-10-29',full_historical_closure=False,full_V_credit=False)
    state['scope_amendments'].append(dict(version='1.0.2',date='2026-10-29',authority='NORDIC-01/USER_REQUEST.json',
        change='Explicit Scandinavian/Finnish territorial pass added as auxiliary scope outside the legacy five-phase scoring register; African grouped pass accepted for now.',criteria_total_unchanged=320))
    state['steering_history'].append(state['current_steering'])
    state['current_phase']='NORDIC_AUXILIARY'
    state['current_steering']=dict(date='2026-10-29',authority='NORDIC-01/USER_REQUEST.json',last_lot='NORDIC-01',scope='Scandinavia including Finland, territorial boundaries and necessary POP reassignment',next_pass='Grouped Nordic runtime verification; documented fine-border limits only, no automatic new region',runtime_validation_timing='GROUPED_NORDIC',intermediate_player_tests_requested=False,full_V_credit=False)
    state['phase_transition_gate']=dict(source='NORDIC-01/USER_REQUEST.json',explicit_transition_authorized=True,
        rule='User reports African checks passed and explicitly requests Scandinavia including Finland.',authorized_next_phase='NORDIC_AUXILIARY',
        African_user_acceptance=acceptance,authorization_is_full_canonical_V_validation=False,partial_lot_tests_requested=False)
    state['lots'].append(dict(id='NORDIC-01',date='2026-10-29',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',
        auxiliary_scope_outside_legacy_denominator=True,native_RGBs_transferred=5,existing_files_modified=3,population_delta=0,new_TAGs=0,
        receipt='NORDIC-01/FILES_DELIVERED.json',runtime='NOT_RUN',credited_criteria=[]))
    assert state['progress']['technical_verified']==10 and state['progress']['criteria_total']==320
    entry='\n\n## 29 octobre2026 — Afrique acceptée ; NORDIC-01 installé\n\nLe joueur déclare tous les contrôles africains passés, accepte l’Afrique pour le moment et autorise explicitement Scandinavie/Finlande. Reçu NORDIC-01/AFRICA_USER_ACCEPTANCE.json : aucun détail de version, durée ou rechargement ajouté. Les anciennes limites historiques et le lissage différé subsistent ; pas de V entier ou clôture flavor inventés.\n\nNORDIC-01 : Savonlinna suédoise→russe après la cession1743 ; quatre provinces des districts communs Neiden/Pasvik rattachées au propriétaire moteur russe pour la juridiction séculière/ecclésiastique, fiscalité danoise-norvégienne superposée non reproduite. Cinq RGB existants, trois fichiers ciblés,12058 habitants réaffectés sans variation mondiale (837328654). Ni pixel, nouveau pays, bâtiment, PM, technologie ni institution ajouté. Tracés natifs approximatifs, pas de souveraineté exclusive certifiée au nord. 33/33 statiques, aucun test moteur nordique ; DP-02 concurrent préservé et rapproché de ses manifestes.\n\nExtension documentaire1.0.2 pour ce secteur auxiliaire, hors du registre historique320 critères ; progression calculée10/320 inchangée. Rapport NORDIC-01/REPORT.md, carte CARTE_REPERES.png ; prochaine étape : contrôle nordique groupé, pas autre région automatique.\n'
    out=dict(old);out['ROADMAP_STATE.json']=json.dumps(state,ensure_ascii=False,indent=2)+'\n'
    for k in ['ROADMAP.md','PROGRESS_HISTORY.md']:out[k]=old[k]+entry
    out['BLOCKERS.md']=old['BLOCKERS.md']+'\n\n## 29 octobre2026 — actualisation Afrique/Scandinavie\n\nLes mentions antérieures «test africain en attente» décrivent leurs versions historiques. Le joueur accepte maintenant l’Afrique pour le moment, reçu NORDIC-01/AFRICA_USER_ACCEPTANCE.json ; aucune nouvelle permission de transition à demander. Les limites documentées et le contenu différé restent ouverts. NORDIC-01 est installé sans test moteur : rayon de Nyslott approximatif, fiscalités conjointes du nord non représentées par le propriétaire unique, petites limites/hubs et démographie héritée non certifiés. Aucun blocage artificiel pour reprendre du flavor ; test nordique groupé seulement.\n'
    out['OWNERSHIP_BOUNDARIES.md']=old['OWNERSHIP_BOUNDARIES.md']+'\n\n## NORDIC-01 — périmètre installé,29 octobre2026\n\nCinq RGB natifs : xB81268 en KUOPIO, x2495FE/xFEC50D/x7005BB/x6480A4 en NORTHERN_NORWAY, vers RUS. Seuls deux nœuds de00_states et les portions POP SWE/Kuopio et DENNOR/NorthernNorway sont ciblés ; cohortes/totaux conservés. Préimages immédiates et FILES_DELIVERED.json font référence, y compris l’installation DP-02 indienne concurrente. Aucun pixel, région native, ressource, locator, bâtiment, recette, PM, technologie, capitale, institution ou personnage écrit. Schleswig-Holstein, Poméranie/Wismar/Poel et suivi SERG restent réservés ; colonies/Groenland hors lot. Afrique et travaux concurrents préservés.\n'
    out['NEXT_ACTION.md']='''# Prochaine action — après NORDIC-01

Afrique acceptée pour le moment par déclaration directe du joueur ; reçu NORDIC-01/AFRICA_USER_ACCEPTANCE.json. Ne pas redemander le test africain ni reprendre personnages/bâtiments. Lissage cosmétique et limites historiques déjà documentés restent différés.

Scandinavie incluant Finlande autorisée et première passe livrée : lire NORDIC-01/REPORT.md, SOURCES.md, PLAN.json, CELL_TRANSFERS.json, POPULATION_LEDGER.json, VALIDATION.json et EXTERNAL_COMPOSITION_REVIEW.json. Savonlinna et districts communs Neiden/Pasvik corrigés sur provinces natives. Propriétaire russe septentrional = approximation de juridiction dans un espace à droits superposés, pas preuve d’annexion exclusive. Aucun nouveau pays ni changement TECH/ECON.

19 régions et contacts examinés, cinq RGB réaffectés ; test moteur nordique NOT_RUN. Contrôle groupé en nouvelle partie1776 : deux repères de la carte, Åland/majorité de Finlande SWE, côte nord Varanger DENNOR, portions RUS et populations, simulation puis sauvegarde/rechargement. Aucun test par sous-lot demandé. Ne lancer aucune autre région sans nouvelle consigne ; ne reprendre aucune interface SERG. Progression historique320 critères inchangée ; Scandinavie suivie en portée auxiliaire1.0.2.
'''
    con=json.loads(old['CONCURRENT_CHANGES.json']);con['NORDIC-01']=dict(receipt='NORDIC-01/CONCURRENT_CHANGES.json',
        functional_files=3,native_RGBs_transferred=5,pixels_recolored=0,population_delta=0,
        peer_composition='NORDIC-01/EXTERNAL_COMPOSITION_REVIEW.json',Git_writes=0,vanilla_writes=0,SERG_writes=0)
    out['CONCURRENT_CHANGES.json']=json.dumps(con,ensure_ascii=False,indent=2)+'\n'
    assert all(n.b.a.sha(WORLD/k)==sha[k] for k in TRACK),'Tracking changed concurrently; reread.'
    for k,text in out.items():write(WORLD/k,text)
    n.save('TRACKING_PATCHES.json',[dict(file=(WORLD/k).relative_to(ROOT).as_posix(),before=sha[k],after=n.b.a.sha(WORLD/k)) for k in TRACK])
    print('Recorded scoped African acceptance and Nordic extension; legacy score unchanged.')

def final():
    v=n.load('VALIDATION.json');assert v['status']=='PASS'
    s=json.loads(n.b.a.raw(WORLD/'ROADMAP_STATE.json'))
    static=sum(c['status']=='STATIC_VERIFIED' for p in s['phases'] for r in p['subregions'] for c in r['criteria'].values())
    human=sum(c['status']=='USER_VALIDATED' for p in s['phases'] for r in p['subregions'] for c in r['criteria'].values())
    assert static==10 and human==0 and s['progress']['criteria_total']==320
    n.save('PROGRESS_CALCULATION.json',dict(technical_verified=static,criteria_total=320,runtime_full_criteria=human,
        African_scoped_player_acceptance_recorded=True,Nordic_scored_in_legacy_register=False,new_points=0))
    files=[ROOT/r['file'] for r in n.load('FILES_DELIVERED.json')]+[p for p in LOT.rglob('*') if p.is_file() and p.name!='DELIVERY_MANIFEST.json']+[WORLD/k for k in TRACK]+[ROOT/'tools/world1776_nordic01.py',ROOT/'tools/world1776_nordic01_closeout.py']
    n.save('DELIVERY_MANIFEST.json',{p.relative_to(ROOT).as_posix():n.b.a.sha(p) for p in files})
    print('Delivery recorded; Nordic runtime NOT_RUN, African user acceptance preserved.')

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser()
    for k in ['evidence','map','reports','tracking','final']:p.add_argument('--'+k,action='store_true')
    a=p.parse_args()
    if a.evidence:evidence()
    if a.map:map_image()
    if a.reports:reports()
    if a.tracking:tracking()
    if a.final:final()
