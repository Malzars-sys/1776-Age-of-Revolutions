# HOTFIX-2 - Merchant Banking / Navigation Acts

## 1. Résumé

Fusion manuelle limitée aux deux nouvelles lois utiles du hotfix DLC :

- `law_merchant_banking`
- `law_mercantilism_navigation_acts`

Le fichier `common/laws/00_inject_laws.txt` n'a pas été remplacé en entier. Le contenu local existant, notamment `law_merchant_republic`, a été conservé.

## 2. Fichiers comparés

| Rôle | Fichier |
|---|---|
| Fork | `common/laws/00_inject_laws.txt` |
| Hotfix upstream | `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source\common\laws\00_inject_laws.txt` |
| Vanilla 1.13 | `C:\Games\Victoria 3 The Great Wave\game` |

## 3. Lois hotfix identifiées

| Loi | Groupe | Parent | Icône | Statut |
|---|---|---|---|---|
| `law_merchant_banking` | `lawgroup_economic_system` | `law_agrarianism` | `merchant_banks.dds` | importée |
| `law_mercantilism_navigation_acts` | `lawgroup_trade_policy` | `law_mercantilism` | `regulation_acts.dds` | importée |
| `REPLACE:law_factory_councils` | `lawgroup_labour_associations` | aucun | vanilla | non importée |

## 4. Lois importées

Les blocs `law_merchant_banking` et `law_mercantilism_navigation_acts` ont été ajoutés manuellement dans `common/laws/00_inject_laws.txt`, juste avant `law_merchant_republic`.

La loi `law_mercantilism_navigation_acts` conserve son unlock `international_trade`.

La loi `law_merchant_banking` est visible pour `VEN` et `GEN`, comme dans le hotfix.

## 5. Lois locales préservées

| Élément local | Statut | Action |
|---|---|---|
| `law_merchant_republic` | existe dans le fork | conservée |
| Localisation anglaise `law_merchant_republic` | existe dans `localization/english/mod_v2content_l_english.yml` | conservée |
| Localisation française `law_merchant_republic` | existe dans `localization/french/mod_v2content_l_french.yml` | conservée |
| Icône `merchant_republic.dds` | présente dans le fork | non utilisée ici, aucune modification de la loi existante |

Le hotfix change l'icône de `law_merchant_republic` vers `merchant_republic.dds`, mais cette phase ne modifie pas les lois existantes du fork sauf nécessité. Ce changement n'a donc pas été importé.

## 6. Dépendances vérifiées

| Dépendance | Vérification |
|---|---|
| `lawgroup_economic_system` | présent en vanilla 1.13 |
| `lawgroup_trade_policy` | présent en vanilla 1.13 |
| `law_agrarianism` | présent en vanilla 1.13 |
| `law_mercantilism` | présent en vanilla 1.13 |
| `international_trade` | présent en vanilla 1.13 |
| `subject_type_colony` | présent en vanilla 1.13 |
| `subject_type_personal_union` | présent en vanilla 1.13 |
| modifiers économiques et commerciaux | présents en vanilla 1.13 |

Aucune technologie ou trigger local inventé n'a été ajouté.

## 7. Icônes utilisées

| Icône | Statut |
|---|---|
| `gfx/interface/icons/law_icons/merchant_banks.dds` | présente, utilisée par `law_merchant_banking` |
| `gfx/interface/icons/law_icons/regulation_acts.dds` | présente, utilisée par `law_mercantilism_navigation_acts` |
| `gfx/interface/icons/law_icons/merchant_republic.dds` | présente, non utilisée dans cette phase |

## 8. Localisation anglaise ajoutée

Fichier créé :

- `localization/english/hotfix_laws_l_english.yml`

Clés ajoutées :

- `law_mercantilism_navigation_acts`
- `law_mercantilism_navigation_acts_desc`
- `law_merchant_banking`
- `law_merchant_banking_desc`

Le fichier est encodé en UTF-8 BOM, comme les autres fichiers de localisation du mod.

## 9. Localisation française ajoutée

Fichier créé :

- `localization/french/hotfix_laws_l_french.yml`

Traductions principales :

- `Merchant Banking` -> `Banque marchande`
- `Navigation Acts` -> `Actes de navigation`

Le fichier est encodé en UTF-8 BOM.

## 10. Ce qui n'a pas été importé

| Élément hotfix | Raison |
|---|---|
| `REPLACE:law_factory_councils` | hors objectif HOTFIX-2 |
| changement d'icône de `law_merchant_republic` | loi locale existante, modification non nécessaire pour importer Merchant Banking / Navigation Acts |
| autres fichiers de localisation du hotfix | seules les clés nécessaires ont été isolées |
| fichiers `history/`, `events/`, `journal_entries/`, `on_actions`, `map_data`, `military_formations`, `buildings` | explicitement hors périmètre |

## 11. Risques restants

- `law_mercantilism_navigation_acts` est visible pour GBR et certains sujets de GBR, mais aucun pays n'a encore été modifié pour l'activer au départ.
- `law_merchant_banking` est visible pour VEN et GEN, mais aucun pays n'a encore été modifié pour l'activer au départ.
- L'équilibrage économique est celui du hotfix, non réévalué historiquement pour 1776.
- Le changement d'icône de `law_merchant_republic` reste disponible comme phase future, mais n'a pas été fait ici.

## 12. Tests à faire en jeu

1. Lancer le mod jusqu'au menu principal.
2. Démarrer une partie avec Venise et vérifier que `Banque marchande` / `Merchant Banking` apparaît sans clé brute.
3. Démarrer une partie avec Gênes et vérifier la même chose.
4. Démarrer une partie avec la Grande-Bretagne et vérifier que `Actes de navigation` / `Navigation Acts` apparaît dans le groupe de politique commerciale.
5. Vérifier `error.log` après chargement et après quelques jours de jeu.

Patterns utiles :

```powershell
Select-String "$env:USERPROFILE\Documents\Paradox Interactive\Victoria 3\logs\error.log" -Pattern "law_merchant_banking","law_mercantilism_navigation_acts","merchant_banks","regulation_acts"
```

## 13. Fichiers modifiés

| Fichier | Type de changement |
|---|---|
| `common/laws/00_inject_laws.txt` | ajout manuel de deux lois |
| `localization/english/hotfix_laws_l_english.yml` | nouveau fichier de localisation anglaise |
| `localization/french/hotfix_laws_l_french.yml` | nouveau fichier de localisation française |
| `docs/reports/hotfix/HOTFIX_2_LAWS_MERCHANT_BANKING_NAVIGATION_ACTS.md` | rapport de phase |

## 14. Confirmation de périmètre

Aucun fichier `history/`, `events/`, `journal_entries/`, `on_actions`, `map_data`, `military_formations`, `buildings`, BIC, Japon, Inde, NAVY ou ADMIN n'a été modifié pendant cette phase.

Le stash MARATH n'a pas été touché.
