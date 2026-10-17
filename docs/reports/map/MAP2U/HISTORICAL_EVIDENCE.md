# Preuves et méthode MAP-2U

## Souverainetés avant 1776

[Landeszentrale für politische Bildung Thüringen, résidences des Reuss](https://www.politische-bildung-thueringen.de/informieren/dossiers/dossier/2/residenzen-der-reussen/), auteur Marco Kreutzmann: branches distinctes de Lobenstein et Ebersdorf issues du partage1678; dignités princières seulement 1790 et 1806. Les deux résidences sont antérieures à 1776. Cela établit l’identité des deux comtés, pas une frontière pixel par pixel.

[Archives de Thuringe, gouvernement de Sondershausen, fonds 5-14-1130](https://www.archive-in-thueringen.de/de/bestand/view/id/25954): depuis 1716, Unterherrschaft et Oberherrschaft relèvent du même État tout en conservant des gouvernements distincts. Les réorganisations de 1842–1847 ne sont pas appliquées au départ.

## Séparation territoriale et cartes comparatives

Les cartes IEG-MAPS650,653 et 673, Andreas Kunz / Joachim Robert Moeschl,2006, représentent1820 et sont conservées avec empreintes dans SOURCE_FILES.json. Liens: [Ebersdorf](https://www.ieg-maps.uni-mainz.de/mapsp/mapvSK820Th_RjL_Eb_Vw.htm), [Lobenstein](https://www.ieg-maps.uni-mainz.de/mapsp/mapvSK820Th_RjL_Lo_Vw.htm), [Sondershausen](https://www.ieg-maps.uni-mainz.de/mapsp/mapvSK820Th_SS_Vw.htm). Les traces bleues sont conservées dans les images TRACING_REVIEW et leurs sommets exacts dans GEOMETRY.json.

La reconstruction1789 de Putzger et son ALIGNMENT.json restent disponibles dans MAP2T. Les contours Reuss y sont regroupés à une échelle qui ne sépare pas correctement Ebersdorf: ils ne suffisent pas à attribuer chaque enclave. Les feuilles IEG apportent cette distinction, sous contrôle de la chronologie; les contours intérieurs demeurent B, pas des levés1776.

[IEG, notice Reuss-Ebersdorf](https://www.hgisg-ekompendium.ieg-mainz.de/Dokumentation_Datensaetze/Multimedia/Staaten/Reuss-Ebersdorf.php): le partage consécutif à l’extinction de Hirschberg en 1711 donne à Ebersdorf les environs de cette résidence. L’union de 1824 est écartée. Les zones hachurées de Gera/Saalburg, condominium seulement après 1802, sont exclues des nouveaux tracés. Les possessions devenues prussiennes en 1815 ne sont pas importées comme telles dans les comtés. Les éventuelles petites rectifications entre1776 et 1820 ne sont pas toutes résolues: seuls des noyaux sont retenus.

## Souverains

Lobenstein: Heinrich II,1702–1782, né le 19 juillet 1702. Le catalogue historique de la société des sciences naturelles de Gera relève sa prédication funèbre de 1782, entrée 2173, sous le titre comtal: [bibliographie conservée par ZOBODAT](https://www.zobodat.at/pdf/Jber-Ges-Freunden-Naturwiss-Gera_39-42_0147-0228.pdf), repérage par le numéro de l’entrée. Heinrich XXXV ne lui succède qu’en 1782; il n’est pas installé en 1776.

Ebersdorf: Heinrich XXIV,1724–1779, identité comtale [Deutsche Biographie, GND143309773](https://www.deutsche-biographie.de/gnd143309773.html). Date de naissance22 janvier 1724 corroborée par [LAGIS, registre familial](https://www.lagis-hessen.de/de/subjects/rsrec/current/1/entry/heinrich%2Bx.%252C%2Breuss-ebersdorf%252C%2Bgraf/sn/bio/register/person). Aucun successeur1779 ni titre princier1806 anticipé. SSO conserve le souverain contemporain déjà vérifié et installé par MAP2T.

## Démographie et limites documentaires

[Archives, Landesdirektion Ebersdorf, rubrique démographique](https://www.archive-in-thueringen.de/de/findbuch/view/bestand/21761/systematik/83870): dossier 0992, fonds 3-12-2500, annonce des comparaisons 1714/1784 dans un dossier 1811; dossier 0990 signale aussi des données Lobenstein1794. Les notices ne donnent pas les tableaux eux-mêmes: aucune population1776 n’en est inventée. La notice IEG donne des ordres de grandeur postérieurs qui ne correspondent ni à la date ni aux noyaux installés; ils ne deviennent pas une estimation1776.

L’accès à la rubrique de frontières83834 fournie dans le prompt n’a pas livré de contenu exploitable. Aucune de ses limites n’est prétendue lue ou appliquée. Le document institutionnel accessible de Sondershausen et les cartes comparatives sont distingués de cette lacune.

## Précision et traçabilité

SOURCE_ALIGNMENT.json aligne les nouvelles feuilles sur le profil diagnostique conservé. Les faibles résidus des points d’ajustement ne sont pas des erreurs géographiques indépendantes. Ni refonte régionale de projection, ni translation 7,20 pixels, ni rivières assimilées à des centres urbains certifiés. Les villes modernes sont des repères explicites du guide; les limites politiques proviennent des polygones, et non de la seule position d’une ville.

Les zones A concernent les identités et filiations politiques établies. Les cellules effectivement transférées sont B. Les secteurs C sont conservés sans transfert, avec les réserves d’UNRESOLVED.csv. La quantification d’Ebersdorf à une cellule reste visible comme approximation.
