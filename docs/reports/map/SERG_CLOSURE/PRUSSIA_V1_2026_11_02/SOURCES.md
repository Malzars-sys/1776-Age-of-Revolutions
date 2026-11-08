# Prusse V1 — sources et portée

Recherche commencée le 2 novembre, finalisation le 5 novembre 2026. Situation visée : 1er janvier 1776. Mission utilisateur : privilégier les frontières visibles de la Prusse ; suspendre les micro-États, réserver la Bavière à une décision ultérieure. Aucun changement du périmètre comptable SERG 1.0.0.

## Sources primaires effectivement lues

- **Lotter, Haute-Lusace**, Universitätsbibliothek Bern, **MUE Ryh 4410 : 15**, catalogue **[après 1758]**, exemplaire sans année exacte certifiée. [Notice et reproduction](https://www.e-rara.ch/bes_1/content/titleinfo/29505820), [identifiant pérenne](https://doi.org/10.3931/e-rara-122008). Image IIIF 3000 × 2864, effectivement examinée : `EVIDENCE/UPPER_1758.jpg`. Le nom de fichier est un repère de collecte ; il ne signifie pas une publication datée exactement de 1758. Görlitz, Lauban, Hoyerswerda, Muskau, les ressorts et le raccord avec la Silésie sont lisibles.
- **Lotter, Basse-Lusace**, même institution, **MUE Ryh 4410 : 17**, catalogue **[après 1758]**. [Notice et reproduction](https://www.e-rara.ch/bes_1/content/titleinfo/29505745), [identifiant pérenne](https://doi.org/10.3931/e-rara-121983). Image IIIF 3000 × 2800, effectivement examinée : `EVIDENCE/LOWER.jpg`. Luckau, Lübben, Calau, Guben, Forst, Sorau, Spremberg et le ressort brandebourgeois de Cottbus/Peitz sont distingués.

Les notices correctes et leurs textes sont conservés dans `EVIDENCE/*_TITLE_CATALOG.*`. Les premiers appels sur les identifiants des images, au lieu des notices, ont rendu des pages sans titre : `*_CATALOG.html` ne sert pas à établir la datation. Les deux premières tentatives de manifeste individuel ont donné HTTP 404 ; le manifeste public du recueil a ensuite fourni les services d'images. Aucun accès protégé contourné.

**Lecture déterminante : les couleurs distinguent des districts, pas uniformément des souverains.** Les espaces non coloriés de la seigneurie de Muskau et de l'abbaye de Neuzelle/Pforten ne deviennent pas prussiens. Leurs raccords ont été lus séparément ; voir `UPPER_EAST.jpg`, `NEUZELLE_PFORTEN_BOUNDARY_READING.jpg`, les tracés et leurs polygones. Le ressort rose de Cottbus/Peitz reste prussien ; `COTTBUS_BOUNDARY_READING.jpg` documente son contour. Le blanc à l'est relevant de la Silésie/Neumark n'est pas annexé à la Saxe par une simple absence de couleur.

## Contrôles historiques indépendants

- [Institut sorabe, contexte archivistique des Lusaces](https://www1.sorabicon.de/quellen-zur-sorbischen-geschichte-1918-1945/hauptstaatsarchiv-dresden/) : souveraineté saxonne issue de 1635, changement majeur en 1815. Appuie la chronologie générale, sans certifier les pixels.
- [Brandenburgisches Landeshauptarchiv, Stadtarchiv Cottbus](https://blha.brandenburg.de/blha/de/suchen-finden/archive-in-brandenburg/stadtarchiv-cottbus/) : Cottbus brandebourgeois/prussien, épisode saxon napoléonien ultérieur. La chronologie de l'acquisition ancienne diffère d'autres notices (1445/1455) ; cette divergence n'affecte pas l'attribution de 1776 et n'est pas arbitrée ici.
- [Deutsche Stiftung Denkmalschutz, Neuzelle](https://www.denkmalschutz.de/denkmal/zisterzienserkloster.html) : appartenance à la Saxe à partir de 1635, passage à la Prusse en 1815. Les droits fonciers monastiques et la protection religieuse ne sont pas assimilés à un pays souverain nouveau.
- [Geheimes Staatsarchiv, chronologie prussienne](https://gsta.preussischer-kulturbesitz.de/nutzung/arbeitshilfen/zeitleiste.html) : Frise orientale acquise en 1744 ; acquisitions polonaises de 1772 distinctes de Dantzig/Thorn en 1793 ; Mansfeld 1780 et Ansbach/Bayreuth 1791 restent postérieurs au départ. Cette source soutient le tri chronologique, sans délimitation par cellule.
- [Sächsisches Staatsarchiv, changements de 1815](https://www.archiv.sachsen.de/orts-und-heimatgeschichte-8293.html) : les autres cessions saxonnes septentrionales doivent encore être traitées. Elles ne sont pas toutes réparées par le sous-lot lusacien.

## Réutilisation des travaux du dépôt

- `MAP2M/R9/PRUSSIAN_HRE_BORDERS_AUDIT.md`, `PRUSSIA_POLAND_AUDIT.md`, `THORN_CORRECTION.md` : inventaire et anomalies distinctes ; Emden/Minden sont depuis reçus, ce que leurs anciens rapports ne pouvaient pas encore constater.
- `MAP2T/HISTORICAL_EVIDENCE.md` et `UNRESOLVED.csv` : les corrections saxonnes précédentes excluaient explicitement les cessions de 1815 hors de leur lot.
- `MAP1B/.../SILESIA_READING.md` : ses mauvais contrôles n'ont pas servi au tracé. Les corrections MAP2A et les portions autrichiennes sont protégées.
- Le profil natif `MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json` reste **empirique**, inchangé. Seules les deux nouvelles feuilles sont rapprochées de ce profil ; aucun ancien recalage ni translation rejetée n'est relancé.

## Limites et méthode

`TRACING.json` conserve lectures, contrôles, matrices et polygones. Les résidus de lecture sont d'environ 0,19–0,39 pixel pour l'ajustement de la Haute-Lusace, jusqu'à 1,39 pour celui de Basse-Lusace ; contrôles réservés jusqu'à 1,79 pixel. Ils ne mesurent pas une précision géographique indépendante de la carte du jeu. Les quatorze diagnostics de villes ne sont pas des centres urbains homologués.

Le transfert de `x614121` entier, 260 cellules, représente l'ensemble saxon Hoyerswerda–Spremberg–Muskau et son raccord occidental meissénien. Conserver les lacunes de couleur de la première lecture créait cinq îlots prussiens artificiels, dont Muskau ; cette proposition a été écartée. Le ressort prussien de Cottbus/Peitz se trouve dans l'autre parent `xDF4020`, protégé séparément. Les autres parents conservent leurs résidus prussiens plutôt que de transférer des provinces entières contenant aussi Sagan, la Silésie ou le Brandebourg.

La livraison reste une **généralisation politique B**. Elle corrige des attributions importantes antérieures à 1815, sans certifier toutes les limites du royaume de Prusse au pixel. Le nord de l'électorat de Saxe, Magdebourg/Halberstadt, des franges silésiennes, Netze/Thorn/Inowrocław et les limites occidentales restent explicitement ouverts. Aucun contour contemporain de l'Allemagne, de la Pologne ou de la Saxe n'est projeté sur 1776.

La population déplacée provient exclusivement des profils déjà présents, répartis par un calcul entier déterministe. Aucun nouveau recensement historique n'a été trouvé au périmètre exact ; aucune ventilation technique n'est présentée comme une mesure de 1776. La politique démographique SERG autorise des corrections historiques sourcées, mais n'en impose pas l'invention dans cette passe.
