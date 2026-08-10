# HOTFIX-6A.12F — Alignement Victoria 3 1.13 des régions stratégiques du colonialisme portugais

Date : 30 juillet 2026

Phase : `HOTFIX_6A12F_PORTUGUESE_COLONIALISM_STRATEGIC_REGION_KEYS_1_13_ALIGNMENT`

Branche : `hotfix-dlc-audit`

HEAD initial et final : `0560bf8e74786755f11cdb61ee5a42ebdea26296` —
`Select Portuguese colonialism strategic region alignment`

## 1. État de la phase

Le correctif atomique est appliqué et validé statiquement et en runtime. Le
runtime a été exécuté par l'opérateur humain, jamais par Codex. Le Portugal a
atteint le 2 janvier 1776, l'entrée potentielle est lisible sans clé brute et
les diagnostics ciblés passent à zéro. Le jeu et le launcher étaient fermés
avant l'analyse des nouveaux logs.

## 2. Préflight

| Contrôle | Résultat |
| --- | --- |
| Racine Git | `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork` |
| Branche | `hotfix-dlc-audit` |
| Rapport 6A.12 dans `HEAD` | PASS |
| Cinq verdicts d'entrée 6A.12 dans `HEAD` | PASS |
| 6A.12 commitée manuellement | PASS, commit `0560bf8` |
| Fichiers suivis | propres |
| Index staged | vide |
| `git diff --check` | propre |
| Stash protégé | ligne unique exacte |
| Victoria 3, `dowser`, Paradox | aucun processus |

Le stash exact est :

```txt
stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla
```

État Git initial :

```txt
?? bject
?? docs/research/technology/TECH_TREE_BUILDING_AND_PRODUCTION_CANDIDATES.csv
?? docs/research/technology/TECH_TREE_INDUSTRIAL_CHAINS.md
?? docs/research/technology/TECH_TREE_INDUSTRIAL_HISTORY_DEEP_RESEARCH.md
?? docs/research/technology/TECH_TREE_INDUSTRIAL_INNOVATIONS_DATABASE.csv
?? docs/research/technology/TECH_TREE_RESEARCH_BIBLIOGRAPHY.md
?? docs/research/technology/TECH_TREE_RESOURCE_CANDIDATES.csv
?? docs/research/technology/TECH_TREE_VICTORIA3_GAP_ANALYSIS.md
```

Aucun autre non-suivi n'était présent. Aucune commande Git destructive, aucun
accès au contenu du stash, aucun commit et aucune interaction avec le jeu ou le
launcher n'ont été effectués.

## 3. Verdicts d'entrée

Les cinq verdicts exigés sont présents dans le rapport 6A.12 de `HEAD` :

- `HOTFIX_6A12_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE`;
- `PORTUGUESE_COLONIALISM_STRATEGIC_REGION_KEYS_SELECTED`;
- `NO_GAMEPLAY_CHANGED`;
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`;
- `NEXT_EXECUTION_PHASE = HOTFIX_6A12F_PORTUGUESE_COLONIALISM_STRATEGIC_REGION_KEYS_1_13_ALIGNMENT`.

## 4. Hashes trois voies

| Preuve | SHA-256 | État |
| --- | --- | --- |
| Fork avant correction | `DB0B4CDC27B670F419D52148E6E5DF0C1D77CEA81BD9FD52115CAD27F1CCDB20` | PASS |
| Source hotfix | `04CCCCF13E9D7B4EA1DBBB29F86861CA8B1DB7F77B635175A39D889B9234EE7A` | PASS |
| Vanilla Victoria 3 1.13 | `15834E8FE1DBA56ADD9D970F9CECDF8AD1FB45100585770A457DF96BDF65FDF4` | PASS |
| Fork attendu et obtenu après correction | `99DB30D8078C39930B82E79242D70CD70DB422BA148DB2D655E1A534E5DDF126` | PASS |

La différence globale de hash entre les trois versions n'a autorisé aucun
import adjacent.

## 5. Hashes protégés

| Élément | SHA-256 | État |
| --- | --- | --- |
| Romania fork | `DEE084181C30A4DD72D85132F50EF725B654ACA70E22AA30E851FF7D743DE578` | PASS |
| Sick Man fork | `B04C07388C944E5DA74CFCE142599797F582EA809412B9690170735BFA17B04A` | PASS |
| Grande Crise orientale fork | `96F65E2B3CC7129DD8D4AD41382F9F8DD97FB5FA24C66C05F129B1E31615F75A` | PASS |
| BIC fork | `37B836DBE9A273F1202B592533EB8C851B3657DBB63422F50AE11021437F580C` | PASS |
| `bject` | `A6D3772BDFBFA8E9987DE8753D52079062AAC7F3277FEE22C338AA4AF2D6171B` | PASS |
| `TECH_TREE_BUILDING_AND_PRODUCTION_CANDIDATES.csv` | `315CB857B94D547492E1F7C36E10A67EF53DBCBDA0FF63CBA4246DBA7B6FC6D5` | PASS |
| `TECH_TREE_INDUSTRIAL_CHAINS.md` | `88D090A496C1C3CDB8A04D24AA2E31369E6AB6FAD843052CBE4C26467F4AA410` | PASS |
| `TECH_TREE_INDUSTRIAL_HISTORY_DEEP_RESEARCH.md` | `0FE06A1843F5B67413E222ECFDABBF4E6957EAA2E97D466A018C59FA27DA4596` | PASS |
| `TECH_TREE_INDUSTRIAL_INNOVATIONS_DATABASE.csv` | `01A37C0BD8BE839EC59E11AA4742CB4D96824EEAFCEA94979839391D8798094D` | PASS |
| `TECH_TREE_RESEARCH_BIBLIOGRAPHY.md` | `C4EF474D8C1502DBC1D36A9D52473EE4B5E41C3D14A2081F1A526B9383FF1AF5` | PASS |
| `TECH_TREE_RESOURCE_CANDIDATES.csv` | `6E7A48765FB9C20A4F8992D1CCD32BB75340A7BD6FC00B365E503F930BFD8F9A` | PASS |
| `TECH_TREE_VICTORIA3_GAP_ANALYSIS.md` | `150256D3C56333CAF8C37A7631074110060678FC115DB24FC48F702DFD6840FA` | PASS |

BIC conserve exactement :

```txt
activate_law = law_type:law_frontier_colonization
```

`law_colonial_exploitation` n'a pas été restaurée.

## 6. Sources consultées

Les sources obligatoires ont été lues intégralement en lecture seule :

- `HOTFIX_6A12_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md`;
- `HOTFIX_6A11F_PORTUGUESE_COLONIALISM_TWO_JE_PINNING_1_13_ALIGNMENT.md`;
- `HOTFIX_6A11_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md`;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md`;
- `HOTFIX_MERGE_BLOCK_STATUS.csv`;
- `HOTFIX_REPORT_INDEX.csv`;
- les trois versions de
  `common/journal_entries/06_portuguese_colonialism.txt`;
- vanilla
  `common/strategic_regions/african_strategic_regions.txt`;
- les localisations anglaise et française de la chaîne du colonialisme
  portugais et des deux régions stratégiques;
- les logs 6A.11F `debug.1.log`, `debug.log`, `error.log`, `game.log`,
  `system.log` et les rotations `debug.2.log` à `debug.5.log`.

Les neuf hashes des logs correspondent exactement au snapshot publié en
6A.11F. La baseline historique lue avant ce correctif contient 186 occurrences
de diagnostic `region_congo`, 186 de `region_zanj` et 373 retours de scope `sr`
non défini. Ces logs n'ont pas été modifiés et ne constituent pas un runtime
6A.12F.

## 7. Comparaison trois voies

Le fork avant correction contenait :

```txt
sr:region_congo = {
	save_scope_as = congo_scope
}
sr:region_zanj = {
	save_scope_as = zanj_scope
}
```

La source hotfix et vanilla 1.13 convergent exactement sur :

```txt
sr:region_equatorial_africa = {
	save_scope_as = congo_scope
}
sr:region_east_africa = {
	save_scope_as = zanj_scope
}
```

Les noms de scopes sont identiques dans les trois voies. Les localisations
anglaise et française les consomment comme `sStrategicRegion` afin d'afficher
les noms des deux régions.

## 8. Preuve géographique

Vanilla définit dans
`common/strategic_regions/african_strategic_regions.txt` :

- `region_equatorial_africa`, avec notamment `STATE_BAS_CONGO`,
  `STATE_CONGO`, `STATE_NORTH_ANGOLA`, `STATE_EAST_ANGOLA` et
  `STATE_SOUTH_ANGOLA`;
- `region_east_africa`, avec notamment `STATE_MOCAMBIQUE`,
  `STATE_ZAMBEZIA` et `STATE_LOURENCO_MARQUES`.

La recherche exhaustive des clés racines dans les strategic regions vanilla
ne trouve ni `region_congo` ni `region_zanj`; seules les deux clés modernes
sont valides. Le fork et la source hotfix ne possèdent aucun répertoire
`common/strategic_regions` et héritent donc tous deux des définitions vanilla.

Le correctif n'exige aucun nouveau fichier de carte, aucune modification de
state region et aucun import de données de carte.

## 9. Snapshot avant correction

Le fichier initial avait un BOM UTF-8, uniquement des fins de ligne LF, un
saut final et 95 accolades ouvrantes pour 95 fermantes. Le bloc exact était :

```txt
	immediate = {
		sr:region_congo = {
			save_scope_as = congo_scope
		}
		sr:region_zanj = {
			save_scope_as = zanj_scope
		}
		trigger_event = portuguese_colonialism.1
	}
```

Comptages initiaux :

| Jeton | Occurrences |
| --- | ---: |
| `sr:region_congo` | 1 |
| `sr:region_zanj` | 1 |
| `sr:region_equatorial_africa` | 0 |
| `sr:region_east_africa` | 0 |
| `congo_scope` | 1 |
| `zanj_scope` | 1 |

## 10. Correction atomique

L'unique objet ciblé est `je_portuguese_colonialism`. Les deux substitutions
exactes sont :

```txt
sr:region_congo               -> sr:region_equatorial_africa
sr:region_zanj                -> sr:region_east_africa
```

Hunk unifié exact :

```diff
@@ -8,10 +8,10 @@
 	weight = 10000

 	immediate = {
-		sr:region_congo = {
+		sr:region_equatorial_africa = {
 			save_scope_as = congo_scope
 		}
-		sr:region_zanj = {
+		sr:region_east_africa = {
 			save_scope_as = zanj_scope
 		}
 		trigger_event = portuguese_colonialism.1
```

Le diff gameplay compte exactement un fichier, un objet, un hunk unifié, deux
additions et deux suppressions. Aucune ligne adjacente n'est modifiée.

## 11. Snapshot après correction

Le bloc ciblé est désormais :

```txt
	immediate = {
		sr:region_equatorial_africa = {
			save_scope_as = congo_scope
		}
		sr:region_east_africa = {
			save_scope_as = zanj_scope
		}
		trigger_event = portuguese_colonialism.1
	}
```

Comptages après correction :

| Jeton | Occurrences |
| --- | ---: |
| `sr:region_congo` | 0 |
| `sr:region_zanj` | 0 |
| `sr:region_equatorial_africa` | 1 |
| `sr:region_east_africa` | 1 |
| `congo_scope` | 1 |
| `zanj_scope` | 1 |

Le hash final est exactement :

`99DB30D8078C39930B82E79242D70CD70DB422BA148DB2D655E1A534E5DDF126`.

Le BOM UTF-8, les LF, le saut final et l'équilibre `95/95` des accolades sont
préservés.

## 12. Pinning et progression conservés

Les deux objets conservent chacun exactement :

```txt
should_be_pinned_by_default_uninvolved_or_context = yes
```

Le fichier contient donc toujours deux propriétés modernes et zéro occurrence
de l'ancienne propriété exacte :

```txt
should_be_pinned_by_default = yes
```

Les conditions de visibilité, progression, complétion, échec et invalidation,
ainsi que les événements de `je_the_pink_map`, sont inchangés.

## 13. Exclusions adjacentes

Le correctif n'importe ni ne modifie le filtre de culture portugaise,
`geographic_region_iberia_old`, la prise en charge de `c:IBE`, les événements
ou la progression de la Carte rose, les titres, raisons, tooltips,
localisations, scopes supplémentaires, rôles, poids, transferts ou DLC gates.

La répétition française « Royaume de Portugal » n'est pas corrigée. Merchant
Banking et Navigation Acts restent hors périmètre.

## 14. Protections

Aucun élément relatif aux blocs protégés DEI/VOC, Java, NAVY, MARATH, ADMIN,
Inde/BIC, Japon, Russie, Autriche, Balkans, révolutions, technologies,
descripteurs, launcher, sauvegardes, `bject`, Tanzimat, Sick Man, Grande Crise
orientale ou Romania n'a été modifié.

La source hotfix et vanilla sont restées strictement en lecture seule. Aucun
fichier de localisation ou de carte n'a été écrit.

## 15. Validations statiques

| Contrôle | Résultat |
| --- | --- |
| Hash cible | PASS |
| Anciennes clés absentes | PASS |
| Nouvelles clés présentes une fois chacune | PASS |
| `congo_scope` et `zanj_scope` inchangés | PASS |
| Un fichier gameplay | PASS |
| Un objet | PASS |
| Un hunk unifié | PASS |
| Deux additions et deux suppressions | PASS |
| Lignes adjacentes inchangées | PASS |
| Deux pinning modernes conservés | PASS |
| Ancien pinning absent | PASS |
| Accolades équilibrées | PASS, `95/95` |
| BOM, LF et saut final préservés | PASS |
| Source hotfix et vanilla inchangées | PASS |
| Romania, Sick Man, Grande Crise orientale inchangés | PASS |
| BIC et sa loi protégée intacts | PASS |
| `bject` intact | PASS |
| Sept recherches technologiques intactes | PASS |
| Stash NAVY-3C-3 intact | PASS |
| Processus Victoria 3, `dowser`, Paradox | zéro |
| `git diff --check` | propre |
| Index staged | vide |

## 16. Rollback exact

Le rollback autorisé remplace uniquement, dans
`je_portuguese_colonialism` :

```txt
sr:region_equatorial_africa -> sr:region_congo
sr:region_east_africa       -> sr:region_zanj
```

Il conserve `congo_scope` et `zanj_scope`. Une simulation byte pour byte en
mémoire depuis le fichier corrigé restaure exactement :

`DB0B4CDC27B670F419D52148E6E5DF0C1D77CEA81BD9FD52115CAD27F1CCDB20`.

Le rollback n'a pas été nécessaire et n'a pas été appliqué.

## 17. Fichiers écrits et état Git au handoff

Les seuls fichiers écrits par la phase avant runtime sont :

1. `common/journal_entries/06_portuguese_colonialism.txt`;
2. ce rapport
   `HOTFIX_6A12F_PORTUGUESE_COLONIALISM_STRATEGIC_REGION_KEYS_1_13_ALIGNMENT.md`.

Les quatre documents de navigation et
`HOTFIX_NEXT_MERGE_PHASE_PROMPT.md` sont inchangés. Les huit non-suivis
protégés restent présents et intacts. L'index staged reste vide et aucun commit
automatique n'est créé.

## 18. Fiche runtime humaine unique

L'opérateur humain doit effectuer un seul lancement :

1. lancer le launcher Paradox;
2. confirmer le montage de `1776_Age_of_Revolutions_fork` et `dlc014_ip3`;
3. lancer Victoria 3;
4. commencer une nouvelle partie avec le Portugal au 1er janvier 1776;
5. confirmer que l'écran de jeu est atteint;
6. ouvrir `Journal → Potentiel → Além-mar africain`;
7. vérifier l'entrée visible, le titre, les conditions et raisons lisibles;
8. vérifier les références géographiques cohérentes avec l'Angola et le
   Mozambique;
9. vérifier l'absence de clé brute, d'erreur visible de scope, d'anomalie de
   pinning, de visibilité ou de progression;
10. confirmer qu'aucune modification inattendue de la Carte rose n'est
    visible;
11. noter la date initiale, avancer au 2 janvier 1776 et noter la date finale;
12. prendre une capture si possible;
13. fermer normalement Victoria 3 puis le launcher;
14. confirmer explicitement que les deux sont fermés.

Ne pas utiliser la console et ne pas forcer l'activation d'une entrée
indisponible.

Compte rendu demandé :

- pays joué;
- date initiale et date finale;
- écran de jeu atteint;
- journal potentiel accessible;
- `Além-mar africain` visible;
- titre, conditions et raisons lisibles;
- mentions de l'Angola et du Mozambique correctes;
- éventuelle clé brute;
- anomalies éventuelles de scope, pinning, visibilité ou progression;
- comportement visible de la Carte rose;
- capture éventuelle;
- confirmation explicite de fermeture de Victoria 3 et du launcher.

Codex ne doit analyser aucun nouveau log avant cette confirmation explicite.

## 19. Verdicts statiques

- `HOTFIX_6A12F_PORTUGUESE_COLONIALISM_STRATEGIC_REGION_KEYS_1_13_STATIC_PASS`
- `PORTUGUESE_COLONIALISM_STRATEGIC_REGION_KEYS_ONE_HUNK_1_13_ALIGNMENT_COMPLETE`
- `PORTUGUESE_COLONIALISM_SCOPE_NAMES_PINNING_AND_PROGRESSION_UNCHANGED`
- `RUNTIME_OPERATOR_ACTION_REQUIRED`

## 20. Compte rendu runtime humain

L'opérateur a effectué le lancement unique demandé et a fourni une capture.

| Observation | Résultat |
| --- | --- |
| Pays joué | Portugal |
| Date initiale | 1er janvier 1776 |
| Date finale | 2 janvier 1776 |
| Écran de jeu atteint | oui |
| `Journal → Potentiel` accessible | oui |
| `Além-mar africain` visible | oui |
| Titre lisible | oui |
| Conditions et raisons visibles | oui |
| Angola affiché correctement | oui |
| Mozambique affiché correctement | oui |
| Clé brute | aucune, confirmation humaine |
| Anomalie visible de scope | aucune |
| Anomalie visible de pinning | aucune |
| Anomalie de visibilité | aucune |
| Anomalie de progression | aucune pendant le passage au 2 janvier |
| Carte rose | aucune modification inattendue visible |
| Capture | fournie dans le compte rendu humain |
| Victoria 3 fermé | confirmation humaine et processus absent |
| Launcher Paradox fermé | processus `dowser`/Paradox absent |

La capture montre le drapeau portugais, l'entrée `Além-mar africain` dans
l'onglet Potentiel et les conditions localisées « région Angola » et « région
Mozambique ». Elle ne montre aucune clé de région stratégique brute.

La répétition « Royaume de Portugal » reste visible dans une condition et dans
une autre entrée du journal. Elle correspond exactement à la dette française
liée au nom dynamique et aux triggers génériques, documentée et exclue avant
correction. Elle n'est ni causée ni modifiée par le hunk de régions
stratégiques.

Après le compte rendu, un contrôle système a trouvé zéro processus Victoria 3,
`dowser` ou Paradox. Codex n'a jamais lancé ni piloté le jeu ou le launcher.

## 21. Logs avant runtime

Le snapshot 6A.11F antérieur au lancement était :

| Log | SHA-256 |
| --- | --- |
| `debug.1.log` | `1F25D03EAE1B45C68A84BE77CC36F8D8F8CCD9F540104CA5D7CE52B1F1C3194B` |
| `debug.log` | `31E79BBDA56B49BA16E2F07800D39CB7C579B622FA68E5BB92C67976265B1298` |
| `error.log` | `1D761021E38CC35578BB273E1DD82E7665D6EE8011F2D25370592FA808D311C8` |
| `game.log` | `04C9BC554C4A34D045291D5CD830BBE8D606923AE03F4F71E002202B28550C99` |
| `system.log` | `CA73FC2FC88D7E720083742B3C673812614065C90C58A808DDB0EDB78D2CF34E` |
| `debug.2.log` | `72E998A9E079984DB6D93B24F1CD4E6B13F2755FF2640E81BA660A01DE417899` |
| `debug.3.log` | `A75AD954D9AA33D27B11BFDBB75A804F319555610F75266604E0565C4D5004E8` |
| `debug.4.log` | `38B2B29FAD0922C6192B27CB69BC202F0C431F1DC9FDF5427C3835EBFDD75C35` |
| `debug.5.log` | `78068296741B912AFC46A4E763ED393F35F7D00967E4F17EB98075BC8EB177F5` |

## 22. Nouveaux logs et rotations

La nouvelle session est répartie entre `debug.1.log` et `debug.log`. Les
rotations `error.1.log` à `error.5.log` et `game.1.log` à `game.5.log` ont été
créées pendant ce même runtime et sont donc incluses dans l'analyse.

| Nouveau log ou rotation | SHA-256 | Octets |
| --- | --- | ---: |
| `debug.1.log` | `A32A481753B631F757BC5A1A653DF34AC8F87261A91FE116A31F1C32E94757FD` | 305819 |
| `debug.log` | `CC6C1C8E19DD564DBDA8FAC7BC9357338CB60F4E91441C71DE6FF57D15342C15` | 324759 |
| `error.1.log` | `038F12DE851088F4914D5E4DDA29C16301240CAC435749221E61EF6CFF64486A` | 524105 |
| `error.2.log` | `038F12DE851088F4914D5E4DDA29C16301240CAC435749221E61EF6CFF64486A` | 524105 |
| `error.3.log` | `038F12DE851088F4914D5E4DDA29C16301240CAC435749221E61EF6CFF64486A` | 524105 |
| `error.4.log` | `907058C33B0819B5E6DCD08FE176CC904E611460A08684E13B3B6BDF59FF8773` | 524105 |
| `error.5.log` | `19350807BD321783BB3E6FB2041044686CE03C325485EB06253AC8524203BB9F` | 524105 |
| `error.log` | `B59CAC5F9347290AB7D3EEC8C7DC8D62D78C43C6A48F97663F46F2664BDEAC60` | 309426 |
| `game.1.log` | `038F12DE851088F4914D5E4DDA29C16301240CAC435749221E61EF6CFF64486A` | 524105 |
| `game.2.log` | `038F12DE851088F4914D5E4DDA29C16301240CAC435749221E61EF6CFF64486A` | 524105 |
| `game.3.log` | `038F12DE851088F4914D5E4DDA29C16301240CAC435749221E61EF6CFF64486A` | 524105 |
| `game.4.log` | `95916791E6D3DC6E2227012B77FF7D9614F2251744FC2363D17305CE5001C612` | 524105 |
| `game.5.log` | `19350807BD321783BB3E6FB2041044686CE03C325485EB06253AC8524203BB9F` | 524105 |
| `game.log` | `D649F3E990F72FD273F2269E536AB46FF0E297DCE811A8C462FE39DEB10A816F` | 216186 |
| `system.log` | `06EB548ED07E5F4FFB497897FAF62D3B7948F91B5A1774E3C6F74F942EE32867` | 1100 |

Les rotations historiques sont séparées des nouveaux résultats :

| Rotation historique après décalage | SHA-256 | Identité antérieure |
| --- | --- | --- |
| `debug.2.log` | `31E79BBDA56B49BA16E2F07800D39CB7C579B622FA68E5BB92C67976265B1298` | ancien `debug.log` 6A.11F |
| `debug.3.log` | `1F25D03EAE1B45C68A84BE77CC36F8D8F8CCD9F540104CA5D7CE52B1F1C3194B` | ancien `debug.1.log` 6A.11F |
| `debug.4.log` | `72E998A9E079984DB6D93B24F1CD4E6B13F2755FF2640E81BA660A01DE417899` | ancien `debug.2.log` |
| `debug.5.log` | `A75AD954D9AA33D27B11BFDBB75A804F319555610F75266604E0565C4D5004E8` | ancien `debug.3.log` |
| `system.1.log` | `CA73FC2FC88D7E720083742B3C673812614065C90C58A808DDB0EDB78D2CF34E` | ancien `system.log` 6A.11F |

Ces rotations historiques ne sont jamais additionnées aux résultats de la
nouvelle session.

## 23. Montage et progression

`debug.1.log` prouve :

- ligne 80 : montage de
  `C:/Games/Victoria 3 The Great Wave/game/dlc/dlc014_ip3`;
- ligne 87 : montage du fork exact
  `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork`.

Le compte rendu humain constitue la preuve de la progression du 1er au
2 janvier 1776. Aucun log n'est substitué à cette observation humaine.

## 24. Diagnostics runtime

Les nouveaux `debug.1.log`, `debug.log`, `error.log` et leurs rotations de la
session ont été lus après fermeture du jeu et du launcher.

| Mesure ciblée | Avant | Après | Verdict |
| --- | ---: | ---: | --- |
| Clé stratégique invalide `region_congo` dans le fichier portugais | 186 | 0 | PASS |
| Clé stratégique invalide `region_zanj` dans le fichier portugais | 186 | 0 | PASS |
| Scope `sr` non défini associé | 373 | 0 | PASS |
| Nouveau diagnostic dans `06_portuguese_colonialism.txt` | — | 0 | PASS |
| Diagnostics legacy de pinning | 374/140 | 374/140 | inchangé |
| Diagnostics legacy de pinning dans le fichier cible | 0 | 0 | PASS |
| Rejet des propriétés modernes de pinning | 0 | 0 | PASS |

La baseline de pinning ne diminue pas, conformément au périmètre : les deux
propriétés avaient déjà été corrigées en 6A.11F.

Deux lignes nouvelles contiennent encore les chaînes `region_congo` et
`region_zanj`, mais uniquement comme tokens invalides dans
`common/ai_strategies/00_default_strategy.txt`, lignes gameplay 4601 et 4629.
Ces clés d'AI strategy ne proviennent pas du fichier portugais, ne sont pas des
objets `sr:` et sont classées hors périmètre. Elles ne changent pas le résultat
ciblé `186 → 0` pour chacune des deux anciennes strategic regions.

Les quatre références Tanzimat connues produisent huit lignes de diagnostic
dans la nouvelle session : `tanzimat_events.10` dans l'on-action globale,
puis `.5`, `.10` et `.9` dans `00_sick_man.txt`. Elles restent séparées,
inchangées et ne sont pas corrigées.

## 25. Fichiers finaux de la phase

Après runtime, exactement les six fichiers autorisés sont créés ou modifiés :

1. `common/journal_entries/06_portuguese_colonialism.txt`;
2. ce rapport;
3. `docs/reports/hotfix/INDEX.md`;
4. `docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv`;
5. `docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv`;
6. `docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md`.

`HOTFIX_NEXT_MERGE_PHASE_PROMPT.md` reste strictement inchangé. Aucune phase
suivante n'est commencée.

## 26. Contrôles finaux et décision de commit

Le hash gameplay reste
`99DB30D8078C39930B82E79242D70CD70DB422BA148DB2D655E1A534E5DDF126`.
Le diff gameplay reste un fichier, un objet, un hunk, deux additions et deux
suppressions. Les anciennes clés sont absentes du fichier, les nouvelles sont
présentes une fois chacune, les scopes et les pinning modernes sont inchangés.

La source hotfix, vanilla, Romania, Sick Man, Grande Crise orientale, BIC,
`bject`, les sept recherches technologiques et le stash NAVY-3C-3 restent aux
hashes protégés. Les CSV sont valides, `git diff --check` est propre, l'index
staged est vide et aucun processus Victoria 3, `dowser` ou Paradox n'est actif.

Aucun commit automatique n'est créé. La décision de commit appartient à
l'opérateur humain.

## 27. Verdicts finaux

- `HOTFIX_6A12F_PORTUGUESE_COLONIALISM_STRATEGIC_REGION_KEYS_1_13_RUNTIME_PASS`
- `PORTUGUESE_COLONIALISM_INVALID_STRATEGIC_REGION_DIAGNOSTICS_REMOVED`
- `PORTUGUESE_COLONIALISM_1776_VISIBILITY_GEOGRAPHY_AND_PROGRESSION_VALIDATED`
- `HOTFIX_6A12F_PORTUGUESE_COLONIALISM_STRATEGIC_REGION_KEYS_1_13_ALIGNMENT_COMPLETE`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`
