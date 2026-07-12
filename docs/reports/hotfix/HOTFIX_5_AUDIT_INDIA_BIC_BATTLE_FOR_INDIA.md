# HOTFIX-5-AUDIT - Inde, BIC et Battle for India

## 1. Resume executif

Cet audit compare le fork 1776, le hotfix upstream et la vanilla The Great Wave 1.13. Aucun fichier gameplay n'a ete modifie.

Conclusions principales :

- La chaine dediee `Battle for India` est deja presente dans le fork et ses fichiers principaux sont identiques au hotfix, y compris le BOM de la journal entry.
- Le hotfix n'offre donc aucun import direct indispensable pour l'objectif. Son apport le plus utile est une serie de hunks qui reviennent aux deux strategic regions vanilla valides : `region_north_india` et `region_south_india`.
- Le fork utilise encore massivement cinq IDs non definis par la vanilla 1.13 : `region_bengal`, `region_bombay`, `region_central_india`, `region_madras` et `region_punjab`. Cela touche les formations, les journal entries, les events et les boutons coloniaux.
- Le hotfix corrige une partie de ce probleme, notamment `06_new_imperialism_mod.txt`, `00_new_colonial_admins.txt`, le setup BIC, la JE Durrani et les HQ militaires. Il ne corrige cependant pas toutes les references et contient lui-meme plusieurs variantes plus anciennes que la vraie vanilla 1.13.
- La loi locale BIC `law_frontier_colonization` est un choix volontaire a conserver. Le hotfix remettrait `law_colonial_exploitation` et `law_mercantilism_navigation_acts` dans le fichier pays BIC : ces changements sont classes **CONFLIT AVEC BIC**.
- Les states, ownerships, pops, relations et principaux historiques de pays indiens sont deja identiques entre fork et hotfix. Aucun import massif de ces fichiers n'est justifie.
- `common/history/buildings/10_india.txt` et `common/history/military_formations/05_military_formations_india.txt` chevauchent NAVY, ADMIN et le stash MARATH. Ils ne doivent etre modifies que par hunks isoles.
- Le hotfix ne contient aucun dossier `localization/french`. Le fork dispose deja de paires EN/FR completes pour les deux gros fichiers de localisation examines.
- Le contenu DLC Inde suppose largement une chronologie 1836-1936. Plusieurs garde-fous sont technologiques ou contextuels, mais certains contenus sont visibles des 1776 et BIC commence avec un tier technologique 4. Une phase d'adaptation 1776 est necessaire avant d'activer davantage de contenu.

Decision globale : **ne rien importer en bloc**. Proceder par petits hunks, en commencant par les strategic regions et le systeme d'administration coloniale unique.

## 2. Etat Git et stash MARATH

| Element | Resultat |
|---|---|
| Branche | `hotfix-dlc-audit` |
| Working tree initial | Propre |
| HEAD initial | `2228ce8 Fix Ezo Hokkaido journal gate` |
| Tags `post-hotfix-japan-*` | Aucun tag retourne |
| Stash | `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` |
| Action sur le stash | Aucune |

Le stash MARATH n'a ete ni applique, ni inspecte comme contenu courant, ni supprime, ni modifie.

## 3. Methode et perimetre

Racines comparees :

- fork : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork` ;
- hotfix : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source` ;
- vanilla : `C:\Games\Victoria 3 The Great Wave\game`.

La recherche textuelle cible BIC, Battle for India, Bengal, Bombay, Hyderabad, Travancore, Maratha, Mysore, Punjab/Sikh, sepoys, presidencies, princely states et doctrine of lapse. Elle retourne 95 fichiers hotfix potentiels : 29 identiques au fork, 64 differents et 2 absents du fork. Les deux absences sont `06_new_imperialism_mod.txt`, remplace localement par `06_new_imperialism.txt`, et un faux positif sans rapport direct (`vampire_panic_events.txt`).

Les comparaisons ont ensuite ete reduites aux hunks indiens afin de ne pas confondre les differences Japon, IR1, Australie ou autres avec le scope HOTFIX-5.

## 4. Resume du changelog hotfix

Le changelog annonce notamment :

- `Battle For India Journal Entry now in UTF-8 BOM format` ;
- `Battle For India JE fixed` ;
- `Battle for India player objective` ;
- `Battle For India Countries get a unique India Company flag` ;
- `Indian Colonial Admins overhauled, you now create one East India Company` ;
- `British India now has claims on all of India` ;
- `Mughal's and Maratha now also have claims over all of India` ;
- `Dutch East Indies & British East India get faster incorporation bonuses` ;
- `Historical Characters added to British East India Company` ;
- `Great Britain will expand British India rather than create a new colony`.

La plupart de ces apports sont deja dans le fork. Le point encore incomplet est l'alignement du systeme de colonial administrations sur les deux strategic regions vanilla.

## 5. Inventaire des fichiers hotfix pertinents

| Fichier hotfix | Domaine | Entites | Etat fork | Etat vanilla | Priorite |
|---|---|---|---|---|---|
| `common/objectives/01_player_objectives.txt` | objectif | Battle for India | Identique | Fichier vanilla different | Deja present |
| `common/objective_subgoal_categories/01_mod_categories.txt` | objectif | categorie Battle for India | Identique | Absent | Deja present |
| `common/objective_subgoals/03_battle_for_india_mod.txt` | objectif | `sg_consolidate_india` | Identique | Absent | Deja present |
| `common/journal_entries/00_battle_for_india_mod.txt` | JE | objectif territorial | Identique, BOM present | Absent | Deja present |
| `events/battle_for_india_events.txt` | event | victoire Durrani | Identique | Absent | Deja present |
| `common/journal_entries/07_hindustan_is_durrani_mod.txt` | JE | DUR/Hindustan | Different | Absent | Elevee, par hunk |
| `common/history/countries/bic - british east india company.txt` | pays | BIC | Different | Different | Critique, conflit volontaire |
| `common/character_templates/country_bic.txt` | personnages | dirigeants BIC | Identique | Different | Deja present |
| `common/history/characters/bic - british india.txt` | personnages | roster initial BIC | Identique | Absent au meme chemin | Adaptation 1776 |
| `common/history/states/00_states.txt` | states | ownership et claims Inde | Fichier global different, blocs Inde equivalents | Different | Ne pas remplacer |
| `common/history/pops/10_india.txt` | pops | populations Inde | Identique | Different | Deja present |
| `common/history/buildings/10_india.txt` | buildings | BIC, TRA, MARATH, BHV, ADMIN | Different | Different | Conflit NAVY/ADMIN/MARATH |
| `common/history/military_formations/05_military_formations_india.txt` | formations | armees et flotte TRA | Different | Different | Elevee, par hunk |
| `common/history/diplomacy/00_subject_relationships.txt` | diplomatie | GBR/BIC, princes indiens | Differences globales ; Inde identique sauf PUD local | Different | Ne pas remplacer |
| `common/history/diplomacy/00_relations.txt` | diplomatie | relations BIC/Inde | Identique | Different | Deja present |
| `common/journal_entries/06_new_imperialism_mod.txt` | colonial admin | EIC unique | Fork utilise `06_new_imperialism.txt`, different | Absent | Elevee, fusion manuelle |
| `common/scripted_buttons/00_new_colonial_admins.txt` | boutons | creation/expansion EIC | Different | Absent | Critique, par blocs |
| `events/new_imperialism_events_mod.txt` | events | creation colonial admin | Identique | Absent | Deja present |
| `common/on_actions/00_code_on_actions.txt` | hooks globaux | BIC et contenu Inde DLC | Different globalement ; lignes Inde equivalentes | Different | Ne pas remplacer |
| `common/scripted_triggers/00_coa_triggers.txt` | triggers | flags compagnie Inde | Identique au fork et a la vanilla | Identique | Aucun import |
| `common/journal_entries/04_*.txt` lies a l'Inde | JE DLC | BIC, PAN, MUG, famines, railways | Generalement differents | Hotfix souvent identique vanilla | Audit par chaine |
| `events/india_events/*.txt` | events DLC | Inde tardive et Raj | Melange d'identiques et de differences | Hotfix souvent identique vanilla | Audit par chaine |
| `events/bic_breakup.txt` | event | independance BIC | Different | Hotfix identique vanilla | Par hunk apres test |
| `events/british_raj_events.txt` | event | Company/Crown rule | Different | Hotfix differe d'une condition | Par hunk apres test |
| `localization/english/mod_v2content_l_english.yml` | localisation | objectif, event, pays | Different hors bloc Battle | Absent vanilla | Fusion dediee seulement |
| `localization/english/mod_journal_entries_l_english.yml` | localisation | colonial admins | Fork contient 19 lignes regionales en plus | Absent vanilla | Adapter avec gameplay |
| `localization/english/NM_Countries_l_english.yml` | localisation | pays moddes | Identique | Absent | Deja present |
| `localization/english/country_flavor_text_l_english.yml` | localisation | flavor pays | Identique | Different | Deja present |

## 6. Audit BIC

### 6.1 Setup compare

| Element BIC | Fork | Hotfix | Vanilla 1.13 | Decision |
|---|---|---|---|---|
| Tag | Colonial, principality, culture britannique, capitale `STATE_WEST_BENGAL` | Identique | Tag disponible | Deja present |
| Technologie | Tier 4 + `academia`, `colonization`, `line_infantry`, `law_enforcement` | Identique | Tier 2 + railways/corporate techs | Adapter au depart 1776, ne pas importer aveuglement |
| Loi coloniale | `law_frontier_colonization` | `law_colonial_exploitation` | Pas la meme sequence | **CONFLIT AVEC BIC**, garder fork |
| Navigation Acts | Non activee dans BIC | `law_mercantilism_navigation_acts` activee | Non activee | Conflit HOTFIX-2/BIC, decision separee |
| Autres lois | Colonial administration, subjecthood, extraction, oligarchy, professional army, etc. | Identiques | Setup different | Deja present |
| Variable | `new_imperialism_mod_var` | Identique | Absente | Necessaire a l'expansion BIC locale |
| Modifiers | company rule, `colonial_administration_76`, efforts et civil service | Identiques | Setup plus reduit | Deja present |
| Ryotwari regions | `region_bombay` + `region_madras` + Assam | `region_south_india` + Assam | Geographic regions anciennes + Assam | Importer seulement le retour a `region_south_india` |
| Overlord | Chartered company de GBR | Identique | Mecanique disponible | Deja present |
| Sujets | JEY et COO puppets | Identique | Contexte vanilla different | Deja present |
| Liberty desire | `-30` | Identique | Disponible | Deja present |
| Service | `exempt_from_service` avec GBR | Identique | Disponible | Deja present |
| Armee | `Bengal_Army`, 80 unites, trois generaux | Identique sauf HQ hotfix valide | Formation vanilla differente | HQ par hunk ; taille a auditer 1776 |
| Flotte | Aucune | Aucune | Selon setup vanilla | Garder absence volontaire |
| Infrastructure | 9 ports, 2 niveaux de shipyard dans fork | Shipyard West Bengal niveau 6 | Different | **CONFLIT AVEC NAVY**, garder niveau 2 |

### 6.2 Loi a preserver

La ligne suivante est volontaire et doit rester :

```txt
activate_law = law_type:law_frontier_colonization
```

Le hunk hotfix qui la remplace par `law_colonial_exploitation` est classe **CONFLIT AVEC BIC** et **NE PAS IMPORTER**.

### 6.3 Risques 1776 propres a BIC

- Le tier technologique 4 est tres avance pour 1776 et peut satisfaire immediatement des triggers concus pour le XIXe siecle tardif.
- `Bengal_Army` totalise 80 unites et emploie line infantry, hussars, cuirassiers, lancers, cannon et mobile artillery. La composition est a revoir historiquement, mais pas pendant un merge hotfix.
- `scope:maitland_gen` et `scope:madras_army` sont references sans `save_scope_as` trouve dans les fichiers runtime recherches. Ce bloc est suspect.
- Le roster initial cree Robert Clive alors qu'il est mort en 1774. D'autres ages ou fonctions semblent calibres pour une date plus tardive.
- Warren Hastings est en revanche explicitement configure pour une utilisation a partir de `1776.1.1`.

Classification : **ADAPTER AU SETUP 1776**, sans modifier la loi frontier colonization ni creer une flotte BIC.

## 7. Audit Battle for India

### 7.1 Chaine principale

| Chaine | Entry point | Date attendue | Compatible 1776 ? | Dependances | Decision |
|---|---|---|---|---|---|
| Objectif `objective_battle_for_india` | Choix d'objectif au lobby | Concu pour le setup du mod | Oui | categorie + subgoal + JE + loc | **DEJA PRESENT** |
| `sg_consolidate_india` | Demarrage de l'objectif | Immediate | Oui | `je_battle_for_india_goal` | **DEJA PRESENT** |
| `je_battle_for_india_goal` | Ajoutee par le subgoal | Sans date | Oui | liste de states, controle 80 %, goal engine | **DEJA PRESENT** |
| `je_hindustan_is_durrani` | Visible au lobby pour DUR | 1776 plausible | Oui, mais regions cassees dans fork | event `.1`, modifiers et notifications | **IMPORTER PAR HUNK** |
| `battle_for_india_events.1` | Completion Durrani | Contextuel | Oui | caste hierarchy, claims, modifiers | **DEJA PRESENT** |

Le bloc objectif ne depend pas implicitement de 1836. Il liste explicitement les pays FRA, BIC, MARATH, DUR, HYD, DEI, NET et POR et convient au scenario 1776.

### 7.2 Dependances verifiees

| Dependance | Fork | Hotfix | Vanilla | Statut |
|---|---:|---:|---:|---|
| `modifier_conversion_of_hindustan_mod` | Oui | Oui | Non | Fournie par le mod |
| `modifier_coop_hindustan_mod` | Oui | Oui | Non | Fournie par le mod |
| `british_indian_caste_system` | Oui | Oui | Oui | Disponible |
| `durrani_abandons_mughal_sov` | Oui | Oui | Non | Fournie par le mod |
| `caste_hierarchy_appears` | Oui | Oui | Oui | Disponible |
| `sgcat_battle_for_india` | Oui | Oui | Non | Fournie par le mod |
| `sg_consolidate_india` | Oui | Oui | Non | Fournie par le mod |

Aucune dependance manquante n'a ete identifiee pour la chaine dediee.

### 7.3 Probleme Durrani

Le hotfix utilise `region_south_india` et `region_north_india`, toutes deux definies par la vanilla. Le fork les a remplacees par `region_central_india`, `region_punjab` et `region_bombay`, absentes des definitions vanilla et du mod.

La logique hotfix exige trois largest states dans chacune des deux regions. Le fork exige deux states dans trois regions inexistantes. Recommandation : restaurer par hunk les deux regions vanilla, puis retester l'equilibrage du seuil 3 dans une phase dediee.

## 8. Audit des colonial administrations indiennes

### 8.1 Intention du hotfix

Le hotfix remplace les administrations separees Bengal/Bombay/Madras/Central India/Punjab par une creation principale couvrant `region_north_india` et `region_south_india`. Le bouton `je_colonial_administration_button_east_india_company` cree un unique dynamic country colonial avec `india_mod_subject_var`, puis l'event `new_imperialism_events.3` lui applique le setup de compagnie.

Le bouton `expand_east_india` transfere ensuite les states des deux regions au meme sujet. Le bouton `expand_for_bic` fait de meme pour la BIC de depart via `new_imperialism_mod_var`.

### 8.2 Fork actuel

Le fork conserve une East India Company principale, mais expose aussi des boutons regionaux utilisant les cinq strategic regions inexistantes. Son fichier `06_new_imperialism.txt` et `00_new_colonial_admins.txt` restent donc incompatibles avec la carte strategic regions vanilla 1.13.

| Element | Hotfix | Fork | Decision |
|---|---|---|---|
| JE principale | `06_new_imperialism_mod.txt` | `06_new_imperialism.txt` | Fusionner dans le nom local, ne pas ajouter un doublon |
| Main EIC button | Deux regions vanilla | Cinq IDs absents | **IMPORTER PAR HUNK** |
| Expand EIC | Deux regions vanilla | Cinq IDs absents | **IMPORTER PAR HUNK** |
| Expand existing BIC | Deux regions vanilla | Cinq IDs absents | **IMPORTER PAR HUNK** |
| Boutons regionaux | North India legacy masque dans hotfix | Cinq boutons visibles dans fork | Retirer seulement apres validation de la chaine unique |
| Event `.3` | Identique au fork | Identique | Aucun import |
| Loi de la nouvelle compagnie | Event applique colonial exploitation | Identique | Conflit de design a decider pour les compagnies creees dynamiquement |

Important : la restriction locale `law_frontier_colonization` concerne BIC. L'event de creation dynamique applique encore `law_colonial_exploitation`. Avant merge, il faut decider si la politique locale doit aussi s'appliquer aux nouvelles compagnies. Ne pas changer ce point implicitement.

## 9. Strategic regions : anomalie prioritaire

La vanilla 1.13 definit seulement :

- `region_north_india` ;
- `region_south_india`.

Elle ne definit pas :

- `region_bengal` ;
- `region_bombay` ;
- `region_central_india` ;
- `region_madras` ;
- `region_punjab`.

Le fork ne fournit aucune definition locale de ces cinq IDs. Leur utilisation est donc un risque de post-validation ou de contenu silencieusement inactif.

Domaines affectes observes :

- 107 references `region_madras` ;
- 139 references `region_bombay` ;
- 98 references `region_bengal` ;
- 104 references `region_central_india` ;
- 134 references `region_punjab`.

Ces comptes couvrent le runtime `common` et `events`, pas seulement les fichiers HOTFIX-5. Le probleme depasse un import BIC et exige une phase technique separee.

## 10. Audit par pays indien

| Pays | Changements hotfix | Adaptations locales | Risques | Priorite |
|---|---|---|---|---|
| BIC | Loi exploitation, Navigation Acts, regions broad, shipyard 6 | Frontier colonization, shipyard 2, NAVY sans flotte | Tech/army 1776, regions invalides | Critique |
| Bengal | Pas de tag actif distinct dans le setup ; territoire BIC/COO | BIC possede Bihar, East Bengal et part de West Bengal | Confusion tag `BNG`/region_state | Important |
| Bombay | Ownership MARATH/KHP/SAT/POR identique | Shipyard MARATH reduit, future flottille stashee | Conflit MARATH/NAVY | Critique pour stash |
| Hyderabad | Historique HYD identique ; KNO vassal | Fork ajoute PUD comme vassal HYD | Ne pas perdre PUD par remplacement global | Important |
| Travancore | Hotfix a la flotte mais pas l'administration navale locale | NAVY ajoute administration et `state_region` au navire | Reimport hotfix annulerait NAVY | Critique NAVY |
| Maratha | Pays, claims et armee deja presents | Shipyard 1, pas d'admin navale courant, stash futur | Chevauche les deux fichiers stashes | Critique stash |
| Mysore | Historique identique | PM ADMIN `pm_simple_organization` | Hotfix remet ancien PM | Important ADMIN |
| Punjab/PAN | Contenu Sikh DLC present | HQ militaire utilise ID absent | Chaine Ranjit Singh suppose calendrier 1836 | Important |
| Awadh/AWA | Ownership et armee presents | Aucun fichier pays dedie trouve lors de l'audit naval | HQ invalide, contenu princier | Important |
| Sindh/SIN | Ownership et armee presents | Pas de fichier pays dedie trouve | HQ invalide, tag incomplet possible | Important |
| Mughal/MUG | Delhi, JE et claims presents | Setup 1776 propre au mod | JE visible au lobby sans date | Important |
| Etats princiers | JE/events DLC presents | Relations 1776 specifiques | Plusieurs hooks mensuels sans date basse | Important |
| France/Portugal/DEI | Enclaves dans Madras/Bombay/Ceylon identiques | NAVY deja traite ces puissances | Ne pas modifier via import Inde | Secondaire |

## 11. Ownership, claims et pops

Les blocs indiens de `00_states.txt` ne presentent aucun hunk fork/hotfix. Les owners observes sont identiques, par exemple :

| State | Owners actifs fork/hotfix |
|---|---|
| Punjab | DUR, PAN |
| Hill Punjab | DUR |
| Awadh | AWA, BIC |
| Bihar | BIC |
| Bombay | KHP, MARATH, POR, SAT |
| Circars | BIC, JEY |
| Delhi | MUG |
| Hyderabad | HYD |
| Mysore | MYS |
| Travancore | COC, NET, TRA |
| West Bengal | BIC, COO |
| East Bengal | BIC |

Les claims BIC/MARATH/MUG annonces par le changelog sont deja presents dans le fork aux memes endroits que le hotfix. `common/history/pops/10_india.txt` est identique au hotfix. Decision : **DEJA PRESENT**, ne pas remplacer states ou pops.

## 12. Audit des formations militaires et navales

Le hotfix et le fork contiennent les memes formations et tailles. Les differences principales sont les HQ :

| Pays/formation | Hotfix | Fork | Decision |
|---|---|---|---|
| PAN, trois armees | `region_north_india` | `region_punjab` | Hunk hotfix utile |
| BIC `Bengal_Army` | `region_north_india` | `region_bengal` | Hunk hotfix utile |
| HYD/MYS/KNO/PUD/JEY/COC/TRA army | `region_south_india` | `region_madras` | Hunks hotfix utiles |
| AWA/GWA/GAR/MUG | `region_north_india` | IDs split absents | Hunks hotfix utiles |
| NAG/SAT/KHP/BHV/SIN | Broad regions hotfix | IDs split absents | Hunks hotfix utiles apres verification geographique |
| MARATH army | `region_north_india` | `region_central_india` | **CONFLIT AVEC STASH MARATH** |
| TRA fleet | `region_south_india`, sans `state_region` | `region_south_india` + `STATE_TRAVANCORE` | Garder fork NAVY |

Autres risques :

- `Bengal_Army` compte 80 unites et merite un audit 1776 separe.
- Aucun nouveau fleet BIC ou MARATH n'est apporte par le hotfix.
- Le hotfix ne doit pas reintroduire l'absence de `state_region` sur le navire Travancore.
- Aucun hunk MARATH de `05_military_formations_india.txt` ne doit etre applique tant que le stash reste separe.

Classification : **IMPORTER PAR HUNK** pour les HQ non conflictuels ; **A REPRENDRE APRES LE STASH MARATH** pour MARATH.

## 13. Audit des batiments, ports et administration

| State/pays | Difference hotfix -> fork | Conflit | Decision |
|---|---|---|---|
| West Bengal/BIC | Shipyard 6 -> 2 | NAVY/equilibrage | Garder fork |
| Gujarat/BHV | Administration navale hotfix absente du fork | Pas de flotte BHV | Ignorer sauf recherche dediee |
| Travancore/TRA | Fork ajoute administration navale niveau 1 | NAVY-3C-1 | Garder fork |
| Bombay/MARATH | Hotfix ajoute administration navale ; fork ne l'a pas courant | Stash MARATH | Ne pas importer maintenant |
| Bombay/MARATH | Shipyard 5 -> 1 dans fork | NAVY/equilibrage | Garder fork |
| MUG/MYS/MARATH | Hotfix utilise `pm_horizontal_drawer_cabinets`, fork `pm_simple_organization` | ADMIN | Garder fork |

Le hotfix ne change pas l'ownership des buildings indiens par rapport au setup de base, mais ses niveaux et PM annuleraient des corrections locales. `10_india.txt` est classe **CONFLIT AVEC NAVY**, **CONFLIT AVEC ADMIN** et **CONFLIT AVEC STASH MARATH**. Aucun remplacement complet n'est acceptable.

## 14. Audit diplomatique

| Relation | Fork | Hotfix | Compatible 1776 ? | Decision |
|---|---|---|---|---|
| GBR -> BIC | Chartered company | Identique | Oui pour le setup local | Deja present |
| GBR -> BIC | Exempt from service | Identique | Oui | Deja present |
| BIC liberty desire | -30 | Identique | Oui | Deja present |
| BIC -> JEY/COO | Puppets | Identique | A confirmer historiquement | Conserver pendant merge |
| BIC subjects | Exempt from service, liberty desire -20 | Identique | Mecanique locale | Deja present |
| HYD -> KNO | Vassal | Identique | Setup local | Deja present |
| HYD -> PUD | Vassal | Present seulement fork | Setup local | Preserver |
| MARATH -> SAT/KHP/GAR/GWA | Vassaux | Identique | Setup 1776 | Deja present |
| GBR/BIC relations | +80 dans `00_relations.txt` | Identique | Oui | Deja present |

Aucun changement diplomatique Inde du hotfix ne justifie un import. Le fichier global hotfix de sujets perdrait la relation HYD -> PUD et deplacerait aussi des blocs Japon ; ne pas le remplacer.

## 15. Journal entries et events DLC Inde

| Chaine | Garde principale | Hypothese chronologique | Risque 1776 | Decision |
|---|---|---|---|---|
| Uneasy Raj / Sepoy Mutiny | `possible = always = no` actuellement | 1830-1857 | Desactivee, mais nombreuses regions invalides | A auditer plus tard |
| Sikh Sovereignty | Lobby `ip2` + PAN | Ranjit Singh, 1839 et apres | Visible des 1776 si PAN existe | Adapter au setup 1776 |
| Princely States | `ip2` + `is_princely_state` | Systeme 1836 | Peut apparaitre en 1776 | Tester pays par pays |
| Mughal Hindustan | Lobby `ip2` + MUG | Decline moghol tardif | Peut apparaitre en 1776 | Adapter si necessaire |
| India Railway | `railways` + presence Inde | XIXe siecle industriel | BIC tier 4 peut la rendre precoce ; regions invalides | Critique |
| Home Rule | `pan-nationalism`, BIC sujet | Fin XIXe/debut XXe | Tech tier 4 peut accelerer | Ajouter garde chronologique/contextuelle future |
| Nationalism | Mouvement pan-national + BIC sujet | XIXe tardif | Meme risque | Adapter 1776 |
| Non-Cooperation | Lobby `ip2` + BIC ; activation pan-nationalism | XXe siecle | Nom visible au lobby en 1776 | Adapter 1776 |
| Famines | Famine + regions Inde | Transhistorique | Phase 1.1 locale, mais IDs split suspects | Ne pas ecraser ; re-audit technique |
| BIC breakup | BIC independante et paix | Contextuel | Peut arriver a toute date, acceptable | Vanilla/hotfix par hunk apres test |
| British Raj | Evenements Company/Crown rule | 1857+ | Depend des autres chaines | Fusion manuelle seulement |
| British Dictates | `ip2`, BIC sujet, law imposition | Colonial tardif | Peut se declencher avant 1836 | Tester et ajouter garde si necessaire |

Plusieurs events tardifs ont des bornes explicites (`1893`, `1900`, `1904`, `1910`, `1917`, `1925`, `1928`). D'autres reposent seulement sur une technologie ou un statut politique. Le risque principal vient du tier technologique initial BIC et des JEs `is_shown_in_lobby` sans date basse.

## 16. Hotfix versus vraie vanilla 1.13

Le hotfix n'est pas toujours la meilleure reference technique :

- `events/india_events/sikh_empire.txt` hotfix utilise encore `exile_character_with_role_cleanup`, alors que la vanilla utilise `exile_character` et ajuste les roles.
- `india_non_cooperation.txt` hotfix utilise `role = character_role_politician`, alors que la vanilla utilise `ig_leader = yes`.
- `utilitarian.txt` hotfix conserve plusieurs conditions de prominence/roles et filtres de pops differents de la vanilla.
- `jail.txt` hotfix contient des blocs `ai_chance` retires de la vanilla.
- `events/british_raj_events.txt` hotfix differe de la vanilla sur une condition `always = yes` / `exists = heir`.
- De nombreuses JEs hotfix sont identiques a la vanilla, mais le fork a deja des adaptations locales. Il faut comparer les trois versions avant chaque hunk.

Conclusion : **la vanilla 1.13 reste l'autorite pour les APIs**, le hotfix pour l'intention du mod, et le fork pour le setup 1776.

## 17. Hooks globaux et scripted content

### Hooks presents

| Hook | Caller | Garde | Risque | Import recommande |
|---|---|---|---|---|
| BIC breakup | `on_monthly_pulse_country` | Trigger dans `bic_breakup.1` : BIC independante, paix, variable absente | Faible | Deja present |
| Phool Walon Ki Sair | Pulse mensuel | Trigger event | Chronologie a verifier | Deja present |
| Princely state creation `.1-.5` | Pulse mensuel | `ip2`, BIC et conditions event | Peut se produire tot | Deja present, tester |
| Berar lease cleanup | Pulse mensuel | BIC/HYD, modifier, guerre/ownership | Contextuel | Deja present |
| BIC ruler industrialist | `on_character_death`, `on_new_ruler` | `c:BIC ?= owner` | Difference locale, pas hotfix | Preserver |
| Revolution/secession BIC | `on_revolution_start`, `on_secession_start` | BIC root | Fort effet culturel/politique | Preserver, tester |
| Koh-i-Noor | `on_wargoal_enforced` | BIC sujet + controle Punjab | Peut arriver des 1776 | Adapter si necessaire |
| British dictates | `on_impose_law` | BIC sujet + `ip2_content` | Pas de date basse | Adapter 1776 |

Les lignes Inde du hotfix et du fork sont identiques, sauf les deux overrides locaux de ruler BIC. Aucun fichier on_action global ne doit etre importe en entier.

`00_coa_triggers.txt` est identique dans les trois sources. Aucun scripted effect indien dedie supplementaire n'a ete trouve dans les repertoires recherches. Le fichier critique hors liste initiale est `common/scripted_buttons/00_new_colonial_admins.txt`.

## 18. Audit des localisations

Le hotfix ne possede pas de dossier `localization/french`.

| Cle ou fichier | EN | FR fork | Utilisee ? | Conflit | Decision |
|---|---|---|---|---|---|
| Bloc `objective_battle_for_india*` | Present | Present et traduit | Oui | Aucun | Deja present |
| `je_battle_for_india_goal*` | Present | Present et traduit | Oui | Aucun | Deja present |
| `battle_for_india_events.1.*` | Present | Present et traduit | Oui | Aucun | Deja present |
| `mod_v2content` | 472 cles fork | 472 cles FR, meme jeu de cles | Oui | Hotfix ajoute aussi lois/IR1 deja separes localement | Garder fork |
| `mod_journal_entries` | 127 cles fork | 127 cles FR, meme jeu de cles | Oui | 19 cles regionales fork deviendraient inutiles apres merge | Ne pas supprimer avant validation |
| Navigation Acts/Merchant Banking | Fichiers hotfix dedies dans fork | Traduction FR dediee | Oui | Ne pas dupliquer depuis `mod_v2content` | Deja present |
| IR1 | Fichier hotfix dedie dans fork | Traduction FR dediee | Oui | Hors Inde | Ne pas dupliquer |
| North/South India admin buttons | Present dans hotfix EN | Absents ou remplaces par cles regionales fork | Seulement si les blocs hotfix sont conserves | FR obligatoire | Creer des cles dediees au moment du merge |
| Travancore fleet | Fichier EN local | Fichier FR local | Oui | NAVY | Preserver |

Les fichiers `mod_v2content_l_english.yml`, `mod_v2content_l_french.yml`, `mod_journal_entries_l_english.yml` et `mod_journal_entries_l_french.yml` ont un BOM UTF-8. Les paires EN/FR examinees possedent les memes ensembles de cles. Aucun doublon Battle for India n'a ete identifie dans ces paires.

## 19. Dependances candidates

| Dependance | Source | Statut | Decision |
|---|---|---|---|
| `ip2_content` | Vanilla/DLC | Disponible | Utiliser comme garde DLC |
| `region_north_india`, `region_south_india` | Vanilla strategic regions | Disponibles | IDs cibles |
| Cinq regions split | Ni vanilla ni mod | Manquantes | Remplacer, ne pas definir artificiellement |
| `law_frontier_colonization` | Vanilla + fork | Disponible | Preserver pour BIC |
| `law_colonial_exploitation` | Vanilla | Disponible | Ne pas reintroduire pour BIC |
| `modifier_india_company_rule` | Vanilla + fork | Disponible | Aucun import |
| `colonial_administration_76` | Fork/hotfix | Disponible | Necessaire au contenu mod |
| `modifier_ryotwari_system` | Vanilla + fork | Disponible | Corriger seulement le ciblage region |
| `company_east_india_company` | Vanilla + fork | Disponible | Compatible avec BIC |
| Battle modifiers/notifications | Fork/hotfix | Disponibles | Chaine complete |
| Scripted buttons coloniaux | Fork/hotfix | Disponibles mais versions divergentes | Fusion manuelle |
| Localisation FR hotfix | Hotfix | Manquante | Produire localement lors des imports visibles |

## 20. Classification finale des changements

### IMPORTER TEL QUEL

Aucun nouveau fichier gameplay n'a besoin d'etre importe tel quel. Les fichiers dedies Battle for India, les characters BIC, les pops, relations et events de creation coloniale utiles sont deja identiques au hotfix.

### DEJA PRESENT

- objectif, categorie, subgoal et JE Battle for India ;
- event Durrani `.1` ;
- EN/FR de l'objectif ;
- characters/templates BIC ;
- claims BIC/MARATH/MUG ;
- pops Inde ;
- diplomatie GBR/BIC et princely states ;
- event `new_imperialism_events_mod.txt` ;
- hooks Inde globaux.

### IMPORTER PAR HUNK

- retour a `region_north_india` / `region_south_india` dans `bic - british east india company.txt`, sans toucher aux lois ;
- logique EIC unique dans le fichier local `06_new_imperialism.txt` ;
- blocs main/expand EIC/BIC de `00_new_colonial_admins.txt` ;
- conditions Durrani dans `07_hindustan_is_durrani_mod.txt` ;
- HQ non-MARATH dans `05_military_formations_india.txt` ;
- corrections ciblees des JEs/events qui referencent les cinq regions absentes.

### ADAPTER AU SETUP 1776

- tier technologique et roster initial BIC ;
- taille/composition de Bengal Army ;
- visibilite Sikh, Mughal, princely states et non-cooperation ;
- triggers technologiques de nationalism/home rule/railway ;
- events sans date basse ;
- loi appliquee aux nouvelles compagnies dynamiques.

### CONFLIT AVEC LE FORK / BIC / NAVY / ADMIN

- `law_colonial_exploitation` pour BIC ;
- activation Navigation Acts dans BIC sans decision dediee ;
- shipyard BIC niveau 6 ;
- suppression de l'administration navale TRA ou du `state_region` de sa flotte ;
- reintroduction des anciens PM ADMIN ;
- toute modification globale de states, subject relationships ou on_actions.

### CONFLIT AVEC STASH MARATH

- administration navale MARATH dans `10_india.txt` ;
- shipyard MARATH ;
- bloc formation MARATH dans `05_military_formations_india.txt` ;
- noms, flotte ou localisation Konkan absents du working tree courant.

Ces elements sont classes **A REPRENDRE APRES TRAITEMENT SEPARE DU STASH**, sans planifier son application pendant HOTFIX-5.

### IGNORER

- fichiers hotfix identiques a la vanilla mais plus anciens sur certaines APIs que la vraie installation 1.13 ;
- administration navale BHV sans flotte ni justification ;
- remplacement integral des fichiers globaux ;
- localisations EN hotfix dupliquees par des fichiers dedies fork ;
- faux positifs de recherche sans relation fonctionnelle avec l'Inde.

## 21. Plan de merge par petits lots

### HOTFIX-5A - BIC technique isolee

Fichiers autorises : `common/history/countries/bic - british east india company.txt` et rapport dedie.

Action : remplacer uniquement le ciblage `region_bombay`/`region_madras` par `region_south_india`. Interdit : lois, techs, modifiers, army, buildings. Test : BIC au premier jour, Ryotwari, `error.log`. Verifier explicitement `law_frontier_colonization`.

### HOTFIX-5B - East India Company unique

Fichiers autorises : `common/journal_entries/06_new_imperialism.txt`, blocs indiens de `common/scripted_buttons/00_new_colonial_admins.txt`, localisations dediees EN/FR, rapport.

Action : porter les hunks broad regions et retirer les appels aux boutons regionaux seulement apres comparaison. Interdit : remplacement integral du scripted buttons, event `.3`, lois BIC. Test : creation d'une seule compagnie, expansion nord/sud, pas de doublon.

### HOTFIX-5C - Strategic regions DLC Inde

Fichiers autorises : liste fermee de JEs/events contenant les cinq IDs invalides, rapport.

Action : cartographier chaque usage vers north/south ou geographic region. Interdit : remplacement de tous les events par hotfix. La vraie vanilla 1.13 doit arbitrer les APIs. Test : zero reference runtime aux cinq IDs, `error.log` propre.

### HOTFIX-5D - Battle for India / Durrani

Fichiers autorises : `common/journal_entries/07_hindustan_is_durrani_mod.txt`, rapport.

Action : restaurer les deux regions vanilla et verifier les seuils. Interdit : objectif, subgoal, event deja identiques. Test : DUR, completion, event `.1`, claims.

### HOTFIX-5E - Cycle BIC / Raj

Fichiers autorises : `events/bic_breakup.txt`, `events/british_raj_events.txt`, hunks necessaires des JEs liees, rapport.

Action : comparer chaque hunk a la vanilla 1.13, conserver les adaptations 1776. Interdit : import global des events Inde. Test : independance BIC, suppression company, transition Raj, personnages.

### HOTFIX-5F - Formations militaires non conflictuelles

Fichier autorise : `common/history/military_formations/05_military_formations_india.txt`, hors bloc MARATH et hors flotte TRA.

Action : corriger uniquement les HQ des armees non conflictuelles vers north/south. Interdit : tailles, unites, commanders, MARATH, NAVY. Test : post-validation de toutes les formations et passage du premier jour.

### HOTFIX-5G - Batiments non conflictuels

Par defaut aucune modification. Reevaluer seulement les erreurs de logs restantes. Interdit : BIC shipyard, TRA, MARATH, PM ADMIN sans phase dediee.

### HOTFIX-5H - Localisations

Fichiers autorises : fichiers EN/FR dedies HOTFIX-5. Ajouter uniquement les cles visibles reellement requises apres 5B-5G. Conserver BOM, indentation et traductions existantes.

### HOTFIX-5I - Validation finale Inde

Audit uniquement : objectif Battle for India, BIC, DUR, HYD, PAN, MUG, TRA et MARATH sans stash. Verifier menu, lobby, premier jour, un mois, un an et logs. Le stash MARATH reste hors HOTFIX-5.

## 22. Tests recommandes

1. Lancer avec uniquement le mod et verifier le menu et les cartes de l'objectif Battle for India en francais.
2. Tester BIC au `1 janvier 1776`, puis un jour, un mois et un an.
3. Confirmer `law_frontier_colonization` et l'absence de `law_colonial_exploitation` dans les lois BIC de depart.
4. Verifier `Bengal_Army`, son HQ, ses 80 unites et l'absence de flotte BIC.
5. Tester DUR avec l'objectif et la JE Hindustan, puis forcer sa completion.
6. Tester HYD et confirmer KNO/PUD ; tester MARATH et ses sujets sans restaurer le stash.
7. Tester TRA et confirmer sa flotte, son administration navale et son `state_region`.
8. Tester PAN et verifier qu'aucune chaine 1839 ne se comporte comme si la partie avait commence en 1836.
9. Debloquer railways/pan-nationalism par console dans une sauvegarde de test et verifier le moment d'apparition des JEs Inde.
10. Tester la creation puis l'expansion d'une administration coloniale indienne par GBR et FRA ; verifier qu'une seule compagnie est creee.
11. Surveiller `error.log`, `game.log` et `debug.log` avec les patterns : `region_bengal`, `region_bombay`, `region_central_india`, `region_madras`, `region_punjab`, `Invalid right side`, `PostValidate`, `BIC`, `battle_for_india`, `create_military_formation`, `unknown strategic region`.
12. Rechercher les cles brutes en francais dans l'objectif, la JE Durrani et les boutons colonial administration.

## 23. Fichiers consultes principaux

- `Changelog.txt` du hotfix ;
- fichiers Battle for India : objectives, category, subgoal, JE, event et localisation ;
- `common/history/countries/bic - british east india company.txt` dans les trois sources ;
- historiques hotfix/fork de BHV, COC, COO, HYD, MARATH, MUG, MYS, NAG et PUD ;
- `common/history/states/00_states.txt` ;
- `common/history/pops/10_india.txt` ;
- `common/history/buildings/10_india.txt` ;
- `common/history/military_formations/05_military_formations_india.txt` ;
- `common/history/diplomacy/00_subject_relationships.txt` et `00_relations.txt` ;
- `common/character_templates/country_bic.txt` ;
- `common/history/characters/bic - british india.txt` ;
- `common/journal_entries/04_*.txt` lies a l'Inde ;
- `events/india_events/*.txt`, `events/bic_breakup.txt`, `events/british_raj_events.txt` ;
- `common/journal_entries/06_new_imperialism_mod.txt` hotfix et `06_new_imperialism.txt` fork ;
- `common/scripted_buttons/00_new_colonial_admins.txt` ;
- `events/new_imperialism_events_mod.txt` ;
- `common/on_actions/00_code_on_actions.txt` ;
- `common/scripted_triggers/00_coa_triggers.txt` ;
- localisations EN hotfix et paires EN/FR fork pertinentes ;
- `common/strategic_regions/west_south_asia_strategic_regions.txt` vanilla ;
- rapports NAVY-3C et decision BIC existants.

## 24. Fichier cree et confirmations finales

Fichier cree par l'audit :

- `docs/reports/hotfix/HOTFIX_5_AUDIT_INDIA_BIC_BATTLE_FOR_INDIA.md`.

Confirmations :

- aucun fichier `common/` n'a ete modifie ;
- aucun fichier `events/` n'a ete modifie ;
- aucun fichier `localization/` n'a ete modifie ;
- aucun fichier `map_data/` n'a ete modifie ;
- aucun fichier gameplay n'a ete copie depuis le hotfix ou la vanilla ;
- aucun merge, stash pop ou commit n'a ete effectue ;
- `law_frontier_colonization` n'a pas ete modifiee ;
- NAVY, ADMIN, BIC gameplay et le contenu MARATH courant n'ont pas ete modifies ;
- le stash MARATH est reste intact.
