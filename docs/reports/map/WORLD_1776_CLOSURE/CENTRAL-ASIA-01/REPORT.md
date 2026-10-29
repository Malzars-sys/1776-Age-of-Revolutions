# CENTRAL-ASIA-01 — Asie centrale, première passe territoriale

**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION** — référence : 1er janvier 1776. Installation du 29 octobre 2026. **Aucun test moteur ni reçu joueur nouveau.** Les corrections portent sur les appartenances territoriales et leurs dépendances indispensables, sans personnages ni contenu flavor.

## Corrections installées

**172 provinces natives**, dans 7 régions, changent de propriétaire. Aucun nouveau RGB, pixel ou État géographique. Liste exacte dans PLAN.json et GEOGRAPHIC_CROSSWALK.json ; CARTE_REPERES.png montre où regarder.

- Samara/Orenbourg :76 provinces de KZH à RUS. Ouralsk et le port dessiné de Gouriev :2 provinces de KZH à RUS. Trois noyaux d’Irtych — Koriakov/Pavlodar, Semipalatinsk, Oust-Kamenogorsk — passent de OZH à RUS. Ce sont des approximations natives de juridiction fortifiée, pas la preuve d’un contrôle russe de toute la steppe.
- Kokand perd ses extensions prématurées :27 provinces du Syr-Daria et3 des approches de Tachkent vers les jüz ; Tachkent2, Oura-Tépa/Khodjent6, Karategin6, noyau oriental de Koulab2, Choughnan–Rouchan5 et hautes terres kirghizes39 sont distingués. Une province bukharane rejoint le noyau de Koulab. Kokand conserve son noyau ferganien et la cellule d’Osh ; les prétentions locales restent ouvertes.
- **Cinq nouveaux TAG** :TSH,URT,QTG,KLB,SHG ; **KYR réactivé comme agrégat décentralisé de clans**, pas comme État moderne. Les cinq noyaux urbains/royaux sont non reconnus. Tachkent utilise l’oligarchie pour représenter ensemble ses quatre quartiers indépendants, sans anticiper leur unification1784. Aucune nouvelle biographie ou armée n’est créée.
- Capitales régionales :OZH→AKMOLINSK, UZH→SYRDARYA. Le nom interne SEMIRECHE couvre ici le nord-est autour de Semipalatinsk et ne justifie donc pas un transfert massif à la Grande jüz. L’ancrage régional n’affirme pas l’existence d’une capitale fixe dans une ville fondée ultérieurement.
- OZH/UZH ne sont plus des protectorats russes de lancement. KZH garde une **protection nominale privée**, sans paiement, service militaire automatique ou interdiction de guerre/diplomatie propre. Cette relation de jeu traduit une allégeance indirecte ; elle ne certifie pas un contrôle russe effectif de tous ses clans. Les souhaits d’autonomie devenus sans objet sont retirés pour OZH/UZH. Les autres pactes, dont UBD/Alaska et Kalat, restent identiques.

## Institutions et technologies

Six profils explicites anciens, différenciés par les secteurs représentés ; **6/6 PASS_STATIC_ONLY**. Les courts noyaux ruraux n’obtiennent ni banque moderne ni industrie pour satisfaire artificiellement les gates. La loi privée de droits caravaniers reprend les effets du mercantilisme natif et son seul prérequis diplomatique ancien ; aucune recette ou arête technologique commune n’est refondue. Les catégories politiques utilisent un remplacement explicite pour KYR/OZH/UZH, ce qui évite le défaut de doublons africain déjà corrigé.

Lois demandées contrôlées statiquement ; lois effectivement chargées, noms générés, capitales exactes, drapeaux générés et économies restent à observer dans le moteur. Les pays existants conservent leurs dettes techniques héritées ; **aucun nouveau P0/P1 sur 10 témoins**.

## Populations et stocks

Monde : **837 328 654 → 837 328 654**, delta0. Chaque cohorte conserve culture, religion, profession et autres champs. Répartition par comptes de provinces et plus forts restes : allocation technique, **pas un recensement historique**, pas une densité calculée à partir des pixels. Aucun champ de culture ou de religion n’est réécrit. Les confessions implicites restent à observer au chargement ; le proxy national chiite du Choughnan ne constitue pas un recensement ismaélien.

| Région / pays | Avant | Après |
|---|---:|---:|
| FERGANA / KOK | 671 007 | 335 504 |
| FERGANA / TSH | 0 | 41 937 |
| FERGANA / URT | 0 | 167 753 |
| FERGANA / UZH | 0 | 125 813 |
| KIRGHIZIA / KOK | 310 758 | 10 357 |
| KIRGHIZIA / KYR | 0 | 300 401 |
| SAMARA / KZH | 1 410 630 | 0 |
| SAMARA / RUS | 0 | 1 410 630 |
| SEMIRECHE / OZH | 194 139 | 190 094 |
| SEMIRECHE / RUS | 0 | 4 045 |
| SYRDARYA / KOK | 124 804 | 0 |
| SYRDARYA / OZH | 29 200 | 96 059 |
| SYRDARYA / TSH | 0 | 4 457 |
| SYRDARYA / UZH | 157 396 | 210 884 |
| TAJIKISTAN / BUK | 265 148 | 238 634 |
| TAJIKISTAN / KLB | 0 | 41 634 |
| TAJIKISTAN / KOK | 188 998 | 0 |
| TAJIKISTAN / KYR | 0 | 75 599 |
| TAJIKISTAN / QTG | 0 | 45 359 |
| TAJIKISTAN / SHG | 0 | 37 800 |
| TAJIKISTAN / URT | 0 | 15 120 |
| URALSK / KZH | 180 361 | 177 520 |
| URALSK / RUS | 0 | 2 841 |

Tous les niveaux bâtis existants sont conservés. Les services et petites productions de la portion tajike quittée par Kokand sont réattribués aux portions restantes ; ranchs aux communautés pastorales. Ce placement est nécessaire au transfert, sans prétendre restituer des établissements précis. Deux déclarations commerciales transférées utilisent le PM **commerce limité** déjà disponible, au lieu du PM normal verrouillé par les institutions financières organisées. Pas de changement de recette ; les autres PM sont conservés. Les doublons de déclarations préexistants ne sont ni effacés ni certifiés comme niveaux réellement chargés.

Trois conscrits KZH recrutés en Samara sont référencés vers AKTOBE ; un conscrit KOK de la portion tajike vers FERGANA. Tous comptes/types/services et personnages existants sont conservés. OZH garde sa portion SEMIRECHE et sa référence militaire : aucun déplacement inutile.

## Géographie, sources et incertitudes

SOURCES.md distingue la carte1776 réellement vue, les articles historiques et les cartes ultérieures de repérage. Les frontières installées sont des **approximations politiques natives**. Aucun lissage cosmétique ni frontière rectiligne nouvelle. Les six nouveaux profils correspondent à des noyaux connectés ; aucun nouveau pouvoir centralisé isolé au milieu de seules communautés décentralisées.

Le contrôle visuel a corrigé une première sélection erronée de Gouriev : xD1364F est le pointeur minier situé45pixels à l’est du port ; il est rendu à KZH et **xEFFD2B**, le port dessiné, va à RUS. Le premier résultat statique et le plan initial restent archivés dans audit_history/INITIAL ; réparation séparée GURIEV_LOCATOR_REPAIR.json. Un contrôle de syntaxe ou de conservation ne prouve pas à lui seul l’exactitude historique d’une sélection.

Restent ouverts : Darvaz/Badakhshan au contact de DUR ; l’allégeance exacte des vallées pamiriennes ; confins de Hissar, Chahrisabz, Merv/Khiva et autonomie de l’Aral ; limite entre jüz et portée des droits Qing ; cadastre des oasis, position exacte des petites cours et caractère contemporain de Khodjent. Boukhara/Khiva/Turkmènes et les portions Qing sont conservés lorsqu’aucune preuve datée ne justifie un nouveau contour. Cette conservation n’est pas une homologation historique intégrale.

## Concurrence et preuves

**DP-03 installé pendant la recherche est préservé** :18 sorties et6 changements de cellule du Pendjab/Cachemire rapprochés du manifeste et archivés, puis application sur préimages courantes. Aucune portion DUR ou nouveau pays DP, aucun suivi Durrani/Pendjab ni SERG écrit. Afrique et Scandinavie, TECH-R1/R2/R3, ECON-alloys/quincaillerie et Amériques protégés par empreintes et comparaison des nœuds extérieurs ; pas de restauration d’ancienne baseline.7 fichiers existants ciblés + 13 ajouts privés. Aucun Git ou vanilla écrit.

Le premier accès au fichier d’états a échoué avant toute écriture ; préimages vérifiées identiques, échec archivé failed_attempt_01, puis installation autorisée avec le même périmètre et contrôles d’empreinte. Aucun changement extérieur écrasé. Après la correction de Gouriev, un contrôle textuel a relevé un ordre différent des listes malgré des propriétaires identiques : échec conservé dans audit_history, ordre harmonisé sans nouveau transfert. Les libellés du pacte et de sa rupture sont complétés dans le même reçu CANONICAL_ORDER_AND_UI_REPAIR.json. Les 25 clés de chaque langue n’introduisent aucun doublon dans le mod ; preuve SCOPED_LOCALIZATION_AUDIT.json.

**274/274 contrôles statiques PASS** sur la version finale : propriétaires exacts, continuité de provinces, non-enclavement, réserves durranies, cohortes, niveaux/PM, unités, références, profils et empreintes des fichiers extérieurs. Commandes : Python de l’environnement, tools/world1776_centralasia01_install.py --preflight puis --apply ; tools/world1776_centralasia01_closeout.py --tech --validate. La réparation géographique est un patch indépendant et ne rejoue jamais l’application initiale.

Validation moteur **NOT_RUN**. Protocole groupé dans RUNTIME_PROTOCOL.md ; aucun test intermédiaire par micro-lot exigé. WORLD conserve son registre historique **10/320**, 3,13 %, aucun point humain nouveau ; extension auxiliaire1.0.3 sans modification du dénominateur. Aucun passage automatique à une autre région.
