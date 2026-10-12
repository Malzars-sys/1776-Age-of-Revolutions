# MAP-2I — Correctif du siège de Bassora

## Version locale proposée au test

Après le constat d'une coalition ottomane disproportionnée, le joueur a choisi explicitement **d'essayer la contre-offensive irakienne**, plutôt que de créer immédiatement un journal de siège. Sa dernière consigne porte l'armée d'IR1 à **20 unités permanentes au total**, pas vingt unités supplémentaires.

Trois fichiers de gameplay sont modifiés :

1. `common/history/diplomatic_plays/00_otto_iraqi_persia_war.txt`
2. `common/history/military_formations/04_military_formations_middle_east.txt`
3. Nouveau `common/history/treaties/08_1776_basra_ottoman_assistance.txt`

Le scénario natif est préparé, **mais l'exclusion effective de TUR doit encore être confirmée dans une nouvelle partie**. Les scripts locaux de la version 1.13.11 établissent qu'un protectorat peut initier son propre coup diplomatique ; ils ne constituent pas une observation de tous les automatismes de participation du moteur.

## Mécanisme et compromis

L'ancien scénario plaçait PER en attaque contre IR1. Le protecteur ottoman devenait alors un acteur majeur du camp défensif dans le test du joueur.

Le scénario est inversé techniquement :

- **Initiateur : IR1**, contre-offensive des autorités locales.
- **Soutien de l'initiateur : OMA**.
- **Cible : PER** ; aucun objectif n'attaque un sujet ottoman.
- **Conflit déjà actif : `war = yes`**, pas une crise vouée à recommencer en janvier.
- **Demande principale de PER : conquérir `STATE_BASRA.region_state:IR1`**.
- **Demande native d'IR1 : humiliation de PER**, utilisée comme approximation d'une levée victorieuse du siège.

Cette humiliation est un effet réel de gameplay, pas seulement un nom de guerre. Elle est le compromis adopté pour conserver une guerre native sans présenter la Perse comme l'initiateur technique d'une attaque contre un protectorat. La Perse reste la puissance cherchant à prendre Bassora ; le nom de guerre affiché pourra néanmoins évoquer la contre-offensive irakienne.

Les anciennes demandes de conquête du Khuzestan par IR1 et de port perse par Oman sont retirées **délibérément** pour limiter le conflit au siège et éviter un objectif omanais favorisant un second théâtre d'Ormuz. Ce retrait n'affecte aucune frontière initiale, propriété économique ou dépendance. L'armée reste contrôlée par ses joueurs ou son IA : aucun ordre de mobilisation ou de déploiement n'est imposé par ce correctif.

TUR n'est ni initiateur, ni cible, ni soutien écrit dans le scénario. **Le protectorat TUR → IR1 reste exactement inchangé.** Aucun retrait temporaire de la dépendance, règle mondiale de neutralité, trêve artificielle ou immunité permanente n'est utilisé. Aucun journal parallèle n'est créé. Les éventuels sujets persans restent soumis aux règles natives de participation ; le script ne prétend pas supprimer ces règles globales pour n'afficher que trois TAGs.

### Résolution

Le moteur de guerre conserve ses mécanismes de progression et de paix :

- PER peut gagner Bassora par l'objectif territorial principal.
- IR1 peut obtenir l'humiliation de PER et représenter ainsi une résistance victorieuse.
- Une paix blanche ou négociée peut terminer le conflit sans transfert.
- Aucun résultat ni date de victoire en avril n'est imposé.

Ce correctif ne développe pas de quatrième branche scriptée d'escalade ottomane. TUR conserve toutes ses capacités militaires et diplomatiques ordinaires, sans nouvelle interdiction permanente. Si le moteur le fait encore entrer automatiquement au démarrage, **la tentative sera un échec natif**, malgré une syntaxe statiquement valide : le journal régional prévu dans le prompt sera alors la solution de repli, sans casser le protectorat.

Les fichiers d'historique initialisent une nouvelle campagne ; aucun on-action ne recrée cette guerre à chaque chargement d'une sauvegarde.

## Armée irakienne : 20 permanentes et 9 conscrits

| Recrutement | Avant | Après |
|---|---:|---:|
| Bagdad, infanterie permanente | 5 irrégulières | 5 mousquets |
| Bagdad, hussards | 4 | 4 |
| Bagdad, artillerie | 1 | 1 |
| Bassora, infanterie permanente | 0 | 10 mousquets |
| Total permanent IR1 | **10** | **20** |
| Total conscription IR1 | **9** | **9** |

IR1 possède déjà `light_infantry_tactics`, technologie réellement exigée par `combat_unit_type_musket_infantry`. Aucune technologie gratuite n'est accordée à IR1, PER ou TUR. Les quatre groupes de conscription, toujours irréguliers, restent inchangés. La formation `cleanup2d3e_r1_ir1_land_1`, son quartier général et son commandant Süleyman Ağa sont conservés.

Les dix nouveaux permanents sont des renforts de gameplay autorisés par le joueur, pas une estimation documentaire de dix régiments historiques. Leur recrutement se fait à Bassora, une région de **362 018 habitants existants**. Aucun habitant ou niveau d'infrastructure n'est ajouté. Les unités initialisent leur recrutement natif : aucun doublon de casernes n'est ajouté à l'historique civil.

### Capacité statique, non observée dans le moteur

| Région | Permanentes avant → après | Infrastructure nominale à plein emploi | Demande civile modélisée | Demande militaire permanente après | Réserve de paix modélisée après |
|---|---:|---:|---:|---:|---:|
| Bagdad | 10 → 10 | 49,0 | 5,7 | 2,0 | +41,3 |
| Bassora | 0 → 10 | 52,0 | 4,1 | 2,0 | +45,9 |

Le modèle inclut les infrastructures à plein emploi, les ports et les traits régionaux, et estime les déclarations civiles superposées avec la dernière déclaration par type. Il ne garantit pas l'emploi effectif, les qualifications, les pénuries ou les bonus réellement chargés. Le proxy de main-d'œuvre libre à Bassora est de 87 316 travailleurs à 25 % des populations libres : après les 13 000 emplois civils explicites et 10 000 militaires, la marge modélisée est **64 316**, pas une mesure de chômage disponible.

Les quinze mousquets demandent des armes légères selon leurs règles existantes. Le budget, l'approvisionnement et le recrutement effectifs d'IR1 sont donc à vérifier ; aucun bien, recette ou mécanisme militaire global n'est modifié pour masquer ces besoins.

## Assistance ottomane

Un traité historique initialisé contient **l'article natif dirigé `military_assistance`, TUR → IR1**. Il ne contient ni alliance ni pacte défensif supplémentaire, et n'ajoute pas TUR à la liste des participants de la guerre.

La date écrite 1775.1.1 est une initialisation de gameplay, non la date attestée d'un traité conservé. Son engagement d'un an est déjà écoulé au départ ; ce n'est pas une expiration automatique. Le traité reste résiliable selon les règles natives et n'est pas recréé par un événement périodique.

Les effets standards de l'article restent inchangés : expérience et entraînement pour IR1, coût des biens militaires réduit de 10 %, diffusion technologique militaire, et un coût accru de biens militaires de 10 % pour le fournisseur TUR. **Aucun bataillon, technologie ou puissance militaire ottomane n'est retiré.** Le coût diplomatique standard est 25.

**Limite de chargement à tester :** l'article est normalement débloqué par `general_staff`, que TUR ne possède pas dans ses technologies initiales. Le correctif initialise uniquement le traité historique ; il ne donne pas cette technologie et ne change pas le déblocage mondial de l'assistance. Les conditions de maintien natives ne demandent pas cette technologie, mais cela ne prouve pas que l'initialisation historique passe tous les contrôles du moteur. Vérifier que l'article apparaît et fonctionne ; s'il est rejeté, transmettre les logs avant de décider d'une exception locale ou d'un soutien régional scripté.

## Validation et preuves

`VALIDATION.json` contient **35 contrôles réussis**, statut `PASS_STATIC_NATIVE_TEST_REQUIRED`. Les nouveaux changements militaires sont comparés à la **baseline réelle MAP-2I testée**, conservée avant ce correctif, et non à un état théorique de main.

- Propriétaires RGB, États, géométrie, populations et leurs compositions, bâtiments civils, PM, titulaires économiques et pays restent identiques.
- Seuls les cinq permanents irakiens préexistants changent de type et dix nouveaux permanents sont ajoutés à Bassora.
- Les unités de tous les autres pays, les conscrits irakiens, les formations, commandants et quartiers généraux restent identiques.
- Le protectorat, les technologies, les réformes ottomanes, MAP-2A à MAP-2I, les populations régionales et les correctifs IA sont protégés par inventaires et empreintes.
- Un seul scénario de guerre sur Bassora, aucun second siège scripté, pas de nouvelle annexion initiale ou mécanisme de redéclenchement sur sauvegarde.
- Analyse syntaxique des fichiers modifiés, tests existants des objectifs ottomans et des infrastructures IA, HEAD/index/références Git inchangés.

L'autosauvegarde la plus récente a été examinée en lecture seule : elle date du **24 octobre 1777**, pas du démarrage de janvier 1776. Elle ne permet donc pas d'établir le déploiement initial vu dans la fenêtre fournie. Les **76/218 bataillons et 17 flottilles** restent les disponibilités de coalition rapportées par le joueur, **pas des forces mobilisées certifiées par ce correctif**. `SAVE_EVIDENCE.json` documente cette limite. Aucun jeu n'a été lancé, aucune sauvegarde du joueur modifiée. Seul le texte temporaire généré pour ce diagnostic a été supprimé après conservation de la preuve légère : 127 486 312 octets récupérés. Il peut être régénéré depuis la sauvegarde originale intacte.

Les anciens contrôles MAP2I exigeant la conservation stricte des unités de tous les pays et PER comme initiateur sont conservés comme preuve de la phase précédente. Pour ce suivi, ils sont remplacés par le validateur ciblé `tools/basra_siege_fix.py`, qui exige la modification militaire IR1 autorisée et l'inversion approuvée, tout en contrôlant les autres systèmes.

Pas de nouvelle archive complète, commit, merge ou push. Aucun MAP-2J commencé.

## Test du joueur

**Nouvelle partie au 1er janvier 1776 :**

1. Vérifier le camp IR1 + OMA face à PER. **TUR ne doit pas figurer comme belligérant.** Vérifier aussi l'intégrité du protectorat TUR → IR1.
2. Vérifier PER comme détenteur de la demande principale sur Bassora, encore possédée par IR1 ; l'Irak porte la demande d'humiliation.
3. Vérifier **20 permanents + 9 conscrits** pour IR1, dont 15 mousquets, 4 hussards et 1 artillerie ; Bassora recrute les dix nouveaux mousquets.
4. Vérifier l'article d'assistance TUR → IR1 dans les traités et ses effets, sans alliance supplémentaire.
5. Distinguer les bataillons disponibles de ceux réellement mobilisés ; relever leurs affectations et fronts, sans conclure à partir des seuls totaux des coalitions.

**Février :** recrutement et ravitaillement de Bassora, infrastructures, armes légères, budgets IR1/TUR, assistance toujours active, absence d'arrivée automatique ottomane et absence de guerre dupliquée.

**Avril :** progression, paix possible et propriété de Bassora. Une victoire perse n'est pas obligatoire. Si TUR apparaît encore automatiquement, ou si le traité d'assistance ne charge pas, fournir capture et logs : ne pas présenter cette tentative comme validée avant ce test.
