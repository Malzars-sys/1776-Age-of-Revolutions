# Phase NAVY-1A-quinquies - Russian Fleet HQ and Rebalance

## 1. Resume

Cette phase corrige uniquement la flotte initiale russe dans `common/history/military_formations/00_military_formations_europe.txt`.

Objectifs appliques :

- verifier les `hq_region` russes avec la vanilla locale The Great Wave ;
- corriger le `hq_region` obsolete de la flottille d'Okhotsk avec la region vanilla qui contient `STATE_OKHOTSK` ;
- reduire prudemment les effectifs navals russes pour replacer la Russie derriere la France et l'Espagne ;
- ne pas modifier les flottes ou amiraux de Grande-Bretagne, France et Espagne.

## 2. Probleme observe

Apres NAVY-1A, le classement naval en jeu placait la Russie au rang 2, devant la France et l'Espagne.

Audit des effectifs avant cette phase :

| Pays | Total navires | Vaisseaux de ligne | Fregates |
|---|---:|---:|---:|
| GBR | 56 | 28 | 28 |
| FRA | 34 | 18 | 16 |
| SPA | 29 | 15 | 14 |
| RUS | 42 | 25 | 17 |

La Russie etait donc trop proche de la Grande-Bretagne et au-dessus du couple France/Espagne, alors que le rapport naval 1776 classe la Russie comme puissance navale reelle mais surtout regionale.

## 3. Flottes russes avant correction

Dans `c:RUS`, deux flottes etaient presentes :

| Flotte | hq_region avant | Etat | Navires avant |
|---|---|---|---:|
| `Baltiyskiy_Flot` | `sr:region_russia` | valide vanilla 1.13 | 25 vaisseaux de ligne + 16 fregates |
| `Okhotskaya_Voyennaya_Flotiliya` | `sr:region_east_siberia` | obsolete / introuvable vanilla 1.13 | 1 fregate |

Verification vanilla :

- `region_russia` existe dans `C:\Games\Victoria 3 The Great Wave\game\common\strategic_regions\europe_strategic_regions.txt`.
- `region_northeast_asia` existe dans `C:\Games\Victoria 3 The Great Wave\game\common\strategic_regions\east_asia_strategic_regions.txt` et contient `STATE_OKHOTSK`.
- `region_siberia` existe aussi, mais ne contient pas `STATE_OKHOTSK`.
- `region_east_siberia` n'a pas ete trouve dans les strategic regions vanilla The Great Wave.

## 4. Corrections appliquees

| Fichier | Ligne actuelle | Ancien contenu | Nouveau contenu |
|---|---:|---|---|
| `common/history/military_formations/00_military_formations_europe.txt` | 2734 | `count = 25` | `count = 14` |
| `common/history/military_formations/00_military_formations_europe.txt` | 2740 | `count = 15` | `count = 8` |
| `common/history/military_formations/00_military_formations_europe.txt` | 2753 | `hq_region = sr:region_east_siberia` | `hq_region = sr:region_northeast_asia` |

La fregate d'Arkhangelsk et la fregate d'Okhotsk sont conservees.

## 5. Flottes russes apres correction

| Flotte | hq_region apres | Navires apres |
|---|---|---:|
| `Baltiyskiy_Flot` | `sr:region_russia` | 14 vaisseaux de ligne + 9 fregates |
| `Okhotskaya_Voyennaya_Flotiliya` | `sr:region_northeast_asia` | 1 fregate |

Total russe apres correction :

| Pays | Total navires | Vaisseaux de ligne | Fregates |
|---|---:|---:|---:|
| RUS avant | 42 | 25 | 17 |
| RUS apres | 24 | 14 | 10 |

Classement attendu apres correction technique :

| Pays | Total navires |
|---|---:|
| GBR | 56 |
| FRA | 34 |
| SPA | 29 |
| RUS | 24 |

## 6. Justification historique et gameplay

La Russie reste une puissance navale importante en Baltique, avec une capacite de projection deja demontree par Tchesme et l'expedition mediterraneenne. Elle ne doit cependant pas depasser la France ou l'Espagne dans le setup initial 1776, car sa puissance reste surtout regionale et la flotte permanente de mer Noire n'est pas encore stabilisee.

La reduction conserve une flotte baltique credible, mais retire l'effet de masse qui la placait artificiellement au-dessus de la France et de l'Espagne.

## 7. Limites confirmees

Cette phase n'a pas modifie :

- les flottes britanniques ;
- les flottes francaises ;
- les flottes espagnoles ;
- les amiraux GB/FRA/SPA ;
- les batiments ;
- les lois ;
- les technologies ;
- les types de navires ;
- les formations militaires non russes.

## 8. Risques restants

- Le score naval final en jeu peut encore dependre des batiments, ports, commandants, technologies et modifiers.
- `sr:region_northeast_asia` est valide en vanilla 1.13 et contient `STATE_OKHOTSK`, mais le score naval final reste a verifier en jeu.
- La Russie reste a retester en jeu pour confirmer que le classement affiche bien l'ordre attendu.

## 9. Tests a faire ensuite

1. Lancer une nouvelle partie avec le mod seul.
2. Verifier le classement naval au 1 janvier 1776.
3. Confirmer que l'ordre attendu est Grande-Bretagne, France, Espagne, puis Russie.
4. Ouvrir la Russie et verifier que les flottes `Baltiyskiy_Flot` et `Okhotskaya_Voyennaya_Flotiliya` existent.
5. Avancer d'un mois et surveiller `error.log` pour `region_east_siberia`, `create_military_formation` et erreurs de flotte russe.
