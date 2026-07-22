# HOTFIX-3B - Activation territoriale minimale de IR1 / Mamluk Iraq

## 1. Résumé

Cette phase active territorialement `IR1` / Mamluk Iraq en transférant uniquement quatre states depuis `TUR` vers `IR1` :

- `STATE_BASRA`
- `STATE_BAGHDAD`
- `STATE_MOSUL`
- `STATE_DEIR_EZ_ZOR`

La correction reste volontairement limitée aux states, pops et bâtiments correspondants. Aucune diplomatie, armée, diplomatic play, secret goal IA, localisation ou mécanique générale du Moyen-Orient n'a été importée.

## 2. Pourquoi inclure states + pops + bâtiments ensemble

Un changement d'owner dans `common/history/states/00_states.txt` doit être accompagné par les blocs `region_state` des pops et bâtiments. Sinon, le pays posséderait les provinces, mais ses pops et bâtiments resteraient historiquement attachés à `TUR`, ce qui créerait un setup incohérent au lancement.

## 3. Fichiers hotfix consultés

- `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source\common\history\states\00_states.txt`
- `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source\common\history\pops\08_middle_east.txt`
- `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source\common\history\buildings\08_middle_east.txt`

## 4. Fichiers modifiés

- `common/history/states/00_states.txt`
- `common/history/pops/08_middle_east.txt`
- `common/history/buildings/08_middle_east.txt`
- `docs/reports/hotfix/HOTFIX_3B_ACTIVATE_IR1_TERRITORY.md`

## 5. States transférés à IR1

| State | Owner fork | Owner hotfix | Owner final | Claims ajoutés | Commentaire |
|---|---:|---:|---:|---|---|
| `STATE_BASRA` | `TUR` | `IR1` | `IR1` | `TUR` | Provinces conservées, seul l'owner change. |
| `STATE_BAGHDAD` | `TUR` | `IR1` | `IR1` | `TUR` | Capitale IR1 déjà définie en HOTFIX-3A. |
| `STATE_MOSUL` | `TUR` | `IR1` | `IR1` | `TUR` | Homelands conservés. |
| `STATE_DEIR_EZ_ZOR` | `TUR` | `IR1` | `IR1` | `TUR` | Provinces et homelands conservés. |

## 6. Claims TUR ajoutés ou confirmés

Le hotfix ajoute un claim ottoman sur les quatre states transférés. Ces claims ont été repris :

- `STATE_BASRA`: `add_claim = c:TUR`
- `STATE_BAGHDAD`: `add_claim = c:TUR`
- `STATE_MOSUL`: `add_claim = c:TUR`
- `STATE_DEIR_EZ_ZOR`: `add_claim = c:TUR`

## 7. Pops converties vers region_state:IR1

| State | region_state fork | region_state hotfix | region_state final | Pops modifiées ? |
|---|---:|---:|---:|---|
| `STATE_BASRA` | `TUR` | `IR1` | `IR1` | Composition conservée, rattachement converti. |
| `STATE_BAGHDAD` | `TUR` | `IR1` | `IR1` | Composition conservée, rattachement converti. |
| `STATE_MOSUL` | `TUR` | `IR1` | `IR1` | Composition conservée, rattachement converti. |
| `STATE_DEIR_EZ_ZOR` | `TUR` | `IR1` | `IR1` | Composition conservée, rattachement converti. |

Les ajouts de pops géorgiennes présents dans le hotfix n'ont pas été importés afin de rester sur une activation territoriale minimale et de ne pas modifier la démographie au-delà du rattachement pays.

## 8. Bâtiments convertis vers region_state:IR1

| State | Bâtiments fork | Bâtiments hotfix | Bâtiments final | country final | Commentaire |
|---|---|---|---|---|---|
| `STATE_BASRA` | Trade center, fishing wharf, rice farm, tobacco plantation, port | Même base, rattachée à IR1 | Même liste que le fork | `c:IR1` | Conversion ownership uniquement. |
| `STATE_BAGHDAD` | Textile mill, rice farm, tobacco plantation hérité | Hotfix ajoute aussi arms/artillery industries | Textile mill et rice farm convertis ; pas d'ajout industriel | `c:IR1` pour les bâtiments Baghdad existants | Les nouveaux bâtiments militaires du hotfix sont exclus de cette phase. |
| `STATE_MOSUL` | Wheat farm | Wheat farm IR1 | Wheat farm | `c:IR1` | Conversion ownership uniquement. |
| `STATE_DEIR_EZ_ZOR` | Livestock ranch | Livestock ranch IR1 | Livestock ranch | `c:IR1` | Conversion ownership uniquement. |

Note : le bloc `building_tobacco_plantation` situé dans `STATE_BAGHDAD` garde sa référence existante à `STATE_EASTERN_THRACE` et `c:TUR`, comme dans le hotfix. Cette phase ne corrige pas les anomalies historiques ou structurelles non directement nécessaires à l'activation IR1.

## 9. Ce qui n'a pas été importé

- Aucune formation militaire IR1.
- Aucune diplomatie `TUR -> IR1`.
- Aucun diplomatic play `PER / IR1 / ARB / OMA`.
- Aucun secret goal IA.
- Aucun changement général `TUR`, `PER`, `ARB` ou `OMA`.
- Aucun ajout de bâtiments militaires à Bagdad.
- Aucune conversion de lois, technologies, PM générales ou localisation.

## 10. Vérifications de cohérence

Les recherches ciblées confirment que :

- les quatre states ciblés ont `country = c:IR1` ;
- les quatre states conservent ou reçoivent `add_claim = c:TUR` ;
- les blocs pops des quatre states utilisent `region_state:IR1` ;
- les blocs bâtiments des quatre states utilisent `region_state:IR1` ;
- les `region_state:TUR` restants dans `08_middle_east.txt` concernent d'autres states ottomans ;
- aucun fichier de diplomatie, formation militaire, diplomatic play ou IA n'a été créé ou modifié.

## 11. Risques restants

- `IR1` n'a pas encore de relation diplomatique explicite avec `TUR`; cela sera traité dans une phase séparée si nécessaire.
- `IR1` n'a pas encore de formation militaire propre.
- Le hotfix ajoute des bâtiments militaires à Bagdad, mais ils n'ont pas été importés pour éviter d'élargir cette phase.
- Le bloc de bâtiment Baghdad contenant une référence à `STATE_EASTERN_THRACE` reste inchangé car il existe déjà dans le fork et dans le hotfix.

## 12. Tests à faire en jeu

1. Lancer le mod seul et vérifier que la partie atteint la sélection pays.
2. Démarrer une partie au 1er janvier 1776.
3. Vérifier que `Mamluk Iraq` / `Irak mamelouk` existe sur Basra, Baghdad, Mosul et Deir ez-Zor.
4. Vérifier que l'Empire ottoman conserve des claims sur ces states.
5. Observer un mois de jeu et surveiller `error.log`.
6. Rechercher particulièrement `IR1`, `STATE_BASRA`, `STATE_BAGHDAD`, `STATE_MOSUL`, `STATE_DEIR_EZ_ZOR`, `invalid country`, `region_state`.

## 13. Liste exacte des fichiers modifiés

- `common/history/states/00_states.txt`
- `common/history/pops/08_middle_east.txt`
- `common/history/buildings/08_middle_east.txt`
- `docs/reports/hotfix/HOTFIX_3B_ACTIVATE_IR1_TERRITORY.md`

## 14. Confirmation de périmètre

- Aucune formation militaire modifiée.
- Aucune diplomatie modifiée.
- Aucun diplomatic play importé.
- Aucun secret goal IA importé.
- Aucun changement à BIC, Japon, Inde ou NAVY.
- Aucun changement aux lois HOTFIX-2.
- Aucun fichier `common/country_definitions`, `coat_of_arms`, `flag_definitions`, `government_types`, `localization`, `events` ou `map_data` modifié.
- Le stash MARATH n'a pas été appliqué ni modifié.
