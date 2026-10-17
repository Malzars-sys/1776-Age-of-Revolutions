# MAP-2Q-R2 — Limites et contrôle en jeu

La correction démographique acceptée de **7 600 habitants** est installée. Elle ne clôt pas tous les travaux territoriaux MAP-2Q.

## Incertitudes historiques conservées

- Pas de recensement original de 1776 identifié et lu. La ville est interpolée à partir de deux valeurs rapportées ; l'Amt combine une estimation vers 1769 et une agrégation de 1819.
- La correspondance village par village entre la ville/Amt et les 31 cellules reste non certifiée. Les frontières ne sont pas modifiées pour faire coïncider artificiellement les sources.
- Écart AGGSH/Kohli non résolu : +34 urbains, +246 ruraux dans l'AGGSH. Il faudrait comparer les transcriptions aux registres LAS Abt. 260 nos 10212–10216 et vérifier les maisons sous juridiction spéciale. Les causes ne sont pas inventées.
- Mentions différentes de 1735 et 1755 dans les sources urbaines : ne pas les fusionner. L'original de 1755 et les règles de comptage permettraient d'améliorer l'interpolation.
- Les quatre sous-estimations rurales supposent des poids de 1819 stables ; aucune série de croissance propre à chaque district n'a été lue.
- Schwartau/Kaltenhof, Großvogtei, Collegiatstift et certains domaines allodiaux restent hors reconstruction complète. Le total de 18 721 de 1819, celui de 22 000 des synthèses de 1803 et la population des acquisitions de 1842/1867 ne sont pas installés.
- Lien PDF du Reporter de 2024 : téléchargement indisponible pendant cette passe. Chiffre 1791 vérifié dans son texte indexé et recoupé, mais pas d'inspection visuelle de la page complète.

## Technique et validation manuelle

Les **44 doublons RGB et 12 références invalides préexistants** restent ouverts, sans nouvelles occurrences dans R2. Les six anciens échecs de snapshots mondiaux restent consignés dans le rapport Q initial ; ils ne sont pas déclarés corrigés par une modification de population.

**Aucun test moteur automatisé ou test manuel utilisateur de R2 n'est attesté.** Dans une nouvelle partie, vérifier HLB autour de 7,6 milliers d'habitants au départ, ses cultures/religions, sa viabilité économique, l'absence de changement chez les voisins et la survie de l'union OLD–HLB après un mois. Les économies n'ont pas été rééquilibrées : moins d'habitants peut modifier recrutement, emploi et recettes sans que les bâtiments aient été supprimés.

Les limites historiques ne sont pas masquées par le statut des contrôles statiques. Aucun autre lot, commit, push, merge ou changement d'index n'est effectué.
