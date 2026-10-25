# Piombino et Elbe — audit du 1er janvier 1776

## Réponse sur la présence d'Elbe

**Oui, Elbe est présente dans le bitmap politique natif.** Elle forme une composante terrestre de **54 cellules**, entourée d'eau, dans les limites x=4325–4335, y=1060–1068. Elle n'est pas une province indépendante : le même RGB **x6A7662** couvre aussi **165 cellules continentales**. Les 219 cellules appartiennent à **TUS / STATE_TUSCANY** et sont actuellement liées à un même droit impérial TUS. L'image ELBA_DETAIL.png distingue visuellement les deux composantes sans proposer de nouveaux propriétaires. Il ne faut ni ajouter une île déjà présente ni transférer toute la province sous prétexte de corriger l'île.

Les six RGB toscans totalisent 1321 cellules : x32BA1A=135, x6A7662=219, x7080A0=90, xB04020=276, xF12431=205, xFAFCD4=396. Les voisins, composantes connexes et limites sont inventoriés ; aucun de ces agrégats n'est reconnu comme le territoire exclusif de Piombino sur la seule position de sa ville.

## Pays et données actuels

Le TAG PIO n'existe pas dans les définitions effectives. TUS existe, capitale STATE_TUSCANY, gouvernement monarchique de Pierre-Léopold ; SIC existe, capitale STATE_CAMPANIA, royaume méridional. Les personnages et leurs scripts restent inchangés. L'absence d'un TAG Piombino n'est donc pas une simple erreur de nom ou de souverain à corriger dans TUS : il faut distinguer un pays princier et conserver la Toscane.

Population TUS : **1273269**, dont 1267811 north_italian à religion par défaut et 5458 north_italian/jewish. Les pops sont affectées à la subdivision TUS entière, sans enregistrement séparé pour les 54 cellules d'Elbe, Portoferraio, Longone ou Piombino. Population SIC mondiale : 4200365 ; aucune subdivision SIC en Toscane n'est installée. Ni partage par surface ni multiplication par 54/1321 ne constitue une population historique de l'île.

TUS possède **10 déclarations de bâtiments**, dont ses deux niveaux administratifs préexistants ; ces chiffres sont des déclarations/niveaux du mod, pas le nombre d'établissements historiques. Leurs signatures, propriété et méthodes, ainsi que les unités, sont conservées. Les lois/technologies et les références de personnages, diplomatie et bloc sont consignées dans INITIAL_CONTEXT.json. Les six droits TUS ne démontrent pas la légitimité de toutes les souverainetés qu'englobe leur bitmap.

## Situation historique et erreurs démontrées

Les notices archivistiques attestent le principat et ses institutions propres. **Gaetano Domenico Boncompagni Ludovisi** est le prince de 1776 ; Antonio ne lui succède qu'en 1777. Les sources distinguent la dignité impériale, l'exercice princier local et les droits supérieurs revendiqués/exercés par Naples. Une relation moteur de simple indépendance absolue ou de marionnette autrichienne ne peut être déduite du seul titre impérial. Le droit napolitain n'est pas une annexion automatique de toute la principauté.

L'île se partage entre **Portoferraio et sa campagne toscane**, **Longone dans le dispositif napolitain des Présides**, et les **possessions du prince de Piombino**. La propriété TUS de l'intégralité des 54 cellules ne représente pas ces trois autorités. Les îlots et dépendances doivent être distingués, comme les possessions continentales, des listes anciennes ayant subi cessions ou réorganisations. La matrice donne les corrections minimales envisagées et leurs effets voisins.

Le problème est une **omission politique P0 démontrée**, pas une conformité sans correction. Les deux institutions administratives TUS déjà présentes ne sont pas un office de Piombino : ajouter un troisième niveau TUS ne corrigerait pas cette omission. Aucun changement économique artificiel n'est créé pour donner l'impression d'avoir installé la principauté.

## Faisabilité B et blocage précis

Une représentation B est techniquement envisageable : isoler les cellules de l'île depuis la province partagée, distinguer ses trois autorités, puis un noyau continental princier et ses interfaces. Le masque de l'île est **déterminé**, la séparation des trois juridictions dans ce masque ne l'est pas encore. Ce blocage ne demande pas un cadastre parfait ; il demande au moins une attribution politique bornée qui n'emporte ni la ville/territoire de Portoferraio, ni le golfe et les forts de Longone, ni une portion de Livourne. La forme littorale du jeu est simplifiée : les toponymes et les rectangles ne sont pas une preuve suffisante de la portion à transférer.

Les index recensent des plans de frontière et des états de population, mais la feuille de carte effectivement affichée ne fournit pas l'ensemble des lignes nécessaires, et les états nominatifs repérés sont postérieurs. Les catalogues Bellin constituent une piste précise pour compléter la confrontation, pas des cartes déjà lues. B_PROPOSAL.md présente deux réalisations possibles, les garanties, les documents ciblés et les éléments restant à fixer. Aucun candidat géométrique forcé ni ancien recalage improductif relancé.

Créer PIO demanderait aussi des pops fondées, une administration et des liens compatibles avec les droits de 1776. En l'état, choisir quelques cellules à partir d'un seul lieu, donner tout le RGB x6A7662 au prince, ou lui attribuer tout Elbe reviendrait à fabriquer la correspondance manquante. De même, conserver définitivement tout TUS n'est pas approuvé. **Aucun fichier fonctionnel modifié ; tâche BLOCKED P0, sans point.**

## Conservation et suite

Tous les 2411 fichiers fonctionnels courants doivent rester d'empreinte identique à BASELINE.json, y compris la méthode génoise désormais acceptée, les administrations SAR/MOD/PAR/LUC/AUS, Ljubljana, les noyaux impériaux, le registre, les électeurs et les travaux militaires/américains/français. Aucun TAG, province, terrain, pop, bâtiment, unité, pacte, bloc ou droit nouveau installé.

Cette passe sans installation ne réclame pas de nouveau mois de simulation. Le protocole joint est une reconnaissance visuelle facultative, sans pouvoir de clôture historique. La prochaine candidate indépendante, SC4-MASSA-CARRARA, sera seulement identifiée par le validateur ; elle n'est pas commencée.
