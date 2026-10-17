# MAP-2L — Frontières prussiennes de 1776 : premier correctif appliqué

Statut : **PARTIEL**. Cette passe ne clôt pas les frontières prussiennes ni MAP-2L. Aucune modification de Nassau ou d'Erfurt–Eichsfeld. Aucun commit, merge, changement de branche, indexation Git ou push.

## Modification effective

`x567452`, `STATE_POMERANIA` : **PRU → SWE**, 341 cellules existantes. Ce noyau comprend Rügen et le littoral septentrional de la Poméranie occidentale. Le point portuaire natif nommé Greifswald y est inclus ; ce nom de locator ne constitue pas à lui seul une preuve de frontière ou de position du centre urbain historique.

Il s'agit d'une correction de souveraineté d'une province existante, **pas d'un nouveau tracé de la Peene**. Le bitmap est conservé pixel pour pixel, sans nouvel RGB ni changement de côte, rivière ou State_ID. Les limites internes du State Region ne sont pas des frontières historiques certifiées.

Le registre de jure conserve ces terres impériales, avec SWE comme titulaire légitime. Aucun pays « Poméranie suédoise » n'est créé. La Suède n'entre pas dans le bloc, les électeurs ou la liste des candidats impériaux. Le compilateur et les aperçus de restitution reconnaissent ce titre territorial précis sans exiger de faux statut de membre pour toute la Suède. Aucun territoire suédois, finlandais ou norvégien supplémentaire n'est enregistré. Le calcul existant d'autorité impériale reste distinct de la légitimité territoriale : le pays suédois reste une puissance extérieure.

## Justification et limites

Le dossier conservé `MAP1/MAP1_CASE_DOSSIERS/R2_NORTHERN_CENTRAL_EASTERN_EUROPE-0098.md` établit la souveraineté suédoise au nord de la Peene et sur Rügen après 1720. La carte contemporaine de Mayer/Lotter (1763), conservée par l'université de Greifswald, confirme ce noyau côtier. Le transfert est limité à la province nord existante ; les provinces méridionales `xE1A03A` et `xA04121` restent inchangées.

Source primaire : [Mayer, 1763, université de Greifswald](https://www.uni-greifswald.de/universitaet/einrichtungen/kustodie/wissenschaftliche-sammlungen/sammlungsobjekt-des-quartals/geographische-kartensammlung-die-mayersche-karte/), copie locale et empreinte dans `MAYER_SOURCE.json`.

La Peene et la Trebel ne sont pas représentées dans l'hydrographie native examinée. Aucun décalage uniforme ou calage subpixel n'est prétendu. La matrice identité dans `TRACING.json` est un champ de compatibilité documentaire ; elle n'est **jamais utilisée comme transformation entre la carte ancienne et le jeu**.

La carte générale de Lotter de 1759 est écartée comme arbitre : le [catalogue de Szczecin](https://zbc.ksiaznica.szczecin.pl/dlibra/publication/2869/edition/2489) signale explicitement une frontière suédo-prussienne incorrecte.

Le district de la Netze et l'enclave de Thorn restent à corriger. Dantzig est déjà polonaise (`x80A0A0`) et le demeure. La carte rétrospective de Toeppen (1858, représentant le district de 1772) et l'index des feuilles de Schmettau ont été conservés dans `EVIDENCE/` ; ils ne sont pas transformés automatiquement en transferts fondés sur les noms Bromberg ou Thorn. L'index Schmettau comporte aussi des dénominations postérieures aux partages : il n'est pas traité comme un instantané intégral de 1776. [Catalogue des cartes de Prusse-Occidentale](https://westpreussische-gesellschaft.de/provinz-erkunden/historische-karten/).

## Démographie et économie

40 084 habitants existants sont réaffectés à la subdivision suédoise, sans ajout ni conversion de culture ou religion : 35 578 north_german/default, 3 632 north_german/catholic, 699 polish/default, 175 ashkenazi/default. Allocation entière à l'échelle du jeu, non recensement historique.

Un niveau préexistant d'élevage passe de la subdivision prussienne à la subdivision suédoise ; ses propriétaires économiques sont conservés. Les bâtiments sont conservés mondialement, avec leurs PM et profils pondérés. Les ajouts prussiens récents restent sur la subdivision prussienne : notamment quatre camps de bûcherons et les deux niveaux d'élevage déplacés depuis le Brandebourg. Le total d'élevage de la région reste dix niveaux (neuf PRU, un SWE), et non dix plus un. Les six niveaux d'armes au Brandebourg, les mines, le papier et la suppression du textile en Basse-Silésie ne sont pas modifiés. Aucune unité ni recrutement n'est déplacé.

## Vérifications et test en jeu

Premier contrôle différentiel : **377/377 réussis** ; tests des outils MAP-2L : **30/30 réussis** ; carte native : **16/16 contrôles hors moteur réussis**. La population mondiale reste **835 804 980**, le registre **498 RGB**, l'étendue impériale **62 580 cellules**. `git diff --check` signale encore des espaces de fin de ligne dans les modifications héritées ; les blancs ajoutés dans les nouveaux blocs de cette passe ont été retirés, sans nettoyage global des travaux antérieurs.

Résultats détaillés : `VALIDATION.json`, `POPULATION_VALIDATION.csv` et `MAIN_MAP/VALIDATION.json`. La validation différentielle utilise l'état réel après les micro-ajustements économiques, sans réécrire les anciennes références de tests. Elle contrôle aussi les géométries cumulées des lots précédents, les références, les pays, les gouvernements, les unités et les seuls fichiers autorisés à changer. Ce n'est pas la réexécution intégrale des 17 anciens scripts.

Les 44 doublons RGB et 12 références invalides hérités restent distincts des régressions de cette passe. Les anciens résultats avant les ajouts économiques, dont dix écarts Git historiques autorisés, ne sont pas recertifiés ou masqués. La validation manuelle de SWABIA_COMPLETION et de l'ancien addon industriel est enregistrée séparément ; elle ne valide ni ce nouveau transfert ni les micro-ajustements ultérieurs.

**Nouveau test moteur non réalisé.** Dans une nouvelle partie : vérifier la subdivision SWE en Poméranie, ses populations et son économie ; Stettin/Anklam/Demmin et le reste de la Prusse doivent rester prussiens ; vérifier les ports partagés du State Region, la carte de jure, l'absence de la Suède dans le bloc et l'absence de demande impériale erronée contre son propre noyau légitime. Laisser passer un mois et contrôler unités, échanges et journal.

## Fichiers fonctionnels modifiés

- `common/history/states/00_states.txt` : subdivision côtière suédoise.
- `common/history/pops/00_west_europe.txt` : redistribution conservatrice des profils existants.
- `common/history/buildings/98_build_start_1776_world_redistribution.txt` : un niveau d'élevage réaffecté, propriétaire économique inchangé.
- `map_data/state_regions/00_west_europe.txt` : réémission de la liste de provinces par le générateur, sans changement de contenu ou de référence.
- `common/scripted_triggers/1776_imperial_constitution.txt`, `common/scripted_effects/1776_imperial_constitution.txt` : droit territorial suédois restreint au noyau enregistré.
- `localization/english/1776_imperial_feedback_l_english.yml`, `localization/french/1776_imperial_feedback_l_french.yml` : bénéficiaire suédois dans l'aperçu de restitution.
- `docs/reports/map/MAP2L/IMPERIAL_DE_JURE_REGISTRY.json` et le présent `REGISTRY_MIGRATION.json` : titulaire légal et provenance.

Outils : `map2l_prussian_borders.py`, `validate_map2l_prussian_borders.py`, `map2l_registry.py`, les trois compilateurs `map2k_imperial_system/feedback/repairs.py`, le gestionnaire d'attestations et ses tests. Les rendus cartographiques ont été régénérés ; leur masque ne change pas puisque l'étendue de jure reste identique. Aucun fichier de pays, de gouvernement, de formation militaire ou de recrutement n'est modifié. La liste effective des fichiers fonctionnels changés est conservée dans `VALIDATION.json`.

## Attestation manuelle ajoutée le 15 octobre 2026

Le joueur a confirmé **sept points de contrôle en nouvelle partie et un mois de simulation sans problème** pour le premier correctif prussien. Statut du noyau accepté : **PASS_RUNTIME_USER_VALIDATED**, voir `../RUNTIME_USER_VALIDATION_PRUSSIAN_CORE.json`. Les 341 cellules suédoises et les six niveaux d'armement conservés constituent la référence de MAP-2M. Les mentions de test non réalisé ci-dessus décrivent la livraison initiale et sont remplacées, pour ce seul périmètre inspecté, par cette attestation manuelle. Il ne s'agit ni d'un test moteur automatisé ni d'une certification historique exhaustive ; cette validation ne couvre pas les propositions Peene–Netze non appliquées.

## Mesure ColGrep de la livraison initiale

Un appel `colgrep.exe --agent` a été effectué pour retrouver les sources et dépendances conservées ; sortie 0, deux emplacements retournés puis vérifiés, **tous deux non pertinents**. Le journal est `COLGREP_AGENT.log`. Repli sur les dossiers connus et des recherches exactes avec `rg`, sans reconstruire l'index ni modifier le modèle.

Le mode agent configuré a été invoqué ; la sortie redirigée n'affiche pas de preuve indépendante du chargement du modèle 2B ou de l'utilisation de la Radeon. Durée exacte non instrumentée, compteur fiable des recherches classiques absent, tokens de cette tâche non accessibles. Aucune économie de quota ne peut être chiffrée. Pour cette recherche précise, les résultats n'ont pas évité une recherche utile ; aucun bénéfice n'est démontré.

Les bitmaps PNG et autres ressources binaires ont été inspectés directement, pas recherchés sémantiquement. La couverture exacte de l'index n'a pas été réauditée pendant cette passe.
