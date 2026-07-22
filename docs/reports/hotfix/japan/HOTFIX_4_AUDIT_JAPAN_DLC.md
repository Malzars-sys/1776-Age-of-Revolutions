# HOTFIX-4-AUDIT - Japon DLC / Sakoku / Tenpo / Ryukyu / Hokkaido

## 1. Resume executif

Audit uniquement, sans import ni modification gameplay.

Le hotfix upstream contient bien un paquet Japon DLC plus large que la seule correction de carte annoncee dans son changelog. Il apporte ou expose des blocs Ryukyu Rivalry, Hokkaido/Ezo, Iwakura Mission, Zaibatsu, Sakoku et Tenpo. En revanche, ces blocs ne sont pas autonomes dans le dossier hotfix : plusieurs dependances existent dans la vanilla The Great Wave mais pas dans le hotfix ni dans le fork actuel.

Conclusion principale : ne pas importer le bloc Japon du hotfix en masse. Le fork contient deja des corrections locales importantes pour le depart 1776, notamment Sakhalin/SKH, ULT, Ezo, Ryukyu, Sakoku lisible en francais, et une chaine Tenpo locale differee. Les apports hotfix utiles doivent etre traites en petites phases manuelles.

## 2. Etat Git initial

| Element | Valeur |
|---|---|
| Branche | `hotfix-dlc-audit` |
| `git status --short` initial | propre |
| Dernier commit | `a24fe7e Set Mamluk Iraq AI secret goal` |
| Stash detecte | `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` |
| Action sur stash | aucune |

Le stash MARATH a ete detecte mais n'a pas ete applique, lu comme source de verite, ni modifie.

## 3. Changelog hotfix Japon

Ligne pertinente trouvee dans `Changelog.txt` du hotfix :

```text
Fixed missing piece of Japan's map
```

Le changelog annonce une correction de carte Japon, mais l'arborescence du hotfix contient aussi des fichiers DLC Japon plus larges : Ryukyu Rivalry, Hokkaido, Iwakura, Zaibatsu, Sakoku, Tenpo et evenements Japon.

## 4. Fichiers candidats trouves

| Fichier hotfix | Domaine | Termes trouves | Role probable | A comparer ? |
|---|---|---|---|---|
| `common/history/countries/jap - japan.txt` | pays | JAP, ryukyu, sakoku, tenpo | setup pays Japon, lois, JE initiales | oui |
| `common/history/countries/ezo - ezochi.txt` | pays | EZO | setup Ezo/Hokkaido | oui |
| `common/history/countries/ryu - ryukyu.txt` | pays | RYU, ryukyu | setup Ryukyu | oui |
| `common/history/states/00_states.txt` | states | EZO, HOKKAIDO, RYU, JAP | ownership Est-Asie / carte | oui |
| `common/history/buildings/11_east_asia.txt` | batiments | EZO, HOKKAIDO, JAP, RYU | batiments Japon/Ezo/Ryukyu | oui |
| `common/history/pops/11_east_asia.txt` | pops | EZO, HOKKAIDO, JAP, RYU | populations Japon/Ezo/Ryukyu | oui |
| `common/history/diplomacy/00_subject_relationships.txt` | diplomatie | EZO, JAP, RYU | sujets/protectorats/tributaires | oui |
| `common/journal_entries/01_ryukyu_rivalry.txt` | JE | JAP, RYU, ryukyu | Rivalite Ryukyu | oui |
| `common/journal_entries/07_hokkaido.txt` | JE | EZO, HOKKAIDO, JAP | Taming the North / Hokkaido | oui |
| `common/journal_entries/07_iwakura_mission.txt` | JE | iwakura, japan | mission Iwakura | oui |
| `common/journal_entries/07_zaibatsu.txt` | JE | zaibatsu, JAP | Zaibatsu | oui |
| `common/journal_entries/07_sakoku.txt` | JE | sakoku, japan | The Locked Country | oui |
| `common/journal_entries/07_tenpo_crisis.txt` | JE | tenpo, tokugawa | crise Tenpo | oui |
| `common/on_actions/00_code_on_actions.txt` | on_actions | ryukyu, sakoku, tenpo, HOKKAIDO | declencheurs globaux | oui, tres risque |
| `events/japan_events/ep2_sakoku_events.txt` | events | sakoku | resolution Sakoku | oui |
| `events/japan_events/ep2_tenpo_events.txt` | events | tenpo, sakoku | crise Tenpo et lien Sakoku | oui |
| `events/japan_events/ryukyu_rivalry_events.txt` | events | RYU, ryukyu | evenements rivalite Ryukyu | oui |
| `events/japan_events/ep2_hokkaido_events.txt` | events | HOKKAIDO, EZO | evenements Hokkaido/Ezo | oui |
| `events/japan_events/ep2_iwakura_events.txt` | events | iwakura | mission Iwakura | oui |
| `events/japan_events/ep2_zaibatsu_events.txt` | events | zaibatsu | evenements Zaibatsu | oui |
| `localization/english/country_flavor_text_l_english.yml` | localisation | Japan | flavor Japon seulement cote hotfix | secondaire |

## 5. Comparaison des fichiers sensibles

| Fichier | Existe fork ? | Existe hotfix ? | Diff notable ? | Chevauche correction locale ? | Risque |
|---|---:|---:|---|---|---|
| `common/history/countries/jap - japan.txt` | oui | oui | different : lois et JE initiales differentes | oui, depart 1776 Japon | eleve |
| `common/history/countries/ezo - ezochi.txt` | oui | oui | different mineur | oui, Ezo local | moyen |
| `common/history/countries/ryu - ryukyu.txt` | oui | oui | different mineur | oui, Ryukyu local tributaire | moyen |
| `common/history/countries/skh - sakhalin.txt` | oui | non | hotfix absent | oui, fix Sakhalin local | conflit probable |
| `common/history/countries/ult - ulta.txt` | oui | non | hotfix absent | oui, fix Sakhalin/Ulta local | conflit probable |
| `common/history/states/00_states.txt` | oui | oui | tres different | oui, carte Japon/Sakhalin/Australasie/IR1 | eleve |
| `common/history/states/11_east_asia.txt` | non | non | sans objet | non | faible |
| `common/history/buildings/11_east_asia.txt` | oui | oui | tres different | oui, Japon/Sakhalin/Ryukyu | eleve |
| `common/history/pops/11_east_asia.txt` | oui | oui | different | oui, Japon/Sakhalin/Ryukyu | eleve |
| `common/journal_entries/07_sakoku.txt` | oui | oui | different : fork garde tooltips propres | oui, fix affichage Sakoku | eleve |
| `common/journal_entries/07_tenpo_crisis.txt` | oui | oui | identique | oui, JE deja couverte | faible |
| `common/journal_entries/01_ryukyu_rivalry.txt` | non | oui | nouveau hotfix | non direct, mais dependances manquantes | moyen |
| `common/journal_entries/07_hokkaido.txt` | non | oui | nouveau hotfix | oui, Hokkaido/Ezo/Sakhalin local | eleve |
| `common/journal_entries/07_iwakura_mission.txt` | non | oui | nouveau, identique vanilla | non direct | moyen |
| `common/journal_entries/07_zaibatsu.txt` | non | oui | nouveau, identique vanilla | non direct | moyen |
| `events/phase1_japan_tenpo_events.txt` | oui | non | local uniquement | oui, chaine Tenpo 1776 | eleve si ecrase |
| `events/japan_events/ep2_tenpo_events.txt` | oui | oui | different | oui, lien Tenpo/Sakoku local | eleve |
| `events/japan_events/ep2_sakoku_events.txt` | oui | oui | different | oui, fix Sakoku | eleve |
| `events/japan_events/ep2_hokkaido_events.txt` | non | oui | nouveau hotfix | oui, Ezo/Hokkaido | eleve |
| `events/japan_events/ep2_iwakura_events.txt` | non | oui | nouveau, identique vanilla | dependances vanilla | moyen |
| `events/japan_events/ep2_zaibatsu_events.txt` | non | oui | nouveau, identique vanilla | dependances vanilla | moyen |
| `events/japan_events/ryukyu_rivalry_events.txt` | non | oui | nouveau hotfix | Ryukyu local | moyen |
| `common/on_actions/phase1_japan_tenpo_on_actions.txt` | oui | non | local uniquement | oui, declenchement Tenpo 1776 | eleve si perdu |
| `common/on_actions/00_code_on_actions.txt` | oui | oui | tres different | oui, nombreux systemes globaux | eleve |

## 6. Apports hotfix utiles

| Apport hotfix | Fichiers necessaires | Deja couvert par fork ? | Dependances | Risque | Recommandation |
|---|---|---|---|---|---|
| Ryukyu Rivalry | `01_ryukyu_rivalry.txt`, `ryukyu_rivalry_events.txt`, relations RYU/JAP/CHI, `00_code_on_actions.txt` | non, sauf Ryukyu tributaire local | scripted buttons, progress bars, localisations `ep2_ryukyu_rivalry`, on_action yearly | moyen a eleve | audit/import dedie |
| Hokkaido / Ezo | `07_hokkaido.txt`, `ep2_hokkaido_events.txt`, EZO, states/pops/buildings Hokkaido/Sakhalin | partiellement : carte Ezo/Sakhalin corrigee | buttons Hokkaido, modifiers, Ezo events, ownership | eleve | fusion manuelle avec protections SKH/ULT |
| Iwakura | `07_iwakura_mission.txt`, `ep2_iwakura_events.txt` | non | scripted button, scripted effect `iwakura_mission_cleanup`, loc EN/FR vanilla | moyen | importer seulement avec dependances vanilla |
| Zaibatsu | `07_zaibatsu.txt`, `ep2_zaibatsu_events.txt` | non | company charter types, scripted trigger `company_is_zaibatsu`, scripted GUI, amendments/localisation | moyen a eleve | phase separee apres verification economie |
| Tenpo | `07_tenpo_crisis.txt`, `ep2_tenpo_events.txt`, `jap - japan.txt`, `00_code_on_actions.txt` | oui, partiellement et volontairement adapte 1776 | boutons Tenpo, variables locales, Sakoku | eleve | ne pas importer tel quel |
| Sakoku | `07_sakoku.txt`, `ep2_sakoku_events.txt`, loc EP2 | oui, corrige localement | scripted button, loc tooltips, laws Sakoku/Bakufu | eleve | conserver fork, fusionner seulement hunk utile si besoin |
| Autres events Japon | dossier `events/japan_events/*` | partiel | nombreux on_actions et locs EP2 | moyen | importer par sous-bloc, jamais dossier entier |

## 7. Elements locaux a preserver

| Element local | Present dans fork ? | Present dans hotfix ? | Risque si import naif | Action recommandee |
|---|---:|---:|---|---|
| Fix Japon / Sakhalin | oui | partiel | perte des provinces corrigees et retour zone grise | garder fork comme base |
| Tags `SKH` / `ULT` | oui | non comme fichiers pays hotfix | pays utilises par states mais non definis si hotfix ecrase | preserver absolument |
| Fix Ezo | oui | partiel | conflit avec Hokkaido vanilla/hotfix | fusion manuelle |
| Fix Ryukyu tributaire | oui | partiel | relation Ryukyu/Japon ecrasee ou double logique Rivalry | fusion manuelle |
| Chaine locale Tenpo 1776 | oui | non | Tenpo pourrait demarrer trop tot ou dupliquer les events | preserver, comparer hunk par hunk |
| `common/on_actions/phase1_japan_tenpo_on_actions.txt` | oui | non | perte des declenchements 1776 -> 1830 | ne pas toucher |
| `events/phase1_japan_tenpo_events.txt` | oui | non | perte de la progression historique locale | ne pas toucher |
| Tooltips/localisations FR/EN Sakoku/Tenpo | oui | vanilla disponible, hotfix pauvre | retour des conditions illisibles Sakoku | preserver |
| Ownership provinces grises | oui | partiel | regression carte Japon/Sakhalin/Ryukyu | garder fork comme reference |
| Sakoku compatible The Great Wave | oui | hotfix/vanilla different | reintroduction de triggers bruts sans custom tooltips | ne pas remplacer tel quel |

## 8. Dependances par bloc

| Bloc | Dependances necessaires | Manquants dans le fork | A traduire en FR ? | Risque |
|---|---|---|---:|---|
| Ryukyu Rivalry | JE, events, scripted buttons, progress bars, on_action yearly, loc `ep2_ryukyu_rivalry`, relations RYU/JAP/CHI | buttons/progress bars, loc dediee, on_action propre | oui | moyen |
| Hokkaido/Ezo | JE, events Hokkaido/Ezo, states/pops/buildings, modifiers, buttons, loc `ep2_07` | buttons Hokkaido, events, loc complete | oui | eleve |
| Iwakura | JE, events, scripted button, scripted effect `iwakura_mission_cleanup`, variables de mission, loc `ep2_04` | scripted button/effect | oui | moyen |
| Zaibatsu | JE, events, company charter types, scripted trigger `company_is_zaibatsu`, scripted GUI, amendments, loc | company_charter_types, scripted_guis, scripted_trigger vanilla | oui | eleve |
| Sakoku | JE, events, scripted button, loc `ep2_07`, lois Sakoku/Bakufu/Closed Borders | button vanilla absent, mais le fork a deja une JE fonctionnelle | deja fait en partie | eleve si remplace |
| Tenpo | JE, events, buttons `07_japan_buttons`, on_actions, variables, loc `ep2_07` | boutons Tenpo vanilla absents, mais fork a chaine locale | deja fait en partie | eleve |

## 9. Conflits probables

- `common/history/countries/jap - japan.txt` : le hotfix ajoute/active des lois et JE au depart (`je_sakoku`, `je_tenpo_crisis`, event `tenpo_events.1`, variable Ryukyu). Cela contredit le choix local de garder Tenpo hors demarrage 1776.
- `common/history/states/00_states.txt` : fichier global deja modifie localement pour Japon/Sakhalin/Australasie/IR1. Import entier interdit.
- `common/history/buildings/11_east_asia.txt` et `common/history/pops/11_east_asia.txt` : divergences fortes sur Japon, Hokkaido, Ryukyu et Sakhalin.
- `common/journal_entries/07_sakoku.txt` : le hotfix/vanilla retire les custom tooltips locaux qui corrigent l'affichage francais des conditions.
- `events/japan_events/ep2_tenpo_events.txt` : differences autour du bouton de fin de Sakoku et des variables `je_sakoku_maybe_we_should_open_up`.
- `common/on_actions/00_code_on_actions.txt` : fichier global tres divergent, contient des ajouts sans rapport Japon et des hooks Ryukyu/Hokkaido/Tenpo. Import entier trop dangereux.

## 10. Import direct possible plus tard

Aucun import direct gameplay n'est recommande sans verifier les dependances vanilla.

Import direct potentiel apres audit dedie :

- `common/journal_entries/07_iwakura_mission.txt` et `events/japan_events/ep2_iwakura_events.txt`, seulement avec `common/scripted_buttons/07_iwakura_buttons.txt`, `common/scripted_effects/00_victoria_ep2_scripted_effects.txt` ou extraction minimale, et localisation EN/FR.
- `common/journal_entries/07_zaibatsu.txt` et `events/japan_events/ep2_zaibatsu_events.txt`, seulement apres verification des company charter types, scripted triggers, scripted GUI et amendments.

Ces fichiers sont identiques a la vanilla The Great Wave cote hotfix, mais pas autonomes.

## 11. Fusion manuelle necessaire

- `common/history/countries/jap - japan.txt`
- `common/history/countries/ezo - ezochi.txt`
- `common/history/countries/ryu - ryukyu.txt`
- `common/history/states/00_states.txt`
- `common/history/buildings/11_east_asia.txt`
- `common/history/pops/11_east_asia.txt`
- `common/history/diplomacy/00_subject_relationships.txt`
- `common/journal_entries/07_sakoku.txt`
- `events/japan_events/ep2_sakoku_events.txt`
- `events/japan_events/ep2_tenpo_events.txt`
- `common/on_actions/00_code_on_actions.txt`

Ces fichiers chevauchent des corrections locales ou sont trop globaux pour etre remplaces.

## 12. Changements a ne pas importer tels quels

- Remplacement entier de `common/history/states/00_states.txt`.
- Remplacement entier de `common/history/buildings/11_east_asia.txt`.
- Remplacement entier de `common/history/pops/11_east_asia.txt`.
- Remplacement entier de `common/on_actions/00_code_on_actions.txt`.
- Remplacement entier de `common/journal_entries/07_sakoku.txt`.
- Activation directe de `je_tenpo_crisis` au demarrage 1776 via `jap - japan.txt`.
- Suppression indirecte des fichiers locaux `SKH`, `ULT`, `phase1_japan_tenpo_events.txt`, `phase1_japan_tenpo_on_actions.txt`.

## 13. Plan d'import recommande

### HOTFIX-4A - Ryukyu Rivalry audit/import

Comparer hotfix et vanilla pour Ryukyu. Importer seulement si les dependances suivantes sont ajoutees proprement : JE, events, scripted buttons, progress bars, on_action yearly, localisations EN/FR. Verifier que Ryukyu reste tributaire du Japon au depart 1776.

### HOTFIX-4B - Hokkaido/Ezo

Auditer `07_hokkaido.txt`, `ep2_hokkaido_events.txt`, Ezo, Hokkaido, Sakhalin. Ne pas ecraser les tags `SKH` et `ULT`. Tester visuellement Hokkaido/Sakhalin et verifier les provinces grises.

### HOTFIX-4C - Iwakura/Zaibatsu

Importer en bloc separe si les dependances vanilla sont copiees/adaptees : scripted buttons, scripted effects, scripted triggers, scripted GUI, company charter types, amendments et locs.

### HOTFIX-4D - Tenpo/Sakoku fusion manuelle

Conserver la logique locale 1776. Comparer seulement les hunks utiles de `ep2_tenpo_events.txt` et `ep2_sakoku_events.txt`. Ne pas remplacer `07_sakoku.txt` sans conserver les custom tooltips locaux.

### HOTFIX-4E - Localisations FR

Importer ou adapter les fichiers vanilla FR : `ep2_07_l_french.yml`, `ep2_ryukyu_rivalry_l_french.yml`, `ep2_04_l_french.yml` et les autres fichiers requis, mais seulement les cles necessaires au contenu importe.

## 14. Risques

- Regression carte : zones blanches ou infranchissables sur Sakhalin/Hokkaido/Ryukyu si `00_states` est remplace.
- Regression Sakoku : retour des conditions illisibles si les custom tooltips locaux sont perdus.
- Double Tenpo : crise Tenpo au demarrage 1776 plus chaine locale differee.
- Dependances manquantes : scripted buttons/progress bars/effects/triggers absents si un fichier JE est importe seul.
- Localisation incomplete : jeu en francais avec cles brutes pour Ryukyu/Hokkaido/Iwakura/Zaibatsu.
- Effets globaux imprevus : `00_code_on_actions.txt` touche beaucoup de systemes non japonais.

## 15. Tests a faire en jeu

- Lancer une partie Japon au 1 janvier 1776.
- Verifier que `je_sakoku` apparait, avec conditions lisibles en francais.
- Verifier que `je_tenpo_crisis` n'apparait pas au demarrage 1776 si la logique locale est conservee.
- Verifier Ryukyu : tag present, tributaire du Japon, pas de doublon avec une future rivalite.
- Verifier Hokkaido, Sakhalin, Ezo, SKH et ULT visuellement sur la carte.
- Laisser tourner un mois, puis un an.
- Surveiller `error.log` pour `je_ryukyu_rivalry`, `je_taming_the_north`, `iwakura_mission`, `zaibatsu`, `scripted_button`, `scripted_progress_bar`, `company_is_zaibatsu`, `STATE_SAKHALIN`, `STATE_HOKKAIDO`, `RYU`, `EZO`, `SKH`, `ULT`.

## 16. Liste exacte des fichiers crees

- `docs/reports/hotfix/HOTFIX_4_AUDIT_JAPAN_DLC.md`

## 17. Confirmation

Aucun fichier gameplay n'a ete modifie pendant cette phase.

Non modifies :

- `common/history/countries/`
- `common/history/states/`
- `common/history/buildings/`
- `common/journal_entries/`
- `common/on_actions/`
- `events/`
- `localization/`
- `map_data/`
- NAVY
- ADMIN
- IR1 / HOTFIX-3
- BIC
- stash MARATH

Cette phase est un audit seulement. Aucun merge, aucune copie depuis le hotfix, aucun stash pop et aucun commit n'ont ete effectues.
