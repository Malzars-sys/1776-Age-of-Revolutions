# 1. Résumé

La phase statique E-1 prépare, dans la copie jetable seulement, une portion réelle de `STATE_BOMBAY` détenue par BIC tout en conservant la portion BIC existante de `STATE_WEST_BENGAL`. La portion portugaise d’une province est transférée par une unique mutation, puis reçoit les deux appels de baseline radicale à 1 %. Aucun filtre de `sepoy_mutiny_events.2.e` n’est modifié. Verdict : `READY_FOR_E1_RUNTIME_TEST`.

# 2. État Git initial

Racine : `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork`. Branche : `hotfix-dlc-audit`. HEAD : `5565a75 Validate Sepoy Madras core preservation`. Aucun fichier suivi n’était modifié. Le stash MARATH était présent et n’a fait l’objet d’aucune opération.

# 3. Exception docs/research/technology/

La seule entrée non suivie initiale était `docs/research/technology/`. Elle est restée hors périmètre et inchangée.

# 4. Vérification initiale de la copie

Avant E-1 : 968 fichiers, 24 fichiers de harnais, quatre fichiers C-1, aucun `.git`, aucun `remote_file_id`. Les contrôles du manifeste C-1 applicable donnaient zéro divergence. Le Sepoy de la copie et du fork faisait 63 540 octets, SHA-256 `98C4A50C1DCF2CE79B13AFF82B1FE461651BB99A9B42B002914FD10C338FDCAD`.

# 5. Analyse complète de 2.e

Le bloc complet couvre les lignes 1428–1811 dans le fork et la copie, et 1412–1795 dans la source hotfix et vanilla 1.13. Les quatre blocs ont 384 lignes, 8 096 caractères normalisés LF, et sont strictement identiques caractère par caractère. La localisation vanilla anglaise se trouve dans `localization/english/ip2_02_l_english.yml` lignes 87 et 89 ; la française aux lignes 84 et 86 du fichier français.

Pseudo-flux exact :

1. afficher 2.e si BIC possède une portion quelconque de West Bengal ; poids IA 40 ;
2. libérer les sujets dont la capitale est en North India, South India, Pashtunistan ou Quetta et retirer 500 de levier GBR ;
3. si BIC possède un état de la grande zone Inde/Himalaya/Pashtunistan/Quetta, exécuter les transferts prioritaires ;
4. tant qu’un état BIC de cette zone jouxte un propriétaire receveur sud-asiatique à capitale admissible, parcourir les pays receveurs et leur transférer un état BIC voisin choisi aléatoirement ;
5. effacer le scope temporaire après chaque tour ;
6. appliquer `large_radicals` aux hindous puis aux sunnites de tous les états BIC encore situés en `region_south_india` ;
7. aucun changement de pays : le joueur reste BIC.

# 6. Trigger réel West Bengal

Lignes 1434–1438 : `any_scope_state = { state_region = s:STATE_WEST_BENGAL }`. Comme le scope est BIC, toute portion West Bengal détenue par BIC rend 2.e accessible. Le trigger ne teste ni Bombay ni `geographic_region_bombay_old`.

# 7. Absence ou présence de Bombay dans le trigger

`STATE_BOMBAY` apparaît zéro fois dans le bloc 2.e. Bombay n’est donc pas requis par le trigger. E-1 exige Bombay uniquement dans son propre harnais afin d’observer le comportement réel du script actuel.

# 8. Intention du libellé Bombay

Le libellé « Bombay holds » et le tooltip décrivant la conservation de la géorégion historique de Bombay demandent une retraite vers le noyau occidental. L’omission de Bombay dans les branches de redistribution prioritaires renforce cette lecture. Le noyau concret à conserver est au minimum `STATE_BOMBAY`; West Bengal est le trigger copié erronément de 2.b, pas un second noyau intentionnel démontré. La localisation vise toutefois une géorégion Bombay plus large : E-1 ne prétend pas résoudre cette divergence sémantique.

# 9. Structure des sujets

Les sujets de root dont la capitale est en North India, South India, Pashtunistan ou Quetta deviennent indépendants. Himalaya est absent de cette condition de capitale. Aucun sujet n’est créé, annexé ou modifié par le harnais E-1.

# 10. Branches prioritaires

Les prises prioritaires traitent Madras/CAR, Mandalay et Pegu/BUR, Tenasserim, Travancore, Circars, Kurnool, Delhi, Agra, Awadh et Central Provinces. Elles omettent explicitement `STATE_BOMBAY` et `STATE_WEST_BENGAL`. Elles précèdent la boucle générique.

# 11. Boucle générique

La garde (1740–1764) admet les états BIC en South India, North India, Himalayas, Pashtunistan ou Quetta ayant un voisin dont le propriétaire possède une culture primaire d’héritage sud-asiatique et une capitale en South India, North India, Pashtunistan ou Quetta. La sélection (1779–1793) reprend le même ensemble géographique et exige un voisin appartenant au `prince_scope` courant. Les listes géographiques ne sont pas textuellement dans le même ordre (South/North dans la garde, North/South dans la sélection), mais elles sont logiquement équivalentes.

Réponses obligatoires séparées :

- Une portion BIC de `STATE_BOMBAY` peut rendre la garde vraie : oui, car Bombay est en South India, si elle a un voisin au propriétaire receveur admissible.
- Une portion BIC de `STATE_BOMBAY` peut être sélectionnée : oui, sous la même condition, pour le `prince_scope` propriétaire du voisin.
- Une portion BIC de `STATE_WEST_BENGAL` peut rendre la garde vraie : oui, car West Bengal est en North India, si elle a un voisin admissible.
- Une portion BIC de `STATE_WEST_BENGAL` peut être sélectionnée : oui, sous la même condition pour le receveur courant.
- Les ensembles sont textuellement différents par ordre seulement et logiquement cohérents dans l’état actuel. Ils ne protègent aucun des deux noyaux.

# 12. Protection réelle de Bombay

Il n’existe aucune exclusion `NOT = { state_region = s:STATE_BOMBAY }` dans la garde ou la sélection. Bombay est donc redistribuable. Si le runtime E-1 démontre sa perte, une phase corrective distincte devra exclure `STATE_BOMBAY` à la fois dans la garde et dans `random_scope_state`. Une correction limitée à la sélection est interdite : la garde pourrait rester vraie sans candidat sélectionnable et maintenir une boucle vide.

# 13. Protection réelle de West Bengal

Il n’existe aucune exclusion de West Bengal dans 2.e. West Bengal est donc également redistribuable. Si le runtime le perd, ce résultat devra être documenté séparément ; l’audit statique le classe d’abord comme trigger erroné de 2.e, sans preuve qu’il constitue un second noyau à protéger.

# 14. Effet radical South India

Lignes 1798–1810 : tous les `every_scope_state` BIC encore en `region_south_india` reçoivent `large_radicals` pour les hindous et les sunnites. L’effet est plus large que `STATE_BOMBAY` et s’exécute après la redistribution.

| Occurrence | Ligne fork | Fonction | West Bengal requis | Bombay requis | Bombay redistribuable | West Bengal redistribuable | Risque runtime |
|---|---:|---|---|---|---|---|---|
| trigger 2.e | 1434–1438 | accès option | oui | non | n/a | n/a | option ouverte sans Bombay |
| branches prioritaires | 1481–1738 | transferts nommés | non | non | pas ici | pas ici | aucun noyau protégé ensuite |
| garde while | 1740–1764 | existence d’un candidat | conditionnellement admissible | conditionnellement admissible | oui | oui | boucle alimentée par l’un ou l’autre |
| random_scope_state | 1779–1793 | état transféré | conditionnellement sélectionnable | conditionnellement sélectionnable | oui | oui | perte possible du noyau |
| effet final | 1798–1810 | radicaux South India | non | non | effet seulement si encore BIC | hors zone | absence cohérente si Bombay a déjà quitté BIC |

# 15. Baseline des portions Bombay

La seule définition historique trouvée crée quatre portions : POR, MARATH, SAT et KHP ; aucun autre propriétaire. Aucun `controller` séparé n’est déclaré, donc le contrôle initial suit le propriétaire. Totaux de pops historiques : POR 446 391 ; MARATH 11 802 465 ; SAT 742 713 ; KHP 517 691.

# 16. Portion POR

Scope `s:STATE_BOMBAY.region_state:POR`, province `x51F0A0`, également port et prime land de la région. Population : 446 391, dont 75 852 marathis hindous, 364 858 marathis catholiques et 5 681 Portugais catholiques ; aucune pop sunnite initiale. État non incorporé. Bâtiments : centre de commerce, rizière niveau 2 et port niveau 1, propriétés POR. POR est reconnu, culture primaire portugaise, capitale `STATE_ESTREMADURA`, rival des Pays-Bas, relation GBR +50, et possède de nombreux autres territoires européens, africains et asiatiques. Il survit au transfert. Sa culture primaire non sud-asiatique l’exclut comme receveur de la boucle. La province est topologiquement intégrée au Bombay partagé et fournit une portion BIC mesurable susceptible d’être redistribuée vers un voisin admissible.

# 17. Portion MARATH, lecture seule

Scope `region_state:MARATH`, 25 provinces, 11 802 465 pops ; fortes populations hindoues, sunnites, chiites et protestantes, plus des minorités européennes, parsies et juives. Incorporée par défaut ; bâtiments administratifs, chantier naval, construction, artillerie, pêche, port et exploitation forestière. MARATH est hindou, culture primaire marathi, capitale Bombay, royaume non reconnu, maître de SAT/KHP/GAR/GWA et receveur admissible. Cette portion et toute donnée MARATH restent strictement en lecture seule.

# 18. Portion SAT

Scope `region_state:SAT`, dix provinces. Population 742 713 : 675 337 hindous et 67 376 sunnites. Aucun bâtiment explicite dans le bloc Bombay. SAT est une principauté non reconnue, culture primaire marathi, capitale Bombay et vassal de MARATH ; il est receveur admissible. Son transfert supprimerait son unique portion/capitale attestée et risquerait de le rendre sans territoire : rejeté.

# 19. Portion KHP

Scope `region_state:KHP`, trois provinces. Population 517 691 : 456 794 hindous et 60 897 sunnites. Aucun bâtiment explicite dans le bloc Bombay. KHP est une principauté non reconnue, culture primaire marathi, capitale Bombay et vassal de MARATH ; il est receveur admissible. Son transfert supprimerait son unique portion/capitale attestée et risquerait de le rendre sans territoire : rejeté.

# 20. Portion retenue

POR est retenu : `s:STATE_BOMBAY.region_state:POR`, propriétaire avant POR, après BIC, province `x51F0A0`, 446 391 pops, 75 852 hindous ciblables. Le Portugal survit, aucun sujet n’est affecté, la portion est petite et mesurable, et sa topologie dans Bombay permet le test de redistribution. L’absence initiale de sunnites n’empêche pas l’appel sunnite exact ; le signal hindou est suffisamment profond.

# 21. Portions rejetées

MARATH est interdit et expérimentalement trop central. SAT et KHP possèdent des baselines religieuses plus mixtes mais leur unique territoire/capitale serait menacé. POR est donc le seul choix respectant simultanément sûreté, survie de l’ancien owner, faible mutation diplomatique et ordre de préférence.

# 22. Mutation exacte

```text
s:STATE_BOMBAY.region_state:POR = {
    set_state_owner = c:BIC
}
```

Une mutation territoriale, aucun autre `set_state_owner`.

# 23. Effets secondaires

Les bâtiments et pops de la portion passent avec l’état à BIC. Le Portugal perd seulement cette province et conserve son existence, sa capitale, ses autres territoires, son sujet BRZ et ses relations. Aucun contrôleur, capitale, culture, religion, sujet ou autre portion n’est modifié explicitement. Une nouvelle partie annule naturellement le setup ; aucune restauration automatique n’existe.

# 24. Baseline radicale

Après le transfert, deux appels seulement ciblent `s:STATE_BOMBAY.region_state:BIC` : hindou puis sunnite, tous deux `very_small_radicals` (1 %). Aucun autre state, aucune portion tierce et aucune pop hors BIC ne sont ciblés.

# 25. Temporalité des deux ticks

Le runtime préparera le 1er janvier, observera le 2 janvier sans conclure, puis attendra le second tick quotidien du 3 janvier avant validation profonde ou visible de la baseline.

# 26. Namespace et identifiants

Namespace `zz_sepoy_test_e1`; décisions `zz_sepoy_test_e1_prepare` et `zz_sepoy_test_e1_open_event`; event `zz_sepoy_test_e1.1`; marqueur `zz_sepoy_test_e1_ready`; dix clés de localisation prescrites. La recherche préalable dans fork, copie et vanilla a trouvé zéro conflit.

# 27. Décision de préparation

Visible seulement au joueur BIC, exige `is_player = yes`, `c:BIC ?= this` et marqueur absent, chance IA zéro. Son trigger évalué confirme West Bengal BIC, Bombay POR existant, absence de Bombay BIC et pop hindoue/sunnite ciblable. `when_taken` ouvre uniquement l’event de préparation et ne mute rien.

# 28. Event de préparation

Country event sur root BIC avec exactement deux options. L’option explicite exécute dans l’ordre : transfert POR→BIC, baseline hindoue, baseline sunnite, `set_variable`. L’annulation n’a aucun effet. Aucun event Sepoy réel n’est appelé ici.

# 29. Décision d’ouverture

Visible seulement au joueur BIC avec marqueur. Elle vérifie West Bengal BIC réel, Bombay BIC réel/non vide en South India, disparition de la portion POR et pops ciblables. Chance IA zéro ; aucune mutation ; un seul `trigger_event = { id = sepoy_mutiny_events.2 popup = yes }`. Aucun `default_option` ni choix automatique.

# 30. Custom tooltips

Les triggers visibles complexes des décisions et le trigger complexe de l’event sont enveloppés dans des `custom_tooltip` réellement évalués, suivant les modèles A-3/B-1/C-1. Trois occurrences, toutes localisées via les deux clés tooltip minimales.

# 31. Localisations

Les dix clés existent en anglais et français. Elles décrivent E-1 jetable, owner POR, mutation unique, West Bengal inchangé, Bombay BIC temporaire, baseline 1 %, attente au 3 janvier, choix manuel destructif 2.e, sauvegarde immuable, interdiction des saves A/B/C, absence de restauration et distinction E-2/E-3.

# 32. Contrôles BOM/LF

Les quatre fichiers E-1 commencent par `EF BB BF`, sont UTF-8 valides, LF uniquement, sans CR. Les scripts ont des accolades équilibrées et portent la bannière exacte `DISPOSABLE E-1 TEST HARNESS - DO NOT COPY TO MAIN MOD`.

# 33. Validation statique

Deux décisions, un event, deux options, un marqueur, un `set_variable`, un `set_state_owner`, deux `add_radicals_in_state`, un appel à event 2, zéro option automatique, zéro console, zéro boucle et zéro hasard dans le harnais. West Bengal n’est jamais muté ; aucune portion MARATH, Bengal, Madras ou Travancore n’est mutée. La copie compte 972 fichiers et 28 harnais.

# 34. Résumé du manifeste

Le manifeste recense les quatre nouveaux E-1, les 24 anciens harnais, les Sepoy et journaux fork/copie, les descripteurs et marqueur jetable, puis les deux livrables C1U. Il contient tailles, SHA-256 et contrôles d’encodage disponibles.

# 35. PLAN RUNTIME E-1 CONDENSÉ

Une seule session : (1) nouvelle partie BIC au 1er janvier ; (2) contrôler West Bengal BIC ; (3) relever toutes les portions Bombay ; (4) préparer E-1 ; (5) confirmer l’unique transfert ; (6) confirmer MARATH/SAT/KHP inchangés ; (7) relever tick 0 ; (8) passer au 2 sans conclure ; (9) passer au 3 ; (10) vérifier la baseline ; (11) sauvegarde pré-2.e immuable ; (12) ouvrir manuellement ; (13) confirmer 2.e ; (14) choisir uniquement 2.e ; (15) vérifier terminaison ; (16) vérifier joueur BIC ; (17) relever Bombay préparé ; (18) relever West Bengal ; (19) identifier le receveur si Bombay est perdu ; (20) contrôle rapide COO/JEY et principaux transferts ; (21) sauvegarde post-option ; (22) ticks jusqu’au 5 seulement pour UI ; (23) sauvegarde finale ; (24) fermeture unique ; (25) Rakaly/logs après fermeture ; (26) aucune session GBR ; (27) aucune relance.

# 36. Critères territoriaux

Avant option : West Bengal BIC, exactement la province POR de Bombay passée à BIC, MARATH/SAT/KHP inchangés. Après 2.e : boucle terminée, joueur toujours BIC, owner de la portion préparée identifié, West Bengal relevé séparément, aucune conclusion de protection déduite d’un simple affichage agrégé.

# 37. Critères radicaux

Chercher profondément `large_radicals` dans les pops hindoues et sunnites de Bombay si la portion reste BIC. Si elle quitte BIC avant le bloc final, documenter que l’absence d’effet final est cohérente avec l’ordre du script. La baseline E-1 est validée seulement après le second tick du 3 janvier.

# 38. Risques restants

Bombay et West Bengal sont tous deux admissibles à la garde et à la sélection selon leur voisinage. Le caractère aléatoire du receveur/état impose la sauvegarde immuable. La portion POR n’a aucune pop sunnite initiale ; le contrôle sunnite peut donc être nul sans invalider le signal hindou. L’audit d’adjacence détaillé devra être confirmé par le runtime.

# 39. Verdict

`READY_FOR_E1_RUNTIME_TEST`

# 40. Fichiers créés

Copie : quatre fichiers `zz_sepoy_functional_test_e1*`. Fork : ce rapport et `HOTFIX_5C2E4C1U_E1_HARNESS_MANIFEST.csv`. Aucun autre fichier n’est autorisé ni attendu.

# 41. Confirmation fichier Sepoy

Le fichier Sepoy n’a pas été modifié : 63 540 octets, SHA-256 attendu dans fork et copie.

# 42. Confirmation anciens harnais

Les 24 anciens harnais, dont les quatre C-1, restent inchangés d’après les contrôles de référence et le manifeste final.

# 43. Confirmation Bengal/Madras/Travancore/MARATH

Aucune mutation ne cible Bengal, Madras, Travancore, `STATE_TRAVANCORE` ou une portion/donnée MARATH. Le seul état muté est la portion POR de `STATE_BOMBAY` dans la copie jetable.

# 44. Confirmation docs/research/technology/

Le répertoire non suivi `docs/research/technology/` n’a pas été lu pour modification et n’a pas été changé.

# 45. Confirmation stash MARATH

Le stash MARATH est intact ; aucun `apply`, `pop`, `drop` ou autre changement de stash n’a été exécuté. Aucun commit automatique n’a été créé.
