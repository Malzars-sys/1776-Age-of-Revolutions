# HOTFIX-6A.8R — Audit Victoria 3 1.13 de la Grande Crise orientale

## 1. Identification

- Date : 29 juillet 2026.
- Phase : `HOTFIX_6A8R_GREAT_EASTERN_CRISIS_1_13_AUDIT`.
- Nature : audit strictement documentaire.
- Branche : `hotfix-dlc-audit`.
- HEAD initial et final attendu :
  `b1ba3ef0a649ff45f42df2daec44986863957a66`.
- Commit initial :
  `b1ba3ef Align Greek nationalism APIs with Victoria 3 1.13`.
- Gameplay modifié par 6A.8R : aucun.

## 2. État Git initial

Le préflight est conforme :

- racine exacte du fork ;
- branche `hotfix-dlc-audit` ;
- rapport 6A.7F présent dans le HEAD ;
- verdicts runtime et de clôture 6A.7F présents ;
- prochaine phase 6A.8R présente dans le HEAD ;
- aucun fichier suivi modifié ;
- aucun fichier staged ;
- seuls `bject` et les sept fichiers de
  `docs/research/technology/` non suivis ;
- stash exact présent :
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` ;
- `git diff --check` propre ;
- aucun processus Victoria 3 ou Paradox.

État initial :

```text
?? bject
?? docs/research/technology/
```

## 3. Sources consultées

Documents lus intégralement :

- `HOTFIX_6A7F_GREEK_NATIONALISM_1_13_API_ALIGNMENT.md` ;
- `HOTFIX_6A7_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md` ;
- `HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_ALIGNMENT.md` ;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- `HOTFIX_REPORT_INDEX.csv` ;
- `HOTFIX_GLOBAL_DIFFERENCE_INVENTORY.csv` ;
- `HOTFIX_C1AI_CONCURRENT_WORK_RECONCILIATION.md` ;
- changelogs complets du fork et de la source hotfix ;
- logs et rotations existants de 6A.7F, en lecture seule.

Comparaison gameplay intégrale, sans modification :

1. fork ;
2. source `1776_Age_of_Revolutions_hotfix_source` ;
3. vanilla Victoria 3 1.13.

## 4. Objet et structure

Fichier :

`common/journal_entries/05_great_eastern_crisis.txt`

Objet unique :

`je_great_eastern_crisis`

| Arbre | Début | Fin | Accolades ouvrantes/fermantes | Profondeur finale/minimale |
| --- | ---: | ---: | ---: | ---: |
| Fork | 1 | 316 | 104 / 104 | 0 / 0 |
| Source hotfix | 1 | 334 | 109 / 109 | 0 / 0 |
| Vanilla 1.13 | 1 | 335 | 109 / 109 | 0 / 0 |

L’objet occupe l’intégralité du fichier dans les trois arbres.

## 5. Hashes, encodages et fins de ligne

| Arbre | SHA-256 | Octets | Encodage | LF/CRLF | Saut final |
| --- | --- | ---: | --- | ---: | --- |
| Fork | `77E6FE839DDFF0CC4A33102D284186FFB440434FA9960DC20B316A721ED3A3A4` | 7 392 | UTF-8 avec BOM | 316 / 0 | présent |
| Source hotfix | `269CD001D5DE0D04CC53F2077B66BEBA76A9E4A4C6D1253E3DE4DF816098E808` | 7 995 | UTF-8 avec BOM | 334 / 0 | présent |
| Vanilla 1.13 | `55237D5C08DE84CFCBE266DC92DF18C56FAF818C28DCE2B8CB69A4A25C44809D` | 7 996 | UTF-8 avec BOM | 335 / 0 | présent |

Source hotfix et vanilla sont fonctionnellement identiques. Leur seule
différence est une ligne blanche après l’ouverture de l’objet : vanilla la
conserve, la source la supprime.

Le futur fichier corrigé doit conserver la ligne blanche du fork, retirer la
tabulation d’une ligne blanche vanilla et produire :

`96F65E2B3CC7129DD8D4AD41382F9F8DD97FB5FA24C66C05F129B1E31615F75A`

Taille prévisible : 7 995 octets, 335 LF, 0 CRLF, BOM et saut final présents.

## 6. Erreur runtime historique

La session 6A.7F contient exactement 387 erreurs globales de l’ancien pinning
et exactement une occurrence pour le fichier audité :

```text
[13:26:20][pdx_persistent_reader.cpp:268]: Error: "Unexpected token: should_be_pinned_by_default, near line: 313" in file: "common/journal_entries/05_great_eastern_crisis.txt" near line: 313
```

Cette occurrence se trouve à la ligne 365 de `debug.log`. `debug.1.log` et
`debug.log` constituent les nouveaux logs de 6A.7F ; les autres rotations sont
historiques.

Comptes dans les nouveaux logs 6A.7F :

| Diagnostic | Occurrences |
| --- | ---: |
| Ancien pinning global | 387 |
| Chemin `05_great_eastern_crisis.txt` | 1 |
| `should_be_pinned_by_default_involved` | 0 erreur |
| `should_be_pinned_by_default_uninvolved_or_context` | 0 erreur |
| Autre erreur propre au fichier | 0 |

Les rotations antérieures sont séparées. Aucun nouveau runtime n’a été produit.

## 7. Carte des six hunks fonctionnels

Les six hunks sont six groupes fonctionnels. Leur proximité produit seulement
deux blocs `@@` dans un diff unifié.

| Hunk | Fonction | Fork | Source | Vanilla | Bloc parent |
| ---: | --- | ---: | ---: | ---: | --- |
| 1 | Région du sujet | 12 | 11 | 12 | `should_be_involved > any_subject_or_below` |
| 2 | Région du pays | 14 | 13 | 14 | `should_be_involved > OR` |
| 3 | Scope stratégique russe | 17 | 16 | 17 | `should_be_involved > AND` |
| 4 | Visibilité hors implication | absent, insertion après 20 | 21–35 | 22–36 | niveau racine |
| 5 | Héritage révolutionnaire | absent, insertion après 315 | 333 | 334 | niveau racine |
| 6 | Pinning impliqué/contextuel | 313 | 328–329 | 329–330 | niveau racine |

## 8. Hunk 1 — Région du sujet

| Champ | Résultat |
| --- | --- |
| Numéro du hunk | 1 |
| Chemin | `common/journal_entries/05_great_eastern_crisis.txt` |
| Objet | `je_great_eastern_crisis` |
| Bloc parent | `should_be_involved > OR > any_subject_or_below` |
| Ligne fork | 12 |
| Texte fork | `is_in_geographic_region = geographic_region_balkans` |
| Ligne hotfix | 11 |
| Texte hotfix | `is_in_geographic_region = geographic_region_balkans_old` |
| Ligne vanilla | 12 |
| Texte vanilla | `is_in_geographic_region = geographic_region_balkans_old` |
| Convergence hotfix/vanilla | exacte |
| Comportement moteur attendu | implique un pays possédant un sujet dans les 21 États balkaniques historiques |
| Impact 1776 | évite d’impliquer via un sujet situé seulement en Hongrie, Roumanie ou Bessarabie |
| Dépendances | définition vanilla héritée de `geographic_region_balkans_old` |
| Collision avec les autres hunks | couplé au hunk 2 et au bloc de visibilité |
| Localisation | aucune |
| Risque de régression | faible ; le fork hérite déjà de la région |
| Rollback futur | retirer `_old` sur cette occurrence seulement |
| Décision exclusive | `REQUIRED_1_13_ALIGNMENT` |

Cette occurrence porte sur les sujets du pays évalué, pas uniquement sur les
sujets ottomans.

## 9. Hunk 2 — Région du pays

| Champ | Résultat |
| --- | --- |
| Numéro du hunk | 2 |
| Chemin | même fichier |
| Objet | même objet |
| Bloc parent | `should_be_involved > OR` |
| Ligne fork | 14 |
| Texte fork | `is_in_geographic_region = geographic_region_balkans` |
| Ligne hotfix | 13 |
| Texte hotfix | `is_in_geographic_region = geographic_region_balkans_old` |
| Ligne vanilla | 14 |
| Texte vanilla | `is_in_geographic_region = geographic_region_balkans_old` |
| Convergence hotfix/vanilla | exacte |
| Comportement moteur attendu | implique directement les pays présents dans les Balkans historiques |
| Impact 1776 | Wallachie, Moldavie et États hongrois ne sont plus impliqués par la seule région stratégique élargie |
| Dépendances | même région que le hunk 1 |
| Collision avec les autres hunks | cohérence requise avec hunks 1 et 4 |
| Localisation | aucune |
| Risque de régression | faible |
| Rollback futur | retirer `_old` sur cette occurrence seulement |
| Décision exclusive | `REQUIRED_1_13_ALIGNMENT` |

Les hunks 1 et 2 reçoivent la même décision mais remplissent des fonctions
différentes : sujet d’un pays contre présence directe du pays.

## 10. Hunk 3 — Scope stratégique

| Champ | Résultat |
| --- | --- |
| Numéro du hunk | 3 |
| Chemin | même fichier |
| Objet | même objet |
| Bloc parent | `should_be_involved > AND`, branche Russie |
| Ligne fork | 17 |
| Texte fork | `has_interest_marker_in_region = region_balkans` |
| Ligne hotfix | 16 |
| Texte hotfix | `has_interest_marker_in_region = sr:region_balkans` |
| Ligne vanilla | 17 |
| Texte vanilla | `has_interest_marker_in_region = sr:region_balkans` |
| Convergence hotfix/vanilla | exacte |
| Comportement moteur attendu | fournit un scope de région stratégique typé |
| Impact 1776 | conserve l’implication russe conditionnée à son intérêt balkanique |
| Dépendances | définition `region_balkans` dans les strategic regions |
| Collision avec les autres hunks | indépendante de la composition de la geographic region, mais située dans le même bloc d’implication |
| Localisation | aucune |
| Risque de régression | très faible |
| Rollback futur | retirer le préfixe `sr:` |
| Décision exclusive | `REQUIRED_1_13_ALIGNMENT` |

Le préfixe `sr:` est la syntaxe 1.13 cohérente. Le fork utilise déjà cette forme
dans cinq fichiers et 30 lignes ; l’occurrence non typée du fichier audité est
unique.

## 11. Hunk 4 — Visibilité hors implication

| Champ | Résultat |
| --- | --- |
| Numéro du hunk | 4 |
| Chemin | même fichier |
| Objet | même objet |
| Bloc parent | niveau racine |
| Ligne fork | absente ; point d’insertion après la ligne 20 |
| Texte fork | bloc absent |
| Ligne hotfix | 21–35 |
| Texte hotfix | bloc exact reproduit ci-dessous |
| Ligne vanilla | 22–36 |
| Texte vanilla | même bloc exact |
| Convergence hotfix/vanilla | exacte |
| Comportement moteur attendu | montre l’entrée aux pays balkaniques/anatoliens, aux pays ayant un intérêt Balkans/Proche-Orient et aux sujets dont le suzerain est régional |
| Impact 1776 | rend la situation consultable sans transformer tous les observateurs en impliqués |
| Dépendances | hunks 1–3, `geographic_region_megali_greece`, scripted trigger d’intérêt |
| Collision avec les autres hunks | directement couplé au pinning contextuel du hunk 6 |
| Localisation | aucune |
| Risque de régression | faible à modéré, contrôlable en runtime |
| Rollback futur | supprimer exactement le bloc |
| Décision exclusive | `REQUIRED_1_13_ALIGNMENT` |

Bloc futur exact :

```txt
	should_show_when_not_involved = {
		OR = {
			is_in_geographic_region = geographic_region_balkans_old
			is_in_geographic_region = geographic_region_megali_greece # Proxy for Anatolia
			country_has_interest_marker_in_great_eastern_crisis_region = yes
            top_overlord ?= {
                capital = {
					OR = {
						is_in_geographic_region = geographic_region_balkans_old
						is_in_geographic_region = geographic_region_megali_greece
					}
                }
            }
		}
	}
```

Le scripted trigger hérité de vanilla teste `sr:region_balkans` ou
`sr:region_near_east`. Le fork ne remplace pas `common/scripted_triggers`,
`common/geographic_regions` ou `common/strategic_regions`; toutes les
dépendances sont donc déjà effectives.

## 12. Hunk 5 — Héritage par révolution

| Champ | Résultat |
| --- | --- |
| Numéro du hunk | 5 |
| Chemin | même fichier |
| Objet | même objet |
| Bloc parent | niveau racine, après `transferable = no` |
| Ligne fork | absente ; point d’insertion après la ligne 315 |
| Texte fork | propriété absente |
| Ligne hotfix | 333 |
| Texte hotfix | `can_revolution_inherit = yes` |
| Ligne vanilla | 334 |
| Texte vanilla | `can_revolution_inherit = yes` |
| Convergence hotfix/vanilla | exacte |
| Comportement moteur attendu | autorise le successeur révolutionnaire à conserver la situation |
| Impact 1776 | évite la disparition de la crise lors d’une guerre civile ottomane ou balkanique |
| Dépendances | aucune dépendance syntaxique aux autres hunks |
| Collision avec les autres hunks | indépendant techniquement, cohérent avec la continuité de l’objet |
| Localisation | aucune |
| Risque de régression | faible ; 20 occurrences vanilla dans 15 fichiers |
| Rollback futur | supprimer la propriété |
| Décision exclusive | `REQUIRED_1_13_ALIGNMENT` |

Cette propriété est un choix comportemental explicite, pas une API obligatoire
pour toutes les entrées. L’accord exact hotfix/vanilla et l’absence de
contre-indication 1776 justifient néanmoins son alignement dans cet objet.

## 13. Hunk 6 — Pinning impliqué/contextuel

| Champ | Résultat |
| --- | --- |
| Numéro du hunk | 6 |
| Chemin | même fichier |
| Objet | même objet |
| Bloc parent | niveau racine |
| Ligne fork | 313 |
| Texte fork | `should_be_pinned_by_default = yes` |
| Ligne hotfix | 328–329 |
| Texte hotfix | `should_be_pinned_by_default_involved = yes` puis `should_be_pinned_by_default_uninvolved_or_context = no` |
| Ligne vanilla | 329–330 |
| Texte vanilla | mêmes deux propriétés |
| Convergence hotfix/vanilla | exacte |
| Comportement moteur attendu | épingle automatiquement pour les acteurs impliqués, jamais pour les simples observateurs |
| Impact 1776 | évite d’épingler la crise chez tous les pays autorisés à la consulter |
| Dépendances | `should_be_involved` et hunk 4 |
| Collision avec les autres hunks | fortement couplé au hunk 4 |
| Localisation | aucune |
| Risque de régression | faible |
| Rollback futur | remplacer les deux propriétés par l’ancien champ |
| Décision exclusive | `REQUIRED_1_13_ALIGNMENT` |

Les deux propriétés sont nécessaires parce que l’entrée distingue acteurs
impliqués et observateurs contextuels. Corriger seulement le parser sans
ajouter la visibilité laisserait cette sémantique incomplète.

## 14. Analyse des régions

Les deux geographic regions existent toujours dans vanilla 1.13 et sont
héritées par le fork.

| Région | Construction | États |
| --- | --- | ---: |
| `geographic_region_balkans_old` | liste explicite des anciens Balkans | 21 |
| `geographic_region_balkans` | enveloppe de `sr:region_balkans` | 36 |

Les 21 États de `_old` sont tous inclus dans la nouvelle région. La nouvelle
région ajoute exactement :

- Banat, Békés, Bessarabie, Bucovine ;
- Hongrie centrale, Délvidék, Ruthénie, Slovaquie, Transdanubie ;
- Dobroudja, Moldavie, Valachie ;
- Transylvanie septentrionale et méridionale ;
- Thrace orientale.

Le suffixe `_old` ne désigne donc pas une API disparue. Il identifie une région
historique volontairement conservée pour les contenus dont le périmètre ne doit
pas suivre l’élargissement de la nouvelle strategic region.

`sr:region_balkans` est un scope de région stratégique typé et indépendant des
geographic regions. Il est approprié aux marqueurs d’intérêt, tandis que
`geographic_region_balkans_old` est appropriée aux tests territoriaux précis.

## 15. Réponses sémantiques

1. `_old` préserve les 21 Balkans historiques ; l’absence du suffixe englobe
   15 États hongrois, roumains, transylvains ou orientaux supplémentaires.
2. Les deux occurrences reçoivent la même décision, mais l’une teste les sujets
   et l’autre le pays lui-même.
3. `sr:` est la forme typée requise par l’API actuelle du marqueur d’intérêt.
4. Les observateurs pertinents sont les pays de la zone historique/anatolienne,
   ceux ayant un intérêt Balkans/Proche-Orient et les sujets de suzerains
   régionaux.
5. Le bloc hors implication est cohérent avec la géographie étroite pour les
   acteurs et élargit seulement la consultation contextuelle.
6. Le pinning `yes/no` correspond exactement à cette séparation.
7. L’héritage évite la perte de la situation lors d’une révolution.
8. `can_revolution_inherit` est un choix comportemental explicite, pas une
   obligation universelle du moteur.
9. Les hunks 1–4 et 6 sont fortement liés ; le hunk 5 est techniquement
   indépendant mais cohérent et sans collision dans le même objet.
10. Une future correction tient dans 1 fichier, 1 objet et 6 hunks
    fonctionnels.
11. Le diff futur propre reste exactement de 23 additions et 4 suppressions.
12. Un sous-ensemble, notamment le seul pinning, laisserait visibilité, région,
    scope ou continuité partiellement obsolètes.
13. Aucun hunk ne requiert un report pour préserver 1776.
14. Un runtime humain sera requis pour la visibilité et le pinning.
15. Une session neuve avec l’Empire ottoman puis un observateur contextuel
    suffit ; l’héritage révolutionnaire peut rester statique.

## 16. Impact sur le scénario 1776

L’Empire ottoman reste toujours impliqué par `c:TUR ?= this`. Les hunks
géographiques empêchent surtout que les pays situés seulement dans l’extension
hongroise/roumaine de la nouvelle région deviennent automatiquement impliqués.

Dans le setup observé :

- Valachie et Moldavie existent et se trouvent dans les 15 États ajoutés ;
- l’utilisation de `_old` évite de les assimiler sans distinction au noyau
  balkanique historique ;
- elles peuvent toutefois voir la situation via un intérêt pertinent ou leur
  suzerain ;
- la Russie reste impliquée uniquement si elle possède un marqueur d’intérêt
  dans `sr:region_balkans`.

La géographie proposée améliore donc la distinction entre implication et
contexte au lieu d’importer aveuglément une carte vanilla. Elle ne rouvre ni
Balkan National Awakening ni le nationalisme grec.

## 17. Dépendances, collisions et localisations

### Dépendances déjà présentes

- `geographic_region_balkans_old` ;
- `geographic_region_megali_greece` ;
- `sr:region_balkans` ;
- `sr:region_near_east` ;
- `country_has_interest_marker_in_great_eastern_crisis_region`.

Le fork remplace `common/journal_entries`, mais pas les répertoires définissant
ces régions ou scripted triggers.

### Collision

- aucune collision avec un fichier protégé ;
- un seul objet ;
- hunks 1–4 et 6 sémantiquement couplés ;
- hunk 5 indépendant mais local et convergent ;
- risque global faible à modéré.

### Localisations

Aucune nouvelle clé ou modification de localisation n’est requise.

## 18. Taille et diff futurs

Périmètre fermé :

- 1 fichier ;
- 1 objet ;
- 6 hunks fonctionnels ;
- 2 blocs `@@` dans le diff unifié ;
- 23 additions ;
- 4 suppressions ;
- aucune autre ligne ;
- aucun remplacement complet.

La 23e addition est une ligne blanche structurelle. Elle doit rester réellement
vide : ne pas importer la tabulation présente sur la ligne blanche vanilla.
Conserver aussi la ligne blanche initiale du fork, absente de la source hotfix.

## 19. Rollback futur

1. remplacer les deux `_old` du bloc `should_be_involved` par
   `geographic_region_balkans` ;
2. remplacer `sr:region_balkans` par `region_balkans` ;
3. supprimer exactement `should_show_when_not_involved` ;
4. supprimer `can_revolution_inherit = yes` ;
5. remplacer les deux propriétés de pinning par
   `should_be_pinned_by_default = yes`.

Le rollback ne doit modifier aucune autre ligne et ne doit jamais restaurer le
fichier complet.

## 20. Scénario runtime humain futur

Un seul lancement :

1. partie neuve en 1776 avec fork et `dlc014_ip3` montés ;
2. jouer l’Empire ottoman ;
3. ouvrir `Journal > Potentiel` et inspecter `Grande Crise orientale` ;
4. vérifier texte, conditions, implication et pinning ;
5. dans la même session et sans console, utiliser le changement de pays
   standard si disponible pour un observateur ayant un intérêt
   Balkans/Proche-Orient ;
6. vérifier la visibilité contextuelle ou son absence cohérente et l’absence de
   pinning automatique ;
7. avancer d’au moins un jour ;
8. fermer le jeu et le launcher ;
9. transmettre les observations ;
10. analyser ensuite les logs : erreur ciblée 1 vers 0 et aucune erreur sur les
    nouvelles propriétés.

Ne pas provoquer artificiellement une révolution. Le hunk 5 reste couvert par
la preuve statique et le smoke global final.

## 21. Décision atomique

Décision : **Option A**.

Les six hunks sont cohérents et exécutables ensemble :

- source hotfix et vanilla convergent fonctionnellement sur les six ;
- aucune divergence intentionnelle 1776 n’est démontrée ;
- les dépendances sont déjà disponibles ;
- aucun hunk ne touche un bloc protégé ;
- un sous-ensemble laisserait l’objet partiellement obsolète ;
- le hunk révolutionnaire, bien qu’indépendant, est local, convergent et sans
  motif de report.

Classification exclusive :

| Hunk | Décision |
| ---: | --- |
| 1 | `REQUIRED_1_13_ALIGNMENT` |
| 2 | `REQUIRED_1_13_ALIGNMENT` |
| 3 | `REQUIRED_1_13_ALIGNMENT` |
| 4 | `REQUIRED_1_13_ALIGNMENT` |
| 5 | `REQUIRED_1_13_ALIGNMENT` |
| 6 | `REQUIRED_1_13_ALIGNMENT` |

Future phase :

`NEXT_EXECUTION_PHASE = HOTFIX_6A8F_GREAT_EASTERN_CRISIS_1_13_ALIGNMENT`

## 22. Protections

Restent intacts : 6A.3F à 6A.7F, DEI/VOC, Java, Balkan National Awakening,
Yugoslavia, Risorgimento, nationalisme grec, Coup, Imperialism of Promise,
Merchant Banking, Navigation Acts, NAVY, formations, MARATH, SAT, KHP,
Travancore, Inde, BIC, Sepoy, Bombay, ADMIN, Japon, Russie, Autriche, Croatie,
Slavonie, Suisse, révolutions américaine et française, lettres de Kew,
technologies, agriculture, alimentation, industrie, localisations générales,
descripteurs, launcher, sauvegardes et `bject`.

Les huit hashes protégés sont identiques à ceux du préflight. BIC conserve
`law_frontier_colonization` et `law_colonial_exploitation` n’est pas restaurée.

## 23. Documents modifiés

Uniquement :

1. `HOTFIX_6A8R_GREAT_EASTERN_CRISIS_1_13_AUDIT.md` ;
2. `docs/reports/hotfix/INDEX.md` ;
3. `HOTFIX_REPORT_INDEX.csv` ;
4. `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
5. `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
6. `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

## 24. État Git final et commit

Le HEAD final reste
`b1ba3ef0a649ff45f42df2daec44986863957a66`. L’index Git reste vide et
aucun gameplay n’est modifié.

État attendu :

```text
 M docs/reports/hotfix/INDEX.md
 M docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv
 M docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md
 M docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md
 M docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv
?? bject
?? docs/reports/hotfix/_index/HOTFIX_6A8R_GREAT_EASTERN_CRISIS_1_13_AUDIT.md
?? docs/research/technology/
```

Aucun commit automatique n’est créé. 6A.8R doit être commitée manuellement
avant 6A.8F.

## 25. Verdicts

`HOTFIX_6A8R_GREAT_EASTERN_CRISIS_1_13_AUDIT_COMPLETE`

`GREAT_EASTERN_CRISIS_SIX_HUNK_DECISION_RECORDED`

`NO_GAMEPLAY_CHANGED`

`GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`

`NEXT_EXECUTION_PHASE = HOTFIX_6A8F_GREAT_EASTERN_CRISIS_1_13_ALIGNMENT`
