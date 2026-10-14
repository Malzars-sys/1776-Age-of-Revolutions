# MAP-2L — noyaux westphaliens de l'électorat de Cologne

14 octobre 2026. **Appliqué localement : 84 cellules PRU → KCL, huit nouveaux RGB.** Les 69 cellules du noyau ducal et les 15 cellules du Vest Recklinghausen rejoignent Cologne, sans créer un pays indépendant. **409/409 contrôles statiques**, test en jeu du nouveau sous-lot encore nécessaire. La validation manuelle des anciens territoires inspectés n'est pas étendue à ces corrections.

## Provinces réellement modifiées

Toutes appartiennent à `STATE_WESTPHALIA`, State_ID **61**. Les identifiants ci-dessous sont des couleurs du bitmap, pas des numéros historiques.

| RGB parent | Avant ce sous-lot | Après | Justification |
|---|---|---|---|
| `x418021` | PRU, 296 cellules | PRU 283 ; KCL 13 sur `xEDAB00` | Portion occidentale du noyau ducal tracé |
| `x4101A0` | Reste PRU, 140 cellules | PRU 84 sur `x4101A0`, `xEDAB01`, `xEDAB02` ; KCL 56 sur `xEDAB03` à `xEDAB06` | Prolongement du même noyau ; le fragment Paderborn antérieur `xEDA90B` reste intact |
| `xA08061` | PRU, 170 cellules | PRU 155 ; KCL 15 sur `xEDAB07` | Noyau occidental du Vest, au sud de la Lippe |

Le masque initial des trois parents, **606 cellules**, est conservé sans ajout ni retrait. **109 cellules recolorées** : les 84 transferts plus 25 cellules de fragments PRU séparés. Onze composantes à connexité quatre remplacent trois RGB, donc huit nouvelles identités `xEDAB00`–`xEDAB07`. Les deux fragments ducaux d'une cellule ne sont pas agrandis artificiellement.

## Fondement historique et sources réutilisées

La carte de Vaugondy/Santini datée de 1753, édition 1777, était déjà conservée dans `RHINE_CENTRAL/VAUGONDY_SANTINI_DETAIL.jpg`. Elle distingue le duché de Westphalie, les possessions de la Mark, les voisins orientaux et l'enclave du Vest. La carte de Schenk 1710/1730, déjà conservée dans `RHINE_WESTPHALIA`, sert de comparaison géographique ; le duché appartenant au cercle électoral rhénan, les plages non colorées sur la carte du cercle bas-rhénan-westphalien ne constituent pas seules une preuve de souveraineté.

Le [LWL documente le duché sous l'autorité de Cologne](https://www.lwl.org/westfaelische-geschichte/portal/Internet/finde/langDatensatz.php?urlID=125&url_tabelle=tab_websegmente), l'acquisition d'Arnsberg en 1368 et la perte de Soest et de sa Börde au profit de Clèves au XVe siècle. Le titre ducal ne justifie ni l'attribution de toute la Westphalie géographique à Cologne ni celle de Paderborn. Les changements de 1802–1816 ne sont pas anticipés en 1776.

Le [Vest Recklinghausen est une juridiction propre de l'électorat](https://www.lwl.org/westfaelische-geschichte/portal/Internet/finde/langDatensatz.php?urlID=115&url_tabelle=tab_websegmente), à l'ouest de Recklinghausen et au sud de la Lippe, avec gouverneur et États locaux. Il n'est pas traité comme une extension automatique du titre ducal, ni projeté rétrospectivement dans l'Arenberg ou la Prusse du XIXe siècle.

## Correspondance cartographique et limites

Une comparaison entre les deux cartes conserve quatre correspondances de symboles : Düsseldorf, Bonn, Arnsberg et Brilon. Le contrôle indépendant de Rüthen donne **3,85 pixels**, celui de Cologne **0,60 pixel**, après conversion dans l'échelle du jeu ; moyenne **2,22 pixels**. Ce sont des résidus **entre cartes**, pas une précision physique certifiée sur le bitmap. Le pont Schenk/jeu précédemment établi est réutilisé sans optimisation : les anciens écarts des locators de Cologne (**10,93 px**) et Bonn (**7,99 px**) demeurent explicitement signalés.

Le premier brouillon avait identifié à tort un symbole plus septentrional comme Düsseldorf. La lecture large et les grilles source ont permis de le rejeter **avant toute installation**, puis de recalculer la comparaison avec le symbole de Düsseldorf à (645,425). `DRAFT_REJECTED.json` en conserve la distinction. Le premier candidat de 39 cellules n'a jamais été installé ; seul le tracé final de 84 cellules est appliqué.

Les enveloppes mises en œuvre sont des noyaux conservateurs **à l'intérieur des juridictions dessinées**, pas la copie exhaustive de chaque frontière ou enclave. Les provinces voisines, les franges non tracées, les raccords orientaux vers les régions économiques de Hesse et les micro-juridictions restent à examiner ; leur ancien contrôleur n'est pas certifié historiquement. Aucune frontière n'est créée à partir du seul nom d'un bâtiment.

Dortmund et Essen ne sont pas attribués à Cologne : leurs locators, RGB et cellules restent inchangés. Leurs statuts de ville/abbaye impériales ne sont pas encore entièrement reconstruits. Soest/Börde ne sont pas inclus dans l'enveloppe ducale ; cela ne certifie pas toutes leurs représentations natives. Münster, Paderborn, Juliers–Berg, Lippe et Schaumburg-Lippe conservent leurs allocations antérieures.

## Conservation et dépendances

**27 631 habitants réalloués depuis la subdivision PRU existante**, sans nouvelle population : 16 661 north_german catholiques, 10 948 north_german de religion par défaut, 22 ashkenazi de religion par défaut. Répartition entière pondérée par la superficie de la subdivision source complète, effectuée une seule fois depuis la baseline immuable. Ce n'est pas un recensement historique du duché ou du Vest. Totaux culture/religion, attributs et population mondiale **835 804 980** conservés.

Les bâtiments et leurs fichiers, niveaux, méthodes de production, détenteurs économiques, unités, formations et recrutements restent inchangés. Les faibles allocations n'emportent aucun niveau entier de bâtiment. PRU garde sa subdivision ; KCL reçoit une subdivision supplémentaire dans la région économique partagée, sans modifier sa capitale, ses lois, son gouvernement, ses technologies ou ses droits électoraux.

Aucun déplacement ni changement de RGB de locator. Les identifiants State_ID et les ressources sont inchangés. La liste `prime_land` s'étend aux enfants de `x418021` et `xA08061` : **sa surface physique est exactement la même**, pas un nouveau bonus de terres.

Le registre impérial actif passe de **427 à 435 RGB** ; l'empreinte de jure demeure **62 580 cellules**. Registre, textes dépendants de restitution/territoires et cartes principale/journal sont régénérés. Les élections, relations et règles de centralisation ne sont pas refondus.

Les vingt nouveaux RGB et les 1 081 cellules restaurées de la première passe Rhin–Westphalie restent intacts. Seul le reste PRU alors non résolu de `x4101A0` est recoupé, par migration explicite ; son enfant Paderborn n'est pas touché. Les quatre RGB et les 76 cellules du sous-lot Minden sont conservés. Belgique, Franconie, Mayence, Milan, Piémont et autres lots sont vérifiés cumulativement. Erfurt–Eichsfeld et la Souabe ne sont pas modifiés.

## Fichiers et contrôles

`PLAN.json`, `IMPERIAL_FILES.json` et `TERRITORIAL_CHANGES.csv` détaillent les changements. Principaux fichiers : bitmap, terrains, régions européennes, historiques states/pops, registre de jure ; sept textes impériaux compilés et textures de carte. Outils : `tools/map2l_duchy_westphalia.py`, `tools/validate_map2l_duchy_westphalia.py`, chaîne explicite dans `tools/map2l_registry.py` et adaptation des contrôles cumulés de Westphalie/Minden aux seules migrations ultérieures exactes.

**409/409 contrôles du sous-lot**, **10/10 tests unitaires des migrations**, **3/3 tests du reçu manuel**, **16/16 contrôles de carte hors moteur**, y compris le helper HLSL dans son harnais, pas le shader complet dans Victoria 3. Les contrôles cumulés restent distincts des tests manuels ; la différence Git des anciennes baselines correspond au commit personnel autorisé `f34a6b8` et demeure visible dans les résultats bruts.

Anomalies héritées conservées : **44 références RGB doublement attribuées, 12 erreurs de référence**. Aucune régression supplémentaire observée. L'avertissement de fin de ligne Git est conservé ; seuls les espaces finaux nouvellement insérés dans ce sous-lot sont retirés. Les deux lignes de formatage préexistantes de Minden ne sont pas nettoyées globalement.

À vérifier en jeu : possessions KCL dans `STATE_WESTPHALIA`, lisibilité des petits fragments, absence d'emprise sur Dortmund/Essen/Paderborn, population partagée, continuité des recrutements et bâtiments PRU, restitution impériale et cartes du journal/principale. Les nouvelles frontières ne bénéficient pas encore de `PASS_RUNTIME_USER_VALIDATED`.

## Suite du Rhin–Westphalie

Le secteur n'est pas achevé : raccords restants du duché/Vest, Osnabrück, Niederstift Münster, Bentheim, Steinfurt/Rietberg/Corvey, branches de Nassau, limites de Clèves/Mark/Gueldre, Ravensberg et villes impériales restent ouverts. Le problème d'Erfurt ne les bloque pas ; la Souabe demeure exclue à la demande du joueur.

Aucun commit, merge, push, changement de branche ou mutation de l'index. Le checkpoint publié précédemment est antérieur à ce sous-lot ; aucune nouvelle sauvegarde distante n'est fabriquée sans autorisation.

ColGrep : **zéro appel**, chemins, outils et cartes connus ; deux recherches exactes `rg`, lectures ciblées et vérifications institutionnelles locales au secteur. Aucun rebuild d'index, aucune mesure fiable de tokens ou d'économie exacte de quota revendiquée.
