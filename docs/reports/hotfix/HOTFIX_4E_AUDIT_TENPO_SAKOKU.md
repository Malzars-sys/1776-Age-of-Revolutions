# HOTFIX-4E-AUDIT - Tenpo / Sakoku

## 1. Resume executif

Cet audit compare le fork, le hotfix upstream et la vanilla The Great Wave pour les chaines Sakoku et Tenpo. Aucun fichier gameplay n'a ete modifie.

La conclusion principale est de **conserver le declenchement local du fork** : le hotfix reprend le depart vanilla 1836 et ajoute immediatement `je_tenpo_crisis` ainsi que `tenpo_events.1` dans l'historique japonais. Applique tel quel au depart 1776, ce bloc lancerait la crise environ cinquante-sept ans trop tot et court-circuiterait toute la chaine locale differee.

La definition `je_tenpo_crisis` est strictement identique dans les trois versions. La definition locale `je_sakoku` doit egalement etre conservee, car ses trois `custom_tooltip` corrigent l'affichage francais illisible des conditions vanilla/hotfix.

Quelques corrections de `ep2_sakoku_events.txt` du hotfix paraissent utiles, mais elles doivent etre reprises hunk par hunk et testees separement. Deux ajouts du hotfix ne sont pas importables tels quels : `government_ig_dislikes_sakoku_tt` n'a ete trouve dans aucune localisation EN/FR consultee, et `modifier_ended_sakoku_movement` n'a ete trouve dans aucune definition du fork, du hotfix ou de la vanilla examinee.

Le hunk `tenpo_events.6` du hotfix est techniquement interessant, notamment parce qu'il centralise l'ouverture du bouton Sakoku dans `after`, mais l'evenement n'est actuellement appele nulle part dans le fork : son `events/opium_wars_events.txt`, qui masque la version vanilla, ne contient pas l'appel a `tenpo_events.6`. Ce travail doit donc etre reporte a une phase dediee a la guerre de l'opium.

## 2. Etat Git initial

| Element | Resultat |
|---|---|
| Branche | `hotfix-dlc-audit` |
| Working tree | Propre au debut de l'audit |
| HEAD | `ea3905e Import Zaibatsu journal content` |
| Stash | `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` |
| Action sur le stash | Aucune lecture de contenu, aucune application, aucune modification |

## 3. Replace paths pertinents

`.metadata/metadata.json` declare `events` et `common/journal_entries` dans `replace_paths`. `descriptor.mod` ne declare aucun `replace_path` supplementaire.

| Chemin | Remplace explicitement ? | Version effectivement disponible |
|---|---:|---|
| `common/journal_entries` | Oui | Seulement les fichiers du fork. Les JE vanilla absentes du fork sont masquees. |
| `events` | Oui | Seulement les fichiers du fork. Les evenements vanilla absents du fork sont masquees. |
| `common/on_actions` | Non | Les fichiers de noms differents peuvent se cumuler, mais le `00_code_on_actions.txt` local masque le fichier vanilla de meme chemin. |
| `localization` | Non | Les localisations du fork et de la vanilla restent disponibles ; une cle locale identique peut surcharger la cle vanilla. |
| `common/scripted_buttons` | Non | Les boutons vanilla restent disponibles, sauf collision de chemin. Le fork n'a pas de copie de `07_japan_buttons.txt` ni de `sakoku_buttons.txt`. |

Consequences techniques :

- `je_sakoku` et `je_tenpo_crisis` doivent exister dans le fork, ce qui est le cas.
- `ep2_sakoku_events.txt` et `ep2_tenpo_events.txt` doivent exister dans le fork, ce qui est le cas.
- Les boutons vanilla `je_sakoku_stop_being_closed_button` et les trois `button_je_tenpo_*` restent disponibles.
- Les evenements vanilla non copies dans le fork ne sont pas charges. C'est notamment important pour `japan_religion.10`.
- Le fichier local `events/opium_wars_events.txt` est charge a la place de la version vanilla et ne contient pas l'appel a `tenpo_events.6`.

## 4. Fonctionnement actuel du fork

| Mecanisme local | Fichier | Bloc ou identifiant | Role | A preserver absolument ? |
|---|---|---|---|---:|
| Lois japonaises de depart | `common/history/countries/jap - japan.txt` | `c:JAP` | Active notamment `law_bakufu`, `law_sakoku`, `law_closed_borders`, `law_terakoya` et `law_no_colonial_affairs`. | Oui |
| Activation Sakoku | meme fichier | `add_journal_entry = { type = je_sakoku }` | Ajoute Sakoku au depart 1776 sans ajouter Tenpo. | Oui |
| Conditions lisibles Sakoku | `common/journal_entries/07_sakoku.txt` | `complete` et `fail` | Encapsule les lois dans trois `custom_tooltip` locaux lisibles. | Oui |
| Bouton d'ouverture | meme fichier | `je_sakoku_stop_being_closed_button` | Rend disponible le bouton vanilla lorsque `je_sakoku_maybe_we_should_open_up` existe. | Oui |
| Incident Morrison | `events/japan_events/ep2_sakoku_events.txt` | `ep2_sakoku.3` | Peut poser `je_sakoku_maybe_we_should_open_up` via l'option C. | Oui, sous reserve de futurs hunks isoles |
| Resolution Sakoku | meme fichier | `ep2_sakoku.2`, `.4`, `.5` | Choix de la nouvelle loi commerciale puis resultats de completion/echec. | Oui |
| Lecons Tenmei | `events/phase1_japan_tenpo_events.txt` | `phase1_japan_tenpo.1` | Evenement 1787-1790, verrouille par `phase1_japan_tenmei_lessons_done`. | Oui |
| Reformes Kansei | meme fichier | `phase1_japan_tenpo.2` | Evenement 1789-1793 apres Tenmei, verrouille par `phase1_japan_kansei_reforms_done`. | Oui |
| Navires etrangers | meme fichier | `phase1_japan_tenpo.3` | Evenement 1825-1827 exigeant `law_sakoku`. | Oui |
| Mauvaises recoltes | meme fichier | `phase1_japan_tenpo.4` | Evenement 1832-1833 exigeant Bakufu et Sakoku. | Oui |
| Crise du prix du riz | meme fichier | `phase1_japan_tenpo.5` | Evenement 1833-1834 apres les mauvaises recoltes. | Oui |
| Demarrage Tenpo | meme fichier | `phase1_japan_tenpo.6` | Entre 1833 et 1835, initialise `tenpo_gdp_goal`, ajoute la JE et appelle `tenpo_events.1`. | Oui |
| Planificateur local | `common/on_actions/phase1_japan_tenpo_on_actions.txt` | `on_yearly_pulse` | Appelle les six evenements dans leurs fenetres historiques. | Oui |
| Garde anti-double | les deux fichiers locaux precedents | `phase1_japan_tenpo_crisis_started_from_1776_mod` et `NOT has_journal_entry` | Empeche un nouveau lancement par le chemin local. | Oui |
| JE Tenpo | `common/journal_entries/07_tenpo_crisis.txt` | `je_tenpo_crisis` | JE vanilla 1.13 conservee telle quelle, timeout 12 ans et boutons Tenpo. | Oui |

### Relations Sakoku / Tenpo locales

La chaine locale n'exige Sakoku que pour les jalons de 1825 et 1832. Le demarrage final de 1833 exige les deux variables de crise alimentaire, mais pas directement `law_sakoku`. Cela permet a la famine de se produire meme si le Japon s'est ouvert entre-temps.

Dans la JE Tenpo, `tenpo_events.6` peut normalement debloquer le bouton de sortie de Sakoku apres la guerre de l'opium. Toutefois, ce chemin est actuellement inactif dans le fork, car l'ancien `opium_wars_events.txt` local n'appelle pas `tenpo_events.6`.

## 5. Fonctionnement du hotfix

Le hotfix et la vanilla sont identiques pour `jap - japan.txt`, `07_sakoku.txt`, `07_tenpo_crisis.txt` et la majeure partie de la chaine Tenpo. Le hotfix est donc construit autour du depart vanilla, pas autour de 1776.

| Mecanisme hotfix | Fichier | Bloc ou identifiant | Difference avec le fork | Utilite possible | Risque |
|---|---|---|---|---|---|
| Demarrage Tenpo immediat | `common/history/countries/jap - japan.txt` | bloc DLC | Ajoute `je_tenpo_crisis`, appelle `tenpo_events.1` et ajoute de la devastation des le depart. | Aucune pour 1776 | Critique : crise immediate et double chemin |
| Objectif PIB initialise au chargement | `common/on_actions/00_code_on_actions.txt` | initialisation globale | Definit `tenpo_gdp_goal = JAP.gdp * 1.35` des le debut. | Utile uniquement au depart 1836 | Eleve : valeur obsolete en 1833 |
| Sakoku vanilla brut | `common/journal_entries/07_sakoku.txt` | `complete` / `fail` | Retire les tooltips locaux. | Aucune | Eleve : regression de l'affichage francais |
| Selection des IG pro-commerce | `ep2_sakoku.2` | `immediate` | Exige un IG au gouvernement et passe les comparaisons de `< neutral` a `> neutral`. | Correction logique probable | Moyen : change les options disponibles |
| IA des choix commerciaux | `ep2_sakoku.2` | options A/B/C | Ajoute `ai_chance = 10`. | Oui | Faible |
| Effets communs de sortie | `ep2_sakoku.2` | `after` | Mutualise `forced_transition_from_tradition`, ajoute decroissance et un modifier au mouvement Meiji. | Partiellement | Eleve : modifier Meiji introuvable |
| Relations Morrison | `ep2_sakoku.3.a` | relation | Evite le double changement bilateral et utilise un scope optionnel. | Correction probable | Faible a moyen |
| Condition option C | `ep2_sakoku.3.c` | trigger / `show_as_unavailable` | Rend la condition visible et impose une opposition stricte a l'isolation. | Oui, apres localisation | Moyen : cle de tooltip absente |
| Modifier option C | `ep2_sakoku.3.c` | opposition | Remplace `caved_to_foreign_pressure_opposition` par `light_hand_with_foreigners`. | Douteuse | Moyen : semantique moins coherente |
| Sortie Sakoku apres guerre de l'opium | `ep2_tenpo_events.txt` | `tenpo_events.6` | Mutualise le `set_variable` dans `after` et le protege contre une seconde initialisation. | Oui en principe | Inactif tant que le caller manque |
| Trigger de `tenpo_events.6` | meme fichier | `trigger` | Remplace `exists CHI/GBR` par le seul DLC. | Douteuse | Moyen : scopes CHI/GBR potentiellement absents |
| Religion apres ouverture | `common/on_actions/00_code_on_actions.txt` | `on_law_activated` | Planifie `japan_religion.10` apres 1836 si Sakoku et frontieres fermees sont tous deux termines. | Contenu futur | Bloque : evenement absent du fork |
| Variable Ryukyu | `jap - japan.txt` | bloc DLC | Pose `ryukyu_rival_member` sur JAP. | Deja gere par HOTFIX-4A | Risque de doublon |

## 6. Comparaison fork / hotfix / vanilla

| Fichier | Fork | Hotfix | Vanilla | Conclusion |
|---|---|---|---|---|
| `common/history/countries/jap - japan.txt` | Setup 1776 local | Setup vanilla 1836 | Identique hotfix | Conserver le fork |
| `common/journal_entries/07_sakoku.txt` | Vanilla adaptee avec trois tooltips locaux | Definition brute | Identique hotfix | Conserver le fork |
| `common/journal_entries/07_tenpo_crisis.txt` | 141 lignes | Identique bit a bit | Identique bit a bit | Aucun import |
| `events/japan_events/ep2_sakoku_events.txt` | Quasi vanilla | Plusieurs corrections propres au hotfix | Quasi identique au fork | Fusion manuelle par hunks |
| `events/japan_events/ep2_tenpo_events.txt` | Identique vanilla | Hunk limite a `tenpo_events.6` | Identique fork | Reporter jusqu'au caller Opium Wars |
| `common/on_actions/00_code_on_actions.txt` | Ancienne base locale | Base 1.13 hotfix | Base 1.13 proche du hotfix | Ne jamais remplacer entierement |
| `events/phase1_japan_tenpo_events.txt` | Chaine locale 1776, 6 evenements | Absent | Absent | Conserver |
| `common/on_actions/phase1_japan_tenpo_on_actions.txt` | Planificateur local 1776 | Absent | Absent | Conserver |
| `common/journal_entries/00_meiji_restoration.txt` | Ancienne version courte | Version EP2 etendue | Version EP2 etendue | Reporter a Meiji/Iwakura |

## 7. Tableau hunk par hunk

| Fichier | Bloc | Fork | Hotfix | Vanilla | Decision | Justification |
|---|---|---|---|---|---|---|
| `jap - japan.txt` | technologies et lois | Setup 1776 local | Setup 1836 EP2 | Identique hotfix | CONSERVER FORK | Hors Sakoku/Tenpo et sensible a l'equilibrage 1776. |
| `jap - japan.txt` | ajout `je_sakoku` | Sakoku seule | Sakoku sous garde DLC | Identique hotfix | CONSERVER FORK | Fonctionne deja au depart 1776. |
| `jap - japan.txt` | ajout `je_tenpo_crisis` et `tenpo_events.1` | Absent | Present au jour 1 | Identique hotfix | IGNORER | Declencherait Tenpo en 1776. |
| `jap - japan.txt` | devastation / pluies Honshu | Absent | Present au jour 1 | Identique hotfix | IGNORER | Correspond au scenario 1836, pas a 1776. |
| `jap - japan.txt` | `ryukyu_rival_member` | Gere par les fichiers Ryukyu locaux | Pose sur JAP | Identique hotfix | IGNORER | HOTFIX-4A est deja en place. |
| `07_sakoku.txt` | `complete` | Deux tooltips lisibles | `NOR` brut | Identique hotfix | CONSERVER FORK | Evite la repetition corrompue du nom du pays en francais. |
| `07_sakoku.txt` | echec monarchie | Tooltip local lisible | Trigger brut | Identique hotfix | CONSERVER FORK | Meme raison. |
| `07_sakoku.txt` | variable empereur | `japan_emperor_restored` | Identique | Identique | REPORTER A UNE PHASE MEIJI/IWAKURA | L'ancienne JE Meiji du fork ne pose pas cette variable. |
| `07_tenpo_crisis.txt` | fichier complet | Identique | Identique | Identique | IGNORER | Rien a fusionner. |
| `ep2_sakoku_events.txt` | `ep2_sakoku.2` selection IG | Stance `< neutral`, tous IG | Stance `> neutral`, IG au gouvernement | Identique fork | ADAPTER MANUELLEMENT | Le hotfix semble corriger la selection des soutiens, mais change le gameplay. Test isole necessaire. |
| meme fichier | `ep2_sakoku.2` AI chance | Aucune valeur explicite | `base = 10` sur A/B/C | Comme fork | IMPORTER LE HUNK HOTFIX | Petit hunk autonome et faible risque. |
| meme fichier | effets `forced_transition` | Dupliques dans chaque option | Mutualises dans `after`, decroissants | Comme fork | ADAPTER MANUELLEMENT | Mutualisation utile ; ne pas reprendre le modifier Meiji introuvable. |
| meme fichier | `modifier_ended_sakoku_movement` | Absent | Ajoute au mouvement Meiji | Absent | REPORTER A UNE PHASE MEIJI/IWAKURA | Definition introuvable et Iwakura volontairement non importe. |
| meme fichier | `ep2_sakoku.3.a` relations | Deux changements de relations | Un changement via scope optionnel | Comme fork | IMPORTER LE HUNK HOTFIX | Evite une penalite possiblement double et protege le scope. |
| meme fichier | `ep2_sakoku.3.c` trigger visible | Trigger cache, `<= neutral` | Tooltip visible, `< neutral`, `show_as_unavailable` | Comme fork | ADAPTER MANUELLEMENT | Ajouter d'abord une cle EN/FR locale ; la cle hotfix est absente. |
| meme fichier | modifier opposition option C | `caved_to_foreign_pressure_opposition` | `light_hand_with_foreigners` | Comme fork | CONSERVER FORK | Le nom local/vanilla correspond mieux a la pression etrangere. |
| `ep2_tenpo_events.txt` | trigger `tenpo_events.6` | Exige CHI et GBR | Exige seulement EP2 | Comme fork | CONSERVER FORK | Les scopes CHI/GBR sont utilises dans l'evenement ; leur existence est une garde prudente. |
| meme fichier | ouverture Sakoku dans A/B/C | Effet duplique dans chaque option | Un seul `after`, garde anti-double | Comme fork | ADAPTER MANUELLEMENT | Bonne simplification, mais evenement actuellement sans caller dans le fork. |
| `00_code_on_actions.txt` | `tenpo_gdp_goal` au demarrage | Absent | Initialise au jour 1 | Identique hotfix | IGNORER | Le fork calcule l'objectif au vrai demarrage de la crise en 1833. |
| meme fichier | `japan_religion.10` | Hook absent | Hook apres ouverture | Identique hotfix | REPORTER A UNE PHASE MEIJI/IWAKURA | L'evenement cible est masque et absent du fork. |
| `00_meiji_restoration.txt` | variables de restauration | Ancienne architecture | `japan_emperor_restored` et architecture EP2 | Proche hotfix | REPORTER A UNE PHASE MEIJI/IWAKURA | Fusion globale necessaire, hors scope et deja volontairement reportee. |

## 8. Dependances techniques

| Dependance | Etat dans le fork | Provenance chargee | Observation |
|---|---|---|---|
| `je_sakoku_stop_being_closed_button` | Disponible | Vanilla `common/scripted_buttons/sakoku_buttons.txt` | `common/scripted_buttons` n'est pas remplace. |
| `button_je_tenpo_combat_rice_hoarding` | Disponible | Vanilla `07_japan_buttons.txt` | Appele par la JE locale. |
| `button_je_tenpo_frugal_ordinance` | Disponible | Vanilla | Appele par la JE locale. |
| `button_je_tenpo_confiscate_land` | Disponible | Vanilla | Appele par la JE locale. |
| `je_sakoku_maybe_we_should_open_up` | Utilisee | Events Sakoku et Tenpo du fork | Retiree par `ep2_sakoku.2`, posee par Morrison C ou `tenpo_events.6`. |
| `tenpo_gdp_goal` | Initialise tardivement | `phase1_japan_tenpo.6` | Valeur calculee au moment pertinent, pas en 1776. |
| `phase1_japan_tenpo_crisis_started_from_1776_mod` | Disponible | Chaine locale | Garde principale anti-double. |
| `japan_emperor_restored` | Lue mais non initialisee par la JE Meiji locale | `07_sakoku.txt` / ancienne `00_meiji_restoration.txt` | Dette technique Meiji. |
| `government_ig_dislikes_sakoku_tt` | Absente | Aucune loc EN/FR trouvee | Ne pas importer le hunk sans creer la localisation. |
| `modifier_ended_sakoku_movement` | Definition introuvable | Reference hotfix uniquement | Ne pas importer. |
| `tenpo_events.6` caller | Absent | Ancien `events/opium_wars_events.txt` du fork | L'evenement existe mais n'est pas declenche par la guerre de l'opium. |
| `japan_religion.10` | Absent | Masque par `replace_path = events` | Le hook hotfix serait invalide s'il etait importe seul. |

## 9. Risques de double declenchement

| Risque de doublon | Cause possible | Present actuellement ? | Consequence | Prevention |
|---|---|---:|---|---|
| Tenpo des 1776 | Import du bloc hotfix dans `jap - japan.txt` | Non | JE et event hors periode | Ne jamais importer ce bloc. |
| Tenpo lance par deux chemins | Bloc historique hotfix plus `phase1_japan_tenpo.6` | Non | Deux initialisations et deux ouvertures possibles | Conserver uniquement la chaine locale. |
| `tenpo_events.1` lance deux fois | Appel historique et appel local | Non | Radicaux et popup dupliques | Un seul caller local ; cooldown de l'event en garde secondaire. |
| `tenpo_gdp_goal` initialise deux fois | `00_code_on_actions` hotfix plus event local | Non | Objectif calcule sur le PIB 1776 puis ecrase en 1833 | Ignorer l'initialisation hotfix. |
| `je_sakoku_maybe_we_should_open_up` pose plusieurs fois | Chaque option de `tenpo_events.6` ou Morrison | Possible mais sans caller Tenpo actuel | Tooltip repete, variable deja existante | Future mutualisation dans `after` avec `NOT has_variable`. |
| Sakoku termine a tort | Remplacement des tooltips par triggers mal affiches | Non fonctionnellement, mais regression UI possible | Conditions incomprehensibles | Conserver `07_sakoku.txt` local. |
| Sakoku ne detecte pas l'empereur | `japan_emperor_restored` jamais posee par l'ancienne Meiji | Oui, dette potentielle | Echec Sakoku incomplet si la monarchie reste active | Corriger uniquement dans une phase Meiji. |
| Ryukyu initialise deux fois | Import de `set_variable = ryukyu_rival_member` hotfix | Non | Etat de rivalite ambigu | Conserver HOTFIX-4A sans bloc JAP hotfix. |
| Iwakura devient accessible | Import de la nouvelle `00_meiji_restoration.txt` | Non | Active du contenu volontairement reporte | Ne pas importer Meiji dans HOTFIX-4E. |

## 10. Elements locaux a preserver

- Le setup japonais 1776 et ses lois actuelles.
- L'ajout de `je_sakoku` sans `je_tenpo_crisis` au depart.
- Les trois cles locales `je_sakoku_no_sakoku_law_tt`, `je_sakoku_no_closed_borders_law_tt` et `je_sakoku_no_monarchy_law_tt`.
- Les fichiers `events/phase1_japan_tenpo_events.txt` et `common/on_actions/phase1_japan_tenpo_on_actions.txt`.
- Les six fenetres chronologiques locales, notamment le lancement Tenpo en 1833-1835.
- Les variables de garde locales.
- Les corrections Ryukyu, Hokkaido/Ezo, Sakhalin, SKH/ULT et Zaibatsu deja presentes.

## 11. Elements hotfix utiles

- Les `ai_chance = { base = 10 }` des trois options de `ep2_sakoku.2`.
- La selection plus explicite des IG au gouvernement dans `ep2_sakoku.2`, apres validation du sens de `law_enactment_stance`.
- La mutualisation de `forced_transition_from_tradition` dans `after`, sans le modifier Meiji introuvable.
- Le changement de relations unique et scope-safe dans `ep2_sakoku.3.a`.
- Le principe d'un trigger visible et d'un `show_as_unavailable` dans `ep2_sakoku.3.c`, avec une nouvelle localisation locale obligatoire.
- Le principe de mutualiser l'ouverture Sakoku dans `tenpo_events.6.after`, mais seulement apres restauration du caller Opium Wars.

## 12. Elements hotfix a ignorer

- L'ajout immediat de `je_tenpo_crisis` et de `tenpo_events.1` au depart.
- La devastation et les pluies forcees sur Honshu au jour 1.
- L'initialisation de `tenpo_gdp_goal` au chargement de la partie.
- Le remplacement de la JE Sakoku locale par la definition brute vanilla/hotfix.
- Le remplacement global de `00_code_on_actions.txt`.
- Le trigger de `tenpo_events.6` limite au seul DLC.
- Le remplacement de `caved_to_foreign_pressure_opposition` par `light_hand_with_foreigners` dans Morrison C.
- Toute reinitialisation Ryukyu depuis le bloc historique JAP.

## 13. Elements a reporter a Meiji / Iwakura

- L'alignement de `japan_emperor_restored` entre Sakoku et la restauration Meiji.
- `modifier_ended_sakoku_movement` et le mouvement `movement_meiji_restorationist`.
- La nouvelle architecture de `je_meiji_main`, les boutons Iwakura et Edo, et les nouvelles JE Meiji.
- Le hook `japan_religion.10`, qui exige d'abord l'import controle de son fichier d'evenements et de ses localisations.
- Les annexions conditionnelles EZO du hotfix, qui chevauchent les corrections locales EZO/SKH/ULT.

## 14. Plan d'implementation futur

### HOTFIX-4E1 - Corrections isolees Sakoku

- Fichier autorise : `events/japan_events/ep2_sakoku_events.txt`.
- Hunks : `ai_chance` de `.2`, changement de relation de `.3.a`.
- Fichiers interdits : historique JAP, JE, Tenpo, on_actions, localisation.
- Tests : ouvrir le bouton Sakoku, tester les trois options commerciales, verifier les relations Morrison.
- Rollback : un commit dedie contenant un seul fichier.

### HOTFIX-4E2 - Presentation Morrison C

- Fichiers autorises : `events/japan_events/ep2_sakoku_events.txt` et deux fichiers de localisation dedies EN/FR.
- Hunks : `custom_tooltip`, comparaison `< neutral`, `show_as_unavailable`.
- Fichiers interdits : JE Sakoku et tout Meiji/Iwakura.
- Tests : option C cachee, indisponible puis disponible ; aucune cle brute en francais.
- Rollback : commit dedie evenement plus localisation.

### HOTFIX-4E3 - Effets communs de sortie Sakoku

- Fichier autorise : `events/japan_events/ep2_sakoku_events.txt`.
- Hunk : mutualisation de `forced_transition_from_tradition` dans `after` avec `is_decaying = yes`.
- Exclusion explicite : ne pas ajouter `modifier_ended_sakoku_movement`.
- Tests : chacune des trois options applique une seule fois le modifier attendu.
- Rollback : commit dedie.

### HOTFIX-4E4 - Pont Opium Wars / Tenpo

- Fichiers autorises : `events/opium_wars_events.txt` et `events/japan_events/ep2_tenpo_events.txt`.
- Hunks : caller exact de `tenpo_events.6`, puis mutualisation de `je_sakoku_maybe_we_should_open_up` dans `after`.
- Fichiers interdits : historique JAP, JE Tenpo, chaine locale 1776.
- Tests : guerre de l'opium, un seul popup, variable posee une seule fois, bouton Sakoku disponible.
- Rollback : commit dedie a deux fichiers.

### HOTFIX-4E5 - Validation Japon 1776

- Aucun nouveau hunk gameplay.
- Tester 1776, 1787, 1789, 1825, 1832, 1833 et la resolution de Sakoku/Tenpo.
- Verifier `error.log` pour `je_sakoku`, `je_tenpo_crisis`, `tenpo_events`, `ep2_sakoku`, `scripted_button`, `custom_tooltip`, `invalid scope` et `unknown modifier`.
- Confirmer que Iwakura reste inaccessible.

## 15. Tests recommandes

1. Demarrer JAP au 1er janvier 1776 : Sakoku presente, Tenpo absente.
2. Passer le premier mois et la premiere annee : aucun `tenpo_events.1` premature.
3. Tester les jalons 1787 et 1789 : une occurrence de chaque evenement local.
4. Tester 1825 avec et sans `law_sakoku`.
5. Tester 1832-1835 : une seule creation de `je_tenpo_crisis`, un seul `tenpo_events.1`, objectif PIB calcule au moment du lancement.
6. Tester les trois choix de `ep2_sakoku.2` apres chaque futur petit lot.
7. Tester l'incident Morrison et l'apparition du bouton de revocation Sakoku.
8. Tester la fin de Sakoku par les lois et son echec par changement de regime.
9. Apres une future phase Opium Wars, verifier que `tenpo_events.6` est appele exactement une fois.
10. Surveiller `error.log` pour les cles ou identifiants cites dans HOTFIX-4E5.

## 16. Fichier cree

- `docs/reports/hotfix/HOTFIX_4E_AUDIT_TENPO_SAKOKU.md`

## 17. Confirmation de perimetre

- Aucun fichier gameplay n'a ete modifie.
- Aucun fichier hotfix n'a ete copie.
- Aucun merge automatique n'a ete effectue.
- Aucune localisation n'a ete modifiee.
- Sakoku, Tenpo, Meiji, Ryukyu, Hokkaido/Ezo, Zaibatsu, Iwakura, SKH/ULT, NAVY, ADMIN, IR1, BIC et Inde n'ont subi aucune modification.
- Le stash MARATH n'a pas ete applique, restaure, inspecte comme contenu courant ou modifie.
- Aucun commit n'a ete cree.
