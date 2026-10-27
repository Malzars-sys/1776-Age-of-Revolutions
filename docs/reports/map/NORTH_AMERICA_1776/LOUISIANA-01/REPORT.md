# LOUISIANA-01 — Louisiane espagnole au 1er janvier 1776

**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION — 27 octobre 2026.** Installation effectuée ; aucune validation moteur ou humaine déclarée. Aucun commit, merge, rebase, push ou changement du vanilla.

## Territoires installés

La Louisiane possède désormais **30 provinces**, contre 28 auparavant, dans **trois State Regions partagées** :

| Région | Louisiane | Autres changements |
|---|---:|---|
| Louisiane | 19 | 6 provinces du nord-ouest rendues au regroupement caddo ; 3 provinces britanniques retirées de cette State Region |
| Arkansas | 6 | Poste des Arkansas et corridor du Mississippi ; l'intérieur demeure autochtone |
| Missouri | 5 | Saint-Louis, Saint-Charles, Sainte-Geneviève et corridor ; l'intérieur demeure autochtone |

**20 changements de propriétaire**, tous listés dans `PLAN.json`. Les trois cellules Baton Rouge–nord des lacs sont rattachées à la **Floride occidentale britannique**, désormais 12 provinces. Cela sépare leurs revendications de celles de la Louisiane, au lieu d'ajouter une prétention espagnole sur une région mixte.

Chaque poste est relié à la Nouvelle-Orléans par des côtés de provinces et par un chemin terrestre de pixels, en tenant compte des interdictions de passage natives. Les seules portions LOU des États partagés sont explicitement **incorporées**. Une cellule de rive évite une poche quapaw isolée ; `COMPACTNESS_AMENDMENT.json` en explique la concession. La liaison et l'incorporation ne certifient pas encore l'accès au marché, la capacité d'infrastructure ou le ravitaillement en jeu.

Les hubs urbains sont corrigés : **Nouvelle-Orléans** remplace Baton Rouge comme ville louisianaise ; **Poste des Arkansas** remplace Little Rock, ville tardive. Le poste de 1776 est représenté dans sa zone aval, et non sur le site actuel occupé à partir de 1779. Les cellules du corridor proches de New Madrid ou Cape Girardeau ne sont pas présentées comme des établissements déjà fondés.

## Contrôle et revendications

Les grands espaces des plaines restent sous les autorités autochtones. La Louisiane reçoit les claims manquants du bassin du Mississippi/Missouri ; les prétentions USA anachroniques à l'ouest du fleuve sont retirées dans les **13 régions concernées**, ainsi qu'au Texas pour préserver le domaine de la Nouvelle-Espagne. Les claims LOU/SC1 du Mississippi oriental sont également retirés : **15 régions de claims modifiées** au total.

Le Texas et le Nouveau-Mexique conservent leurs revendications de Nouvelle-Espagne. Le double claim du Colorado est conservé : il représente deux domaines dans un State Region mixte, pas une frontière de conflit certaine couvrant tout l'État moderne. Les claims de montagne et du Minnesota débordent partiellement le bassin à cause de la granularité du jeu ; cette limite est déclarée dans [SOURCES.md](SOURCES.md). Aucun règlement frontalier de 1819 ni conquête de 1779 n'est rétroprojeté.

Ces priorités utilisent la mécanique native de revendication et d'intérêt pour limiter la colonisation concurrente. Elles ne garantissent pas une séparation intangible après toutes les évolutions possibles d'une campagne.

## Conservation et économie

**Aucune population supprimée ou créée par cette mission**, aucune conversion de culture, religion ou statut. Chaque total de cohorte par pays est conservé. Les **212 172 habitants hérités de la Louisiane** restent à la Louisiane : placement technique de 1 600 au Missouri et 400 en Arkansas, retranchés des mêmes cohortes de Louisiane. Les 500 Caddos placés dans la portion restaurée proviennent de leur portion d'Arkansas, sous le même pays.

Ces chiffres ne sont **pas un recensement de 1776** : le total colonial hérité est nettement trop élevé et reste un problème distinct. Les faibles populations des postes ne sont pas des estimations démographiques nouvelles. Les cohortes native et coloniale, les bâtiments, niveaux, propriétaires économiques, PM et formations existants sont préservés.

Le transfert administratif des trois provinces britanniques déplace 13 terres arables et une fraction explicite des potentiels de ressources vers la Floride occidentale. Chaque potentiel total Louisiane + Floride occidentale est conservé. Cette répartition est une approximation technique, sans affirmation de réserves géologiques historiques. Aucun bâtiment n'est effacé pour s'adapter au redécoupage.

## Vérifications et concurrence

**56 contrôles réussis** dans `VALIDATION.json` : propriétaires prévus, unicité des RGB concernés, absence de nouveaux trous ou doubles propriétaires, références et hubs, claims ciblés, sommes des populations et identités, bâtiments et profils conservés, capacités régionales, chemins terrestres des postes et absence de poche quapaw/caddo/britannique créée. Le témoin terrestre HBC–Québec–USA est également relu sur la carte actuelle. Les empreintes et patchs sont archivés dans `PATCH.json` et `patch/` ; les fichiers de départ dans `before/`.

Les tests de non-régression du verrou colonial américain ont été réexécutés : **8 réussites**. Les audits de connaissances avant/après LOU, CAD, QPW, OSG, COM et GBR n'ajoutent **aucun nouveau signalement**. Les erreurs héritées restent distinctes : LOU 13, COM 2, GBR 6 ; CAD/QPW/OSG restent en revue historique. Parmi les dettes LOU, le port sélectionne un PM demandant `enclosed_dock_systems`, déjà absent avant cette mission. Aucun don général de technologies n'a masqué ces problèmes.

Les **28 doubles propriétaires préexistants** du dépôt restent hors de cette correction, sans nouvelle anomalie de ce type dans les RGB traités. Les anciennes attestations R8/Floride/Colonies restent datées de leur version ; leurs hashes globaux et l'ancien compte de neuf provinces de Floride occidentale ne sont pas réécrits.

Des travaux concurrents ont modifié Tripoli, le désert libyen et le Sénégal ainsi que des fichiers sahéliens. Les blocs ont été repris exactement depuis le fichier vivant lors de la retouche bornée ; `CONCURRENT_SHARED_CHANGES.json` et `CONCURRENT_FILES.json` les distinguent de cette mission. Le bitmap mondial a aussi changé de **5 pixels au Sénégal**, hors de toute l'Amérique du Nord. Comparaison à son fichier de départ dont le hash correspond à notre baseline : rectangle nord-américain 0,0–3000,1900 identique pixel par pixel. Le premier contrôle global du bitmap, devenu faux pour cette raison externe, est conservé avec la preuve indépendante dans `CONCURRENT_BITMAP_CHANGE.json` ; aucune restauration de ces travaux.

## Limites ouvertes

- Corridors et six cellules caddos : représentation régionale par provinces existantes, sans cadastre homologué.
- Natchez/Panmure britannique, les implantations de la haute Red River et les villages autochtones de la basse Louisiane ne sont pas tous représentés finement ; leur recherche ne doit pas être confondue avec une annexion générale.
- La frontière interne Texas/Louisiane près de l'Arroyo Hondo reste une approximation à cette échelle. Les claims des régions montagneuses et des sources du Mississippi doivent être affinés si de nouveaux State Regions sont autorisés.
- Démographie héritée et accès économique effectif des postes à contrôler ; pas de promesse de rentabilité ou de ravitaillement observé.

## Test en jeu

Créer une **nouvelle partie en 1776**. Vérifier Louisiane espagnole, capitale Nouvelle-Orléans, Arkansas Post et Saint-Louis ; parcourir le corridor, contrôler les trois portions incorporées, les habitants et les anciens bâtiments. Vérifier les trois cellules britanniques et les 12 provinces de Floride occidentale.

Ouvrir les claims du bassin, vérifier l'exclusivité de colonisation face à Nouvelle-Espagne et aux USA avec les intérêts actifs, puis le cas mixte du Colorado. Le verrou américain d'avant indépendance doit rester actif. Contrôler HBC–Québec–USA, l'accès au marché des postes, un mois de simulation et sauvegarde/rechargement. Le moteur n'a pas été lancé par cette mission.

ColGrep : un appel échoué avant recherche, modèle 2B non attesté ; aucune économie exacte de ressources mesurable. Détail et sources historiques dans [SOURCES.md](SOURCES.md).
