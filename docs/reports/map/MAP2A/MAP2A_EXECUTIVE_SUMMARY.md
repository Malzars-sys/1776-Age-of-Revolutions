# MAP-2A — Premier lot intégré localement

Date : 10 octobre 2026. Date du scénario : 1er janvier 1776.

## Résultat

**4 provinces corrigées, 4 State Regions concernées, 7 fichiers historiques modifiés dans ce lot.** Aucun nouveau TAG, aucune modification du bitmap, aucun commit, merge ou push.

- `x9AC196` : VEN → SWI en Lombardie. Représentation explicite des Trois Ligues associées à la Confédération, **pas** d'un canton suisse moderne. Les populations existantes sont conservées : 5 000 habitants passent du pool vénitien à SWI.
- `x71E080` et `xF0E080` : fin de la double attribution AUS/PRU ; AUS seul, dans la région physique `STATE_MORAVIA`, au titre de la Silésie autrichienne conservée après 1742.
- `x9061E0` : AUS conservé ; correction de `STATE_UPPER_SILESIA` vers la région physique `STATE_WEST_GALICIA`, pour Teschen. Ce nom de région du jeu ne signifie pas que Teschen appartenait historiquement à la Galicie.
- `x867A90` reste VEN : Bergame n'est pas ajouté à l'Autriche.

Les limites locales utilisent les provinces existantes et restent des **approximations de gameplay documentées**, autorisées par la nouvelle méthode. La précision cadastrale n'est ni revendiquée ni nécessaire. Voir le manifeste CSV pour les limites propres à chaque décision.

## Conservation

Population mondiale écrite : **835 804 980 → 835 804 980**. Conservation exacte par culture et religion, y compris la religion par défaut issue des définitions effectives des cultures.

Le pool autrichien de Silésie de 326 892 habitants est conservé : 191 139 rejoignent Moravie/Opava, 135 753 Teschen. Cette ventilation linguistique prudente n'est pas présentée comme un recensement historique.

Les 3 950 déclarations de bâtiments et leurs niveaux de propriété écrits sont conservés mondialement. Les deux niveaux textiles autrichiens et le niveau d'infrastructure régionale sont déplacés vers Teschen, avec leurs PM, réserves et propriétaires ; la déclaration textile de l'overlay suit le même déplacement. **Les répétitions base/overlay sont conservées, pas additionnées artificiellement.** Leur résultat effectif est à confirmer en jeu.

Les nombres d'unités, les formations, commandants et quartiers généraux sont conservés. Un seul sélecteur de recrutement change : le conscrit autrichien précédemment placé dans un État autrichien de Haute-Silésie invalide est rattaché à Teschen. Aucune unité permanente supplémentaire n'est créée ou retirée.

## Collaborateur et développements préservés

Le sommet distant vérifié de `georg3mx-map-rework` est `0e018d9b292ec263d424500a47279d895cf1020a`. Les deux commits absents de main sont `3126bac` et `0e018d9` ; les anciens changements `d909641` / `d5b7421` sont déjà intégrés. Pas de fusion globale.

Les propositions nouvelles de population luxembourgeoise et d'Autriche sur Bormio ne sont pas reprises : la première perdait 37 881 habitants par rapport à la décision approuvée, la seconde ne correspondait pas aux Trois Ligues. Le Luxembourg déjà intégré demeure intégralement BEO : 137 881 anciens habitants de LUX, mêmes cultures/religions, administrations, 3 permanents et général, BEO terre de la Couronne autrichienne.

Dans la **copie candidate seulement**, les cinq tokens des deux commandes Git accidentelles en Bessarabie sont retirés et le doublon AUS/VEN de `x867A90` est supprimé en gardant VEN. Aucun changement de souveraineté moldave pour corriger la syntaxe. L'index et la fusion en attente n'ont pas été finalisés ; cette copie reste impropre à une fusion globale tant que ses autres anciennes divergences subsistent.

Dobroudja, Bessarabie, Suisse orientale, Grand Caucase, Istrie, Tyrol du Sud et Nunavut ne sont pas réécrits. Les sélecteurs de population, bâtiments et recrutement des partages Istrie/Tyrol sont structurellement valides ; leur précision historique reste provisoire, particulièrement la frontière du Trentin. Leurs populations spécifiques, comme celles de Gênes et de Venise ailleurs, sont inchangées. Le Nunavut reste dans son état d'incorporation existant ; pas de redistribution coloniale générale.

Tous les anciens fichiers hors des 7 historiques nécessaires sont vérifiés par empreintes, dont les travaux MAP-1C, les journaux ottomans, l'économie, les technologies, assets et le correctif IA. Les scripts nouveaux MAP-2A sont exclus de cette protection d'anciens travaux.

## Tests

- Validateur Luxembourg strict exécuté **avant** le lot : PASS. Mode ciblé Luxembourg **après** le lot : PASS. Le mode strict original reste disponible ; il refuse intentionnellement les changements d'autres frontières et n'est donc pas utilisé comme validateur mondial après MAP-2A.
- Validateur spécifique `tools/validate_map2a.py` : PASS, avec comparaison au workspace réellement modifié avant intervention, pas à HEAD.
- 40 717 RGB attribués avant/après ; doublons effectifs : **64 → 62**. Les deux doubles attributions silésiennes sont éliminées. Cinq références province/région incorrectes sont corrigées. Aucun nouveau avertissement de région ou sélecteur orphelin détecté dans la portée statique contrôlée.
- Tests existants de l'IA : 10 scénarios réussis.
- Tests ottomans : 1 024 combinaisons administratives, 192 combinaisons politiques, indépendance des journaux, événements d'introduction, échéance, consolidation, réductions administratives et bâtiments égyptiens : réussis.
- 62 doublons préexistants et 14 avertissements statiques distincts restent hors lot. Ils sont détaillés dans la validation, **pas masqués ni assimilés à des régressions**. Les avertissements de propriétaires économiques sont des problèmes potentiels de résolution de scopes, pas des disparitions constatées dans le moteur.

**Tests natifs de chargement et d'évolution sur un mois NON effectués.** Le contrôle natif du jeu n'est pas disponible dans cette session. Les tests ci-dessus n'exécutent pas le moteur et ne garantissent pas son interprétation des historiques superposés.

## Validation demandée au joueur

1. Relancer Victoria 3 avec ce dossier de travail actif et créer une **nouvelle partie** au 1er janvier 1776, sans recharger une ancienne sauvegarde.
2. Vérifier BEO/Luxembourg et l'absence de Luxembourg indépendant ; comparer le général et les 3 unités transférées.
3. Vérifier le petit territoire SWI au nord de la Lombardie, Bergame VEN, les districts autrichiens de Moravie et Teschen autrichien dans la région du jeu Galicie occidentale.
4. À Teschen, vérifier les deux niveaux textiles, le niveau d'infrastructure et le conscrit autrichien ; vérifier les effectifs PRU inchangés et les PM conservés. Ne pas interpréter les deux déclarations textiles base/overlay comme quatre niveaux attendus.
5. Laisser tourner jusqu'au 1er février ; contrôler emplois, accès au marché, absence de disparition de formations et les journaux ottomans. Examiner les logs pour les provinces/regions/scopes de ce lot en distinguant les avertissements anciens.

Les prochains lots attendent cette validation. Voir `MAP2A_NEXT_REGIONS.md` pour l'ordre proposé et `MAP2A_UNRESOLVED.csv` pour les reports.
