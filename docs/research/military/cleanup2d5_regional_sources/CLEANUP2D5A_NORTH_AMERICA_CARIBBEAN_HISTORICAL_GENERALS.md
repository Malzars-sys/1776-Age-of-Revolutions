# CLEANUP-2D-5A — HISTORICAL GENERALS 1776 — NORTH AMERICA & CARIBBEAN

## Statut du livrable

**Phase : recherche historique uniquement.**  
**Aucune modification gameplay effectuée. Aucun commit. Aucun push.**  
**Date de référence absolue : 1776-01-01.**  
**Dépôt audité : `Malzars-sys/1776-Age-of-Revolutions`.**  
**Branche : `cleanup-post-release`.**  
**Snapshot Git utilisé : `66ed0fc4ef838a54a19810496a5b7d005fde120d` — `Implement historical and procedural starting generals for 1776`.**

Ce rapport accompagne `GENERALS_1776_NORTH_AMERICA_CARIBBEAN_IMPLEMENTATION.csv`. Le CSV est le registre de décision : **une ligne et une seule par formation terrestre incluse dans le périmètre**.

---

## 1. Résultat exécutif

L’audit du dépôt et des sources historiques aboutit à **10 formations terrestres** pertinentes pour l’Amérique du Nord et les Caraïbes au démarrage.

Décision proposée :

| record_id | Tag | Formation | HQ | Décision | Candidat |
|---|---|---|---|---|---|
| GEN1776-018 | FRA | `cleanup2d3b_fra_land_4` | `region_central_america` | USE_HISTORICAL_GENERAL | Vital-Auguste de Grégoire, comte de Nozières |
| GEN1776-019 | GBR | `cleanup2d3b_gbr_land_2` | `region_atlantic_coast` | USE_HISTORICAL_GENERAL | William Howe |
| GEN1776-022 | GBR | `cleanup2d3b_gbr_land_3` | `region_central_america` | **KEEP_PROCEDURAL** | Aucun candidat suffisamment défendable |
| GEN1776-067 | SPA | `cleanup2d3b_spa_land_3` | `region_central_america` | USE_HISTORICAL_GENERAL | José Francisco Antonio Solano y Bote |
| GEN1776-087 | USA | `cleanup2d3b_usa_land_1` | `region_atlantic_coast` | USE_HISTORICAL_GENERAL | George Washington |
| GEN1776-088 | HAI | `ArmeeIndigene` | `region_central_america` | USE_HISTORICAL_GENERAL | Victor-Thérèse Charpentier d’Ennery |
| GEN1776-089 | CUB | `MiliciasdeCuba` | `region_central_america` | USE_HISTORICAL_GENERAL | Felipe de Fonsdeviela y Ondeano |
| GEN1776-090 | PCO | `MiliciasDiciplinadas` | `region_central_america` | USE_HISTORICAL_GENERAL | Miguel de Muesas |
| GEN1776-091 | HBC | `cleanup2d3b_hbc_land_1` | `region_canada` | **KEEP_PROCEDURAL** | Aucun commandement militaire terrestre défendable |
| GEN1776-092 | MKT | `cleanup2d3b_mkt_land_1` | `region_central_america` | USE_HISTORICAL_GENERAL | Tempest, « General » miskito |

**Bilan : 8 profils historiques retenus, 2 formations conservées procédurales.**

---

## 2. Périmètre exact issu du dépôt

### 2.1 Fichiers de formations audités

Le périmètre ne peut pas être obtenu en lisant uniquement le fichier « North America ».

Les six formations locales sont dans :

- `common/history/military_formations/01_military_formations_north_america.txt`

Mais quatre formations coloniales supplémentaires appartenant à des puissances européennes sont créées dans :

- `common/history/military_formations/00_military_formations_europe.txt`

Elles sont incluses parce que leur **HQ et/ou leurs unités de départ sont explicitement nord-américains/caribéens**, même si leur pays est codé dans le fichier européen.

### 2.2 Les dix formations

1. FRA — `cleanup2d3b_fra_land_4` — HQ `region_central_america` — unités principales `STATE_WEST_INDIES`.
2. GBR — `cleanup2d3b_gbr_land_2` — HQ `region_atlantic_coast` — noyau d’unités `STATE_BERMUDA`.
3. GBR — `cleanup2d3b_gbr_land_3` — HQ `region_central_america` — unités `STATE_BAHAMAS`.
4. SPA — `cleanup2d3b_spa_land_3` — HQ `region_central_america` — noyau `STATE_WEST_INDIES`, avec un élément métropolitain.
5. USA — `cleanup2d3b_usa_land_1` — HQ `region_atlantic_coast` — armée abstraite couvrant plusieurs anciennes colonies.
6. HAI — `ArmeeIndigene` — HQ `region_central_america` — `STATE_HAITI`.
7. CUB — `MiliciasdeCuba` — HQ `region_central_america` — Cuba occidental/central/oriental.
8. PCO — `MiliciasDiciplinadas` — HQ `region_central_america` — Puerto Rico.
9. HBC — `cleanup2d3b_hbc_land_1` — HQ `region_canada` — une unité irrégulière au Manitoba.
10. MKT — `cleanup2d3b_mkt_land_1` — HQ `region_central_america` — une unité irrégulière dans `STATE_NICARAGUA`.

### 2.3 Tags voisins sans formation terrestre de départ à ajouter

Le dépôt définit ou connaît de nombreux autres tags nord-américains/centraméricains : CAN, QUE, NEW, NBS, NVS, ONT, MEX, DOM, etc. Ils **ne reçoivent pas automatiquement une ligne** dans ce livrable : le critère est l’existence d’une formation terrestre de départ réellement créée dans l’état audité du mod.

L’audit global des scripts de formations n’a pas révélé d’autre armée de départ appartenant au périmètre qui doive être ajoutée au CSV.

---

## 3. Méthodologie

### 3.1 Filtre chronologique

Le test est strict :

> Un profil n’est admissible que s’il est vivant et déjà officier/commandant militaire pertinent **au plus tard le 1776-01-01**.

Une nomination plus tardive en 1776 ne répare pas un échec au filtre.

### 3.2 Filtre fonctionnel

Les fonctions suivantes ne suffisent pas à elles seules :

- gouverneur ;
- administrateur colonial ;
- responsable de compagnie ;
- souverain ;
- homme politique ;
- amiral.

Pour un gouverneur/capitaine général, il faut des indices indépendants que la fonction comprend bien un **commandement militaire terrestre**, l’administration de troupes, milices, fortifications ou défense de territoire.

Pour un officier naval, une preuve distincte de commandement/office terrestre est impérative.

### 3.3 Types de mapping employés

- `FORMATION_COMMAND` : commandement historiquement proche de la formation elle-même.
- `THEATRE_COMMAND` : commandement d’un théâtre plus vaste auquel la formation du mod est rattachée.
- `HIGHER_COMMAND_ABSTRACTION` : la formation du jeu agrège des forces placées sous un haut commandement réel.
- `MILITARY_OFFICEHOLDER` : titulaire d’un office militaire territorial/colonial pertinent.
- `COLLECTIVE_HIGH_COMMAND` : structure collective plutôt qu’un individu.
- `NO_DEFENSIBLE_MAPPING` : aucune identité ne justifie raisonnablement le remplacement.

### 3.4 Règle sur les noms de formations

Les noms tels que `cleanup2d3b_fra_land_4`, `ArmeeIndigene` ou `cleanup2d3b_spa_land_3` sont des constructions du mod.

**Aucun mapping de ce rapport ne prétend que ces formations existaient littéralement en 1776 sous ces noms, cette taille ou cette composition.**

### 3.5 Dates de naissance

Aucune date n’est complétée par convention.

- année seule connue → `YEAR`;
- date approximative/non confirmée → `UNKNOWN`;
- aucune donnée fiable → `UNKNOWN`.

Le cas Miguel de Muesas est volontairement conservateur : le « 1715 » souvent repris reste non confirmé, donc le CSV ne le transforme pas en `1715-01-01`.

---

# 4. Audit formation par formation

## 4.1 FRA — `cleanup2d3b_fra_land_4`

### Décision
**USE_HISTORICAL_GENERAL — Vital-Auguste de Grégoire, comte de Nozières**

### Pourquoi il est admissible
Les catalogues BnF/CCFr identifient explicitement Nozières comme :

- **maréchal de camp** ;
- **commandant général des îles françaises du Vent** ;
- gouverneur colonial dans les Antilles françaises.

Un numéro contemporain du *Mercure de France* de janvier 1772 annonce que le Roi l’a nommé commandant général des îles du Vent. Sa présence dans l’office est donc antérieure de plusieurs années au 1er janvier 1776.

### Mapping
`THEATRE_COMMAND`

La formation du mod concentre des unités dans les West Indies mais comporte aussi un élément métropolitain. Nozières est donc un excellent commandant du **théâtre antillais**, pas le commandant littéral d’une unité identique au script.

### Identité
- Nom : Vital-Auguste de Grégoire, comte de Nozières.
- Naissance : **UNKNOWN** dans ce livrable.
- Décès : **UNKNOWN** dans ce livrable.
- Rang : maréchal de camp.
- Office : commandant général des îles françaises du Vent.
- Actif au 1776-01-01 : **oui**.

La date « 1715 » apparaît dans des listes tertiaires mais n’a pas été élevée au rang de donnée de naissance définitive.

### Candidats rejetés
- **Robert d’Argout** : successeur en 1776, mais après la date absolue.
- **François-Claude-Amour de Bouillé** : gouverneur général à partir de 1777, donc inadmissible.

### Sources principales
- BnF/CCFr, correspondance des administrateurs de la Martinique :  
  https://ccfr.bnf.fr/portailccfr/jsp/index_view_direct_anonymous.jsp?record=eadcgm%3AEADC%3AMAR020130
- BnF/CCFr, Nozières « maréchal de camp », gouverneur de Guadeloupe :  
  https://ccfr.bnf.fr/portailccfr/ark:/16871/004MAR011103
- *Mercure de France*, janvier 1772, annonce de nomination :  
  https://bureaudumercure.org/mercure/node/1044875

---

## 4.2 GBR — `cleanup2d3b_gbr_land_2`

### Décision
**USE_HISTORICAL_GENERAL — William Howe**

CLEANUP-2D-4 a déjà fait le bon choix d’identité.

### Pourquoi il est admissible
Howe est déjà commandant en chef des forces terrestres britanniques en Amérique du Nord à l’automne 1775.

Le 1er janvier 1776 il exerce donc le commandement depuis plusieurs mois.

### Mapping
`THEATRE_COMMAND`

La formation du mod est centrée sur l’Atlantique/Bermudes et ne correspond pas à une formation historique précise de Howe. En revanche elle fait partie du théâtre nord-américain que Howe commande.

### Profil
- William Howe, 5th Viscount Howe.
- Naissance : **10 août 1729** — précision `DAY`.
- Lieu exact de naissance : **non confirmé par les sources prioritaires consultées**.
- Association familiale : Langar Hall, Nottinghamshire.
- Rang/office : Major-General, Commander-in-Chief of British land forces in North America.
- Commandement : octobre 1775 – mai 1778.
- Actif au 1776-01-01 : **oui**.
- Décès : 12 juillet 1814.

Le CSV marque `STATE_MIDLANDS` comme **tentatif**, uniquement à partir de l’association Nottinghamshire ; il ne transforme pas Langar Hall en lieu de naissance prouvé.

### Portrait
Le National Portrait Gallery conserve un mezzotint publié en 1778.

### Sources
- The National Archives, guide des opérations de l’armée britannique.
- George Washington’s Mount Vernon, *Sir William Howe* :  
  https://www.mountvernon.org/library/digitalhistory/digital-encyclopedia/article/sir-william-howe
- National Portrait Gallery :  
  https://www.npg.org.uk/collections/search/person/mp124228/william-howe-5th-viscount-howe

---

## 4.3 GBR — `cleanup2d3b_gbr_land_3` — Bahamas

### Décision
**KEEP_PROCEDURAL**

### Principal candidat étudié puis rejeté : Montfort Browne
Montfort Browne est gouverneur des Bahamas et gère la défense de New Providence, ce qui en fait au premier regard un excellent candidat.

Mais le filtre imposé par ce projet interdit précisément de convertir automatiquement un gouverneur.

Une preuve éditoriale très forte tranche le cas : dans sa lettre du 21 septembre 1776 à Washington, William Howe décrit Browne comme **n’étant plus dans la ligne militaire**. L’annotation de *Founders Online* précise que Browne avait quitté le 35th Regiment of Foot comme lieutenant en demi-solde à la fin de la guerre de Sept Ans.

Son futur retour dans les armes ne sauve pas sa candidature :
- il devient plus tard commandant loyaliste ;
- son grade de brigadier loyaliste est de **1777**.

Ces faits sont postérieurs au 1776-01-01.

### Conclusion
Le gouverneur peut avoir supervisé matériellement des forts et des magasins sans être un officier terrestre actif admissible.

`NO_DEFENSIBLE_MAPPING` → `KEEP_PROCEDURAL`.

### Sources
- Founders Online, Howe à Washington, 21 septembre 1776 :  
  https://founders.archives.gov/documents/Washington/03-06-02-0283
- Naval History and Heritage Command, opération de New Providence :  
  https://www.history.navy.mil/browse-by-topic/ships/ships-of-sail/alfred.html
- Founders Online, capture de Browne :  
  https://founders.archives.gov/documents/Washington/03-04-02-0038

---

## 4.4 SPA — `cleanup2d3b_spa_land_3`

### Décision
**USE_HISTORICAL_GENERAL — José Francisco Antonio Solano y Bote**

### Cas limite : officier de marine
Ce profil a été soumis à un filtre renforcé car Solano est avant tout un **marino**.

Il n’est **pas** admissible simplement parce qu’il est gouverneur ou officier naval.

### Preuve qui rend le mapping acceptable
Les archives espagnoles et dominicaines apportent une seconde couche :

- PARES le montre en 1775-1777 comme **Brigadier de Marina et gouverneur de Santo Domingo**, demandant son avancement à *Jefe de Escuadra* ;
- les fonds de l’Archivo General de la Nación dominicain le décrivent comme **Governor and Captain General** et documentent des décisions relatives aux troupes, à la frontière, à la défense, aux armes et aux garnisons.

Il existe donc une responsabilité terrestre/territoriale indépendante de son rang naval.

### Données biographiques
- Nom complet : José Francisco Antonio Solano y Bote.
- Naissance : **6 mars 1726**, Zorita (Cáceres).
- Mapping naissance : `STATE_EXTREMADURA`.
- Décès : **24 mars 1806**, Madrid.
- Rang au 1776-01-01 : **Brigadier de Marina**, pas encore Jefe de Escuadra.
- Office : gouverneur et capitaine général de Santo Domingo.
- Actif : **oui**.

### Mapping
`MILITARY_OFFICEHOLDER`

Confiance de formation : **MEDIUM**.

La formation espagnole du mod est une abstraction large des forces espagnoles caribéennes et comporte même un élément galicien. Solano est défendable comme haut officier militaire territorial de l’Hispaniola espagnole, pas comme commandant littéral de toute la pile du script.

### Sources
- Real Academia de la Historia / Historia Hispánica, Solano y Bote.
- PARES, dossier d’avancement 1775-1777.
- Archivo General de la Nación, République dominicaine, fonds Solano.

---

## 4.5 USA — `cleanup2d3b_usa_land_1`

### Décision
**USE_HISTORICAL_GENERAL — George Washington**

C’est un cas à très haute confiance.

### Situation au 1er janvier 1776
La commission de Washington comme « General and Commander in Chief » date du **19 juin 1775**. Il prend effectivement le commandement de l’armée à Cambridge le 3 juillet 1775.

Il est donc incontestablement en poste au 1776-01-01.

### Données historiques
- George Washington.
- Naissance : **22 février 1732**.
- Lieu : **Pope’s Creek, Westmoreland County, Colony of Virginia**.
- Mapping : `STATE_VIRGINIA`.
- Décès : **14 décembre 1799**.
- Religion : Anglican → recommandation Victoria 3 `protestant`.
- Culture : `dixie` reste un mapping de gameplay raisonnable pour un Anglo-Virginien né dans la colonie de Virginie, mais le terme est évidemment anachronique comme auto-identification de 1732/1776.
- IG recommandé pour le personnage militaire : `ig_armed_forces`.
- Origine sociale : planteur/gentry de Virginie ; `ig_landowners` est donc un contexte secondaire plausible, mais il ne doit pas être restauré automatiquement comme choix principal.
- Idéologie : **aucune idéologie mécanique précise recommandée par défaut**.
- Trait biographique solide : **surveyor** / expérience d’arpenteur. Les anciens traits militaires doivent être ré-audités un par un.

### Mapping
`HIGHER_COMMAND_ABSTRACTION`

L’armée du script agrège plusieurs États/colonies ; Washington commande effectivement l’ensemble continental, ce qui justifie un mapping de haut commandement.

---

# 5. Washington — audit DNA obligatoire

## 5.1 Constat dépôt

Le dépôt contient toujours :

`common/dna_data/00_washington_traitor.txt`

avec :

`dna_washington_traitor`

Un ancien template `USA_washington_traitor` utilisait :

`dna = dna_washington_traitor`

Dans l’état actuel CLEANUP-2D-4, Washington est créé directement comme personnage historique dans le script de formation, **sans réassignation de ce DNA**. Il reçoit donc une apparence procédurale.

## 5.2 Décision obligatoire dans le CSV

Le CSV contient explicitement :

- `existing_mod_dna = YES`
- `dna_id = dna_washington_traitor`
- `recommended_action = REUSE_EXISTING_MOD_DNA`

## 5.3 Ce qui doit être réutilisé
**Le DNA uniquement.**

## 5.4 Ce qui ne doit PAS être restauré aveuglément

L’ancien template ne constitue pas une autorité historique pour :

- date de naissance ;
- culture ;
- religion ;
- IG ;
- idéologie ;
- traits ;
- état d’origine.

Ces champs ont été réévalués séparément.

### Réévaluation
- naissance : `1732-02-22`, précision `DAY`;
- lieu : Pope’s Creek, Virginie;
- state : `STATE_VIRGINIA`;
- religion : `protestant` comme abstraction de l’anglicanisme;
- culture : `dixie` défendable comme convention Victoria 3, pas comme étiquette historique;
- IG : `ig_armed_forces` recommandé pour sa fonction militaire, avec contexte social de planteur/gentry;
- idéologie : `NO_SPECIFIC_IDEOLOGY`;
- traits : ne pas recopier en bloc l’ancien template.

### Références dépôt
- DNA actuel :  
  https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/cleanup-post-release/common/dna_data/00_washington_traitor.txt
- Template USA actuel :  
  https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/cleanup-post-release/common/character_templates/country_usa.txt
- Ancienne version du template montrant `USA_washington_traitor` et son DNA :  
  https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/1e374f2f40252d229bc249600e3cbbe26085122d/common/character_templates/country_usa.txt

### Sources historiques
- Founders Online, commission de Washington :  
  https://founders.archives.gov/documents/Washington/03-01-02-0004
- Library of Congress, guide de la commission :  
  https://guides.loc.gov/washington-commission
- Mount Vernon, données biographiques :  
  https://www.mountvernon.org/george-washington/george-washington-key-facts

---

## 4.6 HAI — `ArmeeIndigene`

### Décision
**USE_HISTORICAL_GENERAL — Victor-Thérèse Charpentier d’Ennery**

### Avertissement sur la formation
`ArmeeIndigene` est un nom de formation anachronique pour le Saint-Domingue de 1776.

Ce rapport **ne valide pas le nom gameplay**. Il répond uniquement à la question : quel commandant réel peut représenter le haut commandement terrestre sur le territoire le 1er janvier 1776 ?

### Preuve exceptionnelle
Une ordonnance de Port-au-Prince du **23 octobre 1775**, conservée/numérisée dans la Brown Haiti Collection de l’Université de Chicago, donne directement les titres de d’Ennery :

- maréchal des camps et armées du Roi ;
- inspecteur-général d’infanterie ;
- directeur-général des troupes, fortifications, artillerie et milices de toutes les colonies ;
- gouverneur-lieutenant-général des Isles françaises Sous le Vent.

C’est précisément le type de preuve qui permet de distinguer un véritable haut responsable militaire d’un simple administrateur.

### Profil
- Victor-Thérèse Charpentier d’Ennery.
- Naissance : **24 mars 1732**, Paris.
- Mapping : `STATE_ILE_DE_FRANCE`.
- Décès : **13 décembre 1776**, Saint-Domingue.
- Actif au 1776-01-01 : **oui**.

Le Louvre conserve le monument du cœur réalisé par Houdon en 1781, avec portrait en médaillon et inscription datée du 13 décembre 1776. C’est une bonne référence visuelle, même si elle est posthume.

### Mapping
`MILITARY_OFFICEHOLDER`

### Candidats révolutionnaires rejetés
Toussaint Louverture et Jean-Jacques Dessalines sont des figures militaires futures. Ils ne satisfont pas le filtre du 1er janvier 1776.

### Sources
- Brown Haiti Collection, University of Chicago :  
  https://artfl-permalink.uchicago.edu/permalinks/brownhaiti
- Louvre :  
  https://collections.louvre.fr/ark:/53355/cl010094527
- Ennery, synthèse biographique locale issue d’un travail d’archives :  
  https://ennery.fr/decouvrir/victor-therese-charpentier/

---

## 4.7 CUB — `MiliciasdeCuba`

### Décision
**USE_HISTORICAL_GENERAL — Felipe de Fonsdeviela y Ondeano**

C’est l’un des mappings les plus solides du lot.

### Profil
PARES identifie Felipe Fonsdeviela :

- né en **1725** à Zaragoza ;
- mort en **1784** à Madrid ;
- militaire, noble et diplomate ;
- inspecteur d’infanterie en Nouvelle-Espagne en 1767 ;
- **mariscal de campo en 1770** ;
- gouverneur et capitaine général de Cuba **1771-1777**.

### Mapping
`MILITARY_OFFICEHOLDER`

Les dossiers PARES associés indexent directement :
- artillerie ;
- cavalerie ;
- infanterie ;
- troupes ;
- officiers militaires ;
- fortifications ;
- défense ;
- rapports militaires.

Cela fournit une preuve indépendante que « capitaine général » est ici une fonction militaire réelle et pas seulement un titre administratif.

### Naissance
Seulement l’année **1725** est utilisée.

Aucune transformation en `1725-01-01`.

### State de naissance
Zaragoza → `STATE_ARAGON`.

### Portrait
PARES fournit une image dans la notice d’autorité.

### Sources
- PARES, autorité Fonsdeviela :  
  https://pares.mcu.es/ParesBusquedas20/catalogo/autoridad/143953
- PARES, documentation militaire/défense :  
  https://pares.mcu.es/ParesBusquedas20/catalogo/description/13351152
- PARES, inventaires de Capitanías Generales :  
  https://pares.mcu.es/ParesBusquedas20/catalogo/description/13317310/imprimir

---

## 4.8 PCO — `MiliciasDiciplinadas`

### Décision
**USE_HISTORICAL_GENERAL — Miguel de Muesas**

### Adéquation avec la formation
Le titre même de l’ouvrage universitaire d’Altagracia Ortiz fixe la période :

> *Miguel de Muesas, Governor of Puerto Rico, 1769-76*

La table des matières distingue :
- l’office de Governor and Captain General ;
- sa **Military and Political Administration** ;
- et l’index fait apparaître *Milicias Disciplinadas*.

Pour cette formation, l’adéquation fonctionnelle est particulièrement forte.

### Profil
- Miguel de Muesas.
- Origine : Trujillo, Extremadura.
- Naissance : souvent donnée **vers 1715**, mais non confirmée.
- CSV : `ca. 1715 (unconfirmed)` + `birth_date_precision = UNKNOWN`.
- Décès : **26 juillet 1783** à Poyos.
- Rang attesté dans son testament : **coronel de infantería de los Reales Ejércitos**.
- Office : gouverneur et capitaine général de Puerto Rico.
- Religion : son testament professe explicitement la foi catholique romaine.

### Mapping
`MILITARY_OFFICEHOLDER`

### State
Trujillo, Extremadura → `STATE_EXTREMADURA`.

### Successeur
Un successeur intervenant plus tard en 1776 n’est pas admissible au 1er janvier et n’a pas été substitué à Muesas.

### Sources
- Altagracia Ortiz, Fairleigh Dickinson University Press, 1983 :  
  https://books.google.com/books/about/Eighteenth_century_Reforms_in_the_Caribb.html?id=z0hHaBQF2z8C
- CHDE Trujillo, avec transcription du testament de 1782 :  
  https://chdetrujillo.com/alguna-noticia-sobre-el-militar-trujillano-don-miguel-de-muesas-1715-1783-gobernador-de-puerto-rico-durante-el-reinado-de-carlos-iii/
- EnciclopediaPR, chronologie des gouverneurs :  
  https://enciclopediapr.org/content/cronologia-de-gobernadores-del-siglo-xviii/

---

## 4.9 HBC — `cleanup2d3b_hbc_land_1`

### Décision
**KEEP_PROCEDURAL**

### Samuel Hearne — rejeté
Hearne est un personnage historique majeur et tentant pour la HBC.

Mais il ne faut pas confondre :
- « land service » au sens de service terrestre de la compagnie ;
- et commandement d’une armée.

Le *Dictionary of Canadian Biography* le décrit comme explorateur, trafiquant et officier de compagnie.

Il fonde Cumberland House en 1774 comme **poste de traite**.

Il est ensuite nommé chief au Prince of Wales Fort, mais **n’y arrive que le 17 janvier 1776**, donc après la date absolue.

Plus encore, la même biographie précise qu’en 1782 le fort :
- ne dispose pas de garnison militaire ;
- est tenu par un effectif civil.

Cela montre pourquoi transformer automatiquement un chef de poste HBC en général serait historiquement trompeur.

### Matthew Cocking — rejeté
Même problème : employé/trafiquant/officier de poste de la compagnie, sans preuve d’un commandement d’armée terrestre au 1776-01-01.

### Ferdinand Jacobs — rejeté
Il est un dirigeant HBC important, mais il a pris sa retraite en 1775.

### Conclusion
La petite formation HBC du mod est une abstraction gameplay. Aucun nom n’atteint le seuil.

`NO_DEFENSIBLE_MAPPING` → `KEEP_PROCEDURAL`.

### Sources
- Dictionary of Canadian Biography, Samuel Hearne :  
  https://www.biographi.ca/en/bio/hearne_samuel_4F.html?revision_id=6805
- Parks Canada, Cumberland House.
- Dictionary of Canadian Biography, Ferdinand Jacobs :  
  https://www.biographi.ca/en/bio/jacobs_ferdinand_4E.html

---

## 4.10 MKT — `cleanup2d3b_mkt_land_1`

### Décision
**USE_HISTORICAL_GENERAL — Tempest**

### Pourquoi ce cas est important
Le piège aurait été de prendre automatiquement le **roi miskito** et d’en faire un général.

La recherche permet mieux : la structure politique miskito possède réellement un office distinct intitulé **General**.

Michael D. Olien, dans *Ethnohistory* 45/2 (1998), reconstruit trois lignes de succession distinctes : General, Governor et Admiral.

Pour la période qui nous intéresse, la ligne des Generals donne :

**Tempest — ca. 1764 à ca. 1785.**

### Preuve militaire
La transcription de l’article rapporte :
- résidence de Tempest à Brewers Lagoon, près du río Patuca ;
- des **troupes de Tempest stationnées à Río Negro en 1764** ;
- une démonstration de force devant l’envoyé espagnol Luis Diez Navarro ;
- en 1776, un rapport espagnol l’appelle « Captain Tempest » et note les armes/poudre distribuées à ses gens.

On a donc beaucoup mieux qu’un titre décoratif.

### Données inconnues
La biographie individuelle reste pauvre :
- date de naissance : inconnue ;
- lieu de naissance : inconnu ;
- nom complet : non sécurisé ;
- religion personnelle : non sécurisée.

Le CSV conserve donc ces inconnues.

`Tempest` est traité comme le nom historique enregistré, avec indication de mononyme/nom complet non démontré.

### Mapping
`MILITARY_OFFICEHOLDER`

Confiance identité : **MEDIUM-HIGH**.  
Confiance mapping formation : **MEDIUM**.

Le jeu place la formation dans `STATE_NICARAGUA`, tandis que les zones documentées autour de Río Negro, Brewers Lagoon et Patuca appartiennent à un espace miskito plus large chevauchant les actuels Honduras/Nicaragua. Il ne faut pas prétendre à une identité unité-zone parfaite.

### Culture et religion
- culture recommandée : `miskito`;
- religion : **UNKNOWN** dans ce livrable.

La présence d’influences chrétiennes/britanniques dans les élites miskito ne suffit pas à attribuer une religion individuelle à Tempest.

### Sources
- Michael D. Olien, *General, Governor, and Admiral: Three Miskito Lines of Succession*, *Ethnohistory* 45/2 (1998), JSTOR :  
  https://www.jstor.org/stable/i220998
- Transcription de la section « Generales » :  
  https://pueblosoriginarios.com/textos/miskito/generales.html
- Présentation et structure de l’article :  
  https://pueblosoriginarios.com/textos/miskito/lineas_sucesion.html

---

# 6. Candidats rejetés — synthèse

| Formation / territoire | Candidat rejeté | Raison |
|---|---|---|
| GBR Bahamas | Montfort Browne | Gouverneur, mais explicitement « no longer in the military Line » ; grade militaire loyaliste futur en 1777. |
| HBC | Samuel Hearne | HBC trader/explorer/company chief, pas commandant d’armée ; arrivée au nouveau poste seulement le 17 Jan 1776 ; fort sans garnison militaire. |
| HBC | Matthew Cocking | Officier de compagnie/trafiquant ; absence de preuve de commandement terrestre militaire. |
| HBC | Ferdinand Jacobs | Retiré de la HBC en 1775. |
| FRA Antilles | Robert d’Argout | Succession plus tard en 1776 → hors filtre. |
| FRA Antilles | François-Claude-Amour de Bouillé | Gouverneur général à partir de 1777 → hors filtre. |
| PCO | successeur de Muesas en 1776 | Nomination/prise de fonction postérieure au 1er janvier → hors filtre. |
| HAI/Saint-Domingue | Toussaint Louverture | Futur commandant révolutionnaire ; pas commandant militaire admissible au 1776-01-01. |
| HAI/Saint-Domingue | Jean-Jacques Dessalines | Même raison chronologique. |
| MKT | Roi miskito | Rejet de principe : souverain non converti automatiquement ; un véritable office distinct de General existe et est occupé par Tempest. |

---

# 7. DNA, templates et personnages déjà présents

## 7.1 Recherche dans le mod

Audit ciblé réalisé dans :
- `common/dna_data/`;
- `common/character_templates/`;
- `common/history/characters/`;
- `common/history/military_formations/`;
- recherche globale des noms dans le dépôt.

### Résultat
**Un seul DNA historique réutilisable retrouvé parmi les 8 profils retenus : Washington.**

| Profil | Personnage déjà créé dans CLEANUP-2D-4 | Template actuel dédié | DNA mod dédié |
|---|---:|---:|---:|
| George Washington | OUI | NON — ancien `USA_washington_traitor` seulement | **OUI — `dna_washington_traitor`** |
| William Howe | OUI | NON | NON |
| Vital-Auguste de Nozières | NON | NON | NON |
| José Solano y Bote | NON | NON | NON |
| Victor-Thérèse d’Ennery | NON | NON | NON |
| Felipe de Fonsdeviela | NON | NON | NON |
| Miguel de Muesas | NON | NON | NON |
| Tempest | NON | NON | NON |

Les recherches dépôt sur Fonsdeviela, Nozières, Ennery et Muesas n’ont trouvé aucun personnage/template/DNA existant. Une recherche Solano n’a remonté qu’un contexte sans rapport avec un template de ce personnage. Howe est actuellement créé directement dans le script de formations, sans DNA dédié.

---

# 8. Portraits / travail DNA futur

## Références disponibles

### George Washington
**Oui, très forte disponibilité.**  
Charles Willson Peale peint Washington en 1776 ; le mod possède déjà un DNA dédié.

### William Howe
**Oui.**  
National Portrait Gallery : mezzotint publié en 1778.

### Victor-Thérèse d’Ennery
**Oui.**  
Portrait en médaillon dans le monument de Houdon, 1781, Louvre. Posthume mais institutionnellement documenté.

### Felipe de Fonsdeviela
**Oui.**  
Image associée à la notice d’autorité PARES.

### José Solano y Bote
**Oui.**  
Référence biographique/portrait via Real Academia de la Historia / Historia Hispánica.

### Nozières
**Pas de portrait suffisamment vérifié dans cet audit.**

### Miguel de Muesas
**Pas de portrait suffisamment vérifié dans cet audit.**

### Tempest
**Pas de portrait vérifié.**

### Conséquence
Si l’objectif futur est de supprimer l’apparence procédurale pour tous les historiques retenus :
- Washington : **réemploi immédiat possible du DNA existant** ;
- les **7 autres profils historiques retenus** n’ont pas de DNA dédié retrouvé dans le dépôt et nécessitent soit :
  - un futur travail DNA ;
  - soit une apparence procédurale conservatoire jusqu’à ce travail.

---

# 9. Recommandations culture / religion / IG / idéologie

Ces champs sont **des recommandations d’implémentation Victoria 3**, pas une prétention à réduire l’identité historique à une clé de jeu.

## Washington
- culture : `dixie` comme abstraction de Virginie ;
- religion : `protestant` / Anglican ;
- IG : `ig_armed_forces`, avec gentry/planter en contexte secondaire ;
- idéologie : aucune idéologie mécanique précise sans preuve supplémentaire.

## Howe
- culture : `british`;
- religion : `protestant` proposé à confiance moyenne ;
- IG : `ig_armed_forces`;
- idéologie : aucune spécifique.

## Nozières / d’Ennery
- culture : `french`;
- religion : `catholic` comme recommandation raisonnable, mais ne pas sur-vendre une preuve individuelle si elle n’est pas fournie ;
- IG : `ig_armed_forces`;
- idéologie : aucune spécifique.

## Fonsdeviela / Muesas / Solano
- culture : `spanish`;
- religion : `catholic`; Muesas est directement attesté par son testament ;
- IG : `ig_armed_forces`;
- idéologie : aucune spécifique.

## Tempest
- culture : `miskito`;
- religion : `UNKNOWN`;
- IG : `ig_armed_forces` uniquement comme abstraction de son office politico-militaire ;
- idéologie : aucune spécifique.

---

# 10. Traits : garde-fous

Le rapport ne demande pas de créer des traits ni de modifier le gameplay.

Les suggestions CSV sont des **axes biographiques**, à convertir éventuellement plus tard vers des IDs de traits déjà disponibles après audit des fichiers de jeu.

À éviter :
- transformer une fonction de gouverneur en trait de commandement sans preuve ;
- attribuer un trait « offensive planner » simplement parce qu’une personne a gagné une bataille ;
- restaurer automatiquement les traits d’anciens templates ;
- fabriquer des traits pour remplir des cases.

---

# 11. Incertitudes conservées volontairement

1. **Nozières — naissance** : non stabilisée par une source prioritaire assez bonne → `UNKNOWN`.
2. **William Howe — lieu exact de naissance** : l’association à Langar Hall/Nottinghamshire est solide pour sa famille, pas suffisante pour inventer une localité de naissance → état V3 marqué `TENTATIVE`.
3. **Muesas — année 1715** : probablement correcte, mais explicitement non confirmée dans la source utilisée → précision `UNKNOWN`.
4. **Tempest — identité civile complète** : office et activité militaire solides, biographie personnelle lacunaire.
5. **Solano — nature du rôle** : conservé comme `MILITARY_OFFICEHOLDER`, jamais présenté comme général terrestre de carrière ; son admission repose sur l’évidence indépendante de commandement territorial/troupes.
6. **HAI / `ArmeeIndigene`** : nom de formation anachronique ; le mapping d’Ennery vise le commandement réel de Saint-Domingue, pas cette appellation.
7. **Formations impériales FRA/SPA/GBR** : ce sont des agrégations gameplay ; une confiance de mapping inférieure à l’identité est normale.

---

# 12. Statistiques finales

- **Formations terrestres auditées : 10**
- **Candidats historiques retenus : 8**
- **Formations restant procédurales : 2**
- **DNA existants retrouvés pour les profils retenus : 1**
- **Profils historiques retenus nécessitant un futur travail DNA : 7**
- **Personnages historiques déjà créés par CLEANUP-2D-4 dans ce périmètre : 2** — George Washington, William Howe
- **Nouveaux remplacements historiques proposés par cette recherche : 6** — Nozières, Solano, d’Ennery, Fonsdeviela, Muesas, Tempest

---

# 13. Contrôle de complétude CSV

Validation effectuée lors de la génération :

- nombre de lignes de données : **10** ;
- nombre de `record_id` uniques : **10** ;
- décisions `USE_HISTORICAL_GENERAL` : **8** ;
- décisions `KEEP_PROCEDURAL` : **2** ;
- ligne Washington :
  - `existing_mod_dna = YES` ;
  - `dna_id = dna_washington_traitor` ;
  - `recommended_action = REUSE_EXISTING_MOD_DNA`.

**Chaque formation terrestre du périmètre possède exactement une décision dans le CSV.**

---

# 14. Références dépôt principales

- Snapshot de référence :  
  https://github.com/Malzars-sys/1776-Age-of-Revolutions/commit/66ed0fc4ef838a54a19810496a5b7d005fde120d
- Formations North America :  
  https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/cleanup-post-release/common/history/military_formations/01_military_formations_north_america.txt
- Formations Europe contenant les armées coloniales :  
  https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/cleanup-post-release/common/history/military_formations/00_military_formations_europe.txt
- DNA Washington :  
  https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/cleanup-post-release/common/dna_data/00_washington_traitor.txt
- Templates USA actuels :  
  https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/cleanup-post-release/common/character_templates/country_usa.txt

---

## Conclusion

Le périmètre permet de remplacer raisonnablement **six généraux procéduraux supplémentaires** par des identités historiques tout en conservant les deux choix déjà corrects de CLEANUP-2D-4, Washington et Howe.

Les deux refus sont significatifs :
- le **Bahamas britannique** montre pourquoi un gouverneur ne doit pas devenir général sans statut militaire actif ;
- la **Hudson’s Bay Company** montre pourquoi un responsable de compagnie ou de poste ne doit pas être assimilé à un commandant d’armée.

À l’inverse, les cas Fonsdeviela, Muesas, d’Ennery et Tempest disposent précisément des preuves d’office ou de commandement militaire territorial nécessaires.

**Aucune implémentation n’a été réalisée dans cette phase.**
