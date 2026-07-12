# HOTFIX-5C1-AUDIT - Anciennes strategic regions indiennes

## 1. Resume executif

L'audit runtime de `common/` et `events/`, commentaires exclus, trouve **515 references** aux cinq strategic regions indiennes invalides. Le total historique avant HOTFIX-5A et HOTFIX-5B2 etait de 582 : la baisse exacte est donc de 67.

Les 515 occurrences sont reparties dans 23 fichiers et 101 blocs semantiques coherents dans la carte CSV. Elles ne doivent pas recevoir un remplacement global :

- 126 occurrences correspondent clairement a l'union nord/sud ;
- 244 doivent utiliser une geographic region vanilla, souvent `geographic_region_india` ou une subdivision `*_old` ;
- 58 demandent des state regions explicites ;
- 34 ont une cible directe nord ou sud, dont 26 occurrences de HQ/formation ;
- 13 exigent encore une recherche manuelle ;
- 40 appartiennent aux dix boutons coloniaux legacy detaches en HOTFIX-5B2 et doivent rester preserves temporairement.

Priorite recommandee : corriger d'abord les JE/events a forte confiance dans HOTFIX-5C2, puis les subdivisions geographiques dans HOTFIX-5C3. Les HQ sont isoles en HOTFIX-5C4. Durrani reste reserve a HOTFIX-5D et les boutons legacy a une decision ulterieure.

## 2. Etat Git et stash

| Element | Resultat |
|---|---|
| Branche | `hotfix-dlc-audit` |
| Working tree initial | Propre |
| HEAD initial | `fc9805f Unify East India Company workflow` |
| HOTFIX-5B2 | Commit present |
| Stash | `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` |
| Action sur le stash | Aucune |

Le stash MARATH n'a ete ni applique, ni inspecte comme contenu courant, ni restaure, ni supprime, ni modifie.

## 3. Definitions vanilla

Reference : `C:\Games\Victoria 3 The Great Wave\game\common\strategic_regions\west_south_asia_strategic_regions.txt`.

| Strategic region | Definie ? | State regions principales | Usage recommande |
|---|---|---|---|
| `region_north_india` | Oui, ligne 43 | Gujarat, Sindh, Central Provinces, Awadh, Malwa, Agra, Bundelkhand, Bihar, East/West Bengal, Assam, Orissa, Punjab, Hill Punjab, Delhi, Rajputana | HQ et mecanismes couvrant le nord indien |
| `region_south_india` | Oui, ligne 29 | Ceylon, Circars, Mysore, Travancore, Madras, Hyderabad, Kurnool, Bombay | HQ et mecanismes couvrant le sud indien |
| `region_bengal` | Non | Sans objet | Ne jamais utiliser comme strategic region |
| `region_bombay` | Non | Sans objet | Ne jamais utiliser comme strategic region |
| `region_central_india` | Non | Sans objet | Ne jamais utiliser comme strategic region |
| `region_madras` | Non | Sans objet | Ne jamais utiliser comme strategic region |
| `region_punjab` | Non | Sans objet | Ne jamais utiliser comme strategic region |

La vanilla fournit aussi des geographic regions utiles :

- `geographic_region_india` = nord + sud + Quetta, Pashtunistan, Kashmir et Baluchistan ;
- `geographic_region_madras_old` = Ceylon, Circars, Mysore, Travancore, Madras, Hyderabad, Kurnool ;
- `geographic_region_bengal_old` = Bihar, East/West Bengal, Assam, Orissa ;
- `geographic_region_bombay_old` = Bombay, Gujarat, Sindh, Baluchistan ;
- `geographic_region_punjab_old` = Punjab, Hill Punjab, Delhi, Rajputana ;
- `geographic_region_central_india_old` = Central Provinces, Awadh, Malwa, Agra, Bundelkhand.

Ces subdivisions expliquent pourquoi un remplacement systematique par nord/sud serait parfois incorrect.

## 4. Total historique

Avant HOTFIX-5A et HOTFIX-5B2 :

| ID | Total historique |
|---|---:|
| `region_madras` | 107 |
| `region_bombay` | 139 |
| `region_bengal` | 98 |
| `region_central_india` | 104 |
| `region_punjab` | 134 |
| **Total** | **582** |

## 5. Nouveau total courant

Le recomptage lit tous les fichiers de `common/` et `events/`, retire la partie de ligne suivant `#`, puis compte les identifiants exacts. La localisation, `docs/`, Git et les fichiers temporaires sont exclus.

**Total courant : 515 occurrences runtime.**

## 6. Difference expliquee

| Phase | Reduction | Detail |
|---|---:|---|
| HOTFIX-5A | 2 | Une occurrence Bombay et une occurrence Madras retirees du setup BIC/Ryotwari |
| HOTFIX-5B2 - JE | 5 | Les cinq marqueurs invalides remplaces dans `06_new_imperialism.txt` |
| HOTFIX-5B2 - creation EIC | 30 | Six OR de cinq IDs remplaces dans le bouton actif |
| HOTFIX-5B2 - expansion dynamique | 15 | Trois OR de cinq IDs remplaces |
| HOTFIX-5B2 - expansion BIC | 15 | Un OR de cinq et cinq transferts de deux references chacun remplaces |
| **Total retire** | **67** | `582 - 67 = 515` |

Par identifiant, Bombay et Madras baissent de 14 chacun (13 en 5B2 plus un en 5A) ; Bengal, Central India et Punjab baissent de 13 chacun.

## 7. Comptage par identifiant

| Identifiant | Historique | Courant | Difference |
|---|---:|---:|---:|
| `region_bengal` | 98 | 85 | -13 |
| `region_bombay` | 139 | 125 | -14 |
| `region_central_india` | 104 | 91 | -13 |
| `region_madras` | 107 | 93 | -14 |
| `region_punjab` | 134 | 121 | -13 |
| **Total** | **582** | **515** | **-67** |

## 8. Comptage par dossier et type

| Domaine | Occurrences |
|---|---:|
| `events/india_events` | 187 |
| `common/journal_entries` | 125 |
| `common/ai_strategies` | 43 |
| `common/history` | 41 |
| `common/scripted_buttons` | 40 |
| `events/soi_events` | 36 |
| `common/company_types` | 25 |
| `common/dynamic_country_names` | 10 |
| `events/krakatoa_events.txt` | 6 |
| `common/character_templates` | 2 |
| **Total** | **515** |

Les deux racines donnent 286 occurrences dans `common/` et 229 dans `events/`.

Fichiers les plus charges :

| Fichier | Occurrences |
|---|---:|
| `events/india_events/sepoy_mutiny_events.txt` | 132 |
| `common/journal_entries/04_indian_famines.txt` | 60 |
| `common/ai_strategies/00_default_strategy.txt` | 43 |
| `common/journal_entries/03_afghanistan.txt` | 40 |
| `common/scripted_buttons/00_new_colonial_admins.txt` | 40 |
| `events/india_events/indian_famines.txt` | 40 |
| `common/company_types/02_new_companies.txt` | 25 |
| `common/history/military_formations/05_military_formations_india.txt` | 23 |
| `events/soi_events/00_ep1_kazakh_events.txt` | 20 |
| `events/soi_events/00_ep1_afghanistan_events.txt` | 16 |

Les treize autres fichiers portent ensemble 76 occurrences et sont tous enumeres dans le CSV.

## 9. Classification active et dormante

| Classification | Blocs | Occurrences | Priorite |
|---|---:|---:|---|
| `ACTIVE_RUNTIME` | 63 | 273 | Haute |
| `ACTIVE_BUT_DLC_GATED` | 26 | 196 | Haute si DLC actif |
| `ACTIVE_BUT_DATE_GATED` | 2 | 6 | Moyenne ; Krakatoa apres 1850 |
| `LEGACY_DORMANT_5B2` | 10 | 40 | Ne pas corriger immediatement |
| **Total** | **101** | **515** | |

Aucune occurrence `COMMENT_ONLY` n'entre dans le total. Aucun bloc n'a ete classe `DISABLED_ALWAYS_NO` comme classification principale : les cinq boutons de creation explicitement masques appartiennent avant tout au groupe `LEGACY_DORMANT_5B2` demande par la phase.

## 10. Fichiers deja corriges

Les controles donnent zero ancien ID dans :

- `common/history/countries/bic - british east india company.txt` ;
- `common/journal_entries/06_new_imperialism.txt` ;
- les trois blocs actifs `east_india_company`, `expand_east_india` et `expand_for_bic`.

Les 40 occurrences restantes dans `00_new_colonial_admins.txt` sont toutes dans les dix definitions legacy sans caller. Aucune n'appartient aux trois blocs HOTFIX-5B2.

## 11. Journal entries et events

| Chaine | Entry point/garde | Occurrences | Role | Cible |
|---|---|---:|---|---|
| Consolidate British India | Objectif Great Game | 4 | Territoires objectifs Inde/Birmanie | Nord/sud pour l'immediate ; states explicites pour la completion |
| Consolidate Afghanistan | `ep1_content` | 40 | Frontiere et transferts de traite | `geographic_region_india` |
| India Railway | `ip2_content` + technologie `railways` | 10 JE/event | Possessions et selection de states | Nord + sud |
| Indian Famines | `ip2_content` | 100 JE/events | Famine panindienne et sous-regions historiques | Geographic India pour le large ; `*_old` pour les branches regionales |
| Uneasy Raj / Sepoy Mutiny | JE BIC et events associes | 142 JE/events | Stabilite des presidencies, revolte, propagation, breakup | Nord/sud, geographic India et states explicites selon le bloc |
| Hindu-German Conspiracy | `ip2_content` | 10 | Interets ennemis en Inde | Nord + sud |
| Krakatoa | `game_date >= 1850.1.1` | 6 | Effets cotiers par anciennes presidencies | Geographic regions `*_old` |
| Afghanistan border events | Chaine `ep1` | 16 | Cote indien des transferts frontaliers | `geographic_region_india` |
| Russian Central Asia | Chaine `ep1` | 20 | Detection de puissances presentes en Inde | `geographic_region_india` |
| Hindustan is Durrani | JE mod active | 6 | Controle territorial/failure | Reserve HOTFIX-5D |

Risque 1776 : les chaines simplement DLC-gated peuvent etre chargees des le debut si leurs autres prerequis sont satisfaits. Sepoy Mutiny ne porte pas de garde DLC directe dans la JE examinee et doit donc etre consideree runtime. Les contenus Home Rule, Nationalism, Non-Cooperation et Federation existent ailleurs mais ne contiennent aucun des cinq anciens IDs ; ils ne sont pas inclus artificiellement dans cet audit.

## 12. Formations militaires

| Pays/formation | Type | HQ fork | Hotfix | Cible audit | Conflit |
|---|---|---|---|---|---|
| GBR `Army_of_India` | Armee | Madras invalide | Nord | Nord, confiance moyenne | Recherche manuelle |
| DUR, deux armees Baluchistan | Armees | Bombay invalide | Sud | Recherche manuelle : Baluchistan est hors nord/sud | HOTFIX-5D |
| PAN, trois Fauji + Alexander Gardner | Armees/general | Punjab invalide | Nord | Nord | Aucun |
| BIC `Bengal_Army` | Armee | Bengal invalide | Nord | Nord | BIC preserve |
| HYD `sarf_e_khas` | Armee | Madras invalide | Sud | Sud | Aucun |
| AWA `OudhRoyalArmy` | Armee | Central India invalide | Nord | Nord | Aucun |
| MARATH | Armee | Central India invalide | Nord | Nord probable | `STASH_MARATH` : interdit |
| GWA `GwaliorArmy` | Armee | Central India invalide | Nord | Nord | Aucun |
| NAG `NagpurArmy` | Armee | Central India invalide | Nord | Nord | Aucun |
| MYS `MysoreArmy` | Armee | Madras invalide | Sud | Sud | Aucun |
| COO/GAR | Armees | Bengal/Punjab invalides | Nord | Nord | Aucun |
| SAT/KHP | Armees | Bombay invalide | Sud | Sud | Aucun |
| KNO/PUD/JEY/COC | Armees | Madras invalide | Sud | Sud | Aucun |
| BHV `BhavnagarArmy` | Armee | Bombay invalide | Sud dans hotfix | **Nord** selon Gujarat vanilla | Recherche manuelle |
| TRA `TravancoreArmy` | Armee | Madras invalide | Sud | Sud, HQ seulement | `TRAVANCORE_PRESERVE` |
| SIN `SindhArmy` | Armee | Bombay invalide | Sud dans hotfix | **Nord** selon Sindh vanilla | Recherche manuelle |
| MUG `MughalArmy` | Armee | Punjab invalide | Nord | Nord | Aucun |
| BIC John Wood/Charles Malcolm | Amiraux | Bombay invalide | Inchanger | Sud | `NAVY` |

Le hotfix n'est pas fiable seul pour BHV et SIN : la composition vanilla place Gujarat et Sindh dans `region_north_india`, alors que le hotfix leur donne un HQ sud. HOTFIX-5C4 doit suivre les state regions vanilla et ne modifier que les lignes HQ approuvees. Taille, unites, commandants et flottes restent hors scope.

## 13. Boutons coloniaux legacy

| Bouton | Occurrences | Caller actuel | Variable/etat | Decision |
|---|---:|---|---|---|
| Creation Central India, Madras, Bengal, Bombay, Punjab | 25 | Aucun | Cinq references chacun ; `visible = always = no` | `LEGACY_DORMANT_5B2`, conserver |
| Expansion Bengal, Bombay, Punjab, Madras, Central India | 15 | Aucun | Trois references chacun ; variables de sujets legacy | `LEGACY_DORMANT_5B2`, conserver |

La recherche globale de chaque ID de bouton hors de son fichier de definition retourne zero caller. La compatibilite d'anciennes sauvegardes reste toutefois une raison suffisante pour ne pas supprimer ces blocs dans HOTFIX-5C2.

## 14. Comparaison fork, hotfix et vanilla

| Domaine | Fork | Hotfix | Vanilla | Conclusion |
|---|---|---|---|---|
| Company type DEI | Cinq strategic regions invalides | Nord + sud | IDs nord/sud valides | Suivre le hotfix par hunks |
| Global BIC/princely states | Cinq invalides + Himalaya/Birmanie | Nord + sud + contexte conserve | Nord/sud valides | Suivre le hunk, conserver les siblings |
| Dynamic country names | Strategic regions de presidencies | Geographic regions `*_old` | `*_old` definies | Suivre le hotfix |
| India Railway | Cinq invalides | Geographic India + nord/sud | APIs valides | Suivre les hunks pertinents |
| Famines | Strategic regions larges et regionales confondues | Geographic India, nord/sud et `*_old` | Toutes ces APIs existent | Copier l'intention bloc par bloc, jamais le fichier entier |
| Sepoy chain | Cinq invalides repetes | Nord/sud + frontier states + states explicites | APIs valides | Fusion manuelle necessaire |
| Afghanistan/SoI | Punjab/Bombay invalides | Geographic India et Balkh explicite | Geographic India valide | Hunk cible a haute confiance |
| HQ indiens | Anciens HQ | Majoritairement nord/sud | Membership state regions normative | Corriger par formation ; ne pas suivre BHV/SIN aveuglement |
| Interests | Anciens IDs | Hotfix encore invalide | Nord/sud valides | Correction locale necessaire |
| AI strategy | 43 anciens IDs | Fichier hotfix absent | Geographic APIs valides | Recherche manuelle avant edition |

Aucun fichier global ne doit etre remplace integralement.

## 15. Cartographie geographique proposee

| Cible CSV | Blocs | Occurrences | Usage |
|---|---:|---:|---|
| `geographic_region_required` | 32 | 244 | Inde large ou subdivisions historiques |
| `north_and_south` | 23 | 126 | Mecanismes panindiens bases sur strategic regions |
| `explicit_state_region` | 5 | 58 | Presidencies/objectifs dont la precision doit etre preservee |
| `preserve_legacy_temporarily` | 10 | 40 | Boutons HOTFIX-5B2 detaches |
| `region_north_india` | 15 | 21 | HQ et blocs clairement nordiques |
| `region_south_india` | 11 | 13 | HQ et blocs clairement meridionaux |
| `manual_research_required` | 5 | 13 | Frontieres IA/Durrani ambiguës |

## 16. Conflits proteges

| Conflit | Constat | Regle |
|---|---|---|
| BIC | 220 occurrences classees BIC dans le CSV, surtout Sepoy et setup colonial | Preserver `law_frontier_colonization`, HOTFIX-5A/5B2 et les chemins de compagnie unique |
| NAVY | Deux HQ d'amiraux BIC | Reporter a une phase NAVY ; aucun changement ici |
| ADMIN | Aucun fichier buildings/PM dans les 23 fichiers concernes | Ne pas introduire de PM ou changement administratif pendant les corrections |
| STASH_MARATH | Une occurrence HQ dans le bloc MARATH | Ne pas modifier ce bloc et ne pas appliquer le stash |
| Travancore | Une occurrence dans `TravancoreArmy`; la flotte voisine a deja un HQ sud valide | Hunk HQ armee seulement ; preserver flotte, administration et `STATE_TRAVANCORE` |
| Durrani | Dix occurrences : interests 2, armees 2, JE 6 | Reserver a HOTFIX-5D |

## 17. Cas Durrani reserve

Les dix occurrences Durrani sont volontairement exclues des lots generiques :

- `common/history/interests/00_interests.txt`, bloc `c:DUR` : 2 ;
- `common/history/military_formations/04_military_formations_middle_east.txt`, deux armees : 2 ;
- `common/journal_entries/07_hindustan_is_durrani_mod.txt` : 6.

Le hotfix propose nord/sud pour la JE et sud pour les deux armees, mais Baluchistan appartient a `region_greater_persia` dans la vanilla. HOTFIX-5D doit donc examiner ensemble objectif territorial, interests et HQ au lieu d'importer ces hunks separement.

## 18. References a haute confiance

Le CSV classe 79 blocs et 371 occurrences en confiance `HIGH`. Les principaux groupes sont :

- company type DEI vers nord/sud ;
- setup global BIC et interests GBR/BIC vers nord/sud ;
- Afghanistan et Central Asia vers `geographic_region_india` ;
- broad checks India Railway, famines et Sepoy vers nord/sud/geographic India ;
- Krakatoa et noms dynamiques vers les geographic regions `*_old` ;
- la plupart des HQ, determines par la state region de leurs unites.

## 19. References necessitant une recherche

Le CSV classe 18 blocs/136 occurrences en confiance moyenne et 4 blocs/8 occurrences en confiance basse. Les points principaux :

- les 43 references AI strategy, sans version hotfix equivalente ;
- les branches de presidencies dans Famines et Sepoy, qui doivent conserver une precision inferieure a une strategic region ;
- la completion de l'objectif British India, qui inclut la Birmanie ;
- les targets Persia/India et les HQ Durrani ;
- GBR `Army_of_India`, a verifier selon ses units/states ;
- les divergences hotfix BHV et SIN, pour lesquelles la vanilla indique le nord.

## 20. Plan ferme des phases suivantes

### HOTFIX-5C2 - Corrections a forte confiance

Fichiers autorises par hunks seulement :

- `common/company_types/02_new_companies.txt` ;
- `common/history/global/00_global.txt` ;
- `common/history/interests/00_interests.txt`, blocs GBR/BIC uniquement ;
- `common/journal_entries/00_player_objectives_great_game.txt`, immediate uniquement ;
- `common/journal_entries/03_afghanistan.txt` ;
- `common/journal_entries/04_india_railway.txt` ;
- `common/journal_entries/04_indian_famines.txt`, seulement les broad checks identifies CSV 5C2 ;
- `common/journal_entries/04_sepoy_mutiny.txt`, hidden trigger uniquement ;
- `events/india_events/india_misc_events.txt` ;
- `events/india_events/india_railway.txt` ;
- `events/india_events/indian_famines.txt` ;
- `events/india_events/sepoy_mutiny_events.txt`, seulement les blocs 5C2 ;
- `events/krakatoa_events.txt` ;
- `events/soi_events/00_ep1_afghanistan_events.txt` ;
- `events/soi_events/00_ep1_kazakh_events.txt`.

Interdits : Durrani, formations, AI strategy, dynamic names, boutons legacy, laws, buildings, PM et stash MARATH. Tests : validation syntaxique, recomptage par bloc, DLC IP2/EP1, BIC/Sepoy, famine et railway.

### HOTFIX-5C3 - Precision geographique

Fichiers/objets fermes :

- `common/ai_strategies/00_default_strategy.txt`, huit groupes CSV ;
- `common/dynamic_country_names/00_dynamic_country_names.txt`, quatre noms ;
- `common/journal_entries/00_player_objectives_great_game.txt`, completion de British India ;
- `common/journal_entries/04_indian_famines.txt`, branches de subdivisions ;
- `common/journal_entries/04_sepoy_mutiny.txt`, initialisation des cinq presidency bars ;
- `events/india_events/sepoy_mutiny_events.txt`, branches `explicit_state_region` et `*_old` uniquement.

Cibles : geographic regions vanilla et listes explicites de state regions. Interdits : remplacement integral, Durrani, formations, laws et boutons legacy. Tests : chaque presidency, tooltip, progress bar, dynamic country name et comportement IA observe.

### HOTFIX-5C4 - HQ non conflictuels

Fichiers autorises :

- `common/history/military_formations/00_military_formations_europe.txt`, `Army_of_India` apres verification ;
- `common/history/military_formations/05_military_formations_india.txt`, lignes HQ approuvees seulement.

Exclusions obligatoires : bloc MARATH, flotte Travancore, tailles, unites, commandants, `country_bic.txt`, DUR et toute modification NAVY. BHV/SIN doivent suivre le membership vanilla nord, sous reserve d'un controle final. Tests : PostValidate formations, HQ de chaque pays, Travancore intact.

### HOTFIX-5D - Durrani/Hindustan

Fichiers a auditer ensemble :

- `common/history/interests/00_interests.txt`, `c:DUR` ;
- `common/history/military_formations/04_military_formations_middle_east.txt`, deux armees DUR ;
- `common/journal_entries/07_hindustan_is_durrani_mod.txt`.

Aucune decision avant analyse de Baluchistan, de l'objectif Hindustan et des frontieres 1776.

### HOTFIX-5C-LEGACY

Fichier unique : `common/scripted_buttons/00_new_colonial_admins.txt`. Ne rien supprimer immediatement. Decider d'abord si la compatibilite des sauvegardes et d'eventuels callers externes doit etre maintenue.

### HOTFIX-5C-VALIDATION

Aucun changement gameplay. Recompter les cinq IDs dans `common/` et `events/`, verifier chaque lot contre le CSV, lancer avec/sans DLC, puis surveiller `error.log` et `game.log`. Le stash MARATH reste non applique pendant tout HOTFIX-5.

## 21. Tests recommandes

1. Recompter apres chaque lot, commentaires exclus, et comparer au sous-total CSV du lot.
2. Rechercher les cinq IDs dans les seuls objets corriges, pas exiger zero global tant que legacy/Durrani/HQ subsistent.
3. Lancer sans DLC puis avec IP2 et EP1.
4. Tester BIC : Uneasy Raj, Sepoy Mutiny, Railway, Famines et consolidation British India.
5. Tester Afghanistan/Great Game et les transferts de frontiere.
6. Tester Krakatoa apres 1850 via console/date si necessaire.
7. Pour chaque HQ, verifier la creation de la formation et l'absence de PostValidate.
8. Confirmer que MARATH et Travancore restent inchanges.
9. Surveiller les patterns `region_bengal`, `region_bombay`, `region_central_india`, `region_madras`, `region_punjab`, `Invalid strategic region`, `PostValidate`, `create_military_formation` et erreurs de scope.

## 22. Fichiers crees

- `docs/reports/hotfix/HOTFIX_5C1_AUDIT_INDIA_REGION_REFERENCES.md` ;
- `docs/reports/hotfix/HOTFIX_5C1_INDIA_REGION_REFERENCE_MAP.csv`.

Le CSV est en UTF-8 avec BOM, contient les 16 en-tetes imposes, 101 lignes de blocs et un total agrege exact de 515 occurrences.

## 23. Confirmation gameplay

Aucun fichier gameplay, localisation, hotfix ou vanilla n'a ete modifie ou copie. Aucun remplacement, merge ou commit n'a ete effectue. Seuls les deux rapports HOTFIX-5C1 ont ete crees.

## 24. Confirmation stash MARATH

Le stash `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` est reste present et intact. Aucune commande `git stash pop`, `apply`, `drop` ou equivalente n'a ete executee.
