# MAP2W-R2-A — Nassau de rive droite et institutions hessoises

17 octobre 2026 — situation historique du 1er janvier 1776.

**Attestation manuelle reçue le 17 octobre 2026 : `PASS_RUNTIME_USER_VALIDATED`, au périmètre général déclaré par le joueur.** Le prompt R2-B indique que les corrections des lots récents, notamment celles du Saint-Empire, fonctionnent sans les bugs précédemment rencontrés. Les territoires inspectés individuellement et la durée de simulation ne sont pas précisés. Voir `../RUNTIME_USER_ATTESTATION_R2B.json`. Aucun test moteur automatisé ni contrôle historique exhaustif n’est revendiqué. Les ajouts R2-B ne sont pas couverts ; les cas C restent ouverts.

Statut de livraison initial conservé dans `VALIDATION_R2.json` : **MAP2W_R2_READY_FOR_SCOPED_RUNTIME_VALIDATION**. Ce premier sous-lot ne termine pas toutes les possessions de Hesse, Nassau et Fulda. Les mentions « test attendu » plus bas décrivent la livraison avant cette attestation, non un refus de la confirmation du joueur.

## Réutilisation des passes précédentes

L’examen chronologique des rapports et migrations a précédé les modifications. Franconie, Rhin central/Mayence/Palatinat, Rhin–Westphalie, Souabe, Anhalt et Thuringe ne sont pas reconstruits une seconde fois. Les anciennes listes de réserves ne sont pas prises pour un état actuel de la carte. La Belgique, Poméranie, Wismar/Poel, Emden, Eutin et les lots MAP2R/S/T/U restent protégés. Le noyau de Fulda de R1 et ses quatre RGB sont inchangés.

Nassau était encore agrégé dans NAS et les rapports rhénans laissaient ses branches ouvertes. Ce premier sous-lot traite des intérieurs identifiables sur la carte conservée, sans prétendre achever toutes leurs possessions. Les sources et précautions sont détaillées dans [HISTORICAL_EVIDENCE_R2.md](HISTORICAL_EVIDENCE_R2.md).

## Corrections réellement installées

Deux pays ajoutés, **NOU — Nassau-Orange** et **NWB — Nassau-Weilbourg**. NAS est conservé et nommé **Nassau-Usingen** ; ses franges héritées non reconstruites restent explicitement C. L’identifiant NOR n’est pas réutilisé : il appartient déjà à la Norvège.

| Secteur intérieur | Propriétaires avant | Après | Cellules transférées |
| --- | --- | --- | ---: |
| Siegen–Dillenburg–Herborn, enveloppe limitée | NAS 12 + WLD 31 | NOU | 43 |
| Weilbourg–Weilmünster, enveloppe limitée | NAS 4 + HES 9 | NWB | 13 |
| Raccord d’Idstein | HES | NAS | 16 |
| **Total** | | | **72** |

Tout se trouve dans **STATE_HESSE, ID économique 74**. Cet ID n’est ni un RGB ni un identifiant historique. Les régions économiques natives ne deviennent pas des pays entiers. Les 561 cellules des trois RGB parents sont toutes conservées. **75 cellules changent de couleur**, dont trois seulement pour isoler un résidu NAS connexe sans changer son propriétaire. Aucun corridor ajouté.

| Parent RGB | RGB après | Propriétaire avant → après | Cellules |
| --- | --- | --- | ---: |
| x1357DB | x1357DB | NAS → NAS, résidu C | 131 |
| x1357DB | xEDB700 | NAS → NAS, résidu C | 3 |
| x1357DB | xEDB701 | NAS → NOU | 11 |
| x1357DB | xEDB702 | NAS → NOU | 1 |
| x1357DB | xEDB703 | NAS → NWB | 3 |
| x1357DB | xEDB704 | NAS → NWB | 1 |
| x3E794B | xEDB705 | WLD → NOU | 31 |
| x3E794B | x3E794B | WLD → WLD, résidu C | 64 |
| x8B7C67 | x8B7C67 | HES → HES, résidu C | 291 |
| x8B7C67 | xEDB706 | HES → NAS | 16 |
| x8B7C67 | xEDB707 | HES → NWB | 8 |
| x8B7C67 | xEDB708 | HES → NWB | 1 |

Neuf nouveaux RGB, **xEDB700–xEDB708**. Chaque RGB forme une composante connexe. Le pays peut avoir plusieurs composantes, sans relier artificiellement ses enclaves. Les petites composantes ne sont pas de nouveaux pays d’une cellule.

Souverains de départ : NOU **Wilhelm V.**, NWB **Karl Christian**, NAS **Karl Wilhelm**, HEK **Friedrich II.**, HES **Ludwig IX.** Les trois derniers héritaient encore de fichiers de personnages vanilla de 1836. Les nouveaux fichiers reprennent exactement les noms de fichiers effectifs pour les remplacer, et non ajouter ces souverains à côté de personnages anachroniques.

HES passe du rang grand-princier hérité du vanilla au rang princier technique. Le gouvernement landgraviat existant, ses titres et ses règles sont conservés. Friedrich II. est personnellement catholique ; la religion et les lois de Hesse-Cassel ne sont pas converties pour autant.

Définitions, capitale technique possédée, localisations FR/EN et drapeaux sont présents. Les nouvelles principautés utilisent les institutions existantes de leur rang. Les armes nassoviennes communes au lion d’or sur bleu sont une **approximation graphique provisoire**, pas la restitution de chaque pavillon historique.

## Statut impérial

Le registre passe de **545 à 554 RGB**, par migration explicite et rejouable. La surface impériale physique ne change pas. NOU et NWB rejoignent les mécanismes existants et le bloc ; aucune sujétion native à l’empereur, aucune union personnelle native avec les Provinces-Unies n’est ajoutée. L’organisation allemande commune de Nassau-Orange repose sur le gouvernement de Dillenburg, et non sur une fusion de tous les États ayant un lien familial.

Le compilateur impérial reproduisait 73/73 fichiers avant la passe. L’ajout des membres et références de provinces nécessite 17 sorties modifiées sur ces 73 fichiers : listes de membres, répliques, votes et restauration des droits. Les neuf électeurs, les transitions d’autonomie, les contributions et les autres règles restent les mêmes. La carte du journal est régénérée depuis le registre, sans extension de son emprise.

## Population et économie

**Aucun recensement de 1776 n’est revendiqué.** Redistribution technique entière par profil culturel et religieux, à partir des populations préexistantes des subdivisions concernées. Les poids spatiaux servent seulement à répartir ces données en l’absence de séries démographiques comparables. Ils ne sont pas présentés comme une densité réelle uniforme.

| Pays | Avant | Après | Delta |
| --- | ---: | ---: | ---: |
| NAS | 313 875 | 309 489 | −4 386 |
| WLD | 43 249 | 29 136 | −14 113 |
| HES | 415 789 | 394 313 | −21 476 |
| NOU | 0 | 27 710 | +27 710 |
| NWB | 0 | 12 265 | +12 265 |
| **Total** | **772 913** | **772 913** | **0** |

Monde : **835 801 255 → 835 801 255**. Fulda conserve ses **20 047** habitants techniques. Le changement de règle démographique autorise une correction historique justifiée ; il n’autorise pas à inventer ici des effectifs précis sans sources.

**Aucun bâtiment, PM, propriétaire économique, recrutement ou infrastructure n’est déplacé ou ajouté par MAP2W-R2.** Les intérieurs tracés ne permettent pas de localiser historiquement les usines des subdivisions sources. Ces dernières subsistent et leurs investisseurs restent valides. Les nouveaux pays disposent de leur population, de leurs terres et des mécanismes de subsistance, sans usine, route, unité ou technologie créée pour améliorer artificiellement leur viabilité. L’emploi, la subsistance et l’accès au marché restent à vérifier en jeu.

Les cinq technologies et les institutions initiales de NAS sont réutilisées pour NOU/NWB ; les références effectives ont été contrôlées. Compatibilité statique vérifiée contre l’installation canonique **Victoria 3 1.13.11**, pas contre une version supposée.

## Vérifications et échecs conservés

- **1 657 / 1 657 contrôles statiques** : bitmap exact, propriétaires, connexité des RGB, régions, terrains, capitales, populations entières, références économiques, ressources et capacités agraires, localisations, personnages, reprise cumulative du registre, sorties impériales et protection des rapports antérieurs.
- **23 / 23 tests ciblés R2**, **60 / 60 contrats cumulatifs**, **17 / 17 attestations/tests R1 conservés** : **100 / 100** au total. Ce sont des tests de fichiers et de modèles de transition, pas des tests exécutés par le moteur du jeu.
- Anciennes photographies MAP2T/U : **30 / 39**, neuf échecs laissés visibles dans `UNIT_TESTS_R2.json`. Sept attentes globales propres à une ancienne étape excluent les ajouts ultérieurs ; deux comparaisons économiques/militaires divergeaient déjà avant R2. Les noms correspondent aux échecs documentés de R1. Les modifications françaises et militaires concurrentes ajoutent également des écarts hors MAP. Les tests anciens et leurs baselines ne sont pas réécrits pour les rendre verts.
- **44 doublons RGB et 12 sélecteurs invalides préexistants**, liste inchangée. Ce résultat local ne certifie pas que le mod entier est exempt d’erreurs.
- Quatre tableaux CSV : valeurs typées, relecture exacte et aperçus visuels ; 20 entrées ciblées, 20 écarts, 17 réserves et 22 lignes de changements. Le workflow tableur a servi à vérifier les livrables, pas à décider les frontières.
- Comparatif avant/après, guide de localisation et empreintes des cellules acceptées sur la carte source examinés visuellement. Les repères cartographiques sont schématiques ; aucune position urbaine native exacte n’est déduite des locators.

Les premières comparaisons globales ont volontairement signalé les écritures extérieures. Elles sont documentées dans `CONCURRENT_WORK_OBSERVED.json`, non effacées de la baseline : le contrôle final distingue ce qui appartient à MAP de ce qui appartient au collaborateur.

## Travaux concurrents et Git

Le HEAD initial était `4e51ba6032370020b7724b0edcc8bfe84460734a`. Un **pull extérieur**, observé dans le reflog, l’a avancé à `f97dc56778a9df6e5b33733089ef47a95977f4b5` : fusion de la PR nº 6 sur les sociétés françaises. Ce n’est pas une opération effectuée par cette passe.

La comparaison des commits n’introduit qu’un fichier de bâtiments : trois propriétaires économiques français, Anzin et Saint-Gobain. Les niveaux, PM et toutes les autres régions restent équivalents. Ce fichier est préservé exactement et n’est pas compté comme une modification MAP2W-R2.

L’autre agent poursuit la mission militaire explicitement prévue : Portugal, Brésil, SC2/SC4, commandants américains et modificateur d’indépendance. Ses fichiers ont été lus uniquement pour classer les écarts. Les blocs de pays hors de sa portée sont vérifiés inchangés. Ses fichiers et nouveaux textes ne sont ni restaurés ni inclus dans notre liste de modifications. Leurs tests et leur validation moteur lui appartiennent. Un travail concurrent peut continuer après notre photographie de contrôle ; l’intégrité finale vérifie séparément les empreintes des fichiers MAP.

**Aucun staging, commit, push, merge, reset, rebase, changement de branche ou écriture dans le jeu canonique n’a été effectué par cet agent.** Aucune archive complète créée.

## Limites et prochaine continuation

Les contours installés sont **B**, pas un cadastre. Les faits de souverain et titulature corrigés sont A pour ces seuls faits. Restent ouverts :

- Nassau-Sarrebruck et les possessions de rive gauche ; aucune réunion anachronique à Usingen.
- Diez/Hadamar et franges de Nassau-Orange ; condominiums et communautés, dont la ville de Nassau et le partage du Vierherrisches.
- Limites fines de Löhnberg après 1773, franges de Weilbourg et acquisitions ultérieures exclues.
- Usingen-centre et Wiesbaden : leurs points diagnostiques restent respectivement HES et FRM. Les 16 cellules du raccord d’Idstein ne terminent pas Nassau-Usingen. Les résidus NAS ne sont pas tous historiquement certifiés Usingen.
- Hesse-Hombourg, Hanau-Münzenberg, possessions dispersées de Hesse et éventuels apanages. Une administration séparée ou une parenté ne suffit pas à décider une indépendance native.
- Geisa, Dermbach, Herbstein et franges de Fulda. La possession fuldienne d’Herbstein est documentée, mais cela n’est pas encore une limite RGB suffisamment reconstruite.
- Démographie territoriale historique, drapeaux complets et viabilité réelle des nouveaux noyaux.

**Erfurt–Eichsfeld reste intact.** Aucune reprise automatique d’une autre région. Le prochain sous-lot devra résoudre un secteur précis de cette liste, pas reprendre les zones déjà traitées.

## Fichiers

Liste exhaustive des 36 fichiers d’exécution attribuables à cette passe : `VALIDATION_R2.json`, champ `runtime_files_modified`, avec empreintes dans `INSTALLED_MANIFEST.json`.

Principales modifications directes :

- `map_data/provinces.png`, `province_terrains.txt`, `state_regions/00_west_europe.txt`.
- `common/history/states/00_states.txt`, `common/history/pops/00_west_europe.txt`.
- `common/country_definitions/00_countries.txt` : seulement le rang HES ; nouveau `1776_map2w_r2_nassau.txt`.
- Historiques de NOU/NWB et fichiers de personnages effectifs NOU/NWB/NAS/HEK/HES.
- Drapeaux et armes `1776_map2w_r2_nassau.txt`, localisations FR/EN dans `replace/` avec priorité explicite.
- Les 17 sorties impériales générées et la carte du journal.

Hors fichiers d’exécution : migration et registre impérial ; `tools/map2l_registry.py` avec garde strictement bornée au lot ; outil `map2w_r2_hesse_nassau.py`, tests ciblés, constructeur des quatre tableaux ; dossiers de preuves, comparatifs, inventaires et validations sous ce répertoire. Le PNG source de la carte du journal est également actualisé. Aucun fichier militaire ou bâtiment n’appartient à cette liste MAP.

## ColGrep

Un appel à `C:/Users/simeo/.cargo/bin/colgrep.exe --agent`, question ciblée sur la localisation des outils de séparation territoriale et de conservation des propriétaires économiques. Sortie conservée dans `COLGREP_SEARCH.log`, commande terminée avec code zéro. Les pistes retournées ont été vérifiées : `tools/build_start_1776_runtime_wave1.py:787`, `tools/prussian_start_micro_adjustment.py:31` et l’historique global des bâtiments. Elles sont surtout liées à l’équilibrage ou à la prévision d’infrastructure, pas au découpage Nassau : aucune décision territoriale ne s’appuie dessus. Les outils déjà connus des anciens lots et les identifiants exacts ont fourni les références utiles.

La sortie capturée ne comporte pas de bannière de modèle ni de trace permettant d’attester indépendamment l’exécution du fichier 2B précis. Ne pas présenter le seul drapeau `--agent` comme une preuve instrumentée du backend. Aucun réglage de modèle, intégration ou reconstruction complète d’index n’a été effectué. Temps de modèle, tokens Codex et recherches évitées non mesurés de manière fiable ; **aucune économie chiffrée de quota revendiquée**. Pour cette passe riche en emplacements déjà connus, le bénéfice observé de cette recherche est faible.

## Contrôle en jeu

Voir [RUNTIME_TEST_PLAN.md](RUNTIME_TEST_PLAN.md), `PLAYER_LOCATION_GUIDE.png` et `HESSE_NASSAU_BEFORE_AFTER.png`. Nouvelle partie au 1er janvier 1776, puis au moins un mois de simulation. La validation demandée concerne les seuls noyaux et institutions supplémentaires, sans certifier toutes les frontières laissées C.
