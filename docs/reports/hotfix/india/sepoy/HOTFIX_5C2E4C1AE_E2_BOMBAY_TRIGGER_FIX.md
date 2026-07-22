# HOTFIX-5C2E4C1AE — Correction du trigger Bombay de l’option Sepoy 2.e

## 1. Résumé

Le trigger de disponibilité de `sepoy_mutiny_events.2.e` a reçu la correction minimale prescrite : son unique test `STATE_WEST_BENGAL` est remplacé par `STATE_BOMBAY`. Le diff gameplay final contient exactement une suppression et un ajout. Aucun effet, protection, harnais ou autre option n’est modifié. Verdict : `READY_FOR_BOMBAY_TRIGGER_RUNTIME_VALIDATION`.

## 2. État Git initial

Racine exacte : `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork`. Branche : `hotfix-dlc-audit`. HEAD initial : `4e6e849 Validate Sepoy Bombay trigger mismatch`. Aucun fichier suivi n’était modifié. Le stash MARATH attendu était présent.

## 3. Exception docs/research/technology/

`docs/research/technology/` était la seule entrée non suivie initiale. Ce répertoire est resté intact et hors périmètre.

## 4. Vérification de la copie

Avant correction, la copie contenait exactement 980 fichiers et 36 harnais : quatre E-2, quatre E-1, quatre E1D et vingt-quatre legacy. Aucun `.git`, aucun `remote_file_id`. Les 44 contrôles non auto-référentiels C1AC correspondaient. Sepoy fork/copie faisait 63 658 octets, SHA-256 `51F489F00FA6CB2D7BBF1D1FDC587104F2A17D4932187DAA8BBE954F7312A9FB`, avec identité octet par octet.

## 5. Défaut AD reproduit

C1AD a établi Bombay state 482 réel, non vide, `country=218` BIC, avec 39686/`x51F0A0` et 446 391 habitants. West Bengal BIC était absent et agrégé chez COO ; East Bengal state 14 restait BIC. 2.e était entièrement cachée, aucune option réelle n’a été choisie, la recharge était propre et aucune fuite d’effet n’a été observée. Verdicts conservés : `PASS_E2_OPTION_BLOCKED`, `PASS_E2_OPTION_HIDDEN`, `TRIGGER_WEST_BENGAL_GOVERNS_2E_CONFIRMED`.

## 6. Distinction accès/retrait

Le défaut est l’exigence de West Bengal avant de pouvoir choisir une retraite annoncée vers Bombay. La perte ultérieure de West Bengal après sélection de 2.e reste un comportement territorial attendu et distinct ; elle n’est pas corrigée ici.

## 7. Trigger avant correction

| Fichier | Ligne option | Ligne trigger | State testé | Bombay testé | West Bengal testé | Comportement E-2 | Statut après correction |
|---|---:|---:|---|---|---|---|---|
| fork | 1428 | 1434, test 1436 | `STATE_WEST_BENGAL` | non | oui | 2.e cachée | corrigé vers Bombay |
| copie | 1428 | 1434, test 1436 | `STATE_WEST_BENGAL` | non | oui | 2.e cachée | corrigé vers Bombay |
| source hotfix, lecture seule | 1412 | 1418, test 1420 | `STATE_WEST_BENGAL` | non | oui | référence statique | inchangée |
| vanilla 1.13, lecture seule | 1412 | 1418, test 1420 | `STATE_WEST_BENGAL` | non | oui | référence statique | inchangée |

Dans les quatre fichiers, l’option appartient au `country_event` `.2`; `root` est BIC. Le trigger contient un unique `any_scope_state`. `ai_chance` reste `base = 40`. Le premier effet commence avec `if = {` immédiatement après le trigger.

## 8. Intention Bombay

La localisation anglaise vanilla ligne 87 dit « Bombay holds! Direct all remaining forces to the West. » ; la française ligne 84 dit « Bombay tient bon ! Dirigez toutes les forces restantes vers l’ouest. » Le tooltip Bombay, lignes 89/86, décrit l’indépendance des sujets extérieurs et la redistribution des states détenus dans la zone de retraite. Aucune localisation n’est modifiée.

## 9. Pourquoi West Bengal n’est pas le noyau

Bombay est omis des transferts prioritaires, exclu de la garde générique et de `random_scope_state`, puis reste dans le scope South India des radicaux finaux. West Bengal ne possède aucune protection 2.e et peut être redistribué. Le noyau nécessaire à l’accès est donc exactement `STATE_BOMBAY`, sans élargissement géographique.

## 10. Correction appliquée

Dans le seul trigger de 2.e, fork et copie :

```diff
-               state_region = s:STATE_WEST_BENGAL
+               state_region = s:STATE_BOMBAY
```

## 11. Trigger après correction

```text
trigger = {
    any_scope_state = {
        state_region = s:STATE_BOMBAY
    }
}
```

## 12. Nombre exact de lignes changées

`git diff --numstat` donne exactement `1 1 events/india_events/sepoy_mutiny_events.txt` : une ligne supprimée, une ajoutée, aucune autre différence gameplay.

## 13. Scope any_scope_state

Le country scope root BIC est conservé. `any_scope_state` exige naturellement qu’au moins une portion réelle de `STATE_BOMBAY` soit possédée par BIC. Aucun scope explicite supplémentaire n’est ajouté.

## 14. Absence de condition supplémentaire

Zéro ajout de `has_state`, `owns_entire_state_region`, `region_state`, population, incorporation, controller, OR/fallback West Bengal, diplomatie ou condition POR/MARATH/SAT/KHP.

## 15. Protection Bombay existante

Les deux exclusions C1W restent présentes et textuellement inchangées : une dans la garde du `while` à la ligne 1751, une dans le filtre de `random_scope_state` à la ligne 1792. Le bloc 2.e corrigé contient toujours exactement deux `NOR` visant `STATE_BOMBAY`.

## 16. Garde du while inchangée

La garde, sa géographie North/South India, ses exceptions Himalaya/Pashtunistan/Quetta, son voisinage et l’exclusion Bombay sont identiques à HEAD.

## 17. random_scope_state inchangé

La sélection, les receveurs, le voisinage, l’ordre et l’exclusion Bombay sont identiques à HEAD. Aucun risque de divergence garde/sélection n’est introduit.

## 18. Redistribution West Bengal inchangée

Zéro protection ou exclusion West Bengal est ajoutée. West Bengal reste dans le domaine North India de la boucle et peut être cédé comme dans C1V/C1AB. COO et East Bengal ne sont pas modifiés.

## 19. WEST_BENGAL_RETREAT_TRANSFER_EXPECTED

`WEST_BENGAL_RETREAT_TRANSFER_EXPECTED`. West Bengal n’est pas le noyau conservé de 2.e ; sa perte après sélection reste attendue et aucune correction de protection n’est recommandée.

## 20. Branches prioritaires inchangées

Les listes et transferts prioritaires de Madras/CAR, Mandalay/Pegu, Tenasserim, Travancore, Circars, Kurnool, Delhi, Agra, Awadh et Central Provinces sont inchangés.

## 21. Sujets inchangés

Les tests de sujets, `make_independent`, le retrait du levier GBR, les scopes sauvegardés et les receveurs sont inchangés. Le bloc 2.e conserve un `make_independent` et douze `set_state_owner`.

## 22. Radicaux inchangés

Les deux appels `add_radicals_in_state` hindu/sunni avec `large_radicals` restent identiques. Aucun ordre ou scope South India n’est modifié.

## 23. Autres options inchangées

Les blocs 2.a, 2.b et 2.c sont strictement identiques à HEAD, avec les SHA-256 normalisés respectifs `2CE8FCD4E673636177B35CB6F6DB81AF5CCDBFAE3139C80C450DE35BD53C5F59`, `36EA97C08E3D304E94A2BDEB472DFB421F31B77BAF4FF78BC1BC6920DA299213` et `0178E9C46514ED78382558D1DCFDDDA874DB9EE1C71BB54FB4A8B357C8252D47`. Les events .3/.4 et le namespace sont hors du diff.

## 24. Comparaison fork/copie

Après correction, les deux fichiers font 63 653 octets et portent le même SHA-256 `66465CB840A5D7348E342F233205F0389E46E5E1C5ECA97B17870ED09D93C6BB`. Ils sont identiques octet par octet, commencent par le BOM `EF BB BF`, contiennent 2 969 LF et zéro CR.

## 25. Validation statique

- exactement une occurrence remplacée dans le trigger 2.e ;
- trigger West Bengal : 1 avant, 0 après ;
- trigger Bombay : 0 avant, 1 après ;
- West Bengal ailleurs dans 2.e : 0 avant et après ;
- Bombay total dans 2.e : 2 avant, 3 après, dont deux protections inchangées ;
- annuler uniquement la première occurrence Bombay du bloc corrigé restitue exactement le bloc 2.e de HEAD ;
- 972 accolades ouvrantes et 972 fermantes ;
- `git diff --check` propre.

## 26. Contrôle des harnais

Les 36 harnais correspondent au manifeste C1AC : 4 E-2, 4 E-1, 4 E1D et 24 legacy, zéro divergence. E-2 conserve exactement deux `set_state_owner`, un appel manuel à l’événement .2 et zéro radical ; E-1 conserve Bombay avec West Bengal ; E1D conserve ses BOM corrigés. La copie reste à 980 fichiers et 36 harnais.

## 27. Résumé du manifeste

Le manifeste AE inventorie deux Sepoy modifiés, deux journaux, 36 harnais inchangés, trois descripteurs/marqueurs et deux livrables AE. Le seul changement fonctionnel est le trigger 2.e.

## 28. Plan runtime positif E-2

Dans une future session unique : nouvelle partie BIC, préparation E-2, confirmer Bombay BIC réel et West Bengal BIC absent, sauvegarder, ouvrir `.2`, confirmer que 2.e est visible et sélectionnable, ne pas nécessairement la choisir, puis recharger proprement.

## 29. Plan runtime négatif E-3

Préparer séparément un état West Bengal BIC présent et Bombay BIC absent, ouvrir `.2`, confirmer que 2.e est cachée ou désactivée, ne sélectionner aucune option et recharger. Aucun harnais E-3 n’est créé dans C1AE.

## 30. Critères futurs

- `PASS_E2_TRIGGER_FIX_POSITIVE` : Bombay BIC présent, West Bengal absent, 2.e visible et sélectionnable.
- `PASS_E3_TRIGGER_FIX_NEGATIVE` : West Bengal BIC présent, Bombay absent, 2.e cachée ou désactivée.
- `FAIL_E2_TRIGGER_FIX_STILL_BLOCKED` : E-2 reste bloquée.
- `FAIL_E3_TRIGGER_FIX_FALSE_POSITIVE` : E-3 reste disponible sans Bombay.

La validation complète exige les deux directions.

## 31. Risques restants

La correction statique doit encore être validée positivement et négativement en runtime. La présentation UI peut être cachée ou désactivée côté négatif. West Bengal reste volontairement redistribuable. Aucun de ces risques ne justifie d’élargir le diff AE.

## 32. Verdict

`READY_FOR_BOMBAY_TRIGGER_RUNTIME_VALIDATION`.

## 33. Fichiers modifiés dans le fork

- modifié : `events/india_events/sepoy_mutiny_events.txt` ;
- créé : `docs/reports/hotfix/HOTFIX_5C2E4C1AE_E2_BOMBAY_TRIGGER_FIX.md` ;
- créé : `docs/reports/hotfix/HOTFIX_5C2E4C1AE_E2_TRIGGER_FIX_MANIFEST.csv`.

## 34. Fichiers modifiés dans la copie

Uniquement `events/india_events/sepoy_mutiny_events.txt`. Aucun ajout, suppression ou harnais modifié.

## 35. Confirmation Sepoy et journal

Sepoy fork/copie est identique au nouveau hash. Le journal fork/copie reste à 16 040 octets, SHA-256 `DAEFCB59CCF6B303D2E39C948D8038006C1346AFE40A2B812D45EE4D947E361C`.

## 36. Confirmation Bengal/Madras/Bombay/Travancore/MARATH

2.b Bengal, 2.c Madras, les deux protections Bombay C1W, Travancore, East Bengal, COO, MARATH/SAT/KHP, NAVY et ADMIN sont inchangés. West Bengal n’est ni protégé ni exclu.

## 37. Confirmation docs/research/technology/

Le répertoire non suivi `docs/research/technology/` est resté intact et hors périmètre.

## 38. Confirmation stash MARATH

`stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` est intact. Aucun apply, pop, drop ou commit automatique n’a été exécuté.
