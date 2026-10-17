# MAP2L — Franconie, lot principal appliqué

Date de finalisation : 13 octobre 2026. Démarrage visé : 1er janvier 1776.

Mise à jour du 14 octobre : **PASS_RUNTIME_USER_VALIDATED** pour les territoires franconiens et principautés inspectés par le joueur dans une nouvelle partie. Test manuel déclaré, pas test moteur automatisé. Les contrôles statiques et leurs alertes Git historiques sont conservés séparément ; ni les frontières non inspectées ni toutes les juridictions ne sont certifiées. Reçu : `../RUNTIME_USER_VALIDATION.json`.

## Territoires implémentés

| Pays | Représentation | Pixels | Population de départ répartie |
| --- | --- | ---: | ---: |
| ANS | Ansbach-Bayreuth, un margrave et deux ensembles territoriaux | 485 | 357 744 |
| FBM | Principauté épiscopale de Bamberg | 181 | 133 509 |
| WZB | Principauté épiscopale de Würzburg | 459 | 338 566 |
| NUR | Ville libre de Nuremberg et territoire oriental | 109 | 80 400 |
| EIC | Fragment septentrional d'Eichstätt seulement | 44 | 32 455 |
| COB | Fragment ajouté au pays Cobourg existant | 44 | 32 455 |
| BAV | Franges conservées provisoirement, attribution non résolue | 662 | 488 301 |
| Total | Région économique STATE_FRANCONIA | 1 984 | 1 463 430 |

Cinq nouveaux tags sont créés. FBM évite une collision avec le tag natif BMB. Les huit identités RGB natives deviennent **43 provinces connexes**, dont **35 nouvelles**. Les frontières des régions économiques voisines ne sont pas modifiées. La liste exhaustive des RGB, parents et propriétaires figure dans `TERRITORIAL_CHANGES.csv`.

Les nouveaux pays rejoignent le bloc impérial, Nuremberg la liste des villes libres ; aucun électorat supplémentaire n'est inventé. Les mécanismes de succession, vote, demandes impériales et principes sont recompilés avec leurs nouvelles listes de membres. Le registre de jure passe de 324 à **359 identités**, sans changement de son étendue géographique franconienne. Les cartes principale et du journal sont régénérées. La Belgique et les neuf provinces piémontaises restent conservées ; la Sardaigne reste hors des provinces enregistrées.

Les cinq nouvelles capitales utilisent une région économique possédée. Les pays reçoivent les technologies déjà présentes dans BAV, sans octroi massif d'avancées tardives. Trois variantes de lois limitées aux nouveaux pays permettent leurs institutions de départ sans débloquer artificiellement des technologies ultérieures. Nuremberg possède un gouvernement de conseil oligarchique ; les trois principautés épiscopales sont théocratiques. Les bannières sont des identifiants procéduraux, pas des armoiries historiques certifiées.

## Conservation et limites

La population mondiale reste **835 804 980**. Chaque profil de culture/religion et chaque total régional est conservé. La répartition des 1 463 430 habitants franconiens suit la surface des enveloppes, avec arrondis conservatifs : ce n'est pas un recensement de 1776. `POPULATION_VALIDATION.csv` détaille les trois profils initiaux et leur répartition.

Les niveaux de bâtiments, méthodes de production et autres attributs pondérés par niveau sont conservés. Les administrations publiques suivent le nouveau contrôleur ; les détenteurs économiques privés préexistants restent BAV dans sa subdivision subsistante. Les armées, marines, formations et recrutements existants ne sont pas modifiés ; aucun contingent historique conjectural n'est ajouté aux nouveaux pays.

La méthode et les sources sont dans `GEOGRAPHIC_EVIDENCE.md`. Le contrôle indépendant de Ratisbonne présente un écart de 5,121 pixels du jeu. Les minuscules enclaves sont abstraites sans dilation. **Un tiers de la surface native (662 pixels, 33,4 %) reste une frange non résolue à BAV.** Cela comprend des limites ou juridictions qui exigent une passe ciblée, pas une affirmation de souveraineté bavaroise. `UNRESOLVED.csv` liste aussi les villes secondaires, le prolongement d'Eichstätt, les noms dynastiques existants et les limites de la simulation d'un évêque commun à Bamberg/Würzburg.

## Fichiers modifiés

Les manifestes `PLAN.json` (20 fichiers textuels, dont registre et migration) et `IMPERIAL_FILES.json` (16 fichiers impériaux recompilés) donnent les chemins exhaustifs. Principaux groupes :

- Territoires : `map_data/provinces.png`, `map_data/province_terrains.txt`, `map_data/state_regions/00_west_europe.txt`, `common/history/states/00_states.txt`.
- Démographie et économie : `common/history/pops/00_west_europe.txt`, `common/history/buildings/00_west_europe.txt`, `common/history/buildings/98_build_start_1776_world_redistribution.txt`.
- Nouveaux pays : définition commune `1776_map2l_franconian_estates.txt`, cinq historiques de pays, dirigeants, drapeaux, gouvernement de Nuremberg, variantes de lois et localisations françaises/anglaises.
- Intégration impériale : bloc initial, identité, triggers, effets, événements, journal, votes, listes et localisations recompilées ; registre actif `../IMPERIAL_DE_JURE_REGISTRY.json`.
- Graphismes : `gfx/interface/journal_entries/aor1776_hre_registered_map.dds`, `gfx/map/map_painting/aor1776_hre_mask.dds`, `gfx/map/map_painting/aor1776_hre_sentinel.dds` et aperçus générés.
- Outils : `tools/map2l_franconia.py`, `tools/validate_map2l_franconia.py`, compatibilité des compilateurs/validateurs `map2l_registry.py`, `map2k_imperial_feedback.py`, `validate_map2l_belgium.py`, `map2l_piedmont.py`, `audit_map2l_hre_readiness.py`. Aucun nouvel audit de readiness n'a été exécuté.

Les sauvegardes initiales ne sont pas réécrites. Le bitmap candidat franconien et les inventaires différentiels permettent de vérifier les seuls changements attendus. Aucun commit, staging, merge, rebase ou push n'a été réalisé ; HEAD et index sont vérifiés inchangés.

## Résultats techniques

Dernière exécution des suites :

- `validate_map2l_franconia.py` : **473/473**, PASS_STATIC_ENGINE_PENDING.
- `validate_map2l_belgium.py` : **315/315**, PASS_STATIC_ENGINE_PENDING ; les 413 pixels belges et 1 028 pixels franconiens modifiés sont admis explicitement.
- `map2l_piedmont.py validate` : **232/232** ; les 2 227 pixels de l'extension piémontaise restent exacts.
- Carte principale : **16/16 contrôles hors moteur** ; DDS sans perte, masque mondial exact de 62 516 pixels, aucune collision avec les 91 textures natives examinées ; compilation du helper HLSL réussie. Ce test n'est pas la compilation complète du shader dans le jeu.

Les 43 provinces sont connexes, présentes, attribuées exactement une fois dans le lot ; aucun nouveau propriétaire manquant, doublon ou renvoi invalide n'est introduit. Les 359 RGB du registre sont uniques. Les sorties du compilateur correspondent aux fichiers runtime et les tests impériaux précédents restent réussis.

**Préexistant, séparé des régressions :** l'inventaire mondial conserve exactement 44 RGB doublement attribués et 12 erreurs de références hérités hors de ces corrections. Le lot ne les introduit ni ne les corrige silencieusement. Les initialisations politiques anciennes d'autres pays ne sont pas refondues ici.

**Moteur non testé :** charger une nouvelle campagne au 1er janvier 1776 ; contrôler la sélection des cinq pays, leurs propriétaires, gouvernements et lois, la carte principale, le journal et l'absence de nouvelles erreurs dans les logs. Une sauvegarde ancienne ne suffit pas pour tester le nouvel historique de départ.

## Prochain lot retenu

**Rhin central : Mayence et Palatinat en premier.** Ce lot prolonge le bord occidental de la Franconie, permet de traiter le raccord d'Aschaffenburg et remplace progressivement les approximations électorales de MAP2K. Il est prioritaire avant une grande passe de Westphalie ou de Souabe.

Réutiliser les dossiers territoriaux existants, résoudre les possessions partagées par province et les franges franconiennes raccordables, puis appliquer la même conservation différentielle. Cologne et Trèves ainsi que Clèves/Mark/Ravensberg viendront ensuite selon les dossiers disponibles. Le redécoupage des possessions prussiennes occidentales reste prévu ; il n'est pas compris dans la modification franconienne actuelle. Ce choix n'est pas une attribution anticipée de toutes les terres rhénanes à un pays : **aucun découpage du prochain lot n'a encore été appliqué**.

## ColGrep et mesure des ressources

Les instructions ColGrep installées sont respectées. Pendant cette finalisation, les chemins et identifiants nécessaires étaient déjà établis : **aucun appel au modèle local 2B** n'était nécessaire ; relancer une recherche exploratoire aurait été redondant. Trois commandes ciblées `rg` ont servi à vérifier des identifiants, les points du générateur et les fichiers présents avant la rédaction du rapport ; les autres lectures sont des lectures directes de fichiers connus et des tests, pas des recherches sémantiques.

Il n'y a donc pas de temps d'inférence 2B ni d'économie de quota mesurable à attribuer à cette finalisation. Aucun compteur fiable de tokens par opération n'est accessible ici et aucune comparaison A/B n'a été faite. L'intérêt du 2B demeure la localisation exploratoire d'un dossier inconnu ; il ne remplace ni le tracé historique, ni les contrôles de conservation, ni les essais du moteur.

Actualisation incrémentale exécutée avec `& 'C:/Users/simeo/.cargo/bin/colgrep.exe' init .` : **40 fichiers ajoutés, 26 actualisés, 0 supprimé, 4 322 inchangés**, soit 4 388 fichiers. Aucun effacement/rebuild n'a été demandé. Cette actualisation de l'index n'est pas une exécution de ColGrep-Agent-2B. La première consultation du cache sous sandbox a reçu « accès refusé » ; l'actualisation autorisée a ensuite réussi. La durée totale exacte de l'actualisation asynchrone n'a pas été instrumentée. Les bitmaps/DDS sont vérifiés directement par les outils d'image et les CSV par lecture structurée : leur contenu n'est pas supposé couvert par les recherches sémantiques.

## Aperçu

`BEFORE_AFTER.png` montre le bitmap réellement appliqué : gris = franges maintenues à BAV, orange = ANS, bleu = FBM, violet rose = WZB, rouge = NUR, vert = EIC, violet = COB. `HISTORICAL_OVERLAY.png` montre les enveloppes dans la carte source ; il ne s'agit pas d'une capture de partie Victoria 3.
