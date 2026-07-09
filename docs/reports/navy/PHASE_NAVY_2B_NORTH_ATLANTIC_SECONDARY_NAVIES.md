# Phase NAVY-2B - Puissances navales secondaires Europe du Nord / Atlantique

## 1. Resume

Cette phase implemente uniquement le bloc NAVY-2B issu de l'audit NAVY-2A :

- `NET` / Netherlands / Provinces-Unies ;
- `POR` / Portugal ;
- `DENNOR` / Danemark-Norvege ;
- `NOR` seulement pour la petite flotte deja existante ;
- `SWE` / Suede ;
- `DEI` verifie mais non modifie.

Les corrections appliquees sont conservatrices :

- correction des `hq_region` invalides des flottes ciblees ;
- reduction prudente des flottes trop hautes ;
- ajout d'un amiral historique simple pour `NET`, `DENNOR` et `SWE` ;
- ajout d'une loi navale uniquement pour les pays dont `effect_starting_technology_tier_4_tech` confirme le prerequis `military_drill` ;
- aucune modification de batiment, technologie, pops, frontieres ou flotte hors NAVY-2B.

## 2. Fichiers modifies

Gameplay :

- `common/history/military_formations/00_military_formations_europe.txt`
- `common/history/countries/net - netherlands.txt`
- `common/history/countries/por - portugal.txt`
- `common/history/countries/dennor - denmark-norway.txt`
- `common/history/countries/swe - sweden.txt`

Localisation :

- `localization/english/phase_navy_2b_admirals_l_english.yml`
- `localization/french/phase_navy_2b_admirals_l_french.yml`

Rapport :

- `docs/reports/navy/PHASE_NAVY_2B_NORTH_ATLANTIC_SECONDARY_NAVIES.md`

## 3. Rappel des constats NAVY-2A

| Pays | Etat NAVY-2A | Probleme |
|---|---|---|
| `NET` | 9 vaisseaux de ligne + 25 fregates | `region_rhine` invalide, flotte trop haute |
| `POR` | 6 vaisseaux de ligne + 8 fregates | `region_iberia` invalide |
| `DENNOR` | 6 vaisseaux de ligne + 8 fregates | `region_baltic` invalide |
| `NOR` | 1 fregate | `region_baltic` invalide |
| `SWE` | 9 vaisseaux de ligne + 9 fregates | `region_baltic` invalide, flotte un peu haute |
| `DEI` | 1 fregate | `region_indonesia` valide, pas d'action necessaire |

## 4. Corrections de hq_region

Regions vanilla verifiees dans `C:\Games\Victoria 3 The Great Wave\game\common\strategic_regions` :

- `region_western_europe`
- `region_northern_europe`
- `region_southern_europe`
- `region_indonesia`

Corrections appliquees :

| Pays | Flotte | Avant | Apres |
|---|---|---|---|
| `NET` | `Koninklijke_Marine` | `region_rhine` | `region_western_europe` |
| `POR` | `Marinha_Real_Portuguesa` | `region_iberia` | `region_southern_europe` |
| `DENNOR` | `Kongelige_Danske_Marine` | `region_baltic` | `region_northern_europe` |
| `NOR` | `Kongelige_Norske_Marine` | `region_baltic` | `region_northern_europe` |
| `SWE` | `Hgsjflottan` | `region_baltic` | `region_northern_europe` |

`DEI` conserve `region_indonesia`, deja valide.

## 5. Reequilibrage des flottes

Echelle de reference apres NAVY-1 :

- `GBR` : 56 navires ;
- `FRA` : 34 navires ;
- `SPA` : 29 navires ;
- `RUS` : 24 navires.

Resultat NAVY-2B :

| Pays | Avant | Apres | Justification |
|---|---:|---:|---|
| `NET` | 9 SOL + 25 fregates = 34 | 7 SOL + 13 fregates = 20 | puissance commerciale majeure, mais sous la Russie corrigee et loin du trio GB/FRA/SPA |
| `POR` | 6 SOL + 8 fregates = 14 | 6 SOL + 7 fregates = 13 | ajustement minimal, inferieur a l'Espagne |
| `DENNOR` | 6 SOL + 8 fregates = 14 | 6 SOL + 7 fregates = 13 | marine baltique solide, mais regionale |
| `NOR` | 1 fregate = 1 | 1 fregate = 1 | conserve sans grossissement |
| `SWE` | 9 SOL + 9 fregates = 18 | 7 SOL + 7 fregates = 14 | reste une flotte baltique importante, sans depasser la Russie |
| `DEI` | 1 fregate = 1 | 1 fregate = 1 | non modifiee |

## 6. Noms de flottes

| Pays | Decision |
|---|---|
| `NET` | `Koninklijke_Marine` conserve, nom stable et lisible |
| `POR` | `Marinha_Real_Portuguesa` conserve, nom stable et plausible |
| `DENNOR` | `Kongelige_Danske_Marine` conserve, nom stable et plausible |
| `NOR` | `Kongelige_Norske_Marine` conserve |
| `SWE` | `Hgsjflottan` remplace par `Orlogsflottan`, pour eviter le nom tronque/mojibake et rester sans caractere special |
| `DEI` | `Koloniale_Marine` conserve, non modifie |

## 7. Amiraux ajoutes ou non ajoutes

Amiraux ajoutes :

| Pays | Amiral | Rattachement | Justification |
|---|---|---|---|
| `NET` | Jan Hendrik van Kinsbergen | `Koninklijke_Marine` | candidat solide de l'audit NAVY-2A |
| `DENNOR` | Frederik Christian Kaas | `Kongelige_Danske_Marine` | candidat le plus acceptable pour une flotte danoise |
| `SWE` | Henrik af Trolle | `Orlogsflottan` | candidat principal et le plus solide pour 1776 |

Amiraux volontairement non ajoutes :

| Pays | Decision |
|---|---|
| `POR` | pas d'amiral ajoute ; les candidats portugais de l'audit restent trop incertains sans recherche dediee |
| `NOR` | pas d'amiral ajoute ; flotte symbolique d'une fregate |
| `DEI` | pas d'amiral colonial ajoute ; aucun candidat fiable dans NAVY-2A |

Les amiraux ajoutes utilisent un format simple, inspire des corrections NAVY-1A :

- `is_admiral = yes`
- nom via cles `navy_*`
- `historical = yes`
- `age`
- culture, religion, interest group et ideology minimales
- `commander_rank = default`
- transfert vers la flotte via `transfer_to_formation`

Aucune fiche detaillee, biographie ou lien Wikipedia n'a ete ajoute dans cette phase.

## 8. Lois navales ajoutees ou non ajoutees

Verification technique :

- `NET`, `POR`, `DENNOR` et `SWE` ont `effect_starting_technology_tier_4_tech = yes`.
- Dans la vanilla The Great Wave, ce niveau ajoute `military_drill`.
- `law_professional_navy` et `law_diplomatic_navy` demandent `military_drill`.

Lois ajoutees :

| Pays | Loi ajoutee | Justification |
|---|---|---|
| `NET` | `law_diplomatic_navy` | puissance commerciale et diplomatique maritime |
| `POR` | `law_diplomatic_navy` | empire atlantique et routes coloniales |
| `DENNOR` | `law_professional_navy` | battlefleet baltique d'Etat |
| `SWE` | `law_professional_navy` | battlefleet baltique d'Etat |

Lois non ajoutees :

| Pays | Decision |
|---|---|
| `NOR` | pas de loi forcee, car le setup politique avec `DENNOR` reste ambigu |
| `DEI` | pas de loi forcee, car tag colonial et flotte minime |

`law_jeune_ecole` n'a pas ete utilisee.

## 9. Confirmations de perimetre grandes puissances

Ces pays n'ont pas ete modifies :

- `GBR`
- `FRA`
- `SPA`
- `RUS`

Leurs flottes, amiraux, lois, batiments et technologies restent hors perimetre NAVY-2B.

## 10. Confirmations de perimetre hors NAVY-2B

Ces pays et zones n'ont pas ete modifies :

- `TUR` / Ottomans ;
- `VEN` / Venise ;
- `SIC` / Deux-Siciles ;
- `GEN`, `SAR`, `PAP`, `TUS` ;
- `MOR`, `MAS`, `TUN`, `TRI` ;
- `OMA` ;
- Inde, Chine, Japon, Coree, Siam.

`DEI` a ete verifie mais pas modifie.

## 11. Tests a faire en jeu

1. Lancer une nouvelle partie 1776 avec le mod seul.
2. Verifier `NET` :
   - flotte visible ;
   - `Koninklijke_Marine` dans une region valide ;
   - total autour de 20 navires ;
   - Jan Hendrik van Kinsbergen present.
3. Verifier `POR` :
   - flotte visible ;
   - total autour de 13 navires ;
   - pas d'amiral brut ou manquant.
4. Verifier `DENNOR` :
   - flotte visible ;
   - Frederik Christian Kaas present ;
   - total autour de 13 navires.
5. Verifier `NOR` :
   - petite flotte d'une fregate conservee.
6. Verifier `SWE` :
   - `Orlogsflottan` visible ;
   - Henrik af Trolle present ;
   - total autour de 14 navires.
7. Verifier que `GBR`, `FRA`, `SPA` et `RUS` n'ont pas change.
8. Laisser tourner un mois.
9. Surveiller `error.log` pour :
   - `invalid hq_region` ;
   - `create_military_formation` ;
   - `invalid character` ;
   - `invalid law` ;
   - `missing localization` ;
   - `PostValidate`.

## 12. Risques restants

- La commande de recherche signale encore `region_rhine`, `region_baltic` et `region_iberia`, mais les occurrences restantes sont dans des armees ou dans des pays hors correction NAVY-2B. Elles n'ont pas ete corrigees pour ne pas elargir la phase.
- Les lois navales sont techniquement possibles via `military_drill`, mais doivent etre confirmees en jeu pour verifier que le groupe `lawgroup_navy_model` s'applique correctement a ces pays.
- Les amiraux sont volontairement simples ; une phase future peut enrichir les fiches ou ajouter des liens Wikipedia.
- `POR` reste sans amiral historique pour eviter une attribution incertaine.
- `DEI` reste minimal avec une seule fregate.

## 13. Liste exacte des fichiers modifies

- `common/history/military_formations/00_military_formations_europe.txt`
- `common/history/countries/net - netherlands.txt`
- `common/history/countries/por - portugal.txt`
- `common/history/countries/dennor - denmark-norway.txt`
- `common/history/countries/swe - sweden.txt`
- `localization/english/phase_navy_2b_admirals_l_english.yml`
- `localization/french/phase_navy_2b_admirals_l_french.yml`
- `docs/reports/navy/PHASE_NAVY_2B_NORTH_ATLANTIC_SECONDARY_NAVIES.md`
