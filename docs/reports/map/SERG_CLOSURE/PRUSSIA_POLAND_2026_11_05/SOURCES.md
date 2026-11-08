# Frontière polono-prussienne — décision du 5 novembre 2026

Référence du scénario : **1er janvier 1776**. Livraison de **catégorie B**, sans certificat cadastral ou validation humaine nouvelle.

## Recherches réutilisées et limites respectées

Les dossiers MAP2M/R2–R9, leurs scans, propositions, résultats bruts et reçus sont conservés. Ils établissent les acquis de Bromberg, les anomalies de Thorn/Inowrocław et la contradiction du liseré méridional de 1775 avec l'incorporation de Szubin. Aucun ancien ajustement Pfau, manuscrit N1146/1 ou profil natif n'est relancé. Le liseré contesté n'est pas installé comme une frontière de janvier 1776.

Les propositions urbaines U1/U2 de R9 restent des propositions archivées non approuvées. La présente mission prend une **nouvelle décision d'implémentation B**, documentée et à tester ; elle n'invente pas une approbation du joueur pour ces variantes ou pour le nouveau noyau.

## Sources réellement consultées

1. **Güssefeld/Homann, 1775**, image institutionnelle déjà conservée, `docs/reports/map/MAP2M/EVIDENCE/GUESSEFELD_1775.jpg`, 4000 × 3079. [Image de Berne](https://www.e-rara.ch/i3f/v20/29730664/full/4000,/0/default.jpg). Lecture nouvelle de la frontière Culmland–Dobrzyń, du territoire réservé de Thorn et des villes voisines. La ligne souveraine orientale est distinguée de la ligne méridionale contestée de la Netze.
2. **Güssefeld, Borussiae occidentalis tabula, editio emendatior, 1780**, Berne, MUE Ryh 6103, [notice](https://ryhiner.ub.unibe.ch/en/world/location/53/image/14314), [DOI](https://doi.org/10.3931/e-rara-127551). L'image `EVIDENCE/GUESSEFELD_1780.jpg`, 4000 × 4203, et son encart agrandi ont été examinés. **Cette édition est postérieure à 1776**. Son encart sert à dessiner un noyau contrôlé par les chronologies ci-dessous, pas à certifier toute la frontière à la date cible. Les éditions 1775/1780 d'une même famille ne sont pas deux témoins indépendants.
3. **Pfau, feuille 45**, scan conservé dans MAP2M/R4 et extrait MAP2M/R8 : noyau fortifié de Thoren et configuration riveraine. Les levés 1772–1773 et l'édition cataloguée [1778] ne sont pas confondus. Le document topographique confirme le côté de la rivière, pas toute la juridiction rurale de 1776.
4. [Geheimes Staatsarchiv, chronologie territoriale](https://gsta.preussischer-kulturbesitz.de/recherche/geografischer-wegweiser) : acquisitions de 1772 distinctes des annexions de Dantzig et Thorn en 1793 ; la propriété prussienne de la Netze ne signifie pas appartenance impériale.
5. [Ville d'Inowrocław](https://www.inowroclaw.pl/strona-4640-historia.html) : domination prussienne à partir de janvier 1773. [Ville de Szubin](https://szubin.pl/historia-gminy.html) : incorporation prussienne en 1773.
6. [Gmina Żnin](https://gminaznin.pl/cms/16411) : prise par la Prusse en **mars 1774**, dans le contexte d'une interprétation de la frontière du premier partage. [Chronologie de Mogilno](https://www.mogilno.pl/asp//kalendarium-wydarzen%2C214) : prise prussienne en **mars 1774**, au-delà de la délimitation initiale. Il s'agit du **contrôle effectif**, sans inventer une date de reconnaissance juridique de chaque limite. Une autre synthèse municipale donne l'année générale 1772 ; cela ne modifie pas la conclusion minimale d'un contrôle antérieur à 1776, mais la divergence de date n'est pas effacée.
7. [Ville de Trzemeszno](https://trzemeszno.pl/okres-zaborow-i-niespokojne-miasto-powstancow.html) : tentative prussienne de 1774 repoussée, prise après le deuxième partage en janvier 1793. **Trzemeszno reste polonaise** ; Mogilno et Trzemeszno ne sont pas assimilées.
8. [Ville de Rypin](https://rypin.eu/strona-49-historia.html) : annexion prussienne en 1793. Cette chronologie et la carte contemporaine motivent la restitution de la frange méridionale du parent partagé, en préservant Brodnica/Górzno.

Les pages acquises figurent dans `EVIDENCE/`, avec leurs URL et empreintes. Les notices de cartes datées [1793] et [1789–1806], consultées comme pistes, ne sont pas utilisées pour une annexion de 1776. Aucun plan d'archives non obtenu n'est déclaré examiné.

## Décisions géographiques

**PP-NETZE-CORE — 222 cellules PLC → PRU.** L'encart révisé montre le prolongement autour de Żnin, Mogilno et Inowrocław. Six lectures de villes servent à transformer la nouvelle feuille vers le profil natif R5 **figé**, deux autres servent de contrôles séparés. Résidus d'ajustement : 0,43–2,01 cellules ; contrôles Łabiszyn/Pakość : 1,88 et 1,45. Ce ne sont ni une erreur de frontière certifiée, ni un intervalle de confiance. Le sommet nord de l'enveloppe est une **fermeture technique**, pas une frontière souveraine. Seuls deux parents PLC sont concernés ; le noyau nord est limité à la ligne native Y ≤ 780. Le reste du contour méridional de 1780 n'est pas rétroprojeté. Les 85 cellules PRU déjà reçues sont strictement préservées.

**PP-THORN-CORE — 4 cellules PRU → PLC.** Une généralisation urbaine de 2 × 2 cellules est retenue sur la rive nord de la Vistule, au voisinage du diagnostic géographique R5. Les boucles réservant Thorn sur les cartes politiques, le noyau fortifié de Pfau et l'hydrographie native justifient cette représentation B. **Ce n'est pas tout le territoire municipal ou rural historique.** Les 149 autres cellules du parent restent prussiennes faute de délimitation suffisante. Le repère agricole nommé Toruń est déplacé de cinq cellules environ sur ce noyau ; son ancien point est au sud de la rivière native, le nouveau au nord. L'instance 158 seule change de position, sans changement de rotation, d'échelle ou d'autres repères. `LOCATOR_RELOCATION.json` conserve les positions exactes. Le nouveau terrain est `plains`, sans recopier l'anomalie `tundra` du parent rural, qui reste hors correction.

**PP-DOBRZYN-FRINGE — 59 cellules PRU → PLC.** Le tracé de 1775 est lu séparément, avec quatre repères et Golub comme contrôle. Résidus d'ajustement : 0,32–1,93 cellule ; diagnostic Golub : 1,72. Une cellule adjacente de bordure représente explicitement Rypin du côté polonais, compte tenu de la généralisation et de sa souveraineté connue ; cette décision B est conservée dans `DOBRZYN_TRACING.json`. Le parent PRU conserve 162 cellules. Ses deux fragments RGB restent reliés à la Prusse par les provinces voisines ; ce ne sont pas deux enclaves prussiennes artificielles. Brodnica, Górzno et le repère forestier restent prussiens et inchangés.

Les vingt-deux diagnostics grossiers de localités contrôlent la cohérence générale. Ils ne sont pas des locators natifs homologués indépendamment. Les villes Inowrocław, Żnin, Mogilno et Rypin ne reçoivent pas de nouveau hub nommé.

## Limites et comptabilité

Les 285 cellules modifiées corrigent des noyaux et une frange importante. **Les quatre districts de la Netze et toutes les possessions rurales de Thorn ne sont pas déclarés historiquement achevés.** Les limites demeurent B ; les micro-juridictions et les rectifications non datées ne sont pas inventées.

Dantzig, Poznań, Gniezno, Trzemeszno, Lipno et Płock restent polonaises ; les noyaux de Prusse occidentale et de Warmie contrôlés restent prussiens. Aucun nouveau pays, aucune région économique déplacée. Les populations sont une redistribution technique des profils actuels, sans recensement urbain fictif ; bâtiments, PM et unités sont conservés.

Ces corrections sont **extérieures au Saint-Empire**. Les 592 titres impériaux et leur étendue restent identiques. L'ajout d'un manifeste géométrique à la chaîne technique ne constitue ni appartenance impériale, ni réception humaine. Les 81 tâches, les 235 points et leurs attestations ne sont pas modifiés.
