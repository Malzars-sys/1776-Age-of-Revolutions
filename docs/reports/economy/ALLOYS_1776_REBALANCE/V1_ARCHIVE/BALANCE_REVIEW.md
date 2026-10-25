# Bilan économique

Statut : `IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION`.

## Hypothèses reproductibles

Quantités par niveau pleinement employé et par semaine, sans débit, accès de marché, pénurie, prix locaux, qualification ou subvention. Prix du mod effectivement chargés par superposition des fichiers : fer 40, cuivre 50, plomb 40, charbon 30, alliages 50, acier 50, aluminium 50, meubles 30, bois dur 40, artillerie 70 £.

Recettes et salaires sont lus depuis les fichiers. Pour les salaires : effectifs × coefficient de profession × salaire annuel d'ouvrier / 52. Ouvrier 1, machiniste 1,5, commerçant 3, ingénieur 3 ; les autres coefficients proviennent aussi des fichiers. Les calculs excluent les dividendes et les impôts. Le salaire de référence 10 £ n'est pas présenté comme une mesure du départ 1776.

## Production primitive et salaires

La diminution des entrants est plus forte que celle du produit pour corriger le très faible rendement initial : 2 450 → 420 £ d'intrants ; 3 000 → 1 000 £ de produits. Les qualifications sont simplifiées, sans ingénieur. Marge avant salaires 580 £, salaire annuel d'ouvrier à l'équilibre environ 12,31 £ pour ce seul PM.

| Hypothèse, PM seul | Résultat hebdomadaire avant taxes/subventions |
|---|---:|
| Prix de base, salaire annuel 5 | +344,42 £ |
| Prix de base, salaire annuel 10 | +108,85 £ |
| Prix de base, salaire annuel 12 | +14,62 £ |
| Entrants +25 %, salaire 10 | +3,85 £ |
| Entrants +25 %, produit −25 %, salaire 10 | −246,15 £ |

La première méthode est utilisable aux hypothèses centrales et ne repose pas sur une subvention fictive. Une recette ne peut garantir un profit face à tous les prix/salaires. La combinaison des premières entrées de tous les PMG existants est contrôlée séparément : 0,4 papier et 40 employés de bureau pour 4 données industrielles s'ajoutent à la recette ; aux prix de base, +285,31 £/semaine à salaire 10. Ce débouché de données reste celui du mod, sans retouche.

Le bâtiment conserve son coût de construction élevé déjà présent : aucune estimation de retour sur investissement réel n'est déduite de ces seules marges.

## Ustensiles : progression des rendements

| PM actif | Matières différentes | Coût entrant | Produit valorisé | Rapport produit/entrant | Marge après salaires à 10 |
|---|---:|---:|---:|---:|---:|
| Fer forgé | 1 | 40 | 60 | 1,50 | 10,38 |
| Cuivre/laiton | 3 | 90 | 150 | 1,67 | 37,88 |
| Usiné | 4 | 120 | 240 | 2,00 | 80,58 |
| Industrialisé | 5 | 220 | 480 | 2,18 | 205,19 |

Tous restent positifs à salaire 10 avec entrants +25 %, même le palier minimal (+0,38). Ce sont les marges incrémentales du groupe secondaire, pas celles de la manufacture entière. Le PM neutre annule intégralement ces apports. Les combinaisons autorisées avec les PM de base et de luxe conservent les anciennes sorties et leur ajoutent exactement 0/2/5/8/16 meubles.

Le fer forgé peut être ancien sans consommer d'alliages. Le palier cuivre/laiton fait apparaître une demande de seulement 0,5 alliage par niveau : 40 manufactures à ce palier consomment la production d'une usine traditionnelle. L'artillerie en consomme 4 : cinq fonderies au bronze absorbent 20 alliages. Ni un canon en fer ni une manufacture au PM neutre ne sont obligés d'en consommer.

## Scénarios explicites

Ces niveaux sont des cas de calcul, pas des estimations de cinq pays réels ni de l'équilibre mondial. Aucune consommation POP n'est convertie arbitrairement en unités.

| Scénario | Niveaux alliages | Niveaux artillerie bronze | Niveaux ustensiles | Production alliages | Nouvelle demande industrielle | Solde avant commerce/POPs/autres industries |
|---|---:|---:|---:|---:|---:|---:|
| Faible industrialisation, importation | 0 | 0 | 5 cuivre/laiton | 0 | 2,5 | −2,5 |
| Métallurgie européenne | 1 | 3 | 10 cuivre/laiton | 20 | 17 | +3 |
| Puissance militaire | 3 | 10 | 20 cuivre/laiton | 60 | 50 | +10 |
| Pays exportateur de meubles | 2 | 2 | 60 cuivre/laiton | 40 | 38 | +2 |
| Industrialisation V–VI | 6 | 10 | 40 usinés | 120 | 60 | +60 |

Le dernier solde n'inclut volontairement pas les anciennes industries modernes, recensées séparément dans le CSV de demande ; ce n'est donc pas un surplus prédit en jeu. La production primitive seule ne suffit pas à généraliser les recettes modernes consommatrices de 10/15/20+ alliages.

## Méthodes avancées préservées

L'arc électrique conserve 90 alliages contre 20, et 5 000 employés contre 2 200 : environ deux fois plus d'unités par employé. Ses entrées valent 3 150 £, ses sorties 4 500 £ ; le PM isolé donne −212,50 £ après salaires à 10, avant automatisation, débit et autres groupes. Cette faiblesse existait avant la mission ; elle est explicitement conservée, pas masquée comme une validation de marge moderne. Le fichier CSV avant/après et les empreintes de tous les autres PM le prouvent.

Les procédés d'aluminium retirant 10 ou 15 alliages à la sortie restent compatibles avec la nouvelle base de 20 : aucune sortie cumulée négative. Leur équilibrage propre reste hors de cette refonte.

Les risques à mesurer sont le volume réel de demande POP à l'échelle mondiale, les salaires locaux, le choix automatique des PM, et la transition vers l'arc électrique. Aucun résultat moteur n'est déduit des seuls tests statiques.
