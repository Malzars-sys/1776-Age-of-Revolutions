# HOTFIX-4D - Zaibatsu

## 1. Resume

Import effectue, de facon limitee.

Le bloc Zaibatsu du hotfix a ete importe car les deux fichiers dedies sont nouveaux dans le fork et identiques a la vanilla The Great Wave :

- `common/journal_entries/07_zaibatsu.txt`
- `events/japan_events/ep2_zaibatsu_events.txt`

La localisation anglaise et francaise visible a ete ajoutee dans des fichiers dedies pour eviter les cles brutes en jeu francais.

## 2. Decision : import effectue ou non

Decision : import effectue.

Motif : le bloc Zaibatsu est suffisamment isole. Il ne demande pas de changement dans le setup historique du Japon, ni dans les states, pops, buildings, Sakoku, Tenpo, Ryukyu, Hokkaido/Ezo ou Iwakura.

## 3. Fichiers hotfix et vanilla etudies

| Fichier | Source | Resultat |
| --- | --- | --- |
| `common/journal_entries/07_zaibatsu.txt` | hotfix + vanilla | identique hotfix/vanilla, absent du fork |
| `events/japan_events/ep2_zaibatsu_events.txt` | hotfix + vanilla | identique hotfix/vanilla, absent du fork |
| `common/on_actions/00_code_on_actions.txt` | fork + vanilla | aucune modification importee |
| `common/company_charter_types/00_company_charter_types.txt` | vanilla | dependance disponible via vanilla |
| `common/amendments/00_amendments_ep2_04.txt` | vanilla | dependance disponible via vanilla |
| `common/scripted_triggers/00_ep2_victoria_scripted_triggers.txt` | vanilla | contient `company_is_zaibatsu` |
| `common/scripted_guis/journal_entry_sguis.txt` | vanilla | contient `je_zaibatsu_companies_sgui` |
| `common/script_values/ep2_japan_values.txt` | vanilla | contient les seuils et valeurs Zaibatsu |
| `common/static_modifiers/00_ep2_04_modifiers.txt` | vanilla | contient les modifiers Zaibatsu |
| `common/customizable_localization/japan_custom_loc.txt` | vanilla | contient `zaibatsu_democracy_snippet` |
| `localization/english/ep2_04_l_english.yml` | vanilla | source des cles visibles EN |
| `localization/french/ep2_04_l_french.yml` | vanilla | source des cles visibles FR |
| `localization/english/amendments_ip4_l_english.yml` | vanilla | source des cles d'amendments EN |
| `localization/french/amendments_ip4_l_french.yml` | vanilla | source des cles d'amendments FR |

## 4. Dependances trouvees

| Dependance | Presente dans fork ? | Presente dans hotfix ? | Presente dans vanilla ? | Action |
| --- | --- | --- | --- | --- |
| `company_is_zaibatsu` | non directement | oui via usage | oui | utiliser vanilla |
| `country_levels_owned_by_zaibatsu` | non directement | oui via usage | oui | utiliser vanilla |
| `fraction_of_country_levels_owned_by_zaibatsu` | non directement | oui via usage | oui | utiliser vanilla |
| `je_zaibatsu_*_threshold` | non directement | oui via usage | oui | utiliser vanilla |
| `je_zaibatsu_companies_sgui` | non directement | oui via usage | oui | utiliser vanilla |
| `modifier_zaibatsu_*` | non directement | oui via usage | oui | utiliser vanilla |
| `modifier_japan_reasserted_control` | non directement | oui via usage | oui | utiliser vanilla |
| `amendment_zaibatsu_oligopoly_1/2` | non directement | oui via usage | oui | utiliser vanilla |
| `company_mitsui`, `company_mitsubishi`, `company_yasuda`, `company_sumitomo` | oui/vanilla | oui via usage | oui | utiliser vanilla |
| `zaibatsu_democracy_snippet` | non directement | oui via loc | oui | utiliser vanilla |

Les dossiers de dependances ci-dessus ne sont pas dans les `replace_paths` du mod. Les `replace_paths` actifs qui comptent ici sont seulement `events` et `common/journal_entries`, ce qui justifie l'import des deux fichiers dedies.

## 5. Pourquoi l'import est juge sur

- Les fichiers Zaibatsu sont absents du fork et nouveaux.
- Les fichiers hotfix importes sont identiques aux fichiers vanilla The Great Wave.
- Les dependances lourdes sont dans des dossiers non remplaces par le mod.
- Aucun fichier global existant n'a ete remplace.
- Aucun fichier historique pays/state/pop/building n'a ete touche.
- Aucun hook on_action n'a ete ajoute : le bloc fonctionne sans modifier `common/on_actions/00_code_on_actions.txt`, et la mecanique generique de confiance electorale existe deja dans le fork.

## 6. Fichiers modifies

| Fichier | Type | Role |
| --- | --- | --- |
| `common/journal_entries/07_zaibatsu.txt` | nouveau gameplay dedie | entree de journal `je_zaibatsu` |
| `events/japan_events/ep2_zaibatsu_events.txt` | nouveau gameplay dedie | evenements `zaibatsu.1` et `zaibatsu.2` |
| `localization/english/hotfix_zaibatsu_l_english.yml` | nouvelle localisation | cles visibles EN Zaibatsu |
| `localization/french/hotfix_zaibatsu_l_french.yml` | nouvelle localisation | cles visibles FR Zaibatsu |
| `docs/reports/hotfix/HOTFIX_4D_ZAIBATSU.md` | nouveau rapport | trace d'audit/import |

## 7. Ce qui n'a pas ete importe

- Pas de `events/japan_events/ep2_japan_political_events.txt`.
- Pas de `common/journal_entries/07_korea_colonization.txt`, meme s'il contient une condition alternative liee a `je_zaibatsu` dans la vanilla/hotfix.
- Pas de fichier `common/on_actions/00_code_on_actions.txt`.
- Pas de fichier `common/history/countries/jap - japan.txt`.
- Pas de states, pops, buildings, diplomatie ou pays.
- Pas de Sakoku, Tenpo, Iwakura, Ryukyu, Hokkaido/Ezo.

## 8. Risques restants

| Risque | Niveau | Commentaire |
| --- | --- | --- |
| Zaibatsu peut apparaitre tard ou jamais en 1776 | faible | L'entree demande industrialisation, compagnies et lois economiques avancees. C'est attendu. |
| Renommage IG en `ig_zaibatsu` absent | faible a moyen | L'evenement politique vanilla qui renomme les industrialistes n'a pas ete importe. Les events Zaibatsu utilisent `ig_industrialists`, donc ce n'est pas bloquant. |
| Colonisation de la Coree non adaptee a `je_zaibatsu` | faible | `07_korea_colonization.txt` n'existe pas dans le fork. Ce n'est pas une dependance directe de Zaibatsu. |
| Localisation volontairement dediee | faible | Les cles existent aussi en vanilla, mais les fichiers dedies rendent l'import robuste cote mod. |

## 9. Tests a faire en jeu

1. Lancer le jeu avec le mod seul et verifier `error.log` au menu.
2. Demarrer une partie avec le Japon.
3. Verifier qu'aucune erreur `je_zaibatsu`, `zaibatsu.1`, `zaibatsu.2`, `company_is_zaibatsu`, `je_zaibatsu_companies_sgui`, `amendment_zaibatsu_oligopoly` n'apparait dans `error.log`.
4. En partie avancee ou en console, verifier que `je_zaibatsu` peut apparaitre apres industrialisation et compagnies japonaises.
5. En francais, verifier que les textes Zaibatsu ne s'affichent pas en cles brutes.

## 10. Liste exacte des fichiers crees/modifies

- `common/journal_entries/07_zaibatsu.txt`
- `events/japan_events/ep2_zaibatsu_events.txt`
- `localization/english/hotfix_zaibatsu_l_english.yml`
- `localization/french/hotfix_zaibatsu_l_french.yml`
- `docs/reports/hotfix/HOTFIX_4D_ZAIBATSU.md`

## 11. Confirmations

- Pas d'Iwakura importe.
- Pas de Ryukyu modifie.
- Pas de Hokkaido/Ezo modifie.
- Pas de Sakoku modifie.
- Pas de Tenpo modifie.
- Pas de SKH/ULT/EZO modifie.
- Pas de NAVY modifie.
- Pas d'ADMIN modifie.
- Pas d'IR1 modifie.
- Pas de BIC modifie.
- Aucun fichier states/pops/buildings/country n'a ete modifie.
- Aucun fichier on_action existant n'a ete modifie.
- Le stash MARATH n'a pas ete applique ni modifie.
