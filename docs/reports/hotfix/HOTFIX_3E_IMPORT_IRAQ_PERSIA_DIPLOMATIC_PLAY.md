# HOTFIX-3E - Diplomatic play Iraq / Persia / Arabia / Oman

## 1. Résumé

Le diplomatic play du hotfix `00_otto_iraqi_persia_war.txt` a été importé après validation des tags, des `region_state` ciblés et de la syntaxe vanilla 1.13. Le fichier est entièrement dédié au play `PER / IR1 / ARB / OMA` et a donc été créé tel quel dans le fork.

## 2. Fichier hotfix consulté

- `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source\common\history\diplomatic_plays\00_otto_iraqi_persia_war.txt`

## 3. Lecture du diplomatic play hotfix

| Élément | Valeur hotfix | Référence à vérifier |
|---|---|---|
| Initiateur | `c:PER` | Tag PER |
| Cible initiale | `s:STATE_BASRA.region_state:IR1` | State Basra sous IR1 |
| `war` | `no` | Syntaxe vanilla `create_diplomatic_play` |
| Type de play | `dp_conquer_state` | Type vanilla |
| Backer cible | `c:OMA` | Tag OMA |
| War goal 1 | `holder = c:IR1`, `type = conquer_state`, `target_state = s:STATE_KHUZESTAN.region_state:ARB` | Tags IR1/ARB et Khuzestan sous ARB |
| War goal 2 | `holder = c:OMA`, `type = take_treaty_port`, `target_state = s:STATE_FARS.region_state:PER` | Tags OMA/PER et Fars sous PER |

## 4. Tags vérifiés

| Tag | Country definition ? | History country ? | Statut |
|---|---|---|---|
| `PER` | Oui, `common/country_definitions/00_countries.txt` | Oui, `common/history/countries/per - persia.txt` | Valide |
| `IR1` | Oui, `common/country_definitions/02_modded_countries.txt` | Oui, `common/history/countries/ir1 - mamluk iraq.txt` | Valide |
| `ARB` | Oui, `common/country_definitions/00_countries.txt` | Oui, `common/history/countries/arb - arabistan.txt` | Valide |
| `OMA` | Oui, `common/country_definitions/00_countries.txt` | Oui, `common/history/countries/oma - oman.txt` | Valide |
| `TUR` | Oui, `common/country_definitions/00_countries.txt` | Oui, `common/history/countries/tur - ottoman empire.txt` | Valide |

## 5. States / region_state vérifiés

| State | region_state attendu par diplomatic play | region_state trouvé | Valide ? |
|---|---|---|---|
| `STATE_BASRA` | `IR1` | `region_state:IR1` dans `common/history/pops/08_middle_east.txt` et `common/history/buildings/08_middle_east.txt`; owner `c:IR1` dans `00_states.txt` | Oui |
| `STATE_KHUZESTAN` | `ARB` | `region_state:ARB` dans `common/history/pops/08_middle_east.txt`; owner `c:ARB` dans `00_states.txt` | Oui |
| `STATE_FARS` | `PER` | `region_state:PER` dans `common/history/pops/08_middle_east.txt`; owner `c:PER` dans `00_states.txt` | Oui |

## 6. Syntaxe vanilla vérifiée

Les éléments utilisés existent ou sont attestés dans la vanilla The Great Wave :

- `create_diplomatic_play` est utilisé dans `common/history/diplomatic_plays`.
- `war = yes/no` est utilisé dans les diplomatic plays vanilla.
- `dp_conquer_state` existe dans `common/diplomatic_plays/00_diplomatic_plays.txt`.
- `conquer_state` existe comme war goal.
- `take_treaty_port` existe comme war goal.
- `add_target_backers` est référencé dans la localisation d'effets et utilisé par des scripts vanilla.
- La syntaxe `s:STATE_X.region_state:TAG` est utilisée dans des scripts vanilla et dans le fichier local `00_american_revolution.txt`.

## 7. Diplomatic play importé

Import réussi.

Fichier créé :

- `common/history/diplomatic_plays/00_otto_iraqi_persia_war.txt`

Résumé du play :

| Élément | Valeur |
|---|---|
| Initiateur | `PER` |
| Cible initiale | `STATE_BASRA.region_state:IR1` |
| Backer cible | `OMA` |
| War goal principal | `dp_conquer_state` sur Basra |
| War goal ajouté 1 | `IR1` revendique `STATE_KHUZESTAN.region_state:ARB` avec `conquer_state` |
| War goal ajouté 2 | `OMA` revendique un treaty port sur `STATE_FARS.region_state:PER` |
| Guerre immédiate | `war = no` |

## 8. Ce qui n'a pas été modifié

- Aucun state modifié.
- Aucune pop modifiée.
- Aucun bâtiment modifié.
- Aucune formation militaire modifiée.
- Aucune diplomatie existante modifiée.
- Aucun secret goal IA importé.
- Aucun changement à `PER`, `ARB`, `OMA`, `TUR` ou `IR1` hors création du play.
- Aucun changement BIC, Japon, Inde, NAVY ou ADMIN.
- Aucun changement aux lois HOTFIX-2.

## 9. Risques restants

- Le play démarre avec `war = no`; son comportement exact doit être vérifié en jeu.
- L'équilibrage diplomatique entre `PER`, `IR1`, `ARB` et `OMA` peut nécessiter une phase séparée.
- Aucune IA secret goal n'a été importée, donc le comportement IA peut différer du hotfix complet.

## 10. Tests à faire en jeu

1. Lancer le mod seul.
2. Démarrer une partie en 1776.
3. Vérifier que le diplomatic play existe ou se déclenche correctement.
4. Vérifier les participants : `PER`, `IR1`, `ARB`, `OMA`.
5. Vérifier que la cible initiale est Basra sous IR1.
6. Vérifier les war goals sur Khuzestan et Fars.
7. Observer les premières semaines et surveiller `error.log`.
8. Rechercher dans les logs : `00_otto_iraqi_persia_war`, `create_diplomatic_play`, `STATE_BASRA`, `STATE_KHUZESTAN`, `STATE_FARS`, `IR1`, `ARB`, `OMA`, `PER`.

## 11. Liste exacte des fichiers créés/modifiés

- `common/history/diplomatic_plays/00_otto_iraqi_persia_war.txt`
- `docs/reports/hotfix/HOTFIX_3E_IMPORT_IRAQ_PERSIA_DIPLOMATIC_PLAY.md`

## 12. Confirmation de périmètre

- Aucun state modifié.
- Aucune pop modifiée.
- Aucun bâtiment modifié.
- Aucune formation militaire modifiée.
- Aucune diplomatie existante modifiée.
- Aucun secret goal IA importé.
- Aucun changement BIC, Japon, Inde, NAVY ou ADMIN.
- Le stash MARATH n'a pas été appliqué ni modifié.
