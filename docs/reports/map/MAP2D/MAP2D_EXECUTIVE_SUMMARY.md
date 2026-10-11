# MAP-2D — Mer Noire au 1er janvier 1776

## Résultat intégré localement

**28 provinces existantes réattribuées, aucune province redessinée, aucun nouveau RGB.** Pays concernés : Moldavie (`MOL`), Empire ottoman (`TUR`), khanat de Crimée (`CRI`) et Russie (`RUS`). Les transferts aboutissent à 21 provinces russes, 6 ottomanes et 1 tatare supplémentaire. Ce sont des approximations documentées à l'échelle du jeu, non des délimitations cadastrales certifiées.

Le bitmap reste identique, octet par octet, à l'instantané initial : Avignon, Comtat Venaissin et Frioul sont préservés. MAP-2A/B/C, Luxembourg/BEO, les noms vénitiens, le transit France → États pontificaux, les journaux ottomans, les sujets danubiens, les révisions démographiques et les correctifs IA antérieurs ne sont pas modifiés.

**Aucun commit, merge ou push. Aucun lot suivant commencé.** Validation statique : `PASS_STATIC`. Chargement et observations en jeu : **non réalisés** durant ce lot.

## Territoires

| Région du jeu | Modification | Conservé / limite |
|---|---|---|
| Bessarabie | MOL → TUR : `x1E1DEF`, `x23621B`, `x6BF7B8`, `xB0E0A0`. MOL → CRI : `x5F2259`. | Neuf RGB restent moldaves. Les quatre districts fortifiés représentent Bender, Akkerman, Kilia/Izmaïl et leur côte ; le RGB intérieur représente l'autonomie tatare du Budjak. |
| Cherson | CRI → RUS : 19 RGB des secteurs entre Bug et Dniepr et des possessions septentrionales antérieures à 1776. CRI → TUR : `x716121`, `xB02161`. | Quatorze RGB restent tatars ; les deux districts côtiers ottomans représentent Hadjibey et Ochakiv. Pas d'attribution automatique de tout l'Yedisan à la Russie. |
| Crimée | CRI → RUS : `x706060`, secteur Kerch / Yeni-Kale. | Les huit autres RGB de la péninsule restent au khanat. Le RGB oriental est plus vaste que le district fortifié exact. Aucune annexion de 1783. |
| Tauride | CRI → RUS : `x8A09FD`, district de Kinburn. | Les 26 autres RGB restent au khanat. Le fort et son arrière-pays sont représentés par une province entière. |

Le traité de Küçük Kaynarca distingue l'indépendance tatare, les exceptions ottomanes et les acquisitions russes. Ses articles 3, 16, 18–20 et 24 fondent la distinction retenue pour les forteresses et districts de 1774 ; ils ne justifient pas les frontières ultérieures de la Bessarabie. [Transcription du traité de 1774](https://www.vostlit.info/Texts/Dokumenty/Turk/XVIII/1760-1780/Traktat_Kucuk_Karnaji_1774/text.phtml).

Les possessions russes septentrionales ne se limitent pas aux concessions de 1774 : les implantations de Nouvelle-Serbie et les frontières cosaques antérieures sont également prises en compte. [Étude documentaire du Musée historique national de Dnipro](https://www.museum.dp.ua/uk/cossacksborder/).

Azov est déjà russe : aucun transfert forcé. Bucovine habsbourgeoise, Dobroudja ottomane, Valachie et Moldavie à l'ouest du Prut sont conservées. La Moldavie demeure une principauté distincte dans la dépendance ottomane existante.

### Limite importante : Hotin

**Hotin/Khotyn n'est pas corrigé dans ce lot.** Le RGB septentrional `x79D62E` comprend également Bălți et un vaste territoire moldave. Le transférer entièrement aux Ottomans créerait une erreur disproportionnée. Une subdivision locale reste nécessaire pour représenter sa raya ; cette incertitude n'est pas présentée comme résolue.

### Méthode et travaux réutilisés

Réutilisation des recommandations régionales R2/R3 et des dossiers MAP-0/MAP-1. Confrontation ciblée des RGB aux côtes, cours du Bug/Dniepr, géométries existantes et locators physiques. Pas de nouvelle recherche mondiale ni de géoréférencement artificiellement précis.

Comparaison en lecture seule avec `georg3mx-map-rework` : les définitions de propriétaires des huit State Regions étudiées correspondent à celles de la baseline locale. Aucun changement supplémentaire pertinent n'a donc été copié depuis cette branche, et aucune fusion globale n'a été effectuée. Les choix déjà valables sont conservés. Aucun token de commande Git réintroduit.

Deux références de hubs ont été alignées sur leurs **locators physiques déjà existants**, sans déplacer ceux-ci : mine de Bessarabie `x1E1DEF` → `x79D62E`, ville de Cherson `xB02161` → `xFDD2CF`. Les ressources, superficies et autres subdivisions restent inchangées.

Les aperçus `bessarabia_before.png` / `bessarabia_after.png` et `black_sea_before.png` / `black_sea_after.png` montrent les propriétaires avant/après. Ce ne sont pas des captures du moteur du jeu. Aucun comparatif de pixels modifiés n'est nécessaire puisque le bitmap n'a pas changé.

## Population et économie

Population mondiale : **835 804 980 avant et après ; différence 0**. Les totaux de chaque State Region, les cultures, religions et attributs des populations — y compris le statut esclave — sont conservés.

| Région / propriétaire territorial | Avant | Après |
|---|---:|---:|
| Bessarabie / MOL | 483 726 | 326 587 |
| Bessarabie / TUR | 0 | 107 570 |
| Bessarabie / CRI | 0 | 49 569 |
| Cherson / CRI | 864 680 | 323 672 |
| Cherson / RUS | 0 | 481 180 |
| Cherson / TUR | 0 | 59 828 |
| Crimée / CRI | 241 221 | 208 604 |
| Crimée / RUS | 0 | 32 617 |
| Tauride / CRI | 1 171 439 | 1 122 179 |
| Tauride / RUS | 0 | 49 260 |

Les pools démographiques préexistants sont répartis, groupe par groupe, selon la part de surface terrestre des RGB transférés. Les arrondis restent dans la subdivision d'origine. **C'est une redistribution technique, pas une estimation historique de recensement**, ni une migration ou un ajout destiné à remplir des emplois. Les compositions héritées éventuellement anachroniques n'ont pas été réinventées dans ce lot.

Quatre déclarations agricoles de niveau 1 ont changé de subdivision territoriale : élevage en Bessarabie vers TUR, ferme de blé vers CRI ; élevage et ferme de blé en Cherson vers RUS. Leurs niveaux, PM, réserves et propriétaires économiques existants sont conservés à l'identique, y compris lorsqu'ils deviennent propriétaires étrangers. Les détenteurs restent référencés dans des subdivisions conservées.

Tous les autres bâtiments, ports et administrations sont conservés. Aucune route, caserne ou administration créée. Les formations, types, effectifs et références de recrutement sont inchangés et restent valides. Aucun changement de général ou d'unité permanente. L'emploi, le placement des propriétaires générés, les budgets et l'accès au marché des nouvelles subdivisions doivent encore être observés en jeu ; aucun accès à 100 % n'est promis.

## Diplomatie russe demandée en complément

### Crimée

Le khanat reste territorialement distinct au départ. L'IA russe reçoit, avant le 1er janvier 1783, une fréquence d'évaluation et une priorité très élevées pour l'action native de mise en dépendance du membre de son bloc : chance d'évaluation 1, score de proposition 1 000. L'exemption de délai RUS → CRI déjà présente est préservée.

Les conditions et effets natifs ne sont pas contournés : cohésion minimale, prestige relatif, paix et éligibilité restent nécessaires. La Russie reconnue crée un **protectorat**, pas une annexion. Le changement n'impose donc pas une date certaine. L'influence russe sur un khanat formellement indépendant est documentée ; le protectorat est une abstraction de gameplay. [Étude historique de Nihat Çelik](https://journalofislamiclaw.com/current/article/view/celik).

### Pologne-Lituanie

Ajout d'un traité avec deux articles : engagement polonais sur la loi déjà active `law_oligarchy`, au bénéfice russe ; garantie d'indépendance de PLC par RUS. C'est une abstraction de la garantie des lois cardinales de 1768, pas une nouvelle loi, une sujétion ou un partage territorial. [Traité russo-polonais de 1768, articles II et IV](https://pl.wikisource.org/wiki/Traktat_wieczystej_przyja%C5%BAni_pomi%C4%99dzy_Rosj%C4%85_a_Rzecz%C4%85pospolit%C4%85_(1768)).

Date d'entrée en vigueur : 24 février 1768 ; engagement de vingt ans. Les coûts natifs sont conservés : 25 + 50 = **75 d'influence russe**, pas une dépense budgétaire en livres. Les localisations françaises et anglaises sont ajoutées.

Le jeu utilise le score d'acceptation de l'invitation au bloc pour l'évaluation d'une sortie volontaire de l'IA ; son seuil natif est −100. Un bonus ciblé +150, avec plancher −75, s'applique à PLC dans le bloc russe, avant le 24 février 1788, tant que l'oligarchie et la garantie russe existent, que les relations ne sont pas mauvaises et qu'aucun conflit diplomatique mutuel n'est en cours. Les autres pays gardent leur comportement natif. Le joueur n'est pas empêché de sortir ; aucune réintégration forcée n'est ajoutée. La sortie polonaise après trois mois n'est pas encore testée dans le moteur.

## Validation et limites connues

- Instantané vérifiable : `MAP2D_BASELINE.json`, empreintes de 1 971 fichiers protégés, textes historiques et bitmap initial conservés. Le patch final `MAP2D_FINAL.patch` et `PATCH_MANIFEST.json` documentent les dix fichiers de jeu concernés. `INTEGRATION.patch` est un artefact intermédiaire, non le patch final.
- Les six fichiers préexistants modifiés et quatre nouveaux fichiers sont dans le périmètre autorisé. Aucun autre fichier protégé ne dérive de la baseline.
- 28 changements de propriétaires exactement ; univers des provinces conservé ; aucun nouveau doublon, aucune province perdue, aucune nouvelle référence orpheline.
- Les **62 doubles attributions préexistantes** restent 62. Celle de `xBCF376` au Kouban reste non arbitrée. Les défauts de référence historiques passent de 14 à 13 : le secteur russe de Crimée rend valide le propriétaire russe d'une exploitation de tabac déjà présente.
- Conservation indépendante des populations, attributs, bâtiments, niveaux, PM, réserves, propriétaires économiques et formations militaires.
- Parse structurel, identifiants natifs utilisés, sens des deux articles, loi polonaise existante et encodage des localisations contrôlés. Les possibilités et effets des actions diplomatiques natives sont préservés.
- Tests de modèles ottomans existants : 1 024 combinaisons administratives, 192 combinaisons politiques, introduction des deux journaux, idempotence, douze mois de consolidation et échéance 1836 : **PASS**.
- Dix scénarios existants de pénurie d'infrastructure : **PASS**. Les anciens contrôles figés sur des instantanés antérieurs ne sont pas utilisés pour rejeter les changements autorisés de MAP-2D ; les empreintes de la baseline actuelle assurent la protection des travaux précédents.
- Les trois CSV sont recalculés, contrôlés cellule par cellule et vérifiés visuellement ; les colonnes de variation démographique sont dérivées des nombres avant/après. Cette mise en forme n'affecte pas les données du jeu.
- Le contrôle Git de whitespace signale aussi des espaces de fin de ligne dans le checkout déjà modifié. Les nouveaux motifs introduits dans les lignes du lot ont été nettoyés ; les diagnostics restants sont documentés dans `QA/CSV_VALIDATION.json`, sans reformatage global des fichiers hérités. Ce contrôle de présentation n'est pas un test de chargement.

Les contrôles statiques et les modèles ne remplacent **ni un test de chargement natif, ni une observation de recrutement ou de diplomatie**. Les noms de certains hubs vanilla, issus de fondations/renommages ultérieurs, restent un problème préexistant reporté. Aucun système de connexion intérieure des enclaves n'a été développé.

## À inspecter dans une nouvelle partie

1. Bender, Akkerman, Kilia/Izmaïl : districts ottomans ; cœur moldave conservé ; zone tatare intérieure du Budjak.
2. Kerch / Yeni-Kale russes, reste de la péninsule au khanat ; Kinburn russe sans annexion générale de la Tauride.
3. Répartition de Cherson : Russie à l'est/nord, Ochakiv et district côtier ottomans, Yedisan tatare conservé. Bucovine et Dobroudja inchangées.
4. Panneaux de populations, propriétaires agricoles, administrations, recrutement, infrastructures et marchés au premier jour puis après un mois.
5. En observateur, disponibilité du bouton natif russe pour la Crimée et éventuelle proposition de protectorat ; cohésion/prestige si l'action reste bloquée.
6. Traité RUS–PLC, sens des articles, coût d'influence et présence polonaise dans le bloc après **au moins trois mois**.
7. Contrôle rapide d'Avignon/Frioul et des deux journaux ottomans pour confirmer la protection statique dans le moteur.

Les détails RGB et géométriques figurent dans `MAP2D_TERRITORIAL_CHANGES.csv`, les redistributions dans `MAP2D_POPULATION_VALIDATION.csv`, les limites dans `MAP2D_UNRESOLVED.csv`, et les résultats des contrôles dans `MAP2D_VALIDATION.json`.
