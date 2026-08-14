# CLEANUP-2D-5M — HISTORICAL GENERALS 1776 — COVERAGE GAPS

## 1. Statut et méthodologie

**Nature de la phase : recherche historique uniquement.** Aucun fichier gameplay n’a été modifié, aucun personnage/DNA/template/localisation n’a été créé, et aucun commit/push n’a été effectué.

**Date de référence absolue : 1776-01-01.** Un candidat n’est retenu que si son identité est historiquement identifiable et si une fonction ou un commandement militaire pertinent est déjà établi à cette date. Une fonction politique, dynastique, religieuse ou administrative n’est jamais assimilée automatiquement à un commandement militaire.

La recherche applique quatre filtres distincts :

1. **Existence et architecture dans le dépôt courant** : vérification de la branche `cleanup-post-release`, du fichier de formations et du général procédural actuellement attaché.
2. **Admissibilité chronologique** : aucune nomination ou campagne postérieure au 1er janvier 1776 n’est rétroprojetée.
3. **Nature réelle du commandement** : distinction entre commandement de formation, office militaire, commandement territorial, commandement collectif/clanique et simple autorité politique.
4. **Profil individuel** : dates, lieux, calendrier, culture/religion, origine sociale, portrait et ressources déjà présentes dans le mod sont séparés des suppositions nécessaires au moteur.

Hiérarchie des preuves : annales/archives et institutions académiques en priorité ; ouvrages et encyclopédies savantes ensuite ; sources secondaires spécialisées seulement comme chaîne de piste lorsqu’une source primaire ou académique directement exploitable n’a pas été retrouvée. Un niveau de confiance est donné séparément pour **l’identité** et pour **le mapping vers la formation V3**.

### Vérification du dépôt

Les neuf enregistrements attendus sont toujours présents dans :

`common/history/military_formations/00_military_formations_europe.txt`

sur la branche `cleanup-post-release`, et chacun possède encore un général créé depuis `template = default`, commenté `PROCEDURAL_ALLOWED` dans CLEANUP-2D-4.

Aucun changement de nom de formation ou de HQ n’a été constaté par rapport à la baseline fournie.

## 2. Pourquoi ces neuf formations avaient été oubliées

Le trou de couverture vient de l’architecture des fichiers et non de la géographie réelle. Les neuf formations sont rangées dans `00_military_formations_europe.txt`, y compris BHU, KOR, NEP, SIK et TIB. Les recherches régionales précédentes qui s’appuyaient sur les fichiers asiatiques pouvaient donc conclure qu’un tag n’avait aucune formation alors que sa formation existait ailleurs.

Cela explique en particulier KOR et TIB : leur absence d’un fichier asiatique ne signifiait pas leur absence de la baseline globale. CLEANUP-2D-5M rétablit donc une recherche explicite pour exactement les neuf identifiants manquants et aucune dixième formation.

## 3. Matrice exécutive des neuf formations

| ID | Tag | Formation | Candidat / structure | Décision | Mapping | Identité | Mapping formation |
|---|---|---|---|---|---|---|---|
| GEN1776-051 | WAL | `Armata_rii_Romneti` | Aucun titulaire militaire daté suffisamment sûr | `KEEP_PROCEDURAL` | `NO_DEFENSIBLE_MAPPING` | LOW | MEDIUM_HIGH |
| GEN1776-052 | MON | `Montengrin_Raiders` | Commandement clanique/tribal distribué | `PROCEDURAL_REQUIRED_COLLECTIVE_STRUCTURE` | `CLAN_OR_TRIBAL_COMMAND` | LOW | HIGH |
| GEN1776-053 | MOL | `Armata_Principatului_Moldovei` | Office de hatman pertinent mais titulaire du 01-01 non établi | `KEEP_PROCEDURAL` | `NO_DEFENSIBLE_MAPPING` | LOW | MEDIUM_HIGH |
| GEN1776-068 | UBD | `cleanup2d3e_r1_ubd_land_1` | **George Browne** | `REUSE_EXISTING_HISTORICAL_CHARACTER_AS_GENERAL` | `HIGHER_COMMAND_ABSTRACTION` | VERY_HIGH | MEDIUM_HIGH |
| GEN1776-069 | BHU | `cleanup2d3b_bhu_land_1` | Structure régionale/dzong ; candidat militaire fort hors date | `KEEP_PROCEDURAL_PENDING_STRUCTURE_REWORK` | `NO_DEFENSIBLE_MAPPING` | LOW | HIGH |
| GEN1776-076 | KOR | `cleanup2d3b_kor_land_1` | **Gu Seon-bok / 구선복 (具善復)** | `IMPLEMENT_NAMED_HISTORICAL_GENERAL` | `HIGHER_COMMAND_ABSTRACTION` | VERY_HIGH | HIGH |
| GEN1776-080 | NEP | `cleanup2d3b_nep_land_1` | **Abhiman Singh Basnyat** | `IMPLEMENT_NAMED_HISTORICAL_GENERAL` | `HIGHER_COMMAND_ABSTRACTION` | HIGH | MEDIUM_HIGH |
| GEN1776-083 | SIK | `cleanup2d3b_sik_land_1` | Aucun commandant individuel daté assez sûrement | `KEEP_PROCEDURAL` | `NO_DEFENSIBLE_MAPPING` | LOW | HIGH |
| GEN1776-085 | TIB | `cleanup2d3b_tib_land_1` | Commandement militaire institutionnel mais titulaire unique non reconstructible | `PROCEDURAL_REQUIRED_COLLECTIVE_STRUCTURE` | `COLLECTIVE_HIGH_COMMAND` | LOW | HIGH |

**Résultat : 3 remplacements historiques recommandés, dont 1 réutilisation d’un personnage déjà présent ; 6 formations restent procédurales.**

## 4. WAL — Wallachia

### Architecture militaire en 1776

La Valachie phanariote ne doit pas être représentée comme une armée nationale permanente centralisée comparable à une armée du XIXe siècle. Les études sur l’organisation militaire valaque au XVIIIe siècle décrivent une réduction sensible des forces et une réorientation vers la garde, les frontières, la police et les fonctions fiscales/territoriales.

L’office de **mare spătar** pouvait avoir une réelle dimension de commandement en Valachie, notamment sur la cavalerie et, selon les contextes, comme commandement supérieur en l’absence du prince. Cela prouve que la bonne piste institutionnelle existe ; cela ne fournit pas pour autant un titulaire individuellement vérifié au 1er janvier 1776.

### Candidats examinés

- **Alexandru Ipsilanti** : prince/hospodar à la période. Rejeté comme général faute de preuve indépendante que sa fonction politique correspond au commandement personnel de la formation V3.
- **Mare spătar de Valachie** : office militaire pertinent, mais le titulaire exact au 1776-01-01 n’a pas été établi avec une source suffisamment forte.

### Conclusion

**Décision : `KEEP_PROCEDURAL`.**

La formation `Armata_rii_Romneti` est elle-même une abstraction historiquement trop centralisée. Il vaut mieux conserver un général procédural que d’inventer le titulaire du mare spătar ou de transformer le prince en général.

### Profil / V3

Aucun individu n’étant retenu, aucune date de naissance, culture, religion, IG, idéologie, trait ou portrait n’est assigné. La conclusion porte sur la structure, pas sur l’identité d’un candidat.

### Sources principales

- Claudiu Neagoe, étude universitaire sur l’organisation militaire de la Valachie phanariote : https://www.persee.fr/doc/valah_1584-1855_2020_num_22_1_1443
- Étude comparative des grands offices roumains, notamment le mare spătar : https://journals.rcsi.science/0869-544X/article/view/255403

## 5. MON — Montenegro

### Architecture militaire en 1776

Le Monténégro de la période ne possédait pas une armée nationale permanente structurée autour d’un état-major unique. La mobilisation reposait largement sur les **plemena**, les **bratstva** et leurs autorités locales. Le **vojvoda** est explicitement décrit dans l’historiographie comme un chef de guerre au niveau tribal ; les serdars et autres notables militaires participent à une architecture distribuée.

### Candidats examinés

**Jovan Radonjić** est historiquement bien identifié comme guvernadur à partir de 1764. Son importance politique est certaine. Des sources monténégrines lui attribuent aussi un commandement militaire personnel, mais l’exemple explicite retrouvé concerne la défense de Cetinje en **1785**. Cette preuve tardive ne peut pas être rétroprojetée au 1er janvier 1776.

Le métropolite et les principales autorités religieuses/politiques ne deviennent pas généraux par leur seule position.

### Conclusion

**Décision : `PROCEDURAL_REQUIRED_COLLECTIVE_STRUCTURE`.**

**Mapping : `CLAN_OR_TRIBAL_COMMAND`.**

`Montengrin_Raiders` représente mieux une compression gameplay de multiples contingents et chefs locaux qu’une force historiquement placée sous un général national unique.

### Sources principales

- Académie monténégrine (CANU), Jovan Radonjić / diplomatie : https://leks.canu.ac.me/web/ldcg.php?OID=2909
- CANU, notice biographique et commandement ultérieur : https://leks.canu.ac.me/web/lcd.php?OID=6237
- Étude universitaire sur les structures tribales et le rôle du vojvoda : https://books.openedition.org/pur/165081?lang=en

## 6. MOL — Moldavia

### Architecture militaire en 1776

La Moldavie possédait des offices militaires princiers, mais la terminologie ne doit pas être copiée mécaniquement depuis la Valachie. Le **hatman / mare hatman** est la piste la plus forte pour le commandement général des forces moldaves. Le **mare spătar** moldave n’est pas, à lui seul, l’équivalent automatique du commandant en chef valaque.

### Candidats examinés

- **Manolache Bogdan** : le nom apparaît associé à l’office de mare spătar autour de la période, mais cet office ne prouve pas en Moldavie un commandement de l’ensemble de l’armée.
- **Grigore III Ghica** : hospodar. Rejeté comme général en l’absence d’une preuve indépendante de commandement personnel de la formation.
- **Mare hatman** : office institutionnel historiquement pertinent, mais le titulaire exact et sa continuité au 1776-01-01 n’ont pas été établis de façon assez sûre.

### Conclusion

**Décision : `KEEP_PROCEDURAL`.**

Le bon office militaire est identifiable, mais pas son titulaire à la date absolue. Inventer un nom ou transposer le mare spătar serait moins historique que le procédural.

### Sources principales

- Synthèse des offices historiques moldaves : https://www.moldovenii.md/md/section/224/content/514
- C. C. Giurescu / travaux historiques sur les offices et le hatman : https://ro.scribd.com/document/336627488/Buletinul-Comisiei-istorice-a-Romaniei-1926-Volumul-5-pdf
- Comparaison des offices de Valachie et Moldavie : https://journals.rcsi.science/0869-544X/article/view/255403

## 7. UBD — United Baltic Provinces

### Architecture militaire et politique

`UBD` est une construction du mod destinée à rendre visibles des provinces baltiques sous domination russe. Elle n’équivaut pas à un État balte indépendant de 1776. Il faut donc chercher un **commandement russe supérieur ou territorial** capable de servir d’abstraction, et non un « général national UBD ».

### George Browne

**George Browne** est retenu pour des raisons militaires indépendantes de son existence politique dans le mod.

- Né le **15 juin 1698 Old Style** à Moyne/Castle Mahan, comté de Limerick, Royaume d’Irlande.
- Conversion grégorienne recommandée pour documentation : **25 juin 1698** ; le fichier du mod conserve actuellement `1698.6.15`.
- Officier de très haut rang au service russe, avec une carrière de commandement de campagne documentée.
- Gouverneur/Gouverneur général de Livonie et d’Estonie sur une longue durée, fonction encore détenue en 1776.
- Les biographies le présentent explicitement comme haut officier/général russe, indépendamment de son office civil/territorial.

Le mapping vers la formation UBD reste une **`HIGHER_COMMAND_ABSTRACTION`** : aucune source ne montre Browne commandant littéralement les six unités V3. En revanche, le chevauchement entre son autorité territoriale balte et sa carrière militaire russe rend cette abstraction défendable.

### Personnage déjà présent

Le dépôt contient déjà George Browne dans :

`common/history/characters/cleanup2b3 - residual europe rulers 1776.txt`

sous `c:UBD`, avec `historical = yes` et `birth_date = 1698.6.15`.

**Il ne faut pas créer un clone.**

### Conclusion

**Décision : `REUSE_EXISTING_HISTORICAL_CHARACTER_AS_GENERAL`.**

**Recommandation technique future : `REUSE_EXISTING_CHARACTER_IF_ENGINE_PERMITS`.**

Si le moteur ne gère pas proprement ruler + general sur le même personnage, cet arbitrage appartient à la phase Codex, pas à la recherche.

### Profil recommandé

- Culture historique : irlandaise / milieu Old English anglo-irlandais.
- V3 : `irish`.
- Religion : catholique romaine → `catholic`.
- Origine : gentry/famille foncière, puis carrière militaire professionnelle.
- IG pour le rôle militaire : `ig_armed_forces`.
- Idéologie : `UNSET`.
- Trait : `experienced_commander — HIGH`.
- DNA/template existant : aucun dédié retrouvé.
- Portrait : **`NEAR_CONTEMPORARY_PORTRAIT`**, gravure W. Arendt de 1794 associée à la biographie de Borch.

### Conflit de décès

Les sources consultées divergent sur le jour/mois du décès en 1792 (février vs septembre). Le CSV conserve donc **`1792` / `YEAR`** au lieu de choisir arbitrairement une date complète.

### Sources principales

- Dictionary of Irish Biography / Ulster University : https://pure.ulster.ac.uk/en/publications/browne-george-16981792-2/
- Université de Tartu, exemplaire numérisé de la biographie de Borch (1794) : https://dspace.ut.ee/items/626543a4-a286-46de-846f-0a792e2f2707
- Dictionary of National Biography : https://en.wikisource.org/wiki/Dictionary_of_National_Biography%2C_1885-1900/Browne%2C_George_%281698-1792%29
- Russian State Library, notice avec portrait : https://search.rsl.ru/ru/record/01004694716

## 8. BHU — Bhutan

### Architecture militaire en 1776

La structure militaire bhoutanaise doit être lue à travers les dzongs, les penlops/dzongpons et les mobilisations régionales, et non comme une armée nationale permanente dirigée par le Druk Desi par définition.

### Candidats examinés

**Zhidar** est un exemple important parce qu’il prouve que le commandement personnel d’une force par un haut dirigeant bhoutanais est historiquement documentable : les sources pédagogiques officielles bhoutanaises le montrent conduisant des troupes en 1772-1773.

Mais il est **ineligible** au 1776-01-01 : il a été renversé puis a fui avant cette date.

**Kunga Rinchen**, son successeur comme Druk Desi, est politiquement pertinent mais aucune preuve indépendante suffisamment forte n’a été retrouvée pour lui attribuer le commandement personnel de la formation V3 le 1er janvier 1776.

### Conclusion

**Décision : `KEEP_PROCEDURAL_PENDING_STRUCTURE_REWORK`.**

La très petite formation de deux unités paraît davantage être une abstraction de capacités régionales/dzong qu’un commandement national. Zhidar serait un vrai militaire mais échoue à la règle de date ; Kunga Rinchen ne doit pas être transformé en général par son seul titre.

### Sources principales

- Ressources éducatives officielles du Bhoutan, Desi Zhidar : https://sites.google.com/education.gov.bt/phuentshog-wangdi/x-history/chapter-2/druk-desi-sonam-lhundup/desi-zhidar
- Ressources éducatives officielles, guerre et commandement de Zhidar : https://sites.google.com/education.gov.bt/phuentshog-wangdi/vii-history/bhutan-history/chapter-6/events-of-the-war

## 9. KOR — Joseon Korea

### Architecture militaire en 1776

La formation de ~48 unités exige un représentant de haut niveau. Joseon ne doit cependant pas être simplifié en une armée nationale unique : les grands camps de la capitale, dont **Hunryeondogam**, constituent des institutions militaires distinctes.

### Gu Seon-bok — 구선복 (具善復)

C’est le cas le plus solide de CLEANUP-2D-5M.

Les **Annales de la dynastie Joseon** montrent :

- le **2 mai 1765**, la nomination de Gu Seon-bok comme **훈련대장 / 訓鍊大將**, Training Commander ;
- le **2 avril 1776**, sa destitution de ce même commandement et son remplacement.

Cette séquence constitue une preuve directe qu’il est encore titulaire de l’office au **1er janvier 1776**.

Les bases biographiques académiques coréennes donnent :

- naissance : **1718**, précision `YEAR` ;
- décès : **1786**, précision `YEAR` ;
- clan : Neungseong Gu ;
- longue carrière dans les principaux commandements militaires, dont Geumwiyeong, Hunryeondogam, commandements provinciaux et fonctions supérieures.

Le lieu de naissance individuel n’est pas établi par ces sources. Sa résidence ou son milieu familial ne doit donc pas être transformé en lieu de naissance.

### Conclusion

**Décision : `IMPLEMENT_NAMED_HISTORICAL_GENERAL`.**

**Mapping : `HIGHER_COMMAND_ABSTRACTION`.**

Gu commande une institution militaire majeure de la capitale, pas la totalité littérale des ~48 unités V3. Pour autant, son niveau et sa date d’office en font le meilleur représentant défendable de la grande formation coréenne.

### Profil recommandé

- Nom original : `구선복 (具善復)`.
- Variantes : Gu Seon-bok / Ku Sŏn-bok ; nom de courtoisie Sacho `士初`.
- Naissance : `1718`, `YEAR`.
- Lieu : `UNKNOWN`.
- Culture : Joseon Korean → `korean`.
- Religion : `UNRESOLVED` ; ne pas déduire automatiquement une religion individuelle de l’ordre confucéen de l’État.
- Origine sociale : lignée de military yangban.
- IG : `ig_armed_forces`.
- Idéologie : `UNSET`.
- Trait : `experienced_commander — HIGH`.
- DNA/template/personnage existant dans le mod : aucun retrouvé.
- Portrait : `NO_VERIFIED_PORTRAIT`.

### Sources principales

- Joseon Wangjo Sillok, nomination de 1765 : https://sillok.history.go.kr/id/kua_14105002_001
- Joseon Wangjo Sillok, destitution/remplacement du 2 avril 1776 : https://sillok.history.go.kr/id/kva_10004002_001
- Encyclopedia of Korean Culture (AKS) : https://encykorea.aks.ac.kr/Article/E0005843
- Sillokwiki (AKS) : https://dh.aks.ac.kr/sillokwiki/index.php/%EA%B5%AC%EC%84%A0%EB%B3%B5%28%E5%85%B7%E5%96%84%E5%BE%A9%29

## 10. NEP — Nepal

### Architecture militaire en 1776

Le 1er janvier 1776 se situe immédiatement après la mort de Prithvi Narayan Shah (1775), pendant la consolidation du royaume gorkhali. Le souverain ne doit pas être substitué automatiquement à un commandant de campagne.

### Abhiman Singh Basnyat

**Abhiman Singh Basnyat** est retenu comme meilleur compromis entre identité reconstruisible, expérience militaire antérieure à la date et niveau de commandement.

L’autorité prosopographique **Documenta Nepalica / Heidelberg Academy** donne :

- naissance : **1744** ;
- date népalaise : **Vikram Samvat 1801**, année seulement ;
- lieu : **Gorkha** ;
- père : Shivarama Singh Basnyat ;
- décès : **1800**.

Sa famille appartient à l’élite militaire/bharadar gorkhali. Les traditions et synthèses militaires le placent dans le commandement des opérations d’unification avant et après 1776. Une chaîne secondaire rapporte sa promotion/confirmation comme **Kaji dans la Pajani annuelle de 1775** et un commandement de campagne antérieur en 1772.

### Limite documentaire

C’est **le remplacement le moins robuste des trois**.

L’identité, la naissance et la famille sont solides. En revanche, la continuité exacte de l’office au 1er janvier 1776 dépend en partie de sources secondaires qui transmettent la Pajani de 1775 et les campagnes antérieures. Elle est crédible, mais moins directement prouvée que le cas Gu Seon-bok.

Pour cette raison :

- `identity_confidence = HIGH`
- `formation_mapping_confidence = MEDIUM_HIGH`

et non VERY_HIGH/HIGH.

### Conclusion

**Décision : `IMPLEMENT_NAMED_HISTORICAL_GENERAL`.**

**Mapping : `HIGHER_COMMAND_ABSTRACTION`.**

Il représente un haut commandement gorkhali ; le CSV ne prétend pas qu’il commande littéralement chaque unité de la formation V3.

### Profil recommandé

- Nom : Abhiman Singh Basnyat / Basnet.
- Original : `अभिमान सिंह बस्न्यात`.
- Naissance : `1744`, `YEAR`.
- Calendrier : `VS 1801`, année seulement.
- Lieu : Gorkha → mapping proposé `STATE_HIMALAYAS`, confiance MEDIUM_HIGH.
- Culture : Khas-Chhetri / Shreepali Basnyat → V3 `nepali`.
- Religion : `UNRESOLVED`; le contexte hindou n’est pas utilisé comme preuve d’une identification personnelle.
- Origine sociale : famille military-noble / bharadar.
- IG : `ig_armed_forces`.
- Idéologie : `UNSET`.
- Trait : `experienced_commander — HIGH`.
- DNA/template/personnage existant : aucun retrouvé.
- Portrait : `NO_VERIFIED_PORTRAIT`; les images modernes en circulation n’ont pas une provenance suffisante pour être classées authentiques.

### Candidats rejetés

- **Swarup Singh Karki** : présence militaire et politique importante en 1775, mais reconstruction biographique moins propre.
- **Vamsharaj Pande** : commandant important, mais mapping exact au 1776-01-01 moins sûr dans les sources retenues.
- **Pratap Singh Shah** : souverain ; pas automatiquement général.

### Sources principales

- Documenta Nepalica / Heidelberg Academy : https://nepalica.hadw-bw.de/nepal/ontologies/viewitem/1594
- Kantipur, s’appuyant sur l’histoire militaire institutionnelle népalaise pour la carrière militaire : https://ekantipur.com/bagmati-pradesh/2026/07/11/en/abhiman-singhs-statue-installed-in-someshwagadhi-35-03.html
- Chaîne secondaire pour les campagnes/Pajani de 1775, utilisée avec prudence : https://military-history.fandom.com/wiki/Unification_of_Nepal
- Notice bibliographique de *Military History of Nepal* : https://books.google.com/books/about/Military_History_of_Nepal.html?id=O3RuAAAAMAAJ

## 11. SIK — Sikkim

### Architecture militaire en 1776

Avec une seule unité V3, la formation doit être interprétée comme une abstraction très légère de défense territoriale. Il serait particulièrement anachronique de rechercher à tout prix un « général en chef » national.

### Candidats examinés

- **Phuntsog Namgyal II** : Chogyal. Rejeté comme général faute de preuve militaire indépendante.
- **Yug Choktub / Changzot Chogthup** : des traditions lui attribuent des succès militaires contre les Gorkhas, mais la chronologie la mieux établie dans les sources consultées place ces actions dans la fin des années 1770 et les années 1780, donc trop tard pour le 1er janvier 1776.
- **Deba Tshang Rinzing** : apparaît dans des récits secondaires de faible qualité/provenance ; insuffisant pour une implémentation nominative datée.

### Conclusion

**Décision : `KEEP_PROCEDURAL`.**

L’absence d’un titulaire individuel sûr est cohérente avec la petite taille de la formation et l’architecture locale. Aucun souverain n’est transformé artificiellement en général.

### Sources principales

- Gouvernement du Sikkim, chronologie historique : https://sikkimforest.gov.in/sikkim.htm
- Clio, chronologie du Sikkim et des conflits gorkhas : https://www.clio.fr/bibliotheque/chronologie/chronologie_le_sikkim.php
- Archives historiques de la monarchie du Sikkim : https://www.royalsikkim.com/Archives%20and%20History/Royal%20History.aspx

## 12. TIB — Tibet

### Architecture militaire en 1776

Le Tibet du Ganden Phodrang disposait d’institutions militaires réelles, mais l’organisation du XVIIIe siècle est complexe et partiellement reconstruite. Les recherches académiques soulignent les lacunes documentaires pour les premières phases du système militaire.

Des offices comme **dapon / mda' dpon** existent : un dapon peut commander une cohorte importante, avec une hiérarchie militaire supérieure. Cela ne suffit toutefois pas à identifier le titulaire exact chargé de la formation globale le 1er janvier 1776.

Il faut en outre distinguer :

- les forces tibétaines ;
- les troupes et garnisons sino-mandchoues/Qing présentes à Lhasa ;
- les ambans, qui exercent une supervision impériale mais ne deviennent pas pour cette raison « généraux de l’armée tibétaine » ;
- les kalön/régents et autres offices politiques.

### Conclusion

**Décision : `PROCEDURAL_REQUIRED_COLLECTIVE_STRUCTURE`.**

**Mapping : `COLLECTIVE_HIGH_COMMAND`.**

La formation de ~17 unités compresse plusieurs niveaux d’organisation. Aucun amban, régent ou kalön n’est imposé comme général sans preuve. Un poste militaire tibétain individuel serait préférable si un titulaire du 1776-01-01 était retrouvé, mais ce niveau de certitude n’a pas été atteint.

### Sources principales

- Federica Venturi, étude académique sur l’organisation militaire tibétaine : https://www.persee.fr/doc/asie_0766-1177_2018_num_27_1_1507
- Projet ERC TibArmy / CORDIS : https://cordis.europa.eu/project/id/677952/reporting
- TibArmy, recherches sur la garnison sino-mandchoue et les structures militaires : https://tibarmy.hypotheses.org/date/2018/02
- Treasury of Lives, institution Dapon : https://treasuryoflives.org/institution/Dapon

## 13. Conflits de dates / naissance

### George Browne

- Naissance historique : **15 juin 1698 Old Style / calendrier julien**.
- Conversion documentaire grégorienne : **25 juin 1698**.
- Le mod utilise déjà `1698.6.15`.
- La future implémentation ne doit pas écraser silencieusement le fait source par une convention de moteur.

Décès : plusieurs références divergent sur le jour/mois en **1792**. Le livrable conserve donc l’année seule.

### Gu Seon-bok

Naissance : **1718 seulement**. Interdiction de produire artificiellement `1718-01-01`.

### Abhiman Singh Basnyat

Naissance : **1744**, correspondant à **VS 1801**, mais sans mois/jour établi. Interdiction de produire artificiellement `1744-01-01`.

### Bilan des dates retenues

Aucun des trois candidats historiques ne reçoit une date complète inventée. Les six formations procédurales n’ont volontairement pas de pseudo-biographie.

## 14. Personnages existants à réutiliser

Un seul cas :

### George Browne — UBD

**`existing_mod_character = YES`**

Emplacement :

`common/history/characters/cleanup2b3 - residual europe rulers 1776.txt`

Le futur travail Codex doit tester la possibilité d’utiliser la même instance comme ruler et general. La recherche recommande **`REUSE_EXISTING_CHARACTER_IF_ENGINE_PERMITS`**, jamais la création immédiate d’un second George Browne.

Aucun personnage existant correspondant à Gu Seon-bok ou Abhiman Singh Basnyat n’a été retrouvé dans les recherches repo-wide réalisées.

## 15. DNA et portraits

### DNA/templates

Aucun DNA dédié n’a été trouvé pour les trois candidats retenus.

**`EXISTING_DNA_FOUND = 0`**

Aucun template spécifique Browne / Gu Seon-bok / Abhiman Singh Basnyat n’a été identifié.

### Portraits

- **George Browne** : `NEAR_CONTEMPORARY_PORTRAIT`. Gravure W. Arendt datée de 1794, donc postérieure d’environ deux ans à la mort mais proche chronologiquement.
- **Gu Seon-bok** : `NO_VERIFIED_PORTRAIT`.
- **Abhiman Singh Basnyat** : `NO_VERIFIED_PORTRAIT`. Des images historiques circulent en ligne, mais leur provenance n’est pas assez forte pour les qualifier de portrait authentique ou quasi contemporain.

Aucun DNA ne doit être généré dans cette phase.

## 16. Candidats rejetés globalement

| Formation | Candidat | Motif principal |
|---|---|---|
| WAL | Alexandru Ipsilanti | Hospodar/ruler ≠ général sans preuve indépendante |
| WAL | titulaire non identifié du mare spătar | Office pertinent mais titulaire/date du 01-01 non sécurisé |
| MON | Jovan Radonjić | Office réel ; commandement personnel explicitement retrouvé seulement plus tard (1785) |
| MON | métropolite / vladika | Autorité politique/religieuse ≠ général automatique |
| MOL | Manolache Bogdan | Mare spătar moldave ne prouve pas le commandement général |
| MOL | Grigore III Ghica | Hospodar/ruler ≠ général automatique |
| BHU | Zhidar | Vrai commandant mais renversé/exilé avant 1776 |
| BHU | Kunga Rinchen | Druk Desi sans preuve indépendante de commandement personnel le 01-01 |
| KOR | Yeongjo | Roi ≠ général |
| NEP | Pratap Singh Shah | Roi ≠ général |
| NEP | Swarup Singh Karki | Candidat crédible mais profil et mapping moins propres que Basnyat |
| NEP | Vamsharaj Pande | Candidat militaire important ; mapping exact au 01-01 moins sûr |
| SIK | Phuntsog Namgyal II | Chogyal ≠ général |
| SIK | Yug Choktub / Changzot Chogthup | Commandements mieux attestés plus tard dans les années 1770-1780 |
| TIB | ambans Qing | Supervision impériale/garnison ≠ général de la formation tibétaine |
| TIB | régent / kalön | Office politique ≠ commandement militaire automatique |
| TIB | dapon/makchi non identifié | Office approprié, titulaire du 01-01 non établi |

## 17. Statistiques finales

```text
FORMATIONS_AUDITED = 9
HISTORICAL_REPLACEMENTS_RECOMMENDED = 3
EXISTING_CHARACTERS_REUSED = 1
PROCEDURAL_RETAINED = 6
COLLECTIVE_STRUCTURE_CASES = 2
UNRESOLVED_BIRTH_DATES = 0
EXISTING_DNA_FOUND = 0
```

`UNRESOLVED_BIRTH_DATES = 0` compte uniquement les **trois candidats historiques retenus** : Browne a un jour exact documenté avec problème de calendrier explicité ; Gu et Basnyat ont des années documentées. Aucune date complète n’a été fabriquée.

### Validation CSV

```text
ROWS = 9
UNIQUE_RECORD_IDS = 9
MISSING_DECISIONS = 0
```

## 18. Checklist pour fusion globale

- [x] Branche `cleanup-post-release` vérifiée.
- [x] Les neuf GEN1776 attendus sont présents dans `00_military_formations_europe.txt`.
- [x] Aucun dixième enregistrement créé.
- [x] Les neuf généraux actuels restent procéduraux dans CLEANUP-2D-4.
- [x] Date absolue `1776-01-01` appliquée.
- [x] Aucune nomination postérieure utilisée rétroactivement.
- [x] Political ruler ≠ general appliqué à WAL, MON, MOL, BHU, KOR, NEP, SIK et TIB.
- [x] Structures collectives/claniques préservées lorsque nécessaire.
- [x] George Browne retenu pour sa carrière militaire indépendamment de son statut de Governor-General.
- [x] Réutilisation du personnage Browne existant recommandée au lieu d’un clone.
- [x] Dates de naissance YEAR conservées comme YEAR pour Gu Seon-bok et Abhiman Singh Basnyat.
- [x] Calendrier julien/grégorien de Browne signalé sans assimilation silencieuse.
- [x] Lieux de naissance inconnus laissés UNKNOWN.
- [x] Culture/religion non copiées automatiquement depuis le pays.
- [x] Idéologies laissées UNSET sans justification forte.
- [x] Traits limités à des éléments biographiquement défendables.
- [x] Aucun DNA inventé.
- [x] Aucun fichier gameplay modifié.
- [x] Aucun commit.
- [x] Aucun push.
- [x] CSV : 9 lignes, 9 IDs uniques, 0 décision manquante.
- [x] Cette phase permet de porter la couverture de recherche prévue de **205/214 à 214/214** après fusion des résultats.
