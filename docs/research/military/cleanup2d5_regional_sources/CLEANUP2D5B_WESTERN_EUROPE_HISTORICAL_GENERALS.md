# CLEANUP-2D-5B — HISTORICAL GENERALS 1776 — WESTERN EUROPE

**Statut : RECHERCHE UNIQUEMENT — aucune modification gameplay, aucun commit, aucun push.**

**Date de référence absolue : `1776-01-01`.**

## 1. Méthode et règles de décision

L'audit part du **setup réel de la branche `cleanup-post-release`** et non d'une liste théorique de pays. Chaque candidat est ensuite filtré par quatre tests :

1. **Temporalité** — vivant et déjà actif/en fonction au `1776-01-01`. Une prise de fonction plus tard en 1776 est rejetée pour le setup initial.
2. **Identité** — état civil et carrière suffisamment établis. Aucun `1 January`, jour ou mois n'est créé pour remplir un champ incomplet.
3. **Mapping formation ↔ officier** — préférence à un commandement direct; à défaut, un théâtre, un haut commandement ou un office militaire peut représenter une abstraction V3, mais le niveau de confiance est abaissé.
4. **Réutilisation mod** — recherche préalable dans `common/dna_data/`, `common/character_templates/`, `common/history/characters/`, `common/history/military_formations/` et par recherches repo-wide incluant `events/`.

Les recommandations de culture, religion, IG, idéologie et traits sont **des recommandations d'implémentation**, pas des affirmations mécaniques déjà présentes dans le mod.

## 2. Inventaire exact du périmètre

Le fichier de formations donne **16 formations terrestres** pertinentes : FRA ×4, GBR ×5, LUX ×1, NET ×1, BEO ×1, POR ×1 et SPA ×3. Il n'existe pas, dans ce setup, de formation terrestre occidentale séparée pour l'Irlande; la Belgique est représentée par **BEO / Austrian Netherlands**. Certaines formations ont un HQ et des États d'unités qui ne coïncident pas parfaitement (ex. formations britanniques méditerranéenne/indienne encore ancrées en East Anglia), ce qui impose de séparer `identity_confidence` et `formation_mapping_confidence`.

| ID | Tag | Formation | HQ | Général actuel | Décision finale | Candidat |
|---|---|---|---|---|---|---|
| GEN1776-015 | FRA | `cleanup2d3b_fra_land_1` | `region_western_europe` | PROCEDURAL cleanup2d4_general_015 | **IMPLEMENT_HISTORICAL** | Claude-Louis-Robert, comte de Saint-Germain |
| GEN1776-016 | FRA | `cleanup2d3b_fra_land_2` | `region_western_europe` | PROCEDURAL cleanup2d4_general_016 | **IMPLEMENT_HISTORICAL** | Louis-Georges-Érasme de Contades |
| GEN1776-017 | FRA | `cleanup2d3b_fra_land_3` | `region_southern_europe` | PROCEDURAL cleanup2d4_general_017 | **IMPLEMENT_HISTORICAL** | Louis-François-Armand de Vignerot du Plessis, duc de Richelieu |
| GEN1776-018 | FRA | `cleanup2d3b_fra_land_4` | `region_central_america` | PROCEDURAL cleanup2d4_general_018 | **IMPLEMENT_HISTORICAL** | Victor-Thérèse Charpentier d'Ennery |
| GEN1776-019 | GBR | `cleanup2d3b_gbr_land_2` | `region_atlantic_coast` | William Howe (cleanup2d4_general_019) | **KEEP_EXISTING_HISTORICAL** | William Howe, 5th Viscount Howe |
| GEN1776-020 | GBR | `Home_Army` | `region_western_europe` | PROCEDURAL cleanup2d4_general_020 | **IMPLEMENT_HISTORICAL** | Jeffery Amherst |
| GEN1776-021 | GBR | `cleanup2d3b_gbr_land_4` | `region_southern_europe` | PROCEDURAL cleanup2d4_general_021 | **IMPLEMENT_HISTORICAL** | George Augustus Eliott |
| GEN1776-022 | GBR | `cleanup2d3b_gbr_land_3` | `region_central_america` | PROCEDURAL cleanup2d4_general_022 | **IMPLEMENT_HISTORICAL** | Montfort Browne |
| GEN1776-023 | GBR | `cleanup2d3b_gbr_land_5` | `region_south_india` | PROCEDURAL cleanup2d4_general_023 | **IMPLEMENT_HISTORICAL** | John Clavering |
| GEN1776-046 | LUX | `Luxemburger_Miliz` | `region_western_europe` | PROCEDURAL cleanup2d4_general_046 | **KEEP_PROCEDURAL** | — |
| GEN1776-062 | NET | `Koninklijk_Nederlands_Leger` | `region_western_europe` | PROCEDURAL cleanup2d4_general_062 | **IMPLEMENT_HISTORICAL** | Lodewijk Ernst, hertog van Brunswijk-Wolfenbüttel |
| GEN1776-063 | BEO | `Armee_Belge` | `region_western_europe` | PROCEDURAL cleanup2d4_general_063 | **IMPLEMENT_HISTORICAL** | Joseph-Jean-François, comte de Ferraris |
| GEN1776-064 | POR | `Exercito_Portugues` | `region_southern_europe` | PROCEDURAL cleanup2d4_general_064 | **IMPLEMENT_HISTORICAL** | Duarte António da Câmara, 2.º marquês de Tancos |
| GEN1776-065 | SPA | `cleanup2d3b_spa_land_2` | `region_southern_europe` | Antonio Ricardos (cleanup2d4_general_065) | **KEEP_EXISTING_HISTORICAL** | Antonio Ricardos Carrillo de Albornoz |
| GEN1776-066 | SPA | `cleanup2d3b_spa_land_1` | `region_southern_europe` | Alejandro O'Reilly (cleanup2d4_general_066) | **REPLACE_EXISTING_HISTORICAL** | Félix O'Neille y O'Neille |
| GEN1776-067 | SPA | `cleanup2d3b_spa_land_3` | `region_central_america` | PROCEDURAL cleanup2d4_general_067 | **IMPLEMENT_HISTORICAL** | Felipe de Fonsdeviela y Ondeano, II marqués de la Torre |

## 3. Audit de réutilisation DNA / templates / personnages

- `common/dna_data/` contient notamment des DNA de Charles III d'Espagne, Louis XVI, George III, Stanisław, Karim Khan et quelques autres personnages, **mais aucun DNA des candidats retenus ci-dessous**.
- `common/history/characters/fra - france.txt` n'instancie au départ que Louis XVI.
- `common/character_templates/country_spa.txt` ne fournit, pour le setup espagnol inspecté, que les templates royaux Charles III / Charles IV; aucun Ricardos, O'Reilly, O'Neille ou Fonsdeviela réutilisable.
- `common/character_templates/country_gbr.txt` contient de nombreux personnages britanniques plus tardifs (dont Wellington) mais aucune entrée Howe ou Amherst exploitable pour 1776.
- Des recherches repo-wide ciblées n'ont trouvé aucune identité préexistante pour Rochambeau, Richelieu, Saint-Germain, Contades, Amherst, d'Ennery, Eliott, Brunswijk ou Fonsdeviela.
- Les personnages historiques de CLEANUP-2D-4 (Howe, Ricardos, O'Reilly) sont créés **directement dans le fichier de formations**, sans template historique ni DNA spécifique.

Conclusion DNA : **aucun DNA/template historique existant n'est réutilisable pour les nouvelles identités proposées**. Il faudra, lors d'une phase d'implémentation distincte, soit accepter le template par défaut, soit créer des DNA après audit iconographique.

## 4. Analyse formation par formation

### France

#### GEN1776-015 — `cleanup2d3b_fra_land_1`

- **HQ V3 :** `region_western_europe`
- **Général actuel :** PROCEDURAL cleanup2d4_general_015
- **Décision :** **IMPLEMENT_HISTORICAL**
- **Mapping :** `HIGHER_COMMAND_ABSTRACTION` — identité **HIGH**, mapping formation **MEDIUM**.
- **Candidat :** **Claude-Louis-Robert, comte de Saint-Germain**.
- **Naissance :** 1707-04-15 (`DAY`), Vertamboz, Franche-Comté (actuel Jura); territoire politique : Royaume de France.
- **State V3 de naissance recommandé :** STATE_FRANCHE_COMTE
- **Décès :** 1778-01-15
- **Grade au 1776-01-01 :** Lieutenant-général (carrière française); ancien field marshal danois
- **Fonction :** Secrétaire d'État de la Guerre; autorité supérieure sur l'armée française
- **Période de fonction :** 1775-10 (documenté en fonction au plus tard le 1775-11-04) → 1777-09; actif au 1776-01-01 : **YES**.
- **Profil recommandé :** culture `cu:french`, religion `rel:catholic`, IG `ig_armed_forces`, idéologie `ideology_reformer`.
- **Traits à envisager :** réformateur militaire; administrateur expérimenté; méticuleux (choisir des clés V3 valides à l'implémentation).
- **Réutilisation mod :** character=NO; template=NO; DNA=NO.
- **Portrait / description :** YES — gravures/portraits historiques à sourcer précisément avant DNA.
- **Raisonnement :** Meilleur candidat pour la grande formation nationale abstraite. Le poste est déjà exercé avant la date de référence; aucune extrapolation depuis une nomination postérieure.
- **Sources principales :**
  - FR-SG-1 | CCFr/BnF — lettre de Claude-Louis de Saint-Germain, secrétaire d'État de la Guerre, 4 novembre 1775; notice biographique: 15 avril 1707, Vertamboz – 15 janvier 1778, Paris
  - FR-SG-2 | CCFr/BnF — lettre de Claude-Louis de Saint-Germain, secrétaire d'État de la Guerre, 7 juin 1776
  - MOD-3 | GitHub cleanup-post-release — common/character_templates/ + common/history/characters/ + repo-wide surname searches
- **Candidats rejetés / arbitrage :** Alternatives examinées : plusieurs généraux de ligne français; aucun ne donne un meilleur lien avec cette formation nationale de 114 unités que le ministre-général Saint-Germain.

#### GEN1776-016 — `cleanup2d3b_fra_land_2`

- **HQ V3 :** `region_western_europe`
- **Général actuel :** PROCEDURAL cleanup2d4_general_016
- **Décision :** **IMPLEMENT_HISTORICAL**
- **Mapping :** `FORMATION_COMMAND` — identité **HIGH**, mapping formation **HIGH**.
- **Candidat :** **Louis-Georges-Érasme de Contades**.
- **Naissance :** 1704-10-11 (`DAY`), Château de Montgeoffroy, Mazé, Anjou; territoire politique : Royaume de France.
- **State V3 de naissance recommandé :** STATE_LOIRE (mapping géographique probable; vérifier la clé vanilla 1.13 si absente de l'index du fork)
- **Décès :** 1795-01-19
- **Grade au 1776-01-01 :** Maréchal de France
- **Fonction :** Commandant en chef en Alsace
- **Période de fonction :** 1762 → 1788-05; actif au 1776-01-01 : **YES**.
- **Profil recommandé :** culture `cu:french`, religion `rel:catholic`, IG `ig_armed_forces`, idéologie `ideology_royalist`.
- **Traits à envisager :** commandant expérimenté; autorité régionale; réservé/discipliné.
- **Réutilisation mod :** character=NO; template=NO; DNA=NO.
- **Portrait / description :** YES — portraits/gravures du XVIIIe siècle signalés; référence précise à fixer avant DNA.
- **Raisonnement :** Formation ancrée en Alsace-Lorraine; Contades est un mapping direct nettement supérieur à Rochambeau. Rochambeau reste historiquement actif comme inspecteur général mais son gouvernement de Villefranche n'est daté que '1776' sans preuve d'une prise de fonction avant le 1er janvier.
- **Sources principales :**
  - FR-CO-1 | Fédération des Sociétés d'Histoire et d'Archéologie d'Alsace — Louis-Georges-Érasme de Contades; commandant en chef en Alsace à partir de 1762, fonction tenue environ 26 ans
  - FR-CO-2 | État militaire de France / notice historique Contades — maréchal de France; commandement supérieur d'Alsace jusqu'en 1788
  - MOD-1 | GitHub cleanup-post-release — common/history/military_formations/00_military_formations_europe.txt
- **Candidats rejetés / arbitrage :** **Rochambeau** : admissible comme officier actif (maréchal de camp / inspecteur général), mais HOLD/rejet pour cette formation. Son gouvernorat de Villefranche est seulement daté « 1776 » dans les notices consultées; sans jour/mois antérieur au 1er janvier il ne peut pas servir de preuve de commandement initial. Contades commande déjà l'Alsace depuis 1762.

#### GEN1776-017 — `cleanup2d3b_fra_land_3`

- **HQ V3 :** `region_southern_europe`
- **Général actuel :** PROCEDURAL cleanup2d4_general_017
- **Décision :** **IMPLEMENT_HISTORICAL**
- **Mapping :** `MILITARY_OFFICEHOLDER` — identité **HIGH**, mapping formation **MEDIUM**.
- **Candidat :** **Louis-François-Armand de Vignerot du Plessis, duc de Richelieu**.
- **Naissance :** 1696-03-13 (`DAY`), Paris; territoire politique : Royaume de France.
- **State V3 de naissance recommandé :** STATE_ILE_DE_FRANCE
- **Décès :** 1788-08-08
- **Grade au 1776-01-01 :** Maréchal de France
- **Fonction :** Gouverneur de Guyenne et Gascogne
- **Période de fonction :** 1755 → 1788; actif au 1776-01-01 : **YES**.
- **Profil recommandé :** culture `cu:french`, religion `rel:catholic`, IG `ig_armed_forces`, idéologie `ideology_royalist`.
- **Traits à envisager :** commandant vétéran; aristocrate de cour; imperious.
- **Réutilisation mod :** character=NO; template=NO; DNA=NO.
- **Portrait / description :** YES — nombreux portraits et gravures contemporains.
- **Raisonnement :** La formation contient un fort noyau en Aquitaine. Le gouvernorat de Guyenne/Gascogne est un lien régional défendable, mais la formation V3 reste une abstraction plus large qu'un commandement d'armée d'Ancien Régime.
- **Sources principales :**
  - FR-RI-1 | BnF, notice d'autorité — Louis-François-Armand de Vignerot du Plessis, duc de Richelieu: 13 mars 1696 – 8 août 1788
  - FR-RI-2 | Larousse, notice Richelieu — maréchal de France; gouverneur de Guyenne et Gascogne à partir de 1755
  - MOD-1 | GitHub cleanup-post-release — common/history/military_formations/00_military_formations_europe.txt
- **Candidats rejetés / arbitrage :** Alternative : Rochambeau n'a pas de lien régional aussi direct avec Guyenne/Gascogne. Richelieu est gouverneur de la zone depuis 1755.

#### GEN1776-018 — `cleanup2d3b_fra_land_4`

- **HQ V3 :** `region_central_america`
- **Général actuel :** PROCEDURAL cleanup2d4_general_018
- **Décision :** **IMPLEMENT_HISTORICAL**
- **Mapping :** `THEATRE_COMMAND` — identité **HIGH**, mapping formation **HIGH**.
- **Candidat :** **Victor-Thérèse Charpentier d'Ennery**.
- **Naissance :** 1732-03-24 (`DAY`), Paris; territoire politique : Royaume de France.
- **State V3 de naissance recommandé :** STATE_ILE_DE_FRANCE
- **Décès :** 1776-12-13
- **Grade au 1776-01-01 :** Maréchal des camps et armées du roi
- **Fonction :** Gouverneur-lieutenant général des Îles du Vent / Saint-Domingue; inspecteur général d'infanterie et directeur général des forces coloniales
- **Période de fonction :** 1775 (fonctions documentées le 1775-10-23) → 1776-12-13; actif au 1776-01-01 : **YES**.
- **Profil recommandé :** culture `cu:french`, religion `rel:catholic`, IG `ig_armed_forces`, idéologie `ideology_royalist`.
- **Traits à envisager :** administrateur colonial; organisateur; logistique/fortifications.
- **Réutilisation mod :** character=NO; template=NO; DNA=NO.
- **Portrait / description :** PARTIAL — monument funéraire documenté; aucun portrait facial contemporain sûr identifié dans l'audit.
- **Raisonnement :** La preuve clé est une ordonnance du 23 octobre 1775 énumérant explicitement ses responsabilités militaires coloniales; activité certaine au 1er janvier 1776.
- **Sources principales :**
  - FR-EN-1 | Ordonnance imprimée à Port-au-Prince, 23 octobre 1775 — d'Ennery y est qualifié maréchal des camps et armées du roi, inspecteur général d'infanterie, directeur général des troupes/fortifications/artillerie/milices des colonies et gouverneur-lieutenant général
  - FR-EN-2 | Commune d'Ennery, notice Victor-Thérèse Charpentier d'Ennery — né à Paris le 24 mars 1732; mort le 13 décembre 1776
  - FR-EN-3 | Ministère français de la Culture, base Palissy — monument funéraire de Victor-Thérèse Charpentier d'Ennery (1732–1776)
- **Candidats rejetés / arbitrage :** Les officiers métropolitains sans mandat colonial explicite sont rejetés au profit de d'Ennery, dont les compétences sur les troupes, fortifications, artillerie et milices coloniales sont explicitement imprimées dès octobre 1775.

### Grande-Bretagne

#### GEN1776-019 — `cleanup2d3b_gbr_land_2`

- **HQ V3 :** `region_atlantic_coast`
- **Général actuel :** William Howe (cleanup2d4_general_019)
- **Décision :** **KEEP_EXISTING_HISTORICAL**
- **Mapping :** `THEATRE_COMMAND` — identité **HIGH**, mapping formation **HIGH**.
- **Candidat :** **William Howe, 5th Viscount Howe**.
- **Naissance :** 1729-08-10 (`DAY`), UNKNOWN — aucune localité exacte n'a été promue sans source institutionnelle vérifiée; territoire politique : Kingdom of Great Britain.
- **State V3 de naissance recommandé :** aucun mapping sûr
- **Décès :** 1814-07-12
- **Grade au 1776-01-01 :** Lieutenant-general / rang local supérieur en Amérique
- **Fonction :** Commander-in-Chief des forces britanniques en Amérique du Nord
- **Période de fonction :** 1775-10-10 → 1778; actif au 1776-01-01 : **YES**.
- **Profil recommandé :** culture `cu:british`, religion `rel:protestant`, IG `ig_armed_forces`, idéologie `ideology_royalist`.
- **Traits à envisager :** commandant expérimenté; prudent; offensive planner à calibrer.
- **Réutilisation mod :** character=YES — direct create_character dans le fichier de formations; template=NO; DNA=NO.
- **Portrait / description :** YES — National Portrait Gallery, gravure 1778.
- **Raisonnement :** Choix de CLEANUP-2D-4 confirmé. Son commandement commence avant le 1er janvier 1776. Ne pas inventer une localité de naissance dans les données de personnage.
- **Sources principales :**
  - GB-HO-1 | Dictionary of National Biography — William Howe: né 10 août 1729; commandement en Amérique, succède à Thomas Gage le 10 octobre 1775; rang local supérieur en Amérique
  - GB-HO-2 | National Portrait Gallery — William Howe, 5th Viscount Howe (1729–1814), portrait gravé publié en 1778
  - MOD-1 | GitHub cleanup-post-release — common/history/military_formations/00_military_formations_europe.txt
- **Candidats rejetés / arbitrage :** **Thomas Gage** est rejeté pour le setup initial car Howe lui succède dès le 10 octobre 1775. Les commandants envoyés ultérieurement en 1776 ne doivent pas rétroagir au 1er janvier.

#### GEN1776-020 — `Home_Army`

- **HQ V3 :** `region_western_europe`
- **Général actuel :** PROCEDURAL cleanup2d4_general_020
- **Décision :** **IMPLEMENT_HISTORICAL**
- **Mapping :** `HIGHER_COMMAND_ABSTRACTION` — identité **HIGH**, mapping formation **MEDIUM**.
- **Candidat :** **Jeffery Amherst**.
- **Naissance :** 1717-01-29 (`DAY`), Riverhead, Sevenoaks, Kent; territoire politique : Kingdom of Great Britain.
- **State V3 de naissance recommandé :** STATE_HOME_COUNTIES
- **Décès :** 1797-08-03
- **Grade au 1776-01-01 :** Lieutenant-general
- **Fonction :** Lieutenant-General of the Ordnance; principal conseiller militaire du roi en l'absence d'un Commander-in-Chief permanent
- **Période de fonction :** 1772 → 1782 (office d'Ordnance / responsabilités supérieures, selon la périodisation retenue); actif au 1776-01-01 : **YES**.
- **Profil recommandé :** culture `cu:british`, religion `rel:protestant`, IG `ig_armed_forces`, idéologie `ideology_royalist`.
- **Traits à envisager :** commandant vétéran; organisateur; prudent.
- **Réutilisation mod :** character=NO; template=NO; DNA=NO.
- **Portrait / description :** YES — NPG, mezzotinte de 1766 d'après Reynolds.
- **Raisonnement :** Ne pas l'appeler 'Baron Amherst' au 1er janvier: la pairie date de mai 1776. Le mapping est supérieur/administratif, pas un commandement direct de la Home Army telle que représentée par V3.
- **Sources principales :**
  - GB-AM-1 | Dictionary of Canadian Biography — Jeffery Amherst: né 29 janvier 1717 à Riverhead, Sevenoaks; mort 3 août 1797; lieutenant-general of the Ordnance dès 1772 et principal conseiller militaire du roi en l'absence d'un C-in-C
  - GB-AM-2 | National Portrait Gallery — portrait de Jeffery Amherst, mezzotinte de 1766 d'après Reynolds
  - MOD-3 | GitHub cleanup-post-release — common/character_templates/ + common/history/characters/ + repo-wide surname searches
- **Candidats rejetés / arbitrage :** Les anciens noms legacy John Colborne / Matthew Whitworth ne sont pas retenus : ils ne correspondent pas au commandement britannique de 1776; Amherst fournit une abstraction supérieure beaucoup plus solide.

#### GEN1776-021 — `cleanup2d3b_gbr_land_4`

- **HQ V3 :** `region_southern_europe`
- **Général actuel :** PROCEDURAL cleanup2d4_general_021
- **Décision :** **IMPLEMENT_HISTORICAL**
- **Mapping :** `THEATRE_COMMAND` — identité **HIGH**, mapping formation **HIGH**.
- **Candidat :** **George Augustus Eliott**.
- **Naissance :** 1717-12-25 (`DAY`), Stobs, Roxburghshire, Scotland; territoire politique : Kingdom of Great Britain.
- **State V3 de naissance recommandé :** STATE_LOWLANDS
- **Décès :** 1790-07-06
- **Grade au 1776-01-01 :** Lieutenant-general
- **Fonction :** Governor and commander of Gibraltar
- **Période de fonction :** 1775 → 1790; actif au 1776-01-01 : **YES**.
- **Profil recommandé :** culture `cu:scottish`, religion `rel:protestant`, IG `ig_armed_forces`, idéologie `ideology_royalist`.
- **Traits à envisager :** défenseur de forteresse; artillerie/ingénierie; discipliné.
- **Réutilisation mod :** character=NO; template=NO; DNA=NO.
- **Portrait / description :** YES — Royal Museums Greenwich / portraits et médailles.
- **Raisonnement :** Ne pas utiliser le titre Baron Heathfield dans le setup 1776: il est postérieur. Le lien Gibraltar ↔ HQ Europe méridionale est direct.
- **Sources principales :**
  - GB-EL-1 | Royal Museums Greenwich, archives — George Augustus Eliott: commandant en chef des forces en Irlande en 1774; nommé gouverneur de Gibraltar l'année suivante
  - GB-EL-2 | Dictionary of National Biography / Encyclopaedia Britannica — né à Stobs, Roxburghshire, 25 décembre 1717; lieutenant-general; gouverneur de Gibraltar à partir de 1775; mort 6 juillet 1790
  - MOD-1 | GitHub cleanup-post-release — common/history/military_formations/00_military_formations_europe.txt
- **Candidats rejetés / arbitrage :** Le legacy `aylmer_gen` manquant n'offre pas d'identité vérifiable. Eliott gouverne déjà Gibraltar en 1775.

#### GEN1776-022 — `cleanup2d3b_gbr_land_3`

- **HQ V3 :** `region_central_america`
- **Général actuel :** PROCEDURAL cleanup2d4_general_022
- **Décision :** **IMPLEMENT_HISTORICAL**
- **Mapping :** `MILITARY_OFFICEHOLDER` — identité **MEDIUM**, mapping formation **HIGH**.
- **Candidat :** **Montfort Browne**.
- **Naissance :** UNKNOWN (`UNKNOWN`), UNKNOWN; territoire politique : UNKNOWN.
- **State V3 de naissance recommandé :** aucun mapping sûr
- **Décès :** UNKNOWN
- **Grade au 1776-01-01 :** Lieutenant à demi-solde (ancien 35th Foot); gouverneur royal — ne pas rétrograder/élever artificiellement au rang de brigadier
- **Fonction :** Governor of the Bahamas / autorité de défense de New Providence
- **Période de fonction :** 1774 → 1776-03-04 (fin du contrôle effectif à Nassau; gouvernorat nominal parfois listé plus longtemps); actif au 1776-01-01 : **YES**.
- **Profil recommandé :** culture `cu:british (LOW confidence)`, religion `rel:protestant (LOW confidence)`, IG `ig_armed_forces`, idéologie `ideology_royalist`.
- **Traits à envisager :** loyaliste; administrateur colonial; éviter les traits de général de haut rang non prouvés.
- **Réutilisation mod :** character=NO; template=NO; DNA=NO.
- **Portrait / description :** NO SECURE PORTRAIT FOUND.
- **Raisonnement :** Très bon mapping géographique car la formation contient STATE_BAHAMAS. État civil incomplet: volontairement laissé UNKNOWN. Le grade de brigadier ne doit pas être daté de 1776-01-01, car il est postérieur.
- **Sources principales :**
  - GB-BR-1 | University of New Brunswick, Loyalist Collection — Montfort Browne: lieutenant-gouverneur de West Florida 1766–1769; gouverneur des Bahamas 1774–1780
  - GB-BR-2 | Naval Documents of the American Revolution — journal du 4 mars 1776: Governor Montfort Browne présent à Nassau lors du raid
  - GB-BR-3 | Founders Online / Washington Papers, note éditoriale — Browne avait quitté le 35th Foot comme lieutenant à demi-solde; son grade de brigadier n'est obtenu qu'en 1777
- **Candidats rejetés / arbitrage :** **Henry Hardinge** (legacy) est anachronique pour un commandement en 1776. Browne est physiquement gouverneur des Bahamas et présent à Nassau.

#### GEN1776-023 — `cleanup2d3b_gbr_land_5`

- **HQ V3 :** `region_south_india`
- **Général actuel :** PROCEDURAL cleanup2d4_general_023
- **Décision :** **IMPLEMENT_HISTORICAL**
- **Mapping :** `THEATRE_COMMAND` — identité **HIGH**, mapping formation **HIGH**.
- **Candidat :** **John Clavering**.
- **Naissance :** 1722 (`YEAR`), UNKNOWN — le siège familial de Greencroft (County Durham) n'est pas promu comme lieu de naissance sans preuve explicite; territoire politique : Kingdom of Great Britain.
- **State V3 de naissance recommandé :** aucun mapping sûr
- **Décès :** 1777-08-30
- **Grade au 1776-01-01 :** Lieutenant-general
- **Fonction :** Commander-in-Chief in India; membre du Supreme Council of Bengal
- **Période de fonction :** 1774 → 1777-08-30; actif au 1776-01-01 : **YES**.
- **Profil recommandé :** culture `cu:british`, religion `rel:protestant`, IG `ig_armed_forces`, idéologie `ideology_royalist`.
- **Traits à envisager :** commandant de théâtre; administrateur; expérimenté.
- **Réutilisation mod :** character=NO; template=NO; DNA=NO.
- **Portrait / description :** UNKNOWN — aucun portrait institutionnel sûr identifié dans l'audit.
- **Raisonnement :** Ne pas utiliser le titre K.B. au 1er janvier: son admission à l'ordre du Bain date du 9 novembre 1776. Naissance conservée à YEAR uniquement.
- **Sources principales :**
  - GB-CL-1 | Dictionary of Indian Biography — John Clavering: né en 1722; lieutenant-general en 1770; envoyé en Inde en 1774 comme Commander-in-Chief et membre du Supreme Council; mort 30 août 1777
  - GB-CL-2 | Dictionary of National Biography — John Clavering (1722–1777), officier britannique et membre du Supreme Council of Bengal
  - MOD-3 | GitHub cleanup-post-release — common/character_templates/ + common/history/characters/ + repo-wide surname searches
- **Candidats rejetés / arbitrage :** **Hugh Gough** (legacy) est anachronique pour 1776. Clavering est Commander-in-Chief in India depuis 1774.

### Luxembourg

#### GEN1776-046 — `Luxemburger_Miliz`

- **HQ V3 :** `region_western_europe`
- **Général actuel :** PROCEDURAL cleanup2d4_general_046
- **Décision :** **KEEP_PROCEDURAL**
- **Mapping :** `NO_DEFENSIBLE_MAPPING` — identité **N/A**, mapping formation **LOW**.
- **Candidat :** aucun candidat n'atteint le seuil de preuve.
- **Raisonnement :** Présence militaire autrichienne certaine, mais aucun commandant de la formation/milice luxembourgeoise au 1er janvier 1776 n'a été établi avec un niveau de preuve suffisant. Neipperg est mort en 1774. Ne pas dupliquer Ferraris artificiellement.
- **Sources principales :**
  - LU-1 | Ville de Luxembourg — histoire de la forteresse: garnison et administration militaire autrichiennes au XVIIIe siècle
  - LU-2 | Archives nationales de Luxembourg — cartes de 1776 par l'ingénieur Bergé, premier lieutenant de l'armée autrichienne; présence militaire attestée mais aucun commandant général de la milice identifié
  - LU-3 | Persée / étude historique — le gouverneur militaire antérieur Wilhelm Reinhard von Neipperg est mort en 1774, donc inéligible au 1er janvier 1776
- **Candidats rejetés / arbitrage :** **Wilhelm Reinhard von Neipperg** est inéligible car mort en 1774. Ferraris n'est pas dupliqué ici faute de preuve qu'il commandait spécifiquement la milice luxembourgeoise.

### Provinces-Unies / Pays-Bas

#### GEN1776-062 — `Koninklijk_Nederlands_Leger`

- **HQ V3 :** `region_western_europe`
- **Général actuel :** PROCEDURAL cleanup2d4_general_062
- **Décision :** **IMPLEMENT_HISTORICAL**
- **Mapping :** `HIGHER_COMMAND_ABSTRACTION` — identité **HIGH**, mapping formation **HIGH**.
- **Candidat :** **Lodewijk Ernst, hertog van Brunswijk-Wolfenbüttel**.
- **Naissance :** 1718-09-25 (`DAY`), Wolfenbüttel; territoire politique : Principality of Brunswick-Wolfenbüttel, Holy Roman Empire.
- **State V3 de naissance recommandé :** STATE_BRUNSWICK
- **Décès :** 1788-05-12
- **Grade au 1776-01-01 :** Veldmaarschalk (Field Marshal) des États-Généraux
- **Fonction :** Field Marshal au service des Provinces-Unies; autorité militaire supérieure et conseiller orangiste
- **Période de fonction :** 1750 → 1784-10-14; actif au 1776-01-01 : **YES**.
- **Profil recommandé :** culture `cu:north_german`, religion `rel:protestant`, IG `ig_armed_forces`, idéologie `ideology_royalist`.
- **Traits à envisager :** field marshal expérimenté; conseiller politique; conservateur/orangiste.
- **Réutilisation mod :** character=NO; template=NO; DNA=NO.
- **Portrait / description :** YES — Rijksmuseum, dessin/portrait daté 1763.
- **Raisonnement :** Le nom de formation du mod est anachroniquement 'Koninklijk'; le candidat est cependant parfaitement admissible pour les Provinces-Unies de 1776. Ne pas confondre avec un général néerlandais du XIXe siècle.
- **Sources principales :**
  - NL-BR-1 | Nationaal Archief, inventaire Fagel — dossier de nomination de Lodewijk Ernst, hertog van Brunswijk-Wolfenbüttel, comme veldmaarschalk au service des Provinces-Unies en 1750
  - NL-BR-2 | DBNL / Nieuw Nederlandsch Biografisch Woordenboek — né 25 septembre 1718 à Wolfenbüttel; veldmaarschalk néerlandais; abandon de ses charges militaires le 14 octobre 1784; mort 12 mai 1788 à Vechelde
  - NL-BR-3 | Rijksmuseum — dessin/portrait de 1763 légendé 'Gen. Veldmaarschalk van den Staat der Vereenigde Nederlanden'
- **Candidats rejetés / arbitrage :** Le stathouder Guillaume V aurait pu servir d'abstraction politico-militaire, mais Lodewijk Ernst est un professionnel nommé field marshal dès 1750 et offre un mapping militaire plus propre.

### Pays-Bas autrichiens / BEO

#### GEN1776-063 — `Armee_Belge`

- **HQ V3 :** `region_western_europe`
- **Général actuel :** PROCEDURAL cleanup2d4_general_063
- **Décision :** **IMPLEMENT_HISTORICAL**
- **Mapping :** `MILITARY_OFFICEHOLDER` — identité **HIGH**, mapping formation **MEDIUM**.
- **Candidat :** **Joseph-Jean-François, comte de Ferraris**.
- **Naissance :** 1726-04-20 (`DAY`), Lunéville, Lorraine; territoire politique : Duchy of Lorraine.
- **State V3 de naissance recommandé :** STATE_ALSACE_LORRAINE
- **Décès :** 1814-04-01
- **Grade au 1776-01-01 :** Feldmarschalleutnant
- **Fonction :** General-inspecteur d'Artillerie / officier supérieur des Pays-Bas autrichiens; direction de la carte militaire Ferraris
- **Période de fonction :** <=1770 (fonction d'inspection documentée avant 1776) → UNKNOWN; actif au 1776-01-01 : **YES**.
- **Profil recommandé :** culture `cu:french (Lorraine francophone; à arbitrer avec la culture de service)`, religion `rel:catholic`, IG `ig_armed_forces`, idéologie `ideology_moderate`.
- **Traits à envisager :** artillerie/ingénierie; cartographe; méticuleux; logistique.
- **Réutilisation mod :** character=NO; template=NO; DNA=NO.
- **Portrait / description :** YES — portrait connu, notamment une représentation de 1784; postérieure au setup.
- **Raisonnement :** Mapping militaire solide mais pas un commandement explicite de toute 'Armée belge'. La fonction d'inspection et son rôle central dans l'appareil militaire des Pays-Bas autrichiens justifient MILITARY_OFFICEHOLDER.
- **Sources principales :**
  - BE-FE-1 | KBR — carte des Pays-Bas autrichiens dirigée par le comte de Ferraris; titre le qualifiant général-inspecteur d'artillerie; travaux officiels 1769–1777
  - BE-FE-2 | Austrian Generals biographical dictionary — Joseph Johann Franz de Ferraris: né 20 avril 1726 à Lunéville; Feldmarschalleutnant au 1er mai 1773; mort 1er avril 1814 à Vienne
  - MOD-3 | GitHub cleanup-post-release — common/character_templates/ + common/history/characters/ + repo-wide surname searches
- **Candidats rejetés / arbitrage :** Le gouverneur général Charles-Alexandre de Lorraine est une figure politique forte, mais Ferraris fournit une fonction militaire technique et documentée dans les Pays-Bas autrichiens.

### Portugal

#### GEN1776-064 — `Exercito_Portugues`

- **HQ V3 :** `region_southern_europe`
- **Général actuel :** PROCEDURAL cleanup2d4_general_064
- **Décision :** **IMPLEMENT_HISTORICAL**
- **Mapping :** `MILITARY_OFFICEHOLDER` — identité **MEDIUM**, mapping formation **MEDIUM**.
- **Candidat :** **Duarte António da Câmara, 2.º marquês de Tancos**.
- **Naissance :** 1693 (`YEAR`), Ponta Delgada, São Miguel, Açores (lieu rapporté par la tradition biographique; jour/mois volontairement non promus); territoire politique : Kingdom of Portugal.
- **State V3 de naissance recommandé :** STATE_AZORES
- **Décès :** 1779
- **Grade au 1776-01-01 :** Tenente-general
- **Fonction :** Governador das Armas da Corte e da Província da Estremadura; Conselheiro da Guerra
- **Période de fonction :** <=1762 (fonction déjà attestée dans un imprimé de 1762) → 1779 (au plus tard); actif au 1776-01-01 : **YES**.
- **Profil recommandé :** culture `cu:portuguese`, religion `rel:catholic`, IG `ig_armed_forces`, idéologie `ideology_royalist`.
- **Traits à envisager :** officier supérieur de cour; administrateur militaire; aristocrate.
- **Réutilisation mod :** character=NO; template=NO; DNA=NO.
- **Portrait / description :** UNKNOWN — aucune référence institutionnelle de portrait suffisamment sûre n'a été fixée.
- **Raisonnement :** Choisi comme meilleure abstraction nationale. Robert Wrey est aussi actif en 1775 comme gouverneur des armes de Trás-os-Montes, mais il est moins senior et moins représentatif de l'ensemble de l'armée. Le comte de Lippe est rejeté: il n'exerce plus de commandement opérationnel portugais en 1776.
- **Sources principales :**
  - PT-TA-1 | PAEM / étude prosopographique de l'armée portugaise — D. Duarte António da Câmara, 2.º marquês de Tancos (1693–1779), tenente-general et Conselheiro da Guerra
  - PT-TA-2 | Dicionário histórico de Portugal — marquês de Tancos, général et governador das armas da Corte e província da Estremadura
  - PT-TA-3 | Colecção Pombalina / Arquivo Histórico Militar — correspondance adressée au marquês de Tancos en 1775 et 1776 sur les affaires militaires, munitions et forteresses
- **Candidats rejetés / arbitrage :** **Comte de Lippe** : rejeté pour le setup initial; son grand commandement portugais appartient à la crise de 1762–1768 et il n'exerce pas un commandement opérationnel au Portugal en 1776. **Robert Wrey** est actif en 1775 comme gouverneur des armes de Trás-os-Montes, mais son périmètre est plus provincial et son rang inférieur à celui de Tancos.

### Espagne

#### GEN1776-065 — `cleanup2d3b_spa_land_2`

- **HQ V3 :** `region_southern_europe`
- **Général actuel :** Antonio Ricardos (cleanup2d4_general_065)
- **Décision :** **KEEP_EXISTING_HISTORICAL**
- **Mapping :** `MILITARY_OFFICEHOLDER` — identité **HIGH**, mapping formation **MEDIUM**.
- **Candidat :** **Antonio Ricardos Carrillo de Albornoz**.
- **Naissance :** 1727-09-12 (`DAY`), Barbastro, Aragón; territoire politique : Spanish Monarchy.
- **State V3 de naissance recommandé :** STATE_ARAGON
- **Décès :** 1794-03-13
- **Grade au 1776-01-01 :** Teniente general
- **Fonction :** Inspector General de Caballería; réformateur de l'instruction de cavalerie
- **Période de fonction :** 1773 (inspection générale; activité confirmée par l'état militaire de 1776) → UNKNOWN; actif au 1776-01-01 : **YES**.
- **Profil recommandé :** culture `cu:spanish`, religion `rel:catholic`, IG `ig_armed_forces`, idéologie `ideology_reformer`.
- **Traits à envisager :** réformateur; cavalerie; méticuleux; commandant expérimenté.
- **Réutilisation mod :** character=YES — direct create_character dans le fichier de formations; template=NO; DNA=NO.
- **Portrait / description :** YES — portraits historiques signalés; référence institutionnelle à fixer avant DNA.
- **Raisonnement :** Choix CLEANUP-2D-4 confirmé comme officier supérieur effectivement en fonction le 1er janvier. Le mapping à la formation de New Castile reste une abstraction nationale/inspection, pas un commandement régional strict.
- **Sources principales :**
  - ES-RI-1 | PARES, notice d'autorité — Antonio Ricardos Carrillo de Albornoz: Barbastro, 12 septembre 1727 – Madrid, 13 mars 1794; lieutenant-general et inspector de caballería
  - ES-RI-2 | Estado Militar de España, 1776 — Antonio Ricardos apparaît comme Inspector General de Caballería (liste contemporaine)
  - MOD-1 | GitHub cleanup-post-release — common/history/military_formations/00_military_formations_europe.txt
- **Candidats rejetés / arbitrage :** Ricardos est réévalué et **confirmé** : état civil correct, vivant, teniente general et inspector general de caballería dans la liste militaire de 1776.

#### GEN1776-066 — `cleanup2d3b_spa_land_1`

- **HQ V3 :** `region_southern_europe`
- **Général actuel :** Alejandro O'Reilly (cleanup2d4_general_066)
- **Décision :** **REPLACE_EXISTING_HISTORICAL**
- **Mapping :** `FORMATION_COMMAND` — identité **HIGH**, mapping formation **HIGH**.
- **Candidat :** **Félix O'Neille y O'Neille**.
- **Naissance :** 1720-11-01 (`DAY`), Creggan, County Armagh, Kingdom of Ireland; territoire politique : Kingdom of Ireland under the British Crown.
- **State V3 de naissance recommandé :** STATE_ULSTER
- **Décès :** 1792-07-12
- **Grade au 1776-01-01 :** Mariscal de campo (grade de période; promotion ultérieure comme teniente general à ne pas antidater)
- **Fonction :** Comandante General / Capitán General del Reino de Galicia
- **Période de fonction :** 1774 (prise de fonction fin 1774; attesté comme Comandante General dans les actes de 1774) → 1776/1777 (date exacte de fin à vérifier avant implémentation); actif au 1776-01-01 : **YES**.
- **Profil recommandé :** culture `cu:irish`, religion `rel:catholic`, IG `ig_armed_forces`, idéologie `ideology_royalist`.
- **Traits à envisager :** commandant régional; vétéran; loyaliste bourbonien.
- **Réutilisation mod :** character=NO — le personnage actuellement présent est O'Reilly, pas O'Neille; template=NO; DNA=NO.
- **Portrait / description :** UNKNOWN — image secondaire existante mais provenance institutionnelle non verrouillée.
- **Raisonnement :** O'Reilly n'est PAS rejeté comme anachronique: il est bien Inspector General de Infantería depuis 1772 et actif au 1er janvier 1776. Il est remplacé uniquement parce qu'O'Neille fournit un mapping direct et documenté avec la Galice, où la formation du mod est ancrée.
- **Sources principales :**
  - ES-ON-1 | Actes municipaux / fonds galiciens, 1774 — correspondance de Félix O'Neille en qualité de 'Comandante General del Reino' de Galice
  - ES-ON-2 | Real Academia de la Historia / Diccionario Biográfico Español — Félix O'Neille y O'Neille: né à Creggan le 1 novembre 1720; officier irlandais au service de l'Espagne; mort 12 juillet 1792
  - ES-OR-1 | PARES — correspondance d'Alejandro O'Reilly en qualité d'Inspector General de Infantería, série active de 1772 à 1780
- **Candidats rejetés / arbitrage :** **Alejandro O'Reilly** est historiquement admissible : Inspector General de Infantería depuis 1772, donc actif au 1er janvier 1776. Il est néanmoins remplacé car Félix O'Neille est déjà Comandante General de Galicia en 1774 et correspond directement à la formation galicienne.

#### GEN1776-067 — `cleanup2d3b_spa_land_3`

- **HQ V3 :** `region_central_america`
- **Général actuel :** PROCEDURAL cleanup2d4_general_067
- **Décision :** **IMPLEMENT_HISTORICAL**
- **Mapping :** `THEATRE_COMMAND` — identité **HIGH**, mapping formation **HIGH**.
- **Candidat :** **Felipe de Fonsdeviela y Ondeano, II marqués de la Torre**.
- **Naissance :** 1725 (`YEAR`), Zaragoza, Aragón; territoire politique : Spanish Monarchy.
- **State V3 de naissance recommandé :** STATE_ARAGON
- **Décès :** 1784
- **Grade au 1776-01-01 :** Mariscal de campo
- **Fonction :** Gobernador y Capitán General de Cuba
- **Période de fonction :** 1771 → 1777; actif au 1776-01-01 : **YES**.
- **Profil recommandé :** culture `cu:spanish`, religion `rel:catholic`, IG `ig_armed_forces`, idéologie `ideology_royalist`.
- **Traits à envisager :** administrateur colonial; organisateur; défenses/fortifications.
- **Réutilisation mod :** character=NO; template=NO; DNA=NO.
- **Portrait / description :** YES — notice PARES avec iconographie; vérifier droits/provenance avant DNA.
- **Raisonnement :** Le HQ est Central America; Fonsdeviela est capitaine général de Cuba depuis 1771, donc nettement meilleur que le général procédural. Sa naissance reste YEAR: aucun jour/mois n'a été inventé.
- **Sources principales :**
  - ES-FO-1 | PARES, notice d'autorité — Felipe de Fonsdeviela y Ondeano, marqués de la Torre: Zaragoza 1725 – Madrid 1784; mariscal de campo en 1770; gobernador y capitán general de Cuba 1771–1777
  - ES-FO-2 | PARES / Archivo General de Indias — correspondance de Felipe de Fonsdeviela comme capitán general de Cuba, dossiers 1775–1776
  - MOD-1 | GitHub cleanup-post-release — common/history/military_formations/00_military_formations_europe.txt
- **Candidats rejetés / arbitrage :** Pour la formation Central America, O'Reilly ou Ricardos seraient des abstractions nationales moins précises. Fonsdeviela est déjà capitaine général de Cuba depuis 1771.

## 5. Réévaluation explicite de CLEANUP-2D-4

### William Howe
**CONFIRMÉ — KEEP_EXISTING_HISTORICAL.** Son commandement nord-américain commence le 10 octobre 1775, donc il satisfait strictement le test du `1776-01-01`. La seule donnée laissée volontairement incomplète est la localité exacte de naissance, faute de source institutionnelle vérifiée pendant cet audit.

### Antonio Ricardos
**CONFIRMÉ — KEEP_EXISTING_HISTORICAL.** Sa date de naissance `1727-09-12` à Barbastro est solide. Il est lieutenant-general et inspecteur général de la cavalerie; l'*Estado Militar de España* de 1776 confirme l'office dans la période du setup. Le lien avec la formation de New Castile reste une abstraction d'inspection nationale, d'où mapping MEDIUM.

### Alejandro O'Reilly
**HISTORIQUEMENT VALIDE MAIS À REMPLACER POUR CETTE FORMATION — REPLACE_EXISTING_HISTORICAL.** PARES documente son activité comme Inspector General de Infantería depuis 1772. Il n'est donc ni anachronique ni « faux ». Cependant, la formation `cleanup2d3b_spa_land_1` est fortement galicienne; Félix O'Neille est déjà Comandante General de Galicia fin 1774. La substitution améliore le mapping sans réécrire l'histoire d'O'Reilly.

### Rochambeau
**NE PAS FORCER DANS LE SETUP INITIAL.** Jean-Baptiste Donatien de Vimeur, comte de Rochambeau, est bien un officier général actif et inspecteur général. Mais son gouvernorat de Villefranche est seulement daté « 1776 » dans la notice contrôlée. La règle utilisateur impose de rejeter toute prise de poste possiblement postérieure au `1776-01-01`. Pour l'Alsace, Contades est de toute façon beaucoup plus direct.

## 6. Points de prudence avant une future implémentation

1. **Ne pas fabriquer de dates.** Browne reste `UNKNOWN`; Clavering, Tancos et Fonsdeviela restent `YEAR` lorsque le jour/mois n'est pas sécurisé.
2. **Ne pas antidater des titres.** Amherst n'est pas encore Baron Amherst au 1er janvier; Eliott n'est pas encore Baron Heathfield; Clavering n'est pas encore K.B.; Browne n'est pas encore brigadier.
3. **Éviter les doubles emplois.** Ferraris ne doit pas être copié sur Luxembourg sans preuve; O'Reilly peut être conservé pour un futur événement/office mais pas comme commandant galicien si O'Neille est adopté.
4. **DNA.** Aucun DNA existant n'a été trouvé pour ces candidats. Une future phase portrait/DNA doit partir d'images institutionnelles clairement attribuées et datées.
5. **State mapping.** `STATE_FRANCHE_COMTE`, `STATE_HOME_COUNTIES`, `STATE_AZORES` et `STATE_ULSTER` sont attestés dans les données/index du fork. `STATE_LOIRE` pour Montgeoffroy est un mapping géographique probable à revérifier contre les state regions vanilla 1.13 avant écriture.
6. **Formations abstraites.** Les armées V3 ne correspondent pas toujours à des commandements d'Ancien Régime. Les cas `HIGHER_COMMAND_ABSTRACTION` ou `MILITARY_OFFICEHOLDER` doivent rester explicitement marqués comme tels dans le futur code/documentation.

## 7. Statistiques de couverture

- **Formations auditées : 16**
- **Formations avec candidat historique recommandé/conservé : 15/16 = 93.75%**
- `IMPLEMENT_HISTORICAL` : 12
- `KEEP_EXISTING_HISTORICAL` : 2
- `REPLACE_EXISTING_HISTORICAL` : 1
- `KEEP_PROCEDURAL` : 1
- Mapping HIGH : 9; MEDIUM : 6; LOW : 1
- Précision naissance DAY : 11; MONTH : 0; YEAR : 3; UNKNOWN : 2
- **DNA existant réutilisable pour les candidats retenus : 0**
- **Templates historiques existants réutilisables pour les candidats retenus : 0**

## 8. Verdict de phase

La recherche permet de passer d'un setup Western Europe majoritairement procédural à une proposition **15/16 historiquement couverte** sans sacrifier la règle temporelle du 1er janvier 1776. Le seul cas volontairement non résolu est Luxembourg. La prochaine phase, si elle est lancée séparément, pourra transformer ce CSV en plan d'implémentation tout en conservant les précautions de date, de mapping et de DNA ci-dessus.

## Référentiel des sources

### Dépôt / setup du mod

- **MOD-1** — branche `cleanup-post-release`, `common/history/military_formations/00_military_formations_europe.txt` : inventaire des formations, HQ, unités, scopes et généraux de CLEANUP-2D-4.
  - https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/cleanup-post-release/common/history/military_formations/00_military_formations_europe.txt
- **MOD-2** — `common/dna_data/` : audit des DNA nommés.
  - https://github.com/Malzars-sys/1776-Age-of-Revolutions/tree/cleanup-post-release/common/dna_data
- **MOD-3** — `common/character_templates/`, `common/history/characters/` et recherches repo-wide dans `events/` et le reste du dépôt.
  - https://github.com/Malzars-sys/1776-Age-of-Revolutions/tree/cleanup-post-release/common/character_templates
  - https://github.com/Malzars-sys/1776-Age-of-Revolutions/tree/cleanup-post-release/common/history/characters

### Sources historiques principales

- **FR-SG-1 / FR-SG-2** — CCFr / Bibliothèque nationale de France, correspondance de Claude-Louis de Saint-Germain comme secrétaire d'État de la Guerre (4 novembre 1775; 7 juin 1776) et notice biographique. Une notice consultée est accessible via :
  - https://ccfr.bnf.fr/portailccfr/ark%3A/16871/004a1393970
- **FR-CO-1 / FR-CO-2** — Fédération des Sociétés d'Histoire et d'Archéologie d'Alsace; État militaire de France / notice historique de Contades.
- **FR-RI-1 / FR-RI-2** — BnF (notice d'autorité Richelieu); Larousse, notice biographique du maréchal de Richelieu.
- **FR-EN-1** — ordonnance imprimée à Port-au-Prince le 23 octobre 1775 détaillant les titres militaires et coloniaux de d'Ennery.
- **FR-EN-2 / FR-EN-3** — notice de la commune d'Ennery; Ministère français de la Culture, base Palissy.
- **GB-HO-1 / GB-HO-2** — Dictionary of National Biography; National Portrait Gallery.
- **GB-AM-1 / GB-AM-2** — Dictionary of Canadian Biography; National Portrait Gallery.
- **GB-EL-1 / GB-EL-2** — Royal Museums Greenwich; Dictionary of National Biography / Encyclopaedia Britannica.
- **GB-BR-1 / GB-BR-2 / GB-BR-3** — University of New Brunswick, Loyalist Collection; Naval Documents of the American Revolution; Founders Online / Washington Papers.
- **GB-CL-1 / GB-CL-2** — Dictionary of Indian Biography; Dictionary of National Biography.
- **NL-BR-1 / NL-BR-2 / NL-BR-3** — Nationaal Archief (fonds Fagel); DBNL / NNBW; Rijksmuseum.
- **BE-FE-1 / BE-FE-2** — KBR, carte de Ferraris et manuscrits associés; dictionnaire biographique des généraux autrichiens.
- **PT-TA-1 / PT-TA-2 / PT-TA-3** — PAEM / prosopographie militaire; Dicionário histórico de Portugal; Colecção Pombalina / Arquivo Histórico Militar.
- **ES-RI-1 / ES-RI-2** — PARES; *Estado Militar de España* (1776).
- **ES-ON-1 / ES-ON-2** — actes municipaux/fonds galiciens de 1774; Real Academia de la Historia / Diccionario Biográfico Español.
- **ES-OR-1** — PARES, correspondance d'Alejandro O'Reilly comme Inspector General de Infantería.
- **ES-FO-1 / ES-FO-2** — PARES, notice d'autorité et correspondance de l'Archivo General de Indias pour Felipe de Fonsdeviela.
- **LU-1 / LU-2 / LU-3** — Ville de Luxembourg; Archives nationales de Luxembourg; étude historique Persée.

> **Important :** lorsqu'une source institutionnelle consultée n'a pas fourni un jour/mois de naissance, ce rapport conserve volontairement `YEAR` ou `UNKNOWN`. Les URLs opaques de catalogues qui n'ont pas pu être stabilisées ne sont pas reconstituées artificiellement.
