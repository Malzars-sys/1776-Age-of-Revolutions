# Sources et décisions R3-A1

**Statut final : candidat retiré, aucune correction R3 active.** La documentation ci-dessous explique sa préparation ; la correspondance avec le bitmap a été refusée lors de la confrontation finale des référentiels. Voir `REPORT.md` et `NATIVE_REFERENCE_CONTRADICTION.json`.

## Sources conservées et confrontation

Les rapports MAP2L/FRANCONIA et FRANCONIA_CONTINUATION, leurs géométries, anciennes planches Homann/Le Rouge et propriétaires effectifs ont été relus. Ils établissent les noyaux déjà travaillés, mais ne suffisent pas à délimiter les branches de Hohenlohe : aucune frontière interne nouvelle n’a été déduite de leur seule couleur globale.

## Hohenlohe : institution et chronologie

Source principale : Gerhard Taddey, « Hohenlohe », *Historischer Atlas von Baden-Württemberg*, VI,6, Erläuterungen, livraison 1985, [PDF LEO-BW](https://www.leo-bw.de/media/kgl_atlas/current/delivered/pdf/HABW_6_6.pdf), conservé dans `EVIDENCE/HABW_6_6.pdf`. Pages imprimées 5–7 : arbre dynastique, partages et notice de lecture. La carte principale se rapporte à 1806, donc n’est pas directement transférable à 1776.

Le tableau dynastique distingue Langenburg et Kirchberg sous Christian Albrecht et Christian Friedrich Karl, après les décès des titulaires précédents en 1765/1767. Ingelfingen demeure sous Heinrich August, pas sous son successeur de 1796. Les princes catholiques de la branche de Waldenburg ne justifient pas la conversion générale de leurs sujets. La ville d’Öhringen a encore des droits partagés avant 1782. Les acquisitions de 1797, 1799 et 1803 doivent être retranchées d’une lecture tardive. Ancienne lignée Waldenburg éteinte en 1679, Pfedelbach en 1728 ; ne pas fabriquer la jeune branche de 1807 en 1776.

Recoupement institutionnel : Landesarchiv Baden-Württemberg, [« Fürstenwürde auf Raten »](https://www.landesarchiv-bw.de/de/aktuelles/nachrichten/64437), 2019. Distingue titres personnels/territoriaux de la branche catholique et élévation de la branche Neuenstein ; ne confère pas un électorat.

Dates des deux souverains proposés : notices d’autorité de la [Deutsche Biographie, Christian Albrecht](https://www.deutsche-biographie.de/gnd104194847.html) et [Christian Friedrich Karl](https://www.deutsche-biographie.de/pnd102556490.html). Naissances 27 mars 1726 et 19 octobre 1729. Les dates ne servent pas à déduire des frontières.

## Source géométrique : usage borné

Franzpaul, [*States and districts as of 1800, Oberamt Gerabronn*](https://commons.wikimedia.org/wiki/File:HkDE-wt_Gerabronn_1800.svg), dessin vectoriel moderne, source topographique déclarée : *Topographischer Atlas des Königreichs Württemberg*, 1851. Échelle nominale 1:100 000, emprise de l’Oberamt de 1813. **Ce n’est ni une carte originale de 1776, ni une source souveraine suffisante isolément.**

Le SVG conserve des objets distincts : `HoLaLangenburg`, `HoKiKirchberg`, `HoBaWerdeck`, ainsi que les condominiums. Seul le plus grand corps continu des deux premiers est retenu, après confrontation institutionnelle. Les corps détachés sont différés ; Werdeck, autres acquisitions tardives, fragments de droits partagés et tous les autres pays de la planche sont exclus.

Trois symboles de ville de la source, pas leurs libellés décalés, enregistrent la feuille sur le modèle diagnostique hérité : Langenburg (561,6 ; 457,7), Bartenstein (564,1 ; 469,2), Kirchberg (571,6 ; 452,4). Gerabronn et Schrozberg servent de contrôles de feuille non ajustés. Les écarts 0,079/0,222 pixel mesurent uniquement la cohérence relative **source → modèle diagnostique** ; ils ne prouvent pas l’exactitude physique du modèle dans le jeu. Voir `SOURCE_ALIGNMENT.json`.

Les métadonnées et la licence du fichier original sont conservées dans `EVIDENCE/Gerabronn_SOURCE.html`. Choix de licence pour le SVG et les dérivés cartographiques de cette source : **CC BY-SA 3.0**, attribution **Franzpaul, Wikimedia Commons**, modifications : couleurs diagnostiques, enregistrement, sélection/rastérisation des noyaux, annotations. La notice d’origine propose aussi d’autres licences. `GERABRONN_SOURCE_REVIEW.png`, `SOURCE_ACCEPTED_REVIEW.png` et les cartes de résultat dérivées suivent cette attribution ; elle ne s’applique pas à tout le dépôt ou aux textures du jeu. Aucun droit nouveau sur le PDF institutionnel n’est revendiqué.

## Castell et Wertheim : inventoriés, non installés

[Deutsche Biographie, Castell](https://www.deutsche-biographie.de/sfz8048.html) distingue les lignées nouvelles de 1803 et le titre princier de 1901. Le [bulletin institutionnel Castell 53/2023](https://castell.de/media/56/da/d5/1703236788/Casteller_Nachrichten_53_2023_web_.pdf) documente tutelle et achats postérieurs à 1776. Une régence ne suffit pas à justifier plusieurs pays natifs ni des territoires acquis ultérieurement.

Landesarchiv Baden-Württemberg, [formation des deux lignées de Löwenstein-Wertheim](https://www.landesarchiv-bw.de/de/themen/praesentationen---themenzugaenge/71708) : Virneburg/Rochefort, appellations Freudenberg/Rosenberg de 1813 à exclure. [Historisches Lexikon Bayerns, comté de Wertheim](https://www.historisches-lexikon-bayerns.de/Lexikon/Wertheim%2C_Grafschaft) : ne pas importer les compensations de 1803. Titulaires de 1776, coseigneuries et géométrie exacte restent à finaliser avant des pays supplémentaires.

## Villes et petites juridictions

La planche franconienne conservée identifie plusieurs villes impériales, mais leurs positions diagnostiques tombent aujourd’hui dans des RGB de régions plus larges. Cela ne justifie pas le transfert du RGB entier. Rothenburg, Schweinfurt, Windsheim et Weißenburg n’ont pas de pays distinct trouvé dans les définitions effectives du mod lors de ce contrôle. Nuremberg est déjà traité. Voir également [HLB, évolution du territoire bavarois](https://www.historisches-lexikon-bayerns.de/Lexikon/Staatsgebiet_%2819./20._Jahrhundert%29) pour les acquisitions tardives, non appliquées.

Limpurg, Schwarzenberg, Comburg et autres droits fragmentés restent C quant à leur traduction territoriale précise. Un nom d’abbaye, un chapitre ou une famille ne constitue pas à lui seul une preuve d’État souverain. L’inventaire est ciblé sur la mission, pas une nouvelle certification exhaustive de toute la Franconie.
