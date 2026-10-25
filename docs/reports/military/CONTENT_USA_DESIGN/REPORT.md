# CONTENT-USA-DESIGN — architecture et feuille de route

Statut : **DESIGN_ONLY**. Aucun journal, événement, loi ou traitement périodique nouveau n'est chargé par le jeu dans ce lot. Les nombres ci-dessous sont des paramètres proposés à tester, pas des effets installés ou des mesures historiques.

## Contrat d'intégration

La dépendance de départ est MIL-USA + BAL-USA-REVOLUTION-R1 + USA-COMMANDERS-1776, puis une nouvelle partie validée en jeu. Ne pas convertir automatiquement les anciennes sauvegardes : prévoir un numéro de version et un mode désactivé sans migration financière implicite.

| Système | Historique | Faisabilité locale | Effets proposés | État |
|---|---|---|---|---|
| Minutemen | milices locales et compagnies volontaires distinctes | variantes de lois natives possibles ; modèle militaire à tester | mobilisation rapide, contingent limité, coût d'instruction | planifié ; variante littérale de la sécurité intérieure rejetée |
| Ferveur | engagement sensible à la situation, au recrutement, aux revers et au soutien | événements de bataille observables ; pertes et pénuries fines non démontrées | trois états exclusifs de moral, sans attaque/défense | planifié |
| Aide française | dons, matériel et prêts de nature distincte, avant/après 1778 | transferts de trésorerie possibles ; registre spécifique indispensable | coût français égal au transfert, dette seulement si consentie | planifié |
| Échos | circulation sélective des idées et contre-exemples | événement d'issue puis ciblage limité des pays | choix politiques locaux, aucun effet mondial uniforme | planifié |
| Personnalités fondatrices | acteurs d'âges, fonctions et opinions différentes | personnages, rôles et vie observables | options institutionnelles conditionnées à leur présence | planifié |

La conception n'ajoute pas prématurément un prototype actif : une variante de loi peut recalculer les centres militaires ; un registre de dette touche les deux économies ; des généraux sans affectation restent à vérifier. Les dépendances manquantes sont des tests moteur et des choix d'échelle, explicitement listés, pas une demande d'autorisation supplémentaire.

## 1. Minutemen : ne pas confondre garde nationale et modèle d'armée

Le [NPS, The Militia and Minute Men of 1775](https://home.nps.gov/mima/learn/historyculture/the-militia-and-minute-men-of-1775.htm) distingue la milice obligatoire et les compagnies volontaires de minute men. En Massachusetts, l'entraînement ordinaire était de six jours annuels ; certaines compagnies volontaires s'exerçaient deux jours par semaine et recevaient équipement et rémunération des communautés. Organisation municipale, disponibilité rapide et durée de service locale ne signifient donc pas absence d'instruction. Les réalités des autres colonies varient ; ce modèle ne doit pas être présenté comme uniforme de la Géorgie au Massachusetts.

Dans le mod actuel, `law_national_guard` appartient à `lawgroup_internal_security`, requiert professional_civil_policing et finance une institution. Ses effets comprennent radicalisme, résistance aux coups, catastrophes et conscription. Copier cette loi importerait des effets étrangers à l'organisation des compagnies de 1775.

**Choix proposé :** `law_aor1776_minutemen`, variante nationale de `law_national_militia` dans `lawgroup_army_model`, à créer dans un nouveau fichier. Le `parent` et `is_visible` des variantes sont démontrés par `law_warrior_caste` dans le mod et le vanilla. Restreindre visibilité ET adoption/imposition aux USA dans la situation révolutionnaire prévue ; empêcher qu'un autre pays puisse l'imposer à une colonie étrangère. Une simple restriction d'interface ne suffit pas.

Paramètres de prototype : taux de conscription 0,03 ; plafond de centres 25 ; casernes 25 ; vitesse de mobilisation +0,20 ; instruction +0,10 ; aucun bonus offensif/défensif, anti-révolution, de sécession ou d'ordre public. Les 25 casernes permettent de conserver les 9 réguliers du Massachusetts ; copier le plafond 5 de la milice nationale détruirait cette cohérence. La loi doit énoncer ses propres modificateurs au lieu de supposer une addition automatique à ceux du parent. Retirer la restriction aux seuls paysans est un changement important à tester sur les populations et l'économie civile.

L'instruction représente la préparation locale et doit avoir un coût visible proposé de +0,05 sur les dépenses de biens militaires. Ne pas attribuer un malus global d'expérience aux minute men sous prétexte qu'ils sont miliciens. L'absence des avantages de l'armée professionnelle et les durées de disponibilité représentent leurs limites ; une crise de renouvellement d'engagement sera événementielle, sans supprimer au hasard des bataillons.

Conserver light_infantry_tactics comme prérequis du prototype national, au lieu de donner permanent_engineer_services aux USA. Le déblocage propre doit être vérifié avec l'héritage du parent. Après l'indépendance, permettre de conserver la loi ou d'entamer une réforme normale vers l'armée professionnelle lorsque ses prérequis sont satisfaits. Aucune activation forcée au départ : le premier prototype est une décision volontaire sur une nouvelle partie de test, avec sauvegarde avant changement et comparaison des centres à J+1, J+7 et M+1.

Acceptation : loi invisible et inadoptable pour GBR/FRA/SC2/BRZ, coûts affichés, 13 réguliers et 15 conscrits préservés, aucune consommation double des effectifs lors de la réforme, sortie de guerre ne détruisant pas les recruteurs. Tester également une monarchie américaine alternative et un retour sous tutelle.

## 2. Revolutionary Fervour : événements bornés et effets exclusifs

La [correspondance de ravitaillement étudiée par les Washington Papers](https://washingtonpapers.org/resources/articles/supply-problems-plagued-the-continental-army-from-the-start/) documente les difficultés d'armes, de finances et de renouvellement. Le [NPS sur Valley Forge](https://home.nps.gov/vafo/learn/historyculture/valley-forge-history-and-significance.htm) décrit aussi la cohésion et les changements de recrutement ; il ne s'agit pas d'un enthousiasme qui disparaîtrait automatiquement à date fixe.

Observations techniques dans le vanilla canonique :

| Besoin | Preuve disponible | Usage retenu |
|---|---|---|
| Victoire/défaite terrestre | `00_code_on_actions.txt`, on_battle_won/on_battle_lost : root pays, enemy_country, battle, attacker/defender, state | utilisable après branche de test ; exclure les hooks de bataille vide |
| Compter un succès événementiel | `ip4_on_actions.txt`, carlist_war_battle_score | variable modifiée lors du hook, pas une recherche quotidienne de toutes les batailles |
| Guerre, sujet, issue | journal américain existant | gardes d'activation et nettoyage |
| Argent disponible et transfert | `british_raj_events.txt`, gold_reserves et add_treasury | crise financière et choix de dépense observables |
| Pertes exactes et ratio de ravitaillement | pas de déclencheur numérique fiable démontré dans cet audit | **bloqué pour V2**, ne pas inventer un identifiant de script |
| Événement politique ou aide acceptée | effets de l'option contrôlés par le mod | changement du score dans le même effet |

V1 proposée : variable américaine `aor1776_fervour` bornée entre 0 et 100, initialisée à 50 une seule fois. Première victoire non vide contre GBR ou un participant à cette guerre : +5 ; première défaite correspondante : −5 ; chacune a un délai de 90 jours et une garde de campagne pour limiter les microbatailles répétées. La liste des ennemis doit provenir de la guerre concernée, pas de toute guerre américaine. Si le rattachement à cette guerre n'est pas démontré, limiter V1 à GBR et documenter la limite.

Une aide française réellement payée donne +5 une seule fois par tranche diplomatique ; une déclaration politique adoptée +5 une fois ; un refus de financer un renouvellement donne −5 une fois. Les dates débloquent les événements possibles mais ne font pas décroître le score d'elles-mêmes. Ni découverte de technologie ni présence d'une célébrité ne donnent un bonus gratuit.

Trois états exclusifs : faible (<35), ordinaire (35–65), élevé (>65). Propositions relatives au niveau R1 : faible récupération −0,05 et perte de moral +0,05 ; ordinaire 0 ; élevé récupération +0,05 et perte −0,05. Chaque changement retire d'abord les trois modificateurs possibles puis applique au plus un seul. Pas d'attaque/défense/expérience supplémentaire. Le cumul national R1 + ferveur doit rester entre récupération +10 et +20 %, perte de moral −5 et −15 %, avant lois et chefs. À la paix finale, retirer tous ces effets, les délais et les variables temporaires.

Coût de calcul : un filtre constant par hook de bataille, effet seulement USA pendant la guerre ; aucun `every_country` ou parcours mondial quotidien. Un contrôle mensuel américain répare seulement les variables/modificateurs pendant le journal actif ; pas de traitement de toutes les unités. Ne pas compter un même succès par le hook et par un événement narratif.

Tests : victoire, défaite, bataille vide, autre guerre, combat allié, répétition dans les 90 jours, franchissement exact de 35/65, sortie de guerre, annexion/suppression USA, chargement de sauvegarde et double appel. Tant que le rattachement des pertes ou des pénuries à une formation n'est pas vérifié, ces facteurs restent des événements de choix explicites, pas des capteurs fictifs.

## 3. Aide française : trois comptes et des engagements consentis

L'[Office of the Historian](https://history.state.gov/milestones/1776-1783/french-alliance) distingue l'aide clandestine initiale et les deux traités du 6 février 1778. Les hésitations diplomatiques, les agents et les livraisons ne constituent pas une alliance ouverte au 1er janvier 1776. Le soutien officiel doit être une option conditionnelle à la survie américaine, à la diplomatie française et à son financement ; aucune entrée en guerre imposée en 1778.

Le [contrat du 16 juillet 1782, transcription Avalon/Yale](https://avalon.law.yale.edu/18th_century/fr-1782.asp), distingue 18 millions de livres de prêts français, un prêt hollandais garanti, les intérêts et leur remise partielle. Le principal français est échelonné en douze paiements débutant la troisième année après la paix ; le taux mentionné est 5 %, distinct du montage hollandais à 4 %. Il n'impose pas un remboursement intégral immédiat à la victoire. Ce contrat spécifique ne doit pas être appliqué à toute aide antérieure ni traité comme une conversion directe en monnaie du jeu.

Dette existante à migrer : `french_revolution_mod_events.2` est ouvert après la victoire sans montant de prêt enregistré ; le refus donne 25 d'infamie et le paiement prélève 57 700 par semaine pendant 84 mois via debt_usa_big_money. L'événement .3 crédite la France de 57 700 ; les événements .1/.4 peuvent ouvrir une crise française. Le journal français réagit aussi à l'échec américain. **Préserver ces scripts en R1 ne les valide pas historiquement.** Le futur lot doit remplacer cette chaîne dans son ensemble, avec une garde de version empêchant les deux systèmes de facturer le même prêt. Ne pas modifier seulement une infobulle.

Comptes proposés, sur le pays USA avec vérification miroir côté FRA : `aor1776_french_grants_received`, `aor1776_french_loan_principal`, `aor1776_french_loan_interest_due`. Un quatrième compteur de livraisons distingue le matériel des transferts monétaires. Les dons ne deviennent jamais du principal ; un prêt exige acceptation des deux parties, montant et échéancier visibles. Identifier le prêteur réel ; si FRA disparaît, geler l'obligation et ouvrir un choix de succession, sans verser à un tag inexistant.

V1 limitée : offres à choix bilatéral, 180 jours entre tranches ; exemple de calibration 10 000 £ de don ou 20 000 £ de prêt, plafond de principal 100 000 £. Ces montants sont des essais budgétaires, sans équivalence livres tournois/£. Vérifier que FRA possède la somme avant l'exécution finale ; débiter puis créditer exactement la même valeur dans le même effet. En cas de refus, d'absence du pays ou de fonds insuffisants : aucun crédit, aucune dette et aucune hausse de ferveur. Poser un verrou d'exécution contre le double clic ou le chargement d'événement. Les effets add_treasury natifs permettent la paire de transferts ; ils ne créent pas automatiquement un contrat de prêt juridique du moteur.

Les livraisons d'armes doivent passer par un mécanisme d'approvisionnement vérifié : acheter des biens ou ouvrir une relation de marché ne livre pas instantanément un stock national abstrait inexistant. En V1, un don pour approvisionnement demeure un transfert financier affecté narrativement ; ne pas ajouter simultanément argent et réduction gratuite du prix des armes. L'aide matérielle détaillée est un sous-lot V2.

Après la paix, ouvrir une négociation si et seulement si le principal est positif. Choix de référence : grâce de trois ans, principal étalé en douze versements annuels, intérêts simples à 5 % du solde après la paix, remise des intérêts de guerre ; ce sont les termes du contrat historique de référence, ajustables par accord du joueur. Proposer aussi un report négocié, une remise ou un refus aux conséquences diplomatiques proportionnées à la somme. Ne pas imposer 25 d'infamie indépendamment de la dette. Le principal et les intérêts payés diminuent leurs comptes séparés, sans devenir négatifs. Aucun transfert mensuel lorsque le compte est nul ; aucun intérêt sur un don.

Validation indispensable : conservation FRA+USA de la trésorerie à chaque tranche, zéro prêt/zéro remboursement, prêt refusé, fonds dépensés avant acceptation, remboursement partiel/anticipé, grâce, nouvelle guerre, changement de régime français, disparition d'un pays, sauvegarde/rechargement et migration désactivée. Les frais budgétaires supplémentaires français doivent venir d'une guerre réelle ou d'un transfert consenti, jamais d'une révolution française automatique parce que les USA ont gagné/perdu.

## 4. Echoes of the Revolution : des destinataires et des choix

La [Library of Congress sur les échanges franco-américains](https://blogs.loc.gov/international-collections/2021/07/the-franco-american-revolution-part-2/) décrit une circulation d'idées et une relation géopolitique. La [lettre de José da Maia à Jefferson du 21 novembre 1786](https://founders.archives.gov/documents/Jefferson/01-10-02-0398) invoque explicitement l'exemple américain pour le Brésil. Cette lettre est tardive et exprime une demande particulière : elle ne démontre ni une révolte brésilienne générale de 1776 ni une causalité unique. L'influence intellectuelle et le précédent institutionnel sont établis dans ces cas ; les coefficients de diffusion proposés restent des abstractions.

Déclencheur unique lors de la résolution du journal USA. Enregistrer victoire/défaite et une liste de pays déjà traités. Parcourir une fois les sujets des couronnes pertinentes et FRA ; la sélection ultérieure de réformateurs européens doit exiger des liens diplomatiques/commerciaux ou une circulation imprimée et un groupe réformateur présent. Ne pas ajouter des effets aux pays simplement parce qu'ils existent en Europe.

| Destinataire | Garde proposée | Choix et effet V1 proposé |
|---|---|---|
| Colonie britannique | encore sujette de GBR, présente dans les Amériques, ni USA ni participant déjà indépendant | victoire : débat sur représentation, concession fiscale payante ou répression avec risque local ; défaite : confiance coloniale temporaire sans verrouiller l'avenir |
| Colonie espagnole | encore sujette de SPA, élites réformatrices présentes et contact avec la nouvelle république | discussion limitée des institutions ; aucune sécession automatique ; la crainte de contagion peut aussi soutenir la Couronne |
| Brésil/sujet portugais américain | même logique avec POR ; diffusion et relais réels nécessaires | option savante/réformatrice tardive possible, pas révolution instantanée ni rôle forcé de Maia s'il n'existe pas |
| France | soutien réellement accordé ou débat intellectuel actif | débat parlementaire/institutionnel selon régime ; coût financier seulement si enregistré ; pas de passage obligatoire aux États généraux |
| Réformateurs européens | pays connecté, groupe réformateur non marginal, institutions compatibles | événement sur une réforme précise, option conservatrice possible ; aucun bonus militaire |
| Couronnes coloniales après défaite USA | implication ou sujets effectivement concernés | confiance locale temporaire, proposition +1 d'approbation du groupe conservateur durant 12 mois, une seule fois |

Les effets de réforme doivent utiliser les mécanismes locaux de mouvement/approbation après validation de leurs scopes. Ne pas appeler un effet générique « +radicalisme mondial ». Aucun changement de loi forcé, de frontière, de révolution française, de guerre napoléonienne ou d'indépendance latino-américaine. Si les contacts ou les réformateurs manquent, aucun événement n'est préférable à une diffusion universelle.

Tests : victoire, défaite, pays annexé/libéré avant issue, FRA neutre, colonies déjà rebelles, couronne disparue, sauvegarde/rechargement, destinataire déjà notifié. Profil de performance : une seule collecte à l'issue, zéro boucle mondiale persistante.

## 5. Founding Fathers : présence vérifiée avant attribution

La catégorie « fondateur » réunit des trajectoires différentes : les signataires de la Déclaration ne sont pas identiques aux délégués de 1787. Voir les [National Archives sur la Déclaration](https://www.archives.gov/milestone-documents/declaration-of-independence) et la [liste des délégués constitutionnels](https://www.archives.gov/founding-docs/founding-fathers).

| Personnalité | Âge au départ | Position à respecter | Rôle futur conditionnel |
|---|---:|---|---|
| Washington | 43 | commandant existant | pouvoir civil seulement après choix institutionnel ; pas président automatique |
| Hancock | 38 | président du Congrès, déjà modèle de dirigeant du mod | médiation entre colonies, pas commandement militaire inventé |
| Franklin | 69 | délégué au Congrès ; pas encore ambassadeur de 1778 | mission diplomatique si vivant, disponible et effectivement envoyé |
| John Adams | 40 | délégué, avec périodes d'absence à vérifier pour la scène choisie | diplomatie/commission législative si nommé |
| Jefferson | 32 | délégué virginien ; la rédaction de juin 1776 reste future | rédaction d'une déclaration seulement si commission et orientation choisies |
| Madison | 24 | comité local de sûreté en 1775 ; pas encore acteur constitutionnel de 1787 | rôle national après entrée effective en politique et débat constitutionnel |
| Hamilton | 18 selon naissance 1757, 20 selon 1755 | jeune militant/étudiant, pas secrétaire au Trésor | finances après nomination et institutions adaptées, sans « génie financier » national initial |

Les notices des [National Archives, Pennsylvanie](https://www.archives.gov/founding-docs/founding-fathers-pennsylvania), [Virginie](https://www.archives.gov/founding-docs/founding-fathers-virginia) et [New York](https://www.archives.gov/founding-docs/founding-fathers-new-york) établissent les carrières de Franklin, Madison et Hamilton. Pour Hamilton, la notice NARA retient 1757 ; la divergence 1755/1757 doit être résolue et documentée avant création, sans fabriquer un jour pour la masquer.

État du code : Hancock est prédéfini par USA_john_hancock_continental_congress ; Washington existe dans l'historique militaire. Aucun modèle actuel de Franklin/Adams/Jefferson/Madison/Hamilton n'a été trouvé dans les historiques/modèles américains ciblés. Leur absence ne doit pas provoquer une création tardive d'un personnage dupliqué ou ressuscité : le futur lot fait un inventaire global des identifiants avant création, puis enregistre chacun par modèle/variable stable.

Filtres démontrés dans le vanilla : `any_scope_character`, `has_template`, `has_role_of_type`, `is_ruler_of_own_country`, `is_busy` et **`is_character_alive`**. Le déclencheur `character_is_valid_for_events` n'est pas un test de vie : il écarte des rôles, exige l'âge adulte et certains drapeaux. Il faut vérifier séparément la vie, le propriétaire, l'exil/emploi, le rôle et la disponibilité du personnage au moment où l'option est affichée ET au moment de son exécution. La syntaxe is_alive ne doit pas être inventée.

V1 : trois décisions à coût et effet réel, aucune collection de bonus de célébrité. Une commission diplomatique peut réduire le coût d'une négociation particulière si Franklin/Adams est disponible ; une commission de rédaction peut débloquer une option institutionnelle si un rédacteur vivant est nommé ; un règlement de dette peut changer un échéancier consenti si le gouvernement a nommé un responsable financier compétent. Hors fonction, le trait personnel n'agit pas sur tout le pays. Les effets exacts et les rôles d'emploi doivent être prouvés par un prototype avant d'ajouter de nouveaux traits.

Les morts/exilés ne sont ni rappelés automatiquement ni remplacés par une copie homonyme. Prévoir une variante anonyme de commission si une fonction doit continuer, avec un coût normal et sans portrait disparu. Une monarchie américaine, une défaite ou une autre constitution peut fermer certaines options et en ouvrir d'autres ; aucune scène ne présuppose la future présidence d'un personnage.

## Exécution proposée, fichiers et validation éditoriale

| Sous-lot | Fichiers nouveaux envisagés | Dépendances / condition de sortie |
|---|---|---|
| USA-MINUTEMEN-P1 | common/laws/1776_minutemen.txt ; décision de test ; FR/EN propres | vérifier héritage du parent, droit d'imposition, centres et effectifs ; pas d'activation automatique |
| USA-FERVOUR-P1 | common/on_actions/1776_usa_revolution.txt ; scripted_effects, static_modifiers et events dédiés | hook de bataille puis événements, exclusions et nettoyage testés ; aucun sondage permanent |
| USA-FRENCH-AID-P1 | events/1776_usa_french_aid.txt ; effets et variables dédiés ; remplacement ciblé chaîne financière | registre et conservation des sommes, migration et interdiction du double système |
| USA-ECHOES-P1 | événements dédiés appelés une fois à l'issue | sélection des destinataires, choix politiques et idempotence |
| USA-FOUNDERS-P1 | modèles/personnages conditionnels, décisions et traits de rôle dédiés | identité unique, vie, fonction, chronologie et absence de résurrection |

Commencer chaque sous-lot par un manifeste d'identifiants et les tests de branches, puis les textes FR/EN. Ne pas toucher aux variantes impériales, cartes, populations, technologies globales, lois générales ou définitions de cavalerie. Les essais de loi et les transitions financières nécessitent une nouvelle partie isolée ; ne pas présenter une réussite de parsing comme un test d'effet.

Conformément à `.agents/agent.md`, ce document est la **première passe technique interne** : compteurs, fréquences, seuils, coûts, remises à zéro et issues. Aucune localisation de journal fictive n'est ajoutée sans consommateur. Après validation humaine du fonctionnement d'un prototype, conserver son explication ici puis effectuer la seconde passe immersive FR/EN dans les clés réellement affichées. Statut éditorial : **technique à valider**, pas « rédaction immersive terminée ».
