# Optimisations agressives de 1776 Age of Revolutions

Les essais se déroulent dans des profils Windows isolés avec l'exécutable Steam Victoria 3 1.15.2. La première série utilise le deuxième écran. La répétition du 25 novembre utilise l'écran principal. Le point de départ est `bd776919f625016cb9e63b2359cc04796c681ef5`, qui comprend COMPACT. Les copies expérimentales et les preuves volumineuses sont dans le laboratoire `aor56_aggressive_20261124`. Les deux chantiers sont suivis dans [#57, IA des micro-États](https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/57) et [#58, cultures et POP](https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/58), reliés à [#56](https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/56).

## Pays candidats à une IA passive

L'inventaire part des pays et contrôleurs réellement présents au 1er janvier 1776. Il rapproche chaque capitale des régions stratégiques effectives et compte les provinces du pays après expansion des plages de la sauvegarde. Un fragment correspond à la portion d'une région d'État appartenant à un même pays. Les pactes entrants aident à repérer la suzeraineté et la dépendance. Le moteur fournit un PIB de départ pour chacun des 646 pays. Les colonnes `gdp_fresh_normal_1776_01_01` et `gdp_fresh_consolidated_1776_01_01` donnent respectivement les résultats des campagnes neuves `A2` et `C3`. Les champs d'historique sérialisé indiquent les observations antérieures quand elles sont disponibles.

Les seuils de population sont croisés avec des limites respectives de 4, 8, 16 et 25 provinces et de 2, 3, 4 et 6 fragments. Les priorités couvrent le Saint-Empire, les Balkans, l'Afrique, le Moyen-Orient et l'Inde. Les administrations chinoises `YUN`, `XIN` et `MGL` et les pays balkaniques `MON`, `RAG`, `MOL`, `WAL` et `TRS` figurent dans toutes les variantes par décision de périmètre. Les principaux électorats, les acteurs centraux des institutions impériales et les pays à contenu national structurant sont protégés. L'[inventaire des 646 pays](INVENTAIRE_PAYS.csv) indique le premier lot dans lequel chacun entre et les motifs de classement. Les [listes intégrales](COHORTES.json) sont cumulatives. Les tableaux comptent les drapeaux de contrôleur actifs, dont celui de la France jouée. Pour une campagne solo en France, le témoin a 646 drapeaux actifs et 645 pays autonomes au départ.

| Seuil | Contrôleurs ciblés | Décentralisés ciblés | Drapeaux restant actifs | Pays autonomes en solo |
| --- | ---: | ---: | ---: | ---: |
| 50 000 | 103 | 11 | 543 | 542 |
| 100 000 | 170 | 26 | 476 | 475 |
| 250 000 | 293 | 84 | 353 | 352 |
| 500 000 | 386 | 116 | 260 | 259 |

Le lot modéré cible 59 membres des 92 présents selon le déclencheur impérial. Le lot agressif en cible 75. Dans le lot agressif, 170 autres pays ont leur capitale en Afrique ou dans le bassin du Nil et 23 en Arabie ou en Grande Perse. Les exclusions nommées et leur motif figurent dans l'inventaire. La pertinence indiquée dans l'inventaire reflète le rôle des pays dans le scénario et ses mécaniques. Elle ne prétend pas classer leur importance historique générale.

La réactivation souhaitée concerne une interaction directe du joueur, dont un jeu diplomatique ou une guerre. Le moteur fournit un hook après le choix des joueurs, puis des hooks d'ouverture et de fin du conflit. L'export `script_docs` de l'exécutable testé contient 3 667 effets et itérateurs. Il confirme `set_strategy`, qui donne une stratégie au pays, ainsi que les conditions `is_player` et `is_ai`. La recherche des effets d'activation et de désactivation du contrôleur n'a trouvé aucun équivalent scripté. L'empreinte SHA-256 de `effects.log` est `1f41fca34944c06dad227d815c65e80b02ca2d026ea5d133e0adff72f2a1e549`. Les prises modifiant le drapeau dans une copie du laboratoire mesurent la désactivation seule. Le [journal de modding de la version 1.15.0](https://github.com/Victoria-3-Modding-Co-op/Modding-Digests/blob/main/1.15.0/types/changes_script_docs.md) documente également le rôle de `set_strategy`.

## Variante de population

La version expérimentale contient [39 fusions](FUSIONS_CULTURELLES.tsv). Elle passe de 324 à 285 définitions effectives et de 6 815 à 5 719 entrées historiques de population. L'audit relit les fichiers générés et retrouve exactement **837 328 654 personnes**, réparties de la même manière dans 3 753 clés combinant région d'État, propriétaire, religion et catégorie de POP. La réduction des entrées est de 16,1 %. Les fichiers de population, cultures nationales, foyers culturels et autres références utilisées par les scripts sont adaptés dans une copie isolée. Un premier essai a été écarté avant la création de la campagne à cause de la collision entre l'identifiant de la culture min et un paramètre natif. La version corrigée conserve cette culture et l'identité australienne.

Les regroupements modifient l'apparition de certaines minorités dans les territoires et les règles liées au ciblage par culture, aux foyers, à l'acceptation et au séparatisme. Le jeu conserve notamment les identités yue et hakka, les principaux ensembles du sous-continent indien et les identités qui structurent les conflits balkaniques. Les compromis comprennent l'absorption de la catégorie mixtèque par l'étiquette zapotèque, l'absorption du gaélique écossais par la culture écossaise et le regroupement des Bouriates et des Kalmouks sous l'étiquette mongole. Les distinctions religieuses restent dans les données de population.

Les entrées historiques ne fixent pas l'emploi et les bâtiments des objets runtime. Le moteur répartit la population après initialisation. Dans le témoin d'avril, 25 005 objets se distribuent en 16 529 combinaisons culture–religion–profession–lieu, puis 23 918 lorsque le lieu de travail est ajouté. Richesse, qualifications et autres attributs restent distincts. Ces nombres décrivent le fichier d'avril et ne constituent pas une règle d'éligibilité à la fusion.

Les 39 fusions élimineraient 135 combinaisons dans l'instantané d'avril du témoin si l'on conservait exactement l'État, l'employeur, la profession et la religion de chaque objet. C'est une projection sur un instantané, puisque le moteur peut ensuite modifier l'emploi, les lieux et les migrations. Les plus fortes coïncidences restantes touchent souvent des identités importantes à garder distinctes. Dans le même instantané, l'effacement théorique de toute différence de culture ramènerait les 23 918 clés à 19 545, avant même de considérer la richesse et les qualifications. Ce calcul donne l'ordre de grandeur du levier culturel à emploi et religion donnés.

## Campagnes neuves mesurées

Le 24 novembre, `A1` est parti d'une campagne neuve de la France à vitesse 5. Les temps natifs sont **139 / 182 / 245 secondes** sur les 14, 28 et 56 premiers jours complets et **352 secondes** du 2 janvier au 1er juillet. Une interruption de 103 secondes entre le 14 et le 15 janvier est incluse. Sa cause reste indéterminée. Ce passage ne suffit pas à juger un gain. Le CPU moyen est de 19,4 % de la machine sur cet intervalle et l'ensemble résident moyen de 9 147 Mio, avec un pic à 12 319 Mio. Le 95e percentile des intervalles entre jours est de quatre secondes. Les horodatages proviennent des lignes du moteur, à la seconde.

La campagne neuve `C2` a chargé les 39 fusions. Les temps bruts sont **39 / 337 / 438 secondes** sur les mêmes fenêtres et **570 secondes** jusqu'au 1er juillet. Une interruption visible de 252 secondes figure entre les 16 et 17 janvier. La reprise a coïncidé avec le rechargement du contrôle d'interface du laboratoire. Le CPU moyen est de 16,5 % et l'ensemble résident moyen de 12 791 Mio, avec un pic de 16 654 Mio. Le 95e percentile est de quatre secondes. Les pauses et la variabilité limitent la comparaison du débit absolu.

| Sauvegarde | Contrôleurs actifs | Cultures présentes | Objets POP | Population |
| --- | ---: | ---: | ---: | ---: |
| 1er janvier, campagne neuve de référence `A2` | 646 | 304 | 31 482 | 837 119 763 |
| 1er janvier, campagne neuve consolidée `C4` | 646 | 265 | 30 219 | 837 119 765 |
| 1er avril, campagne neuve `A1` | 645 | 304 | 25 005 | 840 479 289 |
| 1er avril, campagne neuve `C2` | 646 | 265 | 24 887 | 840 518 965 |
| 1er juillet, campagne neuve `A1` | 645 | 304 | 26 196 | 844 137 545 |
| 1er juillet, campagne neuve `C2` | 645 | 265 | 25 812 | 844 178 463 |

Le moteur enregistre effectivement 285 cultures dans la base de données de `C2`, dont 265 représentées dans les POP. L'écart observé du nombre d'objets POP est de −118 en avril (−0,47 %) et −384 en juillet (−1,47 %). Les trajectoires des campagnes diffèrent, y compris par les pays qui subsistent et l'évolution de la population. Au 1er janvier, les sauvegardes natives `A2` et `C4` ont été générées par le même menu et enregistrées avant le premier jour simulé. La consolidation donne 1 263 objets POP de moins (−4,01 %) et deux personnes de plus après initialisation. L’audit des données historiques retrouve exactement les mêmes effectifs. Ces écarts restent faibles au regard des compromis introduits. Le contrôle statique des références `cu:` et la recherche d'erreurs de résolution culturelle dans les journaux de `C2` n'ont signalé aucune référence manquante.

La transition native d'initialisation `Empty->Game` a pris 293,0 s dans `A1` et 207,6 s dans `C2`. Ce relevé exclut le temps de sélection de la France. Le lancement `C2` a suivi une première tentative de la variante, avec un état des caches différent. L'écart n'est donc pas attribuable à la consolidation à partir de ces deux observations. Pour le même relevé sur les départs `A2` et `C4`, les durées sont de 270,5 s et 254,2 s. Ces deux passages étaient destinés à l’inventaire du 1er janvier et ne fournissent pas de comparaison de simulation à 14 jours.

## Essais de désactivation dans le laboratoire

La prise agressive `B5002` a chargé la copie du 1er janvier 1776 dont seuls les 386 champs `ai.enabled` ciblés avaient été passés à `no`. L'inverse restitue le contenu de départ. La France et les 259 autres contrôleurs hors liste restent à `yes`. La sauvegarde du 1er avril retrouve les 386 contrôleurs désactivés et les 260 actifs. En juillet, le pays `COO` ne figure plus dans les contrôleurs, et les 645 autres présentent tous le drapeau attendu. Le scénario, les pays et leurs territoires étaient identiques au chargement.

En avril, l’essai modéré conserve ses 170 contrôleurs inactifs et ses 476 actifs. En juillet, les 170 restent désactivés. `JEY`, qui était actif au départ, a disparu de la liste, d’où 475 contrôleurs actifs. La première répétition agressive `B5003` s’est interrompue le 6 janvier, avant les fenêtres mesurées. Ses journaux ont été conservés et ce passage est exclu du tableau.

| Prise | 14 j | 28 j | 56 j | 180 j | CPU moyen | RAM moyenne | P95 / maximum quotidien |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A chargé `AL2` | 49 s | 96 s | 169 s | 304 s | 21,8 % | 11 210 Mio | 4 s / 6 s |
| A chargé `AL3` | 38 s | 70 s | 117 s | 222 s | 22,9 % | 9 119 Mio | 3 s / 5 s |
| B modéré `B1002` | 42 s | 82 s | 135 s | 253 s | 22,5 % | 11 251 Mio | 3 s / 5 s |
| B agressif `B5002` | 36 s | 66 s | 112 s | 223 s | 22,4 % | 11 765 Mio | 3 s / 4 s |
| B agressif `B5004` | 18 s | 34 s | 61 s | 150 s | 24,2 % | 9 559 Mio | 2 s / 3 s |

Le témoin `AL2` a repris la sauvegarde d'origine avec les mêmes réglages de simulation et de messages. `AL1`, l'essai initial du témoin, s'est arrêté avant le premier jour simulé et ne fournit aucune mesure. Le premier passage agressif et le témoin sont espacés de plusieurs heures. Leur écart est de 34 % sur 56 jours et de 27 % sur l'ensemble des six mois. Le lot modéré a été mesuré après le témoin, avec 20 % de temps en moins sur 56 jours et 17 % sur six mois. Les sauvegardes de juillet des deux passages agressifs ont la même taille de 130 156 620 octets. La comparaison ne trouve que 19 octets d’écart dans l’en-tête et les horodatages réels, avec un état de partie identique après normalisation. Cet état identique a été obtenu en 223 puis 150 secondes sur six mois, ce qui confirme que les temps absolus varient sensiblement d’un lancement à l’autre. Les témoins donnent eux-mêmes 169 puis 117 secondes sur 56 jours et 304 puis 222 secondes sur six mois. Le résultat modéré tombe dans la plage des témoins. Pour le lot agressif, le signal est cohérent sur 56 jours, avec 61 à 112 secondes contre 117 à 169. Sur six mois, le passage agressif le plus lent et le témoin le plus rapide sont pratiquement à égalité. L’amplitude observée interdit de fixer un gain unique. Les sauvegardes de juillet des témoins sont elles aussi identiques après normalisation de l’en-tête et de l’horloge réelle, avec 20 octets différents sur 131 956 690.

L'initialisation native a pris 339,3 s pour `AL2` et 302,5 s pour `B5002`. Elle a pris 207,1 s pour `AL3`, 307,9 s pour `B1002` et 167,3 s pour `B5004`. Du lancement au premier jour mesuré, il s'est écoulé respectivement 424,9 et 386,8 s, reprises automatiques comprises. Les réglages de messages de la série chargée renvoient les notifications courantes vers le flux de messages pour limiter les interruptions d'interface. Ils sont propres aux profils du laboratoire.

## Comparaison consolidée C et D

Les deux paires repartent de la sauvegarde du 1er janvier créée par Victoria 3 dans une campagne neuve France avec les 39 fusions. Les prises d'une même paire chargent les mêmes fichiers, sur le même écran et avec les mêmes réglages. `D1` a précédé `CL1` sur le deuxième écran. `CL2` a précédé `D2` sur l'écran principal le 25 novembre. Le réglage d'affichage est la seule différence entre les paramètres de simulation archivés des deux paires. Dans la copie de D, les 386 drapeaux `ai.enabled` sont la seule différence dans la sauvegarde. Les compteurs d’IA sont vérifiés dans les autosauvegardes.

| Configuration | 14 j | 28 j | 56 j | 180 j | CPU moyen | RAM moyenne / pic | P95 / maximum quotidien | Initialisation | Lancement au premier jour |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| C cultures consolidées, IA normale `CL1` | 34 s | 64 s | 117 s | 223 s | 23,1 % | 10 828 / 12 481 Mio | 3 / 4 s | 268,5 s | 352,7 s |
| D cultures consolidées, IA agressive `D1` | 17 s | 30 s | 51 s | 118 s | 25,7 % | 10 542 / 10 713 Mio | 1 / 2 s | 203,3 s | 286,7 s |
| C cultures consolidées, IA normale `CL2` | 36 s | 69 s | 122 s | 241 s | 18,0 % | 11 741 / 12 010 Mio | 3 / 4 s | 281,0 s | 369,8 s |
| D cultures consolidées, IA agressive `D2` | 26 s | 46 s | 82 s | 213 s | 16,3 % | 12 911 / 16 545 Mio | 2 / 3 s | 138,6 s | 219,9 s |

D réduit le temps de simulation sur les deux paires. Le gain sur 56 jours est de 56 % puis de 33 %. Il est de 47 % puis de 12 % sur six mois. Le 95e percentile des intervalles entre jours tombe de 3 à 1 s puis de 3 à 2 s. Les 386 contrôleurs désactivés et les 260 contrôleurs actifs sont retrouvés dans les sauvegardes d'avril et de juillet des deux prises D. Lors de la répétition, la RAM moyenne augmente de 1 170 Mio et le pic augmente de 4 535 Mio dans D. Les deux paires ne montrent donc pas de baisse stable de la RAM. Les temps d’initialisation et de chargement varient sensiblement. Les différences entre B et D mélangent deux générations du monde et la variabilité de la machine. Elles ne permettent pas d’attribuer un gain supplémentaire aux fusions de cultures.

## Sauvegardes de juillet des essais appariés

| Essai | Contrôleurs actifs | Contrôleurs inactifs | Définitions | Cultures présentes | Objets POP | Population |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `AL2` | 645 | 0 | 324 | 304 | 26 140 | 844 185 454 |
| `AL3` | 645 | 0 | 324 | 304 | 26 140 | 844 185 454 |
| `B1002` | 475 | 170 | 324 | 304 | 26 044 | 844 182 640 |
| `B5002` | 260 | 385 | 324 | 304 | 25 949 | 844 167 427 |
| `B5004` | 260 | 385 | 324 | 304 | 25 949 | 844 167 427 |
| `CL1` | 645 | 0 | 285 | 265 | 26 011 | 844 187 566 |
| `D1` | 260 | 386 | 285 | 265 | 25 741 | 844 043 393 |
| `CL2` | 645 | 0 | 285 | 265 | 26 011 | 844 187 566 |
| `D2` | 260 | 386 | 285 | 265 | 25 841 | 844 055 982 |

## Reproduction de la consolidation

Le passage `C3` a atteint le 1er janvier à partir d’une campagne neuve et a fourni les PIB pays par pays, puis a été arrêté après une pause précoce. Son pilote de sauvegarde appelait `PauseMenu.Save` hors du menu de pause. Le profil `C4` a utilisé le menu natif et enregistré la France le 1er janvier 1776 avant le premier tick. La sauvegarde source des essais combinés a pour SHA-256 `bb08aa9dae2842016851a27f349267f5608ee56b53c35a9147aeb78370f0d648`. Le témoin neuf `A2`, créé par le même menu, a pour SHA-256 `0254c0fc1e447a135ccc0c738270688479ae633244d523bb8c3d0f272863dece`.

Les [outils expérimentaux](../../../../tools/performance/aggressive_2026_11_24/) s'exécutent depuis la racine du dépôt avec Python 3.12. `consolidate.py` prend en argument un nouveau répertoire de destination hors dépôt et produit la surcouche ainsi qu'un inventaire des fichiers modifiés. `audit_population.py` prend le même répertoire et vérifie la conservation des effectifs et les références de cultures. La variable `AOR56_FROZEN_BASE` permet de pointer vers une copie figée du mod. Les définitions du jeu sont prises dans Steam 1.15.2. Le code source du mod courant et les données d'origine restent disponibles.

## Recommandation pour main

Garder la configuration A pour l’intégration actuelle. Les 39 fusions réduisent réellement le nombre de cultures et de POP. Leur avantage sur le temps de simulation reste indéterminé et la baisse du nombre de POP s’atténue après le départ. Les changements de foyers, d’acceptation et de séparatisme sont donc trop importants au regard du gain établi. Conserver la variante en copie expérimentale.

Le lot agressif réduit le temps des deux prises appariées sur 56 jours et sur six mois. L'ampleur du gain varie selon la prise. Le relevé de l'écran principal confirme surtout la baisse des temps au début de la campagne. Les variantes B et D utilisent des copies de sauvegardes modifiées avant chargement. Le moteur ne fournit dans son registre de scripts aucun effet attesté pour désactiver les contrôleurs d’une campagne ordinaire ou les rallumer lors d’une interaction directe du joueur. Cette limitation est décisive pour l’intégration. Un contrôleur désactivé peut laisser un pays sans réponse autonome à une agression, y compris lorsqu’un joueur intervient. Les essais attestent les drapeaux au chargement et jusqu’en juillet ainsi que la France jouable dans les captures. Ils ne valident pas un réveil automatique, le multijoueur ou les campagnes longues.

Les modifications de jeu ont été exécutées dans des copies isolées. Le contrôle de l’arbre Git suivi est vide sur `bd776919f625016cb9e63b2359cc04796c681ef5`. COMPACT fait partie de cette référence. Les empreintes des trois fichiers de la diplomatie Russie–Kazakh correspondent à celles conservées avant les essais. Le relevé complet des chronos, de l’initialisation, du CPU, de la RAM et des POP est dans [BENCHMARKS.csv](BENCHMARKS.csv).
