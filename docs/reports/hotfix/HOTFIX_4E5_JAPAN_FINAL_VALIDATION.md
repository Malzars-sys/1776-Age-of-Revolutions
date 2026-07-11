# HOTFIX-4E5 - Validation finale Japon 1776

## 1. Resume executif

La validation statique confirme que le coeur Japon 1776 est coherent : JAP commence avec Sakoku, Tenpo n'est pas lance au jour 1, la chaine locale `phase1_japan_tenpo` reste l'unique chemin d'entree vers `tenpo_events.1`, et le pont Opium Wars possede exactement un caller vers `tenpo_events.6`.

Ryukyu Rivalry, Hokkaido/Ezo et Zaibatsu possedent chacun une seule JE et leurs suites d'evenements attendues. Ryukyu reste tributaire de JAP. Les tags EZO, SKH et ULT et leurs fichiers d'historique sont toujours presents. Iwakura est bien absent du runtime et reste volontairement reporte.

La validation finale est toutefois **bloquee avant validation complete en jeu** par trois dettes techniques :

1. `localization/english/hotfix_ryukyu_rivalry_l_english.yml` contient 48 cles sans indentation, contrairement au format localisation Victoria 3 ;
2. `gov_ezo_republic` et `gov_ezo_republic_colonial` sont testes dans `07_hokkaido.txt`, mais aucune definition ni localisation n'a ete trouvee dans le fork, le hotfix ou la vanilla locale ;
3. `japan_emperor_restored` est lu par `je_sakoku`, mais n'est pose par aucun script runtime du fork actuel.

Ces constats ne justifient aucune correction automatique dans cette phase de validation.

## 2. Etat Git

| Element | Resultat |
|---|---|
| Branche | `hotfix-dlc-audit` |
| Working tree initial | Propre |
| HEAD initial | `0552e8c Restore Opium Wars Tenpo bridge` |
| Stash | `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` |
| Action sur le stash | Aucune |

## 3. References uniques

| Identifiant | Definitions | Callers ou points d'ajout | Statut | Risque |
|---|---:|---:|---|---|
| `je_tenpo_crisis` | 1 dans `07_tenpo_crisis.txt` | 2 effets d'ajout dans le meme chemin : `phase1_japan_tenpo.6`, puis affichage de l'effet dans `tenpo_events.1` | Valide, pas de chemin concurrent | Faible |
| `tenpo_events.1` | 1 | 1 caller dans `phase1_japan_tenpo.6` | Valide | Faible |
| `phase1_japan_tenpo_crisis_started_from_1776_mod` | Variable locale | 1 ecriture, 2 gardes | Valide | Faible |
| `je_sakoku` | 1 | 1 ajout dans l'historique JAP | Valide | Faible |
| `je_ryukyu_rivalry` | 1 | Ajout contextless depuis `ryukyu_rivalry.8` | Valide | Faible |
| `ryukyu_rivalry_coin_toss` | 1 definition vanilla dans `00_on_actions_yearly.txt` | 1 hook local dans `00_code_on_actions.txt` | Valide, sans doublon charge du meme hook | Faible |
| `je_taming_the_north` | 1 | Ajouts conditionnels dans `hokkaido_events.1` | Valide sous reserve des gouvernements Ezo | Moyen |
| `je_zaibatsu` | 1 | Activation par ses conditions de JE | Valide | Faible |
| `tenpo_events.6` | 1 | 1 caller dans `opium_wars.4` | Valide | Faible |
| `je_sakoku_maybe_we_should_open_up` | Variable locale | 2 chemins legitimes : Morrison C et `tenpo_events.6.after` | Valide, chaque chemin est garde | Faible |

Le motif litteral sur une seule ligne `add_journal_entry = { type = je_tenpo_crisis }` retourne zero parce que les deux effets sont ecrits sur plusieurs lignes. La recherche structurelle retrouve bien les deux occurrences de `type = je_tenpo_crisis` decrites ci-dessus.

## 4. Validation Tenpo 1776

| Controle | Resultat | Fichier | Conforme ? |
|---|---|---|---:|
| Aucun ajout de `je_tenpo_crisis` dans JAP | Seule `je_sakoku` est ajoutee | `common/history/countries/jap - japan.txt` | Oui |
| Aucun `tenpo_events.1` au demarrage | Aucun caller dans l'historique JAP ou `00_code_on_actions.txt` | Historique JAP / on_actions global | Oui |
| Aucun `tenpo_gdp_goal` au chargement | Une seule initialisation trouvee, dans `phase1_japan_tenpo.6` | `events/phase1_japan_tenpo_events.txt` | Oui |
| Lancement local present | `phase1_japan_tenpo.6` ajoute la JE et appelle `tenpo_events.1` | meme fichier | Oui |
| Fenetre historique | `game_date >= 1833.1.1` et `< 1836.1.1` | evenement et on_action locaux | Oui |
| Garde anti-double | Variable locale plus `NOT has_journal_entry = je_tenpo_crisis` | evenement et on_action locaux | Oui |
| On_action local | `on_yearly_pulse` appelle `phase1_japan_tenpo.6` sous les memes gardes | `phase1_japan_tenpo_on_actions.txt` | Oui |

Conclusion Tenpo : la chaine locale est le seul caller de `tenpo_events.1`. Le bloc Opium Wars appelle uniquement `tenpo_events.6` apres 1836 et ne constitue pas un second demarrage de la JE Tenpo.

## 5. Validation Sakoku

| Element Sakoku | Resultat | Conforme ? |
|---|---|---:|
| Sakoku actif au depart | `law_sakoku` activee et `je_sakoku` ajoutee dans JAP | Oui |
| Tooltips locaux | 3 cles `je_sakoku_no_*_law_tt` conservees | Oui |
| AI chances HOTFIX-4E1 | Exactement 3 blocs `base = 10` dans `ep2_sakoku.2` | Oui |
| Relation Morrison | 1 scope protege `scope:morrison_incident_country ?=` | Oui |
| Morrison C visible | `custom_tooltip` et `show_as_unavailable` presents | Oui |
| Seuil Morrison C | Une comparaison stricte `value < neutral` | Oui |
| Cle Morrison EN/FR | Une definition dans chaque langue | Oui |
| Modifier d'opposition | `caved_to_foreign_pressure_opposition` conserve | Oui |
| Effet commun de sortie | Une occurrence de `forced_transition_from_tradition` dans un seul `after` | Oui |
| Decroissance | Une occurrence `is_decaying = yes` dans cet effet | Oui |
| Effet Meiji non voulu | `modifier_ended_sakoku_movement` absent | Oui |
| Restauration imperiale | `japan_emperor_restored` est lu mais jamais pose localement | Non, dette Meiji |

La dette `japan_emperor_restored` ne provoque pas le demarrage premature de Sakoku ou Tenpo. Elle peut en revanche rendre inoperante la branche d'echec de Sakoku fondee sur la restauration de l'empereur tant que Meiji/Iwakura reste sur l'ancienne architecture locale.

## 6. Validation Opium Wars / Tenpo

| Controle | Resultat | Conforme ? |
|---|---|---:|
| Nombre de callers locaux de `tenpo_events.6` | 1 | Oui |
| Emplacement | `opium_wars.4.immediate` | Oui |
| Scope JAP | `c:JAP ?=` | Oui |
| Pays vaincu | `opium_wars_defeated_country ?= c:CHI` | Oui |
| Victoire GBR / libre-echange | Vainqueur de port `GBR` ou CHI en libre-echange | Oui |
| Garde chronologique | `year >= 1836` conserve dans `opium_wars.1` | Oui |
| Trigger prudent de l'evenement | `exists = c:CHI` et `exists = c:GBR` | Oui |
| Variable dans les options A/B/C | 0 occurrence | Oui |
| Variable dans `after` | 1 occurrence | Oui |
| Garde anti-double | `NOT has_variable = je_sakoku_maybe_we_should_open_up` | Oui |

## 7. Validation Ryukyu

| Controle | Resultat | Conforme ? |
|---|---|---:|
| `je_ryukyu_rivalry` | 1 definition | Oui |
| Evenements | `ryukyu_rivalry.1` a `.8`, soit 8 definitions | Oui |
| Coin toss | 1 definition vanilla et 1 hook local | Oui |
| Localisations dediees | EN et FR presentes, BOM correct | Partiel |
| Setup pays | Le commit HOTFIX-4A n'a modifie aucun fichier RYU/JAP/CHI | Oui |
| Statut RYU | Pacte `JAP -> RYU`, type `tributary` | Oui |

Le fichier francais contient 95 cles correctement indentees. Le fichier anglais contient les memes 95 entrees, mais 48 d'entre elles commencent en colonne 1 au lieu d'avoir l'indentation localisation requise. Ryukyu est donc valide cote gameplay, mais sa localisation anglaise doit etre consideree bloquante pour une validation multilingue complete.

## 8. Validation Hokkaido / Ezo

| Controle | Resultat | Conforme ? |
|---|---|---:|
| `je_taming_the_north` | 1 definition | Oui |
| Evenements | `hokkaido_events.1` a `.8`, soit 8 definitions | Oui |
| Localisations | EN et FR presentes, 103 cles chacune, BOM et indentation corrects | Oui |
| Boutons JE | Les 5 boutons appeles sont fournis par la vanilla non masquee | Oui |
| States / pops / buildings HOTFIX-4B | Aucun de ces fichiers dans le commit `e5b3aea` | Oui |
| Tags | EZO, SKH et ULT definis dans `00_countries.txt` | Oui |
| Historiques pays | Les 3 fichiers EZO/SKH/ULT existent | Oui |
| Ownership local | Les trois tags restent references dans `00_states.txt` | Oui |
| Gouvernements Ezo | Deux identifiants testes, aucune definition/localisation trouvee | A verifier |

`gov_ezo_republic` et `gov_ezo_republic_colonial` apparaissent uniquement dans `common/journal_entries/07_hokkaido.txt`. La recherche dans le fork, le hotfix et la vanilla locale ne trouve aucune declaration ni localisation correspondante. Cette condition peut etre un identifiant dynamique non documente, mais elle doit etre verifiee dans `error.log` et en jeu avant de declarer Hokkaido totalement valide.

## 9. Validation Zaibatsu

| Controle | Resultat | Conforme ? |
|---|---|---:|
| `je_zaibatsu` | 1 definition | Oui |
| Evenements | `zaibatsu.1` et `.2`, soit 2 definitions | Oui |
| Localisations | EN et FR presentes, 51 cles chacune, BOM et indentation corrects | Oui |
| `company_is_zaibatsu` | Fourni par `00_ep2_victoria_scripted_triggers.txt` vanilla | Oui |
| `je_zaibatsu_companies_sgui` | Fourni par `journal_entry_sguis.txt` vanilla | Oui |
| On_action global | Aucun fichier on_action dans le commit Zaibatsu | Oui |
| Pays / states / pops / buildings | Aucun fichier de ces domaines dans le commit Zaibatsu | Oui |

Les repertoires vanilla qui fournissent les scripted triggers, script values et scripted GUIs ne sont pas remplaces par le mod. Les dependances Zaibatsu restent donc chargees.

## 10. Iwakura volontairement reporte

| Controle | Resultat | Conforme ? |
|---|---|---:|
| `common/journal_entries/07_iwakura_mission.txt` | Absent | Oui |
| `events/japan_events/ep2_iwakura_events.txt` | Absent | Oui |
| Bouton dans `00_meiji_restoration.txt` | Absent | Oui |
| Caller runtime `iwakura_mission` | Aucun dans `common`, `events` ou `localization` | Oui |
| Rapport HOTFIX-4C | Present | Oui |

Iwakura n'est pas une erreur de merge. Son absence est la decision documentee dans HOTFIX-4C, car son activation exige une future fusion manuelle du setup Meiji.

## 11. Validation des localisations

| Fichier | BOM | En-tete | Cles | Doublons dans le fork | Indentation | Cle brute evidente |
|---|---|---|---:|---:|---|---|
| `hotfix_ryukyu_rivalry_l_english.yml` | Oui | `l_english:` | 95 | 0 | **48 cles invalides** | Aucune valeur egale a sa cle, mais risque de cles brutes |
| `hotfix_ryukyu_rivalry_l_french.yml` | Oui | `l_french:` | 95 | 0 | Valide | Non |
| `hotfix_hokkaido_l_english.yml` | Oui | `l_english:` | 103 | 0 | Valide | Non |
| `hotfix_hokkaido_l_french.yml` | Oui | `l_french:` | 103 | 0 | Valide | Non |
| `hotfix_zaibatsu_l_english.yml` | Oui | `l_english:` | 51 | 0 | Valide | Non |
| `hotfix_zaibatsu_l_french.yml` | Oui | `l_french:` | 51 | 0 | Valide | Non |
| `hotfix_sakoku_morrison_l_english.yml` | Oui | `l_english:` | 1 | 0 | Valide | Non |
| `hotfix_sakoku_morrison_l_french.yml` | Oui | `l_french:` | 1 | 0 | Valide | Non |

Les lignes vides et commentaires du fichier anglais Ryukyu ne sont pas en eux-memes invalides. Le blocage concerne les 48 lignes de cles sans espace initial.

## 12. References invalides ou dettes techniques

| Reference | Classement | Justification |
|---|---|---|
| `government_ig_dislikes_sakoku_tt` | Valide | Une reference evenement, une localisation EN et une FR. |
| `modifier_ended_sakoku_movement` | Valide par absence | Aucun import ni reference runtime. |
| `japan_emperor_restored` | Potentiellement invalide | Une lecture dans Sakoku, aucune ecriture locale trouvee. |
| `iwakura_mission` | Volontairement reporte | Aucun runtime importe ; seulement le rapport HOTFIX-4C. |
| `gov_ezo_republic` | Potentiellement invalide | Teste dans la JE Hokkaido, aucune definition/localisation trouvee. |
| `gov_ezo_republic_colonial` | Potentiellement invalide | Meme constat. |
| `je_ryukyu_rivalry` | Valide | Une definition et huit evenements associes. |
| `je_taming_the_north` | Valide avec reserve | Une definition, huit evenements, boutons vanilla disponibles. |
| `je_zaibatsu` | Valide | Une definition, deux evenements et dependances vanilla disponibles. |
| `tenpo_events.6` | Valide | Une definition et exactement un caller. |
| `opium_wars_defeated_country` | Valide | Un `save_scope_as` et une utilisation dans le meme `immediate`. |

## 13. Import massif

Aucun fichier global Japon du hotfix n'a ete remplace en masse pendant HOTFIX-4A a 4E4.

- Ryukyu, Hokkaido et Zaibatsu ont ajoute leurs fichiers JE/evenements dedies.
- HOTFIX-4A a ajoute un seul hook dans `00_code_on_actions.txt`.
- HOTFIX-4E1 a 4E4 ont applique des hunks limites dans les fichiers existants.
- Aucun historique JAP, state, pop ou building n'a ete remplace par les versions hotfix pendant ces phases.
- Iwakura et la nouvelle architecture Meiji n'ont pas ete importes.

## 14. Tests manuels a faire en jeu

1. Lancer JAP au 1er janvier 1776 : Sakoku presente, Tenpo absente.
2. Passer le premier jour, le premier mois et la premiere annee sans popup Tenpo.
3. Tester les jalons locaux 1787, 1789, 1825, 1832 et 1833-1835.
4. Verifier une seule creation de la JE Tenpo et un seul `tenpo_events.1`.
5. Tester les trois options de sortie Sakoku et la decroissance de `forced_transition_from_tradition`.
6. Tester Morrison C en francais et en anglais.
7. Resoudre une guerre de l'opium CHI/GBR apres 1836 et confirmer un seul `tenpo_events.6`.
8. Tester Ryukyu Rivalry, notamment le coin toss annuel, les huit evenements et le statut tributaire initial.
9. Lancer le jeu en anglais et relever les cles brutes Ryukyu attendues en raison de l'indentation.
10. Tester l'activation de `je_taming_the_north` avec les variantes de gouvernement Ezo et surveiller les deux identifiants `gov_ezo_*`.
11. Tester Zaibatsu et son panneau de compagnies.
12. Confirmer qu'aucun bouton ou JE Iwakura n'apparait.
13. Surveiller `error.log` pour `japan_emperor_restored`, `gov_ezo_republic`, `gov_ezo_republic_colonial`, `ryukyu_rivalry`, `je_taming_the_north`, `je_zaibatsu`, `tenpo_events.6`, `invalid scope`, `unknown trigger` et `localization`.

## 15. Conclusion

**Bloc Japon structurellement coherent, mais validation finale bloquee.**

Le demarrage 1776, Sakoku, le lancement differe de Tenpo, le pont Opium Wars et Zaibatsu passent la validation statique. Ryukyu passe la validation gameplay mais echoue sur la forme de sa localisation anglaise. Hokkaido/Ezo reste en attente d'une verification des deux identifiants de gouvernement. La dette `japan_emperor_restored` doit etre resolue dans la future phase Meiji/Iwakura, pas dans cette validation.

La prochaine correction minimale recommandee est une phase de localisation seule pour indenter les 48 cles anglaises Ryukyu, suivie d'un diagnostic cible des gouvernements Ezo. Aucun de ces correctifs n'est effectue ici.

## 16. Fichier cree

- `docs/reports/hotfix/HOTFIX_4E5_JAPAN_FINAL_VALIDATION.md`

## 17. Confirmation de perimetre

- Aucun fichier gameplay n'a ete modifie.
- Aucun fichier de localisation n'a ete modifie.
- Aucun fichier hotfix n'a ete copie.
- Aucun merge automatique n'a ete effectue.
- Aucun commit n'a ete cree.
- Le stash MARATH n'a pas ete applique, restaure ou modifie.
