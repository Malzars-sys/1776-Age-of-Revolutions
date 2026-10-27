# Contraintes de jouabilité — découpage colonial

## Continuité des postes avancés

Consigne directe du joueur, 25 octobre 2026 : ne pas créer de poste isolé dans des territoires non incorporés ; relier chaque poste avancé au territoire principal par une petite ligne de cellules incorporées, afin de préserver son accès au marché et son ravitaillement.

Application aux lots nord-américains, à commencer par HBC :

- Chaque poste retenu doit appartenir à un ensemble continu de provinces du même pays, relié au territoire principal par un corridor aussi étroit que possible. Un simple contact par les coins ne suffit pas à démontrer une connexion terrestre.
- Privilégier les axes fluviaux ou côtiers attestés lorsque leur tracé permet cette continuité. Documenter les RGB du poste et du corridor, leurs adjacences et leur destination.
- Le corridor est une concession de représentation pour la jouabilité, demandée par le joueur : il ne constitue pas une preuve de souveraineté historique sur tout le trajet ni sur l'arrière-pays.
- Vérifier séparément l'accès effectif au marché dans le moteur, les infrastructures et le ravitaillement. La continuité graphique seule ne vaut pas validation économique.
- Les cellules du bitmap sont des provinces ; l'incorporation administrative est portée par les États du jeu. Ne pas incorporer automatiquement une State Region entière pour obtenir ce corridor : vérifier et documenter la représentation compatible avec les États partagés.
- Aucun poste isolé ne doit être livré. Si le corridor exige une attribution historique non établie, signaler précisément ce point et conserver le tracé en attente plutôt que créer une enclave sans accès au marché.

Statut : corridors préparés dans les propositions ; aucune application ni validation d'accès au marché en jeu à ce stade. La proposition active est indiquée dans `CURRENT.json`.

## Remplissage du côté littoral

Consigne directe complémentaire du joueur, 25 octobre 2026 : toutes les terres comprises entre le côté littoral de la ligne et la côte doivent rejoindre les territoires contrôlés par la compagnie, afin d'obtenir une bande côtière lisible et continue. Ce choix esthétique est autorisé par le joueur ; il ne constitue pas une nouvelle preuve historique.

Appliquer ce remplissage au côté littoral de toute la ligne de la proposition HBC-02, y compris la branche de Cumberland : la ligne forme la limite intérieure et les terres vers la côte sont incluses. Ne pas étendre le remplissage du côté de l'intérieur des terres au-delà de la ligne. Conserver les provinces entières et vérifier que les postes restent connectés. La version ajustée est `HBC-02/COASTAL_CANDIDATE.json` avec aperçu `COASTAL_CANDIDATE.png` ; la proposition n'est pas encore appliquée aux historiques du jeu.

## Conservation intégrale de la population et des bâtiments HBC

Consigne directe du joueur, 25 octobre 2026, pour des raisons de gameplay : la réduction des territoires contrôlés et la décentralisation d'une partie des régions ne doivent réduire ni la population de la compagnie ni son patrimoine bâti existant.

- Référence démographique figée : **108 626 habitants**, avec conservation des effectifs par culture/religion ; aucun transfert de ces POPs hors du pays HBC pour financer un nouveau détenteur décentralisé.
- Conserver tous les bâtiments, leurs niveaux, méthodes de production, réserves et propriétaires économiques. Les 21 commandes d'historique recensées ne signifient pas 21 bâtiments distincts ni un total de niveaux certifié par le moteur : conserver aussi leur ordre pertinent.
- Lorsqu'une ancienne portion HBC disparaît entièrement d'une State Region, réaffecter ses POPs et, si nécessaire, ses bâtiments à une portion HBC conservée et connectée. Ne pas laisser des commandes attachées à un `region_state:HBC` inexistant ; ne pas supprimer leur contenu avec ce scope.
- Ne pas dupliquer les mêmes POPs simultanément chez HBC et chez les nouveaux détenteurs. La démographie propre des futurs territoires décentralisés nécessite un traitement distinct, qui ne peut prélever sur le total protégé de HBC.
- Utiliser le socle figé `HBC-03/CONSERVATION_BASELINE.json` et `python tools/hbc03_quebec_arc.py --check-conservation` pour contrôler les historiques après implantation ; ne pas remplacer le socle pour masquer une perte. Compléter par une vérification moteur du pays et des bâtiments.

La base `HBC-03/EASTMAIN_CANDIDATE.json` prolonge l'arc jusqu'à Eastmain House, sans poste supposé actif sur la façade atlantique. Le plan de conservation est préparé ; le complément militaire HBC-04 et `CURRENT.json` indiquent la proposition active. L'application au jeu demeure en attente.

## Continuité militaire HBC → Haut-Canada → Treize Colonies

Consigne directe supplémentaire du joueur, 25 octobre 2026 : conserver un lien terrestre direct entre HBC et le Haut-Canada (`ONT`), puis entre ce Haut-Canada et les Treize Colonies (`USA`). Aucun territoire décentralisé ne doit interrompre cette chaîne, afin que les troupes loyalistes puissent atteindre le front américain pendant la guerre d'indépendance.

- Exiger une frontière terrestre HBC–ONT et une frontière terrestre ONT–USA, reliées entre elles dans la même partie accessible du Haut-Canada. Deux contacts appartenant à des enclaves distinctes ne suffisent pas.
- Vérifier les contacts par bords de pixels, les provinces infranchissables et les adjacences spéciales natives. Un simple contact diagonal ou un trajet par mer ne satisfait pas cette consigne.
- Réserver le raccord HBC et le passage ONT lors des futures décentralisations. Toute modification du tracé doit préserver une chaîne terrestre équivalente ; ne pas reclasser ses provinces chez un tiers sans préparer un autre passage valide.
- Vérifier aussi les camps de guerre, les obligations des sujets et le passage effectif des formations en jeu. Une frontière physique ne garantit pas à elle seule un accès militaire opérationnel.
- Conserver intégralement la population et les bâtiments HBC déjà protégés ; ne pas financer le raccord par une perte démographique ou économique.

Proposition active : `HBC-04/LAND_LINK_CANDIDATE.json` et `HBC-04/LAND_LINKS.png`, avec **233 provinces HBC**, dont **5 conservées en plus** pour le raccord vers ONT. Le témoin de trajet utilise ensuite **11 provinces du Haut-Canada**, conservées sous propriétaire ONT. Tous ces RGB sont déjà détenus respectivement par HBC et ONT dans les historiques actuels ; la proposition prévoit de les maintenir, sans annexion d'un autre pays pour créer le raccord. Aucune intégration au jeu dans ce lot.

## Blocs compacts autour des raccords

Dernière précision du joueur, 25 octobre 2026, avec dessin : élargir les raccords en ensembles plus carrés/compacts, pour éviter une fine languette artificielle. Les provinces existantes sont regroupées dans des enveloppes plus larges, avec leurs contours natifs ; aucune prétention à une frontière historique nouvelle.

La proposition active devient `HBC-05/COMPACT_BLOCKS.json` / `HBC-05/COMPACT_BLOCKS.png` : **278 provinces HBC** et **103 provinces ONT**. Les 233 provinces HBC précédentes et les 94 provinces ONT actuelles sont conservées. Ajouts : 45 provinces au bloc HBC (32 du premier élargissement, puis 13 de l'encoche indiquée dans le dernier dessin), 9 au bloc ONT ; les 9 proviennent de terres HBC déjà omises de la proposition antérieure, sans prendre de territoire à un autre pays. Cette réaffectation prévue ne transfère pas les POPs/bâtiments HBC à ONT et ne réduit pas le socle protégé du pays.

Afficher tout ONT dans une même couleur ; la précédente bande rose claire n'était que le chemin de validation, pas un pays ni un corridor territorial distinct. Conserver la preuve de passage HBC → ONT → USA dans les données, sans la présenter comme une frontière sur l'aperçu politique. Le passage terrestre, les cinq postes et le plan économique antérieur doivent rester valides. Aucun changement runtime appliqué dans cette passe.

## 26 octobre 2026 — intégration et scénario autochtone

Le joueur approuve HBC-05 et autorise explicitement une très forte population autochtone anachronique, des peuples régionaux nombreux et des revendications HBC séparées du contrôle. HBC-06 installe 13 ensembles décentralisés et ajoute 2 400 000 habitants. Les 108 626 HBC, tous les bâtiments et la continuité HBC–ONT–USA restent protégés. Frontières autochtones approximatives ; claims par State Region, avec limites documentées. Statut : IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION ; aucun test moteur attesté.

## 26 octobre 2026 — succession de l’interface canadienne

La réunification demandée des deux Canadas remplace ONT par QUE au départ. Les 103 anciennes provinces ONT, dont le passage réservé, restent dans le même ensemble colonial ; chaîne protégée HBC–QUE–USA. HBC et le scénario autochtone restent intacts. La calibration de 90 000 personnes concerne uniquement la colonie réunifiée ; elle ne révoque aucune protection de population HBC.
