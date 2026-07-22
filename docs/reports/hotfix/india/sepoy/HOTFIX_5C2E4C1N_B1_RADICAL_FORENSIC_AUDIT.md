# HOTFIX-5C2E4C1N — Audit médico-légal des radicaux B-1

## 1. Résumé

L’audit confirme que le harnais B-1 appelle bien `add_radicals_in_state` dans les region states BIC de West Bengal et East Bengal avant de poser `zz_sepoy_test_b1_ready`. Les deux religions ciblées existent en grand nombre dans ces states. Les deux appels gameplay finaux de `sepoy_mutiny_events.2.b` reprennent exactement une API, un scope state, des filtres religieux et une valeur nommée attestés dans la vanilla Victoria 3 1.13.

Les trois sauvegardes sont toutefois toutes au `tick=0`, le 1er janvier 1776. Leurs données sérialisées donnent 0 radical BIC avant préparation, 0 après la préparation et 0 après 2.b. Le bloc BIC `pop_radicals_and_loyalists_statistics` est textuellement identique dans les trois sauvegardes fondues, et les 110 objets de pops hindoues/sunnites appartenant aux portions BIC des deux Bengales sont strictement identiques entre C1M pré-option et C1M post-option. Cela prouve l’absence de changement radical sérialisé, mais pas la raison de l’absence d’effet.

Cause classée : **`SAVE_EVIDENCE_INCONCLUSIVE`**. Aucun script n’est modifié. Verdict : **`BLOCKED_B1_RADICAL_CAUSE_UNPROVEN`**.

## 2. Intégrité initiale

- Racine : `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork`.
- Branche : `hotfix-dlc-audit`.
- HEAD/C1M : `f881fec704858bf80448a130593a7d610866ab11`, message `Validate Sepoy Bengal core preservation`; le commit contient les deux livrables C1M.
- Aucun changement suivi initial.
- Seuls éléments non suivis : les sept fichiers préexistants sous `docs/research/technology/`.
- Stash : `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`.
- Copie jetable : 964 fichiers.
- Manifeste C1L : toutes les 27 lignes non autoréférentielles ont été recalculées; 27 tailles et 27 SHA-256 conformes.
- Sepoy fork/copie : 63 422 octets, SHA-256 `FFB4060E659FB8A30691E26BA5BBDA838650EF11AB1760C89EDACFA2310D9BBE`, identité octet par octet.

La porte d’arrêt A est donc passée sans exception.

## 3. Audit du harnais

### Scope et chemin réellement cliqué

`zz_sepoy_test_b1_prepare.when_taken` (`common/decisions/zz_sepoy_functional_test_b1.txt:37-39`) déclenche `zz_sepoy_test_b1.1` depuis le pays qui prend la décision. L’event est explicitement un `country_event` (`events/zz_sepoy_functional_test_b1_events.txt:5-7`), et son trigger exige `c:BIC ?= this` (`:19-22`). Le scope racine de l’option est donc BIC.

L’option réellement cliquée `zz_sepoy_test_b1.1.prepare` (`:46-67`) contient les effets eux-mêmes; elle ne pose pas seulement le marqueur. Son ordre exact est :

1. `every_scope_state` sous BIC;
2. filtre `STATE_WEST_BENGAL` ou `STATE_EAST_BENGAL`;
3. `add_radicals_in_state = { religion = rel:hindu value = very_small_radicals }`;
4. `add_radicals_in_state = { religion = rel:sunni value = very_small_radicals }`;
5. seulement ensuite `set_variable = zz_sepoy_test_b1_ready`.

`every_scope_state` est utilisé ici en scope pays et parcourt les region states de ce pays. Le propriétaire attendu est donc BIC. La portion COO de West Bengal n’est pas visitée. Les sauvegardes confirment les objets internes suivants : East Bengal BIC = state 14/owner 218; West Bengal BIC = state 487/owner 218; West Bengal COO = state 488/owner 412; les définitions pays associent 218 à BIC et 412 à COO.

### Conditions et populations

Le trigger/tooltip exige une portion BIC dans chacun des deux Bengales et au moins une pop hindoue ou sunnite dans leur union. Il n’exige pas que les deux religions existent dans chaque state; un appel individuel peut donc être sans cible sans bloquer l’autre. Les saves éliminent néanmoins ce cas pratique :

| Region state | Religion | Objets de pop | Workforce | Dependents | Population sérialisée |
|---|---:|---:|---:|---:|---:|
| West Bengal BIC (487) | hindu | 60 | 3 372 835 | 9 698 406 | 13 071 241 |
| West Bengal BIC (487) | sunni | 11 | 1 008 029 | 2 814 087 | 3 822 116 |
| East Bengal BIC (14) | hindu | 29 | 1 572 900 | 4 419 100 | 5 992 000 |
| East Bengal BIC (14) | sunni | 10 | 4 044 625 | 11 363 477 | 15 408 102 |

Les filtres trouvent donc des populations valides. Le scope n’est pas un state region abstrait incorrect : les objets 14 et 487 sont les region states BIC possédés et contiennent les pops ciblées.

`very_small_radicals` se résout dans `common/script_values/event_values.txt:1` à `0.01`. Le nom est employé activement par la vanilla dans des effets `add_radicals`/`add_loyalists`; les effets `*_in_state` emploient de la même manière les valeurs nommées `small_radicals`, `medium_radicals` et `large_radicals`.

La seconde décision appelle une seule fois `sepoy_mutiny_events.2` (`common/decisions/zz_sepoy_functional_test_b1.txt:80-82`). Aucun `default_option`, choix automatique ou effet territorial n’existe dans les deux fichiers B-1.

### Tick journalier

Aucun script vanilla pertinent n’enveloppe l’effet dans un délai, un on-action journalier ou un pop scope. Statique­ment, l’effet est appelé directement lors du choix. En revanche, les trois saves auditées sont toutes au tick 0 et ne permettent pas d’observer le comportement après la première mise à jour journalière. Un tick d’un jour est donc justifié comme test discriminant futur, mais il n’est pas démontré comme correctif.

## 4. Audit gameplay

Dans le fork, les deux appels finaux de 2.b sont aux lignes 1026-1033, sous :

```text
every_scope_state = {
    limit = { region = sr:region_north_india }
    add_radicals_in_state = {
        religion = rel:hindu
        value = large_radicals
    }
    add_radicals_in_state = {
        religion = rel:sunni
        value = large_radicals
    }
}
```

Le scope de l’option reste le pays BIC. Après les transferts, `every_scope_state` visite les states encore possédés par BIC en North India, notamment les portions protégées de West/East Bengal. `large_radicals` vaut `0.1` (`common/script_values/event_values.txt:4`). Aucune enveloppe owner, aucun pop scope et aucun tick ne figurent dans le code vanilla identique. Rien ne démontre une erreur de l’API gameplay.

## 5. Exemples vanilla

La recherche lexicale exhaustive sur `common/**/*.txt` et `events/**/*.txt` trouve 484 occurrences de `add_radicals_in_state`, 154 de `add_loyalists_in_state`, 241 de `large_radicals` et 6 de `very_small_radicals`, commentaires compris. Les exemples actifs pertinents sont :

| Fichier et lignes | Scope d’appel | Syntaxe pertinente | Délai/owner/pop requis |
|---|---|---|---|
| `events/india_events/sepoy_mutiny_events.txt:1012-1024` | country option → `every_scope_state` North India | hindou + sunnite, `large_radicals` | aucun |
| même fichier `:1397-1409` | country option → `every_scope_state` South India | mêmes deux filtres et même valeur | aucun |
| `events/india_events/communal_divides_events.txt:241-249` | `scope:relevant_state` | sunnite + hindou, `medium_radicals` | aucun |
| `events/india_events/india_misc_events.txt:913-921` | state sauvegardé | hindou + sunnite, `medium_radicals` | aucun |
| `events/tanzimat_events.txt:868-876` | state sauvegardé | sunnite, `large_radicals`, puis religion dynamique | aucun |
| `events/agitators_events/dreyfus_events.txt:939-944,970-975,1015-1025` | state sauvegardé | religion catholique/juive; radicaux et loyalistes | aucun |
| `common/history/global/00_global.txt:1110-1133` | pays → random/every state | valeurs nommées + filtres strata/culture | aucun |
| `events/decree_events.txt:457-483` | `scope:decree_state` | loyalistes puis radicaux, `small_radicals`, laborers | aucun |
| `common/character_interactions/01_additional_interactions.txt:1261-1273` | owner → random state | `large_radicals` sans filtre | aucun |

Le fichier vanilla commenté `events/test_events.txt:4095-4167` documente aussi toutes les combinaisons de filtre, dont `religion = rel:catholic`, directement sous `capital`; il est retenu comme documentation de test, pas comme exemple runtime actif.

Pour `very_small_radicals`, les usages actifs recensés sont `events/iberia_events/spanish_events.txt:194-218,309-333` et `events/japan_events/ep2_hokkaido_events.txt:936-941`. Ils attestent la résolution de la valeur nommée, mais utilisent les variantes pays `add_radicals`/`add_loyalists` plutôt que `*_in_state`.

## 6. Sémantique attestée

- `very_small_radicals = 0.01`; `large_radicals = 0.1`.
- `localization/english/effects_l_english.yml:571-587` définit les filtres religion/culture/pop type/strata et décrit `add_radicals_in_state` comme la part filtrée qui devient « more radical » dans le state.
- Les variantes `add_radicals_in_state` et `add_loyalists_in_state` sont déclarées dans `common/effect_localization/00_pop_effects_loc.txt:61-69`.
- La syntaxe attend un state scope. Un owner ou un pop scope supplémentaire n’est pas requis par les exemples actifs.
- Les exemples exécutent l’effet directement dans une option ou un effet; aucun délai scripté n’est attesté.
- Le code statique n’atteste pas le moment de rafraîchissement du compteur UI ni la sérialisation interne avant le premier tick. Il serait donc abusif de conclure `UI_REFRESH_REQUIRED` sans un test après tick.

## 7. Format des sauvegardes

Les trois `.v3` commencent par 24 octets ASCII de forme `SAV0105…\n`; la signature ZIP `50 4B 03 04` commence à l’offset 24. L’archive contient `gamestate` et `meta`. `gamestate` est un binaire Jomini tokenisé, non du texte brut.

Méthode sûre employée : copies dans un dossier temporaire hors de `save games`, extraction locale avec `tar`, puis fonte des copies avec `rakaly` 0.8.18, commande `melt --format vic3 --unknown-key stringify`. Les trois fontes terminent avec exit code 0. Le décodeur provient de la [release officielle du projet rakaly/cli](https://github.com/rakaly/cli/releases/tag/v0.8.18); aucune sauvegarde originale n’a été ouverte en écriture, déplacée, recomprimée ou réenregistrée.

| Save | Taille `.v3` | SHA-256 original | Taille `gamestate` binaire | Taille fondue |
|---|---:|---|---:|---:|
| C1K pré-option | 7 901 193 | `19ED98D357672806DFF4B9204E2A1D2DCCC859AD99A468509E57F0B5FBC19BB9` | 80 126 018 | 106 979 064 |
| C1M pré-option | 7 899 432 | `771B4AB364ABED9BCF306ED070ECCCD6D973F561AB155FB2F166957469080CA4` | 80 116 984 | 106 964 760 |
| C1M post-option | 7 902 306 | `08845B6E7A572F0E8A71D8030A839DCBC562616022BB3C4B8B7B0F006B5776B9` | 80 141 430 | 106 999 028 |

## 8. Comparaison C1K/C1M pré-option

Les deux saves sont au `date=1776.1.1`, tick 0. Dans les deux : owner BIC 218 pour East Bengal 14 et West Bengal 487; owner COO 412 pour West Bengal 488; marqueur `zz_sepoy_test_b1_ready` présent sur BIC avec `tick=0`; mêmes nombres d’objets de pops et mêmes totaux workforce/dependents hindous et sunnites dans les trois region states bengalis.

Les blocs individuels de pops de deux nouvelles parties ne sont pas tous identiques (86 différences sur 124 objets ciblés, dues à d’autres champs sérialisés); on ne leur attribue donc aucune causalité. En revanche, la tendance BIC `trend_radicals` vaut explicitement 0 dans les deux et le bloc complet `pop_radicals_and_loyalists_statistics` est identique.

Le marqueur prouve que l’option de préparation a atteint le `set_variable` situé après les effets. Il ne prouve pas à lui seul que le moteur a muté une donnée radicale.

## 9. Comparaison C1M pré/post-option

Les deux saves restent au `date=1776.1.1`, tick 0. Les owners bengalis sont inchangés, conformément à la correction territoriale validée. Le marqueur est présent dans les deux.

Les 124 objets de pops hindoues/sunnites situés dans les states 14, 487 et 488 ont exactement le même SHA-256 objet par objet entre C1M pré et C1M post : 124 identiques, 0 différent, 0 ajouté, 0 retiré. Le sous-ensemble effectivement possédé par BIC représente 110 objets; il est donc lui aussi intégralement identique. Les totaux de population sont inchangés.

La tendance BIC `trend_radicals` vaut 0 dans les deux. Le bloc complet BIC `pop_radicals_and_loyalists_statistics` a dans C1K pré, C1M pré et C1M post le même SHA-256 fondu : `CF9A55D443C21CAD1E37F424685202C7B48F3458A60D76CE3B7651492D34CFFB`.

## 10. Preuve ou absence de changement radical

Preuve positive : aucune mutation radicale sérialisée identifiable n’existe entre C1K pré et C1M pré, ni entre C1M pré et C1M post. Les champs attestés restent à 0 et les blocs statistiques sont identiques. La comparaison C1M pré/post ajoute la preuve forte que les objets de pops ciblés sont inchangés.

Absence de preuve : les saves ne permettent pas de déterminer si l’effet a été ignoré au tick 0, mis en attente dans une donnée non sérialisée, ou soumis à une sémantique moteur non visible dans les champs identifiés. Comme les données sérialisées n’existent pas, ce n’est pas une simple preuve d’arrondi UI. Une baseline de 1 % sur plus de 38 millions de personnes BIC ciblées ne serait de toute façon pas raisonnablement masquée par un compteur national à zéro si elle avait été agrégée.

## 11. Cause racine

Classification unique : **`SAVE_EVIDENCE_INCONCLUSIVE`**.

Les catégories 1 et 2 ne sont pas soutenues : le scope state et les populations cibles existent. Les catégories 3 et 4 ne sont pas soutenues : syntaxe, valeurs et filtres sont attestés par la vanilla, y compris le code gameplay exact. Les catégories 5 et 6 ne peuvent pas être retenues : les données attendues ne figurent pas dans les saves, et aucun test après tick n’existe. La catégorie 7 n’est pas démontrée : la localisation décrit bien une part des pops devenant plus radicale. Les preuves établissent l’échec observé, pas son mécanisme causal.

## 12. Correction éventuelle

Aucune correction de gameplay ou de harnais n’est appliquée. Modifier l’API, remplacer les filtres ou injecter une autre baseline serait une conjecture interdite par la phase. La seule suite sûre est un retest discriminant avec une journée de stabilisation.

## 13. Diff logique

- Gameplay : aucun diff.
- Harnais B-1 : aucun diff.
- Localisations B-1 : aucun diff.
- Territoire Bengal : aucun diff.
- Livrables : création du présent rapport et du manifeste C1N uniquement.

## 14. Validation statique

- Accolades Sepoy : 968 ouvrantes, 968 fermantes.
- Accolades décision B-1 : 28/28; event B-1 : 18/18.
- Quatre fichiers B-1 : UTF-8 avec BOM, LF uniquement, zéro CR.
- Zéro effet territorial dans les deux scripts B-1.
- Correction Bengal inchangée : hash Sepoy attendu conservé dans fork et copie.
- Autres options Sepoy et journal inchangés; journal fork/copie : 16 040 octets, SHA-256 `DAEFCB59CCF6B303D2E39C948D8038006C1346AFE40A2B812D45EE4D947E361C`.
- Anciens harnais : toutes les empreintes contrôlées C1L demeurent conformes.
- Exactement un appel à `sepoy_mutiny_events.2` dans B-1.
- Aucun `default_option` ni choix automatique.
- Aucune mutation territoriale et aucune ligne Bengal modifiée.

## 15. Plan runtime condensé

1. Ouvrir Victoria 3 une seule fois avec la seule copie jetable B-1.
2. Démarrer une seule nouvelle partie BIC; aucune session GBR.
3. Au 1er janvier, relever uniquement le compteur national de radicaux et les mêmes vues détaillées hindoues/sunnites de West/East Bengal; contrôle rapide des owners BIC/COO.
4. Exécuter la préparation explicite B-1; relever immédiatement le compteur et confirmer l’absence de mutation territoriale.
5. Laisser passer exactement un jour, jusqu’au 2 janvier. Ce tick unique est justifié parce que toutes les preuves C1K/C1M actuelles sont au tick 0.
6. Relever les radicaux après stabilisation dans les mêmes vues. Si la baseline reste 0, arrêter le scénario destructif, sauvegarder ce constat et classer l’hypothèse du tick réfutée.
7. Si la baseline devient mesurable, créer la sauvegarde pré-option distincte.
8. Ouvrir une seule fois `sepoy_mutiny_events.2` via la décision B-1 et choisir manuellement uniquement 2.b.
9. Relever immédiatement les radicaux dans les mêmes vues; vérifier rapidement que les portions BIC de West/East Bengal restent BIC.
10. Créer la sauvegarde post-option distincte.
11. Fermer Victoria 3 une seule fois.
12. Après fermeture, analyser seulement les logs ciblés et les deux saves. Aucun redémarrage, aucune reprise complète du protocole territorial C1M.

Le test ne valide que la baseline, l’augmentation après 2.b et un contrôle territorial rapide. Il ne répète pas Bihar/Awadh/Bundelkhand/Circars/Pegu/COO/JEY sauf symptôme de régression.

## 16. Verdict

**`BLOCKED_B1_RADICAL_CAUSE_UNPROVEN`**

L’absence de changement est prouvée; la cause ne l’est pas. Aucun correctif local attesté ne peut être choisi sans nouveau runtime au-delà du tick 0.

## 17. Fichiers modifiés

Créés dans le fork uniquement :

- `docs/reports/hotfix/HOTFIX_5C2E4C1N_B1_RADICAL_FORENSIC_AUDIT.md`
- `docs/reports/hotfix/HOTFIX_5C2E4C1N_B1_RADICAL_AUDIT_MANIFEST.csv`

Aucun fichier de la copie jetable n’est modifié. Aucun fichier gameplay, journal, décision, event ou localisation n’est modifié.

## 18. Confirmation de la correction Bengal

La correction territoriale West/East Bengal n’a pas été remise en cause ni touchée. Fork et copie Sepoy restent identiques, 63 422 octets, SHA-256 `FFB4060E659FB8A30691E26BA5BBDA838650EF11AB1760C89EDACFA2310D9BBE`.

## 19. Confirmation des anciens harnais

Les seize anciens fichiers racine/A-1/A-2/A-3 et leurs contrôles C1L restent conformes en taille et SHA-256. Aucun ancien harnais n’a été ouvert en écriture.

## 20. Confirmation `docs/research/technology/`

Les sept fichiers non suivis préexistants sous `docs/research/technology/` restent la seule exception non suivie hors livrables C1N. Ils n’ont été ni lus pour cet audit, ni modifiés.

## 21. Confirmation stash MARATH

`stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` reste présent. Il n’a été ni appliqué, ni modifié, ni supprimé.
