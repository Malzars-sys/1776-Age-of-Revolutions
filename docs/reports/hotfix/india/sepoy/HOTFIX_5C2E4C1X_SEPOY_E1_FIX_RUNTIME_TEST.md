# 1. Résumé

La correction C1W passe intégralement son objectif territorial Bombay : `x51F0A0` (province interne `39686`) reste à BIC, le region state Bombay BIC 482 reste réel et non vide, KHP ne l’absorbe pas, MARATH/SAT/KHP restent respectivement à 25/10/3 provinces, la boucle termine et BIC reste joué. West Bengal est perdu séparément, sans transformer ce succès territorial en échec.

Le volet radical ne passe pas. La sauvegarde pré-2.e ne contient aucune baseline profonde `very_small_radicals` sur la pop hindoue 14727. Après 2.e, `loyalists_and_radicals` ne passe que de zéro à `-0.00001` et `radicals_increase` de zéro à `0.00001`, soit environ une personne au lieu des quelque 7 585 attendues. Verdict principal : **FAIL_E1_FIX_RADICAL_BASELINE / WEST_BENGAL_LOST** ; le même jeu de preuves établit aussi **FAIL_E1_FIX_RADICAL_EFFECT**. Le sous-verdict territorial est PASS.

# 2. État Git initial

Racine exacte : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`. Branche : `hotfix-dlc-audit`. HEAD : `5ca1b50 Protect Sepoy Bombay retreat core`. Aucun fichier suivi n’était modifié.

# 3. Exception docs/research/technology/

Le seul état initial hors suivi était `?? docs/research/technology/`. Ce répertoire préexistant est resté hors périmètre et n’a pas été touché.

# 4. Vérification de la copie

La copie jetable contenait avant et après session exactement 972 fichiers, 28 harnais dont quatre E-1, aucun `.git` et aucun `remote_file_id`. Les 35 lignes applicables du manifeste C1W ont zéro divergence. Le Sepoy du fork et celui de la copie sont identiques : 63 658 octets, SHA-256 `51F489F00FA6CB2D7BBF1D1FDC587104F2A17D4932187DAA8BBE954F7312A9FB`.

# 5. Playset

L’utilisateur a confirmé que seule `1776_Age_of_Revolutions_sepoy_test` était active ; fork principal, autres copies 1776 et versions Workshop étaient désactivés.

# 6. Logs avant session

| Log | Taille | LastWriteTime UTC | SHA-256 |
|---|---:|---|---|
| `debug.log` | 268 319 | 2026-07-21T21:26:39.1052118Z | `99517804BDD7BBCFFD92514242D93FBA3F9A6E187EF33D4C13A932EA56B8ED3A` |
| `error.log` | 426 875 | 2026-07-21T21:26:25.0511198Z | `88FF88350394649402801C6883F0E7E44135447CD4E5BEC97203F86A114A8595` |
| `game.log` | 72 865 | 2026-07-21T21:26:25.0511198Z | `B66008EB9E11D26B961C2CA0DE723923416315E85E46EE8866FF7547E8B1712A` |

# 7. Fiche opérateur unique

La checklist complète de 42 étapes a été fournie dans un seul message avant lancement : nouvelle partie BIC, préparation POR → BIC, contrôles initiaux, ticks, trois sauvegardes, ouverture manuelle de l’événement, sélection exclusive de 2.e, observations territoriales/radicales et fermeture finale.

# 8. Nombre réel d’ouvertures et fermetures

Une ouverture de Victoria 3, une nouvelle partie BIC, aucune session GBR, aucune relance et une fermeture finale. Après confirmation de fermeture, zéro processus Victoria 3/launcher était actif.

# 9. État initial West Bengal

Après préparation et avant 2.e, le state 487 appartient à BIC avec `40292 12 40306 2`; le state 488 appartient à COO avec `40305 0`. La préparation n’a pas modifié ce partage.

# 10. État initial Bombay

Avant préparation, `x51F0A0` est portugais ; MARATH possède 25 provinces, SAT 10 et KHP 3. BIC ne possède initialement aucune portion Bombay.

# 11. Préparation POR → BIC

La préparation transfère uniquement `x51F0A0`/`39686` de POR à BIC. Dans la sauvegarde pré-2.e, le state 482 a `country=218`, `capital=39686` et `provinces={39686 0}`.

# 12. Absence d’autre mutation

L’opérateur a déclaré le reste nominal. Les encodages sérialisés des states Bombay MARATH 483, SAT 484 et KHP 485 sont identiques avant et après 2.e ; West Bengal reste inchangé pendant la préparation.

# 13. Tick 0

La portion Bombay BIC compte 446 391 personnes. L’UI affiche zéro radical. Ce seul résultat visuel n’a pas servi à conclure.

# 14. Premier tick

Le territoire préparé reste à BIC et aucun radical pertinent n’apparaît visuellement. Aucun événement Sepoy réel ne s’est ouvert automatiquement.

# 15. Second tick

Le contrôle opérateur reste nominal territorialement et le compteur radical reste nul. La sauvegarde appelée « pré-2.e 3 janvier » est toutefois sérialisée à `1776.1.4.6`.

# 16. Sauvegarde pré-2.e

`HOTFIX_5C2E4C1X_E1_FIX_PRE_2E_1776_01_03.v3` : 8 281 534 octets, LastWriteTime UTC `2026-07-21T23:28:06.0275748Z`, SHA-256 `2E04BCA6AF509216D792F351B9D13F06EE7275B64CF0488BBA751C7E71B6768E`, date réelle `1776.1.4.6`. Le décalage nom/date est documenté ; il n’empêche pas la comparaison immédiate à date égale.

# 17. Baseline hindoue profonde

La pop 14727 a workforce 18 963, dependents 56 889, total 75 852, location 482 et religion `hindu`. Avant 2.e, le champ `loyalists_and_radicals` est absent, donc nul ; `population_radicals`, `radicals_increase` et `trend_radicals={0 0 0}` sont nuls. La baseline `very_small_radicals` exigée n’existe pas : **FAIL_E1_FIX_RADICAL_BASELINE**.

# 18. Absence de cible sunnite

Les quinze pops de location 482 sont quatorze pops catholiques et une pop hindoue. Aucune pop sunnite n’existe dans cette portion ; un delta sunnite nul est attendu et n’est pas une erreur.

# 19. Ouverture manuelle de l’événement

L’événement `sepoy_mutiny_events.2` a été ouvert manuellement par la décision E-1 sur BIC. Aucun appel automatique n’a été observé.

# 20. Sélection exclusive de 2.e

L’utilisateur a sélectionné uniquement « Bombay tient bon ». Les trois sauvegardes réglementaires ont été créées et aucune autre option n’a été choisie.

# 21. Terminaison de la boucle

L’événement s’est fermé, le jeu est resté réactif et les ticks suivants ont été atteints. Aucun signe de boucle vide ou non terminée : PASS boucle.

# 22. Pays joué final

BIC reste le pays joué après 2.e et jusqu’à la sauvegarde finale.

# 23. x51F0A0 après 2.e

Immédiatement et à la fin, la province interne 39686 reste rattachée au state 482, lui-même `country=218` (BIC). Aucun owner nul et aucune double attribution ne sont sérialisés.

# 24. Region state Bombay BIC

Le state 482 reste réel, non vide, capital 39686, avec exactement `provinces={39686 0}`. Sa population reste 446 391. La protection territoriale C1W est validée.

# 25. MARATH après 2.e

Le state 483 reste à MARATH (country 744) avec son encodage de 25 provinces inchangé.

# 26. SAT après 2.e

Le state 484 reste à SAT (country 423) avec son encodage de 10 provinces inchangé.

# 27. KHP après 2.e

Le state 485 reste à KHP (country 424) avec trois provinces (`39690`, `39692`, `39696`). KHP ne reçoit pas 39686.

# 28. West Bengal après 2.e

Le state BIC 487 devient vide et sans country, avec `previous_country=218`. Le state COO 488 absorbe la portion et porte ensuite l’encodage agrégé `40292 16`. Statut : **WEST_BENGAL_LOST**. Cette perte ne remet pas en cause le PASS territorial Bombay.

# 29. WEST_BENGAL_FUNCTIONAL_DECISION_DEFERRED

**WEST_BENGAL_FUNCTIONAL_DECISION_DEFERRED.** Aucune protection, correction de trigger ou recommandation de modification West Bengal n’est formulée dans C1X.

# 30. Statut COO

Immédiatement après 2.e, COO possède son propre marché 282 et `power_bloc_leave_date=1776.1.4.6`, preuves sérialisées de l’indépendance attendue. L’évolution ultérieure visible vers Bengal est postérieure au contrôle immédiat et n’est pas attribuée au correctif Bombay.

# 31. Statut JEY

Immédiatement après 2.e, JEY possède son propre marché 283 et `power_bloc_leave_date=1776.1.4.6`. L’indépendance attendue est validée.

# 32. Owners nuls ou incohérents

Aucun territoire réel contrôlé par le scénario n’a un owner nul ou double. Le state 487 vide conserve seulement son historique `previous_country`, ce qui est cohérent avec son transfert complet.

# 33. Résultat radical immédiat

À date sérialisée identique `1776.1.4.6`, la pop hindoue 14727 passe de zéro à `loyalists_and_radicals=-0.00001`; BIC passe de zéro à `radicals_increase=0.00001`. Cela correspond à environ une personne, pas aux quelque 7 585 attendues de `large_radicals=0.1` : **FAIL_E1_FIX_RADICAL_EFFECT**.

# 34. Premier tick après 2.e

Le territoire Bombay reste stable et le compteur UI reste à zéro. Aucun signal profond supplémentaire n’est attesté entre la sauvegarde immédiate et le contrôle suivant.

# 35. Second tick après 2.e

La sauvegarde finale est sérialisée à `1776.1.6.6`, un jour après le nom prévu. Bombay est toujours BIC ; les valeurs profondes radicales restent exactement `-0.00001` et `0.00001`.

# 36. Analyse hindoue

Population cible constante : 75 852. Delta profond immédiat et final : `-0.00001`, soit environ une personne à l’échelle utilisée par les tests précédents. Ordre attendu : environ `-0.07585`, soit 7 585 personnes. Le rapport entre observé et attendu exclut une simple tolérance numérique.

# 37. Analyse sunnite sans cible

Aucune pop sunnite n’est présente à location 482 dans les trois sauvegardes. Aucun objet sunnite ne pouvait être modifié ; le delta zéro ne révèle aucun défaut de scope.

# 38. Radicals increase

BIC a `radicals_increase=0` avant 2.e, `0.00001` immédiatement, puis `0.00001` à la fin. Le signal attendu proche de `0.07585` n’est pas matérialisé.

# 39. Loyalists and radicals

La pop hindoue 14727 n’a pas de champ pré-2.e (zéro). Elle porte `-0.00001` immédiatement et à la fin. Aucun autre objet de location 482 n’est une cible hindoue ou sunnite.

# 40. Comparaison UI

L’UI affiche zéro radical avant et après 2.e, y compris au 4 janvier. Contrairement aux phases B-1/C-1, les données sources ne contiennent pas un large delta caché : l’UI n’est donc pas la seule couche en retard.

# 41. Comparaison sérialisée

| Champ | Pré-2.e | Immédiat | Final |
|---|---:|---:|---:|
| Date réelle | 1776.1.4.6 | 1776.1.4.6 | 1776.1.6.6 |
| Owner state 482 | BIC | BIC | BIC |
| Provinces state 482 | `39686 0` | `39686 0` | `39686 0` |
| Population | 446 391 | 446 391 | 446 391 |
| Hindous | 75 852 | 75 852 | 75 852 |
| `population_radicals` | 0 | 0 | 0 |
| `trend_radicals` | `0 0 0` | `0 0 0` | `0 0 0` |
| `radicals_increase` | 0 | 0.00001 | 0.00001 |
| pop hindoue `loyalists_and_radicals` | 0 | -0.00001 | -0.00001 |

# 42. Logs ciblés

La recherche obligatoire a utilisé `Get-ChildItem` et `Select-String`, sans `rg`. Les onze motifs directs E-1/2.e/territoriaux, `Invalid scope`, `jomini_trigger_description` et le diagnostic tooltip ont zéro occurrence. Le motif BOM compte 16 occurrences génériques dans `debug.log`, mais aucune ne vise E-1. Il n’existe aucune erreur directe E-1, 2.e, Bombay, West Bengal, scope, transfert ou boucle.

Métadonnées finales :

| Log | Taille | LastWriteTime UTC | SHA-256 |
|---|---:|---|---|
| `debug.log` | 351 372 | 2026-07-21T23:30:44.4122355Z | `3E87919DD475E31F249A0FCEB11327BC2EA81519B374CAC0A9FE3B6CD8B6F9EC` |
| `error.log` | 324 440 | 2026-07-21T23:30:37.9841594Z | `14725DCE6515FC3A7C8B43EA30021B4C57B955FDC1E92289A724D81BEA2E997D` |
| `game.log` | 191 242 | 2026-07-21T23:30:37.9841594Z | `F4587717F7EA33A635C9A35A3A336298495BD366432614324E6CDAED9DED11DD` |

# 43. Diagnostics hors périmètre

Les motifs génériques donnent : `Invalid right side` 2 313, `Script system error` 2 519, `PostValidate` 677, `Unexpected token` 427 et avertissement UTF-8 BOM 16. Ils ne contiennent aucun identifiant E-1, 2.e, Bombay ou harnais C1X ; ils sont classés comme bruit global de chargement hors périmètre, pas comme `FAIL_E1_FIX_RUNTIME_ERROR`.

# 44. Intégrité des sauvegardes

Rakaly 0.8.18 a fondu uniquement des copies temporaires hors de `save games` avec `melt --format vic3 --unknown-key stringify`. Les copies, fontes, archive et exécutable temporaires ont été supprimés. Les trois originaux ont été rehashés ensuite et conservent exactement leurs tailles et SHA-256 : pré `2E04...768E`, immédiat `AF68...0F0D`, final `99D3...FE61`.

# 45. Intégrité des fichiers

Après runtime : 35 contrôles C1W sur 35 conformes, zéro mismatch ; copie à 972 fichiers et 28 harnais ; quatre E-1 ; aucun `.git` ni `remote_file_id`; Sepoy fork/copie identiques à 63 658 octets et au SHA attendu. Aucun gameplay, harnais ou fichier de localisation n’a été modifié.

# 46. Verdict principal

**FAIL_E1_FIX_RADICAL_BASELINE / WEST_BENGAL_LOST.** Sous-verdicts : **PASS_BOMBAY_TERRITORIAL**, **PASS_LOOP**, **PASS_SUBJECTS**, et **FAIL_E1_FIX_RADICAL_EFFECT**. Le défaut radical est indépendant du correctif territorial C1W et doit faire l’objet d’un diagnostic distinct avant toute correction.

# 47. Statut West Bengal

**WEST_BENGAL_LOST.** La portion BIC est transférée à COO pendant 2.e. Selon les règles C1X, ce résultat n’est pas un échec Bombay et sa décision fonctionnelle reste différée.

# 48. Ce que le test valide

Le test valide définitivement la double exclusion Bombay de C1W, la conservation de 39686 par BIC, la non-absorption par KHP, la stabilité MARATH/SAT/KHP, la terminaison et les indépendances COO/JEY. Il invalide la baseline radicale de cette exécution et ne valide pas `large_radicals` sur Bombay.

# 49. Suite recommandée

Conserver C1W sans changement territorial. Ouvrir, si souhaité, une phase de diagnostic radical distincte et statique/runtime pour expliquer pourquoi la préparation ne matérialise pas `very_small_radicals` et pourquoi 2.e ne produit que `0.00001`. Ne corriger ni West Bengal ni les filtres Bombay dans cette phase.

# 50. Fichiers créés

Uniquement `docs/reports/hotfix/HOTFIX_5C2E4C1X_SEPOY_E1_FIX_RUNTIME_TEST.md` et `docs/reports/hotfix/HOTFIX_5C2E4C1X_E1_FIX_RUNTIME_RESULTS.csv`.

# 51. Confirmation Bengal/Madras/Travancore/MARATH

Les branches et contrôles Bengal, Madras et Travancore restent byte-identiques au manifeste C1W. Aucune donnée MARATH n’a été modifiée ; sa portion Bombay reste à 25 provinces. La perte West Bengal constatée est le résultat séparé de 2.e, pas une modification de fichiers.

# 52. Confirmation docs/research/technology/

`docs/research/technology/` est resté non suivi, préexistant et entièrement hors périmètre.

# 53. Confirmation stash MARATH

Le stash reste intact : `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`. Aucun commit automatique n’a été créé.
