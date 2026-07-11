# HOTFIX-4B - Hokkaido / Ezo / Sakhalin

## 1. Resume

Decision : import effectue, mais uniquement pour le bloc dedie Hokkaido/Ezo.

Le fork remplace `common/journal_entries` et `events` via `.metadata/metadata.json`. La journal entry et les evenements vanilla/hotfix Hokkaido ne pouvaient donc pas etre charges tant qu'ils n'etaient pas ajoutes au fork. En revanche, les dependances vanilla hors `events` et `common/journal_entries` restent disponibles : scripted buttons, scripted effects, static modifiers, decrees et localisations vanilla.

Import retenu :

- `common/journal_entries/07_hokkaido.txt`
- `events/japan_events/ep2_hokkaido_events.txt`
- `localization/english/hotfix_hokkaido_l_english.yml`
- `localization/french/hotfix_hokkaido_l_french.yml`

Import refuse :

- aucun changement dans `common/history/states/00_states.txt`
- aucun changement dans `common/history/pops/11_east_asia.txt`
- aucun changement dans `common/history/buildings/11_east_asia.txt`
- aucun changement dans les pays `EZO`, `SKH`, `ULT`, `JAP`
- aucun changement dans `common/on_actions/00_code_on_actions.txt`

## 2. Decision : import effectue ou non

Import effectue, car les deux fichiers gameplay dedies du hotfix sont nouveaux dans le fork et ne remplacent pas un fichier local existant.

Le bloc est suffisamment isole pour etre importe sans ecraser les corrections locales Japon/Sakhalin/Ezo/SKH/ULT. Les fichiers d'historique states/pops/buildings du hotfix ne sont pas importes, car ils touchent directement au setup de carte deja corrige dans le fork.

## 3. Fichiers hotfix et vanilla etudies

| Fichier | Source | Role | Decision |
|---|---|---|---|
| `common/journal_entries/07_hokkaido.txt` | hotfix | Ajoute `je_taming_the_north` | importe |
| `events/japan_events/ep2_hokkaido_events.txt` | hotfix | Ajoute `hokkaido_events.1` a `.8` | importe |
| `common/history/countries/ezo - ezochi.txt` | fork/hotfix | Setup pays EZO | lu, non modifie |
| `common/history/countries/skh - sakhalin.txt` | fork | Setup pays SKH | lu, non modifie |
| `common/history/countries/ult - ulta.txt` | fork | Setup pays ULT | lu, non modifie |
| `common/history/countries/jap - japan.txt` | fork/hotfix | Setup Japon | lu, non modifie |
| `common/history/states/00_states.txt` | fork/hotfix | Ownership Hokkaido/Sakhalin | lu, non modifie |
| `common/history/pops/11_east_asia.txt` | fork/hotfix | Pops Hokkaido/Sakhalin | lu, non modifie |
| `common/history/buildings/11_east_asia.txt` | fork/hotfix | Buildings Hokkaido/Sakhalin | lu, non modifie |
| `common/scripted_buttons/07_japan_buttons.txt` | vanilla | Boutons `button_je_taming_the_north_*` | dependance vanilla conservee |
| `common/scripted_effects/00_dynamic_state_names_asia.txt` | vanilla | `STATE_HOKKAIDO_state_name_assign` | dependance vanilla conservee |
| `common/static_modifiers/00_ep2_02_modifiers.txt` | vanilla | Modifiers Hokkaido/Ainu | dependance vanilla conservee |
| `localization/english/ep2_02_l_english.yml` | vanilla | Localisation EN Hokkaido | extrait dedie cree |
| `localization/french/ep2_02_l_french.yml` | vanilla | Localisation FR Hokkaido | extrait dedie cree |

## 4. Dependances trouvees

| Dependence | Presente dans fork ? | Presente dans hotfix ? | Presente dans vanilla ? | Action recommandee |
|---|---:|---:|---:|---|
| `je_taming_the_north` | non | oui | oui | importer depuis hotfix |
| `hokkaido_events.*` | non | oui | oui | importer depuis hotfix |
| `button_je_taming_the_north_*` | non localement | non dedie | oui | ne pas copier, laisser vanilla |
| `STATE_HOKKAIDO_state_name_assign` | non localement | non dedie | oui | ne pas copier, laisser vanilla |
| `modifier_tamed_north` et modifiers Ainu/Hokkaido | non localement | non dedie | oui | ne pas copier, laisser vanilla |
| `gov_ezo_republic`, `gov_ezo_republic_colonial` | non localement | references hotfix | vanilla attendue | risque residuel a tester |
| Localisation Hokkaido EN/FR | non dediee | absente du hotfix localise | oui | fichiers dedies crees |

Note : `.metadata/metadata.json` remplace `common/journal_entries` et `events`, mais ne remplace pas `common/scripted_buttons`, `common/scripted_effects`, `common/static_modifiers` ni `localization`.

## 5. Setup EZO/SKH/ULT/JAP verifie

| Element | Statut fork | Statut hotfix | Conflit ? | Action |
|---|---|---|---|---|
| `c:JAP` | defini, actif, conserve ses corrections Sakoku/Tenpo | present dans setup hotfix | conflit possible si import global | garder fork |
| `c:EZO` | defini, vassal du Japon, possede Hokkaido et une part de Sakhalin | reference dans Hokkaido/Sakhalin | non pour JE/events | garder fork |
| `c:SKH` | defini, possede une part de Sakhalin | reference dans hotfix states | risque si import states/countries global | garder fork |
| `c:ULT` | defini, possede une part de Sakhalin | reference dans hotfix states | risque si import states/countries global | garder fork |
| `STATE_HOKKAIDO` | EZO majoritaire, JAP enclave | tres proche du hotfix | non pour JE/events | garder fork |
| `STATE_SAKHALIN` | partage SKH/AIN/ULT/EZO/ALK | tres proche du hotfix | non pour JE/events | garder fork |

## 6. Comparaison states / pops / buildings

### States

| State | Owner fork | Owner hotfix | Claims fork | Claims hotfix | Risque |
|---|---|---|---|---|---|
| `STATE_SAKHALIN` | `SKH`, `AIN`, `ULT`, `EZO`, `ALK` | `SKH`, `AIN`, `ULT`, `EZO`, `ALK` | non audite dans cette phase | non audite dans cette phase | faible si non importe |
| `STATE_HOKKAIDO` | `EZO` + enclave `JAP` | `EZO` + enclave `JAP` | non audite dans cette phase | non audite dans cette phase | faible si non importe |

### Pops

| State | region_state fork | region_state hotfix | Difference notable | Risque |
|---|---|---|---|---|
| `STATE_SAKHALIN` | `SKH`, `ULT`, `EZO`, autres blocs locaux | `SKH`, `ULT`, `EZO`, autres blocs hotfix | tailles de pops differentes | moyen si importe |
| `STATE_HOKKAIDO` | `EZO`, `JAP` | `JAP`, probablement `EZO` selon blocs hotfix | hotfix ajoute plus de granularite historique | moyen si importe |

### Buildings

| State | region_state fork | region_state hotfix | Difference notable | Risque |
|---|---|---|---|---|
| `STATE_SAKHALIN` | blocs vides/legers pour `EZO`, `ALK`, `SKH`, `AIN` | ajoute au moins un `building_fishing_wharf` cote `EZO` | pourrait changer economie locale | moyen |
| `STATE_HOKKAIDO` | `EZO` vide, `JAP` avec wheat farm/fishing wharf | `EZO` et `JAP` avec fishing wharves et PM differentes | risque d'ecraser l'equilibre 1776 | moyen |

Conclusion : les fichiers states/pops/buildings du hotfix ne sont pas importes dans cette phase.

## 7. Fichiers modifies

| Fichier | Type | Modification |
|---|---|---|
| `common/journal_entries/07_hokkaido.txt` | nouveau | Import du bloc `je_taming_the_north` depuis le hotfix |
| `events/japan_events/ep2_hokkaido_events.txt` | nouveau | Import des evenements `hokkaido_events.1` a `.8` depuis le hotfix |
| `localization/english/hotfix_hokkaido_l_english.yml` | nouveau | Localisation anglaise Hokkaido extraite de la vanilla avec ajout des variantes EZO hotfix |
| `localization/french/hotfix_hokkaido_l_french.yml` | nouveau | Localisation francaise Hokkaido extraite de la vanilla avec ajout des variantes EZO hotfix |
| `docs/reports/hotfix/HOTFIX_4B_HOKKAIDO_EZO_SAKHALIN.md` | nouveau | Rapport de phase |

## 8. Ce qui n'a pas ete importe

- Aucun fichier `common/history/states/*`.
- Aucun fichier `common/history/pops/*`.
- Aucun fichier `common/history/buildings/*`.
- Aucun fichier `common/history/countries/*`.
- Aucun fichier `common/country_definitions/*`.
- Aucun hook dans `common/on_actions/00_code_on_actions.txt`.
- Aucun contenu Iwakura.
- Aucun contenu Zaibatsu.
- Aucun contenu Ryukyu.
- Aucun contenu Tenpo.
- Aucun contenu Sakoku.

## 9. Risques restants

- `je_taming_the_north` est gatee par `has_dlc_feature = ep2_content`; elle ne doit apparaitre que si le DLC/feature The Great Wave est disponible.
- La variante EZO de la journal entry teste `gov_ezo_republic` ou `gov_ezo_republic_colonial`. Le fichier pays actuel d'EZO utilise des lois republicaines, mais cette phase ne modifie pas les government types. A tester en jeu.
- Les boutons Hokkaido viennent de la vanilla. Si un futur changement ajoute un `replace_path` sur `common/scripted_buttons` ou `common/scripted_effects`, il faudra importer ces dependances aussi.
- Les events peuvent modifier Hokkaido/Sakhalin via variables, modifiers, arable land et buildings dynamiques quand la JE progresse. C'est le comportement vanilla/hotfix attendu, mais a tester avec le setup 1776.
- Les fichiers states/pops/buildings hotfix n'ont pas ete importes ; les differences economiques/locales restent donc celles du fork.

## 10. Tests a faire en jeu

1. Lancer avec The Great Wave actif et verifier qu'aucun crash ne se produit au chargement.
2. Demarrer en `JAP` et verifier si `Apprivoiser le nord` apparait uniquement lorsque les conditions sont remplies.
3. Verifier qu'aucune cle brute `je_taming_the_north`, `hokkaido_events.*` ou `button_je_taming_the_north_*` n'apparait en francais.
4. Tester une progression minimale de la JE : bouton colonies, bouton college agricole, puis evenements associes.
5. Observer Hokkaido/Sakhalin plusieurs mois et verifier qu'aucune province grise ne reapparait.
6. Surveiller `error.log` avec les patterns `je_taming_the_north`, `hokkaido_events`, `gov_ezo_republic`, `STATE_HOKKAIDO`, `STATE_SAKHALIN`.

## 11. Liste exacte des fichiers crees/modifies

- `common/journal_entries/07_hokkaido.txt`
- `events/japan_events/ep2_hokkaido_events.txt`
- `localization/english/hotfix_hokkaido_l_english.yml`
- `localization/french/hotfix_hokkaido_l_french.yml`
- `docs/reports/hotfix/HOTFIX_4B_HOKKAIDO_EZO_SAKHALIN.md`

## 12. Confirmations

- Pas de Ryukyu modifie.
- Pas d'Iwakura importe.
- Pas de Zaibatsu importe.
- Pas de Tenpo modifie.
- Pas de Sakoku modifie.
- Pas de suppression de `SKH`, `ULT` ou `EZO`.
- Pas de NAVY modifie.
- Pas d'ADMIN modifie.
- Pas d'IR1 / HOTFIX-3 modifie.
- Pas de BIC modifie.
- Stash MARATH non touche.
- Aucun commit effectue.
