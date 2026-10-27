# R8-CORRECTIONS-01 — corrections installées, mission régionale partielle

26 octobre 2026 — date de départ : **1er janvier 1776**.

**Suite du 26 octobre : [FLORIDA-01](../FLORIDA-01/REPORT.md) installe maintenant les deux régions administratives de Floride et leurs sièges, Saint Augustine/Pensacola.** Les chiffres et contrôles ci-dessous restent ceux de la livraison R8 initiale. Les limites du contrôle autochtone et colonial en Floride restent ouvertes ; les empreintes partagées sont désormais suivies par la livraison suivante.

**192 provinces réattribuées**, dont 189 à huit ensembles autochtones et trois au littoral britannique. Statut du patch : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. La correction de toute l'Amérique du Nord n'est pas achevée ; les blocs essentiels restant à établir sont détaillés dans [OPEN_PROBLEMS.md](OPEN_PROBLEMS.md).

## Résultat territorial installé

| State_ID | Répartition après correction des anciennes cellules COM |
|---|---|
| STATE_ALABAMA | MSC 20 ; CTW 4 ; CKS 3 ; CHE 1 ; GBR 1 |
| STATE_MISSISSIPPI | CTW 16 ; CKS 8 ; GBR 2 |
| STATE_TENNESSEE | CHE 20 ; CKS 10 |
| STATE_ARKANSAS | OSG 20 ; QPW 10 ; CAD 6 |
| STATE_OKLAHOMA | COM 13 ; WCH 27 ; OSG 7 ; CAD 1 |
| STATE_TEXAS | COM 100 ; CAD 12 ; WCH 8 — les 39 cellules SC1 préexistantes sont préservées |
| STATE_MISSOURI | OSG 15 ; COM 29 encore à corriger |
| STATE_KENTUCKY | CKS 1 ; COM 31 encore à corriger |

Les 8 cellules COM du Kansas et les 12 du Nouveau-Mexique n'ont pas été réattribuées. Onze de ces dernières sont déjà déclarées simultanément SC1 ; défaut hérité consigné, pas nouvellement créé. Au départ, COM apparaissait sur **385 RGB**, dont des State Regions entiers sans rapport avec la Comanchería ; 193 restent déclarés COM après ce patch.

Six nouveaux TAGs : **CTW Choctaws, CKS Chickasaws, CAD Caddos, QPW Quapaws, OSG Osages, WCH Wichitas/Taovayas**. Les TAGs existants **CHE et MSC** sont réactivés comme pays décentralisés, avec capitales de région Tennessee et Alabama plutôt que les anciennes valeurs Arkansas/Floride. Ces pays représentent des ensembles régionaux autonomes, pas huit monarchies centralisées. Les nouvelles bannières sont décoratives, sans prétention à des drapeaux nationaux attestés.

**Précision B** : provinces existantes, correspondance RGB/State_ID vérifiée, marges de chasse et espaces disputés arbitrés pour le jeu. Les sources établissent les régions et groupes ; elles ne certifient pas les seuils géométriques du script. Aucun bitmap, State_ID, terrain, locator ni ressource n'a été redessiné. Les villes-hubs modernes restent une abstraction héritée ; la capitale de pays est un State_ID, pas un village historiquement recalé.

Voir [BEFORE.png](BEFORE.png), [AFTER.png](AFTER.png), [PROVINCE_TRANSFERS.csv](PROVINCE_TRANSFERS.csv) et [SOURCES.md](SOURCES.md).

## Population et dépendances

Chaque cohorte d'origine conserve son State, son effectif cumulé, sa culture, sa religion explicite ou implicite, son type et ses autres attributs. Ventilation par plus forts restes entre portions provinciales : **redistribution technique, jamais estimation de recensement par surface ou nombre de cellules**. Variation de population mondiale introduite : **0**. Aucun bâtiment, PM, réserve, unité ou propriétaire économique supprimé.

Les données héritées sont historiquement problématiques (commentaires citant 1832/1835 et populations de la période des déplacements). Leur conservation empêche une conversion culturelle automatique en fonction du nouveau drapeau ; elle ne les certifie pas en 1776. Les chiffres par pays dans [COUNTRIES_AND_POPULATION.json](COUNTRIES_AND_POPULATION.json) restent à reprendre sur sources démographiques. Les familles culturelles vanilla sont réutilisées sans inventer une nouvelle ethnogenèse ; leurs limites sont explicites dans les problèmes ouverts.

Les huit histoires nationales emploient un profil agricole explicite : `traditional_food_processing`, lois natives compatibles, levée traditionnelle. **Aucun tier européen copié**. Aucun de ces pays ne reçoit de bâtiment industriel ni de formation militaire nouvelle. Les définitions effectives ont été contrôlées pour éviter notamment les collisions avec Chitral/Chechnya/Lippe/Shandong/Shanxi.

HBC : population **108 626**, cultures/religions et commandes de bâtiments conservées. Québec : **323 provinces**, POPs inchangées, antérieurement calibrées à **90 000** ; liaison HBC–Québec–USA inchangée. Les 2,4 millions d'habitants autochtones ajoutés au scénario HBC par décision explicite antérieure du joueur ne sont pas touchés. Pas de mise à jour SERG/WORLD ni d'intervention dans les travaux balkaniques, techniques ou économiques concurrents.

## Fichiers de jeu modifiés

1. `common/history/states/00_states.txt` — seuls blocs COM des huit State Regions et homelands concernés.
2. `common/history/pops/05_north_america.txt` — ventilation conservatoire des cohortes COM de ces régions.
3. `common/history/buildings/05_north_america.txt` — retrait des seuls blocs COM devenus orphelins et **vides** ; toutes les commandes de construction restent identiques.
4. `common/country_definitions/00_countries.txt` — seuls CHE/MSC : type décentralisé, capitale et religion nationale.
5. `common/country_definitions/1776_r8_southern_nations.txt` — six nouveaux pays.
6. `common/history/countries/1776_r8_southern_nations.txt` — huit profils initiaux.
7. `common/flag_definitions/1776_r8_southern_nations.txt`.
8. `common/coat_of_arms/coat_of_arms/1776_r8_southern_nations.txt`.
9. `localization/french/1776_r8_southern_nations_l_french.yml`.
10. `localization/english/1776_r8_southern_nations_l_english.yml`.

Outils : `tools/r8_south_geometry.py` et `tools/r8_south_correct.py`. Préparation séparée, empreintes contrôlées avant application, copies des seuls fichiers touchés dans `before/`, patch dans `patch/`. `PATCH.json` contient les empreintes d'entrée/sortie. Les anciens fichiers partagés n'ont jamais été restaurés depuis Git ou depuis une ancienne passe.

## Vérifications exécutées

- **24 contrôles statiques réussis** : manifeste d'attribution, RGB et State_ID, aucune nouvelle province orpheline/double, frontières hors manifeste préservées, conservation des cohortes et commandes de bâtiments, capitales et pays, localisations FR/EN BOM, témoins HBC/Québec/Hawaï.
- **9 contrôles de références supplémentaires réussis** : cultures/religion existantes, scripts analysables, TAGs uniques, blasons et textures présents, raccord britannique à la Floride existante, autres blocs territoriaux et définitions nationales inchangés ; preuves dans [REFERENCE_AUDIT.json](REFERENCE_AUDIT.json).
- **Connexité** : les huit ensembles forment chacun une composante terrestre dans le graphe des provinces. Tailles : CHE 21, MSC 20, CTW 20, CKS 22, CAD 19, QPW 10, OSG 42, WCH 35.
- Contrat technologique : **8 PASS_STATIC_ONLY**, aucun constat bloquant pour les huit pays de cette passe.
- Non-régression : **16 tests HBC + 4 tests Québec réussis**.
- Les sorties [VALIDATION.json](VALIDATION.json), [TECHNOLOGY_VALIDATION.json](TECHNOLOGY_VALIDATION.json), [CONNECTIVITY.json](CONNECTIVITY.json) et [CUMULATIVE_TESTS.json](CUMULATIVE_TESTS.json) sont propres à cette exécution.
- Version installée lue dans les paramètres du launcher : **1.13.11 Matcha** ; descriptor du mod compatible `1.13.*`.

Ces contrôles ne ferment pas les erreurs héritées : les 11 chevauchements du Nouveau-Mexique, les 60 cellules COM du reste Kentucky/Missouri, les marges du golfe texan et la démographie restent ouverts. Le précédent audit technologique de QUE était FAIL_STATIC sur des prérequis hérités ; cette passe ne lui distribue pas de technologies supplémentaires pour masquer cette dette. Les anciens validateurs exigeant ONT actif sont devenus obsolètes après CANADA-01 : aucun retour à ONT n'a été effectué pour les faire passer.

**Aucun moteur lancé ni résultat de jeu revendiqué.** Voir [RUNTIME_PROTOCOL.md](RUNTIME_PROTOCOL.md) pour nouvelle partie, un mois et sauvegarde/rechargement. Aucun commit, staging, merge, rebase ou push.

## Frontières encore ouvertes et efficacité du modèle local

P0/P1 sont partiellement corrigés. Les deux Florides administratives, Alachua, les postes espagnols et leurs communications, le nord mexicain/apache et les frontières orientales issues des traités restent `RESEARCH_REQUIRED`, avec les raisons et erreurs résiduelles précisément listées. Hawaï est `ALREADY_CORRECT` pour sa configuration en trois pays ; aucun travail R6 refait.

ColGrep-Agent-2B a été appelé **une fois** ; retour terminé mais peu pertinent, vérifié puis écarté pour cette localisation. Ni durée d'inférence, ni tokens Codex, ni économie exacte mesurables ici. **Aucun gain de quota démontré pour cet appel.** Commande, résultat et limites dans [COLGREP.md](COLGREP.md).
