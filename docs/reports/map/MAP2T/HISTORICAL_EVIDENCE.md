# Preuves utilisées et portée

## Sources conservées et réutilisées

R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv, lignes50–54: cinq propriétaires déjà signalés sans frontière microterritoriale démontrée. MAP2Q/R3/HRE_REGIONS_INVENTORY_UPDATED.csv et MAP2S/NEXT_HRE_REGION_RECOMMENDATION.md: secteur encore non reconstruit. Ces pistes ne sont pas transformées en preuves cartographiques.

## Cartographie comparative, pas preuve directe1776

[Putzger, États thuringiens1789, atlas publié1905](https://commons.wikimedia.org/wiki/File:Th%C3%BCringische_Staaten_1789_%E2%80%93_F._W._Putzgers_Historischer_Schul-Atlas_1905_(135770778).jpg). Fichier conservé dans EVIDENCE/PUTZGER_1789_1905.jpg; empreinte et dimensions dans SOURCE_FILE.json. Les remplissages historiques et indications des branches guident les noyaux. Les limites rouges des États et provinces contemporains de l’atlas ne sont pas utilisées comme frontières1776. Les polygones intérieurs sont conservés dans GEOMETRY.json et visibles sur SOURCE_TRACING_REVIEW.png.

## Souverainetés et dates

- [Landesarchiv, engagements des agents d’Altenbourg envers Ernst II en1772–1773](https://www.archive-in-thueringen.de/de/findbuch/view/bestand/21702/systematik/276244): Gotha–Altenbourg relève bien du même duché avant1776. [Biographie académique d’Ernst II](https://www.deutsche-biographie.de/sfz52922.html): règne1772–1804. Pas de création Cobourg–Gotha de1826.
- [Landesarchiv, Geheimes Archiv Hildburghausen](https://www.archive-in-thueringen.de/de/bestand/view/id/23365/bestand/23370): pleine souveraineté en1702, offices d’origine et acquisitions distingués. [Notice d’Ernst Friedrich III](https://www.deutsche-digitale-bibliothek.de/person/gnd/118954776): souverain contemporain. Ne pas importer son remplacement par Altenbourg en1826.
- [Landesarchiv, Amtsarchiv Heldburg](https://www.archive-in-thueringen.de/de/bestand/view/id/23369): filiation Hildburghausen jusqu’au réaménagement1826. [Themar/Römhild](https://www.archive-in-thueringen.de/en/bestand/view/id/23367/bestand/23377): juridictions partagées; elles ne sont pas attribuées unilatéralement dans les noyaux.
- [Inventaire institutionnel du Staatsarchiv Rudolstadt](https://landesarchiv.thueringen.de/media/landesarchiv/5Standorte/Rudolstadt/Veroeffentlichungen/Bestaendeuebersicht_2019_12_09.pdf): Rudolstadt et Sondershausen séparés, Oberherrschaft et Unterherrschaft distinguées. [Heidecksburg, souverains](https://www.heidecksburg.de/historie/regenten/): Ludwig Günther II règne1767–1790. [Stiftung Thüringer Schlösser, Sondershausen](https://www.thueringerschloesser.de/objekt/schloss-sondershausen-mit-park/): Christian Günther III règne1758–1794.
- [Ville de Greiz, chronologie](https://www.greiz.de/tourismus-kultur/tourismus/chronik): union des deux Greiz en1768, dignité princière seulement1778. [Deutsche Biographie, famille Reuss](https://www.deutsche-biographie.de/gnd118744674.html): pas d’unification de la jeune ligne avant1848. RGZ est donc un comté en1776, pas une principauté créée rétroactivement.
- [Heinrich XXX, Reuss-Gera, GND104254211](https://www.deutsche-biographie.de/gnd104254211.html): identité et dates1727–1802; pas d’annexion successorale de Gera en1802 appliquée au départ.
- [Heinrich XII, Reuss-Schleiz, GND104254254](https://www.deutsche-biographie.de/gnd104254254.html):1716–1784. Le souverain retenu n’est pas Heinrich XLII, qui lui succède en1784. Les archives de la [Landesdirektion Ebersdorf](https://www.archive-in-thueringen.de/en/findbuch/view/phrase/Me%C3%9F/exactphrase/1/limit/10/submit/Suche%2Bstarten/page/3/bestand/21761/systematik/83873) distinguent les maisons de Gera, Schleiz, Lobenstein et Ebersdorf et documentent les affaires des années1774–1779.

Ces sources institutionnelles établissent des souverainetés ou une chronologie. Elles ne valident pas séparément chacun des121 pixels transférés. La lecture du fond rétrospectif, sa correspondance au bitmap et la protection d’Erfurt restent des généralisations B explicites.

## Précision et arbitrage

Le profil MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json est conservé sans modification. La feuille nouvelle est ajustée au diagnostic déjà disponible, sans prétendre corriger la projection native. Les écarts de l’ajustement de la feuille ne sont pas des erreurs indépendantes de position des villes. Aucun hub agricole nommé Erfurt, aucune distance à une rivière et aucune translation7,20px ne justifie un transfert.

Les contours conservés sont limités à STATE_SAXONY. Pas de correction du nord prussien de la Saxe en1815, pas d’extension vers Anhalt, pas de nouvelle interprétation du chantier Erfurt. Lobenstein/Ebersdorf restent C: créer deux pays sur une séparation non identifiée serait arbitraire malgré leur existence politique établie. Les franges sont explicitement répertoriées comme incomplètes.

## Population

Aucune valeur de population historique datée au périmètre exact de ces noyaux tronqués n’a été identifiée dans les recherches retenues ou les notices consultées. La redistribution des historiques existants par parts techniques est déterministe, conserve chaque profil écrit et n’est pas présentée comme un recensement. Les surfaces ne produisent aucune nouvelle estimation démographique. Un chiffre territorial total d’une date postérieure ne serait pas applicable automatiquement à un noyau incomplet.

La tentative d’accès au PDF egierendef_rsten.pdf a renvoyé404. Il n’a pas servi à certifier les souverains; les notices accessibles ci-dessus sont utilisées.
