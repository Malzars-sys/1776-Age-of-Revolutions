# CLEANUP-2D-5F — HISTORICAL GENERALS 1776 — AFRICA

**Projet :** Victoria 3 — *1776 – Age of Revolutions*  
**Dépôt :** `Malzars-sys/1776-Age-of-Revolutions`  
**Branche :** `cleanup-post-release`  
**Date de référence absolue :** **1776-01-01**  
**Statut :** **RECHERCHE UNIQUEMENT — aucune implémentation, aucun commit, aucun push.**

## 1. Résultat exécutif

L’audit identifie **41 formations terrestres africaines** dans les deux fichiers du dépôt : **8 en Afrique du Nord** et **33 en Afrique subsaharienne**. Sources de périmètre : https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/cleanup-post-release/common/history/military_formations/03_military_formations_north_africa.txt et https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/cleanup-post-release/common/history/military_formations/07_military_formations_subsaharan_africa.txt.

Bilan final : **8 `IMPLEMENT_HISTORICAL`**, **22 `KEEP_PROCEDURAL`**, **11 `PROCEDURAL_REQUIRED_COLLECTIVE_STRUCTURE`**.

> **Contrôle final Tunis :** un neuvième cas avait été provisoirement envisagé. Il a été déclassé en `KEEP_PROCEDURAL` car Ismaʿil Kahiya est bien attesté comme ministre/gendre d’Ali Bey, mais pas assez directement comme commandant unique de la formation au 1er janvier 1776. C’est exactement l’application de la règle « procédural plutôt qu’inventé ».

### Huit remplacements historiques recommandés

- **MAS — Ibrahim Bey of Mascara** — `THEATRE_COMMAND` — confiance **MEDIUM**.
- **CON — Salah Bey** — `THEATRE_COMMAND` — confiance **HIGH**.
- **MOR — Sidi Tahar ben Abdelhaq Fennich** — `HIGHER_COMMAND_ABSTRACTION` — confiance **MEDIUM**.
- **ETH — Dejazmach Wand Bewossen (Wänd Bäwäsän)** — `THEATRE_COMMAND` — confiance **HIGH**.
- **FTJ — Ibrahima Sori Mawdo** — `COLLECTIVE_HIGH_COMMAND` — confiance **HIGH**.
- **KRT — Sira Bo Kulibali (Coulibaly)** — `HIGHER_COMMAND_ABSTRACTION` — confiance **HIGH**.
- **SGU — Ngolo Diarra** — `HIGHER_COMMAND_ABSTRACTION` — confiance **HIGH**.
- **SWZ — Ngwane III** — `HIGHER_COMMAND_ABSTRACTION` — confiance **MEDIUM_HIGH**.

## 2. Méthode

Le test n’est pas « personnage important en 1776 », mais : **commandait-il réellement des forces terrestres au 1er janvier 1776 d’une manière que la formation du mod peut représenter sans déformer l’institution ?**

- souverain/gouverneur/bey/pacha ≠ automatiquement général ;
- une nomination ou victoire plus tard en 1776 n’est pas rétroprojetée au 1er janvier ;
- les structures claniques, segmentaires, confédérales ou à commandements multiples restent collectives/procédurales ;
- aucun jour/mois de naissance n’est inventé ;
- les titres réels (`dejazmach`, `almamy`, `faama`, chef tonjon, commandant d’artillerie…) sont préférés à des grades européens fictifs.

## 3. DNA / templates existants

Inspection de `https://github.com/Malzars-sys/1776-Age-of-Revolutions/tree/cleanup-post-release/common/dna_data` et `https://github.com/Malzars-sys/1776-Age-of-Revolutions/tree/cleanup-post-release/common/character_templates`, complétée par des recherches textuelles ciblées : **aucun DNA/template correspondant aux candidats retenus n’a été identifié**. Le CSV porte donc `NO_EXISTING_CANDIDATE_DNA_OR_TEMPLATE_IDENTIFIED`.

## 4.1 — F1 NORTH AFRICA

| ID | Tag | Formation | Candidat étudié/retenu | Mapping | Décision | Confiance |
|---|---|---|---|---|---|---|
| GEN1776-098 | `TUN` | `cleanup2d3b_tun_land_1` | Ismaʿil Kahiya / Ali Bey (examined, not adopted) | `NO_DEFENSIBLE_MAPPING` | **KEEP_PROCEDURAL** | HIGH |
| GEN1776-099 | `TRI` | `cleanup2d3b_tri_land_1` | Ali Pasha Karamanli (examined) | `NO_DEFENSIBLE_MAPPING` | **KEEP_PROCEDURAL** | HIGH |
| GEN1776-100 | `MAS` | `Jaish_alMohammadi` | Ibrahim Bey of Mascara | `THEATRE_COMMAND` | **IMPLEMENT_HISTORICAL** | MEDIUM |
| GEN1776-101 | `AIT` | `cleanup2d3b_ait_land_1` | El Hadj Bouzid Mokrani (examined) | `COLLECTIVE_HIGH_COMMAND` | **PROCEDURAL_REQUIRED_COLLECTIVE_STRUCTURE** | HIGH |
| GEN1776-102 | `CON` | `cleanup2d3b_con_land_1` | Salah Bey | `THEATRE_COMMAND` | **IMPLEMENT_HISTORICAL** | HIGH |
| GEN1776-103 | `DFR` | `cleanup2d3b_dfr_land_1` | Muhammad Tayrab ibn Ahmad Bukr (examined) | `NO_DEFENSIBLE_MAPPING` | **KEEP_PROCEDURAL** | HIGH |
| GEN1776-104 | `MOR` | `cleanup2d3b_mor_land_1` | Sidi Tahar ben Abdelhaq Fennich | `HIGHER_COMMAND_ABSTRACTION` | **IMPLEMENT_HISTORICAL** | MEDIUM |
| GEN1776-105 | `TUG` | `cleanup2d3b_tug_land_1` | — | `NO_DEFENSIBLE_MAPPING` | **KEEP_PROCEDURAL** | HIGH |

## 4.2 — F2 SUB-SAHARAN AFRICA

| ID | Tag | Formation | Candidat étudié/retenu | Mapping | Décision | Confiance |
|---|---|---|---|---|---|---|
| GEN1776-182 | `AGC` | `cleanup2d3b_agc_land_1` | — | `COLLECTIVE_HIGH_COMMAND` | **PROCEDURAL_REQUIRED_COLLECTIVE_STRUCTURE** | HIGH |
| GEN1776-183 | `ANK` | `cleanup2d3b_ank_land_1` | — | `NO_DEFENSIBLE_MAPPING` | **KEEP_PROCEDURAL** | HIGH |
| GEN1776-184 | `ASH` | `cleanup2d3b_ash_land_1` | Osei Kwadwo (examined) | `COLLECTIVE_HIGH_COMMAND` | **PROCEDURAL_REQUIRED_COLLECTIVE_STRUCTURE** | HIGH |
| GEN1776-185 | `BEN` | `cleanup2d3b_ben_land_1` | Oba Akengbuda (examined) | `NO_DEFENSIBLE_MAPPING` | **KEEP_PROCEDURAL** | HIGH |
| GEN1776-186 | `BGI` | `cleanup2d3b_bgi_land_1` | Muhammad al-Amin (examined) | `NO_DEFENSIBLE_MAPPING` | **KEEP_PROCEDURAL** | HIGH |
| GEN1776-187 | `BNY` | `cleanup2d3b_bny_land_1` | — | `NO_DEFENSIBLE_MAPPING` | **KEEP_PROCEDURAL** | HIGH |
| GEN1776-188 | `BOR` | `cleanup2d3b_bor_land_1` | Ali ibn Hamdun (examined) | `NO_DEFENSIBLE_MAPPING` | **KEEP_PROCEDURAL** | MEDIUM_HIGH |
| GEN1776-189 | `BRD` | `cleanup2d3b_brd_land_1` | — | `NO_DEFENSIBLE_MAPPING` | **KEEP_PROCEDURAL** | HIGH |
| GEN1776-190 | `BRG` | `cleanup2d3b_brg_land_1` | — | `COLLECTIVE_HIGH_COMMAND` | **PROCEDURAL_REQUIRED_COLLECTIVE_STRUCTURE** | HIGH |
| GEN1776-191 | `BST` | `cleanup2d3b_bst_land_1` | — | `COLLECTIVE_HIGH_COMMAND` | **PROCEDURAL_REQUIRED_COLLECTIVE_STRUCTURE** | HIGH |
| GEN1776-192 | `BUG` | `cleanup2d3b_bug_land_1` | — | `NO_DEFENSIBLE_MAPPING` | **KEEP_PROCEDURAL** | HIGH |
| GEN1776-193 | `DAH` | `cleanup2d3b_dah_land_1` | Kpengla (Yansunu) | `NO_DEFENSIBLE_MAPPING` | **KEEP_PROCEDURAL** | HIGH |
| GEN1776-194 | `ETH` | `cleanup2d3b_eth_land_1` | Dejazmach Wand Bewossen (Wänd Bäwäsän) | `THEATRE_COMMAND` | **IMPLEMENT_HISTORICAL** | HIGH |
| GEN1776-195 | `FTJ` | `cleanup2d3b_ftj_land_1` | Ibrahima Sori Mawdo | `COLLECTIVE_HIGH_COMMAND` | **IMPLEMENT_HISTORICAL** | HIGH |
| GEN1776-196 | `FTR` | `cleanup2d3b_ftr_land_1` | Suleyman Baal / Abdul Qadir Kan (examined) | `NO_DEFENSIBLE_MAPPING` | **KEEP_PROCEDURAL** | HIGH |
| GEN1776-197 | `GLD` | `cleanup2d3b_gld_land_1` | Mahamud Ibrahim (examined) | `NO_DEFENSIBLE_MAPPING` | **KEEP_PROCEDURAL** | HIGH |
| GEN1776-198 | `HAU` | `cleanup2d3b_hau_land_1` | Babari (examined, too early) | `NO_DEFENSIBLE_MAPPING` | **KEEP_PROCEDURAL** | HIGH |
| GEN1776-199 | `ISQ` | `cleanup2d3b_isq_land_1` | — | `COLLECTIVE_HIGH_COMMAND` | **PROCEDURAL_REQUIRED_COLLECTIVE_STRUCTURE** | HIGH |
| GEN1776-200 | `KON` | `cleanup2d3b_kon_land_1` | — | `NO_DEFENSIBLE_MAPPING` | **KEEP_PROCEDURAL** | HIGH |
| GEN1776-201 | `KRG` | `cleanup2d3b_krg_land_1` | — | `NO_DEFENSIBLE_MAPPING` | **KEEP_PROCEDURAL** | HIGH |
| GEN1776-202 | `KRT` | `cleanup2d3b_krt_land_1` | Sira Bo Kulibali (Coulibaly) | `HIGHER_COMMAND_ABSTRACTION` | **IMPLEMENT_HISTORICAL** | HIGH |
| GEN1776-203 | `MAD` | `cleanup2d3b_mad_land_1` | — | `COLLECTIVE_HIGH_COMMAND` | **PROCEDURAL_REQUIRED_COLLECTIVE_STRUCTURE** | HIGH |
| GEN1776-204 | `MBS` | `cleanup2d3b_mbs_land_1` | Mazrui officeholders around the 1770s (examined) | `NO_DEFENSIBLE_MAPPING` | **KEEP_PROCEDURAL** | HIGH |
| GEN1776-205 | `MJT` | `cleanup2d3b_mjt_land_1` | — | `COLLECTIVE_HIGH_COMMAND` | **PROCEDURAL_REQUIRED_COLLECTIVE_STRUCTURE** | HIGH |
| GEN1776-206 | `MSN` | `cleanup2d3b_msn_land_1` | — | `COLLECTIVE_HIGH_COMMAND` | **PROCEDURAL_REQUIRED_COLLECTIVE_STRUCTURE** | HIGH |
| GEN1776-207 | `OYO` | `cleanup2d3b_oyo_land_1` | Are Ona Kakanfo officeholder (identity unresolved) | `MILITARY_OFFICEHOLDER` | **KEEP_PROCEDURAL** | HIGH |
| GEN1776-208 | `RWD` | `cleanup2d3b_rwd_land_1` | — | `NO_DEFENSIBLE_MAPPING` | **KEEP_PROCEDURAL** | HIGH |
| GEN1776-209 | `SGU` | `cleanup2d3b_sgu_land_1` | Ngolo Diarra | `HIGHER_COMMAND_ABSTRACTION` | **IMPLEMENT_HISTORICAL** | HIGH |
| GEN1776-210 | `SWZ` | `cleanup2d3b_swz_land_1` | Ngwane III | `HIGHER_COMMAND_ABSTRACTION` | **IMPLEMENT_HISTORICAL** | MEDIUM_HIGH |
| GEN1776-211 | `TGI` | `cleanup2d3b_tgi_land_1` | — | `NO_DEFENSIBLE_MAPPING` | **KEEP_PROCEDURAL** | HIGH |
| GEN1776-212 | `WAD` | `cleanup2d3b_wad_land_1` | Muhammad Jawda (examined) | `NO_DEFENSIBLE_MAPPING` | **KEEP_PROCEDURAL** | MEDIUM_HIGH |
| GEN1776-213 | `WBL` | `cleanup2d3b_wbl_land_1` | Adam Kok I (examined) | `COLLECTIVE_HIGH_COMMAND` | **PROCEDURAL_REQUIRED_COLLECTIVE_STRUCTURE** | HIGH |
| GEN1776-214 | `WSG` | `cleanup2d3b_wsg_land_1` | — | `COLLECTIVE_HIGH_COMMAND` | **PROCEDURAL_REQUIRED_COLLECTIVE_STRUCTURE** | HIGH |

## 5. Dossiers positifs détaillés

### MAS — Ibrahim Bey of Mascara

- **Formation :** `Jaish_alMohammadi` — Beylik of Mascara / Western Beylik of Algiers.
- **Décision / mapping :** `IMPLEMENT_HISTORICAL` / `THEATRE_COMMAND` — confiance **MEDIUM**.
- **Naissance :** inconnue (`UNKNOWN`), lieu non établi; polité : non établie.
- **Âge au 1776-01-01 :** inconnu.
- **Décès :** non établi (`UNKNOWN`).
- **Religion / culture :** Sunni Islam (office/polity context) / Ottoman-Algerian / Maghrebi; exact personal origin unresolved.
- **Titre/fonction militaire :** Bey of Mascara. Regional military-political commander of the western beylik; documented participant in the defense against the Spanish expedition.
- **Fonction :** 1775 → 1776.
- **Théâtre :** Western Algeria / Mascara-Oran-Algiers.
- **Preuve pour la date de référence :** A specialist chronology places Ibrahim as bey in 1775–1776 and explicitly states that he participated, with his khalifa, against the 1775 expedition.
- **Garde-fou institutionnel :** Exact day of succession during 1776 was not recovered; confidence is therefore MEDIUM, but his tenure starts in 1775 and covers 1776-01-01.
- **Sources :**
  - https://www.archivodelafrontera.com/docs/cronologias-y-algunos-personajes/
  - Ismet Terki-Hassaine, work on Spanish-Ottoman Algerian relations, underlying chronology.

### CON — Salah Bey

- **Formation :** `cleanup2d3b_con_land_1` — Beylik of Constantine.
- **Décision / mapping :** `IMPLEMENT_HISTORICAL` / `THEATRE_COMMAND` — confiance **HIGH**.
- **Naissance :** 1725 (`YEAR`), İzmir (Smyrna); polité : Ottoman Empire.
- **Âge au 1776-01-01 :** 50-51.
- **Décès :** 1792 (`YEAR`).
- **Religion / culture :** Sunni Islam / Ottoman/Turkish-born; Algerian-Ottoman elite.
- **Titre/fonction militaire :** Bey of Constantine. Regional commander with documented military expeditions/campaigns; associated with resistance to the Spanish expedition of 1775.
- **Fonction :** 1771 → 1792.
- **Théâtre :** Eastern Algerian beylik; Algiers theatre in 1775.
- **Preuve pour la date de référence :** The 1771–1792 tenure covers the date and specialized work explicitly treats Salah Bey’s military campaigns. Sources also connect him with the 1775 defense.
- **Garde-fou institutionnel :** Use only as regional theatre command. The valid logic is documented command, not “governor = general”.
- **Sources :**
  - https://bina.bulac.fr/s/bina/item/335499
  - Specialized Algerian study on the military campaigns of Salah Bey during his rule of Constantine (1771–1792).
  - CRASC/Insaniyat regional biographical studies.

### MOR — Sidi Tahar ben Abdelhaq Fennich

- **Formation :** `cleanup2d3b_mor_land_1` — Sultanate of Morocco.
- **Décision / mapping :** `IMPLEMENT_HISTORICAL` / `HIGHER_COMMAND_ABSTRACTION` — confiance **MEDIUM**.
- **Naissance :** inconnue (`UNKNOWN`), Salé (probable family/local association; exact birth evidence remains insufficient); polité : Sultanate of Morocco.
- **Âge au 1776-01-01 :** inconnu.
- **Décès :** non établi (`UNKNOWN`).
- **Religion / culture :** Sunni Islam / Moroccan/Maghrebi; Salé notable family, often described as Andalusi-origin.
- **Titre/fonction militaire :** Qāʾid / commander of Moroccan artillery. Commander of the Moroccan artillery; military specialist also employed as a diplomat.
- **Fonction :** by 1773 → after 1777.
- **Théâtre :** Moroccan royal army / artillery arm.
- **Preuve pour la date de référence :** The title “commander of Moroccan artillery” is attached to Fennich in sources for 1773 and 1777. Continuity through 1776 is a reasonable but inferential bridge.
- **Garde-fou institutionnel :** Do not present him as commander-in-chief of all Moroccan land forces.
- **Sources :**
  - https://en.yabiladi.com/articles/details/66826/moroccan-diplomats-tahar-fennish-sultan
  - https://founders.archives.gov/documents/Jefferson/01-11-02-0077
  - Rabih Saied, dissertation on French views of Moroccan envoys, as cited in later studies.

### ETH — Dejazmach Wand Bewossen (Wänd Bäwäsän)

- **Formation :** `cleanup2d3b_eth_land_1` — Ethiopia / Gondarine-Begemder sphere.
- **Décision / mapping :** `IMPLEMENT_HISTORICAL` / `THEATRE_COMMAND` — confiance **HIGH**.
- **Naissance :** inconnue (`UNKNOWN`), lieu non établi; polité : non établie.
- **Âge au 1776-01-01 :** inconnu.
- **Décès :** 1777-12-10 (`DAY`).
- **Religion / culture :** Ethiopian Orthodox Christianity (high-confidence social/political context; personal profession not separately documented here) / Amhara/Ethiopian highland nobility; V3 mapping to verify.
- **Titre/fonction militaire :** Dejazmach; governor/balabbat of Begemder. Regional warlord commanding substantial Begemder/Lasta forces; principal commander in the Sarbakusa conflict.
- **Fonction :** 1770 → 1777.
- **Théâtre :** Begemder, Gondar, Lake Tana / northern Ethiopian highlands.
- **Preuve pour la date de référence :** James Bruce’s near-contemporary account explicitly places “Powussen of … Begemder” at the head of forces raised in the region. Later specialist reference work identifies Wand Bewossen as a prominent warlord.
- **Garde-fou institutionnel :** Ethiopia was in the Zemene Mesafint. The mapping must remain regional/factional and must not imply centralized imperial command.
- **Sources :**
  - https://en.wikisource.org/wiki/Travels_to_Discover_the_Source_of_the_Nile%3A_in_the_Years_1768%2C_1769%2C_1770%2C_1771%2C_1772%2C_and_1773%2FVolume_4%2FBk7Ch5
  - https://en.sewasew.com/p/wa-nd-ba-wa-sa-n-%28%E1%8B%88%E1%8A%95%E1%8B%B5-%E1%89%A0%E1%8B%88%E1%88%B0%E1%8A%95%29
  - Encyclopaedia Aethiopica entry on Wänd Bäwäsän.

### FTJ — Ibrahima Sori Mawdo

- **Formation :** `cleanup2d3b_ftj_land_1` — Futa Jallon.
- **Décision / mapping :** `IMPLEMENT_HISTORICAL` / `COLLECTIVE_HIGH_COMMAND` — confiance **HIGH**.
- **Naissance :** inconnue (`UNKNOWN`), lieu non établi; polité : non établie.
- **Âge au 1776-01-01 :** inconnu.
- **Décès :** 1784 (common scholarly chronology; traditions vary) (`YEAR_DISPUTED`).
- **Religion / culture :** Sunni Islam / Fulbe/Fulani.
- **Titre/fonction militaire :** War leader / Almamy or acting supreme leader depending chronology. Supra-provincial war chief coordinating forces of the Futa Jallon confederation.
- **Fonction :** at least by 1770 as major war leader in one strong chronology → 1784 (common scholarly chronology).
- **Théâtre :** Futa Jallon and neighboring campaigns.
- **Preuve pour la date de référence :** Independent traditions and modern scholarship agree on Sori Mawdo’s military leadership before/during 1776 even when accession dates differ. TDV notes that in 1776 he adopted a title explicitly framing obedience to him as commander/head of state.
- **Garde-fou institutionnel :** Futa Jallon was a confederation of nine provinces with a council and provincial chiefs. Sori is the best documented coordinating war leader, not a European-style national general.
- **Sources :**
  - https://islamansiklopedisi.org.tr/futa-calon
  - https://www.webfuuta.site/bibliotheque/aisow/crfj/chronoFJ.html
  - https://books.openedition.org/pur/191878?lang=fr

### KRT — Sira Bo Kulibali (Coulibaly)

- **Formation :** `cleanup2d3b_krt_land_1` — Kaarta.
- **Décision / mapping :** `IMPLEMENT_HISTORICAL` / `HIGHER_COMMAND_ABSTRACTION` — confiance **HIGH**.
- **Naissance :** inconnue (`UNKNOWN`), lieu non établi; polité : non établie.
- **Âge au 1776-01-01 :** inconnu.
- **Décès :** c.1780 (`APPROX_YEAR`).
- **Religion / culture :** Bamana traditional religion / non-Islamic dynastic context; personal practice not directly documented / Bamana/Bambara (Massassi).
- **Titre/fonction militaire :** King / faama of Kaarta. Sovereign-war leader of the Massassi restoration; military reconquest is integral to his political authority.
- **Fonction :** c.1760-1761 → c.1780.
- **Théâtre :** Kaarta / western Middle Niger.
- **Preuve pour la date de référence :** Universalis and Treccani place Sira Bo in power across the reference date and directly connect his reign to restored Kaarta independence.
- **Garde-fou institutionnel :** Use indigenous sovereign-war-leader logic; do not invent a European rank.
- **Sources :**
  - https://www.universalis.fr/encyclopedie/kaarta/
  - https://www.treccani.it/enciclopedia/kaarta_%28Dizionario-di-Storia%29/
  - UNESCO General History of Africa, volume on the 16th-18th centuries (Kaarta/Segu discussion).

### SGU — Ngolo Diarra

- **Formation :** `cleanup2d3b_sgu_land_1` — Segu.
- **Décision / mapping :** `IMPLEMENT_HISTORICAL` / `HIGHER_COMMAND_ABSTRACTION` — confiance **HIGH**.
- **Naissance :** c.1718 (`APPROX_YEAR`), Niola, region of Koulikoro (reported in later syntheses); polité : Middle Niger/Bamana sphere; exact local sovereignty unresolved.
- **Âge au 1776-01-01 :** about 57-58.
- **Décès :** 1787 (`YEAR`).
- **Religion / culture :** Bamana religious tradition; exact personal affiliation unresolved / Bamana/Bambara.
- **Titre/fonction militaire :** Faama / ruler of Segu; former tonjon chief. Military leader from the tonjon warrior organization who seized and consolidated political power.
- **Fonction :** 1766 → 1787.
- **Théâtre :** Segu / Middle Niger.
- **Preuve pour la date de référence :** The chronology places him firmly in power in 1776, and accounts of his career explicitly trace his rise through the tonjon military hierarchy.
- **Garde-fou institutionnel :** Use indigenous title/function; do not invent a European general rank.
- **Sources :**
  - https://www.africanhistoryextra.com/p/the-empire-of-segu-1712-1861-ethnic
  - UNESCO General History of Africa, volume on the 16th-18th centuries (Segu/Bamana discussion).

### SWZ — Ngwane III

- **Formation :** `cleanup2d3b_swz_land_1` — Swazi / proto-Swazi chiefdom.
- **Décision / mapping :** `IMPLEMENT_HISTORICAL` / `HIGHER_COMMAND_ABSTRACTION` — confiance **MEDIUM_HIGH**.
- **Naissance :** inconnue (`UNKNOWN`), lieu non établi; polité : non établie.
- **Âge au 1776-01-01 :** inconnu.
- **Décès :** 1780 (`YEAR`).
- **Religion / culture :** Swazi/Nguni traditional religion / Swazi / Nguni.
- **Titre/fonction militaire :** King/chief Ngwane III. Chief and war leader directing migration, conquest and incorporation of subordinate clans.
- **Fonction :** 1750s leadership attested → 1780.
- **Théâtre :** Pongola / early Swazi settlement and expansion zone.
- **Preuve pour la date de référence :** Biographical and Cambridge scholarship directly describe Ngwane leading his chiefdom and expansion before the reference date; he remained alive and in leadership in 1776.
- **Garde-fou institutionnel :** Swazi kingship was embedded in royal/dual structures and subordinate chiefdoms; do not describe him as a modern national general.
- **Sources :**
  - https://encyclopaediaafricana.com/ngwane-iii/
  - Cambridge University Press, Kingdoms and Chiefdoms of Southeastern Africa, chronology of eighteenth-century political reconfiguration.

## 6. Structures collectives : pourquoi un personnage unique serait trompeur

### AIT — Aït Abbas / Mokrani sphere

Do not adopt a single general: dynastic, clan and regional military authority cannot be securely collapsed into one formation command for 1776.

**Pourquoi :** The formation aggregates clan/dynastic command rather than a modern national army.

**Source de structure :** Specialized studies of the Mokrani / Beni Abbas political structure and chronology.

### AGC — Angoche Sultanate

No date-safe 1776 individual command recovered; the early Angoche polity is reconstructed from later traditions and regional networks.

**Pourquoi :** Do not impose a modern centralized national army on early Angoche.

**Source de structure :** https://www.cambridge.org/core/journals/journal-of-african-history/article/early-history-of-the-sultanate-of-angoche/BD49CBB7EA60F18F4EEFBC28D421C5ED

### ASH — Asante

Do not map the Asantehene alone to the formation. Asante warfare operated through multiple chiefs, stools, divisions/wings and contingents.

**Pourquoi :** One character would misrepresent a documented multi-chief high-command system.

**Source de structure :** https://www.persee.fr/doc/cea_0008-0055_1976_num_16_61_2905

### BRG — Borgu

Borgu is best treated as a segmentary political field of multiple kingdoms/chiefdoms rather than a unitary national command.

**Pourquoi :** A single “Borgu general” would be structurally misleading.

**Source de structure :** https://dalspace.library.dal.ca/items/e9fe3da2-31a6-4ad1-a243-87f43b844905/full

### BST — Basutoland / proto-Basotho polities

The centralized Basotho polity associated with Moshoeshoe belongs to the 19th century; a 1776 “Basutoland general” would be anachronistic.

**Pourquoi :** Represent chiefdom forces procedurally; do not back-project the later Basotho nation-state.

**Source de structure :** Oxford Research Encyclopedia / southern African state-formation scholarship on the 19th-century emergence of Basotho political unity.

### ISQ — Isaaq

Retain collective classification. Northern Somali pastoral politics were strongly segmentary and lineage-based; no unitary 1776 formation commander is defensible.

**Pourquoi :** A single “Isaaq general” would impose a centralized institution unsupported by the political structure.

**Source de structure :** I. M. Lewis, A Pastoral Democracy (International African Institute).

### MAD — Madagascar / Merina highlands abstraction

1776 predates the late-18th-century Merina reunification. The formation spans politically fragmented territory; no single historical “Madagascar general” is defensible.

**Pourquoi :** Do not back-project Andrianampoinimerina’s later unification or c.1785+ warfare into 1776.

**Source de structure :** https://www.persee.fr/doc/outre_0300-9513_1974_num_61_224_1776

### MJT — Majerteen

The Majerteen sultanate emerges in the 18th century, but exact 1776 central command is not securely identifiable and northern Somali military politics remained lineage-based.

**Pourquoi :** Do not use later 19th-century centralization for 1776.

**Source de structure :** https://www.cambridge.org/core/books/abs/colonial-chaos-in-the-southern-red-sea/sultan-uthmans-salvage-agreements/D1EDDB34CC5C4A6A252CB42FD97C6F16

### MSN — Massina / Macina

In 1776 Massina is not the 1818 Dina/empire. It consists of Fulbe groups/clans under multiple ardo and under Segu suzerainty.

**Pourquoi :** A unique national general is materially misleading for 1776 Massina.

**Source de structure :** https://www.larousse.fr/encyclopedie/autre-region/Macina/130928

### WBL — Griqualand / pre-Griqua communities

Do not adopt as a single general. In 1776 the “Griqua” territorial/state identity is itself anachronistic; communities were dispersed and the name Griqua was adopted later.

**Pourquoi :** The formation is an abstraction of several communities, not an 18th-century Griqua state army.

**Source de structure :** https://books.openedition.org/pur/255616

### WSG — Warsangali

No date-safe individual field commander identified; lineage/clan political organization makes a unique general particularly hazardous.

**Pourquoi :** Use collective procedural representation unless a specialist source identifies an actual 1776 field commander.

**Source de structure :** I. M. Lewis, A Pastoral Democracy and northern Somali lineage-political studies.

## 7. Exclusions temporelles / faux amis

- **Tunis — Hammuda ibn Ali :** ne pas utiliser sa future fonction de Bey al-Mahalla pour le setup du 1er janvier 1776 ; la nomination formelle est postérieure.
- **Mascara — Mohammed el-Kébir :** son beylicat pertinent commence en 1779.
- **Futa Toro — Suleyman Baal / Abdul Qadir Kan :** la révolution torodbe est un processus de 1776 ; aucune justification pour faire commencer le nouvel ordre au 1er janvier.
- **Madagascar/Merina :** ne pas rétroprojeter l’unification militaire de la fin des années 1780.
- **Massina :** ne pas rétroprojeter la Dina/Empire de 1818.
- **Basutoland et Griqualand :** ne pas projeter les constructions politiques du XIXe siècle sur 1776.

## 8. Cas Salah Bey — justification spécifique

Salah Bey est retenu **non parce qu’il est bey/gouverneur**, mais parce que son dossier comprend des campagnes terrestres documentées pendant son office 1771–1792 et une implication militaire dans le contexte de l’expédition espagnole de 1775. Le mapping doit rester `THEATRE_COMMAND`, régional, et ne jamais être formulé comme « gouverneur = général ». La BULAC/BiNA conserve en outre un manuscrit numérisé centré sur sa trajectoire : https://bina.bulac.fr/s/bina/item/335499

## 9. Limites et règles d’implémentation future

- Les traditions orales tardivement consignées sont une raison de conserver `UNKNOWN`, pas de fabriquer une date.
- Les religions/cultures sont parfois indiquées comme contexte de cour ou de société plutôt que comme certitude biographique individuelle.
- Les mappings V3 de lieux de naissance doivent être revalidés au moment de l’implémentation ; le rapport n’invente pas un State quand il n’est pas sûr.
- Aucune recommandation de traits/idéologie/DNA n’est implémentée ici.

## 10. Sources principales

- Repo North Africa : https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/cleanup-post-release/common/history/military_formations/03_military_formations_north_africa.txt
- Repo Sub-Saharan Africa : https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/cleanup-post-release/common/history/military_formations/07_military_formations_subsaharan_africa.txt
- Mascara / Algérie ottomane : https://www.archivodelafrontera.com/docs/cronologias-y-algunos-personajes/
- Salah Bey — BULAC/BiNA : https://bina.bulac.fr/s/bina/item/335499
- Wand Bewossen — James Bruce : https://en.wikisource.org/wiki/Travels_to_Discover_the_Source_of_the_Nile%3A_in_the_Years_1768%2C_1769%2C_1770%2C_1771%2C_1772%2C_and_1773%2FVolume_4%2FBk7Ch5
- Futa Jallon — TDV : https://islamansiklopedisi.org.tr/futa-calon
- Futa Jallon — Chroniques et Récits : https://www.webfuuta.site/bibliotheque/aisow/crfj/chronoFJ.html
- Kaarta — Universalis : https://www.universalis.fr/encyclopedie/kaarta/
- Kaarta — Treccani : https://www.treccani.it/enciclopedia/kaarta_%28Dizionario-di-Storia%29/
- Ngwane III — Encyclopaedia Africana : https://encyclopaediaafricana.com/ngwane-iii/
- Asante — Emmanuel Terray : https://www.persee.fr/doc/cea_0008-0055_1976_num_16_61_2905
- Futa Toro — Oumar Kane / AfricaBib : https://www.africabib.org/rec.php?RID=119546809
- Massina — Larousse : https://www.larousse.fr/encyclopedie/autre-region/Macina/130928
- Merina warfare : https://www.persee.fr/doc/outre_0300-9513_1974_num_61_224_1776
- Kpengla : https://www.editions-harmattan.fr/catalogue/livre/biographie-du-roi-kpengla-du-danhome-1774-1789/13987
- Geledi — Virginia Luling/UCL : https://discovery.ucl.ac.uk/id/eprint/1317929/
- Borgu segmentary society : https://dalspace.library.dal.ca/items/e9fe3da2-31a6-4ad1-a243-87f43b844905/full

---

**Conclusion :** le setup africain de 1776 doit représenter des commandements réels sans transformer artificiellement chaque formation en armée nationale moderne. Le CSV conserve explicitement les incertitudes et les cas collectifs afin qu’une phase d’implémentation ultérieure puisse rester historiquement défendable.