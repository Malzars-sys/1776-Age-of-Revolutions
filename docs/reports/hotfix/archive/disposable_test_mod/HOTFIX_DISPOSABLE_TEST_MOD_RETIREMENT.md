# HOTFIX — Audit de retrait de la copie jetable Sepoy

## 1. Résumé

La copie jetable est auditée et sûre à retirer ultérieurement, mais aucune suppression n’est exécutée dans AH.

## 2. Rôle de la copie jetable

Elle a isolé les harnais runtime Sepoy sans contaminer le fork principal.

## 3. Pourquoi elle ne doit pas être fusionnée

Elle contient des décisions, événements et localisations de diagnostic non destinés au mod principal. Toute copie récursive est interdite.

## 4. Correctifs gameplay déjà intégrés

Les changements Sepoy et journal légitimes sont déjà présents dans le fork et contrôlés individuellement par l’historique HOTFIX-5C2E4.

## 5. Harnais non destinés au mod principal

Les familles `zz_sepoy*`, E-1, E1D, E-2, E-3 et leurs localisations restent exclusivement jetables.

## 6. Comparaison fork/copie

984 fichiers : 943 chemins ont un correspondant dans le fork, dont 942 identiques ; la seule différence correspondante est le `descriptor.mod` attendu. Quarante et un fichiers sont propres à la copie.

## 7. Sepoy

`events/india_events/sepoy_mutiny_events.txt` est identique octet par octet : 63 653 octets, SHA-256 `66465CB840A5D7348E342F233205F0389E46E5E1C5ECA97B17870ED09D93C6BB`.

## 8. Journal Sepoy

`common/journal_entries/04_sepoy_mutiny.txt` est identique octet par octet : 16 040 octets, SHA-256 `DAEFCB59CCF6B303D2E39C948D8038006C1346AFE40A2B812D45EE4D947E361C`.

## 9. Fichiers gameplay différents

Aucun fichier gameplay légitime différent ou uniquement présent dans la copie n’a été détecté.

## 10. Fichiers uniquement dans la copie

Les 41 fichiers propres à la copie sont 20 fichiers de harnais, 20 localisations de test et un marqueur jetable.

## 11. Localisations de test

Les 20 localisations de test sont classées `TEST_LOCALIZATION` et ne sont pas destinées au fork.

## 12. Descripteurs

Le descripteur interne de test est classé `TEST_DESCRIPTOR`. Le descripteur launcher externe existe également. Aucun `remote_file_id` n’a été trouvé.

## 13. Manifestes de contrôle utilisés

L’audit s’appuie sur les manifestes de copie et de harnais C1A à AF, les résultats AG et le manifeste final individuel de 984 lignes produit avec ce rapport.

## 14. Risque de modification non fusionnée

Risque écarté : aucune divergence gameplay non fusionnée et aucun fichier inattendu ou à revoir.

## 15. Résultat de l’audit

942 références identiques, 20 harnais, 20 localisations, un descripteur et un marqueur ; zéro `UNEXPECTED_FILE`, zéro `REVIEW_REQUIRED`.

## 16. Autorisation ou blocage du retrait

Le retrait est techniquement autorisable après commit de la clôture et confirmation explicite de l’utilisateur. Il n’est pas exécuté dans AH.

## 17. Dossier à supprimer

Chemin futur : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_sepoy_test`.

## 18. Descripteur launcher à supprimer

Chemin futur : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_sepoy_test.mod`.

Commandes préparées, non exécutées :

```powershell
$TestMod = "C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_sepoy_test"
$TestDescriptor = "C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_sepoy_test.mod"

Test-Path -LiteralPath $TestMod
Test-Path -LiteralPath $TestDescriptor

Remove-Item -LiteralPath $TestMod -Recurse -Force
Remove-Item -LiteralPath $TestDescriptor -Force

Test-Path -LiteralPath $TestMod
Test-Path -LiteralPath $TestDescriptor
```

## 19. Sauvegardes volontairement conservées

Aucune sauvegarde Victoria 3 n’est incluse dans ce retrait ; leur archivage ou suppression exige une décision séparée.

## 20. Confirmation qu’aucun fichier de test n’a été copié dans le fork

L’audit du fork ne trouve aucun des 40 fichiers jetables. `NO_TEST_HARNESS_MERGED_TO_MAIN_MOD`.

## 21. Verdict

- `DISPOSABLE_TEST_MOD_AUDITED`
- `DISPOSABLE_TEST_MOD_SAFE_TO_RETIRE`
- `NO_UNMERGED_GAMEPLAY_IN_DISPOSABLE_COPY`
- `NO_TEST_HARNESS_MERGED_TO_MAIN_MOD`

La copie et son descripteur sont toujours présents à la fin de AH.
