# Essais moteur — fortifications terrestres

**Statut : NOT_RUN.** Ces étapes sont un protocole, pas une preuve d’essais réussis. Conserver une sauvegarde de départ et des branches séparées. Relever la version du jeu et les mods chargés ; rechercher les nouvelles erreurs concernant les fichiers du lot.

## Construction et recherche

1. Dans un pays disposant de **Fortification et poliorcétique**, ouvrir un État intérieur, par exemple le Brandebourg : le bâtiment terrestre doit être proposé. Contrôler également un pays sans cette technologie : le bâtiment doit être verrouillé.
2. Dans un État côtier appartenant au même pays, vérifier l’absence du bâtiment terrestre et le maintien du fort naval. Vérifier un État partagé : c’est la condition côtière de l’État concerné qui doit correspondre à celle utilisée par le naval.
3. Construire jusqu’à cinq niveaux. Essayer un sixième, une commande groupée et plusieurs ajouts à la file : le plafond natif doit empêcher le dépassement. Annuler puis reconstruire pour vérifier le recalcul.
4. Contrôler les trois méthodes, leurs icônes et leurs ressources : base, **Forts casematés**, puis **Fortifications en béton**. Ne pas donner de déblocage gratuit pour ce test ; une sauvegarde de test avancée peut servir aux méthodes tardives.
5. Vérifier qu’aucun bataillon ni commandant supplémentaire n’est créé. Comparer budget, emplois et achats de biens à cinq niveaux et à différents taux d’emploi.

## Protection locale et paliers

1. À cinq niveaux entièrement employés, vérifier les puissances de 5, 10 et 15 pour les trois méthodes. Contrôler les mêmes valeurs après sauvegarde et rechargement. Essayer aussi une garnison incomplète, puis vide.
2. Faire défendre le pays propriétaire dans une province qu’il possède et contrôle dans cet État. La condition de **Position fortifiée** doit fournir les valeurs par niveau R2 : au niveau 1, simples −10/−5/+5 %, renforcées −20/−10/+10 %, avancées −30/−15/+15 % (provinces / pertes / défense). Au niveau 5 : simples −50/−25/+25 %, renforcées −85/−50/+50 %, avancées −85/−75/+75 %. Vérifier le plafond territorial de 85 % dans chaque variante de retraite ; les autres statistiques gardent leur cumul.
3. Comparer à une attaque du propriétaire, une bataille dans un autre État et une bataille où l’ennemi contrôle la province : aucun soutien du fort dans ces cas. Tester un allié dirigeant le côté de bataille dans le territoire d’un autre pays, afin de confirmer la règle stricte de propriété.
4. Déclencher une défaite défensive. Inspecter la présence du modificateur de provinces perdues au moment du résultat ; comparer des sauvegardes avec et sans fort, en tenant compte des autres modificateurs et des arrondis du moteur. Un résultat aléatoire unique ne mesure pas à lui seul une réduction exacte de 85 %. Le plafond porte sur la contribution des fortifications : vérifier séparément le cumul avec Liberty Or Death et les autres effets existants.
5. Examiner pertes, défense et survie des unités sur plusieurs combats comparables. Le modificateur de pertes subies n’est pas un modificateur de mortalité civile.

## Retraites et changement de situation

1. Observer une poursuite, une déroute et une retraite contrôlée. Les effets natifs de chacune doivent rester visibles avec le supplément de protection, et le fort ne doit pas empêcher une retraite normale.
2. Observer le comportement adverse face à une retraite fortifiée : les conditions reconnaissant une déroute ou une retraite contrôlée doivent toujours réagir.
3. Pendant un combat de test, modifier la méthode, réduire la garnison ou démolir le bâtiment. Contrôler le changement de palier et le retrait de la protection au contrôle natif suivant.
4. Contrôler un transfert de souveraineté et la reconquête d’une province : la protection doit suivre le propriétaire et le contrôle effectifs, sans modificateur national ou de commandant laissé en mémoire.
5. Vérifier des combats ordinaires sans fort, y compris sans général et en guerre de guérilla, pour comparer le comportement au vanilla.

## Affichage, sauvegarde et non-régression

Contrôler le fond transparent de l’icône sur plusieurs panneaux, les trois icônes de méthode inchangées, les survols et les textes FR/EN. Sauvegarder/recharger un bâtiment en construction, un fort employé avec chaque méthode et un combat fortifié. Vérifier les forts navals, l’armée américaine, les Minutemen, Liberty Or Death, la ferveur et le financement français.

Lancer les trois outils du lot en lecture seule après le test et conserver leur rapport avec captures, sauvegardes et erreurs moteur. Le statut ne devient **LAND_FORTIFICATIONS_RUNTIME_VALIDATED** qu’après réussite des essais réels pertinents.
