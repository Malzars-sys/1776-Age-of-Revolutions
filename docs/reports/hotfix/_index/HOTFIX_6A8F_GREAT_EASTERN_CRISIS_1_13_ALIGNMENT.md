# HOTFIX-6A.8F — Alignement Victoria 3 1.13 de la Grande Crise orientale

## 1. Identification

- Date : 29 juillet 2026.
- Phase : `HOTFIX_6A8F_GREAT_EASTERN_CRISIS_1_13_ALIGNMENT`.
- Branche : `hotfix-dlc-audit`.
- HEAD initial et courant :
  `da4b160326776c1a23492e0ef76308c41e126b22`.
- Commit d’entrée :
  `da4b160 Audit Great Eastern Crisis Victoria 3 1.13 alignment`.
- Objet unique : `je_great_eastern_crisis`.
- État : correction, validation statique et runtime humain terminés.

## 2. Préflight Git

Le préflight a passé toutes les conditions :

- 6A.8R est présente dans le HEAD et commitée manuellement ;
- ses cinq verdicts d’entrée sont présents ;
- le worktree suivi et l’index étaient propres ;
- seuls `bject` et les sept fichiers de
  `docs/research/technology/` étaient non suivis ;
- `git diff --check` était propre ;
- stash exact présent :
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` ;
- aucun processus Victoria 3, dowser ou Paradox.

État initial :

```text
?? bject
?? docs/research/technology/
```

## 3. Sources consultées

Ont été lus intégralement :

- rapport d’audit 6A.8R ;
- rapport runtime 6A.7F ;
- roadmap, état des blocs et index CSV ;
- changelogs du fork et de la source hotfix ;
- les 55 logs et rotations existants de 6A.7F, en lecture seule ;
- les trois versions intégrales du fichier gameplay ;
- les définitions vanilla des régions géographiques et stratégiques ;
- le scripted trigger d’intérêt de la Grande Crise orientale.

La source hotfix et vanilla sont restées strictement en lecture seule.

## 4. Hashes trois voies d’entrée

| Arbre | SHA-256 |
| --- | --- |
| Fork avant correction | `77E6FE839DDFF0CC4A33102D284186FFB440434FA9960DC20B316A721ED3A3A4` |
| Source hotfix | `269CD001D5DE0D04CC53F2077B66BEBA76A9E4A4C6D1253E3DE4DF816098E808` |
| Vanilla 1.13 | `55237D5C08DE84CFCBE266DC92DF18C56FAF818C28DCE2B8CB69A4A25C44809D` |

Les trois hashes correspondaient exactement à 6A.8R avant écriture.

## 5. Baseline runtime historique

Les nouveaux logs 6A.7F sont `debug.1.log` et `debug.log`.

| Diagnostic | Baseline |
| --- | ---: |
| Ancien pinning global | 387 |
| Chemin `05_great_eastern_crisis.txt` | 1 |
| Nouvelle propriété impliqué | 0 erreur |
| Nouvelle propriété contexte | 0 erreur |
| Autre erreur propre au fichier | 0 |

Occurrence ciblée :

```text
debug.log:365
Unexpected token: should_be_pinned_by_default, near line: 313
```

Cette baseline n’est pas une preuve runtime après correction. Aucun nouveau log
n’a été produit ou analysé pendant la partie statique de 6A.8F.

## 6. Snapshot avant correction

| Propriété | Valeur |
| --- | --- |
| Taille | 7 392 octets |
| Encodage | UTF-8 avec BOM |
| LF | 316 |
| CRLF | 0 |
| Saut final | présent |
| Accolades | 104 ouvrantes / 104 fermantes |
| Profondeur finale/minimale | 0 / 0 |
| Objet | lignes 1 à 316, fichier entier |

Le bloc `should_be_involved` contenait deux
`geographic_region_balkans`, un `region_balkans` non typé et aucun bloc de
visibilité hors implication. La racine contenait l’ancien pinning ligne 313,
`weight = 1000`, puis `transferable = no` sans héritage révolutionnaire.

## 7. Six groupes appliqués

| Hunk | Correction |
| ---: | --- |
| 1 | région du sujet : `geographic_region_balkans_old` |
| 2 | région du pays : `geographic_region_balkans_old` |
| 3 | marqueur russe : `sr:region_balkans` |
| 4 | ajout exact de `should_show_when_not_involved` |
| 5 | ajout de `can_revolution_inherit = yes` |
| 6 | pinning impliqué `yes`, non impliqué/contexte `no` |

Les hunks ont été édités localement. Aucun fichier complet n’a été remplacé et
aucune ligne hors périmètre n’a été reformattée.

## 8. Diff gameplay exact

```text
1 fichier
1 objet
6 groupes fonctionnels
2 blocs @@
23 additions
4 suppressions
gain net : 19 lignes
```

Blocs unifiés :

```text
@@ -9,16 +9,32 @@
@@ -310,7 +326,10 @@
```

La ligne blanche initiale du fork est conservée. La ligne blanche après le
nouveau pinning est réellement vide, sans tabulation.

## 9. Résultat statique

| Propriété | Résultat |
| --- | --- |
| SHA-256 | `96F65E2B3CC7129DD8D4AD41382F9F8DD97FB5FA24C66C05F129B1E31615F75A` |
| Taille | 7 995 octets |
| Encodage | UTF-8 avec BOM |
| LF | 335 |
| CRLF | 0 |
| Saut final | présent |
| Accolades | 109 ouvrantes / 109 fermantes |
| Profondeur finale/minimale | 0 / 0 |
| Objet | lignes 1 à 335, fichier entier |

Le résultat correspond byte pour byte au futur hash calculé par 6A.8R.

## 10. Validations statiques

- les deux occurrences territoriales de `should_be_involved` utilisent
  `geographic_region_balkans_old` ;
- la branche russe contient une occurrence de `sr:region_balkans` ;
- le bloc `should_show_when_not_involved` est présent une fois et conforme ;
- `can_revolution_inherit = yes` est présent une fois ;
- l’ancien pinning exact est absent ;
- chacune des deux nouvelles propriétés de pinning est présente une fois ;
- aucun besoin de localisation ;
- source hotfix et vanilla inchangées ;
- aucun autre fichier gameplay modifié ;
- aucun fichier staged ;
- `git diff --check` propre ;
- Victoria 3 et le launcher restent fermés.

## 11. Dépendances et impact 1776

Les dépendances héritées sont présentes :

- `geographic_region_balkans_old` ;
- `geographic_region_megali_greece` ;
- `sr:region_balkans` ;
- `sr:region_near_east` ;
- `country_has_interest_marker_in_great_eastern_crisis_region`.

L’Empire ottoman reste impliqué. La région historique étroite évite de classer
automatiquement la Valachie, la Moldavie et les États hongrois comme acteurs
balkaniques centraux, tout en permettant une visibilité contextuelle par
intérêt ou suzerain. Aucune phase balkanique close n’est rouverte.

## 12. Protections

Les huit hashes protégés sont identiques au préflight. `bject`, la recherche
technologique et le stash NAVY-3C-3 sont intacts. Aucun élément DEI/VOC, Java,
Balkan National Awakening, Yugoslavia, Risorgimento, nationalisme grec,
Merchant Banking, Navigation Acts, NAVY, formations, MARATH, Inde, ADMIN,
Japon, Russie, Autriche, Croatie, Suisse, révolutions, agriculture, industrie
ou localisation générale n’a été modifié.

BIC conserve `law_frontier_colonization` et
`law_colonial_exploitation` n’a pas été restaurée.

## 13. Rollback exact

1. remettre les deux occurrences de `geographic_region_balkans` dans
   `should_be_involved` ;
2. retirer `sr:` de la branche russe ;
3. supprimer exactement `should_show_when_not_involved` ;
4. supprimer `can_revolution_inherit = yes` ;
5. remplacer les deux nouvelles propriétés par
   `should_be_pinned_by_default = yes`.

Le rollback doit rester ciblé et ne doit jamais restaurer le fichier complet.

## 14. Fichiers de phase

Gameplay :

1. `common/journal_entries/05_great_eastern_crisis.txt`.

Documentation :

2. `HOTFIX_6A8F_GREAT_EASTERN_CRISIS_1_13_ALIGNMENT.md` ;
3. `docs/reports/hotfix/INDEX.md` ;
4. `HOTFIX_REPORT_INDEX.csv` ;
5. `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
6. `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
7. `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

## 15. Fiche opérateur

Un seul lancement humain :

1. monter le fork et `dlc014_ip3` ;
2. lancer une partie neuve en 1776 avec l’Empire ottoman ;
3. noter la date initiale ;
4. ouvrir `Journal > Potentiel > Grande Crise orientale` ;
5. vérifier titre, description, conditions, absence de clé brute et pinning ;
6. confirmer que l’Empire ottoman est impliqué et noter si l’entrée est
   automatiquement épinglée ;
7. prendre une capture si possible ;
8. sans console et dans la même session, utiliser le changement de pays
   standard si disponible vers un observateur non impliqué ayant un intérêt
   Balkans ou Proche-Orient ;
9. vérifier sa visibilité contextuelle et l’absence de pinning automatique ;
10. avancer d’au moins un jour ;
11. ne pas provoquer de révolution ;
12. noter la date finale ;
13. fermer normalement le jeu puis le launcher ;
14. confirmer explicitement leur fermeture et transmettre les observations.

Si le changement de pays standard est indisponible, le signaler sans second
lancement. L’héritage révolutionnaire reste couvert statiquement et par le
smoke global.

## 16. État Git final

Le HEAD reste
`da4b160326776c1a23492e0ef76308c41e126b22`. Aucun commit automatique n’est
créé. Après le runtime humain, le périmètre reste exactement un fichier
gameplay et six documents de phase.

```text
 M common/journal_entries/05_great_eastern_crisis.txt
 M docs/reports/hotfix/INDEX.md
 M docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv
 M docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md
 M docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md
 M docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv
?? bject
?? docs/reports/hotfix/_index/HOTFIX_6A8F_GREAT_EASTERN_CRISIS_1_13_ALIGNMENT.md
?? docs/research/technology/
```

## 17. Observations humaines

Session unique réalisée exclusivement par l’opérateur :

- pays initial : Empire ottoman ;
- date initiale : 1er janvier 1776 ;
- `Grande Crise orientale` visible dans `Journal > Potentiel` ;
- titre, texte et conditions lisibles ;
- aucune clé brute ;
- aucune anomalie visible de pinning ;
- Empire ottoman correctement présenté comme pays impliqué ;
- changement de pays standard vers la Grande-Bretagne dans la même session ;
- intérêts britanniques créés au Proche-Orient et dans les Balkans avant
  l’inspection du journal ;
- entrée ensuite visible contextuellement pour la Grande-Bretagne ;
- aucune clé brute et aucun pinning automatique chez l’observateur ;
- date finale : 8 avril 1776 ;
- jeu fermé normalement.

L’absence de processus Victoria 3, dowser ou Paradox après le retour confirme
également la fermeture du jeu et du launcher. Les captures fournies montrent
les deux vues et la progression temporelle.

## 18. Analyse des nouveaux logs

Les nouveaux logs sont datés du 29 juillet 2026 entre 16:06 et 16:24.

Preuves de montage :

```text
debug.1.log:53  National Awakening|dlc/dlc014_ip3/dlc014_ip3.dlc
debug.1.log:68  1776 - Age of Revolutions ...\1776_Age_of_Revolutions_fork
debug.1.log:80  Mounted Data: .../dlc/dlc014_ip3
debug.1.log:87  Mounted Data: .../1776_Age_of_Revolutions_fork
```

Résultats ciblés :

| Diagnostic | Avant | Après |
| --- | ---: | ---: |
| Ancien pinning global | 387 | 386 |
| Chemin `05_great_eastern_crisis.txt` | 1 | 0 |
| Nouvelle propriété impliqué | 0 | 0 |
| Nouvelle propriété contexte | 0 | 0 |
| `should_show_when_not_involved` | 0 | 0 |
| `can_revolution_inherit` | 0 | 0 |
| `sr:region_balkans` | 0 | 0 |
| `geographic_region_balkans_old` | 0 | 0 |

Le diagnostic ciblé passe donc de un à zéro. Aucun nouveau diagnostic propre au
fichier n’est présent. La progression jusqu’au 8 avril 1776 est fournie par
l’observation et les captures humaines ; elle n’est pas attribuée à une
observation de Codex.

## 19. Constat Tanzimat signalé pendant le runtime

L’opérateur a constaté que l’Empire ottoman ne commence pas avec
`L’homme malade de l’Europe` ni les entrées Tanzimat.

La cause statique est confirmée :

- dans le fork, `common/history/countries/tur - ottoman empire.txt:31-41`
  commente `sick_man.1`, `sick_man_of_europe` et
  `outmoded_bureaucracy` ;
- la source hotfix contient la même omission commentée ;
- vanilla active `sick_man.1` et les deux modificateurs aux lignes 29–38 ;
- l’événement vanilla hérité `sick_man.1` ajoute `je_sick_man_main`, puis les
  six entrées de réforme ;
- `00_sick_man.txt` conserve par ailleurs huit anciens champs de pinning dans
  le fork, contre huit propriétés contextuelles modernes dans source/vanilla.

Cette absence retire bien la voie d’activation fondée sur l’échec de
`je_sick_man_main` ou de `je_sick_man_separatism`.

Elle ne rend toutefois pas la Grande Crise orientale impossible :
`05_great_eastern_crisis.txt:50-65` contient une autre branche autonome,
`nationalism` recherché et progression sécessionniste ottomane supérieure ou
égale à 50 %. La capture ottomane affiche correctement ces deux routes.

Le setup 1776 et la source hotfix convergent contre le setup vanilla 1836. La
restauration immédiate de `sick_man.1` serait donc une décision de design, pas
une correction sûre de 6A.8F. Elle est reportée à un audit documentaire dédié,
qui devra aussi traiter les huit API de pinning de `00_sick_man.txt`.

## 20. Décision de clôture

Le constat Tanzimat ne remet pas en cause les six hunks de 6A.8F :

- visibilité impliquée : PASS ;
- visibilité contextuelle : PASS ;
- pinning impliqué/contextuel : PASS ;
- textes et conditions : PASS ;
- parser ciblé : PASS ;
- héritage révolutionnaire : preuve statique maintenue.

6A.8F est donc close. La question de la chaîne ottomane 1776 est isolée sans
modification gameplay supplémentaire.

Prochaine phase documentaire :

`NEXT_EXECUTION_PHASE = HOTFIX_6A9R_OTTOMAN_TANZIMAT_1776_ENTRY_CHAIN_AUDIT`

## 21. Verdicts finaux

`HOTFIX_6A8F_GREAT_EASTERN_CRISIS_1_13_STATIC_PASS`

`HOTFIX_6A8F_GREAT_EASTERN_CRISIS_1_13_RUNTIME_PASS`

`GREAT_EASTERN_CRISIS_SIX_HUNK_1_13_ALIGNMENT_COMPLETE`

`GREAT_EASTERN_CRISIS_GEOGRAPHY_VISIBILITY_AND_PINNING_VALIDATED`

`OTTOMAN_TANZIMAT_1776_ROUTE_REQUIRES_DOCUMENTARY_AUDIT`

`HOTFIX_6A8F_GREAT_EASTERN_CRISIS_1_13_ALIGNMENT_COMPLETE`

`GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`

`NEXT_EXECUTION_PHASE = HOTFIX_6A9R_OTTOMAN_TANZIMAT_1776_ENTRY_CHAIN_AUDIT`
