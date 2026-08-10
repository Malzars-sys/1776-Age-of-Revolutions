# HOTFIX-6A.3 — Audit ciblé DEI

Date : 2026-07-23
Périmètre : audit statique documentaire, aucun gameplay, aucun runtime

## 1. Résumé

L’inventaire canonique désigne un seul fichier DEI à revoir : `events/dei_breakup.txt`. Le fork, la source hotfix et vanilla 1.13 diffèrent au niveau du fichier complet, mais le résultat utile se sépare en trois groupes :

- les annonces hotfix « perte de Cape Colony et Ceylon » et « plus de nom Malaya à l’indépendance » disposent déjà dans le fork des mêmes blocs que la source hotfix ; aucun delta hotfix custom n’est donc importable ;
- le résultat territorial Cape/Ceylon reste `UNVERIFIED` : le script n’identifie aucun bénéficiaire explicite, l’admissibilité et l’adjacence des candidats ne sont pas démontrées pour les deux territoires, et `independence.2` ne transfère aucun état ;
- sept différences dans `dei_breakup.1` sont identiques entre source hotfix et vanilla 1.13. Ce sont des adaptations vanilla 1.13 masquées par l’override ancien du fork, pas des deltas hotfix custom.

Verdict : audit complet, aucune correction gameplay autorisée dans cette phase et résolution ciblée requise avant tout prompt de correction.

## 2. Verdicts d’entrée

- `AUSTRIA_CROATIA_WEST_SWITZERLAND_TARGETED_FIX_COMPLETE`
- `RUSSIA_SUBJECTHOOD_ALIGNMENT_COMPLETE`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`
- `NEXT_MERGE_BLOCK_IDENTIFIED`

## 3. État Git initial

Branche `hotfix-dlc-audit`, zéro staged, stash `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` intact et aucun processus Victoria/launcher. `docs/research/technology/` et le fichier non suivi `bject` ont été explicitement déclarés normaux, futurs, non suivis et hors périmètre par l’opérateur. Ils n’ont pas été modifiés.

## 4. Sources et méthode

Sources lues : C1AI, roadmap, inventaire global, registre restant, matrice des blocs, audit upstream DLC, rapport 6A.2F2 et rapports NAVY concernant DEI/VOC. La ligne canonique est `HOTFIX_GLOBAL_DIFFERENCE_INVENTORY.csv:333`, `events/dei_breakup.txt`, région `east_indies`, statut initial `ALL_THREE_DIFFER / PENDING_REVIEW`.

Après identification de cette ligne, les dépendances DEI ont été contrôlées par extraction de blocs équilibrés et SHA-256 entre :

- fork : `1776_Age_of_Revolutions_fork` ;
- source hotfix en lecture seule : `1776_Age_of_Revolutions_hotfix_source` ;
- vanilla 1.13 en lecture seule : `C:\Games\Victoria 3 The Great Wave\game`.

## 5. Changelog

Preuves directes :

- ligne 12 : `The Dutch East Indies breaking up will lose both Cape Colony and Ceylon` ;
- ligne 13 : `Dutch East Indies won't be called 'Malaya' on independence`.

Preuves setup complémentaires : leader industrialiste DEI (ligne 34), ownership de bâtiments à Ceylon (ligne 35), bonus d’incorporation DEI (ligne 73), retrait du Northern Cape (ligne 153) et retrait du traité de transit avec Waterboersland (ligne 167).

## 6. Inventaire trois voies du fichier canonique

| Valeur | Fork | Hotfix | Vanilla 1.13 |
|---|---:|---:|---:|
| Octets | 9 828 | 10 822 | 10 757 |
| Lignes | 520 | 545 | 545 |
| SHA-256 | `D960CB89…E829591` | `D4742B89…6855A5EE` | `5E5780EA…8657EA` |

La seule différence hotfix/vanilla du fichier complet est dans `alk_breakup.1`, hors DEI. Le bloc `dei_breakup.1` hotfix est identique au bloc vanilla 1.13. Aucun remplacement complet du fichier n’est permis.

## 7. Delta annoncé Cape Colony / Ceylon

Les blocs `STATE_CEYLON`, `STATE_EASTERN_CAPE` et `STATE_CAPE_COLONY` sont identiques entre fork et hotfix dans states, bâtiments et pops. Ils diffèrent de vanilla parce qu’ils constituent le setup 1776. La source hotfix n’apporte donc aucun hunk absent au fork.

La boucle de `dei_breakup.1.a`, lignes fork 42–102, ne sélectionne qu’un pays sujet de DEI ou porteur d’une culture primaire de langue malaise, possédant un état voisin du territoire DEI. Les sujets DEI initiaux sont `YOG`, `SRK` et `COC` (Cochin). Aucun pacte ne fait de `KND`, `SAF`, `ORA` ou d’un autre voisin du Cap/Ceylon un sujet DEI. Le changement de tag conserve les territoires et `independence.2` ne fait qu’offrir une loi de gouvernement puis reconnaître le pays.

Classification : `UNVERIFIED`. Égalité fork/hotfix prouvée, mais résultat fonctionnel du changelog non prouvé et statiquement douteux. Une résolution doit identifier des bénéficiaires et hunks territoriaux exacts avant correction.

## 8. Delta annoncé « Malaya »

Le bloc `DEFAULT` de noms dynamiques exclut explicitement `c:DEI` du nom `colonial_admin_malaya`. Le bloc dynamique `DEI` n’applique `dyn_c_east_indies` que lorsque le pays est sujet. Ces blocs, le setup pays avec `malaya_subject_var` et les localisations anglaises correspondantes sont identiques fork/hotfix.

Classification : `ALREADY_MERGED_EQUIVALENT`. Aucun hunk de localisation ou de script n’est requis. Les localisations françaises restent protégées.

## 9. Adaptation vanilla — Ulema sunnite, option Java

Hunk fork `events/dei_breakup.txt:103-107`, hotfix/vanilla `:103-113` : hotfix et vanilla ajoutent au groupe dévot le nom `ig_sunni_madrasahs` et les traits `ig_trait_pious_fiction`, `ig_trait_sharia`, `ig_trait_da_wat` avant `change_tag = JAV`.

Classification : `VANILLA_1_13_ALREADY_PROVIDES`. Les objets et localisations existent dans vanilla 1.13. Rollback d’une future correction : supprimer uniquement ce bloc `ig:ig_devout`.

## 10. Adaptation vanilla — cultures et personnages, option Java

Hunk fork `:108-119`, hotfix/vanilla `:114-136` : le fork retire seulement `cu:dutch` et tue les personnages néerlandais non immortels. Hotfix/vanilla parcourent toutes les cultures primaires, retirent chacune avec un scope temporaire, retirent les personnages correspondants de la vie publique et utilisent `retire_character` pour les Néerlandais restants. Le délai de l’événement est enregistré séparément comme DEI-010 dans la delta map.

Classification : `VANILLA_1_13_ALREADY_PROVIDES`. Rollback : restaurer les instructions fork `remove_primary_culture` et `kill_character` ; le rollback du délai reste DEI-010.

## 11. Adaptation vanilla — Ulema sunnite, option Indonésie

Hunk fork `:133-138`, hotfix/vanilla `:150-161` : même bloc dévot sunnite que pour Java.

Classification : `VANILLA_1_13_ALREADY_PROVIDES`. Rollback : supprimer uniquement ce bloc `ig:ig_devout`.

## 12. Adaptation vanilla — cultures, religion et personnages, option Indonésie

Hunk fork `:138-154`, hotfix/vanilla `:161-182` : le fork retire seulement `cu:dutch`, ajoute huit cultures et tue les personnages néerlandais. Hotfix/vanilla retirent toutes les cultures primaires et leurs personnages par scopes, réajoutent les huit cultures et fixent `rel:sunni`. Le délai de l’événement est enregistré séparément comme DEI-011 dans la delta map.

Classification : `VANILLA_1_13_ALREADY_PROVIDES`. Rollback : restaurer le bloc fork exact sans `set_state_religion` ; le rollback du délai reste DEI-011.

## 13. Adaptation vanilla — délai de l’option de refus

Hunk fork `:167`, hotfix/vanilla `:195` : `trigger_event = { id = independence.2 }` devient `trigger_event = { id = independence.2 days = 1 }`.

Classification : `VANILLA_1_13_ALREADY_PROVIDES`. Rollback : retirer seulement `days = 1`.

## 14. Pourquoi ces adaptations ne sont pas des deltas hotfix requis

Le bloc DEI hotfix est byte-for-byte équivalent à vanilla 1.13. La règle de phase interdit de confondre cette égalité avec du contenu custom hotfix. Le fork masque toutefois ces valeurs par son override ancien, présent depuis le commit initial `b602804`. Leur éventuelle intégration relève donc d’un alignement vanilla 1.13 ciblé, à décider après résolution, et non d’un import hotfix.

## 15. Pays, lois et technologies

Le fichier pays DEI est strictement identique fork/hotfix (`170523CE…F87CAE`) et conserve le setup 1776 : technologies, `law_subjecthood`, `law_colonial_administration`, amendement racialized subjecthood, `malaya_subject_var` et modificateurs. Aucun changement de loi ou technologie n’est requis. `pan-nationalism` reste uniquement le trigger de l’option Indonésie.

## 16. États, bâtiments et pops

Les neuf blocs inspectés pour Ceylon, Eastern Cape et Cape Colony sont identiques fork/hotfix dans states, bâtiments et pops. Ils sont des divergences 1776 face à vanilla. Aucun remplacement de `00_states.txt`, `10_india.txt`, `04_subsaharan_africa.txt` ou fichiers de pops n’est autorisé. ADMIN, BIC et les six fichiers gameplay protégés 6A.2 restent intacts.

## 17. Diplomatie

Le bloc sujets DEI est identique fork/hotfix : `YOG`, `SRK`, `COC` puppets. `NET -> DEI` reste une `chartered_company` et la liberté initiale DEI reste `-30`. Ces valeurs n’établissent pas le transfert Cape/Ceylon. Le traité de transit DEI–ORA présent dans le fork devra être réaudité séparément contre l’annonce ligne 167 ; il n’est pas une ligne DEI de l’inventaire canonique initial et n’est pas modifié ici.

## 18. Formations et NAVY

Le bloc DEI de `06_military_formations_asia.txt` diffère volontairement : fork `Koloniale_Marine`, zéro capital ship, trois frégates à `STATE_EAST_JAVA`; hotfix une frégate sans state region; vanilla fournit une autre base. Le rapport NAVY-2B-bis documente précisément le passage local de une à trois frégates, sans amiral ni loi navale.

Classification : `NAVY_PROTECTED`. Aucune correction DEI ne doit toucher cette formation.

## 19. Journal entries, BIC et Travancore

`common/journal_entries/00_east_indies.txt` mélange BIC, régions indiennes et DEI. Le fork y porte les corrections Inde closes. Aucun hunk de ce fichier n’est nécessaire aux deltas de `dei_breakup.1`; il reste protégé BIC/Travancore/Inde.

## 20. Localisation

Les clés anglaises DEI/Malaya pertinentes sont déjà présentes et identiques fork/hotfix. Les adaptations vanilla du bloc événement réutilisent des clés vanilla existantes. Aucune localisation française n’est touchée ou requise.

## 21. Dépendances fonctionnelles

- pays : DEI, JAV, IDN, NET, YOG, SRK, COC ;
- états : Java, Sumatra, Ceylon, Eastern Cape, Cape Colony et leurs voisins ;
- bâtiments/pops : scopes DEI 1776 de Ceylon et du Cap, identiques fork/hotfix ;
- diplomatie : sujet chartered company de NET, trois puppets DEI ;
- formations : `Koloniale_Marine` protégée NAVY ;
- lois/technologies : `pan-nationalism`, lois proposées par `independence.2`, aucune modification requise ;
- localisation : noms DEI/East Indies/Malaya et Ulema sunnite, déjà fournis.

## 22. Chevauchements protégés

- NAVY : formation DEI trois frégates, protégée ;
- ADMIN : historiques de bâtiments, aucune modification ;
- BIC/Travancore/Inde : journal et fichiers Inde, aucune modification ;
- MARATH : stash non inspecté et intact ;
- Russie, Japon, Mamluk Iraq, localisations françaises, descripteurs, launcher, sauvegardes et recherches technologiques : hors périmètre et intacts ;
- `activate_law = law_type:law_frontier_colonization` n’a pas été touché.

## 23. Classification consolidée

| Classe | Nombre | Résultat |
|---|---:|---|
| `ALREADY_MERGED_EQUIVALENT` | 3 | nom Malaya, setup/leader DEI, ownership bâtiments Ceylon |
| `VANILLA_1_13_ALREADY_PROVIDES` | 7 | hunks exacts de `dei_breakup.1` masqués par le fork |
| `NAVY_PROTECTED` | 1 | flotte DEI trois frégates |
| `ADMIN_PROTECTED` | 1 | historiques bâtiments dépendants |
| `UNVERIFIED` | 1 | perte fonctionnelle Cape Colony/Ceylon |
| `REQUIRED_HOTFIX_DELTA` | 0 | aucun contenu custom hotfix absent prouvé |

La carte détaillée est `HOTFIX_6A3_DEI_TARGETED_AUDIT_DELTA_MAP.csv`.

## 24. Priorités

- P0 : résoudre statiquement le bénéficiaire et le hunk exact de perte Cape/Ceylon ;
- P1 : décider l’alignement des sept hunks vanilla 1.13 sans toucher `alk_breakup.1` ;
- P3 : préserver les équivalences déjà fusionnées et toutes les protections.

## 25. Correction minimale éventuelle

Aucun prompt de correction n’est publié. La phase suivante est `HOTFIX_6A3R_DEI_BREAKUP_HUNK_RESOLUTION`, en lecture seule. Elle doit fermer deux décisions : mécanisme exact Cape/Ceylon avec bénéficiaires valides, puis admission ou rejet groupé des sept hunks vanilla 1.13. Une future correction ne pourra modifier que `dei_breakup.1` et éventuellement des hunks territoriaux explicitement prouvés ; jamais le fichier complet.

## 26. Runtime

Zéro runtime exécuté, conformément au prompt. Un runtime ne sera justifié qu’après définition d’un correctif fermé.

## 27. Gameplay inchangé

Aucun fichier gameplay, localisation, carte, descripteur, launcher, sauvegarde ou recherche technologique n’a été modifié. Seuls le présent rapport, sa delta map et les index canoniques nécessaires sont produits.

## 28. Verdict final

- `HOTFIX_6A3_DEI_TARGETED_AUDIT_COMPLETE`
- `NO_REQUIRED_HOTFIX_DELTA_IDENTIFIED`
- `DEI_CAPE_CEYLON_OUTCOME_UNVERIFIED`
- `DEI_VANILLA_1_13_ALIGNMENT_REQUIRES_RESOLUTION`
- `NAVY_PROTECTED`
- `ADMIN_PROTECTED`
- `NO_GAMEPLAY_CHANGED`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`
