# HOTFIX-5C2C - India Railway strategic regions

## 1. Resume

La chaine India Railway utilisait dix references aux cinq anciennes strategic regions indiennes. Les deux listes regionales sont remplacees par les strategic regions vanilla valides `region_north_india` et `region_south_india`, sans changer la technologie, les dates ou la mecanique ferroviaire.

## 2. Etat Git initial

| Element | Resultat |
|---|---|
| Branche | `hotfix-dlc-audit` |
| Working tree initial | Propre |
| HEAD initial | `ca595b5 Fix India geographic region references` |
| HOTFIX-5C2B | Present |
| Stash | `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` |
| Action sur le stash | Aucune |

## 3. Definitions vanilla verifiees

La vanilla locale definit `region_south_india` a la ligne 29 et `region_north_india` a la ligne 43 de `C:\Games\Victoria 3 The Great Wave\game\common\strategic_regions\west_south_asia_strategic_regions.txt`. Les cinq anciennes regions Bengal, Bombay, Central India, Madras et Punjab ne possedent aucune definition vanilla dans ce dossier.

## 4. References initiales trouvees

| Fichier | Bloc | Anciennes references |
|---|---|---:|
| `common/journal_entries/04_india_railway.txt` | `je_india_railway.possible` / presence pres de la ligne | 5 |
| `events/india_events/india_railway.txt` | `india_railway.5` / `ordered_scope_state.limit` | 5 |
| **Total** | | **10** |

## 5. Comparaison fork/hotfix/vanilla

Le hotfix et la vanilla emploient les deux regions nord/sud dans les memes deux blocs. La JE evalue des strategic-region scopes avec `root_owns_state_in_region`; l'evenement evalue un state avec `region = sr:*` dans un `ordered_scope_state`. Les deux syntaxes sont donc conservees.

## 6. Modification de la JE India Railway

Dans `je_india_railway`, les cinq scopes invalides sont remplaces par:

```txt
sr:region_north_india = { root_owns_state_in_region = yes }
sr:region_south_india = { root_owns_state_in_region = yes }
```

La garde `ip2_content`, `railways`, les conditions de possession, progress bars, modifiers, seuils, recompenses, tooltips, variables et le niveau technologique initial de BIC sont inchanges.

## 7. Modification des events India Railway

Dans `india_railway.5`, la liste de cinq regions de l'`OR` est remplacee par `region_south_india` et `region_north_india`. IDs, triggers technologiques, scopes, random lists, options, modifiers, constructions, niveaux de railway, batiments, personnages, dates, poids IA et localisations sont inchanges.

## 8. Tableau des dix references retirees

| Fichier | References retirees | Remplacement |
|---|---:|---|
| `common/journal_entries/04_india_railway.txt` | 5 | `region_north_india`, `region_south_india` |
| `events/india_events/india_railway.txt` | 5 | `region_south_india`, `region_north_india` |
| **Total** | **10** | |

## 9. Total global avant/apres

Le recomptage de `common/` et `events/`, sur les cinq tokens exacts et en excluant les commentaires, passe de **383** a **373** references invalides. Repartition apres phase: Bengal 68, Bombay 79, Central India 75, Madras 74, Punjab 77.

## 10. Technologies et dates

Aucune technologie ni date n'a ete modifiee. La condition `has_technology_researched = railways` reste strictement identique.

## 11. Batiments et niveaux de railway

Aucun batiment, effet de construction, niveau de railway ou mecanique ferroviaire n'a ete modifie.

## 12. BIC et frontier colonization

BIC, ses lois et `law_frontier_colonization` sont inchanges.

## 13. Risques restants

Les 373 references invalides restantes sont hors perimetre, notamment dans les chaines Sepoy/Famines, IA, HQ/formations, Durrani et boutons coloniaux legacy. La chaine India Railway doit etre testee en jeu avec le contenu IP2 actif.

## 14. Tests recommandes en jeu

1. Lancer une partie avec le mod seul et verifier `error.log` pour les cinq anciennes regions.
2. Jouer BIC ou Raj avec IP2 actif, rechercher `je_india_railway` et verifier son activation apres la technologie `railways`.
3. Verifier le choix de state de `india_railway.5`, les options et les constructions de railway associees.
4. Confirmer que les rails existants, les dates, les modifiers et les textes restent inchanges.

## 15. Fichiers modifies/crees

- `common/journal_entries/04_india_railway.txt`
- `events/india_events/india_railway.txt`
- `docs/reports/hotfix/HOTFIX_5C2C_INDIA_RAILWAY_REGIONS.md`

## 16. Autre gameplay non modifie

Aucun fichier Famines, Sepoy, Durrani, formation militaire, loi, localisation, bouton colonial, NAVY, ADMIN ou MARATH n'a ete modifie.

## 17. Stash MARATH

Le stash `WIP NAVY-3C-3 Maratha Konkan Flotilla` n'a ete ni applique, ni inspecte, ni restaure, ni modifie.
