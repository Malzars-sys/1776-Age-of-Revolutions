# HOTFIX-3-AUDIT - Iraq / Iran / Ottomans

## 1. Resume executif

Le hotfix upstream contient un bloc Iraq/Iran/Ottomans coherent mais non isolable en un seul fichier.

Le coeur du changement est l'ajout du tag `IR1` pour `Mamluk Iraq`, utilise comme protectorat ottoman et proprietaire de plusieurs states actuellement ottomans dans le fork :

- `STATE_BASRA`
- `STATE_BAGHDAD`
- `STATE_MOSUL`
- `STATE_DEIR_EZ_ZOR`

Le bloc depend aussi de :

- definition pays `IR1` ;
- blason et drapeau `IR1` ;
- gouvernement `gov_pashalik` ;
- historique pays `ir1 - mamluk iraq.txt` ;
- personnage dirigeant IR1 ;
- relations de sujet TUR -> IR1 ;
- states / ownership / claims ;
- pops et batiments `region_state:IR1` ;
- formation militaire IR1 ;
- diplomatic play `00_otto_iraqi_persia_war.txt` ;
- localisation anglaise `IR1`, `IR1_ADJ`, `gov_pashalik`.

Conclusion : import futur possible, mais uniquement en fusion manuelle par paquet. Ne pas importer `00_states.txt`, `08_middle_east.txt`, `08_middle_east pops` ou `04_military_formations_middle_east.txt` en entier.

## 2. Etat Git initial

| Element | Valeur |
|---|---|
| Branche | `hotfix-dlc-audit` |
| `git status --short` initial | propre |
| Derniers commits | `d43e4f2 Import hotfix merchant laws`; `eca384e Import hotfix law icons`; `fc88ab8 Audit upstream DLC hotfix`; `319df22 Set BIC to frontier colonization`; `2dedf0b Document BIC naval decision` |
| Stash detecte | `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` |
| Action sur stash | aucune |

Le stash MARATH n'a pas ete applique, restaure, inspecte ou modifie.

## 3. Changelog hotfix lie au bloc Iraq/Iran/Ottomans

Lignes pertinentes extraites de `Changelog.txt` du hotfix :

| Ligne | Contenu |
|---|---|
| 7 | `Iraq is now ruled by a Mamluk Governor and who starts at war with Iran` |
| 9 | `Iran is now at war with Ottomans` |
| 79 | `For Persia's Agha Mohammed Qajar his ideology was changed from 'modernizer' to 'modernizer leader'...` |
| 81 | `Qajar ascending to Persian Throne gives Azerbaijani Primary Culture to Persia` |
| 103 | `Durrani Empire, Crimean Khanate, Ottoman Empire now uses 'Subjecthood' Law` |
| 113 | `Persia Deputy of the People Journal Entry...` |
| 127 | `Changed Persia's select country screen flavour text` |
| 134 | `Dutch East Indies Iranian Trade Privilege Deal (Historical)` |
| 136 | `Crimean Khanate removed as Ottoman Subject (Ottomans lost it in 1774)` |
| 138 | `Improved Great Britain relations with Persia (historical)` |
| 146 | `Added ability to make colonial administrations in Persia and Indonesia` |
| 169 | `Leader of Persia added` |
| 170 | `Persia name changed to 'Sublime Zand'` |

Les fichiers Iran/Persia de journal entries et events semblent deja presents dans le fork et dans le hotfix ; l'audit HOTFIX-3 se concentre donc surtout sur le paquet nouveau `IR1` et la guerre associee.

## 4. Fichiers candidats trouves

| Fichier hotfix | Domaine | Termes trouves | Role probable | A comparer ? |
|---|---|---|---|---|
| `common/country_definitions/02_modded_countries.txt` | country definitions | `IR1`, `Mamluk Iraq` | definition du tag IR1 | oui |
| `common/coat_of_arms/coat_of_arms/03_new.txt` | gfx/script drapeau | `IR1` | blason IR1 | oui |
| `common/flag_definitions/07_NM_Flags.txt` | flags | `IR1`, `coa = IR1` | definition drapeau IR1 | oui |
| `common/government_types/00_mod_gov_types.txt` | gouvernement | `gov_pashalik`, `IR1`, `TUR` | gouvernement special Mamluk Iraq | oui |
| `common/history/countries/ir1 - mamluk iraq.txt` | history country | `c:IR1` | lois, tech, taxes, IG de depart | oui |
| `common/history/characters/ir1 - mamluk iraq.txt` | characters | `c:IR1`, ruler | dirigeant Omar Ahmad | oui |
| `common/history/ai/00_secret_goals.txt` | AI history | `c:IR1`, `c:TUR`, `defy` | objectif IA IR1 contre TUR | oui |
| `common/history/diplomacy/00_subject_relationships.txt` | diplomacy | `c:TUR`, `c:IR1`, `protectorate` | IR1 sujet ottoman | oui |
| `common/history/diplomatic_plays/00_otto_iraqi_persia_war.txt` | diplomatic plays | `PER`, `IR1`, `ARB`, `OMA` | guerre / diplomatic play regional | oui |
| `common/history/states/00_states.txt` | states | `c:IR1`, `STATE_BASRA`, `STATE_BAGHDAD`, `STATE_MOSUL`, `STATE_DEIR_EZ_ZOR` | ownership/claims | oui |
| `common/history/buildings/08_middle_east.txt` | buildings | `region_state:IR1`, `country="c:IR1"` | batiments de depart IR1 | oui |
| `common/history/pops/08_middle_east.txt` | pops | `region_state:IR1` | pops de depart IR1 | oui |
| `common/history/military_formations/04_military_formations_middle_east.txt` | military formations | `c:IR1`, `mamluk_army`, `mamluk_gen` | armee IR1 et general | oui |
| `localization/english/mod_v2content_l_english.yml` | localisation EN | `IR1`, `IR1_ADJ`, `gov_pashalik` | noms pays/gouvernement | oui |

## 5. Tags exacts fork / hotfix / vanilla

| Entite historique | Tag fork | Tag hotfix | Tag vanilla | Fichiers associes | Commentaire |
|---|---|---|---|---|---|
| Iraq vanilla | `IRQ` defini dans `common/country_definitions/00_countries.txt` | `IRQ` existe aussi comme tag vanilla general | `IRQ` | country definitions / flags vanilla | Non utilise pour le bloc hotfix. |
| Mamluk Iraq | absent | `IR1` | absent | `02_modded_countries.txt`, history country, characters, states, pops, buildings, formations, diplomacy, loc | Nouveau tag hotfix. |
| Persia / Iran | `PER` | `PER` | `PER` | `per - persia.txt`, `per - persia.txt` characters, Iran events/JEs | Pas de tag `IRN` trouve comme tag principal. |
| Ottomans | `TUR` | `TUR` | `TUR` | `tur - ottoman empire.txt`, diplomacy, states, formations | Hotfix retire des territoires a TUR pour IR1. |

Verification importante : `IR1` n'existe pas dans le fork ni dans vanilla The Great Wave. Il doit etre importe comme nouveau tag complet si ce bloc est repris.

## 6. Comparaison des fichiers essentiels

| Fichier | Existe fork ? | Existe hotfix ? | Diff notable ? | Dependence critique ? | Risque |
|---|---:|---:|---|---|---|
| `common/history/countries/ir1 - mamluk iraq.txt` | non | oui | nouveau fichier | oui, necessite tag IR1 | moyen |
| `common/history/characters/ir1 - mamluk iraq.txt` | non | oui | nouveau fichier | oui, necessite tag IR1 | faible a moyen |
| `common/country_definitions/02_modded_countries.txt` | oui | oui | hotfix ajoute `IR1` en tete ; diff globale 13/1 | oui | fusion manuelle |
| `common/coat_of_arms/coat_of_arms/03_new.txt` | oui | oui | hotfix ajoute blason `IR1` en tete | oui | fusion manuelle |
| `common/flag_definitions/07_NM_Flags.txt` | oui | oui | hotfix ajoute drapeau `IR1` en tete | oui | fusion manuelle |
| `common/government_types/00_mod_gov_types.txt` | non | oui | nouveau fichier hotfix | oui si `gov_pashalik` souhaite etre actif | moyen |
| `common/history/ai/00_secret_goals.txt` | oui | oui | hotfix ajoute objectif IR1 -> TUR | non bloquant | faible |
| `common/history/diplomacy/00_subject_relationships.txt` | oui | oui | hotfix ajoute IR1 comme protectorat de TUR | oui | fusion manuelle |
| `common/history/diplomatic_plays/00_otto_iraqi_persia_war.txt` | non | oui | nouveau fichier | oui si guerre de depart voulue | moyen a eleve |
| `common/history/states/00_states.txt` | oui | oui | diff globale importante ; ownership IR1 dans 4 states | oui | eleve |
| `common/history/buildings/08_middle_east.txt` | oui | oui | diff 58/24 ; region_state:IR1 | oui | eleve |
| `common/history/pops/08_middle_east.txt` | oui | oui | diff 24/4 ; region_state:IR1 | oui | eleve |
| `common/history/military_formations/04_military_formations_middle_east.txt` | oui | oui | diff 110/89 ; bloc IR1 ajoute et TUR different | oui | eleve, chevauche NAVY/military fixes |
| `events/iran_conclusion_mod_redo.txt` | oui | oui | pas de numstat notable | non pour IR1 | faible |
| `events/iran_troubles_events_mod.txt` | oui | oui | pas de numstat notable | non pour IR1 | faible |
| `common/journal_entries/07_iran_troubles_mod.txt` | oui | oui | pas de numstat notable | non pour IR1 | faible |
| `localization/english/mod_v2content_l_english.yml` | oui | oui | hotfix contient `IR1`, `gov_pashalik`; diff 28/1 | oui | fusion manuelle |
| `localization/french/mod_v2content_l_french.yml` | oui | non | hotfix n'a pas le fichier FR local | oui pour traduction future | ne pas remplacer |

## 7. Diplomatie et guerres identifiees

| Relation | Participants | Fichier | Type de relation | Presente dans fork ? | Import necessaire ? |
|---|---|---|---|---|---|
| Suzerainete ottomane | `TUR` -> `IR1` | `common/history/diplomacy/00_subject_relationships.txt` | `protectorate` | non | oui si IR1 importe |
| Secret goal | `IR1` vs `TUR` | `common/history/ai/00_secret_goals.txt` | `secret_goal = defy` | non | optionnel |
| Diplomatic play regional | `PER` cible `STATE_BASRA.region_state:IR1` | `common/history/diplomatic_plays/00_otto_iraqi_persia_war.txt` | `dp_conquer_state`, `war = no` | non | oui si la guerre/DP du hotfix est voulue |
| Wargoal contre IR1 | holder `IR1`, target `STATE_KHUZESTAN.region_state:ARB` | meme fichier | `conquer_state` | non | a verifier, depend de `ARB` et ownership Khuzestan |
| Wargoal Oman | holder `OMA`, target `STATE_FARS.region_state:PER` | meme fichier | `take_treaty_port` | non | a verifier avec Oman/NAVY pour eviter effets de bord |
| PER -> ARB | `PER` -> `ARB` | `00_subject_relationships.txt` | `vassal` | oui | deja present |
| PER -> ARM | `PER` -> `ARM` | `00_subject_relationships.txt` | `vassal` | oui | deja present |

Note : le changelog parle de guerre Iran/Ottomans, mais le fichier observe cree plutot un diplomatic play initie par `PER` contre `IR1`, avec wargoals impliquant `ARB` et `OMA`. Le champ `war = no` indique qu'il faut tester si cela demarre comme diplomatic play plutot que guerre active.

## 8. States / ownership / claims concernes

| State | Ownership fork | Ownership hotfix | Claims fork | Claims hotfix | Changement hotfix | Risque |
|---|---|---|---|---|---|---|
| `STATE_BASRA` | `TUR` | `IR1` | aucun claim TUR dans le bloc local | `add_claim = c:TUR` | transfert a IR1 | eleve |
| `STATE_BAGHDAD` | `TUR` | `IR1` | aucun claim TUR dans le bloc local | `add_claim = c:TUR` | transfert a IR1 | eleve |
| `STATE_MOSUL` | `TUR` | `IR1` | aucun claim TUR dans le bloc local | `add_claim = c:TUR` | transfert a IR1 | eleve |
| `STATE_DEIR_EZ_ZOR` | `TUR` | `IR1` | `add_claim = c:TUR` deja proche | `add_claim = c:TUR` | transfert a IR1 | eleve |
| `STATE_KHUZESTAN` | `PER` | `PER` | non lie directement a IR1 dans state | non change notable | cible de wargoal via `region_state:ARB` | moyen, verifier `ARB` |
| `STATE_LURISTAN` | `PER` | `PER` | non change notable | non change notable | pas de transfert | faible |
| `STATE_ARMENIA` | `PER` | `PER` | non change notable | non change notable | pas de transfert direct | faible |
| `STATE_AZERBAIJAN` | `PER` | `PER` | claims PER/TUR existants | claims PER/TUR existants | pas de transfert direct | faible |

Les owned provinces des states transferes semblent identiques entre fork et hotfix ; le changement principal est le pays proprietaire et l'ajout de claims TUR.

## 9. Personnages et dirigeants

| Personnage | Tag | Role | Fichier | Import direct possible ? | Dependances |
|---|---|---|---|---|---|
| Omar Ahmad | `IR1` | ruler historique, culture georgian, armed forces, jingoist leader | `common/history/characters/ir1 - mamluk iraq.txt` | oui, apres tag IR1 | country definition IR1, localisation, possibly names/cultures vanilla |
| General mamluk anonyme | `IR1` | general, commander_rank_2, formation `mamluk_army` | `common/history/military_formations/04_military_formations_middle_east.txt` | non tel quel | formation IR1, states IR1, hq `region_near_east` |
| Karim Khan Zand | `PER` | ruler/template Persia | `common/history/characters/per - persia.txt` | deja present | pas de diff notable |

Le fichier `ir1 - mamluk iraq.txt` des personnages est nouveau et relativement isole, mais il ne sert a rien sans definition de tag, history country et ownership.

## 10. Localisation necessaire

| Cle | Langue | Fichier hotfix | Presente dans fork ? | A importer/traduire ? |
|---|---|---|---|---|
| `IR1` | anglais | `localization/english/mod_v2content_l_english.yml` | non | oui |
| `IR1_ADJ` | anglais | `localization/english/mod_v2content_l_english.yml` | non | oui |
| `gov_pashalik` | anglais | `localization/english/mod_v2content_l_english.yml` | non | oui si gouvernement importe |
| `gov_pashalik_desc` | anglais | `localization/english/mod_v2content_l_english.yml` | non | oui si gouvernement importe |
| `RULER_TITLE_PASHA` | anglais | `localization/english/mod_v2content_l_english.yml` | probablement non local au fork | verifier avant import |
| `RULER_TITLE_MUTASARRIF` | anglais | mentionne dans government type | pas trouve dans extrait loc hotfix lu | verifier avant import |
| `IR1` | francais | absent hotfix | non | a creer |
| `IR1_ADJ` | francais | absent hotfix | non | a creer |
| `gov_pashalik` | francais | absent hotfix | non | a creer si gouvernement importe |

Le hotfix ne fournit pas de localisation francaise pour ce bloc. Toute phase d'import doit donc ajouter des cles FR dediees pour eviter les cles brutes.

## 11. Conflits avec corrections locales

| Domaine | Interaction observee | Risque |
|---|---|---|
| BIC | aucune interaction directe IR1/BIC ; recherches larges ont vu fichiers BIC mais hors bloc | faible |
| Japon | aucune interaction directe | faible |
| Australasie | aucune interaction directe | faible |
| NAVY-1/2/3 | `04_military_formations_middle_east.txt` chevauche le domaine formations deja corrige | eleve |
| ADMIN | `08_middle_east.txt` buildings peut chevaucher des corrections de PM/batiments | moyen a eleve |
| HOTFIX-2 laws | aucune interaction directe | faible |
| Localisation FR | hotfix n'a pas le fichier FR local | risque de cles brutes si oublie |
| States | `00_states.txt` est fortement modifie localement et globalement | eleve |
| Diplomacy | `00_subject_relationships.txt` partage avec beaucoup d'autres sujets | moyen |

## 12. Import direct possible plus tard

Ces elements sont nouveaux ou quasi isoles, mais doivent quand meme etre ajoutes dans une phase d'import, pas pendant cet audit :

| Fichier / bloc | Condition |
|---|---|
| `common/history/countries/ir1 - mamluk iraq.txt` | apres ajout de `IR1` en country definitions |
| `common/history/characters/ir1 - mamluk iraq.txt` | apres ajout de `IR1` |
| bloc `IR1` dans `common/coat_of_arms/coat_of_arms/03_new.txt` | fusion manuelle du bloc uniquement |
| bloc `IR1` dans `common/flag_definitions/07_NM_Flags.txt` | fusion manuelle du bloc uniquement |
| bloc `IR1` dans `common/history/ai/00_secret_goals.txt` | optionnel, apres import IR1 |
| nouveau fichier `common/history/diplomatic_plays/00_otto_iraqi_persia_war.txt` | seulement apres ownership IR1 et verification `ARB`/`OMA` |

## 13. Fusion manuelle necessaire

| Fichier | Pourquoi |
|---|---|
| `common/country_definitions/02_modded_countries.txt` | fichier existe des deux cotes ; ajouter seulement le bloc `IR1` |
| `common/government_types/00_mod_gov_types.txt` | nouveau fichier hotfix, mais verifier absence de conflit avec les government types locaux |
| `common/history/diplomacy/00_subject_relationships.txt` | ajouter seulement le pact TUR -> IR1 |
| `common/history/states/00_states.txt` | transferer uniquement les states concernes et claims, sans ecraser les autres corrections |
| `common/history/buildings/08_middle_east.txt` | convertir seulement les blocs Baghdad/Mosul/Basra/Deir ez-Zor vers `region_state:IR1` |
| `common/history/pops/08_middle_east.txt` | convertir seulement les blocs IR1 concernes |
| `common/history/military_formations/04_military_formations_middle_east.txt` | ajouter le bloc IR1 sans annuler corrections locales des formations TUR/Oman/NAVY |
| `localization/english/mod_v2content_l_english.yml` ou fichier dedie | ajouter seulement les cles IR1/gov_pashalik |
| `localization/french/*.yml` | creer/traduire les cles IR1/gov_pashalik |

## 14. Changements a ne pas importer tels quels

| Changement | Raison |
|---|---|
| Remplacement complet de `common/history/states/00_states.txt` | risque majeur de perdre les corrections Japon/Sakhalin/Australie et autres corrections locales |
| Remplacement complet de `common/history/buildings/08_middle_east.txt` | risque ADMIN/NAVY/PM |
| Remplacement complet de `common/history/pops/08_middle_east.txt` | risque de modifier tout le Moyen-Orient |
| Remplacement complet de `common/history/military_formations/04_military_formations_middle_east.txt` | risque de perdre les corrections formations 1.13 et NAVY |
| Remplacement complet de `localization/english/mod_v2content_l_english.yml` | risque de perdre localisations locales |
| Suppression/absence de localisation francaise | ferait apparaitre des cles brutes en jeu FR |
| Import du diplomatic play sans states IR1 | cible `STATE_BASRA.region_state:IR1` invalide si IR1 n'existe pas dans le state |
| Import de `gov_pashalik` sans titres localises | possible cle brute `RULER_TITLE_MUTASARRIF` |

## 15. Plan d'import recommande

Etape 1 :
Ajouter le tag `IR1` dans `common/country_definitions/02_modded_countries.txt`, puis ajouter son blason/drapeau (`03_new.txt`, `07_NM_Flags.txt`).

Etape 2 :
Ajouter `common/history/countries/ir1 - mamluk iraq.txt` et `common/history/characters/ir1 - mamluk iraq.txt`.

Etape 3 :
Ajouter les cles EN/FR minimales : `IR1`, `IR1_ADJ`, `gov_pashalik`, `gov_pashalik_desc`, `RULER_TITLE_PASHA`, `RULER_TITLE_MUTASARRIF`.

Etape 4 :
Fusionner le gouvernement `gov_pashalik`, puis tester que le pays peut charger sans cle brute.

Etape 5 :
Fusionner ownership/claims dans `00_states.txt` pour Basra, Baghdad, Mosul et Deir ez-Zor.

Etape 6 :
Fusionner les blocs `region_state:IR1` dans `08_middle_east.txt` buildings et pops.

Etape 7 :
Ajouter seulement le bloc militaire IR1 dans `04_military_formations_middle_east.txt`, en conservant les corrections locales des Ottomans et d'Oman.

Etape 8 :
Ajouter le pacte TUR -> IR1 dans `00_subject_relationships.txt`.

Etape 9 :
Importer le diplomatic play `00_otto_iraqi_persia_war.txt` seulement apres verification de `ARB`, `OMA`, `STATE_KHUZESTAN.region_state:ARB` et `STATE_FARS.region_state:PER`.

Etape 10 :
Tester en jeu : TUR, PER, IR1/Mamluk Iraq, Basra/Baghdad/Mosul/Deir ez-Zor, et logs.

## 16. Risques

- `IR1` absent du fork : tout import partiel de states/diplomatic play peut casser si le tag n'est pas ajoute avant.
- `STATE_BASRA.region_state:IR1` est une dependance dure du diplomatic play.
- `STATE_KHUZESTAN.region_state:ARB` doit etre verifie avant import ; si `ARB` ne possede pas le region_state attendu, le wargoal peut etre invalide.
- `04_military_formations_middle_east.txt` est un fichier sensible apres les corrections 1.13/NAVY.
- `08_middle_east.txt` buildings peut chevaucher les corrections ADMIN.
- Le hotfix fournit la localisation EN mais pas FR.
- Le changelog parle de guerre Iran/Ottomans, mais l'implementation observee ressemble a un diplomatic play `PER` contre `IR1`, avec `war = no`.

## 17. Tests a faire en jeu

Apres une future phase d'import :

1. Lancer le mod jusqu'au menu principal.
2. Demarrer en Ottomans (`TUR`) et verifier que Mamluk Iraq est sujet/protectorat.
3. Demarrer en Persia (`PER`) et verifier la situation diplomatique avec IR1/ARB/OMA.
4. Verifier les states Basra, Baghdad, Mosul, Deir ez-Zor : pas de province blanche, ownership correct, pops et batiments visibles.
5. Verifier que `Mamluk Iraq`, `Autonomous Pashalik`, `Pasha` et `Mutasarrif` ne s'affichent pas en cles brutes en francais.
6. Laisser tourner un mois.
7. Surveiller `error.log` avec :

```powershell
Select-String "$env:USERPROFILE\Documents\Paradox Interactive\Victoria 3\logs\error.log" -Pattern "IR1","Mamluk","gov_pashalik","STATE_BASRA","STATE_KHUZESTAN","00_otto_iraqi_persia_war","region_state:IR1"
```

## 18. Fichiers crees

| Fichier | Role |
|---|---|
| `docs/reports/hotfix/HOTFIX_3_AUDIT_IRAQ_IRAN_OTTOMANS.md` | rapport d'audit ciblé Iraq/Iran/Ottomans |

## 19. Confirmation

Aucun fichier gameplay n'a ete modifie pendant cette phase.

Aucun fichier `common/history/`, `common/country_definitions/`, `common/history/diplomacy/`, `common/history/states/`, `common/history/buildings/`, `common/history/military_formations/`, `events/`, `localization/`, `map_data/`, BIC, Japon, Inde, NAVY, ADMIN ou lois HOTFIX-2 n'a ete modifie.

Le stash MARATH n'a pas ete touche.
