# MAP-2K — Saint-Empire de 1776 : version locale à tester

Date de dernière révision : 13 octobre 2026. Dernière révision : **PASS_STATIC_ENGINE_PENDING**, 401 contrôles. Aucun test natif de la dernière révision n'a été réalisé dans Victoria 3. Ce statut ne signifie pas une validation finale du lot.

Le [rapport actualisé](MAP2K_PRINCIPLES_AND_REPAIRS.md) fait foi pour les quatre principes approuvés, leur perte à la succession, la centralisation, les obligations militaires, les objectifs individuels de libération, l'acceptation, les textes et l'accès à l'atlas. Les descriptions antérieures ci-dessous restent un historique du lot initial et sont remplacées sur ces points.

## Carte et pays

Cinq provinces RGB ont changé de propriétaire, exclusivement selon les approximations de représentation approuvées par l'utilisateur :

| Région | RGB | Avant | Après |
|---|---|---|---|
| Rhineland | x11C021 | BAV | KPF — Palatinat |
| Rhineland | x707505 | BAV | KPF — Palatinat |
| Rhineland | xD080A0 | PRU | KTR — Trèves |
| Hesse | x1141A0 | HES | KMZ — Mayence |
| North Rhine | x518021 | PRU | KCL — Cologne, résidence à Bonn |

Quatre pays actifs supplémentaires, avec capitale possédée, gouvernement, dirigeant, noms français/anglais et héraldique stylisée. Trèves, Mayence et Cologne sont des gouvernements ecclésiastiques. Le Palatinat reste distinct de la Bavière : aucune anticipation de la succession de décembre 1777. Aucun nouveau RGB, aucune modification du bitmap, aucune nouvelle ville libre ajoutée dans ce lot. Les villes libres existantes sont conservées.

Les provinces du jeu englobent des fragments historiquement distincts. Leur affectation n'est **pas** déclarée HISTORICALLY_VERIFIED. Les locators du jeu ont servi à choisir des représentations existantes ; ils ne constituent pas une preuve des limites historiques. Aucun atlas mondial supplémentaire ni redécoupage général des enclaves.

## Constitution impériale minimale

L'identité de bloc propre au Saint-Empire comporte un marché commun, une interdiction de sortie ordinaire et une admission réservée aux États reconnus. Le lien impérial est un pacte sans tribut ni suzerain natif supplémentaire, afin de préserver les unions personnelles et la possibilité des guerres internes. Il ne constitue pas une alliance universelle : l'empereur défend un membre attaqué par une puissance extérieure, mais doit être retiré des guerres entre deux autres membres.

Les neuf titres électoraux initiaux sont Mayence, Trèves, Cologne, Bohême (AUS), Palatinat, Saxe, Brandebourg (PRU), Bavière et Hanovre. La reconnaissance exige le titre enregistré, un territoire et un gouvernement monarchique ou ecclésiastique ; le PIB ne crée pas un électorat. Un conquérant ne reçoit pas automatiquement la voix d'un titre annexé. Une future transmission légale des titres reste du flavor à développer.

Joseph II est suivi personnellement comme empereur, indépendamment de Marie-Thérèse, souveraine autrichienne. Son décès déclenche le scrutin après un jour pour laisser intervenir la succession native. Les voix sont recomptées contre les candidats et électeurs encore éligibles. Majorité absolue, second tour entre les deux premiers si nécessaire ; un blocage n'installe pas arbitrairement le candidat arrivé en tête. Après la révision des retours joueur, chaque scrutin prévoit trente jours de délibération avant investiture, même si tous les électeurs sont IA.

Préférences IA explicites : relations, prestige plafonné, continuité habsbourgeoise et impériale, intérêts dynastiques Wittelsbach, religion, alliances/accords défensifs, rivalités et guerre. Les pondérations numériques sont des **heuristiques de gameplay**, pas des probabilités archivistiques ni la promesse de reproduire un scrutin historique précis. Les garanties de privilèges constituent un cadre minimal, non un système complet de négociations électorales.

Si le pays élu est déjà le chef natif du bloc, aucun bloc n'est recréé. Sinon, toutes les branches et tous les niveaux de principes natifs sont mémorisés avant la tentative de création et restaurés seulement après réussite. Aucun effet de destruction ou de sortie non vérifié n'est utilisé. L'échec natif conserve l'ancien bloc et signale le transfert en attente. Les mandats/cohésion ne sont pas garantis conservés lors d'un changement de pays, conformément au compromis approuvé.

## Restitution territoriale et libération des sujets

Le registre figé contient **278 provinces** des régions impériales représentées et leurs titulaires de départ après ces cinq corrections. Il définit des droits de gameplay : il ne transforme pas toutes les possessions mondiales de la Prusse ou de l'Autriche en terres impériales et ne crée pas de droits sur leurs conquêtes futures. Le retour porte sur les seuls RGB détenus indûment, non sur une State Region entière. Aucun territoire n'est donné à l'empereur sauf si son pays était déjà le titulaire enregistré.

La demande de rétrocession à un membre est obligatoire sauf si **l'empereur doit une obligation à ce membre**. Un détenteur extérieur peut refuser : première sanction de 5 infamies par pays/région sur dix ans, casus belli valable dix ans, trêves ordinaires conservées. Les membres impériaux sont appelés à soutenir la manœuvre spéciale de restitution.

### Extension demandée pour Lübeck et les autres sujets

Les dépendances initiales restent intégralement inchangées. Cela inclut les liens natifs Suède/Lübeck, Suède/Mecklembourg, Suède/Mecklembourg-Strelitz, Grande-Bretagne/Hanovre et Danemark-Norvège/Holstein. Leur conservation est une instruction de gameplay explicite ; elle ne certifie pas l'historicité des dépendances suédoises héritées du mod.

Le lien impérial scripté ne force pas ces sujets extérieurs à quitter le marché ou le bloc de leur suzerain au départ. Le marché commun natif concerne les pays réellement rattachés au bloc impérial ; le rattachement des sujets libérés intervient seulement après acceptation ou application du but de guerre.

Une interaction complémentaire, **Exiger la libération des États impériaux**, vise une puissance extérieure possédant des sujets impériaux reconnus, directs ou indirects. Elle porte sur tous ses sujets impériaux, pas ses colonies ou autres sujets non impériaux. Les pays ayant fait sécession sont exclus. Les suzerains eux-mêmes membres de l'Empire ne sont pas visés par cette demande extérieure.

Acceptation, ou application du but de guerre après un refus :

1. Mémoriser les sujets impériaux concernés avant de modifier les dépendances.
2. Les rendre indépendants, sans les transférer à l'empereur.
3. Rendre leurs éventuelles provinces impériales enregistrées détenues indûment aux titulaires légitimes **encore existants**.
4. Rétablir le lien impérial et tenter leur rattachement au bloc. Un rattachement natif refusé reste marqué et est réessayé mensuellement.

Le refus coûte 5 infamies au maximum une fois par puissance sur dix ans et ouvre le casus belli de libération pour dix ans. Tous les membres reconnus sont appelés au côté impérial dans cette manœuvre. Les règles natives peuvent cependant empêcher un sujet de rejoindre une guerre contre son suzerain : cette interaction exige impérativement un test en jeu. Aucune libération gratuite au lancement de la guerre n'est utilisée pour contourner cette restriction.

**Limite importante :** un titulaire territorial entièrement annexé n'est pas recréé automatiquement. Le mécanisme restitue les droits des pays existants ; il ne prétend pas restaurer actuellement tous les micro-États disparus.

Les deux illustrations diplomatiques fournies et le deuxième emblème préféré sont intégrés aux chemins d'icônes natifs, en conservant la transparence. Leur affichage réel reste à vérifier.

## Économie, populations et protections

Population mondiale écrite : **835 804 980**, inchangée. Les profils de culture, religion et autres attributs écrits sont conservés, ainsi que les niveaux de bâtiments, PM, réserves et effectifs/formations militaires. Les ventilations démographiques des parties d'État utilisent une proportion géométrique entière, pas un recensement historique.

Populations attribuées : Palatinat 434 922 ; Trèves 73 946 ; Mayence 137 452 ; Cologne 70 861. Les propriétaires privés existants sont conservés. Un siège privé bavarois déplacé du Rhin vers la Bavière évite une référence à une partie d'État bavaroise supprimée. Aucun renforcement gratuit des nouveaux pays : leur recrutement, accès au marché et fonctionnement économique réel nécessitent le test initial, notamment pour Trèves et Cologne sans bâtiment explicitement écrit hors économie native de subsistance.

Les anciens historiques diplomatiques, les anciennes définitions de pays, les rapports MAP antérieurs et les autres fichiers protégés non autorisés restent inchangés. Les 12 erreurs de référence et 44 doubles attributions héritées recensées hors corrections sont distinguées des régressions ; aucune nouvelle anomalie de ces catégories n'a été ajoutée.

La guerre Irak/Zand conserve la contre-offensive et la demande perse sur Bassora. Deux objectifs sont rétablis : conquête de l'Arabistan/Khuzestan pour IR1 contre ARB, et port de traité au Fars pour Oman contre PER. Aucun ajout explicite de TUR. Leur résultat natif doit être vérifié.

## Vérifications et performances

`tools/validate_map2k_imperial.py` : 186 contrôles passants après révision des retours joueur, dont conservation différentielle, correspondance compilateur/fichiers installés, syntaxe structurelle, assets référencés, titres électoraux, vote majoritaire, obligation dans le bon sens, sauvegarde/restauration de chaque niveau de principe, cinq transferts exacts, restitution par RGB, libération filtrée avec sujets indirects, exclusion des colonies et dépendances initiales inchangées. Les protections contre l'expulsion, la nouvelle cohésion et les interfaces sont décrites dans [MAP2K_FEEDBACK_REVISION.md](MAP2K_FEEDBACK_REVISION.md). Elles restent à tester dans le moteur.

Ces contrôles ne remplacent pas le chargement par le moteur. Les logs disponibles précèdent cette implémentation ; ils ne prouvent pas l'absence d'erreurs nouvelles. Version native observée : Victoria 3 1.13.11.

Estimation, non mesure : +4 pays, aucun bâtiment/unité/RGB ajouté. Les événements d'élection tournent à la succession, les transferts de 278 RGB seulement lors des restitutions/libérations ; contrôleur et reprises mensuels. Aucun chronométrage de chargement ou d'un mois de simulation n'a été réalisé.

Tests à effectuer dans une **nouvelle partie après redémarrage** :

- Pays, dirigeants, marchés, économies et neuf voix électorales au départ ; Joseph II distinct de Marie-Thérèse.
- Un mois de simulation et relevé de nouveaux logs.
- Élection du même pays : principes/mandats inchangés ; élection d'un autre : transfert natif réussi et mêmes principes/niveaux.
- Guerre extérieure contre un membre, guerre interne entre deux membres, sécession.
- Rétrocession de Silésie détenue par un autre membre, cas avec obligation et refus extérieur.
- Demande à la Suède : acceptation, puis autre test avec refus et guerre ; vérifier Lübeck/Mecklembourg/Strelitz indépendants, membres du bloc, territoires réattribués, autres sujets inchangés.
- Tester aussi les unions personnelles extérieures : leur préservation au départ, puis une libération expressément obtenue par la nouvelle interaction.
- Vérifier les objectifs Irak/Zand et les trois illustrations fournies.

Les compétitions natives de direction par prestige ne disposent pas d'une désactivation spécifique vérifiée par identité ; une restauration constitutionnelle mensuelle sert de garde-fou. Aucun changement de defines global ni prestige artificiel n'est ajouté. Ce compromis et les restrictions natives sur les sujets figurent dans le registre des points non résolus.

## Sauvegarde et livrables

Checkpoint pré-MAP2K publié avec autorisation explicite : `adfa30da1cf497470322036d4a8b5e6db49ea32b`, branche `backup/1776-checkpoints`. Restauration Git indépendante : 5 875 fichiers, toutes empreintes concordantes, fsck passant, sans LFS ni alternates. Aucun commit dans le workspace principal, aucun merge, aucun push vers main. Les modifications MAP2K restent locales jusqu'à validation en jeu. L'utilisateur a validé MAP2J, mais aucun rapport MAP2J local séparé n'était présent à la capture : cette distinction est conservée.

Les cinq livrables demandés se trouvent dans ce dossier. `BASELINE.json`, `PLAN.json`, le registre territorial figé et le schéma de principes rendent les vérifications reproductibles. Ne pas réexécuter la capture de baseline après modification.

Les deux copies temporaires indépendantes `prepared` et `restored` ont été supprimées après contrôle de leur HEAD, de leur propreté et de leurs chemins exacts. Le checkpoint distant et les reçus de contrôle sont conservés ; ces copies restent récupérables depuis la branche de sauvegarde.

## Sources et limites historiques

- [Historisches Lexikon Bayerns — Kurfürsten](https://www.historisches-lexikon-bayerns.de/Lexikon/Kurf%C3%BCrsten) : titres électoraux, additions successives, poids des alliances dynastiques. Base de la règle des neuf voix, pas des frontières RGB.
- [Historisches Lexikon Bayerns — Wahlkapitulationen](https://www.historisches-lexikon-bayerns.de/Lexikon/Wahlkapitulationen) : engagements impériaux et sauvegarde des privilèges. Motif des préférences politiques, pas justification de coefficients précis.
- [The World of the Habsburgs — Joseph II as co-regent](https://www.habsburger.net/en/chapter/joseph-ii-co-regent) : distinction entre dignité impériale et gouvernement des possessions héréditaires.
- [The World of the Habsburgs — Franz Stephan, Holy Roman Emperor](https://www.habsburger.net/en/chapter/franz-stephan-holy-roman-emperor) : négociations dynastiques et intérêts des puissances lors des élections.
- [Historisches Lexikon Bayerns — Kurpfalz: Politische Geschichte](https://www.historisches-lexikon-bayerns.de/Lexikon/Kurpfalz%3A_Politische_Geschichte) : Palatinat et chronologie de la succession. Ne prouve pas chaque contour proposé.
- [LVR — Résidence de Bonn](https://click-rhein.lvr.de/detail/spot/78578?discoveryId=185) : résidence des électeurs de Cologne, distincte de la ville libre de Cologne.
- [Ville de Lübeck — Le chemin vers la liberté impériale](https://www2.luebeck.de/de/stadtleben/tourismus/luebeck/geschichte/luebecks-weg-zur-reichsfreiheit.html) : statut de ville impériale. Ne justifie pas la dépendance suédoise conservée à la demande de l'utilisateur.
- [Stiftung Mecklenburg — 1750 bis 1800](https://www.landesmuseum-mv.de/zeitraeume/1750-bis-1800/) : pouvoirs ducaux et distinction avec la Poméranie suédoise.
- [Landesarchiv Baden-Württemberg — Hohenzollern](https://www.landesarchiv-bw.de/de/themen/praesentationen---themenzugaenge/75301) : principautés et chronologie de leur passage ultérieur à la Prusse. La dépendance native héritée n'est pas corrigée dans ce lot.

API vérifiées dans les fichiers installés : `14_liberate_subject.txt`, `29_restore_union.txt`, effets des guerres balkaniques (`make_independent`), itérateurs des sujets (`00_spanish_new_world_scripted_effects.txt`), transfert de provinces (`00_chris_scripted_effects.txt`) et documentation native des actions/identités. Présence d'une API dans ces sources ne garantit pas les effets combinés de ce nouveau système sans test moteur.
