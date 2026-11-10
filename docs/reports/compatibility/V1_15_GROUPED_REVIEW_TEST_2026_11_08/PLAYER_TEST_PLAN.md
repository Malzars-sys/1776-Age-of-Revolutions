# Test joueur groupé — les six missions en review

Préparé le 8 novembre 2026 pour le workspace local courant, basé sur HEAD `0396b113` **avec les modifications locales présentes**. Aucun essai moteur ni résultat joueur n'est attesté par cette fiche. Aucun statut de mission n'est modifié.

## Ce que couvre cette tournée

Les six cartes ont été vérifiées dans la colonne **In review** du tableau de bord :

| Mission | Objet à valider |
| --- | --- |
| #21 | Migration des anciennes API : chargement, simulation, diplomatie, personnages, décrets et effets concernés. |
| #27 | Conclusions des journaux migrés, effets de sortie, continuations et absence de doublons. |
| #29 | Articles de traité concernant les péages des détroits. |
| #30 | Projection navale des deux lois et des trois paliers du principe naval. |
| #32 | Conquête d'État, annexion de pays et unification : infamie, application en cours de guerre et contre-objectifs. |
| #33 | Icônes natives du bien cuivre et de sa mine. |

Le froid, les quatre coques cuivrées et la cogue sont intégrés à la même tournée comme contrôles supplémentaires de la dernière livraison. Ils ne constituent pas trois nouvelles cartes en review. Les missions déjà terminées ne sont pas rouvertes.

**Mode d'emploi :** faire d'abord A, puis B dans des copies séparées des sauvegardes. A vérifie le démarrage et les régressions visibles ; B vérifie les effets et les branches nécessaires à une clôture complète. Une condition inaccessible reste **non testée**, sans imposer une campagne de plusieurs décennies pour la débloquer.

## Préparer une seule base de test

- [ ] Quitter complètement le jeu, puis le relancer avec la version locale actuelle du mod. Désactiver les autres mods pour cette référence. Noter version/build du jeu, DLC actifs, langue et playset.
- [ ] Commencer une **nouvelle partie en 1776**, en Grande-Bretagne. L'ancien identifiant de la cogue a changé : une ancienne sauvegarde ne convient pas pour certifier cette livraison.
- [ ] Faire les choix d'introduction, puis enregistrer sous **REVUE_BASE_GBR**. Créer une copie distincte avant chaque essai qui change une loi, conclut un traité ou termine une guerre.
- [ ] Pour chaque observation : relever pays, date et sauvegarde ; garder une capture si une valeur ou une fenêtre semble incorrecte. Ne pas utiliser les anciens logs comme résultat du nouveau lancement.

Changer ensuite de pays depuis le menu lorsque cette option est disponible. À défaut, ouvrir une nouvelle partie 1776 du pays demandé ; noter ce changement de partie.

## A — Tournée de démarrage et simulation commune

### A1. Grande-Bretagne : cuivre, chantiers et transports

- [ ] Ouvrir le **marché**, la fiche du **cuivre**, le menu de construction d'une **mine de cuivre**, puis une mine existante. Vérifier l'icône du bien, le portrait du bâtiment et les petits pictogrammes dans les recettes/infobulles : aucun cerf, carré vide ou texture manquante. Vérifier aussi les icônes des méthodes minières standard. **#33**
- [ ] Contrôle associé à l'alignement économique : le **prix de base** du cuivre doit être **40 £**. Le prix de marché courant peut être différent. Les gisements restent ceux du mod ; leur différence avec la carte vanilla est attendue.
- [ ] Ouvrir les méthodes des chantiers navals : construction artisanale, doublage en cuivre et coques non traitées doivent avoir leurs icônes lisibles. La coque non traitée doit porter le symbole d'interdiction. Vérifier également les icônes ordinaires de concentration des minerais dans une mine.
- [ ] Dans le concepteur naval, comparer les coques **légère / intermédiaire / supérieure** d'une **frégate**, puis d'un **vaisseau de ligne / manowar**. Les deux coques améliorées de chaque famille doivent demander du cuivre ; la légère doit rester disponible sans cuivre. Référence brute de construction : **35 cuivre** pour chaque coque améliorée de frégate ; **60** pour chaque coque améliorée de vaisseau de ligne. Relever les éventuels modificateurs du coût affiché. Ce n'est pas une consommation hebdomadaire ajoutée.
- [ ] Vérifier qu'il existe une seule **cogue** comme transport précoce, avec un nom, une silhouette et une représentation 3D fonctionnels. Il ne doit pas y avoir un second transport précoce identique ajouté à côté.
- [ ] Sur une copie où les technologies nécessaires sont disponibles, comparer ses trois aménagements de portée : la capacité de transport doit augmenter. Référence coque + module, avant autres bonus : **0,55 → 0,65 → 0,80 bataillon par navire**. Le transport moderne reste le palier suivant, avec **1,10 → 1,25 → 1,50**. Distinguer cette capacité de celle des marines et de l'efficacité d'invasion. Un palier encore verrouillé est non testé.

### A2. Tour des pays : les fenêtres de journal

Ouvrir chaque entrée et survoler ses conditions/effets. Enregistrer au moins une situation de journal actif avant de poursuivre la simulation.

| Pays | Action et résultat attendu |
| --- | --- |
| **Grande-Bretagne** | Dans Destin des Amériques, **Confédérer le Canada** doit avoir un titre traduit, des conditions lisibles et aucune clé brute. Faire le même contrôle côté colonie canadienne lorsque l'entrée est présente. Le nationalisme peut encore la verrouiller. |
| **Treize Colonies / États-Unis insurgés** | Ouvrir **Révolution américaine**, puis **Les voies discrètes du secours** et **L'engagement des insurgés** lorsqu'ils sont activés. Vérifier que les conclusions/conditions et effets ne sont plus remplacés par une grande zone vide ; la progression des soutiens et de l'engagement doit se mettre à jour. La guerre d'indépendance initiale doit être présente, sans implication espagnole ajoutée par ce lot. |
| **Pologne-Lituanie** | Ouvrir **Réformer la République des Deux Nations**. Vérifier les conditions et récompenses, dont PIB de 9 millions, alphabétisation strictement supérieure à 20 %, niveau de vie strictement supérieur à 8, intelligentsia et petite bourgeoisie non marginales. Les réformes spécialisées disponibles doivent également afficher leurs conclusions. Aucun compte à rebours de partage forcé ne doit être réintroduit. |
| **Empire ottoman** | Après les choix d'introduction, regarder **Le fardeau de la Sublime Porte**, **Un empire aux multiples maîtres** et le groupe **Déclin ottoman**. Les entrées ouvertes doivent avoir des conditions lisibles. **L'homme malade** doit déjà être visible en gris, inactif, avec sa condition d'activation ; son délai de réforme et ses modificateurs actifs ne doivent pas démarrer à ce stade. |
| **Empereur du Saint-Empire**, puis un électeur éligible | Vérifier **La réforme de l'Empire**, la situation du Saint-Empire et, lorsqu'elle est ouverte, **L'élection impériale**. La situation générale est permanente : son absence de réussite finale est normale. Une élection inactive n'est pas une élection testée. |
| **Russie** | Contrôle de non-régression : ouvrir lois, souverain/héritier et commandants, puis simuler quelques mises à jour sans crash. Vérifier aussi la dernière correction voisine : **Césaropapisme** au départ, bureaucrates militaires et amendement noble conservés. Ces lois ne sont pas l'objet d'une septième mission en review. |

- [ ] Dans un pays où elles sont proposées, ouvrir les entrées d'**urbanisation**, en distinguant Potentiel et actif. Une seule entrée visible au départ peut être normale. Potentiel affiche d'abord l'activation ; vérifier les conditions de réussite après activation.
- [ ] Ne pas chercher à faire apparaître une **migration** dans n'importe quel pays de 1776 : les trois programmes demandent notamment **Mission civilisatrice**, l'indépendance, la paix, un niveau de vie d'au moins 10 et le rang de puissance mineure au minimum. Le test de leur conclusion se fait en B4.
- [ ] Ne pas compter comme défaut l'absence des chaînes espagnoles laissées de côté, ni celle des anciens partages forcés polonais. La **Frontière du Nord-Ouest** n'est pas le journal de peuplement de l'Ouest ni l'ensemble des conquêtes mexicaines.

### A3. Froid, décrets, personnages et sauvegarde

- [ ] Avec State and Revolution actif pour le rendu saisonnier, vérifier le réglage **Activer les saisons**. Comparer une région froide de Russie en janvier puis en juillet, et une région chaude témoin. Relever séparément le rendu visuel et le froid mécanique.
- [ ] Examiner une route/flotte traversant une mer froide et les effets affichés sur vitesse, ravitaillement et accès au marché. La Baltique septentrionale atteint du **froid modéré**, pas nécessairement du froid sévère. Relever la route et la période ; ne pas demander de neige ou de gel partout.
- [ ] Dans plusieurs États britanniques/russes de compositions différentes, ouvrir les décrets concernés et leurs conditions. Vérifier les bons pays/États visés et l'absence de conditions vides. Noter les parts de cultures primaires lorsque les seuils de 10/30/50/90 % sont approchés ; leur contrôle précis est complété en B5. **#21**
- [ ] Examiner un souverain, un héritier, un général, un amiral, puis un agitateur et un politicien là où ils existent. Vérifier portraits, rôles et actions sans nouvelle erreur visible. L'absence d'un rôle dans un pays ne valide pas ce rôle. **#21**
- [ ] Sur la branche principale choisie, avancer jusqu'à juillet 1776 en notant les dates réellement atteintes. Cela couvre des mises à jour quotidiennes, hebdomadaires et mensuelles ainsi que la comparaison hiver/été ; cela ne vaut pas essai des échéances longues.
- [ ] Sauvegarder, quitter la partie, recharger cette sauvegarde et avancer au moins une semaine. Les journaux actifs, navires, modificateurs et compteurs doivent rester cohérents, sans double récompense ou nouvelle activation.

## B — Effets réels et branches de clôture

Utiliser des **copies distinctes**, en conservant une sauvegarde juste avant chaque résultat. Si les conditions ne sont pas atteignables dans les parties disponibles, noter le cas non testé. Un déblocage utilisé dans une copie de test doit être signalé ; ne pas forcer un événement dépourvu de ses pays/personnages/variables de contexte.

### B1. Péages des détroits — #29

Essayer d'abord **Grande-Bretagne / Danemark**, puis vérifier dans cette sauvegarde que le Danemark contrôle bien le détroit et que le commerce britannique en dépend. Ce couple est un candidat, pas une dépendance garantie. La technologie requise du mod est **Assurance commerciale**.

- [ ] Noter les péages et raisons d'acceptation avant traité. Essayer avec un détenteur direct, puis un cas où le détroit est dans sa hiérarchie de sujets ; un pays sans détroit doit rester refusé.
- [ ] Faire demander une **exemption personnelle** par le bénéficiaire ; dans une autre copie, faire offrir cette exemption par le contrôleur. Le bon bénéficiaire doit être exempté dans les deux sens.
- [ ] Dans une autre copie, conclure l'article de **suppression générale des péages** : vérifier son étendue, distincte d'une exemption personnelle, et la facturation réelle après mise à jour.
- [ ] Comparer des dépendances commerciales inférieures à 5 et d'au moins 5, si ces cas sont disponibles, en relevant les valeurs exactes et le signe des raisons d'acceptation.
- [ ] Pour les propositions IA, comparer libre-échange / autre loi et grief nul / positif : avec grief positif, préférence pour la suppression générale sous libre-échange, pour l'exemption personnelle sinon. Un score affiché seul ne démontre pas une proposition effective. L'IA native ne fait que **demander** la suppression générale ; ne pas attendre une offre IA de cet article.
- [ ] Après chaque article effectivement conclu : simuler la mise à jour, sauvegarder/recharger, vérifier sa persistance puis son retrait/sa rupture sur une copie. Vérifier aussi que les deux articles ne peuvent pas produire un doublon interdit.

### B2. Projection navale — #30

Utiliser une flotte active dont la projection est non nulle. Comparer à l'arrêt, avec les **mêmes navires, équipages et autres bonus**. Photographier le détail de projection avant/après, puis recharger pour contrôler la persistance.

| Variante à activer dans une copie éligible | Contribution attendue |
| --- | ---: |
| **Marine marchande** | −10 % de projection des navires. |
| **Flotte diplomatique** — nécessite **Signaux navals** | +20 %. |
| Principe **Suprématie maritime**, palier 1 | +10 %. |
| Même principe, palier 2 | +10 % du palier actif. |
| Même principe, palier 3 | +10 % du palier actif. |

- [ ] Tester les cinq lignes séparément, y compris l'application aux membres éligibles du bloc et le maintien des bonus de navire amiral. Les trois définitions de palier ne signifient pas automatiquement +30 % cumulés.
- [ ] Relever la projection elle-même ; ne pas exiger la même variation en pourcentage du prestige ou de l'implication régionale, qui ont d'autres facteurs/plafonds. Une bonne infobulle de loi ne suffit pas à valider son effet.

### B3. Objectifs de guerre — #32

Faire les trois scénarios suivants. La guerre d'indépendance américaine sert de témoin de démarrage ; elle ne remplace pas ces trois objectifs. La guerre régionale **Irak / Perse**, avec conquête de Bassora notamment, est un point de départ existant pour la conquête d'État.

| Scénario | Action et résultat attendu |
| --- | --- |
| **Conquérir un État** | Relever l'infamie et sa décomposition lors de l'ajout d'un objectif neuf dans une partie appropriée. Dans une guerre active, occuper l'objectif et attendre l'exigence/le délai d'application affichés : l'État doit pouvoir être transféré **avant la paix**, pendant que la guerre continue. Le camp dépossédé reçoit le contre-objectif approprié sans nouvelle infamie ; en présence d'une revendication, il peut s'agir de **Restituer un État**. Sur une copie, reprendre le contrôle et appliquer ce contre-objectif. Conclure la paix et vérifier propriété, fronts et absence de double transfert. |
| **Annexer un pays** | Sur une cible autorisée hors lien impérial interdisant l'annexion, relever l'infamie et ses éventuels facteurs de sujet. Atteindre l'occupation/durée affichées, puis constater l'annexion en cours de guerre. Pour tester le contre-objectif, garder un adversaire éligible encore en guerre : une guerre terminée ne peut pas démontrer cette branche. Vérifier la libération/reprise proposée selon le statut du pays, puis paix et cohérence des sujets/participants. Vérifier séparément le refus d'une annexion interdite par un lien impérial. |
| **Unification** | Utiliser un pays et une sauvegarde où une véritable action d'unification est disponible, avec ses prérequis/candidats corrects. Vérifier l'infamie nulle prévue, l'application en cours de guerre, le contre-objectif et la reprise lorsque la guerre peut continuer, puis la paix. Vérifier les restrictions impériales applicables. Une fenêtre forcée sans candidat valide ne certifie pas ce cas. |

- [ ] Sauvegarder/recharger avant et après une application en cours de guerre : objectifs, propriétaires et participants doivent persister sans réinitialisation ni doublon.
- [ ] Comparer l'infamie de conquête ordinaire au cas impérial autorisé : surcharge appliquée une fois ; ne pas ajouter à nouveau l'ancienne formule ou un double rabais de restitution.

### B4. Conclusions et continuations des journaux — #27

Pour chaque branche réellement exécutée : capture avant conclusion, résultat/événement après conclusion, effets de sortie, puis sauvegarde/rechargement. La récompense, le nettoyage et la continuation doivent arriver **une seule fois** ; les impulsions d'un journal terminé doivent s'arrêter.

| Ensemble | Branches à exercer pour une validation complète du lot correspondant |
| --- | --- |
| **Insurgés américains** | Terminer la chaîne/guerre d'indépendance de manière appropriée : sortie de Révolution américaine et des journaux de soutien/engagement concernés, compteurs et effets de soutien nettoyés, absence de répétition après rechargement. |
| **Pologne-Lituanie** | Réussite de la réforme principale puis des réformes spécialisées lorsqu'elles sont activées : industrie, commerce, éducation, chemins de fer, agriculture, armée et grande puissance. Vérifier les récompenses et les ajouts de journaux suivants. L'affichage seul en A2 ne certifie pas leurs conclusions. |
| **Canada et Frontière du Nord-Ouest** | Canada : conclusion dans les perspectives métropolitaine et coloniale, bouton/continuation et invalidation du journal colonial dans un cas approprié. Nord-Ouest : réussite sur les cinq États Ohio, Wisconsin, Indiana, Michigan et Illinois ; sur une autre copie, expiration à **2 300 jours**. Ne pas attendre une conquête du Mexique. |
| **Deux urbanisations** | **Des fermes aux usines** : sortie du servage et de l'impôt foncier pour activer ; réussite avec moins de 35 % de paysans et industrialistes non marginaux, sous les conditions légales maintenues. **Urbaniser la nation** : activation avec centre urbain incorporé de niveau 5 et absence d'agrarianisme ; réussite avec centres de niveau 5 dans au moins 75 % des États incorporés et au moins un centre incorporé de niveau 10. Vérifier progression, événement et retrait du journal. |
| **Trois migrations** | Sur des pays éligibles d'Amérique du Sud, d'Amérique centrale et de l'Ouest américain : activation, recalcul hebdomadaire de population/objectif, réussite et invalidation si les conditions requises cessent. L'Ouest demande aussi trois États incorporés des Grandes Plaines ou de la côte pacifique. Les objectifs hérités ne sont pas tous identiques : Sud à 1,5 million par État incorporé ; Centre/Ouest initialisés à 1,5 million puis recalculés à 1 million. Ne pas attribuer cette différence antérieure à la migration du format des journaux. |
| **Réformes ottomanes de 1776** | Administration : dix objectifs et seuil de **12 mois**, succès et retrait des malus/allègements actifs. Politique : stabilité **36 mois** et réussite ; sur d'autres copies, crise prolongée et échec ou échéance de **1836**. Après échec, événement de transition le lendemain et activation unique de L'homme malade. Après réussite politique, la crise future grisée ne doit plus rester proposée. Vérifier aussi l'invalidation de l'ancien journal par sa continuation. |
| **L'homme malade et ses sept réformes** | Succès du journal principal après **quatre réformes**, et expiration sur une autre copie (**10 950 jours**). Tester les réussites Syrie, Égypte, économie, éducation, séparatisme, armée et bureaucratie ; chaque réussite crédite une seule réforme. Vérifier revendications/événements, nettoyage culturel et modificateurs attendus. Pour séparatisme, comparer la progression maximale de sécession **inférieure à 50 %**, **égale à 50 %** et **supérieure à 50 %** : progrès/réussite en dessous sous les autres conditions requises, échec au-dessus, aucun de ces deux seuils franchi à l'égalité. Vérifier échecs/invalidations applicables et, si le contenu DLC correspondant est actif, les continuations associées. |
| **Saint-Empire** | Centralisation : unification, perte du titre impérial et priorité lorsque plusieurs issues deviennent vraies. Situation générale : maintien permanent, sortie silencieuse du pays qui cesse d'être éligible. Élection : clôture effective, perte d'éligibilité/électorat et conditions concurrentes ; aucune fausse réussite de la situation permanente. |
| **L'épreuve des quotas de naissance** | Sur un pays ayant réellement cette loi et ce journal : succès à **200**, échec à **0**, puis retrait de la loi dans une autre copie. Vérifier le retour arrière et l'événement seulement dans les cas où la loi existe encore ; contrôler les conditions concurrentes. |

Ne pas jouer jusqu'en 1836 ou pendant trente ans uniquement pour fabriquer une preuve : ces échéances se testent sur des situations préparées et identifiées. Sans ces situations, inscrire les branches correspondantes comme non testées. La mission ne migre pas l'intégralité des journaux historiques encore présents dans le dépôt.

### B5. Cas spécialisés de l'API — #21

Les actions visibles de A et les essais de B1–B4 sont réutilisés : inutile de refaire six lancements identiques. Compléter les cas suivants seulement avec leur contexte réel ; l'absence d'erreur au démarrage ne prouve pas un événement jamais exécuté.

| Famille | Ce qui reste à observer dans une copie appropriée |
| --- | --- |
| IA diplomatique et décrets | Cibles accessibles/inaccessibles pour conquête, soumission, contrainte commerciale/port et protection ; bon refus pour une cible invalide. Décrets autour des seuils de cultures primaires **10/30/50/90 %**, selon leurs opérateurs propres et avec le bon propriétaire d'État. Les poids IA non visibles seront à croiser avec les diagnostics du moteur. |
| Personnages | Succession industrialiste de la Compagnie des Indes orientales dans un cas éligible. Protection temporaire d'un personnage initialement mortel : activation, retrait normal, expiration de secours ; personnage déjà immortel : maintien de sa protection permanente. Pools d'exil avec leurs DLC et personnages de contexte. |
| Navires futurs | Cas éligibles avec dreadnoughts, destroyers, super-dreadnoughts, sous-marins et porte-avions ; seuils de proportions **0,1 / 0,2** selon l'événement. Pré-dreadnoughts du canular et du Potemkine séparément. Les anciennes dépendances de bâtiments navals doivent être résolues avant de certifier le déclenchement complet de ces événements. |
| Dates et initialisation | Fortifications semées dans la fenêtre initiale du **1er janvier 1776**, sans nouveau semis au rechargement d'une campagne avancée ; changements de noms prévus en **1799 / 1801 / 1828**, sur sauvegardes datées appropriées. |
| Mouvements et économie | Mise à jour du mouvement modernisateur après activation de loi ; score social-démocrate correspondant aux sept groupes conservés (**0 à 7**) ; proportions de population des appels migrés. Remises de sécurité au travail aux trois paliers (**−10 / −20 / −30 %**) et débit de la compagnie de carrières de calcaire (**+15 %**) sur les bénéficiaires corrects. |
| Soutien de guerre, témoin partagé | Dans les événements concernés, vérifier une **variation** du soutien, sans écraser sa valeur totale. Si rencontrés : Colère sur le front et Un pacifiste dénonce la guerre, choix aléatoire/garanti distincts et seuil électoral strictement inférieur à **−5**. Cela ne rouvre pas automatiquement les anciennes missions déjà terminées. |

## Retour à fournir après la tournée

En cas de problème : arrêter la branche concernée, noter l'action et la date, conserver la sauvegarde avant/après si possible et faire une capture de la fenêtre ou du message. Il est possible de continuer les autres copies indépendantes.

Les nouveaux logs sont dans le dossier utilisateur **Victoria 3/logs**. Après la session, signaler qu'ils sont prêts à être examinés ; garder la session identifiable avant de relancer plusieurs essais qui pourraient remplacer les traces. Leur analyse doit comparer les anciennes erreurs d'API et les nouvelles erreurs, sans attribuer toute la dette du mod à ces six lots.

Retour minimal à copier :

| Contrôle | Réussi / échec / non testé + pays, date, sauvegarde ou capture |
| --- | --- |
| #21 — chargement, simulation, rechargement et cas spécialisés réellement faits | |
| #27 — journaux : affichage, branches de conclusion et suites réellement faites | |
| #29 — exemptions, suppression générale, effets et persistance | |
| #30 — les deux lois et les trois paliers | |
| #32 — conquête / annexion / unification et contre-objectifs | |
| #33 — cuivre : marché, construction, mine et pictogrammes | |
| Supplément — saisons/froid, quatre coques cuivrées, cogue et ses améliorations | |

Une carte ne passe à Done qu'après confirmation du périmètre réellement validé. Laisser les branches non exécutées explicites ; une fenêtre correcte ou un lancement réussi ne vaut pas validation des effets absents de l'essai.

## Sources du regroupement

- Tableau de bord Project 1 : colonne In review consultée le 8 novembre 2026 ; issues #21, #27, #29, #30, #32 et #33.
- Protocoles locaux : `V1_15_ISSUE21_REVIEW_2026_11_08/RUNTIME_PROTOCOL.md`, `V1_15_ISSUE29_TOLL_TREATIES_2026_11_08/RUNTIME_PROTOCOL.md`, `V1_15_ISSUE30_NAVAL_PROJECTION_2026_11_08/RUNTIME_PROTOCOL.md`, `V1_15_ISSUE32_WAR_GOALS_2026_11_08/RUNTIME_PROTOCOL.md`.
- Lots journaux : `V1_15_ISSUE27_JOURNAL_BATCH1_2026_11_06.md`, `V1_15_ISSUE27_SICK_MAN_2026_11_07.md`, `V1_15_MIGRATION_URBANIZATION_2026_11_07/REPORT.md`, `V1_15_RUNTIME_FEEDBACK_2026_11_07/REPORT.md` et `V1_15_USA_INDEPENDENCE_2026_11_07/REPORT.md`.
- État ottoman/russe et supplément : `V1_15_OTTOMAN_VISIBILITY_RUSSIAN_RELIGION_2026_11_08/REPORT.md`, `V1_15_COLD_NAVAL_FOLLOWUP_2026_11_08/REPORT.md`.
- Contrôles des données actuelles : bien cuivre hérité du vanilla, icône de mine native, lois/localisations navales et guerre régionale initiale dans les fichiers locaux. Les anciennes mentions de #33 décrivant une livraison seulement distante ne remplacent pas cet état installé.

Les dossiers cités sans préfixe sont relatifs à `docs/reports/compatibility`. Les sources sont des documents de référence ; seules les actions cochées et confirmées par le joueur constitueront des résultats d'essai.


## Retour joueur du 8 novembre 2026

Le mainteneur rapporte avoir teste les sept points du resume, sauf l unification, et autorise la cloture du reste. Les missions **21, 27, 29, 30 et 33 sont Done** ; la **32 reste In review uniquement pour l essai moteur d unification**. Le recu detaille et les limites de cette attestation figurent dans [HUMAN_ACCEPTANCE_2026_11_08.json](HUMAN_ACCEPTANCE_2026_11_08.json). Les cases du protocole initial ci-dessus ne sont pas cochees artificiellement : les mesures et les scenarios specialises n ont pas ete fournis individuellement.

Le defaut de capacite de marines de la cogue signale pendant cette session a recu un correctif local distinct : bonus des amenagements moyen/superieur **+0,05 / +0,15**, avec verification moteur apres correctif encore a faire. Les deux statuts ottomans provisoires sont reecrits en francais et en anglais apres acceptation fonctionnelle ; leurs expressions dynamiques et les mecaniques sont conservees.

Precision de lecture de B4 : le seuil politique ottoman est de **36 points de consolidation**, et non necessairement 36 mois. Un mois stable apporte un point, ou deux apres resolution du fardeau administratif. Le seuil et les calculs du jeu ne changent pas.
