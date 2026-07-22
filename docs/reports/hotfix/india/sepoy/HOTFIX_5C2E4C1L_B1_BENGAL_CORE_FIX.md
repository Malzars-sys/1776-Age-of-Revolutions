# HOTFIX-5C2E4C1L — Correction du noyau bengali B-1

## 1. Résumé

La correction minimale de `sepoy_mutiny_events.2.b` exclut désormais les portions BIC de `STATE_WEST_BENGAL` et `STATE_EAST_BENGAL` des deux ensembles de redistribution générique : garde de boucle et sélection. Le harnais B-1 jetable ajoute avant l'ouverture de l'événement une baseline déterministe de 1 % de radicaux aux pops hindoues et sunnites des portions BIC des deux Bengales. Aucun test runtime n'a été lancé. Verdict statique : **READY_FOR_B1_FIX_RUNTIME_TEST**.

## 2. État Git initial

Racine confirmée : `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork`. Branche : `hotfix-dlc-audit`. HEAD : `ccb293c Document Sepoy Bengal retreat failure`. La reprise de phase présentait déjà le seul fichier gameplay autorisé modifié, `events/india_events/sepoy_mutiny_events.txt`; aucun autre fichier suivi n'était modifié. La baseline antérieure est attestée par Git et le manifeste C1J.

## 3. Exception `docs/research/technology/`

`docs/research/technology/` était et demeure le seul chemin non suivi préexistant hors livrables C1L. Il n'a été ni modifié ni utilisé.

## 4. Vérification de la copie

La copie jetable existe, contient exactement 964 fichiers, aucun dossier `.git`, aucun `remote_file_id`, exactement vingt fichiers de harnais (racine, A-1, A-2, A-3 et B-1), aucun scénario C/E/F et aucune sauvegarde `.v3`. Les seize anciens fichiers correspondent tous au manifeste C1J; les fichiers A-3 ont les hashes tooltip propres C1I1. Avant la phase, les deux sources Sepoy avaient la même taille (63 210) et le même SHA-256 (`557936500AC585F7F69B9F5B063BDDA377AFF4A5AFAA06C70650C55D4AD612F7`). Les sauvegardes C1K sont hors copie.

## 5. Résultat C1K reproduit depuis le rapport

Le fonctionnement technique avait réussi : une ouverture, une nouvelle partie BIC, choix manuel exclusif de 2.b, boucle terminée, BIC toujours jouée, aucun owner nul et COO/JEY indépendants. Le résultat territorial était incorrect : West Bengal BIC → COO; East Bengal BIC → COO; Bihar BIC → NAG; portion BIC d'Awadh → AWA; portion BIC de Bundelkhand → MARATH; portion BIC des Northern Circars → HYD; reliquat BIC persistant à Pegu. BIC survivait sans noyau bengali. L'effet radical n'était pas validé, le compteur restant nul.

## 6. Cause racine

Les deux Bengales appartiennent à `region_north_india`. Après l'indépendance de COO, ils satisfont le filtre géographique et possèdent un voisin dont la culture primaire a l'héritage sud-asiatique et dont la capitale est en North/South India : COO. Aucune exclusion bengalie n'existait dans la garde ou la sélection générique. La portée `any_scope_state`/`random_scope_state` sous `root` limite implicitement les candidats aux states encore possédés par BIC; aucun `owner = root` explicite n'est nécessaire.

## 7. Structure complète de la boucle 2.b

Avant la boucle, `every_country` libère les sujets admissibles, puis les branches prioritaires Madras, Mandalay/Pegu, Gujarat, Tenasserim, Travancore, Circars/Kurnool, Delhi/Agra, Awadh, Central Provinces et Bombay s'exécutent dans leur ordre original. La boucle générique commence ligne 956; sa garde examine les states BIC restants, puis `every_country` parcourt les receveurs culturellement et géographiquement admissibles, sauvegarde `prince_scope`, et `random_scope_state` cède un state adjacent à ce receveur. Le scope est effacé à chaque tour. Les radicaux sont appliqués après la boucle.

## 8. Conditions de continuation

La garde (lignes 956–984) exige : state BIC dans North India, South India, Himalayas, Pashtunistan ou Quetta; state hors West/East Bengal; voisin dont une culture primaire possède `heritage_group_south_asian`; capitale du propriétaire voisin en North/South India, Pashtunistan ou Quetta.

## 9. Conditions de sélection

`every_country` (985–997) énumère exactement les pays au profil culturel/capital requis. Pour chacun, `random_scope_state` (999–1017) reprend le même filtre géographique, les deux mêmes exclusions et exige un voisin dont l'owner est `scope:prince_scope`. `set_state_owner` ne s'exécute qu'après une sélection valide.

## 10. Divergence potentielle des filtres

Une correction limitée à `random_scope_state` aurait laissé la garde vraie avec seulement un Bengal protégé admissible, créant un tour sans sélection et un risque de non-terminaison. Les exclusions sont donc présentes dans les deux prédicats territoriaux équivalents.

| Occurrence | Ligne | Type | Scope | Fonction | West admissible avant | East admissible avant | Modification |
|---|---:|---|---|---|---|---|---|
| Trigger de 2.b | 607 | `any_scope_state` | BIC/root | Rend l'option accessible | oui, intentionnel | sans objet | aucune |
| Poids IA | 599 | `has_state_in_state_region` | BIC | Pondération seulement | sans objet | oui, intentionnel | aucune |
| Libération des sujets | 623 | `every_country` | monde/pays | Rend les sujets admissibles indépendants | pas un filtre de state BIC | idem | aucune |
| Branches prioritaires | 655–953 | `if`/states nommés | BIC/root | Transferts historiques | non ciblé | non ciblé | aucune |
| Garde de boucle | 958–983 | `any_scope_state` + `any_neighbouring_state` | states BIC | Décide la continuation | oui | oui | `NOR` ajouté lignes 966–969 |
| Parcours receveurs | 985–997 | `every_country` | pays | Culture/capitale des receveurs | indirect | indirect | aucune; cohérent avec le voisin de garde |
| Sélection | 999–1017 | `random_scope_state` + voisin | states BIC | Choisit puis transfère | oui | oui | même `NOR` ajouté lignes 1008–1011 |
| Radicaux finaux | 1022–1034 | `every_scope_state` | states BIC restants | Cible North India | oui après correction | oui après correction | aucune |

## 11. Définition du noyau bengali

Le noyau protégé est exactement toute portion encore possédée par BIC dans `STATE_WEST_BENGAL` et toute portion encore possédée par BIC dans `STATE_EAST_BENGAL`. La correction ne crée, ne fusionne, ne restitue et ne contrôle aucune portion; elle n'annexe pas COO et ne protège aucun autre state.

## 12. Exemples syntaxiques vanilla

Recherche effectuée avec `Get-ChildItem` et `Select-String`, complétée par une recherche contextuelle. Dans `game/events/agitators_events/natural_borders.txt`, lignes 727–732, un `NOR` dans un filtre de state exclut quatre `state_region`; lignes 785–802, un `every_scope_state.limit` emploie le même modèle avant `set_state_owner`. Dans `game/events/balkans_events/austria_federalism.txt`, lignes 1422–1431, `NOR` nie plusieurs prédicats contenant `any_scope_state` et `state_region`. Aucun `state_region !=` attesté n'a été trouvé. `NOR = { state_region = ... }` est donc une syntaxe directement attestée dans Victoria 3 1.13, en scope state et avec exclusions multiples.

## 13. Correction West Bengal

`state_region = s:STATE_WEST_BENGAL` a été ajouté à un `NOR` dans la garde et au `NOR` identique de la sélection. Les portions déjà COO ou tierces ne sont jamais dans les scopes BIC et ne changent pas.

## 14. Correction East Bengal

La même exclusion a été ajoutée aux deux mêmes ensembles pour `STATE_EAST_BENGAL`.

## 15. Nombre exact d'emplacements modifiés

Deux blocs `NOR`, quatre lignes d'exclusion au total : deux state regions dans la garde et les deux mêmes dans la sélection. Le diff gameplay contient huit lignes ajoutées et aucune suppression.

## 16. Cohérence loop guard/sélection

Les ensembles géographiques et exclusions sont textuellement identiques. La garde existe s'il y a au moins un couple state/receveur valide; `every_country` visite tous les receveurs du même domaine, et la sélection recherche un state adjacent au receveur courant.

## 17. Preuve d'absence de boucle vide

Si la garde est vraie, son `any_neighbouring_state.owner` désigne un pays satisfaisant culture et capitale. Ce pays sera inclus par `every_country`; pour ce `prince_scope`, le state témoin satisfait le filtre identique de `random_scope_state`. Au moins un transfert se produit. Les Bengales seuls ne peuvent plus maintenir la garde vraie.

## 18. Préservation des branches prioritaires

Le diff commence après toutes les branches prioritaires et ne change ni leur ordre, ni leurs receivers, ni leurs conditions. Les transferts Bihar/NAG, Awadh/AWA, Bundelkhand/MARATH, Circars/HYD et Pegu restent gouvernés par le code antérieur.

## 19. Préservation des autres options

Le diff Git se limite aux lignes 963–1011 de 2.b. 2.a, 2.c, 2.d, 2.e, événements .3/.4, namespace, triggers d'accès, poids IA, localisations gameplay et journal sont inchangés.

## 20. Comparaison fork/copie

Après correction, les deux `sepoy_mutiny_events.txt` font 63 422 octets et ont le SHA-256 `FFB4060E659FB8A30691E26BA5BBDA838650EF11AB1760C89EDACFA2310D9BBE`; ils sont identiques octet par octet.

## 21. Audit exact des radicaux

| Effet | Syntaxe exacte | Sémantique attestée | Baseline C1K | Pourquoi zéro | Baseline retest |
|---|---|---|---:|---|---|
| Hindous | `add_radicals_in_state = { religion = rel:hindu value = large_radicals }` | 10 % des pops filtrées deviennent plus radicales | 0 | après les transferts, aucun state BIC de North India ne restait dans le scope | 1 % préalable dans les Bengales protégés |
| Sunnites | `add_radicals_in_state = { religion = rel:sunni value = large_radicals }` | même sémantique pour les pops sunnites | 0 | même scope vide | même baseline 1 % |

L'effet n'ajoute pas un nombre fixe et n'applique pas 10 % aux radicaux existants. `common/script_values/event_values.txt` définit `large_radicals = 0.1`; `localization/english/effects_l_english.yml:586` affiche que cette part du filtre devient plus radicale. Il s'exécute après les transferts, sur chaque state BIC restant dans `region_north_india`.

## 22. Cause de la baseline nulle

L'interprétation C1K « 10 % de zéro reste zéro » n'est pas confirmée par le code. La cause structurelle est que West/East Bengal avaient déjà été cédés et que le reliquat BIC de Pegu était hors North India : `every_scope_state.limit` n'avait plus de cible. La correction rend à nouveau la cible observable; la baseline non nulle permet en plus une comparaison avant/après explicite.

## 23. API de baseline retenue

Le harnais utilise la même API vanilla `add_radicals_in_state`, avec `very_small_radicals`. `common/script_values/event_values.txt:1` atteste `very_small_radicals = 0.01`, valeur nommée la plus petite (devant `small_radicals = 0.02`). Des usages vanilla de l'API avec filtres et valeurs nommées figurent notamment dans `common/history/global/00_global.txt:1115–1122`.

## 24. Ciblage radical du harnais

Dans l'option explicite de préparation seulement, `every_scope_state` reste sous BIC et limite West/East Bengal; chaque effet filtre `rel:hindu` ou `rel:sunni`. Aucun state hors des deux Bengales, donc aucun hors North India, n'est touché.

## 25. Modifications du harnais B-1

La décision exige désormais une portion BIC dans chacun des deux Bengales et au moins une pop hindoue/sunnite ciblable. L'événement de préparation ajoute la baseline, puis pose l'unique marqueur. Deux décisions, un événement, deux options, un seul appel manuel à `sepoy_mutiny_events.2`, chance IA nulle et zéro choix automatique sont conservés.

## 26. Tooltips

Les triggers complexes visibles restent dans des `custom_tooltip` évalués, selon le modèle A-3 propre. Aucun trigger n'est remplacé par un texte non évalué.

## 27. Localisations EN/FR

Les deux langues précisent : noyau West/East protégé, zéro mutation territoriale, baseline jetable de 1 %, relevés après préparation et avant 2.b, option 2.b manuelle, sauvegarde pré-option immuable et interdiction des sauvegardes A.

## 28. Contrôles BOM/LF

Les quatre fichiers B-1 ont un BOM UTF-8 et uniquement des fins de ligne LF. Les localisations EN/FR conservent les accents et dix clés chacune.

## 29. Validation statique gameplay

Accolades équilibrées; syntaxe `NOR/state_region` attestée; exactement deux exclusions West et deux East dans les ensembles génériques; garde et sélection cohérentes; aucune branche prioritaire, aucun autre event et aucun transfert non lié modifié; aucun terme ou scope nouveau autre que les state regions attestées.

Pseudo-flux : BIC possède West/East Bengal → 2.b disponible → sujets admissibles indépendants → reprises prioritaires inchangées → boucle générique ignore explicitement West/East Bengal → autres portions redistribuées → BIC conserve ses portions bengalies → radicaux appliqués aux states BIC restants de North India → BIC reste jouée avec un noyau bengali réel.

## 30. Validation statique harnais

Préparation territoriale : zéro. Baseline : déterministe, 1 %, BIC seulement, West/East Bengal seulement, hindous/sunnites seulement. L'événement réel n'est pas appelé pendant la préparation. Un marqueur, un appel manuel, aucune option automatique, tooltips propres, localisations complètes, BOM/LF conformes.

## 31. Résumé du manifest

Le manifeste inventorie les deux sources Sepoy, les deux journaux, les quatre fichiers B-1, les seize anciens harnais, le descriptor, le marqueur, le descripteur launcher et les deux livrables. Les contrôles inchangés reprennent leurs empreintes C1J; le manifeste se marque `SELF_REFERENTIAL`.

## 32. PLAN RUNTIME CONDENSÉ APRÈS CORRECTION

1. Ouvrir Victoria 3 une seule fois.
2. Démarrer une seule nouvelle partie BIC.
3. Relever owners/controllers et portions territoriales initiales.
4. Exécuter la préparation B-1 avec baseline radicale, sans mutation territoriale.
5. Relever les radicaux après préparation sur les mêmes pops/states.
6. Créer une sauvegarde pré-option immuable.
7. Ouvrir manuellement l'événement réel.
8. Choisir exclusivement 2.b.
9. Relever territoire et diplomatie après 2.b.
10. Vérifier que les portions BIC de West et East Bengal restent BIC.
11. Comparer les radicaux des mêmes populations et states.
12. Vérifier les autres transferts, COO et JEY.
13. Laisser passer au maximum un jour si l'interface doit se stabiliser.
14. Créer une sauvegarde post-option distincte.
15. Fermer le jeu une seule fois.
16. Analyser les logs seulement après fermeture.
17. Ne créer aucune session GBR.
18. Ne faire aucune relance.

Toute ouverture supplémentaire serait marquée `TECHNICALLY_REQUIRED` avec justification d'une impossibilité technique démontrée.

## 33. Nombre prévu d'ouvertures

Une.

## 34. Nombre prévu de fermetures

Une.

## 35. Observations avant préparation

Pays joué BIC; owners/controllers et portions de West/East Bengal, Bihar, Awadh, Bundelkhand, Northern Circars et Pegu; statut COO/JEY; populations hindoues/sunnites et radicaux correspondants.

## 36. Observations après préparation

Carte et diplomatie strictement inchangées; baseline non nulle de 1 % dans les populations ciblées; marqueur prêt; sauvegarde pré-option distincte et immuable.

## 37. Observations après 2.b

Boucle terminée; BIC jouée; West/East Bengal toujours BIC; COO/JEY indépendants selon le code; Bihar, Awadh, Bundelkhand, Circars et Pegu conformes; aucun owner nul; radicaux comparés dans le même scope.

## 38. Critères territoriaux

PASS seulement si les deux portions BIC bengalies restent BIC, les autres transferts principaux restent conformes, aucun owner n'est nul et la boucle termine.

## 39. Critères radicaux

PASS seulement si la baseline est non nulle, l'effet final augmente les pops religieuses ciblées dans les states BIC restants de North India et aucun effet n'apparaît hors North India.

## 40. Risques restants

Le choix générique des autres states demeure aléatoire comme avant. Une lecture UI agrégée peut masquer les variations par religion; il faudra relever exactement les mêmes pops et states. Aucun runtime n'a encore validé la correction.

## 41. Verdict

**READY_FOR_B1_FIX_RUNTIME_TEST**

## 42. Fichiers modifiés dans le fork

- `events/india_events/sepoy_mutiny_events.txt`
- `docs/reports/hotfix/HOTFIX_5C2E4C1L_B1_BENGAL_CORE_FIX.md` (créé)
- `docs/reports/hotfix/HOTFIX_5C2E4C1L_B1_FIX_MANIFEST.csv` (créé)

## 43. Fichiers modifiés dans la copie

- `events/india_events/sepoy_mutiny_events.txt`
- `common/decisions/zz_sepoy_functional_test_b1.txt`
- `events/zz_sepoy_functional_test_b1_events.txt`
- `localization/english/zz_sepoy_functional_test_b1_l_english.yml`
- `localization/french/zz_sepoy_functional_test_b1_l_french.yml`

## 44. Confirmation journal Sepoy inchangé

Fork et copie : 16 040 octets, SHA-256 `DAEFCB59CCF6B303D2E39C948D8038006C1346AFE40A2B812D45EE4D947E361C`.

## 45. Confirmation anciens harnais inchangés

Les seize hashes racine/A-1/A-2/A-3 correspondent exactement au manifeste C1J.

## 46. Confirmation `docs/research/technology/`

Le dossier reste non suivi, hors périmètre et intact.

## 47. Confirmation stash MARATH

`stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` est présent et n'a été ni appliqué, ni modifié, ni supprimé.
