# HOTFIX-5C2E4C1S — Correction statique du noyau Madras de l’option 2.c

## 1. Résumé

La redistribution générique de `sepoy_mutiny_events.2.c` pouvait sélectionner toute portion BIC de `STATE_MADRAS`, alors que cette option doit laisser à BIC son noyau de retraite à Madras. La correction ajoute le même filtre `NOR` dans la garde du `while` et dans le `random_scope_state`. Six lignes sont ajoutées, sans remplacement ni suppression. Le verdict statique est **READY_FOR_C1_FIX_RUNTIME_TEST**.

## 2. État Git initial

- racine : `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork` ;
- branche : `hotfix-dlc-audit` ;
- HEAD : `8bd3f00 Document Sepoy Madras retreat failure` ;
- aucun fichier suivi modifié ;
- seule entrée non suivie : `docs/research/technology/` ;
- stash : `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`.

Les préconditions de source étaient donc satisfaites avant toute écriture.

## 3. Exception `docs/research/technology/`

Cette arborescence non suivie préexistante n’a été ni lue pour établir la correction, ni modifiée, ni incluse dans les livrables.

## 4. Vérification de la copie

La copie jetable contenait exactement 968 fichiers, exactement 24 fichiers `zz_sepoy*`, dont les quatre fichiers C-1 attendus, aucun dossier `.git` et aucune occurrence de `remote_file_id`. Avant correction, son fichier Sepoy était identique octet par octet à celui du fork : 63 422 octets, SHA-256 `FFB4060E659FB8A30691E26BA5BBDA838650EF11AB1760C89EDACFA2310D9BBE`.

Les 31 contrôles non auto-référents pertinents du manifeste C1Q ont été recalculés avant écriture : aucune divergence. Cela couvre les quatre fichiers C-1, les vingt anciens harnais, le journal Sepoy, `descriptor.mod`, le marqueur et le descripteur launcher.

## 5. Défaut C1R reproduit depuis le rapport

Le rapport C1R et son CSV établissent la séquence suivante :

- `xABADB1` appartient à FRA avant préparation, puis à BIC après l’unique mutation de préparation ;
- après le choix exclusif de 2.c, `xABADB1` appartient à PUD ;
- le region state BIC 473 devient vide ;
- le region state PUD 475 passe de 24 à 25 provinces ;
- le region state DENNOR 474 et `x10B060` restent inchangés ;
- BIC reste le pays joué, la boucle termine et aucun owner nul n’est créé ;
- la baseline radicale profonde est confirmée ;
- `large_radicals` ne s’applique pas à Madras, conformément à l’ordre du script, car BIC a déjà perdu cette portion avant le bloc final.

Le fonctionnement technique de la boucle est donc valide, son résultat territorial est fonctionnellement incorrect pour l’option de retraite à Madras, et le résultat radical observé est cohérent avec cet ordre d’exécution.

## 6. Cause racine

`STATE_MADRAS` satisfait le filtre géographique `region_south_india`. Avant C1S, aucune exclusion ne l’écartait de la garde ou de la sélection générique. La portion BIC préparée pouvait donc maintenir le `while` vrai puis être tirée par `random_scope_state` au profit d’un voisin culturellement admissible, PUD dans C1R.

## 7. Structure de la boucle 2.c

Les lignes ci-dessous sont celles du fichier corrigé.

| Occurrence | Ligne | Scope | Fonction | Madras admissible avant | Modification nécessaire | Madras admissible après |
|---|---:|---|---|---|---|---|
| `while` | 1349 | BIC/root | Répète la redistribution tant qu’un candidat existe | Oui | Aucune directement | Non via sa garde |
| `any_scope_state` | 1351 | states possédés par BIC | Cherche un state territorialement et voisinage-admissible | Oui | Ajouter l’exclusion territoriale | Non |
| `OR` géographique | 1352–1358 | state candidat | Inde du Sud/Nord/Himalaya/Pashtunistan/Quetta | Oui, par South India | Inchangé | Oui avant composition avec `NOR` |
| `NOR STATE_MADRAS` | 1359–1361 | state candidat | Exclut exactement Madras | Absent | Ajouté | Non |
| `any_neighbouring_state` | 1362–1374 | voisins du candidat | Exige un owner à héritage sud-asiatique et capitale admissible | Oui | Inchangé | Sans objet pour Madras |
| filtre culturel | 1364–1365 | culture du voisin | Héritage sud-asiatique | Oui si voisin conforme | Inchangé | Inchangé |
| filtre de capitale | 1367–1372 | owner du voisin | Capitale dans les régions admises | Oui si voisin conforme | Inchangé | Inchangé |
| `every_country` | 1377–1410 | tous les pays | Visite chaque receveur culturellement/capitalement admissible | Oui indirectement | Inchangé | Ne peut plus tirer Madras |
| `save_scope_as` | 1389 | pays receveur | Mémorise le receveur courant | Oui indirectement | Inchangé | Inchangé |
| `random_scope_state` | 1391 | states de BIC/root | Tire un candidat adjacent au receveur courant | Oui | Ajouter la même exclusion | Non |
| `OR` géographique | 1393–1399 | state candidat | Même ensemble géographique que la garde | Oui | Inchangé | Oui avant composition avec `NOR` |
| `NOR STATE_MADRAS` | 1400–1402 | state candidat | Exclut exactement Madras | Absent | Ajouté | Non |
| voisinage du receveur | 1403–1405 | voisins du candidat | Owner égal à `prince_scope` | Oui si PUD voisin | Inchangé | Sans objet pour Madras |
| `set_state_owner` | 1407 | state sélectionné | Transfère le state au receveur | Oui | Inchangé | Ne reçoit jamais Madras |
| fin d’itération | 1411–1412 | boucle | Efface le scope puis réévalue la garde | Oui | Inchangé | Madras seul ne maintient pas la garde |
| `every_scope_state` final | 1413–1425 | states BIC restants | Applique `large_radicals` aux states de South India | Madras seulement s’il survivait | Inchangé | Madras BIC est désormais inclus |

## 8. Garde de continuation

Le prédicat territorial de `any_scope_state` compose désormais l’ancien `OR` géographique avec :

```text
NOR = {
    state_region = s:STATE_MADRAS
}
```

Madras ne peut plus, à lui seul, rendre la garde vraie.

## 9. Sélection `random_scope_state`

Le `limit` de `random_scope_state` contient le même `NOR`, au même niveau que le filtre géographique et avant le test de voisinage. Madras ne peut donc plus être sélectionné pour `set_state_owner`.

## 10. Modèle Bengal réutilisé

La correction déjà validée de 2.b emploie un `NOR` contenant `STATE_WEST_BENGAL` et `STATE_EAST_BENGAL` aux lignes 966–969 de la garde, puis un ensemble textuellement identique aux lignes 1008–1011 de la sélection. C1M/C1P a validé la terminaison de cette boucle et C1P a validé la conservation des deux portions Bengal et l’effet radical profond. C1S reprend uniquement cette syntaxe attestée, avec le seul `STATE_MADRAS`, sans recopier ni modifier aucun élément de 2.b.

## 11. Définition du noyau Madras

Le noyau protégé est exactement toute portion de `STATE_MADRAS` encore possédée par BIC, parce que les deux filtres s’exécutent dans les scopes de states de BIC/root. Le filtre ne transfère rien à BIC, ne fusionne aucun split state et ne restaure aucune portion déjà perdue. Dans C-1, seule `xABADB1`, devenue BIC lors de la préparation, est protégée ; FRA, DENNOR et PUD conservent leurs portions propres.

## 12. Correction de la garde

Trois lignes ont été ajoutées après l’ancien `OR` géographique de la garde, lignes 1359–1361. Aucun autre terme de la garde n’a changé.

## 13. Correction de la sélection

Trois lignes identiques ont été ajoutées après l’ancien `OR` géographique du `random_scope_state`, lignes 1400–1402. Le hasard, le voisinage, le receveur et l’effet de transfert restent inchangés.

## 14. Nombre exact de lignes ajoutées

Le diff gameplay contient exactement **6 ajouts, 0 suppression** : deux blocs `NOR` de trois lignes chacun.

## 15. Cohérence garde/sélection

Les ensembles territoriaux de la garde et de la sélection restent identiques : même `OR` géographique et même exclusion unique `STATE_MADRAS`. Il n’existe donc ni candidat admis seulement par la garde, ni candidat admis seulement par la sélection du fait du correctif.

## 16. Preuve d’absence de boucle vide

Si la garde est vraie, elle fournit au moins un state BIC non-Madras qui satisfait le filtre géographique et possède un voisin dont l’owner satisfait les filtres culturel et de capitale. Cet owner est nécessairement visité par `every_country`. Quand il est mémorisé dans `prince_scope`, le même state satisfait le `limit` de `random_scope_state`, car celui-ci possède le même filtre territorial et teste précisément un voisin appartenant à `prince_scope`. Au moins un `set_state_owner` est donc possible pendant l’itération. Si seuls des states Madras protégés subsistent, le `NOR` rend la garde fausse et le `while` se termine sans dépendre de Madras.

## 17. Préservation des branches prioritaires

Le bloc `hidden_effect` précédant le `while`, y compris Mandalay/Pegu, Gujarat, Tenasserim, Travancore, Delhi, Agra, Awadh, Central Provinces et Bombay, est inchangé. L’ordre des branches et leurs effets sont inchangés ; COO et JEY peuvent toujours devenir indépendants par les blocs antérieurs.

## 18. Préservation des radicaux

Le `every_scope_state` final et ses deux appels `add_radicals_in_state` (`hindu`, `sunni`, `large_radicals`) sont inchangés. La correction permet simplement à la portion Madras BIC survivante d’être encore dans ce scope au moment prévu.

## 19. Préservation des autres options

Le diff Git démontre que 2.a, 2.b — y compris ses exclusions West/East Bengal — et 2.e sont inchangées. Les events .3 et .4, le namespace et toutes les autres parties du fichier sont inchangés.

## 20. Comparaison fork/copie

Après correction, les deux fichiers Sepoy font 63 540 octets et ont le SHA-256 `98C4A50C1DCF2CE79B13AFF82B1FE461651BB99A9B42B002914FD10C338FDCAD`. `fc /b` ne trouve aucune différence. Ils conservent le BOM UTF-8 `EF BB BF` et le style LF préexistant : 2 957 LF avant, 2 963 après les six ajouts, sans octet CR.

## 21. Validation statique

- accolades : 970 ouvrantes et 970 fermantes ;
- exactement deux nouvelles occurrences de `STATE_MADRAS` par rapport à HEAD, une dans la garde et une dans la sélection ;
- aucune autre nouvelle occurrence Madras ;
- filtres garde/sélection identiques ;
- syntaxe `NOR`, `state_region` et scope attestée par 2.b ;
- aucune branche prioritaire, aucun effet radical et aucun autre event modifié ;
- `git diff --check` sans erreur ;
- fork et copie identiques octet par octet.

## 22. Contrôle du harnais C-1

Les quatre tailles et SHA-256 restent exactement ceux du manifeste C1Q :

| Fichier | Taille | SHA-256 |
|---|---:|---|
| `common/decisions/zz_sepoy_functional_test_c1.txt` | 1 496 | `CCF4F7B97AB864631D94DAF641D58065F020FB9FC11FF5FBDE30EA75D9BD1373` |
| `events/zz_sepoy_functional_test_c1_events.txt` | 1 462 | `E4D8EFC14CD004268D33CE374F50FD71B0587DB358DF498AB0251B962F34E313` |
| `localization/english/zz_sepoy_functional_test_c1_l_english.yml` | 2 345 | `FA8DED06482051D664529F133FDE1F43406A3C22C3BA4F2DD41EDDB76E9C5F26` |
| `localization/french/zz_sepoy_functional_test_c1_l_french.yml` | 2 731 | `2FD0E74D30B0A89321F0FBA707AF29270F9D52A9BD7166BADA9A6E4E1386135C` |

Le code conserve une seule mutation FRA → BIC, une baseline de 1 %, un seul marqueur, un seul appel manuel à l’event 2 et aucune option automatique. Aucun changement ne masque le défaut.

## 23. Résumé du manifeste

Le manifeste C1S recense 33 lignes de données : deux sources Sepoy modifiées, deux journaux contrôles, quatre fichiers C-1, vingt anciens harnais, trois contrôles copie/launcher et deux livrables C1S. Le manifeste est auto-référentiel et porte donc le statut `SELF_REFERENTIAL` pour sa propre ligne.

## 24. Plan runtime condensé

Une seule ouverture de Victoria 3 ; une seule nouvelle partie BIC ; aucune session GBR ; préparation C-1 FRA → BIC ; contrôle rapide des trois portions Madras ; sauvegarde pré-2.c ; ouverture manuelle de l’event ; choix exclusif de 2.c ; contrôle immédiat de `xABADB1`, DENNOR et PUD ; contrôle rapide de la terminaison et des sujets ; analyse profonde immédiate de `large_radicals` ; ticks seulement si nécessaires à l’UI ; fermeture finale unique ; analyse des logs et sauvegardes après fermeture. Aucun transfert déjà validé par C1R ne doit être réaudité au-delà du nécessaire.

## 25. Critères du futur runtime

Le retest doit établir que `xABADB1` reste BIC, que DENNOR et PUD restent distincts, que PUD reste à 24 provinces, que le region state BIC Madras reste réel et non vide, que la boucle termine, que BIC reste jouée, que les sujets attendus deviennent indépendants et que `large_radicals` est sérialisé sur les pops hindoues et sunnites de la portion Madras BIC.

Pseudo-flux attendu :

```text
BIC possède une portion Madras
→ 2.c disponible
→ sujets admissibles indépendants
→ branches prioritaires inchangées
→ boucle générique ignore STATE_MADRAS
→ autres states admissibles redistribués
→ portion Madras BIC conservée
→ radicaux appliqués aux states BIC restants de South India
→ BIC reste jouée avec un noyau Madras réel
```

## 26. Risques restants

La preuve est statique. Le moteur doit encore confirmer en runtime la conservation effective de la portion split-state et la matérialisation de `large_radicals`. Aucun nouveau risque de divergence garde/sélection n’est introduit, les deux filtres étant textuellement cohérents.

## 27. Verdict

**READY_FOR_C1_FIX_RUNTIME_TEST**

Cause racine identifiée ; Madras exclu de la garde et de la sélection ; filtres cohérents ; aucune autre logique modifiée ; fork/copie identiques ; harnais C-1 inchangé ; validations statiques réussies ; futur runtime condensé en une session.

## 28. Fichiers modifiés dans le fork

- `events/india_events/sepoy_mutiny_events.txt` ;
- `docs/reports/hotfix/HOTFIX_5C2E4C1S_C1_MADRAS_CORE_FIX.md` (créé) ;
- `docs/reports/hotfix/HOTFIX_5C2E4C1S_C1_FIX_MANIFEST.csv` (créé).

## 29. Fichiers modifiés dans la copie

- `events/india_events/sepoy_mutiny_events.txt` uniquement.

La copie reste à 968 fichiers et aucun harnais n’y a été modifié.

## 30. Confirmation journal Sepoy

Le journal fork/copie reste à 16 040 octets, SHA-256 `DAEFCB59CCF6B303D2E39C948D8038006C1346AFE40A2B812D45EE4D947E361C`. Il est inchangé et identique dans les deux emplacements.

## 31. Confirmation anciens harnais

Les vingt harnais racine/A-1/A-2/A-3/B-1 conservent exactement les tailles et SHA-256 du manifeste C1Q. Avec les quatre C-1, la copie contient toujours exactement 24 harnais.

## 32. Confirmation Travancore/Bengal/Bombay/MARATH

`state_region = STATE_TRAVANCORE` et tous ses blocs sont intégralement inchangés. Les exclusions Bengal de 2.b, les branches Bombay et toute logique MARATH sont inchangées. Aucun fichier ou stash associé n’a été touché.

## 33. Confirmation `docs/research/technology/`

L’arborescence reste l’unique exception non suivie préexistante et n’a pas été touchée.

## 34. Confirmation stash MARATH

`stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` reste présent. Aucun `stash apply`, `pop` ou `drop` n’a été exécuté.
