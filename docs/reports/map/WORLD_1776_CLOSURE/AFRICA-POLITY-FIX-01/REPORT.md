# AFRICA-POLITY-FIX-01 — chargement des statuts et tributaires

29 octobre 2026. IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION. Correctif autorisé par les signalements du joueur : Kanyok tributaire d'un Luba décentralisé, puis Lunda et Kazembe décentralisés et non contigus. Les captures prouvent le problème signalé, pas un succès après correction ; date en jeu, durée et sauvegarde inconnues.

## Cause et correction

Le vanilla définit LBA/LND/KZM/MSH/MNC décentralisés ; les fichiers WORLD les redéfinissaient sans mode explicite. Le validateur précédent choisissait systématiquement la dernière définition et masquait ce défaut. Les remplacements doivent être explicites avec le mode de base de données prévu par les versions récentes. La correction ajoute REPLACE_OR_CREATE: aux49 redéfinitions africaines préexistantes de7 fichiers WORLD. Le contenu des49 définitions est strictement identique : catégories, cultures, couleurs, capitales et tiers restent les décisions historiques déjà installées. Les nouveaux TAG restent des créations simples. Il ne s'agit pas de centraliser indistinctement les communautés : leurs catégories décentralisées sont également préservées, y compris Luyana, les communautés du Karoo et les chefferies sotho.

Luba, Lunda et Kazembe deviennent donc effectivement déclarés comme États non reconnus centralisés, de même que les autres pouvoirs dont la déclaration était ignorée. Tous les11pactes tributaires WORLD africains conservés ont des acteurs non décentralisés dans le modèle explicite. Les rangs, la diplomatie permise au joueur, les lois effectivement retenues et les budgets demandent une observation moteur ; aucun prestige ni technologie ni armée n'est créé pour forcer leur conformité.

Kanyok garde son lien au Luba et le touche déjà. Le pacte Lunda→Kazembe est retiré : Kazembe reste indépendant, sans annexion ni corridor. Une dépendance historique éloignée n'est pas impossible par principe ; sa traduction par le sujet de marché du jeu était ici trop forte et peu adaptée à la demande du joueur. Source historique : Ndaywel è Nziem, UNESCO V ch20 pp651,659-660, PDF local INTERIOR-01/sources/UNESCO_LUBA_LUNDA.pdf réellement relu. La source décrit une royauté structurée, un Kazembe autonome et des tributs attestés notamment dans les années1790 ; elle ne certifie pas le partage économique moteur en1776.

## Conservation et preuves

8 fichiers fonctionnels ciblés :7fichiers de définitions (seules49clés changées) et le seul pacte LND→KZM de la diplomatie INTERIOR-01. Aucun pixel/RGB/frontière, POP, bâtiment/PM, technologie, loi, personnage ou formation militaire modifié. Monde : 837,328,654→837,328,654, delta0 ; tous les propriétaires RGB inchangés. Les pays des autres chantiers et les versions courantes sont conservés ; pas de Git, vanilla ou suiviSERG écrit. Préimages immédiates et empreintes : apply_inputs/ et FILES_MODIFIED.json. Les anciens reçus ne sont pas écrasés : ce correctif s'applique au-dessus de leur version historique.

271/271 contrôles statiques, détail VALIDATION.json ; résolution sans remplacement implicite, invariance des corps de définition, audit des pactes, technologies et non-régression, voisinages, conservation des fichiers protégés. La résolution explicite est un modèle statique ; aucun chargement corrigé n'est encore attesté en jeu.

Le test africain groupé reste en cours. La zone5 a un défaut rapporté par le joueur, aucun critère V entier ni succès inventé. WORLD10/320(3,13%) inchangé. Le guide est corrigé : Kazembe doit désormais être indépendant ; Kanyok doit rester tributaire d'un Luba centralisé. Les déclarations modifiées requièrent un redémarrage et une nouvelle partie pour vérifier l'initialisation ; aucun correctif silencieux de la sauvegarde ouverte n'est prétendu.

## Composition concurrente de fin de passe

Après le premier contrôle, ARABIA-01 a finalisé le formatage de quatre fichiers partagés. Leurs empreintes d’entrée et de sortie correspondent exactement aux reçus FORMATTING_FINISH.json : changements conservés et attribués à ce chantier externe, sans réécriture de notre part. Les6016RGB africains restent aux mêmes propriétaires. Le signalement du joueur est ajouté à l’ancienne fiche de test (zone5 en défaut, pas de succès). Le contrôle courant accepte uniquement ces sorties sourcées et les écritures documentaires autorisées ; aucune exception générale aux tests de conservation. Voir EXTERNAL_COMPOSITION_REVIEW.json et AFRICAN_OWNERSHIP_RECHECK.json.
