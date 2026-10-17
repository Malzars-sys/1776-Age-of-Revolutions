# MAP-2Q-R3 — Preuves utilisées et limites

Situation cible : 1er janvier 1776. Les sources ne constituent pas un cadastre de cette date.

## S1 — Autorité et institutions

[Niedersächsisches Landesarchiv, Best. 30](https://www.arcinsys.niedersachsen.de/arcinsys/showFondsDetails.action?fondsId=2633&request_locale=en) distingue les deux Ämter de l'évêque, les possessions du chapitre cathédral, le chapitre collégial et les domaines privés gottorpois. Cette distinction interdit d'assimiler la totalité du territoire séculier postérieur à 1803 au domaine administratif de HLB en 1776.

## S2 — Schwartau et Kaltenhof avant 1776

La [ville de Bad Schwartau, Kaltenhof](https://www.bad-schwartau.de/Stadt-Menschen/Unsere-Stadt/Stadtteile/Kaltenhof/) retrace le domaine épiscopal médiéval, la constitution de l'Amt en 1623 et son transfert administratif à Schwartau dans les années 1640. La [notice municipale Schwartau](https://www.bad-schwartau.de/Stadt-Menschen/Unsere-Stadt/Stadtteile/Schwartau/) confirme ce siège administratif et le privilège de marché de 1742. La [notice Rensefeld](https://www.bad-schwartau.de/Stadt-Menschen/Unsere-Stadt/Stadtteile/Rensefeld/) renseigne le site et la paroisse, pas les limites souveraines de tout le Kirchspiel.

## S3 — Titres fonciers et distinction des juridictions

[LAS, Abt. 260, inventaire ciblé](https://arcinsys.schleswig-holstein.de/arcinsys/list.action?nodeid=g17863&page=1) : dossiers 3694–3696/3702 sur Rensefeld, 3653 sur Offendorf, 3656 sur Ovendorf (1712–1713), 3700/3704 sur Ratekau, 3632–3637 sur Neuhof et 3743/3756 sur Ruppersdorf. Les dates couvrent des titres antérieurs à 1776. La notice 3611 distingue explicitement Hobbersdorf, passé au chapitre : aucune incorporation automatique.

Ces notices d'inventaire ont été lues via le service web. Le téléchargement direct LAS a échoué sur un certificat TLS ; aucun contournement du certificat n'a été tenté. Les pièces originales et leurs plans ne sont pas déclarés consultés. Un titre foncier seul ne prouve pas toutes les limites de souveraineté ; il est rapproché des notices institutionnelles et de la description administrative S4.

Le [dossier 13250](https://arcinsys.schleswig-holstein.de/arcinsys/showArchivalDescriptionDetails?archivalDescriptionId=539263), daté 1778–1844, relie les prestations d'Ovendorf, Ratekau, Offendorf et Sereetz à la caisse de Schwartau. Il corrobore une organisation proche de la date cible, sans être présenté comme un document de 1776.

## S4 — Description géographique et anachronismes contrôlés

Ludwig Kohli, *Handbuch…*, volume II/2, 1826, [BSB bsb10020025](https://www.digitale-sammlungen.de/en/view/bsb10020025?page=161), pages imprimées 139–143 / vues 161–165, distingue l'Amt Kaltenhof de la Großvogtei. Les textes lus sont archivés dans `EVIDENCE/KOHLI_161.txt` à `KOHLI_165.txt`, avec manifeste et notices de provenance.

Cette source situe Rensefeld à l'ouest de Schwartau, Kaltenhof à l'est près du confluent, puis décrit Sereetz, Ratekau, Offendorf et Ovendorf. Elle signale des droits danois particuliers aux bâtiments ecclésiastiques de Ratekau : toute la paroisse ne devient pas épiscopale. Elle indique Wilmsdorf comme ancien domaine relevant de Lübeck.

Les textes AGGSH déjà conservés dans R2 datent le gain de Wilmsdorf de **1804** et distinguent les simples droits seigneuriaux des villages conservant une souveraineté holsteinoise. Wilmsdorf et ces villages ne sont pas transférés dans R3. La liste AGGSH de 1819 et celle de Kohli ne concordent pas entièrement, notamment pour Ratekau ; cette divergence n'est pas effacée.

## S5 — Carte de travail, pas une carte souveraine de 1776

[LAS Abt. 402 A 36 Nr. 183, carte diffusée par AGGSH comme vers 1819](https://aggsh.net/images/karte_fuerstentum_luebeck.jpg), copie conservée dans `EVIDENCE/LAS_402_A36_183_1819.jpg`. La carte et sa légende ont été inspectées intégralement puis en détail. Elle inclut les territoires du chapitre après 1803 et plusieurs catégories de domaines privés : **son aplat rouge n'a pas été intégralement importé**.

Trois petites enveloppes intérieures sont documentées dans `TRACING.json`, autour de localités relevant directement de l'Amt, en excluant les grandes zones capitulaires de Parin/Cleve/Hobbersdorf et l'acquisition de Wilmsdorf. Il s'agit d'une **approximation B interprétative**, non d'un relevé des limites de chaque village. Leur rasterisation au centre des cellules retient quatre cellules ; Ruppersdorf et Neuhof ne reçoivent pas de cellule supplémentaire forcée.

Le calage réutilise le diagnostic géographique et le repère technique Kiel de Q, avec cinq symboles de la carte. Les résidus de l'ajustement sont consignés, mais **aucune borne d'exactitude géographique native indépendante n'est certifiée**. Les empreintes vertes sur `SOURCE_SELECTION.png` montrent aussi les dépassements dus à la cellule entière. Aucune translation manuelle ni corridor vers Eutin n'est ajouté.

## Démographie

La valeur AGGSH 1819 de 2 356 habitants pour Kaltenhof et celle de Kohli, 2 270, concernent un Amt postérieur incluant des différences de périmètre. L'estimation Hennings vers 1769 de 4 072 concerne Kaltenhof **et** Großvogtei réunis. Aucune de ces valeurs n'est appliquée comme recensement des quatre cellules nouvelles. La redistribution technique de 1 606 habitants est provisoire et ne prétend pas résoudre cette démographie historique.
