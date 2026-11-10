# #22 — Protocole moteur de review

Version livrée le 9 novembre 2026 : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Tous les points ci-dessous sont **à tester**. Ne pas confondre les résultats statiques du rapport avec une partie exécutée.

Préparer deux nouvelles parties au 1er janvier 1776, avec ce workspace et le jeu 1.15. Noter le build affiché et les autres mods actifs. Conserver une sauvegarde au départ et avant une application d'objectif. Un ancien enregistrement ne suffit pas à vérifier les déclarations initiales.

## A — Treize Colonies et Grande-Bretagne

1. Commencer en jouant les Treize Colonies. Vérifier que la guerre d'indépendance existe contre GBR, que les camps et objectifs s'affichent, et que l'Espagne n'est pas déjà participante à l'initialisation. Relever les pays réellement entraînés par le moteur, sans attendre qu'ils correspondent seulement à la liste des backers explicites.
2. Laisser progresser les combats : fronts utilisables, armées capables de combattre, soutien qui évolue sur 0–100. Un soutien à zéro ne doit pas être interprété comme une promesse d'ancienne capitulation automatique. Relever tout blocage avec date et sauvegarde.
3. À une étape d'exécution d'objectif, comparer l'écran de guerre, le lien de sujet, le bénéficiaire et les notifications avant/après. Vérifier l'indépendance accordée au bon pays ou, dans la branche inverse, le rétablissement correct de la sujétion via l'objectif miroir. Sauvegarder et recharger après le changement pour vérifier sa persistance.
4. Conclure la guerre par les moyens proposés par l'interface. Vérifier les participants restants, le statut USA/GBR, les éventuels objectifs miroirs, trêves et résultat du journal américain. Si un autre conflit continue, distinguer le délai du journal dû à son ancienne condition de paix globale d'une erreur d'exécution d'objectif. Le prêt français et son scénario complet relèvent de #38.

## B — Perse, Bassora et Irak ottoman

1. Lancer une seconde nouvelle partie, en Perse. Au départ, IR1 est l'initiateur de la guerre contre PER ; OMA est déclaré avec IR1 et ARB avec PER. Vérifier ce que le moteur charge réellement, notamment le rôle du suzerain ottoman et le maintien des liens de sujets.
2. Vérifier les demandes : Bassora pour la Perse, Khuzestan pour IR1, port de traité au Fars pour Oman. Les propriétaires initiaux attendus sont respectivement IR1, ARB et PER. Aucun objectif ne doit viser un État inexistant ou un mauvais titulaire.
3. Occuper Bassora et observer les conditions/délais d'application affichés. Si l'objectif est exécuté avant la fin de la guerre, vérifier le propriétaire transféré, l'objectif miroir, la guerre encore en cours lorsque d'autres demandes restent à résoudre, et les notifications/callbacks pertinents. Si la situation permet une reconquête, vérifier son effet sur le miroir. Une simple disparition de l'objectif dans la liste ne suffit pas comme preuve de transfert.
4. Sauvegarder/recharger après une application d'objectif, puis conclure la guerre. Vérifier les fronts, les détenteurs des États ou du port concernés, les relations de sujets et le résultat de paix. Les demandes opposées ne doivent pas produire de double transfert incohérent.

## C — Compléments ciblés, sans les forcer dans les parties de départ

- Les deux nouvelles actions génériques (retour à un sujet, libération comme sujet) doivent être visibles et autorisées seulement quand leurs conditions natives sont réunies. Vérifier le destinataire, le sujet sélectionné et les motifs d'indisponibilité.
- Les actions russe et polonaise restaurées ne doivent pas créer spontanément une guerre en janvier 1776. Leur scénario DLC nécessite ses propres conditions ; l'inventaire statique ne certifie pas ce déroulement. L'essai d'unification territoriale déjà restant en #32 demeure à faire séparément, sans modifier massivement les pays de départ uniquement pour ce test.
- Pour les branches d'événements inaccessibles en 1776, une copie de sauvegarde de test ou un déclenchement contrôlé peut vérifier les effets immédiats `+5`, `−5`, `+50` et leurs cibles. Ne pas certifier aviation, Taiping, identité nationale ou poids pacifistes sur la seule base d'une partie de quelques mois où ces branches ne se produisent pas.

## Retour attendu

Pour chaque scénario testé : build, pays joué, nouvelle partie confirmée, dates utiles, résultat obtenu et sauvegarde avant/après en cas d'anomalie. Joindre les passages pertinents du journal d'erreurs si une commande de guerre, un scope ou un callback échoue. Le fichier natif hérité `war_exhaustion_values.txt` constitue une réserve documentée à distinguer des six fichiers du mod modifiés par #22.

Une branche non rencontrée reste **non testée**. La réception de ce protocole ou la mise en In review ne constitue pas une validation moteur. Aucun résultat ni attestation humaine n'est prérempli.
