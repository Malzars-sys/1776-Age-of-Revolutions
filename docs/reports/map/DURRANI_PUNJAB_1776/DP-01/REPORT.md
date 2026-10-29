# DP-01 — Empire durrani et Pendjab au 1er janvier 1776

**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION** — 29 octobre 2026. Aucun test moteur et aucune homologation humaine attribués à cette installation.

## Résultat

La vérification a trouvé des corrections nécessaires. La condition donnée par le joueur pour passer directement à l'Asie centrale (« s'il n'y a pas de changement ») n'est donc pas remplie : **aucun territoire ni pacte kazakh, russe ou d'Asie centrale n'a été modifié**.

- **KAL réactivé**, sans nouveau TAG : noyau Kalat–Sarawan–Jhalawan/Kacchi et ville de Quetta. **Douze provinces** passent de DUR à KAL, dont onze de `STATE_BALUCHISTAN` et une de `STATE_QUETTA`. Pishin (`x1910AD`) reste DUR ; le Gwadar MAK installé antérieurement est conservé. Mir Nasir Khan Ier devient le dirigeant. Son âge exact n'est pas inventé.
- **PTA réactivé** : noyau **Patiala–Sirhind**, trois provinces de `STATE_HILL_PUNJAB`, sous Amar Singh. C'est une enveloppe de gameplay des deux centres, pas la totalité des chefferies cis-Sutlej ni un tracé cadastral. Aucune protection britannique de 1809 n'est anticipée.
- **PAN**, représentation collective préexistante des misls, reçoit **quatre provinces des plaines** autour des hubs Amritsar/Ludhiana et du Doab de Jalandhar. Son nom de confédération et le Jathedar Jassa Singh, déjà présents dans les corrections antérieures, sont conservés. Le détail de tous les misls n'est pas créé.
- **Multan était déjà PAN** ; pas de transfert inventé ni de reconquête durranie de 1780 anticipée. **Kaboul et Timur Shah étaient déjà correctement initialisés** ; ils ne sont pas refaits.
- Les templates vanilla de la cour sikh de 1836 et des deux pays réactivés sont remplacés par l'initialisation de 1776. Le journal de succession des maharajas de 1839 n'est plus ajouté à PAN au lancement de 1776 ; sa définition n'est pas supprimée.
- **Six pointeurs de hubs** sont réalignés sur les locators nommés effectivement présents : Kalat/Sibi, Lahore/Multan, Amritsar/Patiala. Les anciennes références plaçaient notamment le pointeur Kalat sur la côte. Les emplacements des locators, le bitmap et les State_ID ne sont pas déplacés.

Total : **19 provinces transférées**, deux TAGs existants réactivés. Pas de nouveau pays de nom ou de frontière inventé pour remplir les secteurs non résolus.

## Contrôle, suzeraineté et limites de représentation

Le gouvernement local de Kalat est distingué de l'administration directe durranie. Un lien spécifique **DUR → KAL** conserve la suzeraineté nominale, **sans versement régulier**, sans souverain partagé ni incorporation automatique, avec initiatives diplomatiques propres et sujets permis. La participation conditionnelle à certaines expéditions extérieures, décrite par les sources, n'est **pas** reproduite : l'appel automatique à toutes les guerres serait excessif. Marché partagé, protection militaire et rupture effective du pacte doivent être observés en jeu ; un type de sujet natif n'est pas la transcription du traité.

Patiala est représenté par son propriétaire local ; titres accordés par les Durrani et engagements personnels ne sont pas transformés sans preuve en annexion, tribut permanent ou protectorat britannique.

Les coordonnées des aperçus servent uniquement au repérage. Le modèle a treize contrôles et une précision indépendante **non établie** ; certains hubs du Pendjab/Cachemire sont décalés de plusieurs dizaines de pixels. Les transferts retiennent des noyaux nommés et leurs cellules contiguës ; **aucune superposition cadastrale d'une carte de 1776 n'est prétendue**. Les franges restent des approximations de provinces entières.

## Conservation des habitants, bâtiments et forces

Les deux fichiers POPs conservent respectivement **22 545 523** et **190 000 000** habitants. Chaque combinaison culture/religion/statut est conservée par State_ID. Aucun chiffre vanilla n'est réinjecté à la place des valeurs courantes.

La comparaison avec les subdivisions vanilla sert seulement à identifier la provenance de groupes que le mod avait regroupés sous DUR : cohortes KAL et PTA récupérées dans leur ordre courant. **Ce n'est pas une démographie de 1776**. Les 8 010 habitants étiquetés Brahui affectés à la portion de Quetta constituent une répartition technique provisoire explicitement signalée, sans prétendre définir une frontière ethnique.

| Région | Stock courant après réaffectation |
| --- | --- |
| STATE_BALUCHISTAN | KAL : 461 912, DUR : 394 946 |
| STATE_QUETTA | KAL : 8 010, DUR : 225 531 |
| STATE_HILL_PUNJAB | PAN : 1 627 993, PTA : 795 451, DUR : 398 579 |

Les bâtiments du noyau civil de Kalat suivent KAL. Les cinq niveaux administratifs des collines sont répartis DUR2/PAN2/PTA1, et les deux niveaux de routes PAN1/PTA1. Ranchs, plantations, méthodes de production, réserves et participations sont conservés. Les déclarations du fichier mondial98 restent cohérentes avec les histoires régionales ; aucun niveau civil supplémentaire n'est ajouté.

**Seize unités de conscription existantes** sont réaffectées : huit à PAN, quatre à KAL, quatre à PTA. DUR conserve deux conscriptions dans chacune des deux régions de recrutement concernées. Types, régions et quantités globales sont identiques ; aucune armée permanente, caserne explicite ou population n'est ajoutée pour gonfler les nouveaux pays. Cette répartition technique n'est pas un décompte des armées de 1776.

KAL/PTA ont des profils initiaux explicites et sobres, sans palier industriel copié. Trois variantes de lois limitées à ces pays maintiennent les effets natifs souhaités pour les douanes, la servitude coutumière et, à Patiala, la tolérance des cultes. Elles évitent d'accorder gouvernement constitutionnel ou réseaux scientifiques institutionnalisés pour satisfaire des prérequis tardifs. Ce sont des abstractions du moteur, pas une certification de leurs codes juridiques.

## Vérifications

- **127 contrôles statiques ciblés réussis** : changements exactement conformes au plan, unicité des attributions dans les régions concernées, régions et ressources conservées, capitales possédées, cœurs KAL/PTA connectés par arêtes, Pishin et Gwadar témoins, maintien des corrections arabiques.
- Stocks de POPs et niveaux civils conservés, ainsi que types/nombres/régions de recrutement militaire. Les contenus syntaxiques extérieurs aux scopes sont comparés aux préimages actuelles dans les fichiers partagés.
- **KAL et PTA : PASS_STATIC_ONLY** pour technologies, recettes sélectionnées, demandes de lois et unités. **DUR et PAN : erreurs antérieures conservées, aucun nouveau signal**. Les alertes héritées ne sont pas maquillées en réussite générale de l'Asie.
- Paires action/type de sujet et transfert financier nul, caractères de 1776, suppression des templates de 1836, références de hubs, localisation FR/EN avec BOM et clés nouvelles uniques vérifiés.
- 0 changement(s) de runtime hors fichiers du lot constaté(s) depuis la préparation : conservés dans `CONCURRENT_RUNTIME_DELTA.json`, sans attribution à cette passe.

Commandes exécutées : `dp01.py`, `dp01_geography.py`, `dp01_plan.py`, `dp01_install.py --prepare`, `--apply`, `dp01_profile_repair.py`, `dp01_audit.py`, `dp01_closeout.py --finish`, puis nouvel audit et clôture. L'installation contrôle les empreintes avant chaque écriture et conserve les préimages ; aucun ancien fichier partagé n'est restauré globalement.

Ces résultats ne prouvent ni chargement moteur, ni emploi des bâtiments, ni équilibre alimentaire/budgétaire, ni placement des hubs secondaires par le moteur. Voir `RUNTIME_PROTOCOL.md`.

## Réserves ouvertes

1. **Bahawalpur**, les autres chefferies cis-Sutlej et les contours fins de chaque misl restent à cartographier ; les trois provinces PTA ne représentent pas Jind, Nabha et toutes leurs enclaves.
2. **Jammu, Ladakh, Garhwal et autres États des collines** : l'ancien propriétaire DUR de leurs secteurs restants n'est pas historiquement certifié. Le calage courant ne permet pas de transformer ces réserves en frontières précises sans un lot himalayen spécifique.
3. **Makran, Kharan, Las Bela et confins baloutches** : influence, partage de revenus et administration Gichki ne se confondent pas. Pas de transfert uniforme des65 anciennes provinces à Kalat. La présente passe ne clôture pas ces périphéries.
4. **Bactriane, Hazarajat et confins pachtounes** : conserver leur traitement actuel ne démontre pas une administration uniforme de Timur Shah.
5. Répartition démographique locale, ressources par propriétaire d'État partagé, revenus et capacité d'emploi : contrôles approfondis ouverts. Les stocks conservés ne sont pas un recensement validé.

La prochaine étape demandée conditionnellement, **Asie centrale et trois jüz kazakhs**, n'est pas installée ici. Leur état de dépendance envers la Russie devra être vérifié séparément ; le simple serment d'un khan n'établit pas l'administration russe uniforme de tous les jüz.

## Fichiers runtime modifiés ou créés

- `common/history/states/00_states.txt`
- `common/history/pops/09_central_asia.txt`
- `common/history/pops/10_india.txt`
- `common/history/buildings/09_central_asia.txt`
- `common/history/buildings/10_india.txt`
- `common/history/buildings/98_build_start_1776_world_redistribution.txt`
- `common/history/military_formations/04_military_formations_middle_east.txt`
- `common/history/military_formations/05_military_formations_india.txt`
- `common/history/military_formations/1776_dp01.txt`
- `common/history/countries/kal - kalat.txt`
- `common/history/countries/pta - patiala.txt`
- `common/history/characters/pan - punjab.txt`
- `common/history/characters/kal - kalat.txt`
- `common/history/characters/pta - patiala.txt`
- `common/history/countries/pan - panjab.txt`
- `common/laws/1776_dp01.txt`
- `common/subject_types/1776_dp01.txt`
- `common/diplomatic_actions/1776_dp01.txt`
- `common/history/diplomacy/1776_dp01.txt`
- `map_data/state_regions/09_central_asia.txt`
- `map_data/state_regions/10_india.txt`
- `localization/french/replace/1776_dp01_l_french.yml`
- `localization/english/replace/1776_dp01_l_english.yml`

Outils et preuves dans ce dossier et `tools/dp01*.py`. Aucune écriture dans le vanilla, aucun commit, merge, rebase ou push. Les suivis WORLD/SERG et les reçus américains restent hors mission ; aucun pourcentage de clôture ne leur est attribué.

## ColGrep

Un appel à `C:/Users/simeo/.cargo/bin/colgrep.exe --agent` a été tenté pour localiser les dossiers Durrani/Pendjab et les dépendances. Échec en **1,34 seconde environ**, au verrou de l'index local : accès refusé, erreur système5. Le modèle2B n'est pas confirmé comme exécuté ; repli sur les dossiers R3/R4 connus et `rg`. Aucun réglage, modèle ou index n'a été modifié. Les tokens Codex et une économie comparative fiable ne sont pas disponibles.
