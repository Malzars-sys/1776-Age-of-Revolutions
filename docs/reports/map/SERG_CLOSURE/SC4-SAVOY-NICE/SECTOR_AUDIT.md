# Audit Savoie–Nice au 1er janvier 1776

## Inventaire réel

Pays existant **SAR**, royaume reconnu; capitale `STATE_PIEDMONT` (Turin), Victor-Amédée III déjà installé, monarchie et lois initiales conservées. Aucun pays savoyard distinct ou nouveau vassal nécessaire. Le TAG sert plusieurs pays historiques sous le même souverain et ne leur donne pas un statut impérial uniforme.

| Agrégat SAR | RGB / cellules | Population écrite | Administration publique avant / prévue |
| --- | --- | --- | --- |
| STATE_SAVOY | 4 / 802 | 365 664 | 0 → 1 |
| STATE_PROVENCE, seule subdivision SAR | 1 / 177 | 134 316 | 0 → 1 |
| Piémont, contexte protégé | 9 / 2 227 | 1 921 911 | 4 → 4 |
| Île de Sardaigne, contexte extérieur | 8 / 1 621 | 408 786 | aucun changement |

Périmètre principal : **5 RGB / 979 cellules, 499 980 habitants écrits**, populations conservées sans prétendre à un recensement historique. Les 134 316 habitants sont ceux de la seule portion SAR de Provence, pas de toute la région. RGB et tous les voisins : NATIVE_INVENTORY.json; tableau avant/après et carte native disponibles. Les deux déclarations de port identiques de Nice sont héritées, conservées; leur présence ne constitue pas deux ports historiquement certifiés. Réseau routier, activités, unités et futurs placements de forteresses ne sont pas réécrits.

## Frontières et juridictions

- Duché et administrations savoyardes sous SAR : Chambéry, Genevois, Faucigny/Chablais, Maurienne et Tarentaise distingués de la France et des États suisses. Aoste et Piémont sont des pays voisins de la même monarchie, non des synonymes du duché. Les contours contemporains franco-italiens ne décident pas de leur souveraineté en 1776.
- Genève : appliquer le traité de 1754 et ses réserves. Les cessions de 1815/1816 ne sont pas acquises en 1776. L'agrégat SWI du jeu ne suffit pas à homologuer les alentours genevois; ne pas prendre une confession, un droit privé ou un ancien diocèse pour une frontière d'État.
- France : accords de 1713/1718 puis 1760; Barcelonnette demeure française, versant piémontais et cols à distinguer. Rhône et Guiers Vif structurent la limite savoyarde; les échanges riverains de 1760 interdisent de copier simplement la carte de 1750.
- Nice : Var/Estéron et cessions du Haut-Var, Tende et accès de Villefranche à distinguer des voisins français, monégasques et génois. Les acquisitions françaises de 1792/1793, 1796 et 1860 sont exclues. Une province SAR proche de Nice n'est pas une preuve de couverture de tous les villages cédés en 1760. Aucun RGB français ou génois entier annexé pour compléter une vallée.
- Oneglia/Loano et autres fiefs ligures restent interfaces seulement, réservées à SC4-LIGURIAN-FIEFS. Les noyaux milanais et les Trois Ligues déjà acquis ne sont pas touchés.

## Constitution impériale : diagnostic et décision bornée

SAR est déjà membre du bloc et du déclencheur impérial, sans titre électoral; neuf RGB piémontais sont inscrits parmi **574 lignes**. Aucun des quatre RGB de Savoie ni `x5080E0` de Nice n'est inscrit. L'île de Sardaigne ne l'est pas non plus. Le membre national, le registre de droits territoriaux et la souveraineté SAR sont trois données différentes.

Les diplômes décrits dans SN-S04 et les dossiers de 1733 et 1773–1774 démontrent qu'un titre royal extérieur ne supprime pas les droits impériaux continentaux. Ils ne permettent pas de transformer le vicariat, notamment sur des diocèses extérieurs, en propriété sarde. Les efforts électoraux de 1773 ne donnent aucun électorat acquis.

Le modèle courant crée une obligation impériale au niveau du pays et utilise chaque ligne du registre pour les demandes et retours automatiques de provinces, notamment `aor1776_hre_return_requested_provinces`. Une nouvelle ligne est donc une modification fonctionnelle de droits, pas une simple étiquette historique. Le registre ne distingue pas aujourd'hui, pour ces territoires, vicariat, investiture contestée et contrôle de restitution automatique.

**Aucune exclusion définitive de Savoie/Nice approuvée.** Leur absence est une lacune P0 à instruire, conservée visible. Pas d'inclusion de toute SAR, pas de suppression de l'appartenance nationale existante. Le blocage porte sur la correspondance de la limitation ancienne aux RGB et la qualification des droits à inscrire et des obligations à appliquer; pas sur l'existence des offices locaux, directement exploitable.

Hypothèses concrètes pour reprise, sans relancer un ancien calage :

1. Proposition B continentale : confronter les quatre RGB de Savoie à l'édition 1772 et aux cartes de 1754/1760; documenter les franges genevoises et les pays alpins puis proposer une liste fermée de droits SAR. Les quatre RGB ne sont pas approuvés automatiquement par le nom STATE_SAVOY.
2. Nice : confronter `x5080E0` et les RGB français/génois limitrophes aux cartes des limites 1760/1763–1764 et aux actes; distinguer souveraineté, Tende/Monaco et extensions de vicariat. Pas de transfert sans attribution défendable.
3. Établir le contenu opératoire des investitures/dossiers 1773–1774 référencés par le MAE, puis qualifier une extension bornée du registre ou une représentation différenciée dans les mécanismes existants. Un arbitrage explicite doit présenter les effets de restitution, sans inventer de tribut ni de vassalité.

## Corrections installables maintenant

**SN-I-SAV** : un niveau administratif public SAR dans STATE_SAVOY pour les offices régionaux attestés à Chambéry, sans déplacer la capitale de Turin. **SN-I-NIC** : un niveau public SAR dans sa seule subdivision de STATE_PROVENCE pour les offices et le Sénat de Nice. Deux fichiers nouveaux, aucune réécriture partagée.

Catégorie **B d'abstraction institutionnelle** : un niveau représente une capacité minimale de jeu, pas un sénateur, un effectif, un budget ou une réforme datée précisément. Les quatre PM sont vérifiées contre les définitions effectives et les lois/technologies de SAR. La monarchie est conservée. Ce ne sont ni deux nouveaux États souverains ni un changement de régime.

Statut régional prévu **BLOCKED**, installations **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION** après contrôles. Aucun point supplémentaire. Leur futur test ne certifiera ni les frontières ni les obligations impériales. Les blocages italiens, Innviertel, Hohenberg/Fricktal/chantier naval et Teschen restent indépendants.
