# Phase 1.3 - Correction minimale des formations militaires/navales

## 1. Erreurs ciblees

Cette phase cible uniquement les erreurs de compatibilite Victoria 3 1.13 / The Great Wave liees aux anciennes formations navales :

- `PostValidate of effect 'create_military_formation' returned false` dans les fichiers `common/history/military_formations`.
- `PostValidate of trigger 'has_role' returned false` dans `events/tech_events/military_tech_events_01.txt`, lignes liees aux evenements navals Ironclads et Monitors.

Les erreurs `create_character` non directement navales restent hors perimetre de cette phase.

## 2. Anciens IDs trouves

Dans les formations militaires/navales :

- `unit_type:combat_unit_type_frigate`
- `unit_type:combat_unit_type_man_o_war`

Dans `events/tech_events/military_tech_events_01.txt` :

- `unit_type:combat_unit_type_ironclad`
- `unit_type:combat_unit_type_monitor`
- `has_role = admiral`
- `country_navy_unit_type_fraction`
- `formation_navy_unit_type_fraction`

## 3. Nouveaux IDs utilises ou strategie choisie

Les IDs ont ete verifies dans l'installation locale vanilla Victoria 3 1.13 :

- `combat_unit_type_frigate` -> `ship_type:ship_type_frigate`
- `combat_unit_type_man_o_war` -> `ship_type:ship_type_ship_of_the_line`
- `combat_unit_type_ironclad` -> `ship_type:ship_type_early_ironclad`
- `combat_unit_type_monitor` -> `ship_type:ship_type_monitor`

Les blocs de flotte ont ete convertis de :

```txt
combat_unit = {
    type = unit_type:combat_unit_type_frigate
}
```

vers la syntaxe 1.13 :

```txt
ship = {
    type = ship_type:ship_type_frigate
}
```

Pour les evenements Ironclads et Monitors, la strategie a ete de reprendre la structure vanilla 1.13 :

- `any_scope_fleet`
- `any_scope_ship`
- `is_ship_type`
- `formation_ship_type_fraction`
- `commander ?=`

## 4. Fichiers modifies

- `common/history/military_formations/00_military_formations_europe.txt`
  - 85 references navales converties.
- `common/history/military_formations/01_military_formations_north_america.txt`
  - 13 references navales converties.
- `common/history/military_formations/02_military_formations_south_america.txt`
  - 1 reference navale convertie.
- `common/history/military_formations/03_military_formations_north_africa.txt`
  - 1 reference navale convertie.
- `common/history/military_formations/04_military_formations_middle_east.txt`
  - 8 references navales converties.
- `common/history/military_formations/05_military_formations_india.txt`
  - 1 reference navale convertie.
- `common/history/military_formations/06_military_formations_asia.txt`
  - 3 references navales converties.
- `events/tech_events/military_tech_events_01.txt`
  - evenements `military_tech_events.403` et `military_tech_events.404` adaptes a la logique navale 1.13.

## 5. Fichiers volontairement non modifies

- `common/history/military_formations/99_military_formations_example.txt`
  - aucun ancien ID naval actif a convertir.
- `common/history/buildings/*`
  - hors perimetre Phase 1.3, deja traite en Phase 1.2.
- `common/journal_entries/*`
  - hors perimetre Phase 1.3, deja traite en Phase 1.1.
- `localization/*`
  - hors perimetre.
- Autres events
  - non modifies, car les logs ne signalaient directement que `events/tech_events/military_tech_events_01.txt` pour cette correction navale.

## 6. Pourquoi la correction est minimale

La correction ne change pas les tailles de flotte, les regions, les noms de formations, les pays, ni l'equilibrage historique.

Elle remplace seulement les anciens types d'unites navales supprimes par les `ship_type` vanilla 1.13 les plus proches et convertit les blocs navals vers la syntaxe attendue par The Great Wave.

## 7. Risques restants

- Les erreurs `create_character` peuvent encore apparaitre si certains commandants ont une structure devenue invalide, mais elles n'ont pas ete modifiees ici pour eviter une refonte des personnages ou des roles.
- Les flottes converties peuvent necessiter plus tard un equilibrage fin avec les nouveaux types de navires 1.13.
- Les evenements Ironclads/Monitors utilisent la structure vanilla 1.13 ; il faudra verifier en jeu qu'ils se declenchent encore dans les conditions souhaitees du mod 1776.

## 8. Tests a faire ensuite

1. Lancer Victoria 3 avec uniquement le mod active.
2. Verifier que le jeu arrive au menu principal.
3. Verifier que la selection pays s'ouvre.
4. Lancer une partie au 1 janvier 1776.
5. Laisser tourner au moins un mois.
6. Surveiller `Documents/Paradox Interactive/Victoria 3/logs/error.log`.
7. Confirmer que les erreurs suivantes ont disparu :
   - `combat_unit_type_frigate`
   - `combat_unit_type_man_o_war`
   - `combat_unit_type_ironclad`
   - `combat_unit_type_monitor`
   - `has_role = admiral` dans `military_tech_events_01.txt`
8. Tester en priorite les pays navals :
   - France
   - Grande-Bretagne
   - Espagne
   - Pays-Bas
   - Portugal
   - Etats-Unis
   - Empire ottoman
   - Japon
