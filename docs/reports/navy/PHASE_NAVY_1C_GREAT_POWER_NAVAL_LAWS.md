# Phase NAVY-1C - Lois navales GBR/FRA/SPA

## 1. Resume

Cette phase a deux objectifs :

- ranger les rapports Markdown dans `docs/reports/` ;
- verifier puis corriger la loi de modele naval de depart pour la Grande-Bretagne, la France et l'Espagne.

Les trois pays ont maintenant `law_professional_navy`, localisee en francais comme "Flotte capitale".

## 2. Fichiers modifies

Rangement :

- rapports Markdown deplaces vers `docs/reports/audit/`
- rapports Markdown deplaces vers `docs/reports/phase1/`
- rapports Markdown deplaces vers `docs/reports/navy/`
- rapports Markdown deplaces vers `docs/reports/admin/`
- rapports Markdown deplaces vers `docs/reports/localization/`
- `docs/reports/INDEX.md`
- `docs/reports/PHASE_HOUSEKEEPING_1_REPORTS_ORGANIZATION.md`

Gameplay, uniquement lois pays :

- `common/history/countries/gbr - great britain.txt`
- `common/history/countries/fra - france.txt`
- `common/history/countries/spa - spain.txt`

## 3. Lois navales vanilla identifiees

Reference : `C:\Games\Victoria 3 The Great Wave\game\common\laws\00_navy_model.txt`

| ID | Localisation FR | Groupe | Prequis |
|---|---|---|---|
| `law_merchant_navy` | Marine marchande | `lawgroup_navy_model` | aucun, pays côtier |
| `law_jeune_ecole` | Jeune Ecole | `lawgroup_navy_model` | `jeune_ecole` |
| `law_professional_navy` | Flotte capitale | `lawgroup_navy_model` | `military_drill` |
| `law_diplomatic_navy` | Flotte diplomatique | `lawgroup_navy_model` | `military_drill` |

Reference groupe : `C:\Games\Victoria 3 The Great Wave\game\common\law_groups\00_laws.txt`

`lawgroup_navy_model` est un groupe `power_structure` active pour les pays ayant au moins un state côtier.

## 4. IDs exacts trouves

Les IDs exacts utilises par The Great Wave sont :

- `law_merchant_navy`
- `law_jeune_ecole`
- `law_professional_navy`
- `law_diplomatic_navy`

Il n'existe pas d'ID `law_capital_navy` : la loi affichee "Flotte capitale" correspond a `law_professional_navy`.

## 5. Syntaxe vanilla confirmee

La syntaxe vanilla dans `common/history/countries/*.txt` est :

```txt
activate_law = law_type:law_professional_navy
```

Exemples vanilla The Great Wave :

- `gbr - great britain.txt` : `activate_law = law_type:law_professional_navy`
- `fra - france.txt` : `activate_law = law_type:law_professional_navy`
- `rus - russia.txt` : `activate_law = law_type:law_professional_navy`
- `spa - spain.txt` : `activate_law = law_type:law_diplomatic_navy`

## 6. Audit des lois actuelles GBR/FRA/SPA

Avant correction, les trois fichiers du mod ne contenaient pas de loi du groupe `lawgroup_navy_model`.

| Pays | Loi navale actuelle | Loi recommandee | Justification | Action |
|---|---|---|---|---|
| `GBR` | absente | `law_professional_navy` | premiere puissance navale, flotte de ligne massive, presence mondiale | ajoutee |
| `FRA` | absente | `law_professional_navy` | grande marine d'Etat, rivalite directe avec la Royal Navy | ajoutee |
| `SPA` | absente | `law_professional_navy` | grande flotte imperiale encore importante en 1776 | ajoutee |

Les trois pays utilisent `effect_starting_technology_tier_4_tech`, qui donne `military_drill`. Le prequis de `law_professional_navy` est donc rempli sans ajout de technologie.

## 7. Corrections appliquees

Ajouts effectues :

- `GBR` : `activate_law = law_type:law_professional_navy`
- `FRA` : `activate_law = law_type:law_professional_navy`
- `SPA` : `activate_law = law_type:law_professional_navy`

Aucune autre loi n'a ete modifiee.

## 8. Justification historique

### Grande-Bretagne

La Royal Navy est le coeur de la puissance britannique en 1776. Une loi de flotte capitale est coherente avec sa flotte de ligne, ses arsenaux, ses bases et sa projection mondiale.

### France

La France possede une marine d'Etat importante, organisee pour soutenir une guerre de flotte contre la Grande-Bretagne. `law_professional_navy` correspond mieux que `law_merchant_navy`.

### Espagne

L'Espagne conserve une flotte imperiale majeure et des arsenaux importants. En 1776, la logique est encore celle d'une marine de bataille et d'empire, pas d'une doctrine tardive de type Jeune Ecole.

## 9. Justification gameplay

`law_professional_navy` donne :

- bonus de construction aux capital ships ;
- bonus de prestige lie a la projection navale ;
- meilleure embauche dans les administrations navales.

Cette loi correspond aux flottes reactivees en NAVY-1A et a la logistique ajoutee en NAVY-1B, sans toucher aux ships, counts, HQ, amiraux, batiments ou technologies.

## 10. Confirmations de perimetre

Confirme :

- aucun navire modifie ;
- aucun count de flotte modifie ;
- aucun `hq_region` modifie ;
- aucun `ship_type` modifie ;
- aucun amiral modifie ;
- aucun batiment modifie ;
- aucune methode de production modifiee ;
- aucune technologie modifiee ;
- Russie et autres puissances navales non modifiees dans cette phase.

## 11. Tests a refaire en jeu

1. Lancer une nouvelle partie 1776.
2. Ouvrir la Grande-Bretagne et verifier que la loi navale est "Flotte capitale".
3. Ouvrir la France et verifier que la loi navale est "Flotte capitale".
4. Ouvrir l'Espagne et verifier que la loi navale est "Flotte capitale".
5. Verifier que les flottes, amiraux et batiments n'ont pas change.
6. Verifier que la Russie n'a pas change.
7. Laisser tourner un mois.
8. Controler `error.log` pour `invalid law`, `law group`, `naval law`, `PostValidate`, `Missing localization` et `Invalid localization`.

## 12. Risques restants

- La vanilla 1.13 donne `law_diplomatic_navy` a l'Espagne en 1836 ; le choix `law_professional_navy` est volontaire pour le setup 1776 et la flotte imperiale traitee en NAVY-1A.
- Si l'equilibrage naval devient trop favorable a l'Espagne, une phase ulterieure pourra comparer `law_professional_navy` et `law_diplomatic_navy` en test gameplay.
