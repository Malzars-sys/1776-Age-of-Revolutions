# HOTFIX-5C2E4B3 - Retest runtime des API Sepoy

## 1. Resume

Le retest runtime des corrections HOTFIX-5C2E4B1 et HOTFIX-5C2E4B2 est
reussi.

L'utilisateur a charge une partie avec la Compagnie des Indes orientales
(`BIC`) en 1776, simule un mois sans crash, confirme que `je_uneasy_raj` est
restee inactive, puis quitte proprement le jeu.

Les logs frais ne contiennent plus aucune mention de
`common/journal_entries/04_sepoy_mutiny.txt` ni de
`events/india_events/sepoy_mutiny_events.txt`. Les deux erreurs de pinning et
les deux PostValidate `has_role` propres a ces fichiers ont disparu. Aucune
nouvelle erreur de parsing, de scope ou de validation Sepoy n'a ete introduite.

**Verdict : PASS.**

## 2. Etat Git initial

- Branche : `hotfix-dlc-audit`.
- HEAD initial : `a974f07 Update Sepoy character role API`.
- Commit HOTFIX-5C2E4B2 present : `a974f07`.
- Commit HOTFIX-5C2E4B1 present : `2ca2a03`.
- Aucun fichier suivi n'etait modifie au debut de la phase.
- Seul `docs/research/technology/` apparaissait comme exception non suivie.
- Stash present et intact :
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`.

## 3. Exception docs/research/technology

Les sept fichiers preexistants sous `docs/research/technology/` ont ete
inventories avec leur taille et leur empreinte SHA-256 avant le test. Ils
n'ont ete ni modifies, ni ajoutes a Git, ni supprimes, ni renommes.

## 4. Verification statique des API

### Journal entries Sepoy

Dans `common/journal_entries/04_sepoy_mutiny.txt` :

| Controle | Resultat |
|---|---:|
| Ligne exacte `should_be_pinned_by_default = ...` | 0 |
| `should_be_pinned_by_default_involved = yes` | 2 |
| `should_be_pinned_by_default_uninvolved_or_context = no` | 2 |
| Garde `possible = { always = no }` | Presente |

### Events Sepoy

Dans `events/india_events/sepoy_mutiny_events.txt` :

| Controle | Resultat |
|---|---:|
| `has_role = general` exact | 0 |
| `has_role_of_type = general` exact | 2 |
| Anciens IDs regionaux Sepoy | 0 |

Les deux fichiers Sepoy etaient conformes avant le lancement.

## 5. Total regional global

Le recomptage des cinq anciens IDs dans `common/` et `events/`, commentaires
exclus et identifiants complets, donne toujours exactement **131** occurrences.

Les cinq IDs controles sont :

- `region_bengal` ;
- `region_bombay` ;
- `region_central_india` ;
- `region_madras` ;
- `region_punjab`.

Les 131 occurrences restantes sont hors des deux fichiers Sepoy testes.

## 6. Horodatage des logs avant test

Le releve pre-test a ete effectue le **14 juillet 2026 a 21:59:10 UTC**.
Victoria 3 etait deja en cours d'execution et cette session a ete confirmee
comme session de test.

| Log | Derniere ecriture avant test | Taille avant test |
|---|---|---:|
| `debug.log` | 2026-07-14 21:54:42.992 UTC | 0 octet |
| `error.log` | 2026-07-14 21:54:42.909 UTC | 0 octet |
| `game.log` | 2026-07-14 21:58:39.273 UTC | 8 989 octets |

Aucun ancien log n'a ete supprime ou renomme automatiquement.

## 7. Deroulement du test manuel

L'utilisateur confirme les actions et resultats suivants :

1. Victoria 3 a ete lance avec la configuration de mod requise.
2. Le menu principal a ete atteint.
3. Une partie `BIC` en 1776 a ete chargee ou demarree.
4. Un mois a ete simule sans crash.
5. `je_uneasy_raj` ne s'est pas activee spontanement.
6. Le jeu a ete quitte proprement.

Aucune option territoriale Sepoy n'a ete declenchee ou testee pendant cette
phase.

## 8. Horodatage des logs apres test

Apres la fermeture, aucun processus `victoria3` ne restait actif.

| Log | Derniere ecriture apres test | Taille apres test |
|---|---|---:|
| `debug.log` | 2026-07-14 22:05:23.501 UTC | 110 737 octets |
| `error.log` | 2026-07-14 22:05:17.020 UTC | 238 648 octets |
| `game.log` | 2026-07-14 22:05:17.020 UTC | 208 228 octets |

Les trois fichiers ont change de taille et d'horodatage. `debug.log` et
`error.log` correspondent donc sans ambiguite au nouveau lancement.

## 9. Resultat du menu principal

**PASS.** Le menu principal a ete atteint sans crash.

## 10. Resultat du chargement BIC

**PASS.** La partie `BIC` en 1776 a ete chargee et jouee normalement.

## 11. Duree simulee

**Un mois complet**, soit davantage que le minimum d'un jour demande, sans
crash.

## 12. Etat de je_uneasy_raj

**Inactive.** L'utilisateur confirme explicitement que `je_uneasy_raj` ne
s'est pas activee spontanement pendant le mois teste.

La correction des API de pinning et de role n'a donc pas modifie la garde
`possible = { always = no }` ni le comportement d'activation en 1776.

## 13. Anciens diagnostics de pinning

Recherche dans `error.log`, `game.log` et `debug.log` :

- `Unexpected token: should_be_pinned_by_default` : aucune occurrence ;
- `should_be_pinned_by_default` : aucune occurrence dans les logs ;
- `should_be_pinned_by_default_involved` : aucune occurrence dans les logs ;
- `should_be_pinned_by_default_uninvolved_or_context` : aucune occurrence
  dans les logs.

L'absence des noms d'API valides dans les logs est normale : aucun diagnostic
ne les a imprimes. Les deux erreurs de lecture observees en E4A ont disparu.

## 14. Anciens diagnostics has_role

Le texte generique
`PostValidate of trigger 'has_role' returned false` apparait encore **397**
fois dans `debug.log`, reparti sur **55 autres fichiers**. Aucune de ces lignes
ne vise `sepoy_mutiny_events.txt`.

Pour la cible de cette phase :

- PostValidate `has_role` provenant de `sepoy_mutiny_events.txt` : 0 ;
- mention `has_role = general` dans les logs : 0 ;
- mention `has_role_of_type = general` dans les logs : 0.

Les deux diagnostics propres aux lignes 2742 et 2747 observes en E4A ont donc
disparu. Les 397 diagnostics restants constituent une dette globale separee et
ne doivent pas etre corriges dans HOTFIX-5C2E4B3.

## 15. Mentions des deux fichiers Sepoy

La recherche de :

- `04_sepoy_mutiny.txt` ;
- `sepoy_mutiny_events.txt` ;

ne retourne **aucune ligne** dans les trois logs frais.

Il n'existe donc aucun resultat a classer comme chargement anormal, warning,
erreur de parsing, erreur de scope ou erreur de validation pour ces deux
fichiers. Aucune nouvelle erreur Sepoy n'a ete introduite par B1 ou B2.

## 16. Anciens IDs regionaux

Le comptage par token complet dans chacun des trois logs donne zero occurrence
pour les cinq anciens IDs.

Cette methode evite de confondre les IDs invalides avec les subdivisions
valides telles que `geographic_region_bombay_old`,
`geographic_region_bengal_old` et `geographic_region_madras_old`.

Resultat pour la chaine Sepoy : **zero erreur regionale**.

## 17. Diagnostics hors perimetre

Les diagnostics suivants restent presents mais ne proviennent pas des deux
fichiers Sepoy :

### PostValidate has_role globaux

- 397 occurrences dans `debug.log` ;
- 55 fichiers sources distincts ;
- 0 source Sepoy.

Les principaux fichiers concernes comprennent
`events/agitators_events/agitators_election_events.txt`,
`events/india_events/utilitarian.txt`, `events/suffragist_events.txt` et divers
events d'expedition ou de revolution.

### Invalid right side during comparison 'sr'

- 1 208 occurrences dans `error.log` ;
- 1 052 occurrences dans `game.log` ;
- 21 emplacements distincts releves dans `error.log`.

La majorite provient de `common/journal_entries/01_natural_borders_of_france.txt` :

- ligne 128 : 359 occurrences ;
- ligne 129 : 359 occurrences ;
- ligne 130 : 359 occurrences.

D'autres occurrences concernent notamment
`common/scripted_buttons/00_new_colonial_admins.txt` et plusieurs journal
entries hors Sepoy.

### region_persia

Le token exact `region_persia` n'apparait dans aucun des trois logs de ce
retest. La dette relevee dans E4A n'a pas ete reproduite pendant cette session.

### Classes generiques

Les logs frais ne contiennent aucune chaine `Invalid scope`, `Parsing Error`
ou `Unexpected token`. `debug.log` contient 554 diagnostics PostValidate
globaux, dont aucun n'est attribue aux deux fichiers Sepoy.

Aucun de ces diagnostics hors perimetre n'a ete corrige.

## 18. Verdict

**PASS** selon les criteres HOTFIX-5C2E4B3 :

- menu principal atteint ;
- partie `BIC` chargee ;
- un mois simule sans crash ;
- `je_uneasy_raj` reste inactive ;
- logs frais confirmes ;
- zero ancien diagnostic de pinning provenant de la JE Sepoy ;
- zero PostValidate `has_role` provenant de l'event Sepoy ;
- aucune nouvelle erreur parsing/scope/validation provenant des deux fichiers ;
- zero ancien ID regional Sepoy dans les logs.

Les erreurs hors perimetre ne changent pas ce verdict cible.

## 19. Ce que le test valide

- La nouvelle API de pinning est acceptee au chargement.
- La nouvelle API `has_role_of_type = general` est acceptee dans les deux
  character scopes de `sepoy_mutiny_events.10`.
- Les quatre diagnostics E4A propres aux fichiers Sepoy ont disparu.
- La chaine reste inactive en 1776 comme prevu.
- Le chargement et une simulation courte avec `BIC` restent stables.
- Les remplacements regionaux Sepoy ne produisent aucune erreur au chargement
  passif.

## 20. Ce que le test ne valide pas

- L'execution fonctionnelle de `sepoy_mutiny_events.10` lorsque la chaine est
  active.
- La qualite historique du general selectionne.
- Les options territoriales `sepoy_mutiny_events.2.a`, `.2.b`, `.2.c` et `.2.e`.
- Le trigger fonctionnel de `STATE_WEST_BENGAL`.
- Les transferts territoriaux, changements de proprietaire et selections de
  capitales.
- La creation, la propagation et la resolution complete de la revolte.
- Les erreurs `has_role` ou `sr` appartenant a d'autres systemes.

## 21. Etapes restantes pour les options territoriales

1. Preparer une sauvegarde ou un scenario de test ou la chaine Sepoy est deja
   active, sans modifier ses gardes dans la branche principale.
2. Tester l'option `.2.a` et verifier les selections, transferts et logs.
3. Revenir a la sauvegarde de reference puis tester `.2.b`.
4. Refaire le meme protocole pour `.2.c`.
5. Tester `.2.e` separement, avec une attention particuliere a
   `STATE_WEST_BENGAL`.
6. Pour chaque option, utiliser des logs frais et verifier les owners avant et
   apres, les pays revoltes, les capitales, `set_state_owner`, les scopes
   aleatoires et les erreurs de region.

Ces tests doivent constituer une phase fonctionnelle distincte. Aucun n'a ete
execute dans B3.

## 22. Liste exacte des fichiers crees

- `docs/reports/hotfix/HOTFIX_5C2E4B3_SEPOY_API_RUNTIME_RETEST.md`.

Aucun autre fichier n'a ete cree par cette phase.

## 23. Confirmation d'absence de modification gameplay

Aucun fichier gameplay n'a ete modifie. Aucun diagnostic decouvert pendant le
retest n'a ete corrige. `STATE_WEST_BENGAL`, les options territoriales, les
journal entries, les events et toutes les API existantes sont restes
strictement inchanges.

## 24. Confirmation docs/research/technology

Les sept fichiers concurrents sous `docs/research/technology/` n'ont pas ete
touches, ajoutes, supprimes ou renommes par cette phase.

## 25. Confirmation du stash MARATH

Le stash
`stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`
reste present et intact. Aucun `git stash pop` n'a ete execute.

Aucun commit automatique n'a ete cree.
