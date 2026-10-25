# Sources et arbitrages R2-B

Référence : **1er janvier 1776**. Ce complément utilise les recherches R1/R2-A, puis ajoute les preuves manquantes ciblées. Il ne reprend pas une recherche générale sur l’Allemagne. Les polygones sont des intérieurs de juridictions, pas les emprises de communes modernes.

## Nassau-Sarrebruck — institution A, géométrie B

Le [Stadtarchiv Saarbrücken, fonds NSU](https://scopearchiv.saarbruecken.de/detail.aspx?ID=85) décrit un territoire immédiat avec résidence à Sarrebruck, distinct des municipalités de Sarrebruck et Saint-Jean et de leurs institutions. Les [historiques municipaux](https://www.saarbruecken.de/kultur/stadtgeschichte/700_jahre_saarbruecker_freiheit/freiheitsbrief_und_historie/wie_geht_es_mit_saarbruecken_und_stjohann_weiter) distinguent Wilhelm Heinrich puis Ludwig, régnant depuis 1768. La [Hessische Biografie, Ludwig](https://www.lagis-hessen.de/pnd/12862910X), identifiant d’autorité `12862910X`, donne le 3 janvier 1745. Son successeur Heinrich Ludwig, né en 1768, n’est pas le souverain en 1776. Les dates de fin de règne divergent dans les notices municipales ; cela ne modifie pas le souverain de la date de départ.

Le partage avec Usingen et les possessions de rive droite étaient déjà établis en R2-A : [Stadtlexikon Wiesbaden](https://www.wiesbaden.de/en/microsite/stadtlexikon/import/a-z/wiesbaden-unter-nassauischer-herrschaft). La parenté ne vaut ni fusion ni sujétion. Aucun lien natif avec NAS, les Provinces-Unies, la France ou l’empereur n’est ajouté.

Nouvelle carte : **Die Grafschaft Saarbrücken und ihre Nachbargebiete im Jahre 1789**, F. Wirtz, Darmstadt, **1909**, d’après W. Fabricius, atlas historique de la province rhénane, cartes VI/VII. BnF, Cartes et plans, **GE D-27288**, échelle 1:160 000, [notice BnF](https://catalogue.bnf.fr/ark:/12148/cb40574057q), [Gallica](https://gallica.bnf.fr/ark:/12148/btv1b53079451h). Le fac-similé téléchargé est le [fichier de consultation Wikimedia issu de Gallica](https://commons.wikimedia.org/wiki/File:Die_Grafschaft_Saarbr%C3%BCcken_und_ihre_Nachbargebiete_im_Jahre_1789_-_mit_Erlaubnis_der_Gesellschaft_f%C3%BCr_Rheinische_Geschichtskunde_nach_Karte_VI_u._VII_des_geschichtlichen_Atlas_d._Rheinprovinz_von_Dr._W._Fabricius_-_btv1b53079451h.jpg), 5400 × 4386, conservé dans `EVIDENCE/Saarbruecken_1789_Fabricius_1909.jpg`. Carte ancienne reproduite, domaine public selon la notice du dépôt ; attribution conservée ici.

**1789 n’est pas 1776.** Le tracé ne retient qu’un intérieur Sarrebruck/Saint-Jean–Ottweiler, dont la continuité dynastique est établie. Les franges de Warndt, bandes d’échanges avec la France signalées sur la carte, seigneuries chevaleresques, possessions de Trèves, territoire de Blieskastel, Saint-Ingbert, Pfalz-Zweibrücken et droits de Sarrewerden ne sont pas absorbés. Un filtre de couleur jaune ne suffirait pas : les enveloppes choisies excluent les petites seigneuries jaunes et un filtrage renforcé a retiré deux cellules candidates dont le remplissage était ambigu. Voir `SAAR_ACCEPTED_REVIEW.png`, empreintes de cellules **effectivement** retenues sur la carte, non seulement l’enveloppe de travail. Quelques bords de cellules débordent nécessairement de contours fins : généralisation B, pas cadastre.

Le gouvernement NSB est explicitement princier. Le vanilla canonique `common/government_types/01_monarchies.txt:2977` réserve ses gouvernements princiers génériques hors Europe, tandis que ses gouvernements européens de rang `principality` peuvent donner le titre de duc. Un type propre, borné à NSB et à la monarchie, évite ce défaut sans retoucher les gouvernements existants de R2-A. Armes nassoviennes simplifiées réutilisées : pas un pavillon complet certifié.

## Possessions de Nassau de rive droite — B

Carte **Friedrich Uhlhorn, Hessen 1789**, 1962, atlas historique de la Hesse, carte 22, conservée depuis R1 dans `../EVIDENCE/Hessen_1789_Uhlhorn.jpg` ; [HIL/LAGIS, notice permanente 40](https://lagis.hessen.de/resolve/de/ga/40). Licence **CC BY-SA 4.0** : les recadrages et annotations de cette carte sont des adaptations de cette source, sous la même licence. La date et la séparation des souverainetés sont confrontées aux fonds et biographies déjà recensés dans `../R2/HISTORICAL_EVIDENCE_R2.md`.

- **Diez–Hadamar–Ellar : NOU**. [HHStAW, fonds 171](https://arcinsys.hessen.de/arcinsys/showFondsDetails.action?fondsId=2005) et [172](https://arcinsys.hessen.de/arcinsys/showFondsDetails?fondsId=3508) : gouvernement allemand commun, pas autant de pays que d’anciennes branches éteintes. Huit cellules NAS vers NOU, sans retoucher Siegen–Dillenburg.
- **Merenberg–Löhnberg : NWB**. Le [fonds 163, HHStAW](https://arcinsys.hessen.de/arcinsys/showFondsDetails.action?fondsId=1992) précise l’acquisition par Weilbourg d’un quart en 1536, des trois quarts restants en **1773**, puis la réunion administrative de **1774** avec Weilbourg, Weilmünster et Merenberg. Cette preuve résout l’ancienne réserve institutionnelle, sans garantir chaque limite parcellaire. Deux cellules ajoutées ; le noyau R2-A n’est pas déplacé.
- **Usingen-centre et Wiesbaden : NAS**. Le Stadtlexikon de Wiesbaden recoupe l’attribution issue du partage de 1735. Cinq cellules HES et six FRM, sans absorber la ville libre de Francfort, Solms, Hombourg ou les possessions de Mayence. Les secteurs d’Idstein de R2-A restent intacts.

Toujours exclus : ville et condominium de Nassau avant l’échange de **1781**, partage fin du Vierherrisches de **1775**, acquisition de Burgschwalbach de **1777**, Sayn-Hachenburg en **1799**, compensations de **1803**, ainsi que les zones rayées de juridictions partagées. Les résidus NAS ne sont pas déclarés tous historiquement « Usingen ».

## Fulda — B

La carte Uhlhorn distingue le noyau territorial de Fulda, Geisa/Rasdorf, le secteur de Dermbach et la petite enclave d’Herbstein. Le [Landesgeschichtliches Informationssystem Hessen, Burg Herbstein](https://lagis.hessen.de/de/orte/burgen-schloesser-herrenhaeuser/alle-eintraege/14639_burg-herbstein) établit la possession fuldienne jusqu’en 1802. La [commune de Dermbach, château](https://www.dermbach.de/kultur-freizeit/schloss-dermbach) documente le siège fuldien de Fischberg–Dermbach depuis le début du XVIIIe siècle ; son rattachement ultérieur à Saxe-Weimar-Eisenach n’est pas projeté en 1776. Les sources de Fulda/Geisa déjà conservées en R1 restent les références complémentaires.

Six cellules intérieures Geisa–Rasdorf et deux Dermbach, prélevées sur le résidu MEI, plus **une cellule d’Herbstein**, prélevée sur HEK. Celle-ci entre dans l’enveloppe tracée : aucune croissance artificielle pour faire exister une enclave subpixel. Les empreintes sont visibles dans `FULDA_ACCEPTED_REVIEW.png`. Les 39 cellules précédemment acceptées pour FUL restent exactes. Pas de corridor ajouté entre les noyaux ; pas de substitution de tout un RGB d’après une ville.

## Limite géographique commune

Les transformations de R1 et R2-A sont réutilisées sans modification pour la Hesse/Fulda. La nouvelle feuille de Sarrebruck est enregistrée sur six repères, dans `SAAR_SOURCE_ALIGNMENT.json`, **sur le modèle diagnostique hérité**. Ses résidus de feuille ne constituent pas une validation indépendante du bitmap natif. Aucune précision GPS de deux pixels n’est annoncée. Les enveloppes historiques, la couleur territoriale, les intérieurs prudents et le contrôle des anciennes corrections fondent la classe B autorisée, pas le seul centre d’une ville.

Erfurt–Eichsfeld demeure hors de cette passe. Aucune translation de 7,20 pixels, aucune optimisation à partir des anciens points, aucun déplacement physique de locator.

## Cas laissés C

Hesse-Hombourg, Hanau-Münzenberg, apanages/branches hessoises, Hanau-Lichtenberg et condominiums : pas d’indépendance native déduite d’une administration, d’une parenté ou d’un nom. Meisenheim 1816 n’est pas Hombourg 1776. Les sources restent dans R2-A, et les conditions de reprise figurent dans `UNRESOLVED_R2B.csv`. Ces réserves ne bloquent plus les corrections B installées.
