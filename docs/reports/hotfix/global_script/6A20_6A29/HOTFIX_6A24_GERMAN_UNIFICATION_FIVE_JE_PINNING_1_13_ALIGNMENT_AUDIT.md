# HOTFIX-6A.24 — Audit de l'alignement 1.13 des cinq pinning de l'unification allemande

Date : 5 août 2026

Branche : `hotfix-dlc-audit`

HEAD et commit réel de 6A.23 :
`13fd3f946b9728b8e34702fed173127d8d2a4037`

Message d'entrée :
`Select German unification pinning audit after Afghanistan runtime`

Nature : audit documentaire et statique, gameplay en lecture seule.

Modèle recommandé : GPT-5.6 Thinking avec raisonnement élevé. Nombre de
lancements Victoria 3 : **0**.

## 1. Verdict

Les cinq diagnostics frais correspondent exactement aux cinq anciennes
propriétés racine du fork. Les cinq mêmes objets existent dans le fork, la
source hotfix et la vanilla 1.13. La source et la vanilla utilisent cinq fois
la même propriété 1.13, à la même profondeur structurelle, et la vanilla ne
contient aucune occurrence de l'ancienne forme.

Le patch théorique remplace uniquement les cinq noms de propriété. Il produit
un diff `5+/5-`, conserve tous les autres octets, le BOM, les fins LF et les
448 lignes, puis s'inverse exactement vers le hash d'entrée. Toutes les
différences fonctionnelles adjacentes restent exclues. La correction 6A.24F
est donc sélectionnée, mais elle n'est pas commencée.

## 2. Préflight

| Contrôle | Résultat |
|---|---|
| Racine Git | conforme |
| Branche | `hotfix-dlc-audit` |
| HEAD | `13fd3f946b9728b8e34702fed173127d8d2a4037` |
| Rapport 6A.23 dans le HEAD | présent, verdicts complets |
| Arbre suivi | propre |
| Index Git | vide |
| `git diff --check` | propre |
| Processus Victoria 3, Dowser ou launcher Paradox | aucun |
| Non-suivis | huit éléments protégés connus seulement |
| Stash NAVY-3C-3 | intact, `518df704fa14599c0f254fae13859210663dd976` |

Les non-suivis protégés n'ont pas été ouverts, déplacés, modifiés ou indexés.

## 3. Identité trois voies

| Arbre | SHA-256 | Octets | Encodage | BOM | Fins de ligne | Lignes | Ancienne | Nouvelle | Git blob calculé |
|---|---|---:|---|---|---|---:|---:|---:|---|
| fork | `A52D4525DED1BE8F804CEEDD99329E03EAABB9E53376D04F4BBE9A8CDC32EC22` | 9 417 | UTF-8 | oui | 448 LF | 448 | 5 | 0 | `eaeb2a43caaa01420e4f2226305f03a12296940d` |
| source hotfix | `38A42BBFAE01CBC32D42B9076C904A4D0CB65C3C2959F7F7C3ACA2271A7C66B8` | 7 717 | UTF-8 | oui | 372 LF | 372 | 0 | 5 | `2b40b1dc1fb829078e5c197105195a3625686603` |
| vanilla 1.13 | `842D3205CAB766B681DED9BF53D3D17381DA5284CF5DC25EEAB9DE6803B0BF6F` | 9 782 | UTF-8 | oui | 453 LF | 453 | 0 | 5 | `176afa5c4b9ee6abe05716b75fa9d7d1b594b308` |

Le hash et les comptes du fork correspondent exactement à la baseline 6A.23.

## 4. Diagnostics existants

Les deux segments frais conservent leurs hashes attendus :

| Segment | SHA-256 |
|---|---|
| `debug.1.log` | `F0D820034D164FF22C7691D700F5ADD97C35D5921A4F12EEAF41EA75D98DB252` |
| `debug.log` | `92BA705426CAE91590CFF40BC99243DA15226A6858C7B2988B6D553CC9D81123` |

La déduplication utilise génération, message normalisé, chemin et ligne.

| Génération | Segments | Bruts | Dédupliqués | Parser ciblé | Autre parser | `PostValidate` |
|---|---|---:|---:|---:|---:|---:|
| fraîche 6A.22Q | `debug.1.log`, `debug.log` | 5 | 5 | 5 | 0 | 0 |
| immédiatement précédente | `debug.3.log`, `debug.2.log` | 5 | 5 | 5 | 0 | 0 |
| rotations anciennes | `debug.5.log`, `debug.4.log` | 5 | 5 | 5 | 0 | 0 |

Les cinq identités fraîches sont toutes :

```text
Unexpected token: should_be_pinned_by_default
common/journal_entries/00_german_unification.txt
lignes 105, 275, 333, 394 et 447
```

Aucun autre diagnostic parser ou `PostValidate` n'est attribué au fichier dans
la génération fraîche.

## 5. Preuve de syntaxe vanilla 1.13

Dans `game/common/journal_entries`, la propriété
`should_be_pinned_by_default_uninvolved_or_context` possède 394 occurrences
dans 157 fichiers : 378 valeurs `yes` et 16 valeurs `no`. Les 394 occurrences
sont à profondeur structurelle 1, donc à la racine d'une journal entry.

La forme exacte `should_be_pinned_by_default =` possède zéro occurrence dans
la vanilla 1.13. Le moteur 1.13 rejette par ailleurs les cinq occurrences du
fork dans trois générations consécutives. Les objets complexes
`je_acw_countdown`, `je_acw_war`, `je_acw_reconstruction`,
`je_acw_reincorporate`, `je_acw_equality`, `je_acw_wild_wild_west` et les
exemples `no` comme `je_abolish_monarchy`, `je_king_in_parliament`,
`je_suez_survey`, `je_panama_survey` et `je_corn_laws` confirment que le champ
est autonome au niveau racine.

Réponses syntaxiques :

1. oui, la propriété 1.13 est valide à la racine d'une journal entry ;
2. oui, l'ancienne propriété est rejetée par le parser 1.13 ;
3. oui, la propriété moderne existe dans les mêmes cinq objets de la source et
   de la vanilla ;
4. non, elle n'est contenue dans aucun scope, trigger ou bloc adjacent ;
5. oui, chaque substitution est indépendante et terminale après `weight`.

Aucun comportement UI n'est déduit de cette preuve statique.

## 6. Bornes exactes des cinq objets

Les bornes sont calculées par un parseur d'accolades qui ignore commentaires,
chaînes et caractères échappés.

| Objet | Fork | Source | Vanilla | Pinning fork / source / vanilla | Profondeur | Champ précédent | Champ suivant |
|---|---|---|---|---|---:|---|---|
| `je_schleswig_holstein_question` | 1–106, 106 lignes | 1–109, 109 lignes | 1–107, 107 lignes | 105 / 108 / 106 | 1 | `weight` 104 / 106 / 104 | aucun, accolade de fermeture |
| `je_german_unification_idea` | 108–276, 169 lignes | 111–197, 87 lignes | 109–278, 170 lignes | 275 / 196 / 277 | 1 | `weight` 274 / 194 / 275 | aucun, accolade de fermeture |
| `je_north_german_unification` | 278–334, 57 lignes | 199–256, 58 lignes | 280–337, 58 lignes | 333 / 255 / 336 | 1 | `weight` 332 / 253 / 334 | aucun, accolade de fermeture |
| `je_south_german_unification` | 336–395, 60 lignes | 258–318, 61 lignes | 339–399, 61 lignes | 394 / 317 / 398 | 1 | `weight` 393 / 315 / 396 | aucun, accolade de fermeture |
| `je_german_unification` | 397–448, 52 lignes | 320–372, 53 lignes | 401–453, 53 lignes | 447 / 371 / 452 | 1 | `weight` 446 / 369 / 450 | aucun, accolade de fermeture |

Dans le fork, la propriété vaut toujours :

```text
should_be_pinned_by_default = yes
```

Dans la source et la vanilla, elle vaut toujours :

```text
should_be_pinned_by_default_uninvolved_or_context = yes
```

La ligne blanche supplémentaire présente avant le champ moderne dans la source
et la vanilla est seulement une différence de présentation ; elle n'est pas
importée par le patch théorique.

## 7. Comparaison fonctionnelle objet par objet

| Objet | Groupe fonctionnel | Relation trois voies | Fonction et pertinence 1776 | Correction future |
|---|---|---|---|---|
| `je_schleswig_holstein_question` | pinning | fork ancien, source/vanilla modernes | présentation racine | inclure le nom de propriété seulement |
| même objet | icône, groupe, statut, `possible`, complétion, échec, `on_complete`, poids | identiques dans les trois arbres | logique de la question Schleswig-Holstein | exclure |
| même objet | visibilité active et inactive | fork = vanilla ; source différente | la source ajoute `geographic_region_german_confederation`, potentiellement matériel dès 1776 | exclure absolument |
| `je_german_unification_idea` | pinning | fork ancien, source/vanilla modernes | présentation racine | inclure le nom de propriété seulement |
| même objet | icône, groupe, statut, `possible`, complétion, poids | identiques dans les trois arbres | création et statut de l'idée d'unification | exclure |
| même objet | visibilité active et inactive | fork = vanilla ; source différente | la source ajoute la région géographique allemande | exclure |
| même objet | `on_complete`, pays, cultures, scopes, sélection et sauvegarde du candidat | trois versions différentes | fork : `any_country`/`random_country` ; vanilla : variantes `*_in_german_confederation` ; source : itération ordonnée, limite alternative, prestige et position | exclure absolument |
| `je_north_german_unification` | pinning | fork ancien, source/vanilla modernes | présentation racine | inclure le nom de propriété seulement |
| même objet | icône, groupe, statut, échec, `on_complete`, pulse mensuel, effets, récompenses, poids | identiques dans les trois arbres | logique et effets d'unification nord-allemande | exclure |
| même objet | complétion et recherche d'un autre candidat | source = vanilla ; fork différent | `any_country_in_german_confederation` contre `any_country`, matériel pour la formation | exclure absolument |
| `je_south_german_unification` | pinning | fork ancien, source/vanilla modernes | présentation racine | inclure le nom de propriété seulement |
| même objet | icône, groupe, statut, échec, `on_complete`, pulse mensuel, effets, récompenses, poids | identiques dans les trois arbres | logique et effets d'unification sud-allemande | exclure |
| même objet | complétion et recherche d'un autre candidat | source = vanilla ; fork différent | `any_country_in_german_confederation` contre `any_country`, matériel pour la formation | exclure absolument |
| `je_german_unification` | pinning | fork ancien, source/vanilla modernes | présentation racine | inclure le nom de propriété seulement |
| même objet | icône, groupe, statut, visibilité active/inactive, `possible`, `invalid`, complétion, `on_complete`, effets et poids | structurellement identiques dans les trois arbres | logique finale d'unification | exclure ; aucun remplacement d'objet |

Les groupes progression explicite, variables, états, frontières, modificateurs,
tooltips, délais et effets hebdomadaires absents d'un objet ne sont pas créés ni
importés. Les régions, cultures, pays, scopes, événements, effets immédiats,
effets de complétion, récompenses et pulses présents restent byte-identiques au
fork dans le patch théorique.

## 8. Asymétries trois voies

### `je_schleswig_holstein_question`

Fork et vanilla convergent fonctionnellement hors pinning. La source ajoute
deux filtres géographiques. Ces différences source sont exclues.

### `je_german_unification_idea`

Les trois versions divergent dans `on_complete`. La source refactore la
sélection par prestige ; la vanilla modernise les itérateurs de confédération ;
le fork conserve ses itérateurs historiques. Aucun hunk adjacent n'est admis.

### `je_north_german_unification`

Source et vanilla convergent sur l'itérateur de candidat dans `complete`, face
au fork. Cette convergence n'autorise ni import ni remplacement d'objet.

### `je_south_german_unification`

La même convergence source/vanilla existe dans `complete` et reste exclue.

### `je_german_unification`

Tous les champs adjacents sont structurellement identiques entre les trois
arbres. La seule différence fonctionnelle est le pinning ; la source et la
vanilla ajoutent aussi une ligne blanche avant celui-ci. Le patch reste limité
au nom de propriété et n'importe pas cette présentation.

## 9. Exclusions absolues

Le patch théorique exclut progression, conditions de formation et de création,
visibilité, géographie, régions stratégiques ou géographiques, états,
frontières, cultures, pays, sujets, variables, scopes, événements, effets,
récompenses, modificateurs, tooltips, icônes, groupes, délais et poids.

Il ne remplace ni le fichier ni aucun objet. Une convergence source/vanilla
n'est jamais utilisée comme autorisation d'import.

## 10. Patch théorique en mémoire

Pour chacun des cinq objets, le seul hunk est :

```diff
-	should_be_pinned_by_default = yes
+	should_be_pinned_by_default_uninvolved_or_context = yes
```

Les cinq contextes minimaux sont identiques dans leur structure :

```text
je_schleswig_holstein_question @ 105
je_german_unification_idea @ 275
je_north_german_unification @ 333
je_south_german_unification @ 394
je_german_unification @ 447

	weight = 1000
	should_be_pinned_by_default_uninvolved_or_context = yes
}
```

| Mesure théorique | Résultat |
|---|---|
| fichiers | 1 |
| objets | 5 |
| hunks | 5 |
| diff | `5+/5-` |
| SHA-256 final | `30A3F3356AA43060C0E8D315DDF34D8D304680290134E0212AE6AEB852C8F239` |
| taille finale | 9 527 octets |
| delta de taille | +110 octets |
| lignes | 448 |
| fins de ligne | 448 LF, 0 CRLF |
| BOM UTF-8 | conservé |
| ancienne propriété après | 0 |
| nouvelle propriété après | 5 |
| autres octets modifiés | 0 |

Le remplacement inverse restitue byte à byte l'entrée, au SHA-256 :

`A52D4525DED1BE8F804CEEDD99329E03EAABB9E53376D04F4BBE9A8CDC32EC22`

## 11. Réponses aux questions de décision

1. Oui, les cinq diagnostics frais correspondent exactement aux cinq lignes.
2. Oui, les cinq objets existent dans les trois arbres.
3. Oui, source et vanilla convergent sur la nouvelle propriété dans chacun.
4. Oui, toutes les propriétés sont à profondeur racine 1.
5. Oui, elles sont terminales après `weight` et indépendantes des voisins.
6. Oui, aucun autre diagnostic frais ne concerne le fichier.
7. Oui, toutes les différences fonctionnelles adjacentes restent exclues.
8. Oui, le patch reste limité à un fichier, cinq objets et cinq substitutions.
9. Oui, le hash théorique est reproductible.
10. Oui, l'inversion restitue exactement le hash d'entrée.
11. Non, le remplacement API isolé ne nécessite aucun choix humain de design.
12. Oui, une seule ouverture humaine ultérieure pourra mesurer `5 → 0` au
    chargement, sans forcer l'apparition des journal entries ; aucune validation
    UI ne devra être revendiquée si elles ne sont pas naturellement visibles.

## 12. Décision d'atomicité et phase suivante

Toutes les conditions de sélection passent. La phase suivante est donc :

```text
HOTFIX_6A24F_GERMAN_UNIFICATION_FIVE_JE_PINNING_1_13_ALIGNMENT
```

6A.24F n'est pas commencée. Elle devra appliquer exactement le patch théorique
ci-dessus, vérifier le hash final et ne sélectionner qu'ensuite une QA runtime
humaine unique. Aucun autre hunk ne lui est autorisé.

## 13. Fichiers documentaires et état final

Les seuls documents autorisés de 6A.24 sont le présent rapport, l'index, le
registre des rapports, la matrice des blocs, la feuille de route, l'unique ligne
allemande du registre résiduel et le prompt de 6A.24F. Aucun gameplay n'est
modifié, aucune correction n'est appliquée et aucun runtime n'est lancé.

L'index Git reste vide, le HEAD reste
`13fd3f946b9728b8e34702fed173127d8d2a4037`, aucun commit automatique n'est
créé et le stash NAVY-3C-3 reste intact au hash
`518df704fa14599c0f254fae13859210663dd976`.

```text
HOTFIX_6A24_GERMAN_UNIFICATION_FIVE_JE_PINNING_1_13_ALIGNMENT_AUDIT_COMPLETE
GERMAN_UNIFICATION_FIVE_JE_THREE_WAY_COMPARISON_COMPLETE
GERMAN_UNIFICATION_FIVE_JE_PINNING_DIAGNOSTICS_CONFIRMED
GERMAN_UNIFICATION_PINNING_AND_FUNCTIONAL_HUNKS_SEPARATED
GERMAN_UNIFICATION_FIVE_HUNK_THEORETICAL_PATCH_COMPUTED
NO_GAMEPLAY_CHANGED
NO_RUNTIME_REQUIRED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
GERMAN_UNIFICATION_FIVE_JE_PINNING_ATOMIC_ALIGNMENT_PROVEN
NEXT_EXECUTION_PHASE = HOTFIX_6A24F_GERMAN_UNIFICATION_FIVE_JE_PINNING_1_13_ALIGNMENT
```
