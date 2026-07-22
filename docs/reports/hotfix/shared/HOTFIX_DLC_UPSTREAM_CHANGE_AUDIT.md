# HOTFIX-DLC-AUDIT - Audit comparatif upstream hotfix

## 1. Résumé exécutif

Le hotfix upstream contient des apports réels, notamment des ajustements DLC/The Great Wave, des nouvelles lois économiques et maritimes, des icônes, des changements Inde/Iraq/Iran/Ottomans, ainsi qu'un lot important de fichiers vanilla ou DLC remis à jour.

Cependant, il chevauche directement plusieurs corrections locales déjà validées dans le fork :

- Japon / Sakoku / Tenpo / Ryukyu / Ezo / Sakhalin ;
- Australie / Nouvelle-Zélande / `map_data/state_regions/13_australasia.txt` ;
- corrections de bâtiments et PM d'administration ;
- corrections navales NAVY-1, NAVY-2, NAVY-3 ;
- choix BIC actuel avec `law_frontier_colonization` ;
- localisation française et localisation navale locale ;
- rapports `docs/reports`.

Conclusion : ne pas importer le hotfix en bloc. La bonne stratégie est une fusion manuelle par petits lots, en préservant les corrections locales et en important seulement les nouveautés clairement utiles.

## 2. Chemins comparés

| Rôle | Chemin | Statut |
|---|---|---|
| Fork courant | `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork` | existe |
| Hotfix upstream | `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source` | existe |
| Vanilla The Great Wave | `C:\Games\Victoria 3 The Great Wave\game` | existe |

Racine hotfix observée :

- `.metadata`
- `common`
- `events`
- `gfx`
- `gui`
- `localization`
- `map_data`
- `Changelog.txt`
- `Source.txt`
- `thumbnail.png`

## 3. État Git initial

| Élément | Valeur |
|---|---|
| Branche | `hotfix-dlc-audit` |
| Statut initial | working tree propre avant création des rapports d'audit |
| Stash détecté | `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` |
| Action sur stash | aucune |

Le stash MARATH a été détecté mais n'a pas été appliqué, restauré, fusionné ou inspecté comme contenu actif du fork.

## 4. Méthode de comparaison

Comparaison globale générée avec :

```powershell
$Fork = "C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork"
$Hotfix = "C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source"
git diff --no-index --name-status -- "$Fork" "$Hotfix" | Out-File "$Fork\docs\reports\hotfix\HOTFIX_DLC_RAW_NAME_STATUS.txt" -Encoding utf8
```

`git diff --no-index` retourne un code non nul lorsqu'il trouve des différences ; ce comportement est normal ici.

La comparaison brute contient beaucoup de bruit volontairement ignoré dans l'analyse :

- `.git`
- `.metadata`
- caches et métadonnées locales ;
- docs/reports locaux absents du hotfix ;
- fichiers launcher ou temporaires ;
- suppressions apparentes de fichiers de rapport qui n'ont pas vocation à exister dans le hotfix.

## 5. Résumé du Changelog hotfix

Principaux changements annoncés dans `Changelog.txt` :

| Changement annoncé dans le hotfix | Fichier probable | Déjà couvert par notre fork ? | À importer ? | Risque |
|---|---|---|---|---|
| Mise à jour vers la dernière version | nombreux fichiers vanilla/DLC | partiel | uniquement par lots | élevé |
| Hyderabad perd le vassal Southern Tamil | history countries/states/diplomacy Inde | non vérifié en détail | fusion manuelle | moyen |
| Iraq gouverné par les Mamluks et en guerre contre l'Iran | `ir1 - mamluk iraq.txt`, diplomatie, states | non | paquet cohérent seulement | élevé |
| Russie : racial law devient subjecthood | `rus - russia.txt`, lois | non vérifié | fusion manuelle | moyen |
| Iran en guerre contre les Ottomans | diplomatie / pays | non vérifié | fusion manuelle | moyen |
| Croatia-Slovenia absorbée dans l'Autriche pour accès mer/flotte | pays/states/formations | non | fusion manuelle | élevé |
| Sliver West Switzerland donné à l'Autriche | states | non | fusion manuelle | élevé |
| DEI perd Cape Colony et Ceylon à l'éclatement | East Indies events/JEs | non vérifié | fusion manuelle | moyen |
| DEI ne s'appelle plus Malaya à l'indépendance | localization/dynamic country names | non vérifié | fusion manuelle | faible à moyen |
| New laws: Merchant Banking, Navigation Acts | `common/laws/00_inject_laws.txt`, icônes | non | fusion manuelle | élevé |
| Icônes Merchant Banking / Merchant Republic / Regulation Acts | `gfx/interface/icons/law_icons/*.dds` | non | import direct possible | faible |
| Merchant Republics unique landowners name | interest groups/localization/laws | non vérifié | fusion manuelle | moyen |
| Battle For India JE / BOM fixes | journal entries / India history | partiel, Inde déjà auditée | fusion manuelle | moyen |
| British/French generals/admirals appropriate | formations militaires Europe | partiel via NAVY | fusion manuelle | élevé |
| Indian colonial administration overhaul | BIC/India/diplomacy | partiel | fusion manuelle | élevé |

## 6. Fichiers hotfix différents par domaine

| Domaine | Différences observées | Risque | Commentaire |
|---|---|---|---|
| Changelog / Source / metadata | `Changelog.txt`, `Source.txt`, `.metadata` | faible | Changelog utile ; metadata à ignorer. |
| `common/history/countries` | BIC, JAP, EZO, RYU, GBR, FRA, RUS, TUR, etc. ; hotfix ajoute `ir1 - mamluk iraq.txt` ; hotfix ne contient pas nos `skh`/`ult` | élevé | Chevauchement direct avec Japon, BIC, Sakhalin/Ezo et diplomatie. |
| `common/history/states` | `00_states.txt` modifié | élevé | Fichier central, risque de casser ownership/provinces locales. |
| `common/history/buildings` | 13 fichiers régionaux modifiés | conflit probable | Chevauche ADMIN, shipyards, naval administration et ports. |
| `common/history/military_formations` | 8 fichiers régionaux modifiés | conflit probable | Chevauche NAVY-1/2/3 et corrections formations 1.13. |
| `common/journal_entries` | très grand nombre de fichiers modifiés ; hotfix ajoute Oregon, Treaty of London, Ryukyu Rivalry, Hokkaido, Iwakura, Zaibatsu, etc. | élevé | Beaucoup de contenu DLC, mais très dépendant des events/on_actions/localization. |
| `common/on_actions` | `00_code_on_actions.txt` modifié ; hotfix ne contient pas `phase1_japan_tenpo_on_actions.txt` | élevé | Import naïf ferait perdre le déclenchement local Tenpo/Sakoku. |
| `common/laws` | `00_inject_laws.txt` modifié de façon structurelle | élevé | Fork contient `law_merchant_republic`; hotfix contient Merchant Banking / Navigation Acts. Fusion manuelle obligatoire. |
| `common/technology` | pas de différence notable dans l'extrait brut par domaine | faible | À revérifier en phase d'import si des lois dépendent de techs. |
| `events` | nombreux fichiers vanilla/DLC modifiés ; hotfix ajoute plusieurs événements Japon DLC | élevé | Ne pas remplacer les événements Japon locaux sans comparaison ligne à ligne. |
| `localization` | anglais modifié ; nombreux fichiers français et phase_navy locaux absents du hotfix | conflit probable | Import naïf supprimerait la localisation française créée localement. |
| `map_data/state_regions` | `13_australasia.txt` modifié | conflit probable | Hotfix garde des `naval_exit_id` que notre fork a déjà corrigés. |
| `gfx/gui` | hotfix ajoute trois icônes de lois | faible | Import direct possible pour les binaires, si les lois sont fusionnées. |
| autres | country definitions, interest groups, custom localization | moyen à élevé | Les nouveaux systèmes du hotfix ont des dépendances croisées. |

## 7. Chevauchements avec nos corrections locales

| Zone | Fichier | Observation | Classement |
|---|---|---|---|
| BIC | `common/history/countries/bic - british east india company.txt` | Fork : `law_frontier_colonization`; hotfix : `law_colonial_exploitation` | garder notre version par défaut |
| Japon pays | `common/history/countries/jap - japan.txt` | Les deux touchent Sakoku ; hotfix ajoute aussi Tenpo/Ryukyu Rivalry vanilla | fusion manuelle nécessaire |
| Sakhalin/Ezo | `skh - sakhalin.txt`, `ult - ulta.txt`, EZO/JAP/RYU | Hotfix ne contient pas `skh` ni `ult` locaux | ne pas écraser |
| Sakoku JE | `common/journal_entries/07_sakoku.txt` | Fork contient tooltips/localisation phase 1.7D ; hotfix est proche mais pas identique | garder fork sauf comparaison ciblée |
| Tenpo | `events/japan_events/ep2_tenpo_events.txt`, `phase1_japan_tenpo_events.txt`, on_action local | Hotfix a le fichier DLC, mais pas les adaptations locales 1776 | fusion manuelle nécessaire |
| Australasie | `map_data/state_regions/13_australasia.txt` | Fork corrige `naval_exit_id` 3129/3110/3125/3156 ; hotfix garde 3124/3123/3126/3122 | ne pas importer hotfix tel quel |
| Administration | `common/history/buildings/*.txt` | Hotfix touche les mêmes fichiers que les corrections ADMIN | fusion manuelle nécessaire |
| Naval Europe | `common/history/military_formations/00_military_formations_europe.txt` | Chevauche NAVY-1/2 et amiraux européens | fusion manuelle nécessaire |
| Naval Inde | `common/history/military_formations/05_military_formations_india.txt` | Travancore apparaît dans les deux, mais le fork porte les décisions locales NAVY-3C | fusion manuelle ligne à ligne |
| Bâtiments Inde | `common/history/buildings/10_india.txt` | BIC/ports/chantiers/administration peuvent se chevaucher | fusion manuelle nécessaire |
| Localization navale | `localization/english/phase_navy_*.yml`, `localization/french/phase_navy_*.yml` | Fichiers locaux absents du hotfix | préserver |
| Rapports | `docs/reports/*` | Hotfix ne contient pas les rapports d'audit/migration | préserver |

## 8. Changements locaux à préserver explicitement

| Élément local | Présent dans fork ? | Présent dans hotfix ? | Risque si hotfix importé naïvement | Action recommandée |
|---|---|---|---|---|
| Série d'événements Japon Tenpo / Sakoku adaptée 1776 | oui | partiel | perte des garde-fous 1776 | préserver et fusionner manuellement |
| Fix Japon / Sakhalin / Ezo / Ryukyu | oui | partiel/non | retour de provinces grises ou tags manquants | préserver |
| `skh - sakhalin.txt` et `ult - ulta.txt` | oui | non | Sakhalin/Ezo peuvent redevenir cassés | ne pas supprimer |
| Fix Australie / Nouvelle-Zélande | oui | non ou moins avancé | régression `naval_exit_id` et impassables | garder fork |
| Fix government administration PM | oui | inconnu/partiel | retour d'erreurs PostValidate bâtiments | comparer manuellement |
| NAVY-1 / NAVY-2 / NAVY-3 | oui | partiel | perte des flottes historiques et corrections 1.13 | garder fork comme base |
| BIC avec `law_frontier_colonization` | oui | non, hotfix a `law_colonial_exploitation` | régression du choix validé localement | garder fork |
| Travancore Coastal Flotilla | oui | partiel ou identique sur extrait | risque de doublon ou suppression | vérifier ligne à ligne |
| Oman / Bahriat al-Masqat | oui | inconnu | perte NAVY-3B | préserver |
| Localisation française | oui | non | retour des clés brutes en français | préserver |
| Rapports `docs/reports` | oui | non | perte de traçabilité | préserver |

## 9. Apports nouveaux utiles du hotfix

| Apport | Utilité | Condition d'import |
|---|---|---|
| Icônes `merchant_banks.dds`, `merchant_republic.dds`, `regulation_acts.dds` | utile pour nouvelles lois | import direct possible, mais seulement avec fusion des lois/localisation |
| Lois Merchant Banking / Navigation Acts | contenu hotfix important | fusion manuelle dans `00_inject_laws.txt` |
| `ir1 - mamluk iraq.txt` et guerre Iraq/Iran/Ottomans | contenu historique utile | importer comme paquet cohérent avec country definitions, states, diplomacy et localisation |
| Ryukyu Rivalry / Hokkaido / Iwakura / Zaibatsu DLC | contenu Japon DLC utile | adapter à notre setup 1776, ne pas remplacer les fixes existants |
| Treaty of London / Oregon / Iberia JEs | contenu upstream utile | importer avec events, on_actions, localization et custom loc associés |
| Ajustements Inde/Battle for India/BOM | probablement utile | comparer à nos corrections NAVY/BIC/Inde avant import |
| Corrections British/French generals/admirals | potentiellement utile | comparer avec NAVY-1/2 pour éviter doublon |

## 10. Conflits probables

| Fichier / domaine | Type de conflit | Recommandation |
|---|---|---|
| `common/laws/00_inject_laws.txt` | structure différente entre fork et hotfix | fusion manuelle obligatoire |
| `common/history/countries/bic - british east india company.txt` | loi BIC divergente | garder fork sauf décision explicite |
| `map_data/state_regions/13_australasia.txt` | hotfix réintroduit anciens `naval_exit_id` | ne pas importer tel quel |
| `common/history/countries/jap - japan.txt` | JE Sakoku/Tenpo/Ryukyu overlap | fusion manuelle |
| `common/journal_entries/07_sakoku.txt` | définition proche mais fork contient correctifs d'affichage | garder fork comme base |
| `common/on_actions/phase1_japan_tenpo_on_actions.txt` | absent hotfix | préserver absolument |
| `events/phase1_japan_tenpo_events.txt` | absent hotfix | préserver absolument |
| `common/history/military_formations/*.txt` | NAVY local vs hotfix admiraux/flottes | fusion manuelle |
| `common/history/buildings/*.txt` | ADMIN/NAVY shipyards vs hotfix | fusion manuelle |
| `localization/french/*.yml` | hotfix ne contient pas notre traduction | ne pas supprimer |

## 11. Import direct sûr

Ces fichiers semblent importables directement uniquement parce qu'ils ne chevauchent pas les corrections locales et sont des assets isolés :

| Fichier hotfix | Pourquoi c'est relativement sûr | Remarque |
|---|---|---|
| `gfx/interface/icons/law_icons/merchant_banks.dds` | nouvel asset binaire | utile si `law_merchant_banking` est importée |
| `gfx/interface/icons/law_icons/merchant_republic.dds` | nouvel asset binaire | vérifier que le fork n'a pas déjà une icône différente |
| `gfx/interface/icons/law_icons/regulation_acts.dds` | nouvel asset binaire | utile si Navigation Acts est importée |
| `Source.txt` | information externe | faible intérêt gameplay |

Même ces imports doivent être faits dans une phase dédiée, pas pendant cet audit.

## 12. Fusion manuelle nécessaire

| Fichier / groupe | Pourquoi |
|---|---|
| `common/laws/00_inject_laws.txt` | le hotfix ajoute des lois, le fork contient déjà `law_merchant_republic` et ses contraintes |
| `common/history/countries/*.txt` | beaucoup de pays touchés, dont BIC/JAP/EZO/RYU/RUS/TUR |
| `common/history/states/00_states.txt` | fichier central d'ownership |
| `common/history/buildings/*.txt` | chevauche ADMIN et NAVY |
| `common/history/military_formations/*.txt` | chevauche toutes les corrections navales |
| `common/journal_entries/07_sakoku.txt` | ne pas perdre les tooltips corrigés |
| `common/journal_entries/07_tenpo_crisis.txt` et JEs Japon DLC | adapter au départ 1776 |
| `events/japan_events/*.txt` | les fichiers DLC doivent respecter les garde-fous locaux |
| `common/on_actions/00_code_on_actions.txt` | fusionner sans supprimer les on_actions locaux |
| `localization/english/mod_*.yml` | fusionner les nouvelles clés sans écraser les clés locales |
| `localization/french/*.yml` | traduire/compléter après import anglais |
| `map_data/state_regions/13_australasia.txt` | conserver les corrections locales de naval exits et impassables |
| `common/country_definitions/*` | hotfix semble utiliser une structure différente, à intégrer prudemment |

## 13. Changements à ne pas importer tels quels

| Changement | Pourquoi |
|---|---|
| Remplacement complet du fork par hotfix | annulerait les corrections validées 1.13 |
| `map_data/state_regions/13_australasia.txt` hotfix entier | réintroduit les anciens `naval_exit_id` australiens/NZ |
| Suppression de `skh - sakhalin.txt` et `ult - ulta.txt` | casserait les corrections Sakhalin/Ezo |
| Suppression de `phase1_japan_tenpo_on_actions.txt` | casserait la chaîne locale Tenpo |
| Suppression de `events/phase1_japan_tenpo_events.txt` | casserait la chaîne locale Tenpo/Sakoku |
| Suppression des fichiers `localization/french/*.yml` | ferait revenir des clés brutes en jeu français |
| Suppression des fichiers `localization/*/phase_navy_*.yml` | casserait les noms/localisations des flottes et amiraux locaux |
| Remplacement brut de `bic - british east india company.txt` | repasserait BIC de `law_frontier_colonization` à `law_colonial_exploitation` |
| Remplacement brut de `07_sakoku.txt` | risque de régression sur l'affichage corrigé des conditions |
| Remplacement brut des formations militaires | risque de perdre NAVY-1/2/3 et d'introduire des doublons |

## 14. Plan de merge recommandé

Étape 1 :
Créer une branche dédiée d'import hotfix et conserver `hotfix-dlc-audit` comme point de référence.

Étape 2 :
Importer uniquement les assets graphiques isolés des nouvelles lois, puis vérifier que le jeu ignore correctement les assets non référencés.

Étape 3 :
Fusionner `common/laws/00_inject_laws.txt` manuellement pour intégrer Merchant Banking / Navigation Acts sans écraser `law_merchant_republic`.

Étape 4 :
Importer le bloc Iraq/Iran/Ottomans comme paquet complet seulement après avoir listé tous les fichiers dépendants : pays, country definitions, states, diplomacy, localization, events.

Étape 5 :
Traiter Japon en phase séparée : comparer `jap`, `ezo`, `ryu`, `07_sakoku`, `07_tenpo_crisis`, `ep2_*` et on_actions. Garder le fork comme base.

Étape 6 :
Traiter Inde/BIC en phase séparée : comparer Battle For India, BIC, BOM, Hyderabad, Travancore, formations et bâtiments. Ne pas réintroduire `law_colonial_exploitation` pour BIC sans décision explicite.

Étape 7 :
Traiter formations militaires Europe/Monde en petites séries, avec test de lancement entre chaque série.

Étape 8 :
Traiter `map_data/state_regions/13_australasia.txt` uniquement par patch manuel ciblé, en conservant les `naval_exit_id` locaux corrigés.

Étape 9 :
Mettre à jour localisation anglaise puis française, en évitant de supprimer les fichiers `phase_*` locaux.

Étape 10 :
Tester en jeu : menu, sélection pays, lancement Japon/GBR/BIC/RUS/TUR/Australie, passage du premier mois, puis scan `error.log`.

## 15. Commandes utiles pour la phase suivante

Commandes de base :

```powershell
git status --short
git diff --name-only
git diff --check
```

Comparer un fichier précis :

```powershell
$Fork = "C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork"
$Hotfix = "C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source"
git diff --no-index -- "$Fork\common\laws\00_inject_laws.txt" "$Hotfix\common\laws\00_inject_laws.txt"
```

Chercher les IDs sensibles :

```powershell
Select-String -Path "$Fork\common\**\*.txt" -Pattern "law_colonial_exploitation|law_frontier_colonization|je_sakoku|je_tenpo_crisis|building_naval_administration|ship_type_frigate|naval_exit_id"
```

Comparer Japon :

```powershell
git diff --no-index -- "$Fork\common\history\countries\jap - japan.txt" "$Hotfix\common\history\countries\jap - japan.txt"
git diff --no-index -- "$Fork\common\journal_entries\07_sakoku.txt" "$Hotfix\common\journal_entries\07_sakoku.txt"
```

Comparer Australasie :

```powershell
git diff --no-index -- "$Fork\map_data\state_regions\13_australasia.txt" "$Hotfix\map_data\state_regions\13_australasia.txt"
Select-String -Path "$Fork\map_data\state_regions\13_australasia.txt" -Pattern "STATE_QUEENSLAND|STATE_WESTERN_AUSTRALIA|STATE_NORTHERN_TERRITORY|STATE_SOUTH_ISLAND|naval_exit_id"
```

Comparer BIC :

```powershell
git diff --no-index -- "$Fork\common\history\countries\bic - british east india company.txt" "$Hotfix\common\history\countries\bic - british east india company.txt"
Select-String -Path "$Fork\common\history\countries\bic - british east india company.txt","$Hotfix\common\history\countries\bic - british east india company.txt" -Pattern "law_colonial_exploitation|law_frontier_colonization"
```

## 16. Risques

- Import global du hotfix : risque élevé de régression sur les corrections validées en jeu.
- Import Japon non ciblé : risque de casser Sakoku/Tenpo/Ryukyu ou de faire réapparaître des conditions mal localisées.
- Import Australasie non ciblé : risque de réintroduire les `naval_exit_id` obsolètes et des zones infranchissables.
- Import BIC non ciblé : risque de perdre le choix `law_frontier_colonization`.
- Import formations militaires non ciblé : risque de doublons de flottes/amiral ou de perdre NAVY-1/2/3.
- Import localisation non ciblé : risque de supprimer la localisation française et les clés navales locales.
- Import country definitions non ciblé : risque de supprimer des tags locaux nécessaires comme SKH/ULT.

## 17. Fichiers créés par l'audit

| Fichier | Rôle |
|---|---|
| `docs/reports/hotfix/HOTFIX_DLC_RAW_NAME_STATUS.txt` | sortie brute `git diff --no-index --name-status` |
| `docs/reports/hotfix/HOTFIX_DLC_UPSTREAM_CHANGE_AUDIT.md` | rapport d'analyse et plan de merge recommandé |

## 18. Confirmation

Aucun fichier gameplay n'a été modifié pendant cet audit.

Aucun fichier `common/`, `events/`, `localization/`, `map_data/`, `gfx/`, `gui/` ou `docs/research/` n'a été modifié dans le fork.

Le stash MARATH `WIP NAVY-3C-3 Maratha Konkan Flotilla` n'a pas été appliqué, restauré, fusionné ou analysé comme partie du fork courant.
