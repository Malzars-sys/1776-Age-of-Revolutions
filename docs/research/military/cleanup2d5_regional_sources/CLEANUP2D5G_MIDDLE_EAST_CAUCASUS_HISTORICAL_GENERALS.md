# CLEANUP-2D-5G — HISTORICAL GENERALS 1776 — MIDDLE EAST & CAUCASUS

**Projet :** *1776 – Age of Revolutions* — Victoria 3  
**Dépôt :** `Malzars-sys/1776-Age-of-Revolutions`  
**Branche auditée :** `cleanup-post-release`  
**Date de référence absolue :** **1776-01-01**  
**Statut :** **RECHERCHE HISTORIQUE UNIQUEMENT — AUCUNE IMPLÉMENTATION, AUCUN COMMIT, AUCUN PUSH**

---

## 1. Résultat exécutif

L’audit du dépôt donne **14 formations terrestres dans le périmètre effectif** de CLEANUP-2D-5G : 12 dans `04_military_formations_middle_east.txt`, auxquelles s’ajoutent les formations de **Circassie (`CIR`)** et de **Tchétchénie (`CHC`)** rangées dans le fichier européen.

Décision finale :

- **4 formations** ont un remplacement historique défendable ;
- **10 formations** doivent conserver un général procédural ;
- parmi les 4 remplacements, **2 seulement** utilisent `HIGHER_COMMAND_ABSTRACTION` ;
- aucune identité n’est créée à partir d’un simple titre de pacha, bey, wali, khan, gouverneur ou souverain ;
- aucune date de naissance inconnue n’est artificiellement transformée en date complète.

### Remplacements historiques recommandés

| Tag | Formation | Candidat | Classification | Décision | Confiance |
|---|---|---|---|---|---|
| IR1 | `cleanup2d3e_r1_ir1_land_1` | **Süleyman Ağa** | `THEATRE_COMMAND` | `IMPLEMENT_HISTORICAL` | Haute sur le commandement |
| PER | `cleanup2d3e_r1_per_land_1` | **Moḥammad Ṣādeq Khan Zand** | `FORMATION_COMMAND` | `IMPLEMENT_HISTORICAL` | Haute |
| DUR | `cleanup2d3e_r1_dur_land_1` | **Tīmūr Shah Dorrānī** | `HIGHER_COMMAND_ABSTRACTION` | `IMPLEMENT_HISTORICAL` | Moyenne-haute |
| HDJ | `cleanup2d3b_hdj_land_1` | **Sharīf Surūr ibn Musāʿid** | `HIGHER_COMMAND_ABSTRACTION` | `IMPLEMENT_HISTORICAL` | Moyenne-haute |

Les cas ottomans constituent le principal exemple où **remplacer un procédural serait moins historique** que le conserver : les quatre formations du mod sont des agrégats permanents que la structure militaire ottomane de 1776 ne reproduit pas directement.

---

## 2. Méthode et seuil d’admissibilité

Un candidat n’est retenu que si les conditions suivantes sont satisfaites :

1. il est vivant au **1er janvier 1776** ;
2. il occupe déjà à cette date une fonction militaire ou exerce un commandement documenté ;
3. un titre politique ou provincial ne suffit jamais à prouver le commandement ;
4. le lien entre le personnage et la formation Victoria 3 doit être défendable ;
5. `HIGHER_COMMAND_ABSTRACTION` n’est utilisé que lorsque la formation du mod condense réellement un système de forces historiques sans équivalent permanent moderne ;
6. lorsqu’une naissance n’est connue qu’à l’année, au calendrier hégirien, à la décennie ou pas du tout, cette imprécision est conservée ;
7. les personnages, DNA et templates préexistants du dépôt sont recherchés séparément de la décision historique : **un asset existant n’est pas une preuve historique**.

### Hiérarchie des classifications employées

- `FORMATION_COMMAND` : commandement direct de la force qui correspond raisonnablement à la formation du mod ;
- `THEATRE_COMMAND` : commandement militaire direct dans le théâtre représenté, sans équivalent exact de formation permanente ;
- `HIGHER_COMMAND_ABSTRACTION` : autorité militaire supérieure réellement documentée, utilisée uniquement parce que la formation V3 condense un système non permanent ;
- `COLLECTIVE_HIGH_COMMAND` : structure réellement collective/décentralisée ; le personnage unique serait artificiel ;
- `NO_DEFENSIBLE_MAPPING` : pas de correspondance individuelle suffisamment sûre.

---

## 3. Périmètre exact trouvé dans le dépôt

| # | Tag | Formation | HQ | Décision |
|---:|---|---|---|---|
| 1 | IR1 | `cleanup2d3e_r1_ir1_land_1` | `region_near_east` | **Süleyman Ağa** |
| 2 | TUR | `cleanup2d3b_tur_land_1` | `region_balkans` | Procédural |
| 3 | TUR | `cleanup2d3b_tur_land_2` | `region_balkans` | Procédural |
| 4 | TUR | `cleanup2d3b_tur_land_3` | `region_near_east` | Procédural |
| 5 | TUR | `cleanup2d3b_tur_land_4` | `region_near_east` | Procédural |
| 6 | OMA | `cleanup2d3e_r1_oma_land_1` | `region_greater_persia` | Procédural |
| 7 | PER | `cleanup2d3e_r1_per_land_1` | `region_greater_persia` | **Ṣādeq Khan Zand** |
| 8 | DUR | `cleanup2d3e_r1_dur_land_1` | `region_greater_persia` | **Tīmūr Shah** — HCA |
| 9 | DUR | `cleanup2d3e_r1_dur_land_2` | `region_greater_persia` | Procédural |
| 10 | ARB | `cleanup2d3e_r1_arb_land_1` | `region_greater_persia` | Procédural |
| 11 | HDJ | `cleanup2d3b_hdj_land_1` | `region_arabia` | **Surūr ibn Musāʿid** — HCA |
| 12 | ZAI | `cleanup2d3b_zai_land_1` | `region_arabia` | Procédural |
| 13 | CIR | `cleanup2d3e_r1_cir_land_1` | `region_russia` | Procédural / structure collective |
| 14 | CHC | `Murtazeki` | `region_russia` | Procédural / structure collective |

### Cas contrôlés mais hors CSV

**Crimée (`CRI`)** a été contrôlée parce que sa formation contient notamment un contingent du Kuban. Elle reste cependant une formation de l’architecture Europe orientale / mer Noire (`region_eastern_europe`) et doit rester dans le lot européen pour éviter un doublon inter-phase.

**Égypte** ne possède pas de formation `EGY` autonome dans l’architecture actuelle. Les États égyptiens sont incorporés aux formations `TUR`. Cela interdit de créer une ligne séparée dans le CSV : « une ligne par formation » implique qu’une formation absente ne doit pas être inventée.

Aucune formation indépendante géorgienne, arménienne ou de khanat azéri/caucasien distinct n’a été trouvée dans l’architecture de départ auditée. Une partie des territoires transcaucasiens apparaît dans la formation `PER`.

---

# 4. Dossiers des personnes retenues

## 4.1 IR1 — Süleyman Ağa

### Identité

- **Nom principal :** Süleyman Ağa
- **Variantes :** Sulaiman Agha, Soliman Aga ; plus tard **Büyük Süleyman Paşa / Sulayman Pasha the Great**
- **Naissance :** **inconnue** ; une littérature secondaire estime seulement les **années 1720**
- **`birth_date_precision` :** `UNKNOWN — DECADE_ESTIMATE_ONLY`
- **Lieu de naissance :** Caucase, localité inconnue
- **Polité de naissance :** indéterminée
- **State V3 :** `UNRESOLVED`
- **Décès :** **8 août 1802**

Il serait méthodologiquement incorrect de transformer l’estimation « années 1720 » en `1722.1.1` ou en toute autre date précise. L’ethnicité exacte n’est pas non plus suffisamment établie pour imposer « Georgian » ou « Circassian ».

### Fonction militaire au 1776-01-01

Süleyman est le **mütesellim de Bassora** et, surtout, le **commandant effectif de la défense de Bassora** contre l’armée zand. Lorimer indique que Bassora est investie le 7 avril 1775 et tient sous Süleyman Agha pendant plus d’un an. Le volume des Factory Records couvrant décembre 1775 et la suite contient également la correspondance avec « Soliman Aga the Mussaleem », ce qui confirme sa présence institutionnelle pendant la fenêtre exacte.

Ce n’est donc **pas** son titre administratif qui fonde la sélection : c’est son commandement militaire explicite et prolongé.

### Mapping

- **Classification :** `THEATRE_COMMAND`
- **Formation :** `cleanup2d3e_r1_ir1_land_1`
- **Décision :** `IMPLEMENT_HISTORICAL`
- **Justification :** la formation IR1 est une armée synthétique de l’Irak mamelouk ; le commandement de Bassora ne correspond pas à une formation permanente identique, mais représente le commandement militaire terrestre le mieux documenté du théâtre au 1er janvier 1776.

### Culture, religion, profil

- **Culture :** mamelouk caucasien ; origine ethnique exacte non résolue
- **Religion :** contexte sunnite ottoman très probable ; ne pas sur-spécifier si une preuve individuelle n’est pas disponible
- **Profil social :** élite mamelouke militaire et administrative de l’Irak ottoman

### Portrait / DNA / assets

- aucun portrait individuel contemporain authentifié n’a été validé ;
- aucun DNA/template de Süleyman Ağa n’a été trouvé ;
- le dépôt possède déjà **Omar Pasha** comme souverain historique de `IR1`, mais il s’agit d’une autre personne et son office de pacha ne remplace pas le commandement défensif de Süleyman.

### Sources principales

1. J. G. Lorimer, *Gazetteer of the Persian Gulf*, Qatar Digital Library — siège et commandement :  
   https://www.qdl.qa/en/archive/81055/vdc_100023575942.0x000059
2. Lorimer, capitulation et rôle personnel de Süleyman :  
   https://www.qdl.qa/en/archive/81055/vdc_100023575948.0x000011
3. TDV İslâm Ansiklopedisi, **Bağdat** — carrière ultérieure et décès :  
   https://islamansiklopedisi.org.tr/bagdat
4. India Office / British Library Factory Records, Basra 1775–1779 :  
   https://www.qdl.qa/archive/81055/vdc_100107757920.0x0000b3

---

## 4.2 PER — Moḥammad Ṣādeq Khan Zand

### Identité

- **Nom principal :** Moḥammad Ṣādeq Khan Zand
- **Variantes :** Ṣādeq Khan Zand, Sadeq Khan Zand, Sadiq Khan Zand, Muhammad Sadeq Khan Zand
- **Naissance :** **inconnue**
- **`birth_date_precision` :** `UNKNOWN`
- **Lieu de naissance :** inconnu
- **Polité de naissance :** inconnue
- **State V3 :** `UNRESOLVED`
- **Décès :** **février 1781**, Shiraz ; jour non établi dans les sources retenues

Aucune année de naissance n’est produite par extrapolation à partir de celle de Karim Khan.

### Fonction militaire au 1776-01-01

L’*Encyclopaedia Iranica* décrit le siège de Bassora de 1775–1776 comme **la seule opération à grande échelle de l’armée zand à son apogée** et précise qu’elle est **commandée par Ṣādeq Khan**, frère du wakil, à la tête d’environ 30 000 hommes.

Il s’agit donc du cas le plus net de ce lot : au **1er janvier 1776**, Ṣādeq commande déjà une grande armée zand en opération.

### Mapping

- **Classification :** `FORMATION_COMMAND`
- **Formation :** `cleanup2d3e_r1_per_land_1`
- **Décision :** `IMPLEMENT_HISTORICAL`
- **Justification :** `PER` n’a qu’une grande formation terrestre, et Ṣādeq commande précisément l’opération terrestre majeure de l’État zand à cette date.

### Culture, religion, profil

- **Culture historique :** Zand, branche Lak des Lors du Nord selon Iranica ; ne pas inventer un identifiant V3 si le mapping culture exact n’est pas confirmé
- **Religion :** chiisme duodécimain, à forte confiance contextuelle pour l’armée/dynastie zand
- **Profil social :** élite dynastique et militaire zand ; frère cadet et lieutenant capable de Karim Khan

### Portrait / DNA / assets

- aucun portrait contemporain authentifié de Ṣādeq n’a été validé ;
- aucun template/DNA exact de Ṣādeq n’a été trouvé ;
- **Karim Khan Zand**, son frère, possède déjà `dna_karim_khan_zand` et `per_karim_khand_zand_template` dans le dépôt ; cela constitue une référence familiale/artistique potentielle, **pas un DNA à recopier automatiquement** ;
- le dépôt contient également un template d’**Āghā Moḥammad Qājār**, mais Iranica rappelle qu’il reste otage à la cour de Karim Khan jusqu’à la mort de celui-ci : il est donc rejeté pour le commandement initial de 1776.

### Sources principales

1. Encyclopaedia Iranica, **ARMY iv. Afšar and Zand Periods** :  
   https://www.iranicaonline.org/articles/army-iv/
2. Encyclopaedia Iranica, **KARIM KHAN ZAND** :  
   https://www.iranicaonline.org/articles/karim-khan-zand/
3. Encyclopaedia Iranica, **ZAND DYNASTY** :  
   https://www.iranicaonline.org/articles/zand-dynasty/

---

## 4.3 DUR — Tīmūr Shah Dorrānī

### Identité

- **Nom principal :** Tīmūr Shah Dorrānī
- **Variantes :** Timur Shah Durrani, Taimur Shah Durrani, Timur Shah Sadōzay/Sadozai
- **Naissance :** **1746**
- **`birth_date_precision` :** `YEAR`
- **Lieu :** Mashhad
- **Polité :** Iran afsharide / Khorasan
- **State V3 :** `STATE_KHORASAN`
- **Décès :** **18 mai 1793**, Kabul

Une tradition donne décembre 1746, mais l’audit conserve **l’année** comme niveau de précision robuste plutôt que de fabriquer un jour.

### Fonction militaire et structure durrani

L’armée durrani du XVIIIe siècle n’est pas un système à deux corps permanents correspondant aux deux formations V3. Elle repose sur des contingents des khans pachtounes et sur des forces royales — notamment des éléments ghulam/qizilbash — dont Tīmūr cherche à accroître l’importance pour réduire sa dépendance envers l’aristocratie tribale.

Iranica situe en **1775** le transfert de la capitale de Qandahar à Kabul, qui devient le nouveau centre du pouvoir. Tīmūr est souverain depuis 1772 et constitue l’autorité militaire dynastique supérieure au 1er janvier 1776.

### Mapping

- **Formation retenue :** `cleanup2d3e_r1_dur_land_1`
- **Classification :** `HIGHER_COMMAND_ABSTRACTION`
- **Décision :** `IMPLEMENT_HISTORICAL`

La décision **ne signifie pas** que Tīmūr commandait un « Iᵉʳ corps durrani » permanent. Elle signifie que la formation principale V3 condense les forces centrales et tribales du royaume et que le souverain est le seul niveau supérieur historiquement défendable.

La seconde formation `cleanup2d3e_r1_dur_land_2` reste procédurale : dupliquer Tīmūr sur les deux créerait précisément la structure fictive que l’audit cherche à éviter.

### Culture, religion, profil

- **Culture :** Pachtoune, confédération durrani, branche Sadozai ; le dépôt possède `cu:pashtun`
- **Religion :** sunnite
- **Profil social/politique :** aristocratie royale sadozai ; politique de rééquilibrage entre chefs tribaux pachtounes et éléments urbains persianisés/qizilbash

### Portrait / DNA / assets

- un personnage historique Tīmūr Shah existe déjà dans `common/history/characters/dur.txt` ;
- aucun DNA/template explicite propre à Tīmūr n’a été trouvé dans cette définition ;
- son `age = 29` actuel est globalement compatible avec une naissance en 1746, mais l’implémentation future devrait préférer la donnée historique `birth_date_precision = YEAR` à une date inventée.

### Sources principales

1. Encyclopaedia Iranica, **AFGHANISTAN x. Political History** :  
   https://www.iranicaonline.org/articles/afghanistan-x-political-history/
2. Encyclopaedia Iranica, **AFGHANISTAN xi. Administration** :  
   https://www.iranicaonline.org/articles/afghanistan-xi-admin/
3. Willem Vogelsang, *The Afghans*, Blackwell, 2002 — naissance en 1746 à Mashhad.

---

## 4.4 HDJ — Sharīf Surūr ibn Musāʿid

### Identité

- **Nom principal :** Sharīf Surūr ibn Musāʿid
- **Nom développé :** Surūr b. Musāʿid b. Saʿīd b. Saʿd b. Zayd
- **Naissance :** **1167 AH ≈ 1754 CE**
- **`birth_date_precision` :** `HIJRI_YEAR / APPROXIMATE_CE_YEAR`
- **Lieu de naissance :** inconnu dans les sources retenues
- **Polité :** milieu sharifien du Hedjaz ; lieu précis non établi
- **State V3 :** `UNRESOLVED`
- **Décès :** **1202 AH ≈ 1788 CE**, à La Mecque selon la notice biographique

**Point important pour le dépôt :** le personnage HDJ actuel a `age = 31`, ce qui implique environ 1744/45. La notice biographique donne 1167 AH / 1754. Le futur passage d’implémentation devra donc **corriger cette divergence**, pas la conserver.

### Fonction militaire

Surūr n’est pas retenu parce qu’il est « émir ». Les chroniques et l’histoire de La Mecque documentent une activité militaire personnelle :

- entrée victorieuse à La Mecque et proclamation à l’émirat en 1186 AH ;
- bataille contre son oncle Aḥmad près de Minā ;
- recours à la cavalerie et à des tribus alliées pour reprendre l’avantage ;
- série de conflits répétés durant les années suivantes ;
- mobilisation directe d’alliés tribaux et conduite de campagnes.

Ce système ne correspond pas à une armée permanente moderne : forces sharifiennes, gardes, troupes payées et alliés tribaux sont mobilisés selon les crises.

### Mapping

- **Formation :** `cleanup2d3b_hdj_land_1`
- **Classification :** `HIGHER_COMMAND_ABSTRACTION`
- **Décision :** `IMPLEMENT_HISTORICAL`

La HCA est ici justifiée : la formation unique du Hedjaz est elle-même une abstraction d’un système de mobilisation sharifien et tribal, et Surūr est documenté comme autorité qui **lève et mène personnellement** ces forces.

### Culture, religion, profil

- **Culture :** arabe hedjazi ; milieu sharifien hassanide, Dhawu Zayd/Banu Qatada
- **Religion :** sunnite
- **Profil :** aristocratie sharifienne de La Mecque ; chef politique et militaire devant composer avec troupes urbaines, pèlerinage et alliances tribales

### Portrait / DNA / assets

- personnage historique **déjà présent** comme souverain HDJ ;
- aucun DNA/template spécifique repéré ;
- aucun portrait contemporain individuel authentifié n’a été validé.

### Sources principales

1. Aḥmad al-Sibāʿī, *Tārīkh Makka*, bibliothèque al-Ithnainya :  
   https://alithnainya.com/tocs/default.asp?path=0%3B2%3B21881%3B21992%3B22841%3B23009&toc_brother=-1&toc_id=23009
2. al-Ziriklī, *al-Aʿlām*, notice reproduite par al-Jamhara :  
   https://islamic-content.com/t/19256
3. *Khizānat al-Tawārīkh al-Najdiyya*, chronique numérisée :  
   https://www.masaha.org/book/view/4693/page/377

---

# 5. Décision formation par formation

## 5.1 IR1 — `cleanup2d3e_r1_ir1_land_1`

**Décision : `IMPLEMENT_HISTORICAL` — Süleyman Ağa.**  
La défense de Bassora est explicitement son commandement actif au 1er janvier 1776. Le mapping retenu est `THEATRE_COMMAND` et non une prétention à l’existence d’un corps permanent identique.

## 5.2 TUR — `cleanup2d3b_tur_land_1`

**Décision : `KEEP_PROCEDURAL`.**  
La formation combine un cœur balkanique et un immense vivier de conscription allant jusque dans les provinces égyptiennes. Aucun commandement permanent ottoman unique ne correspond à cet agrégat au 1er janvier 1776.

## 5.3 TUR — `cleanup2d3b_tur_land_2`

**Décision : `KEEP_PROCEDURAL`.**  
Même problème structurel. Un pacha provincial, un wali ou le grand vizir ne peut pas être converti automatiquement en général de cette formation.

## 5.4 TUR — `cleanup2d3b_tur_land_3`

**Décision : `KEEP_PROCEDURAL`.**  
Aucun titulaire d’un commandement militaire de type serasker correspondant à cette formation n’est vérifié pour la date exacte. **Canikli Ali Paşa** est un cas explicitement rejeté : sa nomination comme serasker de Kars date des **3–11 décembre 1776**, onze mois trop tard.

## 5.5 TUR — `cleanup2d3b_tur_land_4`

**Décision : `KEEP_PROCEDURAL`.**  
Cette formation est également synthétique et mélange Near East / composante égyptienne. Y placer un commandant mamelouk d’Égypte ou un dignitaire ottoman créerait un faux lien hiérarchique.

## 5.6 OMA — `cleanup2d3e_r1_oma_land_1`

**Décision : `KEEP_PROCEDURAL`.**  
**Hilal bin Ahmad**, fils de l’imam, est bien un vrai commandant : l’expédition omanaise envoyée secourir Bassora en 1775 est placée sous son commandement. Il n’est toutefois pas retenu, car :

1. le retrait des forces est situé « au début de 1776 », ce qui ne permet pas de verrouiller son statut au jour exact sans extrapolation ;
2. son commandement concerne une expédition du Golfe à forte composante navale ;
3. la formation OMA du mod est une abstraction Baluchistan/Zanzibar, sans correspondance directe.

**Ahmad bin Said** n’est pas retenu comme général simplement parce qu’il est imam et souverain.

## 5.7 PER — `cleanup2d3e_r1_per_land_1`

**Décision : `IMPLEMENT_HISTORICAL` — Moḥammad Ṣādeq Khan Zand.**  
C’est le mapping le plus fort du lot : commandement explicite de la principale opération zand, déjà en cours au 1er janvier.

## 5.8 DUR — `cleanup2d3e_r1_dur_land_1`

**Décision : `IMPLEMENT_HISTORICAL` — Tīmūr Shah Dorrānī, `HIGHER_COMMAND_ABSTRACTION`.**  
L’autorité est réelle, mais le caractère de « formation » est abstrait. La HCA doit être explicitement documentée dans l’implémentation future.

## 5.9 DUR — `cleanup2d3e_r1_dur_land_2`

**Décision : `KEEP_PROCEDURAL`.**  
Aucun second commandant de « corps » n’est défendable. La structure durrani ne justifie pas deux généraux nationaux permanents calqués sur les deux objets V3.

## 5.10 ARB — `cleanup2d3e_r1_arb_land_1`

**Décision : `KEEP_PROCEDURAL`.**  
Les Banu Kaʿb constituent une puissance armée réelle du Khuzestan et du Shatt al-Arab. Cependant, l’audit n’a pas obtenu une preuve suffisante de **commandement militaire terrestre personnel** permettant de transformer le dirigeant politique supposé de 1776 en général. Le commentaire du dépôt `PROCEDURAL_ALLOWED_PENDING_STRUCTURE_REWORK` est historiquement prudent et doit rester ainsi.

## 5.11 HDJ — `cleanup2d3b_hdj_land_1`

**Décision : `IMPLEMENT_HISTORICAL` — Sharīf Surūr ibn Musāʿid, `HIGHER_COMMAND_ABSTRACTION`.**  
Sa conduite personnelle des luttes et mobilisations est documentée ; la HCA reflète le caractère non permanent de l’armée sharifienne.

## 5.12 ZAI — `cleanup2d3b_zai_land_1`

**Décision : `KEEP_PROCEDURAL`.**  
Le cas d’**al-Manṣūr ʿAlī I** montre pourquoi un souverain militaire ne doit pas être automatiquement nommé général. Al-Shawkānī rapporte qu’avant son accession il était **Amīr al-ajnād** et gouverneur de Sanaʿa, et qu’il mena personnellement des combats. Mais après son accession en Rajab 1189 AH / 1775, la charge militaire passa d’abord brièvement à son frère al-Qāsim, puis à son fils Aḥmad. La transition n’est pas datée assez finement pour déterminer le titulaire exact au 1er janvier 1776.

## 5.13 CIR — `cleanup2d3e_r1_cir_land_1`

**Décision : `KEEP_PROCEDURAL` — `COLLECTIVE_HIGH_COMMAND`.**  
Les études sur la Circassie occidentale décrivent des structures territoriales, des assemblées, des élites guerrières et des mobilisations qui ne se réduisent pas à un général national unique. Imposer un prince connu comme « commandant de toute la Circassie » serait précisément la projection européenne moderne interdite par cette phase.

## 5.14 CHC — `Murtazeki`

**Décision : `KEEP_PROCEDURAL` — `COLLECTIVE_HIGH_COMMAND`.**  
Aucun commandant unique n’est défendable. En outre, le **nom de formation lui-même est anachronique** : la littérature académique traite les *murtazeki* comme une institution militaire permanente du cycle des premiers imams et surtout de l’imamat de Shamil, au XIXe siècle. Cela doit être enregistré comme problème de structure/nomenclature pour une future phase distincte, sans modification ici.

---

# 6. Empire ottoman : pourquoi aucun des quatre procéduraux n’est remplacé

Le terme `serdar` et sa forme supérieure `serdâr-ı ekrem` sont liés à l’exercice du commandement en campagne. Le grand vizir peut devenir commandant suprême lorsque le sultan ne mène pas personnellement l’armée, mais cela ne transforme pas automatiquement chaque grand vizir en chef permanent d’une formation territoriale V3.

**Derviş Mehmed Paşa**, grand vizir depuis juillet 1775, est donc rejeté comme simple correspondance d’office. Après Küçük Kaynarca, le 1er janvier 1776 ne fournit pas un théâtre de campagne qui justifierait de lui attribuer l’une des quatre armées synthétiques.

**Canikli Ali Paşa** est également rejeté pour la date initiale : le document BOA utilisé dans l’étude de Rıza Karagöz date son ordre comme **serasker de Kars des 3–11 décembre 1776**.

Conclusion : les quatre généraux procéduraux ottomans sont historiquement moins trompeurs qu’une liste de quatre pachas nommés artificiellement.

Sources :

- TDV, **Serdar** : https://islamansiklopedisi.org.tr/serdar
- TDV, **Derviş Mehmed Paşa** : https://islamansiklopedisi.org.tr/mehmed-pasa-dervis
- Rıza Karagöz, *Canikli Ali Paşa*, TTK 2003 (référence BOA) : https://dokumen.pub/canikli-ali-paa-975161564x.html

---

# 7. Égypte : candidat historique réel, mais aucune formation à lui donner

Après la mort de Muḥammad Bey Abū al-Dhahab en 1775, le pouvoir mamelouk égyptien passe notamment à **Ibrāhīm Bey** et **Murad Bey**. La notice TDV sur Ibrāhīm indique explicitement que celui-ci s’occupe des affaires administratives tandis que **Murad Bey prend en charge les affaires militaires**.

Cela fait de Murad Bey un candidat historique sérieux **si une formation terrestre égyptienne autonome est créée ultérieurement**.

Il n’est cependant pas retenu aujourd’hui parce que :

- aucune formation `EGY` n’existe dans l’architecture auditée ;
- les unités/conscrits d’Égypte sont inclus dans les formations `TUR` ;
- attribuer l’une de ces armées ottomanes globales à Murad Bey lui donnerait artificiellement autorité sur des forces balkaniques/levantines qu’il ne commandait pas.

**Statut : `HISTORICAL_CANDIDATE_NOT_MAPPABLE_UNDER_CURRENT_ARCHITECTURE`.**

Source : TDV İslâm Ansiklopedisi, **İbrahim Bey** :  
https://islamansiklopedisi.org.tr/ibrahim-bey

---

# 8. Caucase : résultats structurels

## 8.1 Circassie

La formation unique CIR ne doit pas être interprétée comme la preuve d’un état-major national circassien. Les recherches sur les structures occidentales montrent une pluralité de communautés/polities, d’assemblées et d’élites guerrières. Un chef pouvait exercer une influence militaire locale ou temporaire sans devenir le « général de la Circassie » au sens V3.

Source académique principale : Samir Khotko, *Journal of Caucasian Studies* :  
https://dergipark.org.tr/en/pub/jocas/article/1215889

## 8.2 Tchétchénie / Nord-Est caucasien

Le mod nomme la formation `Murtazeki`. L’article de U. U. Dadaev dans *History, Archeology and Ethnography of the Caucasus* relie cette institution à l’imamat du XIXe siècle et au système de Shamil. Elle ne doit donc pas servir de base pour chercher un « chef des Murtazeki » en 1776.

Source :  
https://caucasushistory.ru/2618-6772/en/article/view/346

## 8.3 Khanats et Géorgie

Aucune formation terrestre autonome correspondant à un khanat azéri/caucasien distinct, à la Géorgie, ou à une Arménie indépendante n’a été trouvée dans les formations de départ auditées. Il n’y a donc **aucune ligne à inventer** dans le CSV. Les territoires arméniens/transcaucasiens présents dans la structure sont en partie absorbés par `PER` ou par les grandes architectures voisines.

---

# 9. Audit des anciens personnages, DNA et templates du dépôt

## Personnages déjà existants et pertinents

- `IR1` : **Omar Pasha**, souverain historique ; culture `cu:georgian`, IG Armed Forces dans la définition actuelle — **pas le candidat militaire retenu** ;
- `DUR` : **Timur Shah Durrani**, souverain historique existant ;
- `HDJ` : **Surur ibn Musa'id**, souverain historique existant ;
- `OMA` : **Ahmad bin Said al-Busaidi**, souverain historique existant ;
- `ZAI` : **al-Mansur Ali I**, souverain historique existant ;
- `TUR` : **Abdülhamid I**, souverain historique existant.

L’existence de ces personnages ne vaut pas preuve de commandement de formation.

## Assets persans réutilisables ou à connaître

`common/character_templates/country_per.txt` contient notamment :

- `per_karim_khand_zand_template` avec `dna_karim_khan_zand` ;
- `per_agha_mohammed_qajar_template` avec `dna_agha_mohammed_qajar`.

`common/dna_data/` contient également les fichiers correspondants pour Karim Khan et le personnage qajar.

**Aucun template/DNA exact de Ṣādeq Khan n’a été trouvé.** La présence d’un DNA de son frère Karim ne justifie pas de le dupliquer : il peut au mieux servir de référence familiale lors d’un futur travail visuel.

## Recherche des nouveaux candidats

La recherche textuelle du dépôt n’a trouvé ni **Ṣādeq Khan** ni **Süleyman Ağa** comme ancien personnage historique réutilisable.

---

# 10. Candidats examinés mais rejetés

| Candidat | Polité | Motif du rejet |
|---|---|---|
| Derviş Mehmed Paşa | Ottoman | Grand vizir ≠ commandant permanent d’une formation ; pas de campagne justifiant `serdâr-ı ekrem` au 01/01/1776 |
| Canikli Ali Paşa | Ottoman | Serasker de Kars seulement en décembre 1776 — trop tard |
| Murad Bey | Égypte | Vrai responsable militaire, mais aucune formation EGY autonome ; impossible à mapper sans contresens |
| Hilal bin Ahmad | Oman | Vrai commandant de l’expédition de 1775, mais retrait au début de 1776 + mauvais mapping avec la formation Baluchistan/Zanzibar |
| Ahmad bin Said | Oman | Souverain/imam ; ne doit pas remplacer son fils commandant ni être promu automatiquement |
| Āghā Moḥammad Qājār | Perse | Asset existant dans le dépôt, mais otage à Shiraz sous Karim Khan ; pas commandant de l’armée zand de 1776 |
| Barakat bin Uthman | Arabistan / Banu Kaʿb | Direction politique possible, mais commandement terrestre personnel insuffisamment documenté dans les sources prioritaires |
| al-Manṣūr ʿAlī I | Yemen | Ancien Amīr al-ajnād et vrai combattant, mais cette charge cesse à l’accession de 1775 ; titulaire exact du 01/01/1776 non verrouillé |
| al-Qāsim b. al-Mahdī / Aḥmad b. al-Manṣūr | Yemen | Succession au commandement attestée, mais transition datée trop grossièrement pour le jour de référence |
| « chef national circassien » | Circassie | Catégorie artificielle : structure plurielle/collective |
| « chef des Murtazeki » | CHC | Institution anachronique pour 1776 et structure collective |

---

# 11. Problèmes historiques adjacents découverts — sans implémentation

1. **CHC — `Murtazeki`** : nom de formation anachronique pour 1776 ; à reprendre dans une future phase de nomenclature/structure militaire.
2. **HDJ — Surur** : `age = 31` dans le personnage actuel est incompatible avec la naissance 1167 AH / 1754 de la notice biographique.
3. **Égypte** : l’architecture actuelle absorbe les forces égyptiennes dans `TUR`, ce qui empêche de représenter proprement le commandement mamelouk de Murad Bey.
4. **Ottomans** : les quatre armées permanentes du setup sont des abstractions gameplay et ne doivent pas recevoir quatre titulaires historiques uniquement pour éliminer des procéduraux.
5. **PER** : le dépôt contient des assets qajar et Karim Khan qui peuvent inciter à réutiliser des personnages non admissibles ; ne pas laisser la disponibilité technique dicter la décision historique.

Aucun de ces constats n’est une autorisation de modifier le gameplay dans CLEANUP-2D-5G.

---

# 12. Checklist pour la future fusion globale

- [ ] Remplacer le procédural IR1 par **Süleyman Ağa** avec date de naissance laissée inconnue.
- [ ] Remplacer le procédural PER par **Moḥammad Ṣādeq Khan Zand**, sans inventer naissance/lieu de naissance.
- [ ] Utiliser **Tīmūr Shah** seulement pour `DUR land_1` et documenter `HIGHER_COMMAND_ABSTRACTION`.
- [ ] Ne pas dupliquer Tīmūr sur `DUR land_2`.
- [ ] Utiliser **Surūr ibn Musāʿid** pour HDJ sous `HIGHER_COMMAND_ABSTRACTION`, et corriger ultérieurement son âge historique.
- [ ] Conserver les quatre généraux procéduraux `TUR`.
- [ ] Conserver les procéduraux `OMA`, `ARB`, `ZAI`, `CIR`, `CHC` et `DUR land_2`.
- [ ] Ne pas créer un général EGY tant qu’aucune formation EGY n’existe.
- [ ] Enregistrer `Murtazeki` comme anomalie de nomenclature à traiter séparément.
- [ ] Ne réutiliser aucun DNA familial/voisin comme s’il s’agissait du portrait du candidat sans validation visuelle spécifique.

---

# 13. Sources et qualité documentaire

### Niveau A — institutions / références académiques

- Encyclopaedia Iranica — *ARMY iv. Afšar and Zand Periods*  
  https://www.iranicaonline.org/articles/army-iv/
- Encyclopaedia Iranica — *KARIM KHAN ZAND*  
  https://www.iranicaonline.org/articles/karim-khan-zand/
- Encyclopaedia Iranica — *ZAND DYNASTY*  
  https://www.iranicaonline.org/articles/zand-dynasty/
- Encyclopaedia Iranica — *AFGHANISTAN x. Political History*  
  https://www.iranicaonline.org/articles/afghanistan-x-political-history/
- Encyclopaedia Iranica — *AFGHANISTAN xi. Administration*  
  https://www.iranicaonline.org/articles/afghanistan-xi-admin/
- Encyclopaedia Iranica — *SHATT AL-ARAB*  
  https://www.iranicaonline.org/articles/shatt-al-arab/
- Qatar Digital Library / British Library India Office Records — Lorimer et Factory Records sur Bassora  
  https://www.qdl.qa/en/archive/81055/vdc_100023575942.0x000059  
  https://www.qdl.qa/en/archive/81055/vdc_100023575948.0x000011  
  https://www.qdl.qa/archive/81055/vdc_100107757920.0x0000b3
- TDV İslâm Ansiklopedisi — *Bağdat*  
  https://islamansiklopedisi.org.tr/bagdat
- TDV İslâm Ansiklopedisi — *Serdar*  
  https://islamansiklopedisi.org.tr/serdar
- TDV İslâm Ansiklopedisi — *Derviş Mehmed Paşa*  
  https://islamansiklopedisi.org.tr/mehmed-pasa-dervis
- TDV İslâm Ansiklopedisi — *İbrahim Bey*  
  https://islamansiklopedisi.org.tr/ibrahim-bey
- *History, Archeology and Ethnography of the Caucasus* — Dadaev sur les Murtazeki  
  https://caucasushistory.ru/2618-6772/en/article/view/346
- *Journal of Caucasian Studies* — Khotko sur les structures de Circassie occidentale  
  https://dergipark.org.tr/en/pub/jocas/article/1215889

### Niveau B — chroniques, synthèses savantes, éditions en ligne

- Aḥmad al-Sibāʿī, *Tārīkh Makka*  
  https://alithnainya.com/tocs/default.asp?path=0%3B2%3B21881%3B21992%3B22841%3B23009&toc_brother=-1&toc_id=23009
- al-Shawkānī, *al-Badr al-ṭāliʿ*, biographie d’al-Manṣūr ʿAlī reproduite par Taraajem  
  https://www.taraajem.com/persons/191938/مولانا-الإمام-خليفة-العصر-أمير-المؤمنين-المنصور-بالله-رب-العالمين-علي-بن-الإمام-المهدي
- al-Ziriklī, *al-Aʿlām*, notice Surūr reproduite par al-Jamhara  
  https://islamic-content.com/t/19256
- *Khizānat al-Tawārīkh al-Najdiyya*  
  https://www.masaha.org/book/view/4693/page/377
- Rıza Karagöz, *Canikli Ali Paşa*, Türk Tarih Kurumu, 2003 — fondé notamment sur des références BOA.
- Willem Vogelsang, *The Afghans*, Blackwell, 2002.

### Niveau C — contexte omanais avec bibliographie institutionnelle explicite

- Atheer, « العلاقات العمانية العثمانية في عهد الإمام أحمد بن سعيد » ; l’article cite une thèse de Sultan Qaboos University et une publication de la **National Records and Archives Authority of Oman** :  
  https://www.atheer.om/archive/6503/

---

# 14. Conclusion de phase

Pour CLEANUP-2D-5G, la solution historiquement la plus robuste n’est **pas** de maximiser le nombre de noms réels. Elle consiste à remplacer les procéduraux seulement quand l’individu est à la fois historiquement actif au 1er janvier 1776 et correctement mappable à l’objet militaire du mod.

La sélection finale recommandée est donc :

- **Süleyman Ağa** — IR1 ;
- **Moḥammad Ṣādeq Khan Zand** — PER ;
- **Tīmūr Shah Dorrānī** — DUR formation principale, HCA ;
- **Sharīf Surūr ibn Musāʿid** — HDJ, HCA ;
- **tous les autres : maintien procédural**.

Le CSV joint constitue la table normative de cette phase de recherche. Aucune modification du dépôt n’a été effectuée.
