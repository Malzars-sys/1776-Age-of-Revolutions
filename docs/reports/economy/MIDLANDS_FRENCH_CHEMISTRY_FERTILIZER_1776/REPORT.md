# Acier des Midlands, chimie normande et consommation agricole d’engrais

1er novembre 2026 — **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Départ concerné : 1er janvier 1776. Aucun test moteur ni nouvelle validation humaine revendiqués.

## Installation

1. **Grande-Bretagne : un niveau d’aciérie transféré du Yorkshire vers les Midlands.** Dans la déclaration tardive de `98_build_start_1776_world_redistribution.txt`, le Yorkshire passe de deux à un niveau et un niveau identique est créé dans les Midlands. Les PM `pm_coke_blast_furnaces` et `pm_automation_disabled`, les réserves et la propriété du district financier du Yorkshire sont conservés. La référence géographique du propriétaire financier n’est pas la position physique de l’usine et reste donc au Yorkshire.
2. **Normandie française : engrais activés en complément des chambres de plomb.** L’unique usine chimique française de niveau un avait déjà `pm_lead_chamber_process`. Seul `pm_no_fertilizer_production` est remplacé par `pm_artificial_fertilizers`. La pharmacie et les autres champs restent identiques. Aucune technologie ou recette chimique n’est modifiée.
3. **Commerce initial : cinq unités de plomb à l’exportation dans le West Country britannique et cinq à l’importation en Normandie.** Le nouveau fichier d’historique `99_1776_british_lead_french_chemistry.txt` utilise les effets natifs `sg:lead / add_exports` et `sg:lead / add_imports`, au même format que `00_historical_trade.txt`. Le West Country possède les mines de plomb et un port/centre de commerce ; la Normandie possède également un port/centre de commerce. Les deux pays disposent des technologies initiales du commerce et du PM commercial existant.
4. **Engrais des cultures :** les trois PM partagés par le blé, le seigle, le maïs et le millet passent de **5 / 10 / 15 à 10 / 15 / 20**. Conformément à la réponse explicite du joueur, les trois variantes du riz passent de **10 / 20 / 30 à 20 / 30 / 40**. Les coûts de référence indiqués en commentaires sont actualisés ; sorties, emploi, autres intrants, gates et groupes sont conservés. Les autres bâtiments agricoles ne reçoivent pas de PM ni de nouvel intrant. Les recettes d’explosifs qui consomment aussi de l’engrais sont préservées.

## Nature du flux de plomb

Il s’agit d’**ordres commerciaux de départ sur le marché mondial**, mécanisme natif de la version locale. La Grande-Bretagne est mise en position de vendre et la France de demander le volume nécessaire à cette usine. Aucun traité bilatéral fictivement daté ni don de marchandises ou d’argent n’est ajouté.

L’initialisation ne fixe pas durablement l’identité du vendeur de chaque unité ni le volume futur : appariement du marché, capacité commerciale, demande, prix, frais, tarifs et décisions de l’IA restent actifs. Les cinq unités sont des quantités de commerce déclarées, pas la preuve de cinq unités livrées à plein emploi dans une partie exécutée. La confirmation du flux et de son prix nécessite le moteur.

Le relevé des PM explicitement sélectionnés en France ne trouve qu’un consommateur initial de plomb : l’usine chimique de Normandie, **cinq unités par niveau à plein emploi**. C’est le volume retenu pour l’import initial, sans accroître les mines britanniques.

## Échelle économique

Valeurs par niveau et par semaine, à effectif plein, avant bonus de débit et autres groupes de PM :

| Objet | Intrants principaux | Sorties |
|---|---|---|
| Niveau d’aciérie déplacé | 25 fer, 25 charbon | 40 acier |
| Niveau d’outillage au PM existant | 30 bois, 15 fer, 3 acier | 60 outils |
| Usine chimique, deux PM cumulés | 5 plomb, 10 soufre, 10 charbon, 10 outils, 20 calcaire | 40 produits chimiques industriels et 40 engrais |

Le rapprochement de l’acier et des ateliers d’outillage vise le prix local et l’effet MAPI. Un niveau d’aciérie produit théoriquement l’acier consommé par environ 13,3 niveaux d’outillage au PM concerné ; ce n’est pas un résultat d’emploi ou de prix observé.

Aux prix de base du catalogue, les deux PM chimiques procurent **2 800 £ de recettes de biens pour 1 800 £ d’intrants**, soit **1 000 £ avant salaires, transport, fiscalité et autres PM**. Les deux PM ajoutent chacun leur emploi déclaré : leur activation simultanée ne garantit donc pas la rentabilité. L’export initial de cinq unités représente 5 % de la production théorique des cinq niveaux de mines du West Country, avant bonus et emploi réel.

L’augmentation de consommation agricole coûte, au prix de base de 30 £ par unité d’engrais, **150 £ de plus par niveau** pour les quatre cultures ordinaires, **300 £ pour le riz**, sans hausse de production céréalière. Les prix de marché et l’emploi font varier ces montants ; le changement de demande est le réglage de gameplay explicitement demandé.

## Historique des Midlands

**Oui, la production d’acier dans les Midlands est historiquement défendable en 1776.** La lettre de Robert Erskine du **11 octobre 1770, écrite à Birmingham**, décrit la conversion du fer en acier et la fusion au creuset dans les établissements associés à Matthew Boulton. Ce sont des installations du XVIIIe siècle, pas une grande aciérie Bessemer. Le niveau de bâtiment reste une abstraction de gameplay ; aucun déplacement d’une usine historique précise depuis Sheffield n’est affirmé.

Source primaire publiée : Carol Siri Johnson, « Robert Erskine’s letters of 1770 about the British iron and steel industry », *Historical Metallurgy*, 43(2), 2009, pp.75–97 ; **table d’itinéraire p.77 et lettre8 pp.86–88**, texte effectivement consulté. [PDF de la revue](https://www.hmsjournal.org/index.php/home/article/download/165/161/161), [notice éditoriale](https://hmsjournal.org/index.php/home/article/view/165). La date2021 affichée sur le site est celle de la mise en ligne, pas celle du voyage ni du numéro imprimé. La tentative de capture d’image du PDF a échoué ; aucune vérification visuelle de cette capture n’est revendiquée.

Corroboration archéologique : [Historical Metallurgy Society, Archaeology Datasheet302, Steelmaking](https://historicalmetallurgy.org/media/eoikpxmw/hmsdatasheet302.pdf), p.1, passages sur les fours de cémentation des West Midlands, texte effectivement lu. Les thèses repérées mais inaccessibles à l’ouverture ne servent pas de preuve supplémentaire lue intégralement. Le transfert est autorisé pour des raisons de gameplay indépendamment de l’argument historique.

## Contrôles et concurrence

**75/75 contrôles statiques réussis**, résultats dans `STATIC_CHECKS.json`. Commandes exécutées avec le Python local :

```
tools/rebalance_midlands_french_chemistry_1776.py install
tools/rebalance_midlands_french_chemistry_1776.py validate
```

Vérifications : syntaxe des quatre fichiers, déplacement d’un seul niveau et conservation du total britannique déclaré, propriétaire et PM du niveau transféré, restitution exacte des autres octets des deux fichiers partagés de bâtiments, conservation des autres champs agricoles, quantités commerciales, technologies des bâtiments et PM ciblés. Le collecteur de `validate_starting_technology_1776.py` est réutilisé ; les profils nationaux ne sont pas uniformisés ou complétés par des technologies nouvelles.

**Déclarations héritées :** les historiques contiennent deux déclarations britanniques de deux niveaux d’acier au Yorkshire, dans le fichier régional et dans la redistribution. Leur somme déclarative passe de quatre à trois, les Midlands de zéro à un ; la déclaration tardive passe de deux à un. Cette somme statique ne constitue pas une mesure d’effectifs observée en moteur. La redondance héritée n’est pas refondue dans ce lot.

Préimages et empreintes de l’état courant dans `BASELINE.json` et `preimages/`. Les scripts, technologies, recettes hors des six champs agricoles autorisés, carte et fichiers canoniques SERG protégés restent inchangés. Les modifications concurrentes déjà présentes au Groenland, en Islande et dans le suivi SERG sont conservées. Aucune opération Git d’écriture ni modification du vanilla. Les autres dossiers et anciens reçus ne sont pas réécrits.

## Vérification moteur restant à faire

Nouvelle partie1776 : confirmer le niveau d’acier déplacé et le prix local dans les Midlands ; vérifier les deux PM chimiques en Normandie ; inspecter les ordres et livraisons de plomb après le calcul commercial initial ; vérifier emploi, intrants, sorties et budget des bâtiments concernés ; comparer les trois paliers agricoles ordinaires et du riz ; sauvegarder/recharger si nécessaire. Aucun résultat moteur ni profit garanti n’est attesté par cette livraison.
