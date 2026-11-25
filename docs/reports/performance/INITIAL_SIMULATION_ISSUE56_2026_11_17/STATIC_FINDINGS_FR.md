# Analyse statique des charges — issue 56

Référence : main bd776919f625016cb9e63b2359cc04796c681ef5. Analyse du contenu effectivement superposé au jeu Steam 1.15.1, avec les replace_paths de .metadata/metadata.json. Aucun échec de parsing dans STATIC_INVENTORY_RECURRENT.json. Ces inventaires localisent les charges possibles ; ils ne mesurent ni nombre d'appels effectifs ni temps d'exécution.

## Taille du monde et limites des décomptes

| Objet initial défini | Mod 1776 | Vanilla Steam 1836 | Interprétation |
|---|---:|---:|---|
| TAG propriétaires d'États, proxy statique | 646 | 449 | Inclut les décentralisés ; ne compte pas seulement les pays parcourus par every_country |
| Décentralisés dans ce proxy | 246 | 158 | À séparer des pays reconnus/non reconnus/coloniaux |
| Groupes de POP scriptés | 6 815 | 4 483 | +52 %, sans démontrer le coût runtime de chaque groupe |
| Population littérale totale | 837 328 654 | 1 021 666 179 | Le nombre d'habitants est inférieur malgré davantage de groupes |
| Blocs create_building | 4 126 | 3 171 | +30 %, pas un compte de bâtiments employés en jeu |
| Niveaux explicites | 9 404 | 8 699 | +8 %, hors affirmation de rentabilité ou d'emploi |
| Pactes de l'historique | 108 | 140 | Ne compte pas les pactes ajoutés par initialisation, ni le coût de l'IA diplomatique |

Le scope every_country de l'instrumentation retourne 400 pays au pilote du mod ; la différence avec 646 correspond aux 246 décentralisés du proxy. Le nombre de marchés actifs et de routes commerciales n'est pas mesuré. Ne pas assimiler pays, marchés, groupes de POP, niveaux et objets effectifs. Le markets_counter de la sauvegarde est un compteur d'identifiants, pas une attestation du nombre de marchés actifs.

Les stratégies d'IA passent de 37 à 39 définitions, les effets scriptés de 1 380 à 1 535, les triggers de 1 019 à 1 138. Les contributions on_action sont 421 contre 287, mais les noms uniques 322 contre 287 : les extensions additives d'un hook ne sont pas autant de hooks natifs distincts.

## Systèmes suspects et fréquence vérifiée

### Contrôleur impérial : priorité d'expérience, coût encore à mesurer

- common/on_actions/1776_imperial_constitution.txt:2 initialise après le lobby ; :17 effectue le travail mensuel global (adhésions, pactes, retour visuel, réformes, élections selon état).
- common/scripted_effects/1776_imperial_constitution.txt:5473, aor1776_hre_schedule_membership_guard, pose un marqueur de 2 jours et programme aor1776_hre.40 à 1 jour.
- events/1776_imperial_constitution_events.txt:910 : l'événement caché retire le marqueur, restaure les adhésions, actualise le tableau et les votes non engagés au plus tous les 7 jours, appelle le contrôleur de réformes, puis se reprogramme. Il s'agit bien d'une chaîne quotidienne, distincte du hook mensuel.
- common/scripted_effects/1776_imperial_reforms.txt:56 : reform_controller parcourt every_country pour nettoyer une autorité indue avant la condition de chef de bloc. L'absence de DLC de gameplay ne suffit donc pas à affirmer que tout le contrôleur est inactif.
- Le graphe mensuel contient plusieurs dizaines de helpers et de sites de boucles ; les compteurs du graphe ne sont pas une multiplication d'appels garantie, puisque des conditions filtrent les branches.
- Le pilote émet des erreurs récurrentes « already has a journal entry of type je_aor1776_hre_situation ». Elles sont observées ; leur responsabilité dans le temps total ne l'est pas.

DIAGNOSTIC_PREPARATION.json décrit la copie qui supprime seulement la reprogrammation quotidienne. Elle conserve le mensuel, l'historique et les autres helpers. Cette ablation retire volontairement une fonction de gameplay ; elle ne constitue pas une correction équivalente et ne doit jamais être intégrée telle quelle. Un petit gain isolé dans une mesure de 8–10 secondes serait insuffisant pour conclure.

### IA des infrastructures régionales : charge mensuelle plausible

common/on_actions/13_1776_ai_regional_infrastructure.txt appelle l'initialisation pour les pays IA après lobby, puis aor1776_ai_refresh_regional_infrastructure dans on_monthly_pulse_country.

common/scripted_effects/1776_ai_regional_infrastructure_effects.txt:414 réinitialise les réserves, remet à zéro les rangs de PIB, rappelle un classement ordered_scope_state pour dix positions et examine les États dotés de building_railway. Dans le mod ce bâtiment représente aussi routes et canaux : 773 blocs initiaux ne signifient pas 773 chemins de fer modernes.

Le cooldown de 180 jours filtre certaines décisions de PM sains ; il ne suspend pas le contrôleur entier pendant six mois. Les variables de besoins ont également des durées de 180 jours. Le nombre 180 ne prouve donc pas l'explication de la disparition du lag à six mois. Une expérience séparée désactivant le seul hook mensuel permettrait d'en estimer le coût, en conservant le même état initial et le même protocole.

### Initialisation, IA native, économie et marchés : plausibles, non attribués

Davantage de pays et de groupes de POP peuvent multiplier des évaluations natives diplomatiques, politiques, économiques et des caches. Les décisions initiales, les transitions d'emploi/PM, la stabilisation des marchés et les files d'évaluations IA peuvent évoluer au fil des premiers mois. Leurs coûts internes ne sont pas ventilés par le simple suivi CPU du processus.

La constante native NEconomy.NUM_TIMES_TO_UPDATE_TRADE_DURING_INITIALIZATION vaut 10 dans les deux environnements superposés. Les taux d'embauche et les mises à jour de qualifications ne sont pas une preuve d'une phase bloquante de six mois. Le monde 1776 diffère aussi par son économie, ses lois, ses PM et ses constantes démographiques : ne pas attribuer automatiquement toute différence vanilla/mod au seul nombre de pays.

Un rechargement froid d'une sauvegarde après un an est un contrôle discriminant à réaliser : il sépare partiellement les calculs/caches au chargement de la maturation de l'état du monde. Ne pas confondre ce contrôle avec le temps de démarrage du programme.

### Quotas de naissance : travail résiduel même sans loi

common/on_actions/10_1776_birth_quotas.txt:80 appelle mensuellement align_birth_quota_interest_groups, ensure_birth_quota_trial et refresh_birth_quota_demography pour chaque pays. En l'absence de loi active, certains parcours de nettoyage restent possibles, notamment sur les États. La fonction n'est pas prouvée responsable de la lenteur initiale et n'a pas de mécanisme global d'arrêt à six mois identifié ici.

### Laboratoires : coût conditionnel, faible priorité au départ

Le système de surveillance des laboratoires peut programmer du travail tous les deux jours et actualiser des modificateurs. Cependant, aucun building_research_laboratory n'est présent dans l'inventaire initial de 1776. Ne pas classer cette boucle comme coût initial global sans montrer que la condition s'active réellement ou qu'un bâtiment est créé ensuite.

### Journaux, événements et décisions : filtrer les cas réellement actifs

495 définitions brutes de journaux correspondent à 494 noms uniques dans le mod contre 449 vanilla. Les pulses déclarés de journaux sont 187 mensuels contre 183, 75 hebdomadaires contre 74 et34 annuels contre 33. Les cadences natives restent NCountry.JOURNAL_ENTRY_UPDATE_ACTIVE=4 jours et INACTIVE=14 jours.

Le classement de tous les champs d'un journal peut être trompeur : les effets de conclusion ponctuels ne coûtent pas comme une condition réévaluée. STATIC_INVENTORY_RECURRENT.json sépare les champs récurrents et les dispatchs d'on_actions. Plusieurs gros journaux sont hérités du vanilla et bloqués par des DLC ou des dates postérieures à1776 ; par exemple 08_russia_provisional_government.txt est une source vanilla, avec condition dlc019. Il ne faut ni lui attribuer un chemin de mod inexistant ni présumer son activité dans la série sans DLC. Aucun coût CPU par journal n'a été profilé.

### Drapeaux : hypothèse encore ouverte

Les listes de drapeaux passent de 440 à 556, les définitions de 1445 à 1561. Les plus grandes listes ne montrent pas de boucles mondiales dans cet inventaire. Les constantes NGraphics.COA_FLAGS_FRAMES_BETWEEN_UPDATES=30 images et COA_FLAGS_UPDATES_BETWEEN_CLEANUP=20 concernent le rafraîchissement graphique et son nettoyage. Elles ne confirment ni ne réfutent une vérification hebdomadaire des conditions de sélection des drapeaux. Aucune cadence hebdomadaire du sélecteur n'a été établie ici. Il faudrait une ablation cosmétique dédiée ou un profil moteur pour attribuer un coût à cette piste.

## Ce que l'analyse ne justifie pas

Elle ne justifie ni suppression de pays, ni réduction des POP, ni changement de lois, ni désactivation permanente de l'IA ou des journaux, ni intégration de l'ablation impériale. Une optimisation finale demanderait un effet mesuré, répété au-delà de la précision du protocole, et une démonstration distincte de conservation du comportement. Les résultats des expériences doivent déterminer le classement final des causes.
