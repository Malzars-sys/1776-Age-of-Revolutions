# Sources et portée — Prusse occidentale

Consultation : 5 novembre 2026. Cible : 1er janvier 1776. Aucun résultat local n'est transformé en règle permanente.

## Cartes réellement obtenues et lues

1. **J. C. Schloenbach, Charte von der Grafschaft Ravensberg, 1772.** Original signalé par le portail du Kreis Herford : Staatsbibliothek Berlin, no 31 615, manuscrit colorié, environ 1:60 000. [Catalogue institutionnel](https://geoportal.kreis-herford.de/geschichtsportal/kartengalerie.html), [reproduction fournie par le portail](https://geoportal.kreis-herford.de/geschichtsportal/daten/karten/1772_grafschaft_ravensberg.jpg). Fichiers `HERFORD_CATALOGUE.html`, `RAVENSBERG_1772.jpg`, vue générale et grille dans ce dossier. Le titre et 1772 sont visibles sur la carte ; Herford, Bielefeld, Ämter et voisins sont lus. Cette source ne fournit pas les coordonnées natives du jeu.
2. **Cleve, Geldern, Meurs und Mark**, [Berne MUE Ryh 5106:3 B, DOI e-rara-124818](https://doi.org/10.3931/e-rara-124818), [notice Ryhiner](https://ryhiner.ub.unibe.ch/de/world/volume/150/image/10464). Notice : Hambourg, Carl Ernst Bohn, **1793**, environ 1:720 000. Le manifeste observé `CLEVE_MANIFEST.json` fournit le service image ; reproduction 4 000 pixels `CLEVE_GELDERN_MARK_1793.jpg`, vue générale et grille. Mention d'une réduction d'après Sotzmann lue en marge. La carte est postérieure de dix-sept ans à la cible : ni ses couleurs ni un simple nom de province ne suffisent à homologuer une frontière de 1776.
3. **D. Robert de Vaugondy, Carte des cercles du Haut et du Bas-Rhin, 1753**, exemplaire Santini de **1777** déjà conservé. [Notice BnF](https://catalogue.bnf.fr/ark:/12148/cb41904894h). Image réutilisée : `docs/reports/map/MAP2L/RHINE_CENTRAL/VAUGONDY_SANTINI_DETAIL.jpg`, provenance et empreinte dans le JSON voisin `VAUGONDY_SANTINI_SOURCE.json`. Le territoire nommé Berg et ses voisins sont examinés, puis un intérieur conservateur est dessiné. La notice et la photographie ne sont pas présentées comme le même exemplaire physique. Aucun contour complet ou relevé cadastral n'est déduit de cette lecture.

## Souverainetés et chronologie

- [Hommage des états de la part prussienne de Gueldre, 14 septembre 1713](https://www.preussen-im-rheinland.de/geschichte/brandenburg-preussen-am-niederrhein-1718-jh/nebenlande-und-laboratorien-der-moderne-der-preussische-niederrhein-im-18-jahrhundert/lehnseid-der-geldrischen-staende-in-der-landessprache/), publication institutionnelle LVR d'une source primaire : confirme une part du Haut-Quartier et le souverain prussien, pas toute la Gueldre ni un contour RGB.
- [Archives municipales de Düsseldorf, succession Pfalz-Sulzbach](https://www.duesseldorf.de/stadtarchiv/stadtgeschichte/aufsaetze/berg-genealogie/aus-den-linien-pfalz-sulzbach-pfalz-zweibruecken-birkenfeld) : Charles-Théodore devient électeur palatin et duc de Jülich–Berg en 1742 ; succession bavaroise ultérieure, en 1777. Cela justifie KPF pour un noyau bergien de 1776 réellement établi, sans anticiper BAY ou PRU.
- [GStA PK, guide géographique du Nord et de l'Ouest](https://gsta.preussischer-kulturbesitz.de/recherche/geografischer-wegweiser/der-norden-und-westen.html) : orientation dans les fonds des possessions occidentales. Source d'identification des fonds, pas une géométrie de frontière.

## Piste non obtenue comme image

[LWL, Sotzmann/Jäck, KSA 11921](https://www.lwl.org/westfaelische-geschichte/portal/Internet/finde/langDatensatz.php?urlID=406&url_tabelle=tab_karte) : notice consultée par l'outil web, état représenté **1788**, édition **1790**. Le téléchargement direct a renvoyé une **page de maintenance**, conservée sous `SOTZMANN_CATALOGUE.html` ; ce fichier n'est pas une copie de la carte. L'image de cet exemplaire n'a pas été obtenue ni prétendue lue. La feuille de Berne de 1793 ci-dessus est une autre source réellement lue.

## Réemplois conservés

- `MAP2L/RHINE_WESTPHALIA_COMPLETION/REPORT.md` et `UNRESOLVED.csv` : noyaux installés, réserves sur Gueldre et Ravensberg, confusion ancienne du point Osnabrück/Tecklenburg.
- `MAP2L/MINDEN_RAVENSBERG/ALIGNMENT.json` : ancienne correspondance de Bielefeld et repères inégaux ; aucune répétition de ce calage.
- `MAP2M/R9/PRUSSIAN_HRE_BORDERS_AUDIT.md` : travaux partiels, ne certifiant pas l'ensemble occidental.
- `MAP2M/R5/TRANSFORMATIONS.json` et `MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json` : deux hypothèses natives héritées, domaines et incertitudes conservés. Pas de modification de leurs matrices ; aucune exactitude locale déduite de leurs statistiques anciennes.

L'écart entre les modèles et les 39 cellules hypothétiques de Berg sont des résultats de cette analyse technique, pas une donnée historique fournie par les sources.
