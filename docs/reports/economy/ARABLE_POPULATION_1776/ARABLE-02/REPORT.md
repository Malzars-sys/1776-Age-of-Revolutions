# ARABLE-02 — contrôle mondial et stabilisation de gameplay

29 octobre 2026 — **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**.

## Autorisation et périmètre

Le joueur maintient les 24 millions d'Agra. Il demande un contrôle automatisé mondial, des redistributions locales pour les communautés décentralisées et des ajouts de terres pour les États incorporés en manque de capacité. Le total canadien autochtone voulu, 2,4 millions, doit être conservé. Ces changements sont des choix de gameplay, pas une nouvelle certification démographique ou une affirmation que tous les peuples décentralisés sont chasseurs-cueilleurs.

Réponse humaine complémentaire : **« Non, conserver ces territoires et signaler ce cas séparément »**, à propos des trois territoires inuits du Nunavut entièrement impraticables. H11, H12 et H13 sont donc inchangés : aucune cellule n'est rendue habitable, aucun peuple n'est vidé pour faire disparaître un signal.

## Résultats installés

| Contrôle | Avant | Projection après |
|---|---:|---:|
| Portions d'État inventoriées | 1 405 | 1 405 |
| Régions géographiques couvertes | 677 | 677 |
| Population déclarée dans les historiques inventoriés | 837 328 654 | 837 328 654 |
| Portions incorporées centralisées en déficit de capacité | 183 | 1, entièrement impraticable |
| Portions décentralisées en déficit de capacité | 53 | 17 |
| Population du scénario canadien H01–H13 | 2 400 000 | 2 400 000 |
| Agra, portion MARATH | 23 928 236 | 23 928 236 |
| Agra, région entière, terres arables | 764 | 764 |

**134 régions** reçoivent au total **6 931 unités de terres arables supplémentaires**. Le changement de chaque région est le maximum requis par ses propriétaires incorporés, sans diminuer les valeurs existantes. Les autres propriétaires d'une région partagée bénéficient aussi mécaniquement de cet ajout ; ce n'est pas un changement de souveraineté.

**50 transferts**, soit **2 613 067 personnes**, répartissent les communautés décentralisées dans des portions voisines disposant de capacité. Les profils de culture, religion, type de POP et autres champs sont conservés ; les identités implicites sont explicitées lorsque nécessaire. Les bâtiments, pays, propriétaires, frontières, homelands, ressources, hubs et terrains ne changent pas.

Les transferts utilisent des contacts latéraux réels entre cellules habitables et respectent les interdictions d'adjacence explicites. Des chaînes de trois contacts au maximum sont admises, sans transporter fictivement les personnes dans les populations intermédiaires. Priorité aux portions du même pays, puis aux communautés ayant déjà une culture en commun. Le Canada H01–H13 constitue l'exception de gameplay explicitement délimitée : mélange de cohortes au sein du scénario régional autorisé, conservation de chaque culture et religion, aucun transfert vers les États-Unis ou l'Alaska. Aucun territoire habité n'est vidé : un petit noyau est conservé lorsque tout le surplus ne peut pas être accueilli.

### Canada : transferts effectifs

| Départ | Arrivée | Habitants |
|---|---|---:|
| Ontario, Anishinabeg H06 | Manitoba, Cris des marais H02 | 126 280 |
| Québec, Inuit du Nunavik H09 | Québec, Eeyou H07 | 120 730 |
| Ontario, Mushkegowuk H05 | Manitoba, Cris des marais H02 | 7 850 |
| Ontario, Mushkegowuk H05 | Saskatchewan, Cris des bois H01 | 30 700 |

Total rééquilibré : **285 560**. Les personnes algonquiennes ou inuites déplacées gardent leur culture et leur religion ; elles ne sont pas transformées en Cris. La HBC et ses 108 626 habitants ne sont pas une réserve de population pour ces opérations. Le découpage territorial n'est pas retouché.

## Méthode et limites du calcul

Le calcul distingue habitants et travailleurs. Il repart des effectifs de main-d'œuvre et des bâtiments effectivement chargés dans la sauvegarde de diagnostic du **1er janvier 1776**, conservée par ARABLE-01. Les données natives ne sont utilisées automatiquement que si la population déclarée correspond et que les fichiers d'entrée sont restés identiques ; l'augmentation déjà acceptée d'Agra est recalculée séparément. Ce contrôle a été réalisé avant installation.

Les emplois commerciaux et industriels existants sont comptés. Les fermes commerciales occupent aussi des terres, qui ne sont pas disponibles pour la subsistance. Les emplois de subsistance suivent les PM locaux : notamment 5 000 emplois par niveau pour la ferme ordinaire et 10 000 pour la rizière observée. Le calcul de terres nécessaires est :

`niveaux agricoles existants + plafond(max(0, travailleurs - autres emplois) / emplois par niveau de subsistance)`.

Pour une région partagée, le minimum régional garantit cette capacité à chaque propriétaire visé, en prenant le plancher d'allocation comme sécurité contre les arrondis. Il n'y a pas de marge forfaitaire de 10 ou 20 %.

**Correction de l'outil préalable :** le poids de partage doit exclure les provinces impraticables et tenir compte de `SPLIT_STATE_PRIME_LAND_WEIGHT = 5.0`. Les portions effectives sont normalisées entre propriétaires existants. Le simple nombre de provinces masquait la pression de l'Ontario et donnait de fausses terres aux îles impraticables. Le calcul pondéré concorde largement avec la sauvegarde, mais certains écarts de carte ou de partage préexistants subsistent. Pour ces écarts, le plan conserve explicitement une fraction mesurée en jeu avec une marge de précision de sérialisation, au lieu de prétendre connaître une géométrie exacte. Le champ `allocation_basis` de chaque ligne expose ce choix.

Pour un transfert, la demande de travailleurs déplacée se fonde sur les ratios de main-d'œuvre observés, avec un minimum de scénario de 30 %. L'accueil utilise le plus élevé des ratios de départ et d'arrivée, sans créer de déficit de capacité chez le receveur dans cette projection. Cela ne simule pas les futures conversions de professions, les qualifications, les salaires, les prix ou les circuits commerciaux.

**Une capacité d'emploi suffisante n'est pas une preuve de disparition de la faim.** Les 61 crises d'ARABLE-01 restent des observations antérieures. Aucun indicateur de famine postérieur n'est inventé à partir du calcul. Le gain de terres accroît aussi le potentiel futur d'agriculture commerciale.

## Cas conservés séparément

- **Nunavut H11, H12, H13** : zéro province habitable, conservés sur demande explicite. Population et géométrie inchangées.
- **Portion russe de STATE_NORTHERN_NORWAY** : 7 028 habitants dans des provinces toutes impraticables ; augmenter le total régional ne lui attribue aucune terre. Aucun changement géométrique non demandé.
- **Autres déficits décentralisés** : des portions d'Alaska, de Libye, d'Australie, du sud de Madagascar et d'Ouganda ne trouvent pas assez de capacité chez les voisins admissibles, ou sont réduites à un petit noyau conservé. Pas de déplacement lointain arbitraire, de changement culturel ou de suppression de population pour masquer ces cas. Liste chiffrée : `REMAINING_CASES.json`.
- Les possessions centralisées **non incorporées** ne sont pas automatiquement assimilées aux États incorporés. Les déficits restants y sont inventoriés séparément.
- Les trois historiques de POP français d'Afrique du Nord déjà absents de la sauvegarde initiale restent une dette préexistante. Le total des historiques inventoriés ne doit pas être présenté comme une nouvelle mesure de la population mondiale chargée en jeu.

## Fichiers et preuves

**21 fichiers runtime** modifiés : 14 fichiers régionaux de `map_data/state_regions/` et 7 historiques de population de `common/history/pops/`. Liste exacte, empreintes et valeurs : `PLAN.json`, reçu : `APPLIED.json`. Les préimages et les fichiers préparés sont conservés dans `preimages/` et `staged/` ; différence lisible : `CHANGES.diff`.

Outils :

- `tools/audit_arable_population_1776.py` : contrôle en lecture seule, calcul de partage pondéré corrigé ; export JSON, CSV et tableau filtrable.
- `tools/stabilize_arable_population_1776.py` : préparation, installation gardée par empreintes, validation indépendante ; réexécution d'une installation déjà faite refusée.
- `tools/test_audit_arable_population_1776.py` et `tools/test_stabilize_arable_population_1776.py` : **22 tests réussis**, portant sur unités de population/main-d'œuvre, PM, consommation de terres, arrondis, proportions de cohortes et étanchéité du groupe canadien.

Les **14 contrôles de validation statique passent** : fichiers installés conformes, autres fichiers suivis préservés, total mondial et canadien, chaque cohorte mondiale, absence de dépopulation, valeurs réelles reparsées, géométrie et autres champs régionaux préservés, commandes d'historique inchangées et capacité prévue. **2 429 autres fichiers runtime suivis** gardent leur empreinte.

Deux incidents de préparation sont conservés : une première proposition envoyait une cohorte canadienne vers un peuple extérieur au groupe autorisé ; elle a été rejetée **avant installation** et archivée dans `preparation_attempts/`. Le premier contrôle des chemins installés comparait les séparateurs Windows et POSIX et donnait un faux échec ; l'écart de représentation a été corrigé, avec le premier reçu conservé. Les contrôles de conservation et de structure n'ont pas été supprimés.

ColGrep : un appel tenté, refus d'accès au verrou de l'index ; aucun modèle 2B exécuté. Recherche exacte et outils existants utilisés en repli. Aucune estimation d'économie de quota.

## Refaire un contrôle et valider en jeu

`WORLD_CONTROL.csv` rapproche, pour chacune des 1 405 portions, population avant/après, travail observé/projeté, terres avant/après, capacité avant/après et réserves. `after_static/` est un nouveau contrôle en lecture seule des fichiers installés, avec ses scénarios de 25/30/35 % ; il ne remplace pas le calcul calé sur la main-d'œuvre native ni un nouveau relevé moteur.

Pour un nouveau contrôle indépendant :

`python -B -X utf8 tools/audit_arable_population_1776.py --out <nouveau_dossier_de_rapport>`

On peut ajouter `--save-text <sauvegarde_texte_locale>` pour importer une observation moteur datée, sans avancer le jeu. Toujours utiliser un dossier neuf afin de préserver les preuves antérieures.

Pour le lot installé : **nouvelle partie en 1776**, vérifier Ontario/Manitoba/Saskatchewan/Québec, Agra et plusieurs États incorporés corrigés. Contrôler population, paysans, emplois disponibles, terres allouées, sécurité alimentaire, salaires et prix ; faire une simulation bornée avec dates relevées et sauvegarde/rechargement. Comparer aussi les territoires impraticables laissés en réserve. Le statut reste **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**, sans prétention de validation moteur ni d'éradication mondiale des famines.

Aucun commit, push, changement du vanilla ou modification des suivis territoriaux WORLD/SERG.
