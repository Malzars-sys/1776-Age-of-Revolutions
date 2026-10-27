# Amérique du Nord — HBC-01 : contrôle, revendications et connaissance

Date de l'audit : 25 octobre 2026. Date historique : **1er janvier 1776**.

Statut : `AUDITED_HISTORICAL_CLASSIFICATION_READY_GEOMETRY_PENDING`.

## Résultat

La HBC ne doit pas être représentée comme administrant uniformément l'ensemble de sa concession. Le cadre retenu distingue **implantations de la compagnie**, **autorités autochtones**, **prétentions coloniales** et **connaissance géographique**. La charte reste une revendication à documenter, pas une preuve de domination politique de chaque province.

La demande du joueur du 25 octobre ouvre ce lot nord-américain directement. Elle ne vaut ni validation du test balkanique ni clôture des phases du registre WORLD antérieur. Les suivis WORLD/SERG, leurs dénominateurs et leurs reçus humains ne sont pas modifiés.

## Travaux régionaux retrouvés et réutilisés

Le dossier régional est `docs/reports/map/MAP1/inputs/regional_originals/R8_NORTH_AMERICA_CARIBBEAN_*` : incertitudes, sources, recommandations et couverture. Les fiches centrales **0048, 0079, 0083, 0089 et 0095** portent respectivement Manitoba, Nunavut, Ontario, Québec et Saskatchewan. Les empreintes figurent dans `REUSED_WORK.json`.

Ces travaux concluent déjà : compagnie dans les postes, nations autochtones dans leurs territoires ; aucun transfert RGB historiquement vérifié. Les cinq fiches sont encore `MAPPING_REQUIRED`. Les notices de source `CATALOG_ONLY_NOT_FETCHED` n'ont pas été considérées comme des documents lus. Les références pertinentes ont été rouvertes et les compléments ciblés sont distingués ci-dessous. Le dossier `MAP2M/R8` concerne une autre numérotation de passes, en Poméranie : il ne remplace pas la région nord-américaine R8.

## État réel du workspace

Inventaire refait sur les fichiers actuels et le bitmap actuel, sans reprendre comme vérité la baseline d'octobre 10.

| State_ID | ID numérique | Provinces RGB HBC distinctes | Population déclarée sous HBC |
|---|---:|---:|---:|
| STATE_NUNAVUT | 320 | 1 085 | 17 362 |
| STATE_SASKATCHEWAN | 316 | 206 | 11 285 |
| STATE_MANITOBA | 317 | 259 | 32 511 |
| STATE_ONTARIO | 310 | 276 | 23 440 |
| STATE_QUEBEC | 312 | 420 | 24 028 |
| Total | — | **2 246** | **108 626** |

Il existe 2 247 déclarations, car `x8D15CB` est écrit deux fois sous HBC en Ontario. Il ne s'agit pas de deux propriétaires concurrents. Cette anomalie déjà signalée par R8 reste isolée de la question historique.

La HBC possède **toute** la State Region `STATE_NUNAVUT` du jeu, pas seulement un poste. Les quatre autres régions sont partagées. Les State Regions sont des unités du jeu, pas les limites actuelles ou historiques des provinces canadiennes.

Population par code culturel : `anglo_canadian` 21 317, `franco_canadian` 9 338, `metis` 21 399, `cree` 22 567, `inuit` 16 399, `athabaskan` 7 781, `siouan` 9 825. Les 108 626 habitants ne sont **pas** 108 626 employés de la compagnie. Ce sont des POPs attribuées aux territoires sous sa couleur, sans garantie de recensement historique. Une faible densité seule ne prouve pas l'absence de contrôle ; le problème est la nature du pouvoir réellement exercé.

`BUILDING_COMMANDS_CURRENT.csv` relève 21 commandes de création et leurs propriétaires économiques déclarés. Ce n'est pas une somme certifiée des niveaux chargés : l'ordre des écritures et les effets peuvent compter. Les bâtiments `building_railway` relevés peuvent utiliser `pm_traditional_road_network` avec rail/canal désactivés ; leur identifiant ne prouve pas un chemin de fer en 1776. Certaines propriétés économiques appartiennent à `company_hbc` rattachée à GBR, ce qui doit être préservé séparément du futur propriétaire politique.

[Carte de diagnostic actuelle](CURRENT_HBC_EXTENT.png) : jaune = attribution HBC actuelle ; les autres couleurs sont hors du périmètre surligné, sans carte de revendication proposée. Les 2 246 RGB sont consignés dans `HBC_PROVINCE_REGISTER.csv`, avec State_ID, ID numérique, présence dans le bitmap et absence d'attribution historique validée.

## Règle historique retenue

1. **Postes et forts attestés** : contrôler l'emprise de l'établissement et ses installations directement défendues. Une route de traite, un bassin d'approvisionnement ou des partenaires commerciaux ne suffisent pas à colorier tout l'arrière-pays.
2. **Intérieurs autochtones** : représenter les communautés et formations politiques locales ; ne pas les convertir en espaces vides. Un regroupement décentralisé peut être une abstraction, mais pas un État centralisé inventé.
3. **Revendication HBC/britannique** : conserver une couche distincte de la possession, avec portée contestée et limites documentées. Ne pas réduire la charte à un simple contrat commercial : elle contient aussi des prétentions territoriales et des pouvoirs de gouvernement. Cela ne démontre pas leur exercice universel.
4. **Connaissance** : une zone peu cartographiée par les Européens peut déjà être revendiquée par eux et connue/habitée par des peuples locaux. `INCOGNITA` ne signifie donc ni sans population ni sans droits, ni nécessairement sans revendication. Ces dimensions ne sont pas trois propriétaires exclusifs.

La [charte de 1670, transcription du texte primaire](https://www.gutenberg.org/cache/epub/6580/pg6580.html) comporte commerce exclusif, attributions territoriales et facultés d'administration, sous souveraineté royale alléguée. L'étendue de ces prétentions et la possession effective restent à distinguer, comme le soulignent les recherches régionales réutilisées. Le bassin versant n'est pas une limite de contrôle administratif à recopier dans `owned_provinces`.

## Réseau de postes : présences et dates

| Lieu | Décision au départ | Preuve et limite |
|---|---|---|
| York Factory | Conserver un noyau HBC localisé | Poste de 1684 ; représentation des années 1770 et expansion vers l'intérieur documentées par Parcs Canada. Aucune emprise foncière RGB déduite du seul point. |
| Prince of Wales / Churchill | Conserver un noyau fortifié localisé | Reconstruction en pierre à partir de 1732 ; installations de compagnie, pas souveraineté sur les territoires voisins. |
| Moose Factory | Conserver un noyau HBC localisé | Réoccupation de 1730 et activité des années 1770 établies par la désignation patrimoniale. |
| Cumberland House | Conserver un noyau HBC localisé | Fondation en 1774 attestée ; ne justifie pas toute la Saskatchewan. |
| Albany / Fort Albany | Candidat à localiser et contrôler dans les journaux de 1775–1776 | Poste ancien et fonds HBCA B.3 ; aucun périmètre initial RGB acquis. |
| Henley House | Candidat intérieur à ne pas oublier | Implantation antérieure, destructions et reconstructions ; des journaux de 1774 sont mentionnés dans la compilation publique. Les dates 1741/1743 et 1764/1766 divergent selon les synthèses : pas de fausse précision. |
| Eastmain | Candidat à préciser | Fonds B.59/MG20-B59 ; les journaux couvrent 1736–1908 selon le catalogue, mais cette plage seule ne certifie pas chaque année ni un contour. |
| Severn | Candidat à vérifier au départ | Fonds HBCA B.198 ; présence dans une carte multiséculaire insuffisante pour confirmer l'exploitation au 1er janvier 1776. |
| Rupert House / Waskaganish | **Ne pas créer automatiquement un poste actif le 1er janvier** | Une fiche fédérale place la réoccupation en 1776, sans jour/mois identifié. L'ancienneté de Fort Charles (1668) n'établit pas la continuité d'activité. Statut initial laissé ouvert, pas déclaré inexistant avec certitude. |

Le résumé fréquent « Cumberland House est le premier poste intérieur » doit être nuancé par Henley House et sa fonction. Les postes figurant dans le catalogue cartographique HBCA sont de dates très diverses ; ils ne constituent pas une carte de 1776.

Sources ciblées : [York Factory, Parcs Canada](https://parks.canada.ca/lhn-nhs/mb/yorkfactory/culture/histoire-history), [Prince of Wales, Parcs Canada](https://www.parks.canada.ca/lhn-nhs/mb/prince/culture/decouvrir-discover1), [Moose Factory, désignation patrimoniale](https://www.pc.gc.ca/apps/dfhd/page_nhs_eng.aspx?i=46239&id=423), [catalogue HBCA](https://www.gov.mb.ca/chc/archives/hbca/post_maps/index.html), [fonds Eastmain](https://recherche-collection-search.bac-lac.gc.ca/eng/home/record?app=FonAndCol&idnumber=104109&resource=folderlist), [fiche fédérale Waskaganish](https://publications.gc.ca/collections/collection_2018/aanc-inac/R72-221-1995-eng.pdf). La fiche Waskaganish a été repérée par son extrait indexé ; son PDF complet dépasse la capacité de lecture Web utilisée. La compilation historique [Forts and Trading Posts](https://geochem.nrcan.gc.ca/ftp/data/publications/pub_10480/labrador_forts_and_trading_posts.pdf) mentionne des journaux de Henley en 1774 ; cet extrait indexé ne remplace pas l'examen des journaux originaux.

## Décision par grand secteur

- **Nunavut du jeu** : rejeter le maintien d'un contrôle uniforme HBC justifié par la charte. Distinguer les sociétés inuit et, dans les portions méridionales incluses dans cette grande State Region, les autres populations. Le TAG `NNV` existe mais est défini `unrecognized` : le substituer tel quel à toute la région inventerait encore un État unique. Pas de transfert massif automatique vers NNV ou ATB.
- **Manitoba** : isoler York/Churchill des territoires locaux et de l'intérieur. Ne pas rétroprojeter la colonie de la Rivière Rouge (1812). Préserver les acteurs et propriétés de compagnie existants lors de la future réaffectation.
- **Saskatchewan** : présence ponctuelle à Cumberland, pas possession administrative générale. `IRC` existe avec cultures `cree siouan`, `ATB` avec `athabaskan` ; leur existence technique ne certifie pas leurs frontières.
- **Ontario** : distinguer Moose/Albany/Henley et les autres postes confirmés de l'intérieur cri/ojibwé et des juridictions de Québec. La revendication du bassin ne correspond pas à tout l'Ontario.
- **Québec** : séparer les établissements de la côte orientale de la baie James des espaces cris/inuit/innus et des autres juridictions coloniales. Traiter Rupert House selon sa réoccupation réelle, pas sa fondation seule.

## Pourquoi aucun transfert n'est encore appliqué

**Contrainte de jouabilité ajoutée par le joueur le 25 octobre :** aucun poste avancé isolé. Les noyaux retenus devront être reliés au territoire principal par un corridor étroit de provinces du même pays, avec adjacences et accès au marché vérifiés. Cette abstraction de jouabilité ne démontre pas une souveraineté historique sur tout le corridor. Voir [les règles de continuité](../GAMEPLAY_CONSTRAINTS.md). Aucun corridor n'est encore appliqué.

La règle politique est tranchée ; **son emprise RGB ne l'est pas**. Les dossiers R8 ne fournissent aucun polygone historique validé. La géométrie MAP1 est un index en pixels, pas un géoréférencement ; ses métadonnées portent `GPS_projection=NOT_ESTABLISHED`. Le jeu possède un outil de calage plus récent, mais ses points par défaut concernent l'Europe et ne certifient pas la baie d'Hudson.

Les obligations précises restantes sont : localiser les sites réellement utilisés en 1775–1776 ; confronter côtes/embouchures au bitmap avec des contrôles locaux indépendants ; isoler les emprises minimales et les portions autochtones ; identifier les nouveaux propriétaires et la répartition des POPs/bâtiments sans pertes ; choisir une représentation de revendication qui ne déborde pas les bassins attestés. Un `add_claim` au niveau State Region ne suffit pas à dessiner une concession plus fine.

Le nombre de pixels à garder à la compagnie ne peut être choisi par un rayon arbitraire autour d'un nom moderne. L'absence de preuve de contrôle HBC ne permet pas non plus d'attribuer automatiquement chaque RGB à un autre TAG. Ce sont des limites de preuve géographique, pas une demande de reconfirmation de l'autorisation du joueur.

## Vérifications et livraison

Les huit contrôles de `VALIDATION.json` passent : cinq régions retrouvées, couleurs présentes dans le bitmap courant, rattachements aux State Regions cohérents, absence de propriétaire concurrent sur les provinces HBC, conservation des totaux de population/cultures dans l'inventaire, sources locales présentes et absence de modification des fichiers du jeu pendant l'audit. Le doublon interne HBC est signalé séparément.

Livrables : inventaire JSON, tableaux par région, registre des 2 246 provinces, POPs, commandes de bâtiments, carte actuelle, empreintes des travaux R8 réutilisés, classification dans `DECISIONS.json` et périmètre de prochaine implantation dans `NEXT_ACTION.md`. Aucun commit, staging, population réécrite, frontière inventée ou validation moteur/humaine créée.
