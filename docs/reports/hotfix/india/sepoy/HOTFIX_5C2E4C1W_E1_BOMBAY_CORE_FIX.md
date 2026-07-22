# 1. Résumé

La phase C1W corrige minimalement la redistribution générique de `sepoy_mutiny_events.2.e`. Toute portion de `STATE_BOMBAY` encore possédée par BIC est désormais exclue à la fois de la garde du `while` et du `random_scope_state`. Le diff gameplay contient exactement six lignes ajoutées et aucune suppression. West Bengal reste entièrement inchangé et hors du périmètre correctif. Verdict : `READY_FOR_E1_FIX_RUNTIME_TEST`.

# 2. État Git initial

Racine : `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork`. Branche : `hotfix-dlc-audit`. HEAD : `632e542 Document Sepoy Bombay retreat failure`. Aucun fichier suivi n’était modifié. Le stash `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` était présent.

# 3. Exception docs/research/technology/

La seule exception non suivie initiale était `docs/research/technology/`. Elle est restée hors périmètre et intacte.

# 4. Vérification de la copie

Avant correction, le fork et la copie possédaient le même fichier Sepoy : 63 540 octets, SHA-256 `98C4A50C1DCF2CE79B13AFF82B1FE461651BB99A9B42B002914FD10C338FDCAD`. La copie contenait exactement 972 fichiers, 28 harnais dont quatre E-1, aucun `.git` et aucun `remote_file_id`. Les 35 contrôles applicables du manifeste C1U avaient zéro divergence. Victoria 3 et le launcher n’ont pas été lancés.

La source hotfix et la vanilla 1.13 ont été consultées en lecture seule. Leur fichier Sepoy commun fait 63 904 octets et porte le SHA-256 `14FE5650F573AA6E3AA8C3DA25B94F74F44DF2A3917B0F9DB7DBA5E84085E638` ; aucun octet n’y a été modifié.

# 5. Défaut C1V reproduit

C1V documente la chaîne exacte : `x51F0A0` appartient à POR avant préparation, à BIC après préparation, puis à KHP après 2.e. Le region state Bombay BIC 482 devient vide ; KHP passe de trois à quatre provinces ; MARATH reste à 25 provinces et SAT à 10. BIC reste joué, la boucle termine, aucun territoire réel n’a un owner nul et la baseline hindoue est confirmée. `large_radicals` n’atteint pas cette population parce que Bombay quitte BIC avant le bloc final. Séparément, la portion BIC de West Bengal est transférée à COO.

# 6. Cause racine Bombay

`STATE_BOMBAY` appartient à `region_south_india`. Avant C1W, une portion BIC de Bombay satisfaisait donc l’`OR` géographique de la garde et, si elle bordait un receveur admissible, maintenait le `while` vrai. Le même state satisfaisait le filtre géographique de `random_scope_state` et pouvait être cédé par `set_state_owner`. Le fonctionnement technique de la boucle était valide, mais son domaine territorial contredisait l’intention « Bombay tient bon ».

# 7. Résultat West Bengal séparé

West Bengal déclenche actuellement 2.e, reste redistribuable, et C1V a observé le transfert de sa portion BIC à COO. Ce résultat est distinct de la perte du noyau Bombay et ne détermine pas à lui seul le statut fonctionnel futur de West Bengal.

# 8. Décision de périmètre West Bengal

C1W ne protège pas `STATE_WEST_BENGAL`, ne modifie pas son trigger, ne remplace pas ce trigger par Bombay et n’ajoute pas Bombay au trigger. West Bengal n’est pas considéré comme un second noyau de retraite sans décision fonctionnelle séparée.

# 9. Structure de la boucle 2.e

Les lignes indiquées sont celles du fichier corrigé.

| Occurrence | Ligne | Scope | Fonction | Bombay admissible avant | West Bengal admissible avant | Modification Bombay nécessaire | Bombay admissible après | West Bengal admissible après |
|---|---:|---|---|---|---|---|---|---|
| `while` | 1740 | BIC/root | Répète la redistribution | Oui via sa garde | Oui | Aucune directement | Non via sa garde | Oui |
| garde `any_scope_state` | 1742 | states BIC | Cherche un candidat territorial | Oui | Oui | Exclusion sœur de l’OR | Non | Oui |
| `OR` géographique | 1743–1749 | state candidat | South/North India, Himalaya, Pashtunistan, Quetta | Oui par South India | Oui par North India | Inchangé | Oui avant composition avec le NOR | Oui |
| `NOR STATE_BOMBAY` | 1750–1752 | state candidat | Exclut exactement Bombay | Absent | Sans exclusion | Ajouter | Non | Oui |
| `any_neighbouring_state` | 1753–1765 | voisin du candidat | Trouve un owner receveur admissible | Oui si voisin conforme | Oui si voisin conforme | Inchangé | Sans objet pour Bombay | Oui |
| filtre culturel | 1755–1756 | culture du voisin | Héritage sud-asiatique | Oui conditionnellement | Oui conditionnellement | Inchangé | Inchangé | Inchangé |
| filtre de capitale | 1758–1763 | owner du voisin | Capitale géographiquement admissible | Oui conditionnellement | Oui conditionnellement | Inchangé | Inchangé | Inchangé |
| `every_country` | 1768–1801 | pays | Visite tous les receveurs admissibles | Oui indirectement | Oui indirectement | Inchangé | Ne peut plus tirer Bombay | Oui |
| `save_scope_as` | 1780 | pays receveur | Sauvegarde `prince_scope` | Oui indirectement | Oui indirectement | Inchangé | Inchangé | Inchangé |
| `random_scope_state` | 1782 | states BIC/root | Sélectionne un state adjacent | Oui | Oui | Exclusion identique | Non | Oui |
| `OR` de sélection | 1784–1790 | state candidat | Même domaine géographique | Oui | Oui | Inchangé | Oui avant composition avec le NOR | Oui |
| `NOR STATE_BOMBAY` | 1791–1793 | state candidat | Exclut exactement Bombay | Absent | Sans exclusion | Ajouter | Non | Oui |
| voisinage `prince_scope` | 1794–1796 | voisin du candidat | Owner égal au receveur courant | Oui conditionnellement | Oui conditionnellement | Inchangé | Sans objet pour Bombay | Oui |
| `set_state_owner` | 1798 | state sélectionné | Transfère au receveur | Oui | Oui | Inchangé | Ne reçoit jamais Bombay | Oui |
| `clear_saved_scope` | 1802 | boucle | Efface le receveur temporaire | Sans objet | Sans objet | Inchangé | Sans objet | Sans objet |
| `every_scope_state` final | 1804–1816 | states BIC survivants | Applique les radicaux en South India | Bombay seulement s’il survivait | Non ciblé géographiquement | Inchangé | Bombay BIC survivant est inclus | Inchangé |

# 10. Garde de continuation

Après l’`OR` géographique de la garde, C1W ajoute au même niveau logique :

```text
NOR = {
    state_region = s:STATE_BOMBAY
}
```

Bombay ne peut plus rendre la garde vraie.

# 11. Sélection random_scope_state

Le `limit` de `random_scope_state` reçoit le même `NOR`, après son `OR` géographique et avant le voisinage `prince_scope`. Bombay ne peut donc plus être tiré puis transmis à `set_state_owner`.

# 12. Modèles Bengal et Madras

Le modèle 2.b exclut `STATE_WEST_BENGAL` et `STATE_EAST_BENGAL` dans la garde et dans la sélection au moyen de deux `NOR` textuellement cohérents, au scope state BIC/root. C1P a validé la terminaison, la conservation du noyau bengali et l’effet profond `large_radicals`. Le modèle 2.c exclut de la même façon `STATE_MADRAS`; C1T a validé la terminaison, la conservation du noyau Madras et les deltas profonds hindous/sunnites. C1W réutilise uniquement cette syntaxe attestée avec le seul `STATE_BOMBAY`.

# 13. Définition du noyau Bombay

Le noyau protégé est exactement toute portion de `STATE_BOMBAY` encore possédée par BIC. Le filtre ne transfère rien à BIC, ne restaure rien, ne fusionne aucun split state, ne change aucun controller et ne modifie aucune portion POR, MARATH, SAT ou KHP. Dans E-1, seule `x51F0A0` déjà préparée pour BIC doit survivre.

# 14. Correction de la garde

Trois lignes sont ajoutées aux lignes 1750–1752. Elles excluent `STATE_BOMBAY` du prédicat territorial de continuation sans changer la géographie, le voisinage, la culture ou la capitale.

# 15. Correction de la sélection

Trois lignes identiques sont ajoutées aux lignes 1791–1793. Aucun appel aléatoire, receveur, ordre ou effet de transfert n’est ajouté ou déplacé.

# 16. Nombre exact de lignes ajoutées

`git diff --numstat` donne exactement `6 0 events/india_events/sepoy_mutiny_events.txt` : six ajouts et zéro suppression.

# 17. Cohérence garde/sélection

Les deux prédicats utilisent le même domaine géographique et la même exclusion unique `STATE_BOMBAY`. L’ordre South/North de la garde et North/South de la sélection diffère textuellement mais les ensembles sont logiquement identiques, comme avant C1W. Le correctif ne crée aucune divergence d’admissibilité.

# 18. Preuve d’absence de boucle vide

Si la garde est vraie, elle expose au moins un state BIC non-Bombay satisfaisant la géographie et un voisin dont l’owner satisfait culture et capitale. Cet owner est visité par `every_country`. Pour son `prince_scope`, le même state satisfait le filtre territorial identique de `random_scope_state` et le test de voisinage ; au moins un `set_state_owner` est donc possible. Si seuls des states Bombay protégés subsistent, le `NOR` rend la garde fausse et le `while` termine. Aucune correction limitée à la sélection n’a été faite.

# 19. Trigger West Bengal inchangé

Le trigger reste aux lignes 1434–1438 et contient toujours une unique occurrence `state_region = s:STATE_WEST_BENGAL` à la ligne 1436. Le comptage dans 2.e est 1 avant et 1 après. Le trigger et `ai_chance base = 40` ont un segment strictement identique à HEAD, SHA-256 normalisé `FBAD17C13DD81F00E447665732E9D2FEBEE1940FC2395AD2D8F8CA28203339C4`.

# 20. Redistributivité West Bengal inchangée

2.e contient zéro `NOR` visant West Bengal avant et après C1W. Ses branches prioritaires contiennent zéro occurrence West Bengal avant/après. West Bengal continue donc à satisfaire le domaine North India de la garde et de la sélection selon l’ancien comportement.

# 21. Préservation des sujets

Le bloc qui rend indépendants les sujets admissibles et retire le levier GBR est inchangé. COO et JEY restent éligibles exactement comme auparavant.

# 22. Préservation des branches prioritaires

Le `hidden_effect` précédent le `while` est strictement identique à HEAD. Madras/CAR, Mandalay/Pegu, Tenasserim, Travancore, Circars, Kurnool, Delhi, Agra, Awadh et Central Provinces gardent leurs conditions, effets et ordre. Il contient zéro nouvelle protection Bombay ou West Bengal.

# 23. Préservation des exceptions frontalières

Les conditions Himalaya, Pashtunistan et Quetta sont inchangées dans la garde, `every_country` et la sélection. Le filtre de capitale reste South India, North India, Pashtunistan ou Quetta.

# 24. Préservation des radicaux

Le `every_scope_state` final et ses deux appels `add_radicals_in_state` pour `hindu` et `sunni` avec `large_radicals` sont strictement identiques à HEAD. Leur segment normalisé porte le SHA-256 `787DA1AEA20077185483E108541619D30AFDE1EC97E1B9F7B7E89873501FF4B7`. La correction permet seulement au state Bombay BIC survivant de rester dans ce scope South India.

# 25. Préservation des autres options

Les blocs 2.a, 2.b et 2.c sont strictement identiques à HEAD, avec les SHA-256 normalisés respectifs `3A64F1A29B262CC37F1E4B1D0BC89ADF72A445DC25958FBD83A9ECF7CB0A5983`, `D787F7BD0F97070E8B5EED5B843B821163EC310C33FB8E48B575344178A7F3D7` et `8BA1F8A64BD0094ADC59B5A588E6A264BB576374CBCC3D808EDA4F4F2163FDEB`. Les protections Bengal et Madras ne changent pas. Les events .3 et .4, le namespace et tout le reste du fichier sont hors du diff.

# 26. Comparaison fork/copie

Après correction, les deux fichiers font 63 658 octets et portent le même SHA-256 `51F489F00FA6CB2D7BBF1D1FDC587104F2A17D4932187DAA8BBE954F7312A9FB`. Ils sont identiques octet par octet, conservent le BOM UTF-8, 2 969 LF et zéro octet CR.

# 27. Validation statique

- accolades avant : 970 ouvrantes / 970 fermantes ; après : 972 / 972 ;
- occurrences `STATE_BOMBAY` fichier : 18 avant, 20 après ;
- occurrences Bombay dans 2.e : 0 avant, 2 après ;
- une occurrence dans la garde et une dans la sélection ;
- occurrences West Bengal dans 2.e : 1 avant, 1 après ;
- suppression des deux blocs C1W du texte corrigé restitue exactement le bloc 2.e de HEAD ;
- branches prioritaires, trigger, sujets et radicaux inchangés ;
- `git diff --check` sans erreur ;
- aucune suppression gameplay ;
- fork et copie identiques.

# 28. Contrôle du harnais E-1

Les quatre fichiers E-1 correspondent exactement au manifeste C1U :

| Fichier | Taille | SHA-256 |
|---|---:|---|
| `common/decisions/zz_sepoy_functional_test_e1.txt` | 1 804 | `296C1FC7B58FB98081D9202A8F2191CD1D6E19E7194B6EA556E5503DC6513BB4` |
| `events/zz_sepoy_functional_test_e1_events.txt` | 1 620 | `FDFCEE011219F08F3FB3296310EC28959F6ACEEBA7FA63EED439F2E9A045C079` |
| `localization/english/zz_sepoy_functional_test_e1_l_english.yml` | 2 396 | `B214114C69916E07FB16FB5FE8721E14DC354B46304D05E724DE6B60B88DAA00` |
| `localization/french/zz_sepoy_functional_test_e1_l_french.yml` | 2 818 | `D5F1BB1EDC06C1C5DC48B756DF1E7E072ACE1C3F34B0E2A3ED4978297B7825FE` |

Le harnais conserve une seule mutation POR → BIC, aucune mutation MARATH/SAT/KHP, aucune mutation West Bengal, les deux appels `very_small_radicals`, un seul marqueur, un seul appel manuel à l’event 2 et aucune option automatique.

# 29. Résumé du manifeste

Le manifeste C1W inventorie 37 lignes : deux fichiers Sepoy modifiés, deux journaux, 28 harnais, le descripteur interne, le marqueur, le descripteur launcher et les deux livrables C1W. Les 35 contrôles hérités de C1U ne divergent que pour les deux fichiers Sepoy attendus.

# 30. Plan runtime condensé

Le futur retest utilisera une ouverture de Victoria 3, une nouvelle partie BIC, aucune session GBR, aucune relance et une fermeture finale. L’opérateur préparera E-1 POR → BIC, vérifiera rapidement West Bengal et les quatre portions Bombay, avancera jusqu’au 3 janvier, créera une sauvegarde pré‑2.e immuable, ouvrira manuellement l’événement et choisira uniquement 2.e. Il vérifiera immédiatement Bombay, MARATH/SAT/KHP, West Bengal séparément, la terminaison, BIC joué et COO/JEY, puis fermera le jeu après les seuls ticks UI nécessaires. Rakaly et les logs ne seront analysés qu’après fermeture.

# 31. Critères du futur runtime

Le retest doit prouver que `x51F0A0` reste BIC, que le region state Bombay BIC reste réel et non vide, que MARATH conserve 25 provinces, SAT 10, KHP 3, que la boucle termine, que BIC reste joué, que COO/JEY deviennent indépendants et qu’aucun owner réel n’est nul. West Bengal sera relevé sans devenir un critère de protection. L’analyse profonde immédiate doit rechercher `large_radicals` sur les pops hindoues Bombay BIC ; l’absence de cible sunnite restera un résultat nul attendu.

# 32. Risques restants

La conservation Bombay et l’exécution profonde des radicaux doivent encore être validées en runtime. West Bengal reste volontairement redistribuable et peut encore être perdu. Les agrégats/UI de radicaux peuvent être différés comme dans B-1/C-1. Aucun de ces risques ne justifie d’élargir C1W.

# 33. WEST_BENGAL_FUNCTIONAL_DECISION_DEFERRED

`WEST_BENGAL_FUNCTIONAL_DECISION_DEFERRED`. Son rôle de trigger, sa redistribution observée vers COO et son éventuelle protection doivent être arbitrés dans une phase séparée. Aucune correction West Bengal ne fait partie de C1W.

# 34. Verdict

`READY_FOR_E1_FIX_RUNTIME_TEST`.

La cause Bombay est identifiée ; Bombay est exclu symétriquement de la garde et de la sélection ; les filtres restent cohérents ; West Bengal et toute autre logique restent inchangés ; fork et copie sont identiques ; le harnais E-1 est intact ; les validations statiques réussissent ; le prochain runtime est condensé en une session.

# 35. Fichiers modifiés dans le fork

- modifié : `events/india_events/sepoy_mutiny_events.txt` ;
- créé : `docs/reports/hotfix/HOTFIX_5C2E4C1W_E1_BOMBAY_CORE_FIX.md` ;
- créé : `docs/reports/hotfix/HOTFIX_5C2E4C1W_E1_FIX_MANIFEST.csv`.

Aucun autre fichier du fork n’est modifié par C1W et aucun commit automatique n’est créé.

# 36. Fichiers modifiés dans la copie

Seul `events/india_events/sepoy_mutiny_events.txt` est modifié. La copie reste à 972 fichiers et 28 harnais ; aucun fichier n’est ajouté.

# 37. Confirmation journal Sepoy

Le journal `common/journal_entries/04_sepoy_mutiny.txt` reste inchangé dans le fork et la copie : 16 040 octets, SHA-256 `DAEFCB59CCF6B303D2E39C948D8038006C1346AFE40A2B812D45EE4D947E361C`.

# 38. Confirmation anciens harnais

Les 24 anciens harnais et les quatre fichiers E-1 correspondent tous au manifeste C1U. Aucun harnais, tooltip ou fichier de localisation n’a été modifié.

# 39. Confirmation Bengal/Madras/Travancore/MARATH

Les protections Bengal de 2.b et Madras de 2.c sont inchangées. Travancore, `STATE_TRAVANCORE`, MARATH, SAT et KHP ne sont pas dans le diff. Aucune donnée NAVY ou ADMIN n’est touchée.

# 40. Confirmation docs/research/technology/

`docs/research/technology/` reste non suivi, hors périmètre et intact.

# 41. Confirmation stash MARATH

Le stash `WIP NAVY-3C-3 Maratha Konkan Flotilla` reste présent. Aucune opération `stash apply`, `pop`, `drop` ou autre manipulation du stash n’a été effectuée.
