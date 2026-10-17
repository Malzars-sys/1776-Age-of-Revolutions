# MAP-2N — Wismar, Poel et Amt Neukloster, 1er janvier 1776

Date : 2026-10-15. Statique : **MAP2N_READY_FOR_RUNTIME_VALIDATION**. Retour manuel : **PASS_RUNTIME_USER_VALIDATED**.

Les trois secteurs sont intégrés localement. Le joueur confirme maintenant que MAP2N passe en jeu. Attestation : RUNTIME_USER_VALIDATION_2026_10_15.json. Ce retour manuel n'est pas un test moteur automatisé ni une certification historique de chaque frontière. La durée et les points individuellement inspectés ne sont pas précisés ; aucun nouveau passage d'un mois n'est déduit de cette seule confirmation.

## Périmètre et décisions

R8/R9 ont été acceptés manuellement par le joueur, passage du mois sans crash : attestation additive ../MAP2M/R8_R9_USER_RUNTIME_VALIDATION_2026_10_15.json. Ce retour n'est ni un test moteur automatisé ni une certification historique générale.

Poel a été reconstruite sur demande expresse du joueur, puis regroupée techniquement dans STATE_POMERANIA. Wismar et Neukloster restent dans STATE_MECKLENBURG, identifiant numérique 75. La souveraineté suédoise n'entraîne pas l'adhésion de toute la Suède au bloc impérial.

## Territoires effectivement intégrés

| Secteur | Avant | Après |
|---|---|---|
| Wismar et dépendances principales | 4 cellules MEC, xE080A0 et xD8F441 | SWE, STATE_MECKLENBURG, xEDB102 (1 cellule) et xEDB103 (3) |
| Dépendance orientale de Benz | 1 cellule MEC, xD8F441 | SWE, STATE_MECKLENBURG, xEDB104 |
| Amt Neukloster | 8 cellules MEC, xD8F441 | SWE, STATE_MECKLENBURG, xEDB105 |
| Partie suédoise de Poel | Pas de province insulaire distincte | SWE, STATE_POMERANIA, xEDB100, 3 cellules |
| Dépendances lübeckoises de Poel | Pas de représentation distincte | LUB, STATE_POMERANIA, xEDB101, 1 cellule sud-ouest |
| Détroit de Poel | Côte native partiellement continue | Quatre cellules de terre devenues mer ; île distincte |

Cumul : **21 pixels du bitmap modifiés**, dont 13 transferts continentaux MEC → SWE et 8 modifications de Poel/littoral. **Six nouveaux RGB**. Aucun RGB antérieur supprimé. Les deux cellules marines de la nouvelle île sont compensées physiquement par le détroit, pas par une création de population.

xD8F441 reste à MEC avec 138 cellules (156 avant MAP2N, 150 après Poel seule). xE080A0 reste à MEC avec 517 cellules, contre 518 avant. Rostock, Schwerin, les autres territoires MEC/MST et les autres pays ne changent pas de propriétaire.

La liste complète cellule par cellule figure dans TERRITORIAL_CHANGES.csv. Les trois images sectorielles et MAP2N_BEFORE_AFTER.png montrent le même comparatif cumulatif véridique : référence R9 acceptée contre résultat final MAP2N.

## Justifications historiques et cartographiques

Les sources conservées établissent les titres suédois de Wismar, Poel et Neukloster en 1648, le retour de Wismar en 1720 et le règlement postérieur de 1803. La pièce parlementaire suédoise reproduisant la convention de Malmö a maintenant été consultée, au lieu d'être seulement citée comme notice. Voir HISTORICAL_EVIDENCE.md.

La carte comparative conservée est utilisée pour les dépendances de Wismar et l'Amt Neukloster, et non pour transformer la seule position d'une ville en souveraineté sur une province entière. L'aperçu régional de 1720 corrobore l'organisation générale. Le contour de Neukloster est représenté sur huit cellules et plusieurs rangées, pas sur sa seule agglomération.

Le calage de la carte source réutilise le gazetteer GeoNames déjà conservé : trois symboles de localité bien répartis (Neubukow, Warin, Dorf Mecklenburg) servent au placement ; Neukloster, Zurow, Lübow et Hornstorf sont réservés à la vérification. Sur ces quatre contrôles, l'écart moyen de correspondance de la carte source vaut **0,107 pixel natif**, maximum **0,150**.

**Ces chiffres contrôlent l'alignement de la carte source, pas l'exactitude géographique indépendante du bitmap du jeu.** La projection R5 est conservée sans nouvelle optimisation ; aucun centre de ville n'est présenté comme certifié.

La sélection continentale mesure la couverture source sur 225 échantillons par cellule, seuil de majorité de 50 %. Seules les cellules terrestres déjà attribuées à MEC sont retenues. Les RGB sont séparés par parent et composante connexe : pas de province déconnectée, pas de corridor ajouté entre Wismar, Benz et Neukloster.

## Approximations explicites

- Littoral et frontières généralisés à l'échelle du jeu, pas restitution cadastrale de 1776.
- Poel : quatre cellules ; sa dépendance lübeckoise est abstraite par une seule cellule, sans prétendre reproduire quatre petits contours.
- Détroit de Poel élargi à une cellule pour éviter les ponts latéraux ou diagonaux.
- La liaison étroite vers Benz et les petits contours de Martensdorf ne sont pas artificiellement agrandis ; certaines franges de Wismar et de l'Amt restent généralisées dans le voisinage.
- Deux cellules de mer touchées par la projection de la carte de Wismar ne sont pas remblayées : le décalage de projection ne suffit pas à justifier une reconstruction supplémentaire du littoral continental.
- La carte comparative s'appuie sur une source de 1800 et une hydrographie moderne ; elle est croisée avec les titres historiques et la carte de synthèse de 1720. Le scan primaire de 1800 n'a pas été accessible et n'est pas présenté comme directement vérifié.

Ces limites sont conservées dans UNRESOLVED.csv ; elles ne sont pas masquées par le statut de disponibilité du correctif.

## Relief de Poel

Les deux overrides heightmap.png et packed_heightmap.png sont conservés exactement depuis le sous-correctif Poel : 64 échantillons source et 32 compressés changés dans deux tuiles locales, aucun ailleurs. Leur orientation effective et leurs bords communs ont été vérifiés. L'indirection et la description de topologie restent héritées, sans modification.

Hauteurs 16 bits : terre 5 400, eau 4 200 ; seuil effectif 4 751,2875. La couronne d'eau est sous le seuil. rivers.png conserve sa palette native, avec cinq corrections de fond terre/mer et aucun cours d'eau effacé. Aucun locator, matériau global, spline ou nodes.dat n'est déplacé/modifié.

Le joueur a accepté le lot en jeu. Son retour ne détaille pas individuellement toutes les connexions et le relief : la liste de contrôle reste disponible pour une investigation ciblée si une anomalie apparaît.

## Populations, bâtiments et unités

Population mondiale : **835 804 980, inchangée**. Profils culturels et religieux bruts/résolus conservés exactement.

- Sous-correctif Poel : 1 192 habitants existants réalloués depuis MEC, dont 894 à SWE et 298 à LUB en Poméranie.
- Wismar–Benz–Neukloster : 3 874 habitants existants passent de MEC à SWE dans le même STATE_MECKLENBURG, dont 3 843 nord-germaniques et 31 ashkénazes.
- Solde cumulé MEC en Mecklembourg : −5 066 ; nouveaux totaux SWE en Mecklembourg +3 874, SWE en Poméranie +894 et LUB en Poméranie +298.
- MST inchangé. Somme Mecklembourg + Poméranie conservée ; le transfert régional entre ces deux grands États correspond seulement au regroupement demandé pour Poel.

Les allocations sont entières et déterministes par profil, à plus forts restes. Les poids de la continuation sont MEC 1 276 / SWE 13, appliqués à la population MEC réellement restante après Poel. Ce n'est pas un recensement historique de Wismar.

Tous les bâtiments, niveaux, PM, propriétaires économiques, infrastructures, formations, recrutements, capitales et définitions de pays sont conservés. Aucun bâtiment artificiel n'est ajouté. Les accès maritimes et au marché des nouvelles parts régionales sont des points de contrôle moteur explicites, pas des résultats statiques prétendument acquis.

## Mécanismes impériaux

Registre actif : **504 RGB**, les 498 entrées de départ intactes. Les migrations sont additives et rejouables : Poel puis COMPLETION. Les baselines antérieures et les preuves R8/R9 ne sont pas réécrites.

Une exception territoriale explicitement contrôlée ajoute les quatre nouvelles provinces suédoises de STATE_MECKLENBURG à celle déjà approuvée de STATE_POMERANIA. Aucun membre supplémentaire ni aucune autre région de la Suède n'est ajouté. Les droits de restitution, les compteurs, les localisations et les textures impériales sont actualisés.

La carte principale correspond exactement aux 504 droits du registre ; la carte du journal est régénérée. Les transferts continentaux ne changent pas l'emprise de jure déjà impériale : seuls leur propriétaire légitime et leurs subdivisions changent.

## Vérifications finales

- **151/151 contrôles cumulatifs**, couvrant les 21 pixels, les six RGB, les propriétaires/State_ID, l'absence de corridor artificiel, les données démographiques/économiques/militaires, les ressources/hubs, les dépendances impériales et les fichiers hors périmètre.
- **44/44 tests de non-régression**, incluant les deux étapes MAP2N, les mutations négatives et le registre territorial cumulatif.
- **16/16 contrôles du filtre de carte**, dont compilation du helper HLSL avec D3DCompile et aller-retour DDS exact. Ce n'est pas une compilation du jeu entier.
- Le contrôle physique détaillé de Poel (244/244 au sous-correctif précédent) est conservé dans COMPLETION/POEL_STAGE_VALIDATION.json ; ses couches physiques sont maintenant comparées byte pour byte à cette étape.
- Poméranie R9 et pixels à l'est de X=4380 identiques ; secteurs prussiens et anomalies hors périmètre inchangés.
- 44 doublons RGB et 12 références invalides préexistants identiques, aucune nouvelle occurrence.
- HEAD et index Git inchangés. Aucun fichier du dossier d'installation du jeu modifié.

VALIDATION.json et COMPLETION/UNIT_TESTS.json contiennent les résultats statiques. Le retour manuel de MAP2N est maintenant enregistré séparément, comme celui de R8/R9. Aucun test moteur automatisé n'est revendiqué.

## Fichiers et livrables

Les dix livrables du prompt sont présents dans ce dossier, plus MAP2N_BEFORE_AFTER.png. Liste exacte des fichiers fonctionnels et empreintes : COMPLETION/INSTALLED_MANIFEST.json.

Modifications principales : bitmap des provinces ; relief et rivières de Poel ; terrains et définitions des deux grands États ; historiques des États et populations ; registre impérial actif ; lecteur des migrations ; scripts impériaux de triggers/effets/identité ; quatre localisations dérivées ; cartes principale/journal et leur aperçu source.

Outils reproductibles : tools/map2n_work.py (audit initial), map2n_island.py (étape Poel), map2n_completion.py (continuation et validation finale), test_map2n_island.py et test_map2n_completion.py. Ne pas relancer les préparations additives ni remplacer une baseline. La validation finale s'exécute avec map2n_completion.py validate ; tests avec map2n_completion.py tests.

## Suite

Le lot bénéficie du retour manuel PASS_RUNTIME_USER_VALIDATED. RUNTIME_TEST_PLAN.md conserve le protocole proposé (nouvelle partie, trois secteurs, relief/accès maritimes, marché et mécanismes impériaux, puis passage d'un mois), sans affirmer que chaque étape a été explicitement confirmée par ce dernier message.

Thorn, Netze, Inowrocław, Bromberg, Emden/Frise orientale et Erfurt–Eichsfeld restent ouverts et inchangés. La validation n'en fait pas des problèmes résolus. Le prototype graphique demandé est distinct de MAP2N et n'est pas couvert par ce retour.

## Recherche locale et Git

Les résultats ColGrep vérifiés lors de l'étape précédente ont été réutilisés. Aucun nouvel appel redondant à l'agent local, aucun changement de modèle/configuration ou reconstruction générale d'index pendant cette continuation : les chemins et sources utiles étaient déjà connus.

Pas de mesure exacte d'économie de quota : compteurs de tokens et comparaison contrôlée indisponibles. Les documents, cartes et données géographiques existants ont été réutilisés ; seules des vérifications documentaires ciblées ont complété les références conservées.

Aucun commit, merge, reset, changement de branche, modification de l'index ou push.
