# B06 — Contrôles exécutés

| Exécution | Résultat et portée |
| --- | --- |
| `python tools/validate_starting_technology_1776.py --tag TUR --output .../TECH_BEFORE.json` | Sortie 1 : FAIL_STATIC, trois constats hérités |
| `python tools/world1776_balkans06.py --apply` | Cinq ajouts propres ; refuse une seconde application ; aucun fichier partagé écrit |
| Même audit vers TECH_AFTER.json | Sortie 1 : trois constats identiques ; nouveaux forts et PM compatibles |
| `python tools/world1776_balkans06.py --validate` | **55/55**, sortie 0 ; conservation et références du lot |

Le contrôle lit les données effectives mod/vanilla, les recettes communes, les historiques et les deux captures. Il ne lance aucun moteur et ne certifie ni le budget ni les frontières historiques. Les anciens tests B01–B05 ne sont pas réécrits pour faire disparaître les changements extérieurs. Le reçu B04 de 00_states.txt est daté avant HBC-06 ; la région grecque et la carte courantes sont conservées, pas restaurées depuis B04.
