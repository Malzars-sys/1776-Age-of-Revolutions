# DP-02 — Affinage Durrani et Pendjab

Date de référence : **1er janvier 1776**. Statut : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Installation technique effectuée ; aucune validation en jeu ni clôture historique générale n'est revendiquée.

## Résultat installé

**81 provinces existantes réattribuées**, sans modification du bitmap, des State_ID, des ressources ou des locators. Les 19 transferts de DP-01 demeurent en place. Les modifications portent sur quatre régions : Baloutchistan, Pendjab, collines du Pendjab et Cachemire.

| Administration | Provinces après DP-02 | Changement |
|---|---:|---|
| Bahawalpur | 10 | Administration de Bahawal Khan II, sous allégeance durranie ; plus de contrôle direct afghan uniforme |
| Ladakh | 18 | Gouvernement de Tsewang Namgyal II ; les secteurs occidentaux du Baltistan ne sont pas absorbés par simple copie du vanilla |
| Jammu | 3 | Gouvernement local de Ranjit Dev ; pas d'annexion sikhe anticipée |
| Kangra | 2 | Sansar Chand II ; la souveraineté sur le fort reste une réserve spécifique |
| Chamba | 1 | Raj Singh ; pas d'annexion anticipée de Bhadarwah/Kishtwar |
| Mandi | 1 | Shamsher Sen |
| Kullu | 2 | Pritam Singh |
| Sirmur | 2 | Jagat Prakash |
| Bashahr | 4 | Ugar Singh, datation de règne approximative |
| Garhwal | 5 | Deux cellules des collines ajoutées au noyau existant ; suppression du lien marathe erroné, maintien de Lalit Shah déjà créé par le nettoyage de 1776 |
| Patiala | 7 | Quatre cellules méridionales supplémentaires, en continuité avec le noyau de DP-01 |
| Makran | 18 | Raccordement de Gwadar au Kech et à Panjgur, administration locale Gichki |
| Kharan | 4 | Noyau local distinct, sans lui donner les confins occidentaux par hypothèse |
| Las Bela | 6 | Gouvernement du jam Ghulam Shah et lien avec Kalat |
| Kalat | 17 | Cinq cellules contiguës supplémentaires dans le prolongement central de Jhalawan |

Les sept nouveaux TAGs sont D2J, D2K, D2C, D2M, D2U, D2S et D2B. Les autres définitions existaient déjà. `PLAN.json` donne chaque RGB et chaque propriétaire avant/après. `INSTALLED_MAP.png` est un diagnostic produit à partir des propriétaires installés, pas une capture de Victoria 3.

## Dépendances corrigées

- Histoires nationales explicites, profils agricoles et artisanaux différenciés, souverains de 1776. Les modèles de personnages de 1836 des pays rétablis sont masqués.
- Conservation de l'unique Lalit Shah déjà déclaré dans le nettoyage partagé ; la seconde déclaration découverte au contrôle a été supprimée dans le fichier local de Garhwal.
- Allégeance de Bahawalpur à DUR et de Las Bela à KAL représentée avec institutions, couleur et diplomatie locales. Le versement régulier vaut zéro dans cette abstraction : **cela ne prouve pas historiquement l'absence de tribut**. Aucun taux conjectural ni date précise de compromis du Makran n'est imposé.
- Réaffectation des conscriptions existantes : Bahawalpur 1, Kangra 1, Mandi 1, Ladakh 2, Jammu 1, Makran 1, Las Bela 1. Pas d'augmentation du nombre régional d'unités. Les anciennes unités de Garhwal et les formations de DP-01 sont préservées.
- Bâtiments de la portion durranie du Pendjab transférés à Bahawalpur ; deux niveaux d'administration des collines répartis entre Kangra et Mandi. Conservation de tous les niveaux. Le PM commercial « normal » hérité exigeait une technologie financière absente : il est remplacé localement à Bahawalpur par le PM limité déjà disponible, sans supprimer le centre de commerce ni distribuer une technologie tardive.
- Localisation française et anglaise, descriptions des pactes incluses. Pavillon commun provisoire pour les nouveaux rajas, sans prétention à reproduire leurs étendards historiques.

## Populations : conservation, pas nouveau recensement

Les deux fichiers conservent exactement leurs stocks : **22 545 523** habitants pour le fichier d'Asie centrale et **190 000 000** pour le fichier de l'Inde. Les cultures, religions explicites et catégories serviles de chaque cohorte sont conservées ; les religions implicites restent celles des cultures effectives (contrôlées séparément). Aucune population n'est créée par densité de pixels.

La répartition locale est une allocation technique du stock installé, publiée par cohorte dans `POP_LEDGER.json`. Les poids ne sont pas des estimations historiques validées. Valeurs de contrôle : Bahawalpur 262 096 ; Ladakh 413 321 ; Jammu 236 358 ; Garhwal 311 607 ; Makran 299 386 ; Las Bela 55 450 ; Kharan 18 951. Les populations de ces petits pays nécessitent encore un travail démographique spécialisé.

## Vérifications réellement exécutées

Commande : `python -X utf8 tools/dp02_audit.py`, avec le Python fourni par l'environnement Codex. Résultat final : **135 contrôles réussis, aucun échec** (`VALIDATION.json`).

- 81 changements de propriétaire exactement conformes au plan ; une seule attribution par cellule dans les 190 provinces des quatre régions.
- Continuité terrestre de chacun des quinze pays contrôlés, avec une frontière partagée d'au moins deux pixels ; capitales dans une région possédée et populations présentes.
- Stocks de cohortes, niveaux de bâtiments, types/services/régions des unités conservés ; aucune référence POP/bâtiment vers un propriétaire absent dans les régions touchées.
- Bitmap et tous les fichiers State_Region inchangés dans cette passe. Blocs extérieurs des histoires partagées identiques à leur préimage courante.
- Protection des transferts antérieurs DP-01 et Arabie ; aucun autre changement de fichier runtime détecté pendant l'installation.
- Profils des treize pays rétablis ou affinés : `PASS_STATIC_ONLY`. DUR conserve six alertes techniques antérieures et PAN quatre ; aucune alerte nouvelle pour DUR, PAN, KAL ou PTA. Ces dettes héritées ne sont ni des erreurs observées en jeu ni une validation de leur fonctionnement.
- Personnages de départ uniques, absence des modèles de 1836 contrôlés, localisation bilingue avec BOM et clés uniques.

Les empreintes sont dans `PREPARED.json`, `APPLIED.json`, `REPAIR_01.json` et `CURRENT_RUNTIME_MANIFEST.json`. Les préimages initiales et la première installation restent conservées. Le premier résultat négatif (`FIRST_VALIDATION.json`) est conservé ; il n'est pas effacé pour masquer le défaut commercial corrigé.

## Réserves conservées

Cette V1 remplace les principales administrations durranies manifestement excessives, mais n'est pas un cadastre de 1776. Les cellules peuvent englober de petits voisins des rajas ; elles ne prouvent pas leur soumission juridique. Le calage géographique reste approximatif. Les hautes vallées de Gilgit/Baltistan, les micro-juridictions himalayennes, le fort de Kangra, les dates fines des rapports Kalat–Gichki–Kharan et la composition démographique de Jammu restent ouverts. Ils ne sont pas déclarés historiquement résolus.

**Victoria 3 n'a pas été chargé avec cette version pendant DP-02.** Les contrôles de marchés, de nourriture, de mobilisation, d'affichage et de sauvegarde/rechargement restent à réaliser suivant `RUNTIME_PROTOCOL.md`. Les travaux validés d'Amérique et les suivis WORLD/SERG ne sont pas modifiés par cette passe. L'Asie centrale n'a pas été commencée.

## Recherche locale

ColGrep n'a pas été relancé après l'échec d'accès au verrou d'index constaté en DP-01. Il n'y a donc **aucune nouvelle exécution 2B confirmée dans DP-02**. Les recherches ont utilisé les dossiers connus, les identifiants exacts et `rg`, puis les sources historiques ciblées. Aucun compteur de tokens par mission ni économie comparative fiable n'est disponible. Pas de reconstruction d'index ni modification d'intégration.

La prochaine action proposée est le contrôle en jeu de cette version. Le passage à l'Asie centrale peut ensuite faire l'objet du lot suivant ; le présent document ne le lance pas automatiquement.
