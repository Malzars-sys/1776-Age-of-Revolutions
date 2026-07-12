# HOTFIX-5C2B - Afghanistan, Asie centrale et Krakatoa

## 1. Resume

Cette phase remplace uniquement 82 references aux cinq anciennes strategic regions indiennes invalides dans les quatre fichiers autorises. Les chaines Afghanistan et Asie centrale utilisent desormais `geographic_region_india`; Krakatoa conserve ses zones historiques distinctes avec les geographic regions `*_old` appropriees.

## 2. Etat Git initial

| Element | Resultat |
|---|---|
| Branche | `hotfix-dlc-audit` |
| Working tree initial | Propre |
| HEAD initial | `3aeb09e Fix high confidence India region references` |
| Audit HOTFIX-5C1 | Commit `e559efc` present |
| Stash | `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` |
| Action sur le stash | Aucune |

## 3. Definitions geographic regions verifiees

Reference vanilla: `C:\Games\Victoria 3 The Great Wave\game`.

| Geographic region | Fichier vanilla | Membres |
|---|---|---|
| `geographic_region_india` | `common/geographic_regions/04_geographic_regions_asia.txt:43` | `region_north_india`, `region_south_india`, Quetta, Pashtunistan, Kashmir, Baluchistan |
| `geographic_region_madras_old` | `common/geographic_regions/06_old_strategic_regions.txt:512` | Ceylon, Circars, Mysore, Travancore, Madras, Hyderabad, Kurnool |
| `geographic_region_bengal_old` | meme fichier, ligne 517 | Bihar, East Bengal, West Bengal, Assam, Orissa |
| `geographic_region_bombay_old` | meme fichier, ligne 522 | Bombay, Gujarat, Sindh, Baluchistan |
| `geographic_region_punjab_old` | meme fichier, ligne 527 | Punjab, Hill Punjab, Delhi, Rajputana |
| `geographic_region_central_india_old` | meme fichier, ligne 537 | Central Provinces, Awadh, Malwa, Agra, Bundelkhand |

La syntaxe retenue est `is_in_geographic_region = geographic_region_*`, valide dans les scopes d'etat utilises par `any_scope_state`, `every_state` et `random_scope_state`. Elle est utilisee par la vanilla locale et par le hotfix upstream dans les memes chaines.

## 4. Corrections de la JE Afghanistan

`common/journal_entries/03_afghanistan.txt` perd 40 references: vingt paires `region_punjab` et `region_bombay` sont remplacees par vingt tests `geographic_region_india`. Les gardes EP1, Central Asia, Himalayas, Pashtunistan, Quetta, Baluchistan, transferts, seuils, objectifs, progress bars et recompenses restent inchanges.

## 5. Corrections des events Afghanistan

`events/soi_events/00_ep1_afghanistan_events.txt` perd 16 references: huit paires Bombay/Punjab sont remplacees par huit tests `geographic_region_india`. Balkh, Pashtunistan, Quetta, Baluchistan, relations, options et effets de transfert sont inchanges.

## 6. Corrections des events Kazakhstan/Asie centrale

`events/soi_events/00_ep1_kazakh_events.txt` perd 20 references: quatre listes de cinq anciennes regions sont remplacees par quatre tests `geographic_region_india`. Les scopes Russie/Kazakhs, les relations, options, conditions EP1 et le seuil `count >= 3` sont inchanges.

## 7. Corrections Krakatoa

`events/krakatoa_events.txt` perd six references: Bombay devient `geographic_region_bombay_old`, Madras devient `geographic_region_madras_old` et Bengal devient `geographic_region_bengal_old`, dans chacun des deux blocs concernes. La date `game_date >= 1850.1.1`, les states cotiers, modifiers, scopes, effets et zones non indiennes restent inchanges.

## 8. Tableau des references retirees

| Fichier | References retirees | Remplacement |
|---|---:|---|
| `common/journal_entries/03_afghanistan.txt` | 40 | `geographic_region_india` |
| `events/soi_events/00_ep1_afghanistan_events.txt` | 16 | `geographic_region_india` |
| `events/soi_events/00_ep1_kazakh_events.txt` | 20 | `geographic_region_india` |
| `events/krakatoa_events.txt` | 6 | subdivisions `*_old` correspondantes |
| **Total** | **82** | |

## 9. Total global avant/apres

Le recomptage de `common/` et `events/`, sur les cinq tokens exacts et en excluant les commentaires, passe de **465** a **383** references invalides. Repartition apres phase: Bengal 70, Bombay 81, Central India 77, Madras 76, Punjab 79.

## 10. Validation des syntaxes par scope

Les trois chaines Afghanistan/Asie centrale evaluent des states dans leurs iterators: `is_in_geographic_region = geographic_region_india` est donc la forme vanilla adaptee. Les deux selections Krakatoa evaluent aussi des states et utilisent les trois subdivisions vanilla historiques. Aucune syntaxe `region = sr:*` obsolete n'est conservee dans les quatre fichiers modifies.

## 11. Durrani inchange

La JE Durrani, les interets `c:DUR`, les formations DUR et HOTFIX-5D ne sont pas modifies.

## 12. BIC et frontier colonization inchanges

Cette phase ne modifie ni BIC, ni ses lois, ni `law_frontier_colonization`, ni son historique, ni ses formations.

## 13. Risques restants

Les 383 references invalides restantes sont hors perimetre. Elles comprennent notamment les chaines Sepoy/Famines, IA, HQ/formations, Durrani et boutons coloniaux legacy. Les changements de cette phase doivent encore etre verifies dans une partie chargee avec le DLC EP1 actif.

## 14. Tests recommandes en jeu

1. Lancer une partie avec le mod seul et verifier `error.log` pour `region_bengal`, `region_bombay`, `region_central_india`, `region_madras` et `region_punjab`.
2. Tester les contenus EP1 Afghanistan, y compris les propositions de frontiere et transferts potentiels.
3. Verifier les evenements russes d'Asie centrale et leurs conditions de presence en Inde.
4. Apres 1850, verifier la chaine Krakatoa et les effets cotiers indiens.

## 15. Fichiers modifies/crees

- `common/journal_entries/03_afghanistan.txt`
- `events/soi_events/00_ep1_afghanistan_events.txt`
- `events/soi_events/00_ep1_kazakh_events.txt`
- `events/krakatoa_events.txt`
- `docs/reports/hotfix/HOTFIX_5C2B_AFGHANISTAN_CENTRAL_ASIA_KRAKATOA.md`

## 16. Objets non modifies

Aucune formation militaire, loi, localisation, construction, bouton colonial, fichier NAVY, fichier ADMIN, pays, state explicite, recompense, date ou option n'a ete modifie.

## 17. Stash MARATH

Le stash `WIP NAVY-3C-3 Maratha Konkan Flotilla` n'a ete ni applique, ni inspecte, ni restaure, ni modifie.
