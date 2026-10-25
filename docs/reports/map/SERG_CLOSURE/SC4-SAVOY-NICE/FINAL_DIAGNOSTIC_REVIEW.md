# Classement du dernier contrôle de diff

Le premier contrôle final de conservation donnait 14/15 : toutes les données et preuves étaient conservées, mais le classeur attendait un code de sortie Git 1 pour les blancs hérités. Le Git local renvoie **2** pour les quatre occurrences relevées. Le constat brut et ce premier classement sont conservés dans `DIFF_CHECK_ATTEMPT_1.json` et `FINAL_CHECKS_ATTEMPT_1.json`.

Le classeur a été corrigé pour reconnaître seulement ces quatre lignes (2983, 2999, 3015, 3031) de `common/history/pops/00_west_europe.txt`, avec la même erreur et une empreinte strictement identique à l'instantané d'entrée. Une autre occurrence ou un changement d'empreinte échouerait. Aucun fichier fonctionnel n'est corrigé ni restauré pour faire passer le contrôle. Le résultat du diff demeure non nul et est classé **INHERITED_WHITESPACE_ONLY**, sans être présenté comme un diff vierge.

La suite cumulative et les tests finaux n'ont pas été relancés pour ce seul classement documentaire; aucune donnée de jeu n'a changé depuis leurs réussites. Les contrôles de conservation et le validateur canonique sont réexécutés après ce correctif du classeur.
