# HOTFIX-6A.22 — Audit des deux pinning Afghanistan 1.13

Date : 5 août 2026
Branche : `hotfix-dlc-audit`
HEAD d'entrée : `1c9e411cb980f82bc4b49e8e09fcbc73cb074f63`
Mode : audit documentaire et statique, gameplay en lecture seule

## 1. Périmètre et préflight

L'audit porte uniquement sur les propriétés de pinning de
`je_consolidate_afghanistan` et `je_unify_afghanistan` dans
`common/journal_entries/03_afghanistan.txt`. Aucun autre champ afghan, aucun
contenu Great Game et aucun autre fichier gameplay n'est candidat à une
correction dans cette phase.

Le préflight confirme :

- racine Git exacte et branche `hotfix-dlc-audit` ;
- HEAD `1c9e411cb980f82bc4b49e8e09fcbc73cb074f63`, message
  `Reindex residual scripts after Poland runtime` ;
- rapport 6A.21 présent dans le HEAD avec tous ses verdicts ;
- arbre suivi propre et index vide ;
- huit non-suivis protégés connus seulement, non ouverts ;
- aucun processus Victoria 3, Dowser ou launcher Paradox ;
- stash NAVY-3C-3 intact au hash
  `518df704fa14599c0f254fae13859210663dd976`.

## 2. Identité byte-level des trois fichiers

| arbre | octets | encodage | BOM | fins de ligne | lignes | ancienne propriété | propriété 1.13 | SHA-256 |
|---|---:|---|---|---|---:|---:|---:|---|
| fork | 36 769 | UTF-8 | UTF-8 BOM | LF uniquement | 1 877 | 2 | 0 | `D24333CE06C2DE801F91462000713DCEB430822A2167F7336341E9071B19F988` |
| source hotfix | 23 927 | UTF-8 | UTF-8 BOM | LF uniquement | 1 184 | 0 | 2 | `2C4427D13C0AECEE9E89D872CF8CA9B61B491F843D921166D642DCE8F06E9C2F` |
| vanilla 1.13 | 29 870 | UTF-8 | UTF-8 BOM | LF uniquement | 1 526 | 0 | 2 | `386E57394FA9A57E406B1CC1C234856D46E4901159D689D8AE54126140F81266` |

Le blob Git du fichier fork dans le HEAD et celui du worktree valent tous deux
`d93ccfce1cea248e24c4919ed1e11fdecfd8e775`. Le fichier n'a donc pas changé
depuis l'état d'entrée 6A.21.

## 3. Diagnostics existants

La déduplication utilise la clé `génération + message normalisé + chemin +
ligne`. La génération fraîche est strictement `debug.1.log + debug.log`.

| génération | log | horodatage | message | chemin | ligne | objet | brut | dédupliqué | présence |
|---|---|---|---|---|---:|---|---:|---:|---|
| fraîche 6A.20Q | `debug.log` | `01:19:39` | `Unexpected token: should_be_pinned_by_default` | `common/journal_entries/03_afghanistan.txt` | 2 | `je_consolidate_afghanistan` | 1 | 1 | courante |
| fraîche 6A.20Q | `debug.log` | `01:19:39` | `Unexpected token: should_be_pinned_by_default` | `common/journal_entries/03_afghanistan.txt` | 1826 | `je_unify_afghanistan` | 1 | 1 | courante |
| rotation immédiatement antérieure | `debug.2.log` | `21:09:37` | même message | même chemin | 2 et 1826 | mêmes objets | 2 | 2 | rotation |
| rotation ancienne | `debug.4.log` | `19:38:06` | même message | même chemin | 2 et 1826 | mêmes objets | 2 | 2 | rotation |

`debug.1.log`, `debug.3.log` et `debug.5.log` ne contiennent aucune occurrence
ciblée. La génération fraîche contient exactement deux diagnostics bruts et
deux diagnostics dédupliqués ; chacun pointe sur l'unique ancienne propriété
de son objet. Aucun nouveau log n'est produit.

Les hashes de génération sont conformes :

- `debug.1.log` :
  `109EBCACE21F5663AD917C7FA59DBDD61BB225BA9C9681AC25DE827A637B6CC1` ;
- `debug.log` :
  `FFEFFAF26F69C1A0E09F6EB4F1C9FD1723FBA9DF793967F26CF26159725BD4D8` ;
- `debug.2.log` :
  `B401921CD7FF354A3D0D82E385DD514C5C28585638400908C5E98F6DC1D4DF40`.

## 4. Preuve de syntaxe 1.13

Les 172 fichiers vanilla de `common/journal_entries` contiennent 394
occurrences de
`should_be_pinned_by_default_uninvolved_or_context` dans 157 fichiers : 378
valeurs `yes` et 16 valeurs `no`. Toutes les occurrences se trouvent à la
profondeur structurelle 1, donc directement à la racine d'un objet journal
entry. L'ancienne forme exacte `should_be_pinned_by_default =` est absente de
la vanilla.

Le fichier vanilla Afghanistan place la nouvelle propriété aux lignes 3 et
1475, dans les mêmes deux objets. Des fichiers complexes tels que
`00_tutorial.txt`, `00_player_objectives_great_game.txt` et
`05_prestige_goods.txt` utilisent la même propriété à la même profondeur.

Les scripts permettent ainsi de prouver que :

1. la propriété 1.13 est acceptée à la racine d'une journal entry ;
2. l'ancienne propriété est rejetée deux fois par le moteur actuel ;
3. la source et la vanilla utilisent la nouvelle propriété dans chacun des
   deux objets afghans ;
4. cette propriété est un scalaire racine, placé avant `icon`, sans scope,
   trigger ni bloc adjacent ;
5. son remplacement peut être isolé sans importer d'autre contenu.

Aucune sémantique UI non démontrée n'est revendiquée.

## 5. Extraction exacte par accolades

Les bornes ont été calculées par profondeur d'accolades, en ignorant les
accolades contenues dans les chaînes et les commentaires.

| objet | fork | source hotfix | vanilla 1.13 |
|---|---|---|---|
| `je_consolidate_afghanistan` | lignes 1–1823, 1 823 lignes | lignes 1–1133, 1 133 lignes | lignes 1–1471, 1 471 lignes |
| `je_unify_afghanistan` | lignes 1825–1877, 53 lignes | lignes 1135–1184, 50 lignes | lignes 1473–1526, 54 lignes |

Les deux objets existent donc intégralement dans les trois arbres.

## 6. Comparaison fonctionnelle de `je_consolidate_afghanistan`

La relation est établie après normalisation des espaces et commentaires, sans
normaliser les identifiants ni les valeurs.

| groupe fonctionnel | fork | source hotfix | vanilla 1.13 | relation trois voies | fonction syntaxique / pertinence 1776 | correction future |
|---|---|---|---|---|---|---|
| pinning | ancienne clé ligne 2 | nouvelle clé ligne 3 | nouvelle clé ligne 3 | source = vanilla ≠ fork | propriété racine rejetée en 1.13 | incluse, seule différence admissible |
| icône et groupe | mêmes valeurs | mêmes valeurs | mêmes valeurs | tous égaux | présentation et classement | exclu, déjà identique |
| visibilité lobby | bloc GBR/DLC identique | identique | identique | tous égaux | visibilité lobby | exclu |
| visibilité inactive | `region_persia` legacy | chevauchement d'intérêts avec AFG | `sr:region_greater_persia` | tous différents | accès du grand pouvoir au JE | exclu, design et région |
| boutons scriptés | 12 références | mêmes 12 | mêmes 12 | tous égaux | négociations de frontières | exclu absolument |
| invalidation | absence d'AFG | identique | identique | tous égaux | fermeture si AFG n'existe plus | exclu |
| impulsion hebdomadaire | notification et événement `gg_afghanistan.1` | identique | identique | tous égaux | notification Great Game | exclu |
| effets immédiats | 317 lignes | 190 lignes | 317 lignes | tous différents | scopes, pays, frontières et initialisation | exclu absolument |
| conditions `possible` | 94 lignes | 68 lignes | 98 lignes | tous différents | états, régions, sujets et contrôle territorial | exclu absolument |
| complétion | 36 lignes | 36 lignes | 36 lignes | tous égaux | condition de consolidation | exclu |
| effets de complétion | 613 lignes | 385 lignes | 457 lignes | tous différents | traités, frontières, pays, variables et récompenses | exclu absolument |
| délai | `365` | `365` | `365` | tous égaux | durée de l'entrée | exclu |
| effets d'expiration | 691 lignes | 379 lignes | 490 lignes | tous différents | résolution Great Game, événements et effets | exclu absolument |
| poids | `1001` | `1001` | `1001` | tous égaux | pondération | exclu |

Les différences de longueur ne sont pas des invitations à remplacer un bloc :
elles prouvent au contraire que les régions, frontières, états, scopes,
variables, pays, sujets, tooltips, événements, effets, récompenses et la logique
Great Game doivent rester hors des deux hunks de pinning.

## 7. Comparaison fonctionnelle de `je_unify_afghanistan`

| groupe fonctionnel | fork | source hotfix | vanilla 1.13 | relation trois voies | fonction syntaxique / pertinence 1776 | correction future |
|---|---|---|---|---|---|---|
| pinning | ancienne clé ligne 1826 | nouvelle clé ligne 1137 | nouvelle clé ligne 1475 | source = vanilla ≠ fork | propriété racine rejetée en 1.13 | incluse, seule différence admissible |
| icône et groupe | mêmes valeurs | mêmes valeurs | mêmes valeurs | tous égaux | présentation et classement | exclu |
| visibilité lobby | capitale dans `sr:region_persia` | `geographic_region_greater_afghanistan` | capitale dans `sr:region_greater_persia` | tous différents | accès géographique et cultures pashtun/tadjik | exclu absolument |
| boutons scriptés | appels Russie et Grande-Bretagne | identiques | identiques | tous égaux | appels diplomatiques Great Game | exclu |
| conditions `possible` | capitale dans `sr:region_persia` | région géographique Greater Afghanistan | capitale dans `sr:region_greater_persia` | tous différents | formation territoriale et culturelle | exclu absolument |
| complétion | AFG formée | identique | identique | tous égaux | achèvement | exclu |
| effet de complétion | tooltip de `gg_afghanistan.4` | identique | identique | tous égaux | événement de résultat | exclu |
| description de résultat | identique | identique | identique | tous égaux | texte d'issue | exclu |
| poids | `1000` | `1000` | `1000` | tous égaux | pondération | exclu |

L'inventaire lexical du fichier complet confirme des variations massives de
régions stratégiques, régions géographiques, états, pays, scopes, variables et
tooltips entre les trois arbres. Il ne trouve aucune occurrence directe de
religion, personnage, rôle de dirigeant, technologie ou modificateur dans ces
deux objets. Ces catégories restent néanmoins explicitement interdites dans
toute correction future.

## 8. Patch théorique byte-reproductible

Le patch est construit en mémoire sur les octets du fork, sans fichier
temporaire dans le dépôt et sans écriture gameplay :

```diff
 je_consolidate_afghanistan = {
-	should_be_pinned_by_default = yes
+	should_be_pinned_by_default_uninvolved_or_context = yes
 	icon = "gfx/interface/icons/event_icons/event_map.dds"

 je_unify_afghanistan = {
-	should_be_pinned_by_default = yes
+	should_be_pinned_by_default_uninvolved_or_context = yes
 	icon = "gfx/interface/icons/event_icons/waving_flag.dds"
```

| mesure | entrée | résultat théorique |
|---|---:|---:|
| fichiers | 1 | 1 |
| objets | 2 | 2 |
| hunks | 0 | 2 |
| lignes ajoutées/supprimées | 0 | `2+/2-` |
| octets | 36 769 | 36 813 |
| lignes LF | 1 877 | 1 877 |
| anciennes propriétés | 2 | 0 |
| nouvelles propriétés | 0 | 2 |
| BOM | UTF-8 | UTF-8, conservé |
| SHA-256 | `D24333CE06C2DE801F91462000713DCEB430822A2167F7336341E9071B19F988` | `C9165714127E017486949AF8DDE742FD5A0E5F3093C5A43191695FE213969E13` |

Chaque nouvelle clé ajoute 22 octets, soit 44 octets au total. Le remplacement
inverse produit 36 769 octets et restitue exactement le SHA-256 d'entrée ; la
comparaison des tableaux d'octets est vraie. Aucune autre modification n'est
présente dans le résultat théorique.

## 9. Réponses aux questions de décision

1. Oui. Les deux diagnostics frais correspondent exactement aux lignes 2 et
   1826 et aux deux anciennes propriétés.
2. Oui. Les deux objets existent dans les trois arbres aux bornes documentées.
3. Oui. Source et vanilla convergent exactement sur la nouvelle propriété dans
   chacun des deux objets.
4. Oui. Les 394 exemples vanilla la placent tous à la même profondeur racine.
5. Oui. Chaque scalaire est isolé entre l'ouverture de l'objet et `icon`.
6. Oui. Toutes les différences Great Game et géographiques commencent hors des
   deux lignes ciblées et restent exclues.
7. Oui. Aucun bouton, scope, personnage, rôle, événement, effet ou élément de
   progression ne doit être importé.
8. Oui. Le correctif peut rester limité à un fichier, deux objets et deux hunks.
9. Oui. Le hash théorique et l'inversion sont byte-reproductibles.
10. Non. La substitution syntaxique convergente ne requiert aucune décision
    humaine de design ; elle ne tranche aucun hunk fonctionnel adjacent.
11. Oui. Un runtime ultérieur peut vérifier `2 → 0` sur une nouvelle génération
    sans forcer les journal entries.
12. Non pour la validation parser/runtime. Une absence de visibilité naturelle
    interdit seulement de revendiquer une validation UI du pinning.

## 10. Décision

Toutes les conditions d'atomicité sont satisfaites. La seule prochaine phase
sélectionnée est :

`HOTFIX_6A22F_AFGHANISTAN_TWO_JE_PINNING_1_13_ALIGNMENT`

Cette correction est sélectionnée mais n'est pas commencée. Son futur
périmètre devra être exactement les deux substitutions et le hash théorique
ci-dessus. La validation statique devra confirmer `2+/2-`, `2 → 0` anciennes
propriétés, `0 → 2` nouvelles, 36 813 octets, 1 877 lignes LF, BOM conservé et
SHA-256 `C9165714127E017486949AF8DDE742FD5A0E5F3093C5A43191695FE213969E13`.
Un runtime ultérieur sera limité à une seule ouverture humaine et une nouvelle
génération de logs.

## 11. Verdicts

```text
HOTFIX_6A22_AFGHANISTAN_TWO_JE_PINNING_1_13_ALIGNMENT_AUDIT_COMPLETE
AFGHANISTAN_TWO_JE_THREE_WAY_COMPARISON_COMPLETE
AFGHANISTAN_TWO_JE_PINNING_DIAGNOSTICS_CONFIRMED
AFGHANISTAN_PINNING_AND_GREAT_GAME_HUNKS_SEPARATED
AFGHANISTAN_TWO_HUNK_THEORETICAL_PATCH_COMPUTED
NO_GAMEPLAY_CHANGED
NO_RUNTIME_REQUIRED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
AFGHANISTAN_TWO_JE_PINNING_ATOMIC_ALIGNMENT_PROVEN
NEXT_EXECUTION_PHASE = HOTFIX_6A22F_AFGHANISTAN_TWO_JE_PINNING_1_13_ALIGNMENT
```
