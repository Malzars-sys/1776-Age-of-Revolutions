# HOTFIX-6A.5 — Sélection du prochain résidu global

Date : 29 juillet 2026

Phase : `HOTFIX_6A5_RESIDUAL_GLOBAL_SCRIPT_SELECTION`

## 1. Verdict

La phase documentaire est complète.

- `HOTFIX_6A5_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE`
- `NO_GAMEPLAY_CHANGED`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`
- `NEXT_EXECUTION_PHASE = HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_ALIGNMENT`

Le prochain sous-bloc sélectionné est l’alignement de l’API de pinning de
`je_yugoslavia`, dans
`common/journal_entries/05_creation_of_yugoslavia.txt`.

## 2. État Git initial

Contrôles effectués avant toute modification :

- racine :
  `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork` ;
- branche : `hotfix-dlc-audit` ;
- HEAD : `4d00be1 Align Balkan National Awakening with Victoria 3 1.13` ;
- rapport 6A.4F présent dans HEAD ;
- aucun fichier suivi modifié ;
- index Git vide ;
- `git diff --check` propre ;
- huit fichiers non suivis seulement : `bject` et les sept fichiers de
  `docs/research/technology/` ;
- stash intact :
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` ;
- Victoria 3 et le launcher Paradox fermés.

Aucun reset, restore, checkout de fichier, clean, merge, commit automatique,
stash apply/pop/drop ou inspection du contenu du stash n’a été effectué.

## 3. Sources consultées

Les sources canoniques suivantes ont été lues :

- `HOTFIX_6A4F_BALKAN_NATIONAL_AWAKENING_1_13_ALIGNMENT.md` ;
- `HOTFIX_6A4_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md` ;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- `HOTFIX_REPORT_INDEX.csv` ;
- les 534 lignes de `HOTFIX_GLOBAL_DIFFERENCE_INVENTORY.csv` ;
- `HOTFIX_C1AI_CONCURRENT_WORK_RECONCILIATION.md` ;
- les changelogs du fork et de la source hotfix ;
- les derniers `error.log`, `game.log`, `debug.log` et leurs rotations issus de
  la session 6A.4F, arrêtée le 29 juillet 2026 à 00:21:19.

Les candidats ont été comparés dans le fork, la source hotfix en lecture seule
et le vanilla Victoria 3 1.13 en lecture seule.

## 4. Inventaire canonique et actualisation

L’inventaire global contient toujours 534 différences fonctionnelles :

| Statut brut de l’inventaire | Nombre |
|---|---:|
| `CONCURRENT_USER_WORK` | 16 |
| `INTENTIONAL_FORK_DIVERGENCE` | 268 |
| `MERGED_AND_VALIDATED` | 2 |
| `MERGED_STATIC_ONLY` | 66 |
| `OBSOLETE_HOTFIX_CONTENT` | 20 |
| `PENDING_IMPORT` | 1 |
| `PENDING_REVIEW` | 161 |
| **Total** | **534** |

La classification manuelle des 161 anciennes lignes `PENDING_REVIEW` est
actualisée après la clôture balkanique :

| Catégorie exclusive | Nombre |
|---|---:|
| `REQUIRED_HOTFIX_DELTA` | 7 |
| `VANILLA_1_13_ALIGNMENT_REQUIRED` | 21 |
| `ALREADY_MERGED` | 13 |
| `INTENTIONAL_FORK_DIVERGENCE` | 3 |
| `OBSOLETE_HOTFIX_CONTENT` | 1 |
| `POST_MERGE_DESIGN_BACKLOG` | 10 |
| `PROTECTED_CONCURRENT_WORK` | 19 |
| `UNKNOWN_REQUIRES_REVIEW` | 87 |
| **Total** | **161** |

Le fichier balkanique passe de `VANILLA_1_13_ALIGNMENT_REQUIRED` à
`ALREADY_MERGED`. Il ne réapparaît pas parmi les résidus exécutables.

Il reste donc 115 lignes directement exploitables par une future revue
d’exécution : 7 deltas hotfix requis, 21 alignements vanilla 1.13 et 87
inconnus à examiner. Ce nombre ne signifie pas 115 correctifs.

L’ancien total de 26 deltas à haute confiance reste `UNVERIFIED` : aucun
registre canonique de 26 lignes exactes ne le démontre.

## 5. Mesure des diagnostics runtime existants

Aucun jeu ni launcher n’a été ouvert pendant 6A.5. L’analyse porte uniquement
sur les journaux déjà produits par l’opérateur pendant 6A.4F.

### 5.1 Résidu balkanique clos

Les références propres à `05_balkan_national_awakening.txt` sont nulles dans
les journaux de fin de session. Les 51 erreurs antérieures restent donc closes.

### 5.2 Comparaisons `sr` invalides

Les rotations contiennent 14 672 occurrences de
`Invalid right side during comparison 'sr'` :

| Chemin | Occurrences | Classement |
|---|---:|---|
| `common/journal_entries/01_natural_borders_of_france.txt` | 11 983 | divergence/backlog France, exclu |
| `common/journal_entries/00_major_railroads.txt` | 2 096 | divergence intentionnelle, exclu |
| `common/journal_entries/07_american_mod_jes.txt` | 176 | travail Amérique protégé/backlog, exclu |
| `common/scripted_buttons/00_new_colonial_admins.txt` | 146 | Inde/BIC/ADMIN protégé, exclu |
| `common/ai_strategies/00_default_strategy.txt` | 130 | divergence intentionnelle, exclu |
| `common/journal_entries/02_south_america_migration.txt` | 120 | divergence intentionnelle, exclu |
| `common/dynamic_country_names/00_dynamic_country_names.txt` | 21 | noms des présidences indiennes protégés, exclu |

La répétition ne suffit pas à autoriser une correction : toutes ces familles
appartiennent à un bloc protégé, un backlog ou une divergence documentée.

### 5.3 Ancienne API de pinning

Le `debug.log` et ses rotations contiennent 390 erreurs de parsing liées à
`should_be_pinned_by_default`. Les familles les plus répétées sont notamment
le tutoriel (52), les objectifs joueur, les biens de prestige, la Russie
protégée, `sick_man` (8) et plusieurs autres fichiers hors sélection.

Parmi les 21 alignements 1.13 encore ouverts, les six fichiers où l’ancienne
propriété n’apparaît qu’une fois sont :

- `00_greek_nationalism.txt` ;
- `00_italian_unification.txt` ;
- `01_coup.txt` ;
- `04_imperialism_of_promise.txt` ;
- `05_creation_of_yugoslavia.txt` ;
- `05_great_eastern_crisis.txt`.

Le journal existant contient exactement l’erreur ciblée suivante :

```text
Error: "Unexpected token: should_be_pinned_by_default, near line: 144" in file: "common/journal_entries/05_creation_of_yugoslavia.txt" near line: 144
```

## 6. Exclusions et protections

Sont exclus de cette sélection et de la future exécution :

- DEI/VOC, Java et l’économie post-compagnie ;
- `05_balkan_national_awakening.txt`, désormais clos ;
- NAVY, formations, lois et technologies navales ;
- MARATH, SAT, KHP et Travancore ;
- Inde, BIC, Sepoy, Bombay et noms dynamiques des présidences ;
- ADMIN, Japon, Russie, Autriche, Croatie, Slavonie et Suisse ;
- Révolutions américaine et française, ainsi que les lettres de Kew ;
- technologies et `docs/research/technology/` ;
- localisations françaises générales ;
- agriculture, alimentation et industrie générales ;
- descripteurs, launcher, sauvegardes et `bject`.

`activate_law = law_type:law_frontier_colonization` reste protégé. La loi
`law_colonial_exploitation` ne doit jamais être restaurée pour BIC.

## 7. Classement des candidats

Chaque candidat ci-dessous est classé dans une seule catégorie :

| Rang | Phase candidate | Fichiers | Objets | Priorité | Preuve | Collision | Runtime |
|---:|---|---:|---:|---|---|---|---|
| 1 | `HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_ALIGNMENT` | 1 | 1 | P0 | erreur de parsing directe ; hotfix et vanilla convergent | très faible | requis, opérateur humain — **sélectionné** |
| 2 | Merchant Banking GEN/VEN | 2 | 2 | P1 | changelog 2.3 et source hotfix ; tags custom absents du vanilla | faible | requis, opérateur humain — différé |
| 3 | Navigation Acts GBR/HBC/NBS/ONT/ORA | 5 | 5 | P1 | changelog 2.3 et source hotfix ; activations custom absentes du vanilla | moyenne, surtout GBR/NAVY | requis, opérateur humain — différé |

La future phase 6A.5F prévoit exactement un hunk. Merchant Banking en prévoit
deux et Navigation Acts au moins cinq.

### 7.1 Merchant Banking, comparaison trois voies

Dans GEN et VEN, le fork active encore `law_traditionalism` au point où la
source hotfix active `law_merchant_banking`. Les historiques vanilla
correspondants n’existent pas, car ces tags sont propres au mod. Le changelog
hotfix 2.3 annonce explicitement Merchant Banking pour les républiques
maritimes et la loi existe déjà dans le fork. La preuve fonctionnelle est
bonne, mais le paquet touche deux pays et exige une inspection humaine de
leurs lois initiales. Le nom spécifique des propriétaires terriens est une
décision distincte et ne doit pas être mélangé à ces deux hunks.

### 7.2 Navigation Acts, comparaison trois voies

Le fork n’active pas `law_mercantilism_navigation_acts` dans GBR, HBC, NBS,
ONT et ORA, tandis que la source hotfix l’ajoute aux cinq historiques. Le
vanilla n’apporte pas ces activations custom. Le changelog hotfix 2.3 prouve
l’intention, mais le paquet exige cinq hunks, le fichier GBR contient de
nombreux autres écarts et son voisinage augmente le risque de collision avec
les travaux NAVY. BIC est explicitement exclue.

## 8. Pourquoi `je_yugoslavia` est sélectionnée

Le candidat satisfait simultanément les critères d’atomicité et de preuve :

- le fork emploie encore l’API refusée par le parseur ;
- la source hotfix et le vanilla 1.13 emploient tous deux
  `should_be_pinned_by_default_uninvolved_or_context = yes` ;
- une erreur runtime désigne directement le fichier et la ligne ;
- une seule occurrence est concernée ;
- le changement est indépendant des travaux protégés ;
- le rollback est une inversion d’une seule ligne.

Les autres entrées à occurrence unique sont moins sûres :

- `00_greek_nationalism.txt` contient aussi une dette d’API de loi ;
- `00_italian_unification.txt` contient une divergence 1776 intentionnelle ;
- `01_coup.txt` et `04_imperialism_of_promise.txt` comportent plusieurs autres
  écarts ;
- `05_great_eastern_crisis.txt` emploie dans la source et le vanilla des
  valeurs contextuelles différentes d’un simple remplacement par `yes`.

## 9. Comparaison trois voies du choix

Objet fermé : `je_yugoslavia`.

Dans le fork :

```txt
should_be_pinned_by_default = yes
```

Dans la source hotfix et le vanilla 1.13 :

```txt
should_be_pinned_by_default_uninvolved_or_context = yes
```

La source hotfix ajoute par ailleurs
`is_in_geographic_region = geographic_region_balkans` dans
`is_shown_when_inactive`. Cet ajout n’est pas présent dans le vanilla 1.13 et
n’est pas requis pour corriger l’erreur d’API. Il est explicitement exclu de
6A.5F.

## 9.1 Priorité, dépendances et collision

Priorité : P0, car le moteur signale directement une API refusée dans le
fichier cible.

Dépendances :

- l’API `should_be_pinned_by_default_uninvolved_or_context` fournie par
  Victoria 3 1.13 ;
- aucune nouvelle localisation ;
- aucune dépendance de loi, de technologie, d’événement ou de géographie ;
- une validation runtime humaine après les contrôles statiques.

Risque de collision : très faible. Le chemin ne croise aucun fichier protégé
et le diff autorisé tient sur une ligne. Le seul risque identifié serait
l’import accidentel de la condition géographique propre à la source hotfix ;
elle est donc explicitement interdite.

## 10. Périmètre fermé de la future phase

Phase :
`HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_ALIGNMENT`.

Seul fichier gameplay modifiable :

```text
common/journal_entries/05_creation_of_yugoslavia.txt
```

Seul objet modifiable :

```text
je_yugoslavia
```

Seul hunk gameplay autorisé :

```diff
-    should_be_pinned_by_default = yes
+    should_be_pinned_by_default_uninvolved_or_context = yes
```

Aucune condition géographique, condition d’activation, durée, effet,
localisation ou autre propriété de l’entrée ne peut être modifiée.

## 11. Validation statique requise en 6A.5F

La future phase devra vérifier avant tout runtime :

1. une seule définition de `je_yugoslavia` ;
2. accolades équilibrées ;
3. zéro ancienne propriété de pinning dans l’objet ;
4. exactement une nouvelle propriété avec la valeur `yes` ;
5. présence de cette propriété dans la source hotfix et le vanilla 1.13 ;
6. aucune modification de la géographie ;
7. diff gameplay réduit au hunk exact ;
8. aucun autre fichier gameplay modifié ;
9. `git diff --check` propre ;
10. index Git vide.

## 12. Runtime futur réservé à l’opérateur humain

Codex ne doit jamais lancer, piloter ni fermer Victoria 3 ou le launcher.
Après le passage statique de 6A.5F, Codex doit s’arrêter avec :

`RUNTIME_OPERATOR_ACTION_REQUIRED`

L’opérateur humain recevra alors une fiche de session indiquant :

1. lancer le fork par le launcher habituel ;
2. confirmer visuellement que le fork est monté ;
3. charger une partie neuve 1776 ;
4. choisir un pays balkanique valide permettant d’observer l’entrée, si
   disponible ; la Valachie est acceptable seulement si les conditions
   affichées rendent l’entrée pertinente ;
5. ouvrir Journal > Potentiel et contrôler « Création de la Yougoslavie » si
   elle est accessible ;
6. vérifier l’absence de clé brute, la lisibilité des conditions et l’absence
   d’anomalie de pinning ;
7. laisser passer au moins un jour en jeu ;
8. fermer le jeu et le launcher ;
9. transmettre à Codex les observations et, si possible, une capture ;
10. laisser Codex analyser ensuite `error.log`, `game.log`, `debug.log` et
    leurs rotations sans relancer le jeu.

Si l’entrée est inaccessible pour le pays/scénario, l’opérateur doit le
signaler sans forcer un autre changement gameplay. La disparition de l’erreur
de parsing ciblée dans une session où le fork est positivement monté reste la
preuve runtime minimale.

## 13. Rollback

En cas de régression, rétablir uniquement :

```txt
should_be_pinned_by_default = yes
```

Puis refaire les contrôles statiques. Aucun fichier complet ne doit être
remplacé depuis la source hotfix ou le vanilla.

## 14. Fichiers modifiés par 6A.5

Documentation uniquement :

- `HOTFIX_6A5_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md` ;
- `docs/reports/hotfix/INDEX.md` ;
- `HOTFIX_REPORT_INDEX.csv` ;
- `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

Zéro fichier gameplay a été modifié.

## 15. Contrôles documentaires

- exactement trois candidats publiés ;
- exactement un candidat sélectionné ;
- fichier balkanique clos non réintroduit ;
- catégories et totaux cohérents : 534 lignes globales, 161 anciennes lignes
  de revue, 115 lignes encore directement exploitables ;
- périmètre futur fermé à un fichier, un objet et un hunk ;
- protections absolues conservées ;
- runtime futur explicitement réservé à l’opérateur humain.

## 16. État Git final et commit

Les contrôles finaux constatent :

- HEAD inchangé à `4d00be1` ;
- exactement les six documents autorisés modifiés ou créés ;
- zéro diff gameplay ;
- `git diff --check` propre, y compris pour le nouveau rapport non suivi ;
- aucun fichier staged ;
- aucun commit automatique ;
- `bject` et les sept recherches technologiques non suivis, avec les huit
  empreintes SHA-256 identiques au préflight ;
- stash NAVY-3C-3 intact ;
- zéro processus Victoria 3 et zéro processus launcher Paradox.

Décision : ne rien committer automatiquement. Le commit de 6A.5 reste une
action manuelle ultérieure.
