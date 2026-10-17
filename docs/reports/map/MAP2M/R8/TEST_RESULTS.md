# Exécutions techniques R8

Les commandes ci-dessous ont été effectivement exécutées depuis la racine du dépôt avec le Python embarqué et `PYTHONDONTWRITEBYTECODE=1`. Aucun test ne lance le jeu et aucun ancien générateur de rapports n'est exécuté.

| Commande Python | Résultat |
| --- | --- |
| `tools/map2m_r8.py prepare` | PASS : 41 cellules PRU terrestres, connexes à SWE, à l'ouest de l'aide de dessin ; Wolgast exclue ; population calculée 4 820 |
| `tools/map2m_r8.py install` | Bitmap candidat installé après vérification du texte démographique relu et appliqué |
| `tools/map2m_r8.py thorn` | Audit 153 cellules ; un locator ; zéro transfert |
| `tools/map2m_r8.py validate` | 60/60 PASS, détails dans VALIDATION.json |
| `-m unittest discover -s tools -p test_map2m_r8.py -v` | 8/8 PASS ; 2,510 s pour cette exécution |
| `-m unittest discover -s tools -p test_map2l_registry.py -v` | 18/18 PASS ; 0,081 s pour cette exécution |

Les tests R8 comprennent deux contrôles négatifs : une modification extérieure aux 41 pixels est rejetée ; l'ajout d'un seul habitant à un fragment démographique est détecté par la comparaison des profils. Ils contrôlent aussi l'absence de transfert de Thorn, de claim moteur et de retouche des preuves R1–R7/Git.

Les anciens tests dépendant d'un bitmap R2/R3 strictement figé ne sont pas présentés comme exécutés et réussis contre R8. Leurs instantanés restent immuables. Le rejeu de leurs cellules acceptées et leurs invariants encore applicables est intégré à la validation différentielle R8. Cela évite aussi que leurs générateurs écrasent les anciens résultats.

État moteur : **PENDING_USER_NEW_GAME_AND_ONE_MONTH**, pas PASS_RUNTIME_USER_VALIDATED.
