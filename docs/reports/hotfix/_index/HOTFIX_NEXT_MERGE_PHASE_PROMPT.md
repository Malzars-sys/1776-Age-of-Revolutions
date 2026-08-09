# État canonique — réindexation finale 6A.28 sélectionnée

Nous poursuivons le portage du mod Victoria 3 vers Victoria 3 1.13 — The Great
Wave dans `1776_Age_of_Revolutions_fork`.

Modèle recommandé : GPT-5.6 Thinking avec raisonnement élevé.

## Dernière phase terminée

`HOTFIX_6A27Q_GLOBAL_SCRIPT_API_ATOMIC_SWEEP_RUNTIME_QA` est terminée. Une
seule ouverture humaine sous `release/1.13.0 : d9ade554e` valide les six
familles 6A.27, sans nouvelle identité ni changement gameplay.

```text
TOTAL_TARGET_API_DIAGNOSTICS_BEFORE = 609
TOTAL_TARGET_API_DIAGNOSTICS_AFTER = 0
NEW_6A27_ATTRIBUTABLE_ERRORS = 0
GAMEPLAY_HASHES_MATCH = 87
HUMAN_RUNTIME_LAUNCHES = 1

FRESH_TOTAL_DIAGNOSTICS_AFTER_6A27Q = 420
FRESH_PARSER_DIAGNOSTICS_AFTER_6A27Q = 98
FRESH_POSTVALIDATE_DIAGNOSTICS_AFTER_6A27Q = 322
FRESH_PATHS_AFTER_6A27Q = 113
FRESH_NORMALIZED_MESSAGES_AFTER_6A27Q = 65
```

Les 127 exceptions API et les 14 exceptions pinning restent bornées. Le sweep
multi-API et le pinning global sont fermés.

## Phase exclusive à exécuter après commit manuel de 6A.27Q

`HOTFIX_6A28_FINAL_RESIDUAL_MERGE_BLOCKER_REINDEX`

Cette phase est strictement statique : ne lancer ni Victoria 3, ni Dowser, ni
Paradox Launcher. Utiliser comme source canonique les segments frais et les
manifestes 6A.27Q. Reproduire exactement la baseline `420 = 98 + 322`, avec
113 chemins et 65 messages normalisés, selon la clé `generation +
normalized_message + path + line`.

Classifier chaque diagnostic restant, sans appliquer de correction, dans une
et une seule catégorie :

```text
TRUE_MERGE_BLOCKER
PROTECTED_WORK
INTENTIONAL_FORK_DIVERGENCE
POST_MERGE_BACKLOG
SEMANTIC_REWRITE_REQUIRED
BOUNDED_EXCEPTION
ALREADY_ACCOUNTED_FOR
```

Conserver séparément les 127 exceptions API, les 14 exceptions pinning, les
sept recherches technologiques non suivies et tous les blocs historiques
fermés. Ne rouvrir aucune des six familles validées. Ne créer aucune
micro-phase et ne modifier aucun gameplay.

Produire un inventaire exhaustif par diagnostic, une matrice par famille et le
nombre réellement démontré :

```text
TRUE_MERGE_BLOCKERS_REMAINING = N
```

Si `N = 0`, sélectionner directement le runtime global final. Si `N > 0`,
regrouper les bloqueurs compatibles dans le nombre minimal de corrections, sans
commencer ces corrections pendant 6A.28.

```text
HOTFIX_6A27Q_GLOBAL_SCRIPT_API_ATOMIC_SWEEP_RUNTIME_QA_COMPLETE
GLOBAL_MULTI_API_ATOMIC_SWEEP_RUNTIME_PASS
GLOBAL_RESIDUAL_DIAGNOSTICS = 420
NEXT_EXECUTION_PHASE = HOTFIX_6A28_FINAL_RESIDUAL_MERGE_BLOCKER_REINDEX
```

---

# Prompt historique — correction des cinq pinning de l'unification allemande 1.13

Nous poursuivons le portage du mod Victoria 3 vers Victoria 3 1.13 — The Great
Wave dans `1776_Age_of_Revolutions_fork`.

Exécuter exclusivement :

`HOTFIX_6A24F_GERMAN_UNIFICATION_FIVE_JE_PINNING_1_13_ALIGNMENT`

## État canonique d’entrée

Le HEAD doit être le commit manuel de 6A.24 et contenir
`HOTFIX_6A24_GERMAN_UNIFICATION_FIVE_JE_PINNING_1_13_ALIGNMENT_AUDIT.md` avec :

```text
HOTFIX_6A24_GERMAN_UNIFICATION_FIVE_JE_PINNING_1_13_ALIGNMENT_AUDIT_COMPLETE
GERMAN_UNIFICATION_FIVE_JE_THREE_WAY_COMPARISON_COMPLETE
GERMAN_UNIFICATION_PINNING_AND_FUNCTIONAL_HUNKS_SEPARATED
GERMAN_UNIFICATION_FIVE_HUNK_THEORETICAL_PATCH_COMPUTED
GERMAN_UNIFICATION_FIVE_JE_PINNING_ATOMIC_ALIGNMENT_PROVEN
NEXT_EXECUTION_PHASE = HOTFIX_6A24F_GERMAN_UNIFICATION_FIVE_JE_PINNING_1_13_ALIGNMENT
```

## Périmètre exclusif

Modifier uniquement :

`common/journal_entries/00_german_unification.txt`

et exactement les cinq propriétés racine des objets :

1. `je_schleswig_holstein_question` ;
2. `je_german_unification_idea` ;
3. `je_north_german_unification` ;
4. `je_south_german_unification` ;
5. `je_german_unification`.

Appliquer exactement cinq substitutions :

```diff
-should_be_pinned_by_default = yes
+should_be_pinned_by_default_uninvolved_or_context = yes
```

Préconditions et résultat exact :

```text
SHA-256 d'entrée = A52D4525DED1BE8F804CEEDD99329E03EAABB9E53376D04F4BBE9A8CDC32EC22
SHA-256 final = 30A3F3356AA43060C0E8D315DDF34D8D304680290134E0212AE6AEB852C8F239
taille finale = 9527 octets
lignes = 448 LF
BOM UTF-8 = conservé
diff = 5+/5-
ancienne propriété = 0
nouvelle propriété = 5
autres octets modifiés = 0
```

Préserver exactement indentation, BOM, LF et tous les octets adjacents. Ne
remplacer ni le fichier ni un objet complet. Exclure progression, conditions,
visibilité, géographie, régions, états, frontières, cultures, pays, scopes,
événements, effets, récompenses, modificateurs, tooltips, icônes, groupes,
délais et poids.

Cette phase est une correction statique : aucun runtime, aucun stage et aucun
commit automatique. Après validation statique, sélectionner au maximum une QA
runtime humaine unique destinée à mesurer `5 → 0`, sans la lancer.

Modèle recommandé : GPT-5.6 Thinking avec raisonnement élevé. Nombre de
lancements Victoria 3 : **0**.

---

# Prompt historique — correction des deux pinning Afghanistan 1.13

Nous poursuivons le portage du mod Victoria 3 vers Victoria 3 1.13 — The Great
Wave dans `1776_Age_of_Revolutions_fork`.

Exécuter exclusivement :

`HOTFIX_6A22F_AFGHANISTAN_TWO_JE_PINNING_1_13_ALIGNMENT`

## État canonique d’entrée

Le HEAD doit contenir le rapport commité
`HOTFIX_6A22_AFGHANISTAN_TWO_JE_PINNING_1_13_ALIGNMENT_AUDIT.md` avec :

```text
HOTFIX_6A22_AFGHANISTAN_TWO_JE_PINNING_1_13_ALIGNMENT_AUDIT_COMPLETE
AFGHANISTAN_TWO_JE_THREE_WAY_COMPARISON_COMPLETE
AFGHANISTAN_TWO_JE_PINNING_DIAGNOSTICS_CONFIRMED
AFGHANISTAN_PINNING_AND_GREAT_GAME_HUNKS_SEPARATED
AFGHANISTAN_TWO_HUNK_THEORETICAL_PATCH_COMPUTED
NO_GAMEPLAY_CHANGED
NO_RUNTIME_REQUIRED
AFGHANISTAN_TWO_JE_PINNING_ATOMIC_ALIGNMENT_PROVEN
NEXT_EXECUTION_PHASE = HOTFIX_6A22F_AFGHANISTAN_TWO_JE_PINNING_1_13_ALIGNMENT
```

Le fichier `common/journal_entries/03_afghanistan.txt` doit avoir avant
correction :

```text
octets = 36769
lignes = 1877 LF
encodage = UTF-8 avec BOM
SHA-256 = D24333CE06C2DE801F91462000713DCEB430822A2167F7336341E9071B19F988
ancienne propriété = 2
nouvelle propriété = 0
```

## Correction strictement autorisée

Modifier uniquement les propriétés racine de :

- `je_consolidate_afghanistan` ;
- `je_unify_afghanistan`.

Appliquer exactement deux substitutions :

```diff
-	should_be_pinned_by_default = yes
+	should_be_pinned_by_default_uninvolved_or_context = yes
```

Résultat statique obligatoire :

```text
un fichier
deux objets
deux hunks
diff = 2+/2-
octets = 36813
lignes = 1877 LF
BOM UTF-8 conservé
ancienne propriété = 0
nouvelle propriété = 2
SHA-256 = C9165714127E017486949AF8DDE742FD5A0E5F3093C5A43191695FE213969E13
```

Le remplacement inverse doit restituer exactement le hash d'entrée. Préserver
tous les autres octets. Ne remplacer ni le fichier ni les objets depuis la
source ou la vanilla.

Exclure absolument régions, frontières, états, Great Game, boutons, visibilité,
conditions, progression, tooltips, pays, sujets, cultures, religions,
personnages, rôles, technologies, événements, effets, récompenses,
modificateurs, scopes et variables. Ne modifier aucun autre gameplay ni aucun
bloc clos ou protégé.

Ne lancer ni Victoria 3 ni le launcher pendant 6A.22F. Une éventuelle QA
runtime `2 → 0` doit rester une phase humaine ultérieure, sélectionnée seulement
après validation statique complète. Ne pas effectuer de stage ou commit
automatique et préserver le stash NAVY-3C-3.

Modèle recommandé : GPT-5.6 Thinking avec raisonnement élevé. Nombre de
lancements Victoria 3 : **0**.

---

# Prompt historique — audit des deux pinning Afghanistan 1.13

Nous poursuivons le portage du mod Victoria 3 vers Victoria 3 1.13 — The Great
Wave dans `1776_Age_of_Revolutions_fork`.

Exécuter exclusivement :

`HOTFIX_6A22_AFGHANISTAN_TWO_JE_PINNING_1_13_ALIGNMENT_AUDIT`

## État canonique d’entrée

Le HEAD doit contenir le rapport commité
`HOTFIX_6A21_POST_POLAND_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md` avec :

```text
HOTFIX_6A21_POST_POLAND_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE
POST_6A20Q_FRESH_DIAGNOSTICS_REINDEXED
POLAND_TWO_JE_PINNING_BLOCK_REMAINS_CLOSED
RESIDUAL_VANILLA_1_13_ALIGNMENT_COHORT_REVIEWED
RESIDUAL_CURRENT_AND_ROTATION_ONLY_DIAGNOSTICS_SEPARATED
RESIDUAL_P0_P1_PRIORITY_MATRIX_COMPLETE
DESCRIPTOR_1_12_5_WARNING_CLASSIFIED_SEPARATELY
NO_GAMEPLAY_CHANGED
NO_RUNTIME_REQUIRED
NEXT_EXECUTION_PHASE = HOTFIX_6A22_AFGHANISTAN_TWO_JE_PINNING_1_13_ALIGNMENT_AUDIT
```

## Audit strictement borné

Auditer en lecture seule `common/journal_entries/03_afghanistan.txt`, uniquement
les propriétés de pinning de :

- `je_consolidate_afghanistan` ;
- `je_unify_afghanistan`.

Le fork emploie deux fois `should_be_pinned_by_default = yes`, rejeté deux fois
dans la génération fraîche 6A.20Q. La source hotfix et la vanilla 1.13 emploient
dans les deux mêmes objets
`should_be_pinned_by_default_uninvolved_or_context = yes`.

Comparer intégralement fork, source hotfix et vanilla afin de séparer ces deux
propriétés de tous les autres hunks. Calculer le patch théorique et son hash,
mais ne l'appliquer sous aucun prétexte pendant cet audit.

Exclure explicitement régions stratégiques, frontières, Great Game, boutons
scriptés, géographie, visibilité, conditions, progression, événements,
personnages, rôles et effets. Ne remplacer ni le fichier ni les objets. Ne
modifier aucun gameplay, ne lancer ni Victoria 3 ni le launcher et ne commencer
aucune correction 6A.22F.

Créer un rapport autonome
`HOTFIX_6A22_AFGHANISTAN_TWO_JE_PINNING_1_13_ALIGNMENT_AUDIT.md`, mettre à jour
uniquement les index documentaires autorisés et terminer soit par une preuve
d'alignement atomique, soit par un verdict bloqué documenté. Préserver tous les
blocs clos ou protégés ainsi que le stash NAVY-3C-3.

Modèle recommandé : GPT-5.6 Thinking avec raisonnement élevé. Nombre de
lancements Victoria 3 : **0**.

---

# Prompt historique — QA runtime des deux pinning Pologne 1.13

Nous poursuivons le portage du mod Victoria 3 vers Victoria 3 1.13 — The Great
Wave dans `1776_Age_of_Revolutions_fork`.

Exécuter exclusivement :

`HOTFIX_6A20Q_POLAND_TWO_JE_PINNING_1_13_RUNTIME_QA`

## État canonique d’entrée

Le HEAD doit être le commit manuel `Align two Poland journal entry pinning
properties for 1.13` et contenir
`HOTFIX_6A20F_POLAND_TWO_JE_PINNING_1_13_ALIGNMENT.md` avec :

```text
HOTFIX_6A20F_POLAND_TWO_JE_PINNING_1_13_STATIC_PASS
POLAND_TWO_JE_PINNING_GAMEPLAY_DIFF_2_PLUS_2_MINUS
POLAND_TWO_JE_PINNING_SHA256_MATCH
POLAND_TWO_JE_PINNING_OTHER_BYTES_UNCHANGED
NO_RUNTIME_EXECUTED
NEXT_EXECUTION_PHASE = HOTFIX_6A20Q_POLAND_TWO_JE_PINNING_1_13_RUNTIME_QA
```

Le fichier `common/journal_entries/00_poland.txt` doit avoir le SHA-256 :

`A5EAF687DC6A736CD50D3C66E5E7601D29442FF3FA8A292C4EE751A7FF981E6A`

## Protocole humain unique

Effectuer exactement une ouverture de Victoria 3 :

1. capturer le manifeste des logs avant lancement ;
2. confirmer que le fork exact et Victoria 3 1.13 sont montés ;
3. lancer une partie neuve en 1776 sans forcer aucune journal entry ;
4. laisser le chargement produire une nouvelle génération de logs ;
5. ne pas modifier la partie pour fabriquer l’accès aux entrées ;
6. fermer Victoria 3 et le launcher avant l’analyse ;
7. capturer le manifeste après lancement ;
8. dédupliquer les diagnostics par génération, message, chemin et ligne.

Baseline historique :

```text
Unexpected token: should_be_pinned_by_default
common/journal_entries/00_poland.txt
lignes 59 et 131
2 diagnostics dédupliqués
```

La QA passe si la nouvelle génération contient zéro diagnostic ciblé et aucune
nouvelle erreur attribuable à `00_poland.txt`. Ne pas prétendre valider le
comportement UI du pinning si les entrées ne sont pas naturellement visibles.
Ne modifier aucun gameplay et ne rouvrir aucun bloc protégé.

Modèle recommandé : GPT-5.6 Thinking avec raisonnement élevé. Nombre de
lancements Victoria 3 : **1**, humain.

---

# Prompt historique — correction des deux pinning Pologne 1.13

Nous poursuivons le portage du mod Victoria 3 vers Victoria 3 1.13 — The Great
Wave dans `1776_Age_of_Revolutions_fork`.

Exécuter exclusivement :

`HOTFIX_6A20F_POLAND_TWO_JE_PINNING_1_13_ALIGNMENT`

## État canonique d’entrée

Le HEAD doit contenir le rapport commité
`HOTFIX_6A20_POLAND_JOURNAL_ENTRY_1_13_ALIGNMENT_AUDIT.md` avec :

```text
HOTFIX_6A20_POLAND_JOURNAL_ENTRY_1_13_ALIGNMENT_AUDIT_COMPLETE
POLAND_TWO_JE_THREE_WAY_COMPARISON_COMPLETE
POLAND_TWO_JE_PINNING_DIAGNOSTICS_CONFIRMED
POLAND_PINNING_AND_GEOGRAPHIC_HUNKS_SEPARATED
POLAND_TWO_HUNK_THEORETICAL_PATCH_COMPUTED
POLAND_TWO_JE_PINNING_ATOMIC_ALIGNMENT_PROVEN
NEXT_EXECUTION_PHASE = HOTFIX_6A20F_POLAND_TWO_JE_PINNING_1_13_ALIGNMENT
```

## Correction strictement autorisée

Modifier uniquement `common/journal_entries/00_poland.txt`, dans :

- `je_christ_of_nations` ;
- `je_poland_lithuania`.

Appliquer exactement deux substitutions :

```diff
-    should_be_pinned_by_default = yes
+    should_be_pinned_by_default_uninvolved_or_context = yes
```

Préconditions :

- SHA-256 avant correction :
  `DD2696FACF3D7988A933E7541D00D989E3E4B813574493D28A2BCA7AA1DACFD0` ;
- exactement deux anciennes propriétés ;
- aucun changement utilisateur du fichier depuis 6A.20.

Résultat statique obligatoire :

- diff gameplay exactement `2+/2-` ;
- zéro ancienne propriété et deux nouvelles ;
- 132 lignes ;
- SHA-256
  `A5EAF687DC6A736CD50D3C66E5E7601D29442FF3FA8A292C4EE751A7FF981E6A` ;
- toutes les autres lignes byte-identiques ;
- géographie, visibilité, complétion, scopes, progression, récompenses et
  effets inchangés.

Ne pas modifier `07_poland_lithuania_mod.txt` ni aucun autre fichier gameplay.
Ne pas élargir aux blocs protégés ou clos. Le runtime de vérification `2 → 0`
est ultérieur à la correction statique ; ne le lancer que si la phase 6A.20F
l’autorise explicitement après son préflight.

Modèle recommandé : GPT-5.6 Thinking avec raisonnement élevé.

---

# Prompt historique — audit Pologne des journal entries 1.13

Nous poursuivons le portage du mod Victoria 3 vers Victoria 3 1.13 — The Great
Wave dans `1776_Age_of_Revolutions_fork`.

Exécuter exclusivement :

`HOTFIX_6A20_POLAND_JOURNAL_ENTRY_1_13_ALIGNMENT_AUDIT`

## État canonique d’entrée

Le rapport d’entrée obligatoire est
`HOTFIX_6A19_RESIDUAL_GLOBAL_SCRIPT_REINDEX.md`. Il doit contenir :

```text
HOTFIX_6A19_RESIDUAL_GLOBAL_SCRIPT_REINDEX_COMPLETE
RESIDUAL_161_LINE_REGISTRY_RECONCILED
RESIDUAL_87_UNKNOWN_GROUPS_REVIEWED
EGYPTIAN_CRISIS_RUNTIME_DEFERRAL_PRESERVED
DECLARED_INTEREST_BLOCK_REMAINS_CLOSED
DEI_VOC_BLOCK_REMAINS_CLOSED
NO_GAMEPLAY_CHANGED
NO_RUNTIME_REQUIRED
NEXT_RESIDUAL_PHASE_SELECTED
NEXT_EXECUTION_PHASE = HOTFIX_6A20_POLAND_JOURNAL_ENTRY_1_13_ALIGNMENT_AUDIT
```

## Objectif borné

Auditer en lecture seule `common/journal_entries/00_poland.txt`, uniquement :

- `je_christ_of_nations`, clé de pinning actuellement ligne 59 ;
- `je_poland_lithuania`, clé de pinning actuellement ligne 131.

Le fork emploie deux fois `should_be_pinned_by_default = yes`, rejeté deux fois
dans le `debug.log` courant. La source hotfix et la vanilla 1.13 emploient aux
deux objets `should_be_pinned_by_default_uninvolved_or_context = yes`.

L’audit doit cependant séparer ces deux clés des hunks géographiques : fork,
source et vanilla divergent sur les conditions de région, de visibilité et de
complétion. Une égalité sur le pinning n’autorise aucun remplacement de fichier
ni aucune absorption des hunks adjacents.

## Contraintes

- phase documentaire et statique uniquement ;
- aucun fichier gameplay modifié ;
- aucun lancement de Victoria 3 ou du launcher ;
- aucune correction appliquée pendant l’audit ;
- aucun commit automatique ;
- stash NAVY-3C-3 et non-suivis protégés intacts ;
- ne pas élargir à `07_poland_lithuania_mod.txt` ;
- ne rouvrir ni Égypte, intérêts déclarés, DEI/VOC, HBC/Navigation Acts, Coup,
  Imperialism, Tanzimat, NAVY, BIC, Inde, Amérique, France ou technologies.

## Livrable et décision

Créer un rapport `HOTFIX_6A20_POLAND_JOURNAL_ENTRY_1_13_ALIGNMENT_AUDIT.md`
qui documente les hashes, les deux objets, les hunks exacts, les diagnostics
courants et l’atomicité éventuelle d’une correction ultérieure. Sélectionner au
maximum une phase corrective distincte ; ne pas la commencer.

Modèle recommandé : GPT-5.6 Thinking avec raisonnement élevé. Nombre minimal de lancements
Victoria 3 pour 6A.20 : **0**.

---

# Prompt historique — réindexation résiduelle post-6A.18

Nous poursuivons le portage du mod Victoria 3 vers Victoria 3 1.13 — The Great
Wave :

`1776_Age_of_Revolutions_fork`

Exécuter exclusivement :

`HOTFIX_6A19_RESIDUAL_GLOBAL_SCRIPT_REINDEX`

## État canonique d’entrée

```text
HOTFIX_6A18Q3_EGYPTIAN_CRISIS_RUNTIME_DEFERRAL_COMPLETE
EGYPTIAN_CRISIS_RUNTIME_SEMANTIC_VALIDATION_DEFERRED_TO_MIDDLE_EAST_FLAVOR_EXTENSION
DECLARED_INTEREST_BLOCK_CLOSED_WITH_DOCUMENTED_RUNTIME_DEFERRAL
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
NEXT_EXECUTION_PHASE = HOTFIX_6A19_RESIDUAL_GLOBAL_SCRIPT_REINDEX
```

La validation sémantique égyptienne n’est pas un succès runtime. Elle est
reportée à une future extension flavor Moyen-Orient parce que le fork
n’instancie pas `EGY` au départ et ne contient aucune chaîne naturelle
d’émergence du pays. Ne pas lancer ou forcer la crise égyptienne dans 6A.19.

## Objectif

Recalculer l’inventaire trois voies après toutes les corrections 6A.4 à 6A.18
et le commit VOC `78e562f`. Reclasser les 87 groupes encore inconnus, rapprocher
le registre historique de 161 lignes de l’état réel du fork et sélectionner au
maximum une prochaine phase bornée.

Cette phase est documentaire et statique. Elle ne modifie aucun gameplay et ne
lance pas Victoria 3.

## Protections

Ne pas modifier le stash NAVY-3C-3, MARATH/SAT/KHP, BIC, Inde, Sepoy, Bombay,
Travancore, les recherches technologiques non suivies, `bject`, les sauvegardes
ou les localisations françaises par remplacement massif. Ne pas rouvrir les
blocs déjà clos, y compris DEI/VOC et les intérêts déclarés.

HBC/Navigation Acts reste un bloc de design séparé. Japon, Mamluk Iraq,
Amérique, France, technologie et localisation doivent être inventoriés, mais
aucune correction ne doit être absorbée automatiquement.

## Références trois voies

- fork : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork` ;
- source hotfix : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source` ;
- vanilla 1.13 : `C:\Games\Victoria 3 The Great Wave\game`.

## Livrables

Créer `HOTFIX_6A19_RESIDUAL_GLOBAL_SCRIPT_REINDEX.md` et mettre à jour les
index, la matrice des blocs, la roadmap, le registre résiduel et ce prompt si
une phase suivante satisfait les conditions de sélection. Documenter les
comptes avant/après et séparer strictement : déjà fusionné, divergence
intentionnelle, backlog flavor, travail protégé, correction requise et inconnu.

Ne jamais exécuter de merge, rebase, stash apply/pop/drop, nettoyage des
non-suivis, commit automatique ou correction gameplay dans 6A.19.

Le prompt ci-dessous est conservé uniquement comme preuve historique de la
phase 6A.18R2 exécutée. Il ne constitue plus une instruction active.

---

# Prompt historique — audit du mécanisme d'initialisation des intérêts 1.13

Nous poursuivons le portage du mod Victoria 3 vers Victoria 3 1.13 — The Great
Wave :

`1776_Age_of_Revolutions_fork`

Tu dois exécuter exclusivement la phase suivante :

`HOTFIX_6A18R2_DECLARED_INTEREST_INITIALIZATION_MECHANISM_1_13_AUDIT`

Cette phase est un audit en lecture seule. Elle ne doit appliquer aucune
correction gameplay et ne doit pas lancer Victoria 3.

## 1. Objectif exact

Le runtime 6A.18Q a confirmé que :

- `common/history/interests/00_interests.txt` est chargé;
- ses 91 actions actives sont toutes atteintes;
- le moteur 1.13 émet `Unknown effect add_declared_interest` pour chacune;
- l'Autriche ne reçoit aucune implication au Sud de la Chine malgré la ligne
  126;
- le Canada témoin reste sans implication;
- les intérêts visibles sont générés par le nouveau système d'implication.

6A.18R2 doit rechercher le mécanisme exact et documenté par lequel Victoria 3
1.13 initialise ou augmente une implication régionale au démarrage. Il faut
déterminer si un équivalent script utilisable existe avant toute correction.

## 2. État d'entrée obligatoire

Branche : `hotfix-dlc-audit`.

La phase 6A.18Q doit être commitée manuellement dans le HEAD avec le message :

`Validate declared interest history runtime for 1.13`

Rapport obligatoire :

`docs/reports/hotfix/_index/HOTFIX_6A18Q_DECLARED_INTEREST_HISTORY_RUNTIME_VALIDATION.md`

Verdicts obligatoires dans le HEAD :

```text
HOTFIX_6A18Q_DECLARED_INTEREST_HISTORY_RUNTIME_VALIDATION_COMPLETE
DECLARED_INTEREST_POSITIVE_AND_NEGATIVE_CONTROLS_EXECUTED
DECLARED_INTEREST_RUNTIME_LOGS_DEDUPLICATED
NO_GAMEPLAY_CHANGED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
DECLARED_INTEREST_LEGACY_EFFECT_RUNTIME_FAIL
DECLARED_INTEREST_HISTORY_API_INVALIDITY_CONFIRMED
NEXT_EXECUTION_PHASE = HOTFIX_6A18R2_DECLARED_INTEREST_INITIALIZATION_MECHANISM_1_13_AUDIT
```

Si ces conditions ne sont pas réunies, arrêter sans écriture avec :

`HOTFIX_6A18R2_BLOCKED_6A18Q_NOT_COMMITTED`

## 3. Préflight

Exécuter en lecture seule :

```powershell
git rev-parse --show-toplevel
git branch --show-current
git rev-parse HEAD
git log -5 --oneline --decorate
git status --short --untracked-files=all
git diff --check
git diff --cached --name-only
git stash list
git rev-parse 'stash@{0}'
git show HEAD:docs/reports/hotfix/_index/HOTFIX_6A18Q_DECLARED_INTEREST_HISTORY_RUNTIME_VALIDATION.md
```

Exiger : racine exacte, branche exacte, HEAD au message attendu, arbre suivi
propre, staged vide, uniquement `bject` et les sept recherches technologiques
non suivis, stash intact et aucun processus Victoria 3/Dowser/launcher.

Stash attendu :

```text
stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla
518df704fa14599c0f254fae13859210663dd976
```

## 4. Protections absolues

Ne jamais inspecter ou modifier `bject`, les sept recherches technologiques,
le stash, BIC, GBR, Inde, Sepoy, Bombay, Travancore, NAVY, ADMIN, HBC,
Navigation Acts, Coup, Imperialism of Promise, Tanzimat, Merchant Banking, les
localisations françaises, les descripteurs ou les sauvegardes.

Ne jamais restaurer `law_colonial_exploitation`. BIC doit conserver
`law_frontier_colonization`.

Ne lancer ni le jeu ni le launcher. Ne modifier aucun fichier gameplay.

## 5. Arbres de référence

Fork :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`

Source hotfix, lecture seule :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source`

Vanilla 1.13, lecture seule :

`C:\Games\Victoria 3 The Great Wave\game`

## 6. Recherche obligatoire

Rechercher séparément, dans les scripts, métadonnées techniques, GUI anglaise,
exemples et chaînes lisibles installées :

- les effets contenant `interest`, `interest_marker`, `involvement` ou
  `strategic_region`;
- `create_interest_marker`, `set_interest_marker`,
  `add_interest_marker_rank`, `remove_interest_marker` et toute signature
  associée;
- les getters d'implication actuelle, cible et de ventilation;
- les initialisations vanilla de territoire, capitale, revendication, armée,
  flotte, traité, pacte et sujet;
- les on-actions exécutés lors de la création du monde ou d'un pays;
- les racines historiques reconnues en 1.13;
- les effets documentés utilisables depuis un scope pays avec une région
  stratégique actuelle;
- les exemples de test ou scripts DLC qui initialisent une implication sans
  action humaine.

Séparer formellement :

1. API de lecture et de tooltip;
2. commandes debug internes;
3. effets script enregistrés;
4. calcul naturel dynamique;
5. initialisation historique au jour 1;
6. mécanismes réservés au code moteur.

La simple présence d'une chaîne binaire, d'un getter GUI ou d'une commande
debug ne prouve pas qu'un effet script soit utilisable.

## 7. Questions à trancher

Le rapport doit répondre explicitement :

1. Existe-t-il un effet 1.13 enregistré qui accepte un pays et une région ?
2. Cet effet définit-il une implication actuelle, une implication cible, un
   rang d'intérêt ou un marqueur legacy ?
3. Est-il autorisé dans `common/history` au chargement du monde ?
4. Existe-t-il un exemple vanilla ou DLC exécutable qui en prouve la syntaxe ?
5. Les cinq niveaux actifs peuvent-ils être initialisés directement ou doivent
   ils découler uniquement des sources naturelles ?
6. Une valeur historique fixe survivrait-elle au recalcul hebdomadaire de
   l'implication ?
7. Un remplacement des 91 lignes est-il techniquement possible sans inventer
   une nouvelle source d'implication ou modifier l'équilibrage ?
8. Un remappage des 26 régions legacy serait-il utile avant la preuve de ce
   mécanisme ?

## 8. Conditions de sélection d'une correction future

Ne sélectionner une phase de correction que si toutes les preuves suivantes
sont réunies :

- nom exact de l'effet enregistré;
- signature exacte des scopes et arguments;
- contexte historique autorisé;
- exemple vanilla/DLC ou test officiel directement comparable;
- sémantique d'implication actuelle/cible démontrée;
- interaction avec le recalcul dynamique comprise;
- remplacement borné sans toucher aux cartographies protégées;
- hash théorique et diff minimal reproductibles.

Si une seule preuve manque, conclure que le mécanisme reste non démontré et ne
sélectionner aucune correction.

## 9. Documentation

Créer uniquement :

`docs/reports/hotfix/_index/HOTFIX_6A18R2_DECLARED_INTEREST_INITIALIZATION_MECHANISM_1_13_AUDIT.md`

Mettre à jour seulement si nécessaire :

- `docs/reports/hotfix/INDEX.md`;
- `HOTFIX_REPORT_INDEX.csv`;
- `HOTFIX_MERGE_BLOCK_STATUS.csv`;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md`;
- `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

## 10. Git

Ne jamais exécuter `git add`, `git reset`, `git restore`, `git checkout` de
fichier, `git clean`, merge, rebase, amend, commit, push, `stash apply`,
`stash pop` ou `stash drop`.

Le HEAD, l'index, le stash et tous les fichiers gameplay doivent rester
inchangés.

## 11. Verdicts minimaux

Terminer par :

```text
HOTFIX_6A18R2_DECLARED_INTEREST_INITIALIZATION_MECHANISM_1_13_AUDIT_COMPLETE
DECLARED_INTEREST_1_13_INITIALIZATION_PATHS_AUDITED
DECLARED_INTEREST_LEGACY_AND_INVOLVEMENT_SEMANTICS_SEPARATED
NO_GAMEPLAY_CHANGED
NO_RUNTIME_REQUIRED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
```

Ajouter ensuite exactement l'un des résultats suivants :

```text
DECLARED_INTEREST_1_13_REPLACEMENT_MECHANISM_PROVEN
NEXT_EXECUTION_PHASE = HOTFIX_6A18F_DECLARED_INTEREST_HISTORY_1_13_ALIGNMENT
```

ou :

```text
DECLARED_INTEREST_1_13_REPLACEMENT_MECHANISM_UNPROVEN
NO_NEXT_EXECUTION_PHASE_SELECTED
```

Ne jamais commencer la phase éventuellement sélectionnée.
