# HOTFIX-6A.13F — Loi initiale Merchant Banking de GEN et VEN

Date : 30 juillet 2026

Phase : `HOTFIX_6A13F_GEN_VEN_MERCHANT_BANKING_STARTING_LAW`

Branche : `hotfix-dlc-audit`

HEAD initial et final : `415d7c7a11007d2ab98b086feca98eefa99779f4` —
`Select GEN and VEN Merchant Banking starting law`

## 1. État de la phase

L'implémentation statique et le runtime humain sont complets. Dans les objets
`c:GEN` et `c:VEN`, la loi économique initiale `law_traditionalism` a été
remplacée chirurgicalement par `law_merchant_banking`.

`law_merchant_navy`, les dix-sept autres lois actives, les technologies,
institutions, tarifs, modificateurs et toute la structure adjacente ont été
conservés. Codex n'a lancé ni piloté le jeu ou le launcher. L'opérateur humain
a validé successivement GEN et VEN pendant plusieurs jours de jeu, puis a
confirmé la fermeture du jeu. Les processus Victoria 3, `dowser` et Paradox
étaient absents avant l'analyse des nouveaux logs.

## 2. Préflight

| Contrôle | Résultat |
| --- | --- |
| Racine Git | fork exact |
| Branche | `hotfix-dlc-audit` |
| HEAD complet | `415d7c7a11007d2ab98b086feca98eefa99779f4` |
| Message du HEAD | `Select GEN and VEN Merchant Banking starting law` |
| Rapport 6A.13 dans `HEAD` | présent |
| Quatre verdicts d'entrée 6A.13 dans `HEAD` | présents |
| Fichiers suivis avant correction | propres |
| Index staged | vide |
| `git diff --check` initial | PASS |
| Processus Victoria 3, `dowser` ou Paradox | 0 |
| Stash protégé | présent, ligne exacte |
| Hash objet du stash avant correction | `518df704fa14599c0f254fae13859210663dd976` |

État Git initial exhaustif :

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

Le stash est resté fermé :

```txt
stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla
```

## 3. Sources lues

Les sources canoniques et contextuelles suivantes ont été lues intégralement :

- `docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`;
- `docs/reports/hotfix/_index/HOTFIX_6A13_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md`;
- `docs/reports/hotfix/_index/HOTFIX_6A12F_PORTUGUESE_COLONIALISM_STRATEGIC_REGION_KEYS_1_13_ALIGNMENT.md`;
- `docs/reports/hotfix/_index/HOTFIX_6A12_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md`;
- `docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md`;
- `docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv`;
- `docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv`;
- les `Changelog.txt` complets du fork et de la source hotfix;
- les versions fork et source de GEN et VEN;
- `common/laws/00_inject_laws.txt`;
- `localization/english/hotfix_laws_l_english.yml`;
- `localization/french/hotfix_laws_l_french.yml`;
- `gfx/interface/icons/law_icons/merchant_banks.dds`;
- les logs et rotations de référence publiés par 6A.12F.

Les deux CSV ont été parsés intégralement : `123 × 22` et `38 × 17`, sans
cellule structurelle nulle. Les hashes des logs et rotations lus correspondent
au snapshot 6A.12F. Aucun nouveau log n'a été créé ni analysé.

## 4. Objectif et justification

GEN et VEN sont des républiques maritimes en 1776. Le changelog de la source
hotfix annonce explicitement `Merchant Banking (Maritime Republics)`. La loi
est dans `lawgroup_economic_system` et sa visibilité est limitée par sa
définition à `c:GEN` ou `c:VEN`.

La correction aligne donc l'intention historique et fonctionnelle annoncée
avec les deux départs custom de 1776, sans absorber les différences adjacentes
de la source. En particulier, le retrait source de `law_merchant_navy` et son
ajout de `ideo_merchant_landowners` sont expressément exclus.

## 5. Comparaison trois voies

| Pays | Fork avant | Source hotfix | Vanilla 1.13 |
| --- | --- | --- | --- |
| GEN | `law_traditionalism` | `law_merchant_banking` | fichier absent |
| VEN | `law_traditionalism` | `law_merchant_banking` | fichier absent |

Hashes SHA-256 avant correction :

| Preuve | SHA-256 |
| --- | --- |
| GEN fork | `B4EC2FB8C9916425FBFFBAA1CEF7FEDFB63C2E0510352A4744E088748AFD80EF` |
| VEN fork | `33503E48A69A431AD10ABC2AD71AF9D2147CDA6F19C0CD6C0C04434C1E5425B1` |
| GEN source | `05A10969F0C7C378920E3224F83C1BC445486143F130874AAA19DE9592E98EAF` |
| VEN source | `8DDDA736260B18E2412DA1AD9516336938E19BA7266FD79992BD31E84013E5BA` |

Vanilla ne possède aucun des deux fichiers; cette absence est attendue.

## 6. Dépendances vérifiées

| Dépendance dans le fork | Résultat |
| --- | --- |
| Définition unique `law_merchant_banking` | PASS |
| Groupe `lawgroup_economic_system` | PASS |
| Visibilité `c:GEN` | une occurrence |
| Visibilité `c:VEN` | une occurrence |
| Référence à `merchant_banks.dds` | une occurrence |
| Icône DDS | présente, magic `DDS `, 427060 octets |
| SHA-256 de l'icône | `B420CA2FC6DC8D78321074C6F04E7D663944ABCFE4F13A68D5031962B91DA05A` |
| Localisation anglaise | `Merchant Banking` |
| Localisation française | `Banque marchande` |

Aucune dépendance n'a été modifiée.

## 7. Snapshot avant correction

Chaque fichier contenait exactement :

- un objet pays attendu (`c:GEN` ou `c:VEN`);
- une ligne active `law_traditionalism`;
- zéro ligne active `law_merchant_banking`;
- une ligne active `law_merchant_navy`;
- zéro occurrence de `ideo_merchant_landowners`.

Les deux listes de lois actives étaient identiques :

```txt
law_presidential_republic
law_merchant_republic
law_state_religion
law_land_based_taxation
law_hereditary_bureaucrats
law_right_of_assembly
law_national_supremacy
law_mercantilism
law_religious_schools
law_no_colonial_affairs
law_no_health_system
law_local_police
law_professional_army
law_merchant_navy
law_tenant_farmers
law_migration_controls
law_slavery_banned
law_traditionalism
```

GEN avait un BOM UTF-8, 51 LF, aucun CRLF, un saut final et un équilibre
d'accolades `6/6`. VEN avait un BOM UTF-8, 47 LF, aucun CRLF, un saut final et
un équilibre d'accolades `5/5`.

## 8. Méthode et diff exact

Deux hunks explicites ont été appliqués aux deux fichiers autorisés. Aucun
remplacement global et aucune copie complète depuis la source hotfix n'ont été
utilisés.

```diff
diff --git a/common/history/countries/gen - genoa.txt b/common/history/countries/gen - genoa.txt
@@ -27,7 +27,7 @@
         activate_law = law_type:law_tenant_farmers # enclosure acts
         activate_law = law_type:law_migration_controls
         activate_law = law_type:law_slavery_banned
-        activate_law = law_type:law_traditionalism
+        activate_law = law_type:law_merchant_banking

 #        set_institution_investment_level = {
 #            institution = institution_colonial_affairs
diff --git a/common/history/countries/ven - venetia.txt b/common/history/countries/ven - venetia.txt
@@ -27,7 +27,7 @@
         activate_law = law_type:law_tenant_farmers # enclosure acts
         activate_law = law_type:law_migration_controls
         activate_law = law_type:law_slavery_banned
-        activate_law = law_type:law_traditionalism
+        activate_law = law_type:law_merchant_banking

 #        set_institution_investment_level = {
 #            institution = institution_colonial_affairs
```

Forme du diff gameplay :

- deux fichiers;
- deux objets;
- deux hunks;
- deux additions;
- deux suppressions.

## 9. Hashes finaux et structure

| Fichier | SHA-256 final | Attendu |
| --- | --- | --- |
| GEN | `7FC780AB8A8793E1DD1B3E6A32022807CED720FB1BE3F3D63D9EC6FDE9F43327` | identique |
| VEN | `51A65341A2E3947A3D7D71BC3E3B1F31DA5CCD9D000D200C75BFB9570010B6DB` | identique |

Après correction, chaque objet contient exactement une
`law_merchant_banking`, zéro `law_traditionalism`, une `law_merchant_navy` et
zéro `ideo_merchant_landowners`. Le BOM UTF-8, les LF, le saut final,
l'indentation et l'équilibre des accolades sont inchangés.

La comparaison des listes de lois avant/après confirme que la seule
substitution est :

```txt
law_traditionalism -> law_merchant_banking
```

Toutes les autres lois initiales sont inchangées.

## 10. Protections

Les hashes protégés sont restés conformes au préflight :

| Élément | SHA-256 |
| --- | --- |
| Portugal final | `99DB30D8078C39930B82E79242D70CD70DB422BA148DB2D655E1A534E5DDF126` |
| Romania | `DEE084181C30A4DD72D85132F50EF725B654ACA70E22AA30E851FF7D743DE578` |
| Sick Man | `B04C07388C944E5DA74CFCE142599797F582EA809412B9690170735BFA17B04A` |
| Grande Crise orientale | `96F65E2B3CC7129DD8D4AD41382F9F8DD97FB5FA24C66C05F129B1E31615F75A` |
| BIC | `37B836DBE9A273F1202B592533EB8C851B3657DBB63422F50AE11021437F580C` |
| `bject` | `A6D3772BDFBFA8E9987DE8753D52079062AAC7F3277FEE22C338AA4AF2D6171B` |

Les sept recherches technologiques conservent respectivement :

```txt
315CB857B94D547492E1F7C36E10A67EF53DBCBDA0FF63CBA4246DBA7B6FC6D5
88D090A496C1C3CDB8A04D24AA2E31369E6AB6FAD843052CBE4C26467F4AA410
0FE06A1843F5B67413E222ECFDABBF4E6957EAA2E97D466A018C59FA27DA4596
01A37C0BD8BE839EC59E11AA4742CB4D96824EEAFCEA94979839391D8798094D
C4EF474D8C1502DBC1D36A9D52473EE4B5E41C3D14A2081F1A526B9383FF1AF5
6E7A48765FB9C20A4F8992D1CCD32BB75340A7BD6FC00B365E503F930BFD8F9A
150256D3C56333CAF8C37A7631074110060678FC115DB24FC48F702DFD6840FA
```

Le hash BIC conforme garantit la conservation de
`activate_law = law_type:law_frontier_colonization`; aucune
`law_colonial_exploitation` n'a été restaurée.

Aucun fichier NAVY, ADMIN, MARATH, technologique, institutionnel, tarifaire,
de modificateur, de localisation, d'événement, de journal entry, de
descripteur, de sauvegarde ou d'un autre pays n'a été modifié. La source
hotfix et vanilla ont été utilisées en lecture seule.

## 11. Validations statiques

| Contrôle | Résultat |
| --- | --- |
| Hash GEN final exact | PASS |
| Hash VEN final exact | PASS |
| Deux fichiers / deux objets / deux hunks / `2+/2-` | PASS |
| `law_merchant_banking` active dans GEN et VEN | PASS |
| `law_traditionalism` ciblée absente | PASS |
| `law_merchant_navy` conservée dans GEN et VEN | PASS |
| Autres lois initiales inchangées | PASS |
| `ideo_merchant_landowners` absent | PASS |
| Technologies, institutions, tarifs et modificateurs inchangés | PASS |
| BOM UTF-8, LF, saut final et accolades conservés | PASS |
| Dépendances inchangées | PASS |
| Protections inchangées | PASS |
| `git diff --check` | PASS |
| Index staged | vide |
| Commit automatique | aucun |
| Phase suivante | non sélectionnée |

Les avertissements Git éventuels sur une conversion LF/CRLF future proviennent
de la configuration du worktree; `git diff --check` sort avec succès et la
lecture binaire confirme que les deux fichiers restent actuellement en LF.

État Git final exhaustif :

```txt
 M "common/history/countries/gen - genoa.txt"
 M "common/history/countries/ven - venetia.txt"
 M docs/reports/hotfix/INDEX.md
 M docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv
 M docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md
 M docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv
?? bject
?? docs/reports/hotfix/_index/HOTFIX_6A13F_GEN_VEN_MERCHANT_BANKING_STARTING_LAW.md
?? docs/research/technology/TECH_TREE_BUILDING_AND_PRODUCTION_CANDIDATES.csv
?? docs/research/technology/TECH_TREE_INDUSTRIAL_CHAINS.md
?? docs/research/technology/TECH_TREE_INDUSTRIAL_HISTORY_DEEP_RESEARCH.md
?? docs/research/technology/TECH_TREE_INDUSTRIAL_INNOVATIONS_DATABASE.csv
?? docs/research/technology/TECH_TREE_RESEARCH_BIBLIOGRAPHY.md
?? docs/research/technology/TECH_TREE_RESOURCE_CANDIDATES.csv
?? docs/research/technology/TECH_TREE_VICTORIA3_GAP_ANALYSIS.md
```

État du stash avant et après :

```txt
stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla
avant : 518df704fa14599c0f254fae13859210663dd976
après : 518df704fa14599c0f254fae13859210663dd976
```

## 12. Fichiers écrits

Liste exhaustive :

1. `common/history/countries/gen - genoa.txt`;
2. `common/history/countries/ven - venetia.txt`;
3. `docs/reports/hotfix/_index/HOTFIX_6A13F_GEN_VEN_MERCHANT_BANKING_STARTING_LAW.md`;
4. `docs/reports/hotfix/INDEX.md`;
5. `docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv`;
6. `docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv`;
7. `docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md`.

Après validation runtime, les quatre index documentaires autorisés sont mis à
jour. Le prompt de phase suivante reste inchangé et aucune nouvelle phase
n'est sélectionnée.

## 13. Rollback exact

Si le runtime humain impose un rollback, remplacer uniquement dans `c:GEN` et
`c:VEN` :

```txt
law_merchant_banking -> law_traditionalism
```

Ne pas utiliser `git restore`, `git checkout`, `git reset` ni une copie
complète de fichier. Les hashes restaurés obligatoires sont :

```txt
GEN B4EC2FB8C9916425FBFFBAA1CEF7FEDFB63C2E0510352A4744E088748AFD80EF
VEN 33503E48A69A431AD10ABC2AD71AF9D2147CDA6F19C0CD6C0C04434C1E5425B1
```

## 14. Fiche de runtime humaine unique

Prérequis : monter le fork exact et `dlc014_ip3`; lancer manuellement une seule
fois le launcher et Victoria 3; ne pas utiliser la console.

### Test 1 — Gênes

1. Créer une nouvelle partie avec GEN au 1er janvier 1776.
2. Vérifier dans Politique/Législation que **Banque marchande** est la loi
   économique active.
3. Vérifier que **Marine marchande** reste la loi navale active.
4. Vérifier qu'aucune clé brute ou anomalie visible n'apparaît.
5. Avancer jusqu'au 2 janvier 1776.
6. Revenir normalement au menu principal sans fermer le jeu.

### Test 2 — Venise

1. Dans la même session, créer une nouvelle partie avec VEN au 1er janvier
   1776.
2. Vérifier que **Banque marchande** est la loi économique active.
3. Vérifier que **Marine marchande** reste la loi navale active.
4. Vérifier qu'aucune clé brute ou anomalie visible n'apparaît.
5. Avancer jusqu'au 2 janvier 1776.
6. Prendre des captures si possible.
7. Fermer normalement Victoria 3, puis le launcher Paradox.
8. Confirmer explicitement leur fermeture.

L'opérateur transmet ensuite les pays et dates testés, les deux lois observées,
les anomalies ou clés brutes éventuelles, les captures disponibles, la
confirmation de fermeture et les nouveaux logs. Aucun PASS runtime ne sera
prononcé sans ce compte rendu humain.

## 15. Verdicts statiques

```txt
HOTFIX_6A13F_GEN_VEN_MERCHANT_BANKING_STARTING_LAW_STATIC_PASS
GEN_VEN_MERCHANT_BANKING_TWO_FILE_TWO_HUNK_ALIGNMENT_COMPLETE
GEN_VEN_MERCHANT_NAVY_AND_OTHER_STARTING_LAWS_UNCHANGED
HOTFIX_6A13F_STATIC_IMPLEMENTATION_COMPLETE
GEN_MERCHANT_BANKING_STARTING_LAW_ALIGNED
VEN_MERCHANT_BANKING_STARTING_LAW_ALIGNED
GEN_MERCHANT_NAVY_PRESERVED
VEN_MERCHANT_NAVY_PRESERVED
NO_OTHER_STARTING_LAW_CHANGED
EXPECTED_FINAL_HASHES_CONFIRMED
PROTECTED_SCOPE_PRESERVED
STASH_NAVY_3C_3_INTACT
NO_AUTOMATIC_COMMIT
NO_NEXT_PHASE_SELECTED
RUNTIME_OPERATOR_ACTION_REQUIRED
```

## 16. Compte rendu runtime humain

L'opérateur a effectué les deux nouveaux départs demandés dans une même
ouverture du jeu :

| Contrôle | GEN | VEN |
| --- | --- | --- |
| Nouvelle partie 1776 | PASS | PASS |
| **Banque marchande** active | PASS | PASS |
| **Marine marchande** active | PASS | PASS |
| Plusieurs jours écoulés | PASS | PASS |
| Clé brute visible | aucune | aucune |
| Autre anomalie visible | aucune | aucune |

Deux captures ont été fournies. Elles montrent une interface française
correctement localisée, **Banque marchande** comme système économique actif et
**Marine marchande** dans la liste des lois actives. Aucun identifiant brut
`law_merchant_banking`, `law_merchant_navy` ou autre clé de localisation
n'apparaît.

Le compte rendu humain confirme que les deux pays sont restés jouables après
plusieurs jours. Le jeu a ensuite été fermé normalement. Le contrôle système
post-runtime trouve zéro processus Victoria 3, `dowser` ou Paradox.

## 17. Réserve d'équilibrage post-hotfix

L'opérateur considère que la puissance et la formulation de
**Banque marchande** paraissent trop modernes pour 1776. La capture montre
notamment des effets importants sur les chartes de compagnie, l'allocation de
construction privée, les dividendes gouvernementaux, l'avantage commercial et
les contributions au fonds d'investissement.

Cette réserve ne constitue pas un échec du portage : la loi se charge,
s'affiche, s'active et fonctionne sans erreur ciblée. Elle crée toutefois une
dette de design distincte :

`MERCHANT_BANKING_1776_BALANCE_REVIEW_POST_HOTFIX_BACKLOG`

Une future phase, après le hotfix et sur instruction humaine, devra comparer
les bonus aux autres systèmes économiques de 1776, distinguer les mécanismes
historiquement plausibles des effets financiers modernes et proposer un
rééquilibrage dédié. Aucun coefficient, trigger, texte ou effet de loi n'est
modifié pendant 6A.13F.

## 18. Nouveaux logs et rotations

Les logs n'ont été lus qu'après la confirmation humaine de fermeture :

| Log | SHA-256 | Octets |
| --- | --- | ---: |
| `debug.1.log` | `BB6FDDB3BF20710195F0C803725C7EB1A3F0832C11CBE7B4860C43295A8D6A04` | 199460 |
| `debug.log` | `5D0FFA36A251574C08D438531C3B0172D98981C326ABE03D06845DF344ABBEAA` | 438192 |
| `error.1.log` | `B7928FE377489E247B3672E8D0CDD667A3E8762D2FECBDC4629A29E0001A4EC2` | 524105 |
| `error.2.log` | `B7928FE377489E247B3672E8D0CDD667A3E8762D2FECBDC4629A29E0001A4EC2` | 524105 |
| `error.3.log` | `B7928FE377489E247B3672E8D0CDD667A3E8762D2FECBDC4629A29E0001A4EC2` | 524105 |
| `error.4.log` | `B7928FE377489E247B3672E8D0CDD667A3E8762D2FECBDC4629A29E0001A4EC2` | 524105 |
| `error.5.log` | `4C2CBD047376CBE0EC1A1E6A4799F09747E8149909F446E35ECCA025E2489F4D` | 524105 |
| `error.log` | `171F560BA3FFC388B7AEC39B188BFF96D880E84F0A1967166B7731D0C5C46B4F` | 274276 |
| `game.1.log` | `B7928FE377489E247B3672E8D0CDD667A3E8762D2FECBDC4629A29E0001A4EC2` | 524105 |
| `game.2.log` | `B7928FE377489E247B3672E8D0CDD667A3E8762D2FECBDC4629A29E0001A4EC2` | 524105 |
| `game.3.log` | `B7928FE377489E247B3672E8D0CDD667A3E8762D2FECBDC4629A29E0001A4EC2` | 524105 |
| `game.4.log` | `B7928FE377489E247B3672E8D0CDD667A3E8762D2FECBDC4629A29E0001A4EC2` | 524105 |
| `game.5.log` | `E665D458D0E289D4C5D40325229D5F447B39D1AAED773B4AF5537D6BA303D86B` | 524105 |
| `game.log` | `66EC46A1482BAC4363F1889D44E6EADE614E01846D12FC028164BC9F226653B5` | 373532 |
| `system.log` | `71823ABD049DB6D8A1C09FB89615A8D775119966133D8119419A98E90C131EAE` | 1100 |

`debug.1.log` confirme le montage de `dlc014_ip3` et du fork exact.

## 19. Diagnostics runtime

La recherche exhaustive dans les nouveaux logs et rotations donne zéro
occurrence ciblée pour :

- `law_merchant_banking`;
- `law_merchant_navy`;
- `gen - genoa.txt`;
- `ven - venetia.txt`;
- `hotfix_laws_l_english.yml` et `hotfix_laws_l_french.yml`;
- `merchant_banks.dds`;
- `ideo_merchant_landowners`.

La baseline legacy
`Unexpected token: should_be_pinned_by_default` reste exactement à 374
occurrences, comme avant 6A.13F. Les 36 autres tokens inattendus observés
concernent exclusivement des fichiers hors périmètre, notamment
`00_default_strategy.txt`, `00_landowners.txt`,
`07_poland_lithuania_mod.txt` et `15_russia.txt`. Aucun n'est attribué aux deux
histoires pays ou aux dépendances Merchant Banking.

## 20. Fichiers finaux de la phase

Après runtime, exactement les sept fichiers autorisés sont modifiés ou créés :

1. `common/history/countries/gen - genoa.txt`;
2. `common/history/countries/ven - venetia.txt`;
3. ce rapport;
4. `docs/reports/hotfix/INDEX.md`;
5. `docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv`;
6. `docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv`;
7. `docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md`.

`HOTFIX_NEXT_MERGE_PHASE_PROMPT.md` reste inchangé. Aucun commit automatique
n'est créé et aucune phase suivante n'est sélectionnée.

## 21. Verdicts finaux

```txt
HOTFIX_6A13F_GEN_VEN_MERCHANT_BANKING_STARTING_LAW_RUNTIME_PASS
GEN_VEN_MERCHANT_BANKING_1776_START_VALIDATED
GEN_VEN_MERCHANT_NAVY_PRESERVED
HOTFIX_6A13F_GEN_VEN_MERCHANT_BANKING_STARTING_LAW_COMPLETE
MERCHANT_BANKING_1776_BALANCE_REVIEW_POST_HOTFIX_BACKLOG
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
NO_AUTOMATIC_COMMIT
NO_NEXT_PHASE_SELECTED
```
