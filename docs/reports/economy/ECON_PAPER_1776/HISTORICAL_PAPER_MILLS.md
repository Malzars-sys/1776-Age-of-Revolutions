# Implantations historiques des papeteries

Sources consultées le 17 octobre 2026. Les faits ci-dessous justifient les lieux et leur antériorité à 1776 ; les niveaux sont ceux demandés pour le gameplay.

## Franzensthal

Le [Musée de Basse-Autriche, base Gedächtnis des Landes](https://www.gedaechtnisdeslandes.at/orte/ort/ebergassing/) indique que Johann Thomas von Trattner acquiert en 1767 un moulin sur la Fischa et le transforme en papeterie. Il distingue cet établissement, ultérieurement nommé Franzensthal I, d’une seconde implantation acquise en 1784. Seule la première justifie l’implantation de départ. L’acquisition ultérieure du château ou de la seigneurie n’est pas assimilée à la fondation de la papeterie.

Représentation : `STATE_AUSTRIA`, identifiant 51, subdivision AUS. Le moteur agrège les installations de la région et ne place pas le bâtiment dans la commune exacte. Quatre niveaux ne signifient pas quatre moulins historiques.

## Wolfswinkel

L’[office de tourisme d’Eberswalde](https://tourismus-eberswalde.de/entdecken-und-erleben/kunst-kultur-geschichte/baukultur/papierfabrik-wolfswinkel/) donne 1765 pour le début de la production à Wolfswinkel. Il distingue cette activité de l’introduction d’une machine à papier en 1834. Le [catalogue historique Brandenburgikon](https://www.brandenburgikon.net/index.php/de/unternehmen-bis-1945/eberswalde-finow/wolfswinkel) confirme 1765 et décrit les obligations de fourniture à la chambre administrative de Berlin.

Représentation : `STATE_BRANDENBURG`, identifiant 65, subdivision PRU, trois niveaux. L’implantation représente Wolfswinkel ; elle ne représente ni une mécanisation du XIXe siècle ni un établissement ultérieur de Spechthausen.

## Niederzwönitz

Le [musée municipal de Zwönitz](https://www.zwoenitz.de/stadtleben/kultur-freizeit/museen/technisches-museum-papiermuehle-niederzwoenitz) situe la première mention documentaire en 1568. Le [site du patrimoine minier de l’Erzgebirge](https://www.montanregion-erzgebirge.de/welterbe/marienberg/assoziiertes-element/papiermuehle-niederzwoenitz.html) relie la production de papier aux besoins de l’administration minière.

Représentation : `STATE_SAXONY`, identifiant 73, subdivision SAX, deux niveaux. Les nouvelles principautés issues des corrections cartographiques restent distinctes et ne reçoivent pas ces niveaux. La mission ne change ni le pays saxon ni son statut politique.

## Reinerz

L’[office de tourisme de Duszniki](https://visitduszniki.pl/mlyn-papierniczy/) décrit la transaction de parts de 1562, la reconstruction du début du XVIIe siècle et le statut de papetiers royaux acquis en 1750. Il précise l’emploi de chiffons de lin. Le [musée de la papeterie](https://muzeumpapiernictwa.pl/jp/dusznicka.html) confirme l’antériorité à 1562 et l’activité du XVIIIe siècle. Ces sources attestent donc un établissement bien antérieur au départ du scénario.

Représentation : `STATE_LOWER_SILESIA`, identifiant 155, subdivision PRU, un niveau. Les historiques territoriaux actuels et le repérage géographique local attribuent cette position à la Prusse. La papeterie n’est pas placée dans la subdivision autrichienne.

## Limite commune du procédé représenté

Le type natif est `building_paper_mill`. La méthode disponible `pm_pulp_pressing` consomme du bois dans les règles du jeu ; cette recette abstraite ne prouve pas une fabrication historique de pâte de bois dans ces établissements au XVIIIe siècle. Le papier de chiffons attesté par les sources ne justifie pas le déblocage de procédés modernes. Aucun nouveau bâtiment ni aucune nouvelle technologie n’est introduit.
