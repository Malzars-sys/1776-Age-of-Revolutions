# Anciennes attentes R9 — exécutions comparées

La suite `test_map2m_r9` décrit une photographie du 15 octobre, pas un contrat interdisant toute correction future. Elle a été exécutée en lecture **avant et après cette mission**, sans réécrire ses tests, baselines, rapports ou résultats historiques.

| Assertion ancienne | Avant cette passe | Après | Interprétation et contrôle actuel |
| --- | --- | --- | --- |
| Raster mondial égal au seul delta de deux cellules R9 | Échec | Échec | Déjà dépassée par les livraisons ultérieures. Les 285 changements actuels sont comparés exactement à la capture courante ; tout pixel hors des quatre parents reste identique. |
| Tous les fichiers de repères identiques à la capture R9 | Échec | Échec | Déjà différent avant cette mission. La passe actuelle permet seulement la position de farm158/Toruń ; tous les autres octets de ce fichier et tous les autres fichiers sont contrôlés depuis la capture courante. |
| Thorn inchangée, parent de 153 cellules | Réussite | Échec | Nouvelle différence intentionnelle : 149 cellules PRU et quatre cellules PLC, référence et position du repère cohérentes. L'ancienne assertion est incompatible avec la correction demandée ; le nouveau delta ne prétend pas certifier toute la campagne de Thorn. |

Les **cinq autres tests R9 réussissent** avant et après. Bilan brut : **8 tests, 2 échecs avant / 3 après, zéro erreur**. Les anciennes propositions urbaines restent marquées non appliquées dans leurs CSV ; le nouveau noyau a son manifeste propre.

Les traces intégrales sont `LEGACY_BEFORE_RAW.txt` et `LEGACY_AFTER_RAW.txt`, les résultats structurés `LEGACY_BEFORE.json` et `LEGACY_AFTER.json`. Les résultats historiques MAP2M restent inchangés, y compris leurs limites et reçus. Aucun ancien total de tests n'est présenté comme une exécution sur la présente livraison.

Les contrôles différentiels actuels, les tests de migration du registre, les garde-fous R2 réutilisables et le validateur canonique sont consignés séparément. Ils ne démontrent pas un chargement moteur, un rendu correct ou une réception humaine. Le test joueur reste requis.
