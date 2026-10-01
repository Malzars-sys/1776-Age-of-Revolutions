# TECH8C — prototype des laboratoires et des données

Date : 30 septembre 2026. Statut : **implémenté dans les fichiers ; essais moteur et équilibrage en attente**.

Ce lot applique les décisions précisées après [TECH8B](TECH8B_EXPERIMENTAL_LABS_READINESS_2026-09-30.md). Il ne reprend pas la proposition ancienne de laboratoire national unique. La dernière demande remplace la production indépendante des deux biens par une compilation des données brutes en données organisées. La chaîne des quotas de naissance n'est pas modifiée par ce lot.

## Décisions appliquées

- Deux biens en chaîne : les données organisées **consomment des données brutes**. Ratio nominal de prototype choisi : 1 brute pour 1 organisée, en plus du papier et des emplois existants.
- Laboratoire public, extensible, sans limite de niveaux par État et sans plafond national de sites. Construction : **1 000 points par niveau**. Aucune création gratuite automatique ; aucune construction privée.
- Aucune production d'innovation par le laboratoire. Les universités conservent leurs PM et leurs points d'innovation.
- Trois équipements : contribution potentielle au plafond de 5 / 10 / 20 par niveau pleinement employé et approvisionné.
- Orientation séparée : recherche générale à +0,25 % dans chacun des trois domaines, ou production / militaire / société à +1 % dans leur seul domaine, par niveau pleinement employé et approvisionné. Une seule orientation par bâtiment.
- Les deux premiers équipements ne consomment pas de données organisées. **Le dernier consomme les deux types de données**, même en recherche générale. Chaque spécialité demande 20 données organisées supplémentaires ; ce besoin s'ajoute à celui de l'équipement.
- Le bonus direct existant de +5 de la technologie `experimental_research_laboratories` est conservé. Il n'est pas confondu avec la contribution des bâtiments.

Le coût de 1 000 dépasse les coûts ordinaires actuellement utilisés pour les bâtiments productifs. Les canaux et monuments particuliers conservent leurs coûts propres, parfois supérieurs : ils ne sont pas modifiés pour faire du laboratoire un maximum artificiel.

## Biens et producteurs

| Bien | Prix de base | Producteurs | Production par niveau à plein emploi |
|---|---:|---|---:|
| Données brutes industrielles | 50 £, comme l'acier | Exploitations minières, carrières, sel et ports | 1 |
| Données brutes industrielles | 50 £ | Industries légères | 2 |
| Données brutes industrielles | 50 £ | Industries lourdes | 4 |
| Données organisées | 60 £, comme les épices | Administrations et centres de commerce | 1 |
| Données organisées | 60 £ | Universités | 2 |

Ces prix sont des références, pas des prix de marché fixes. Les paramètres commerciaux habituels restent actifs dans ce prototype : biens échangeables, quantité commerciale 10, coût de convoi 0,1. Ce choix de commerce est provisoire, pas une décision explicite de blocage des échanges.

Les PM documentaires sont des groupes **supplémentaires**, avec une option de désactivation : ils ne remplacent ni la production industrielle, ni la bureaucratie, ni l'enseignement universitaire. Les recettes utilisent du papier et des emplois de bureau. Production et consommation sont liées à l'emploi. Depuis la révision du 1er octobre 2026, les trois PM de données brutes nécessitent **Métrologie scientifique** (`scientific_metrology`), et les trois PM de compilation organisée nécessitent **Sociétés savantes** (`specialized_professional_societies`). Ces liens alimentent aussi la liste native des déblocages dans les infobulles technologiques. Les options sans relevés sont les choix par défaut, accessibles sans technologie ; la recherche autorise l'activation sans la forcer. Vérifier les PM déjà actifs dans une sauvegarde existante après rechargement : aucune migration forcée des bâtiments n'est ajoutée.

| Compilation | Données brutes consommées | Organisées produites | Papier consommé | Emplois de bureau supplémentaires |
|---|---:|---:|---:|---:|
| Administration | 1 | 1 | 0,25 | 10 |
| Centre de commerce | 1 | 1 | 0,25 | 10 |
| Université | 2 | 2 | 0,50 | 20 |

Quantités par niveau à plein emploi ; les intrants et extrants sont dans le même bloc `workforce_scaled`. L'option sans dossiers ne consomme ni ne produit de données. Les prix de base restent 50 / 60. Une pénurie de brutes est désormais un manque d'intrant pour ces bâtiments, soumis aux pénuries natives : vérifier en partie son effet sur la compilation et sur leurs autres activités. Aucun nouveau malus scripté ne leur est imposé. Le surcoût resserre fortement la marge de compilation ; l'emploi et la soutenabilité des relevés activés doivent être testés.

Le PM universitaire `pm_analytical_philosophy_department` est renommé **Séminaires de philosophie analytique** (anglais : **Analytical Philosophy Seminars**) via des localisations dédiées dans `replace`. Son identifiant, sa technologie `analytical_philosophy`, son icône et ses effets sont conservés ; le département de philosophie antérieur n'est pas renommé.

Après ces déblocages et le renommage, 1 172 contrôles statiques passent, dont 109 essais arithmétiques. La comparaison avant/après confirme que les huit PM documentaires conservent exactement leurs recettes, emplois et textures ; seuls les prérequis et les choix par défaut changent. Les en-têtes BOM, noms FR/EN et contraintes du menu de test sont contrôlés. L'affichage des déblocages et du nouveau nom reste à confirmer après redémarrage du jeu.

### Liste des 35 bâtiments concernés

- Exploitations / ports (12) : phosphate, bauxite, cuivre, charbon, fer, plomb, soufre, or, carrière de calcaire, mine de sel, saline et port.
- Industries légères (6) : agroalimentaire, textiles, meubles, verrerie, outils et papier.
- Industries lourdes (14) : alliages non ferreux, raffinage, ciment, chimie, explosifs, synthétiques, acier, moteurs, chantiers navals, automobiles, équipements électriques, armes, artillerie et munitions.
- Données organisées (3) : administration gouvernementale, centre de commerce et université.

Les champs agricoles, plantations, chemins de fer, camps de bûcherons et plateformes pétrolières ne reçoivent pas de nouveau PM dans ce lot.

## Recettes et accès des laboratoires

Quantités nominales par niveau à plein emploi, avant économies d'échelle et autres effets du jeu.

| Équipement | Accès | Brutes | Organisées | Autres intrants | Emplois | Plafond potentiel |
|---|---|---:|---:|---|---:|---:|
| Expérimentation instrumentale | Laboratoires expérimentaux, ère 5 | 20 | 0 | Papier 10, outils 5, verre 5, produits chimiques industriels 5 | 2 500 | +5 |
| Laboratoire électrifié | Production d'électricité, ère 9 | 40 | 0 | Papier 15, outils 10, verre 10, machines de précision 10, électricité 20, produits chimiques industriels 10 | 5 000 | +10 |
| Laboratoire de haute précision | Radio, ère 11 | 80 | 40 | Papier 20, outils 15, verre 10, machines de précision 30, électricité 40, radios 20, téléphones 20, produits pharmaceutiques 10, produits chimiques industriels 20 | 10 000 | +20 |

Ajout demandé le 30 septembre : les acides sont représentés par le bien existant `industrial_chemicals`, dont la description inclut déjà les acides et autres réactifs. Leur consommation de 5 / 10 / 20 suit l'emploi et n'ajoute ni nouveau bien ni changement aux usines chimiques. Les quantités sont un réglage de prototype, non une valeur prescrite par l'utilisateur. Une pénurie est couverte par le contrôle des autres intrants décrit ci-dessous.

Une spécialisation ajoute **20 organisées** : le total devient 20 / 20 / 60 respectivement. La recherche générale laisse les besoins à 0 / 0 / 40.

Coût nominal des intrants aux prix de base, **hors salaires, prix locaux et autres modificateurs** : 1 900 / 5 050 / 16 000 £ ; avec spécialisation : 3 100 / 6 250 / 17 200 £. Ces montants incluent les réactifs à leur prix de base de 40 £ et ne sont pas des prévisions de dépenses budgétaires en partie.

Les premiers essais utilisent seulement les biens disponibles à leur période. L'électricité et les équipements avancés restent derrière leurs technologies ; pas de déblocage automatique en 1776. Les coefficients de rendement et les recettes sont des valeurs de prototype à équilibrer, pas des résultats déjà mesurés.

## Révision du 1er octobre 2026 : recherche générale

À la demande de l'utilisateur, la recherche générale accélère désormais les trois catégories, plus faiblement qu'une spécialisation. Le coefficient retenu pour ce prototype est un quart du bonus spécialisé :

| Orientation | Production | Militaire | Société |
|---|---:|---:|---:|
| Générale | +0,25 % | +0,25 % | +0,25 % |
| Production | +1 % | — | — |
| Militaire | — | +1 % | — |
| Société | — | — | +1 % |

Les valeurs sont par niveau pleinement employé et approvisionné. Le calcul national ajoute les niveaux effectifs spécialisés et un quart des niveaux effectifs généraux dans chaque catégorie. Les réductions liées à l'emploi et aux pénuries restent appliquées avant cette pondération ; les bonus généraux ne s'ajoutent pas à ceux d'une spécialisation dans le même bâtiment. Le renouvellement remplace les anciens modificateurs au lieu de les empiler.

Les recettes sont préservées : aucune donnée organisée supplémentaire en orientation générale ; l'équipement final consomme toujours 80 brutes et 40 organisées. Les spécialisations ajoutent toujours 20 organisées. Aucun changement du plafond d'innovation, des emplois ou des points d'innovation. Les textes FR/EN et les marqueurs potentiels des PM reflètent ces nouveaux bonus, avec deux décimales pour afficher 0,25 %.

Validation statique : 1 135 contrôles passent, dont 109 essais arithmétiques. La comparaison avec le fichier des PM avant cette révision confirme que seuls les marqueurs du PM général ont changé ; les recettes des équipements et des spécialisations sont identiques. Les nouveaux essais couvrent les douze combinaisons équipement/orientation, les laboratoires mixtes, l'emploi partiel ou nul, les pénuries et les changements d'orientation. Ces contrôles n'exécutent pas le moteur : utiliser `event research_laboratory_tests.3` après redémarrage, puis comparer les trois modificateurs du pays avant/après le choix général et une spécialisation.

## Pénuries : réduction explicite des bénéfices de recherche

Un contrôle local au système des laboratoires est prévu **tous les deux jours**. Il calcule la disponibilité des données dans le marché commun, en incluant les autres pays du marché et la demande des exportations. Le besoin nominal est calculé à partir du PM, des niveaux et de l'emploi, sans réduire ce besoin avec notre propre malus. La demande brute comprend désormais les administrations, centres de commerce et universités qui compilent des données, en plus des laboratoires. Les options de compilation désactivées n'ajoutent pas de demande. Le besoin indirect et le besoin direct du laboratoire restent distincts : aucune consommation organisée n'est ajoutée aux deux premiers équipements généraux.

| Offre / besoins nominaux d'un bien requis | Réduction des bénéfices du laboratoire |
|---|---:|
| Moins de 75 %, mais au moins 50 % | −50 % |
| Moins de 50 %, mais au moins 10 % | −80 % |
| Moins de 10 % | −95 % |

Le pire des deux biens requis détermine la réduction : les pénalités ne s'additionnent pas. Un premier équipement en recherche générale n'est pas pénalisé pour des données organisées qu'il ne consomme pas. Une pénurie locale documentaire signalée par le moteur impose au moins −80 %. Une autre pénurie d'intrants signalée dans le laboratoire impose au moins −50 %, sans remplacer un malus documentaire plus fort.

Les bénéfices effectivement accordés au pays sont proportionnels à **niveaux × taux d'emploi × efficacité d'approvisionnement**. Un établissement vide ne contribue pas. Les trois bonus de catégorie et le bonus de plafond sont visibles dans les modificateurs du pays, renouvelés sans empilement. Les malus d'approvisionnement sont visibles sur les laboratoires. Les PM affichent les valeurs **potentielles**, pas une promesse de rendement sous pénurie.

Les pénalités documentaires ne modifient pas les règles globales du jeu ni les autres bâtiments. Elles réduisent la contribution de recherche, sans baisser elles-mêmes la demande d'intrants : cela évite de faire disparaître artificiellement une pénurie en pénalisant sa propre consommation. Les effets natifs de pénurie sur les bâtiments restent gérés par le moteur.

Le démarrage et les changements de PM / taille / propriétaire lancent ou réparent le suivi. Une garde évite les boucles multiples ; les contributions expirent au bout de quatre jours si elles ne sont plus renouvelées. Une réparation mensuelle couvre les cas de rechargement où le suivi manquerait.

**À vérifier dans le moteur :** scopes des marchés et bâtiments, évaluations des valeurs scriptées, durée effective des variables, pénuries dans un État isolé et effet des économies d'échelle sur les besoins réels. Le calcul nominal est un contrôle ciblé ; il ne prétend pas reproduire parfaitement tous les achats locaux du moteur.

## IA et limites de validation

Le bâtiment reçoit une priorité de prototype quand l'État contient une université et que le propriétaire possède des réserves d'or. Les marqueurs de rendement ont une valeur IA explicite, mais cela ne prouve pas que l'IA construira, financera et approvisionnera correctement la chaîne. Aucune création annuelle forcée ni dépendance à un mod IA extérieur n'a été ajoutée.

Les 21 fichiers de bâtiments existants contrôlés sont préservés par rapport à leur contenu au début de ce lot, hormis l'ajout des PMG documentaires. Les autres modifications déjà présentes dans le chantier sont conservées. Les modifications à la loi des femmes et au système nataliste ne sont pas rouvertes.

Le validateur `tools/tech8c_validate.cjs` contrôle les références, prix, branchements, recettes, absence de création de points, localisations FR/EN et assets. Ses tests numériques vérifient une formule de référence ; **ils n'exécutent pas le moteur Paradox**. Aucun test de partie, de sauvegarde, d'IA ou de performance n'est revendiqué comme réussi.

## Menus de test et procédure en jeu

Redémarrer le jeu pour charger les nouveaux biens, bâtiments et types de modificateurs. Utiliser **une copie de sauvegarde** ou une nouvelle partie de test, avec la console de débogage.

```text
event research_laboratory_tests.1
event research_laboratory_tests.2
event research_laboratory_tests.3
```

1. **Approvisionnement** : activer les relevés (option commune soumise à Métrologie scientifique et Sociétés savantes), couper les deux biens ou un seul, créer explicitement un laboratoire d'essai dans la capitale. La création de test est gratuite, unique tant que la capitale en contient déjà un et soumise à la technologie du laboratoire. Fermer le menu ne change rien.
2. **Équipement** : appliquer un des trois équipements à tous les laboratoires du pays. Les choix restent soumis aux technologies.
3. **Orientation** : appliquer recherche générale, production, militaire ou société à tous les laboratoires du pays.

Pour un test tardif sans attendre les recherches, la commande `research 12` débloque toutes les technologies jusqu'à l'ère 12 pour le pays joueur. Elle change fortement la partie : usage exclusivement sur la copie de test. Pour éprouver la construction normale à 1 000 points, utiliser le menu normal des bâtiments, pas la création gratuite du menu de test.

### Matrice de contrôle — tous les essais moteur restent à effectuer

| Test | Résultat attendu / observation à relever |
|---|---|
| Prix et sources | Prix de base 50 / 60 ; production brute 1 / 2 / 4 ; organisée 1 / 1 / 2, consommant respectivement 1 / 1 / 2 brutes. Papier et emplois conservés. |
| Déblocages documentaires | Avant Métrologie scientifique, les trois relevés bruts sont verrouillés ; après, ils sont sélectionnables et listés dans son infobulle. Même contrôle pour les trois compilations organisées avec Sociétés savantes. Les options sans relevés restent accessibles. |
| Nom du PM universitaire | La philosophie analytique affiche Séminaires de philosophie analytique, sans changer ses effets ni le nom du département de philosophie antérieur. |
| Compilation et désactivation | Vérifier l'achat de brutes par les trois producteurs, l'effet de leur pénurie, la baisse d'emploi et le retour à zéro intrant / extrant documentaire quand le PM est désactivé. |
| Concurrence pour les brutes | La compilation entre dans le besoin nominal du marché partagé, même si elle appartient à un autre pays. Dix laboratoires manuels + 100 administrations + 50 centres de commerce + 25 universités à plein emploi demandent 400 brutes, pas 200. |
| Construction normale | Bâtiment public, exactement 1 000 par niveau, extensible au-delà de 1, plusieurs États possibles, pas d'investissement privé. |
| Général, deux premiers équipements | Aucune consommation organisée, même si ce bien est absent du marché. Brutes et autres intrants restent requis. |
| Général, équipement final | Consommation nominale de 80 brutes et 40 organisées. |
| Recherche générale | +0,25 % en production, militaire et société par niveau pleinement employé et approvisionné. Aucun intrant supplémentaire, plafond inchangé. |
| Trois spécialités et changement d'orientation | 20 organisées supplémentaires ; +1 % dans le seul domaine choisi, sans les bonus généraux. Le retour à général remplace ce bonus par +0,25 % dans chacun des trois domaines. Aucun empilement. |
| Universités seules / avec laboratoire | Aucun nouveau point d'innovation créé par le laboratoire ; plafond et accélération distincts. Garder l'emploi et les PM universitaires comparables. |
| Plein / demi / zéro emploi | Contribution proportionnelle ; bâtiment vide : zéro. Attendre la stabilisation des emplois après un changement d'équipement. |
| Brutes coupées, organisées conservées | Après le prochain contrôle, forte réduction du rendement du laboratoire ; rétablissement après restauration de l'offre. Les importations éventuelles empêchent une pénurie complète. |
| Organisées coupées seules | Les premiers équipements généraux restent opérationnels si tous leurs intrants sont disponibles ; les spécialités et l'équipement final subissent la pénurie. |
| Seuils documentaires | Vérifier 75 %, 50 % et 10 %, puis panne totale : −50 / −80 / −95 %. La demande de référence ne baisse pas à cause du malus lui-même. |
| Autres intrants absents | La pénurie native de papier / outils / électricité / produits chimiques industriels / équipement ne laisse pas 100 % du bénéfice de recherche. |
| Marché commun, commerce et isolement | Offre des partenaires et importations prises en compte ; exportations ajoutées au besoin nominal ; tester spécialement l'accès au marché très faible. |
| Suppression / transfert / rechargement | Pas de bonus empilé ni de boucle doublée ; contributions recalculées ou expirées ; nouveau propriétaire suivi. |
| Offre avant premiers laboratoires | Production et coûts des relevés soutenables malgré une demande encore faible ; PM désactivables sans détruire l'activité principale. |
| IA, 20 ans et performances | Construction non forcée, emploi, budget, sélection des PM, réponse aux pénuries, rythme de recherche et coût de la boucle de suivi mesurés séparément. |

Après le lancement, relever les nouvelles erreurs de `error.log` portant sur les identifiants `1776_laboratory`, `research_laboratory`, `raw_industrial_data`, `organized_research_data` ou `tech8c`. Un ancien journal d'erreurs ne valide pas ce lot non encore rechargé.

## Assets et provenance

À la demande explicite de l'utilisateur, cinq icônes DDS sont réutilisées telles quelles depuis l'installation locale de **Tech & Res** (Steam Workshop `3472248460`) :

| Source locale | Copie autonome dans le mod | SHA-256 |
|---|---|---|
| `gfx/interface/icons/goods_icons/raw_data.dds` | `gfx/interface/icons/goods_icons/tech_and_res_raw_data.dds` | `A97C6C01BD982CD6B071D0A89833899EEA77573A4E8723EB5F26B9E7302F9BCE` |
| `gfx/interface/icons/goods_icons/organized_data.dds` | `gfx/interface/icons/goods_icons/tech_and_res_organized_data.dds` | `825776B934A7FECC52F5CAC9E68A0CE7F4D8914FAEBA3A7959FA087AEAD9F3A3` |
| `gfx/interface/icons/production_method_icons/pm_manual_data_reporting.dds` | `gfx/interface/icons/production_method_icons/tech_and_res_manual_data_reporting.dds` | `96FFAC9DE9C7DF6A2197DCD3BD375E8FB0B9D281D348C52A2142332220982AA1` |
| `gfx/interface/icons/production_method_icons/pm_manual_data_optimization.dds` | `gfx/interface/icons/production_method_icons/tech_and_res_manual_data_optimization.dds` | `AC09B1FE88628BCFDA549E18B46A8B5FCF734DA54FD60914856AC00DAD8BD322` |
| `gfx/interface/icons/production_method_icons/pm_manual_data_reporting_2.dds` | `gfx/interface/icons/production_method_icons/tech_and_res_no_data_reporting.dds` | `D0F76713B84B9544873E9141F9BC771B4C5B4F01FB27DEA73CA89BF85258ACBC` |

Les trois PM de données brutes utilisent l'icône de relevés manuels ; les trois PM de données organisées utilisent l'icône de compilation manuelle. Les deux options de désactivation utilisent le symbole bleu de roue barrée (`pm_manual_data_reporting_2.dds`), identifié par inspection visuelle. Les icônes numériques de serveurs ne sont pas utilisées pour ces opérations documentaires. Les quantités et emplois ne changent pas lors de ce remplacement visuel.

Le gameplay ne dépend pas de l'activation de Tech & Res. Les règles et localisations sont implémentées ici, pas copiées depuis sa chaîne de recherche. La réutilisation locale demandée **ne prouve pas une autorisation de redistribution publique** : conserver cette provenance et vérifier l'autorisation ou remplacer les icônes tierces avant publication.

L'illustration du laboratoire fournie par l'utilisateur (`codex-clipboard-11358e79-3733-4501-a16f-b8539c43e111.png`, 1 254 × 1 254) remplace l'université sur le bâtiment, les quatre modificateurs nationaux de laboratoire et les trois menus de test. Le cadrage et le contenu sont conservés ; seule la taille est adaptée à 256 × 256, avec une chaîne complète de neuf mipmaps DDS RGBA8, comme les dimensions des icônes natives. Aucune génération d'image ni retouche de contenu n'est réalisée.

- Source conservée : `docs/reports/assets/tech8c_research_laboratory_source.png` (SHA-256 `6B53DFB3D7CF0875A079A6B6A6AA9BCAB45208CF431C1295812DAE117B094C04`).
- Asset branché : `gfx/interface/icons/building_icons/1776_research_laboratory.dds` (SHA-256 `61EEAF87AC2CB8C676E4C4596DE5130BF22F889FF095223EE631022F34E57D36`).
- Aperçu : `docs/reports/assets/tech8c_research_laboratory_preview.png`.
- Export reproductible : `tools/build_research_laboratory_icon.cjs` avec Node.js et Sharp.
- Inspection des icônes originales : `tools/preview_tech8c_pm_assets.py`, lecture/export de prévisualisation uniquement.

Les sept icônes de PM du laboratoire fournies ensuite par l'utilisateur remplacent les icônes du jeu de base :

| Image fournie | PM associé | Asset DDS |
|---|---|---|
| Fiole bleue | Expérimentation instrumentale | `1776_laboratory_manual.dds` |
| Fiole et engrenage bleus | Laboratoire électrifié | `1776_laboratory_electrical.dds` |
| Fiole, engrenage et atome bleus | Laboratoire de haute précision | `1776_laboratory_advanced.dds` |
| Flèches vertes | Recherche générale | `1776_laboratory_general.dds` |
| Usine verte | Recherche de production | `1776_laboratory_production.dds` |
| Plume verte | Recherche sur la société | `1776_laboratory_society.dds` |
| Bicorne vert | Recherche militaire | `1776_laboratory_military.dds` |

Les originaux sont préservés dans `docs/reports/assets/laboratory_pm_icons/`. Le manifeste `docs/reports/assets/tech8c_laboratory_pm_icons.json` relie chaque pièce jointe, son SHA-256, son PM et son export dans `gfx/interface/icons/production_method_icons/`. Correction visuelle du 1er octobre 2026 : les fonds sombres d'origine ont été retirés via l'outil intégré imagegen, avec transparence réelle, et les sept PNG retenus sont conservés sous `*_transparent.png`. La consigne, les chemins et les contrôles sont détaillés dans `docs/reports/assets/laboratory_pm_icons/BACKGROUND_REMOVAL.md`. `tools/build_research_laboratory_pm_icons.cjs` redimensionne et convertit ces détourages en conservant leur alpha ; il n'exporte plus les originaux opaques. Chaque DDS RGBA8 mesure 208 × 208, avec huit mipmaps (208, 104, 52, 26, 13, 6, 3, 1), soit 230 828 octets, conformément aux dimensions natives des PM inspectés.

`tools/preview_tech8c_pm_assets.py` décode les sept DDS exportés indépendamment avec Pillow et produit `docs/reports/assets/tech8c_laboratory_pm_preview.png`, sur damier et à 32 pixels sur fonds clair et sombre. Les sept symboles et leurs ouvertures sont inspectés sur cet aperçu : pas de rectangle de fond. Les fichiers des recettes et du calcul des pénuries sont inchangés lors du détourage, empreintes SHA-256 vérifiées avant/après. Les 1 019 contrôles statiques, dont 34 essais arithmétiques, passent après la correction de transparence. Les références, sources préservées, en-têtes et alpha DDS, recettes 1:1, demande nominale et textes FR/EN sont contrôlés. L'utilisateur confirme que l'ensemble était chargé en jeu avant cette correction visuelle ; l'affichage des nouveaux détourages reste à confirmer après rechargement des textures. Aucun nouvel essai moteur n'est revendiqué.
