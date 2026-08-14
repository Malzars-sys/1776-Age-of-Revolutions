# CLEANUP-2D-5K — HISTORICAL GENERALS 1776 — SOUTHEAST ASIA

## 1. Métadonnées et règle de travail

- **Projet :** Victoria 3 — *1776 Age of Revolutions*
- **Dépôt :** `Malzars-sys/1776-Age-of-Revolutions`
- **Branche auditée :** `cleanup-post-release`
- **Phase :** `CLEANUP-2D-5K`
- **Date de référence absolue :** **1776-01-01**
- **Nature :** recherche historique uniquement.
- **Implémentation :** **aucune**. Aucun fichier gameplay n'a été modifié, aucun commit/push n'a été effectué.

La règle d'admissibilité appliquée est volontairement stricte : un personnage doit être vivant, historiquement attesté et exercer **au 1er janvier 1776** un commandement terrestre ou une fonction militaire suffisamment proche de la formation du mod. Un souverain n'est pas transformé en général simplement parce qu'il gouverne politiquement l'État.

## 2. Périmètre réellement trouvé dans le dépôt

Le fichier courant [`common/history/military_formations/06_military_formations_asia.txt`](https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/cleanup-post-release/common/history/military_formations/06_military_formations_asia.txt) contient **29 formations terrestres relevant de l'Asie du Sud-Est / Insulinde** dans le périmètre demandé, entre `GEN1776-151` et `GEN1776-181`, en excluant les deux formations japonaises `GEN1776-154` et `GEN1776-155`.

Le tag `DAI` existe bien dans l'architecture pays, mais **aucune formation terrestre `c:DAI` n'est présente dans ce fichier courant**. Il est donc conservé comme note d'architecture, sans création artificielle d'un général dans cette phase.

## 3. Conclusion exécutive

Sur les 29 formations terrestres auditables :

- **4 affectations nommées sont recommandées :**
  1. `BUR` — **Maha Thiha Thura** : conserver l'identité, reconstruire le profil.
  2. `SIA` — **Chao Phraya Chakri (Thongduang)** : conserver l'identité, reconstruire le profil.
  3. `PHI` — **Simón de Anda y Salazar** : remplacer le général procédural.
  4. `JOH` — **Raja Haji Fisabilillah**, sous son office de **Engku Kelana** en 1776 : remplacer le général procédural.
- **24 lignes** restent procédurales ou procédurales avec rework structurel.
- **1 cas** sont explicitement différés pour inadéquation de périmètre politique.
- `DAI` reçoit **aucune affectation**, faute de formation terrestre actuelle.

Les cas les plus importants à **ne pas introduire** sont :
- **Luo Fangbo** pour `LAN` : Lanfang est fondée en **1777**, donc le tag/office est anachronique au 1776-01-01.
- **Kawila** pour `CMI` : son pouvoir à Chiang Mai appartient à la phase postérieure, avec nomination en **1782** ; en 1776 son ancrage est Lampang/Lanna.
- **Mangkunegara I** pour `SRK` : excellent commandant, mais commandant d'un appareil mangkunegaran semi-autonome, pas automatiquement de la formation générique du Sunanate de Surakarta.
- **officiers VOC trouvés dans des actes de 1776** pour `DEI` : attestations postérieures au 1er janvier et absence de preuve d'un commandement de toute la formation à la date de référence.

## 4. Matrice complète des formations

| GEN ID | Tag | Formation | Statut dépôt actuel | Décision recherche | Candidat |
|---|---|---|---|---|---|
| GEN1776-151 | `DEI` | Koninklijk_Nederlandsch_Indisch_Leger | PROCEDURAL_ALLOWED | **KEEP_PROCEDURAL** | Gideon Dulez/Dubez; Johan George Englert |
| GEN1776-152 | `BUR` | tatmadaw | IMPLEMENT_NAMED_HISTORICAL_GENERAL | **REBUILD_NAMED_HISTORICAL_GENERAL** | Maha Thiha Thura |
| GEN1776-153 | `PHI` | ejercito_de_filipinas | PROCEDURAL_ALLOWED | **IMPLEMENT_NAMED_HISTORICAL_GENERAL** | Simón de Anda y Salazar |
| GEN1776-156 | `ACE` | cleanup2d3b_ace_land_1 | PROCEDURAL_ALLOWED | **KEEP_PROCEDURAL** | — |
| GEN1776-157 | `BAL` | cleanup2d3b_bal_land_1 | PROCEDURAL_ALLOWED_PENDING_STRUCTURE_REWORK | **KEEP_PROCEDURAL_PENDING_STRUCTURE_REWORK** | — |
| GEN1776-158 | `BLG` | cleanup2d3b_blg_land_1 | PROCEDURAL_ALLOWED | **KEEP_PROCEDURAL** | — |
| GEN1776-159 | `BNJ` | cleanup2d3b_bnj_land_1 | PROCEDURAL_ALLOWED | **KEEP_PROCEDURAL** | — |
| GEN1776-160 | `BRU` | cleanup2d3b_bru_land_1 | PROCEDURAL_ALLOWED | **KEEP_PROCEDURAL** | — |
| GEN1776-161 | `BTN` | cleanup2d3b_btn_land_1 | PROCEDURAL_ALLOWED | **KEEP_PROCEDURAL** | — |
| GEN1776-162 | `CAM` | cleanup2d3b_cam_land_1 | PROCEDURAL_ALLOWED_PENDING_STRUCTURE_REWORK | **KEEP_PROCEDURAL_PENDING_STRUCTURE_REWORK** | — |
| GEN1776-163 | `CHP` | cleanup2d3b_chp_land_1 | PROCEDURAL_ALLOWED_PENDING_STRUCTURE_REWORK | **KEEP_PROCEDURAL_PENDING_STRUCTURE_REWORK** | — |
| GEN1776-164 | `CMI` | cleanup2d3b_cmi_land_1 | PROCEDURAL_ALLOWED_PENDING_STRUCTURE_REWORK | **KEEP_PROCEDURAL_PENDING_STRUCTURE_REWORK** | Kawila |
| GEN1776-165 | `JMB` | cleanup2d3b_jmb_land_1 | PROCEDURAL_ALLOWED_PENDING_STRUCTURE_REWORK | **KEEP_PROCEDURAL_PENDING_STRUCTURE_REWORK** | — |
| GEN1776-166 | `JOH` | cleanup2d3b_joh_land_1 | PROCEDURAL_ALLOWED | **IMPLEMENT_NAMED_HISTORICAL_GENERAL** | Raja Haji Fisabilillah |
| GEN1776-167 | `KTI` | cleanup2d3b_kti_land_1 | PROCEDURAL_ALLOWED | **KEEP_PROCEDURAL** | — |
| GEN1776-168 | `LAN` | cleanup2d3b_lan_land_1 | PROCEDURAL_ALLOWED_PENDING_STRUCTURE_REWORK | **KEEP_PROCEDURAL_PENDING_STRUCTURE_REWORK** | Luo Fangbo |
| GEN1776-169 | `LUA` | cleanup2d3b_lua_land_1 | PROCEDURAL_ALLOWED_PENDING_STRUCTURE_REWORK | **KEEP_PROCEDURAL_PENDING_STRUCTURE_REWORK** | — |
| GEN1776-170 | `MGD` | cleanup2d3b_mgd_land_1 | PROCEDURAL_ALLOWED | **KEEP_PROCEDURAL** | — |
| GEN1776-171 | `PON` | cleanup2d3b_pon_land_1 | PROCEDURAL_ALLOWED | **KEEP_PROCEDURAL** | — |
| GEN1776-172 | `PRK` | cleanup2d3b_prk_land_1 | PROCEDURAL_ALLOWED | **KEEP_PROCEDURAL** | — |
| GEN1776-173 | `SAK` | cleanup2d3b_sak_land_1 | PROCEDURAL_ALLOWED | **KEEP_PROCEDURAL** | — |
| GEN1776-174 | `SEL` | cleanup2d3b_sel_land_1 | PROCEDURAL_ALLOWED | **KEEP_PROCEDURAL** | — |
| GEN1776-175 | `SIA` | cleanup2d3b_sia_land_1 | IMPLEMENT_NAMED_HISTORICAL_GENERAL | **REBUILD_NAMED_HISTORICAL_GENERAL** | Chao Phraya Chakri (Thongduang) |
| GEN1776-176 | `SMB` | cleanup2d3b_smb_land_1 | PROCEDURAL_ALLOWED | **KEEP_PROCEDURAL** | — |
| GEN1776-177 | `SRK` | cleanup2d3b_srk_land_1 | PROCEDURAL_ALLOWED | **DEFER_POLITY_SCOPE_MISMATCH_KEEP_PROCEDURAL** | Mangkunegara I (Raden Mas Said) |
| GEN1776-178 | `STG` | cleanup2d3b_stg_land_1 | PROCEDURAL_ALLOWED | **KEEP_PROCEDURAL** | — |
| GEN1776-179 | `SUL` | cleanup2d3b_sul_land_1 | PROCEDURAL_ALLOWED | **KEEP_PROCEDURAL** | — |
| GEN1776-180 | `TID` | cleanup2d3b_tid_land_1 | PROCEDURAL_ALLOWED | **KEEP_PROCEDURAL** | — |
| GEN1776-181 | `YOG` | cleanup2d3b_yog_land_1 | PROCEDURAL_ALLOWED | **KEEP_PROCEDURAL** | — |
| — | `DAI` | — | NO_LAND_FORMATION_FOUND_IN_CURRENT_ASIA_FORMATION_FILE | **NO_GENERAL_ASSIGNMENT_NO_CURRENT_LAND_FORMATION** | — |

## 5. Dossiers recommandés

### 5.1 `SIA` — Chao Phraya Chakri (Thongduang)

**Décision : `REBUILD_NAMED_HISTORICAL_GENERAL` — confiance élevée.**

Le personnage actuellement nommé est le bon, mais l'entrée du dépôt utilise encore `template = default` sans date de naissance, culture, religion, traits ou DNA explicites dans l'entrée de formation.

#### Identité et date de naissance

- Nom personnel : **Thongduang / Thong Duang** (ทองด้วง).
- Titre au **1776-01-01** : **Chao Phraya Chakri**.
- Date recommandée pour le calendrier grégorien : **1737-03-20**.
- `birth_date_precision` : **EXACT_DAY_MONTH_CALENDAR_CONVERSION_RESOLVED_WITH_NOTE**.
- Lieu : **Ayutthaya**.
- Polité : royaume d'Ayutthaya.
- Mapping V3 recommandé : **`STATE_BANGKOK`**, qui est le meilleur rattachement régional actuel pour Ayutthaya/centre siamois.

Le Département thaïlandais des Beaux-Arts donne le **20 mars B.E. 2279**. Une difficulté importante vient du fait que les années thaïlandaises historiques ne commençaient pas au 1er janvier : le Nouvel An a longtemps été placé autour de Songkran/avril. Certaines pages institutionnelles anglophones soustraient simplement 543 et obtiennent **1736** ; les autorités modernes et catalogues internationaux donnent couramment **1737**. Pour éviter précisément le type d'erreur de date déjà observé dans le mod, le CSV recommande **1737-03-20** et conserve la note de conversion.

#### Fonction militaire au 1er janvier 1776

La bibliothèque de King Mongkut's University of Technology Thonburi donne la progression suivante :
- Chao Phraya Chakri en **1772** ;
- commandant d'avant-garde dans les campagnes de **1773** ;
- **commandant en chef en 1775** ;
- déploiement contre l'invasion birmane de 1775, puis redirection vers **Phitsanulok**.

Il ne faut **pas** lui donner au 1er janvier le titre de **Somdet Chao Phraya Maha Kasat Suek** : la même chronologie place cette élévation **après** sa campagne orientale de 1776.

#### Culture, religion, origine, traits

- Culture historique : **Siamoise/thaïe** dans le cadre politico-militaire de Thonburi.
- Origine : famille noble/administrative d'Ayutthaya ; traditions généalogiques postérieures lui attribuent une ascendance paternelle mon et maternelle chinoise.
- Religion : **bouddhisme theravāda** ; son ordination monastique de jeunesse est explicitement rapportée.
- Traits défendables :
  - commandant expérimenté — **HIGH** ;
  - stratège défensif — **HIGH** ;
  - commandant offensif / avant-garde — **HIGH** ;
  - brave/tenace — **MEDIUM**.

#### Portrait / DNA

Des portraits royaux postérieurs de Rama I existent, mais aucun portrait authentifié comme **portrait de 1776** n'a été trouvé. Ils peuvent aider à une reconstruction prudente, pas être présentés comme une photographie faciale contemporaine. L'entrée de formation actuelle n'a pas de `dna = ...` explicite ; elle repose sur `template = default`.

### 5.2 `BUR` — Maha Thiha Thura

**Décision : `REBUILD_NAMED_HISTORICAL_GENERAL` — identité militaire élevée, naissance de confiance moyenne.**

- Nom : **Maha Thiha Thura / Maha Thihathura** (မဟာသီဟသူရ).
- Source birmane moderne : **1720-1782**, originaire de la région de la **rivière Mu / Shwebo**.
- Mapping V3 de naissance : **`STATE_MANDALAY`** par approximation régionale.
- Fonction au 1776-01-01 : principal commandant birman de l'invasion du Siam de **1775-1776**, au sommet de la hiérarchie de campagne.
- Activité au 1er janvier : opérations dans le théâtre nord-siamois autour de **Phitsanulok** ; le retrait général n'a lieu qu'après la mort d'Hsinbyushin plus tard en 1776.

#### Le problème de l'âge

Il ne faut **en aucun cas** conserver automatiquement un âge procédural.

La source birmane consultée donne **1720**, ce qui donne environ **55 ans** au 1er janvier 1776. Mais une tradition historique thaïlandaise reprise dans une narration institutionnelle décrit le commandant birman de la campagne de 1775 comme ayant environ **72 ans**, ce qui renverrait vers **c.1703**.

Il n'existe donc pas, dans les sources consultées, de base suffisante pour inventer un jour et un mois. Recommandation :
- `birth_date = 1720`
- `birth_date_precision = YEAR_ONLY_DISPUTED`
- conserver textuellement la contradiction dans le rapport/CSV.

#### Culture, religion, origine, traits

- Culture : **Bamar/Birmane** probable et cohérente avec son origine et sa carrière dans l'armée konbaung.
- Religion : **bouddhisme theravāda** très probable, mais aucun document personnel de pratique religieuse n'a été utilisé pour transformer cette probabilité en certitude absolue.
- Origine : Mu Valley/Shwebo ; tradition birmane d'intégration au noyau militaire d'Alaungpaya.
- Traits :
  - commandant expérimenté — **HIGH** ;
  - stratège — **HIGH** ;
  - offensif — **HIGH** ;
  - pragmatique/diplomate — **MEDIUM**, notamment en raison de son rôle dans la paix avec les Qing.

Aucun portrait contemporain authentifié n'a été localisé.

### 5.3 `PHI` — Simón de Anda y Salazar

**Décision : `IMPLEMENT_NAMED_HISTORICAL_GENERAL` — confiance élevée.**

Ce cas respecte la règle « un gouverneur n'est pas automatiquement un général ». Anda est retenu parce que son office était formellement **gouverneur ET capitaine général**, et parce qu'une preuve archivistique le montre exerçant directement une autorité militaire immédiatement avant la date de référence.

L'Archivo General de Indias conserve le dossier **FILIPINAS,376,N.39**, ouvert en décembre 1775. Il comprend une lettre d'Anda datée de **Manille, 30 décembre 1775**, transmettant son avis sur quatre propositions d'officiers pour les compagnies du **Regimiento de Infantería de Filipinas**.

Profil recommandé :
- naissance : **1709-10-28**, Subijana/Subijana-Morillas, Álava ;
- `birth_date_precision = EXACT` ;
- âge au 1776-01-01 : **66 ans** ;
- décès : **1776-10-30**, Cavite ;
- fonction : **Governor and Captain General of the Philippines**, 1770-1776 ;
- activité 1776 : administration de garnison, organisation des défenses et autorité de personnel sur le régiment de Manille ;
- culture historique : **basque**, au service de la monarchie espagnole ;
- religion : **catholique romaine** ;
- mapping V3 de naissance : **`STATE_NAVARRA`** comme approximation du découpage V3 pour Álava/Basque ;
- traits : commandant expérimenté, défense, organisation.

Une tradition tertiaire donne parfois **1701** ; le rapport retient **1709** car cette année est soutenue par l'encyclopédie basque Auñamendi et des notices d'autorité.

### 5.4 `JOH` — Raja Haji Fisabilillah

**Décision : `IMPLEMENT_NAMED_HISTORICAL_GENERAL` — confiance moyenne-haute.**

Le point essentiel est de ne **pas** lui donner en 1776 le titre de **Yang Dipertuan Muda IV**, qui commence en **1777**.

Au 1er janvier 1776, l'office pertinent est **Engku Kelana**. Le profil de héros national IKPNI indique qu'il avait pour tâches de contribuer au gouvernement et surtout de **maintenir la sécurité et l'intégrité du territoire** ; il avait déjà combattu les Néerlandais durant la guerre de Linggi (1756-1758). Cela en fait un meilleur candidat qu'un sultan choisi uniquement pour son statut politique.

Profil :
- naissance : **c.1725-1727**, Kota Lama / Hulu Riau ;
- `birth_date_precision = CONFLICTING_APPROXIMATE_YEAR_RANGE` ;
- lieu V3 : **`STATE_MALAYA`** par approximation de l'architecture actuelle, à vérifier au niveau provincial avant implémentation ;
- décès : **1784-06-18**, Teluk Ketapang, tué au combat contre les Néerlandais ;
- culture : élite **bugis-riau**, dynastie bugis intégrée au monde politique malais de Riau-Johor ;
- religion : **islam sunnite** ;
- fonction : **Engku Kelana**, sécurité/expéditions/assistance au Yang Dipertuan Muda ;
- traits : commandant expérimenté, commandement expéditionnaire, bravoure ; expérience maritime réelle mais à ne traduire en trait terrestre que si le système de traits le permet.

Les images modernes de Raja Haji sont rétrospectives ; aucun portrait contemporain authentifié n'a été identifié.

## 6. Candidats examinés mais rejetés/différés

### 6.1 `LAN` — Luo Fangbo : rejet absolu pour la date

Luo Fangbo (羅芳伯, **1738-1795**) est déjà arrivé à Bornéo occidental en 1772. Toutefois, la littérature académique situe la **fondation de la Lanfang kongsi en 1777**. Il peut donc exister physiquement dans la région en 1776, mais il ne peut pas être « général de Lanfang » un an avant la création de Lanfang.

Décision : **`KEEP_PROCEDURAL_PENDING_STRUCTURE_REWORK`**.

### 6.2 `CMI` — Kawila : mauvais office et mauvaise date

Kawila (**1742-1816**) est une figure militaire majeure de Lanna, mais la littérature de Chiang Mai University, fondée sur le *Tamnan Phuen Muang Chiang Mai*, place sa nomination comme dirigeant de Chiang Mai en **1782**. Son ancrage antérieur est Lampang/Lamphun.

Décision : **ne pas le rétroprojeter en 1776** ; conserver le général procédural en attendant une refonte de la structure de Chiang Mai/Lanna.

### 6.3 `SRK` — Mangkunegara I : excellent général, mauvaise formation politique

Mangkunegara I / Raden Mas Said (1726-1795) est historiquement un des grands commandants javanais du XVIIIe siècle. Mais après 1757, Mangkunegaran forme un pouvoir princier semi-autonome dans l'espace de Surakarta. Le rattacher automatiquement à la formation `SRK` du Sunanate ferait disparaître cette distinction politique.

Décision : **`DEFER_POLITY_SCOPE_MISMATCH_KEEP_PROCEDURAL`**. Il devient candidat prioritaire seulement si une future décision d'architecture affirme explicitement que `SRK` agrège les forces de Mangkunegaran.

### 6.4 `DEI` — officiers VOC attestés plus tard en 1776

Les archives néerlandaises permettent d'identifier des majors à Batavia au cours de 1776, notamment des officiers d'artillerie/militaires. Mais les attestations localisées sont **postérieures au 1er janvier** et ne prouvent pas qu'un de ces hommes commande l'ensemble de la formation terrestre représentée par le tag `DEI`.

Décision : **général procédural conservé**. Ne pas faire du raisonnement « il est major en juin 1776, donc il commandait forcément cette formation le 1er janvier ».

## 7. Formations restant procédurales

Pour les tags `ACE`, `BLG`, `BNJ`, `BRU`, `BTN`, `KTI`, `MGD`, `PON`, `PRK`, `SAK`, `SEL`, `SMB`, `STG`, `SUL`, `TID` et `YOG`, aucun commandant **non souverain**, doté d'une biographie suffisamment reconstruisible et d'un commandement clairement valable au **1776-01-01**, n'a été trouvé dans les sources consultées.

Cela signifie **« aucun candidat admissible localisé »**, pas « aucun commandant historique n'a jamais existé ».

Pour `BAL`, `CAM`, `CHP`, `CMI`, `JMB`, `LAN` et `LUA`, le dépôt signalait déjà un statut **`PROCEDURAL_ALLOWED_PENDING_STRUCTURE_REWORK`**. Cette prudence doit être préservée : plusieurs de ces espaces n'avaient pas une armée nationale centralisée au sens européen que suggère abstraitement Victoria 3.

## 8. Đại Việt / Vietnam

Le dépôt contient un pays `DAI` (`dai - dai viet.txt`), mais le fichier de formations terrestres audité ne contient **aucun bloc `c:DAI`**.

Conséquence :
- aucun général ne doit être créé ici ;
- les commandants de la guerre Tây Sơn/Trịnh/Nguyễn pourront faire l'objet d'une recherche historique séparée **si une formation DAI est ajoutée ou restaurée** dans l'architecture ;
- ne pas fabriquer une affectation sans formation simplement parce que le Vietnam est dans le périmètre géographique.

## 9. Notes de mapping Victoria 3

Les champs `birth_state_v3` sont des **mappings de recherche**, pas des modifications gameplay. Ils doivent être contrôlés lors de l'implémentation contre le découpage exact de la version de carte utilisée.

Mappings les plus importants :
- Thongduang / Ayutthaya → `STATE_BANGKOK` : confiance **HIGH**.
- Maha Thiha Thura / Mu Valley-Shwebo → `STATE_MANDALAY` : confiance **MEDIUM**.
- Simón de Anda / Álava → `STATE_NAVARRA` : confiance **MEDIUM**.
- Raja Haji / Hulu Riau → `STATE_MALAYA` : confiance **MEDIUM**, à revalider pour les îles Riau.
- Luo Fangbo / Jiaying-Meixian → `STATE_GUANGDONG` : confiance **HIGH**.
- Mangkunegara I / Java central → `STATE_CENTRAL_JAVA` : confiance **HIGH**.

## 10. Portraits et DNA/templates

Aucune des quatre recommandations ne dispose, dans l'entrée de formation auditée, d'un `dna = ...` explicite :
- `BUR` Maha Thiha Thura : nom historique + `template = default`.
- `SIA` Chao Phraya Chakri : nom historique + `template = default`.
- `PHI` : général actuellement procédural + `template = default`.
- `JOH` : général actuellement procédural + `template = default`.

Ce constat est volontairement limité à **l'entrée de formation actuelle** : il ne prétend pas qu'aucun asset graphique ou template portant un autre nom n'existe nulle part ailleurs dans l'ensemble du jeu/vanilla.

Règle portrait recommandée :
- Rama I : portraits royaux ultérieurs disponibles, **pas portrait 1776 vérifié**.
- Maha Thiha Thura : aucun portrait contemporain authentifié trouvé.
- Simón de Anda : portrait/gravure historique disponible, mais dater et contrôler la provenance avant DNA.
- Raja Haji : représentations modernes/monuments, pas de portrait contemporain authentifié trouvé.

## 11. Sources principales

### Dépôt

1. [Formation file — `06_military_formations_asia.txt`](https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/cleanup-post-release/common/history/military_formations/06_military_formations_asia.txt)
2. [Country history — `dai - dai viet.txt`](https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/cleanup-post-release/common/history/countries/dai%20-%20dai%20viet.txt)

### Siam / calendrier

3. [Fine Arts Department of Thailand — date royale en B.E. 2279](https://finearts.go.th/museumstorage/view/40646-50Royalinmemory-%E0%B9%92%E0%B9%90-%E0%B8%A1%E0%B8%B5%E0%B8%99%E0%B8%B2%E0%B8%84%E0%B8%A1-%E0%B9%92%E0%B9%92%E0%B9%97%E0%B9%99--%E0%B9%92%E0%B9%98%E0%B9%96-%E0%B8%9B%E0%B8%B5%E0%B8%81%E0%B9%88%E0%B8%AD%E0%B8%99----%E0%B8%A7%E0%B8%B1%E0%B8%99%E0%B8%9E%E0%B8%A3%E0%B8%B0%E0%B8%A3%E0%B8%B2%E0%B8%8A%E0%B8%AA%E0%B8%A1%E0%B8%A0%E0%B8%9E%E0%B8%9E%E0%B8%A3%E0%B8%B0%E0%B8%9A%E0%B8%B2%E0%B8%97%E0%B8%AA%E0%B8%A1%E0%B9%80%E0%B8%94%E0%B9%87%E0%B8%88%E0%B8%9E%E0%B8%A3%E0%B8%B0%E0%B8%9E%E0%B8%B8%E0%B8%97%E0%B8%98%E0%B8%A2%E0%B8%AD%E0%B8%94%E0%B8%9F%E0%B9%89%E0%B8%B2%E0%B8%88%E0%B8%B8%E0%B8%AC%E0%B8%B2%E0%B9%82%E0%B8%A5%E0%B8%81--%E0%B8%A3%E0%B8%B1%E0%B8%8A%E0%B8%81%E0%B8%B2%E0%B8%A5%E0%B8%97%E0%B8%B5%E0%B9%88-%E0%B9%91-)
4. [KMUTT Library — *The Top Generals of King Taksin the Great*](https://www.lib.kmutt.ac.th/chapter-19-the-top-generals-of-king-taksin-the-great/)
5. [Sirindhorn Anthropology Centre — explication de la conversion des anciens millésimes thaïs](https://www.sac.or.th/portal/th/article/detail/108)
6. [National Library of Thailand — histoire des changements du Nouvel An thaï](https://www.nlt.go.th/service/1663)

### Birmanie

7. [Myawady Webportal — biography of Maha Thiha Thura, 1720-1782](https://www.myawady.net.mm/kunbheaangkhette-ccsuukiimhaasiihsuur)
8. Maung Htin Aung, *A History of Burma*, Cambridge University Press, 1967, pp. 184-186 — campagne de 1775 et retrait de 1776.

### Philippines espagnoles

9. [PARES / Archivo General de Indias — FILIPINAS,376,N.39, propositions d'officiers du Regimiento de Manila](https://pares.mcu.es/ParesBusquedas20/catalogo/description/13086945)
10. [Fundación BBVA — Simón de Anda, gobernador y capitán general, 1770-1776](https://www.fbbva.es/publicaciones/la-politica-religiosa-del-alaves-simon-de-anda-y-salazar-en-filipinas-es/)
11. [Auñamendi Eusko Entziklopedia — Simón de Anda, naissance 28 octobre 1709 à Subijana](https://aunamendi.eusko-ikaskuntza.eus/es/anda-y-salazar-simon-de/ar-652/)

### Johor-Riau

12. [IKPNI — Raja Haji Fisabilillah, Engku Kelana et responsabilités de sécurité](https://ikpni.or.id/pahlawan/raja-haji-fisabilillah/)
13. [Kemdikbud / BPNB Kepulauan Riau — notice Raja Haji, variante de naissance 1725](https://kebudayaan.kemdikbud.go.id/bpnbkepri/momen-hari-pahlawan-mengenang-raja-haji/)

### Rejets/différés

14. [World History Connected — Luo Fangbo et fondation de Lanfang en 1777](https://worldhistoryconnected.press.uillinois.edu/17.3/Eng.html)
15. [Jurnal Sosioteknologi / ITB — Lanfang Kongsi 1777-1884](https://journals.itb.ac.id/index.php/sostek/article/view/1379)
16. [Chiang Mai University — Kawila et nomination à Chiang Mai en 1782](https://cmuj.cmu.ac.th/asr/journal_de.php?id=64)
17. [UIII Library catalogue — M.C. Ricklefs, *Soul Catcher: Java's Fiery Prince Mangkunagara I, 1726-95*](https://catalogue.uiii.ac.id/?id=9935&p=show_detail)

## 12. Recommandation pour la future implémentation

Quand toutes les recherches continentales `CLEANUP-2D-5*` seront fusionnées, la passe Codex d'implémentation devrait, pour ce bloc :
1. reconstruire intégralement `GEN1776-152` et `GEN1776-175` sans conserver les âges/apparences procéduraux ;
2. remplacer `GEN1776-153` par Simón de Anda y Salazar ;
3. remplacer `GEN1776-166` par Raja Haji Fisabilillah **comme Engku Kelana**, sans titre YDM IV avant 1777 ;
4. laisser les autres formations procédurales selon le CSV ;
5. préserver les statuts `PENDING_STRUCTURE_REWORK` ;
6. ne pas créer de général `DAI` tant qu'aucune formation terrestre DAI n'existe ;
7. ne modifier ni gameplay, ni formations, ni lois, ni unités dans la phase historique elle-même.

---

**Fin du rapport de recherche — aucune implémentation effectuée.**
