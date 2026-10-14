# MAP-1 — Barrières avant MAP-2

**MAP-2 non autorisé. Aucun transfert admissible à cette passe.**

## Contrôles réalisés

- 36 originaux identiques au manifeste SHA-256, 58 fichiers d'archive ingérés.
- 1 005 Change_ID et 374 Source_ID uniques; 1 043 couples de couverture uniques.
- 9 régions, aucun double comptage R8, références sources existantes, date cible 1776-01-01.
- Bitmap installé Victoria 3 1.13.11 : 8192 × 3616, 40 875 RGB, hash MAP-0 inchangé.
- Les 40 928 lignes d'attribution restent distinctes, doublons inclus.
- Index pixel, tailles, boîtes, ancres et raccordement wrap_x contrôlés contre le bitmap.
- Les attributions et State Regions du checkout concordent avec la baseline MAP-0.
- 20 aperçus P0, 280 vues techniques d'États et 410 fiches de recherche produites.
- 80 pistes de transfert auditées, 85 États inventoriés, 748 enregistrements de pops et 487 commandes de création de bâtiments consignés.
- 1 900 fichiers runtime identiques aux SHA-256 du début de MAP-1. HEAD inchangé.

Voir les comptes exacts dans [MAP1_VALIDATION.json](MAP1_VALIDATION.json) et
[MAP1_DEPENDENCY_VALIDATION.json](MAP1_DEPENDENCY_VALIDATION.json).
La quantité de fiches produites ne mesure pas le nombre de frontières validées.

## 1. Preuve historique et géographique

Chaque proposition doit comporter autorité, contrôle effectif, autonomie et compromis
gameplay séparés; source applicable au 1er janvier; auteur/date/page/feuille; biais;
polygones RGB exacts lisibles; justification du choix et des portions exclues.

Pour une carte ancienne : identifier les points d'ancrage indépendants, expliciter
la transformation et la projection si connue, conserver des points de contrôle
hors ajustement, mesurer les erreurs et la distorsion locale. Trois points non
alignés permettent un ajustement affine mais ne suffisent pas à le valider.
Ne pas inventer de GPS à partir du bitmap. Un toponyme du jeu est un indice,
pas la preuve d'une juridiction. Une notice bibliographique n'est pas une carte lue.

Les sources tardives doivent démontrer la rétrolecture, sans reporter les conquêtes
de 1777/1783, cédules de 1802, frontières de 1836 ou cessions de 1858/1860 au départ.
Les 150 dossiers interrégionaux requièrent confrontation explicite; les 15 DISPUTED
ne peuvent être arbitrés silencieusement.

## 2. Unicité et références techniques

Pour les territoires modifiables, exiger exactement une State Region et une
attribution propriétaire par province terrestre possédable. Traiter séparément
les exceptions documentées, impassables, mers et lacs. Ne pas effacer un doublon
simplement en gardant la première occurrence. Les 59 BLOCKER signalés dans main
par MAP-0 restent des problèmes préexistants ouverts, pas des corrections MAP-1.

Contrôler TAG existant, pays initial actif, capitales, hubs, ports, naval exits,
adjacences, IDs numériques, locators et localisations. Les 375 divergences entre
hub déclaré et échantillon locator vanilla sont des **alertes**, pas 375 erreurs
historiques certifiées : limites pixel/arrondis et adaptations peuvent intervenir.

## 3. Conservation exacte

Avant/après par couple State_ID/TAG et dans le monde : populations par culture,
religion et attributs; bâtiments, niveaux, PM, réserves, propriétaires économiques,
propriétés étrangères/compagnies; formations et recrutement. Conserver les commandes
écrites et leurs scopes, puis vérifier les résultats moteur. Ne pas interpréter
une somme de niveaux de propriété écrits comme une somme effective garantie.

Auditer également souveraineté, sujets, pactes, transit, traités, journaux, décisions
et événements. Les changements économiques/politiques non nécessaires au transfert
restent hors lot. LUX nécessite une décision explicite de maintien/disparition et
la conservation de ses 137 881 habitants; GEN/VEN gardent leurs historiques particuliers.

## 4. Choix A/B/C

- A : réaffectation de polygones existants si l'approximation est documentée et acceptable.
- B : scission/recomposition des State Regions lorsque les scopes administratifs l'exigent. B ne réduit pas un polygone indivisible.
- C : nouveau dessin raster uniquement après démonstration qu'A/B ne peuvent représenter convenablement la zone, avec autorisation spécifique.

Aucune nécessité de C n'est établie par cette passe. Ne pas classer automatiquement
une enclave comme éditable au pixel ou importer toutes les limites modernes.

## 5. Validation moteur, après autorisation distincte

Dans une copie isolée approuvée, démarrer une nouvelle partie au 1er janvier 1776
sous Victoria 3 1.13.11. Contrôler logs complets, propriétaires de chaque RGB changé,
territoires fractionnés, pays/capitales, populations, emploi et niveaux effectifs,
PM, accès marché, recrutement et navigation. Comparer immédiatement puis après
un mois. Retester les journaux ottomans, blocs diplomatiques, sujets, économie
de départ, infrastructures et précédents correctifs sans les réécrire.

Aucun test en jeu ni simulation de budget n'a été exécuté pour MAP-1. L'identité
des fichiers prouve l'absence d'écriture runtime, pas la disparition des défauts
déjà présents dans la version de départ.

## 6. Autorisation et publication

Les champs Apply_To_Mod et Approved_By_User restent NO. Examiner le lot historique,
les exceptions et les inventaires avant accord MAP-2. Définir ensuite les fichiers
autorisés, la sauvegarde de travail et les tests. Merge et push nécessitent encore
leur autorisation propre; aucune commande d'application n'est livrée ici.
