# Phase HOTFIX-6A.8F — Alignement Victoria 3 1.13 de la Grande Crise orientale

## Modèle recommandé

GPT-5.6 Thinking avec raisonnement élevé.

## Chemins

FORK :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`

SOURCE HOTFIX, STRICTEMENT EN LECTURE SEULE :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source`

VANILLA VICTORIA 3 1.13, STRICTEMENT EN LECTURE SEULE :

`C:\Games\Victoria 3 The Great Wave\game`

## Verdicts d’entrée requis

- `HOTFIX_6A8R_GREAT_EASTERN_CRISIS_1_13_AUDIT_COMPLETE`
- `GREAT_EASTERN_CRISIS_SIX_HUNK_DECISION_RECORDED`
- `NO_GAMEPLAY_CHANGED`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`
- `NEXT_EXECUTION_PHASE = HOTFIX_6A8F_GREAT_EASTERN_CRISIS_1_13_ALIGNMENT`

Rapport canonique :

`docs/reports/hotfix/_index/HOTFIX_6A8R_GREAT_EASTERN_CRISIS_1_13_AUDIT.md`

6A.8R doit avoir été commitée manuellement avant de commencer. Si le rapport,
les verdicts ou le commit manuel manquent, arrêter sans modifier le dépôt.

## Nature de la phase

6A.8F est une correction ciblée, puis une validation statique, suivie d’un
runtime exclusivement exécuté par l’opérateur humain.

Codex ne doit jamais :

- lancer Victoria 3 ou le launcher Paradox ;
- piloter l’interface du jeu ;
- utiliser une console de jeu ;
- analyser les logs avant la fermeture normale du jeu et du launcher ;
- remplacer le fichier gameplay complet ;
- modifier un objet autre que `je_great_eastern_crisis` ;
- commencer la phase suivante ;
- créer un commit automatique.

## Objectif unique

Aligner les six groupes fonctionnels validés par 6A.8R dans :

`common/journal_entries/05_great_eastern_crisis.txt`

Objet unique :

`je_great_eastern_crisis`

Classification des six groupes :

| Hunk | Décision |
| ---: | --- |
| 1 | `REQUIRED_1_13_ALIGNMENT` |
| 2 | `REQUIRED_1_13_ALIGNMENT` |
| 3 | `REQUIRED_1_13_ALIGNMENT` |
| 4 | `REQUIRED_1_13_ALIGNMENT` |
| 5 | `REQUIRED_1_13_ALIGNMENT` |
| 6 | `REQUIRED_1_13_ALIGNMENT` |

Décision atomique : option A. Aucun sous-ensemble n’est autorisé.

## Préflight obligatoire

Avant toute modification :

1. confirmer la racine exacte du fork ;
2. confirmer la branche `hotfix-dlc-audit` ;
3. relever le HEAD initial et son sujet ;
4. confirmer que 6A.8R et ses verdicts sont dans le HEAD ;
5. confirmer que le HEAD annonce bien 6A.8F comme prochaine phase ;
6. relever `git status --short`, l’index staged et `git diff --check` ;
7. préserver tout travail utilisateur déjà présent ;
8. confirmer le stash exact sans l’appliquer ni l’inspecter :
   `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` ;
9. confirmer l’absence de processus Victoria 3 ou Paradox ;
10. calculer les hashes protégés avant toute écriture ;
11. confirmer les trois hashes gameplay d’entrée ci-dessous ;
12. si une condition manque, arrêter sans écrire.

## Hashes gameplay d’entrée

Le fichier gameplay doit être lu intégralement dans les trois arbres.

| Arbre | SHA-256 attendu |
| --- | --- |
| Fork | `77E6FE839DDFF0CC4A33102D284186FFB440434FA9960DC20B316A721ED3A3A4` |
| Source hotfix | `269CD001D5DE0D04CC53F2077B66BEBA76A9E4A4C6D1253E3DE4DF816098E808` |
| Vanilla 1.13 | `55237D5C08DE84CFCBE266DC92DF18C56FAF818C28DCE2B8CB69A4A25C44809D` |

La source et vanilla doivent rester inchangées pendant toute la phase.

## Sources obligatoires

Lire intégralement avant correction :

- `HOTFIX_6A8R_GREAT_EASTERN_CRISIS_1_13_AUDIT.md` ;
- `HOTFIX_6A7F_GREEK_NATIONALISM_1_13_API_ALIGNMENT.md` ;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- `HOTFIX_REPORT_INDEX.csv` ;
- les changelogs actuels du fork et de la source hotfix ;
- les nouveaux logs 6A.7F et leurs rotations, uniquement en lecture seule ;
- les trois versions intégrales de
  `common/journal_entries/05_great_eastern_crisis.txt`.

Vérifier aussi, en lecture seule, les définitions héritées de
`geographic_region_balkans_old`, `geographic_region_megali_greece`,
`sr:region_balkans`, `sr:region_near_east` et
`country_has_interest_marker_in_great_eastern_crisis_region`. Ne modifier
aucune région ni aucun scripted trigger.

## Périmètre d’écriture fermé

Gameplay autorisé :

1. `common/journal_entries/05_great_eastern_crisis.txt`

Documents autorisés :

2. `docs/reports/hotfix/_index/HOTFIX_6A8F_GREAT_EASTERN_CRISIS_1_13_ALIGNMENT.md`
3. `docs/reports/hotfix/INDEX.md`
4. `docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv`
5. `docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv`
6. `docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md`
7. `docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`

Tout autre chemin est interdit.

## Correction exacte

Appliquer des hunks ciblés. Ne pas copier ni remplacer le fichier complet.

### Hunk 1 — région du sujet

Dans `should_be_involved > OR > any_subject_or_below`, remplacer :

```txt
is_in_geographic_region = geographic_region_balkans
```

par :

```txt
is_in_geographic_region = geographic_region_balkans_old
```

### Hunk 2 — région du pays

Dans `should_be_involved > OR`, remplacer la seconde occurrence territoriale :

```txt
is_in_geographic_region = geographic_region_balkans
```

par :

```txt
is_in_geographic_region = geographic_region_balkans_old
```

Ne pas confondre les deux occurrences : la première évalue un sujet, la
seconde le pays lui-même.

### Hunk 3 — scope stratégique typé

Dans la branche russe de `should_be_involved`, remplacer :

```txt
has_interest_marker_in_region = region_balkans
```

par :

```txt
has_interest_marker_in_region = sr:region_balkans
```

### Hunk 4 — visibilité hors implication

Insérer au niveau racine, immédiatement après `should_be_involved`, exactement :

```txt
	should_show_when_not_involved = {
		OR = {
			is_in_geographic_region = geographic_region_balkans_old
			is_in_geographic_region = geographic_region_megali_greece # Proxy for Anatolia
			country_has_interest_marker_in_great_eastern_crisis_region = yes
            top_overlord ?= {
                capital = {
					OR = {
						is_in_geographic_region = geographic_region_balkans_old
						is_in_geographic_region = geographic_region_megali_greece
					}
                }
            }
		}
	}
```

Conserver exactement les scopes optionnels, les commentaires et l’imbrication.

### Hunk 5 — héritage révolutionnaire

Au niveau racine, après :

```txt
transferable = no
```

ajouter :

```txt
can_revolution_inherit = yes
```

### Hunk 6 — pinning impliqué et contextuel

Remplacer :

```txt
should_be_pinned_by_default = yes
```

par :

```txt
should_be_pinned_by_default_involved = yes
should_be_pinned_by_default_uninvolved_or_context = no
```

## Contraintes de format

- conserver UTF-8 avec BOM ;
- conserver les fins de ligne LF ;
- conserver le saut final ;
- conserver la ligne blanche initiale du fork après l’ouverture de l’objet ;
- conserver une ligne blanche après le nouveau bloc de pinning ;
- cette ligne blanche doit être réellement vide, sans tabulation ;
- ne pas importer la ligne blanche tabulée de vanilla ;
- ne reformater aucune ligne hors hunks ;
- ne modifier aucun commentaire existant.

## Résultat statique exact attendu

Après correction, le fichier doit présenter :

- SHA-256 :
  `96F65E2B3CC7129DD8D4AD41382F9F8DD97FB5FA24C66C05F129B1E31615F75A` ;
- 7 995 octets ;
- UTF-8 avec BOM ;
- 335 LF ;
- 0 CRLF ;
- saut final présent ;
- 109 accolades ouvrantes et 109 fermantes ;
- profondeur finale 0 ;
- profondeur minimale 0 ;
- objet unique de la ligne 1 à la ligne 335.

Le diff gameplay propre doit contenir exactement :

- 1 fichier ;
- 1 objet ;
- 6 groupes fonctionnels ;
- 2 blocs `@@` dans le diff unifié ;
- 23 additions ;
- 4 suppressions ;
- gain net de 19 lignes ;
- aucune autre différence.

La différence source/vanilla d’une seule ligne blanche initiale est connue et
ne doit pas être « corrigée ».

## Validation statique obligatoire

Avant de demander le runtime :

1. recalculer le hash, la taille, le BOM et les fins de ligne ;
2. recompter les accolades et vérifier la profondeur ;
3. produire le diff ciblé du fichier ;
4. confirmer les six groupes et seulement eux ;
5. confirmer les deux blocs `@@`, 23 additions et 4 suppressions ;
6. confirmer l’absence de l’ancien pinning dans l’objet ;
7. confirmer les deux nouvelles propriétés une fois chacune ;
8. confirmer deux occurrences territoriales de
   `geographic_region_balkans_old` dans `should_be_involved` ;
9. confirmer `sr:region_balkans` dans le marqueur d’intérêt ;
10. confirmer le bloc `should_show_when_not_involved` exact ;
11. confirmer `can_revolution_inherit = yes` ;
12. confirmer qu’aucune localisation n’est nécessaire ;
13. confirmer que les hashes source et vanilla n’ont pas changé ;
14. exécuter `git diff --check` ;
15. confirmer que l’index staged est vide ;
16. confirmer que les protections et le stash sont intacts.

Si le hash final ou le comptage exact ne correspond pas, corriger uniquement
les hunks autorisés. Ne pas demander le runtime tant que le statique n’est pas
parfait.

## Arrêt obligatoire avant runtime

Après passage statique, Codex doit s’arrêter et rendre exactement le marqueur :

`RUNTIME_OPERATOR_ACTION_REQUIRED`

Codex remet alors la fiche suivante à l’opérateur humain. Il ne lance rien.

## Fiche de test pour l’opérateur humain

Un seul lancement :

1. ouvrir le launcher ;
2. confirmer que le fork et `dlc014_ip3` sont montés ;
3. lancer une partie neuve en 1776 avec l’Empire ottoman ;
4. ouvrir `Journal > Potentiel` ;
5. ouvrir `Grande Crise orientale` ;
6. vérifier que le titre, le texte et les conditions sont lisibles ;
7. vérifier qu’aucune clé brute n’apparaît ;
8. vérifier l’absence d’anomalie visible de pinning ;
9. confirmer que l’Empire ottoman est traité comme impliqué ;
10. dans la même session et sans console, utiliser le changement de pays
    standard si disponible vers un observateur possédant un intérêt dans les
    Balkans ou le Proche-Orient ;
11. vérifier que l’entrée est visible contextuellement pour cet observateur ;
12. vérifier qu’elle n’est pas épinglée automatiquement chez cet observateur ;
13. avancer d’au moins un jour ;
14. noter la date atteinte et toute anomalie ;
15. fermer normalement le jeu ;
16. fermer normalement le launcher ;
17. seulement ensuite transmettre les observations à Codex.

Ne pas provoquer artificiellement une révolution. L’héritage révolutionnaire
reste couvert par la preuve statique et le smoke global final.

## Analyse des logs après retour humain

Uniquement après confirmation que le jeu et le launcher sont fermés :

1. identifier les nouveaux logs et les séparer des rotations anciennes ;
2. confirmer que le fork et `dlc014_ip3` étaient montés ;
3. rechercher le chemin
   `common/journal_entries/05_great_eastern_crisis.txt` ;
4. confirmer que l’erreur ciblée
   `should_be_pinned_by_default` passe de 1 à 0 ;
5. confirmer zéro erreur sur
   `should_be_pinned_by_default_involved` ;
6. confirmer zéro erreur sur
   `should_be_pinned_by_default_uninvolved_or_context` ;
7. documenter tout autre diagnostic propre au fichier ;
8. ne pas attribuer à 6A.8F les erreurs historiques ou étrangères au fichier.

Le total global historique de 387 anciens diagnostics de pinning devrait
descendre à 386 dans une session comparable, mais seul le passage ciblé de 1 à
0 constitue le critère obligatoire.

## Rapport de phase

Créer :

`docs/reports/hotfix/_index/HOTFIX_6A8F_GREAT_EASTERN_CRISIS_1_13_ALIGNMENT.md`

Le rapport doit distinguer :

- préflight ;
- correction exacte ;
- validation statique ;
- pause `RUNTIME_OPERATOR_ACTION_REQUIRED` ;
- observations humaines ;
- analyse des nouveaux logs ;
- hashes avant/après ;
- diff exact ;
- protections ;
- état Git final ;
- verdicts.

Ne déclarer le runtime passé qu’après réception des observations humaines et
analyse des logs post-fermeture.

## Livrables exacts

À la clôture complète de 6A.8F, livrer :

1. le seul fichier gameplay ciblé, avec le hash final attendu ;
2. le rapport canonique 6A.8F ;
3. les cinq documents canoniques synchronisés ;
4. la preuve statique exacte ;
5. le compte rendu de l’opérateur humain ;
6. l’analyse des nouveaux logs après fermeture ;
7. l’état Git final et la confirmation d’absence de commit automatique.

## Mise à jour documentaire après runtime

Mettre à jour uniquement les cinq documents canoniques autorisés :

- `docs/reports/hotfix/INDEX.md` ;
- `HOTFIX_REPORT_INDEX.csv` ;
- `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

Le prompt suivant doit préparer une phase de sélection documentaire et ne doit
pas commencer de nouveau correctif.

## Rollback exact

Si le rollback de 6A.8F devient nécessaire :

1. remplacer les deux `_old` du bloc `should_be_involved` par
   `geographic_region_balkans` ;
2. remplacer `sr:region_balkans` par `region_balkans` ;
3. supprimer exactement `should_show_when_not_involved` ;
4. supprimer `can_revolution_inherit = yes` ;
5. remplacer les deux propriétés de pinning par
   `should_be_pinned_by_default = yes`.

Le rollback doit être ciblé. Ne jamais restaurer le fichier complet.

## Protections absolues

Ne pas toucher : 6A.3F à 6A.8R, DEI/VOC, Java, Balkan National Awakening,
Yugoslavia, Risorgimento, nationalisme grec, Coup, Imperialism of Promise,
Merchant Banking, Navigation Acts, NAVY, formations, MARATH, SAT, KHP,
Travancore, Inde, BIC, Sepoy, Bombay, ADMIN, Japon, Russie, Autriche, Croatie,
Slavonie, Suisse, révolutions américaine et française, lettres de Kew,
technologies, agriculture, alimentation, industrie, localisations générales,
descripteurs, launcher, sauvegardes et `bject`.

Préserver les huit hashes protégés consignés dans 6A.8R. Préserver
`law_frontier_colonization` pour BIC et ne pas restaurer
`law_colonial_exploitation`.

## Interdictions Git

- aucun commit automatique ;
- aucun amend ;
- aucun merge ou rebase ;
- aucun stash apply/pop/drop ;
- aucun reset, restore, checkout ou clean ;
- aucune suppression du travail non suivi ;
- aucun lancement de la phase suivante.

## Vérifications finales

Avant de clore la phase :

1. confirmer exactement un fichier gameplay modifié ;
2. confirmer exactement les six documents de phase modifiés ou créés ;
3. confirmer le hash final gameplay attendu ;
4. confirmer que source hotfix et vanilla sont inchangées ;
5. confirmer les six groupes fonctionnels et aucune autre différence ;
6. confirmer les deux blocs `@@`, 23 additions et 4 suppressions ;
7. confirmer les accolades, le BOM, les LF et le saut final ;
8. confirmer zéro localisation ajoutée ou modifiée ;
9. confirmer les huit hashes protégés ;
10. confirmer le stash NAVY-3C-3 intact ;
11. confirmer l’index staged vide ;
12. confirmer `git diff --check` propre ;
13. confirmer les CSV valides, à 22 et 17 colonnes respectivement ;
14. confirmer que Victoria 3 et le launcher sont fermés ;
15. confirmer que Codex n’a lancé ni contrôlé le jeu ;
16. confirmer que le runtime repose sur les observations humaines ;
17. confirmer qu’aucun commit automatique n’a été créé ;
18. publier `git status --short`, `git diff --name-only`,
    `git diff --name-status` et `git diff --stat`.

## Verdicts finaux visés

Après statique et runtime humain réellement passés :

- `HOTFIX_6A8F_GREAT_EASTERN_CRISIS_1_13_STATIC_PASS`
- `HOTFIX_6A8F_GREAT_EASTERN_CRISIS_1_13_RUNTIME_PASS`
- `GREAT_EASTERN_CRISIS_SIX_HUNK_1_13_ALIGNMENT_COMPLETE`
- `GREAT_EASTERN_CRISIS_GEOGRAPHY_VISIBILITY_AND_PINNING_VALIDATED`
- `HOTFIX_6A8F_GREAT_EASTERN_CRISIS_1_13_ALIGNMENT_COMPLETE`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`

La phase doit ensuite annoncer une nouvelle sélection documentaire, sans
l’exécuter.
