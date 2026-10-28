"""Evidence and WORLD-only tracking for the bounded Chad/Nile territorial pass."""
import argparse,csv,json
from collections import Counter
from decimal import Decimal,ROUND_HALF_UP
import world1776_sahel0607 as m
import world1776_sahel0205_closeout as old
import validate_starting_technology_1776 as contract
import localization_duplicate_audit as loc
ROOT,LOT=m.ROOT,m.LOT
WORLD=LOT.parent
TRACK=['ROADMAP.md','ROADMAP_STATE.json','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','OWNERSHIP_BOUNDARIES.md','CONCURRENT_CHANGES.json']

def doc(name,text):m.save(LOT/name,text)
def read(path):return json.loads(path.read_text('utf8'))
def write(path,data):m.save(path,json.dumps(data,ensure_ascii=False,indent=2)+'\n')

def tech():
    snapshot=contract.collect_snapshot()
    new=[contract.audit_country(t,snapshot,dict(required=r['tech'],allowed=r['tech'],historical_evidence=r['basis'])) for t,r in m.p.COUNTRIES.items()]
    existing=[contract.audit_country(r['TAG'],snapshot) for r in m.load('STARTING_TECH_BEFORE.json')]
    m.dump('STARTING_TECH_NEW_COUNTRIES.json',new);m.dump('STARTING_TECH_EXISTING_AFTER.json',existing)
    prior={r['TAG']:r for r in m.load('STARTING_TECH_BEFORE.json')};comparison=[]
    for r in existing:
        a={json.dumps(f,sort_keys=True) for f in prior[r['TAG']]['findings'] if f['priority'] in ['P0','P1']}
        b={json.dumps(f,sort_keys=True) for f in r['findings'] if f['priority'] in ['P0','P1']}
        comparison.append(dict(TAG=r['TAG'],inherited_remaining=[json.loads(f) for f in sorted(a&b)],resolved=[json.loads(f) for f in sorted(a-b)],introduced=[json.loads(f) for f in sorted(b-a)],historical_profile_certification='NOT_RECERTIFIED_BY_TERRITORIAL_PASS'))
    result=dict(new_profiles=len(new),all_new_profiles_pass=all(r['status']=='PASS_STATIC_ONLY' for r in new),existing_country_comparison=comparison,shared_graph_changes=0,shared_recipe_changes=0,human_validation=False)
    m.dump('TECH_NON_REGRESSION.json',result)
    print('New profiles:',[(r['TAG'],r['status'],r['findings']) for r in new])
    print('New existing-country P0/P1:',[(r['TAG'],r['introduced']) for r in comparison if r['introduced']])

def localization():
    checks=[];keys={}
    for lang in ['french','english']:
        entries=loc.entries(lang)
        own={k:v for k,v in entries.items() if any(path.name==m.PREFIX+'_l_'+lang+'.yml' for path,n,t in v)}
        keys[lang]=set(own)
        for k,v in own.items():checks.append(dict(check=lang+'.unique_mod_key.'+k,passed=len(v)==1))
    checks.append(dict(check='same_bilingual_keys',passed=keys['french']==keys['english']))
    m.dump('LOCALIZATION_CHECK.json',dict(status='PASS' if all(c['passed'] for c in checks) else 'FAIL',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,vanilla_SRA_override_intentional=True,render_runtime='NOT_RUN'))

def evidence():
    before=m.load('APPLY_BEFORE.json');plan=m.load('PLAN.json')
    a=Counter();b=Counter()
    for path in m.m.s.b.tech.effective('common/history/pops'):
        rel=path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else None
        b.update(old.portions(m.raw(path)))
        a.update(old.portions(m.raw(LOT/'apply_inputs'/rel) if rel in before['scope'] else m.raw(path)))
    regions={r['state'] for r in plan};tags={r['source'] for r in plan}|{r['target'] for r in plan}
    rows=[dict(state=s,country=t,before=a[s,t],after=b[s,t],delta=b[s,t]-a[s,t]) for s,t in sorted(set(a)|set(b)) if s in regions]
    ledger=m.load('POPULATION_LEDGER.json');ledger.update(portions=rows,
        countries=[dict(TAG=t,before=sum(v for (s,k),v in a.items() if k==t),after=sum(v for (s,k),v in b.items() if k==t)) for t in sorted(tags)],
        state_totals=[dict(state=s,before=sum(v for (k,t),v in a.items() if k==s),after=sum(v for (k,t),v in b.items() if k==s)) for s in sorted(regions)],historical_population_correction=False)
    m.dump('POPULATION_LEDGER.json',ledger)
    with (LOT/'POPULATION_BEFORE_AFTER.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        w=csv.DictWriter(stream,fieldnames=['state','country','before','after','delta']);w.writeheader();w.writerows(rows)
    cells={r['RGB']:r for r in m.load('GEOMETRY_CELLS.json')};cross=[]
    for r in plan:
        for color in r['RGBs']:
            cell=cells[color]
            cross.append(dict(state=r['state'],RGB=color,before=r['source'],after=r['target'],pixels=cell['pixels'],bbox=cell['bbox'],pixel_centroid=cell['centroid'],historical_basis=r['historical_basis'],precision=r['precision']))
    m.dump('GEOGRAPHIC_CROSSWALK.json',dict(historical_date='1776-01-01',new_RGBs=0,pixels_recolored=0,cells=cross,note='Coordinates locate unchanged native provinces, not reconstructed cadastral boundaries.'))
    # Reuse the already-reviewed political palette and crop, with immutable
    # before-state data. No geography or source boundary is inferred here.
    current=m.raw(ROOT/m.ST)
    m.geometry(m.raw(LOT/'apply_inputs'/m.ST))
    for name in ['CHAD','NILE']:(LOT/(name+'_BEFORE.png')).write_bytes((LOT/(name+'_PROPOSED.png')).read_bytes())
    m.geometry(current)
    for name in ['CHAD','NILE']:(LOT/(name+'_AFTER.png')).write_bytes((LOT/(name+'_PROPOSED.png')).read_bytes())

def reports():
    ledger=m.load('POPULATION_LEDGER.json');v=m.load('VALIDATION.json')
    pop='\n'.join('| '+r['TAG']+' | '+format(r['before'],',').replace(',',' ')+' | '+format(r['after'],',').replace(',',' ')+' |' for r in ledger['countries'])
    profiles='\n'.join('| '+t+' | '+r['fr']+' | '+r.get('kind','unrecognized')+' | '+str(len(r['tech']))+' |' for t,r in m.p.COUNTRIES.items())
    doc('REPORT.md',f'''# SAHEL-06-07 — Tchad et vallée du Nil

27 octobre 2026. Référence : **1er janvier 1776**. Statut : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Consigne directe : « Donc tu peux passer à la suite, Chad et Neil. » Le périmètre reste cartographique, avec les seules initialisations nécessaires aux pays restaurés. Aucun test moteur ou joueur acquis.

## Corrections installées

- Lac Tchad : Mandara (MDR) distingué de Bornou/Baguirmi, sous tribut à Bornou ; Fitri/Yao (BIL) et Dar Sila (DLS) séparés de l'ancien aplatissement sous Ouaddaï. Wara, noyau royal du Ouaddaï, passe du territoire décentralisé TBI au WAD ; capitale régionale WAD déplacée vers CHAD. Baguirmi retrouve une enveloppe cohérente du Chari/Massenya/Bokoro. Le sud hors de ces noyaux revient aux communautés Sara (SRA décentralisé), sans royaume Sara unique inventé.
- Nil : Assouan et Kharga retournent à l'Égypte avec un corridor natif entre oasis et Nil. Le corridor des kashifs et garnisons nubiens (NUB), Dongola des makks Zubayr (DNG), les royaumes shayqiyya agrégés (SHQ) et les Abdallab (ABD) remplacent des portions du Soudan décentralisé générique. NUB est tributaire de l'Égypte ; ABD de Sennar.
- Soudan central : noyau Funj/Hamaj de Sennar (SNR), Musabbaat du Kordofan central (MSB), noyau montagnard de Taqali (TQL) et royaume shilluk (SLQ) restaurés. Les espaces pastoraux et périphériques non attribuables avec assez de certitude restent SD1. Aucun État moderne du Soudan n'est projeté en 1776.
- Darfour (DFR), franges septentrionales Kanem/Borkou hors unique cellule de Wara, côte ottomane, frontières éthiopiennes et royaumes haoussa antérieurs conservés. Ni révolte de Mandara vers 1781, ni conquête shayqiyya de Dongola des années 1780, ni annexion darfourienne de 1785/86, ni conquête égyptienne de 1820/21 anticipée.

**205 RGB natifs transférés, 22 groupes, sept régions. Aucun nouveau RGB, aucun pixel redessiné.** [PLAN.json](PLAN.json) et [GEOGRAPHIC_CROSSWALK.json](GEOGRAPHIC_CROSSWALK.json) donnent chaque cellule, propriétaires, coordonnées et fondement. Les indices des cartes d'inspection ne sont que des repères ; les RGB sont les identifiants canoniques.

Enveloppes politiques sur le maillage existant, **pas frontières cadastrales certifiées**. Les cartes UNESCO ont été effectivement vues : leurs routes en pointillés ne sont pas traitées comme frontières. Les localités servent à contrôler les noyaux, sans partage automatique par distance à la capitale. Aucun nouveau territoire centralisé déconnecté ou entouré uniquement de territoires décentralisés ; vérification géométrique sur pixels natifs et voisinage dans [GEOMETRY_PREFLIGHT.json](GEOMETRY_PREFLIGHT.json).

## Institutions et technologies nécessaires

11 TAG nouveaux et SRA natif réactivé. Monarchies/oligarchies de notables et liens tributaires sont des approximations du pouvoir des cours, lignages et kashifs ; ils ne certifient pas une administration uniforme de tous les villages. SHQ agrège plusieurs makks. Les successions exactes et la régence Funj/Hamaj ne font pas l'objet de nouveaux personnages. Aucun personnage, événement flavor, nouvelle troupe ou nouveau bâtiment ajouté.

| TAG | Entité | Type moteur | Technologies explicites |
|---|---|---|---:|
{profiles}

Les profils sont justifiés individuellement dans [COUNTRY_PROFILES.json](COUNTRY_PROFILES.json) : agriculture, élevage, alimentation, ateliers, textile, échanges et établissements militaires traditionnels selon le pays. Aucun paquet technologique par âge, aucune modification des graphes TECH-R1/R2/R3 ou des recettes ECON-ALLOYS/quincaillerie. Une variante privée du mercantilisme, aux coefficients courants, utilise la gate international_relations pour ces seules cours ; pas d'assurance maritime artificiellement accordée. Les lois conditionnelles héritées de l'effet traditionnel ne valent pas attestation des lois actives en moteur.

Les 12 profils passent le contrat technique statique (pré requis, demandes de lois, bâtiments/PM explicites, unités) : [STARTING_TECH_NEW_COUNTRIES.json](STARTING_TECH_NEW_COUNTRIES.json). Sur huit pays existants, aucune nouvelle incompatibilité P0/P1 : [TECH_NON_REGRESSION.json](TECH_NON_REGRESSION.json). Les dettes héritées de Bornou, WAD, DFR ou SD1 restent signalées ; aucune connaissance tardive n'est ajoutée pour les masquer.

Les identifiants culturels Nubian/Shilluk/Daju/Mandara n'existent pas tous dans le catalogue courant. Proxies documentés : sudanese pour la Nubie et les Shayqiyya, nilotic pour Shilluk, fur pour Dar Sila, kanuri pour Mandara, baguirmi pour Fitri. **Nuba n'est pas utilisé comme synonyme de Nubien.** Aucune conversion des cohortes transférées.

## Populations et installations héritées

Monde : **{ledger['world_before']:,} → {ledger['world_after']:,}**, delta **0**. Sept totaux régionaux et chaque cohorte conservés (culture, religion et autres attributs explicites). Répartition par nombre de provinces transférées dans chaque portion source : **redistribution technique, pas recensement ou estimation de densité historique**. Un zéro national avant signifie TAG absent du scénario, pas absence historique d'habitants.

| TAG | Avant | Après |
|---|---:|---:|
{pop}

[POPULATION_BEFORE_AFTER.csv](POPULATION_BEFORE_AFTER.csv) détaille les portions. Tous les niveaux bâtis et PM sont conservés ; leurs parcelles suivent les nouveaux propriétaires. Une unique référence de recrutement du conscrit WAD passe de WADDAI, désormais sans portion WAD, à CHAD. Type, service et effectif inchangés. Aucun bâtiment affiné ou ajouté. Hubs, locators, terrains, ressources et traits régionaux restent inchangés et parfois partagés entre portions selon le moteur ; capitales visuelles, ressources, emploi et viabilité exigent le contrôle groupé en jeu.

## Sources, incertitudes et préservation

[SOURCES.md](SOURCES.md) distingue textes consultés, cartes vues et portée réelle. Dar Sila/Fitri et confins de WAD/BGI restent des approximations politiques ; chronologie d'unification de Taqali et liens Funj contestés, limites exactes des kashifs nubiens et juridictions pastorales non certifiées. Aucun tribut TQL, BIL ou DLS fixé sans preuve suffisante. NUB agrège des autorités héréditaires, non une province homogène. Le corridor Kharga–Égypte applique la règle de continuité du joueur et ne revendique pas une frontière désertique relevée. La présence territoriale restaurée ne certifie ni sa densité ni les souverains exacts au 1er janvier.

Cartes : [Tchad avant](CHAD_BEFORE.png), [Tchad après](CHAD_AFTER.png), [Nil avant](NILE_BEFORE.png), [Nil après](NILE_AFTER.png). Contrôle visuel du résultat installé effectué ; pas rendu du moteur.

Versions courantes préservées : SAHEL-01/02-05 hors cellules explicitement reprises ici (interface Bornou seulement), Balkans, Maghreb/Gibraltar, corridor de Siwa, Fezzan à 78 provinces, SERG, travaux américains NORTHWEST-01, TECH et ECON. [CONCURRENT_CHANGES.json](CONCURRENT_CHANGES.json) compare les empreintes et les blocs extérieurs aux sept régions. Aucun retour à une ancienne baseline, aucune écriture Git/vanilla/SERG.

## Contrôles et suite

Commandes exécutées : `world1776_sahel0607.py --apply --validate`, puis `--validate` après ajout du contrôle de corridor ; contrat collect_snapshot/audit_country par `world1776_sahel0607_closeout.py --tech` ; clôture avec `--evidence --reports --tracking --final`, puis `--reports --final` pour actualiser les résultats. **{v['passed']}/{v['total']} contrôles territoriaux statiques**, contrats techniques et contrôle de livraison séparés. [VALIDATION.json](VALIDATION.json), [DELIVERY_VALIDATION.json](DELIVERY_VALIDATION.json), [FILES_DELIVERED.json](FILES_DELIVERED.json) et [DELIVERY_MANIFEST.json](DELIVERY_MANIFEST.json). Les assertions anciennes imposant les propriétaires d'avant cette passe ne sont pas rejouées comme si ces transferts autorisés étaient des régressions.

Test moteur et joueur **NOT_RUN**. [GROUPED_RUNTIME_ITEMS.md](GROUPED_RUNTIME_ITEMS.md) complète le protocole groupé, sans demande intermédiaire. WORLD reste **10/320 (3,13 %)** : régions partielles, aucun nouveau critère régional ou humain acquis. Prochaine action : contrôle cartographique groupé de la bande sahélienne et du Nil, puis arbitrage des limites encore documentées. Aucune nouvelle région ni pack flavor lancé automatiquement.
''')
    doc('GROUPED_RUNTIME_ITEMS.md','''# Contrôle groupé — Sahel et Nil

NOT_RUN, aucune attestation humaine. Complément au protocole SAHEL-01/02-05, sans test intermédiaire demandé.

Nouvelle partie 1776 : comparer CHAD_AFTER et NILE_AFTER aux frontières effectivement chargées. Examiner Wara/WAD et sa capitale, Fitri, Dar Sila, Mandara/Bornou, Baguirmi/Sara ; vérifier Kharga–Assouan–Égypte, corridor NUB/Dongola/Shayqiyya, Abdallab/Sennar, Musabbaat/Taqali/Shilluk. Pas d'enclave centralisée accidentelle. DFR, côte ottomane, Éthiopie et frontière des lots haoussa servent de témoins.

Vérifier les relations BOR→MDR, EGY→NUB, SNR→ABD et la possibilité d'interactions diplomatiques. Observer capitales/hubs, noms et drapeaux de nouveaux pays, lois effectives, connaissances, parcelles de bâtiments/ressources et recrutement du conscrit WAD à CHAD. Les calculs statiques ne prouvent pas les valeurs budgétaires, les lois finales ni les choix de PM implicites.

Comparer les populations régionales au ledger, emploi et accès au marché. Jouer un mois, sauvegarder/recharger ; consigner uniquement les observations réelles avec version livrée. Témoins extérieurs : SAHEL-01/02-05, Balkans, SERG, Gibraltar/Ceuta, Siwa/Fezzan, Amérique du Nord. Manifeste : DELIVERY_MANIFEST.json. Une réussite locale ne valide pas toute l'Afrique ou WORLD.
''')
    doc('USER_REQUEST.txt','Donc tu peux passer à la suite, Chad et Neil.\nInterprétation contextuelle : Tchad et Nil, après Sénégambie/Mali/Haoussa. Frontières uniquement, initialisations nécessaires, tests groupés.\n')
    doc('REPRODUCE.md','''# Reproduire

Python local depuis le dépôt :

`python tools/world1776_sahel0607.py --validate`

`python tools/world1776_sahel0607_closeout.py --tech --evidence --reports --final`

Ne pas rejouer --apply ni --tracking : gardes anti-rejeu, entrées et reçus immuables. Les validations écrivent seulement les preuves du lot. Le contrat technique porte sur les PM explicitement choisis et les demandes de lois ; les défauts et l'exécution du moteur restent à observer. Une modification territoriale future légitime requiert un rapprochement des nouvelles preuves, jamais une restauration de nos propriétaires antérieurs.
''')

def tracking():
    path=WORLD/'ROADMAP_STATE.json';data=read(path)
    assert not any(r['id']=='SAHEL-06-07' for r in data['lots']),'Already tracked.'
    hashes={n:m.m.s.b.a.sha(WORLD/n) for n in TRACK}
    for n in TRACK:
        dest=LOT/'tracking_inputs'/n;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((WORLD/n).read_bytes())
    for phase in data['phases']:
        if phase['id']=='P3':
            for region in phase['subregions']:
                if region['id'] not in ['P3-04','P3-06']:continue
                for k,c in region['criteria'].items():
                    if k=='V':c.update(status='NOT_STARTED',evidence='SAHEL-06-07/GROUPED_RUNTIME_ITEMS.md');continue
                    if c['status']=='STATIC_VERIFIED':continue
                    # Keep earlier Hausa/Sahel evidence when extending P3-04.
                    prior=c.get('evidence');evidence='SAHEL-06-07/REPORT.md'
                    if prior and evidence not in prior:evidence=prior+' + '+evidence
                    c.update(status='PARTIAL',evidence=evidence,remaining='Noyaux du Tchad/Nil installés ; confins, profils régionaux complets et test groupé ouverts. Aucun crédit régional entier.')
        n=sum(c['status']=='STATIC_VERIFIED' for r in phase['subregions'] for c in r['criteria'].values())
        phase['progress'].update(technical_verified=n,technical_percent=float((Decimal(n)*100/Decimal(phase['progress']['criteria_total'])).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)))
    n=sum(p['progress']['technical_verified'] for p in data['phases'])
    assert n==10 and data['progress']['criteria_total']==320 and data['progress']['runtime_user_validated']==0
    data['progress'].update(technical_verified=n,technical_percent=3.13)
    data['lots'].append(dict(id='SAHEL-06-07',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',scope=['Chad royal cores and Chari interface','Nile / Funj / Kordofan / Shilluk political cores','Aswan and Kharga Egyptian continuity'],excluded=['Further regions','Flavour and building refinement','Exact cadastral or demographic reconstruction'],runtime='NOT_RUN',files_modified=25,existing_files_modified=7,new_files=18,new_tags=11,activated_existing_tags=['SRA'],native_RGBs_transferred=205,new_RGBs=0,pixels_recolored=0,world_population_delta=0,receipt='SAHEL-06-07/FILES_DELIVERED.json',credited_criteria=[]))
    data['steering_history'].append(data['current_steering'])
    data['current_steering']=dict(date='2026-10-27',scope='Chad and Nile political borders after Senegambia/Mali/Hausa',authority='SAHEL-06-07/USER_REQUEST.txt',last_lot='SAHEL-06-07',next_pass='Grouped territorial review of Sahel and Nile; remaining limits documented',intermediate_player_tests_requested=False,runtime_validation_timing='GROUPED_SAHEL_NILE',full_V_credit=False)
    assert all(m.m.s.b.a.sha(WORLD/n)==h for n,h in hashes.items()),'Concurrent WORLD update.'
    write(path,data)
    entry='''\n\n## SAHEL-06-07 — 27 octobre 2026\n\nTchad et Nil autorisés par la consigne directe « Donc tu peux passer à la suite, Chad et Neil. », remplaçant leur report à plus tard de SAHEL-02-05. Wara/Ouaddaï, Baguirmi, Mandara tributaire, Fitri et Dar Sila ; communautés Sara décentralisées. Assouan/Kharga à l'Égypte avec corridor, Nubie des kashifs, Dongola, Shayqiyya, Abdallab/Sennar, Musabbaat/Taqali et Shilluk. 205 RGB natifs réattribués, aucun pixel, hub ou ressource redessiné. 11 nouveaux TAG et SRA réactivé ; sept fichiers existants ciblés, 18 ajouts. Toutes les cohortes/niveaux bâtis conservés, monde 837 328 539, delta 0. Contrôles statiques et 12 profils techniques : preuves SAHEL-06-07/VALIDATION.json et TECH_NON_REGRESSION.json. Enveloppes politiques approximatives et liens contestés explicités dans SOURCES.md/REPORT.md. Aucun test moteur/humain ; WORLD 10/320 (3,13 %), aucun nouveau crédit régional. Suite : contrôle cartographique groupé Sahel/Nil, sans autre région lancée automatiquement.\n'''
    for name in ['ROADMAP.md','PROGRESS_HISTORY.md']:m.save(WORLD/name,m.raw(WORLD/name).rstrip()+entry)
    m.save(WORLD/'BLOCKERS.md',m.raw(WORLD/'BLOCKERS.md').rstrip()+'''\n\n## SAHEL-06-07 — Tchad/Nil\n\nConsigne ultérieure autorisant ces secteurs exécutée. Restent : confins Kanem/Borkou et royautés du Tchad non cadastrés, dates/liens de Dar Sila/Fitri, consolidation de Taqali et vassalage Funj contestés, ressorts héréditaires nubiens et frontières pastorales. SD1 conserve les périphéries non attribuables. Proxies culturels et répartition démographique technique documentés ; hubs, ressources partagées, lois effectives, drapeaux et budgets à observer dans le test groupé. Aucune nouvelle incompatibilité P0/P1 des pays existants ; dettes héritées conservées sans refonte TECH/ECON. Pas de nouvelle région ni flavor automatique.\n''')
    m.save(WORLD/'OWNERSHIP_BOUNDARIES.md',m.raw(WORLD/'OWNERSHIP_BOUNDARIES.md').rstrip()+'''\n\n## SAHEL-06-07 — Tchad/Nil\n\nSept nœuds d'états BORNU/CHAD/WADDAI/EGYPTIAN_DESERT/DONGOLA/KORDOFAN/BLUE_NILE et leurs seules portions POP/bâtiments listées dans PROPOSED_SCOPES.json. Une référence conscrite WAD de WADDAI à CHAD ; capitale régionale WAD vers CHAD dans surcharge propre. 11 nouveaux TAG, SRA activé, trois liens tributaires. Aucune géométrie bitmap, hub/locator, terrain, ressource, recette commune, graphe TECH, caractère ou suivi SERG écrit. Les autres portions Bornou et la totalité de DFR/TUR/ETH restent identiques. Énumération canonique : SAHEL-06-07/PLAN.json ; entrées immédiates apply_inputs, version livrée FILES_DELIVERED.json.\n''')
    m.save(WORLD/'NEXT_ACTION.md','''# Prochaine action — après SAHEL-06-07\n\nLa consigne directe Tchad/Nil a été exécutée après SAHEL-02-05. Lire SAHEL-06-07/REPORT.md, SOURCES.md, PLAN.json, VALIDATION.json, TECH_NON_REGRESSION.json et FILES_DELIVERED.json. Le statut est IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION, aucun reçu joueur créé.\n\nPréparer le contrôle cartographique groupé de la bande Sénégambie/Mali/Haoussa/Tchad/Nil, avec les deux protocoles GROUPED_RUNTIME_ITEMS.md. Aucune demande intermédiaire. Limites encore ouvertes : franges politiques, Kanem/Borkou, Dar Sila/Fitri, Taqali, ressorts nubiens, populations/ressources/hubs partagés. Ne pas les combler par frontières arbitraires, personnages ou raffinements bâtis. Aucune autre région lancée automatiquement.\n\nPréserver les versions courantes de TECH/ECON, SERG, Balkans, Maghreb/Gibraltar, Siwa, Fezzan à 78 provinces, SAHEL-01/02-05 et Amérique du Nord ; pas de retour à une ancienne baseline. Monde 837 328 539, delta 0. WORLD 10/320 (3,13 %), aucun nouveau crédit régional/humain.\n''')
    concurrent=read(WORLD/'CONCURRENT_CHANGES.json');concurrent['SAHEL-06-07']=dict(receipt='SAHEL-06-07/CONCURRENT_CHANGES.json',existing_functional_files_modified=7,new_files=18,native_RGBs_transferred=205,new_RGBs=0,pixels_recolored=0,world_population_delta=0,Git_writes=0,vanilla_writes=0,SERG_writes=0,old_baseline_restored=False)
    write(WORLD/'CONCURRENT_CHANGES.json',concurrent)
    m.dump('TRACKING_PATCHES.json',[dict(file='docs/reports/map/WORLD_1776_CLOSURE/'+n,before=hashes[n],after=m.m.s.b.a.sha(WORLD/n)) for n in TRACK])

def final():
    checks=[]
    def ck(k,v,d=None):checks.append(dict(check=k,passed=bool(v),detail=d))
    receipts=m.load('FILES_MODIFIED.json');edited={r['file'] for r in receipts}
    for r in receipts:ck('delivered_hash.'+r['file'],m.m.s.b.a.sha(ROOT/r['file'])==r['after'])
    ck('25_functional_files',len(receipts)==25)
    m.dump('FILES_DELIVERED.json',receipts)
    ck('static_territorial_pass',m.load('VALIDATION.json')['status']=='PASS')
    for r in m.load('STARTING_TECH_NEW_COUNTRIES.json'):ck('initial_knowledge_contract.'+r['TAG'],r['status']=='PASS_STATIC_ONLY' and not r['findings'])
    for r in m.load('TECH_NON_REGRESSION.json')['existing_country_comparison']:ck('no_new_P0_P1.'+r['TAG'],not r['introduced'])
    ledger=m.load('POPULATION_LEDGER.json');ck('world_conservation',ledger['delta']==0)
    for r in ledger['state_totals']:ck('regional_population_conservation.'+r['state'],r['before']==r['after'])
    ck('all_new_countries_populated',all(any(r['country']==t and r['after']>0 for r in ledger['portions']) for t in m.p.COUNTRIES))
    before=m.load('APPLY_BEFORE.json');outside=[]
    tracking={'docs/reports/map/WORLD_1776_CLOSURE/'+n for n in TRACK}
    for rel,h in before['protected'].items():
        if rel in edited or rel in tracking:continue
        if not (ROOT/rel).exists() or m.m.s.b.a.sha(ROOT/rel)!=h:outside.append(rel)
    ck('current_outside_scope_preservation',not outside,outside)
    state=read(WORLD/'ROADMAP_STATE.json')
    technical=[r['id']+'/'+k for phase in state['phases'] for r in phase['subregions'] for k,c in r['criteria'].items() if c['status']=='STATIC_VERIFIED']
    human=[r['id']+'/'+k for phase in state['phases'] for r in phase['subregions'] for k,c in r['criteria'].items() if c['status']=='USER_VALIDATED']
    ck('canonical_progress',len(technical)==10 and not human and state['progress']['technical_verified']==10 and state['progress']['criteria_total']==320)
    m.dump('PROGRESS_CALCULATION.json',dict(credited=technical,user_validated=human,numerator=10,denominator=320,percent=3.13,newly_credited=[],partial_regions_receive_no_credit=True))
    localization();ck('localization_unique_bilingual_keys',m.load('LOCALIZATION_CHECK.json')['status']=='PASS')
    for r in m.load('EGYPT_CORRIDOR_CHECK.json'):ck('Egyptian_corridor.'+r['RGB'],r['pixels_in_survey']>0 and r['connected_to_existing_Egypt'])
    required=['REPORT.md','SOURCES.md','PLAN.json','GEOGRAPHIC_CROSSWALK.json','POPULATION_BEFORE_AFTER.csv','GROUPED_RUNTIME_ITEMS.md','COUNTRY_PROFILES.json','TECH_NON_REGRESSION.json','LOCALIZATION_CHECK.json','EGYPT_CORRIDOR_CHECK.json','GEOMETRY_PREFLIGHT.json','CHAD_BEFORE.png','CHAD_AFTER.png','NILE_BEFORE.png','NILE_AFTER.png']
    for name in required:ck('evidence_exists.'+name,(LOT/name).is_file())
    result=dict(status='PASS' if all(r['passed'] for r in checks) else 'FAIL',passed=sum(r['passed'] for r in checks),total=len(checks),checks=checks,automated_engine_test=False,human_validated=False)
    m.dump('DELIVERY_VALIDATION.json',result)
    files=[ROOT/r for r in edited]+[LOT/r for r in required]+[LOT/r for r in ['VALIDATION.json','STARTING_TECH_NEW_COUNTRIES.json','STARTING_TECH_EXISTING_AFTER.json','FILES_DELIVERED.json','DELIVERY_VALIDATION.json','PROGRESS_CALCULATION.json','TRACKING_PATCHES.json','CONCURRENT_CHANGES.json','POPULATION_LEDGER.json','APPLY_BEFORE.json']]+[WORLD/r for r in TRACK]+[ROOT/'tools'/r for r in ['world1776_sahel0607.py','world1776_sahel0607_plan.py','world1776_sahel0607_inspect.py','world1776_sahel0607_closeout.py']]
    files+=[f for f in (LOT/'sources').iterdir() if f.is_file()]
    m.dump('DELIVERY_MANIFEST.json',{f.relative_to(ROOT).as_posix():m.m.s.b.a.sha(f) for f in files})
    print('Delivery:',result['status'],result['passed'],'/',result['total']);print('FAIL:',[c for c in checks if not c['passed']])
    return result['status']=='PASS'

if __name__=='__main__':
    a=argparse.ArgumentParser()
    for k in ['tech','evidence','reports','tracking','final']:a.add_argument('--'+k,action='store_true')
    args=a.parse_args()
    if args.tech:tech()
    if args.evidence:evidence()
    if args.reports:reports()
    if args.tracking:tracking()
    if args.final:raise SystemExit(0 if final() else 1)
