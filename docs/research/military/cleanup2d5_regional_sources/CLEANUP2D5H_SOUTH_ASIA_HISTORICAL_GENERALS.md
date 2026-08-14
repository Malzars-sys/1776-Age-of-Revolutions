# CLEANUP-2D-5H — SOUTH ASIA HISTORICAL GENERALS 1776

## Statut

- **Projet** : Victoria 3 — *1776 Age of Revolutions*
- **Dépôt audité** : `Malzars-sys/1776-Age-of-Revolutions`
- **Branche** : `cleanup-post-release`
- **Date de référence absolue** : **1776-01-01**
- **Nature de cette phase** : **recherche historique uniquement**
- **Aucune modification gameplay, aucun commit, aucun push.**
- Fichier principal audité : `common/history/military_formations/05_military_formations_india.txt` (blob observé pendant l'audit : `c06f32902af6925825399ef0ea23fc6f7879a9fc`).

## Résumé exécutif

L'audit du fichier de formations indien donne **20 tags et 25 formations terrestres** au total, après exclusion des flottes. La phase 2D-4 avait déjà nommé huit personnages : Jassa Singh Ahluwalia, John Clavering, Haripant Phadke, Tukoji Holkar, Mahadji Shinde, Hyder Ali, Eustachius De Lannoy et Mirza Najaf Khan. Ces huit choix sont historiquement défendables au 1er janvier 1776, mais leur implémentation actuelle est incomplète : dans le fichier de formations ils sont tous créés avec `template = default`, sans date de naissance, culture, religion ni DNA explicitement fixés.

**Résultat recommandé :**

- **8 profils 2D-4 à conserver**, mais à reconstruire avec données biographiques explicites ;
- **4 ajouts historiques solides ou solides sous condition** : Sir Robert Fletcher, James Stuart (d. 1793), Tipu Sultan et Mudhoji Bhonsle ;
- **13 formations à laisser procédurales** pour éviter d'inventer une hiérarchie ou de transformer automatiquement un souverain en général ;
- **Tukoji Holkar** reste admissible comme personne, mais son affectation actuelle à une formation centrée sur `STATE_AGRA` mérite un réexamen géographique lors de l'implémentation.

## 1. Périmètre exact du dépôt

| ID | Tag | Formation | 2D-4 actuel | Verdict recherche |
|---|---|---|---|---|
| GEN1776-118 | `PAN` | `FaujiKhas` | Jassa Singh Ahluwalia | **RETAIN_NAMED_HISTORICAL_GENERAL** |
| GEN1776-119 | `PAN` | `FaujiAin` | procédural | **KEEP_PROCEDURAL_COLLECTIVE_STRUCTURE** |
| GEN1776-120 | `BIC` | `cleanup2d3b_bic_land_2` | procédural | **ADD_NAMED_HISTORICAL_GENERAL** |
| GEN1776-121 | `BIC` | `cleanup2d3b_bic_land_3` | procédural | **ADD_NAMED_HISTORICAL_GENERAL** |
| GEN1776-122 | `BIC` | `Bengal_Army` | John Clavering | **RETAIN_NAMED_HISTORICAL_GENERAL** |
| GEN1776-123 | `HYD` | `sarf_e_khas` | procédural | **KEEP_PROCEDURAL_REFERENCE_DATE_UNCERTAIN** |
| GEN1776-124 | `AWA` | `OudhRoyalArmy` | procédural | **KEEP_PROCEDURAL_NO_INDEPENDENT_COMMANDER_SECURE** |
| GEN1776-125 | `MARATH` | `cleanup2d3b_marath_land_2` | Haripant Phadke | **RETAIN_NAMED_HISTORICAL_GENERAL** |
| GEN1776-126 | `MARATH` | `cleanup2d3b_marath_land_1` | Tukoji Holkar | **RETAIN_NAMED_REVIEW_FORMATION_MAPPING** |
| GEN1776-127 | `GWA` | `GwaliorArmy` | Mahadji Shinde | **RETAIN_NAMED_HISTORICAL_GENERAL** |
| GEN1776-128 | `NAG` | `NagpurArmy` | procédural | **ADD_NAMED_HISTORICAL_GENERAL_CONDITIONAL_RULER_DUPLICATION** |
| GEN1776-129 | `MYS` | `cleanup2d3b_mys_land_2` | Hyder Ali | **RETAIN_NAMED_HISTORICAL_GENERAL** |
| GEN1776-130 | `MYS` | `cleanup2d3b_mys_land_1` | procédural | **ADD_NAMED_HISTORICAL_GENERAL** |
| GEN1776-131 | `COO` | `CoochBeharArmy` | procédural | **KEEP_PROCEDURAL** |
| GEN1776-132 | `GAR` | `GarhwalArmy` | procédural | **KEEP_PROCEDURAL** |
| GEN1776-133 | `SAT` | `SataraArmy` | procédural | **KEEP_PROCEDURAL_STRUCTURE_DUBIOUS** |
| GEN1776-134 | `KHP` | `KolhapurArmy` | procédural | **KEEP_PROCEDURAL** |
| GEN1776-135 | `KNO` | `KurnoolArmy` | procédural | **KEEP_PROCEDURAL** |
| GEN1776-136 | `BHV` | `BhavnagarArmy` | procédural | **KEEP_PROCEDURAL_RULER_NOT_AUTO_GENERAL** |
| GEN1776-137 | `PUD` | `PudukottaiArmy` | procédural | **KEEP_PROCEDURAL_RULER_NOT_AUTO_GENERAL** |
| GEN1776-138 | `JEY` | `JeyporeArmy` | procédural | **KEEP_PROCEDURAL_NO_COMMANDER_SECURE** |
| GEN1776-139 | `COC` | `CochinArmy` | procédural | **KEEP_PROCEDURAL_PENDING_STRUCTURE_REWORK** |
| GEN1776-140 | `TRA` | `TravancoreArmy` | Eustachius De Lannoy | **RETAIN_NAMED_HISTORICAL_GENERAL** |
| GEN1776-141 | `SIN` | `SindhArmy` | procédural | **KEEP_PROCEDURAL_DYNASTIC_TRANSITION** |
| GEN1776-142 | `MUG` | `MughalArmy` | Mirza Najaf Khan | **RETAIN_NAMED_HISTORICAL_GENERAL** |

### Point de structure

Le fichier ne décrit pas une seule « armée indienne », mais un ensemble de formations liées à des polities très différentes : Compagnie britannique des Indes orientales, monarchies, maisons marathes, misls sikhs, petits États princiers et armée moghole. La recherche ne doit donc **pas homogénéiser les fonctions**. Le titre « général » de Victoria 3 est ici un rôle gameplay ; le rapport conserve le statut historique réel dans les champs `rank_status_1776` et `office_on_1776_01_01`.

## 2. Erreurs probables des profils CLEANUP-2D-4 actuels

Le problème commun est structurel : `template = default` + nom historique ne suffit pas à créer un personnage historique. Sans biographie explicite, le moteur peut produire un âge, une culture, une religion et une apparence procéduraux. Une valeur qui tombe juste par hasard n'est pas une donnée historiquement contrôlée.

| Personnage 2D-4 | Erreurs / risques principaux |
|---|---|
| **Jassa Singh Ahluwalia** | âge et DNA procéduraux ; lieu de naissance absent ; culture/religion possiblement correctes par contexte PAN mais non garanties ; surtout, risque de le présenter comme chef d'une armée nationale centralisée au lieu d'un chef de misl / Dal Khalsa confédéral. |
| **John Clavering** | âge non fixé ; origine anglaise absente ; DNA procédural ; tout héritage culturel/religieux indien serait faux ; le 31 août 1722 est un **baptême**, pas une naissance prouvée. |
| **Haripant Phadke** | date de naissance non fixée alors que les sources disent explicitement qu'elle est inconnue ; DNA procédural ; origine exacte à ne pas réduire automatiquement à Guhagar. |
| **Tukoji Holkar** | âge/DNA procéduraux ; naissance exacte encore contradictoire dans les sources secondaires ; affectation Agra potentiellement mal alignée avec sa présence au sud après 1774. |
| **Mahadji Shinde** | âge/DNA procéduraux ; risque d'utiliser l'exact `3 Dec 1730` alors que la Marathi Vishwakosh donne `? 1727` ; cadre « Gwalior Army » trop centralisé si interprété littéralement en 1776. |
| **Hyder Ali** | âge procédural ; risque élevé d'une religion hindoue si héritage pays ; culture à traiter comme identité mysorienne/deccani musulmane et non simple copie du pays ; DNA non historique. |
| **Eustachius De Lannoy** | **erreur potentielle la plus nette** : il était un Européen flamand/sud-néerlandais et catholique romain, pas Malayali et hindou ; âge, origine et DNA non fixés. |
| **Mirza Najaf Khan** | **erreur potentielle majeure** : Iranien/Persan, de lignée safavide et chiite ; un profil moghol généré nord-indien/sunnite serait historiquement faux ; âge/origine/DNA non fixés. |

## 3. Dossiers historiques — profils à nommer

### Jassa Singh Ahluwalia — GEN1776-118 / PAN / `FaujiKhas`

- **Verdict** : RETAIN_NAMED_HISTORICAL_GENERAL
- **Variantes** : Jassā Siṅgh Āhlūvālīā; Jassa Singh Ahluvalia
- **Naissance** : 1718-05-03 — exact_day_high_confidence
- **Lieu de naissance** : Ahlu village, near Lahore
- **Polité de naissance** : Mughal Empire, Lahore Subah
- **State V3 de naissance** : STATE_PUNJAB
- **Décès** : 1783-10-20 — exact_day_high_confidence
- **Rang/statut** : Sardar; chief of Ahluwalia misl; senior commander of Dal Khalsa
- **Poste au 1776-01-01** : Ahluwalia misl chief and leading Dal Khalsa commander within Sikh confederate structure
- **Début de fonction** : 1748 (year_for_Dal_Khalsa_command)
- **Fin de fonction** : 1783-10-20 (death)
- **Armée/théâtre** : Punjab; misl/Dal Khalsa confederate forces, not a centralized national standing army
- **Culture historique** : Punjabi Sikh
- **Culture V3 recommandée** : panjabi/punjabi token — verify exact mod token — confiance HIGH
- **Religion réelle** : Sikh
- **Religion V3** : sikh — confiance HIGH
- **Origine sociale/caste** : Sikh sardar; son of Badar Singh; no caste assignment needed for gameplay
- **IG** : ig_armed_forces primary; ig_landowners secondary only if desired for misl aristocracy
- **Idéologie** : NONE — no modern ideology mapping justified
- **Traits documentés seulement** : Courageous confederate military leader; organizer; religiously respected. Do not infer modern nationalist traits.
- **Portrait / description** : Use authenticated/recognized Sikh portrait tradition cautiously; many images are later idealizations. Prioritize identity markers and period Sikh sardar dress over random DNA.
- **Présence mod / template / DNA** : Current 2D-4 direct character uses template=default; no birth/culture/religion/DNA pinned in formation file.
- **Erreurs 2D-4 probables** : Age procedural/uncontrolled; origin absent; DNA/appearance procedural; culture/religion may happen to match PAN but are not explicitly controlled.
- **Confiance date de référence** : HIGH
- **Note de décision** : Excellent historical match, but label as confederate Sikh command. FaujiKhas is an abstraction; do not imply a unified Punjabi national army.
- **Sources principales** :
  - https://eos.learnpunjabi.org/JASSA%20SINGH%20AHLUVALIA%20%281718-1783%29.html
  - https://eos.learnpunjabi.org/MISLS.html

### Sir Robert Fletcher — GEN1776-120 / BIC / `cleanup2d3b_bic_land_2`

- **Verdict** : ADD_NAMED_HISTORICAL_GENERAL
- **Variantes** : Robert Fletcher; Brigadier-General Sir Robert Fletcher
- **Naissance** : c.1738 — circa_year
- **Lieu de naissance** : Unknown in sources consulted
- **Polité de naissance** : Great Britain (precise birthplace unresolved)
- **State V3 de naissance** : UNRESOLVED_OUTSIDE_SOUTH_ASIA
- **Décès** : 1776-12-24 — exact_day_secondary; BL confirms 1776
- **Rang/statut** : Brigadier-General; Commander-in-Chief, Madras Army
- **Poste au 1776-01-01** : Commander-in-Chief of the East India Company Madras Army
- **Début de fonction** : 1775 (year_high_confidence)
- **Fin de fonction** : 1776-12-24 (death)
- **Armée/théâtre** : Madras Presidency / Coromandel / Northern Circars
- **Culture historique** : British; probably English, exact birthplace unresolved
- **Culture V3 recommandée** : english only after birthplace/family verification; never Indian culture — confiance MEDIUM
- **Religion réelle** : Protestant probable; not directly established by priority source pass
- **Religion V3** : protestant provisional — confiance LOW-MEDIUM
- **Origine sociale/caste** : British officer and politician; East India Company military elite
- **IG** : ig_armed_forces
- **Idéologie** : NONE
- **Traits documentés seulement** : Experienced commander; controversial Company officer. Avoid turning political controversy into an unsupported personality trait.
- **Portrait / description** : Contemporary portrait dated roughly 1774–76 is reported in later references; verify asset provenance before DNA reconstruction.
- **Présence mod / template / DNA** : Formation currently receives a procedural default-template general; no dedicated Fletcher template/DNA found in the audited formation file.
- **Erreurs 2D-4 probables** : Entire identity is procedural at present; assigning Indian culture/religion would be incorrect.
- **Confiance date de référence** : HIGH
- **Note de décision** : Strong replacement for one Circars/Madras formation: BL India Office catalogue explicitly lists C-in-C Madras 1775–76.
- **Sources principales** :
  - https://searcharchives.bl.uk/?f%5Brelated_names_ssim%5D%5B%5D=Fletcher%2C+Robert%2C+army+officer+and+politician%2C+c+1738-1776&search_field=all_fields

### James Stuart — GEN1776-121 / BIC / `cleanup2d3b_bic_land_3`

- **Verdict** : ADD_NAMED_HISTORICAL_GENERAL
- **Variantes** : Colonel James Stuart; later Brigadier-General / Major-General James Stuart (d. 1793); NOT James Stuart (1741–1815)
- **Naissance** : inconnue — unknown_18th_century
- **Lieu de naissance** : Unknown in sources consulted
- **Polité de naissance** : Great Britain; family was Scottish, precise birthplace unresolved
- **State V3 de naissance** : UNRESOLVED_OUTSIDE_SOUTH_ASIA
- **Décès** : 1793-02-02 — exact_day_high_confidence
- **Rang/statut** : Colonel, East India Company service
- **Poste au 1776-01-01** : Second in command on the Coromandel Coast
- **Début de fonction** : 1775 (year_high_confidence)
- **Fin de fonction** : 1776-12 (month; succeeded Fletcher as C-in-C after Fletcher death)
- **Armée/théâtre** : Coromandel Coast / Madras Presidency
- **Culture historique** : British; Scottish family identity
- **Culture V3 recommandée** : scottish probable; verify exact personal birthplace before hardcoding — confiance MEDIUM
- **Religion réelle** : Protestant probable; not directly established in DNB entry
- **Religion V3** : protestant provisional — confiance LOW-MEDIUM
- **Origine sociale/caste** : British army officer; brother of Andrew Stuart
- **IG** : ig_armed_forces
- **Idéologie** : NONE
- **Traits documentés seulement** : Experienced combat officer; distinguished at Havana; later able line commander. Do not import later Madras political conflict as ideology.
- **Portrait / description** : George Romney portrait exists for the correct James Stuart (d.1793); use that identity, not the distinct 1741–1815 general.
- **Présence mod / template / DNA** : Formation currently procedural; no dedicated Stuart character in audited formation block.
- **Erreurs 2D-4 probables** : Current procedural identity has no historical age/culture/religion/DNA. High risk of conflating him with James Stuart (1741–1815).
- **Confiance date de référence** : HIGH
- **Note de décision** : Very strong second Madras candidate exactly in post from 1775. Explicit disambiguation is essential.
- **Sources principales** :
  - https://en.wikisource.org/wiki/Stuart%2C_James_%28d.1793%29_%28DNB00%29

### Sir John Clavering — GEN1776-122 / BIC / `Bengal_Army`

- **Verdict** : RETAIN_NAMED_HISTORICAL_GENERAL
- **Variantes** : John Clavering; Lieutenant-General Sir John Clavering KB
- **Naissance** : 1722 — year_only; baptised 1722-08-31 at Lanchester
- **Lieu de naissance** : Lanchester, County Durham
- **Polité de naissance** : Kingdom of Great Britain
- **State V3 de naissance** : UNRESOLVED_OUTSIDE_SOUTH_ASIA
- **Décès** : 1777-08-30 — exact_day_high_confidence
- **Rang/statut** : Lieutenant-General
- **Poste au 1776-01-01** : Commander of the Bengal Army; member of the Supreme Council of Bengal
- **Début de fonction** : 1774-10 (month_high_confidence_arrival)
- **Fin de fonction** : 1777-08-30 (death)
- **Armée/théâtre** : Bengal Presidency / northern Company army administration
- **Culture historique** : English
- **Culture V3 recommandée** : english — confiance HIGH
- **Religion réelle** : Church of England / Protestant probable
- **Religion V3** : protestant — confiance MEDIUM-HIGH
- **Origine sociale/caste** : English baronet family; professional army officer
- **IG** : ig_armed_forces
- **Idéologie** : NONE; political opposition to Hastings is not a V3 ideology
- **Traits documentés seulement** : Experienced Seven Years War commander; straightforward and forceful. Avoid caricaturing council disputes.
- **Portrait / description** : British lieutenant-general / KB portrait or engraving; verify sitter provenance. Uniform should be British, not Company-Indian.
- **Présence mod / template / DNA** : Current 2D-4 direct character uses template=default; no biographical fields or DNA pinned in formation file.
- **Erreurs 2D-4 probables** : Age procedural; birthplace/origin absent; DNA procedural; any Indian culture/religion would be wrong. Baptism date must not be silently treated as birth date.
- **Confiance date de référence** : HIGH
- **Note de décision** : Retain. His Bengal Army command is an exceptionally strong reference-date match.
- **Sources principales** :
  - https://en.wikisource.org/wiki/Dictionary_of_National_Biography%2C_1885-1900/Clavering%2C_John
  - https://searcharchives.bl.uk/catalog/040-001116470
  - https://reed.dur.ac.uk/xtf/view?docId=ark%2F32150_s1kw52j8058.xml

### Haripant Phadke — GEN1776-125 / MARATH / `cleanup2d3b_marath_land_2`

- **Verdict** : RETAIN_NAMED_HISTORICAL_GENERAL
- **Variantes** : Haripant Phadke; Hari Pant Phadke; Haripant Fadke
- **Naissance** : c.1729 — circa_year; exact date explicitly unknown
- **Lieu de naissance** : Exact birthplace not securely established; family originally from Guhagar, Konkan
- **Polité de naissance** : Maratha realm (probable)
- **State V3 de naissance** : STATE_BOMBAY provisional if Guhagar association is used
- **Décès** : 1794-06-20 — exact_day_high_confidence
- **Rang/statut** : Senior Maratha commander and statesman; Barbhai leader
- **Poste au 1776-01-01** : Senior military-political servant of the Peshwa/Barbhai regency; active in pursuit and containment of Raghunathrao
- **Début de fonction** : 1773-1774 (period; rise during Barbhai crisis)
- **Fin de fonction** : 1794-06-20 (death)
- **Armée/théâtre** : Pune/Peshwa forces; Gujarat–Deccan operations around Raghunathrao; confederate context
- **Culture historique** : Marathi
- **Culture V3 recommandée** : marathi — confiance HIGH
- **Religion réelle** : Hindu
- **Religion V3** : hindu — confiance HIGH
- **Origine sociale/caste** : Family with clerical/moneylending service background; do not add caste without stronger evidence
- **IG** : ig_armed_forces primary
- **Idéologie** : NONE
- **Traits documentés seulement** : State-minded, selfless, fearless, good judge of men, strong capacity for coalition/administrative support — all explicitly praised in Marathi Vishwakosh.
- **Portrait / description** : No secure contemporary life portrait established in this pass; use generic historically grounded Maratha officer appearance rather than invented distinctive DNA.
- **Présence mod / template / DNA** : Current 2D-4 direct character uses template=default; no birth/culture/religion/DNA pinned.
- **Erreurs 2D-4 probables** : Age and appearance procedural; exact birthplace currently absent; culture/religion may match country but are not explicit.
- **Confiance date de référence** : HIGH
- **Note de décision** : Retain, with explicit confederal/Peshwa context rather than “national Maratha general”.
- **Sources principales** :
  - https://vishwakosh.marathi.gov.in/27523/
  - https://vishwakosh.marathi.gov.in/29242/

### Tukoji Rao Holkar I — GEN1776-126 / MARATH / `cleanup2d3b_marath_land_1`

- **Verdict** : RETAIN_NAMED_REVIEW_FORMATION_MAPPING
- **Variantes** : Tukoji Holkar; Tukojirao Holkar; Tukoji Rao I Holkar
- **Naissance** : 1723-06-26 — claimed_exact_day_but_source_conflict; same secondary page also says 1725; verify before hardcoding
- **Lieu de naissance** : Unknown in sources consulted
- **Polité de naissance** : Maratha sphere, exact locality unresolved
- **State V3 de naissance** : UNRESOLVED
- **Décès** : 1797-08-15 — exact_day_high_confidence
- **Rang/statut** : Senapati / chief of Holkar military forces under Ahilyabai Holkar
- **Poste au 1776-01-01** : Military head of the Holkar house; external campaigns entrusted to him while Ahilyabai held civil authority
- **Début de fonction** : 1767 (year_high_confidence)
- **Fin de fonction** : 1795 (became sole ruler after Ahilyabai; continued military role)
- **Armée/théâtre** : Holkar/Maratha confederate forces; returned south in 1774 and was on Peshwa campaigns through 1778
- **Culture historique** : Marathi / Holkar Maratha-Dhangar milieu
- **Culture V3 recommandée** : marathi — confiance HIGH
- **Religion réelle** : Hindu
- **Religion V3** : hindu — confiance HIGH
- **Origine sociale/caste** : Holkar house; Marathi Vishwakosh identifies family origin as Dhangar
- **IG** : ig_armed_forces primary; ig_landowners secondary
- **Idéologie** : NONE
- **Traits documentés seulement** : Experienced campaign commander; loyal military counterpart to Ahilyabai. Avoid inventing a centralized-state ideology.
- **Portrait / description** : Known later portrait tradition exists; use cautiously because several depictions are posthumous.
- **Présence mod / template / DNA** : Current 2D-4 direct character uses template=default; no historical DNA or dates pinned.
- **Erreurs 2D-4 probables** : Age/DNA procedural; birthplace absent. Formation mapping is questionable: source evidence places him back in the south from 1774, whereas current formation is STATE_AGRA.
- **Confiance date de référence** : HIGH_PERSON / MEDIUM_FORMATION_ASSIGNMENT
- **Note de décision** : The person is admissible, but the north/Agra attachment deserves re-evaluation during implementation; do not silently treat Holkar forces as a unitary Peshwa standing army.
- **Sources principales** :
  - https://vishwakosh.marathi.gov.in/20242/
  - https://vishwakosh.marathi.gov.in/29242/

### Mahadji Shinde — GEN1776-127 / GWA / `GwaliorArmy`

- **Verdict** : RETAIN_NAMED_HISTORICAL_GENERAL
- **Variantes** : Mahadji Shinde; Mahadji Scindia; Mahadaji Sindhia
- **Naissance** : c.1727 — year_uncertain; Maharashtra state encyclopedia gives ?1727; reject false exact 1730 day without stronger evidence
- **Lieu de naissance** : Exact birthplace not explicitly secured; family seat Kanherkhed, Satara district
- **Polité de naissance** : Maratha realm
- **State V3 de naissance** : STATE_BOMBAY provisional for Satara/Kanherkhed
- **Décès** : 1794-02-12 — exact_day_high_confidence
- **Rang/statut** : Maratha sardar; head of Shinde/Scindia power
- **Poste au 1776-01-01** : Senior Shinde chief within Maratha confederacy; northern/Malwa military-political leader aligned with Barbhai after initial hesitation
- **Début de fonction** : 1768 (year_sardarship)
- **Fin de fonction** : 1794-02-12 (death)
- **Armée/théâtre** : Malwa / northern India / Maratha confederate politics; Gwalior tag is a useful abstraction but later institutional form should not be back-projected
- **Culture historique** : Marathi
- **Culture V3 recommandée** : marathi — confiance HIGH
- **Religion réelle** : Hindu; documented Krishna devotion and broad respect for Hindu/Muslim holy men
- **Religion V3** : hindu — confiance HIGH
- **Origine sociale/caste** : Shinde house; mother Chima Bai described as Rajput; avoid simplistic caste gameplay assignment
- **IG** : ig_armed_forces primary; ig_landowners secondary
- **Idéologie** : NONE
- **Traits documentés seulement** : Battle-hardened; disciplined; self-respecting; tactically prudent about when to fight or withdraw; wounded at Panipat.
- **Portrait / description** : James Wales oil portrait tradition provides a strong late-18th-century visual reference; use identifiable white robe/turban/jewelry rather than random DNA.
- **Présence mod / template / DNA** : Current 2D-4 direct character uses template=default; no birth/culture/religion/DNA pinned.
- **Erreurs 2D-4 probables** : Age and DNA procedural; current runtime may use an anachronistically exact 1730 birth if inferred elsewhere; origin absent. Gwalior institutional framing may be too centralized for 1776.
- **Confiance date de référence** : HIGH
- **Note de décision** : Retain. Use Shinde/Scindia confederal chief framing; do not describe a later European-drilled Gwalior army as already fully formed in 1776.
- **Sources principales** :
  - https://vishwakosh.marathi.gov.in/33475/
  - https://commons.wikimedia.org/wiki/File:Mahadaji_Sindhia.jpg

### Mudhoji Bhonsle — GEN1776-128 / NAG / `NagpurArmy`

- **Verdict** : ADD_NAMED_HISTORICAL_GENERAL_CONDITIONAL_RULER_DUPLICATION
- **Variantes** : Mudhoji Bhosle; Mudhoji Bhonsle; Mudhoji I
- **Naissance** : inconnue — unknown; do not use weak 1735 claim
- **Lieu de naissance** : Unknown in priority sources consulted
- **Polité de naissance** : Maratha/Bhonsle sphere, unresolved
- **State V3 de naissance** : UNRESOLVED
- **Décès** : 1788-05-19 — exact_day_high_confidence
- **Rang/statut** : Sena-Dhurandhar; regent/master of Berar and Nagpur after victory over Sabaji
- **Poste au 1776-01-01** : Unchallenged master/regent of Berar and Nagpur; experienced military chief with Sena-Dhurandhar title
- **Début de fonction** : 1775-01-26 (battle-date threshold for uncontested mastery)
- **Fin de fonction** : 1788-05-19 (death)
- **Armée/théâtre** : Nagpur / Berar / Chandrapur; Bhonsle forces
- **Culture historique** : Marathi
- **Culture V3 recommandée** : marathi — confiance HIGH
- **Religion réelle** : Hindu probable
- **Religion V3** : hindu — confiance MEDIUM-HIGH
- **Origine sociale/caste** : Bhonsle dynastic military nobility
- **IG** : ig_armed_forces + ig_landowners
- **Idéologie** : NONE
- **Traits documentés seulement** : Experienced dynastic commander; victorious at Panchgaon 26 Jan 1775; restored/controlled state after civil conflict.
- **Portrait / description** : No secure contemporary portrait established in this pass; avoid creating distinctive DNA from modern images.
- **Présence mod / template / DNA** : Formation currently procedural. Check country-history ruler creation before implementation to avoid duplicate Mudhoji character.
- **Erreurs 2D-4 probables** : Current general entirely procedural. Main implementation risk is duplicating a ruler if Mudhoji already exists elsewhere.
- **Confiance date de référence** : HIGH_FOR_ROLE / MEDIUM_FOR_CHARACTER_DUPLICATION
- **Note de décision** : Strong historical commander for NagpurArmy, but add only if the mod does not already instantiate him as the ruler; otherwise reuse/attach existing character if engine architecture permits.
- **Sources principales** :
  - https://gazetteers.maharashtra.gov.in/cultural.maharashtra.gov.in/english/gazetteer/WARDHA/his_marathas.html
  - https://gazetteers.maharashtra.gov.in/cultural.maharashtra.gov.in/english/gazetteer/Nagpur/his1.html

### Hyder Ali — GEN1776-129 / MYS / `cleanup2d3b_mys_land_2`

- **Verdict** : RETAIN_NAMED_HISTORICAL_GENERAL
- **Variantes** : Haidar Ali; Hyder Ali Khan; Ḥaydar ʿAlī
- **Naissance** : c.1722 — year_uncertain; early-life chronology explicitly uncertain
- **Lieu de naissance** : Budikote near Kolar (commonly attested; early-life details uncertain)
- **Polité de naissance** : Mysore/Deccan frontier polity; exact sovereignty at birth should not be overstated
- **State V3 de naissance** : STATE_MYSORE
- **Décès** : 1782-12-07 — exact_day_high_confidence
- **Rang/statut** : De facto ruler of Mysore and supreme military commander
- **Poste au 1776-01-01** : De facto sovereign and military head of Mysore
- **Début de fonction** : 1761 (year_for_effective_power)
- **Fin de fonction** : 1782-12-07 (death)
- **Armée/théâtre** : Mysore / Deccan; conflict with Maratha and Hyderabad forces; expanding state army
- **Culture historique** : Mysorean/Deccani Muslim; South Indian Persianate military milieu
- **Culture V3 recommandée** : deccani is present in mod and is preferable to blindly inheriting kannada; verify character-system token semantics — confiance MEDIUM-HIGH
- **Religion réelle** : Islam; Sunni attribution probable but not re-proven in priority-source pass
- **Religion V3** : sunni provisional — confiance MEDIUM
- **Origine sociale/caste** : Muslim military family; brother Shahbaz was a Mysore army officer
- **IG** : ig_armed_forces primary; ig_landowners/ruler secondary only if needed
- **Idéologie** : NONE
- **Traits documentés seulement** : Self-made military commander; energetic organizer; adapted disciplined drill/artillery and military technology. Avoid modern “reformer” ideology token unless separately justified.
- **Portrait / description** : Use established Hyder Ali portrait tradition; mature South Indian Muslim ruler/commander in Mysorean court-military dress. Do not use generic Kannada-Hindu DNA.
- **Présence mod / template / DNA** : Current 2D-4 direct character uses template=default; no explicit birth/culture/religion/DNA in formation file.
- **Erreurs 2D-4 probables** : Age procedural; if country default supplies Hindu religion it is wrong; culture may be oversimplified if inherited as Kannada; origin/DNA absent.
- **Confiance date de référence** : HIGH
- **Note de décision** : Retain. Culture/religion must be personal and explicitly pinned; do not let MYS country defaults determine them.
- **Sources principales** :
  - https://vishwakosh.marathi.gov.in/20182/

### Tipu Sultan — GEN1776-130 / MYS / `cleanup2d3b_mys_land_1`

- **Verdict** : ADD_NAMED_HISTORICAL_GENERAL
- **Variantes** : Tipu; Tipu Sultan; Fateh Ali Khan; Shah Bahadur Fateh Ali Khan
- **Naissance** : 1750-11-20 — exact_day_high_confidence
- **Lieu de naissance** : Devanahalli, near Bangalore
- **Polité de naissance** : Kingdom of Mysore
- **State V3 de naissance** : STATE_MYSORE
- **Décès** : 1799-05-04 — exact_day_high_confidence
- **Rang/statut** : Prince and experienced field commander under Hyder Ali
- **Poste au 1776-01-01** : Senior Mysore field commander; had already independently fought campaigns before accession
- **Début de fonction** : by 1767 (at_least_by_year; commanded cavalry/corps before 1776)
- **Fin de fonction** : 1782 (accession after Hyder death)
- **Armée/théâtre** : Mysore / Maratha frontier campaigns
- **Culture historique** : Mysorean/Deccani Muslim; Persianate court and military culture
- **Culture V3 recommandée** : deccani preferred over automatic kannada; verify token and personal semantics — confiance MEDIUM-HIGH
- **Religion réelle** : Islam; Sunni attribution probable
- **Religion V3** : sunni provisional — confiance MEDIUM
- **Origine sociale/caste** : Eldest son of Hyder Ali; Mysore ruling military household
- **IG** : ig_armed_forces
- **Idéologie** : NONE for 1776; do not project later state policies backward
- **Traits documentés seulement** : Militarily trained from youth; already independently commanded and fought Maratha forces before 1776.
- **Portrait / description** : Use authenticated Tipu portrait tradition only with age adjustment: he is 25 on reference date, not the older ruler depicted in many later portraits.
- **Présence mod / template / DNA** : Formation currently procedural; no Tipu character was found in the targeted branch name search performed for this audit, but country/event files should still be checked before implementation.
- **Erreurs 2D-4 probables** : Current general entirely procedural. Any older Tipu appearance would be anachronistic for age 25.
- **Confiance date de référence** : HIGH
- **Note de décision** : Strong second Mysore commander and preferable to a procedural general. Keep subordinate-to-Hyder framing for 1776.
- **Sources principales** :
  - https://vishwakosh.marathi.gov.in/17542/

### Eustachius Benedictus De Lannoy — GEN1776-140 / TRA / `TravancoreArmy`

- **Verdict** : RETAIN_NAMED_HISTORICAL_GENERAL
- **Variantes** : Eustachius De Lannoy; Eustachius Benedictus de Lannoy; Eustathius de Lannoy; De Lanoy
- **Naissance** : 1715 — year_high_confidence; exact day and birthplace disputed
- **Lieu de naissance** : Disputed: Belgium/Southern Netherlands in Ulloor tradition; Arras, Artois, Kingdom of France in Mark de Lannoy reconstruction
- **Polité de naissance** : DISPUTED — Southern Netherlands vs Kingdom of France (Arras)
- **State V3 de naissance** : UNRESOLVED_OUTSIDE_SOUTH_ASIA
- **Décès** : 1777-06-01 — exact_day_high_confidence_from_tomb/records
- **Rang/statut** : General / Commander-in-Chief of Travancore forces (dux generalis; European commander)
- **Poste au 1776-01-01** : Commander-in-Chief of Travancore army
- **Début de fonction** : 1761 (exact_year_high_confidence; succeeded Marthanda Pillai)
- **Fin de fonction** : 1777-06-01 (death)
- **Armée/théâtre** : Travancore; fortification system, army drill, Udayagiri and southern Kerala defenses
- **Culture historique** : Fleming / Southern Netherlandish European; not Malayali
- **Culture V3 recommandée** : flemish — confiance HIGH
- **Religion réelle** : Roman Catholic
- **Religion V3** : catholic — confiance HIGH
- **Origine sociale/caste** : European VOC-trained soldier in Travancore service; no Indian caste
- **IG** : ig_armed_forces
- **Idéologie** : NONE
- **Traits documentés seulement** : Military engineer/fortification expert; organizer of European-style discipline; long loyal service to Travancore.
- **Portrait / description** : No securely authenticated life portrait established. Best visual anchors are his Udayagiri tomb/epitaph and period Flemish/Dutch officer material; avoid modern AI portraits.
- **Présence mod / template / DNA** : Current 2D-4 direct character uses template=default; no culture/religion/birth/DNA pinned.
- **Erreurs 2D-4 probables** : SEVERE: default Travancore generation can wrongly make him Malayali and Hindu; age/DNA also procedural; birth origin missing. Must be Flemish/Southern Netherlandish and Roman Catholic.
- **Confiance date de référence** : VERY_HIGH
- **Note de décision** : One of the strongest matches in the entire region. The 1898 Madras Government compilation explicitly states he was a Fleming and C-in-C 1761–1777.
- **Sources principales** :
  - https://commons.wikimedia.org/wiki/File:The_Nayar_Brigade_of_Travancore._%28IA_nayarbrigadeoftr00madr%29.pdf
  - https://dutchinkerala.com/article15.php
  - https://dutchinkerala.com/1743.php

### Mirza Najaf Khan — GEN1776-142 / MUG / `MughalArmy`

- **Verdict** : RETAIN_NAMED_HISTORICAL_GENERAL
- **Variantes** : Mīrzā Najaf Khān; Mirza Nujuff Khan; Najaf Khan Zulfiqar al-Daulah
- **Naissance** : 1723 — year_high_confidence; exact day/location not secured
- **Lieu de naissance** : Iran/Persia; exact locality unresolved
- **Polité de naissance** : Iran under late Safavid/Afsharid transition; Safavid lineage
- **State V3 de naissance** : UNRESOLVED_OUTSIDE_SOUTH_ASIA
- **Décès** : 1782-04-26 — exact_day_high_confidence
- **Rang/statut** : Highest commander / commander-in-chief of Mughal army
- **Poste au 1776-01-01** : Highest commander of Shah Alam II’s Mughal army
- **Début de fonction** : 1772 (year_high_confidence)
- **Fin de fonction** : 1782-04-26 (death)
- **Armée/théâtre** : Delhi–Agra–Jat theatre; imperial Mughal field army
- **Culture historique** : Persian / Iranian
- **Culture V3 recommandée** : persian — confiance HIGH
- **Religion réelle** : Twelver Shia Islam
- **Religion V3** : shiite/shia token — verify exact mod token — confiance HIGH
- **Origine sociale/caste** : Safavid-lineage Persian military aristocrat/adventurer
- **IG** : ig_armed_forces primary; court elite secondary
- **Idéologie** : NONE
- **Traits documentés seulement** : Experienced imperial commander and military organizer; successful field commander. Avoid modern reformist ideology.
- **Portrait / description** : Excellent period visual anchor: Mughal Library identifies a portrait/image of Mirza Najaf Khan dated 31 Dec 1771; National Galleries of Scotland also holds an engraving after an original.
- **Présence mod / template / DNA** : Current 2D-4 direct character uses template=default; no birth/culture/religion/DNA pinned.
- **Erreurs 2D-4 probables** : SEVERE identity risk: a Mughal default may generate North Indian/Sunni identity, whereas Najaf Khan was Persian and Shia; age/origin/DNA are also uncontrolled.
- **Confiance date de référence** : VERY_HIGH
- **Note de décision** : Retain. Exact office is unusually well matched to 1 Jan 1776.
- **Sources principales** :
  - https://www.mughallibrary.com/images/2588/
  - https://www.nationalgalleries.org/art-and-artists/48876

## 4. Formations maintenues procédurales — justification

Le maintien procédural n'est pas un échec de recherche : il est parfois **plus historique** qu'un nom forcé.

- **GEN1776-119 — `PAN` — `FaujiAin`** : A second individual commander risks falsely centralizing the Sikh misls. Keep procedural/collective unless a formation-specific misl identity is added later.
- **GEN1776-123 — `HYD` — `sarf_e_khas`** : Do not force Ibrahim Beg into the 1 Jan 1776 slot: evidence brackets him around the date but does not securely prove the exact office on the reference day.
- **GEN1776-124 — `AWA` — `OudhRoyalArmy`** : Asaf-ud-Daula was the sovereign and bore military titles, but a ruler is not automatically an independent field general. No separate 1 Jan 1776 army commander was secured in priority-source research; Company brigades also complicated Awadh military autonomy.
- **GEN1776-131 — `COO` — `CoochBeharArmy`** : Dhairyendra/Dhairjendra Narayan had resumed rule in 1775, but the ruler is not automatically a field general. No separate commander securely tied to 1 Jan 1776 was found.
- **GEN1776-132 — `GAR` — `GarhwalArmy`** : Lalit Shah was ruler (1772–1780) and later campaigned against Kumaon, but the documented invasion falls after the reference date. Prempati Khanduri is associated with a later campaign, not securely with 1 Jan 1776.
- **GEN1776-133 — `SAT` — `SataraArmy`** : Ram Raja was Chhatrapati, but effective Peshwa supremacy makes an independent modern Satara standing-army commander questionable. An older military captain Bapuji Khanderao is documented earlier, not securely in office in 1776.
- **GEN1776-134 — `KHP` — `KolhapurArmy`** : 1776–78 conflict is documented, but no commander securely in office on 1 Jan 1776. Yasvantrao Sinde is documented leading military action in 1777 and is therefore post-reference.
- **GEN1776-135 — `KNO` — `KurnoolArmy`** : Munavvar Khan was Nawab in this period, but no separate independent army commander was securely identified for 1 Jan 1776. Do not turn the ruler into a general by default.
- **GEN1776-136 — `BHV` — `BhavnagarArmy`** : Wakhatsinhji Akherajji is a plausible military-ruler reserve candidate, but reference-date field command was not secured from priority-tier evidence. Keep procedural rather than overclaim.
- **GEN1776-137 — `PUD` — `PudukottaiArmy`** : Raya Raghunatha Tondaiman ruled 1769–1789 and later faced Hyder Ali, but no exact 1 Jan 1776 independent military command is documented here.
- **GEN1776-138 — `JEY` — `JeyporeArmy`** : Government Odisha material confirms Vikram Dev I ruled Jeypore 1758–1781, but no separate field commander for 1 Jan 1776 was secured. Do not assign the ruler solely because the formation exists.
- **GEN1776-139 — `COC` — `CochinArmy`** : Kerala Archaeology confirms a military-chief tradition (Sardar Mannadiyar / Kongad Nair commanders) but does not establish which individual held command on 1 Jan 1776. Existing 2D-4 note “pending structure rework” remains appropriate.
- **GEN1776-141 — `SIN` — `SindhArmy`** : Government of Sindh confirms Ghulam Nabi ruled 1775–1776 and died in battle, but exact succession chronology is unstable across secondary works and he should not automatically fill a general slot merely as ruler. Keep procedural pending a commander-specific source.

## 5. Cas méthodologiques à ne pas simplifier

### Sikh / Punjab

Jassa Singh Ahluwalia est un choix de premier ordre, mais le *Dal Khalsa* et les misls ne doivent pas être convertis en une armée nationale moderne. Les misls possédaient leurs chefs et contingents ; le commandement commun dépendait des assemblées et de la coopération confédérale. Pour cette raison, le deuxième poste PAN reste procédural/collectif.

### Marathes

En 1776, les forces marathes relèvent d'une **confédération de maisons et de clientèles militaires**, pas d'un état-major national unifié. Haripant sert la direction de Pune/Barbhai ; Tukoji commande les forces Holkar ; Mahadji dirige la puissance Shinde ; Mudhoji tient le complexe Bhonsle de Nagpur/Berar. Les tags et formations du mod sont des abstractions utiles, mais les biographies doivent conserver ces appartenances.

### Européens au service de polities indiennes

L'employeur ne définit jamais automatiquement l'identité du personnage :

- **Eustachius De Lannoy** : Fleming / Sud-Néerlandais, **catholique romain**, au service de Travancore ;
- **John Clavering**, **Robert Fletcher**, **James Stuart** : officiers britanniques de la BIC, pas cultures indiennes ;
- la culture et la religion doivent être renseignées au niveau du personnage, même si cela diverge de la population ou de la religion dominante du tag employeur.

### Hyder Ali et Tipu

Le mod contient le terme culturel `deccani` ailleurs dans son code. Pour ces deux personnages, une identité **mysorienne/deccani musulmane et persianisée** est historiquement plus défendable qu'une copie automatique de `kannada`. Le choix exact du token de personnage doit toutefois être vérifié dans les définitions de culture avant implémentation ; cette phase ne modifie rien.

## 6. Dates nécessitant une vigilance particulière

- **John Clavering** : 1722 est sûr comme année ; **31 août 1722 = baptême**, pas naissance démontrée.
- **Haripant Phadke** : la source gouvernementale dit explicitement que sa date de naissance est inconnue ; `?1729` seulement.
- **Tukoji Holkar** : le 26 juin 1723 circule largement, mais une même source secondaire affiche aussi 1725 ; ne pas présenter le jour comme incontestable sans vérification supplémentaire.
- **Mahadji Shinde** : la Marathi Vishwakosh donne `?1727`; il faut **rejeter l'exactitude artificielle** de dates populaires non réconciliées.
- **Hyder Ali** : l'année de naissance reste incertaine ; `c.1722` est préférable à un faux jour précis.
- **De Lannoy** : 1715 est solide, mais lieu et jour exacts sont disputés ; sa mort le 1 juin 1777 et son commandement sont bien mieux établis.
- **Mirza Najaf Khan** : année 1723 et décès 26 avril 1782 sont solides dans la source de portrait consultée ; localité de naissance iranienne non sécurisée.

## 7. Portraits et DNA — priorités

1. **Mirza Najaf Khan** : meilleure référence directe de cette phase — image identifiée et datée du 31 décembre 1771 dans la Mughal Library ; autre gravure dans les National Galleries of Scotland.
2. **Mahadji Shinde** : portrait à l'huile par James Wales / tradition de portrait tardive du XVIIIe siècle, exploitable comme référence visuelle.
3. **De Lannoy** : ne pas utiliser les portraits modernes/IA qui circulent ; son tombeau et l'épitaphe d'Udayagiri sont des références sûres, complétées par la description de Fleming et d'officier VOC/Travancore.
4. **Tipu** : les portraits les plus connus représentent un homme plus âgé ; au 1er janvier 1776 il a 25 ans.
5. Pour Haripant, Tukoji, Jassa et plusieurs autres, préférer une reconstruction historiquement sobre si aucun portrait de vie authentifié n'est disponible plutôt qu'un DNA pseudo-précis.

## 8. Recommandation finale par formation

**À conserver et compléter :** Jassa Singh Ahluwalia, John Clavering, Haripant Phadke, Tukoji Holkar, Mahadji Shinde, Hyder Ali, Eustachius De Lannoy, Mirza Najaf Khan.

**À ajouter :** Sir Robert Fletcher, James Stuart (d. 1793), Tipu Sultan. **Mudhoji Bhonsle** est également un très bon candidat pour Nagpur, sous réserve de vérifier qu'il n'existe pas déjà comme souverain réutilisable afin d'éviter un doublon de personnage.

**À laisser procéduraux :** PAN/FaujiAin, HYD, AWA, COO, GAR, SAT, KHP, KNO, BHV, PUD, JEY, COC, SIN, avec les motifs détaillés ci-dessus. (Le total procédural reste 13 parce que les quatre ajouts remplacent quatre procéduraux actuels.)

## 9. Bibliographie / sources de contrôle prioritaires

- *Encyclopaedia of Sikhism*, Punjabi University tradition : Jassa Singh Ahluwalia et structure des misls / Dal Khalsa.
- British Library, India Office Records and Private Papers : Sir Robert Fletcher ; dossiers Bengal Council/Clavering.
- Durham University Library, Clavering Manuscripts.
- *Dictionary of National Biography* : John Clavering ; James Stuart (d. 1793), avec attention au risque de confusion avec James Stuart (1741–1815).
- Marathi Vishwakosh, Maharashtra State : Haripant Phadke, Mahadji Shinde, Holkar house, Hyder Ali, Tipu Sultan.
- Maharashtra Gazetteers : Mudhoji Bhonsle / Nagpur / Wardha.
- Madras Government, *The Nayar Brigade of Travancore* (1898) : De Lannoy, Fleming, C-in-C 1761–1777.
- Ulloor S. Parameswara Iyer / Dutch in Kerala : De Lannoy, catholicisme, épitaphe et débat sur la naissance.
- Mughal Library et National Galleries of Scotland : Mirza Najaf Khan et références iconographiques.
- Government of Sindh, Directorate General of Antiquities : chronologie Ghulam Nabi Kalhoro.
- Government of Odisha / Nabarangpur : Vikram Dev I de Jeypore.
- Kerala Department of Archaeology : histoire de Cochin et tradition des chefs militaires.

## 10. Limites explicites de cette phase

- Aucun fichier gameplay n'a été modifié.
- Aucun template/DNA n'a été créé.
- Aucune idéologie n'a été attribuée par analogie moderne.
- Les `State V3` de naissance hors sous-continent n'ont pas été inventés : ils restent `UNRESOLVED_OUTSIDE_SOUTH_ASIA` quand la cartographie exacte n'a pas été auditée.
- Les cultures V3 proposées sont séparées de l'identité historique. Quand le token exact doit être vérifié, le CSV le dit explicitement.
- L'absence d'un nom dans une recherche GitHub n'est pas traitée comme une preuve absolue d'absence ; une implémentation ultérieure devra faire une vérification finale dans les fichiers de personnages/rulers/templates pour éviter les doublons.
