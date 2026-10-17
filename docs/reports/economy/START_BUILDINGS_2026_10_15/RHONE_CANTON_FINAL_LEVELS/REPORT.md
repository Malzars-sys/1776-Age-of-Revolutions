# Niveaux finaux demandés : Rhône et Canton

**PASS_STATIC_PENDING_RUNTIME** — 15 octobre 2026. Données de nouvelle partie ; pas de test moteur effectué.

- Rhône français : **5 niveaux de manufactures d'armes au total**, dans une seule déclaration. Les trois anciennes déclarations de 2, 2 et 3 niveaux sont consolidées : suppression des deux entrées répétées et définition unique à cinq, propriété publique française, réserves et méthodes de l'entrée récente conservées. Aucun simple ajout de cinq niveaux.
- Guangdong occidental chinois : **10 niveaux de centre de commerce**, au lieu de cinq, dans l'unique déclaration existante. Son port reste à cinq. Aucun centre chinois recréé ailleurs ; Macao portugais inchangé.

Fichiers fonctionnels modifiés : `common/history/buildings/00_west_europe.txt`, `98_build_start_1776_world_redistribution.txt`, `99_1776_player_industry_agriculture_addon.txt` et `11_east_asia.txt`.

Validation : `tools/rhone_canton_levels_2026_10_15.py validate`. Comparaison exacte de toutes les déclarations mondiales de bâtiments avec la transformation attendue ; syntaxe, absence de doublon pour les deux cibles, marges nominales d'infrastructure positives ou nulles et empreintes de tous les autres fichiers fonctionnels contrôlées. Les vingt niveaux de thé, les soixante lanciers chinois, les frontières, populations, technologies, infrastructures, méthodes et propriétés des autres bâtiments sont inchangés. Aucune technologie accordée.

`BASELINE.json` conserve les textes antérieurs et la référence courante du workspace ; les anciennes baselines ne sont pas réécrites. Résultats dans `VALIDATION.json`. HEAD et index Git inchangés ; aucun commit ou push.

À confirmer dans une nouvelle partie : armement français du Rhône niveau cinq, centre de commerce chinois du Guangdong occidental niveau dix et port niveau cinq. Ces modifications de départ ne réécrivent pas une sauvegarde existante.
