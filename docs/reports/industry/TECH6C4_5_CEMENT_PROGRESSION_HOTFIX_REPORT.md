# TECH6C4.5 — Correctif de progression du ciment

## Résultat

Le correctif établit une offre de ciment hydraulique dès `hydraulic_cements`, transforme `portland_cement` en amélioration productive et relie explicitement `reinforced_concrete` à cette amélioration. Aucun bien supplémentaire, bâtiment supplémentaire ni positionnement GUI n'est créé.

## Topologie technologique

### Ancienne topologie locale

```text
professional_civil_engineering + industrial_ceramics
    -> hydraulic_cements
        -> portland_cement

bessemer_process + hydraulic_cements
    -> reinforced_concrete
```

Cette topologie permettait à `reinforced_concrete` de contourner `portland_cement`.

### Nouvelle topologie

```text
professional_civil_engineering + industrial_ceramics
    -> hydraulic_cements
        -> portland_cement
            -> reinforced_concrete

bessemer_process -----------------> reinforced_concrete
```

Changements de parents :

| tech_id | Anciens parents | Nouveaux parents | Raison |
|---|---|---|---|
| `hydraulic_cements` | `professional_civil_engineering`, `industrial_ceramics` | inchangés | Les deux prérequis restent cohérents et aucun changement n'est nécessaire. |
| `portland_cement` | `hydraulic_cements` | inchangé | La relation directe souhaitée existait déjà. |
| `reinforced_concrete` | `bessemer_process`, `hydraulic_cements` | `bessemer_process`, `portland_cement` | Portland devient le prédécesseur cimentier direct obligatoire ; Bessemer est conservé pour la disponibilité de l'acier d'armature. |

Le graphe reste acyclique. `hydraulic_cements` est en `era_6`, `portland_cement` en `era_7` et `reinforced_concrete` en `era_8`.

## Verrou du bâtiment

- Ancien verrou de `building_cement_works` : `portland_cement`.
- Nouveau verrou : `hydraulic_cements`.
- Bien produit : toujours l'unique bien générique `cement`.

## Méthodes de production

Le groupe exclusif `pmg_base_building_cement_works` contient désormais, dans l'ordre :

1. `pm_hydraulic_cement_process`, méthode initiale ; verrou `hydraulic_cements` ;
2. `pm_portland_cement_process`, amélioration ; verrou `portland_cement`.

Un PMG de base n'active qu'une méthode à la fois. `replacement_if_valid` n'est donc pas requis : ce mécanisme vanilla sert au remplacement conditionnel d'une entrée par une autre, tandis qu'ici les deux méthodes appartiennent normalement au même choix progressif.

### Procédé hydraulique

Par niveau :

```text
INPUT limestone = 30
INPUT coal = 10
OUTPUT cement = 30
POLLUTION = 10
SHOPKEEPERS = 500
LABORERS = 3000
MACHINISTS = 1000
ENGINEERS = 500
TOTAL WORKFORCE = 5000
```

L'icône temporaire est `gfx/error_deer.dds`, conformément à la politique d'assets.

### Procédé Portland conservé

Par niveau :

```text
INPUT limestone = 30
INPUT coal = 15
OUTPUT cement = 40
POLLUTION = 15
SHOPKEEPERS = 500
LABORERS = 3000
MACHINISTS = 1000
ENGINEERS = 500
TOTAL WORKFORCE = 5000
```

La recette et la main-d'œuvre Portland existantes sont inchangées ; seul son statut de méthode par défaut est retiré et son verrou technologique devient explicite.

## Comparaison économique aux prix de base

Prix utilisés : `limestone = 20`, `coal = 30`, `cement = 40`.

| Procédé | Valeur des intrants | Valeur de la production | Marge brute avant salaires | Production par 5 000 travailleurs |
|---|---:|---:|---:|---:|
| Hydraulique | `30×20 + 10×30 = 900` | `30×40 = 1 200` | `300` | 30 ciment |
| Portland | `30×20 + 15×30 = 1 050` | `40×40 = 1 600` | `550` | 40 ciment |

Le procédé hydraulique reste exploitable, mais Portland fournit 33,3 % de ciment supplémentaire avec la même main-d'œuvre et augmente la marge brute de 83,3 %.

## Demande de construction préservée

- `pm_steel_frame_buildings` conserve `goods_input_cement_add = 30`.
- `pm_arc_welded_buildings` conserve `goods_input_cement_add = 40`.

## Fichiers changés

Gameplay :

1. `common/technology/technologies/90_tech3a_vanilla_post1836_compatibility.txt`
2. `common/buildings/11_tech6c1b_cement_works.txt`
3. `common/production_method_groups/11_tech6c1b_cement_pmgs.txt`
4. `common/production_methods/11_tech6c1b_cement_production.txt`

Localisation :

5. `localization/english/tech6c1b_portland_cement_l_english.yml`
6. `localization/french/tech6c1b_portland_cement_l_french.yml`

Documentation :

7. `docs/reports/industry/TECH6C4_5_CEMENT_PROGRESSION_HOTFIX_REPORT.md`

## Validation

- Verrou du bâtiment : `hydraulic_cements` — PASS.
- Chaîne directe `hydraulic_cements -> portland_cement -> reinforced_concrete` — PASS.
- Parent acier `bessemer_process` préservé — PASS.
- `pm_hydraulic_cement_process` défini une fois — PASS.
- `pm_portland_cement_process` défini une fois — PASS.
- Les deux PM sont résolus dans `pmg_base_building_cement_works` — PASS.
- Méthode hydraulique disponible au déverrouillage du bâtiment — PASS.
- Méthode Portland verrouillée jusqu'à `portland_cement` — PASS.
- Bien `cement` défini une fois ; aucun bien `concrete` créé — PASS.
- Demande existante des méthodes de construction préservée — PASS.
- Cycle technologique introduit — aucun.
- Autre topologie technologique modifiée — aucune.
- `gui/tech_tree.gui` modifié — non.
- Équilibrage du prix du ciment modifié — non.
- Validation syntaxique/statique — PASS : accolades équilibrées, relations bâtiment/PMG/PM résolues et définitions uniques.
- Graphe technologique — PASS : 286 nœuds analysés, zéro cycle.
- `git diff --check` — PASS (seulement des avertissements informatifs LF/CRLF de Git sous Windows).
- Validation en jeu — non revendiquée.

```text
CEMENT PROGRESSION HOTFIX: PASS
```
