# Pièces et décisions — Frise orientale, 1776

## Sources employées

1. [GStA PK, Fürstentum Ostfriesland](https://archivdatenbank.gsta.spk-berlin.de/midosasearch-gsta/MidosaSEARCH/i_ha_gr_rep_68/xml/inhalt/26660658-9b9a-407e-afde-5d107466323a.htm). Administration prussienne, 1744–1806. Source de souveraineté ; ce fonds n'est pas en lui-même un polygone géoréférencé.
2. [Ostfriesische Landschaft, Preußen](https://bibliothek.ostfriesischelandschaft.de/cirksena/preussen-ua/). Confirmation institutionnelle de la succession de 1744 et de la période prussienne.
3. Carte Schenk de Westphalie, conservée dans MAP2L/RHINE_WESTPHALIA/SCHENK_WESTPHALIA_1710_FULL.jpg. Le recadrage SCHENK_NORTH_READING.png expose les ensembles territoriaux : Frise orientale, Jever, Oldenburg et Niederstift. Carte antérieure à l'accession prussienne : utilisée pour distinguer les juridictions, **pas** pour attribuer son titre de 1710 au souverain de 1776. Pas de précision cadastrale déduite de sa coloration.
4. [Schlossmuseum Jever, cartes et plans](https://www.schlossmuseum.de/sammlungen/virtuelle-sammlungen/regionalgeschichte/landkarten-und-plaene/). Description d'une limite Wittmund–Jever levée en 1745, copie de 1746 (Ka 226), et des conventions littorales de 1666 et 1727. Elles interdisent d'assimiler Jever à la Frise prussienne. Leur description n'a pas servi de faux calage métrique : le levé n'est pas intégré au bitmap dans cette passe.
5. [Landesbibliothek Oldenburg, Güssefeld, 1790, ALBERS 072](https://digital.lb-oldenburg.de/lbolmap/content/titleinfo/1218241). Catalogue et manifeste consultés : méridien de Ferro, statistiques de 1780, source postérieure. Les téléchargements d'image ont échoué côté serveur ; **aucune frontière n'a été tracée à partir d'une image non inspectée**. Ne pas importer une acquisition postérieure à 1776 depuis ce document.
6. [NLA, archives de Jever](https://www.arcinsys.niedersachsen.de/arcinsys/showFondsDetails?fondsId=2640) et [IEG, histoire d'Oldenburg](https://www.hgisg-ekompendium.ieg-mainz.de/Dokumentation_Datensaetze/Multimedia/Staaten/Oldenburg.php). Sources de contrôle des voisins ; détails dans JEVER_VAREL_KNIPHAUSEN_AUDIT.md.

## Arbitrage appliqué

**A — Souveraineté établie :** les possessions du Fürstentum Ostfriesland relèvent de la Prusse en 1776. Emden, Aurich, Norden, Leer, Esens et Wittmund ne sont pas, de ce seul fait, autant de points pixel certifiés dans la carte native.

**B — Enveloppe côtière existante :** conserver xF9DCA2 comme représentation du noyau côtier permet la correction de souveraineté sans annexer les provinces orientales OLD, le territoire NET à l'ouest ou les subdivisions méridionales de Münster. Bornes : X 4251–4274, Y 743–765, 319 cellules. Ses limites restent une généralisation existante, non un nouveau tracé historique. Le hub est un contrôle technique secondaire, pas le fondement historique du transfert.

**C — Marges non résolues :** raccords méridionaux vers Leer/Rheiderland et détails Jever–Wittmund, espaces estuariens et îles. La position politique générale peut être connue alors que l'attribution des cellules ne l'est pas. Aucune modification des voisins n'en découle automatiquement.

Les cours d'eau natifs examinés ne fournissent pas un réseau local assez détaillé pour identifier l'Ems, la Leda et le Dollard avec une erreur locale certifiée. Aucune erreur subpixel ou précision locale de deux pixels n'est annoncée. Les îles absentes ou fusionnées dans le littoral natif ne sont ni inventées ni considérées comme reconstruites.
