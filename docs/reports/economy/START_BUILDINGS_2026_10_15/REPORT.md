# Ajustements économiques de départ — 15 octobre 2026

**PASS_STATIC_ENGINE_PENDING.** Modifications pour une nouvelle partie de 1776 ; aucun test moteur ou solde budgétaire réel certifié. Aucun changement territorial, de population ou de technologie.

## Bâtiments ajoutés

| État et propriétaire | Bâtiment | Avant | Ajout | Après |
|---|---|---:|---:|---:|
| Rhône / FRA | Armement | 4 | 3 | 7 |
| Österreich / AUS | Armement | 2 | 3 | 5 |
| Anhalt / PRU uniquement | Mine de sel | 0 | 2 | 2 |
| Jiangxi / CHI | Armement | 0 | 2 | 2 |

Le duché d'Anhalt (`ANH`) n'est pas modifié. Le gisement régional de sel est déjà défini à 20 unités découvertes ; aucune ressource ni province n'est créée. Les six niveaux d'armement au Brandebourg restent intacts.

| Ensemble de la Chine directement administrée / CHI | Avant | Ajout | Après |
|---|---:|---:|---:|
| Plantations de soie | 18 | 30 | 48 |
| Rizières | 4 | 10 | 14 |
| Élevages | 4 | 20 | 24 |
| Verreries | 0 | 10 | 10 |

Répartition des ajouts :

- Soie : Suzhou 10, Jiangsu 8, Nankin 6, Hubei oriental 3, Guangdong 3.
- Riz : Jiangsu 3, Hunan 3, Jiangxi 2, Hubei oriental 2.
- Élevages : Zhili 6, Shandong 5, Henan 4, Sichuan 3, Shanxi 2.
- Verreries : Jiangxi 4, Nankin 3, Suzhou 3. Les dix niveaux ont **`pm_ceramics` activé**, produisant de la porcelaine ; aucune céramique désactivée ni méthode avancée non recherchée n'est forcée.

Au total : **80 niveaux nouveaux** dans cette première étape. Les données préexistantes sont conservées par un fichier d'ajouts distinct. L'armement nouveau est détenu par le pays, les ajouts agricoles par des domaines locaux et les nouvelles verreries/mines par des quartiers d'affaires locaux, suivant les conventions d'historique du mod.

## Capacité des États chinois

Les ressources agricoles sont autorisées dans les États choisis et leur utilisation écrite reste inférieure aux terres arables. Prévision nominale après tous les ajouts, à partir des bâtiments et méthodes effectifs : marge d'infrastructure **+8 au Jiangxi, +89,5 à Nankin, +54,5 à Suzhou**. Les autres États chinois choisis gardent aussi une marge positive.

Ce calcul ne simule ni les embauches, ni les prix, ni les pénuries d'intrants, ni les bâtiments implicites créés par le moteur. Il ne certifie donc pas l'accès effectif au marché ou la rentabilité. Le Rhône arrive à **0 de marge nominale** après son ajout d'armement : point à inspecter en jeu. Aucune route, population, technologie ou capacité de gisement supplémentaire n'est ajoutée pour masquer cette limite.

Une anomalie de départ reste signalée : la Chine possède déjà un niveau d'armement dans ses historiques, mais `regulated_small_arms` n'apparaît pas parmi ses recherches explicitement accordées. Les deux niveaux de Jiangxi sont créés selon ce précédent d'historique ; **aucune technologie gratuite n'est accordée** et le droit d'agrandir ces usines reste à vérifier en jeu. Ce n'est pas présenté comme un déblocage technologique validé. Les méthodes explicitement choisies sont, elles, compatibles et débloquées ; les PM de collecte de données non recherchés sont remplacés par leur option désactivée avant application.

## Ajouts ultérieurs : Grande-Bretagne, Irlande et salines

Voir [le rapport détaillé du recalcul](BRITISH_ROADS_AND_SALT/REPORT.md).

- Réseaux régionaux métropole + Irlande : **229 → 87 niveaux**. Grande-Bretagne seule : **208 → 79** ; Irlande : **21 → 8**. Colonies et possessions extérieures exclues.
- Routes à péage partout dans ce périmètre. **Canaux industriels conservés et comptés dans le Lancashire, les Midlands et le Yorkshire seulement**, conformément à la dernière instruction du joueur. Aucun canal ajouté dans les autres États.
- Irlande : **15 niveaux d'administration supplémentaires**, soit **+150 de bureaucratie nominale** à plein recrutement face au déficit observé de 128 ; marge théorique +22 hors autres changements. Les besoins d'infrastructure des nouveaux bureaux sont inclus dans le dimensionnement routier.
- Salines : `default_building_salt_pan`, production **10 → 20**. Les mines de sel à pioches produisaient déjà 20 et restent inchangées. Cette modification du PM des salines s'applique mondialement.

La capacité administrative est corrigée, pas une valeur instantanée garantie au premier jour : les bureaux doivent recruter. Le réseau routier a également été dimensionné à plein effectif, pas à partir de sa production sous-recrutée au lancement.

## Fichiers fonctionnels concernés par l'ensemble de la passe

- `common/history/buildings/99_1776_player_industry_agriculture_addon.txt` : les 80 niveaux demandés initialement.
- `common/history/buildings/00_west_europe.txt` et `98_build_start_1776_world_redistribution.txt` : seulement les niveaux/PM des réseaux métropolitains et irlandais autorisés ; les autres déclarations, détenteurs et PM ne sont pas réécrits.
- `common/history/buildings/99_1776_irish_bureaucracy_addon.txt` : les nouveaux bureaux irlandais.
- `common/production_methods/10_tech6a1b_salt_producers.txt` : une seule valeur, sortie de sel du PM des salines.

Outils : `tools/start_buildings_2026_10_15.py`, `tools/british_infrastructure_2026_10_15.py`, `tools/test_start_economy_2026_10_15.py`. Les instantanés ne sont pas réécrits ; la révision d'une proposition non encore appliquée est enregistrée séparément dans `REVIEWED_PLAN.json`.

## Vérifications

Première étape : **203/203 contrôles statiques réussis** avant les demandes britanniques et irlandaises supplémentaires. La validation de continuation actuelle est **131/131**, dans `BRITISH_ROADS_AND_SALT/VALIDATION.json` ; elle contrôle aussi les 21 totaux de la première étape, l'empreinte de son fichier d'ajouts et ses prévisions chinoises inchangées. Les deux comptes ne sont pas additionnés comme s'ils étaient des tests indépendants.

Tests d'outils exécutés : **8/8** pour les nouvelles allocations/formules, **31/31** pour les outils MAP-2L, **8/8** pour l'interface des centres de commerce, soit **47/47**. Pas de test moteur automatisé.

Populations, cultures, religions, pays, gouvernements, provinces, registre impérial et unités conservés. Population mondiale : **835 804 980**. Les 341 cellules suédoises validées, les six niveaux d'armes prussiens et le correctif GUI précédent sont préservés. Les **44 doublons RGB et 12 références invalides hérités** restent isolés des changements nouveaux. Aucun commit, merge, reset, push ou changement d'index Git.

Le contrôle de la première étape reste son attestation historique : son exigence de préserver intégralement tous les anciens fichiers est volontairement dépassée par la demande ultérieure sur les routes et les salines. Utiliser le validateur de continuation pour contrôler l'état final, sans effacer ces anciennes références.

## À contrôler dans une nouvelle partie

Vérifier les totaux des bâtiments ci-dessus, le PM porcelaine dans les trois États chinois, le Rhône et ses infrastructures, puis les réseaux des treize États britanniques/irlandais. Vérifier les canaux dans les trois seuls États prévus, l'absence de déficit d'infrastructure une fois recruté, le recrutement des nouveaux bureaux, la bureaucratie et le budget irlandais après stabilisation. Contrôler les dépenses britanniques une fois les réseaux remplis ; aucun solde monétaire n'est prédit comme exact.

Pièces : `BUILDING_CHANGES.csv`, `INFRASTRUCTURE_BEFORE.json`, `INFRASTRUCTURE_AFTER.json`, et les CSV/JSON de continuation. Un appel ColGrep-Agent a échoué en 0,80 s avec « Path does not exist / accès refusé » ; les recherches ciblées et les vérifications locales ont pris le relais. Aucune exécution du modèle 2B ni économie de quota n'est certifiée à partir de cet échec ; aucun réglage d'intégration modifié.
