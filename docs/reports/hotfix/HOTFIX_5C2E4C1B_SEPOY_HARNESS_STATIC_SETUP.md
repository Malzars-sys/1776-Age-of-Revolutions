# HOTFIX-5C2E4C1B - Harnais statique Sepoy

## 1. Resume

Un harnais jetable minimal a ete cree uniquement dans
`1776_Age_of_Revolutions_sepoy_test`. Il ajoute une decision reservee au
joueur BIC et un country event informatif qui verifie de nouveau le root BIC.
L'unique effet de la decision est l'appel de cet event ; l'event ne contient
aucun effet gameplay.

Victoria 3 et le launcher n'ont pas ete lances. La validation est uniquement
statique.

**Verdict : `READY_FOR_HARNESS_RUNTIME_TEST`.**

## 2. Etat Git initial

- Racine : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`.
- Branche : `hotfix-dlc-audit`.
- HEAD : `df64bda Create disposable Sepoy test copy`.
- Le commit C1A est present.
- Aucun fichier suivi n'etait modifie.
- Stash present et non applique :
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`.

## 3. Exception docs/research/technology

Le dossier non suivi `docs/research/technology/` et ses sept fichiers
preexistaient. Il a ete exclu de la copie C1A et n'a ete ni modifie ni copie
pendant C1B.

## 4. Verification de la copie C1A

Avant creation du harnais, les quatre chemins `zz_sepoy_functional_test*`
etaient absents. La copie contenait 944 fichiers : 943 fichiers suivis copies
et le marqueur jetable.

Le manifest C1A a ete recalcule : ses 945 lignes de controle correspondent a
942 fichiers identiques, au `descriptor.mod` dont seul le nom jetable differe,
au marqueur et au descripteur launcher externe. Les 945 controles de hash et
d'existence ont reussi ; aucune difference inattendue n'a ete trouvee.

La copie ne contient ni `.git`, ni `remote_file_id`, ni fichier sous
`docs/research/technology/`.

## 5. Hashes de protection

| Controle | SHA-256 avant C1B | SHA-256 apres C1B | Resultat |
|---|---|---|---|
| Fork `common/journal_entries/04_sepoy_mutiny.txt` | `DAEFCB59CCF6B303D2E39C948D8038006C1346AFE40A2B812D45EE4D947E361C` | identique | protege |
| Copie `common/journal_entries/04_sepoy_mutiny.txt` | meme hash | meme hash | identique au fork |
| Fork `events/india_events/sepoy_mutiny_events.txt` | `557936500AC585F7F69B9F5B063BDDA377AFF4A5AFAA06C70650C55D4AD612F7` | identique | protege |
| Copie `events/india_events/sepoy_mutiny_events.txt` | meme hash | meme hash | identique au fork |
| Fork `descriptor.mod` | `93C2AD4C459B1E897A37AA6964EEEFB1C7522D5175F12B43B0BB35020BA82021` | identique | protege |
| Copie `descriptor.mod` | `1921791546626A938E18EEADC765538120325AFA87E0EA309C2C3C6502175B40` | identique | difference C1A attendue |
| Marqueur jetable | `280066169F9D9D7020FEF4342264D18C5B1613CA40B74D519ADD4E7F3492838A` | identique | protege |
| Descripteur launcher jetable | `FBFDFB891E3E355C05ED996B4A6866475E259081E8196187A2424C9DECCC3733` | identique | protege |

Taille de la copie avant C1B : 17 325 176 octets. Apres ajout des quatre
fichiers : 948 fichiers et 17 327 120 octets. L'augmentation exacte est de
quatre fichiers et 1 944 octets.

## 6. Exemples vanilla de decisions

| Element | Exemple local | Fichier et ligne | Syntaxe retenue | Justification |
|---|---|---|---|---|
| Scope | aide vanilla | `common/decisions/000_decisions_help.txt:5` | decision evaluee en country scope | documentation 1.13 locale |
| Visibilite | aide et Grand Exhibition | aide `:23`, `grand_exhibition_decision.txt:5` | `is_shown`, puis `is_player = yes` | reserve au joueur |
| Validite | aide vanilla | `000_decisions_help.txt:29` | `possible` | bloc de validite atteste |
| Identite pays | decision autrichienne | `austria_decisions.txt:5` | `c:BIC ?= this` adapte de `c:AUS ?= this` | comparaison country scope attestee |
| Effet | aide vanilla | `000_decisions_help.txt:35` | `when_taken` | nom du bloc 1.13 confirme |
| Event popup | decision Raj | `british_raj_decisions.txt:22` | `trigger_event = { id = ... popup = yes }` | appel direct atteste |
| IA | aide vanilla | `000_decisions_help.txt:42` | `ai_chance = { value = 0 }` | zero interdit la prise par l'IA |
| Localisation | aide vanilla | `000_decisions_help.txt:52` | cle, `_desc`, `_tooltip` | les trois cles sont fournies |

## 7. Exemples vanilla de country events

| Element | Exemple local | Fichier et ligne | Syntaxe retenue |
|---|---|---|---|
| Namespace et ID | event Coree | `events/korea_events.txt:1` | `namespace = zz_sepoy_test`, puis `zz_sepoy_test.1` |
| Type et placement | event Coree | `events/korea_events.txt:4` | `type = country_event`, `placement = root` |
| Titre et description | event Coree | `events/korea_events.txt:6` | cles `.t` et `.d` |
| Presentation popup | event Coree | `events/korea_events.txt:10` | duree, image, son et icone existants |
| Garde BIC | event breakup BIC | `events/bic_breakup.txt:22` | `trigger = { c:BIC ?= this }` |
| Option sans effet | crise egyptienne | `events/egyptian_crisis_events.txt:192` | option contenant uniquement `name` |

Les ressources visuelles et sonores retenues existent deja dans la vanilla
locale. Elles n'ont aucun effet persistant.

## 8. Identifiants et namespace retenus

- Namespace : `zz_sepoy_test`.
- Decision : `zz_sepoy_test_verify_bic_root`.
- Event : `zz_sepoy_test.1`.
- Localisations visibles : decision, description, tooltip, titre, description
  d'event et option.

La recherche prealable dans le fork, la copie et la vanilla a retourne zero
occurrence pour ces identifiants. Aucun conflit n'existait.

## 9. Structure de la decision

La decision est evaluee en country scope. `is_shown` et `possible` exigent a
la fois `is_player = yes` et `c:BIC ?= this`. `ai_chance` vaut zero. Elle ne
possede ni cout, ni cooldown, ni scripted effect. Son seul `when_taken` est :

```txt
trigger_event = { id = zz_sepoy_test.1 popup = yes }
```

## 10. Double garde BIC

La premiere garde se trouve dans la decision, avec le test BIC repete dans
`is_shown` et `possible`. La seconde garde independante se trouve dans le
`trigger` de l'event. Trois comparaisons `c:BIC ?= this` sont donc presentes :
deux pour l'ergonomie de la decision et une pour la protection de l'event.

## 11. Structure de l'evenement

`zz_sepoy_test.1` est un `country_event` place sur `root`. Il affiche un titre,
une description et une seule option de fermeture. Son trigger exige BIC. Il ne
contient ni `immediate`, ni effet d'option, ni appel d'event secondaire.

## 12. Preuve de l'absence d'effet persistant

L'inventaire des blocs executables montre uniquement :

- dans la decision, l'ouverture de l'event de test ;
- dans l'event, une option avec une cle de nom et aucun effet.

Les autres champs de l'event sont des metadonnees d'affichage. Aucun owner,
controller, pays, sujet, state, pop, radical, loyaliste, journal entry, flag,
variable, modifier ou relation n'est lu ou modifie par un effet du harnais.

## 13. Localisations anglaise et francaise

Deux fichiers seulement ont ete crees sous les dossiers deja attestes :
`localization/english` et `localization/french`. Chacun contient six cles, sans
doublon. Les en-tetes sont exactement `l_english:` et `l_french:` et les deux
fichiers sont encodes en UTF-8 avec BOM.

La cle `_tooltip`, en plus des cinq cles recommandees, est necessaire selon
l'aide vanilla des decisions afin d'eviter une cle brute. Aucun texte gameplay
existant n'est remplace.

## 14. Verification des termes interdits

Les quatre fichiers ont ete controles pour les 22 familles interdites : events
Sepoy 2/3/4, effets territoriaux ou diplomatiques, independance/annexion,
creation de pays, radicaux/loyalistes, journal entries, hasard, boucle, scopes
de states et regions/states interdits. Chaque compteur vaut zero.

Le seul `trigger_event` present appelle exactement `zz_sepoy_test.1`. Aucun
autre ID d'event n'est appele.

## 15. Validation statique

- Accolades decision : 6 ouvrantes, 6 fermantes.
- Accolades event : 4 ouvrantes, 4 fermantes.
- Un namespace, une definition de decision et une definition d'event.
- Une seule invocation de `zz_sepoy_test.1` depuis la decision.
- Six cles EN et six cles FR, sans doublon.
- BOM valide et aucun caractere ou ligne vide avant les en-tetes YAML.
- Aucune tabulation dans les YAML ; les tabulations des scripts suivent les
  exemples Clausewitz vanilla locaux.
- Le commentaire `DISPOSABLE TEST HARNESS - DO NOT COPY TO MAIN MOD` figure
  dans les deux scripts.

Ces controles ne prouvent pas encore l'acceptation par le moteur. Cette preuve
appartient a C1C.

## 16. Verification des deux fichiers Sepoy copies

Les deux hashes de la copie sont identiques aux hashes C1A et aux fichiers du
fork. Ils contiennent zero occurrence de `region_bengal`, `region_bombay`,
`region_central_india`, `region_madras` et `region_punjab`, et zero reference
a `zz_sepoy_test`.

`STATE_WEST_BENGAL` n'a pas ete modifie : l'identite bit a bit des deux
fichiers protege toutes ses occurrences et leur contexte.

## 17. Resume du manifest

Le manifest C1B contient 11 lignes : quatre `CREATED_HARNESS`, trois
`UNCHANGED_CONTROL`, deux `EXPECTED_DESCRIPTOR_DIFFERENCE` et deux
`CREATED_REPORT`.

Plus precisement, les controles couvrent les quatre fichiers de harnais, les
deux fichiers Sepoy, le descripteur interne, le descripteur launcher, le
marqueur, ce rapport et le manifest. La ligne auto-referentielle du manifest
laisse volontairement sa propre taille et son propre hash vides : un fichier
ne peut pas contenir son hash final sans modifier ce hash.

## 18. Etat final du fork

Aucun fichier gameplay suivi du fork n'a ete modifie. Les seuls nouveaux
livrables C1B sont ce rapport et son manifest. Le dossier technologique non
suivi reste une exception preexistante distincte.

Le fork compte desormais 945 fichiers suivis : les deux livrables C1A ont ete
commites apres la creation physique de la copie. Ils sont, par construction,
les deux seuls chemins suivis absents de celle-ci. Les 943 fichiers qui
constituaient la copie C1A sont toujours presents ; aucune difference de hash
inattendue n'existe, hors le nom distinct deja documente du descripteur.

## 19. Procedure de test runtime C1C

1. Fermer toute autre instance du jeu et utiliser un playset dedie.
2. Activer uniquement `1776 Sepoy Functional Test (Disposable)` ; desactiver
   le fork principal pour eviter les definitions dupliquees.
3. Demarrer une partie comme BIC et verifier que la decision est visible et
   utilisable.
4. Cliquer la decision et verifier l'ouverture de `BIC root verified`, puis
   fermer l'event.
5. Confirmer qu'aucun state, pays, sujet, variable ou journal entry n'a change.
6. Refaire un controle avec un autre pays : la decision doit etre absente.
7. Quitter proprement et inspecter les logs pour `zz_sepoy_test`, `Script
   system error`, `PostValidate`, `Invalid scope` et les cles brutes.

C1B n'a execute aucune de ces etapes.

## 20. Risques restants

- Seul un lancement C1C peut confirmer que le moteur 1.13 charge les quatre
  fichiers et affiche correctement la decision.
- Le fork et la copie ne doivent jamais etre actifs simultanement.
- Une commande console pourrait contourner la visibilite de la decision ; la
  garde BIC de l'event doit alors refuser un autre root.
- La copie est jetable et ne doit ni etre publiee ni servir de source de merge.

## 21. Verdict

**`READY_FOR_HARNESS_RUNTIME_TEST`**

Le harnais est minimal, non destructif et statiquement conforme. Aucun effet
persistant ni appel a la chaine Sepoy n'a ete detecte.

## 22. Fichiers crees dans la copie

- `common/decisions/zz_sepoy_functional_test.txt`
- `events/zz_sepoy_functional_test_events.txt`
- `localization/english/zz_sepoy_functional_test_l_english.yml`
- `localization/french/zz_sepoy_functional_test_l_french.yml`

## 23. Fichiers crees dans le fork

- `docs/reports/hotfix/HOTFIX_5C2E4C1B_SEPOY_HARNESS_STATIC_SETUP.md`
- `docs/reports/hotfix/HOTFIX_5C2E4C1B_HARNESS_MANIFEST.csv`

## 24. Confirmation docs/research/technology

Les sept fichiers conservent leurs tailles et hashes initiaux. Aucune lecture
d'ecriture, copie ou transformation n'a vise ce dossier.

## 25. Confirmation du stash MARATH

Le stash `WIP NAVY-3C-3 Maratha Konkan Flotilla` reste present, intact et non
applique. Aucun `git stash pop` n'a ete execute.
