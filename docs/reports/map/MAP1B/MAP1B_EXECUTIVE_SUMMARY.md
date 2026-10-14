# MAP-1B — Première validation : résultat pour examen

**10 octobre 2026 — cible historique : 1er janvier 1776.** Aucun changement de frontière ou d'historique; aucun commit, merge ou push.

La mission apporte de nouvelles preuves consultées et une méthode reproductible, mais **ne valide pas encore les trois frontières entières**. Quatre cartes d'époque ont été ouvertes et comparées aux pixels exacts du jeu, deux documents institutionnels lombards consultés, deux études PDF examinées. Trois superpositions nouvelles séparent les villes d'ajustement des contrôles indépendants. Les inventaires MAP1 n'ont pas été refaits.

## Bilan de qualification

| Niveau | RGB | Conséquence |
|---|---:|---|
| Correspondance vérifiée | **0** | Registre VERIFIED vide; aucune intégration admissible |
| Correspondance proposée | **3** | Maintiens à vérifier : Milan/Pavie AUS `xD04060`; Breslau PRU `x6E617F`; Liegnitz PRU `xC108EA` |
| Correspondance encore requise | **31** | Suspendre l'arbitrage des limites; documents nécessaires indiqués individuellement |

Les 34 provinces non définitivement validées sont dans [MAP1B_UNRESOLVED.csv](MAP1B_UNRESOLVED.csv), y compris les trois propositions. MAP1 n'est pas réécrit : les changements de qualification sont livrés ici pour validation, pas injectés dans sa file mondiale.

## Ce que montre chaque dossier

- **[Luxembourg/Wallonie](MAP1B_GEOGRAPHIC_EVIDENCE/LUX_READING.md)** : la carte Janvier 1771 montre que le duché dépasse largement le petit RGB LUX. Sa boîte de 9 × 8 pixels est plus petite que l'écart maximal observé de 10,122 pixels : impossible de certifier ses contours. La souveraineté habsbourgeoise et une identité institutionnelle luxembourgeoise ne rendent pas LUX historiquement indépendant, mais n'imposent pas non plus son absorption dans BEO. Les **137 881 habitants**, bâtiments et autres dépendances restent préservés. Chiny/Bouillon/Liège et les litiges avec Trèves demandent les feuilles locales et actes datés.
- **[Lombardie austro-vénitienne](MAP1B_GEOGRAPHIC_EVIDENCE/LOMBARDY_READING.md)** : les deux scans de 1750 et les fiches administratives distinguent les domaines autrichiens et vénitiens. Les locators étiquetés Bergame/Brescia semblent inversés géographiquement : exclus de l'ajustement. Le secteur milanais reçoit une proposition de maintien, pas une validation. Crema et les marges alpines restent ouvertes; `x9AC196` ne doit pas être assimilé à Mantoue. La double propriété AUS/VEN du candidat est rejetée techniquement.
- **[Haute et Basse Silésie](MAP1B_GEOGRAPHIC_EVIDENCE/SILESIA_READING.md)** : Lotter 1758 apporte les repères, l'article intégral confirme le cadre de partition antérieur à 1776. Deux noyaux de Basse-Silésie sont proposés au maintien PRU. Le contrôle d'Olomouc échoue à **27,864 pixels** : les polygones méridionaux ne sont pas départagés. Trois erreurs de scope sont distinguées des souverainetés; seules deux comportent AUS|PRU, pas `x9061E0`.

## Décision proposée et suite

Accepter ces livrables comme **diagnostic MAP-1B**, non comme autorisation de transfert. Examiner les trois maintiens proposés; demander les documents précis recensés dans [les sources](MAP1B_HISTORICAL_SOURCES.md) et dans chaque ligne du registre. Priorité : Ferraris et accords 1769 pour Luxembourg/Chiny; limites administratives Adda/Crema et Alpes pour Lombardie; annexes de démarcation 1743/1763 et contrôle méridional amélioré pour Silésie.

La méthode A suffit provisoirement aux maintiens; aucune scission C n'est démontrée nécessaire. Le regroupement B et les corrections de scopes doivent être examinés sans arbitrage de propriétaire automatique. Les commandes Git parasites de Bessarabie restent une anomalie syntaxique séparée.

[Méthode et marges d'erreur](MAP1B_TECHNICAL_METHOD.md) · [registre VERIFIED](MAP1B_VERIFIED_PROVINCES.csv) · [validation technique](MAP1B_VALIDATION.json).

Les contrôles vérifient l'absence de modifications des 1900 fichiers runtime, du bitmap et des livrables MAP1, ainsi que la couverture des 34 RGB et des images. Pas de test en jeu ni de résultat moteur prétendu : **aucune intégration n'a eu lieu**.
