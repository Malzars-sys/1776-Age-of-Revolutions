# HOTFIX-4A - Ryukyu Rivalry

## 1. Resume

Import conditionnel effectue. Le bloc Ryukyu Rivalry est suffisamment isole pour etre ajoute sans modifier le setup 1776 local de Ryukyu, du Japon ou de la Chine.

Le fork ne declare pas de `replace_path` dans `descriptor.mod`. Les dependances vanilla The Great Wave restent donc disponibles pour les scripted buttons, scripted progress bars, modifiers, customizable localization et restrictions diplomatiques liees a `je_ryukyu_rivalry`. L'import local se limite aux fichiers dedies absents du fork et a un seul hook annuel dans `common/on_actions/00_code_on_actions.txt`.

## 2. Decision

Import effectue.

Raison : les dependances critiques ont ete identifiees et sont soit ajoutees en fichiers dedies, soit deja fournies par la vanilla The Great Wave. Aucune modification de pays, de states, de pops, de batiments, de Sakoku ou de Tenpo n'a ete necessaire.

## 3. Fichiers hotfix et vanilla etudies

| Fichier | Source | Role |
|---|---|---|
| `common/journal_entries/01_ryukyu_rivalry.txt` | hotfix | entree de journal `je_ryukyu_rivalry` |
| `events/japan_events/ryukyu_rivalry_events.txt` | hotfix | evenements `ryukyu_rivalry.1` a `.8` |
| `common/on_actions/00_code_on_actions.txt` | fork/vanilla | liste annuelle qui appelle `ryukyu_rivalry_coin_toss` |
| `common/on_actions/00_on_actions_yearly.txt` | vanilla | definition de `ryukyu_rivalry_coin_toss` |
| `common/scripted_buttons/ryukyu_rivalry_buttons.txt` | vanilla | quatre boutons de l'entree |
| `common/scripted_progress_bars/00_ep2_ryukyu_rivalry_progress_bars.txt` | vanilla | barres Sway et Assertiveness |
| `common/static_modifiers/00_ep2_01_modifiers.txt` | vanilla | modifiers Ryukyu Rivalry |
| `common/customizable_localization/01_ep2_custom_loc.txt` | vanilla | texte dynamique du bouton de reaffirmation |
| `localization/english/ep2_ryukyu_rivalry_l_english.yml` | vanilla | localisation anglaise principale |
| `localization/french/ep2_ryukyu_rivalry_l_french.yml` | vanilla | localisation francaise principale |
| `localization/english/ep2_01_l_english.yml` | vanilla | tooltips partages Sway/Assertiveness |
| `localization/french/ep2_01_l_french.yml` | vanilla | tooltips partages Sway/Assertiveness |

## 4. Dependances trouvees

| Element | Fichier | Role | Dependance critique ? |
|---|---|---|---|
| `je_ryukyu_rivalry` | `common/journal_entries/01_ryukyu_rivalry.txt` | entree de journal contextless | oui |
| `ryukyu_rivalry.1` a `.8` | `events/japan_events/ryukyu_rivalry_events.txt` | evenements de boutons, resolution, demarrage | oui |
| `je_ryukyu_rivalry_score_bar` | vanilla scripted progress bars | influence Japon/Chine | oui |
| `je_ryukyu_rivalry_progress_bar` | vanilla scripted progress bars | neutralite Ryukyu | oui |
| `je_ryukyu_rivalry_reaffirm_suzerainty_button` | vanilla scripted buttons | action diplomatique | oui |
| `je_ryukyu_rivalry_sway_merchants_button` | vanilla scripted buttons | action commerciale | oui |
| `je_ryukyu_rivalry_inspect_defenses_button` | vanilla scripted buttons | action militaire | oui |
| `je_ryukyu_rivalry_honor_kikoeogimi_button` | vanilla scripted buttons | action ceremonielle | oui |
| `ryukyu_rivalry_coin_toss` | vanilla yearly on_action | incidents aleatoires si les deux rivaux entrainent Ryukyu | oui |
| `modifier_ryukyu_rivalry_*` | vanilla static modifiers | effets des actions et resolutions | oui |
| `ryukyu_rivalry_reaffirm_suzerainty` | vanilla customizable localization | nom dynamique du bouton Japon/Chine | oui |
| `ryukyu_rivalry_sway_tt` | loc EP2 | tooltip de la jauge Sway | oui, recopiee |
| `ryukyu_rivalry_assertiveness_tt` | loc EP2 | tooltip de neutralite | oui, recopiee |

## 5. Setup RYU/JAP/CHI verifie

| Element | Statut fork | Statut hotfix | Conflit ? | Action |
|---|---|---|---|---|
| `c:RYU` | existe dans `common/history/countries/ryu - ryukyu.txt` | existe | non | conserve |
| `c:JAP` | existe dans `common/history/countries/jap - japan.txt` | existe | non | conserve |
| `c:CHI` | existe dans `common/history/countries/chi - china.txt` | existe | non | conserve |
| Ryukyu tributaire | `c:JAP` a `c:RYU` comme tributaire dans `00_subject_relationships.txt` | idem hotfix/vanilla | non | conserve |
| Ryukyu state | `STATE_RYUKYU_ISLANDS` contient du territoire `c:RYU` et `c:JAP` | present | non | conserve |
| Japon ferme | `law_sakoku` et `law_closed_borders` actifs | present | non | la Rivalry reste inactive tant que le Japon est ferme |
| Variable `ryukyu_rival_member` | presente sur `RYU`, absente sur `JAP`/`CHI` dans le fork | presente sur `JAP`; vanilla aussi sur `CHI` | oui mineur | initialisee dans la JE au lieu de modifier les pays |

## 6. Fichiers modifies

| Fichier | Type de changement |
|---|---|
| `common/journal_entries/01_ryukyu_rivalry.txt` | nouveau fichier hotfix, adapte pour initialiser `ryukyu_rival_member` sur `JAP` et `CHI` au demarrage de la JE |
| `events/japan_events/ryukyu_rivalry_events.txt` | nouveau fichier hotfix dedie |
| `common/on_actions/00_code_on_actions.txt` | ajout d'un seul appel `ryukyu_rivalry_coin_toss` dans `on_yearly_pulse_country` |
| `localization/english/hotfix_ryukyu_rivalry_l_english.yml` | nouveau fichier dedie EN |
| `localization/french/hotfix_ryukyu_rivalry_l_french.yml` | nouveau fichier dedie FR |
| `docs/reports/hotfix/HOTFIX_4A_RYUKYU_RIVALRY.md` | rapport |

## 7. Ce qui n'a pas ete importe

- Aucun fichier de pays (`JAP`, `RYU`, `CHI`) n'a ete modifie.
- Aucun fichier de states, pops ou buildings n'a ete modifie.
- Les scripted buttons, progress bars, modifiers, customizable localization et restrictions diplomatiques n'ont pas ete recopies, car la vanilla The Great Wave les fournit et le mod ne les masque pas via `replace_path`.
- Aucun fichier Hokkaido, Iwakura, Zaibatsu, Tenpo ou Sakoku n'a ete importe.

## 8. Risques restants

- Si un futur `replace_path` est ajoute sur `common/scripted_buttons`, `common/scripted_progress_bars`, `common/static_modifiers`, `common/customizable_localization`, `common/diplomatic_actions` ou `common/diplomatic_plays`, il faudra importer les dependances vanilla correspondantes.
- Le bloc Ryukyu Rivalry devient actif seulement apres ouverture du Japon, car la JE exige que `c:JAP` n'ait plus `law_isolationism` ni `law_closed_borders`. C'est voulu pour ne pas casser le depart 1776.
- Les fichiers de localisation dedies reprennent les textes vanilla FR/EN et les quatre tooltips partages necessaires ; il faudra verifier en jeu qu'aucune cle secondaire ne manque.

## 9. Tests a faire en jeu

1. Lancer une partie Japon en 1776.
2. Confirmer que `je_ryukyu_rivalry` n'apparait pas tant que le Japon conserve `law_sakoku` / `law_closed_borders`.
3. Ouvrir le Japon via la chaine Sakoku et verifier que la Rivalry apparait.
4. Verifier que les boutons de l'entree fonctionnent et affichent du texte en francais.
5. Tester Japon, Chine et Ryukyu en observation pour voir les evenements `ryukyu_rivalry.1` a `.8`.
6. Laisser passer au moins un an apres activation pour tester `ryukyu_rivalry_coin_toss`.
7. Surveiller `error.log` avec les patterns : `je_ryukyu_rivalry`, `ryukyu_rivalry`, `scripted_progress_bar`, `scripted_button`, `modifier_ryukyu_rivalry`, `ryukyu_rival_member`.

## 10. Liste exacte des fichiers crees/modifies

Crees :

- `common/journal_entries/01_ryukyu_rivalry.txt`
- `events/japan_events/ryukyu_rivalry_events.txt`
- `localization/english/hotfix_ryukyu_rivalry_l_english.yml`
- `localization/french/hotfix_ryukyu_rivalry_l_french.yml`
- `docs/reports/hotfix/HOTFIX_4A_RYUKYU_RIVALRY.md`

Modifie :

- `common/on_actions/00_code_on_actions.txt`

## 11. Confirmation

- Pas de Hokkaido.
- Pas d'Iwakura.
- Pas de Zaibatsu.
- Pas de Tenpo.
- Pas de Sakoku.
- Pas de modification SKH/ULT/EZO.
- Pas de modification NAVY/ADMIN/IR1/BIC.
- Pas de modification de `common/history/states/00_states.txt`.
- Pas de modification de `common/history/buildings/11_east_asia.txt`.
- Pas de modification de `common/history/pops/11_east_asia.txt`.
- Pas de modification de `common/history/countries/jap - japan.txt`.
- Pas de modification de `common/history/countries/ryu - ryukyu.txt`.
- Stash MARATH non touche.
- Aucun commit automatique.
