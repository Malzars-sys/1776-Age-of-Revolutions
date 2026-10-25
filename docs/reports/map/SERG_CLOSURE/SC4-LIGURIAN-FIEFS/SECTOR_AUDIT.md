# Audit régional et décision bornée

Date historique : **1er janvier 1776**. SC4-LIGURIAN-FIEFS reste **BLOCKED P0** pour la représentation territoriale et juridique des fiefs. Une correction technique indépendante, LF-GEN-ADM-PM, est installable. La matrice CSV distingue les souverainetés et les différents droits : ni titre nobiliaire, ni résidence génoise, ni mariage dynastique ne crée automatiquement un pays ou une annexion.

## État natif

GEN existe : capitale moteur STATE_PIEDMONT, culture north_italian, république présidentielle avec loi de république marchande, doge Brixio Giustiniani déjà présent. Le rang moteur « kingdom » de la définition n'en fait pas une monarchie. Les lois sont résolues après l'effet réactionnaire et ses dérogations directes ; la loi marchande est une définition INJECT_OR_CREATE valide. Aucun changement de gouvernement, capitale, dirigeant, technologie, relation ou unité proposé.

| Carte native | RGB GEN | Région / propriétaire | Cellules avant → après | Voisins terrestres directs hors GEN |
|---|---|---|---|---|
| 1, ouest | x54728A | STATE_PIEDMONT / GEN | 94 → 94 | SAR x5080E0 (Nice), xD080E0 |
| 2, centre-ouest | x5F6BAA | STATE_PIEDMONT / GEN | 96 → 96 | SAR x11C061, xD080E0 |
| 3, centre-est | x904061 | STATE_PIEDMONT / GEN | 138 → 138 | SAR xACB500 ; PAR x0B3B43/x700120 ; MOD xF08021 |

Ces orientations décrivent le bitmap ; elles n'identifient pas cadastralement un fief. Total GEN **3 RGB, 328 cellules, 510000 habitants**, conservés. Les trois groupes initiaux sont 403601 north_italian, 103317 french, 3082 north_italian/jewish ; ce sont les données du mod, aucun recensement certifié de 1776. Les 17 déclarations de bâtiments restent toutes présentes. Une administration publique GEN de niveau 1 existe déjà, avec papier, port, administrations navales, commerces et chantiers navals préexistants : aucun niveau supplémentaire n'est nécessaire.

L'inventaire JSON comprend les interfaces Piémont, Lombardie, Émilie, Toscane, Provence, les voisins et leurs arêtes, les unités et définitions. Le CSV couvre aussi ce contexte conservé. Ses lignes AUS/MOD/PAR/TUS/SAR n'élargissent pas la mission à ces pays. INITIAL_CONTEXT.json relève lois/technologies et références diplomatiques effectives : aucun sujet ou pacte GEN explicite repéré dans les fichiers de diplomatie/traités ; GEN absent du bloc/trigger impérial et du registre. Absence dans ces scripts ≠ preuve historique de non-impérialité de tous ses domaines.

## Conclusions historiques

Les notices AS Genova/SIAS attestent des curies Fieschi, des juridictions Spinola et des domaines Doria distincts du territoire direct de la République. Campo présente des droits partagés avec Gênes ; Masone relève du domaine direct avec droits usufructuaires privés. Les cessions et partages successifs empêchent toute attribution en bloc aux trois familles. Les localités orientales et les anciennes possessions des Langhe/Montferrat exigent la même distinction entre terre, investiture et biens allodiaux. Les sources et dates précises figurent dans SOURCES.md et JURISDICTION_MATRIX.csv.

**Torriglia** mérite l'étude d'une représentation politique propre : principauté attestée avant 1776, administration territoriale distincte, ensemble supérieur à une simple propriété privée. Hypothèse B concrète : un ensemble Doria limité à Torriglia/Santo Stefano et aux domaines contemporains effectivement rattachés, avec liens impériaux bornés. Il ne doit absorber ni les fiefs Pallavicini, ni les autres branches Spinola/Fieschi, ni les possessions romaines de la maison. Il manque encore la correspondance de ses vallées au bitmap et une répartition de population fondée. Le RGB GEN x904061 comprend aussi le noyau côtier et touche PAR/MOD ; le transférer entier retirerait beaucoup plus qu'une principauté intérieure. Les franges SAR xACB500/x11C061 et PAR x0B3B43/x700120 sont des **zones de confrontation à étudier**, pas des cellules autorisées à transférer. Les 9 RGB impériaux piémontais déjà approuvés sont protégés.

**Noli** est un cas de souveraineté communale distincte sous protection génoise, à ne pas effacer par assimilation du protectorat à l'annexion. Un TAG pourrait être examiné si une découpe côtière suffisamment étayée et des données de population sont obtenues. Les RGB GEN occidentaux agrègent une Riviera beaucoup plus vaste ; aucune sélection exclusive de Noli n'est démontrée. Sa qualification impériale ne découle pas du seul mot « république ». Ce contrôle voisin ne commence pas une deuxième tâche.

**Approximation B envisageable** pour les petites curies : représentation juridique regroupée par ensemble de droits réellement communs, sans un pays par village, et sans restitution de toute la République à un prince. Il faut un jeu borné de cellules et un traitement explicite des droits de GEN/SAR et des seigneurs. Cette proposition de méthode n'est ni une conservation définitive approuvée ni une installation de nouveaux droits. Un arbitrage utilisateur explicite pourrait fixer une approximation si les documents ne permettent pas une découpe défendable. Aucun ancien recalage improductif relancé.

## Sous-lot indépendant LF-GEN-ADM-PM

Le bâtiment administratif public GEN active les cabinets horizontaux, dont la technologie obligatoire n'est pas recherchée par GEN au départ. **centralization n'est pas le prérequis effectif de cette méthode dans le mod.** Correction minimale : sélectionner pm_simple_organization, sans prérequis technologique, dans le même groupe ; conserver les méthodes religieuse et héréditaire, niveau, réserves et propriété. Aucune technologie tardive ajoutée, aucune administration artificielle créée. Les offices républicains attestés restent représentés par le bâtiment existant ; la correction assure la cohérence de sa configuration initiale, sans prétendre mesurer le budget génois de 1776.

Effet prévu par les définitions à effectif complet : contribution de la méthode de base de 50 à 10 de bureaucratie, de 10 à 2 de capacité fiscale, suppression de sa consommation de 10 de papier ; emploi écrit de 500 commis conservé. Les autres méthodes peuvent ajouter leurs propres effets. Il s'agit d'effets théoriques des scripts, aucun résultat moteur mesuré. Vérifier la viabilité locale en jeu ; ne pas promettre un solde budgétaire donné.

Un seul token sera substitué dans le fichier **courant** `common/history/buildings/01_south_europe.txt`. BUILDINGS_BEFORE.txt conserve ce préimage ; les gardes exigent qu'il corresponde à la session et empêchent une réapplication. Tous les autres octets, notamment la correction maritime de Ljubljana, le port AUS d'Istrie et le chantier naval litigieux, sont conservés. Les identités des bâtiments mondiaux doivent montrer exactement une méthode modifiée et aucun changement de niveau.

## Blocage résiduel et limites de clôture

P0 : omission/représentation des juridictions autonomes et qualification des droits GEN/SAR/Doria/Spinola/Fieschi/Pallavicini ; géographie des ensembles et traduction du droit impérial non homologuées. Prochaine reprise du dossier : confronter les pièces datées et les vallées aux trois agrégats côtiers et aux voisins, puis choisir une solution B commune, avec population sourcée ou arbitrage explicite. La carte de 1750 aide à situer les ensembles mais ne résout pas leurs changements ultérieurs. Aucune frontière de 1797/1815 employée.

Les **574 droits et neuf électeurs restent inchangés**, ainsi que la limitation SAR aux neuf RGB piémontais. Aucun nouveau TAG, sujet, bloc, droit de restitution ou déclencheur impérial. L'absence de correction territoriale ne reçoit aucune approbation définitive. La réussite future de LF-GEN-ADM-PM ne pourra clôturer ce blocage. Innviertel, Hohenberg/Fricktal/chantier naval, droits italiens, droits Savoie–Nice et Teschen restent ouverts à l'identique.
