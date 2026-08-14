# CLEANUP-2D-5J — HISTORICAL GENERALS 1776 — EAST ASIA

**Projet :** Victoria 3 — *1776 – Age of Revolutions*  
**Dépôt :** `Malzars-sys/1776-Age-of-Revolutions`  
**Branche auditée :** `cleanup-post-release`  
**Date historique absolue :** **1776-01-01**  
**Nature de cette phase :** **RECHERCHE UNIQUEMENT — AUCUNE IMPLÉMENTATION, AUCUN COMMIT, AUCUN PUSH**

---

## 1. Résultat exécutif

L’audit direct de `common/history/military_formations/06_military_formations_asia.txt` donne, pour l’Asie orientale du périmètre demandé :

- **Qing / CHI : 8 formations terrestres**
  - `cleanup2d3b_chi_land_1` — GEN1776-143
  - `cleanup2d3b_chi_land_2` — GEN1776-144
  - `cleanup2d3b_chi_land_3` — GEN1776-145
  - `cleanup2d3b_chi_land_4` — GEN1776-146
  - `cleanup2d3b_chi_land_5` — GEN1776-147
  - `cleanup2d3b_chi_land_6` — GEN1776-148
  - `cleanup2d3b_chi_land_7` — GEN1776-149
  - `cleanup2d3b_chi_land_8` — GEN1776-150
- **Japon / JAP : 2 formations terrestres**
  - `Edo_Guard_Army` — GEN1776-154
  - `Kinai_Guard_Army` — GEN1776-155

Ces dix généraux sont actuellement procéduraux et utilisent `template = default`.

En revanche :

- `KOR` existe comme pays, mais **aucune formation terrestre `c:KOR`** n’est définie dans le fichier asiatique audité ;
- `MGL` existe comme pays, mais **aucune formation terrestre `c:MGL`** ;
- `TIB` existe comme pays, mais **aucune formation terrestre `c:TIB`** ;
- l’historique de `RYU` (Ryūkyū) existe dans la branche, mais **aucune formation terrestre `c:RYU`** ;
- aucune affectation de général ne doit donc être créée pour ces tags dans cette phase.

### Recommandation synthétique

| Formation | Décision recherche | Candidat |
|---|---|---|
| CHI land 1 | remplacer procédural par abstraction historique | **Fengshenge 豐昇額** |
| CHI land 2 | remplacer procédural par abstraction historique | **Agūi 阿桂** |
| CHI land 3 | remplacer procédural par commandant régional historique | **Fuyu 傅玉** |
| CHI land 4 | remplacer procédural par abstraction historique | **Mingliang 明亮** |
| CHI land 5 | remplacer procédural par abstraction historique | **Qilikeqi 齊里克齊** |
| CHI land 6 | remplacer procédural par abstraction historique | **Wufu 五福** |
| CHI land 7 | remplacer procédural par abstraction historique | **Hailancha 海蘭察** |
| CHI land 8 | remplacer procédural par abstraction historique | **Techenge 特成額** |
| Edo_Guard_Army | **conserver procédural** | aucun commandant unique défendable |
| Kinai_Guard_Army | remplacer procédural par abstraction historique | **Kuze Hiroaki 久世広明** |

Le mot **abstraction** est essentiel : plusieurs formations Qing mélangent des provinces éloignées et des labels de Bannières ; elles ne correspondent pas à une unité historique unique possédant nécessairement un seul commandant en janvier 1776.

---

## 2. Méthode d’admissibilité

Un personnage n’est retenu que si une **fonction de commandement terrestre réelle** est démontrée au **1er janvier 1776**.

### Sont admissibles

- général de garnison/Bannière (`將軍`) avec commandement régional réel ;
- commandant provincial ou régional (`提督`, `總兵`) lorsque la fonction implique effectivement le commandement des forces ;
- général de campagne (`將軍`) ;
- vice-général / deputy general (`副將軍`) ;
- `參贊大臣`, `領隊大臣` lorsqu’il s’agit explicitement d’un commandement dans une campagne en cours ;
- au Japon, charge du bakufu dont le contenu militaire et territorial est explicitement documenté, par exemple `大坂城代`.

### Ne sont pas admissibles automatiquement

- gouverneur général (`總督`) ;
- gouverneur (`巡撫`) ;
- ministre (`尚書`) ;
- haut fonctionnaire civil ;
- daimyō ;
- shōgun ;
- rōjū.

Une de ces personnes ne peut être utilisée que si **une fonction militaire distincte** est attestée.

---

## 3. Qing — distinction institutionnelle nécessaire

| Office Qing | Nature | Peut justifier un général V3 ? |
|---|---|---|
| `總督` gouverneur général | administration civile supérieure avec pouvoirs de surveillance militaire | **pas automatiquement** |
| `巡撫` gouverneur | administration provinciale | **pas automatiquement** |
| `駐防將軍` / `將軍` de garnison | commandement Banner/garnison régional | **oui** |
| `提督` | commandement militaire provincial supérieur, surtout Green Standard | **oui** |
| `總兵` | commandement militaire régional | **oui** |
| `尚書` ministre | fonction centrale/civile | **non, à elle seule** |
| `將軍` de campagne | commandement d’expédition | **oui** |
| `副將軍` | commandement adjoint d’expédition | **oui** |
| `參贊大臣` / `領隊大臣` en campagne | état-major/commandement opérationnel | **oui si le contexte militaire est explicite** |

---

# 4. CHI — profils recommandés

## EA-CHI-01 — `cleanup2d3b_chi_land_1`

### Fengshenge — 豐昇額

- **Nom original :** 鈕祜祿·豐昇額
- **Romanisation retenue :** Fengshenge
- **Variantes :** 豐盛額 ; Fengsheng'e
- **Naissance :** inconnue
- **Précision :** `UNKNOWN`
- **Lieu de naissance :** non attesté dans les sources consultées
- **Polité de naissance :** Empire Qing
- **State V3 de naissance :** non mappable sans invention
- **Décès :** 1777
- **Culture historique :** Mandchou, Bannière jaune bordée
- **Culture V3 proposée pour compatibilité :** `manchu`
- **Religion personnelle :** non attestée — ne pas inférer
- **Origine sociale :** haute noblesse héréditaire des Bannières ; fils d’Aligun ; duc de première classe
- **Portrait :** oui, tradition des portraits de mérite du Ziguangge après Jinchuan ; asset individuel/licence à auditer
- **DNA/template existant :** aucun template nommé trouvé dans la branche

### Fonction militaire au 1776-01-01

Fengshenge est documenté comme **副將軍**, vice-général de la campagne du second Jinchuan, sous le commandement général d’Agūi. Sa présence sur le théâtre et ses opérations de terrain sont attestées.

**Admissibilité : HIGH.**

Il n’est pas retenu parce qu’il est duc ou haut dignitaire, mais parce qu’il exerce un **commandement de campagne réel**.

### Correspondance avec la formation V3

La formation possède les scopes :

- `bordered_yellow_banner`
- `plain_yellow_banner`

L’appartenance de Fengshenge à la Bannière jaune bordée fournit un lien institutionnel utile. Cependant la composition géographique de la formation est artificiellement très large.

**Formation fit : MEDIUM.**

---

## EA-CHI-02 — `cleanup2d3b_chi_land_2`

### Agūi — 阿桂

- **Nom original :** 章佳·阿桂
- **Romanisation :** **Agūi**
- **Variantes :** Agui ; A-kuei ; 阿桂
- **Naissance :** **1717-09-07**
- **Précision :** `EXACT_DAY_SOURCE_CONVERTED`
- La date grégorienne n’est pas une reconstruction de ce rapport : la source biographique consultée fournit elle-même la correspondance avec la date lunaire.
- **Lieu de naissance :** non suffisamment attesté dans la source d’autorité consultée
- **Polité :** Empire Qing
- **State V3 de naissance :** inconnu
- **Décès :** 1797
- **Culture historique :** Mandchou ; d’abord Bannière bleue simple, ensuite Bannière blanche simple
- **Culture V3 :** `manchu`
- **Religion personnelle :** inconnue
- **Origine sociale :** famille de fonctionnaires des Bannières ; fils d’Akdun
- **Portrait :** oui, iconographie Qing historique attestée
- **DNA/template :** aucun template nommé trouvé

### Fonction militaire

Agūi est **定西將軍**, général en chef chargé de pacifier l’Ouest, **Qianlong 38–41 (1773–1776)**.

Au 1er janvier 1776, il dirige la phase finale du **second Jinchuan**.

Il cumule aussi des offices centraux, mais **ce n’est pas la raison de son admissibilité**.

**Admissibilité : HIGH.**

### Correspondance V3

`cleanup2d3b_chi_land_2` possède les scopes White Banner. Le rattachement d’Agūi à la Bannière blanche simple et son statut de commandant suprême permettent une bonne abstraction.

**Formation fit : MEDIUM-HIGH.**

---

## EA-CHI-03 — `cleanup2d3b_chi_land_3`

### Fuyu — 傅玉

- **Nom original :** 富察·傅玉
- **Variante :** 富玉
- **Romanisation :** Fuyu
- **Naissance :** **inconnue**
- **Précision :** `UNKNOWN_SOURCE_CONFLICT`
- **Décès :** 1798
- **Lieu de naissance :** inconnu
- **Culture historique :** Mandchou, clan Fuca, Bannière jaune bordée
- **Culture V3 :** `manchu`
- **Religion :** inconnue
- **Origine sociale :** très haute famille Fuca des Bannières ; frère de Fuheng
- **Portrait :** non vérifié
- **DNA/template :** aucun template nommé trouvé

### Fonction militaire

Fuyu est **黑龍江將軍 — General of Heilongjiang / Black Dragon River General** pendant le mandat couvrant **Qianlong 37–44**.

Il s’agit d’un commandement militaire Banner régional direct, pas d’un gouvernorat civil.

Au **1776-01-01**, il est donc effectivement en charge du grand commandement militaire du nord-est.

**Admissibilité : HIGH.**

### Correspondance V3

La formation :

- HQ `region_northeast_asia`
- contient notamment `STATE_AMUR`

C’est la **meilleure correspondance géographique directe** trouvée dans tout l’audit Qing.

Le scope « Red Banner » de la formation n’est en revanche pas cohérent avec la Bannière historique de Fuyu ; il faut considérer la formation comme une abstraction régionale plutôt qu’une véritable unité de Bannière.

**Formation fit : HIGH pour la géographie et l’office ; mismatch de label Banner explicitement signalé.**

### Conflit de source sur la naissance

Une source secondaire CText/DataWiki donne **1715**. L’autorité biographique Academia Sinica utilisée ici ne valide pas cette naissance. La règle conservatrice est donc :

> **ne pas implémenter 1715 à ce stade ; conserver naissance inconnue.**

---

## EA-CHI-04 — `cleanup2d3b_chi_land_4`

### Mingliang — 明亮

- **Nom original :** 富察·明亮
- **Romanisation :** Mingliang
- **Manchu :** `mingliyang`
- **Naissance :** 1736
- **Précision :** `YEAR`
- **Lieu :** inconnu
- **Décès :** 1822
- **Culture historique :** Mandchou, Fuca, Bannière jaune bordée
- **Culture V3 :** `manchu`
- **Religion personnelle :** inconnue
- **Origine sociale :** élite Fuca liée à la maison impériale
- **Portrait :** oui, inclus dans le programme de commémoration des officiers du Jinchuan
- **DNA/template :** aucun nommé

### Fonction militaire

Mingliang est **定邊右副將軍**, senior deputy general de la campagne du Jinchuan, fonction démarrant en Qianlong 38.

Il a également été **廣州將軍**, mais la table officielle change le titulaire de Mingliang à Yongwei pendant Qianlong 40 sans fournir ici une date grégorienne suffisamment précise pour placer le transfert par rapport au **1er janvier 1776**.

Donc :

- **ne pas utiliser le poste de Guangzhou comme preuve principale pour le 1776-01-01** ;
- utiliser son poste de **deputy general de campagne**, clairement actif.

**Admissibilité : HIGH.**  
**Formation fit : MEDIUM.**

---

## EA-CHI-05 — `cleanup2d3b_chi_land_5`

### Qilikeqi — 齊里克齊

- **Nom original :** 鄂魯特·齊里克齊
- **Romanisation :** Qilikeqi
- **Forme native consignée :** `ūlet cirikci`
- **Naissance :** inconnue
- **Décès :** 1799
- **Origine :** Ūlet/Oirat
- **Incorporation :** Bannière mongole jaune bordée
- **Culture historique :** Oirat
- **Culture V3 la moins déformante disponible :** `mongol`
- **Religion personnelle :** inconnue ; **ne pas déduire** islam ou bouddhisme d’une appartenance ethnopolitique
- **Origine sociale :** guerrier oirat intégré au service impérial, puis garde et haut commandement
- **Portrait :** oui, reconnaissance par portrait au Ziguangge attestée
- **DNA/template :** aucun nommé

### Fonction militaire

Il exerce notamment :

- commandement adjoint de la **Bannière mongole jaune bordée** ;
- puis **健銳營總統大臣**, commandant supérieur du **Jianrui Camp**, unité d’élite de la capitale.

Cette dernière fonction couvre la date de référence.

**Admissibilité : HIGH.**

### Correspondance V3

La formation est `region_north_china`; le Jianrui Camp est lié à Beijing/Xiangshan.

**Command State proxy : `STATE_BEIJING`.**  
**Formation fit : MEDIUM-HIGH.**

---

## EA-CHI-06 — `cleanup2d3b_chi_land_6`

### Wufu — 五福

- **Nom original :** 富察·五福
- **Romanisation :** Wufu
- **Manchu :** `ufu`
- **Naissance :** **vers 1728**
- **Précision :** `APPROX_YEAR`
- **Lieu :** inconnu
- **Décès :** 1783
- **Culture :** Mandchou, Fuca, Bannière blanche bordée
- **V3 :** `manchu`
- **Religion :** inconnue
- **Origine sociale :** officier bannerman héréditaire
- **Portrait :** oui, cité parmi les officiers portraiturés pour les mérites du Jinchuan
- **DNA/template :** aucun nommé

### Fonction militaire

Wufu est **松潘鎮總兵 — Songpan zongbing** de Qianlong 37 à 44 et participe activement à la campagne du Jinchuan.

Le titre `總兵` est ici un véritable **commandement militaire régional**.

**Admissibilité : HIGH.**

La formation V3 mélange toutefois Fujian et Shandong : la correspondance géographique n’est pas littérale.

**Formation fit : MEDIUM / abstraction explicite.**

---

## EA-CHI-07 — `cleanup2d3b_chi_land_7`

### Hailancha — 海蘭察

- **Nom original :** 多拉爾·海蘭察
- **Romanisation :** Hailancha
- **Naissance :** inconnue
- **Décès :** 1793
- **Origine historique :** **Solon**
- **Statut initial :** `索倫馬甲`, cavalier Solon
- **Enregistrement Banner :** Bannière mandchoue jaune bordée
- **Culture V3 :** `manchu` **uniquement comme fallback technique**
- **Religion :** inconnue
- **Origine sociale :** militaire de rang modeste ayant progressé par le mérite de campagne
- **Portrait :** oui, grande tradition des portraits militaires Qing du Jinchuan
- **DNA/template :** aucun nommé

### Fonction militaire

Hailancha est un **參贊大臣** de la campagne du Jinchuan et occupe successivement plusieurs responsabilités opérationnelles entre Qianlong 37 et 41.

Il est donc bien un **commandant de terrain actif au 1776-01-01**.

**Admissibilité : HIGH.**

### Avertissement culturel

Le dépôt n’a pas livré de culture `evenki` lors de la recherche, alors que l’identité Solon d’Hailancha est historiquement importante.

Si V3 impose une culture existante :

`manchu` = **fallback de compatibilité**, pas affirmation ethnohistorique.

**Formation fit : LOW-MEDIUM**, car la formation V3 est particulièrement synthétique.

---

## EA-CHI-08 — `cleanup2d3b_chi_land_8`

### Techenge — 特成額

- **Nom original :** 鈕祜祿·特成額
- **Romanisation :** Techenge
- **Manchu :** `tecengge`
- **Naissance :** 1746
- **Précision :** `YEAR`
- **Lieu :** inconnu
- **Décès :** 1796
- **Culture :** Mandchou, Niohuru, Bannière jaune bordée
- **V3 :** `manchu`
- **Religion :** inconnue
- **Origine sociale :** origine de service Banner relativement basse (`黏竿處拜唐阿`), carrière militaire professionnelle
- **Portrait :** mention dans les listes textuelles de mérite du Jinchuan ; image individuelle non validée
- **DNA/template :** aucun nommé

### Fonction militaire au jour de référence

Techenge est **威寧鎮總兵 — Weining zongbing**, Guizhou :

- intérim Qianlong 39–40 ;
- titulaire Qianlong 40–41.

Son commandement de **Taiyuan** n’arrive qu’en **Qianlong 41**.

Par conséquent :

> au **1776-01-01**, ne pas l’implémenter comme commandant de Taiyuan par anticipation.

Son admissibilité repose sur **Weining**, commandement régional réel.

**Admissibilité : HIGH.**  
**Formation fit : MEDIUM**, la formation mélangeant Guangxi et Shanxi.

---

# 5. Japon Tokugawa

## 5.1 `Edo_Guard_Army`

### Décision : `KEEP_PROCEDURAL_ABSTRACTION`

Aucun commandant unique suffisamment défendable n’a été identifié.

Le problème est institutionnel : la garde d’Edo et du château n’est pas une « armée nationale » avec un général unique comparable à un commandement européen. Les responsabilités sont réparties entre plusieurs corps et charges du bakufu.

Il serait historiquement trompeur de transformer automatiquement :

- le shōgun **Tokugawa Ieharu** ;
- le rōjū **Tanuma Okitsugu** ;
- ou un daimyō choisi arbitrairement

en « général de l’Edo Guard Army ».

La formation V3 est déjà une abstraction. **Conserver un général procédural est historiquement préférable à un faux personnage historique.**

---

## 5.2 `Kinai_Guard_Army`

### Kuze Hiroaki — 久世広明

- **Nom original :** 久世広明
- **Romanisation :** Kuze Hiroaki
- **Naissance :** 1732
- **Précision :** `YEAR`
- La biographie japonaise donne une date lunisolaire plus détaillée, mais le présent audit **ne fabrique aucune conversion grégorienne**.
- **Lieu de naissance :** non établi dans la biographie consultée
- **Polité :** Japon Tokugawa
- **State V3 de naissance :** inconnu
- **Décès :** 1785
- **Culture :** Japanese → `japanese`
- **Religion personnelle :** inconnue
- **Origine sociale :** né dans une famille hatamoto, adopté dans la maison Kuze, devenu fudai daimyō et officier du bakufu
- **Portrait :** non vérifié pour implémentation
- **DNA/template :** aucun template nommé trouvé

### Fonction

**大坂城代 — Ōsaka jōdai**, **1769–1777**.

Le contenu institutionnel du poste comprend :

- garde du château d’Osaka ;
- sécurité du Kinai ;
- surveillance de l’Ouest et des daimyō occidentaux ;
- autorité de sécurité/militaire du bakufu dans la région.

Kuze n’est donc **pas retenu parce qu’il est daimyō**, mais parce que la charge de `Ōsaka jōdai` possède un contenu militaire régional directement documenté.

**Admissibilité : HIGH.**  
**Formation fit : HIGH comme abstraction Kinai.**

---

# 6. États orientaux présents sans formation terrestre à pourvoir

## KOR — Joseon Korea

Le tag existe dans les définitions de pays de la branche.

Aucun bloc `c:KOR` n’apparaît dans `06_military_formations_asia.txt`.

**Décision : NO_ASSIGNMENT_REQUIRED.**

Il serait contre la méthode du projet de chercher un haut militaire coréen puis de lui inventer une formation qui n’existe pas.

---

## MGL — Mongolia

Le tag existe.

Aucun bloc `c:MGL` n’est présent dans le fichier de formations audité.

**Décision : NO_ASSIGNMENT_REQUIRED.**

---

## TIB — Tibet

Le tag existe.

Aucun bloc `c:TIB` n’est présent.

**Décision : NO_ASSIGNMENT_REQUIRED.**

---

## RYU — Ryūkyū

Un fichier d’historique de pays `ryu - ryukyu.txt` existe dans la branche et le royaume intervient dans le contenu japonais.

Aucune formation terrestre `c:RYU` n’est toutefois présente dans le fichier audité.

**Décision : NO_ASSIGNMENT_REQUIRED.**

---

## MAN — vérification de périmètre

Aucun bloc `c:MAN` n’a été trouvé dans le fichier de formations terrestres asiatique inspecté.

Aucune affectation n’est proposée dans cette phase.

---

# 7. Portraits et DNA/templates

| Personnage | Portrait historique | DNA/template nommé dans la branche |
|---|---|---|
| Fengshenge | oui, commémoration Ziguangge | non trouvé |
| Agūi | oui | non trouvé |
| Fuyu | non vérifié | non trouvé |
| Mingliang | oui, série de mérite Jinchuan | non trouvé |
| Qilikeqi | oui, Ziguangge attesté | non trouvé |
| Wufu | oui, Ziguangge attesté | non trouvé |
| Hailancha | oui | non trouvé |
| Techenge | mention de portrait de mérite, image individuelle non validée | non trouvé |
| Kuze Hiroaki | non vérifié | non trouvé |

**Important :** l’existence historique d’un portrait ne signifie pas qu’un DNA/template Victoria 3 existe déjà.

Dans la branche auditée, les généraux concernés sont actuellement créés avec :

`template = default`

Aucun nom correspondant aux candidats ci-dessus n’a livré de template/DNA dédié lors de la recherche dans le dépôt.

---

# 8. Naissances : règles de précision

Aucun jour ou mois n’a été complété par supposition.

| Personnage | Valeur retenue | Précision |
|---|---|---|
| Agūi | 1717-09-07 | `EXACT_DAY_SOURCE_CONVERTED` |
| Fengshenge | inconnu | `UNKNOWN` |
| Fuyu | inconnu | `UNKNOWN_SOURCE_CONFLICT` |
| Mingliang | 1736 | `YEAR` |
| Hailancha | inconnu | `UNKNOWN` |
| Wufu | c.1728 | `APPROX_YEAR` |
| Qilikeqi | inconnu | `UNKNOWN` |
| Techenge | 1746 | `YEAR` |
| Kuze Hiroaki | 1732 | `YEAR` |

### Cas Agūi

La conversion grégorienne est conservée uniquement parce que la source consultée donne explicitement le résultat.

### Cas Kuze Hiroaki

La source japonaise donne une date selon le calendrier japonais traditionnel. Aucun jour/mois grégorien n’est généré ici.

### Cas Fuyu

Une source secondaire donne 1715, mais l’autorité Academia Sinica ne le sécurise pas. La valeur finale reste **UNKNOWN**.

---

# 9. Religion : règle conservatrice

Aucune religion personnelle n’a été attribuée en fonction :

- de l’ethnie ;
- de la Bannière ;
- du clan ;
- de la polité ;
- d’une présomption statistique.

Les candidats sont donc marqués :

`UNKNOWN_NOT_PERSONALLY_ATTESTED`

avec recommandation :

`TBD_DO_NOT_INFER`

Une éventuelle valeur V3 devra être décidée séparément lors de l’implémentation si le moteur exige un champ religieux.

---

# 10. Matrice finale de confiance

| ID | Personnage | Admissibilité du personnage | Fit avec la formation |
|---|---|---:|---:|
| EA-CHI-01 | Fengshenge | HIGH | MEDIUM |
| EA-CHI-02 | Agūi | HIGH | MEDIUM-HIGH |
| EA-CHI-03 | Fuyu | HIGH | **HIGH** |
| EA-CHI-04 | Mingliang | HIGH | MEDIUM |
| EA-CHI-05 | Qilikeqi | HIGH | MEDIUM-HIGH |
| EA-CHI-06 | Wufu | HIGH | MEDIUM |
| EA-CHI-07 | Hailancha | HIGH | LOW-MEDIUM |
| EA-CHI-08 | Techenge | HIGH | MEDIUM |
| EA-JAP-01 | aucun — procédural | N/A | N/A |
| EA-JAP-02 | Kuze Hiroaki | HIGH | HIGH comme abstraction |

---

# 11. Points à ne pas perdre lors de l’implémentation future

1. **Ne pas affecter Agūi aux huit armées Qing.**
2. **Ne pas confondre gouverneur/gouverneur général avec général.**
3. **Ne pas transformer les scopes de Bannière du mod en preuve que la formation elle-même est une Bannière historiquement cohérente.**
4. `CHI land 3` → Fuyu est le cas de correspondance régionale le plus solide.
5. Pour Hailancha, conserver explicitement l’origine **Solon** même si `manchu` doit être utilisé comme fallback V3.
6. Pour Qilikeqi, utiliser **Oirat** comme identité historique ; `mongol` n’est qu’un mapping V3.
7. Pour Mingliang, ne pas fonder l’admissibilité sur le poste de Guangzhou au jour exact : la transition de titulaire pendant Q40 n’est pas assez précisément datée.
8. Pour Techenge, ne pas anticiper son futur poste de Taiyuan : au 1776-01-01, le poste défendable est **Weining zongbing**.
9. `Edo_Guard_Army` : **ne pas forcer un personnage historique**.
10. `Kinai_Guard_Army` : Kuze Hiroaki est admissible en vertu de la charge d’**Ōsaka jōdai**, pas de son rang de daimyō.
11. KOR/MGL/TIB/RYU : **aucune formation = aucune création de général dans cette phase**.
12. Ne pas inventer de religion personnelle.
13. Ne pas inventer de lieux de naissance.
14. Ne pas inventer de jour/mois.
15. Portrait historique et DNA/template de jeu sont deux colonnes distinctes.

---

# 12. Sources principales consultées

## Dépôt du mod

- `common/history/military_formations/06_military_formations_asia.txt`, branche `cleanup-post-release`
- `common/country_definitions/00_countries.txt`
- `common/history/countries/chi - china.txt`
- `common/history/countries/ryu - ryukyu.txt`

## Qing / Chine

### Academia Sinica — 人名權威資料

- **Agūi (章佳阿桂)** — authority **000008**
- **Fuyu (富察傅玉)** — authority **001634**
- **Mingliang (富察明亮)** — authority **002606**
- **Hailancha (多拉爾海蘭察)** — authority **007452**
- **Wufu (富察五福)** — authority **004866**
- **Qilikeqi (鄂魯特齊里克齊)** — authority **012531**
- **Techenge (鈕祜祿特成額)** — authority **000929**
- **Fengshenge (鈕祜祿豐昇額)** — Academia Sinica biographical authority record/search result

### Academia Sinica — 清代職官資料庫

- `黑龍江將軍` — utilisé pour confirmer le mandat de Fuyu
- `廣州將軍` — utilisé pour contrôler la transition Mingliang/Yongwei

### Chinese Text Project / textes Qing numérisés

- Agūi person record **ctext:810478**
- `欽定八旗通志` 卷145 — biographie de Fengshenge
- `清史稿` — carrières et listes de mérite du Jinchuan
- `大清一統志` — hiérarchie des commandants du Jinchuan

## Japon

- **Kotobank / デジタル版 日本人名大辞典+Plus — 久世広明**
- **Kotobank — 大坂城代**
- listes historiques de titulaires de l’Ōsaka jōdai — Kuze Hiroaki, **1769–1777**

---

# 13. Conclusion

L’audit ne justifie pas dix remplacements mécaniques.

Il justifie :

- **8 candidats Qing historiquement militaires et actifs**, mais avec un degré d’abstraction variable parce que les formations du mod sont synthétiques ;
- **1 candidat japonais solide**, Kuze Hiroaki, pour la formation Kinai ;
- **1 refus méthodologique**, `Edo_Guard_Army`, où conserver un général procédural est plus historique que d’inventer une chaîne de commandement unique ;
- **aucune création** pour KOR, MGL, TIB ou RYU en l’absence de formation terrestre correspondante.

La prochaine phase d’implémentation devra utiliser le CSV comme **matrice de décision**, et non comme autorisation de gommer les réserves institutionnelles consignées dans ce rapport.
