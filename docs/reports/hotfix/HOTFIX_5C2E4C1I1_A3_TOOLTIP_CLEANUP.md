# HOTFIX-5C2E4C1I1 - Nettoyage des tooltips du harnais A-3

## 1. Résumé

Cette micro-phase corrige uniquement la description automatique de six conditions du harnais jetable A-3. Les conditions restent évaluées, mais leur détail de scope est désormais masqué derrière trois `custom_tooltip` localisés. Les tests runtime BIC et GBR sont concluants et aucun diagnostic A-3 ne subsiste dans les logs frais.

**Verdict : `PASS_A3_TOOLTIP_CLEAN`.**

## 2. État Git initial

- Dépôt : `1776_Age_of_Revolutions_fork`.
- Branche : `hotfix-dlc-audit`.
- HEAD initial : `2002b5d Validate Sepoy two-receiver runtime`.
- Aucun fichier suivi n'était modifié.
- Stash présent : `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`.

## 3. Exception `docs/research/technology/`

`docs/research/technology/` était et reste le seul chemin non suivi préexistant. Il n'a été ni lu comme entrée du harnais, ni modifié, ni ajouté à Git.

## 4. Vérification de la copie

Avant modification, la copie jetable contenait exactement 960 fichiers, aucun `.git`, aucun `remote_file_id`, seize fichiers de harnais et aucun scénario B/C/E/F. Les 25 contrôles du manifeste C1H étaient conformes. La sauvegarde baseline A-3 conservait la taille 7 909 129 octets et le SHA-256 `9E9A7D7884672FA16C9FA665C8E1D5BC5FC2C5DF7C4EA0DA791607C4F9F54136`.

## 5. Diagnostics C1I ciblés

Le test C1I avait produit 810 diagnostics dans `error.log` sur les six emplacements ciblés :

| Ligne C1I | Répétitions | Cause |
|---:|---:|---|
| 23 | 52 | condition MARATH décrite automatiquement |
| 35 | 104 | condition NAG décrite automatiquement |
| 48 | 312 | recherche négative d'un troisième receveur |
| 94 | 38 | condition MARATH répétée dans la décision d'ouverture |
| 106 | 76 | condition NAG répétée dans la décision d'ouverture |
| 119 | 228 | exclusion répétée d'un troisième receveur |

Le diagnostic provenait de `jomini_trigger_description.cpp` et demandait que les valeurs de scope utilisées dans les blocs `any` soient masquées par un `custom_tooltip`.

## 6. Six emplacements identifiés

| Ancienne ligne | Décision | Bloc | Trigger | Fonction | Action |
|---:|---|---|---|---|---|
| 23 | `zz_sepoy_test_a3_prepare` | `possible` | receveur MARATH | impose MARATH comme voisin admissible | enveloppe évaluée MARATH |
| 35 | `zz_sepoy_test_a3_prepare` | `possible` | receveur NAG | impose NAG comme voisin admissible | enveloppe évaluée NAG |
| 48 | `zz_sepoy_test_a3_prepare` | `possible` | `NOT` + voisin admissible | interdit tout troisième propriétaire | enveloppe évaluée négative |
| 94 | `zz_sepoy_test_a3_open_event` | `possible` | receveur MARATH | revalide MARATH avant l'appel manuel | même enveloppe MARATH |
| 106 | `zz_sepoy_test_a3_open_event` | `possible` | receveur NAG | revalide NAG avant l'appel manuel | même enveloppe NAG |
| 119 | `zz_sepoy_test_a3_open_event` | `possible` | `NOT` + voisin admissible | revalide l'absence d'un troisième receveur | même enveloppe négative |

Après ajout des enveloppes, ces blocs se trouvent respectivement aux lignes 23-37, 38-52, 53-70, 103-117, 118-132 et 133-150.

## 7. Exemples vanilla utilisés

La syntaxe a été vérifiée dans `C:\Games\Victoria 3 The Great Wave\game\common\diplomatic_actions\04_trade_states.txt`, notamment aux lignes 50-55 et 57-78. La vanilla 1.13 y place des triggers complexes, dont `any_neighbouring_state`, dans un bloc `custom_tooltip` comportant `text` et un trigger réellement évalué.

## 8. Syntaxe `custom_tooltip` retenue

La forme appliquée est une enveloppe évaluée :

```txt
custom_tooltip = {
    text = zz_sepoy_test_a3_receiver_marath_valid_tt
    <trigger original inchangé>
}
```

Le même modèle est utilisé pour NAG et pour le test négatif. Aucun `hidden_trigger` détaché et aucun simple texte non évalué n'a été employé.

## 9. Invariants avant modification

| Invariant | Valeur |
|---|---:|
| Décisions A-3 | 2 |
| Appels à `sepoy_mutiny_events.2` | 1 |
| Appels automatiques | 0 |
| Choix automatique de 2.a | 0 |
| Identifiant de marqueur A-3 | 1 |
| Mutations territoriales | 0 |
| MARATH requis | oui |
| NAG requis | oui |
| Troisième receveur interdit | oui |
| BIC sujet de GBR requis | oui |
| COO et JEY requis | oui |
| État témoin | `STATE_BUNDELKHAND` |
| Région | `region_north_india` |

## 10. Modification exacte

Dans `common/decisions/zz_sepoy_functional_test_a3.txt`, les six conditions responsables ont uniquement reçu une enveloppe `custom_tooltip`. Les corps de trigger, tags, scopes, valeurs, opérateurs `NOT`, état et région n'ont pas changé.

## 11. Clés EN/FR ajoutées

Trois clés ont été ajoutées une fois dans chaque langue :

- `zz_sepoy_test_a3_receiver_marath_valid_tt`
- `zz_sepoy_test_a3_receiver_nag_valid_tt`
- `zz_sepoy_test_a3_no_third_receiver_tt`

Les textes anglais et français suivent exactement les formulations demandées. Aucune autre valeur de localisation n'a changé.

## 12. Diff logique

Le diff de la copie contient seulement :

- six enveloppes `custom_tooltip` dans la décision A-3 ;
- trois nouvelles clés dans la localisation anglaise A-3 ;
- les trois clés équivalentes dans la localisation française A-3.

Il ne contient aucun nouveau tag, state, receveur, effet territorial, namespace, appel d'événement ou modification de l'événement A-3.

## 13. Contrôles d'encodage

Les trois fichiers modifiés conservent UTF-8 avec BOM, des fins de ligne LF uniquement, zéro CRLF et un texte UTF-8 valide. Aucun encodage d'un fichier de contrôle n'a été modifié.

## 14. Validation statique

- Accolades : 52 ouvrantes et 52 fermantes.
- Décisions : exactement 2.
- `custom_tooltip` : exactement 6.
- Appel à `sepoy_mutiny_events.2` : exactement 1.
- Choix automatique : 0.
- Mutation territoriale : 0.
- MARATH, NAG, `STATE_BUNDELKHAND` et `region_north_india` toujours présents.
- Exclusion du troisième receveur toujours évaluée sous `NOT`.
- Treize clés présentes dans chaque fichier A-3 EN/FR, sans doublon.
- Fichiers Sepoy et anciens harnais inchangés.

## 15. Résumé du manifeste

Le manifeste C1I1 couvre 25 entrées : trois fichiers A-3 modifiés, l'événement A-3 inchangé, douze anciens fichiers de harnais, quatre contrôles Sepoy, les descripteurs, le marqueur et les deux livrables. Les statuts sont limités à `MODIFIED_TOOLTIP_ONLY`, `UNCHANGED_CONTROL`, `CREATED_REPORT` et `EXPECTED_DESCRIPTOR_DIFFERENCE`.

## 16. Vérification du playset

Le playset jetable a été confirmé manuellement : seule `1776_Age_of_Revolutions_sepoy_test` était active, le fork principal et les autres copies 1776 étaient désactivés.

## 17. Session BIC

Une nouvelle partie BIC 1776 a été lancée et conservée en pause au 1er janvier. La décision de préparation A-3 était visible. La session n'a pas utilisé une sauvegarde A-1 ou A-2.

## 18. Tooltips observés

Les trois conditions visibles utilisaient les nouveaux textes localisés pour MARATH, NAG et l'absence de troisième receveur. Aucune des trois nouvelles clés A-3 n'est apparue brute. Les clés brutes `objective_battle_for_india_idle_*` visibles ailleurs dans l'interface sont une dette de localisation indépendante du harnais A-3.

## 19. Préparation A-3

La décision de préparation a été prise et son option de préparation sélectionnée. La carte est restée inchangée. La décision manuelle d'ouverture A-3 est ensuite devenue disponible, confirmant que la logique fonctionnelle des six conditions est préservée.

## 20. Event réel non ouvert

La décision d'ouverture n'a pas été cliquée. `sepoy_mutiny_events.2` n'a pas été ouvert, aucune option Sepoy n'a été sélectionnée et aucun jour n'a été avancé.

## 21. Session GBR

Après fermeture propre de la session BIC, une nouvelle partie GBR 1776 a été lancée et maintenue en pause.

## 22. Absence des décisions pour GBR

Les décisions A-3 étaient absentes pour GBR. Cela confirme que l'enveloppe de présentation n'a pas élargi `is_shown` ni le scope pays du harnais. La session GBR a été quittée proprement sans avancer le temps.

## 23. Fraîcheur des logs

| Log | Taille | Dernière écriture UTC | SHA-256 |
|---|---:|---|---|
| `debug.log` | 342197 | 2026-07-17T18:52:01.3491975Z | `7A20B6B9A791D1629A54962F7768E793B3FD98AC409C047AF1588F6BE36226D3` |
| `error.log` | 274604 | 2026-07-17T18:51:57.3033439Z | `5FA3993588C5D086525CE37305E2E28035A4AABB941607C56788282586C93BFC` |
| `game.log` | 382829 | 2026-07-17T18:51:57.3033439Z | `BF131C6BBB836CBBD4CF10AA289E2E02006592F3AF096ED3961AE8713F8C455B` |
| `system.log` | 1101 | 2026-07-17T18:48:20.3897802Z | `A48632BE8E475DAB0DF1D4787A19157C84F5E68F93AA61472A0F3DC322BC3D57` |

Ces dates et empreintes diffèrent de la baseline antérieure au test et attestent une session fraîche.

## 24. Disparition des diagnostics A-3

Les recherches agrégées dans `debug.log`, `error.log`, `game.log` et `system.log` donnent zéro occurrence pour :

- `zz_sepoy_functional_test_a3.txt` ;
- `zz_sepoy_test_a3` ;
- `jomini_trigger_description.cpp` ;
- `should be hidden by a custom_tooltip` ;
- `Invalid scope` ;
- `Parsing Error` ;
- `Missing localization` ;
- `sepoy_mutiny_events.2`.

Il n'existe donc ni diagnostic direct, ni exécution réelle, ni erreur de parsing/scope/localisation visant A-3.

## 25. Diagnostics globaux hors périmètre

Le `error.log` frais contient encore 1 407 messages `Invalid right side during comparison 'sr'`, dont 1 230 référencent `01_natural_borders_of_france.txt`. Il contient aussi cinq références à `common/interest_groups/00_landowners.txt:459`, un avertissement télémétrique `Unknown tooltip type` et un doublon global de template relevé dans l'analyse agrégée. Ces dettes ne citent aucun fichier ou identifiant A-3. Aucun `PostValidate`, `Unexpected token` ou avertissement BOM n'est relevé dans le log frais ciblé.

## 26. Intégrité finale de la copie

Les quinze contrôles immuables de la copie présents dans le manifeste C1H passent par taille et SHA-256. L'événement A-3, les douze anciens harnais, les deux fichiers Sepoy, `descriptor.mod` et le marqueur restent inchangés. La sauvegarde baseline A-3 n'a pas été modifiée.

## 27. Intégrité finale du fork

Aucun fichier gameplay du fork n'a été modifié. Les fichiers Sepoy du fork correspondent toujours bit à bit à ceux de la copie. Seuls les deux livrables C1I1 sont créés dans `docs/reports/hotfix/`, en plus de l'exception non suivie préexistante `docs/research/technology/`.

## 28. Verdict

**`PASS_A3_TOOLTIP_CLEAN`**

Les diagnostics A-3 ont disparu, les invariants sont préservés, la préparation est fonctionnelle pour BIC, les décisions sont absentes pour GBR, l'événement réel n'a pas été déclenché et aucun log frais ne vise A-3.

## 29. Ce que la phase valide

La phase valide la présentation et l'évaluation des trois conditions de receveur dans les deux décisions A-3, leur localisation EN/FR, leur visibilité BIC, leur absence GBR et l'absence de diagnostics runtime associés.

## 30. Ce que la phase ne rejoue pas

La phase ne rejoue pas les cinq tirages A-3, ne teste pas à nouveau la distribution MARATH/NAG, ne lance pas la dissolution réelle, ne sélectionne pas 2.a et ne prépare aucun scénario B-1.

## 31. Recommandation pour B-1

Conserver cette copie jetable comme baseline validée et préparer B-1 dans une phase séparée. Réutiliser le modèle de `custom_tooltip` évalué si B-1 expose des scopes complexes, sans modifier les scénarios A-1, A-2 ou A-3.

## 32. Fichiers modifiés dans la copie

1. `common/decisions/zz_sepoy_functional_test_a3.txt`
2. `localization/english/zz_sepoy_functional_test_a3_l_english.yml`
3. `localization/french/zz_sepoy_functional_test_a3_l_french.yml`

## 33. Fichiers créés dans le fork

1. `docs/reports/hotfix/HOTFIX_5C2E4C1I1_A3_TOOLTIP_CLEANUP.md`
2. `docs/reports/hotfix/HOTFIX_5C2E4C1I1_A3_TOOLTIP_MANIFEST.csv`

## 34. Fichiers Sepoy inchangés

`common/journal_entries/04_sepoy_mutiny.txt` et `events/india_events/sepoy_mutiny_events.txt` sont inchangés dans le fork et la copie. Leurs SHA-256 communs sont respectivement `DAEFCB59CCF6B303D2E39C948D8038006C1346AFE40A2B812D45EE4D947E361C` et `557936500AC585F7F69B9F5B063BDDA377AFF4A5AFAA06C70650C55D4AD612F7`.

## 35. Anciens harnais inchangés

Les douze fichiers des harnais racine, A-1 et A-2 restent bit à bit conformes au manifeste C1H. Aucun scénario antérieur n'a été édité ou exécuté pendant cette micro-phase.

## 36. `docs/research/technology/` intact

Le répertoire non suivi préexistant `docs/research/technology/` est intact et reste hors des livrables.

## 37. Stash MARATH intact

Le stash `WIP NAVY-3C-3 Maratha Konkan Flotilla` est toujours présent sous `stash@{0}`. Il n'a été ni appliqué, ni modifié, ni supprimé.
