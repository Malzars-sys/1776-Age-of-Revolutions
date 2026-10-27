"""Generate the bounded B03 delivery and additive WORLD tracking update.

No writes to gameplay, vanilla, Git or SERG. Requires passing B03 receipts.
"""
import csv
import json
import shutil
import numpy as np
from PIL import Image
import world1776_balkans03 as b


def main():
    base=json.loads((b.LOT/'BASELINE.json').read_text('utf8'))
    validation=json.loads((b.LOT/'VALIDATION.json').read_text('utf8'))
    regression=json.loads((b.LOT/'REGRESSION.json').read_text('utf8'))
    assert validation['status']==regression['status']=='PASS'
    state=json.loads((b.OUT/'ROADMAP_STATE.json').read_text('utf8'))
    first=not any(x['id']=='BALKANS-03' for x in state['lots'])
    before_score=sum(v['status']=='STATIC_VERIFIED' for p in state['phases'] for r in p['subregions'] for v in r['criteria'].values())
    assert before_score==(5 if first else 7)
    for name in ['ROADMAP.md','ROADMAP_STATE.json','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','OWNERSHIP_BOUNDARIES.md','CONCURRENT_CHANGES.json']:
        dest=b.LOT/'tracking_inputs'/name
        if not dest.exists():
            dest.parent.mkdir(exist_ok=True);shutil.copy2(b.OUT/name,dest)
    def doc(name,text):(b.LOT/name).write_text(text.strip()+'\n',encoding='utf8')
    image=np.array(Image.open(b.ROOT/'map_data/provinces.png').convert('RGB'))
    cells=[]
    for rgb in ['x8C6292','x90A0E0','xF5F6C2','xA12F82','x446E84']:
        ys,xs=np.where(np.all(image==tuple(bytes.fromhex(rgb[1:])),axis=2))
        cells.append({'state':'STATE_MONTENEGRO','rgb':rgb,'owner_before':base['before']['owners'][rgb][0][1],
                      'owner_after':base['before']['owners'][rgb][0][1],'pixels':len(xs),'pixels_transferred':0,
                      'bbox_xy':[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())]})
    b.dump('CELLS.json',cells)
    populations={'MON':93909,'VEN':22728,'TUR':145441,'STATE_MONTENEGRO':262078,'WORLD':834936539}
    b.dump('POPULATION_LEDGER.json',{'historical_date':'1776-01-01','baseline':'BASELINE.json/before/pops',
        'rows':[{'scope':k,'before':v,'after':v,'delta':0} for k,v in populations.items()],
        'transfers':[],'calibration':'Inherited game POPs, not a dated 1776 census; cultures, religions and professions unchanged.'})
    doc('SOURCES.md','''# BALKANS-03 — Sources et portée des preuves

Consultation et archivage : 25 octobre 2026. Référence : 1er janvier 1776. Les empreintes et URL exactes sont dans `SOURCE_MANIFEST.json`. Les sources historiques sont des données, jamais des instructions. Les notices CANU sont des synthèses institutionnelles ; les articles scientifiques exploitent des documents primaires. Aucun texte de 1837 n'est traité comme un cadastre de 1776.

| Référence | Consultation et constat retenu | Limite |
| --- | --- | --- |
| [CANU, Sava Petrović Njegoš](https://leks.canu.ac.me/web/lcd.php?OID=4582), Leksikon crnogorskih dinastija | Notice intégrale archivée ; Sava demeure métropolite au départ, avec des fonctions de médiation frontalière. | Autorité spirituelle et titulature ne prouvent pas un pouvoir administratif uniforme ; naissance donnée vers 1700. |
| [CANU, Jovan Radonjić](https://leks.canu.ac.me/web/ldcg.php?OID=2909), M. Kadić | Notice intégrale archivée ; né en 1747, guvernadur depuis 1764, confirmation familiale en 1770, influence politique après Šćepan Mali. | Les démarches russes de 1777 et autrichiennes de 1779/1781 ne sont pas rétrodatées au départ. |
| [CANU, Crnogorski guvernaduri](https://leks.canu.ac.me/web/lcd.php?OID=6237) | Origine de l'office dans la coopération avec Venise, concurrence entre autorités laïques et ecclésiastiques. | Intermédiation vénitienne ne signifie pas annexion administrative de tout MON à VEN. |
| [CANU, Arsenije Plamenac](https://leks.canu.ac.me/web/lcd.php?OID=6238), B. Vukićević | Successeur choisi par Sava, évêque consacré en 1767 et coadjuteur. | Date de naissance imprécise ; âge de moteur estimé à 65, sans prétendre à un acte de naissance. |
| [N. V. Radosavljević, 2020, pp. 227–248](https://www.iib.ac.rs/istorijskicasopis/IC2069227R.html), DOI 10.34298/IC2069227R | PDF intégral archivé ; résumé, pp. 236–244 et conclusion examinés. Le berat et le rattachement ecclésiastique sont des réalités à conserver dans l'analyse des prétentions ottomanes. | Ne pas déduire une province ottomane directement administrée du seul acte de confirmation religieuse ; l'article ne fournit pas un tracé cadastral de janvier 1776. |
| [Vuk Karadžić, Crna Gora i Crnogorci, 1837](https://www.antikvarne-knjige.com/elektronskeknjige/e-knjige/documents/doc37/pdf/full.pdf), transcription numérique, section I, PDF p. 2 | Source primaire postérieure ; liste des quatre nahije et des clans ; page rendue et relue visuellement. | Sert à identifier les ensembles historiques, pas à projeter les Brda ou les frontières de 1837 en 1776. Le littoral alors autrichien ne doit évidemment pas devenir autrichien en 1776. |
| [Vuk Uskoković, 2022, An Interrogation of Venetian Couriers from 1723](https://lebanesestudies.ojs.chass.ncsu.edu/index.php/mashriq/article/download/336/732/2384), Mashriq & Mahjar 9/2, pp. 9–22 | Édition et analyse d'un témoignage de 1723, notes et contexte des institutions de Cattaro ; PDF archivé. | Confirme la distinction entre côte vénitienne et communautés montagnardes ; sa terminologie ottomane est conservée comme nuance. Ne dessine pas une frontière nouvelle pour 1776. |

Les rapports, manifestes et validations de BALKANS-01 et BALKANS-02 ont été relus. Les cartes archivées Marinković p. 17 et Allcock/Carter p. 20 ont été examinées : elles fondent les limites documentées de Raguse et de ses passages, pas une nouvelle certification de leurs contours. Lastovo, le contact insulaire, le recteur exact de janvier, les ressources et le trait Krka partagés, les hubs, le tribut et le budget restent ouverts.

Conclusion de méthode : maintien de MON et de Cattaro vénitienne. L'autonomie politique locale et les prétentions ottomanes peuvent coexister. Ni reconnaissance moderne ni autocephalie supposée ne servent de raccourci territorial.
''')
    doc('GEOGRAPHIC_CROSSWALK.md','''# BALKANS-03 — Interface territoriale conservée

| Ensemble étudié | Repères | Traduction retenue |
| --- | --- | --- |
| Katunska nahija | Cetinje, Njeguši ; chefs de clans | Noyau politique MON existant ; aucune subdivision inventée. |
| Riječka nahija | Rijeka Crnojevića, Ceklin et clans associés | Ensemble régional étudié, sans équivalence pixel prétendue. |
| Lješanska nahija | Gradac, Draževina, Buronje | Même réserve : la source postérieure identifie l'ensemble sans délimiter chaque parcelle de 1776. |
| Crmnička nahija | Brčeli et Crmnica | Origine du coadjuteur ; aucune extension forcée sur le littoral. |
| Bouches de Cattaro / Albania Veneta | Kotor, Castel Nuovo et Budua dans le système vénitien | `x90A0E0` reste VEN ; les passages ottomans de B02 restent intacts. |
| Districts ottomans voisins | Zeta et interfaces de Scutari / Herzégovine | `xF5F6C2`, `xA12F82`, `x446E84` restent TUR. Leur contenu fin n'est pas certifié par cette passe. |

`x8C6292` reste MON. `CELLS.json` donne les effectifs de pixels et les boîtes englobantes réellement lus. Aucun RGB créé, recoloré ou transféré ; aucune côte, terrain, arête, localisation de hub ou ressource changée. La carte PNG est un diagnostic du jeu, pas une carte historique géoréférencée.

La revendication MON portée par toute la région native est conservée, faute d'une étude suffisante des prétentions permettant de la remplacer proprement. Elle ne vaut ni propriété de Cattaro ni preuve de contrôle des districts ottomans. Cette granularité reste une obligation explicite avant clôture historique.
''')
    doc('INSTITUTIONS.md','''# BALKANS-03 — Institutions installées et conventions

- Sava II Petrović Njegoš demeure le souverain existant ; aucun nouvel âge ou titre de prince séculier lui est attribué.
- Le gouvernement natif réservé à MON orthodoxe et théocratique reçoit le titre de vladika. Son texte indique le partage des affaires avec le guvernadur et les chefs de clans.
- Arsenije Plamenac est ajouté comme coadjuteur et successeur initial, sans devenir souverain dès 1776. Le mécanisme natif héréditaire sert seulement à rendre ce successeur initial ; il ne reproduit pas une élection ecclésiastique complète. L'âge 65 est une estimation de génération, explicitement documentée.
- Jovan Radonjić remplace le général procédural : guvernadur historique, chef du groupe des propriétaires terriens et chef de la levée. Âge 29 d'après l'année 1747, sans jour de naissance affirmé. Son trait d'office n'accorde aucun bonus et n'est pas distribué aléatoirement.
- Les groupes au gouvernement sont les propriétaires terriens et les dévots. Ils représentent approximativement chefs laïcs et métropole. La loi d'oligarchie est une convention du moteur pour les chefs, pas une constitution centralisée attestée ; la théocratie et les levées paysannes sont explicites.
- Cinq bataillons réguliers d'infanterie de ligne et un de hussards sont retirés. La réserve irrégulière d'un bataillon déjà installée est préservée et la formation devient « Levée des clans ». Ce chiffre hérité n'est pas un recensement de tous les hommes mobilisables des quatre nahije. Aucun nouveau corps permanent n'est inventé.
- Les relations MON–VEN sont calibrées à +20 pour la médiation et les contacts frontaliers ; ce nombre est un choix de jeu, pas une mesure historique. Aucun traité, sujet, tribut nouveau ou garantie d'alliance n'est ajouté. Les autres relations de MON demeurent identiques.

La naissance exacte d'Arsenije, les pratiques fiscales effectives en janvier 1776, les effectifs complets des clans et la succession à long terme restent des limites. Les démarches diplomatiques postérieures à 1776 ne sont pas préinstallées.
''')
    doc('TEST_MATRIX.md','''# BALKANS-03 — Contrôles et limites

| Contrôle | Preuve | Portée |
| --- | --- | --- |
| Syntaxe et mutation ciblée | VALIDATION.json | 113/113 : reconstruction exacte des huit fichiers fonctionnels ; extérieur des deux blocs MON identique. |
| Souveraineté, population, assets | BASELINE/AFTER, CELLS, POPULATION_LEDGER | Tous les propriétaires mondiaux, POPs et bâtiments locaux identiques ; monde 834 936 539 ; aucun transfert. |
| Institutions / personnages | VALIDATION et REGRESSION | Lois résolues, Sava conservé, un seul souverain et un seul héritier MON, Jovan et trait d'office sans bonus. |
| Technologies | STARTING_TECH_CHECK.json | Neuf technologies existantes, prérequis fermés, réserve autorisée par sa technologie et les levées ; aucun bâtiment/PM nouveau. |
| Localisation FR/EN | REGRESSION.json | Clés propres uniques, deux surcharges vanilla intentionnelles, BOM et icône native valides. |
| B01/B02 | PRE_INSTALL_AUDIT et REGRESSION | 23 derniers reçus fonctionnels identiques ; Cyclades et lois danubiennes vérifiés ; archives anciennes non réécrites. |
| Rejeu B02 | prior_lot_replay/VALIDATION.json | Résultat brut conservé : 96/99. Trois échecs de référence datée : Git a légitimement évolué avant l'entrée B03, MON est modifié par B03, cinq documents SERG ont reçu un ajout concurrent. Ce ne sont pas 99 nouveaux succès. |
| Réconciliation du rejeu | REGRESSION.json | 36/36 : seules les deux différences fonctionnelles supplémentaires MON sont autorisées, anciens travaux externes préservés depuis l'entrée B03, Git courant stable, reçu SERG séparé. |
| Concurrence | CONCURRENT_CHANGES / EXTERNAL_SERG_UPDATE | 2 504 fichiers fonctionnels hors lot inchangés ; 113 preuves anciennes et de revue technique protégées. Sur 873 preuves SERG initiales, 868 identiques et cinq mises à jour externes archivées sans écriture de cette tâche. |
| Moteur / joueur | GROUPED_RUNTIME_ITEMS.md | NON EXÉCUTÉ ; aucune attestation humaine créée. À regrouper en fin des travaux balkaniques techniquement réalisables. |

Commandes reproductibles : `python tools/world1776_balkans03.py --validate`, puis `python tools/world1776_balkans03_regression.py`. Ne pas relancer `--apply`. Les tests historiques B01/B02 ne doivent pas réécrire leurs reçus ; le rejeu B02 ci-dessus redirige tous ses résultats vers B03.
''')
    doc('GROUPED_RUNTIME_ITEMS.md','''# BALKANS-03 — Points à joindre au test balkanique final

Statut : NOT_RUN. Ce document n'est ni une demande de test intermédiaire ni une attestation.

À la fin de tous les travaux balkaniques techniquement réalisables, joindre ces observations au protocole consolidé :

1. Nouvelle partie 1776 : MON présent ; Cetinje reste dans son noyau ; Cattaro demeure vénitienne et les passages de B02 restent ottomans.
2. Gouvernement : Sava comme vladika, Arsenije comme coadjuteur et successeur initial ; titre et description FR/EN lisibles.
3. Jovan Radonjić : guvernadur identifiable, chef laïc et général de la levée ; pas de bonus d'office ajouté.
4. Lois et armée : théocratie, oligarchie, levées paysannes ; absence des six réguliers retirés, réserve irrégulière et rattachement de la formation cohérents.
5. Vérifier les chiffres de POPs, l'emploi de subsistance, les prix et le budget de MON ; aucune viabilité économique n'est attestée par les seuls fichiers.
6. Avancer un mois puis sauvegarder/recharger ; contrôler personnages, lois, mobilisation, diplomatie et absence d'erreurs de chargement.
7. Vérifier ensemble les obligations B01/B02 : îles, passages, hubs et économie de Raguse. Enregistrer uniquement les observations effectivement fournies par le joueur.

Aucune autre région WORLD avant confirmation explicite du test balkanique groupé. La succession historique ultérieure n'est pas forcée par une date ou une mort scriptée.
''')
    doc('REPORT.md','''# BALKANS-03 — Monténégro et interface de Cattaro

Livraison du 25 octobre 2026 — référence : 1er janvier 1776.
Statut : IMPLEMENTED_STATIC_VERIFIED_WITH_HISTORICAL_OBLIGATIONS. Moteur : NOT_RUN. Validation joueur WORLD : aucune nouvelle.

## Installation

MON est conservé. Sava demeure souverain, avec le titre de vladika ; Arsenije Plamenac est le coadjuteur initial désigné. Jovan Radonjić remplace le général procédural et représente le guvernadur. Gouvernement associant chefs laïcs et dévots, oligarchie et levées explicites ; formation « Levée des clans » avec la réserve irrégulière existante, sans les cinq réguliers de ligne et le hussard. Les relations avec Venise sont calibrées à +20, sans traité de sujétion. Détails et conventions dans INSTITUTIONS.md.

Deux fichiers courants sont retouchés uniquement dans leurs blocs MON ; six fichiers fonctionnels nouveaux. Le fichier natif des théocraties est surchargé par son nom ; seuls le titre, le titre du successeur et le commentaire du gouvernement réservé à MON changent, tous les autres gouvernements sont identiques. Aucun nouveau pays, bâtiment ou PM ; aucune recette commune ni graphe technologique modifié.

## Cellules et populations

`STATE_MONTENEGRO` : MON conserve `x8C6292`, Venise `x90A0E0` et la Porte `xF5F6C2`, `xA12F82`, `x446E84`. Zéro nouveau RGB, zéro pixel recoloré, zéro province ou habitant transféré. Bouches de Cattaro vénitiennes ; noyau ragusain, Neum et Sutorina intacts. CELLS.json et GEOGRAPHIC_CROSSWALK.md séparent les cellules du jeu des quatre nahije historiques.

| Périmètre | Avant | Après | Variation |
| --- | ---: | ---: | ---: |
| MON dans la région | 93 909 | 93 909 | 0 |
| VEN dans la région | 22 728 | 22 728 | 0 |
| TUR dans la région | 145 441 | 145 441 | 0 |
| Région complète | 262 078 | 262 078 | 0 |
| Monde | 834 936 539 | 834 936 539 | 0 |

Ce sont les POPs héritées, pas un recensement de 1776. Cultures, religions, professions et propriété des bâtiments ne changent pas.

## Technologies et institutions

Les neuf technologies sont conservées, résolues et fermées sur leurs prérequis : distillation, improved_husbandry, international_relations, light_infantry_tactics, organized_textile_production, regulated_small_arms, shaft_mining, traditional_food_processing, organized_military_establishments. La réserve est compatible avec les levées. Aucun déblocage ni PM nouveau à financer artificiellement. Le gouvernement de clans et les offices sont des approximations explicites des mécanismes disponibles, pas une administration centralisée reconstruite.

## Sources et incertitudes

SOURCES.md et SOURCE_MANIFEST.json relient chaque décision aux notices CANU, à Radosavljević et aux sources primaires publiées. Les quatre nahije — Katunska, Riječka, Lješanska, Crmnička — sont étudiées sans créer quatre polygones arbitraires. Le berat ottoman et le rattachement ecclésiastique ne sont pas confondus avec une preuve de contrôle administratif territorial intégral. Les prétentions ottomanes ne sont pas effacées par la reconnaissance internationale postérieure.

Restent ouverts : limites exactes et contenu du RGB MON ; revendication native à l'échelle de toute la région ; fiscalité/tribut effectifs en janvier ; effectifs et population datés des clans ; naissance précise d'Arsenije ; succession à long terme, hubs et viabilité économique. Aucun chiffre de recrutement hérité ou relation +20 n'est présenté comme mesure d'archive. Les limites B02 restent toutes actives : îles, Lastovo, recteur de janvier, démographie, tribut, ressources/Krka partagés, hubs et budget.

## Vérification et concurrence

113/113 contrôles propres et 36/36 contrôles de réconciliation/non-régression réussis. Le rejeu des 99 anciens contrôles B02 conserve son résultat brut 96/99 : trois références datées ne correspondent plus au workspace courant, avec justification explicite et empreintes séparées ; les fichiers de preuve historiques ne sont pas réécrits. Les 23 derniers reçus fonctionnels B01/B02 correspondent tous. Voir TEST_MATRIX.md.

Les 2 504 fichiers fonctionnels protégés hors lot sont identiques à l'entrée, dont TECH-R1/R2/R3 et ECON-ALLOYS/quincaillerie. Les deux fichiers communs changent seulement dans MON. Les 113 preuves antérieures/revue technique sont identiques. Sur 873 documents SERG initiaux, cinq ont été modifiés concurremment après notre capture pour le reçu limité de Ratisbonne SERG-RM-0039 ; ils sont conservés, archivés et recensés dans EXTERNAL_SERG_UPDATE.json, 868 restent identiques. Aucune écriture SERG par cette tâche. Aucune écriture Git, aucune modification du vanilla ; identité Git courante inchangée depuis l'entrée B03, sans retour au HEAD historique de B02.

## Progression et prochaine action

L'entrée a été recalculée à partir des critères : 5/80 Balkans et 5/320 WORLD. Ce lot ajoute uniquement T et S au noyau MON : **7/80 Balkans (8,75 %) et 7/320 WORLD (2,19 %)**. O/I/D/E/R restent PARTIAL ; V reste NOT_STARTED. Zéro nouvelle validation joueur ; aucune région close.

Prochaine passe canonique : **BALKANS-04 — possessions ioniennes et places de l'Épire**. Rester en phase balkanique. Les obligations Raguse/Monténégro seront reprises avant clôture technique. Un seul test joueur groupé à la fin des travaux balkaniques techniquement réalisables, puis attente de confirmation explicite avant toute autre région.
''')
    mon=next(r for r in state['phases'][0]['subregions'] if r['id']=='P1-04')
    notes={
        'O':('PARTIAL','BALKANS-03/GEOGRAPHIC_CROSSWALK.md','Noyau MON et Cattaro conservés ; limites exactes des quatre nahije et revendication régionale non closes.'),
        'I':('PARTIAL','BALKANS-03/INSTITUTIONS.md','Sava, coadjuteur et guvernadur corrigés ; modèle des clans, fiscalité et succession ultérieure approximatifs.'),
        'D':('PARTIAL','BALKANS-03/POPULATION_LEDGER.json','Conservation démontrée ; population de 1776 non reconstituée.'),
        'E':('PARTIAL','BALKANS-03/REPORT.md','Assets et ressources conservés ; budget et hubs non validés en moteur.'),
        'T':('STATIC_VERIFIED','BALKANS-03/STARTING_TECH_CHECK.json','Profil initial MON de neuf technologies, prérequis fermés, réserve compatible, aucun PM nouveau.'),
        'R':('PARTIAL','BALKANS-03/INSTITUTIONS.md','Réguliers supprimés et levée conservée ; effectifs exhaustifs et obligations ottomanes non quantifiés.'),
        'S':('STATIC_VERIFIED','BALKANS-03/VALIDATION.json','113 contrôles propres + 36 de réconciliation ; limites du rejeu historique documentées.'),
        'V':('NOT_STARTED','BALKANS-03/GROUPED_RUNTIME_ITEMS.md','Test groupé en fin des travaux techniquement réalisables ; aucune attestation nouvelle.')}
    for k,(status,evidence,remaining) in notes.items():
        mon['criteria'][k]={'status':status,'evidence':evidence,'scope':'Noyau MON et interface conservée de Cattaro ; aucune certification cadastrale ou moteur.'}
        mon['criteria'][k]['note' if status=='STATIC_VERIFIED' else 'remaining']=remaining
    mon['criteria']['V']['test_timing']='END_OF_BALKANS'
    lot={'id':'BALKANS-03','status':'IMPLEMENTED_STATIC_VERIFIED_WITH_HISTORICAL_OBLIGATIONS',
         'scope':['MON institutions and initial clan muster','Cattaro / four nahije interface, no territorial transfer'],
         'runtime':'NOT_RUN','test_timing':'END_OF_BALKANS','files_modified':8,'new_RGBs':0,'new_tags':0,
         'pixels_recolored':0,'people_transferred':0,'world_population_delta':0,
         'receipt':'BALKANS-03/FILES_MODIFIED.json','protocol':'BALKANS-03/GROUPED_RUNTIME_ITEMS.md',
         'historical_research_status':'REGION_INCOMPLETE'}
    if first:state['lots'].append(lot)
    for p in state['phases']:
        n=sum(v['status']=='STATIC_VERIFIED' for r in p['subregions'] for v in r['criteria'].values())
        p['progress']['technical_verified']=n;p['progress']['technical_percent']=round(100*n/p['progress']['criteria_total'],2)
    score=sum(p['progress']['technical_verified'] for p in state['phases'])
    state['progress']['technical_verified']=score;state['progress']['technical_percent']=round(100*score/state['progress']['criteria_total'],2)
    assert score==7 and state['progress']['runtime_user_validated']==0
    (b.OUT/'ROADMAP_STATE.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    marker='BALKANS-03 — 2026-10-25'
    def append(name,text):
        p=b.OUT/name;current=p.read_text('utf8')
        if marker not in current:p.write_text(current.rstrip()+'\n\n## '+marker+'\n\n'+text.strip()+'\n',encoding='utf8')
    append('ROADMAP.md','Noyau MON conservé et institutions/levée corrigées. Deux critères techniques supplémentaires, T et S uniquement : 7/80 Balkans (8,75 %), 7/320 WORLD (2,19 %), zéro validation joueur nouvelle. Rapport : BALKANS-03/REPORT.md. Prochaine passe BALKANS-04, possessions ioniennes et places de l’Épire. La barrière du test balkanique groupé reste applicable ; aucune autre région sans confirmation explicite.')
    append('PROGRESS_HISTORY.md','Entrée recalculée : 5 critères STATIC_VERIFIED, conformes aux preuves B01/B02 ; les 23 derniers reçus fonctionnels correspondent. B03 installe les institutions initiales de MON et une levée de clans : deux fichiers communs, six nouveaux. Aucun RGB/pixel/POP transféré ; monde 834 936 539 → 834 936 539.\n\n113/113 contrôles propres et 36/36 de réconciliation. Rejeu brut B02 : 96/99, trois contrôles de référence datée explicitement réconciliés, sans réécriture des preuves historiques. 2 504 fichiers fonctionnels hors lot et 113 preuves antérieures/revue technique protégés. Mise à jour externe SERG-RM-0039 conservée : cinq documents, reçus et instantanés dans B03, aucune validation WORLD induite.\n\nCrédit uniquement T et S de P1-04 : +2, donc 7/80 et 7/320. Les autres critères restent partiels, V non commencé ; aucune attestation humaine. Prochaine action B04 Ioniennes/Épire, sans transition de phase.')
    append('BLOCKERS.md','Monténégro : titulaire, coadjuteur et guvernadur étayés et installés ; ce constat actualise le blocage initial. Restent limites exactes des quatre nahije, revendication native à toute la région, fiscalité/tribut de janvier 1776, population et effectifs datés, succession future, hubs et viabilité moteur. Aucun motif probant d’annexer MON ou les bouches de Cattaro à un autre pays.\n\nB02 : toutes les obligations insulaires/Lastovo, recteur de janvier, population, tribut abstrait, ressources/Krka partagés, hubs et économie demeurent ouvertes. Les trois divergences du rejeu B02 sont des références historiques datées, documentées dans B03/REGRESSION.json ; ne pas restaurer leurs anciennes baselines.\n\nLes cinq documents SERG modifiés concurremment sont recensés côté WORLD et préservés. Ne pas intervenir dans le suivi SERG. Aucun test intermédiaire requis ; test balkanique groupé seulement en fin de phase techniquement réalisable.')
    append('OWNERSHIP_BOUNDARIES.md','B03 ne transfère aucun territoire : x8C6292 reste MON ; x90A0E0 reste VEN ; xF5F6C2, xA12F82, x446E84 restent TUR. Ni bitmap, état, POPs, ressources, terrain ni hub modifiés. Les deux retouches de fichiers partagés sont strictement internes aux blocs c:MON des histoires de pays et de formations.\n\nLes possessions ragusaines et les passages B02 sont préservés par leurs derniers reçus, sans retour à B01. Le gouvernement natif surchargé garde tous les gouvernements hors MON identiques. Pas de modification fonctionnelle ou documentaire SERG ; mise à jour concurrente de cinq documents seulement observée et archivée dans B03/EXTERNAL_SERG_UPDATE.json. TECH-R1/R2/R3, ECON-ALLOYS et quincaillerie restent hors périmètre.')
    (b.OUT/'NEXT_ACTION.md').write_text('''# Prochaine passe WORLD — BALKANS-04

Référence : 1er janvier 1776. BALKANS-03 installé ; voir BALKANS-03/REPORT.md et DELIVERY_CHECKS.json.

**Possessions ioniennes et places de l’Épire.** Vérifier les possessions vénitiennes insulaires et continentales, leurs autorités et les interfaces ottomanes avec des sources datées, puis retenir un sous-lot cohérent indépendamment testable. Ne pas confondre île, ville fortifiée, juridiction et région native entière.

Avant intervention : lire le suivi WORLD complet et les dernières preuves ; contrôler le workspace courant, les réserves SERG, les interfaces Raguse/Cattaro et la concurrence TECH-R1/R2/R3–ECON-ALLOYS/quincaillerie. Aucun retour à une baseline ancienne, aucune écriture Git ou vanilla. Pour tout nouveau pays, contrôler technologies, dépendances et PM ; conserver le total mondial des POPs ou justifier chaque variation.

Les limites B01/B02 restent ouvertes : îles/Lastovo, recteur de janvier, démographie, tribut, ressources/Krka partagés, hubs et budget. B03 conserve MON et Cattaro, mais ne clôt ni les limites des quatre nahije, ni la fiscalité, ni la revendication régionale, ni les effectifs ou la viabilité moteur. Reprendre ces obligations avant clôture balkanique.

Progression calculée : **7/80 Balkans (8,75 %) ; 7/320 WORLD (2,19 %) ; zéro nouvelle validation joueur.**

Achever les travaux balkaniques techniquement réalisables, préparer un protocole consolidé incluant B03/GROUPED_RUNTIME_ITEMS.md, puis attendre le test groupé du joueur et sa confirmation explicite. Aucun test intermédiaire demandé, aucune autre région WORLD lancée avant cette confirmation. Aucune attestation humaine fictive.
''',encoding='utf8')
    concurrent=json.loads((b.OUT/'CONCURRENT_CHANGES.json').read_text('utf8'))
    concurrent['BALKANS-03']={'receipt':'BALKANS-03/CONCURRENT_CHANGES.json','functional_files_protected':2504,
        'prior_proofs_protected':113,'SERG_entry_proofs':873,'SERG_external_updates_preserved':5,
        'SERG_external_update_receipt':'BALKANS-03/EXTERNAL_SERG_UPDATE.json','SERG_writes_by_this_task':0,
        'old_gameplay_baseline_restored':False,'git_writes':0,'vanilla_writes':0,'world_population_delta':0,
        'preexisting_untracked_work_preserved':'STARTING_TECH_AUDIT_1776_R3_REVIEW_2026_10_25',
        'historical_B02_external_hashes_since_updated_before_B03':['common/pop_needs/00_pop_needs.txt','common/production_methods/01_industry.txt']}
    (b.OUT/'CONCURRENT_CHANGES.json').write_text(json.dumps(concurrent,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    # Final-state correction: the first successful check preceded the other
    # agent's Ortenburg installation. Preserve the dated history, while making
    # the current delivery distinguish unchanged files from observed peer work.
    observations_path=b.LOT/'EXTERNAL_GAMEPLAY_OBSERVATIONS.json'
    if observations_path.exists():
        observed=json.loads(observations_path.read_text('utf8'))
        n=len(observed['files']);unchanged=len(base['protected'])-n
        raw=regression['B02_raw']['passed'];failed=regression['B02_raw']['total']-raw
        for name in ['REPORT.md','TEST_MATRIX.md']:
            p=b.LOT/name;text=p.read_text('utf8').replace('96/99',str(raw)+'/99')
            text=text.replace("identiques à l'entrée",'identiques à l’entrée')
            text=text.replace('trois références datées ne correspondent plus au workspace courant',str(failed)+' références datées ne correspondent plus au workspace courant après les mises à jour concurrentes')
            text=text.replace('Trois échecs de référence datée : Git a légitimement évolué avant l’entrée B03, MON est modifié par B03, cinq documents SERG ont reçu un ajout concurrent.',str(failed)+' échecs de référence datée après les mises à jour concurrentes ; voir EXTERNAL_ORTENBURG_UPDATE.json et REGRESSION.json.')
            text=text.replace("Trois échecs de référence datée : Git a légitimement évolué avant l'entrée B03, MON est modifié par B03, cinq documents SERG ont reçu un ajout concurrent.",str(failed)+' échecs de référence datée après les mises à jour concurrentes ; voir EXTERNAL_ORTENBURG_UPDATE.json et REGRESSION.json.')
            text=text.replace('Les 2 504 fichiers fonctionnels protégés hors lot sont identiques à l’entrée, dont TECH-R1/R2/R3 et ECON-ALLOYS/quincaillerie.',str(unchanged)+' des 2 504 fichiers fonctionnels protégés restent identiques à l’entrée ; '+str(n)+' changements externes sont recensés, sans modification ou annulation par B03. Les cinq fichiers partagés d’Ortenbourg sont reconstruits depuis les preuves indépendantes, dont les quatre pixels bavarois et le transfert de 1 000 habitants, sans variation mondiale. Les autres mutations impériales hors lot sont observées, sans valider ici leurs mécaniques. TECH-R1/R2/R3 et ECON-ALLOYS/quincaillerie sont préservés.')
            text=text.replace('2 504 fichiers fonctionnels hors lot inchangés ;',str(unchanged)+' fichiers fonctionnels hors lot identiques et '+str(n)+' mutations externes recensées, dont cinq fichiers d’Ortenbourg vérifiés ;')
            text=text.replace('Les 23 derniers reçus fonctionnels B01/B02 correspondent tous.','Les 23 derniers reçus fonctionnels B01/B02 correspondaient tous à l’entrée ; trois fichiers ensuite partagés avec Ortenbourg sont réconciliés par ses préimages et sa mutation exacte hors Balkans.')
            text=text.replace('23 derniers reçus fonctionnels identiques ;','23 derniers reçus fonctionnels identiques à l’entrée, puis trois fichiers partagés réconciliés avec Ortenbourg ;')
            text=text.replace('seules les deux différences fonctionnelles supplémentaires MON sont autorisées','deux mutations propres à MON et les travaux externes recensés sont réconciliés séparément')
            p.write_text(text,encoding='utf8')
        doc('CONCURRENT_FINAL_REVIEW.md',f'''# B03 — Concurrence observée avant livraison

La première validation 113/113 et la réconciliation 36/36 précédaient l'installation concurrente d'Ortenbourg. Le contrôle a ensuite été repris sur le workspace composé : {unchanged}/2504 fichiers fonctionnels hors lot identiques, {n} changements externes enregistrés. B03 n'a écrit aucun de ces fichiers.

`EXTERNAL_ORTENBURG_UPDATE.json` vérifie les préimages au regard de l'entrée B03, la reconstruction textuelle du lot voisin, les quatre seuls pixels `(4392,901)`, `(4392,902)`, `(4393,901)`, `(4393,902)`, et l'unique nouveau propriétaire ORT dans STATE_BAVARIA. Tous les états hors Bavière sont identiques ; le total mondial et les POPs de MON sont conservés. Le transfert bavarois de 1000 habitants appartient à SERG, avec zéro variation mondiale et zéro crédit WORLD. Aucun travail SERG n'est installé par ce script WORLD.

Les autres changements de scripts et textes impériaux figurent dans `EXTERNAL_GAMEPLAY_OBSERVATIONS.json` avec leurs empreintes d'entrée et observées. Leurs mécaniques ne sont pas validées ici. Les cinq mises à jour de suivi SERG restent séparées dans leur reçu ; la première observation est conservée. Aucun reçu humain WORLD nouveau.

Le rejeu brut B02 est maintenant {raw}/99 ; ses {failed} échecs de référence datée sont conservés, puis réconciliés par les contrôles actuels. Il ne doit pas être présenté comme 99 succès nouveaux. Voir REGRESSION.json. Les archives B01/B02 ne sont jamais réécrites.
''')
        history=b.OUT/'PROGRESS_HISTORY.md';current=history.read_text('utf8')
        heading='### B03 — revue finale des mutations concurrentes'
        if heading not in current:
            history.write_text(current.rstrip()+f'\n\n{heading}\n\nAprès le premier contrôle, installation externe d’Ortenbourg : quatre pixels bavarois, cinq fichiers partagés, 1000 habitants transférés en Bavière sans variation mondiale. {n} fichiers fonctionnels hors lot ont évolué au total ; {unchanged} restent identiques. Mutations impériales hors périmètre observées sans validation de leurs mécaniques. Voir BALKANS-03/CONCURRENT_FINAL_REVIEW.md. Rejeu brut B02 final {raw}/99, réconciliation courante {regression["passed"]}/{regression["total"]}. Aucune écriture SERG ou crédit WORLD pour ces travaux. Progression inchangée : 7/80 et 7/320, zéro validation joueur WORLD.\n',encoding='utf8')
        concurrent['BALKANS-03'].update(functional_files_unchanged=unchanged,external_functional_files_observed=n,
            external_territorial_receipt='BALKANS-03/EXTERNAL_ORTENBURG_UPDATE.json',
            external_observations='BALKANS-03/EXTERNAL_GAMEPLAY_OBSERVATIONS.json',B02_raw_replay_passed=raw)
        (b.OUT/'CONCURRENT_CHANGES.json').write_text(json.dumps(concurrent,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    b.dump('PROGRESS_CALCULATION.json',{'entry_technical_verified':5,'newly_credited':['P1-04/T','P1-04/S'],
        'Balkans':state['phases'][0]['progress'],'WORLD':state['progress'],'human_attestations_created':0,
        'criterion_evidence':mon['criteria']})
    print('B03 documentation and additive WORLD tracking prepared: 7/80; 7/320; no human validation.')

if __name__=='__main__':main()
