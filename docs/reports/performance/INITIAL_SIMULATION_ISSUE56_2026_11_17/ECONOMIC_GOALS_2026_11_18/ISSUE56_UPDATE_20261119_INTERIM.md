## Point expérimental — 19 novembre 2026 : contrôleurs IA et objectifs économiques

**Aucune optimisation de production préservant le gameplay n'est validée.** Le signal associé aux 400 contrôleurs non décentralisés est reproduit. Le retrait des objectifs d'extension d'une sauvegarde ne constitue toutefois pas une ablation durable : le jeu les recrée dès les premiers jours.

Cette mise à jour rapporte les résultats réellement acquis. Une nouvelle série contrôlée des priorités de construction est en cours sur le PC Windows local ; les passages non terminés sont indiqués comme tels. L'enquête de simulation reste distincte de [#54 / COMPACT](https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/54).

### 1. Signal IA vérifié et limites de comparaison

Même S0 France du 1er janvier 1776, exécutable Steam **1.15.1**, sans DLC de gameplay, vitesse 5, instrumentation native DAY et observateurs CPU/RAM identiques dans chaque lot. Les durées sont cumulées pour 14/28/56 jours, du 2 janvier au 16 janvier, 30 janvier et 27 février, calendrier moteur de 365 jours.

| Passage | Traitement | 14 j | 28 j | 56 j | Vérification dans les sauvegardes natives |
|---|---|---:|---:|---:|---|
| AI_OFF3R | Tous contrôleurs désactivés | 8 s | 15 s | 30 s | PRE/POST : 646 inactifs |
| AI_ON3 | IA normale, série nocturne | 46 s | 88 s | 155 s | PRE/POST : 646 actifs |
| AI_DEC1 | Décentralisés seuls désactivés | 33 s | 65 s | 120 s | PRE 246 non/400 oui ; POST 246 non/399 oui |
| AI_OTHER1 | Les 400 autres seuls désactivés | 7 s | 15 s | 30 s | PRE/POST : 246 oui/400 non |
| AI_DEC2 | Répétition des décentralisés désactivés | 35 s | 68 s | 123 s | PRE/POST : 246 non/400 oui |
| AI_ON4R | IA normale, série diurne | 39 s | 72 s | 122 s | PRE/POST : 646 actifs |
| AI_OFF4 | Tous désactivés, après le témoin diurne | 7 s | 15 s | 30 s | PRE/POST : 646 inactifs |
| ECN1 | Nouveau témoin économique du 18 novembre | 35 s | 69 s | 124 s | PRE/POST : 646 actifs, objectifs intacts |

La paire diurne reproduit le contraste global en ordre inversé : **122 contre 30 secondes**. Les 155 secondes de nuit et 122 secondes de jour diffèrent d'environ 21 % en durée : **ces références ne sont pas interchangeables**. Les contrastes des cohortes ne sont **pas additifs** et ne donnent pas des parts CPU exclusives.

AI_DEC1 perd le contrôleur JEY (pays 428, contrôleur 643) avant sa sauvegarde de juillet ; la cause n'est pas attribuée. Tous les flags présents sont conformes. La répétition AI_DEC2 conserve les 646 contrôleurs. AI_ON4 interrompu ne fournit que 45/87 secondes : aucun temps sur 56 jours n'est inféré.

Inventaire initial complet : **244 décentralisés avec population enregistrée + deux autres décentralisés S72/S74 + 400 autres pays = 646 contrôleurs**. S72 et S74 possèdent des États en Arizona/Sonora ; leur statistique de population vaut zéro, mais l'absence physique d'objets POP n'a pas été vérifiée. Ils ne sont pas sans territoire. Les 400 autres comprennent 123 reconnus, 258 non reconnus et 19 coloniaux. Aucun contrôleur initial ne reste non classé. Le flag actif du contrôleur du pays humain ne prouve pas une exécution identique à celle des pays IA.

### 2. Extension des bâtiments : retrait vérifié, puis recréation native

Le diagnostic retire seulement les 400 blocs sérialisés `expand_production_buildings`. Les autres objectifs et tous les pays, POP, bâtiments, marchés et contenus historiques sont conservés.

- **EXB1 PRE, 1er janvier :** 646 contrôleurs actifs, 400 objectifs ciblés absents, autres objectifs/payloads conservés.
- **EXB1 POST, 9 mars : les 400 objectifs sont revenus.** Le reçu porte `treatment_verified=false`. Les durées brutes 39/75/130 secondes sont conservées, mais **exclues de toute conclusion sur le coût de l'extension**.
- **EXB3, test court séparé :** les objectifs sont déjà tous revenus dans la sauvegarde native du **4 janvier 1776 à 18 heures moteur**. Ce passage n'est pas un benchmark à vitesse 5.
- L'ancien GOAL_EXPAND1 reste une tentative interrompue sans POST. PM1, retrait de `change_production_methods`, est préparé mais **non lancé** ; sa persistance n'est pas supposée.

La recréation est bornée entre S0 et le 4 janvier au soir. Ni son instant exact, ni son mécanisme, ni le coût des objectifs n'est établi. **Ces résultats n'innocentent pas l'extension ni les PM.**

### 3. Remplacement méthodologique : scores moddés de construction

Une couche diagnostique mince, externe au dépôt, remplace **12 blocs `ai_value` dans neuf fichiers** par leurs constantes de base. Elle conserve tous les contrôleurs et objectifs natifs, les PM, budgets, fréquences IA, routines HRE quotidiennes/mensuelles et contrôleur mensuel régional. Les autres octets des fichiers ciblés restent identiques.

Les préférences de construction peuvent changer : il s'agit d'une **ablation diagnostique, pas d'une optimisation équivalente**. Le contrôle natif de chargement constate exactement les neuf fichiers attendus modifiés parmi **7 411 chemins virtuels**, sans ajout ni suppression.

SCORQ1 a effectivement terminé 52/101/174 secondes, avec 646 contrôleurs actifs et objectifs intacts dans l'autosave native d'avril. Mais ECNQ1 n'a pas simulé : **174 secondes n'ont pas de témoin contemporain exploitable**, et ne doivent pas être comparées arbitrairement aux anciens 124 secondes.

Le 19 novembre, l'utilisateur demande de laisser le grand écran 4K OLED libre. Le laboratoire passe en **1600×900 fenêtré sur le seul écran secondaire GAOMON** ; aucune résolution du bureau ni préférence normale n'est changée. Nouvelle série indépendante prévue : **ECNG1 → SCORG1 → SCORG2 → ECNG2**.

**ECNG1 terminé et validé : 35/67/119 secondes**, CPU moyen sur 56 jours **22,61 % des 16 processeurs logiques** ; autosave native du 1er avril : 646 actifs et objectifs intacts. SCORG1 a chargé les neuf surcharges vérifiées, mais son benchmark n'a pas encore démarré à ce point d'étape : capture Windows `FrameArrived timed out`, action physique de départ demandée à l'utilisateur. Aucun résultat de ce diagnostic n'est annoncé.

Les nouveaux réglages et les anciens lots restent séparés. Les répétitions prévues ne sont pas comptées comme réalisées.

### 4. Référence vanilla réellement terminée

Même Steam 1.15.1 et télémétrie, mod absent, France vanilla du 1er janvier **1836**. Monde initial : 449 contrôleurs, 1,022 milliard de personnes, 27 252 objets POP, 1 156 États ; il diffère du mod en date, économie, technologies, pays et vue.

| Passage, ordre ON puis OFF | 14 j | 28 j | 56 j | CPU moyen 56 j | POST natif du 1er avril |
|---|---:|---:|---:|---:|---|
| VAN_ONQ1 | 13 s | 23 s | 45 s | 26,96 % | 450 actifs |
| VAN_OFFQ1 | 10 s | 18 s | 34 s | 21,25 % | 449 inactifs |

Les 449 contrôleurs initiaux sont retrouvés dans les deux POST. Dans ON, un nouveau pays reconnu NIC apparaît, identifiant 16777948, actif comme tous les autres. Le premier reçu trop strict sur le nombre final est conservé ; sa révision explicite cette naissance sans relâcher les exigences sur les flags.

La seule paire indique −24,4 % de durée en OFF, soit +32,4 % de débit. C'est exploratoire, **pas une estimation causale de la pénalité du mod**. La paire inversée sur le nouvel écran est préparée, pas encore exécutée. L'ancien VAN_ON3 est incomplet et sans POST : l'utilisateur a précisé qu'aucune sauvegarde finale n'avait été faite après le redémarrage. Aucun résultat de 56 jours n'en est inventé.

### 5. État du monde, interprétation et suites

Les snapshots existants montrent une forte baisse des bâtiments à profit négatif (2 188 initialement, 776 dans un POST normal de mars) et des objets POP (31 475 vers 23 734). **Ces évolutions existent aussi avec tous les flags IA désactivés**, et le compteur d'investissements autonomes échoués croît encore dans des mondes rapides. Les dates et branches diffèrent : ce sont des observations descriptives, pas des taux ni des causes mesurés.

Les stratégies sérialisées des 646 pays restent identiques dans le POST normal de mars examiné ; cela n'exclut pas des réévaluations coûteuses des mêmes stratégies. Le monde mature rapide possède davantage d'objets bâtiment et de formations que S0. Les 301 objets de secteur de construction en mars comprennent 197 objets de niveau zéro et représentent 116 niveaux : ne pas les présenter comme 301 secteurs construits. Les 38 090 entrées `country_goal` initiales sont diplomatiques, pas une file de construction.

Les callbacks de score régionaux par candidat sont distincts du contrôleur mensuel régional déjà testé. Le nouveau diagnostic vise cette distinction. Après répétitions, s'ils n'expliquent pas un grand effet reproductible, la priorité reste un **contrôle natif persistant d'une seule catégorie** — rentabilité, construction publique, investissement privé ou choix des PM — avec preuve d'activité effective et témoin contemporain. Le simple retrait de blocs de sauvegarde ne suffit pas.

Le profilage GUI Jomini tenté après EXB1 a affiché des ticks, mais aucune table de coûts exploitable avant fermeture. Legacy/TickTask et les mesures de threads restent partiels et ne donnent pas de pile CPU native complète. La restriction Windows de profilage n'a pas été contournée. Le coût exact, le caractère nécessaire ou redondant du travail et une éventuelle mise en cache équivalente restent **non démontrés**.

### 6. Méthode, préservation et preuves

Les horodatages **natifs** des DAY sont utilisés, pas l'arrivée tamponnée des logs. Résolution de différence <1 seconde ; CPU/RAM du processus à environ 500 ms, incluant le rendu. Les fenêtres 14/28/56 sont imbriquées, pas trois répétitions indépendantes. Activité des autres applications, fréquences et pauses physiques ne sont pas entièrement contrôlées. Aucun FPS ni coût exclusif de fonction n'est revendiqué.

La nouvelle méthode continue au-delà de 56 jours jusqu'à une **sauvegarde native trimestrielle d'avril**. Aucune autosave observée dans la fenêtre de mesure, copies et empreintes après celle-ci. La preuve initiale Q/G est une source préparée vérifiée, **pas une PRE native manuelle**. Les processus sont possédés par leur lanceur et seuls ceux-ci sont fermés ; EXIT −1 d'une fermeture contrôlée n'est pas un crash.

Audit complet du 18 novembre à 18:01 UTC : 2 996 fichiers principaux, 2 996 figés, 80 fichiers normaux, trois fichiers Russie–Kazakh, index/HEAD/exécutable, 472 anciens rapports et 38 anciens outils inchangés. Contrôle de reprise du 19 novembre : profil normal 80/80 et protections examinées inchangés ; audit final de cette nouvelle série encore à faire.

La base courante du lanceur a été copiée et conservée : changements antérieurs de tailles, dates de synchronisation et un statut actif ; **sept compositions de playsets, onze liens de mods et 51 liens DLC inchangés**. Auteur non attribué ; aucune ancienne base restaurée.

Rapports locaux, **non commités** : `docs/reports/performance/INITIAL_SIMULATION_ISSUE56_2026_11_17/ECONOMIC_GOALS_2026_11_18/`, notamment REPORT_FR.md, protocoles, VANILLA_REFERENCE_FR.md et ECONOMIC_INSPECTION_FR.md. Le CSV consolidé et l'audit final restent à produire après les essais en cours. Données volumineuses : `%LOCALAPPDATA%/Temp/aor56_ai_20261117`, profils, runs, actions, sources et `autosave_witnesses`. Aucune sauvegarde ni base SQLite publiée.

**Mod principal, COMPACT, diplomatie Russie–Kazakh, contenu historique et travaux non commités préservés. Aucun correctif expérimental intégré, commité, poussé ou fusionné. L'issue reste ouverte.**

---

## Historique antérieur conservé intégralement
