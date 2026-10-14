# MAP2K — corrections après les tests du joueur

Révision suivante : [principes approuvés et réparations](MAP2K_PRINCIPLES_AND_REPAIRS.md). Elle remplace notamment les appels de soutiens, objectifs de libération, scores d'acceptation, textes de réponse et la proposition de principes de ce rapport historique.

12 octobre 2026. Modifications locales, aucun commit, merge ou push. Contrôles structurels : **186 passants**, statut `PASS_STATIC_ENGINE_PENDING`. Pas de nouveau test moteur pendant ce travail.

## Expulsion de la Prusse : preuve dans la sauvegarde

Inspection non destructive de `autosave_exit.v3`, convertie localement sans modifier la sauvegarde originale : pays 5 = PRU, pays 8 = AUS ; trace `catalyst_kicked_out_of_bloc`, country=5, target_country=8, date=1776.3.25. La Prusse porte `power_bloc_leave_date=1776.3.25`. Le bloc possède bien l'identité impériale personnalisée.

Cela établit une **expulsion par l'Autriche**, pas un départ volontaire du joueur. Les poids natifs de l'IA prennent notamment en compte la faible cohésion, les mauvaises relations et l'attitude hostile. La faible cohésion est un facteur plausible, mais la sauvegarde ne conserve pas le calcul précis de la décision : ce n'est pas une cause exclusive démontrée.

## Cohésion corrigée en priorité

`power_bloc_cohesion_per_member_add = 0` pour le SERG. Aucune pénalité liée au nombre de membres libres, à leur part de PIB ou à leur absence de suzerain natif impérial.

Nouvelle cible, avant d'éventuels autres modificateurs de principes :

`90 − 40 × (RGB impériaux hors autorité / 278) − 5 × électeurs aux relations négatives − 3 × villes libres aux relations négatives`, bornée de 0 à 100.

Un sujet d'une puissance extérieure n'est pas sous autorité impériale. Un membre autonome n'est pas pénalisé pour sa seule autonomie. Le journal expose les compteurs. La cohésion courante converge progressivement vers sa cible ; une ancienne sauvegarde n'est pas artificiellement remise à 100.

## Expulsions et sorties ordinaires

- Départ volontaire toujours interdit par `can_leave = { always = no }`.
- Boutons d'expulsion du panneau de bloc et du menu contextuel désactivés pour l'identité impériale, avec tooltip dédié. Autres blocs préservés.
- Aucun champ `can_kick` non documenté, aucun define global ni prestige artificiel.
- Interception du catalyst natif d'expulsion : pour une exclusion impériale invalide uniquement, tentative de réintégration au lieu des effets scriptés de pénalité de relations/trêve/cohésion. Pas de lobby hostile ni recalcul hostile dû à cette exclusion. Tous les autres catalysts et la branche non impériale sont conservés.
- Reprise quotidienne en cas de sortie sans sécession reconnue, initialisée au chargement et à l'investiture ; contrôles mensuels en secours.
- Pays ayant obtenu une sécession exclus. Une manœuvre/guerre active contre l'empereur suspend la reprise. Les sujets natifs des puissances étrangères et leurs unions personnelles ne sont pas libérés par ce correctif.
- Échec de rattachement marqué en attente. Notification uniquement après rattachement réellement constaté, avec protection contre le spam.

**Limite à tester en jeu :** la décision d'expulsion IA reste en partie native. Il faut vérifier l'ordre catalyst/retrait, `join_power_bloc` après expulsion et le cooldown natif de six mois. L'interception et la reprise quotidienne ne prouvent pas une désactivation absolue de la décision native. Ne pas promettre une réintégration réussie sans test moteur.

La [Bayerische Schlösserverwaltung](https://schloesser.bayern.de/deutsch/presse/archiv03/hoechstaedt/schlacht.htm) documente la Reichsacht frappant les électeurs de Bavière et de Cologne en 1706. Cette sanction exceptionnelle n'est pas représentée ici et ne justifie pas l'expulsion ordinaire d'un État pour faible cohésion.

## Autres changements de la révision en cours

- Tooltips des demandes : sujets nommés et provinces RGB accompagnées de l'État et du bénéficiaire légitime ; pas de villes inventées pour les provinces anonymes.
- Libération : score d'acceptation dans la confirmation native, événements d'acceptation/refus à l'empereur, liste des sujets mémorisée avant indépendance.
- Buts de guerre : clés de localisation natives corrigées, notification d'application, hook réel `on_diplo_play_start` pour les appels impériaux.
- Le joueur a confirmé la libération effective des sujets. Une demande acceptée peut créer une trêve sans guerre : aucune guerre forcée n'a été ajoutée pour remplacer cette issue normale.
- Scrutins : trente jours avant investiture, même avec tous les électeurs IA ; journal de vote joueur, vote propre si éligible, majorité et second tour conservés.
- Article de traité natif : engagement pour le prochain vote, durée d'engagement, contreparties dans l'éditeur natif, expiration et respect des promesses encore actives.
- Journal commun : empereur, portraits des électeurs, relations, compteurs et liste cliquable des États.
- Marqueur d'État sur les parties d'État contenant les 278 RGB enregistrés, y compris sous contrôle étranger. +25 % d'infamie dans le but natif Conquérir l'État ; rétrocession/libération impériale exemptes. Le marqueur ne signifie pas que toute la région de jeu ou les possessions mondiales des membres sont impériales.
- Carte jaune dans le journal, suivant l'alternative explicitement approuvée. Les modes natifs inspectés ne fournissent pas de filtre vérifié pour peindre un modificateur arbitraire sur la carte principale ; aucun mode fictif ajouté.

## Principes : proposition seulement

Voir [MAP2K_PRINCIPLES_PROPOSAL.md](MAP2K_PRINCIPLES_PROPOSAL.md) : Diète perpétuelle I au départ et Cercles impériaux optionnel. Commerce intérieur III reste provisoire jusqu'à validation.

## Assets

La compétence imagegen a été utilisée pour détourer les illustrations fournies sur fond blanc, avec l'outil intégré et une sortie transparente. Consignes : conserver sujet, composition, couleurs et détails ; retirer seulement le fond, sans ajouter d'éléments. Le détourage génératif peut introduire de légères variations visuelles.

- Lien impérial : `workshop_assets/source/map2k_hre_imperial_bond_v2.png`, DDS diplomatique 100×100.
- Accès carte : `workshop_assets/source/map2k_hre_map_access_v2.png`, DDS 120×120.
- Marqueur : source déjà transparente conservée directement, `workshop_assets/source/map2k_hre_state_marker.png`, DDS 120×120, pas de régénération du sujet.
- Carte : rendu déterministe des RGB, `map2k_hre_registered_map.png` et DDS 1000×740, proportions natives conservées. Pas une image géographique générée par IA.

## Fichiers et validation

Le compilateur `tools/map2k_imperial_feedback.py` étend le système impérial existant. Principaux fichiers nouveaux/modifiés : identité, effets/triggers/on-actions, actions diplomatiques, événements, buts de guerre, article de traité, journaux/boutons/GUI, modificateurs, localisations anglaises/françaises et assets. Overrides natifs minimaux : calcul d'infamie de `03_conquer_state.txt`, seul catalyst d'expulsion dans `00_diplomatic_catalysts.txt`, seules gardes des deux boutons d'expulsion dans les deux GUI natives.

`MAP2K_VALIDATION.json` contient le détail des 186 contrôles, dont conservation des autres catalysts et interfaces hors gardes, absence de pénalité par membre, exclusions des sécessions, délai électoral, notifications, localisations et surcharge. Les contrôles différentiels de population, bâtiments, unités, dépendances, RGB et Git restent exécutés. Aucun transfert territorial supplémentaire dans cette révision.

Les logs de la session antérieure ne valident pas les nouveaux scripts. Les portraits, tooltips dynamiques, traité et interception d'expulsion restent à charger et tester dans Victoria 3 1.13.11.

Après redémarrage : vérifier Prusse dans le bloc et nouveau tooltip de cohésion ; tester les deux accès d'expulsion, plusieurs mois de simulation, une réintégration et une sécession obtenue ; contrôler que les sujets extérieurs restent dépendants. Puis tester acceptation/refus, notification d'une cession sans guerre, appels lors d'une vraie guerre, journal/carte, scrutin joueur et expiration de promesse. Comparer l'infamie d'une conquête marquée/non marquée et une rétrocession exempte.

Aucune simulation prolongée ou amélioration financière n'est garantie avant ces essais.
