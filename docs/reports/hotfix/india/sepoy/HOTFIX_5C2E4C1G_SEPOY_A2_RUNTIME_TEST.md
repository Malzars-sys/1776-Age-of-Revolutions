# HOTFIX-5C2E4C1G - Test runtime Sepoy A-2

## 1. Verdict

**PASS_A2_RUNTIME**

Le scénario jetable A-2 a atteint son résultat attendu : la boucle de redistribution de `sepoy_mutiny_events.2.a` s'est terminée sans crash, blocage ni répétition infinie malgré l'absence volontaire de receveur valide pour la portion témoin de Ceylan. BIC a ensuite été annexée, le pays joué est devenu GBR et la portion témoin a finalement été transmise à GBR.

Victoria 3 n'a pas été relancé pour produire ce rapport. La documentation repose sur le test déjà terminé, les captures runtime fournies et les logs frais écrits lors de cette session.

## 2. Périmètre et protocole

- Le test a utilisé une **nouvelle partie BIC en 1776** dans le playset jetable `1776_Age_of_Revolutions_sepoy_test`.
- Aucune sauvegarde A-1 n'a été chargée ou réutilisée.
- Une baseline A-2 distincte a été créée avant toute mutation.
- La préparation A-2 a été déclenchée manuellement, puis l'option `Appliquer les deux mutations jetables du setup` a été sélectionnée.
- La décision d'ouverture de l'événement réel n'est devenue disponible qu'après validation de tous ses garde-fous.
- `sepoy_mutiny_events.2` a été ouvert manuellement une seule fois.
- Seule l'option **2.a**, `L'Inde est perdue. Laissons Whitehall se disputer nos ressources restantes.`, a été choisie manuellement.
- Un jour de jeu a ensuite été laissé passer, une sauvegarde post-test distincte a été créée, puis le jeu a été quitté proprement.

## 3. Préparation A-2 observée

| Contrôle | Avant préparation | Après préparation | Résultat |
|---|---|---|---|
| Portion principale de `STATE_CEYLON` | Propriétaire DEI | Propriétaire BIC | Conforme |
| Portion PUD de `STATE_MADRAS` | Propriétaire PUD | Propriétaire GBR | Conforme |
| Pays joué | BIC | BIC | Conforme |
| Relation BIC-GBR | BIC sujet de GBR | Inchangée | Conforme |
| Event Sepoy réel | Non ouvert | Non ouvert automatiquement | Conforme |

La préparation n'a exécuté que les deux mutations prévues :

```text
s:STATE_CEYLON.region_state:DEI -> c:BIC
s:STATE_MADRAS.region_state:PUD -> c:GBR
```

## 4. Zéro receveur valide avant l'événement

Après la préparation, la décision `zz_sepoy_test_a2_open_event` était visible et activable. Son bloc `possible` exige simultanément :

- l'existence de la portion BIC de `STATE_CEYLON` ;
- l'existence de la portion GBR de `STATE_MADRAS` ;
- l'absence de l'ancienne portion PUD de `STATE_MADRAS` ;
- l'appartenance du témoin à `region_south_india` ;
- l'absence de tout state voisin dont le propriétaire possède une culture primaire du groupe d'héritage sud-asiatique.

La disponibilité runtime de cette décision constitue donc la confirmation fonctionnelle de **zéro receveur valide** avant l'ouverture de l'événement réel. Cette garde est même plus stricte que le filtre complet de la boucle 2.a, car elle élimine déjà tout voisin culturellement admissible avant le contrôle de sa capitale.

## 5. Exécution de `sepoy_mutiny_events.2.a`

L'événement réel `sepoy_mutiny_events.2` s'est ouvert manuellement sur BIC. L'option 2.a a été sélectionnée exclusivement et manuellement. Les résultats observés sont les suivants :

| Contrôle | Résultat observé | Verdict |
|---|---|---|
| Fermeture de l'événement | Normale | PASS |
| Fin de la boucle de redistribution | Terminée | PASS |
| Jeu encore actif | Oui | PASS |
| Crash | Aucun | PASS |
| Blocage | Aucun | PASS |
| Boucle non terminée | Aucune | PASS |
| Pays joué après l'effet | GBR | PASS |
| Statut de BIC | Annexée | PASS |
| Portion témoin de Ceylan | Détenue par GBR | PASS |
| Owner nul | Aucun observé | PASS |
| Transfert invalide | Aucun observé | PASS |

Le comportement confirme la lecture statique : faute de receveur valide, le témoin de Ceylan est resté à BIC pendant la boucle, puis a été récupéré par GBR lors de l'annexion finale de BIC.

## 6. Contrôle des logs frais

Les logs de la session terminée ont été lus sans relancer le jeu :

| Log | Dernière écriture locale | Observation |
|---|---|---|
| `debug.log` | 16/07/2026 03:40:55 | Session terminée, aucun motif A-2 ciblé |
| `error.log` | 16/07/2026 03:40:37 | 2 597 erreurs globales, zéro erreur A-2 ciblée |
| `game.log` | 16/07/2026 03:40:37 | Aucun motif A-2 ciblé |
| `system.log` | 16/07/2026 03:14:40 | Informations système de la session |

Aucun processus Victoria 3, Dowser ou Paradox Launcher n'était actif lors de la collecte documentaire.

Les recherches ciblées dans `error.log` ont donné exactement zéro occurrence pour :

- `zz_sepoy_test_a2` ;
- `sepoy_mutiny_events.2` ;
- `STATE_CEYLON` ;
- `STATE_MADRAS` ;
- `set_state_owner`.

Il n'existe donc aucune erreur loguée visant le harnais A-2, l'événement réel testé, les deux state regions témoins ou l'effet de transfert.

## 7. Erreurs hors périmètre

`error.log` contient 2 597 entrées `Error:` sans rapport avec A-2 :

| Groupe | Nombre | Localisation principale | Classement |
|---|---:|---|---|
| `Invalid right side during comparison 'sr'` | 2 591 | Principalement `common/journal_entries/01_natural_borders_of_france.txt` | Hors périmètre |
| `has_law_or_variant trigger [ Given law is a variant, we expect the parent ]` | 6 | `common/interest_groups/00_landowners.txt:459` | Hors périmètre |

Dans `01_natural_borders_of_france.txt`, les lignes 128, 129 et 130 totalisent à elles seules 2 377 erreurs `sr` sur 2 591. Cette pollution préexistante n'affecte pas le verdict A-2.

Un warning unique `Unknown tooltip type` apparaît dans la télémétrie. Il est documenté séparément comme **non bloquant** : il n'est associé à aucun identifiant A-2 et le jeu est resté actif, a franchi un jour, a sauvegardé puis s'est fermé proprement.

## 8. Intégrité des fichiers Sepoy

Les deux sources Sepoy sont restées identiques entre le fork et la copie jetable :

| Fichier | Taille | SHA-256 |
|---|---:|---|
| `common/journal_entries/04_sepoy_mutiny.txt` | 16 040 | `DAEFCB59CCF6B303D2E39C948D8038006C1346AFE40A2B812D45EE4D947E361C` |
| `events/india_events/sepoy_mutiny_events.txt` | 63 210 | `557936500AC585F7F69B9F5B063BDDA377AFF4A5AFAA06C70650C55D4AD612F7` |

Aucun fichier Sepoy du fork n'a été modifié pendant cette documentation.

## 9. Intégrité du harnais A-2

Les quatre fichiers du harnais jetable sont inchangés depuis la préparation statique C1F :

| Fichier | SHA-256 |
|---|---|
| `common/decisions/zz_sepoy_functional_test_a2.txt` | `1F11BDB7CD2F59EDF220E320AD996A11C44F143D9C99F7DAEE5913B7C1E571A2` |
| `events/zz_sepoy_functional_test_a2_events.txt` | `71EC607B1AA2290A429D02AB479B19A84EA54F0A7FF72FB19D0B96C8041B65FB` |
| `localization/english/zz_sepoy_functional_test_a2_l_english.yml` | `882ED5B6B51095923FB614F27E03944C04DA25F3A236CC56685000D8154A8EF9` |
| `localization/french/zz_sepoy_functional_test_a2_l_french.yml` | `0C50B823D8E96B8C4DF3F44E96A13F2010967ED307DF858AB0298BB20AEC630A` |

La copie jetable contient toujours exactement 956 fichiers. Aucun fichier gameplay ou harnais n'a été modifié pour produire le présent rapport.

## 10. Domaines protégés

- `docs/research/technology/` reste présent avec ses 7 fichiers préexistants et inchangés ; il demeure l'unique exception non suivie antérieure à cette documentation.
- Le stash `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` est toujours présent et n'a été ni appliqué, ni modifié, ni supprimé.
- Aucun fichier `common/`, `events/`, `localization/`, `map_data/` ou fichier du harnais jetable n'a été modifié.
- Aucun commit automatique n'a été créé.

## 11. Conclusion

Le test A-2 valide le cas sans receveur de la boucle générique de `sepoy_mutiny_events.2.a`. La redistribution se termine, aucun owner nul n'est produit, BIC est annexée, le contrôle joueur passe à GBR et la portion témoin de Ceylan aboutit correctement chez GBR. Les erreurs présentes dans les logs sont hors périmètre et aucune ne cible le scénario A-2.

**Verdict final : PASS_A2_RUNTIME**
