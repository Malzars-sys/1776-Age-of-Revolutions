# MAP2K — principes approuvés et seconde révision des retours joueur

Dernière révision : 13 octobre 2026. Version locale à tester dans Victoria 3 1.13.11. Aucun commit, merge ou push de ce lot. Ce document remplace les propositions antérieures pour les principes et les comportements ci-dessous.

## Résultat des contrôles

- **403 contrôles statiques passants**, statut `PASS_STATIC_ENGINE_PENDING` ; détail dans `MAP2K_VALIDATION.json`. La carte principale intégrée passe également ses 16 contrôles propres.
- Parmi ces contrôles : **2 712 cas simulés** exécutant le sous-ensemble du script de perte de principes, couvrant tous les niveaux et ordres d'acquisition. Ce ne sont pas des tests du moteur.
- Conservation de 835 804 980 habitants, des attributs de populations, des niveaux et attributs des bâtiments, des unités et des relations historiques par rapport à la baseline MAP2K protégée.
- Toujours exactement les cinq transferts RGB précédemment approuvés, aucune nouvelle modification de frontières dans cette révision ; bitmap inchangé, registre de 278 RGB inchangé.
- HEAD, références et index Git du workspace inchangés. Les autres modifications préexistantes sont conservées.
- Le contrôle général des espaces Git signale des espaces préexistants dans les historiques du workspace sale ; aucune normalisation générale ni réécriture de ces historiques n'a été effectuée.

Les logs lus concernent le jeu déjà lancé, pas un chargement de la dernière révision. Ils ont permis de corriger `ai_chance = { base = 0 }` dans les boutons de journal en `value = 0`, et de déclarer les deux types de modificateurs symboliques `script_only`. Les autres erreurs héritées de la version de base ne sont pas déclarées corrigées. Le jeu n'a pas été arrêté ni relancé pendant ce travail.

## Quatre principes, trois niveaux

Les valeurs sont les totaux de chaque niveau, sans cumul des tiers I/II/III.

| Principe | Niveau I | Niveau II | Niveau III | Bénéficiaire |
|---|---|---|---|---|
| Diète : influence | +50 | +250 | +1 000 | Empereur seulement |
| Diète : autorité nationale | +5 par autre membre | +10 par autre membre | +15 par autre membre | Empereur seulement |
| Diète : amélioration des relations | +10 % | +20 % | +30 % | Tous les participants |
| Cercles : biens supplémentaires de mobilisation | −5 % | −10 % | −15 % | Tous les participants |
| Cercles : vitesse de mobilisation | +5 % | +10 % | +15 % | Tous les participants |
| Justice : risque de blocage des lois | −10 % | −20 % | −30 % | Tous les participants |
| Justice : vitesse de promulgation | +5 % | +10 % | +15 % | Tous les participants |
| Administration : production de bureaucratie | +5 % | +10 % | +15 % | Tous les participants |
| Administration : coût bureaucratique des institutions | −10 % | −20 % | −30 % | Tous les participants |

La Diète I est active au départ, à la place de Commerce intérieur III. Le marché commun reste garanti par l'identité, pas par ce principe. Aucun bonus de capacité fiscale n'est ajouté. Les quatre groupes occupent les choix impériaux ; les groupes et choix des autres identités restent préservés.

L'autorité nationale de la Diète compte les autres membres impériaux reconnus **effectivement présents dans le bloc**, pas tous les sujets natifs de l'empereur. Les dépendances extérieures non impériales sont exclues. Le contrôleur actualise le bonus lorsque le nombre de membres ou le tier change.

### Obligations militaires des Cercles

1. L'empereur intervient dans les manœuvres défensives d'un membre contre une puissance extérieure.
2. Il intervient également dans les offensives de ses membres contre une puissance extérieure.
3. Les membres interviennent dans les manœuvres défensives et offensives de l'empereur contre une puissance extérieure.

La neutralité de l'empereur dans les guerres entre deux autres membres est conservée. Les manœuvres spéciales de rétrocession/libération appellent les membres éligibles indépendamment du niveau des Cercles. Les sujets de l'adversaire ne sont jamais inclus dans cet appel impérial.

## Autorité impériale et succession

L'**autorité impériale de progression des mandats** est distincte de la ressource nationale d'autorité ci-dessus.

`gain hebdomadaire = max(0, cohésion courante − 40) / (1 + ln(max(nombre de membres, 1)))`

La progression native par rang/nombre de membres est supprimée pour cette identité seulement. À une cohésion ≤40 : aucun gain et aucun achat de principe. Les points déjà obtenus ne sont pas retirés. Plus le bloc compte de membres, plus le gain ralentit, sans jamais devenir négatif. Le logarithme est une table exacte pour les nombres entiers de 1 à 128, couvrant largement le registre actuel de 37 pays maximum ; au-delà de 128 le diviseur est plafonné. Aucun opérateur logarithmique inventé ni define global.

Exemples arithmétiques, pas des mesures en jeu : avec 35 membres et une cohésion de 80, environ 8,78 points par semaine ; à 90, environ 10,98. Le seuil natif de 2 000 points par mandat est conservé.

Après décès et élection :

- Même pays réélu : pas de reconstruction et pas de perte de principe.
- Nouveau pays impérial : niveaux sauvegardés avant la création du nouveau bloc ; le dernier **groupe ajouté** est entièrement retiré si plusieurs groupes existent.
- Groupe unique : réduction d'un tier, sans descendre sous I.
- Monter un groupe de I à II/III ne modifie pas son ordre d'acquisition.
- Une correction mensuelle de direction native sans véritable succession ne déclenche pas cette perte.
- Échec natif de création : ancien bloc conservé ; aucune perte appliquée à celui-ci.

L'ordre d'acquisition est suivi quotidiennement, séparément des tiers. Les ajouts usuels sont espacés par le cooldown natif. Un import ancien de plusieurs groupes sans historique d'acquisition ne peut pas restituer des dates inconnues : l'ordre de première observation sert alors de repli documenté. L'ancien départ avec Commerce intérieur III seul est migré vers Diète I.

## Journal de centralisation

« La réforme de l'Empire » apparaît quand les quatre principes sont au niveau III. Chaque étape exige les quatre III, cohésion ≥75, paix et aucune manœuvre engagée pour les membres, tous les États impériaux vivants dans le bloc et aucun suzerain extérieur. Délai de consolidation : deux ans après l'ouverture et après chaque étape.

1. Bouton explicite : protectorats impériaux natifs, autonomes, sans tribut.
2. Bouton explicite : terres de la couronne natives, moins autonomes, sans tribut.
3. Bouton explicite : annexion des terres de la couronne au pays impérial, **y compris leurs possessions hors du périmètre de jure**. Cette conséquence est affichée avant la décision.

Pas d'annexion automatique. Les unions étrangères doivent être libérées par les mécanismes normaux auparavant. Les élections restent prévues durant les étapes de dépendance ; les types impériaux autorisent les grands pays. Après unification, la succession monarchique native prend le relais. Ces interactions de sujets, de création de bloc et d'annexion nécessitent impérativement des tests moteur.

## Boucle des notifications et camps de guerre

Deux causes scriptées ont été supprimées :

- Le pacte appelait sans filtre les pays via `auto_support_type`, y compris les sujets à libérer.
- Chaque callback `on_diplo_play_join_side` relançait un ajout de tous les soutiens, même déjà présents.

Les appels sont désormais filtrés, gardés par un contrôle du camp et un marqueur persistant **par manœuvre/pays/côté**, et ne sont plus déclenchés par le callback d'adhésion au camp. Ils restent évalués au début, au début de la guerre et au pulse hebdomadaire des manœuvres impériales. Une simulation de vingt pulses produit au maximum un appel par pays ; cela ne prouve pas encore la disparition de tous les pop-ups dans une sauvegarde native.

Les sujets directs/indirects du suzerain extérieur visé sont exclus du camp impérial. Une ancienne affectation erronée reçoit une seule tentative de correction par manœuvre, pas une boucle. Les règles natives peuvent empêcher de déplacer un participant déjà engagé dans une guerre : **ne pas garantir la réparation d'une guerre déjà commencée**. Les notifications déjà mises en file ne sont pas effacées du fichier de sauvegarde.

## Objectifs de libération

La nouvelle manœuvre utilise `aor1776_hre_liberate_estate`, de type natif `liberate_subject`. La cible est l'État sujet, son suzerain est le stakeholder. **Seul le sujet sélectionné reçoit l'objectif initial natif.** Les autres objectifs sont ajoutés volontairement par le joueur, avec les coûts de manœuvres normaux ; les colonies et sujets non impériaux restent exclus du type impérial. Cette règle remplace l'ancien ajout automatique d'un objectif par sujet du suzerain.

Les exigences natives portent donc sur **50 % des États du sujet visé ou sa capitale**, pas sur les États incorporés ou la capitale de la Suède. Les rétrocessions territoriales conservent leur condition d'occupation de l'État ciblé.

L'ancien objectif global reste défini pour les sauvegardes mais n'est plus sélectionnable. **L'ancienne migration automatique est supprimée** : le moteur indique explicitement que `has_war_goal` attend une portée `war`, pas `diplomatic_play`. Les contrôles échouaient et le pulse ajoutait de nouveaux doublons sans atteindre son marqueur de fin. L'effet de compatibilité ne crée ni ne retire plus aucun objectif ; il ne conserve que la correction bornée du camp des sujets et la mémorisation du suzerain. Les doublons déjà inscrits dans une sauvegarde ne sont pas effacés automatiquement, car cela risquerait de supprimer des objectifs ajoutés volontairement. Tester une nouvelle manœuvre depuis une sauvegarde antérieure à sa création.

L'émancipation du pays ciblé est native. Ensuite : restituer ses RGB détenus indûment, tenter son retour au bloc ; échec marqué pour reprise mensuelle. Pas de transfert du sujet à l'empereur. L'exécution d'un objectif individuel ne libère jamais les autres sujets, même en cas de demande native acceptée sans création d'une manœuvre. La demande diplomatique collective adressée au suzerain est un mécanisme distinct, dont la liste visible précise tous les sujets concernés.

## Acceptation, textes et infobulles

Les demandes de rétrocession et de libération utilisent désormais le score d'acceptation visible de l'action native, avec motifs localisés :

- Réticence de base : −25, désormais **nommée** dans l'infobulle.
- Relations avec l'empereur : relations ×0,5.
- Comparaison militaire native avec l'empereur : ×2, bornée de −50 à +50.
- Force terrestre des alliés du destinataire rapportée à la force disponible du bloc : malus plafonné à −60, sans division par zéro. Ce calcul n'affirme pas que tous ces alliés interviendront effectivement.
- Cohésion impériale : (cohésion−50) ×0,75.
- Obligation due à l'empereur : +60.
- Membre impérial obligé de restituer, sans obligation de l'empereur envers lui : +1 000. L'exception d'obligation garde son sens correct.

Ce sont des pondérations de gameplay à équilibrer, pas une probabilité historique. Les anciennes demandes territoriales ouvertes dans les sauvegardes conservent leur événement de réponse ; les nouvelles n'emploient plus le tirage caché 60/40.

Le score de +1 000 n'est pas utilisé pour contourner la règle chez les joueurs humains : l'action **Imposer la rétrocession impériale**, immédiate et sans approbation, est réservée aux membres non protégés. L'action de demande soumise à approbation ne cible que les puissances extérieures et les membres envers lesquels l'empereur doit une obligation. Un membre humain non protégé ne reçoit donc pas un droit de veto accidentel.

Tous les événements impériaux visibles ont un contre-texte littéraire **en italique**, attribué à un roman imaginaire. Les notifications de règlement/refus ont un tooltip concret : pays concernés mémorisés avant émancipation, RGB et bénéficiaires mémorisés avant transfert. Les listes sont rendues directement par les tooltips scriptés, plutôt que par l'ancienne localisation personnalisable vide. Un clic d'acquittement ne répète aucun transfert ni sanction. Une nouvelle sanction d'infamie est décrite seulement si elle a effectivement été appliquée lors de ce refus.

La clé UI manquante `aor1776_imperial_obligation_pact_desc` est localisée en anglais/français. Le texte explique autonomie, absence de tribut, sécession et obligations militaires.

## Accès à la carte

Le mode **« Territoires de jure du Saint-Empire »** est désormais intégré au mod principal après confirmation visuelle du prototype par le joueur. Il colore en jaune les 278 RGB de jure, quel que soit le propriétaire. À sa demande, le bouton bitmap du bas, le raccourci contextuel et la fenêtre autonome ont été retirés ; la carte bitmap du journal et ses listes cliquables sont conservées.

Le sélecteur global des captures est le `dropDown` de **`gui/lens_toolbar.gui`**, alimenté par `[GetMapModeIndices]`. Son `scrollwidget` ne peut contenir qu'un enfant : l'ancien en-tête l'invalidait. Désormais toute la barre des outils est identique au vanilla, sans en-tête, décalage de grille ni bouton indépendant. Le générateur et les tests contrôlent aussi le retrait du raccourci contextuel et de la fenêtre bitmap autonome.

Le HUD a retrouvé sa structure native après retrait de la seule fenêtre d'atlas autonome. Les contrôles vérifient l'absence des anciens raccourcis et la conservation de la carte dans le journal. Cette intégration reste à confirmer au prochain lancement avec le mod principal seul ; le mécanisme du prototype a déjà été confirmé par le joueur.

**Il s'agit maintenant d'un vrai mode sur la carte principale**, utilisant un masque de droits fixes et un shader spécifique. Il ne lit pas encore dynamiquement des modificateurs d'État arbitraires. Une future entrée/sortie de territoires exigera un registre partagé et une transmission de ses changements au rendu, dont la faisabilité en cours de partie reste à tester. Voir `MAIN_MAP/INTEGRATION.md`.

## Nouvelle passe : principes, score et journal invisible

### Choix réservés au SERG

Les 23 groupes standards portaient déjà `blocking_identity` pour l'identité impériale. Le verrouillage est maintenant également présent dans `visible` **et** `possible` de leurs 69 tiers : aucun choix ou upgrade standard pour le SERG, y compris un upgrade d'un groupe hérité d'une sauvegarde. Les quatre groupes autorisés et leurs douze tiers restent disponibles selon leurs règles de cohésion. Les conditions, bonus, graphismes et poids des 69 principes sont conservés hors de cette exclusion ; l'absence de bloc est traitée explicitement pour ne pas perturber la création d'autres blocs.

Aucun principe déjà acquis dans une ancienne sauvegarde n'est supprimé par ce verrouillage. La migration déjà définie de Commerce intérieur III seul vers Diète I reste conservée.

### Score bloqué à −25 : pays de référence corrigé

La nouvelle capture affiche bien la ligne localisée de base mais pas les autres contributions. Le calcul lisait `scope:target` pour le pays demandant la rétrocession, contrairement aux exemples natifs actuels (`26_join_power_bloc`, `28_invite_to_power_bloc`, `03_violate_sovereignty`) qui utilisent **`scope:actor`** dans l'acceptation. Il pouvait donc comparer le destinataire à lui-même et lire son bloc au lieu de celui de l'empereur.

Relations, comparaison militaire, dénominateur de force impériale, cohésion et obligation utilisent maintenant `scope:actor`. La règle de l'obligation dans le score territorial est corrigée dans le même sens. Les coefficients annoncés restent inchangés ; la régression interdit désormais le retour de `scope:target` dans ce calcul. Le −25 est un **score d'acceptation**, pas une probabilité de 25 %. Le score détaillé doit encore être mesuré dans une partie chargée avec ces nouvelles définitions.

### Journal permanent : contexte explicite et informations manquantes

Les trois journaux (tableau de bord, scrutin, centralisation) n'avaient pas de groupe déclarant un contexte de pays. La documentation native précise que le groupe définit ce contexte ; les logs du joueur contiennent des comparaisons invalides de `this` lors de l'évaluation du journal. Ils utilisent maintenant `je_group_aor1776_imperial_affairs`, explicitement **`context = country`**, avec nom français et anglais.

Le journal permanent reste destiné à tous les États impériaux reconnus, dont l'empereur et les électeurs. Le contrôle d'initialisation et les reprises existantes ajoutent une entrée manquante sans exiger de rejouer l'initialisation historique. Une reprise hebdomadaire utilise le seul événement quotidien de garde déjà prévu, avec délai de sept jours : pas de nouvelle chaîne d'événements par pays.

Contenu :

- Empereur et pays impérial, compte de provinces sous autorité impériale sur 278, provinces hors autorité et facteurs de cohésion.
- Portraits et dirigeants des électeurs ; vote déjà exprimé, promesse en vigueur ou préférence IA estimée.
- Une préférence IA est calculée par le **même classement** que le scrutin, sans exécuter le vote. Elle est non contraignante et peut changer avec la situation ; mises à jour hebdomadaires.
- Un joueur sans vote ni promesse conserve son choix : aucun candidat n'est choisi pour lui par le tableau de bord.
- Liste des villes libres reconnues et relations avec l'empereur, avec accès cliquable aux pays.
- Carte et liste des États ; explication des décisions électorales et de centralisation déjà disponibles. Les autres futures décisions impériales ne sont pas inventées sans règles approuvées.

Les tests supplémentaires vérifient le groupe de pays, les rattachements des trois journaux, les listes remises à zéro avant reconstruction, les traductions, le délai de sept jours et l'absence de tout vote/effect électoral dans le simple calcul de préférence. Le moteur doit encore confirmer l'activation des journaux dans la sauvegarde du joueur, le rendu des cartes/portraits et les nouvelles lignes du score.

## Nouvelle passe : bonus absents, refus et cible du casus belli

Les douze tiers déclaraient leurs bonus partagés dans `participant_modifier`. Les 69 principes de l'installation native utilisent `member_modifier` ; le premier nom n'est pas retrouvé dans le binaire installé, contrairement au second. La déclaration générée et les fichiers du mod utilisent maintenant **`member_modifier`**. Les bonus propres à l'empereur restent dans `leader_modifier`. La correction porte sur la déclaration des effets, pas uniquement sur leur description ; le rendu des infobulles et l'application réelle des valeurs doivent être confirmés après redémarrage.

Les fenêtres natives de réponse diplomatique recherchent des clés distinctes des titres/descriptions d'événements. Les douze clés `*_proposal_accepted_{name,desc}` et `*_proposal_declined_{name,desc}` des trois actions impériales sont désormais traduites en français et en anglais. Le texte nomme le destinataire et indique quel objectif utiliser après un refus.

La capture de refus concerne **la libération de sujets**, tandis que la capture de la carte sélectionne **une rétrocession territoriale**. Pour libérer un sujet, la manœuvre Libération impériale doit cibler le pays sujet ; pour restituer du territoire, Rétrocession impériale doit cibler un État contenant réellement des RGB impériaux détenus indûment par le pays visé. Ni un refus ni cette révision ne créent de droits sur le territoire national norvégien/suédois sans RGB impériaux enregistrés.

Si la puissance extérieure a refusé la libération et détient aussi directement un État impérial disputé, ce refus autorise désormais également la rétrocession de cet État. Les contrôles `possible` et `valid` conservent la condition de propriétaire actuel et de territoire réellement contesté. L'absence de marqueur local de refus utilise une comparaison optionnelle (`?=`), pour éviter la lecture d'une variable inexistante lors des aperçus. Le refus territorial enregistré reste valable ; aucune trêve ou restriction diplomatique native n'est contournée.

Régressions : schéma des douze tiers, traductions des réponses natives, conditions des deux contrôles territoriaux, lecture optionnelle et cinq cas simulés d'éligibilité (dont rejet d'un territoire non impérial). Ces simulations ne remplacent pas un test de sélection/déclaration en jeu. Fichiers de cette passe : principes, objectifs territoriaux et localisations `1776_imperial_demand_feedback_l_*`, avec leurs générateurs et validateurs.

## Crash à l'ouverture du journal : correction de structure

Deux rapports du 12 octobre 2026 (`victoria3_01260912_223044` et `victoria3_01260912_223735`) donnent, immédiatement avant le crash, la même erreur native `pdx_gui_container.cpp:145` : le `flowcontainer` de `gui/journal_entry_widgets/1776_imperial_widgets.gui` ne peut pas avoir un `hbox/vbox` comme enfant direct. L'exception du second rapport est `C00000FD (EXCEPTION_STACK_OVERFLOW)` à 22:37:36, après cette erreur à 22:37:35. Les rapports sont conservés dans le dossier `crashes` du profil Victoria 3 ; aucun fichier de crash ou de sauvegarde n'est modifié.

La ligne de l'empereur est désormais enveloppée dans un `widget` explicitement dimensionné (500×85), avec le `hbox` à l'intérieur, conformément à la structure des widgets de journal natifs. Les lignes d'électeurs utilisent également un widget dimensionné, porté à 500×150 pour les nouveaux boutons de choix électoral. Les portraits, listes, votes estimés, compteurs et atlas ne sont pas supprimés.

Quatre nouveaux contrôles vérifient l'absence d'enfant interdit, détectent expressément une reproduction minimale de l'ancienne structure et vérifient les dimensions des deux enveloppes. Ils ne prouvent pas que le moteur ouvrira la fenêtre sans autre erreur : **cause fortement corroborée et structure fautive corrigée, réouverture native encore nécessaire**.

Les mêmes logs contiennent des avertissements de lien `power_bloc` invalide dans les gardes ajoutés aux principes standards. Le lien de notre garde est maintenant optionnel (`?=`), en plus du test d'existence ; le moteur n'évalue pas nécessairement les conditions en court-circuit. Un contrôle supplémentaire couvre ce changement. Les conditions et effets natifs restent préservés hors du verrouillage SERG ; les autres erreurs, notamment une référence native `target_country`, ne sont pas déclarées corrigées.

Premier test demandé après redémarrage : ouvrir l'entrée permanente du Saint-Empire, faire défiler les électeurs/villes/États, refermer et rouvrir. En cas de nouveau plantage, lire le nouveau rapport plutôt que de supposer que celui-ci a la même cause.

## Nouveaux retours : fenêtre du destinataire, doublons et manœuvres

Les clés `aor1776_hre_request_subject_release_proposal_notification_name/desc` manquaient du côté du destinataire. Les titres et descriptions de réception des trois actions sont maintenant traduits en français/anglais, avec l'expéditeur `[INITIATOR_COUNTRY.GetName]`. Les réponses destinées aux tiers sont également traduites. La demande collective précise qu'elle couvre les sujets listés, tandis qu'une manœuvre de libération individuelle conserve uniquement le sujet sélectionné.

Le log du joueur à 22:57:20 et 22:59:01 donne `has_war_goal trigger [ Wrong scope for trigger: diplomatic_play, expected war ]` dans le pulse de préparation. Il confirme la cause de la multiplication visible des objectifs. La boucle d'ajout a été supprimée, pas seulement limitée dans le temps. La correction du camp des captifs est gardée par un marqueur de préparation posé avant les opérations et des marqueurs par pays ; elle ne modifie plus la liste des objectifs. Lübeck au départ signifie **Lübeck seul**. Les autres sujets/provinces doivent être choisis manuellement.

`initiator_can_add_war_goals` était explicitement `no`. Il est maintenant `yes` pour les manœuvres de libération et de rétrocession impériales, conformément à la référence native des manœuvres. Les coûts restent ceux des objectifs choisis ; les phases de la manœuvre et autres restrictions natives ne sont pas contournées. La sécession impériale conserve ses règles distinctes. Une sauvegarde ayant déjà accumulé des doublons n'est pas nettoyée sans identifier les objectifs légitimes ; le correctif arrête les ajouts futurs, mais ne promet pas une réparation rétroactive de cette liste.

## Journal épinglé, choix anticipés et promesses électorales

Le journal permanent et le journal de scrutin utilisent maintenant le réglage natif **`should_be_pinned_by_default_uninvolved_or_context = yes`**, prévu pour les journaux de contexte pays. Le journal permanent expose aussi **`is_shown_in_lobby`** aux membres impériaux reconnus, sans dépendre du marqueur d'initialisation après lancement. Ces champs sont attestés par `game/common/journal_entries/journal_entries.md` et `00_canada_australia.txt`. Cela règle le comportement par défaut des nouvelles entrées ; une épingle déjà personnalisée dans une sauvegarde n'est pas forcée à chaque rafraîchissement.

Un électeur humain peut choisir son candidat **avant le décès** depuis les boutons du journal permanent, le bouton « Choisir pour mon vote impérial » sur les fiches des électeurs ou l'action diplomatique « Choisir comme candidat impérial » dans le panneau d'un autre pays. Les boutons du journal permettent de sélectionner son propre pays lorsqu'il est éligible. Ce choix libre est stocké par pays, ne nécessite pas l'accord du candidat et ne crée pas de traité. Les règles historiques d'éligibilité ne sont pas supprimées : toutes les voix électorales ne rendent pas automatiquement leur titulaire éligible à la couronne.

À l'ouverture du scrutin, les électeurs sont d'abord enregistrés. Leur promesse active et réalisable prime ; à défaut, le choix anticipé humain est repris, et l'IA calcule son vote avec les règles historiques existantes. Un joueur sans choix reste libre pendant la délibération. **Des bulletins peuvent être enregistrés dès l'ouverture, mais l'investiture reste interdite avant les trente jours.** Les seconds tours gardent les deux finalistes et une nouvelle délibération.

Pendant la délibération, un humain peut modifier son bulletin. Le script conserve **un seul pays choisi par électeur** et reconstruit les totaux ; aucun ancien bulletin ni compteur supplémentaire n'est laissé derrière. L'IA sélectionne directement le candidat d'une promesse encore réalisable, plutôt que de se fier seulement à un bonus de score, et ne peut pas voter contre cet engagement. Une IA non engagée réévalue son choix chaque semaine selon ses règles pendant la délibération. Une promesse expirée ou devenue irréalisable ne contraint pas le choix.

Montant approuvé par l'utilisateur : **+10 d'infamie une seule fois par promesse rompue**. Un humain choisissant un autre candidat pendant le scrutin reçoit la sanction puis perd le marqueur de cette promesse ; modifier ensuite son choix libre ne répète pas cette sanction. Voter selon la promesse ne coûte rien. La rupture du vote ne retire pas automatiquement les autres articles économiques d'un traité. Les obligations économiques et règles natives de retrait restent distinctes ; aucune annulation générale de traité n'est inventée.

L'acceptation IA de l'article électoral n'est plus un −50 constant. Pour l'électeur donnant sa voix : réticence −40 ; préférence historique du candidat moins sa base 20, bornée de −250 à +100 ; obligation due au candidat +40 ; engagement d'au moins cinq ans : −2 par année, plafonné à −40. Le bénéficiaire évalue l'obtention de la voix à +60. La préférence réutilise relations, prestige plafonné, continuité impériale/habsbourgeoise, intérêts dynastiques, religion, alliances, rivalités et guerre. Ces coefficients restent des **heuristiques de gameplay**, pas des probabilités historiques. L'argent et les contreparties des autres articles restent évalués par le moteur, sans ressource gratuite. Une durée d'engagement positive est exigée ; l'entrée en vigueur met immédiatement à jour le choix affiché.

Contrôles nouveaux : champs natifs d'épinglage/lobby, choix du propre pays et des autres candidats, source/candidat dans les boutons GUI, stockage anticipé, reprise initiale, promesse prioritaire pour l'IA, reconstitution des totaux, sanction exactement 10 et modèles de modifications successives sans double vote ni double sanction, scores de traité et traductions FR/EN. **Ni le clic dans ces nouveaux boutons ni le score réel du traité n'ont été testés dans le moteur.** Tests demandés : nouvelle partie prussienne/autrichienne, fiche de sélection, étoile du journal, choix de soi-même/Autriche avant décès, scrutin de trente jours, changement libre puis rupture d'une promesse humaine et maintien d'une promesse IA.

## Visuels et provenance

Les quatre illustrations fournies sont utilisées pour : dignitaire sur trône → Diète ; registre/plume → Administration ; carte circulaire → Cercles ; balance → Justice. Les trois premières possédaient déjà un alpha transparent : aucun détourage/recoloriage. Les trois tiers partagent leur illustration avec les cadres natifs I/II/III.

PNG conservés dans `workshop_assets/source/map2k_hre_principle_{diet,administration,circles,justice}.png`. DDS : `gfx/interface/icons/principles_icons/aor1776_hre_{diet,administration,circles,justice}.dds`. Taille native 210×210, BGRA avec alpha et chaîne complète de mipmaps.

La balance fournie avait un fond blanc. Détourage réalisé avec l'outil **Built-in image generation** (skill imagegen), transparence demandée ; pas de génération des trois autres illustrations. Sortie sélectionnée : `exec-9d70e406-2d59-4d41-831e-33d6037acf74.png`, copiée dans le PNG Justice du workspace. L'édition générative peut introduire de légères variations picturales : aucune identité pixel à pixel n'est revendiquée.

Prompt exact :

> Use case: background-extraction. Asset type: Victoria 3 Imperial Justice power-bloc principle icon. Input Image 1 is the edit target, not a style reference. Remove only the white/off-white backdrop and its cast shadow, including all white spaces inside and between the scale chains. Preserve the complete gold balance scale, its two hanging pans, central black medallion with gold double-headed eagle and crown, pedestal, original geometry, composition, proportions, painterly textures, gold colors and details. Keep both chains continuous and the negative spaces genuinely transparent. Do not redesign, add, recolor or simplify the scale or emblem; no text, no new objects, no white outline, no background scene. Return the isolated original-looking object with a genuine transparent alpha background.

## Validation en jeu demandée

Redémarrer le jeu pour charger les définitions et GUI ; conserver une copie de la sauvegarde de test. Aucun résultat financier ou militaire n'est garanti par les seuls contrôles statiques.

1. Nouvelle partie autrichienne : Diète I, douze tiers disponibles, ressources du chef/membres correctement distinctes ; cohésion sans malus des membres libres.
2. Sélecteur de cartes : ouvrir/fermer l'atlas ; journal : carte, compteurs, États cliquables et électeurs.
3. Demandes à Suède/Danemark : sujets nommés et score détaillé ; comparer relations/cohésion/alliés différents ; acceptation/refus, sanctions et événements concrets.
4. Nouvelle manœuvre après refus : Lübeck, Mecklembourg et Strelitz côté suzerain ; objectifs individuels principaux ; occupations des sujets, pas de Stockholm. Puis test distinct de l'ancienne sauvegarde.
5. Laisser plusieurs semaines : aucune notification cyclique de soutiens ; acquitter les pop-ups et ouvrir normalement le menu du jeu.
6. Scrutin après décès : trente jours, votes humains/IA et promesses ; réélection sans perte ; autre pays avec perte du dernier groupe seulement.
7. Quatre principes III : journal, délais de deux ans, protectorats, terres de la couronne et unification explicite ; cas avec union extérieure bloqué.

Fichiers de logique principaux : `1776_imperial_principles.txt` (groupes/principes), `1776_imperial_reforms.txt` (valeurs/effets/sujets), `1776_imperial_constitution.txt` (effets/hooks), `1776_imperial_actions.txt`, `1776_imperial_plays.txt`, `1776_imperial_war_goals.txt`, événements impériaux et localisations `1776_imperial_repairs_l_*`. Interface : widgets du journal et `gui/right_click_menu.gui`. Les listes complètes générées sont vérifiées contre le compilateur ; aucune modification supplémentaire des historiques de populations/bâtiments/unités dans cette révision.
