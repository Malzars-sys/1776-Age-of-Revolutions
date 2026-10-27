# BALKANS-04 — Possessions ioniennes et places de l'Épire

Livraison : 25 octobre 2026. Référence : 1er janvier 1776.
Statut : IMPLEMENTED_STATIC_VERIFIED_WITH_HISTORICAL_OBLIGATIONS. Moteur : NOT_RUN. Aucune validation joueur WORLD nouvelle.

## Corrections installées

Les quatre postes continentaux sont distingués de leur arrière-pays ottoman et attribués à Venise. Cérigo/Cythère est également rendue à Venise : son île était dessinée séparément, mais rattachée à TUR. Les deux RGB ioniens déjà vénitiens — Corfou et le groupe natif Leucade/Céphalonie/Zante — restent identiques.

| Possession | Parent et RGB nouveau | Région native | Pixels transférés | POPs réaffectées |
| --- | --- | --- | ---: | ---: |
| Butrinto | `x7BE071` → `xE8D211` | STATE_ALBANIA | 2 | 500 |
| Parga | `x8050E0` → `xE8D212` | STATE_THESSALIA | 2 | 3000 |
| Preveza | `x8050E0` → `xE8D213` | STATE_THESSALIA | 2 | 1700 |
| Vonitsa | `x518791` → `xE8D214` | STATE_ATTICA | 2 | 1000 |
| Cerigo / Kythera | `x0055D7` → `xE8D215` | STATE_PELOPONNESE | 33 | 7500 |

Total : **5 RGB nouveaux, 41 pixels terrestres** (8 pour les postes, 33 pour Cérigo), zéro terre ou côte créée, zéro TAG nouveau. Le continent du parent péloponnésien et son petit îlot oriental non identifié restent ottomans. Les terrains sont hérités des parents. Les quatre noyaux de deux pixels sont des approximations politiques, pas des frontières cadastrales.

Une revue insulaire a permis d'ajouter Cérigo au lot après l'installation des quatre postes. L'extension a utilisé les versions courantes et leurs reçus : KYTHERA_EXTENSION.json. Aucun fichier complet n'a été restauré depuis une ancienne baseline. Cérigo reste dans la région native STATE_PELOPONNESE ; aucun découpage administratif régional ni hub ottoman n'est déplacé.

## Démographie

**13 700 habitants** sont réaffectés des pools grecs TUR vers VEN. Les cultures, religions implicites/explicites, professions et tous les autres pools sont conservés. Monde : **834 936 539 → 834 936 539**, variation nulle.

| Région | Total avant | Total après | Population VEN ajoutée |
| --- | ---: | ---: | ---: |
| STATE_ALBANIA | 1 074 401 | 1 074 401 | 500 |
| STATE_THESSALIA | 962 724 | 962 724 | 4 700 |
| STATE_ATTICA | 542 293 | 542 293 | 1 000 |
| STATE_PELOPONNESE | 188 816 | 188 816 | 7 500 |

L'effectif de Prévéza reprend l'ordre de grandeur d'un recensement situé vers 1780, rendu et vérifié dans Komis. Les 7 500 de Cérigo reprennent une indication de fin de période vénitienne ; les autres valeurs sont des calibrations modestes. Aucun de ces chiffres n'est présenté comme un recensement exact de janvier 1776. Butrinto désigne le poste et son environnement de pêcheries ; aucune grande ville repeuplée n'est inventée. Voir POPULATION_LEDGER.json et SOURCES.md.

## Institutions, bâtiments et technologies

Administration directe VEN, dans le cadre existant du Stato da Mar ; pas de nouvelle république ionienne, protectorat britannique ou pays autonome anachronique. Lois, souverain, diplomatie et formations militaires de Venise restent inchangés. Les compétences locales des conseils et provveditori sont documentées ; aucun titulaire de janvier non vérifié n'est inventé.

Quatre mouillages minimaux sont ajoutés, un par nouvelle portion VEN des régions natives, avec le PM existant pm_anchorage. Un niveau de fortification navale de base dans les Ioniennes représente le complexe corfiote. Il ajoute 1 000 emplois de garnison, les mouillages 400 emplois : **1 400 emplois de capacité**, non une embauche attestée. La fortification consomme 5 armes légères et 5 fer à plein emploi ; les mouillages n'ajoutent pas d'intrants. Les anciennes installations ioniennes et tous leurs PM restent identiques.

Les **27 technologies VEN** sont conservées et leurs prérequis fermés. Les bâtiments, groupes et PM sont résolus, leurs gates satisfaits ; scientific_fortification_siegecraft est déjà acquis. Aucun grant, graphe technologique, recette commune ou gate n'est modifié. Aucun nouveau bâtiment-type ou PM-type n'est créé.

## Limites historiques et moteur

Les ressources, terres arables et traits restent partagés selon les régions natives ; cette passe ne les répartit pas historiquement entre les petits postes et l'arrière-pays. Les hubs partagés et le placement des ports minoritaires, l'accès au marché, les qualifications, le budget et les effectifs effectifs restent à vérifier au test groupé. La fortification corfiote produit des effets à l'échelle de la région ionienne du moteur, pas un périmètre de siège cadastral.

Ithaque n'est pas distinguée proprement de la géométrie céphalonienne. Paxos, les Strophades, Anticythère et l'îlot oriental du parent péloponnésien demandent une identification plus sûre ; aucune terre nouvelle ou attribution arbitraire n'est créée pour les forcer. Les limites exactes des juridictions et les minorités ne sont pas closes. Les obligations B01/B02/B03, dont Lastovo, Krka partagé, recteur ragusain, fiscalité monténégrine et budgets, demeurent ouvertes.

## Vérification, concurrence et suivi

**107/107 contrôles statiques réussis**, notamment conservation de tous les anciens propriétaires, cellules hors masques, POPs mondiales et profils culturels/religieux, ressources et hubs hors listes de provinces, prérequis et PM, pixels ragusains, Cyclades et huit reçus fonctionnels B03. Les résultats ne valent pas validation moteur.

Les 2521 fichiers fonctionnels protégés hors lot et 181 preuves des trois lots WORLD précédents sont identiques à la capture d'application. 922 des 927 preuves SERG sont identiques ; 5 mises à jour de suivi externes sont préservées et archivées dans EXTERNAL_SERG_UPDATE.json (Ortenbourg, dont son reçu joueur propre, sans validation WORLD induite). TECH-R1/R2/R3, ECON-ALLOYS/quincaillerie et les installations concurrentes SERG sont préservés. Cinq fichiers partagés sont modifiés dans les seuls scopes annoncés ; un historique de bâtiments spécifique est nouveau. Aucun suivi SERG, fichier vanilla ou état Git n'est écrit par cette tâche.

Progression d'entrée vérifiée : 7/80 Balkans et 7/320 WORLD. Seuls T et S de P1-03 gagnent du crédit : **9/80 Balkans (11,25 %) et 9/320 WORLD (2,81 %)**. O/I/D/E/R restent partiels ; V non commencé. Aucune région close ni attestation humaine créée.

Prochaine passe : **BALKANS-05 — Albanie et Épire ottomanes**, en conservant les possessions vénitiennes restaurées. Rester dans les Balkans. Test joueur groupé uniquement à la fin du travail techniquement réalisable, puis confirmation explicite avant toute autre région.
