# MAP-2M-R4 — Dossier documentaire et recalages locaux

Date cible : **1er janvier 1776**. État de la recherche : **MAP_2M_R4_PARTIAL**.

Le dossier est livré, mais les frontières ne sont pas déclarées terminées et aucune nouvelle cellule n'est autorisée pour un transfert inconditionnel en R5. L'acquisition documentaire progresse nettement ; le passage de la carte ancienne aux pixels natifs reste insuffisamment contrôlé. Ce résultat ne constitue pas une nouvelle validation en jeu.

## 1. Référence conservée

R3 est enregistré comme **PASS_RUNTIME_USER_VALIDATED**, sur la seule déclaration du joueur. Aucune durée de simulation ni aucun journal moteur n'est inventé. L'attestation est conservée ici, dans `R3_USER_RUNTIME_VALIDATION.json`, sans réécrire les anciens rapports pendant cette mission limitée à R4.

- `x567452` : 357 cellules suédoises.
- `xEDB010` : 85 cellules prussiennes à Bromberg.
- `xFCC7B7` : 142 cellules polonaises résiduelles.
- Population mondiale : **835 804 980**.
- Aucun nouveau RGB, transfert, bâtiment, PM, population, unité ou registre impérial modifié.
- Thorn `x41A021` reste inchangé et hors périmètre.

Les empreintes initiales sont dans `BASELINE.json`. Les résultats finaux, avec chaque assertion et les anomalies héritées, sont dans `GEOMETRY_VALIDATION.json`. Le HEAD et l'index Git sont également comparés par lecture seule. Aucun commit, merge ou push n'est effectué.

## 2. Avancées documentaires effectives

### Nouvelle carte de frontière : Kart. N 1146/1, [1772]

Une recherche ciblée dans le catalogue SBB a permis de retrouver une **édition numérique de 2025**, accessible sans inscription, d'une carte manuscrite intitulée *Carte von der neugemachten Grentze zwischen der acquirirten Provintz und dem Königreich Pohlen ...*.

[Notice officielle](https://stabikat.de/DB=1/XMLPRS=N/PPN?PPN=1936716976) — [reproduction institutionnelle](https://resolver.staatsbibliothek-berlin.de/SBB000396D400000000).

La notice indique `[1772]`, environ 1:136 000, 55 × 134 cm, dessin colorié, **« Brouillon oder flüchtige Kopie »**. La date reste une attribution de catalogue ; la datation de chaque ajout manuscrit n'est pas démontrée.

Les deux rectos complets ont été acquis, chacun à **13 001 × 9 588 pixels**, avec leurs deux versos et une image de mire. Ces cinq images représentent **un seul objet**, pas cinq preuves indépendantes. Les rectos se recouvrent ; ils ne sont pas assemblés par un collage prétendument géographique.

La carte montre réellement Deutsch Krone, Schneidemühl/Piła, Kamin et Bromberg, ainsi que le corridor de la Netze jusqu'à la Vistule. Elle ne fournit pas une restitution détaillée de l'intégralité du district méridional d'Inowrocław. Les mots de voïvodies ne sont pas des points de contrôle urbains. Les noms écrits en rouge concernent notamment des possessions privées selon la note de la carte : leur couleur n'est pas une preuve automatique de souveraineté.

Cette acquisition lève un manque documentaire important, **pas encore le manque de correspondances physiques avec le bitmap du jeu**. Aucun masque territorial n'est produit à partir d'une interprétation non établie de toutes ses couleurs.

### Pfau : cinq feuilles détaillées acquises légalement

[Catalogue WBC](https://www.wbc.poznan.pl/dlibra/publication/773069/edition/588634?language=pl) — [manifeste public IIIF](https://mirabilia.amu.edu.pl/iiif/manifest/588634.json).

Acquis à 4 000 pixels de large : XXXIX Inowratzlaw, XLV Thoren, XLVI Znin, XLVII Zarnikow et XLVIII Dreisen, plus l'index de série et un verso portant une liste manuscrite. Le verso `0002` n'est pas compté comme couverture géographique.

Le catalogue distingue les **relevés de 1772–1773**, la gravure de **1775–1778** et l'édition **[1778]**. Les feuilles gravées sont globalement orientées au sud ; la version de lecture XXXIX est tournée exactement de 180°, sans prétendre que ce redressement rend son axe vertical parfaitement nord-sud. Les noms, croix d'églises, routes et plans d'eau sont exploitables pour des comparaisons topographiques. Les limites gravées de 1778 ne sont pas automatiquement des limites au 1er janvier 1776.

L'index et les feuilles choisies ne justifient pas une couverture détaillée complète de Wałcz et de Kamin. Elles améliorent surtout le corridor occidental/méridional et les environs d'Inowrocław. Les cinq feuilles appartiennent à la même famille de levés : elles ne sont pas cinq confirmations politiques indépendantes.

### Pfau manuscrit AGAD : contradiction conservée

L'[inventaire officiel du fonds 447](https://www.agad.gov.pl/inwentarze/kart447InOd.html), unité **580**, donne *Mapa Pfau'a*, cotes **AK. 103, 104, 105, 106, 107, 107 A**, mais date l'objet **1800–1815**. Il s'agit d'un inventaire provisoire ; cette indication ne suffit pas à expliquer la genèse de la copie, mais interdit de la présenter comme l'original certain des relevés de 1772–1773.

Aucune image du manuscrit n'a été acquise. La mention de galerie dans le code HTML est un fragment commenté et générique, pas un lien de numérisation actif vérifié. Aucun compte, paiement, demande à un archiviste ou contournement d'accès n'a été effectué.

### Grund 1775 : original intégral non obtenu

L'extrait Driesen–Landsberg existant est réutilisé, sans nouveau téléchargement. La [notice SBB PPN428487513](https://stabikat.de/DB=1/XMLPRS=N/PPN?PPN=428487513) confirme **Kart. N 10051**, 1775, manuscrit colorié, environ 1:222 000, 117,5 × 67,5 cm, **« N unten »** et l'absence de la Pomérélie septentrionale. L'auteur y est transcrit `[I. A.] Grund [d. Älteren]`.

Aucun accès intégral public n'a été trouvé dans les notices et liens inspectés. Ce constat borné n'est pas une preuve qu'aucune reproduction n'existe ailleurs. La voie officielle est le [service de reproductions SBB](https://staatsbibliothek-berlin.de/service/digitalisate-und-reproduktionen), avec la cote et le PPN précités, en demandant l'intégralité en couleur et la conservation de l'orientation et de l'échelle. Aucune commande n'a été passée. La carte N 1146/1 constitue désormais une alternative gratuite substantielle, sans remplacer implicitement Grund ni couvrir toutes ses lacunes.

### Anklam 1773 : plan contemporain retrouvé

Le [livre de Stavenhagen, publié à Greifswald chez Röse en 1773](https://www.digitale-sammlungen.de/de/details/bsb10001079), contient à la vue **35/658** un *Grund Riss von der Stadt Anklam*. Le plan replié complet est acquis à **4 000 × 2 259 pixels**. Sa légende identifie Marienkirche (2), Nikolaikirche (3), Pulverturm (7) et Steintor (13). Un moulin figure au nord du pont.

Les empreintes modernes des édifices proviennent d'un extrait OSM public, acquis en lecture seule ; les centres sont calculés comme centroïdes surfaciques des polygones, pas comme positions de labels. La [notice municipale](https://www.anklam.de/Kultur-Tourismus/Anklamer-Geschichte/Europ%C3%A4ische-Route-der-Backsteingotik-ein-Stadtrundgang/Route-Stadtzentrum-Gr%C3%BCn-/) documente les édifices, les reconstructions du pont et le moulin de 1728 sur le Peendamm suédois. **Le pont moderne n'est pas adopté comme point exactement stable** : la municipalité décrit plusieurs remplacements et un pont voisin. Le moulin est un homologue provisoire, non une identification géodésique certifiée.

Les cadastres GeoGREIF de 1694 et les données LUNG déjà conservés restent utiles pour la morphologie ; ils ne sont pas retéléchargés. Les images GeoGREIF à usage local restreint ne sont pas reproduites dans les nouvelles superpositions. Une carte cadastrale de 1694 ne démontre pas la souveraineté de 1776.

## 3. Géoréférencement réellement calculé

### Deux étapes explicitement séparées

1. **Source → réel** : plan de travail métrique local équirectangulaire, longitude/latitude WGS84 des références. Ce choix est un système de calcul, **pas une découverte de la projection historique**. Les axes de l'image sont explicitement traités avec Y descendant et la réflexion nécessaire.
2. **Réel → bitmap** : aucun nouveau modèle exact n'est validé. L'hypothèse Miller et l'offset R2/R3 ne sont conservés que pour les visualisations signalées comme diagnostiques. Aucun bâtiment historique n'a ici d'homologue physique identifié dans le bitmap natif. Une distance à une rivière ou au rivage le plus proche n'est pas transformée en erreur certifiée d'une ville.

### Résultats sur les contrôles réservés avant l'ajustement

| Source | Modèle | Résidu moyen des 3 points d'ajustement | Écart moyen des 2 contrôles réservés | Maximum des contrôles |
| --- | --- | ---: | ---: | ---: |
| Anklam 1773 | Similitude avec réflexion d'axe | 27,08 m | 48,67 m | 74,90 m |
| Anklam 1773 | Affine | ≈ 0 m par construction | 99,61 m | 167,46 m |
| Pfau XXXIX | Similitude avec réflexion d'axe | 643,74 m | 3 722,35 m | 3 965,36 m |
| Pfau XXXIX | Affine | ≈ 0 m par construction | 3 189,21 m | 4 250,79 m |

**Portée de ces chiffres :** ce sont des désaccords source–références réelles, pas des erreurs en pixels du jeu. Les références modernes ne sont pas des levés indépendants réalisés pour ce projet. À Anklam, Steintor donne 22,45 m en similitude ; le moulin provisoire donne 74,90 m. L'échantillon est local et réduit : il ne certifie ni toute la Peene, ni Wolgast.

Pour Pfau, les contrôles d'Inowrocław et de Pakość restent ambigus au niveau de l'édifice exact. Les écarts ne permettent donc **ni d'affirmer une erreur intrinsèque de 4 km de la carte, ni de valider notre lecture**. Ils démontrent que cette première combinaison de points n'est pas assez fiable pour tracer une frontière. Les identifications, la déformation de la planche et la correspondance des sites restent à départager. Le modèle est rejeté pour les attributions territoriales. Aucun réajustement des contrôles réservés n'a été fait pour obtenir artificiellement un meilleur score.

Une projective à huit paramètres n'est pas ajustée à seulement trois ancrages ; aucun polynôme n'est utilisé. L'affine passant exactement par trois points n'est pas présentée comme supérieure à la similitude.

### Sensibilité, et non intervalle de confiance

- Retrait d'un point d'ajustement en similitude : Anklam, écarts de **78,98 à 82,46 m** ; Pfau, **1 561,53 à 4 453,37 m**.
- 250 perturbations reproductibles des lectures, dans des disques de rayon déclaré en pixels source : déplacement maximal des contrôles Anklam **26,20 m** en similitude et **36,24 m** en affine ; Pfau **407,15 m** et **1 527,02 m**.
- Désaccord entre modèles aux contrôles : Anklam **40,83 et 97,37 m** ; Pfau **369,65 et 3 498,08 m**.

Ces enveloppes mesurent la sensibilité aux lectures choisies ; elles ne sont **pas** des intervalles probabilistes, ne couvrent pas une mauvaise identification, et ne prouvent pas la stabilité historique des berges. Le retrait d'un point d'une affine à trois points est non identifiable et n'est pas chiffré.

Les fichiers `*_WGS84_DIAGNOSTIC.png`, avec `.pgw` et `.prj`, sont des rasters de travail géoréférencés reproductibles, explicitement non approuvés pour le découpage politique. Les coordonnées et paramètres complets figurent dans les CSV et JSON. Les superpositions `PEENE_GEOREFERENCE.png` et `NETZE_GEOREFERENCE.png` portent leur avertissement dans l'image ; leur quadrillage est celui des cellules actuelles, pas une modification de `provinces.png`.

## 4. Propositions et limites restantes

- **Classe A nouvelle : 0 cellule.** Aucun nouveau transfert prêt à appliquer sans condition.
- **Peene : 18 cellules B**, un groupe contigu, déjà laissées en attente par R3 près du Peenestrom.
- **Netze : 77 cellules B**, cinq groupes contigus, reliquat des 162 anciennes candidates après exclusion des 85 cellules déjà prussiennes. Ces 77 cellules sont des hypothèses héritées, **pas une nouvelle frontière déduite de Pfau ou de N 1146/1**.
- Les manques documentaires non localisables sans arbitraire sont en classe C dans `UNRESOLVED.csv`, sans coordonnées ou RGB inventés.

Chaque ligne de candidat est relue sur le bitmap installé et résolue vers son RGB, son State_ID et son propriétaire actuels. Aucun RGB de destination n'est inventé. L'appartenance d'une ville à la Prusse ne suffit pas à attribuer toute une province multicolore ou tout un district partagé.

Les notices GStA déjà acquises distinguent désormais explicitement : Tit.50 Nr.1a (table de bornage de septembre 1772), Nr.1 (poteaux vers Thorn, **1776**, sans preuve de validité au 1er janvier), Nr.2 (régulation par von Stach, **1777**), Nr.10 (Ostroveck/Skotnicki, **1776–1780**). Les manuscrits ne sont pas consultés : ces notices ne résolvent pas leur contenu. Une frontière de 1777 ne remplace pas celle de 1776.

## 5. Livraison et reproduction

Tous les nouveaux fichiers se trouvent dans ce dossier R4. Aucun travail n'est écrit ailleurs. Le catalogue `SOURCES.json` contient les URLs, dates distinctes, dimensions, droits, fichiers et SHA-256. `DELIVERABLE_MANIFEST.json` recense les empreintes du dossier final, sans se hacher lui-même.

Depuis le dépôt, avec Python/Numpy/Pillow disponibles :

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python docs/reports/map/MAP2M/R4/analysis.py calibration
python docs/reports/map/MAP2M/R4/deliver.py build
python docs/reports/map/MAP2M/R4/deliver.py validate
```

Ces étapes relisent les sources locales ; elles ne téléchargent rien et n'écrivent aucun fichier fonctionnel. Ne pas relancer `research.py capture` : il refuse de remplacer la référence initiale.

Les validations finales distinguent l'intégrité technique de la validation historique encore partielle. Les **44 doublons RGB et 12 références invalides hérités** restent ouverts ; l'égalité complète des historiques, populations, cultures, religions, bâtiments, PM, propriétaires économiques, unités et recrutements effectifs est contrôlée contre la référence R4. Aucun test moteur automatisé nouveau n'est revendiqué.

ColGrep n'est pas nécessaire à cette continuation : les chemins et helpers étaient déjà connus et vérifiés. Aucun gain exact de tokens n'est mesurable ; les compteurs de consommation de cette tâche ne sont pas disponibles. Aucun appel supplémentaire n'est lancé pour fabriquer une statistique.

## Conclusion

La recherche n'est plus bloquée par l'absence totale de documents détaillés : une nouvelle carte de frontière [1772], cinq feuilles de Pfau et un plan d'Anklam 1773 sont acquis et traçables. **La reconstruction complète des frontières et leur conversion fiable en nouvelles cellules ne sont pas encore obtenues.** Le prochain travail précis est décrit dans `NEXT_IMPLEMENTATION_PLAN.md`, sans autoriser d'import aveugle des hypothèses B.
