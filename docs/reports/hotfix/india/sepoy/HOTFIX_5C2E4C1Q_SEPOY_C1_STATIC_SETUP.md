# HOTFIX-5C2E4C1Q — Audit et préparation statique du scénario Sepoy C-1

## 1. Résumé

Cette phase prépare, sans lancer Victoria 3 ni son launcher, un harnais jetable pour tester manuellement `sepoy_mutiny_events.2.c`, la retraite vers Madras. La portion française à une province de `STATE_MADRAS` est transférée à BIC par une unique mutation territoriale. Une baseline déterministe de 1 % est ensuite appliquée aux pops hindoues et sunnites de cette seule portion BIC. Le fichier Sepoy, le gameplay du fork et tous les harnais antérieurs restent inchangés.

## 2. État Git initial

- racine : `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork` ;
- branche : `hotfix-dlc-audit` ;
- HEAD : `1ef66f3 Validate Sepoy Bengal radical effects` ;
- aucun fichier suivi n'était modifié ;
- stash : `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`.

Le commit C1P est donc présent et la barrière Git est satisfaite.

## 3. Exception `docs/research/technology/`

L'unique état non suivi initial était `?? docs/research/technology/`. Cette arborescence a été exclue de tous les travaux, lectures de contenu et écritures C1Q. Elle reste l'exception non suivie autorisée.

## 4. Vérification initiale de la copie Disposable

Avant C-1, la copie contenait exactement 964 fichiers, vingt fichiers de harnais racine/A-1/A-2/A-3/B-1, aucun répertoire `.git` et aucune occurrence de `remote_file_id`. Le fichier Sepoy copie avait 63 422 octets et le SHA-256 attendu `FFB4060E659FB8A30691E26BA5BBDA838650EF11AB1760C89EDACFA2310D9BBE`. Les quatre fichiers B-1 correspondaient à la dernière version C1P et les contrôles de hachage des seize harnais plus anciens étaient stables.

## 5. Sources obligatoires consultées

Les cinq rapports prescrits ont été lus : préparation fonctionnelle C0, runtime radical C1P, correction Bengal C1L, audit Madras 5C2E3C et nettoyage des tooltips A-3 I1. Ils imposent notamment l'attente du second tick journalier, l'emploi de vrais `custom_tooltip` évalués, l'absence de correction gameplay dans C1Q et la préservation intégrale du correctif Bengal.

## 6. Comparaison complète de l'option 2.c

Le bloc complet a été extrait de chaque source :

| Source | Lignes du bloc | Longueur normalisée | SHA-256 normalisé |
|---|---:|---:|---|
| fork | 1037–1420 | 8 046 caractères | `A72B699110588FEEBE225487431803B576952A8674CA72BFEE2267E47604B855` |
| copie Disposable | 1037–1420 | 8 046 caractères | `A72B699110588FEEBE225487431803B576952A8674CA72BFEE2267E47604B855` |
| source hotfix | 1027–1410 | 8 046 caractères | `A72B699110588FEEBE225487431803B576952A8674CA72BFEE2267E47604B855` |
| vanilla 1.13 | 1027–1410 | 8 046 caractères | `A72B699110588FEEBE225487431803B576952A8674CA72BFEE2267E47604B855` |

Les quatre blocs sont identiques octet pour octet après normalisation LF. Les dix lignes de décalage viennent d'une modification antérieure située avant 2.c ; elles ne changent pas 2.c.

## 7. Localisation de l'option

La localisation vanilla anglaise est définie dans `localization/english/ip2_02_l_english.yml:86` et demande de maintenir la Compagnie au sud en se repliant sur Madras. La française est dans `localization/french/ip2_02_l_french.yml:83` et exprime la même intention. Le tooltip `india_retreat_to_madras_tt` est localisé aux lignes anglaise 90 et française 87.

## 8. Trigger d'accès Madras et pondération IA

Dans le fork, `sepoy_mutiny_events.2.c` est nommé ligne 1038. Son trigger, lignes 1043–1047, exige seulement que le root possède au moins un state-scope dont `state_region = s:STATE_MADRAS`. La pondération IA est `base = 50`, lignes 1040–1042. Le transfert de la portion FRA à BIC suffit donc à rendre l'option accessible sans toucher à une autre région.

## 9. Pseudo-flux exact de 2.c

1. Vérifier qu'au moins une portion de `STATE_MADRAS` appartient à BIC.
2. Si BIC a des sujets ou sous-sujets dont la capitale est en Inde du Sud, en Inde du Nord, au Pashtunistan ou à Quetta, parcourir les sujets directs correspondants, les rendre indépendants et retirer 500 de levier GBR lorsque ce scope existe.
3. Si BIC possède encore un state dans les régions géographiques admises, exécuter les cessions prioritaires.
4. Créer la Birmanie depuis Mandalay si nécessaire et lui donner Pegu si présent.
5. Céder Gujarat à BER quand possible.
6. Céder Tenasserim à BUR, sinon SIA, sinon créer KRN.
7. Céder Travancore à COC, sinon TRA.
8. Céder Delhi à MUG ou créer MUG ; céder ensuite Agra à MUG.
9. Créer AWA depuis Awadh, sinon céder Awadh à MUG.
10. Céder Central Provinces à NAG.
11. Céder Bombay à SAT, sinon KHP.
12. Tant qu'un state BIC admissible a un state voisin dont le propriétaire est un receveur admissible, parcourir les pays receveurs admissibles et céder aléatoirement à chacun un state BIC voisin admissible s'il en existe un.
13. Répéter jusqu'à disparition de toute paire state BIC/receveur voisin admissible.
14. Sur chaque state restant à BIC dans `region_south_india`, appliquer `large_radicals` aux religions hindoue et sunnite.
15. Le pays joué reste BIC ; aucun changement de tag, de joueur ou de pays contrôlé n'est effectué par 2.c.

## 10. Indépendance des sujets

La garde emploie `any_subject_or_below` aux lignes 1050–1057, mais l'effet interne sélectionne `every_country` avec `is_subject_of = root` aux lignes 1061–1075. L'effet vise donc les sujets directs répondant au filtre de capitale. `make_independent = yes` est exécuté ligne 1071. Cette nuance sujets/sous-sujets devra être observée dans la session BIC, sans contrôle GBR séparé.

## 11. Branches prioritaires

Le bloc prioritaire couvre Mandalay/Pegu/BUR, Gujarat/BER, Tenasserim/BUR/SIA/KRN, Travancore/COC/TRA, Delhi/Agra/Awadh/MUG/AWA, Central Provinces/NAG et Bombay/SAT/KHP. Il contient treize appels `set_state_owner` possibles au total. Il ne contient aucune branche prioritaire dédiée à `STATE_MADRAS` et aucune exclusion Madras.

## 12. Boucle générique et filtres

Les states redistribuables sont ceux de `region_south_india`, `region_north_india`, `region_himalayas`, `STATE_PASHTUNISTAN` ou `STATE_QUETTA`. Un receveur doit avoir au moins une culture primaire portant `heritage_group_south_asian` et une capitale en Inde du Sud, en Inde du Nord, au Pashtunistan ou à Quetta. Le filtre de capitale n'inclut pas `region_himalayas`, même si le filtre des states l'inclut. La sélection est un `random_scope_state` voisin du receveur courant.

## 13. Condition de terminaison, effet final et territoire conservable

La boucle s'arrête lorsqu'aucun state BIC dans le périmètre ne possède de state voisin appartenant à un pays répondant aux filtres culturels et de capitale. BIC ne peut conserver que les states restants qui n'ont plus de receveur voisin admissible, ou ceux hors du périmètre. Les deux appels finaux, lignes 1411–1418, ajoutent `large_radicals` aux pops hindoues et sunnites de tous les states encore BIC en Inde du Sud. Madras peut donc être radicalisé seulement s'il a survécu à la boucle.

## 14. Intention du noyau de Madras

Le libellé et le trigger indiquent une retraite vers Madras et supposent un noyau BIC au sud. Cependant, l'implémentation ne réserve pas ce noyau avant d'exécuter le répartiteur générique. C-1 construit le plus petit noyau réel possible afin de mesurer ce comportement, pas afin de le corriger ou de le neutraliser.

## 15. Protection réelle du noyau

Il n'existe aucune protection explicite de `STATE_MADRAS`, ni `NOT`, ni exclusion de state-region, ni garde propriétaire dédiée dans la boucle. Une portion BIC de Madras reste admissible comme n'importe quel state de `region_south_india`. La conservation de Madras est donc un risque fonctionnel à tester ; ce rapport ne présume pas du résultat runtime.

## 16. Table des occurrences redistributives

| Occurrence | Ligne(s) fork | Fonction | Madras admissible | Exclusion présente | Risque |
|---|---:|---|---|---|---|
| garde avant priorités, `any_scope_state` | 1080–1088 | décide si le bloc prioritaire s'exécute | oui, via `region_south_india` | non | Madras participe au constat de territoire restant |
| garde du `while`, `any_scope_state` | 1351–1372 | exige une paire state BIC/voisin admissible | oui | non | la présence d'un voisin sud-asiatique maintient la boucle |
| `any_neighbouring_state` | 1359–1371 | valide le propriétaire receveur voisin | oui | non | PUD peut rendre le noyau Madras redistribuable |
| `every_country` | 1374–1385 | énumère les receveurs culture/capitale | indirectement | aucune exclusion Madras | tout receveur admissible peut recevoir un state voisin |
| `random_scope_state` | 1388–1402 | choisit le state BIC cédé au receveur courant | oui, via `region_south_india` | non | la portion Madras peut être sélectionnée puis transférée |
| `every_scope_state` final | 1407–1419 | radicalise les survivants d'Inde du Sud | oui si conservé | non | aucune radicalisation Madras si la portion a déjà été cédée |

## 17. Baseline 1776 de `STATE_MADRAS`

`common/history/states/00_states.txt:4150–4167` définit exactement trois portions et aucune quatrième : FRA, DENNOR et PUD. Le state-region vanilla contient 26 provinces (`map_data/state_regions/10_india.txt:459–480`). Aucun `controller` distinct n'est défini dans le bloc historique ; le contrôle initial suit donc le propriétaire créé.

| Propriétaire | Provinces | Population source | Religions principales | Autres portions possédées | Risque sans territoire | Aptitude C-1 |
|---|---|---:|---|---:|---|---|
| FRA | `xABADB1` | 230 609 | hindoue 182 284 ; sunnite 20 102 ; catholique 28 223 | 25 autres portions | nul | excellente |
| DENNOR | `x10B060` | 34 313 | hindoue 30 102 ; sunnite 4 010 ; protestante 201 | 10 autres portions | nul | bonne, baseline plus petite |
| PUD | 24 provinces restantes | 8 569 817 | hindoue env. 7 895 350 ; sunnite 522 283 ; minorités chrétiennes | aucune | maximal | rejetée |

Les religions non explicites des cultures locales suivent leurs valeurs par défaut ; les totaux ci-dessus sont issus des blocs de pops `common/history/pops/10_india.txt:1727–1833`.

## 18. Portion FRA

`xABADB1` est le hub portuaire de Madras, localisé Pondicherry/Pondichéry, et un terrain de plaine. C'est une enclave côtière d'une province dans le state-region partagé, topologiquement au contact de la grande portion PUD. FRA conserve 25 autres portions d'État en Europe et outre-mer. FRA n'est pas un receveur admissible de la boucle, car ses cultures primaires et sa capitale ne satisfont pas les filtres sud-asiatiques. Le transfert conserve néanmoins PUD comme receveur voisin potentiel, ce qui laisse le comportement réel de 2.c observable.

## 19. Portion DENNOR

`x10B060` est également une enclave de plaine à une province dans Madras, avec 30 102 hindous et 4 010 sunnites. DENNOR conserve dix autres portions, dont Jutland, Zealand, plusieurs Norvège, Islande, Groenland, Antilles, Gold Coast et Pegu. Le pays est lié à HOL et SCH par unions personnelles. La portion est techniquement sûre, mais sa baseline est environ six fois plus petite que celle de FRA et son contexte diplomatique est plus chargé.

## 20. Portion PUD

PUD possède les 24 autres provinces du state-region, toute sa base territoriale et environ 8,57 millions d'habitants. C'est un vassal de HYD. Son transfert éliminerait son unique territoire, perturberait la relation de sujet, retirerait un receveur sud-asiatique voisin majeur et changerait fortement la topologie testée. PUD est donc impropre au noyau minimal malgré son excellente population radicalisable.

## 21. Portion retenue

La portion FRA est retenue. Elle satisfait dans l'ordre les critères prescrits : FRA survit avec 25 autres portions ; 182 284 hindous et 20 102 sunnites fournissent une baseline mesurable ; le state-scope est une enclave unique et stable ; aucun pays ne disparaît ; la mutation est annulée simplement par une nouvelle partie. Elle réduit davantage les effets secondaires que DENNOR et très fortement par rapport à PUD.

## 22. Portions rejetées et raisons

- DENNOR : viable, mais population cible plus faible, propriétaire lié à deux unions personnelles et intérêt expérimental inférieur à FRA.
- PUD : rejet impératif, car PUD n'a aucun autre territoire, est vassal de HYD et constitue lui-même un receveur important de la boucle Madras.
- autre portion : aucune autre portion n'existe dans le setup 1776.

## 23. Mutation exacte et API

L'unique commande territoriale est :

```text
s:STATE_MADRAS.region_state:FRA = {
	set_state_owner = c:BIC
}
```

Owner avant : FRA. Owner après : BIC. La forme directe `s:STATE_*.region_state:TAG` est utilisée à répétition dans le fichier Sepoy vanilla ; `set_state_owner = c:BIC` est attesté dans `events/india_events/india_misc_events.txt:1761`. L'API ne crée ni ne détruit de pays, ne fusionne pas les portions et ne change pas séparément le controller.

## 24. Effets secondaires de la mutation

FRA perd une enclave non incorporée et BIC acquiert un split state d'une province. Le dye plantation français référence un manor house en Île-de-France et peut donc conserver une propriété étrangère après le transfert ; cet effet économique est local et acceptable. Les portions DENNOR et PUD, leurs pops, leurs relations et leurs propriétaires restent inchangés. Aucun pacte diplomatique n'est créé ou supprimé par le harnais.

## 25. Baseline radicale

Après la mutation, le harnais scope directement `s:STATE_MADRAS.region_state:BIC` et exécute exactement deux `add_radicals_in_state` : un pour `rel:hindu`, un pour `rel:sunni`, chacun avec `value = very_small_radicals`. `common/script_values/event_values.txt:1` définit cette valeur à `0.01`. La baseline est donc une fraction de 1 %, non un nombre fixe, et n'atteint aucun autre state d'Inde du Sud.

## 26. Temporalité des deux ticks

Les observations C1O/C1P montrent que la baseline peut rester visuellement nulle au premier tick. Le protocole impose : préparation au 1er janvier et relevé tick 0 ; 2 janvier, premier tick sans conclusion ; 3 janvier, second tick et confirmation d'une baseline non nulle ; seulement ensuite sauvegarde immuable et ouverture de l'événement réel.

## 27. Namespace, identifiants et conflits

Le namespace est `zz_sepoy_test_c1`. Les décisions sont `zz_sepoy_test_c1_prepare` et `zz_sepoy_test_c1_open_event`, l'événement `zz_sepoy_test_c1.1` et le marqueur `zz_sepoy_test_c1_ready`. Une recherche exacte préalable dans le fork, la copie et la vanilla a retourné zéro occurrence pour chacun de ces identifiants : aucun conflit n'existait avant création.

## 28. Décision de préparation

La décision est visible seulement avec `is_player = yes`, `c:BIC ?= this` et sans marqueur. Sa possibilité réévalue ces conditions puis exige, dans un tooltip évalué, la portion FRA, l'absence de portion BIC et au moins une pop hindoue ou sunnite. `ai_chance.value = 0`. `when_taken` ouvre seulement `zz_sepoy_test_c1.1` et ne mute rien.

## 29. Événement de préparation

`zz_sepoy_test_c1.1` est un `country_event` placé sur le root. Il contient exactement deux options : préparation explicite et annulation vide. La préparation exécute uniquement, dans cet ordre, un `set_state_owner`, les deux appels radicaux sur la portion devenue BIC, puis l'unique `set_variable`. Elle n'appelle aucun événement Sepoy réel.

## 30. Décision d'ouverture

La décision d'ouverture est réservée au joueur BIC et exige le marqueur. Son tooltip évalué exige la portion réelle `region_state:BIC`, l'absence de l'ancienne portion FRA, `STATE_MADRAS`, `region_south_india` et des pops hindoues ou sunnites ciblables. Elle ne produit aucune mutation ; son unique effet appelle une fois `sepoy_mutiny_events.2` sur le root BIC. Le joueur doit sélectionner manuellement et exclusivement 2.c.

## 31. Custom tooltips

Le harnais contient exactement trois `custom_tooltip` réellement évalués : préparation décision, trigger de l'événement de préparation et ouverture décision. Chaque enveloppe contient la logique effective sous sa clé de texte. Le modèle suit `common/diplomatic_actions/04_trade_states.txt:50–78` et les harnais A-3/B-1 validés. Aucun diagnostic complexe n'est exposé comme description Jomini brute.

## 32. Localisations EN et FR

Chaque fichier contient exactement les dix clés minimales demandées. Les textes précisent le scénario Madras jetable, FRA comme owner initial, l'unique mutation, la baseline de 1 %, l'attente obligatoire jusqu'au 3 janvier, le caractère manuel et destructif de 2.c, la sauvegarde pré-option immuable, l'interdiction des sauvegardes A/B et l'absence de restauration automatique.

## 33. Contrôles BOM, LF et structure

Les quatre fichiers C-1 commencent par `EF BB BF`, sont des UTF-8 valides, contiennent uniquement des LF et zéro CR/CRLF. Leurs accolades sont équilibrées. Les deux scripts portent la bannière `DISPOSABLE C-1 TEST HARNESS - DO NOT COPY TO MAIN MOD`. Le harnais contient deux décisions, un événement, deux options, un seul identifiant de marqueur, un seul `set_variable`, une seule mutation, deux appels radicaux, un seul appel à l'événement 2, zéro `while`, zéro effet `every_*`, zéro sélection aléatoire, zéro option automatique et zéro commande console.

## 34. Validation statique fonctionnelle

- option 2.c accessible après préparation : oui, BIC possède alors une portion réelle de Madras ;
- mutation territoriale : exactement 1 ;
- portions DENNOR/PUD : inchangées ;
- baseline : limitée au split state Madras de BIC ;
- Bengal, Bombay, Travancore, MARATH : aucune référence ni mutation dans les scripts C-1 ;
- événement réel pendant la préparation : aucun ;
- autre événement Sepoy : aucun ;
- fichier Sepoy, journal et harnais antérieurs : contrôles de hachage inchangés ;
- option automatique : aucune.

## 35. Résumé du manifeste

Le manifeste C1Q comporte 33 lignes de données : quatre nouveaux fichiers C-1, vingt contrôles de harnais existants, deux fichiers Sepoy, deux journaux Sepoy, le `descriptor.mod`, le marqueur Disposable, le descripteur launcher et les deux livrables C1Q. La ligne du manifeste est explicitement auto-référentielle ; toutes les autres lignes portent leur taille et leur SHA-256 réels.

## 36. PLAN RUNTIME C-1 CONDENSÉ

Une seule ouverture de Victoria 3 est autorisée :

1. lancer une seule nouvelle partie BIC au 1er janvier 1776 ;
2. relever les portions FRA, DENNOR et PUD de Madras ;
3. prendre la décision de préparation C-1 et confirmer explicitement l'option de préparation ;
4. confirmer l'unique transfert FRA → BIC ;
5. confirmer l'absence de toute autre mutation ;
6. relever les radicaux de Madras BIC au tick 0 ;
7. passer au 2 janvier ;
8. relever le premier tick sans conclure si la valeur reste nulle ;
9. passer au 3 janvier ;
10. confirmer la baseline radicale non nulle sur les mêmes pops hindoues et sunnites ;
11. créer une sauvegarde pré-option immuable et ne jamais l'écraser ;
12. ouvrir manuellement l'événement réel avec la décision C-1 ;
13. sélectionner exclusivement l'option 2.c ;
14. observer immédiatement la propriété de Madras et les résultats de la boucle ;
15. contrôler rapidement les sujets et les principaux transferts prioritaires ;
16. créer une sauvegarde d'observation et effectuer l'analyse radicale profonde par fonte ;
17. si nécessaire, laisser passer des ticks jusqu'au 5 janvier pour stabiliser l'UI ;
18. créer une sauvegarde post-option distincte ;
19. fermer le jeu une seule fois ;
20. analyser `error.log`, `game.log` et les fontes seulement après cette fermeture ;
21. ne lancer aucune session GBR ;
22. ne relancer ni le jeu ni le launcher.

Un rechargement éventuel de la sauvegarde immuable peut se faire dans la même session, sans quitter le jeu. Les contrôles territoriaux B-1 ne sont pas répétés inutilement.

## 37. Critères territoriaux runtime

Avant 2.c : FRA ne possède plus `xABADB1`, BIC la possède, DENNOR garde `x10B060`, PUD garde ses 24 provinces et aucun autre state n'a changé. Après 2.c : relever sans présupposition si BIC conserve ou perd sa portion Madras, identifier le receveur éventuel, confirmer les branches prioritaires pertinentes et comparer l'indépendance des sujets directs au tooltip.

## 38. Critères radicaux runtime

La baseline doit être mesurable après le second tick du 3 janvier sur les pops hindoues et/ou sunnites de la portion Madras BIC. Après 2.c, comparer les mêmes populations par sauvegarde profonde. Si BIC conserve Madras, les deux appels `large_radicals` finaux doivent être recherchés ; s'il la perd avant le bloc final, l'absence d'effet final sur cette portion est cohérente avec l'ordre du script et doit être documentée.

## 39. Risques restants

Le risque principal est la non-protection de Madras dans la boucle générique. Le caractère aléatoire de `random_scope_state` peut faire varier l'ordre des cessions ; une observation unique ne prouve pas tous les chemins. Le transfert peut laisser une propriété économique française dans le split state BIC. Enfin, l'UI radicale peut rester en retard par rapport aux pops de sauvegarde, comme en C1P. Aucun de ces risques n'est masqué par le harnais.

## 40. Confirmation des sources Sepoy

Fork et copie conservent tous deux `events/india_events/sepoy_mutiny_events.txt` à 63 422 octets et au SHA-256 `FFB4060E659FB8A30691E26BA5BBDA838650EF11AB1760C89EDACFA2310D9BBE`. Ils sont identiques entre eux. Le journal fork/copie reste à 16 040 octets et au SHA-256 `DAEFCB59CCF6B303D2E39C948D8038006C1346AFE40A2B812D45EE4D947E361C`.

## 41. Confirmation des anciens harnais

Les vingt fichiers de harnais racine/A-1/A-2/A-3/B-1 ont été re-hachés avant et après création. Leurs tailles et SHA-256 sont inchangés et sont consignés individuellement dans le manifeste. Aucun fichier existant de la copie n'a été édité.

## 42. Confirmation Travancore, Bengal, Bombay et MARATH

Le harnais C-1 ne contient aucune occurrence de `STATE_TRAVANCORE`, `STATE_WEST_BENGAL`, `STATE_EAST_BENGAL`, `STATE_BOMBAY` ou `c:MARATH`. Le bloc `state_region = STATE_TRAVANCORE`, les corrections Bengal, les données Bombay et tous les blocs MARATH restent intacts.

## 43. Confirmation des zones préservées

`docs/research/technology/` n'a pas été touché. Le stash MARATH n'a subi ni `apply`, ni `pop`, ni `drop` et reste exactement `stash@{0}`. Aucun processus Victoria 3/launcher n'a été démarré durant la phase.

## 44. Fichiers créés

Dans la copie Disposable :

- `common/decisions/zz_sepoy_functional_test_c1.txt` ;
- `events/zz_sepoy_functional_test_c1_events.txt` ;
- `localization/english/zz_sepoy_functional_test_c1_l_english.yml` ;
- `localization/french/zz_sepoy_functional_test_c1_l_french.yml`.

Dans le fork :

- `docs/reports/hotfix/HOTFIX_5C2E4C1Q_SEPOY_C1_STATIC_SETUP.md` ;
- `docs/reports/hotfix/HOTFIX_5C2E4C1Q_C1_HARNESS_MANIFEST.csv`.

Après création, la copie contient exactement 968 fichiers, dont exactement quatre nouveaux fichiers de harnais C-1.

## 45. Vérifications Git finales

`git diff --check` ne signale aucune erreur. Les seuls nouveaux fichiers C1Q du fork sont le présent rapport et le manifeste C1Q ; l'unique autre chemin non suivi demeure l'exception préexistante `docs/research/technology/`. Aucun fichier suivi n'est modifié et aucun commit automatique n'est effectué.

## 46. Verdict

`READY_FOR_C1_RUNTIME_TEST`

Une portion Madras sûre et mesurable est sélectionnée, le harnais réalise exactement une mutation, rend 2.c accessible, prépare une baseline déterministe, ne choisit aucune option automatiquement et planifie le runtime en une seule session. Le risque de perte du noyau Madras reste volontairement ouvert à la validation runtime.
