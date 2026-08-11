# CLEANUP-1A — Maratha Konkan Flotilla Stash Forensic Audit

Audit Git et code strictement en lecture seule du stash historique `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`. Aucun hunk du stash n'a été appliqué et aucun choix d'équilibrage naval définitif n'est arrêté ici.

## 1. Baseline

| Élément | Valeur observée |
| --- | --- |
| Branche actuelle | `cleanup-post-release` |
| Branche de nettoyage attendue | `cleanup-post-release` |
| `EXPECTED_CLEANUP_BRANCH_ACTIVE` | `YES` |
| HEAD actuel | `1e374f2f40252d229bc249600e3cbbe26085122d` — `Fix GitHub language statistics` |
| Stash demandé | `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` |
| Hash observé de `stash@{0}` | `518df704fa14599c0f254fae13859210663dd976` |
| Hash protégé attendu | `518df704fa14599c0f254fae13859210663dd976` |
| Vérification d'identité | Correspondance exacte |

Le statut initial contenait exactement les sept fichiers de recherche technologique protégés, tous non suivis. Aucun fichier suivi n'était modifié ou staged. Le fichier accidentel `bject` était absent. La liste complète des stashes ne contenait que le stash audité.

`STASH_IDENTITY_MISMATCH = NO`

`STASH_IDENTITY_VERIFIED = YES`

## 2. Stash topology

L'objet stash est un commit de fusion à trois parents créé le 10 juillet 2026 à 23:01:33 +02:00.

| Rôle | Commit | Interprétation |
| --- | --- | --- |
| Stash commit | `518df704fa14599c0f254fae13859210663dd976` | Snapshot du working tree, message `On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` |
| P1 — base/HEAD d'origine | `319df220005f01b23478405697bf0f4ce22e9e8e` | Baseline sur laquelle le stash a été créé |
| P2 — index | `3a2c8d60da770f5f0d5e2a922e98ae57092e5955` | Snapshot de l'index ; son arbre ne diffère pas de P1 |
| P3 — untracked | `f6d137ada2e504763ba4b93e3f359ac7a5d96b9b` | Commit racine contenant les trois fichiers non suivis sauvegardés |

### Métadonnées de P1

- SHA : `319df220005f01b23478405697bf0f4ce22e9e8e`
- date auteur et commit : `2026-07-10T22:25:25+02:00`
- sujet : `Set BIC to frontier colonization`
- parent : `2dedf0bc42cc7946f898901df5c7f1d204acf231`
- contexte : commit présent sur l'ancienne branche `hotfix-dlc-audit`, sur `phase1-map-compatibility` et dans l'ascendance des branches actuelles ; il porte les tags `pre-hotfix-dlc-audit-20260710-2245` et `pre-hotfix-dlc-audit-20260710-2301`.
- contexte naval immédiatement antérieur : `Fix Omani naval setup`, `Audit Indian naval setup`, `Fix Travancore coastal flotilla`, puis `Document BIC naval decision`.

La base est donc identifiée sans ambiguïté. P2 confirme qu'aucune modification du WIP n'était staged. P3 confirme que le stash a été créé avec sauvegarde des fichiers untracked.

## 3. Exact file inventory

### Inventaire exhaustif

| Chemin | Statut | Partie du stash | Lignes + / - | Fonction probable |
| --- | --- | --- | ---: | --- |
| `common/history/buildings/10_india.txt` | `M` | Working tree uniquement | `+11 / -0` | Historique des bâtiments initiaux par state et propriétaire en Inde ; ajoute le support d'équipage naval MARATH à Bombay. |
| `common/history/military_formations/05_military_formations_india.txt` | `M` | Working tree uniquement | `+12 / -0` | Ordre de bataille initial indien ; ajoute une formation navale MARATH. |
| `docs/reports/navy/PHASE_NAVY_3C_3_MARATHA_KONKAN_FLOTILLA.md` | `A` | P3 untracked | `+187 / -0` | Rapport WIP détaillant intention, justification, restrictions et tests runtime envisagés. |
| `localization/english/phase_navy_3c_maratha_fleet_l_english.yml` | `A` | P3 untracked | `+2 / -0` | Localisation anglaise de `Konkan_Flotilla`. |
| `localization/french/phase_navy_3c_maratha_fleet_l_french.yml` | `A` | P3 untracked | `+2 / -0` | Localisation française de `Konkan_Flotilla`. |

### Séparation working tree / index / untracked

- Working tree du stash, comparaison P1 → stash commit : deux fichiers suivis modifiés, `+23 / -0` au total.
- Index du stash, comparaison P1 → P2 : aucun fichier, aucun hunk, arbre identique à la base.
- Différence P2 → stash commit : les mêmes deux modifications du working tree, confirmant qu'elles n'étaient pas staged.
- Parent untracked P3 : trois nouveaux fichiers, `+191 / -0` au total.
- Aucun fichier supprimé, renommé ou copié.
- Aucun autre fichier ne figure dans les arbres du stash ; en particulier aucun fichier BIC, technologie, personnage, événement, journal entry, define, state history ou population n'est touché.

## 4. Reconstructed NAVY-3C-3 intent

1. **Pays concerné** : `c:MARATH`, c'est-à-dire l'Empire/Confédération marathe du fork.
2. **Formation** : création d'une seule formation de type `fleet`, identifiant interne `Konkan_Flotilla`.
3. **HQ / strategic region** : `hq_region = sr:region_south_india`.
4. **Type de navire** : un bloc `ship` de type `ship_type:ship_type_frigate`; aucun `ship_type_ship_of_the_line`.
5. **Nombre prévu** : `count = 1`, donc une unité navale symbolique.
6. **Nombre de flottes** : une seule flottille ; aucune seconde escadre.
7. **Éléments secondaires** :
   - ajout d'un `building_naval_administration` niveau 1 dans `STATE_BOMBAY` / `region_state:MARATH` ;
   - PM `pm_simple_sailor_recruitment` et `reserves = 1` ;
   - localisation anglaise `Konkan Flotilla` et française `Flottille du Konkan` ;
   - rapport documentaire de 187 lignes ;
   - aucune technologie, loi, pop, ownership territoriale, frontière, commandeur/amiral, événement, localisation autre, journal entry ou define modifié.
8. **État d'achèvement** : l'implémentation statique était petite et cohérente, et le rapport était substantiel. Elle restait néanmoins manifestement WIP : message de stash explicite, absence de commit, absence de validation runtime et section entière « Tests à faire en jeu ».
9. **TODO/WIP** : aucun jeton `TODO`, `FIXME` ou `WIP` n'apparaît dans les cinq blobs de contenu. Le caractère WIP est porté par le message du stash et par les tests encore à effectuer dans le rapport.
10. **Références devenues obsolètes** : le champ `state_region = s:STATE_BOMBAY` à l'intérieur du bloc `ship` ne correspond plus au format naval actuel 1.13. Le reste des principaux IDs navals employés existe encore.

L'intention historique documentée était une survivance côtière minimale du Konkan, abstraite en une seule frégate gameplay, sans amiral et sans flotte de ligne. CLEANUP-1A conserve cette intention comme donnée du WIP mais ne valide ni le type de navire, ni le compte, ni le besoin final d'administration navale.

## 5. Current HEAD divergence

| Chemin | P1 → HEAD | Classification | Changements concurrents pertinents |
| --- | --- | --- | --- |
| `common/history/buildings/10_india.txt` | Même blob `796d3ccf600f3d63e8ec87cd9c5ab751f06034a0` | `UNCHANGED_SINCE_STASH` | Aucun ; le bloc MARATH/Bombay est identique à P1 et ne contient toujours pas d'administration navale. |
| `common/history/military_formations/05_military_formations_india.txt` | `+24 / -25`, blob actuel `2b2944fda93a953a71b3ce799c5762f093b68bed` | `MODIFIED_SINCE_STASH` | Portage 1.13 et QA runtime : nouveaux IDs de strategic regions, retrait de `state_region` du navire de Travancore, puis corrections HQ BHV/SIN. Le HQ terrestre MARATH est passé de `region_central_india` à `region_north_india`. |
| `docs/reports/navy/PHASE_NAVY_3C_3_MARATHA_KONKAN_FLOTILLA.md` | Absent à P1 et à HEAD | `UNCHANGED_SINCE_STASH` (chemin toujours absent) | Aucun fichier homonyme ou remplacement exact. Plusieurs rapports rappellent seulement que le stash est protégé. |
| `localization/english/phase_navy_3c_maratha_fleet_l_english.yml` | Absent à P1 et à HEAD | `UNCHANGED_SINCE_STASH` (chemin toujours absent) | Aucun `Konkan_Flotilla` ni texte équivalent dans HEAD. |
| `localization/french/phase_navy_3c_maratha_fleet_l_french.yml` | Absent à P1 et à HEAD | `UNCHANGED_SINCE_STASH` (chemin toujours absent) | Aucun `Konkan_Flotilla` ni texte équivalent dans HEAD. |

Deux commits expliquent toute la divergence du fichier des formations :

- `c6c9429f4f11f28fac744702fc8dc58aeb790563` — `Update military formations for Victoria 3 1.13` ;
- `3b02b2af453707a3755a9553a306ebbdbbadbe1e` — `Correct military formation HQ regions after runtime QA`.

Un contrôle non mutatif du patch P1 → stash avec `git apply --check` réussit séparément pour les deux fichiers suivis. Un apply textuel pourrait donc ne produire aucun marqueur de conflit. Cette propreté textuelle est trompeuse : elle ne protège pas contre la réintroduction du `state_region` naval obsolète ni contre une décision d'équipage non recalibrée.

Aucun chemin n'est renommé, déplacé, supprimé ou réécrit massivement. La divergence est ciblée, mais elle touche précisément les conventions de formation militaire pertinentes pour ce WIP.

## 6. Victoria 3 1.13 compatibility findings

Contrôles effectués uniquement contre HEAD et le vanilla local `C:\Games\Victoria 3 The Great Wave\game` :

| Élément du stash | Résultat 1.13 | Conclusion |
| --- | --- | --- |
| `create_military_formation = { type = fleet ... }` | Forme encore utilisée dans le vanilla et le fork | Valide |
| Bloc naval `ship = { ... }` | 81 blocs inline dans le vanilla et 81 dans le fork | Valide |
| `type = ship_type:ship_type_frigate` | `ship_type_frigate` défini dans `common/ship_types/00_ship_types.txt` | Valide |
| `ship_type_ship_of_the_line` | ID encore défini, mais le stash n'en ajoute aucun | Valide, non utilisé |
| `state_region = s:STATE_BOMBAY` dans `ship` | Zéro occurrence dans les blocs `ship` vanilla 1.13 et zéro dans le fork actuel ; le portage du 28 juillet a supprimé ce champ du navire Travancore | Obsolète à supprimer |
| `sr:region_south_india` | Strategic region vanilla existante | Valide |
| Rattachement géographique de Bombay | `STATE_BOMBAY` figure explicitement parmi les states de `region_south_india` | Valide |
| `STATE_BOMBAY` | State region vanilla existante, côtière, avec `naval_exit_id` | Valide |
| `building_naval_administration` | Bâtiment vanilla existant, `recruits_sailors = yes` | ID valide |
| `pm_simple_sailor_recruitment` | PM vanilla existante, capacité de 1 000 marins par niveau | ID valide |
| Prérequis de l'administration navale | Le bâtiment est déverrouillé par `admiralty`. MARATH reçoit le palier technologique 5, qui inclut `navigation` mais pas `admiralty`, et ne l'ajoute pas explicitement | Risque de cohérence technologique à traiter, sans ajouter automatiquement une technologie |
| Clé `Konkan_Flotilla` et fichiers de localisation | Forme de clé cohérente avec les localisations du mod ; le rapport WIP déclare les blobs en UTF-8 BOM | Statiquement réutilisable, à ajouter seulement avec la formation finale |
| Structure `common/history/buildings` | Le hunk suit la structure actuelle `STATES` / `region_state` / `create_building` | Valide |

Le stash avait déjà effectué la conversion essentielle de l'ancien système naval vers `ship` et `ship_type:ship_type_frigate`. Il ne contient ni ancien `naval combat_unit`, ni `combat_unit_type_frigate`, ni `combat_unit_type_man_o_war`, ni `building_naval_base`. Son incompatibilité principale est plus subtile : le champ de state conservé dans le sous-bloc `ship`.

Le HQ naval `region_south_india` ne doit pas être confondu avec le HQ **terrestre** MARATH désormais `region_north_india`. La récupération ne doit jamais rétablir l'ancien HQ terrestre `region_central_india`.

## 7. Duplicate / obsolete / reusable work

Aucune partie fonctionnelle du WIP n'a été reproduite dans HEAD : il n'existe ni flotte MARATH, ni `Konkan_Flotilla`, ni localisations correspondantes, ni administration navale MARATH à Bombay. Les références actuelles au stash dans les rapports hotfix sont seulement des attestations de protection, pas une réimplémentation.

| Élément | Décision | Motif |
| --- | --- | --- |
| Concept d'une présence navale côtière MARATH/Konkan | `KEEP` | Travail non dupliqué et intention encore exploitable. |
| Identifiant `Konkan_Flotilla` | `KEEP` | Lisible, localisable et non dupliqué. |
| Localisations EN/FR | `KEEP` | Contenu réutilisable si la formation est retenue. |
| `type = fleet` et bloc `ship` | `KEEP` | Syntaxe 1.13 correcte. |
| `hq_region = sr:region_south_india` | `KEEP` | ID valide et Bombay appartient à cette région. |
| `state_region = s:STATE_BOMBAY` dans `ship` | `DROP_AS_OBSOLETE` | Absent du format naval 1.13 actuel et retiré par le portage du fork. |
| Une `ship_type_frigate`, `count = 1` | `NEEDS_HISTORICAL_RESEARCH` | Valeur WIP à préserver comme hypothèse, pas comme chiffre définitif avant la base manpower/équipages mondiale. |
| Zéro vaisseau de ligne et zéro amiral | `NEEDS_HISTORICAL_RESEARCH` | Contraintes WIP plausibles mais non figées par CLEANUP-1A. |
| `building_naval_administration` | `ADAPT` | ID valide, mais nécessité, technologie et niveau doivent découler de la flotte finale et de son équipage. |
| Niveau 1 + `pm_simple_sailor_recruitment` | `NEEDS_HISTORICAL_RESEARCH` | Le niveau encode environ 1 000 marins et ne doit pas être figé avant le recalibrage global ; MARATH ne possède pas explicitement `admiralty`. |
| Rapport NAVY-3C-3 untracked | `ADAPT` | À conserver comme source forensique ; les assertions de compatibilité et le plan de test doivent être actualisés avant toute publication. |

Il n'y a donc aucun `DROP_AS_DUPLICATE`. La seule suppression technique nette est le `state_region` dans le navire. Les chiffres et la logistique doivent rester des hypothèses documentées.

## 8. Conflict risk matrix

| Chemin / élément | Risque textuel | Risque sémantique | Niveau global si récupéré verbatim | Cause principale |
| --- | --- | --- | --- | --- |
| `common/history/buildings/10_india.txt` | `CLEAN` | Moyen | `MEDIUM_RISK` | Hunk textuellement propre, mais niveau d'équipage et prérequis `admiralty` non réévalués. |
| `common/history/military_formations/05_military_formations_india.txt` | `CLEAN` au contrôle de patch | Élevé | `HIGH_RISK` | Fichier modifié par le portage/QA ; champ naval `state_region` obsolète et proximité du HQ MARATH corrigé. |
| Rapport NAVY-3C-3 | `CLEAN` comme nouveau fichier | Moyen | `MEDIUM_RISK` | Certaines conclusions sont antérieures au portage 1.13 et les tests annoncés n'ont pas été exécutés. |
| Localisation anglaise | `CLEAN` | Faible | `LOW_RISK` | Aucun doublon ; dépend seulement de l'existence finale de la formation. |
| Localisation française | `CLEAN` | Faible | `LOW_RISK` | Aucun doublon ; dépend seulement de l'existence finale de la formation. |
| Application globale du stash | Probablement propre textuellement | Élevé | `HIGH_RISK` | L'absence de conflit Git masquerait la réintroduction de conventions navales pré-portage et des choix d'équilibrage non validés. |

Le conflit probable n'est donc pas un conflit de lignes. Il est principalement sémantique et de version.

## 9. Recommended CLEANUP-1B recovery strategy

Stratégie recommandée : combinaison contrôlée **B + A + D**, avec **B comme méthode principale**.

1. Repartir des fichiers de HEAD et reconstruire manuellement la fonctionnalité ; ne pas appliquer ou popper le stash.
2. Utiliser le stash uniquement comme référence forensique pour le nom, l'intention, les localisations et les hypothèses historiques.
3. Si la flotte est retenue, insérer manuellement dans le bloc MARATH actuel une formation 1.13 minimale en préservant intégralement le HQ terrestre `region_north_india`.
4. Conserver `type = fleet`, `hq_region = sr:region_south_india` et le namespace `ship_type:` ; supprimer le champ `state_region` du navire.
5. Ne décider le type et le nombre de navires qu'après la recherche historique/manpower prévue. La valeur `1 frigate` reste une hypothèse à tester, pas une donnée acquise.
6. Ne créer l'administration navale qu'après calcul du besoin d'équipage et décision explicite sur la cohérence avec `admiralty`; ne pas ajouter automatiquement une technologie pour sauver le hunk.
7. Ajouter les localisations manuellement seulement quand l'identifiant final de formation est figé.
8. Réécrire/actualiser le rapport NAVY-3C-3 au lieu de restaurer verbatim ses conclusions pré-portage.
9. Effectuer ensuite les validations statiques, puis un runtime séparé hors CLEANUP-1A si CLEANUP-1B ou une phase ultérieure l'exige.

La stratégie C — appliquer le stash sur une branche isolée — n'apporte pas d'avantage ici : les hunks sont minuscules, lisibles et textuellement propres, tandis que le risque est précisément de conserver silencieusement leur sémantique ancienne.

## 10. Protected-state verification

État protégé contrôlé avant audit et à nouveau après création du présent rapport :

- branche restée `cleanup-post-release` ;
- HEAD resté `1e374f2f40252d229bc249600e3cbbe26085122d` ;
- `stash@{0}` resté `518df704fa14599c0f254fae13859210663dd976` avec le même message ;
- les sept fichiers `docs/research/technology/*` demandés sont toujours présents, non suivis et non staged ;
- leurs SHA-256 de départ ont été relevés pour comparaison de sortie ;
- `bject` reste absent ;
- aucun fichier de gameplay n'a été modifié ;
- le seul nouveau fichier est le présent rapport ;
- aucune commande de mutation Git, aucun lancement du jeu, aucun test runtime et aucune recherche web/historique n'ont été effectués.

Le contrôle BIC confirme dans HEAD :

```text
activate_law = law_type:law_frontier_colonization
```

Le stash ne touche pas le fichier pays BIC et ne contient aucun rétablissement de `law_colonial_exploitation`.

## 11. Final verdict

Le WIP MARATH reste **partiellement pertinent**. Son intention, son nom, ses localisations, son HQ naval et ses IDs principaux sont récupérables. Il ne doit toutefois pas être appliqué tel quel : le `state_region` naval est obsolète, le fichier de formations a été porté et validé depuis, et les valeurs `1 frigate` / administration niveau 1 relèvent désormais de la future méthode historique d'équipage.

Une récupération contrôlée peut commencer lors de CLEANUP-1B à condition de reconstruire depuis HEAD et de traiter les chiffres comme non décidés. CLEANUP-1A s'arrête à cet audit.

```text
STASH_IDENTITY_VERIFIED = YES
STASH_BASE_IDENTIFIED = YES
STASH_CONTENT_FULLY_INVENTORIED = YES
STASH_UNTRACKED_PARENT_PRESENT = YES
CURRENT_HEAD_DIVERGENCE_ASSESSED = YES
V13_COMPATIBILITY_ASSESSED = YES
MARATHA_WIP_STILL_RELEVANT = PARTIAL
SAFE_TO_BEGIN_CONTROLLED_RECOVERY = YES
RECOMMENDED_RECOVERY_METHOD = Rebuild manually from current HEAD; reuse selected intent/localization, drop obsolete ship state_region, recalculate naval numbers and crew support.
RUNTIME_REQUIRED_FOR_CLEANUP1A = NO
GAMEPLAY_FILES_MODIFIED = NO
STASH_MODIFIED = NO
```
